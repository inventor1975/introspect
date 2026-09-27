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
SOURCE_METHS = {"post","json","text","read","form","body"}   # aiohttp + Starlette/FastAPI request methods
SOURCE_ATTRS = {"request.args","request.form","request.values","request.GET","request.POST",
                "request.data","request.json","request.COOKIES","request.cookies","request.headers","request.files",
                "request.match_info","request.query","request.rel_url","request.GET",
                "request.FILES","request.body","request.META","request.POST",
                "request.query_params","request.path_params"}   # Starlette/FastAPI
# sink: callee -> ctx. subprocess handled specially (only shell=True is a shell sink).
SINK_CALLS   = {"os.system":"shell","os.popen":"shell","eval":"code","exec":"code","compile":"code",
                "pickle.loads":"deser","pickle.load":"deser","yaml.load":"deser","marshal.loads":"deser",
                "cursor.execute":"sql","cursor.executescript":"sql","open":"file",
                "render_template_string":"ssti","Template":"ssti","__import__":"code",
                # XSS: mark_safe/Markup exist to BYPASS autoescape; HttpResponse renders text/html by default.
                # escape/html.escape are sanitizers, so mark_safe(escape(x)) stays clean; mark_safe(x) is the flaw.
                "mark_safe":"xss","django.utils.safestring.mark_safe":"xss","safestring.mark_safe":"xss",
                "Markup":"xss","markupsafe.Markup":"xss","flask.Markup":"xss",
                "HttpResponse":"xss","django.http.HttpResponse":"xss"}
SUBPROCESS   = {"subprocess.call","subprocess.run","subprocess.Popen","subprocess.check_output"}
SQL_METHODS  = {"execute","executemany","executescript"}   # cursor.execute by METHOD NAME (any receiver)
# values that cannot carry an injection payload whatever went in
CLEAN_FN     = {"int","float","bool","len","hash","id","abs","round","ord","isinstance","callable"}
# CONTEXT-AWARE escapers: clean for their own sink context only, transparent for every other
CTX_SANITIZERS = {"shlex.quote":"shell","pipes.quote":"shell",
                  "escape":"xss","html.escape":"xss","markupsafe.escape":"xss","cgi.escape":"xss",
                  "django.utils.html.escape":"xss","conditional_escape":"xss",
                  "secure_filename":"file","werkzeug.utils.secure_filename":"file"}
SANITIZERS   = set(CLEAN_FN)          # kept for callers that read the old name
TRANSPARENT_FN = {"str","bytes","bytearray","base64.b64decode","base64.b64encode",
                "base64.urlsafe_b64decode","base64.standard_b64decode","urllib.parse.unquote",
                "urllib.parse.unquote_plus","urllib.parse.unquote_to_bytes","json.loads"}
TRANSPARENT_METH = {"decode","encode","strip","lstrip","rstrip","lower","upper","title","get","read"}
TRANSPARENT_ARG = {"re.sub":2, "re.subn":2}   # transform the string at that arg -> preserve its taint
# calls on a local that store their argument in it
MUTATORS = {"append","extend","insert","add","update","setdefault","appendleft","extendleft","push","write",
            "writelines","put","put_nowait"}
# calls that neither store nor return their argument's taint (their result is not data)
PURE_CLEAN_METH = {"count","index","find","rfind","startswith","endswith","isdigit","isalpha","isalnum",
                   "isnumeric","isspace","islower","isupper","__len__","__contains__"}
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

def _clean_for(v, ctx):
    d, over = _parts(v)
    over[ctx] = F
    return _mk(d, over)

def _ejoin(*envs):
    out, keys = {}, set()
    for e in envs: keys |= set(e)
    for k in keys: out[k] = join(*[e[k] for e in envs if k in e])
    return out

def _set_env(env, new):
    env.clear(); env.update(new)


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

    # ---------- pass 1: register; summaries to a fixpoint once everything is registered ----------
    def index(self, tree):
        """Pass 1 (global): register functions/methods/classes across ALL files."""
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
            for fn in self._all_defs(): self.fsum[id(fn)] = self._summ_of(fn)
            if self.fsum == before: break
        self.summaries = {n: self.fsum[id(ds[-1])] for n, ds in self.funcs.items()}
        self.msums = {(c, m): self.fsum[id(fn)] for c, ms in self.classes.items() for m, fn in ms.items()}
        self._dirty = False

    def _summ_of(self, fn):
        """Walk the body with every parameter clean (BASE: what the function returns / sinks on its own),
        then once per parameter with that one T. Returns are captured where they happen."""
        names, npos, va, kw = _params(fn)
        saved = (self.sinks, self.vtype, self.cur, self._rets)
        self.cur = self.owner.get(id(fn))
        def run(env):
            self.sinks, self.vtype, self._rets = [], {}, []
            self._walk(fn.body, env, report_earned=True)
            got = {}
            for (l, c, ctx, d, _w) in self.sinks:
                k = (l, c, ctx)
                if _DRANK[d] > _DRANK.get(got.get(k), -1): got[k] = d
            return (join(*self._rets) if self._rets else F), got
        try:
            base, bs = run({p: F for p in names})
            summ = {"params": names, "npos": npos, "vararg": va, "kwarg": kw,
                    "base": base, "ret": [], "sinks": {}, "passes": set()}
            for i, p in enumerate(names):
                env = {q: F for q in names}; env[p] = T
                r, ps = run(env)
                summ["ret"].append(r)
                if _at(r, None) == T: summ["passes"].add(i)
                eff = {}
                for k, d in ps.items():
                    if _DRANK[d] > _DRANK.get(bs.get(k), 0) and _DRANK[d] > _DRANK.get(eff.get(k[2]), -1):
                        eff[k[2]] = d
                if eff: summ["sinks"][i] = eff
            return summ
        finally:
            self.sinks, self.vtype, self.cur, self._rets = saved

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

    def _is_whitelist_guard(self, test):
        # if x in (<literals>)   or   if x in KNOWN_CONST
        return (isinstance(test, ast.Compare) and len(test.ops)==1
                and isinstance(test.ops[0], ast.In)
                and isinstance(test.left, ast.Name)
                and literal_collection(test.comparators[0]))

    def _sink_ctx(self, call):
        callee = dotted(call.func)
        if callee in SINK_CALLS: return SINK_CALLS[callee]
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
        if isinstance(node, ast.Name): return env.get(node.id, Z)
        if isinstance(node, ast.NamedExpr): return self.taint(node.value, env)
        if isinstance(node, ast.Starred): return self.taint(node.value, env)
        if isinstance(node, ast.BinOp):
            return join(self.taint(node.left,env), self.taint(node.right,env))
        if isinstance(node, ast.BoolOp):                      # `a or b` evaluates to one of them
            return join(*[self.taint(v, env) for v in node.values])
        if isinstance(node, ast.IfExp):
            return join(self.taint(node.body, env), self.taint(node.orelse, env))
        if isinstance(node, ast.Compare): return F           # a boolean
        if isinstance(node, ast.UnaryOp):
            return F if isinstance(node.op, (ast.Not, ast.USub, ast.UAdd, ast.Invert)) else Z
        if isinstance(node, ast.JoinedStr):
            return join(*[self.taint(v.value,env) for v in node.values if isinstance(v,ast.FormattedValue)])
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
            if callee in CLEAN_FN: return F
            if callee in CTX_SANITIZERS and not (isinstance(node.func, ast.Name) and node.func.id in self.funcs):
                return _clean_for(join(*[self.taint(a, env) for a in node.args]), CTX_SANITIZERS[callee])
            if callee in SOURCE_CALLS: return T
            if callee and node.func.__class__ is ast.Attribute and node.func.attr=="get" \
               and dotted(node.func.value) in SOURCE_ATTRS: return T
            if node.func.__class__ is ast.Attribute and node.func.attr in SOURCE_METHS \
               and dotted(node.func.value)=="request": return T   # aiohttp await request.post()
            if callee in TRANSPARENT_FN and node.args: return self.taint(node.args[0], env)
            if callee in TRANSPARENT_ARG:
                i=TRANSPARENT_ARG[callee]
                if i < len(node.args): return self.taint(node.args[i], env)
            sums, off = self._callee_sums(node)
            if sums is not None: return self._apply(sums, node, env, off)
            if isinstance(node.func, ast.Attribute):
                m=node.func.attr
                if m in PURE_CLEAN_METH: return F
                if m=="format":
                    return join(self.taint(node.func.value,env), *[self.taint(a,env) for a in node.args],
                                *[self.taint(k.value,env) for k in node.keywords])
                if m == "join":
                    return join(self.taint(node.func.value,env), *[self.taint(a,env) for a in node.args])
                if m in TRANSPARENT_METH:
                    r=self.taint(node.func.value,env)
                    if r!=F: return r          # x.decode()/.get()/.read() preserve receiver taint
            return Z
        if isinstance(node, ast.Attribute):
            return T if dotted(node) in SOURCE_ATTRS else Z
        return Z

    # ---------- pass 2: walk with guard narrowing, apply summaries ----------
    def judge(self, tree):
        """Pass 2: judge THIS file's call sites using the (possibly cross-file) global summaries."""
        if self._dirty: self._summarize_all()
        self.sinks = []
        self.vtype = {}              # receiver tracking, per file scope
        self.cur = None; self._rets = None
        self._walk(tree.body, {})    # module-level (import-time) code
        # Walk EVERY function/method body as its own scope. Params seeded clean (F): a param->sink
        # flow is the SUMMARY's job (judged at call sites); the body-walk finds INTERNAL sources
        # (input()/request inside the body) and cross-function/cross-file calls to summarised sinks.
        for n in ast.walk(tree):
            if isinstance(n, FUNC):
                self.vtype = {}
                self.cur = self.owner.get(id(n))
                params = {p: F for p in _params(n)[0]}
                self._walk(n.body, params, report_earned=False)
        self.cur = None
        # a loop body is walked twice: keep the worst record per site
        best, order = {}, []
        for rec in self.sinks:
            k = rec[:3]
            if k not in best: order.append(k); best[k] = rec
            elif _DRANK[rec[3]] > _DRANK[best[k][3]]: best[k] = rec
        self.sinks = [best[k] for k in order]
        return self.sinks

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
                        f"{(self.vtype.get(c.func.value.id) or self.cur or c.func.value.id)}.{c.func.attr}()->sink"
                    self._judge(c, label, cx, l, parameterised=False, report_earned=report_earned)
                if isinstance(c.func, ast.Attribute): continue     # a resolved method is not a bare-name sink
            callee=dotted(c.func); ctx=self._sink_ctx(c)
            if ctx and c.args:
                self._judge(c, callee, ctx, self.taint(c.args[0],env), (ctx=="sql" and len(c.args)>=2), report_earned)

    def _assign(self, tgt, sv, env, val=None):
        if isinstance(tgt, ast.Name):
            env[tgt.id] = sv
            cls = val.func.id if (isinstance(val, ast.Call) and isinstance(val.func, ast.Name)
                                  and val.func.id in self.classes) else None
            if cls: self.vtype[tgt.id] = cls
            elif tgt.id in self.vtype: del self.vtype[tgt.id]
        elif isinstance(tgt, (ast.Tuple, ast.List)):
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
                gv = st.test.left.id if self._is_whitelist_guard(st.test) else None
                e1=dict(env)
                if gv: e1[gv]=F                                  # whitelist-narrowed in the true branch
                self._walk(st.body, e1, report_earned)
                e2=dict(env); self._walk(st.orelse, e2, report_earned)
                _set_env(env, _ejoin(e1, e2))
                continue
            if isinstance(st, getattr(ast, "TryStar", ast.Try)) or isinstance(st, ast.Try):
                e_try = dict(env)
                self._walk(st.body, e_try, report_earned)
                self._walk(st.orelse, e_try, report_earned)
                outs = [e_try]
                for h in st.handlers:                            # the exception may come from anywhere in the body
                    eh = _ejoin(env, e_try)
                    if h.name: eh[h.name] = Z
                    self._walk(h.body, eh, report_earned)
                    outs.append(eh)
                new = _ejoin(*outs)
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
            self._effects(st, env)
            self._sinks_in(st, env, report_earned)

    def _loop(self, st, env, report_earned):
        """Zero or more iterations: join(before, after one, after two)."""
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

def analyze_app(paths):
    """Cross-file: index every file's summaries GLOBALLY, then judge each file's call sites."""
    e=Engine(); trees=[]
    del UNPARSED[:]
    for path in paths:
        try: t=ast.parse(open(path,encoding='utf-8',errors='replace').read())
        except SyntaxError as ex:
            UNPARSED.append((path, "SyntaxError")); continue
        trees.append((path,t)); e.index(t)
    out=[]
    for path,t in trees:
        for rec in e.judge(t): out.append((path,)+rec)
    return out
if __name__=="__main__":
    for ln,fn,ctx,d,w in analyze(open(sys.argv[1],encoding="utf-8").read()):
        print(f"  L{ln}: {d:8} [{ctx}] {fn}  <- {w}")
