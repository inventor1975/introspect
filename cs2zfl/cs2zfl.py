# -*- coding: utf-8 -*-
"""cs2zfl — C# module of the introspect (slice 1, 2026-09-13).
Parser: C#'s OWN Roslyn via the `csast` helper (dotnet, Microsoft.CodeAnalysis.CSharp -> compact JSON).
Shared contract INTROSPECT-SEMANTICS.md: zero-trust F/T/Z -> REFUTED/OPEN/EARNED, honest OPEN.
Slice1: ASP.NET sources (Request.Query/Form/..., [FromQuery]/[FromRoute]/[FromBody] + bare action params)
-> sinks: Process.Start=shell, new SqlCommand(concat)/.CommandText=sql, Response.Write/Html.Raw/new
HtmlString=xss, File.*=file, *.Deserialize=deser; string concat + interpolation, context-aware html
escapers (HttpUtility.HtmlEncode), cross-method + cross-file SUMMARIES, guards, branch-join.
Seventh language after php/py/java/go/js/ruby.
Slice 2 (2026-09-27), the java2zfl soundness lesson ported: tri-valued summaries with a parameter-free
base, returns captured where they happen, OPEN sink effects kept, same-name methods that disagree -> Z,
summaries to a fixpoint; try/catch, switch and loops joined (break/continue reach the exit); foreach binds
its variable; `+=` joins; o.P = v / d[k] = v / sb.Append(v) fold; a transparent call keeps its RECEIVER's
taint (s.Replace("a","b") read only its first argument, so a tainted s became F); escapers tag one context
and the program's own Encode(..) wins over the catalogue's; comparisons and arithmetic give F."""
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


_RANK = {F: 0, Z: 1, T: 2}
_DRANK = {"EARNED": 0, "OPEN": 1, "REFUTED": 2}
# of the transparent methods, those whose ARGUMENTS are content too (Substring(i, j)'s are numbers)
ARG_CONTENT = {"Replace", "Insert", "Format", "Concat", "Join", "FromBase64String", "ToBase64String", "GetString",
               "GetBytes", "Decode", "UrlDecode", "HtmlDecode", "Combine", "ToString"}
NUMERIC_RESULT = {"ToInt32", "ToInt64", "ToInt16", "ToDouble", "ToDecimal", "ToBoolean", "Parse", "TryParse",
                  "Length", "Count", "Contains", "StartsWith", "EndsWith", "Equals", "IndexOf", "LastIndexOf",
                  "IsNullOrEmpty", "IsNullOrWhiteSpace", "Any", "All", "CompareTo", "GetHashCode", "Exists"}
# calls on a local that store their argument in it
MUTATORS = {"Append", "AppendLine", "AppendFormat", "Insert", "Add", "AddRange", "Push", "Enqueue", "Set",
            "Write", "WriteLine", "TryAdd"}


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

def _path(n):
    parts = []
    while isinstance(n, dict) and n.get("k") == "member":
        parts.append(n.get("prop")); n = n.get("object", {})
    if isinstance(n, dict) and n.get("k") == "ident" and parts and all(parts):
        return ".".join([n["name"]] + parts[::-1])
    return None


class Engine:
    def __init__(self):
        self.summaries = {}   # name -> [summary]
        self.funcs = {}
        self.sinks = []
        self._rets = None
        self._esc = []
        self._dirty = False

    def _join(self, a, b): return join(a, b)

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

    def _is_class(self, n, env):
        """A static receiver (Encoding.UTF8, Convert, HttpUtility): a type, not data."""
        b = _base_ident(n)
        return b is not None and b not in env and b[:1].isupper() and b not in REQUEST_BASES

    # ---------- taint ----------
    def taint(self, n, env):
        if not isinstance(n, dict): return F
        k = n.get("k")
        if k in ("lit", "nil"): return F
        if k == "ident": return env.get(n.get("name"), Z)
        if k == "index":                                              # Request.Query["x"] / Request["x"]
            obj = n.get("object", {})
            if isinstance(obj, dict) and obj.get("k") == "ident" and obj.get("name") in REQUEST_BASES:
                return T                                                  # Request["x"] indexer (WebForms)
            return self.taint(obj, env)
        if k == "bin":
            if n.get("op") in ("==", "!=", "<", ">", "<=", ">=", "is", "as", "-", "*", "/", "%", "&", "|", "^",
                               "<<", ">>"):
                return F
            return join(self.taint(n.get("x"), env), self.taint(n.get("y"), env))    # + && || ??
        if k == "template": return join(*[self.taint(e, env) for e in n.get("exprs", [])])
        if k == "await": return self.taint(n.get("x"), env)
        if k == "cond": return join(self.taint(n.get("x"), env), self.taint(n.get("y"), env))
        if k == "assignexpr": return self.taint(n.get("right"), env)
        if k == "unary": return F
        if k == "array": return join(*[self.taint(e, env) for e in n.get("elts", [])])
        if k == "member":
            p = _path(n)
            if p is not None and p in env: return env[p]
            if _prop(n) in REQ_SOURCE_MEMBERS and _base_ident(n) in REQUEST_BASES: return T
            if _prop(n) in NUMERIC_RESULT: return F
            if self._is_class(n, env): return Z                        # a static member: unknown
            return self.taint(n.get("object"), env)                   # propagate (Request.Form.Get chains)
        if k in ("call", "new"): return self._call_taint(n, env)
        return Z                                                      # funcref, other: unknown

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

    def _call_taint(self, n, env):
        callee = n.get("callee", {}); args = n.get("args", [])
        if n.get("k") == "new":                                       # StringBuilder(x) etc: transparent-ish
            return join(*[self.taint(a, env) for a in args]) if args else F
        cn = _callee_name(callee)
        own = callee.get("k") == "ident" and self._sums(cn)
        if cn in CTX_SANITIZERS and not own:                         # the program's own Encode(..) wins
            return _clean_for(join(*[self.taint(a, env) for a in args]), CTX_SANITIZERS[cn])
        if own: return self._apply(self._sums(cn), args, env)
        if cn in NUMERIC_RESULT: return F
        recv = F
        if callee.get("k") == "member":
            obj = callee.get("object")
            recv = F if self._is_class(obj, env) else self.taint(obj, env)
        if cn in TRANSPARENT_METHODS or cn in ARG_CONTENT:
            if cn in ARG_CONTENT: return join(recv, *[self.taint(a, env) for a in args])
            return recv
        sums = self._sums(cn)
        if sums is not None: return self._apply(sums, args, env)
        return Z

    def _ctx_taint(self, node, env, ctx):
        return _at(self.taint(node, env), ctx)

    # ---------- sinks ----------
    def _iter_calls(self, n):
        if isinstance(n, dict):
            if n.get("k") in ("call", "new"): yield n
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
                elif self._sums(prop) and prop not in TRANSPARENT_METHODS | ARG_CONTENT | NUMERIC_RESULT | MUTATORS:
                    self._apply_summary(c, prop, args, env)
            elif callee.get("k") == "ident":
                nm = callee.get("name")
                if self._sums(nm): self._apply_summary(c, nm, args, env)

    def _judge(self, call, name, ctx, st):
        st = _at(st, ctx)
        d = taintjudge.judge_taint(st, ctx, source="input", sink=name)   # the ONE ZTL judge
        if d in ("REFUTED", "OPEN", "EARNED"):
            self.sinks.append((call.get("line", 0), name, ctx, d))

    # ---------- effects ----------
    def _assign_to(self, left, v, env, op):
        compound = op not in (None, "=")
        if not isinstance(left, dict): return
        if left.get("k") == "ident":
            nm = left["name"]; env[nm] = join(env.get(nm, Z), v) if compound else v
        elif left.get("k") == "member":
            p = _path(left)
            if p is not None: env[p] = join(env.get(p, Z), v) if compound else v
            r = _base_ident(left)
            if r is not None and r in env: env[r] = join(env[r], F if v == F else Z)
        elif left.get("k") == "index":                              # d["k"] = v: the collection holds v
            r = _base_ident(left)
            if r is not None: env[r] = join(env.get(r, F), v)

    def _effects(self, node, env):
        if isinstance(node, dict):
            if node.get("k") == "assignexpr":
                self._effects(node.get("right"), env)
                self._assign_to(node.get("left"), self.taint(node.get("right"), env), env, node.get("op"))
                return
            if node.get("k") in ("call", "new"):
                for a in node.get("args", []): self._effects(a, env)
                callee = node.get("callee", {})
                if isinstance(callee, dict) and callee.get("k") == "member":
                    self._effects(callee.get("object"), env)
                    obj = callee.get("object", {}); m = callee.get("prop")
                    if isinstance(obj, dict) and obj.get("k") == "ident" and obj.get("name") in env:
                        vs = [self.taint(a, env) for a in node.get("args", [])]
                        if m in MUTATORS: env[obj["name"]] = join(env[obj["name"]], *vs)
                        elif m not in TRANSPARENT_METHODS and m not in ARG_CONTENT and m not in NUMERIC_RESULT \
                                and any(x != F for x in vs):
                            env[obj["name"]] = join(env[obj["name"]], Z)
                return
            for v in node.values(): self._effects(v, env)
        elif isinstance(node, list):
            for x in node: self._effects(x, env)

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
                self._leaf_sinks(st.get("test"), env); self._effects(st.get("test"), env)
                var, neg = self._guard(st.get("test"))
                then_term = self._terminates(st.get("body"))
                e1 = dict(env); e2 = dict(env)
                if var and not neg: e1[var] = F
                self._walk(st.get("body"), e1)
                if st.get("els"): self._walk([st["els"]], e2)
                if then_term:
                    _set_env(env, e2)
                    if var and neg: env[var] = F
                else:
                    _set_env(env, _ejoin(e1, e2))
                continue
            if k == "for":
                def head(e):
                    if st.get("test"): self._leaf_sinks(st["test"], e); self._effects(st["test"], e)
                    if st.get("left"):
                        v = self.taint(st.get("iter"), e)
                        for nm in st["left"]: e[nm] = v
                esc = []; self._esc.append(esc)
                try:
                    e0 = dict(env)
                    e1 = dict(env); head(e1); self._walk(st.get("body"), e1)
                    e2 = _ejoin(e0, e1, *esc)
                    e3 = dict(e2); head(e3); self._walk(st.get("body"), e3)
                    _set_env(env, _ejoin(e2, e3, *esc))
                finally:
                    self._esc.pop()
                continue
            if k in ("break", "continue"):
                if self._esc:
                    for lv in (self._esc if k == "continue" else self._esc[-1:]): lv.append(dict(env))
                continue
            if k == "try":
                e_try = dict(env); self._walk(st.get("body"), e_try)
                eh = _ejoin(env, e_try)
                for nm in st.get("param") or []: eh[nm] = Z
                self._walk(st.get("handler"), eh)
                new = _ejoin(e_try, eh) if st.get("handler") else e_try
                self._walk(st.get("finalizer"), new)
                _set_env(env, new); continue
            if k == "switch":
                self._leaf_sinks(st.get("disc"), env); self._effects(st.get("disc"), env)
                esc = []; self._esc.append(esc)
                try:
                    outs, has_default = [], False
                    for c in st.get("cases", []):                 # C#: no implicit fallthrough
                        if c.get("isdefault"): has_default = True
                        e = dict(env); self._walk(c.get("body"), e)
                        last = (c.get("body") or [{}])[-1] if c.get("body") else {}
                        if not (isinstance(last, dict) and last.get("k") in ("break", "return", "throw", "continue")):
                            outs.append(e)
                    if not has_default: outs.append(dict(env))
                    outs += esc
                    _set_env(env, _ejoin(*outs) if outs else env)
                finally:
                    self._esc.pop()
                continue
            if k == "vardecl":
                for d in st.get("decls", []):
                    self._effects(d.get("init"), env)
                    if d.get("name"):
                        init = d.get("init")
                        env[d["name"]] = self.taint(init, env) if isinstance(init, dict) and init.get("k") != "nil" else Z
            elif k == "assign":
                self._effects(st.get("right"), env)
                left = st.get("left", {})
                v = self.taint(st.get("right"), env)
                self._assign_to(left, v, env, st.get("op"))
                if left.get("k") == "member" and left.get("prop") == "CommandText":   # cmd.CommandText = concat
                    self._judge(st, "CommandText", "sql", self._ctx_taint(st.get("right"), env, "sql"))
            elif k in ("return", "throw", "exprstmt"):
                self._effects(st.get("argument") if k != "exprstmt" else st.get("x"), env)
                if k == "return" and self._rets is not None:
                    a = st.get("argument")
                    self._rets.append(self.taint(a, env) if isinstance(a, dict) and a.get("k") != "nil" else F)
            self._leaf_sinks(st, env)

    # ---------- passes ----------
    def _param_source(self, p, action):
        attrs = p.get("attrs", []) or []
        if any(a in FROM_ATTRS for a in attrs): return True
        if action and p.get("typ", "").split("<")[0] in SIMPLE_TYPES and not attrs: return True
        return False

    def _summ_of(self, fn):
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
            base, bs = run({p: F for p in params if p})
            summ = {"sinks": {}, "passes": set(), "params": params, "base": base, "ret": []}
            for i, p in enumerate(params):
                env = {q: F for q in params if q}
                if p: env[p] = T
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
            action = fn.get("action", False)
            env = {p["name"]: (T if self._param_source(p, action) else F)
                   for p in fn.get("params", []) if p.get("name")}
            self._rets = None
            self._walk(fn.get("body"), env)
        best, order = {}, []
        for rec in self.sinks:
            key = rec[:3]
            if key not in best: order.append(key); best[key] = rec
            elif _DRANK[rec[3]] > _DRANK[best[key][3]]: best[key] = rec
        self.sinks = [best[key] for key in order if best[key][3] != "EARNED"]
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
