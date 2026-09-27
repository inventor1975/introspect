# -*- coding: utf-8 -*-
"""js2zfl — JavaScript/TypeScript module of the introspect (slices 1-2 + calibration, 2026-09-13).
Parser: @babel/parser via the `jsast` helper (jsast.js -> compact JSON tree; handles JS/JSX/TS/TSX).
Shared contract INTROSPECT-SEMANTICS.md: zero-trust F/T/Z -> REFUTED/OPEN/EARNED, honest OPEN.
Slice1: Express/Node sources (req.query/params/body/headers/cookies, req.get/param) -> sinks
(child_process exec/spawn=shell, eval / new Function=code, .query/.execute=sql, res.send/render=xss,
fs.*=file); string-concat + template-literal propagation, cross-function + cross-file SUMMARIES,
branch-join. Slice2: ssrf (HTTP clients, receiver-gated) + open-redirect sinks, guards
(=== / .includes/.has / negated-return), child_process-gated shell (regex.exec collision fix).
Fifth language after php2zfl/py2zfl/java2zfl/go2zfl.
Slice 3 (2026-09-27), the java2zfl soundness lesson ported: tri-valued summaries with a parameter-free
base, returns captured where they happen, OPEN sink effects kept, same-name functions that disagree ->
Z, summaries to a fixpoint; try/catch, switch and loops joined (break/continue reach the exit); `+=`
joins; o.f = v and arr.push(v) fold into the object; destructuring and for-of bind their names;
escapers tag one context; numeric/boolean operators give F; unmodelled expressions are Z."""
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

def _path(n):
    """'o.f.g' for a non-computed member chain on an identifier, else None."""
    parts = []
    while isinstance(n, dict) and n.get("k") == "member":
        if n.get("computed"): return None
        pn = _prop_name(n)
        if pn is None: return None
        parts.append(pn); n = n.get("object", {})
    if isinstance(n, dict) and n.get("k") == "ident" and parts:
        return ".".join([n["name"]] + parts[::-1])
    return None

def _callee_name(callee):
    if not isinstance(callee, dict): return None
    if callee.get("k") == "ident": return callee.get("name")
    if callee.get("k") == "member": return _prop_name(callee)
    return None


_RANK = {F: 0, Z: 1, T: 2}
_DRANK = {"EARNED": 0, "OPEN": 1, "REFUTED": 2}
# calls on a local that store their argument in it
MUTATORS = {"push", "unshift", "splice", "set", "add", "append", "concat", "assign", "write"}
# library methods that pass the receiver's (and arguments') taint through
TRANSPARENT_M = {"trim", "trimStart", "trimEnd", "toLowerCase", "toUpperCase", "toString", "slice", "substring",
                 "substr", "split", "join", "concat", "replace", "replaceAll", "padStart", "padEnd", "repeat",
                 "normalize", "map", "filter", "reduce", "flat", "flatMap", "find", "at", "get", "values",
                 "keys", "entries", "decode", "parse", "stringify", "from", "format"}
# of those, the ones whose ARGUMENTS are content too (slice(i, j)'s arguments are numbers)
ARG_CONTENT_M = {"concat", "replace", "replaceAll", "join", "padStart", "padEnd", "format", "from", "parse",
                 "stringify", "decode"}
PURE_CLEAN_M = {"length", "indexOf", "lastIndexOf", "includes", "startsWith", "endsWith", "test", "has",
                "some", "every", "findIndex", "parseInt", "parseFloat", "isInteger", "isNaN", "localeCompare"}


# ---------------------------------------------------------------- taint values (see java2zfl)
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


class Engine:
    def __init__(self):
        self.summaries = {}   # name -> [summary] (every function of that name: bare names collide)
        self.funcs = {}       # name -> [func node]
        self.sinks = []
        self._rets = None
        self._esc = []
        self._dirty = False

    def _join(self, a, b): return join(a, b)

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
        if k in ("lit", "nil"): return F
        if k == "ident": return env.get(n.get("name"), Z)
        if k == "bin":
            if n.get("op") in ("==", "===", "!=", "!==", "<", ">", "<=", ">=", "instanceof", "in",
                               "-", "*", "/", "%", "**", "&", "|", "^", "<<", ">>", ">>>"):
                return F                                  # a boolean or a number
            return join(self.taint(n.get("x"), env), self.taint(n.get("y"), env))   # + && || ??
        if k == "template": return join(*[self.taint(e, env) for e in n.get("exprs", [])])
        if k == "await": return self.taint(n.get("x"), env)
        if k == "seq": return self.taint((n.get("exprs") or [{}])[-1], env)
        if k == "cond": return join(self.taint(n.get("x"), env), self.taint(n.get("y"), env))
        if k == "assignexpr": return self.taint(n.get("right"), env)
        if k == "unary": return F
        if k == "array": return join(*[self.taint(e, env) for e in n.get("elts", [])])
        if k == "object": return join(*[self.taint(e, env) for e in n.get("props", [])])
        if k == "member":
            p = _path(n)
            if p is not None and p in env: return env[p]      # a field this code stored into
            if _prop_name(n) in REQ_SOURCE_PROPS and _base_ident(n) in REQUEST_NAMES: return T
            if _prop_name(n) == "length" and not n.get("computed"): return F
            return self.taint(n.get("object"), env)      # propagate: req.query.name -> object req.query = T
        if k in ("call", "new"): return self._call_taint(n, env)
        return Z                                          # funcref, other, anything not modelled: unknown

    def _is_source(self, call):
        callee = call.get("callee", {})
        if isinstance(callee, dict) and callee.get("k") == "member":
            if _prop_name(callee) in REQ_SOURCE_CALLS and _base_ident(callee) in REQUEST_NAMES:
                return True
        return False

    def _sums(self, cn):
        if self._dirty: self._summarize_all()
        return self.summaries.get(cn)

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
        if n.get("k") == "call" and self._is_source(n): return T
        cn = _callee_name(callee)
        if callee.get("k") == "ident" and cn in CONV_IDENTS:
            if cn != "String": return F                   # Number(x) / Boolean(x): not a string
            return self.taint(args[0], env) if args else F
        if cn in CTX_SANITIZERS and not (callee.get("k") == "ident" and self._sums(cn)):   # own function wins
            return _clean_for(join(*[self.taint(a, env) for a in args]), CTX_SANITIZERS[cn])
        sums = self._sums(cn)
        if sums is not None and (callee.get("k") == "ident" or cn not in TRANSPARENT_M | PURE_CLEAN_M):
            return self._apply(sums, args, env)
        if cn in PURE_CLEAN_M: return F
        if callee.get("k") == "member" and cn in TRANSPARENT_M:
            recv = self.taint(callee.get("object"), env)
            if cn in ARG_CONTENT_M: return join(recv, *[self.taint(a, env) for a in args])
            return recv
        return Z

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

    def _ctx_taint(self, n, env, ctx):
        return _at(self.taint(n, env), ctx)

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
                if self._sums(nm): self._apply_summary(c, nm, args, env)
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
                elif self._sums(prop) and prop not in TRANSPARENT_M | PURE_CLEAN_M | MUTATORS:
                    self._apply_summary(c, prop, args, env)

    def _judge(self, call, name, ctx, st):
        st = _at(st, ctx)
        d = taintjudge.judge_taint(st, ctx, source="input", sink=name)   # the ONE ZTL judge
        if d in ("REFUTED", "OPEN", "EARNED"):
            self.sinks.append((call.get("line", 0), name, ctx, d))

    # ---------- effects ----------
    def _assign_names(self, names, left, v, env, op="="):
        if left and isinstance(left, dict) and left.get("k") == "member":
            # o.f = v: the FIELD holds v; the object as a whole "may hold" it (Z) — reading o.g is not
            # made T by it (req.pet.name = body.x must not taint req.pet.id)
            p = _path(left)
            if p is not None:
                env[p] = join(env.get(p, Z), v) if op not in (None, "=") else v
            r = _base_ident(left)
            if r is not None: env[r] = join(env.get(r, F), F if v == F else Z)
            return
        for nm in (names or []):
            env[nm] = join(env.get(nm, Z), v) if op not in (None, "=") else v

    def _effects(self, node, env):
        """Assignments inside expressions, and calls that store their argument in a local."""
        if isinstance(node, dict):
            if node.get("k") == "assignexpr":
                self._effects(node.get("right"), env)
                self._assign_names(node.get("names"), node.get("left"), self.taint(node.get("right"), env), env,
                                   node.get("op"))
                return
            if node.get("k") in ("call", "new"):
                for a in node.get("args", []): self._effects(a, env)
                callee = node.get("callee", {})
                if isinstance(callee, dict) and callee.get("k") == "member":
                    self._effects(callee.get("object"), env)
                    obj = callee.get("object", {})
                    m = _prop_name(callee)
                    if isinstance(obj, dict) and obj.get("k") == "ident" and obj.get("name") in env:
                        vs = [self.taint(a, env) for a in node.get("args", [])]
                        if m in MUTATORS:                          # push/set/add: it IS stored
                            env[obj["name"]] = join(env[obj["name"]], *vs)
                        elif m not in TRANSPARENT_M and m not in PURE_CLEAN_M and any(x != F for x in vs):
                            env[obj["name"]] = join(env[obj["name"]], Z)   # an unknown call MAY store it
                return
            for key, v in node.items():
                if key in ("body", "els"): continue
                self._effects(v, env)
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
            if k == "funcref": continue                  # nested function: judged independently
            if k == "block": self._walk(st.get("body"), env); continue
            if k == "if":
                self._leaf_sinks(st.get("test"), env); self._effects(st.get("test"), env)
                var, neg = self._guard(st.get("test"))
                then_term = self._terminates(st.get("body"))
                else_term = bool(st.get("els")) and self._terminates(
                    st["els"].get("body") if st["els"].get("k") == "block" else [st["els"]])
                e1 = dict(env); e2 = dict(env)
                if var and not neg: e1[var] = F               # positive guard narrows the THEN branch
                self._walk(st.get("body"), e1)
                if st.get("els"): self._walk([st["els"]], e2)
                if then_term and not else_term:
                    _set_env(env, e2)                         # continuation follows else/fallthrough
                    if var and neg: env[var] = F              # !guard { return } -> validated after
                elif else_term and not then_term:
                    _set_env(env, e1)
                else:
                    _set_env(env, _ejoin(e1, e2))
                continue
            if k == "for": self._loop(st, env); continue
            if k in ("break", "continue"):
                if self._esc:
                    for lv in (self._esc if k == "continue" else self._esc[-1:]): lv.append(dict(env))
                continue
            if k == "try":
                e_try = dict(env); self._walk(st.get("body"), e_try)
                eh = _ejoin(env, e_try)                       # the throw may come from anywhere in the body
                for nm in st.get("param") or []: eh[nm] = Z
                self._walk(st.get("handler"), eh)
                new = _ejoin(e_try, eh) if st.get("handler") else e_try
                self._walk(st.get("finalizer"), new)
                _set_env(env, new); continue
            if k == "switch":
                self._leaf_sinks(st.get("disc"), env); self._effects(st.get("disc"), env)
                esc = []; self._esc.append(esc)
                try:
                    outs, fall, has_default = [], None, False
                    for c in st.get("cases", []):
                        if c.get("isdefault"): has_default = True
                        e = dict(env) if fall is None else _ejoin(env, fall)
                        self._walk(c.get("body"), e)
                        last = (c.get("body") or [{}])[-1] if c.get("body") else {}
                        if isinstance(last, dict) and last.get("k") in ("break", "return", "throw", "continue"):
                            fall = None
                        else: fall = e
                    if fall is not None: outs.append(fall)
                    if not has_default: outs.append(dict(env))
                    outs += esc
                    _set_env(env, _ejoin(*outs) if outs else env)
                finally:
                    self._esc.pop()
                continue
            if k == "vardecl":
                for d in st.get("decls", []):
                    self._effects(d.get("init"), env)
                    v = self.taint(d.get("init"), env) if d.get("init") and d["init"].get("k") != "nil" else Z
                    for nm in (d.get("names") or ([d["name"]] if d.get("name") else [])): env[nm] = v
            elif k == "assign":
                self._effects(st.get("right"), env)
                self._assign_names(st.get("names"), st.get("left"), self.taint(st.get("right"), env), env, st.get("op"))
            elif k in ("return", "throw", "exprstmt"):
                self._effects(st.get("argument") if k != "exprstmt" else st.get("x"), env)
                if k == "return" and self._rets is not None:
                    self._rets.append(self.taint(st.get("argument"), env) if st.get("argument", {}).get("k") != "nil" else F)
            self._leaf_sinks(st, env)

    def _loop(self, st, env):
        """Zero or more iterations: join(before, after one, after two)."""
        self._walk(st.get("pre") or [], env)
        def head(e):
            for part in ("test", "iter"):
                if st.get(part): self._leaf_sinks(st[part], e); self._effects(st[part], e)
            if st.get("left"):
                v = self.taint(st.get("iter"), e)
                for nm in st["left"]: e[nm] = v
        def tail(e):
            if st.get("update"): self._leaf_sinks(st["update"], e); self._effects(st["update"], e)
        esc = []; self._esc.append(esc)
        try:
            e0 = dict(env)
            e1 = dict(env); head(e1); self._walk(st.get("body"), e1); tail(e1)
            e2 = _ejoin(e0, e1, *esc)
            e3 = dict(e2); head(e3); self._walk(st.get("body"), e3); tail(e3)
            _set_env(env, _ejoin(e2, e3, *esc))
        finally:
            self._esc.pop()

    # ---------- passes ----------
    def _summ_of(self, fn):
        params = [p for p in fn.get("params", [])]
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
                summ["ret"].append(r if p else Z)          # a destructured parameter: unknown
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
            if fn.get("name") and fn["name"] != "<top>": self.funcs.setdefault(fn["name"], []).append(fn)
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
            env = {p: F for p in fn.get("params", []) if p}
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

UNPARSED = []     # files the last analyze_app could not parse: NOT analysed, NOT clean

def analyze_app(paths):
    e = Engine(); trees = []
    del UNPARSED[:]
    for p in paths:
        t = parse(p)
        if t.get("error"): UNPARSED.append((p, str(t["error"])[:60])); continue
        if t.get("funcs"): trees.append((p, t)); e.index(t)
    out = []
    for p, t in trees:
        for rec in e.judge(t): out.append((p,) + rec)
    return out

if __name__ == "__main__":
    for ln, m, ctx, d in analyze(sys.argv[1]):
        print(f"  L{ln}: {d:8} [{ctx}] {m}")
