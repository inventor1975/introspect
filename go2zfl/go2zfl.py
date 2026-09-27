# -*- coding: utf-8 -*-
"""go2zfl — Go module of the introspect (slices 1-4 + calibration, 2026-09-12).
Parser: Go's OWN go/ast via the `goast` helper (goast.go -> compact JSON tree). Shared contract
INTROSPECT-SEMANTICS.md: zero-trust F/T/Z -> REFUTED/OPEN/EARNED, honest OPEN.
Slice1: source->sink taint, string-concat propagation, transparent conversions/Sprintf,
cross-function + cross-file SUMMARIES, branch-join. Slice2: receiver-aware sources/sinks (gin
c.Query via *gin.Context type; w.Write via http.ResponseWriter), file/ssrf/xss sinks, mux.Vars,
prepared-statement awareness (stmt from .Prepare passes BOUND params, not SQL). Slice3: package-level
constant resolution. Slice4: guards (equality / map-membership / negated-early-return). Fourth language.
Slice5 (2026-09-27), the java2zfl soundness lesson ported: tri-valued summaries with a parameter-free
base, returns captured where they happen, OPEN sink effects kept, same-name functions that disagree
-> Z, summaries to a fixpoint; switch cases and loops joined (zero iterations, fallthrough over-
approximated); range binds key/value; `+=` joins; m[k] = v / append / buf.WriteString fold into the
container; escapers tag one context; comparisons and arithmetic are F."""
import json, subprocess, os, sys
F, T, Z = "F", "T", "Z"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # tool/ -> the shared taint->ZFL->judge adapter
import taintjudge
GOAST = os.path.join(HERE, "goast")

# sources (net/http): method-name calls + selector chains (X.{Query|Header|Form|PostForm}.Get / mux.Vars)
SOURCE_METHODS = {"FormValue", "PostFormValue", "FormFile"}
GET_CHAIN_RECV = {"Header", "Form", "PostForm", "Trailer"}   # X.Header.Get(..) etc.
# gin: RECEIVER-aware (only when the receiver is typed *gin.Context) -> avoids the c.Query / db.Query collision
GIN_CTX_TYPES = {"gin.Context"}
GIN_SRC = {"Query", "Param", "PostForm", "DefaultQuery", "DefaultPostForm",
           "QueryArray", "PostFormArray", "GetHeader"}
# sinks
#   exec.Command / exec.CommandContext -> shell (any tainted arg)
#   database/sql receiver methods -> sql; value maps method -> QUERY arg index (Context variants: ctx first)
SQL_METHODS = {"Query": 0, "Exec": 0, "QueryRow": 0, "Prepare": 0,
               "QueryContext": 1, "ExecContext": 1, "QueryRowContext": 1, "PrepareContext": 1}
# package-function sinks keyed by (pkg-ident, func) -> ctx; the dangerous arg is arg0
PKG_SINKS = {("os", "Open"): "file", ("os", "OpenFile"): "file", ("os", "ReadFile"): "file",
             ("os", "Create"): "file", ("os", "Remove"): "file", ("os", "RemoveAll"): "file",
             ("ioutil", "ReadFile"): "file", ("ioutil", "WriteFile"): "file",
             ("http", "Get"): "ssrf", ("http", "Post"): "ssrf", ("http", "Head"): "ssrf",
             ("http", "PostForm"): "ssrf", ("template", "HTML"): "xss", ("template", "JS"): "xss",
             ("template", "URL"): "xss"}
XSS_WRITER_TYPES = {"http.ResponseWriter"}        # receiver-typed w.Write(..) -> xss
# context-aware escapers: neutralise ONE context, transparent for others (like php2zfl)
CTX_SANITIZERS = {"EscapeString": "xss", "HTMLEscapeString": "xss", "JSEscapeString": "xss",
                  "QueryEscape": "url", "PathEscape": "url"}
CONV_IDENTS = {"string", "byte", "rune"}          # string(x) etc: transparent conversions

_RANK = {F: 0, Z: 1, T: 2}
_DRANK = {"EARNED": 0, "OPEN": 1, "REFUTED": 2}
# package functions whose result carries their arguments' taint (strings.Join, url.QueryUnescape, ...)
PKG_TRANSPARENT = {"Join", "Replace", "ReplaceAll", "TrimSpace", "Trim", "TrimLeft", "TrimRight", "TrimPrefix",
                   "TrimSuffix", "ToLower", "ToUpper", "Title", "Split", "SplitN", "Fields", "Repeat",
                   "QueryUnescape", "PathUnescape", "DecodeString", "EncodeToString", "Quote", "Unquote",
                   "NewBufferString", "NewReader", "Errorf", "New", "Clean", "Base", "Dir", "Ext", "Abs"}
# results that are numbers / booleans
NUMERIC_RESULT = {"len", "cap", "Atoi", "ParseInt", "ParseUint", "ParseFloat", "ParseBool", "Itoa", "FormatInt",
                  "FormatUint", "FormatBool", "Contains", "HasPrefix", "HasSuffix", "Index", "Count",
                  "EqualFold", "Compare", "MatchString"}
# methods that store their argument in the receiver
MUTATORS = {"WriteString", "Write", "WriteByte", "WriteRune", "Add", "Set", "Store", "Push"}

def _parts(v): return (v, {}) if isinstance(v, str) else (v[0], dict(v[1]))
def _mk(d, over):
    over = {c: l for c, l in over.items() if l != d}
    return d if not over else (d, tuple(sorted(over.items())))
def _at(v, ctx): return v if isinstance(v, str) else dict(v[1]).get(ctx, v[0])
def _pc(fn, *vs):
    if all(isinstance(v, str) for v in vs): return fn(*vs)
    ctxs = set()
    for v in vs: ctxs |= set(_parts(v)[1])
    return _mk(fn(*[_parts(v)[0] for v in vs]), {c: fn(*[_at(v, c) for v in vs]) for c in ctxs})
def _lj(*ls): return max(ls, key=_RANK.get) if ls else F
def join(*vs):
    vs = [v for v in vs if v is not None]
    if not vs: return F
    return _lj(*vs) if all(isinstance(v, str) for v in vs) else _pc(lambda *ls: _lj(*ls), *vs)
def _compose(a, r): return _pc(lambda x, y: F if x == F else (y if x == T else (Z if y != F else F)), a, r)
def _clean_for(v, ctx):
    d, over = _parts(v); over[ctx] = F; return _mk(d, over)
def _ejoin(*envs):
    out, keys = {}, set()
    for e in envs: keys |= set(e)
    for k in keys: out[k] = join(*[e[k] for e in envs if k in e])
    return out
def _set_env(env, new): env.clear(); env.update(new)
def _root(n):
    while isinstance(n, dict) and n.get("k") in ("index", "sel", "star", "slice"): n = n.get("x", {})
    return n.get("name") if isinstance(n, dict) and n.get("k") == "ident" else None

def _callee_name(fun):
    if not isinstance(fun, dict): return None
    if fun.get("k") == "ident": return fun.get("name")
    if fun.get("k") == "sel": return fun.get("sel")
    return None

class Engine:
    def __init__(self):
        self.summaries = {}
        self.sinks = []
        self.vt = {}          # per-function: var/param name -> type name (receiver-aware sources & sinks)
        self.prepared = set() # per-function: vars assigned from .Prepare(..) -> their Query/Exec pass BOUND params
        self.genv = {}        # package-level const/var taint (so constant DDL idents are clean, not OPEN)
        self.funcs = {}       # name -> [func node] (bare names: methods of different types collide)
        self._rets = None
        self._dirty = False

    def globals_env(self, trees):
        """Taint of package-level const/var declarations (2 passes for const-of-const chains)."""
        g = {}
        pairs = [(gl.get("name"), gl.get("value")) for t in trees for gl in t.get("globals", [])]
        for _ in range(2):
            for name, val in pairs:
                if name and name != "_": g[name] = self.taint(val, g)
        return g

    def _join(self, a, b): return join(a, b)

    def _terminates(self, body):
        """Does this block end in a return? (for negated-guard early-return narrowing)."""
        if isinstance(body, list) and body:
            last = body[-1]
            return isinstance(last, dict) and last.get("k") == "return"
        return False

    def _guard(self, st):
        """(var, negated) if the if validates one variable, else (None, False).
        x == "c"  |  allow[x]  |  (_, ok := allow[x]; ok)  |  !<any of these> (negated -> early-return narrows after)."""
        cond = st.get("cond", {}); init = st.get("init"); neg = False
        if isinstance(cond, dict) and cond.get("k") == "unary" and cond.get("op") == "!":
            neg = True; cond = cond.get("x", {})
        if isinstance(cond, dict) and cond.get("k") == "bin" and cond.get("op") == "==":   # x == "const"
            for a, b in ((cond.get("x"), cond.get("y")), (cond.get("y"), cond.get("x"))):
                if isinstance(a, dict) and a.get("k") == "ident" and isinstance(b, dict) and b.get("k") == "lit":
                    return (a.get("name"), neg)
        if isinstance(cond, dict) and cond.get("k") == "index":                            # allow[x]
            xi = cond.get("index", {})
            if isinstance(xi, dict) and xi.get("k") == "ident": return (xi.get("name"), neg)
        if isinstance(cond, dict) and cond.get("k") == "ident" and isinstance(init, dict) \
                and init.get("k") == "assign":                                              # _, ok := allow[x]; ok
            for r in init.get("rhs", []):
                if isinstance(r, dict) and r.get("k") == "index":
                    xi = r.get("index", {})
                    if isinstance(xi, dict) and xi.get("k") == "ident": return (xi.get("name"), neg)
        return (None, False)

    def _types_of(self, fn):
        """var/param name -> type name for one function (params + `var x T` declarations)."""
        vt = {}
        for p in fn.get("params", []) + fn.get("recv", []):
            if p.get("name") and p.get("typ"): vt[p["name"]] = p["typ"]
        for st in self._iter_stmts(fn.get("body")):
            if st.get("k") == "var":
                for vd in st.get("vars", []):
                    if vd.get("typ"):
                        for nm in vd.get("names", []): vt[nm] = vd["typ"]
        return vt

    def _prepared_of(self, fn):
        """Vars bound from a .Prepare(..)/.PrepareContext(..) call: calls ON them pass BOUND params (safe)."""
        prep = set()
        for st in self._iter_stmts(fn.get("body")):
            if st.get("k") == "assign":
                for r in st.get("rhs", []):
                    if isinstance(r, dict) and r.get("k") == "call" \
                       and r.get("fun", {}).get("sel") in ("Prepare", "PrepareContext"):
                        for l in st.get("lhs", []):
                            if l.get("k") == "ident" and l.get("name") != "_": prep.add(l["name"])
        return prep

    # ---------- taint of an expression node ----------
    def taint(self, n, env):
        if not isinstance(n, dict): return F
        k = n.get("k")
        if k == "lit": return F
        if k == "ident": return env.get(n.get("name"), Z)
        if k == "bin":
            if n.get("op") != "+": return F                  # comparison, logic, arithmetic: bool / number
            return join(self.taint(n.get("x"), env), self.taint(n.get("y"), env))
        if k == "unary" and n.get("op") in ("!", "-", "^", "+"): return F
        if k in ("star", "unary", "slice", "typeassert", "index"): return self.taint(n.get("x"), env)
        if k == "kv": return join(self.taint(n.get("value"), env), self.taint(n.get("key"), env))
        if k == "composite": return join(*[self.taint(e, env) for e in n.get("elts", [])])
        if k == "call": return self._call_taint(n, env)
        if k == "sel": return Z            # unknown field access (r.Host etc.): honest unknown
        return Z if k == "other" else F

    def _is_source(self, call):
        fun = call.get("fun", {})
        if not isinstance(fun, dict) or fun.get("k") != "sel": return False
        sel = fun.get("sel"); x = fun.get("x", {})
        if sel in SOURCE_METHODS: return True
        if sel == "Vars" and x.get("name") == "mux": return True    # gorilla/mux path vars (tainted map)
        if sel in GIN_SRC and self.vt.get(x.get("name")) in GIN_CTX_TYPES: return True  # receiver-aware gin
        if sel == "Get":                                    # X.Query().Get(..) / X.{Header|Form|PostForm}.Get(..)
            if x.get("k") == "call" and x.get("fun", {}).get("sel") == "Query": return True
            if x.get("k") == "sel" and x.get("sel") in GET_CHAIN_RECV: return True
        return False

    def _call_taint(self, n, env):
        fun = n.get("fun", {}); args = n.get("args", [])
        if self._is_source(n): return T
        if fun.get("k") == "ident" and fun.get("name") in CONV_IDENTS:
            return self.taint(args[0], env) if args else F
        name0 = _callee_name(fun)
        if name0 in CTX_SANITIZERS and not (fun.get("k") == "ident" and self._sums(name0)):   # own function wins
            return _clean_for(join(*[self.taint(a, env) for a in args]), CTX_SANITIZERS[name0])
        if fun.get("k") == "ident" and name0 == "append": return join(*[self.taint(a, env) for a in args])
        if fun.get("k") == "other" and len(args) == 1:      # T(x) / []byte(x): conversion, transparent
            return self.taint(args[0], env)
        if fun.get("k") == "sel" and fun.get("x", {}).get("name") == "fmt" \
                and fun.get("sel") in ("Sprintf", "Sprint", "Sprintln"):
            return join(*[self.taint(a, env) for a in args])
        name = _callee_name(fun)
        sums = self._sums(name)
        pkg = fun.get("k") == "sel" and fun.get("x", {}).get("k") == "ident" \
            and fun.get("x", {}).get("name") not in env and fun.get("x", {}).get("name") not in self.vt
        if sums is not None and not (pkg and (name in PKG_TRANSPARENT or name in NUMERIC_RESULT)):
            return self._apply(sums, args, env)
        if name in NUMERIC_RESULT: return F
        if pkg and name in PKG_TRANSPARENT: return join(*[self.taint(a, env) for a in args])
        if fun.get("k") == "sel" and name == "String" and not args: return self.taint(fun.get("x"), env)
        return Z

    def _sums(self, name):
        if self._dirty: self._summarize_all()
        return self.summaries.get(name)

    def _apply(self, sums, args, env):
        res = []
        for s in sums:
            if s is None: res.append(Z); continue
            v = s["base"]; n = len(s["ret"])
            for i, a in enumerate(args):
                v = join(v, _compose(self.taint(a, env), s["ret"][min(i, n - 1)] if n else Z))
            res.append(v)
        if not res: return Z
        return res[0] if all(r == res[0] for r in res) else Z

    # ---------- sink reporting ----------
    def _iter_calls(self, n):
        if isinstance(n, dict):
            if n.get("k") == "call": yield n
            for v in n.values(): yield from self._iter_calls(v)
        elif isinstance(n, list):
            for x in n: yield from self._iter_calls(x)

    def _join_args(self, args, env):
        return join(*[self.taint(a, env) for a in args])

    def _apply_summary(self, call, name, args, env):
        sums = [s for s in (self._sums(name) or []) if s is not None]
        per = {}
        for s in sums:
            n = len(s["ret"])
            for i, eff in s["sinks"].items():
                for j, a in enumerate(args):
                    if not (j == i or (j > i and i == n - 1)): continue
                    for cx, d in eff.items():
                        x = _at(self.taint(a, env), cx)
                        l = F if x == F else (Z if (x == Z or d != "REFUTED") else T)
                        per.setdefault(cx, {})[id(s)] = _lj(per.get(cx, {}).get(id(s), F), l)
        for cx, by in per.items():
            ls = [by.get(id(s), F) for s in sums]
            l = T if all(x == T for x in ls) else (Z if any(x != F for x in ls) else F)
            self._judge(call, name + "()->sink", cx, l)

    def _ctx_taint(self, n, env, ctx):
        while isinstance(n, dict) and n.get("k") == "call":     # go call key is "fun"; unwrap []byte()/string()
            fun = n.get("fun", {}); nm = _callee_name(fun); a = n.get("args", [])
            if nm in CTX_SANITIZERS:
                if CTX_SANITIZERS[nm] == ctx: return F
                return _at(self.taint(a[0], env), ctx) if a else F   # transparent for other contexts
            if (fun.get("k") == "other" or nm in ("string", "byte")) and len(a) == 1:
                n = a[0]; continue                              # conversion wrapper -> unwrap
            break
        if isinstance(n, dict) and n.get("k") == "bin":         # "a" + html.EscapeString(x) + "b"
            return self._join(self._ctx_taint(n.get("x"), env, ctx), self._ctx_taint(n.get("y"), env, ctx))
        return _at(self.taint(n, env), ctx)

    def _leaf_sinks(self, node, env):
        for c in self._iter_calls(node):
            fun = c.get("fun", {}); args = c.get("args", [])
            sel = fun.get("sel") if fun.get("k") == "sel" else None
            xnm = fun.get("x", {}).get("name") if fun.get("k") == "sel" else None
            if sel in ("Command", "CommandContext") and xnm == "exec":
                self._judge(c, "exec." + sel, "shell", self._join_args(args, env))
            elif (xnm, sel) in PKG_SINKS and args:          # os./ioutil./http./template. package sinks (arg0)
                self._judge(c, xnm + "." + sel, PKG_SINKS[(xnm, sel)], self._ctx_taint(args[0], env, PKG_SINKS[(xnm, sel)]))
            elif sel == "Write" and self.vt.get(xnm) in XSS_WRITER_TYPES and args:   # receiver-typed w.Write
                self._judge(c, "Write", "xss", self._ctx_taint(args[0], env, "xss"))
            elif sel in SQL_METHODS and args and xnm not in self.prepared:  # has-args gate avoids url.Query();
                qi = SQL_METHODS[sel]                        # prepared-stmt receiver passes BOUND params (safe)
                if qi < len(args): self._judge(c, sel, "sql", self.taint(args[qi], env))
            else:
                nm = _callee_name(fun)
                if self._sums(nm): self._apply_summary(c, nm, args, env)

    def _judge(self, call, name, ctx, st):
        st = _at(st, ctx)
        d = taintjudge.judge_taint(st, ctx, source="input", sink=name)   # the ONE ZTL judge, not a local rule
        if d in ("REFUTED", "OPEN", "EARNED"):
            self.sinks.append((call.get("line", 0), name, ctx, d))

    # ---------- statement walk ----------
    def _iter_stmts(self, body):
        for st in (body or []):
            if not isinstance(st, dict): continue
            k = st.get("k")
            if k == "block": yield from self._iter_stmts(st.get("body"))
            elif k == "if":
                yield from self._iter_stmts(st.get("body"))
                if st.get("els"): yield from self._iter_stmts([st["els"]])
            elif k in ("for", "range", "switch", "case"): yield from self._iter_stmts(st.get("body"))
            else: yield st

    def _effects(self, n, env):
        """Calls that store their argument in a local: buf.WriteString(x), v.Add(k, x)."""
        for c in self._iter_calls(n):
            fun = c.get("fun", {})
            if fun.get("k") != "sel": continue
            r = fun.get("x", {})
            if not (isinstance(r, dict) and r.get("k") == "ident" and r.get("name") in env): continue
            vs = [self.taint(a, env) for a in c.get("args", [])]
            if fun.get("sel") in MUTATORS: env[r["name"]] = join(env[r["name"]], *vs)
            elif fun.get("sel") not in NUMERIC_RESULT and any(x != F for x in vs) \
                    and fun.get("sel") not in SQL_METHODS:
                env[r["name"]] = join(env[r["name"]], Z)              # an unknown call MAY store it

    def _walk(self, body, env):
        for st in (body or []):
            if not isinstance(st, dict): continue
            k = st.get("k")
            if k == "block": self._walk(st.get("body"), env); continue
            if k == "if":
                if st.get("init"): self._walk([st["init"]], env)
                self._leaf_sinks(st.get("cond"), env); self._effects(st.get("cond"), env)
                var, neg = self._guard(st)
                then_term = self._terminates(st.get("body"))
                e1 = dict(env); e2 = dict(env)
                if var and not neg: e1[var] = F               # positive guard narrows the THEN branch
                self._walk(st.get("body"), e1)
                if st.get("els"): self._walk([st["els"]], e2)
                if then_term:
                    _set_env(env, e2)                         # continuation follows else/fallthrough
                    if var and neg: env[var] = F              # !guard { return } -> validated after the if
                else:
                    _set_env(env, _ejoin(e1, e2))
                continue
            if k in ("for", "range"):
                if st.get("x"): self._leaf_sinks(st.get("x"), env)
                def head(e):
                    if k == "range":
                        v = self.taint(st.get("x"), e)
                        for part in ("key", "value"):
                            nm = _root(st.get(part))
                            if nm and nm != "_": e[nm] = v
                e0 = dict(env)
                e1 = dict(env); head(e1); self._walk(st.get("body"), e1)
                e2 = _ejoin(e0, e1)
                e3 = dict(e2); head(e3); self._walk(st.get("body"), e3)
                _set_env(env, _ejoin(e2, e3))                 # zero or more iterations
                continue
            if k == "switch":
                outs, prev = [dict(env)], None                 # no case may run (no default is marked)
                for c in st.get("body") or []:
                    e = dict(env) if prev is None else _ejoin(env, prev)   # a fallthrough, over-approximated
                    self._walk(c.get("body") if isinstance(c, dict) and c.get("k") == "case" else [c], e)
                    outs.append(e); prev = e
                _set_env(env, _ejoin(*outs))
                continue
            if k == "case":
                self._walk(st.get("body"), env); continue
            # leaf statements
            if k == "assign":
                self._effects(st, env)
                vals = [self.taint(r, env) for r in st.get("rhs", [])]
                lhs = st.get("lhs", [])
                compound = st.get("tok") not in ("=", ":=", None)
                if len(vals) != len(lhs):                    # a, b := f(): spread the single rhs taint
                    vals = [vals[0] if vals else Z] * len(lhs)
                for l, v in zip(lhs, vals):
                    if not isinstance(l, dict): continue
                    if l.get("k") == "ident":
                        if l["name"] == "_": continue
                        env[l["name"]] = join(env.get(l["name"], Z), v) if compound else v
                    else:                                    # m[k] = v / s.f = v / *p = v
                        r = _root(l)
                        if r is not None:
                            env[r] = join(env.get(r, F), v if l.get("k") in ("index", "star") else
                                          (F if v == F else Z))
            elif k == "var":
                for vd in st.get("vars", []):
                    names, values = vd.get("names", []), vd.get("values", [])
                    for i, nm in enumerate(names):
                        env[nm] = self.taint(values[i], env) if i < len(values) else F   # Go zero value
            elif k == "return":
                self._effects(st, env)
                if self._rets is not None:
                    self._rets.append(join(*[self.taint(r, env) for r in st.get("results", [])]))
            elif k == "exprstmt":
                self._effects(st, env)
            self._leaf_sinks(st, env)

    # ---------- passes ----------
    def _summ_of(self, fn):
        self.vt = self._types_of(fn); self.prepared = self._prepared_of(fn)
        params = [p.get("name") for p in fn.get("params", [])]
        saved = (self.sinks, self._rets)
        def run(env):
            self.sinks, self._rets = [], []
            self._walk(fn.get("body"), env)
            got = {}
            for (l, m, ctx, d) in self.sinks:
                key = (l, m, ctx)
                if _DRANK[d] > _DRANK.get(got.get(key), -1): got[key] = d
            return (join(*self._rets) if self._rets else F), got
        try:
            base_env = dict(self.genv)
            base_env.update({p: F for p in params if p and p != "_"})
            base, bs = run(dict(base_env))
            summ = {"sinks": {}, "passes": set(), "params": params, "base": base, "ret": []}
            for i, p in enumerate(params):
                env = dict(base_env)
                if p and p != "_": env[p] = T
                r, ps = run(env)
                summ["ret"].append(r)
                if _at(r, None) == T: summ["passes"].add(i)
                eff = {}
                for key, d in ps.items():
                    if _DRANK[d] > _DRANK.get(bs.get(key), 0) and _DRANK[d] > _DRANK.get(eff.get(key[2]), -1):
                        eff[key[2]] = d
                if eff: summ["sinks"][i] = eff
            return summ
        finally:
            self.sinks, self._rets = saved

    def index(self, tree):
        for fn in tree.get("funcs", []):
            if fn.get("name"): self.funcs.setdefault(fn["name"], []).append(fn)
        self._dirty = True

    def _summarize_all(self):
        self._dirty = False
        fs = {}
        for _ in range(4):
            before = dict(fs)
            for name, fns in self.funcs.items():
                for fn in fns: fs[id(fn)] = self._summ_of(fn)
                self.summaries[name] = [fs.get(id(fn)) for fn in fns]
            if fs == before: break

    def judge(self, tree):
        if self._dirty: self._summarize_all()
        self.sinks = []
        for fn in tree.get("funcs", []):
            self.vt = self._types_of(fn); self.prepared = self._prepared_of(fn)
            env = dict(self.genv)
            env.update({p["name"]: F for p in fn.get("params", []) if p.get("name") and p.get("name") != "_"})
            self._rets = None
            self._walk(fn.get("body"), env)
        best, order = {}, []
        for rec in self.sinks:
            key = rec[:3]
            if key not in best: order.append(key); best[key] = rec
            elif _DRANK[rec[3]] > _DRANK[best[key][3]]: best[key] = rec
        self.sinks = [best[key] for key in order if best[key][3] != "EARNED"]
        return self.sinks

    def run(self, tree):
        self.genv = self.globals_env([tree]); self.index(tree); return self.judge(tree)

def _ensure_goast():
    """Build the goast helper on first use so the module is self-contained; raise if Go is absent."""
    if os.path.exists(GOAST): return
    src = os.path.join(HERE, "goast.go")
    env = dict(os.environ, GO111MODULE="off", GOCACHE=os.environ.get("GOCACHE", "/tmp/gocache"))
    r = subprocess.run(["go", "build", "-o", GOAST, src], capture_output=True, text=True, cwd=HERE, env=env)
    if r.returncode != 0 or not os.path.exists(GOAST):
        raise RuntimeError("go2zfl: could not build goast helper (need Go toolchain): " + r.stderr.strip())

def parse(path):
    _ensure_goast()
    out = subprocess.run([GOAST, path], capture_output=True, text=True, timeout=30)
    return json.loads(out.stdout) if out.stdout.strip() else {"funcs": []}

def analyze(path): return Engine().run(parse(path))

UNPARSED = []     # files the last analyze_app could not parse: NOT analysed, NOT clean

def analyze_app(paths):
    e = Engine(); trees = []
    del UNPARSED[:]
    for p in paths:
        t = parse(p)
        if t.get("error"): UNPARSED.append((p, str(t["error"])[:60])); continue
        if t.get("funcs") or t.get("globals"): trees.append((p, t))
    e.genv = e.globals_env([t for _, t in trees])
    for _, t in trees: e.index(t)
    out = []
    for p, t in trees:
        for rec in e.judge(t): out.append((p,) + rec)
    return out

if __name__ == "__main__":
    for ln, m, ctx, d in analyze(sys.argv[1]):
        print(f"  L{ln}: {d:8} [{ctx}] {m}")
