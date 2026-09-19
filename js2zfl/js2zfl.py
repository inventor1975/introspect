# -*- coding: utf-8 -*-
"""js2zfl — JavaScript/TypeScript module of the introspect (slices 1-2 + calibration, 2026-09-13).
Parser: @babel/parser via the `jsast` helper (jsast.js -> compact JSON tree; handles JS/JSX/TS/TSX).
Shared contract INTROSPECT-SEMANTICS.md: zero-trust F/T/Z -> REFUTED/OPEN/EARNED, honest OPEN.
Slice1: Express/Node sources (req.query/params/body/headers/cookies, req.get/param) -> sinks
(child_process exec/spawn=shell, eval / new Function=code, .query/.execute=sql, res.send/render=xss,
fs.*=file); string-concat + template-literal propagation, cross-function + cross-file SUMMARIES,
branch-join. Slice2: ssrf (HTTP clients, receiver-gated) + open-redirect sinks, guards
(=== / .includes/.has / negated-return), child_process-gated shell (regex.exec collision fix).
Fifth language after php2zfl/py2zfl/java2zfl/go2zfl."""
import json, subprocess, os, sys
F, T, Z = "F", "T", "Z"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # tool/ -> shared taint->ZFL->judge adapter
import taintjudge
JSAST = os.path.join(HERE, "jsast.js")

REQUEST_NAMES = {"req", "request", "ctx"}           # conventional Express/Koa handler request param
REQ_SOURCE_PROPS = {"query", "params", "body", "headers", "cookies", "hostname", "originalUrl"}
REQ_SOURCE_CALLS = {"param", "get", "header", "cookie"}   # req.param('x') / req.get('h')
RESPONSE_NAMES = {"res", "response", "reply"}
# sinks
SHELL_M = {"exec", "execSync", "spawn", "spawnSync", "execFile", "execFileSync", "fork"}
# member-form shell sinks (cp.exec) are gated on a child_process receiver: `regex.exec(str)` is
# RegExp.prototype.exec, NOT command execution (the bare-method-name collision lesson).
CHILD_PROC_BASES = {"cp", "child_process", "childProcess", "child", "proc", "execa", "shelljs", "sh"}
SQL_M = {"query", "execute"}                          # db.query(sql) (call form; req.query is a member, not a call)
XSS_M = {"send", "write", "end", "render", "sendfile", "sendFile"}   # res.<m>(x)
FILE_M = {"readFile", "readFileSync", "writeFile", "writeFileSync",
          "createReadStream", "createWriteStream", "appendFile", "appendFileSync"}
FILE_OBJS = {"fs", "fsp", "fsPromises", "fse"}
# SSRF: outbound-request clients. member form gated on a known client base (avoids req.get() collision);
# bare-ident form for fetch()/axios()/request(url)/got()/superagent().
HTTP_CLIENTS = {"http", "https", "needle", "axios", "got", "superagent"}
HTTP_METHODS = {"get", "post", "put", "delete", "patch", "head", "request"}
SSRF_IDENTS = {"fetch", "axios", "request", "got", "superagent"}
REDIRECT_M = {"redirect"}                             # res.redirect(userInput) -> open redirect
CODE_IDENTS = {"eval"}
CONV_IDENTS = {"String", "Number", "Boolean"}        # String(x) conversion: transparent
# context-aware escapers: neutralise ONE context, transparent for others
CTX_SANITIZERS = {"escape": "xss", "escapeHtml": "xss", "escapeHTML": "xss", "sanitize": "xss",
                  "encode": "xss", "encodeURIComponent": "url", "encodeURI": "url"}


def _prop_name(member):
    p = member.get("property", {})
    return p.get("name") if isinstance(p, dict) else None

def _base_ident(n):
    while isinstance(n, dict) and n.get("k") == "member":
        n = n.get("object", {})
    return n.get("name") if isinstance(n, dict) and n.get("k") == "ident" else None

def _callee_name(callee):
    if not isinstance(callee, dict): return None
    if callee.get("k") == "ident": return callee.get("name")
    if callee.get("k") == "member": return _prop_name(callee)
    return None


class Engine:
    def __init__(self):
        self.summaries = {}
        self.sinks = []

    def _join(self, a, b): return T if T in (a, b) else (Z if Z in (a, b) else F)

    def _terminates(self, body):
        if isinstance(body, list) and body:
            last = body[-1]
            return isinstance(last, dict) and last.get("k") in ("return", "throw")
        return False

    def _guard(self, test):
        """(var, negated) if the test validates one variable, else (None, False).
        x === "c"  |  allow.includes(x) / allow.has(x)  |  !<either> (negated -> early-return narrows after)."""
        n = test; neg = False
        if isinstance(n, dict) and n.get("k") == "unary" and n.get("op") == "!":
            neg = True; n = n.get("x", {})
        if isinstance(n, dict) and n.get("k") == "bin" and n.get("op") in ("==", "===", "!==", "!="):
            eq = n.get("op") in ("==", "===")
            for a, b in ((n.get("x"), n.get("y")), (n.get("y"), n.get("x"))):
                if isinstance(a, dict) and a.get("k") == "ident" and isinstance(b, dict) and b.get("k") == "lit":
                    return (a.get("name"), neg if eq else (not neg))
        if isinstance(n, dict) and n.get("k") == "call":
            callee = n.get("callee", {}); args = n.get("args", [])
            if isinstance(callee, dict) and callee.get("k") == "member" \
                    and _prop_name(callee) in ("includes", "has") and args \
                    and isinstance(args[0], dict) and args[0].get("k") == "ident":
                return (args[0].get("name"), neg)
        return (None, False)

    # ---------- taint ----------
    def taint(self, n, env):
        if not isinstance(n, dict): return F
        k = n.get("k")
        if k == "lit": return F
        if k == "ident": return env.get(n.get("name"), Z)
        if k == "bin": return self._join(self.taint(n.get("x"), env), self.taint(n.get("y"), env))
        if k == "template":
            ts = [self.taint(e, env) for e in n.get("exprs", [])]
            return T if T in ts else (Z if Z in ts else F)
        if k in ("await", "seq"):
            return self.taint(n.get("x") or (n.get("exprs") or [{}])[-1], env)
        if k == "cond": return self._join(self.taint(n.get("x"), env), self.taint(n.get("y"), env))
        if k == "assignexpr": return self.taint(n.get("right"), env)
        if k == "unary": return F
        if k in ("array",):
            ts = [self.taint(e, env) for e in n.get("elts", [])]
            return T if T in ts else (Z if Z in ts else F)
        if k == "object":
            ts = [self.taint(e, env) for e in n.get("props", [])]
            return T if T in ts else (Z if Z in ts else F)
        if k == "member":
            if _prop_name(n) in REQ_SOURCE_PROPS and _base_ident(n) in REQUEST_NAMES: return T
            return self.taint(n.get("object"), env)      # propagate: req.query.name -> object req.query = T
        if k in ("call", "new"): return self._call_taint(n, env)
        return Z if k in ("funcref", "other") else F

    def _is_source(self, call):
        callee = call.get("callee", {})
        if isinstance(callee, dict) and callee.get("k") == "member":
            if _prop_name(callee) in REQ_SOURCE_CALLS and _base_ident(callee) in REQUEST_NAMES:
                return True
        return False

    def _call_taint(self, n, env):
        callee = n.get("callee", {}); args = n.get("args", [])
        if n.get("k") == "call" and self._is_source(n): return T
        cn = _callee_name(callee)
        if callee.get("k") == "ident" and cn in CONV_IDENTS:
            return self.taint(args[0], env) if args else F
        if cn in self.summaries:
            for i in self.summaries[cn]["passes"]:
                if i < len(args) and self.taint(args[i], env) == T: return T
            return F
        return Z

    # ---------- sinks ----------
    def _iter_calls(self, n):
        if isinstance(n, dict):
            if n.get("k") in ("call", "new"): yield n
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
        if isinstance(n, dict) and n.get("k") == "call":
            nm = _callee_name(n.get("callee", {}))
            if nm in CTX_SANITIZERS:
                if CTX_SANITIZERS[nm] == ctx: return F
                a = n.get("args", [])
                return self.taint(a[0], env) if a else F
        if isinstance(n, dict) and n.get("k") == "bin":
            return self._join(self._ctx_taint(n.get("x"), env, ctx), self._ctx_taint(n.get("y"), env, ctx))
        if isinstance(n, dict) and n.get("k") == "template":
            ts = [self._ctx_taint(e, env, ctx) for e in n.get("exprs", [])]
            return T if T in ts else (Z if Z in ts else F)
        return self.taint(n, env)

    def _leaf_sinks(self, node, env):
        for c in self._iter_calls(node):
            callee = c.get("callee", {}); args = c.get("args", [])
            k = c.get("k")
            if k == "new" and _callee_name(callee) == "Function":     # new Function(..., body) -> code
                self._judge(c, "new Function", "code", self._join_args(args, env)); continue
            if callee.get("k") == "ident":
                nm = callee.get("name")
                if nm in CODE_IDENTS and args: self._judge(c, nm, "code", self.taint(args[0], env)); continue
                if nm in SHELL_M and args: self._judge(c, nm, "shell", self.taint(args[0], env)); continue
                if nm in SSRF_IDENTS and args: self._judge(c, nm, "ssrf", self.taint(args[0], env)); continue
                if nm in self.summaries: self._apply_summary(c, nm, args, env)
                continue
            if callee.get("k") == "member":
                prop = _prop_name(callee); base = _base_ident(callee)
                if prop in HTTP_METHODS and base in HTTP_CLIENTS and args:
                    self._judge(c, base + "." + prop, "ssrf", self.taint(args[0], env))
                elif prop in REDIRECT_M and base in RESPONSE_NAMES and args:
                    self._judge(c, prop, "redirect", self.taint(args[-1], env))
                elif prop in SHELL_M and args and base in CHILD_PROC_BASES:
                    self._judge(c, prop, "shell", self.taint(args[0], env))
                elif prop in SQL_M and args:
                    self._judge(c, prop, "sql", self.taint(args[0], env))
                elif prop in XSS_M and args and base in RESPONSE_NAMES:
                    self._judge(c, prop, "xss", self._ctx_taint(args[0], env, "xss"))
                elif prop in FILE_M and args and base in FILE_OBJS:
                    self._judge(c, prop, "file", self.taint(args[0], env))
                elif prop in self.summaries:
                    self._apply_summary(c, prop, args, env)

    def _judge(self, call, name, ctx, st):
        d = taintjudge.judge_taint(st, ctx, source="input", sink=name)   # the ONE ZTL judge
        if d in ("REFUTED", "OPEN"):
            self.sinks.append((call.get("line", 0), name, ctx, d))

    # ---------- walk ----------
    def _iter_stmts(self, body):
        for st in (body or []):
            if not isinstance(st, dict): continue
            k = st.get("k")
            if k == "block": yield from self._iter_stmts(st.get("body"))
            elif k == "if":
                yield from self._iter_stmts(st.get("body"))
                if st.get("els"): yield from self._iter_stmts([st["els"]])
            elif k == "for": yield from self._iter_stmts(st.get("body"))
            elif k == "try":
                yield from self._iter_stmts(st.get("body")); yield from self._iter_stmts(st.get("handler"))
                yield from self._iter_stmts(st.get("finalizer"))
            elif k == "switch":
                for c in st.get("cases", []): yield from self._iter_stmts(c.get("body"))
            else: yield st

    def _walk(self, body, env):
        for st in (body or []):
            if not isinstance(st, dict): continue
            k = st.get("k")
            if k == "funcref": continue                  # nested function: judged independently
            if k == "block": self._walk(st.get("body"), env); continue
            if k == "if":
                self._leaf_sinks(st.get("test"), env)
                var, neg = self._guard(st.get("test"))
                then_term = self._terminates(st.get("body"))
                e1 = dict(env); e2 = dict(env)
                if var and not neg: e1[var] = F               # positive guard narrows the THEN branch
                self._walk(st.get("body"), e1)
                if st.get("els"): self._walk([st["els"]], e2)
                if then_term:
                    for key in set(e2): env[key] = e2[key]    # continuation follows else/fallthrough
                    if var and neg: env[var] = F              # !guard { return } -> validated after
                else:
                    for key in set(e1) | set(e2):
                        env[key] = self._join(e1.get(key, env.get(key, Z)), e2.get(key, env.get(key, Z)))
                continue
            if k == "for": self._walk(st.get("body"), env); continue
            if k == "try":
                self._walk(st.get("body"), env); self._walk(st.get("handler"), env)
                self._walk(st.get("finalizer"), env); continue
            if k == "switch":
                for c in st.get("cases", []): self._walk(c.get("body"), env)
                continue
            if k == "vardecl":
                for d in st.get("decls", []):
                    if d.get("name"): env[d["name"]] = self.taint(d.get("init"), env)
            elif k == "assign":
                left = st.get("left", {})
                if left.get("k") == "ident": env[left["name"]] = self.taint(st.get("right"), env)
            self._leaf_sinks(st, env)

    # ---------- passes ----------
    def _summ_of(self, fn):
        params = [p for p in fn.get("params", []) if p]
        summ = {"sinks": {}, "passes": set(), "params": params}
        for i, p in enumerate(params):
            saved = self.sinks; self.sinks = []
            env = {p: T}; self._walk(fn.get("body"), env)
            ctxs = sorted({ctx for (_l, _m, ctx, d) in self.sinks if d == "REFUTED"})
            self.sinks = saved
            if ctxs: summ["sinks"][i] = ctxs
            for st in self._iter_stmts(fn.get("body")):
                if st.get("k") == "return" and self.taint(st.get("argument"), env) == T:
                    summ["passes"].add(i); break
        return summ

    def index(self, tree):
        for fn in tree.get("funcs", []):
            if fn.get("name"): self.summaries[fn["name"]] = self._summ_of(fn)

    def judge(self, tree):
        self.sinks = []
        for fn in tree.get("funcs", []):
            env = {p: F for p in fn.get("params", []) if p}
            self._walk(fn.get("body"), env)
        return self.sinks

    def run(self, tree): self.index(tree); return self.judge(tree)


def _ensure_parser():
    """@babel/parser must be installed next to jsast.js; fail LOUD (not silent false-green)."""
    if not os.path.isdir(os.path.join(HERE, "node_modules", "@babel", "parser")):
        raise RuntimeError("js2zfl: @babel/parser missing -- run `npm install` in " + HERE)

def parse(path):
    _ensure_parser()
    # node runs with cwd=HERE, so a RELATIVE path would resolve against the tool
    # directory and fail with ENOENT — which introspect then misreported as a
    # missing parser. Absolutise here. MEASURED 2026-09-19: 3 TS files of a
    # scanned project were silently skipped this way.
    out = subprocess.run(["node", JSAST, os.path.abspath(path)],
                         capture_output=True, text=True, timeout=60, cwd=HERE)
    if out.stdout.strip():
        return json.loads(out.stdout)
    raise RuntimeError("js2zfl: parser produced no output for %s: %s" % (path, out.stderr.strip()[:200]))

def analyze(path): return Engine().run(parse(path))

def analyze_app(paths):
    e = Engine(); trees = []
    for p in paths:
        t = parse(p)
        if t.get("funcs"): trees.append((p, t)); e.index(t)
    out = []
    for p, t in trees:
        for rec in e.judge(t): out.append((p,) + rec)
    return out

if __name__ == "__main__":
    for ln, m, ctx, d in analyze(sys.argv[1]):
        print(f"  L{ln}: {d:8} [{ctx}] {m}")
