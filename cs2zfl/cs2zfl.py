# -*- coding: utf-8 -*-
"""cs2zfl — C# module of the introspect (slice 1, 2026-09-13).
Parser: C#'s OWN Roslyn via the `csast` helper (dotnet, Microsoft.CodeAnalysis.CSharp -> compact JSON).
Shared contract INTROSPECT-SEMANTICS.md: zero-trust F/T/Z -> REFUTED/OPEN/EARNED, honest OPEN.
Slice1: ASP.NET sources (Request.Query/Form/..., [FromQuery]/[FromRoute]/[FromBody] + bare action params)
-> sinks: Process.Start=shell, new SqlCommand(concat)/.CommandText=sql, Response.Write/Html.Raw/new
HtmlString=xss, File.*=file, *.Deserialize=deser; string concat + interpolation, context-aware html
escapers (HttpUtility.HtmlEncode), cross-method + cross-file SUMMARIES, guards, branch-join.
Seventh language after php/py/java/go/js/ruby."""
import json, subprocess, os, sys
F, T, Z = "F", "T", "Z"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # tool/ -> shared taint->ZFL->judge adapter
import taintjudge
CSAST = os.path.join(HERE, "csast", "bin", "pub", "csast")

REQUEST_BASES = {"Request", "httpContext", "HttpContext", "context"}
REQ_SOURCE_MEMBERS = {"Query", "Form", "QueryString", "Params", "Headers", "Cookies",
                      "RouteValues", "ServerVariables", "InputStream"}
FROM_ATTRS = {"FromQuery", "FromRoute", "FromBody", "FromForm", "FromHeader"}
SIMPLE_TYPES = {"string", "String", "int", "Int32", "long", "Int64", "short", "byte", "bool",
                "Boolean", "double", "float", "decimal", "Guid", "string[]", "int?"}
# sinks
SHELL = {("Process", "Start")}                        # Process.Start(file, args)
XSS_MEMBER = {("Response", "Write"), ("Response", "WriteAsync"), ("Html", "Raw"), ("HtmlHelper", "Raw")}
FILE_BASES = {"File"}
FILE_METHODS = {"ReadAllText", "ReadAllBytes", "ReadAllLines", "WriteAllText", "WriteAllBytes",
                "AppendAllText", "OpenRead", "OpenWrite", "Open", "Create"}
DESER_METHODS = {"Deserialize"}                       # BinaryFormatter/LosFormatter/JavaScriptSerializer.Deserialize
SQL_CMD_TYPES = {"SqlCommand", "MySqlCommand", "NpgsqlCommand", "OleDbCommand", "SqlDataAdapter",
                 "OdbcCommand", "SQLiteCommand"}
XSS_NEW_TYPES = {"HtmlString", "MvcHtmlString"}
FILE_NEW_TYPES = {"StreamReader", "StreamWriter", "FileStream"}
# context-aware escapers: neutralise ONE context, transparent for others
CTX_SANITIZERS = {"HtmlEncode": "xss", "HtmlAttributeEncode": "xss", "JavaScriptStringEncode": "xss",
                  "Encode": "xss", "UrlEncode": "url", "UrlPathEncode": "url"}
CONV_IDENTS = {"Convert", "ToString"}
# transparent transforms: PRESERVE taint (decode/encode/case/trim), NOT sanitizers
TRANSPARENT_METHODS = {"FromBase64String", "ToBase64String", "GetString", "GetBytes", "Trim", "TrimStart",
                       "TrimEnd", "ToLower", "ToUpper", "ToLowerInvariant", "ToUpperInvariant",
                       "Substring", "Replace", "ToString", "Decode", "Normalize", "PadLeft", "PadRight"}


def _prop(member): return member.get("prop") if isinstance(member, dict) else None

def _base_ident(n):
    while isinstance(n, dict) and n.get("k") in ("member", "index"):
        n = n.get("object", {})
    return n.get("name") if isinstance(n, dict) and n.get("k") == "ident" else None

def _callee_name(callee):
    if not isinstance(callee, dict): return None
    if callee.get("k") == "ident": return callee.get("name")
    if callee.get("k") == "member": return callee.get("prop")
    return None


class Engine:
    def __init__(self):
        self.summaries = {}
        self.sinks = []

    def _join(self, a, b): return T if T in (a, b) else (Z if Z in (a, b) else F)

    def _terminates(self, body):
        if isinstance(body, list) and body:
            return isinstance(body[-1], dict) and body[-1].get("k") in ("return", "throw")
        return False

    def _guard(self, test):
        n = test; neg = False
        if isinstance(n, dict) and n.get("k") == "unary" and n.get("op") == "!":
            neg = True; n = n.get("x", {})
        if isinstance(n, dict) and n.get("k") == "bin" and n.get("op") in ("==", "!="):
            eq = n.get("op") == "=="
            for a, b in ((n.get("x"), n.get("y")), (n.get("y"), n.get("x"))):
                if isinstance(a, dict) and a.get("k") == "ident" and isinstance(b, dict) and b.get("k") == "lit":
                    return (a.get("name"), neg if eq else (not neg))
        if isinstance(n, dict) and n.get("k") == "call":
            callee = n.get("callee", {}); args = n.get("args", [])
            if _prop(callee) in ("Contains", "ContainsKey", "Any") and args \
                    and isinstance(args[0], dict) and args[0].get("k") == "ident":
                return (args[0].get("name"), neg)
        return (None, False)

    # ---------- taint ----------
    def taint(self, n, env):
        if not isinstance(n, dict): return F
        k = n.get("k")
        if k == "lit": return F
        if k == "ident": return env.get(n.get("name"), Z)
        if k == "index":                                              # Request.Query["x"] / Request["x"]
            obj = n.get("object", {})
            if isinstance(obj, dict) and obj.get("k") == "ident" and obj.get("name") in REQUEST_BASES:
                return T                                                  # Request["x"] indexer (WebForms)
            return self.taint(obj, env)
        if k == "bin": return self._join(self.taint(n.get("x"), env), self.taint(n.get("y"), env))
        if k == "template":
            ts = [self.taint(e, env) for e in n.get("exprs", [])]
            return T if T in ts else (Z if Z in ts else F)
        if k in ("await",): return self.taint(n.get("x"), env)
        if k == "cond": return self._join(self.taint(n.get("x"), env), self.taint(n.get("y"), env))
        if k == "assignexpr": return self.taint(n.get("right"), env)
        if k == "unary": return F
        if k == "array":
            ts = [self.taint(e, env) for e in n.get("elts", [])]
            return T if T in ts else (Z if Z in ts else F)
        if k == "member":
            if _prop(n) in REQ_SOURCE_MEMBERS and _base_ident(n) in REQUEST_BASES: return T
            return self.taint(n.get("object"), env)                   # propagate (Request.Form.Get chains)
        if k in ("call", "new"): return self._call_taint(n, env)
        return Z if k in ("funcref", "other") else F

    def _call_taint(self, n, env):
        callee = n.get("callee", {}); args = n.get("args", [])
        cn = _callee_name(callee)
        if cn in CTX_SANITIZERS:                          # as a value, an escaper is transparent; the
            return self.taint(args[0], env) if args else F  # context-clearing happens at the sink (_ctx_taint)
        if cn in TRANSPARENT_METHODS:                     # decode/case/trim: preserve taint from arg or receiver
            if args: return self.taint(args[0], env)
            if callee.get("k") == "member": return self.taint(callee.get("object"), env)
            return F
        if cn in self.summaries:
            for i in self.summaries[cn]["passes"]:
                if i < len(args) and self.taint(args[i], env) == T: return T
            return F
        if n.get("k") == "new":                                       # transparent-ish ctor for e.g. StringBuilder
            ts = [self.taint(a, env) for a in args]
            return T if T in ts else (Z if Z in ts else F) if ts else F
        return Z

    def _ctx_taint(self, node, env, ctx):
        """Taint for a sink of context `ctx`, crediting a context-matching escaper (transparent for others),
        recursing through concat/interpolation so `"a" + HtmlEncode(x) + "b"` is clean for xss."""
        if not isinstance(node, dict): return F
        k = node.get("k")
        if k == "call":
            nm = _callee_name(node.get("callee", {}))
            if nm in CTX_SANITIZERS:
                if CTX_SANITIZERS[nm] == ctx: return F
                a = node.get("args", [])
                return self.taint(a[0], env) if a else F
        if k == "bin":
            return self._join(self._ctx_taint(node.get("x"), env, ctx), self._ctx_taint(node.get("y"), env, ctx))
        if k == "template":
            ts = [self._ctx_taint(e, env, ctx) for e in node.get("exprs", [])]
            return T if T in ts else (Z if Z in ts else F)
        return self.taint(node, env)

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

    def _leaf_sinks(self, node, env):
        for c in self._iter_calls(node):
            args = c.get("args", [])
            if c.get("k") == "new":
                typ = c.get("type", "").split("<")[0].split(".")[-1]
                if (typ.endswith("Command") or typ.endswith("DataAdapter")) and args:
                    self._judge(c, "new " + typ, "sql", self._ctx_taint(args[0], env, "sql"))
                elif typ in XSS_NEW_TYPES and args:
                    self._judge(c, "new " + typ, "xss", self._ctx_taint(args[0], env, "xss"))
                elif typ in FILE_NEW_TYPES and args:
                    self._judge(c, "new " + typ, "file", self.taint(args[0], env))
                continue
            callee = c.get("callee", {})
            if callee.get("k") == "member":
                prop = callee.get("prop"); base = _base_ident(callee.get("object"))
                if (base, prop) in SHELL:
                    self._judge(c, base + "." + prop, "shell", self._join_args(args, env))
                elif (base, prop) in XSS_MEMBER and args:
                    self._judge(c, prop, "xss", self._ctx_taint(args[0], env, "xss"))
                elif base in FILE_BASES and prop in FILE_METHODS and args:
                    self._judge(c, base + "." + prop, "file", self.taint(args[0], env))
                elif prop in DESER_METHODS and args:
                    self._judge(c, prop, "deser", self.taint(args[0], env))
                elif prop in self.summaries:
                    self._apply_summary(c, prop, args, env)
            elif callee.get("k") == "ident":
                nm = callee.get("name")
                if nm in self.summaries: self._apply_summary(c, nm, args, env)

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
                if left.get("k") == "ident":
                    env[left["name"]] = self.taint(st.get("right"), env)
                elif left.get("k") == "member" and left.get("prop") == "CommandText":   # cmd.CommandText = concat
                    self._judge(st, "CommandText", "sql", self._ctx_taint(st.get("right"), env, "sql"))
            self._leaf_sinks(st, env)

    # ---------- passes ----------
    def _param_source(self, p, action):
        attrs = p.get("attrs", []) or []
        if any(a in FROM_ATTRS for a in attrs): return True
        if action and p.get("typ", "").split("<")[0] in SIMPLE_TYPES and not attrs: return True
        return False

    def _summ_of(self, fn):
        params = [p.get("name") for p in fn.get("params", []) if p.get("name")]
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
            action = fn.get("action", False)
            env = {p["name"]: (T if self._param_source(p, action) else F)
                   for p in fn.get("params", []) if p.get("name")}
            self._walk(fn.get("body"), env)
        return self.sinks

    def run(self, tree): self.index(tree); return self.judge(tree)


def parse(path):
    if not os.path.exists(CSAST):
        raise RuntimeError("cs2zfl: csast helper not built -- run `dotnet build -c Release -o bin/pub` in csast/")
    out = subprocess.run([CSAST, path], capture_output=True, text=True, timeout=60)
    if out.stdout.strip(): return json.loads(out.stdout)
    raise RuntimeError("cs2zfl: parser produced no output for %s: %s" % (path, out.stderr.strip()[:200]))

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
