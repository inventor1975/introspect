# -*- coding: utf-8 -*-
"""rb2zfl — Ruby module of the introspect (slice 1, 2026-09-13).
Parser: Ruby's OWN Ripper (stdlib, zero install) via the `rbast` helper (rbast.rb -> compact JSON).
Shared contract INTROSPECT-SEMANTICS.md: zero-trust F/T/Z -> REFUTED/OPEN/EARNED, honest OPEN.
Slice1: Rails/Sinatra sources (params, params[:x], request.params/GET/POST, cookies) -> sinks
(system/exec/`backticks`=shell, eval/instance_eval=code, AR where/find_by_sql/execute=sql,
raw/html_safe=xss, File.*=file, open/Net::HTTP=ssrf); string-interpolation + concat propagation,
cross-method + cross-file SUMMARIES, branch-join. Sixth language after php/py/java/go/js."""
import json, subprocess, os, sys
F, T, Z = "F", "T", "Z"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # tool/ -> shared taint->ZFL->judge adapter
import taintjudge
RBAST = os.path.join(HERE, "rbast.rb")

SOURCE_IDENTS = {"params", "cookies"}                 # Rails bare sources (params[:x], cookies[:x])
REQ_SOURCE_MEMBERS = {"params", "GET", "POST", "query_parameters", "request_parameters",
                      "body", "cookies", "query_string", "referer", "user_agent", "path_parameters"}
REQUEST_BASES = {"request", "req"}
# sinks
SHELL_IDENTS = {"system", "exec", "spawn", "syscall"}         # Kernel command execution
CODE_IDENTS = {"eval"}
XSS_IDENTS = {"raw"}                                          # ActionView raw() bypasses escaping
SSRF_IDENTS = {"open"}                                        # Kernel#open(url/"|cmd"): classic Ruby vuln
# raw SQL methods take a SQL string -> always a sink (T=REFUTED, Z=OPEN honest).
SQL_RAW = {"find_by_sql", "execute", "exec_query"}
# conditional methods are SAFE with a hash/array (where(active: true)); only a TAINTED STRING is the
# injection -> report ONLY T (suppress Z/OPEN so safe hash-conditions are not noise).
SQL_COND = {"where", "order", "group", "having", "select", "from", "joins", "pluck",
            "find_by", "exists?", "calculate", "reorder", "having"}
CODE_METHODS = {"instance_eval", "class_eval", "module_eval", "eval"}
XSS_MEMBER = {"html_safe"}                                    # x.html_safe -> xss on x's taint
# context-aware escapers: neutralise ONE context, transparent for others
CTX_SANITIZERS = {"html_escape": "xss", "html_escape_once": "xss", "escapeHTML": "xss", "h": "xss",
                  "escape_html": "xss", "sanitize": "xss", "escape_javascript": "js", "j": "js"}
FILE_BASES = {"File", "IO"}
FILE_METHODS = {"open", "read", "write", "new", "readlines", "binread"}
HTTP_BASES = {"Net", "HTTParty", "RestClient", "Faraday"}
HTTP_METHODS = {"get", "post", "get_response", "start", "get_print"}
CONV_IDENTS = {"String", "to_s"}                             # transparent-ish


def _base_ident(n):
    while isinstance(n, dict) and n.get("k") in ("member", "aref"):
        n = n.get("object", {})
    return n.get("name") if isinstance(n, dict) and n.get("k") == "ident" else None


class Engine:
    def __init__(self):
        self.summaries = {}
        self.sinks = []

    def _join(self, a, b): return T if T in (a, b) else (Z if Z in (a, b) else F)

    def _terminates(self, body):
        if isinstance(body, list) and body:
            last = body[-1]
            return isinstance(last, dict) and last.get("k") == "return"
        return False

    def _guard(self, test):
        """(var, negated): x == "c" | allow.include?(x) | !<either>."""
        n = test; neg = False
        if isinstance(n, dict) and n.get("k") == "unary" and n.get("op") in ("!", "not"):
            neg = True; n = n.get("x", {})
        if isinstance(n, dict) and n.get("k") == "bin" and n.get("op") in ("==", "!=", "eql?"):
            eq = n.get("op") == "=="
            for a, b in ((n.get("x"), n.get("y")), (n.get("y"), n.get("x"))):
                if isinstance(a, dict) and a.get("k") == "ident" and isinstance(b, dict) and b.get("k") == "lit":
                    return (a.get("name"), neg if eq else (not neg))
        if isinstance(n, dict) and n.get("k") == "call":
            callee = n.get("callee", {}); args = n.get("args", [])
            if callee.get("k") == "member" and callee.get("prop") in ("include?", "member?", "cover?") \
                    and args and isinstance(args[0], dict) and args[0].get("k") == "ident":
                return (args[0].get("name"), neg)
        return (None, False)

    # ---------- taint ----------
    def taint(self, n, env):
        if not isinstance(n, dict): return F
        k = n.get("k")
        if k == "lit": return F
        if k == "ident":
            nm = n.get("name")
            return T if nm in SOURCE_IDENTS else env.get(nm, Z)
        if k == "aref": return self.taint(n.get("object"), env)   # params[:x] -> taint of params
        if k == "bin": return self._join(self.taint(n.get("x"), env), self.taint(n.get("y"), env))
        if k in ("template", "xstring"):
            ts = [self.taint(e, env) for e in n.get("exprs", [])]
            return T if T in ts else (Z if Z in ts else F)
        if k == "array":
            ts = [self.taint(e, env) for e in n.get("elts", [])]
            return T if T in ts else (Z if Z in ts else F)
        if k == "unary": return F
        if k == "assignexpr": return self.taint(n.get("right"), env)
        if k == "member":
            if n.get("prop") in REQ_SOURCE_MEMBERS and _base_ident(n.get("object")) in REQUEST_BASES:
                return T
            return Z
        if k == "call": return self._call_taint(n, env)
        return Z if k in ("funcref", "other") else F

    def _call_taint(self, n, env):
        callee = n.get("callee", {}); args = n.get("args", [])
        if callee.get("k") == "ident":
            nm = callee.get("name")
            if nm in CONV_IDENTS: return self.taint(args[0], env) if args else F
            if nm in self.summaries:
                for i in self.summaries[nm]["passes"]:
                    if i < len(args) and self.taint(args[i], env) == T: return T
                return F
        if callee.get("k") == "member":
            prop = callee.get("prop")
            if prop in CONV_IDENTS or prop in ("to_s", "strip", "chomp", "downcase", "upcase"):
                return self.taint(callee.get("object"), env)      # transparent string transforms
            if prop in self.summaries:
                for i in self.summaries[prop]["passes"]:
                    if i < len(args) and self.taint(args[i], env) == T: return T
        return Z

    def _ctx_taint(self, n, env, ctx):
        if isinstance(n, dict) and n.get("k") == "call":
            callee = n.get("callee", {})
            nm = callee.get("name") if callee.get("k") == "ident" else callee.get("prop")
            if nm in CTX_SANITIZERS:
                if CTX_SANITIZERS[nm] == ctx: return F
                a = n.get("args", [])
                return self.taint(a[0], env) if a else F
        if isinstance(n, dict) and n.get("k") == "bin":
            return self._join(self._ctx_taint(n.get("x"), env, ctx), self._ctx_taint(n.get("y"), env, ctx))
        if isinstance(n, dict) and n.get("k") in ("template", "xstring"):
            ts = [self._ctx_taint(e, env, ctx) for e in n.get("exprs", [])]
            return T if T in ts else (Z if Z in ts else F)
        return self.taint(n, env)

    # ---------- sinks ----------
    def _iter_nodes(self, n):
        if isinstance(n, dict):
            yield n
            for v in n.values(): yield from self._iter_nodes(v)
        elif isinstance(n, list):
            for x in n: yield from self._iter_nodes(x)

    def _join_args(self, args, env):
        ts = [self.taint(a, env) for a in args]
        return T if T in ts else (Z if Z in ts else F)

    def _apply_summary(self, call, name, args, env):
        for i, ctxs in self.summaries[name]["sinks"].items():
            if i < len(args):
                sti = self.taint(args[i], env)
                for cx in ctxs: self._judge(call, name + "()->sink", cx, sti)

    def _leaf_sinks(self, node, env):
        for c in self._iter_nodes(node):
            k = c.get("k")
            if k == "xstring":
                ts = [self.taint(e, env) for e in c.get("exprs", [])]
                self._judge(c, "`backticks`", "shell", T if T in ts else (Z if Z in ts else F))
            elif k == "member" and c.get("prop") in XSS_MEMBER:
                self._judge(c, c.get("prop"), "xss", self._ctx_taint(c.get("object"), env, "xss"))
            elif k == "call":
                callee = c.get("callee", {}); args = c.get("args", [])
                if callee.get("k") == "ident":
                    nm = callee.get("name")
                    if nm in SHELL_IDENTS and args: self._judge(c, nm, "shell", self._join_args(args, env))
                    elif nm in CODE_IDENTS and args: self._judge(c, nm, "code", self.taint(args[0], env))
                    elif nm in XSS_IDENTS and args: self._judge(c, nm, "xss", self._ctx_taint(args[0], env, "xss"))
                    elif nm in SSRF_IDENTS and args: self._judge(c, nm, "ssrf", self.taint(args[0], env))
                    elif nm in self.summaries: self._apply_summary(c, nm, args, env)
                elif callee.get("k") == "member":
                    prop = callee.get("prop"); base = _base_ident(callee.get("object"))
                    if prop in SQL_RAW and args:
                        self._judge(c, prop, "sql", self._join_args(args, env))
                    elif prop in SQL_COND and args and isinstance(args[0], dict) \
                            and args[0].get("k") in ("template", "bin") and self.taint(args[0], env) == T:
                        self._judge(c, prop, "sql", T)          # ONLY interpolated/concatenated STRING conditions;
                        #                                         where(id: params[:id]) is a SAFE hash -> not a sink
                    elif prop in CODE_METHODS and args:
                        self._judge(c, prop, "code", self.taint(args[0], env))
                    elif prop in FILE_METHODS and base in FILE_BASES and args:
                        self._judge(c, base + "." + prop, "file", self.taint(args[0], env))
                    elif prop in HTTP_METHODS and base in HTTP_BASES and args:
                        self._judge(c, base + "." + prop, "ssrf", self.taint(args[0], env))
                    elif prop == "popen" and base == "IO" and args:
                        self._judge(c, "IO.popen", "shell", self.taint(args[0], env))
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
            elif k == "switch":
                for c in st.get("cases", []): yield from self._iter_stmts(c.get("body"))
            else: yield st

    def _walk(self, body, env):
        for st in (body or []):
            if not isinstance(st, dict): continue
            k = st.get("k")
            if k == "funcref": continue
            if k == "block": self._walk(st.get("body"), env); continue
            if k == "if":
                self._leaf_sinks(st.get("test"), env)
                var, neg = self._guard(st.get("test"))
                then_term = self._terminates(st.get("body"))
                e1 = dict(env); e2 = dict(env)
                if var and not neg: e1[var] = F
                self._walk(st.get("body"), e1)
                if st.get("els"): self._walk([st["els"]], e2)
                if then_term:
                    for key in set(e2): env[key] = e2[key]
                    if var and neg: env[var] = F
                else:
                    for key in set(e1) | set(e2):
                        env[key] = self._join(e1.get(key, env.get(key, Z)), e2.get(key, env.get(key, Z)))
                continue
            if k == "for": self._walk(st.get("body"), env); continue
            if k == "switch":
                for c in st.get("cases", []): self._walk(c.get("body"), env)
                continue
            if k == "assign":
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
            if fn.get("name") and fn["name"] != "<top>":
                self.summaries[fn["name"]] = self._summ_of(fn)

    def judge(self, tree):
        self.sinks = []
        for fn in tree.get("funcs", []):
            env = {p: F for p in fn.get("params", []) if p}
            self._walk(fn.get("body"), env)
        return self.sinks

    def run(self, tree): self.index(tree); return self.judge(tree)


def parse(path):
    try:
        out = subprocess.run(["ruby", RBAST, path], capture_output=True, text=True, timeout=60)
    except FileNotFoundError:
        raise RuntimeError("rb2zfl: `ruby` not found -- Ruby (with stdlib Ripper) is required")
    if out.stdout.strip():
        return json.loads(out.stdout)
    raise RuntimeError("rb2zfl: parser produced no output for %s: %s" % (path, out.stderr.strip()[:200]))

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
