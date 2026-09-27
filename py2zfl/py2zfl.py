# -*- coding: utf-8 -*-
"""code2py — Python module of the introspect.
Native ast; zero-trust F/T/Z -> REFUTED/OPEN/EARNED; honest OPEN on the unresolved.
Slices 1-3 (2026-09-11): single-fn taint; function SUMMARIES (cross-fn); GUARD narrowing
(if x in WHITELIST -> x is F in the branch) + shell=True refinement.

Slice 4 (2026-09-27), the java2zfl lesson ported: every place the walk wrote F for "don't know".
  * a summary keeps the return as F/Z/T per parameter plus a parameter-free BASE, captured AT each
    return (it was "T or nothing", read off the final environment, so a Z return became F and a
    `return p` before a reassignment of p was lost); a sink the parameter makes OPEN is kept too;
  * summaries are computed to a fixpoint after every file is indexed (a caller defined before its
    callee read the callee as unknown); same-name functions that disagree -> Z;
  * keyword, *args and **kwargs arguments reach their parameters (they were ignored);
  * try/except joins (an except no longer overwrites the try path); loops join the zero-iteration
    state and carry values round twice; `x += y` joins; `a, b = v` assigns; `d[k] = v`, `o.f = v`
    and `l.append(v)` fold v into the container; an unknown call given a tainted argument makes its
    receiver Z (it may have stored it);
  * escapers are CONTEXT-AWARE: html.escape(x) is clean for xss and still tainted for os.system."""
import ast, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import taintjudge

SOURCE_CALLS = {"input"}
SOURCE_METHS = {"post","json","text","read","form","body","get_json","get_data"}   # aiohttp + Starlette/FastAPI request methods
SOURCE_ATTRS = {"request.args","request.form","request.values","request.GET","request.POST",
                "request.data","request.json","request.COOKIES","request.cookies","request.headers","request.files",
                "request.match_info","request.query","request.rel_url","request.GET",
                "request.FILES","request.body","request.META","request.POST",
                "request.query_params","request.path_params"}   # Starlette/FastAPI
# sink: callee -> ctx. subprocess handled specially (only shell=True is a shell sink).
SINK_CALLS   = {"os.system":"shell","os.popen":"shell","eval":"code","exec":"code","compile":"code",
                "sympify":"code","sympy.sympify":"code",
                "pickle.loads":"deser","pickle.load":"deser","yaml.load":"deser","marshal.loads":"deser",
                "cursor.execute":"sql","cursor.executescript":"sql","open":"file",
                "render_template_string":"ssti","__import__":"code",
                # XSS: mark_safe/Markup exist to BYPASS autoescape; HttpResponse renders text/html by default.
                # escape/html.escape are sanitizers, so mark_safe(escape(x)) stays clean; mark_safe(x) is the flaw.
                "mark_safe":"xss","django.utils.safestring.mark_safe":"xss","safestring.mark_safe":"xss",
                "Markup":"xss","markupsafe.Markup":"xss","flask.Markup":"xss",
                }
SUBPROCESS   = {"subprocess.call","subprocess.run","subprocess.Popen","subprocess.check_output"}
SQL_METHODS  = {"execute","executemany","executescript","exec_driver_sql"}   # cursor.execute by METHOD NAME (any receiver)
# values that cannot carry an injection payload whatever went in
CLEAN_FN     = {"int","float","bool","len","hash","id","abs","round","ord","isinstance","callable"}
# CONTEXT-AWARE escapers: clean for their own sink context only, transparent for every other
CTX_SANITIZERS = {"shlex.quote":"shell","pipes.quote":"shell",
                  "escape":"xss","html.escape":"xss","markupsafe.escape":"xss","cgi.escape":"xss",
                  "django.utils.html.escape":"xss","conditional_escape":"xss",
                  "secure_filename":"file","werkzeug.utils.secure_filename":"file",
                  "os.path.basename":"file","basename":"file",
                  "urllib.parse.quote":"xss","quote":"xss","urllib.parse.quote_plus":"xss","quote_plus":"xss"}
SANITIZERS   = set(CLEAN_FN)          # kept for callers that read the old name
# decoding AFTER an escaper undoes it: unquote(escape(x)) turns %3C back into <
UNESCAPERS = {"html.unescape", "unescape", "markupsafe.Markup.unescape", "urllib.parse.unquote",
              "urllib.parse.unquote_plus", "urllib.parse.unquote_to_bytes"}
TEMPFILE_FN = {"tempfile.NamedTemporaryFile", "tempfile.TemporaryFile", "tempfile.mkstemp", "tempfile.mkdtemp",
               "tempfile.TemporaryDirectory", "tempfile.SpooledTemporaryFile"}
CLEAN_ANNOTATIONS = {"int", "float", "bool", "UUID", "uuid.UUID", "Decimal", "datetime", "date", "time",
                     "conint", "confloat", "PositiveInt", "NonNegativeInt", "StrictInt", "StrictBool"}
TRANSPARENT_FN = {"Context","RequestContext","str","bytes","bytearray","base64.b64decode","base64.b64encode",
                "base64.urlsafe_b64decode","base64.standard_b64decode","urllib.parse.unquote",
                "urllib.parse.unquote_plus","urllib.parse.unquote_to_bytes","json.loads"}
TRANSPARENT_METH = {"decode","encode","strip","lstrip","rstrip","lower","upper","title","get","read",
                    "split","rsplit","splitlines","casefold","zfill","center","ljust","rjust","partition",
                    "rpartition","expandtabs","swapcase","capitalize","removeprefix","removesuffix","copy",
                    "items","values","keys","getlist","pop","setdefault","translate","normalize"}
ARG_CONTENT_METH = {"replace","format","join","format_map"}   # their arguments are text too
TRANSPARENT_ARG = {"re.sub":2, "re.subn":2}   # transform the string at that arg -> preserve its taint
# calls on a local that store their argument in it
MUTATORS = {"append","extend","insert","add","update","setdefault","appendleft","extendleft","push","write",
            "writelines","put","put_nowait"}
# calls that neither store nor return their argument's taint (their result is not data)
PURE_CLEAN_METH = {"count","index","find","rfind","startswith","endswith","isdigit","isalpha","isalnum",
                   "isnumeric","isspace","islower","isupper","__len__","__contains__"}
# blind corpus (2026-09-27, PR #5): sinks the catalogue did not know
FILE_FN = {"send_file": (0,), "FileResponse": (0,), "os.remove": (0,), "os.unlink": (0,), "os.rename": (0, 1),
           "os.replace": (0, 1), "os.stat": (0,), "os.listdir": (0,), "os.makedirs": (0,), "os.mkdir": (0,),
           "os.rmdir": (0,), "os.removedirs": (0,), "os.chmod": (0,), "os.scandir": (0,),
           "shutil.copy": (0, 1), "shutil.copy2": (0, 1), "shutil.copyfile": (0, 1), "shutil.move": (0, 1),
           "shutil.rmtree": (0,), "shutil.copytree": (0, 1), "web.FileResponse": (0,)}
PATH_METHODS = {"read_text", "read_bytes", "write_text", "write_bytes", "unlink", "rmdir", "touch", "iterdir",
                "mkdir", "open"}                        # Path(x).read_text(): the receiver is the path
XSS_RESPONSE = {"make_response", "Response", "HTMLResponse", "HttpResponse", "StreamingHttpResponse"}
NOT_HTML_RESPONSE = {"JSONResponse", "PlainTextResponse", "jsonify", "JsonResponse", "ORJSONResponse"}
# a handler returning one of these made its own response (judged at that call, not as a bare body)
RESPONSE_BUILDERS = XSS_RESPONSE | NOT_HTML_RESPONSE | {"render_template", "redirect", "send_file",
                    "send_from_directory", "FileResponse", "RedirectResponse", "abort", "render", "url_for"}
TEMPLATE_MODULES = {"jinja2", "django.template", "mako.template", "flask"}
TERMINATORS = {"abort", "flask.abort", "sys.exit", "exit", "os._exit", "quit"}
VALIDATING_METHODS = {"isdigit", "isnumeric", "isdecimal", "isalnum", "isalpha", "isidentifier", "isascii_alnum"}
PARSE_VALIDATORS = {"int", "float", "uuid.UUID", "UUID", "Decimal", "decimal.Decimal", "date.fromisoformat",
                    "datetime.fromisoformat", "ipaddress.ip_address"}
ROUTE_ATTRS = {"route", "get", "post", "put", "delete", "patch", "api_route", "head", "options", "view"}
F,T,Z = "F","T","Z"
_RANK = {F: 0, Z: 1, T: 2}
_DRANK = {"EARNED": 0, "OPEN": 1, "REFUTED": 2}
FUNC = (ast.FunctionDef, ast.AsyncFunctionDef)   # async def (aiohttp/FastAPI) counts too


# ---------------------------------------------------------------- taint values
# A value is a letter F/Z/T, or after an escaper (default letter, ((ctx, letter), ...)).
def _parts(v):
    return (v, {}) if isinstance(v, str) else (v[0], dict(v[1]))

def _mk(default, over):
    over = {c: l for c, l in over.items() if l != default}
    return default if not over else (default, tuple(sorted(over.items())))

def _at(v, ctx):
    if isinstance(v, str): return v
    return dict(v[1]).get(ctx, v[0])

def _pc(fn, *vs):
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
    """A call's result from one argument: a = the argument, r = the result when that parameter is T."""
    return _pc(lambda x, y: F if x == F else (y if x == T else (Z if y != F else F)), a, r)

def _clean_for(v, ctx, fam=None):
    d, over = _parts(v)
    over[ctx] = F
    if fam: over["~" + fam] = F
    return _mk(d, over)

# ---- HTML sub-contexts: the same rules as java2zfl (an escaper protects only where its family is safe)
CTX_ALLOWED = {"text":      {"html_nosq", "html_full", "html_text", "html_attr", "esapi_attr", "url", "strip"},
               "dq_attr":   {"html_nosq", "html_full", "html_attr", "esapi_attr", "url", "strip"},
               "sq_attr":   {"html_full", "html_attr", "esapi_attr", "url", "strip"},
               "uq_attr":   {"esapi_attr", "url"},
               "url_start": {"url"},
               "js_str":    {"js"},
               "event": set(), "tag": set(), "css": set(), "js": set()}
URL_ATTRS = {"href", "src", "action", "formaction", "background", "poster", "data", "codebase", "cite",
             "xlink:href", "srcset", "ping", "manifest"}
ESC_FAMILY = {"escape": "html_full", "html.escape": "html_full", "markupsafe.escape": "html_full",
              "django.utils.html.escape": "html_full", "conditional_escape": "html_full", "cgi.escape": "html_text",
              "urllib.parse.quote": "url", "quote": "url", "urllib.parse.quote_plus": "url", "quote_plus": "url",
              "urlencode": "url", "urllib.parse.urlencode": "url"}

def _html_ctx(prefix):
    """The HTML sub-context at the end of the text emitted so far."""
    p = prefix[-600:].lower()
    so, sc = p.rfind("<script"), p.rfind("</script")
    if so > sc:                                        # inside <script>: in a JS string or bare code
        body = p[p.find(">", so) + 1:] if p.find(">", so) >= 0 else ""
        q = None; i = 0
        while i < len(body):
            ch = body[i]
            if ch == "\\": i += 2; continue
            if q is None and ch in "'\"`": q = ch
            elif q == ch: q = None
            i += 1
        if not q: return "js"
        import re as _re2
        before = body[:body.rfind(q)] if q in body else body
        if _re2.search(r"(location(\.href)?|\.href|\.src|\.action)\s*=\s*$|(window\.open|location\.(assign|replace))\s*\(\s*$",
                       before.rstrip()):
            return "url_start"                        # a JS string that becomes a URL: javascript: survives
        return "js_str"
    st, stc = p.rfind("<style"), p.rfind("</style")
    if st > stc: return "css"
    lt, gt = p.rfind("<"), p.rfind(">")
    if lt <= gt: return "text"
    tag = p[lt + 1:]
    q = None; name = ""; start = 0; i = 0
    import re as _re
    while i < len(tag):
        ch = tag[i]
        if q is None and ch in "'\"":
            m = _re.search(r"([\w:-]+)\s*=\s*$", tag[:i])
            name = m.group(1) if m else ""; q = ch; start = i + 1
        elif q == ch: q = None
        i += 1
    if q is None:
        return "uq_attr" if _re.search(r"=\s*$", tag) else "tag"
    if name.startswith("on"): return "event"
    if name == "style": return "css"
    if name in URL_ATTRS and tag[start:].strip() == "": return "url_start"
    return "dq_attr" if q == '"' else "sq_attr"

def _adjust(v, prefix):
    """An escaped value keeps its xss credit only where its escaper family is safe."""
    if isinstance(v, str) or _at(v, "xss") != F: return v
    d, over = _parts(v)
    if d == F: return v
    fams = {k[1:] for k, l in over.items() if k.startswith("~") and l == F}
    if fams & CTX_ALLOWED.get(_html_ctx(prefix), set()): return v
    over["xss"] = d                                    # wrong sub-context: the escaper does not protect here
    for k in [k for k in over if k.startswith("~")]: del over[k]
    return _mk(d, over)


# ---------------------------------------------------------------- AST helpers
def _is_spring_source(param):
    return any(_anno(a) in SPRING_SOURCES for a in (getattr(param,'annotations',None) or []))

def _ejoin(*envs):
    out, keys = {}, set()
    for e in envs: keys |= set(e)
    for k in keys: out[k] = join(*[e[k] for e in envs if k in e])
    return out

def _set_env(env, new):
    env.clear(); env.update(new)


def _pyrender(node):
    """The constant text an expression contributes (unknown pieces -> NUL)."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str): return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add): return _pyrender(node.left) + _pyrender(node.right)
    if isinstance(node, ast.JoinedStr):
        return "".join(str(v.value) if isinstance(v, ast.Constant) else "\x00" for v in node.values)
    return "\x00"

def dotted(n):
    if isinstance(n, ast.Name): return n.id
    if isinstance(n, ast.Attribute):
        b = dotted(n.value); return f"{b}.{n.attr}" if b else n.attr
    return None

def _root(n):
    """The variable an assignment target writes into: d[k] -> d, o.f.g -> o."""
    while isinstance(n, (ast.Subscript, ast.Attribute, ast.Starred)): n = n.value
    return n.id if isinstance(n, ast.Name) else None

def literal_collection(node):
    """A constant collection literal (whitelist), e.g. ('a','b') or ['x'] or {'y'}."""
    return isinstance(node, (ast.Tuple, ast.List, ast.Set))

def _params(fn):
    """Parameter names in call-mapping order, and where *args / **kwargs sit (None if absent)."""
    a = fn.args
    pos = [x.arg for x in (getattr(a, 'posonlyargs', []) or [])] + [x.arg for x in a.args]
    names = list(pos)
    va = kw = None
    if a.vararg: va = len(names); names.append(a.vararg.arg)
    names += [x.arg for x in a.kwonlyargs]
    if a.kwarg: kw = len(names); names.append(a.kwarg.arg)
    return names, len(pos), va, kw


class Engine:
    def __init__(self):
        self.summaries = {}          # funcname -> summary (the one def of that name; see self.funcs)
        self.funcs = {}              # funcname -> [FunctionDef] (same name in several files)
        self.classes = {}            # ClassName -> {method: FunctionDef}
        self.msums = {}              # (ClassName, method) -> summary
        self.fsum = {}               # id(FunctionDef) -> summary
        self.owner = {}              # id(FunctionDef) -> ClassName for methods
        self.vtype = {}              # var -> ClassName (receiver tracking)
        self.sinks = []
        self.cur = None              # class of the method being walked
        self._rets = None
        self._dirty = False
        self.imports = {}            # per file: local name -> module path ("Template" -> "string.Template")
        self.const_coll = set()      # per file: module-level names bound to a literal-only collection
        self.modvtype = {}           # per file: module-level instances (engine = FormulaEngine())
        self._ret_sink = False       # the function is a handler whose returned str IS the HTML response
        self.unjudged = []           # (line, sink) of maybe-sinks deliberately not judged for an unknown value
        self.autoesc = {}            # names bound to a jinja2 Environment: autoescape on?
        self.pathvars = set()        # locals bound to a pathlib Path
        self.owner_tree = {}         # id(FunctionDef) -> its module (summaries need that file's context)
        self._rets_t = []
        self.str_consts = {}         # module-level names bound once to a string literal
        self.markupvars = set()      # names bound to a markupsafe.Markup template
        self.tmplvars = {}           # names bound to a compiled template: autoescape on?

    # ---------- pass 1: register; summaries to a fixpoint once everything is registered ----------
    def index(self, tree):
        """Pass 1 (global): register functions/methods/classes across ALL files."""
        for n in ast.walk(tree):
            if isinstance(n, FUNC): self.owner_tree[id(n)] = tree
        for n in tree.body:
            if isinstance(n, FUNC):
                self.funcs.setdefault(n.name, []).append(n)
            if isinstance(n, ast.ClassDef):
                self.classes[n.name] = {m.name: m for m in n.body if isinstance(m, FUNC)}
                for m in n.body:
                    if isinstance(m, FUNC): self.owner[id(m)] = n.name
        self._dirty = True

    def summarise(self, fn):
        self.funcs.setdefault(fn.name, []).append(fn); self._dirty = True

    def _all_defs(self):
        for defs in self.funcs.values(): yield from defs
        for ms in self.classes.values(): yield from ms.values()

    def _summarize_all(self):
        self._dirty = False                      # summaries read summaries: no re-entry
        for _ in range(4):
            before = dict(self.fsum)
            for fn in self._all_defs():
                t = self.owner_tree.get(id(fn))
                if t is not None: self._file_context(t)     # imports, constant sets, templates of ITS file
                self.fsum[id(fn)] = self._summ_of(fn)
            if self.fsum == before: break
        self.summaries = {n: self.fsum[id(ds[-1])] for n, ds in self.funcs.items()}
        self.msums = {(c, m): self.fsum[id(fn)] for c, ms in self.classes.items() for m, fn in ms.items()}
        self._dirty = False

    def _summ_of(self, fn):
        """Walk the body with every parameter clean (BASE: what the function returns / sinks on its own),
        then once per parameter with that one T. Returns are captured where they happen."""
        names, npos, va, kw = _params(fn)
        saved = (self.sinks, self.vtype, self.cur, self._rets, self._rets_t)
        self.cur = self.owner.get(id(fn))
        def run(env):
            self.sinks, self.vtype, self._rets, self._rets_t = [], {}, [], []
            self._walk(fn.body, env, report_earned=True)
            got = {}
            for (l, c, ctx, d, _w) in self.sinks:
                k = (l, c, ctx)
                if _DRANK[d] > _DRANK.get(got.get(k), -1): got[k] = d
            rt = self._rets_t
            tup = None                                      # every return a tuple of one length: per position
            if rt and all(isinstance(x, list) for x in rt) and len({len(x) for x in rt}) == 1:
                tup = [join(*[x[k] for x in rt]) for k in range(len(rt[0]))]
            return (join(*self._rets) if self._rets else F), got, tup
        try:
            base, bs, base_t = run({p: F for p in names})
            summ = {"params": names, "npos": npos, "vararg": va, "kwarg": kw,
                    "base": base, "ret": [], "sinks": {}, "passes": set(), "ret_t": None}
            per_t = []
            for i, p in enumerate(names):
                env = {q: F for q in names}; env[p] = T
                r, ps, pt = run(env)
                per_t.append(pt)
                summ["ret"].append(r)
                if _at(r, None) == T: summ["passes"].add(i)
                eff = {}
                for k, d in ps.items():
                    if _DRANK[d] > _DRANK.get(bs.get(k), 0) and _DRANK[d] > _DRANK.get(eff.get(k[2]), -1):
                        eff[k[2]] = d
                if eff: summ["sinks"][i] = eff
            if base_t is not None and all(pt is not None and len(pt) == len(base_t) for pt in per_t):
                summ["ret_t"] = {"base": base_t, "param": per_t}
            return summ
        finally:
            self.sinks, self.vtype, self.cur, self._rets, self._rets_t = saved

    def _bind(self, s, call, env, off=0):
        """(param index, argument value) for every argument of a call; None index = no parameter takes it."""
        out = []
        for j, a in enumerate(call.args):
            v = self.taint(a.value if isinstance(a, ast.Starred) else a, env)
            i = j + off
            if isinstance(a, ast.Starred): out.append((s["vararg"], v)); continue
            if i < s["npos"]: out.append((i, v))
            else: out.append((s["vararg"], v))
        for k in call.keywords:
            v = self.taint(k.value, env)
            if k.arg is not None and k.arg in s["params"][:len(s["params"])]:
                idx = s["params"].index(k.arg)
                out.append((idx, v))
            else:
                out.append((s["kwarg"], v))
        return out

    def _apply(self, sums, call, env, off=0):
        res = []
        for s in sums:
            if s is None: res.append(Z); continue
            v = s["base"]
            for i, a in self._bind(s, call, env, off):
                v = join(v, _compose(a, s["ret"][i]) if i is not None else _compose(a, Z))
            res.append(v)
        if not res: return Z
        return res[0] if all(r == res[0] for r in res) else Z

    def _callee_sums(self, call):
        """(summaries, offset) of the user code a call reaches, or (None, 0) when it reaches none."""
        f = call.func
        if isinstance(f, ast.Name):
            if self._dirty: self._summarize_all()
            if f.id in self.funcs:
                return [self.fsum.get(id(d)) for d in self.funcs[f.id]], 0
            return None, 0
        if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
            recv = f.value.id
            cls = self.vtype.get(recv) or (self.cur if recv == "self" else None)
            if cls is not None and f.attr in self.classes.get(cls, {}):
                return [self.fsum.get(id(self.classes[cls][f.attr]))], 1
            if recv in self.classes and f.attr in self.classes[recv]:
                return [self.fsum.get(id(self.classes[recv][f.attr]))], 0
        if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Call) and f.attr not in PATH_METHODS \
                and f.attr not in {"save", "raw", "extra", "extractall", "extract"}:
            # repository().search(q): a method on a CALL's result resolves by name when only a few user classes
            # define it (a plain variable of unknown type is usually a library object: Path, a cursor)
            if f.attr not in TRANSPARENT_METH | PURE_CLEAN_METH | MUTATORS | SQL_METHODS | {"format", "join", "get"}:
                owners = [c for c, ms in self.classes.items() if f.attr in ms]
                if 0 < len(owners) <= 3:
                    return [self.fsum.get(id(self.classes[c][f.attr])) for c in owners], 1
        return None, 0

    # ---------- statement stream WITH guard narrowing ----------
    def _stmts(self, body, env):
        """Flatten a body to leaf statements, recursing into if/try/for/while/with so nested
        assignments are tracked. `if x in WHITELIST:` narrows x=F inside the true-branch."""
        for st in body:
            if isinstance(st, ast.If) and self._is_whitelist_guard(st.test):
                var = st.test.left.id; saved = env.get(var, Z)
                env[var] = F                                  # narrowed inside the branch
                yield from self._stmts(st.body, env)
                env[var] = saved
                yield from self._stmts(st.orelse, env)
            elif isinstance(st, ast.If):
                yield from self._stmts(st.body, env); yield from self._stmts(st.orelse, env)
            elif isinstance(st, ast.Try):
                yield from self._stmts(st.body, env)
                for h in st.handlers: yield from self._stmts(h.body, env)
                yield from self._stmts(st.orelse, env); yield from self._stmts(st.finalbody, env)
            elif isinstance(st, (ast.For, ast.AsyncFor, ast.While)):
                yield from self._stmts(st.body, env); yield from self._stmts(st.orelse, env)
            elif isinstance(st, (ast.With, ast.AsyncWith)):
                yield from self._stmts(st.body, env)
            else:
                yield st

    def _atom_guard(self, t):
        """(var, negated) when the test validates one variable, else (None, False)."""
        neg = False
        while isinstance(t, ast.UnaryOp) and isinstance(t.op, ast.Not): neg = not neg; t = t.operand
        if isinstance(t, ast.Compare) and len(t.ops) == 1 and isinstance(t.ops[0], (ast.Is, ast.IsNot)) \
                and isinstance(t.comparators[0], ast.Constant) and t.comparators[0].value is None:
            v, n = self._atom_guard(t.left)                 # RE.fullmatch(x) is None -> the negation
            return (v, (n != isinstance(t.ops[0], ast.Is))) if v else (None, False)
        if isinstance(t, ast.Compare) and len(t.ops) == 1 and isinstance(t.left, ast.Name) \
                and isinstance(t.ops[0], (ast.In, ast.NotIn)):
            c = t.comparators[0]
            if literal_collection(c) or (dotted(c) in self.const_coll):
                return (t.left.id, neg != isinstance(t.ops[0], ast.NotIn))
        if isinstance(t, ast.Call) and isinstance(t.func, ast.Attribute):
            if t.func.attr in VALIDATING_METHODS and isinstance(t.func.value, ast.Name) and not t.args:
                return (t.func.value.id, neg)          # x.isdigit()
            if t.func.attr == "fullmatch" and t.args:  # RE.fullmatch(x) / re.fullmatch(p, x)
                a = t.args[-1] if dotted(t.func.value) == "re" else t.args[0]
                if isinstance(a, ast.Name): return (a.id, neg)
        return (None, False)

    def _guards(self, test):
        """(narrowed in THEN, narrowed in ELSE)."""
        if isinstance(test, ast.BoolOp):
            gs = [self._atom_guard(v) for v in test.values]
            if isinstance(test.op, ast.And): return [v for v, n in gs if v and not n], []
            return [], [v for v, n in gs if v and n]
        if isinstance(test, ast.UnaryOp) and isinstance(test.op, ast.Not) and isinstance(test.operand, ast.BoolOp):
            gs = [self._atom_guard(v) for v in test.operand.values]
            if isinstance(test.operand.op, ast.Or):    # not (a or b): ELSE = one holds -> only if one variable
                vs = {v for v, n in gs}
                return [], (list(vs) if len(vs) == 1 and all(v and not n for v, n in gs) else [])
            return [], [v for v, n in gs if v and not n]
        v, n = self._atom_guard(test)
        if not v: return [], []
        return ([], [v]) if n else ([v], [])

    def _terminates(self, body):
        if not body: return False
        last = body[-1]
        if isinstance(last, (ast.Return, ast.Raise, ast.Continue, ast.Break)): return True
        if isinstance(last, ast.Expr) and isinstance(last.value, ast.Call) and dotted(last.value.func) in TERMINATORS:
            return True
        if isinstance(last, ast.If): return self._terminates(last.body) and self._terminates(last.orelse)
        return False

    def _is_whitelist_guard(self, test):
        # if x in (<literals>)   or   if x in KNOWN_CONST
        return (isinstance(test, ast.Compare) and len(test.ops)==1
                and isinstance(test.ops[0], ast.In)
                and isinstance(test.left, ast.Name)
                and literal_collection(test.comparators[0]))

    def _sink_ctx(self, call):
        callee = dotted(call.func)
        canon = self._canon(callee)
        if canon in SINK_CALLS: callee = canon
        if callee in SINK_CALLS: return SINK_CALLS[callee]
        last = (callee or "").split(".")[-1]
        if last in XSS_RESPONSE:                               # Response(body, mimetype=..) / HTMLResponse(..)
            for k in call.keywords:
                if k.arg in ("mimetype", "media_type", "content_type") and isinstance(k.value, ast.Constant) \
                        and "html" not in str(k.value.value).lower():
                    return None                                # declared JSON / plain text: not HTML
            return "xss"
        if last == "from_string": return "ssti"                # Engine.from_string / env.from_string
        if last == "Template" and (self.imports.get(callee.split(".")[0], "") or callee).startswith(
                ("jinja2", "django.template", "mako")):
            return "ssti"                                      # string.Template executes nothing
        if isinstance(call.func, ast.Attribute) and call.func.attr in SQL_METHODS: return "sql"
        if callee in SUBPROCESS:
            for kw in call.keywords:
                if kw.arg=="shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                    return "shell"
            return None                                       # subprocess without shell=True: not a shell-injection sink
        return None

    # ---------- taint of an expression ----------
    def taint(self, node, env):
        if node is None: return F
        if isinstance(node, ast.Await): return self.taint(node.value, env)
        if isinstance(node, ast.Constant): return F
        if isinstance(node, ast.Name):
            if node.id not in env and node.id in self.str_consts: return F      # a module-level constant
            return env.get(node.id, Z)
        if isinstance(node, ast.NamedExpr): return self.taint(node.value, env)
        if isinstance(node, ast.Starred): return self.taint(node.value, env)
        if isinstance(node, ast.BinOp):
            if isinstance(node.op, ast.Mod) and self._is_markup(node.left):     # Markup("..%s") % x: escaped
                return join(self.taint(node.left, env), _clean_for(self.taint(node.right, env), "xss", "html_full"))
            if isinstance(node.op, ast.Add) and (self._is_markup(node.left) or self._is_markup(node.right)):
                l, r = self.taint(node.left, env), self.taint(node.right, env)   # Markup + x escapes x
                return join(l if self._is_markup(node.left) else _clean_for(l, "xss", "html_full"),
                            r if self._is_markup(node.right) else _clean_for(r, "xss", "html_full"))
            if isinstance(node.op, ast.Add):
                l = self.taint(node.left, env)
                if not (isinstance(node.left, ast.BinOp) and isinstance(node.left.op, ast.Add)):
                    l = _adjust(l, "")
                return join(l, _adjust(self.taint(node.right, env), _pyrender(node.left)))
            if isinstance(node.op, ast.Mod) and isinstance(node.left, ast.Constant) and isinstance(node.left.value, str):
                parts = node.left.value.split("%s")
                items = node.right.elts if isinstance(node.right, ast.Tuple) else [node.right]
                return join(*[_adjust(self.taint(it, env), "%s".join(parts[:i + 1])) for i, it in enumerate(items)])
            return join(self.taint(node.left,env), self.taint(node.right,env))
        if isinstance(node, ast.BoolOp):                      # `a or b` evaluates to one of them
            return join(*[self.taint(v, env) for v in node.values])
        if isinstance(node, ast.IfExp):
            return join(self.taint(node.body, env), self.taint(node.orelse, env))
        if isinstance(node, ast.Compare): return F           # a boolean
        if isinstance(node, ast.UnaryOp):
            return F if isinstance(node.op, (ast.Not, ast.USub, ast.UAdd, ast.Invert)) else Z
        if isinstance(node, ast.JoinedStr):
            pre, out = "", []
            for v in node.values:
                if isinstance(v, ast.Constant): pre += str(v.value)
                elif isinstance(v, ast.FormattedValue):
                    out.append(_adjust(self.taint(v.value, env), pre)); pre += "\x00"
            return join(*out)
        if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            return join(*[self.taint(e,env) for e in node.elts])
        if isinstance(node, ast.Dict):
            return join(*[self.taint(v,env) for v in node.values if v is not None],
                        *[self.taint(k,env) for k in node.keys if k is not None])
        if isinstance(node, ast.Subscript):
            if dotted(node.value) in SOURCE_ATTRS: return T
            return self.taint(node.value, env)
        if isinstance(node, ast.Call):
            callee=dotted(node.func)
            canon = self._canon(callee)
            if canon != callee and (canon in CLEAN_FN or canon in CTX_SANITIZERS or canon in TRANSPARENT_FN
                                    or canon in UNESCAPERS or canon in TRANSPARENT_ARG):
                callee = canon                           # from urllib.parse import unquote
            if callee in CLEAN_FN: return F
            if callee in CTX_SANITIZERS and not (isinstance(node.func, ast.Name) and node.func.id in self.funcs):
                fam = ESC_FAMILY.get(callee)
                if any(k.arg == "quote" and isinstance(k.value, ast.Constant) and k.value.value is False
                       for k in node.keywords) or (len(node.args) > 1 and isinstance(node.args[1], ast.Constant)
                                                     and node.args[1].value is False):
                    fam = "html_text"                            # html.escape(x, quote=False): quotes survive
                return _clean_for(join(*[self.taint(a, env) for a in node.args]), CTX_SANITIZERS[callee], fam)
            if False: return _clean_for(join(*[self.taint(a, env) for a in node.args]), CTX_SANITIZERS[callee])
            if callee in SOURCE_CALLS: return T
            if callee and node.func.__class__ is ast.Attribute and node.func.attr=="get" \
               and dotted(node.func.value) in SOURCE_ATTRS: return T
            if node.func.__class__ is ast.Attribute and node.func.attr in SOURCE_METHS \
               and dotted(node.func.value)=="request": return T   # aiohttp await request.post()
            if callee in UNESCAPERS:                         # html.unescape(html.escape(x)) is x again
                return join(*[_parts(self.taint(a, env))[0] for a in node.args]) if node.args else F
            rv = self._render_value(node, env)
            if rv is not None: return rv
            if callee in TRANSPARENT_FN and node.args: return self.taint(node.args[0], env)
            if callee in TRANSPARENT_ARG:
                i=TRANSPARENT_ARG[callee]
                if i < len(node.args): return self.taint(node.args[i], env)
            sums, off = self._callee_sums(node)
            if sums is not None: return self._apply(sums, node, env, off)
            if isinstance(node.func, ast.Attribute):
                m=node.func.attr
                if m in PURE_CLEAN_METH: return F
                if m == "format" and self._is_markup(node.func.value):   # Markup(t).format(x): x is escaped
                    return join(self.taint(node.func.value, env),
                                *[_clean_for(self.taint(a, env), "xss") for a in node.args],
                                *[_clean_for(self.taint(k.value, env), "xss") for k in node.keywords])
                if m == "join" and self._is_markup(node.func.value):     # Markup(sep).join(xs): each escaped
                    return join(*[_clean_for(self.taint(a, env), "xss", "html_full") for a in node.args])
                if m == "format" and isinstance(node.func.value, ast.Constant) and isinstance(node.func.value.value, str):
                    parts = node.func.value.value.split("{")   # "<a title='{}'>".format(esc(x))
                    out = [_adjust(self.taint(a, env), "{".join(parts[:i + 1])) for i, a in enumerate(node.args)]
                    out += [_adjust(self.taint(k.value, env), node.func.value.value.split("{" + k.arg)[0])
                            for k in node.keywords if k.arg]
                    return join(*out)
                if m=="format":
                    return join(self.taint(node.func.value,env), *[self.taint(a,env) for a in node.args],
                                *[self.taint(k.value,env) for k in node.keywords])
                if m == "join":
                    return join(self.taint(node.func.value,env), *[self.taint(a,env) for a in node.args])
                if m in TRANSPARENT_METH:                      # x.strip().split(): the receiver's taint
                    return self.taint(node.func.value, env)
                if m in ("replace", "format_map"):
                    return join(self.taint(node.func.value, env), *[self.taint(a, env) for a in node.args])
            return Z
        if isinstance(node, ast.Attribute):
            return T if dotted(node) in SOURCE_ATTRS else Z
        return Z

    # ---------- pass 2: walk with guard narrowing, apply summaries ----------
    def judge(self, tree):
        """Pass 2: judge THIS file's call sites using the (possibly cross-file) global summaries."""
        if self._dirty: self._summarize_all()
        self.sinks = []
        self.unjudged = []
        self.vtype = {}              # receiver tracking, per file scope
        self.cur = None; self._rets = None; self._ret_sink = False
        self._file_context(tree)
        self._walk(tree.body, {})    # module-level (import-time) code
        self.modvtype = dict(self.vtype)
        # Walk EVERY function/method body as its own scope. Params seeded clean (F): a param->sink
        # flow is the SUMMARY's job (judged at call sites); the body-walk finds INTERNAL sources
        # (input()/request inside the body) and cross-function/cross-file calls to summarised sinks.
        for n in ast.walk(tree):
            if isinstance(n, FUNC):
                self.vtype = dict(self.modvtype)
                self.cur = self.owner.get(id(n))
                params, self._ret_sink = self._param_seeds(n)
                self._walk(n.body, params, report_earned=False)
        self.cur = None; self._ret_sink = False
        # a loop body is walked twice: keep the worst record per site
        best, order = {}, []
        for rec in self.sinks:
            k = rec[:3]
            if k not in best: order.append(k); best[k] = rec
            elif _DRANK[rec[3]] > _DRANK[best[k][3]]: best[k] = rec
        self.sinks = [best[k] for k in order]
        return self.sinks

    def _unsafe_template(self, node):
        """A literal template that turns autoescaping off for a value (|safe, autoescape false)."""
        if isinstance(node, ast.Name) and node.id in self.str_consts:
            node = ast.Constant(value=self.str_consts[node.id])
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            t = node.value.replace(" ", "")
            return "|safe" in t or "autoescapefalse" in t or "{%autoescapeoff%}" in t
        return None

    def _render_value(self, node, env):
        """The HTML a template call produces. Flask render_template_string / Django templates / a jinja2
        Environment with autoescape escape the context; jinja2.Template and a default Environment do not."""
        callee = dotted(node.func) or ""
        ctx = join(*[self.taint(a, env) for a in node.args[1:]], *[self.taint(k.value, env) for k in node.keywords])
        if callee.split(".")[-1] == "render_template_string" and node.args:
            tmpl = self.taint(node.args[0], env)
            if tmpl != F: return tmpl
            unsafe = self._unsafe_template(node.args[0])
            return ctx if unsafe or unsafe is None else _clean_for(ctx, "xss")
        if callee.split(".")[-1] == "render_template": return _clean_for(ctx, "xss")   # .html: autoescaped
        if isinstance(node.func, ast.Attribute) and node.func.attr == "render":
            args = join(*[self.taint(a, env) for a in node.args], *[self.taint(k.value, env) for k in node.keywords])
            src = node.func.value
            if isinstance(src, ast.Name) and src.id in self.tmplvars:          # PLATE.render(first=..)
                return _clean_for(args, "xss") if self.tmplvars[src.id] else args
            if isinstance(src, ast.Call):
                sc = dotted(src.func) or ""
                mod = self.imports.get(sc.split(".")[0], sc)
                auto = mod.startswith("django") or (isinstance(src.func, ast.Attribute) and
                        isinstance(src.func.value, ast.Name) and self.autoesc.get(src.func.value.id))
                tmpl = self.taint(src.args[0], env) if src.args else F
                if tmpl != F: return join(tmpl, args)
                unsafe = self._unsafe_template(src.args[0]) if src.args else None
                return args if (unsafe or not auto) else _clean_for(args, "xss")
        return None

    _CTX_FIELDS = ("imports", "const_coll", "autoesc", "str_consts", "markupvars", "tmplvars", "int_params", "fw")

    def _file_context(self, tree):
        """The file's context, computed once per module (summaries ask for it once per function per pass)."""
        memo = self.__dict__.setdefault("_ctx_memo", {})
        got = memo.get(id(tree))
        if got is not None and got[0] is tree:
            for k, v in got[1].items(): setattr(self, k, v)
            return
        self._file_context0(tree)
        memo[id(tree)] = (tree, {k: getattr(self, k) for k in self._CTX_FIELDS})

    def _file_context0(self, tree):
        self.imports, self.const_coll, self.autoesc = {}, set(), {}
        self.str_consts = {}
        for st in tree.body:                                   # PAGE = "<p>{{ bio|safe }}</p>"
            if isinstance(st, ast.Assign) and isinstance(st.value, ast.Constant) and isinstance(st.value.value, str):
                for t in st.targets:
                    if isinstance(t, ast.Name): self.str_consts[t.id] = st.value.value
        reassigned = {t.id for n in ast.walk(tree) if isinstance(n, (ast.Assign, ast.AugAssign))
                      for t in (n.targets if isinstance(n, ast.Assign) else [n.target]) if isinstance(t, ast.Name)
                      and n not in tree.body}
        for nm in reassigned & set(self.str_consts): del self.str_consts[nm]   # rebound inside a function
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                for a in n.names: self.imports[a.asname or a.name.split(".")[0]] = a.name
            elif isinstance(n, ast.ImportFrom) and n.module:
                for a in n.names: self.imports[a.asname or a.name] = n.module + "." + a.name
        for st in tree.body:                                   # ALLOWED = {"a", "b"} / frozenset((..))
            if isinstance(st, (ast.Assign, ast.AnnAssign)):
                v = st.value
                if isinstance(v, ast.Call) and dotted(v.func) in ("frozenset", "set", "tuple", "list") and v.args:
                    v = v.args[0]
                if isinstance(v, (ast.Tuple, ast.List, ast.Set, ast.Dict)) and \
                        all(isinstance(e, ast.Constant) for e in (v.elts if not isinstance(v, ast.Dict) else v.keys)):
                    for t in (st.targets if isinstance(st, ast.Assign) else [st.target]):
                        if isinstance(t, ast.Name): self.const_coll.add(t.id)
        for n in ast.walk(tree):                               # env = Environment(autoescape=...)
            if isinstance(n, ast.Assign) and isinstance(n.value, ast.Call) and \
                    (dotted(n.value.func) or "").split(".")[-1] == "Environment":
                kw = {k.arg: k.value for k in n.value.keywords}
                on = "autoescape" in kw and not (isinstance(kw["autoescape"], ast.Constant) and kw["autoescape"].value is False)
                for t in n.targets:
                    if isinstance(t, ast.Name): self.autoesc[t.id] = on
        self.markupvars, self.tmplvars, self.int_params = set(), {}, {}
        for n in ast.walk(tree):
            if isinstance(n, ast.Assign) and isinstance(n.value, ast.Call):
                fn_ = (dotted(n.value.func) or "")
                for t in n.targets:
                    if not isinstance(t, ast.Name): continue
                    if fn_.split(".")[-1] == "Markup": self.markupvars.add(t.id)
                    if fn_.split(".")[-1] in ("from_string", "get_template"):    # PLATE = env.from_string(..)
                        base = n.value.func.value if isinstance(n.value.func, ast.Attribute) else None
                        self.tmplvars[t.id] = (bool(isinstance(base, ast.Name) and self.autoesc.get(base.id)) or
                            self.imports.get(fn_.split(".")[0], "").startswith("django")) and \
                            not (n.value.args and self._unsafe_template(n.value.args[0]))
                    if fn_.split(".")[-1] == "Template" and \
                            self.imports.get("Template", "").startswith(("jinja2", "django")):
                        self.tmplvars[t.id] = self.imports["Template"].startswith("django") and \
                            not (n.value.args and self._unsafe_template(n.value.args[0]))
            if isinstance(n, ast.Call) and (dotted(n.func) or "").split(".")[-1] in ("path", "re_path", "route",
                    "get", "post", "api_route", "add_url_rule") and n.args and isinstance(n.args[0], ast.Constant) \
                    and isinstance(n.args[0].value, str):
                import re as _re
                ints = set(_re.findall(r"<(?:int|float|uuid):(\w+)>", n.args[0].value))
                view = n.args[1] if len(n.args) > 1 else None
                if ints and isinstance(view, ast.Name): self.int_params.setdefault(view.id, set()).update(ints)
        for cd in [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]:   # pages = ("a", "b") on a class
            for st in cd.body:
                v = st.value if isinstance(st, (ast.Assign, ast.AnnAssign)) else None
                if isinstance(v, ast.Call) and dotted(v.func) in ("frozenset", "set", "tuple", "list") and v.args:
                    v = v.args[0]                            # pages = frozenset({"terms", "privacy"})
                if isinstance(st, ast.Assign) and isinstance(v, (ast.Tuple, ast.List, ast.Set, ast.Dict)) and \
                        all(isinstance(e, ast.Constant) for e in (v.elts if not isinstance(v, ast.Dict) else v.keys)):
                    for t in st.targets:
                        if isinstance(t, ast.Name): self.const_coll |= {"self." + t.id, cd.name + "." + t.id}
        mods = set(m.split(".")[0] for m in self.imports.values())
        self.fw = "fastapi" if "fastapi" in mods else ("flask" if "flask" in mods else
                  ("django" if "django" in mods or "rest_framework" in mods else ("aiohttp" if "aiohttp" in mods else None)))

    def _param_seeds(self, fn):
        """Handler parameters are request input: Flask route variables, FastAPI query/path/body params, Django
        URL kwargs. Returns (env, is_html_body_handler)."""
        names = _params(fn)[0]
        env = {p: F for p in names}
        decos = fn.decorator_list
        route = None
        for d in decos:
            t = d.func if isinstance(d, ast.Call) else d
            if isinstance(t, ast.Attribute) and t.attr in ROUTE_ATTRS: route = d
        user_deco = any(dotted(d.func if isinstance(d, ast.Call) else d) in self.funcs for d in decos)
        html_body = False
        import re as _re
        ints = set(self.int_params.get(fn.name, set()))
        for d in decos:
            if isinstance(d, ast.Call) and d.args and isinstance(d.args[0], ast.Constant) and isinstance(d.args[0].value, str):
                ints |= set(_re.findall(r"<(?:int|float|uuid):(\w+)>", d.args[0].value))
        if route is not None and self.fw != "aiohttp":
            a = fn.args
            defaults = dict(zip([x.arg for x in a.args][len(a.args) - len(a.defaults):], a.defaults))
            for x in a.args + a.kwonlyargs:
                if x.arg in ("self", "cls"): continue
                ann = dotted(x.annotation) if x.annotation is not None else ""
                dflt = defaults.get(x.arg)
                dname = dotted(dflt.func) if isinstance(dflt, ast.Call) else ""
                if ann and ann.split(".")[-1] in ("Request", "WebSocket", "BackgroundTasks", "Response", "Session",
                                                   "HttpRequest"):
                    continue
                if dname and dname.split(".")[-1] == "Depends": env[x.arg] = Z; continue
                if x.arg in ints: continue                        # <int:id>: the converter made it a number
                if (ann and ann.split(".")[-1] == "Literal") or (isinstance(x.annotation, ast.Subscript) and
                            (dotted(x.annotation.value) or "").split(".")[-1] == "Literal"):
                    continue                                      # Literal["a", "b"]: validated by the framework
                env[x.arg] = F if ((ann or "").split(".")[-1] in CLEAN_ANNOTATIONS or
                                   (ann or "").startswith(("int", "float"))) else T
            if self.fw == "fastapi":
                kws = {k.arg: dotted(k.value) for k in (route.keywords if isinstance(route, ast.Call) else [])}
                html_body = (kws.get("response_class") or "").split(".")[-1] == "HTMLResponse"
            else:
                html_body = True                       # Flask: a returned str is sent as text/html
        elif self.fw == "django" or (names and names[0] == "request") or (len(names) > 1 and names[1] == "request"):
            ps = names[1:] if names and names[0] == "request" else (names[2:] if len(names) > 1 and names[1] == "request" else [])
            if fn.name in ("get", "post", "put", "patch", "delete") or (names and names[0] == "request"):
                for p in ps:
                    if p not in ints: env[p] = T      # Django URL kwargs (and *args/**kwargs); <int:pk> is a number
        if user_deco:
            for p in names:
                if env[p] == F and p not in ("self", "cls", "request"): env[p] = Z   # a decorator may inject it
        return env, html_body

    def run(self, tree):             # single-file convenience: index then judge one tree
        self.index(tree)
        return self.judge(tree)

    def _is_route(self, fn):
        for d in fn.decorator_list:
            t = d.func if isinstance(d, ast.Call) else d
            if isinstance(t, ast.Attribute) and t.attr in ("route","get","post","put","delete","patch"):
                return True
        return False

    def _join(self, a, b): return join(a, b)

    def _sinks_in(self, node, env, report_earned):
        """Report sinks reached within one leaf node/expression (given the current env)."""
        for c in ast.walk(node):
            if not isinstance(c, ast.Call): continue
            sums, off = self._callee_sums(c)
            if sums is not None:
                name = dotted(c.func)
                per = {}
                for s in sums:
                    if s is None: continue
                    for i, a in self._bind(s, c, env, off):
                        if i is None or i not in s["sinks"]: continue
                        for cx, d in s["sinks"][i].items():
                            x = _at(a, cx)
                            l = F if x == F else (Z if (x == Z or d != "REFUTED") else T)
                            per[cx] = _lj(per.get(cx, F), l)
                known = [s for s in sums if s is not None]
                for cx, l in per.items():
                    # a candidate without this sink makes a T only OPEN (which definition runs is unknown)
                    if l == T and not all(cx in {c_ for e in s["sinks"].values() for c_ in e} for s in known):
                        l = Z
                    label = f"{name}()->sink" if isinstance(c.func, ast.Name) else \
                        f"{(self.vtype.get(getattr(c.func.value, 'id', None)) or self.cur or dotted(c.func.value) or '?')}.{c.func.attr}()->sink"
                    self._judge(c, label, cx, l, parameterised=False, report_earned=report_earned)
                if isinstance(c.func, ast.Attribute): continue     # a resolved method is not a bare-name sink
            callee=dotted(c.func); ctx=self._sink_ctx(c)
            first = c.args[0] if c.args else next((k.value for k in c.keywords
                                                   if k.arg in ("query", "sql", "operation", "content", "body",
                                                                "text", "html")), None)
            if ctx and first is not None:
                # a query with bind parameters is still injectable when its TEXT is tainted (was: any second
                # argument -> "parameterised" -> clean, an unverified clean)
                self._judge(c, callee, ctx, self.taint(first, env), False, report_earned)
                continue
            self._more_sinks(c, callee, env, report_earned)

    def _canon(self, callee):
        """unquote -> urllib.parse.unquote when imported so: catalogue names are the dotted ones."""
        if not callee: return callee
        head, _, rest = callee.partition(".")
        full = self.imports.get(head)
        if not full: return callee
        return full + ("." + rest if rest else "")

    def _is_markup(self, node):
        return isinstance(node, ast.Call) and (dotted(node.func) or "").split(".")[-1] == "Markup" or \
            (isinstance(node, ast.Name) and node.id in self.markupvars)

    def _is_path(self, node):
        if isinstance(node, ast.Call) and (dotted(node.func) or "").split(".")[-1] in ("Path", "PurePath", "PosixPath"):
            return True
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div): return True
        return isinstance(node, ast.Name) and node.id in self.pathvars

    def _more_sinks(self, c, callee, env, report_earned):
        """File, template and ORM sinks the blind corpus showed missing (2026-09-27)."""
        callee = callee or ""
        if self._canon(callee) in TEMPFILE_FN or callee in TEMPFILE_FN:      # prefix="../x" leaves dir
            vals = [self.taint(k.value, env) for k in c.keywords if k.arg in ("prefix", "suffix", "dir")]
            if vals: self._judge(c, callee, "file", join(*vals), False, report_earned)
            return
        for name, idx in FILE_FN.items():
            if callee == name or (("." not in name) and callee.split(".")[-1] == name):
                vals = [self.taint(c.args[i], env) for i in idx if i < len(c.args)]
                if vals: self._judge(c, callee, "file", join(*vals), False, report_earned)
                return
        if not isinstance(c.func, ast.Attribute): return
        m, recv = c.func.attr, c.func.value
        if m in PATH_METHODS and self._is_path(recv):
            self._judge(c, callee, "file", self.taint(recv, env), False, report_earned)
        elif m in ("extractall", "extract"):                   # an archive from the request: zip slip
            self._judge(c, callee, "file", self.taint(recv, env), False, report_earned)
        elif m == "save" and c.args and self.taint(recv, env) != F:   # request.files[..].save(path)
            self._judge(c, callee, "file", self.taint(c.args[0], env), False, report_earned)
        elif m == "raw" and c.args:                             # Model.objects.raw(sql)
            self._judge(c, callee, "sql", self.taint(c.args[0], env), False, report_earned)
        elif m == "extra":                                      # QuerySet.extra(where=[..], select={..})
            vals = [self.taint(k.value, env) for k in c.keywords if k.arg in ("where", "select", "tables", "order_by")]
            if vals: self._judge(c, callee, "sql", join(*vals), False, report_earned)

    def _assign(self, tgt, sv, env, val=None):
        if isinstance(tgt, ast.Name):
            env[tgt.id] = sv
            if val is not None and self._is_path(val): self.pathvars.add(tgt.id)
            elif tgt.id in self.pathvars and val is not None: self.pathvars.discard(tgt.id)
            cls = val.func.id if (isinstance(val, ast.Call) and isinstance(val.func, ast.Name)
                                  and val.func.id in self.classes) else None
            if cls: self.vtype[tgt.id] = cls
            elif tgt.id in self.vtype: del self.vtype[tgt.id]
        elif isinstance(tgt, (ast.Tuple, ast.List)):
            if isinstance(val, ast.Call) and not any(isinstance(e, ast.Starred) for e in tgt.elts):
                sums, off = self._callee_sums(val)            # sql, params = build(..): per position
                if sums and all(x is not None and x.get("ret_t") and len(x["ret_t"]["base"]) == len(tgt.elts)
                                for x in sums):
                    for k, e in enumerate(tgt.elts):
                        vals = []
                        for x in sums:
                            v = x["ret_t"]["base"][k]
                            for i, a in self._bind(x, val, env, off):
                                if i is not None: v = join(v, _compose(a, x["ret_t"]["param"][i][k]))
                            vals.append(v)
                        self._assign(e, vals[0] if all(v == vals[0] for v in vals) else Z, env)
                    return
            if isinstance(val, (ast.Tuple, ast.List)) and len(val.elts) == len(tgt.elts) \
                    and not any(isinstance(e, ast.Starred) for e in tgt.elts):
                for e, v in zip(tgt.elts, val.elts): self._assign(e, self.taint(v, env), env, v)   # a, b = x, 1
                return
            for e in tgt.elts: self._assign(e, sv, env)          # each element: at most the whole's taint
        elif isinstance(tgt, ast.Starred):
            self._assign(tgt.value, sv, env)
        else:                                                    # d[k] = v / o.f = v: the container holds v
            r = _root(tgt)
            if r is not None: env[r] = join(env.get(r, F), sv)

    def _effects(self, st, env):
        """Assignments hidden in expressions (walrus) and calls that store their argument in a local."""
        for n in ast.walk(st):
            if isinstance(n, ast.NamedExpr):
                self._assign(n.target, self.taint(n.value, env), env)
            elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name):
                recv, m = n.func.value.id, n.func.attr
                if recv not in env or recv in self.classes: continue
                args = [self.taint(a, env) for a in n.args] + [self.taint(k.value, env) for k in n.keywords]
                if m in MUTATORS:                                 # append/update/write: it IS stored
                    env[recv] = join(env[recv], *args)
                elif m not in TRANSPARENT_METH and m not in PURE_CLEAN_METH and m not in SQL_METHODS \
                        and any(a != F for a in args):
                    env[recv] = join(env[recv], Z)                # an unknown call MAY store it

    def _walk(self, body, env, report_earned=True):
        """Structural walk with proper branch handling: if/else analysed in SEPARATE envs then
        MERGED (taint = join), so a branch assignment never leaks into the other branch."""
        for st in body:
            if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)): continue
            if isinstance(st, ast.If):
                self._sinks_in(st.test, env, report_earned)
                self._effects(st.test, env)
                pos, neg = self._guards(st.test)
                e1, e2 = dict(env), dict(env)
                for v_ in pos: e1[v_] = F                        # validated in the true branch
                for v_ in neg: e2[v_] = F                        # !validated -> abort/return: validated after
                self._walk(st.body, e1, report_earned)
                self._walk(st.orelse, e2, report_earned)
                tt, et = self._terminates(st.body), self._terminates(st.orelse)
                if tt and not et: _set_env(env, e2)
                elif et and not tt: _set_env(env, e1)
                else: _set_env(env, _ejoin(e1, e2))
                continue
            if isinstance(st, getattr(ast, "TryStar", ast.Try)) or isinstance(st, ast.Try):
                e_try = dict(env)
                self._walk(st.body, e_try, report_earned)
                for s2 in st.body:                               # past `int(x)` in the try, x is a number
                    v2 = s2.value if isinstance(s2, (ast.Assign, ast.Expr, ast.AnnAssign)) else None
                    if isinstance(v2, ast.Call) and dotted(v2.func) in PARSE_VALIDATORS and v2.args \
                            and isinstance(v2.args[0], ast.Name):
                        e_try[v2.args[0].id] = F
                self._walk(st.orelse, e_try, report_earned)
                outs = [e_try]
                for h in st.handlers:                            # the exception may come from anywhere in the body
                    eh = _ejoin(env, e_try)
                    if h.name: eh[h.name] = Z
                    self._walk(h.body, eh, report_earned)
                    outs.append(eh)
                new = _ejoin(*outs)
                if st.handlers and all(self._terminates(h.body) for h in st.handlers):
                    for s2 in st.body:                            # try: n = int(x) except ValueError: abort(400)
                        v2 = s2.value if isinstance(s2, (ast.Assign, ast.Expr, ast.AnnAssign)) else None
                        if isinstance(v2, ast.Call) and dotted(v2.func) in PARSE_VALIDATORS and v2.args \
                                and isinstance(v2.args[0], ast.Name):
                            new[v2.args[0].id] = F
                self._walk(st.finalbody, new, report_earned)
                _set_env(env, new)
                continue
            if isinstance(st, (ast.For, ast.AsyncFor, ast.While)):
                self._loop(st, env, report_earned)
                continue
            if isinstance(st, (ast.With, ast.AsyncWith)):
                for it in st.items:
                    self._sinks_in(it.context_expr, env, report_earned)
                    if it.optional_vars is not None:
                        self._assign(it.optional_vars, self.taint(it.context_expr, env), env)
                self._walk(st.body, env, report_earned)
                continue
            if hasattr(ast, "Match") and isinstance(st, ast.Match):
                self._sinks_in(st.subject, env, report_earned)
                outs = [dict(env)]                               # no case may match
                for case in st.cases:
                    ec = dict(env)
                    for n in ast.walk(case.pattern):
                        nm = getattr(n, "name", None)
                        if isinstance(nm, str): ec[nm] = self.taint(st.subject, env)
                    self._walk(case.body, ec, report_earned); outs.append(ec)
                _set_env(env, _ejoin(*outs))
                continue
            # leaf statement: track assignment, then report sinks in it
            if isinstance(st, (ast.Assign, ast.AnnAssign)):
                val = st.value
                if val is not None:
                    sv=self.taint(val, env)
                    tgts = st.targets if isinstance(st, ast.Assign) else [st.target]
                    for t in tgts: self._assign(t, sv, env, val)
            elif isinstance(st, ast.AugAssign):
                sv = self.taint(st.value, env)
                r = _root(st.target)
                if r is not None: env[r] = join(env.get(r, Z), sv)
            elif isinstance(st, ast.Return) and self._rets is not None:
                self._rets.append(self.taint(st.value, env) if st.value is not None else F)
                self._rets_t.append([self.taint(e, env) for e in st.value.elts]
                                    if isinstance(st.value, ast.Tuple) else None)
            elif isinstance(st, ast.Return) and self._ret_sink and st.value is not None:
                body = st.value.elts[0] if isinstance(st.value, ast.Tuple) and st.value.elts else st.value
                built = isinstance(body, ast.Call) and (dotted(body.func) or "").split(".")[-1] in RESPONSE_BUILDERS \
                    and not (isinstance(body.func, ast.Attribute) and body.func.attr == "render"
                             and not (isinstance(body.func.value, ast.Name) and body.func.value.id in self.imports))
                if not built and not isinstance(body, (ast.Dict, ast.List, ast.ListComp, ast.DictComp, ast.SetComp)):
                    v = self.taint(body, env)
                    # a returned str is the HTML body, but a dict/list is JSON: only a value KNOWN to come from
                    # the request (a str) is judged; an unknown one is listed as NOT JUDGED (curator's option b)
                    if _at(v, "xss") == T:
                        self._judge(st, "return (response body)", "xss", v, report_earned=report_earned)
                    elif _at(v, "xss") == Z:
                        self.unjudged.append((st.lineno, "return (response body)"))
            self._effects(st, env)
            self._sinks_in(st, env, report_earned)

    def _loop(self, st, env, report_earned):
        """Zero or more iterations: join(before, after one, after two)."""
        checked = []
        if isinstance(st, ast.For) and isinstance(st.target, ast.Name) and isinstance(st.iter, (ast.Tuple, ast.List)) \
                and all(isinstance(e, ast.Name) for e in st.iter.elts) and st.body and isinstance(st.body[0], ast.If):
            _pos, neg = self._guards(st.body[0].test)
            if st.target.id in neg and self._terminates(st.body[0].body):
                checked = [e.id for e in st.iter.elts]           # each one passed the check or we left
        def head(e):
            if isinstance(st, ast.While):
                self._sinks_in(st.test, e, report_earned); self._effects(st.test, e)
            else:
                self._sinks_in(st.iter, e, report_earned)
                self._assign(st.target, self.taint(st.iter, e), e)
        e0 = dict(env)
        e1 = dict(env); head(e1); self._walk(st.body, e1, report_earned)
        e2 = _ejoin(e0, e1)
        e3 = dict(e2); head(e3); self._walk(st.body, e3, report_earned)
        out = _ejoin(e2, e3)
        for nm in checked: out[nm] = F
        self._walk(st.orelse, out, report_earned)
        _set_env(env, out)

    def _judge(self, c, callee, ctx, st, parameterised=False, report_earned=True):
        st = _at(st, ctx)
        eff = F if parameterised else st              # parameterised query is safe (F)
        d = taintjudge.judge_taint(eff, ctx, source=callee, sink=callee)   # the ONE ZTL judge
        if d == "EARNED":
            if not report_earned: return
            w = "parameterised" if parameterised else "nothing attacker-controlled reaches the sink"
        elif d == "REFUTED": w = "attacker-controlled value reaches the sink"
        elif d == "OPEN": w = "origin not resolved (don't know)"
        else: return
        self.sinks.append((c.lineno, callee, ctx, d, w))

def analyze(src): e=Engine(); return e.run(ast.parse(src))

UNPARSED = []     # files the last analyze_app could not parse: NOT analysed, NOT clean
UNJUDGED = []     # route returns holding an unknown value (HTML if str, JSON if dict): NOT judged, NOT clean

def analyze_app(paths):
    """Cross-file: index every file's summaries GLOBALLY, then judge each file's call sites."""
    e=Engine(); trees=[]
    del UNPARSED[:]; del UNJUDGED[:]
    for path in paths:
        try: t=ast.parse(open(path,encoding='utf-8',errors='replace').read())
        except SyntaxError as ex:
            UNPARSED.append((path, "SyntaxError")); continue
        trees.append((path,t)); e.index(t)
    out=[]
    for path,t in trees:
        for rec in e.judge(t): out.append((path,)+rec)
        UNJUDGED.extend((path,) + u for u in e.unjudged)
    return out
if __name__=="__main__":
    for ln,fn,ctx,d,w in analyze(open(sys.argv[1],encoding="utf-8").read()):
        print(f"  L{ln}: {d:8} [{ctx}] {fn}  <- {w}")
