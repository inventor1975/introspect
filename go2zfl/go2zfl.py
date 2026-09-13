# -*- coding: utf-8 -*-
"""go2zfl — Go module of the introspect (slices 1-4 + calibration, 2026-09-12).
Parser: Go's OWN go/ast via the `goast` helper (goast.go -> compact JSON tree). Shared contract
INTROSPECT-SEMANTICS.md: zero-trust F/T/Z -> REFUTED/OPEN/EARNED, honest OPEN.
Slice1: source->sink taint, string-concat propagation, transparent conversions/Sprintf,
cross-function + cross-file SUMMARIES, branch-join. Slice2: receiver-aware sources/sinks (gin
c.Query via *gin.Context type; w.Write via http.ResponseWriter), file/ssrf/xss sinks, mux.Vars,
prepared-statement awareness (stmt from .Prepare passes BOUND params, not SQL). Slice3: package-level
constant resolution. Slice4: guards (equality / map-membership / negated-early-return). Fourth language."""
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

    def globals_env(self, trees):
        """Taint of package-level const/var declarations (2 passes for const-of-const chains)."""
        g = {}
        pairs = [(gl.get("name"), gl.get("value")) for t in trees for gl in t.get("globals", [])]
        for _ in range(2):
            for name, val in pairs:
                if name and name != "_": g[name] = self.taint(val, g)
        return g

    def _join(self, a, b): return T if T in (a, b) else (Z if Z in (a, b) else F)

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
        if k == "bin": return self._join(self.taint(n.get("x"), env), self.taint(n.get("y"), env))
        if k in ("star", "unary", "slice", "typeassert", "index"): return self.taint(n.get("x"), env)
        if k == "kv": return self.taint(n.get("value"), env)
        if k == "composite":
            ts = [self.taint(e, env) for e in n.get("elts", [])]
            return T if T in ts else (Z if Z in ts else F)
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
        if fun.get("k") == "other" and len(args) == 1:      # T(x) / []byte(x): conversion, transparent
            return self.taint(args[0], env)
        if fun.get("k") == "sel" and fun.get("x", {}).get("name") == "fmt" \
                and fun.get("sel") in ("Sprintf", "Sprint", "Sprintln"):
            ts = [self.taint(a, env) for a in args]
            return T if T in ts else (Z if Z in ts else F)
        name = _callee_name(fun)
        if name in self.summaries:                          # cross-function: passes taint to return?
            for i in self.summaries[name]["passes"]:
                if i < len(args) and self.taint(args[i], env) == T: return T
            return F
        return Z

    # ---------- sink reporting ----------
    def _iter_calls(self, n):
        if isinstance(n, dict):
            if n.get("k") == "call": yield n
            for v in n.values(): yield from self._iter_calls(v)
        elif isinstance(n, list):
            for x in n: yield from self._iter_calls(x)

    def _join_args(self, args, env):
        ts = [self.taint(a, env) for a in args]
        return T if T in ts else (Z if Z in ts else F)

    def _apply_summary(self, call, name, args, env):
        for i, ctxs in self.summaries[name]["sinks"].items():
            if i < len(args):
                sti = self.taint(args[i], env)
                for cx in ctxs: self._judge(call, name + "()->sink", cx, sti)

    def _ctx_taint(self, n, env, ctx):
        while isinstance(n, dict) and n.get("k") == "call":     # go call key is "fun"; unwrap []byte()/string()
            fun = n.get("fun", {}); nm = _callee_name(fun); a = n.get("args", [])
            if nm in CTX_SANITIZERS:
                if CTX_SANITIZERS[nm] == ctx: return F
                return self.taint(a[0], env) if a else F        # transparent for other contexts
            if (fun.get("k") == "other" or nm in ("string", "byte")) and len(a) == 1:
                n = a[0]; continue                              # conversion wrapper -> unwrap
            break
        if isinstance(n, dict) and n.get("k") == "bin":         # "a" + html.EscapeString(x) + "b"
            return self._join(self._ctx_taint(n.get("x"), env, ctx), self._ctx_taint(n.get("y"), env, ctx))
        return self.taint(n, env)

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
                if nm in self.summaries: self._apply_summary(c, nm, args, env)

    def _judge(self, call, name, ctx, st):
        d = taintjudge.judge_taint(st, ctx, source="input", sink=name)   # the ONE ZTL judge, not a local rule
        if d in ("REFUTED", "OPEN"):
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

    def _walk(self, body, env):
        for st in (body or []):
            if not isinstance(st, dict): continue
            k = st.get("k")
            if k == "block": self._walk(st.get("body"), env); continue
            if k == "if":
                if st.get("init"): self._walk([st["init"]], env)
                self._leaf_sinks(st.get("cond"), env)
                var, neg = self._guard(st)
                then_term = self._terminates(st.get("body"))
                e1 = dict(env); e2 = dict(env)
                if var and not neg: e1[var] = F               # positive guard narrows the THEN branch
                self._walk(st.get("body"), e1)
                if st.get("els"): self._walk([st["els"]], e2)
                if then_term:
                    for key in set(e2): env[key] = e2[key]    # continuation follows else/fallthrough
                    if var and neg: env[var] = F              # !guard { return } -> validated after the if
                else:
                    for key in set(e1) | set(e2):
                        env[key] = self._join(e1.get(key, env.get(key, Z)), e2.get(key, env.get(key, Z)))
                continue
            if k in ("for", "range"):
                if st.get("x"): self._leaf_sinks(st.get("x"), env)
                self._walk(st.get("body"), env); continue
            if k in ("switch", "case"):
                self._walk(st.get("body"), env); continue
            # leaf statements
            if k == "assign":
                vals = [self.taint(r, env) for r in st.get("rhs", [])]
                lhs = st.get("lhs", [])
                if len(vals) == len(lhs):
                    for l, v in zip(lhs, vals):
                        if l.get("k") == "ident": env[l["name"]] = v
                else:                                        # a, b := f(): spread the single rhs taint
                    v = vals[0] if vals else Z
                    for l in lhs:
                        if l.get("k") == "ident": env[l["name"]] = v
            elif k == "var":
                for vd in st.get("vars", []):
                    names, values = vd.get("names", []), vd.get("values", [])
                    for i, nm in enumerate(names):
                        env[nm] = self.taint(values[i], env) if i < len(values) else F
            self._leaf_sinks(st, env)

    # ---------- passes ----------
    def _summ_of(self, fn):
        self.vt = self._types_of(fn); self.prepared = self._prepared_of(fn)
        params = [p["name"] for p in fn.get("params", []) if p.get("name") and p.get("name") != "_"]
        summ = {"sinks": {}, "passes": set(), "params": params}
        for i, p in enumerate(params):
            saved = self.sinks; self.sinks = []
            env = dict(self.genv); env[p] = T; self._walk(fn.get("body"), env)
            ctxs = sorted({ctx for (_l, _m, ctx, d) in self.sinks if d == "REFUTED"})
            self.sinks = saved
            if ctxs: summ["sinks"][i] = ctxs
            for st in self._iter_stmts(fn.get("body")):
                if st.get("k") == "return" and any(self.taint(r, env) == T for r in st.get("results", [])):
                    summ["passes"].add(i); break
        return summ

    def index(self, tree):
        for fn in tree.get("funcs", []):
            if fn.get("name"): self.summaries[fn["name"]] = self._summ_of(fn)

    def judge(self, tree):
        self.sinks = []
        for fn in tree.get("funcs", []):
            self.vt = self._types_of(fn); self.prepared = self._prepared_of(fn)
            env = dict(self.genv)
            env.update({p["name"]: F for p in fn.get("params", []) if p.get("name") and p.get("name") != "_"})
            self._walk(fn.get("body"), env)
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

def analyze_app(paths):
    e = Engine(); trees = []
    for p in paths:
        t = parse(p)
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
