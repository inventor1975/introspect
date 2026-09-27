# -*- coding: utf-8 -*-
"""java2zfl — Java module of the introspect.
javalang parser; shared contract INTROSPECT-SEMANTICS.md: zero-trust F/T/Z -> REFUTED/OPEN/EARNED,
honest OPEN ("when unsure, emit OPEN — never downgrade an unverified flow to EARNED").

Slices 1-5 (2026-09-12): source->sink taint; cross-method + cross-file SUMMARIES; GUARD narrowing
(whitelist.contains(x) / x.equals/matches(..) -> x is F) + branch-join; RECEIVER-AWARE generic sinks
(execute/write/print... fire only on a confirmed receiver type); context-aware escapers.

Slice 6 (2026-09-27), after the OWASP Benchmark v1.2 run found 293 vulnerable cases judged EARNED,
every one from a place where the walk read F for "don't know". Fixed at the cause:
  * a summary keeps the return as F/Z/T per parameter plus a parameter-free BASE (a helper that reads
    the request itself is a source); it was "T or nothing", so a Z return became F;
  * a bodiless (interface/abstract) method is unknown -> Z, never an empty summary;
  * summaries are keyed by CLASS and resolved from the receiver (local type, `new C().m()`, field
    type, enclosing class); candidates that disagree -> Z. Bare-name keying let the last `doSomething`
    indexed answer for every class;
  * `new C().m(..)` is read as the call, not as `new C()`;
  * an uninitialised local is Z; switch and ?: are walked; try/catch and loops are joined, not
    overwritten in sequence; `x += y` joins; a[i] = y joins into a;
  * add/put/append on a local fold the argument into the container (was: the empty container's F);
and for precision, without giving any of that back:
  * constant conditions (int/char/String/boolean arithmetic on literals and constant locals) prune
    dead if / ?: / switch branches;
  * lists/maps created empty and used only through constant indices/keys are modelled element-wise;
  * values of numeric/boolean type are F (they cannot carry an injection);
  * escapers tag a value clean for ONE context (escapeHtml(x) assigned to bar is still T for sql);
  * a catalogue of transparent library calls (decode, substring, nextElement, getValue, ...) passes the
    receiver's and arguments' taint instead of the blanket Z."""
import sys, os, javalang
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import taintjudge
from javalang import tree as J
F, T, Z = "F", "T", "Z"
_RANK = {F: 0, Z: 1, T: 2}
_DRANK = {"EARNED": 0, "OPEN": 1, "REFUTED": 2}

SOURCE_METHODS = {"getParameter","getParameterValues","getParameterMap","getParameterNames","getQueryString",
                  "getHeader","getHeaders","getHeaderNames","getCookies","getInputStream","getReader",
                  "getRequestURI","getRequestURL","getPathInfo","getPart","getParts"}
# names shared with files, sockets and processes: a source only on a request (or an unknown) receiver
SOURCE_ON_REQUEST = {"getInputStream","getReader","getPart","getParts"}
REQUEST_TYPES = {"ServletRequest","HttpServletRequest","HttpServletRequestWrapper","ServletRequestWrapper",
                 "MultipartHttpServletRequest","StandardMultipartHttpServletRequest","WebRequest","NativeWebRequest"}
# Spring MVC parameter annotations: an annotated handler param IS user input (entry-point source)
SPRING_SOURCES = {"RequestParam","PathVariable","RequestBody","RequestHeader",
                  "CookieValue","RequestPart","MatrixVariable","ModelAttribute"}
# a @*Mapping handler auto-binds its BARE simple-type params from the request (implicit @RequestParam)
MAPPING_ANNOS = {"GetMapping","PostMapping","RequestMapping","PutMapping","DeleteMapping","PatchMapping"}
SIMPLE_TYPES = {"String","int","Integer","long","Long","short","Short","byte","Byte","boolean","Boolean",
                "char","Character","double","Double","float","Float","BigDecimal","BigInteger"}
# numeric / boolean values cannot carry an injection payload into sql, shell or html: always F.
# (char is NOT here: a single quote is one char.)
CLEAN_TYPES = {"int","long","short","byte","boolean","double","float","Integer","Long","Short","Byte",
               "Boolean","Double","Float","BigDecimal","BigInteger","AtomicInteger","AtomicLong","void"}
# constructor sinks: new ProcessBuilder(taint) is command execution (the injection is the ctor arg)
CTOR_SINKS = {"ProcessBuilder":"shell"}
# specific method names: the name alone is enough to call it a sink. (ctx, which args carry the payload)
# 'first' = the query/command text only (the rest are bind values); 'all' = any argument (a writer's
# format arguments); 'cmd' = exec's command and envp (the third, the working directory, is not a command).
SINK_HIGH = {"exec":("shell","cmd"),
             "executeQuery":("sql","first"),"executeUpdate":("sql","first"),"executeLargeUpdate":("sql","first"),
             "prepareStatement":("sql","first"),"prepareCall":("sql","first"),"addBatch":("sql","first"),
             "queryForObject":("sql","first"),"queryForList":("sql","first"),"queryForMap":("sql","first"),
             "queryForRowSet":("sql","first"),"queryForLong":("sql","first"),"queryForInt":("sql","first"),
             "queryForStream":("sql","first"),"batchUpdate":("sql","first"),
             "readObject":("deser","first")}
WRITER_TYPES = {"PrintWriter","Writer","ServletOutputStream","OutputStream","PrintStream","JspWriter"}
SQL_RECV     = {"Statement","PreparedStatement","CallableStatement","Connection",
                "JdbcTemplate","NamedParameterJdbcTemplate","JdbcOperations"}
JDBC_TPL     = {"JdbcTemplate","NamedParameterJdbcTemplate","JdbcOperations"}
# generic method names collide across libraries -> confirm by receiver type.
# name -> (ctx, confirming receiver types, open_if_unknown, which args)
SINK_RECV = {"execute": ("sql", SQL_RECV, True, "first"),
             "query":   ("sql", JDBC_TPL, False, "first"),
             "update":  ("sql", JDBC_TPL, False, "first"),
             "write":   ("xss", WRITER_TYPES, False, "all"),
             "print":   ("xss", WRITER_TYPES, False, "all"),
             "println": ("xss", WRITER_TYPES, False, "all"),
             "printf":  ("xss", WRITER_TYPES, False, "all"),
             "format":  ("xss", WRITER_TYPES, False, "all"),
             "append":  ("xss", WRITER_TYPES, False, "all"),
             "command": ("shell", {"ProcessBuilder"}, False, "all")}
# sinks whose danger depends on the deployment (does the container escape the error page?): at worst OPEN
RESPONSE_TYPES = {"HttpServletResponse","ServletResponse","HttpServletResponseWrapper"}
SINK_SOFT = {"sendError": ("xss", RESPONSE_TYPES)}
# library calls whose result type we know (receiver typing along a chain: resp.getWriter().write(..))
RETURNS = {"getWriter":"PrintWriter","getOutputStream":"ServletOutputStream","getRuntime":"Runtime",
           "getConnection":"Connection","createStatement":"Statement","prepareStatement":"PreparedStatement",
           "prepareCall":"CallableStatement","command":"ProcessBuilder","redirectErrorStream":"ProcessBuilder"}
SANITIZERS = set()
# CONTEXT-AWARE sanitizers (like php2zfl): an escaper neutralises ONE context, not all. The value it returns
# is tagged clean for that context and stays tainted for the others.
CTX_SANITIZERS = {"escapeHtml":"xss","escapeHtml4":"xss","escapeHtml3":"xss","htmlEscape":"xss",
                  "forHtml":"xss","forHtmlContent":"xss","forHtmlAttribute":"xss","encodeForHTML":"xss",
                  "encodeForHTMLAttribute":"xss","escapeXml":"xss","escapeXml10":"xss","escapeXml11":"xss",
                  "forJavaScript":"xss","encodeForJavaScript":"xss","escapeEcmaScript":"xss",
                  "encodeForSQL":"sql","encodeForOS":"shell"}
# library calls that pass taint through: result = join(receiver, arguments)
TRANSPARENT = {"substring","subSequence","trim","strip","stripLeading","stripTrailing","toLowerCase",
               "toUpperCase","concat","replace","replaceAll","replaceFirst","split","toCharArray","getBytes",
               "charAt","toString","valueOf","copyValueOf","intern","format","formatted","join","repeat",
               "append","insert","reverse","decode","encode","decodeBase64","encodeBase64","encodeBase64String",
               "encodeBase64URLSafe","encodeBase64URLSafeString","encodeToString","unescapeHtml","unescapeHtml4",
               "unescapeJava","get","getOrDefault","getValue","getKey","getName","getComment","next","nextElement",
               "nextToken","previous","iterator","listIterator","elements","keys","keySet","values","entrySet",
               "toArray","asList","of","copyOf","copyOfRange","subList","singletonList","singleton",
               "unmodifiableList","unmodifiableMap","unmodifiableSet","list","stream","collect","map","filter",
               "findFirst","orElse","orElseGet","peek","poll","pop","remove","firstElement","lastElement",
               "getFirst","getLast","elementAt","readLine","lines","requireNonNull","requireNonNullElse",
               "toPath","getPath","getAbsolutePath","getCanonicalPath","normalize","resolve","getFileName",
               "getAttribute","getInitParameter","getString"}
# results that are numbers or booleans: clean whatever went in
NUMERIC_RESULT = {"length","size","isEmpty","hashCode","equals","equalsIgnoreCase","contains","containsKey",
                  "containsValue","startsWith","endsWith","indexOf","lastIndexOf","compareTo","compareToIgnoreCase",
                  "matches","parseInt","parseLong","parseShort","parseByte","parseDouble","parseFloat",
                  "parseBoolean","hasNext","hasMoreElements","hasMoreTokens","countTokens","nextInt","nextLong",
                  "nextBoolean","nextDouble","nextFloat","intValue","longValue","doubleValue","booleanValue"}
# factories whose (argument-free) result is not data
CLEAN_FACTORY = {"getDecoder","getEncoder","getUrlDecoder","getUrlEncoder","getMimeDecoder","getMimeEncoder",
                 "getRuntime","encoder","getWriter","getOutputStream","getInstance","getLogger"}
# calls on a local that fold the argument into it (the container / builder now holds the taint)
MUTATORS = {"append","insert","add","addAll","addElement","put","putAll","push","offer","offerFirst",
            "offerLast","addFirst","addLast","set","setCharAt","putIfAbsent"}
LIST_TYPES = {"ArrayList","LinkedList","Vector","List","Stack","ArrayDeque","Deque","Queue"}
MAP_TYPES = {"HashMap","LinkedHashMap","TreeMap","Hashtable","Map","ConcurrentHashMap"}
GUARD_ARG  = {"contains","containsKey","containsValue"}   # validated var is the ARGUMENT
GUARD_RECV = {"equals","equalsIgnoreCase","matches"}      # validated var is the QUALIFIER
_NC = object()     # "not a constant"


# ---------------------------------------------------------------- taint values
# A value is a letter F/Z/T (the same in every sink context) or, after an escaper, a pair
# (default letter, ((ctx, letter), ...)) — per-context overrides.
def _parts(v):
    return (v, {}) if isinstance(v, str) else (v[0], dict(v[1]))

def _mk(default, over):
    over = {c: l for c, l in over.items() if l != default}
    return default if not over else (default, tuple(sorted(over.items())))

def _at(v, ctx):
    """The letter of v in sink context ctx."""
    if isinstance(v, str): return v
    return dict(v[1]).get(ctx, v[0])

def _pc(fn, *vs):
    """Apply a letter function context by context."""
    if all(isinstance(v, str) for v in vs): return fn(*vs)
    ctxs = set()
    for v in vs: ctxs |= set(_parts(v)[1])
    return _mk(fn(*[_parts(v)[0] for v in vs]), {c: fn(*[_at(v, c) for v in vs]) for c in ctxs})

def _lj(*ls):
    return max(ls, key=_RANK.get) if ls else F

def join(*vs):
    vs = [v for v in vs if v is not None]
    if not vs: return F
    if all(isinstance(v, str) for v in vs): return _lj(*vs)
    return _pc(lambda *ls: _lj(*ls), *vs)

def _compose(a, r):
    """Taint of a call's result from one argument: a = the argument, r = the result when that parameter is T."""
    return _pc(lambda x, y: F if x == F else (y if x == T else (Z if y != F else F)), a, r)

def _clean_for(v, ctx):
    d, over = _parts(v)
    over[ctx] = F
    return _mk(d, over)


# ---------------------------------------------------------------- AST helpers
def _is_spring_source(param):
    return any(getattr(a,'name',None) in SPRING_SOURCES for a in (getattr(param,'annotations',None) or []))

def _is_handler(meth):
    return any(getattr(a,'name',None) in MAPPING_ANNOS for a in (getattr(meth,'annotations',None) or []))

def _typename(ty):
    """Simple (last) name of a possibly-qualified/nested javalang type: java.sql.Statement -> 'Statement'."""
    if ty is None: return None
    n = getattr(ty,'name',None); sub = getattr(ty,'sub_type',None)
    while sub is not None:
        n = getattr(sub,'name',n) or n; sub = getattr(sub,'sub_type',None)
    return n

def _line(node):
    p = getattr(node, 'position', None)
    return p.line if p else None

class _Ch(str):
    """A Java char constant (compares with char literals, adds to ints by code point)."""

def _lit(node):
    v = node.value
    if not isinstance(v, str): return _NC
    try:
        if v in ("true", "false"): return v == "true"
        if v == "null": return _NC
        if v.startswith('"') and v.endswith('"') and len(v) >= 2:
            s = v[1:-1]
            return _NC if "\\" in s else s
        if v.startswith("'") and v.endswith("'") and len(v) == 3: return _Ch(v[1])
        t = v.rstrip("lL")
        if t.lower().startswith("0x"): return int(t, 16)
        if t.isdigit(): return int(t, 8) if (len(t) > 1 and t.startswith("0")) else int(t)
    except ValueError:
        pass
    return _NC

def _num(x):
    if isinstance(x, _Ch): return ord(x)
    if isinstance(x, bool): return _NC
    return x if isinstance(x, int) else _NC

def _jstr(x):
    if isinstance(x, bool): return "true" if x else "false"
    return str(x)

def _binop(op, a, b):
    if op == "+" and (isinstance(a, str) and not isinstance(a, _Ch) or isinstance(b, str) and not isinstance(b, _Ch)):
        return _jstr(a) + _jstr(b)
    if op in ("&&", "||", "&", "|", "^") and isinstance(a, bool) and isinstance(b, bool):
        return {"&&": a and b, "||": a or b, "&": a and b, "|": a or b, "^": a != b}[op]
    if op in ("==", "!="):
        if isinstance(a, bool) or isinstance(b, bool):
            if not (isinstance(a, bool) and isinstance(b, bool)): return _NC
            return (a == b) == (op == "==")
        x, y = _num(a), _num(b)
        if x is _NC or y is _NC: return _NC          # String == compares references: not decidable here
        return (x == y) == (op == "==")
    x, y = _num(a), _num(b)
    if x is _NC or y is _NC: return _NC
    if op == "+": return x + y
    if op == "-": return x - y
    if op == "*": return x * y
    if op in ("/", "%"):
        if y == 0: return _NC
        q = abs(x) // abs(y) * (1 if (x >= 0) == (y >= 0) else -1)
        return q if op == "/" else x - q * y
    if op == "<": return x < y
    if op == ">": return x > y
    if op == "<=": return x <= y
    if op == ">=": return x >= y
    return _NC

def _jumps(stmts):
    """How a statement list ends: 'term' (return/throw/continue), 'break', or None (falls through)."""
    if not stmts: return None
    st = stmts[-1]
    if isinstance(st, (J.ReturnStatement, J.ThrowStatement, J.ContinueStatement)): return "term"
    if isinstance(st, J.BreakStatement): return "break"
    if isinstance(st, J.BlockStatement): return _jumps(st.statements)
    return None

def _ejoin(*envs):
    """Join of environments. Taint keys join; constant (#c:) and container-model (#l:/#m:) keys survive
    only if every environment agrees."""
    out = {}
    keys = set()
    for e in envs: keys |= set(e)
    for k in keys:
        if k.startswith("#"):
            vs = [e.get(k, _NC) for e in envs]
            if all(v is not _NC and v == vs[0] for v in vs): out[k] = vs[0]
        else:
            out[k] = join(*[e[k] for e in envs if k in e])
    return out

def _set_env(env, new):
    env.clear(); env.update(new)


class Engine:
    def __init__(self):
        self.summaries = {}   # id(MethodDeclaration) -> summary (see _summ_of)
        self.sinks = []
        self.vt = {}          # per-method: var name -> simple type name (receiver-aware sinks)
        self.classes = {}     # qname -> {"simple","outer","supers","ftypes","consts"}
        self.by_simple = {}   # simple class name -> [qname]
        self.meths = {}       # (qname, method name) -> [MethodDeclaration]
        self.by_name = {}     # method name -> [(qname, MethodDeclaration)]
        self.owner = {}       # id(MethodDeclaration) -> qname
        self.decls = []       # every indexed MethodDeclaration
        self.cur = None       # qname of the class being walked
        self.alloc = {}       # per-method: local -> exact class it was allocated as
        self._rets = None     # collecting return values (summary walk)
        self._dirty = False
        self._fam = {}
        self._esc = []        # stack (one per enclosing loop/switch) of environments leaving by break/continue

    # ---------------------------------------------------------------- the class index
    def _register(self, tree):
        pkg = tree.package.name if getattr(tree, 'package', None) else ""
        def walk_type(td, outer):
            qn = (outer + "." if outer else (pkg + "." if pkg else "")) + td.name
            supers = []
            ext = getattr(td, 'extends', None)
            for s in (ext if isinstance(ext, list) else [ext] if ext else []): supers.append(_typename(s))
            for s in (getattr(td, 'implements', None) or []): supers.append(_typename(s))
            info = {"simple": td.name, "outer": outer, "supers": [s for s in supers if s],
                    "ftypes": {}, "consts": {}}
            self.classes[qn] = info
            self.by_simple.setdefault(td.name, [])
            if qn not in self.by_simple[td.name]: self.by_simple[td.name].append(qn)
            for m in (td.body or []):
                if isinstance(m, J.FieldDeclaration):
                    for d in m.declarators:
                        info["ftypes"][d.name] = _typename(m.type)
                        if "final" in (m.modifiers or set()) and isinstance(d.initializer, J.Literal):
                            info["consts"][d.name] = _lit(d.initializer)
                elif isinstance(m, (J.MethodDeclaration, J.ConstructorDeclaration)):
                    self.owner[id(m)] = qn
                    if isinstance(m, J.MethodDeclaration):
                        self.meths.setdefault((qn, m.name), []).append(m)
                        self.by_name.setdefault(m.name, []).append((qn, m))
                        self.decls.append(m)
                elif isinstance(m, (J.ClassDeclaration, J.InterfaceDeclaration, J.EnumDeclaration)):
                    walk_type(m, qn)
        for td in (tree.types or []):
            if isinstance(td, (J.ClassDeclaration, J.InterfaceDeclaration, J.EnumDeclaration)):
                walk_type(td, None)
        # anonymous classes `new I() { .. }`: an implementation of I, under a synthetic name
        for n_, (path, cc) in enumerate(tree.filter(J.ClassCreator)):
            if getattr(cc, 'body', None) is None: continue
            tn = _typename(cc.type)
            names = [p.name for p in path if isinstance(p, (J.ClassDeclaration, J.InterfaceDeclaration, J.EnumDeclaration))]
            qn = (pkg + "." if pkg else "") + ".".join(names + [f"$anon{n_}"])
            self.classes[qn] = {"simple": f"$anon{n_}", "outer": None, "supers": [tn] if tn else [],
                                "ftypes": {}, "consts": {}}
            for m in cc.body:
                if isinstance(m, J.MethodDeclaration):
                    self.owner[id(m)] = qn
                    self.meths.setdefault((qn, m.name), []).append(m)
                    self.by_name.setdefault(m.name, []).append((qn, m))
                    self.decls.append(m)
        # methods of local classes: owned by the nearest named class, found by name only
        for path, m in tree.filter(J.MethodDeclaration):
            if id(m) not in self.owner:
                names = [p.name for p in path if isinstance(p, (J.ClassDeclaration, J.InterfaceDeclaration, J.EnumDeclaration))]
                self.owner[id(m)] = (pkg + "." if pkg else "") + ".".join(names) if names else None

    def _class_of(self, simple, ctx=None):
        """qnames a simple class name may denote, seen from class ctx: nested in ctx or its outers first."""
        if not simple: return []
        c = ctx
        while c:
            if c + "." + simple in self.classes: return [c + "." + simple]
            c = self.classes.get(c, {}).get("outer")
        return list(self.by_simple.get(simple, []))

    def _family(self, qnames):
        """The classes whose methods may answer a call on a receiver of these classes: the class, its
        supertypes (inherited), its subtypes (overrides / interface implementations)."""
        key = tuple(qnames)
        if key in self._fam: return self._fam[key]
        out, todo = [], list(qnames)
        while todo:                                                    # up
            q = todo.pop()
            if q in out or q not in self.classes: continue
            out.append(q)
            for s in self.classes[q]["supers"]: todo += self._class_of(s, q)
        simples = {self.classes[q]["simple"] for q in out}
        grew = True
        while grew:                                                    # down
            grew = False
            for q, info in self.classes.items():
                if q not in out and simples & set(info["supers"]):
                    out.append(q); simples.add(info["simple"]); grew = True
        self._fam[key] = out
        return out

    def _cands(self, name, nargs, recv):
        """User-code candidates for a call. recv: ('cls', [qnames]) | ('self',) | ('any',) | ('lib',).
        Returns None for a library call (no user method can answer), else a list of MethodDeclarations
        (possibly bodiless)."""
        if recv[0] == "lib": return None
        found = []
        if recv[0] == "cls":
            for q in self._family(recv[1]): found += self.meths.get((q, name), [])
        elif recv[0] == "exact":                                   # the class and what it inherits, nearest first
            todo, seen = list(recv[1]), set()
            while todo and not any(m.body is not None for m in found):
                q = todo.pop(0)
                if q in seen or q not in self.classes: continue
                seen.add(q)
                found += [m for m in self.meths.get((q, name), []) if len(m.parameters or []) == nargs] \
                    or self.meths.get((q, name), [])
                for s_ in self.classes[q]["supers"]: todo += self._class_of(s_, q)
            if not found: return []
        elif recv[0] == "self":
            c = self.cur
            while c and not found:
                for q in self._family([c]): found += self.meths.get((q, name), [])
                c = self.classes.get(c, {}).get("outer")
        if not found and recv[0] in ("self", "any"):
            found = [m for _q, m in self.by_name.get(name, [])]
        if not found: return None if recv[0] != "cls" else []
        fit = [m for m in found if len(m.parameters or []) == nargs] or found
        # an abstract/interface declaration does not vote when implementations are in view (anonymous
        # `new I(){..}` classes are registered as implementations, so none is silently left out)
        bodied = [m for m in fit if m.body is not None]
        return bodied or fit

    def _user_type(self, tname):
        return self._class_of(tname, self.cur) if tname else []

    # ---------------------------------------------------------------- summaries
    def index(self, tree):
        self._register(tree)
        self._dirty = True
        self._fam = {}

    def _summarize_all(self):
        """Summaries to a fixpoint (a caller summarised before its callee reads the callee's summary on the
        next pass). Pass 1 reads every not-yet-summarised user call as Z."""
        for _ in range(4):
            before = dict(self.summaries)
            for m in self.decls: self.summaries[id(m)] = self._summ_of(m)
            if self.summaries == before: break
        self._dirty = False

    def _summ_of(self, meth):
        params = [p.name for p in (meth.parameters or [])]
        if meth.body is None:
            return {"body": False, "base": Z, "ret": [Z] * len(params), "sinks": {}}
        clean_ret = _typename(meth.return_type) in CLEAN_TYPES if meth.return_type is not None else True
        saved = (self.sinks, self.vt, self.cur, self._rets, self.alloc)
        self.cur = self.owner.get(id(meth))
        self.vt = self._types_of(meth)
        def run(env):
            self.sinks, self._rets = [], []
            self._walk(meth.body, env)
            ret = F if clean_ret else join(*self._rets)
            got = {}
            for (_l, nm, ctx, d) in self.sinks:
                k = (_l, nm, ctx)
                if _DRANK[d] > _DRANK.get(got.get(k), -1): got[k] = d
            return ret, got
        try:
            base_env = {p.name: F for p in (meth.parameters or [])}
            base, bsinks = run(dict(base_env))
            summ = {"body": True, "base": base, "ret": [], "sinks": {}}
            for i, p in enumerate(meth.parameters or []):
                env = dict(base_env)
                env[p.name] = F if _typename(p.type) in CLEAN_TYPES else T
                r, psinks = run(env)
                summ["ret"].append(r)
                eff = {}
                for k, d in psinks.items():
                    if _DRANK[d] > _DRANK.get(bsinks.get(k), 0):
                        ctx = k[2]
                        if _DRANK[d] > _DRANK.get(eff.get(ctx), -1): eff[ctx] = d
                if eff: summ["sinks"][i] = eff
            return summ
        finally:
            self.sinks, self.vt, self.cur, self._rets, self.alloc = saved

    def _types_of(self, meth):
        """Var -> simple type name for one method: params, locals, for-each vars, resources, catch params.
        Also self.alloc: locals initialised by `new C(..)` and never reassigned -> their exact class C."""
        vt = {}
        self.alloc = {}
        for p in (meth.parameters or []): vt[p.name] = _typename(p.type)
        if meth.body is None: return vt
        for st in meth.body:
            for _, d in st.filter(J.VariableDeclaration):
                for x in d.declarators: vt[x.name] = _typename(d.type)
            for _, r in st.filter(J.TryResource): vt[r.name] = _typename(r.type)
        reassigned = set()
        for st in meth.body:
            for _, d in st.filter(J.VariableDeclaration):
                for x in d.declarators:
                    if isinstance(x.initializer, J.ClassCreator) and getattr(x.initializer, 'body', None) is None \
                            and not x.initializer.selectors:
                        if x.name in self.alloc: reassigned.add(x.name)
                        self.alloc[x.name] = _typename(x.initializer.type)
            for _, a in st.filter(J.Assignment):
                l = a.expressionl
                if isinstance(l, J.MemberReference) and not l.qualifier: reassigned.add(l.member)
        for n in reassigned: self.alloc.pop(n, None)
        return vt

    def _apply(self, cands, argvals):
        """Value of a user call from its candidates' summaries; candidates that disagree -> Z."""
        results = []
        for m in cands:
            s = self.summaries.get(id(m))
            if s is None or not s["body"]:
                results.append(Z); continue
            v = s["base"]
            n = len(s["ret"])
            for i, a in enumerate(argvals):
                if n: v = join(v, _compose(a, s["ret"][min(i, n - 1)]))
            results.append(v)
        if not results: return Z
        return results[0] if all(r == results[0] for r in results) else Z

    def _summary_sinks(self, inv, cands, argvals):
        """A tainted argument reaching a sink inside the callee is reported at the call."""
        per = {}                                   # ctx -> [letter per candidate]
        known = [self.summaries.get(id(m)) for m in cands]
        known = [s for s in known if s is not None and s["body"]]
        for s in known:
            for i, eff in s["sinks"].items():
                for ctx, d in eff.items(): per.setdefault(ctx, [])
        for ctx in per:
            for s in known:
                worst = F
                for i, eff in s["sinks"].items():
                    if ctx not in eff: continue
                    for j, a in enumerate(argvals):
                        if j != i and not (j > i and i == len(s["ret"]) - 1): continue
                        x = _at(a, ctx)
                        l = F if x == F else (Z if x == Z or eff[ctx] != "REFUTED" else T)
                        worst = _lj(worst, l)
                per[ctx].append(worst)
            ls = per[ctx]
            eff_l = T if all(l == T for l in ls) else (Z if any(l != F for l in ls) else F)
            self._judge(inv, inv.member + "()->sink", ctx, eff_l, fallback_line=self._stline)

    # ---------------------------------------------------------------- constants
    def _const(self, node, env):
        if node is None: return _NC
        v = self._const0(node, env)
        if v is _NC: return v
        for op in (getattr(node, 'prefix_operators', None) or []):
            if op == "-":
                n = _num(v); v = -n if n is not _NC else _NC
            elif op == "!": v = (not v) if isinstance(v, bool) else _NC
            elif op == "+": v = _num(v)
            else: v = _NC
            if v is _NC: return v
        return v

    def _const0(self, node, env):
        if isinstance(node, J.Literal):
            return _lit(node) if not node.selectors else _NC
        if isinstance(node, J.MemberReference) and not node.selectors:
            if not node.qualifier:
                k = "#c:" + node.member
                if k in env: return env[k]
                if node.member in env: return _NC
                return self.classes.get(self.cur, {}).get("consts", {}).get(node.member, _NC)
            for q in self._class_of(node.qualifier.split(".")[-1], self.cur):
                c = self.classes[q]["consts"].get(node.member, _NC)
                if c is not _NC: return c
            return _NC
        if isinstance(node, J.BinaryOperation):
            a = self._const(node.operandl, env)
            if a is _NC: return _NC
            if node.operator == "&&" and a is False: return False
            if node.operator == "||" and a is True: return True
            b = self._const(node.operandr, env)
            return _NC if b is _NC else _binop(node.operator, a, b)
        if isinstance(node, J.TernaryExpression):
            c = self._const(node.condition, env)
            if c is True: return self._const(node.if_true, env)
            if c is False: return self._const(node.if_false, env)
            return _NC
        if isinstance(node, J.Cast): return self._const(node.expression, env)
        if isinstance(node, J.MethodInvocation) and node.qualifier and not node.selectors \
                and "." not in node.qualifier:
            s = env.get("#c:" + node.qualifier, _NC)
            if not isinstance(s, str) or isinstance(s, _Ch): return _NC
            args = [self._const(a, env) for a in (node.arguments or [])]
            if any(a is _NC for a in args): return _NC
            try:
                if node.member == "charAt" and len(args) == 1 and isinstance(args[0], int):
                    return _Ch(s[args[0]]) if 0 <= args[0] < len(s) else _NC
                if node.member == "length" and not args: return len(s)
                if node.member in ("equals",) and len(args) == 1 and isinstance(args[0], str):
                    return s == args[0]
            except (IndexError, TypeError):
                return _NC
        return _NC

    # ---------------------------------------------------------------- the evaluator
    def taint(self, node, env):
        """Value of an expression. Evaluating has the program's effects: assignments update env,
        mutators fold into their container, sinks reached on the way are judged."""
        return self._ev(node, env)[0]

    def _ev(self, node, env):
        """-> (value, simple type name of the result or None)."""
        if node is None: return F, None
        v, ty = self._ev0(node, env)
        pre = getattr(node, 'prefix_operators', None) or []
        post = getattr(node, 'postfix_operators', None) or []
        if any(op in ("!", "-", "~", "++", "--") for op in pre) or any(op in ("++", "--") for op in post):
            return F, None                             # a number or a boolean
        return v, ty

    def _ev0(self, node, env):
        if isinstance(node, J.Literal): return self._chain(F, None, node.selectors, env, node)
        if isinstance(node, (J.ClassReference, J.VoidClassReference)): return F, None
        if isinstance(node, J.MemberReference): return self._memberref(node, env)
        if isinstance(node, J.Assignment): return self._assign(node, env), None
        if isinstance(node, J.BinaryOperation):
            l = self.taint(node.operandl, env)
            if node.operator == "instanceof": return F, None
            r = self.taint(node.operandr, env)
            return (join(l, r), None) if node.operator == "+" else (F, None)
        if isinstance(node, J.TernaryExpression):
            self.taint(node.condition, env)
            c = self._const(node.condition, env)
            if c is True: return self._ev(node.if_true, env)
            if c is False: return self._ev(node.if_false, env)
            return join(self.taint(node.if_true, env), self.taint(node.if_false, env)), None
        if isinstance(node, J.Cast):
            v, _ = self._ev(node.expression, env)
            ty = _typename(node.type)
            return (F if ty in CLEAN_TYPES else v), ty
        if isinstance(node, J.ArrayCreator):
            ini = getattr(node, 'initializer', None)
            for d in (node.dimensions or []): self.taint(d, env)
            v = self.taint(ini, env) if ini else F
            return self._chain(v, None, node.selectors, env, node)
        if isinstance(node, J.ArrayInitializer):
            return join(*[self.taint(e, env) for e in (node.initializers or [])]), None
        if isinstance(node, J.ClassCreator): return self._creator(node, env)
        if isinstance(node, J.MethodInvocation): return self._invocation(node, env)
        if isinstance(node, J.SuperMethodInvocation):
            args = [self.taint(a, env) for a in (node.arguments or [])]
            outer = self.classes.get(self.cur, {})
            supers = [q for s in outer.get("supers", []) for q in self._class_of(s, self.cur)]
            v, ty = self._call(node, node.member, args, F, ("cls", supers) if supers else ("lib",), None)
            return self._chain(v, ty, node.selectors, env, node)
        if isinstance(node, J.This):
            return self._chain(F, ("self",), node.selectors, env, node)
        if isinstance(node, J.LambdaExpression):
            e = dict(env)
            for p in (node.parameters or []):
                nm = getattr(p, 'name', None) or getattr(p, 'member', None)
                if nm: e[nm] = Z
            if isinstance(node.body, list): self._walk(node.body, e)
            else: self.taint(node.body, e)
            return F, None
        if isinstance(node, J.MethodReference): return Z, None
        if isinstance(node, (J.ExplicitConstructorInvocation, J.SuperConstructorInvocation)):
            for a in (node.arguments or []): self.taint(a, env)
            return F, None
        return Z, None

    def _memberref(self, node, env):
        q = node.qualifier
        if not q:
            name = node.member
            if name in env:
                v = env[name]
                if "#l:" + name in env or "#m:" + name in env:        # the container escapes the model
                    env.pop("#l:" + name, None); env.pop("#m:" + name, None)
            else:
                c = self.classes.get(self.cur, {}).get("consts", {}).get(name, _NC)
                v = F if c is not _NC else Z
            return self._chain(v, self.vt.get(name) or self.classes.get(self.cur, {}).get("ftypes", {}).get(name),
                               node.selectors, env, node)
        first = q.split(".")[0]
        if first in env:
            v = F if node.member == "length" else env[first]
            return self._chain(v, None, node.selectors, env, node)
        last = q.split(".")[-1]
        for cq in self._class_of(last, self.cur):
            info = self.classes[cq]
            if node.member in info["consts"]:
                return self._chain(F, None, node.selectors, env, node)
            if node.member in info["ftypes"]:
                return self._chain(Z, info["ftypes"][node.member], node.selectors, env, node)
        # a LIBRARY class's UPPER_CASE constant (Locale.US, StandardCharsets.UTF_8): not request data
        if last[:1].isupper() and not self._class_of(last, self.cur) and node.member.isupper():
            return self._chain(F, None, node.selectors, env, node)
        return self._chain(Z, None, node.selectors, env, node)

    def _assign(self, node, env):
        lhs = node.expressionl
        v = self.taint(node.value, env)
        if isinstance(lhs, J.MemberReference) and not lhs.qualifier:
            name = lhs.member
            if self.vt.get(name) in CLEAN_TYPES: v = F
            if lhs.selectors:                                     # a[i] = v: the array now holds v too
                env[name] = join(env.get(name, Z), v)
            elif node.type != "=":                                # x += v
                env[name] = join(env.get(name, Z), v)
                env.pop("#c:" + name, None)
            else:
                env[name] = v
                c = self._const(node.value, env)
                if c is _NC: env.pop("#c:" + name, None)
                else: env["#c:" + name] = c
                self._model_init(name, node.value, env)
        elif isinstance(lhs, J.MemberReference):
            first = lhs.qualifier.split(".")[0]
            if first in env: env[first] = join(env[first], v)     # o.f = v: the object now holds v
        return v

    def _model_init(self, name, init, env):
        env.pop("#l:" + name, None); env.pop("#m:" + name, None)
        if isinstance(init, J.ClassCreator) and not init.arguments and not init.selectors \
                and getattr(init, 'body', None) is None:
            tn = _typename(init.type)
            if tn in LIST_TYPES: env["#l:" + name] = ()
            elif tn in MAP_TYPES: env["#m:" + name] = ()

    def _creator(self, node, env):
        args = [self.taint(a, env) for a in (node.arguments or [])]
        tn = _typename(node.type)
        ctx = CTOR_SINKS.get(tn)
        if ctx and args:
            self._judge(node, "new " + tn, ctx, join(*args), fallback_line=self._stline)
        v = join(*args) if args else F
        if tn in CLEAN_TYPES: v = F
        return self._chain(v, tn, node.selectors, env, node)

    def _recv_of_type(self, tn):
        u = self._user_type(tn)
        return ("cls", u) if u else ("lib",)

    def _invocation(self, node, env):
        q = node.qualifier
        args = [self.taint(a, env) for a in (node.arguments or [])]
        rtype = None
        if not q:
            recv_val, recv = F, ("self",)
        else:
            parts = q.split(".")
            if parts[0] in env:
                recv_val = env[parts[0]]
                rtype = self.vt.get(parts[0]) if len(parts) == 1 else None
                recv = self._recv_of_type(rtype) if rtype else ("any",)
                exact = self._user_type(self.alloc.get(parts[0])) if len(parts) == 1 else []
                if exact: recv = ("exact", exact)
                if len(parts) == 1:
                    self._mutate(parts[0], node, args, env)
                    # an unknown call may store its argument in the receiver (props.load(in); props.get(k)):
                    # fold, unless the call is known to be pure
                    if node.member not in MUTATORS and node.member not in NUMERIC_RESULT \
                            and node.member not in TRANSPARENT and node.member not in SOURCE_METHODS \
                            and any(x != F for x in args):
                        env[parts[0]] = join(env[parts[0]], *args)
            elif len(parts) == 1 and parts[0] in self.classes.get(self.cur, {}).get("ftypes", {}):
                rtype = self.classes[self.cur]["ftypes"][parts[0]]
                recv_val, recv = Z, self._recv_of_type(rtype)
            else:
                last = parts[-1]
                ucls = self._class_of(last, self.cur)
                if ucls:
                    recv_val, recv = F, ("cls", ucls)             # a static call on a user class
                elif len(parts) >= 2 and self._class_of(parts[-2], self.cur):
                    ftypes = {}
                    for cq in self._class_of(parts[-2], self.cur): ftypes.update(self.classes[cq]["ftypes"])
                    rtype = ftypes.get(last)
                    recv_val = Z
                    recv = self._recv_of_type(rtype) if rtype else ("any",)
                elif last[:1].isupper() or len(parts) > 1:
                    recv_val, recv = F, ("lib",)                  # a library class (or package path)
                else:
                    recv_val, recv = Z, ("any",)                  # an unknown field
        self._sink(node, node.member, args, rtype, q)
        v, ty = self._call(node, node.member, args, recv_val, recv, rtype)
        if q and "." not in q and q in env:
            m = self._model_get(q, node, env)
            if m is not None: v = m
        v, ty = self._chain(v, ty, node.selectors, env, node)
        if q and "." not in q and q in env and node.member in ("append", "insert") and node.selectors:
            env[q] = join(env[q], v)                              # sb.append(a).append(b): sb holds b too
        return v, ty

    def _chain(self, v, ty, selectors, env, node):
        """Apply selectors left to right. ty: the receiver's simple type name, or ('self',) for this."""
        for sel in (selectors or []):
            if isinstance(sel, J.ArraySelector):
                self.taint(sel.index, env); ty = None
            elif isinstance(sel, J.MemberReference):
                v = F if sel.member == "length" else v
                ty = None
            elif isinstance(sel, J.MethodInvocation):
                args = [self.taint(a, env) for a in (sel.arguments or [])]
                if ty == ("self",): recv, rt = ("self",), None
                else:
                    rt = ty
                    recv = self._recv_of_type(ty) if ty else ("any",)
                self._sink(sel, sel.member, args, rt, None)
                v, ty = self._call(sel, sel.member, args, v, recv, rt)
                if sel.selectors: v, ty = self._chain(v, ty, sel.selectors, env, sel)
            else:
                ty = None
        return v, (None if ty == ("self",) else ty)

    def _call(self, inv, name, args, recv_val, recv, rtype):
        """Value (and result type) of a call. Order: source, escaper, user code, library catalogue, Z."""
        if name in SOURCE_METHODS and not (name in SOURCE_ON_REQUEST and rtype and rtype not in REQUEST_TYPES):
            return T, None
        if name in CTX_SANITIZERS:
            return _clean_for(join(*args), CTX_SANITIZERS[name]), "String"
        if name in SANITIZERS: return F, None
        # an unknown receiver (a chain after a library call, an untyped name): a catalogued library name answers
        # first — otherwise every user class in the project that happens to define toString() is a candidate
        known_lib = name in TRANSPARENT or name in NUMERIC_RESULT or (name in CLEAN_FACTORY and not args)
        cands = None if (recv[0] == "any" and known_lib) else self._cands(name, len(args), recv)
        if cands:
            rtypes = {_typename(m.return_type) for m in cands if m.return_type is not None}
            ty = rtypes.pop() if len(rtypes) == 1 else None
            self._summary_sinks(inv, cands, args)
            if ty in CLEAN_TYPES: return F, ty
            return self._apply(cands, args), ty
        if name in NUMERIC_RESULT: return F, None
        if name in CLEAN_FACTORY and not args: return F, RETURNS.get(name)
        if name in TRANSPARENT: return join(recv_val, *args), RETURNS.get(name)
        return Z, RETURNS.get(name)

    # ---------------------------------------------------------------- containers
    def _mutate(self, var, inv, args, env):
        """add/put/append on a local fold the argument into it; the element model follows constant ops."""
        if inv.member in MUTATORS:
            env[var] = join(env.get(var, Z), *args)
        lk, mk = "#l:" + var, "#m:" + var
        if lk in env:
            L = list(env[lk]); m, a = inv.member, inv.arguments or []
            c = [self._const(x, env) for x in a]
            ok = True
            if m == "add" and len(a) == 1: L.append(args[0])
            elif m == "add" and len(a) == 2 and isinstance(c[0], int) and not isinstance(c[0], bool) and 0 <= c[0] <= len(L):
                L.insert(c[0], args[1])
            elif m == "remove" and len(a) == 1 and isinstance(c[0], int) and not isinstance(c[0], (bool, _Ch)) \
                    and isinstance(a[0], J.Literal) and 0 <= c[0] < len(L):
                L.pop(c[0])
            elif m == "set" and len(a) == 2 and isinstance(c[0], int) and not isinstance(c[0], bool) and 0 <= c[0] < len(L):
                L[c[0]] = args[1]
            elif m == "clear" and not a: L = []
            elif m in ("get", "size", "isEmpty", "contains", "indexOf"): pass
            else: ok = False
            if ok and not (inv.selectors and m not in ("get",)): env[lk] = tuple(L)
            else: env.pop(lk, None)
        if mk in env:
            D = dict(env[mk]); m, a = inv.member, inv.arguments or []
            c = [self._const(x, env) for x in a]
            ok = True
            if m in ("put", "putIfAbsent") and len(a) == 2 and c[0] is not _NC:
                if m == "put" or c[0] not in D: D[c[0]] = args[1]
            elif m == "remove" and len(a) == 1 and c[0] is not _NC: D.pop(c[0], None)
            elif m == "clear" and not a: D = {}
            elif m in ("get", "getOrDefault", "containsKey", "size", "isEmpty"): pass
            else: ok = False
            if ok: env[mk] = tuple(sorted(D.items(), key=lambda kv: repr(kv[0])))
            else: env.pop(mk, None)

    def _model_get(self, var, inv, env):
        a = inv.arguments or []
        if inv.member == "get" and len(a) == 1:
            c = self._const(a[0], env)
            if "#l:" + var in env:
                L = env["#l:" + var]
                if isinstance(c, int) and not isinstance(c, bool) and 0 <= c < len(L): return L[c]
            if "#m:" + var in env and c is not _NC:
                D = dict(env["#m:" + var])
                return D.get(c, Z)
        return None

    # ---------------------------------------------------------------- sinks
    def _sink(self, inv, name, args, rtype, qual):
        if not args: return
        if name in SINK_HIGH:
            ctx, which = SINK_HIGH[name]
            v = args[0] if which == "first" else (join(*args[:2]) if which == "cmd" else join(*args))
            self._judge(inv, name, ctx, v, fallback_line=self._stline)
        elif name in SINK_SOFT:
            ctx, types = SINK_SOFT[name]
            if rtype is None or rtype in types:
                self._judge(inv, name, ctx, join(*args[1:]) if len(args) > 1 else F, soft=True,
                            fallback_line=self._stline)
        elif name in SINK_RECV:
            ctx, types, open_unknown, which = SINK_RECV[name]
            if qual and qual.startswith("System."): return          # console stream, not a web sink
            v = args[0] if which == "first" else join(*args)
            if rtype in types:
                self._judge(inv, name, ctx, v, fallback_line=self._stline)
            elif rtype is not None: return                          # known type, not a sink-bearer
            elif open_unknown:
                self._judge(inv, name, ctx, v, soft=True, fallback_line=self._stline)

    # ---------------------------------------------------------------- guard / branch-join helpers
    def _guard(self, cond):
        """Return (var, negated) if cond validates a single variable, else (None, False).
        whitelist.contains(x) -> ('x',False); x.equals("ok") -> ('x',False); !ALLOWED.contains(x) -> ('x',True)."""
        if not isinstance(cond, J.MethodInvocation): return (None, False)
        neg = "!" in (cond.prefix_operators or [])
        # PATTERN.matcher(x).matches(): a full-match whitelist over x (find() is a partial match: not a guard)
        if cond.member == "matcher" and len(cond.selectors or []) == 1 \
                and isinstance(cond.selectors[0], J.MethodInvocation) and cond.selectors[0].member == "matches":
            a = (cond.arguments or [None])[0]
            if isinstance(a, J.MemberReference) and not a.qualifier and not a.selectors: return (a.member, neg)
            return (None, False)
        if cond.selectors: return (None, False)
        if cond.member in GUARD_ARG:
            for a in (cond.arguments or []):
                if isinstance(a, J.MemberReference) and not a.qualifier and not a.selectors: return (a.member, neg)
        if cond.member in GUARD_RECV and cond.qualifier and "." not in cond.qualifier:
            return (cond.qualifier, neg)
        return (None, False)

    def _join(self, a, b): return join(a, b)

    def _terminates(self, st):
        if st is None: return False
        if isinstance(st, (J.ReturnStatement, J.ThrowStatement, J.BreakStatement, J.ContinueStatement)): return True
        if isinstance(st, J.BlockStatement):
            return bool(st.statements) and self._terminates(st.statements[-1])
        return False

    # ---------------------------------------------------------------- the walk
    _stline = 0

    def _walk(self, body, env):
        """Structural walk: branches in SEPARATE envs then JOINED; constant conditions prune dead branches;
        a terminating then-branch does not reach the continuation (a negated guard over it narrows)."""
        for st in (body or []):
            ln = _line(st)
            if ln: self._stline = ln
            if isinstance(st, J.BlockStatement):
                self._walk(st.statements, env); continue
            if isinstance(st, J.IfStatement):
                self.taint(st.condition, env)
                c = self._const(st.condition, env)
                if c is True:
                    self._walk([st.then_statement], env); continue
                if c is False:
                    self._walk([st.else_statement] if st.else_statement else [], env); continue
                var, neg = self._guard(st.condition)
                then_term = self._terminates(st.then_statement)
                else_term = self._terminates(st.else_statement)
                e1 = dict(env); e2 = dict(env)
                if var and not neg: e1[var] = F               # positive guard narrows the THEN branch
                self._walk([st.then_statement] if st.then_statement else [], e1)
                self._walk([st.else_statement] if st.else_statement else [], e2)
                if then_term and not else_term:
                    _set_env(env, e2)                         # continuation follows else/fallthrough
                    if var and neg: env[var] = F              # !guard{return} => clean after the if
                elif else_term and not then_term:
                    _set_env(env, e1)
                else:
                    _set_env(env, _ejoin(e1, e2))
                continue
            if isinstance(st, (J.ForStatement, J.WhileStatement, J.DoStatement)):
                self._loop(st, env); continue
            if isinstance(st, J.SwitchStatement):
                self._switch(st, env); continue
            if isinstance(st, J.TryStatement):
                self._try(st, env); continue
            if isinstance(st, J.SynchronizedStatement):
                self.taint(st.lock, env); self._walk(st.block or [], env); continue
            if isinstance(st, (J.ClassDeclaration, J.InterfaceDeclaration, J.EnumDeclaration)):
                continue                                      # a local class: its methods are judged on their own
            if isinstance(st, J.LocalVariableDeclaration):
                self._declare(st, env); continue
            if isinstance(st, J.ReturnStatement):
                v = self.taint(st.expression, env) if st.expression is not None else F
                if self._rets is not None: self._rets.append(v)
                continue
            if isinstance(st, J.StatementExpression):
                self.taint(st.expression, env); continue
            if isinstance(st, J.ThrowStatement):
                self.taint(st.expression, env); continue
            if isinstance(st, J.AssertStatement):
                self.taint(st.condition, env); continue
            if isinstance(st, (J.BreakStatement, J.ContinueStatement)):
                # the state here leaves to the loop/switch exit (or the next iteration): record it there.
                # A labelled jump or a continue may leave several levels: recorded at every level (over-approx).
                if self._esc:
                    levels = self._esc if (getattr(st, 'goto', None) or isinstance(st, J.ContinueStatement)) \
                        else self._esc[-1:]
                    for lv in levels: lv.append(dict(env))
                continue
            # anything else: evaluate its expressions (sinks inside are still judged)
            for attr in getattr(st, 'attrs', ()):
                x = getattr(st, attr, None)
                if isinstance(x, J.Expression): self.taint(x, env)

    def _declare(self, decl, env):
        """A local declaration. No initialiser -> Z: Java's definite assignment means a later read sees an
        assignment this walk should also have seen; if it did not, the read must not be clean."""
        tn = _typename(decl.type)
        for d in decl.declarators:
            v = self.taint(d.initializer, env) if d.initializer is not None else Z
            if tn in CLEAN_TYPES: v = F
            env[d.name] = v
            c = self._const(d.initializer, env) if d.initializer is not None else _NC
            if c is _NC: env.pop("#c:" + d.name, None)
            else: env["#c:" + d.name] = c
            self._model_init(d.name, d.initializer, env)

    def _loop(self, st, env):
        """Zero or more iterations: join(before, after one, after two) — two passes carry a value round."""
        ctl = getattr(st, 'control', None)
        def head(e):
            if isinstance(ctl, J.EnhancedForControl):
                v = self.taint(ctl.iterable, e)
                for d in ctl.var.declarators:
                    e[d.name] = F if _typename(ctl.var.type) in CLEAN_TYPES else v
                    e.pop("#c:" + d.name, None)
            elif isinstance(ctl, J.ForControl):
                if ctl.condition is not None: self.taint(ctl.condition, e)
            elif getattr(st, 'condition', None) is not None:
                self.taint(st.condition, e)
        def tail(e):
            if isinstance(ctl, J.ForControl):
                for u in (ctl.update or []): self.taint(u, e)
        if isinstance(ctl, J.ForControl) and ctl.init is not None:
            init = ctl.init
            if isinstance(init, J.VariableDeclaration):
                self._declare(init, env)
            else:
                for x in (init if isinstance(init, list) else [init]): self.taint(x, env)
        cond = ctl.condition if isinstance(ctl, J.ForControl) else getattr(st, 'condition', None)
        forever = (isinstance(ctl, J.ForControl) and cond is None) or \
                  (isinstance(cond, J.Literal) and cond.value == "true" and not cond.prefix_operators)
        # (only the literal: a constant variable may be changed by the body and end the loop normally)
        esc = []
        self._esc.append(esc)
        try:
            e0 = dict(env)
            e1 = dict(env); head(e1); self._walk([st.body] if st.body else [], e1); tail(e1)
            e2 = _ejoin(e0, e1, *esc)
            e3 = dict(e2); head(e3); self._walk([st.body] if st.body else [], e3); tail(e3)
            if forever:                                   # while(true)/for(;;): the only way out is a break
                brk = [e for e in esc]
                _set_env(env, _ejoin(*brk) if brk else e3)
            elif isinstance(st, J.DoStatement):           # the body runs at least once
                _set_env(env, _ejoin(e1, e3, *esc))
            else:
                _set_env(env, _ejoin(e2, e3, *esc))
        finally:
            self._esc.pop()

    def _switch(self, st, env):
        esc = []
        self._esc.append(esc)
        try:
            self._switch0(st, env, esc)
        finally:
            self._esc.pop()

    def _switch0(self, st, env, esc):
        self.taint(st.expression, env)
        v = self._const(st.expression, env)
        cases = st.cases or []
        labels = [[self._const(l, env) for l in (c.case or [])] for c in cases]
        if v is not _NC and all(l is not _NC for ls in labels for l in ls):
            entry = next((i for i, ls in enumerate(labels) if any(self._same(v, l) for l in ls)), None)
            if entry is None:
                entry = next((i for i, c in enumerate(cases) if not c.case), None)
            if entry is None: return
            e = dict(env)
            for c in cases[entry:]:
                self._walk(c.statements, e)
                if _jumps(c.statements): break
            _set_env(env, _ejoin(*esc) if esc else e)
            return
        outs, fall, has_default = [], None, False
        for c in cases:
            if not c.case: has_default = True
            e = dict(env) if fall is None else _ejoin(env, fall)
            self._walk(c.statements, e)
            j = _jumps(c.statements)
            if j == "break": outs.append(e); fall = None
            elif j == "term": fall = None
            else: fall = e
        if fall is not None: outs.append(fall)
        if not has_default: outs.append(dict(env))
        outs += esc
        _set_env(env, _ejoin(*outs) if outs else env)

    @staticmethod
    def _same(a, b):
        if isinstance(a, bool) or isinstance(b, bool): return a is b
        if isinstance(a, _Ch) or isinstance(b, _Ch):
            return _num(a) == _num(b) if not (isinstance(a, str) and not isinstance(a, _Ch)) else False
        return a == b

    def _try(self, st, env):
        for r in (st.resources or []):
            v = self.taint(r.value, env)
            env[r.name] = v
        e_try = dict(env)
        self._walk(st.block or [], e_try)
        outs = [] if _jumps(st.block or []) == "term" else [e_try]
        for c in (st.catches or []):
            ec = _ejoin(env, e_try)                                  # the throw may come from anywhere in the block
            pname = getattr(getattr(c, 'parameter', None), 'name', None)
            if pname: ec[pname] = Z
            self._walk(c.block or [], ec)
            if _jumps(c.block or []) != "term": outs.append(ec)
        new = _ejoin(*outs) if outs else e_try
        if st.finally_block: self._walk(st.finally_block, new)
        _set_env(env, new)

    def _judge(self, inv, name, ctx, st, soft=False, fallback_line=0):
        st = _at(st, ctx)
        eff = Z if (soft and st == T) else st         # soft generic sink, unknown receiver -> honest Z
        d = taintjudge.judge_taint(eff, ctx, source="input", sink=name)   # the ONE ZTL judge
        if d in ("REFUTED", "OPEN"):
            line = inv.position.line if getattr(inv,'position',None) else fallback_line
            self.sinks.append((line, name, ctx, d))

    def judge(self, tree):
        if self._dirty: self._summarize_all()
        self.sinks = []
        for path, m in tree.filter(J.MethodDeclaration):
            self._judge_method(m)
        for path, m in tree.filter(J.ConstructorDeclaration):
            self._judge_method(m)
        # a loop body is walked twice and a sink in it may be reported twice: keep the worst per site
        best = {}
        for rec in self.sinks:
            k = rec[:3]
            if k not in best or _DRANK[rec[3]] > _DRANK[best[k][3]]: best[k] = rec
        seen, out = set(), []
        for rec in self.sinks:
            k = rec[:3]
            if k in seen: continue
            seen.add(k); out.append(best[k])
        self.sinks = out
        return self.sinks

    def _judge_method(self, m):
        self.cur = self.owner.get(id(m))
        self.vt = self._types_of(m)
        # params clean by default (their flows are the summary's job) EXCEPT entry-point sources:
        # Spring-annotated params, and (on a @*Mapping handler) BARE simple-type params, which Spring
        # auto-binds from the request (implicit @RequestParam). Complex/annotated params stay clean.
        handler = _is_handler(m)
        def _src(p):
            if _typename(p.type) in CLEAN_TYPES: return F
            if _is_spring_source(p): return T
            if handler and not (getattr(p,'annotations',None)) and _typename(p.type) in SIMPLE_TYPES: return T
            return F
        env = {p.name: _src(p) for p in (m.parameters or [])}
        self._rets = None
        self._walk(m.body, env)

    def run(self, tree): self.index(tree); return self.judge(tree)

def analyze(code): return Engine().run(javalang.parse.parse(code))
def analyze_app(paths):
    e=Engine(); trees=[]
    for p in paths:
        try: t=javalang.parse.parse(open(p,encoding="utf-8",errors="replace").read())
        except Exception: continue
        trees.append((p,t)); e.index(t)
    out=[]
    for p,t in trees:
        for rec in e.judge(t): out.append((p,)+rec)
    return out

if __name__=="__main__":
    for ln,m,ctx,d in analyze(open(sys.argv[1],encoding="utf-8").read()):
        print(f"  L{ln}: {d:8} [{ctx}] {m}")
