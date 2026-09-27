# -*- coding: utf-8 -*-
"""rb2zfl — Ruby module of the introspect (slice 1, 2026-09-13).
Parser: Ruby's OWN Ripper (stdlib, zero install) via the `rbast` helper (rbast.rb -> compact JSON).
Shared contract INTROSPECT-SEMANTICS.md: zero-trust F/T/Z -> REFUTED/OPEN/EARNED, honest OPEN.
Slice1: Rails/Sinatra sources (params, params[:x], request.params/GET/POST, cookies) -> sinks
(system/exec/`backticks`=shell, eval/instance_eval=code, AR where/find_by_sql/execute=sql,
raw/html_safe=xss, File.*=file, open/Net::HTTP=ssrf); string-interpolation + concat propagation,
cross-method + cross-file SUMMARIES, branch-join. Sixth language after php/py/java/go/js.
Slice 2 (2026-09-27), the java2zfl soundness lesson ported: tri-valued summaries with a parameter-free
base; a method's LAST expression is its return (implicit return was never read, so a helper like
`def clean(x) x.strip end` returned F); block bodies are walked, their params bound to the receiver (they
were not parsed at all); rescue/ensure are parsed and joined; `x += y` joins; `a, b = v` assigns;
`h[k] = v`, `arr << v`, `push` fold into the container; case/when and loops joined; escapers tag one
context; comparisons give F; unmodelled expressions are Z."""
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


_RANK = {F: 0, Z: 1, T: 2}
_DRANK = {"EARNED": 0, "OPEN": 1, "REFUTED": 2}
# calls on a local that store their argument in it
MUTATORS = {"push", "<<", "concat", "append", "store", "merge!", "update", "insert", "unshift", "[]=",
            "add", "prepend"}
# methods whose result carries the receiver's taint
RECV_TRANSPARENT = {"to_s", "strip", "lstrip", "rstrip", "chomp", "chop", "downcase", "upcase", "capitalize",
                    "squeeze", "freeze", "dup", "clone", "to_str", "first", "last", "reverse", "flatten",
                    "compact", "uniq", "sort", "values", "keys", "to_a", "to_h", "fetch", "dig", "slice", "[]",
                    "lines", "chars", "split", "encode", "force_encoding", "unpack1", "b", "permit", "require",
                    "to_unsafe_h", "with_indifferent_access", "presence", "try", "map", "select", "reject",
                    "detect", "find", "each_line", "tr", "delete", "succ", "center", "ljust", "rjust"}
# ... and whose ARGUMENTS are content too
ARG_CONTENT = {"gsub", "sub", "gsub!", "sub!", "join", "concat", "+", "%", "format", "sprintf", "insert",
               "prepend", "merge", "tr", "center"}
# results that are numbers / booleans
NUMERIC_RESULT = {"length", "size", "count", "to_i", "to_f", "include?", "nil?", "empty?", "blank?",
                  "present?", "any?", "none?", "all?", "start_with?", "end_with?", "match?", "zero?", "positive?",
                  "eql?", "is_a?", "kind_of?", "respond_to?", "index", "rindex", "between?", "exist?", "exists?"}


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

def _tail(body):
    """Ruby returns its last expression: make that an explicit return (copy; the tree is not changed)."""
    if not isinstance(body, list) or not body: return body
    last = body[-1]
    if not isinstance(last, dict): return body
    k = last.get("k"); new = dict(last)
    if k == "exprstmt": return body[:-1] + [{"k": "return", "argument": last.get("x"), "line": last.get("line", 0)}]
    if k == "assign": return body + [{"k": "return", "argument": last.get("right"), "line": last.get("line", 0)}]
    if k == "if":
        new["body"] = _tail(last.get("body"))
        if last.get("els"): new["els"] = _tail([last["els"]])[0] if last["els"].get("k") != "block" else \
            dict(last["els"], body=_tail(last["els"].get("body")))
        return body[:-1] + [new]
    if k == "switch":
        new["cases"] = [dict(c, body=_tail(c.get("body"))) for c in last.get("cases", [])]
        return body[:-1] + [new]
    if k == "block": new["body"] = _tail(last.get("body")); return body[:-1] + [new]
    if k == "try":
        new["body"] = _tail(last.get("body")); new["handler"] = _tail(last.get("handler"))
        return body[:-1] + [new]
    return body


class Engine:
    def __init__(self):
        self.summaries = {}   # name -> [summary] (bare names: methods of different classes collide)
        self.funcs = {}
        self.sinks = []
        self._rets = None
        self._dirty = False

    def _join(self, a, b): return join(a, b)

    def _terminates(self, body):
        if isinstance(body, list) and body:
            last = body[-1]
            return isinstance(last, dict) and last.get("k") in ("return",)
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
        if k in ("lit", "nil"): return F
        if k == "ident":
            nm = n.get("name")
            return T if nm in SOURCE_IDENTS else env.get(nm, Z)
        if k == "aref": return self.taint(n.get("object"), env)   # params[:x] -> taint of params
        if k == "bin":
            if n.get("op") in ("==", "!=", "<", ">", "<=", ">=", "=~", "!~", "<=>", "==="): return F
            return join(self.taint(n.get("x"), env), self.taint(n.get("y"), env))
        if k in ("template", "xstring", "array"):
            return join(*[self.taint(e, env) for e in n.get("exprs", n.get("elts", []))])
        if k == "unary": return F
        if k == "assignexpr": return self.taint(n.get("right"), env)
        if k == "member":
            if n.get("prop") in REQ_SOURCE_MEMBERS and _base_ident(n.get("object")) in REQUEST_BASES:
                return T
            prop = n.get("prop")
            if prop in NUMERIC_RESULT: return F
            if prop in RECV_TRANSPARENT: return self.taint(n.get("object"), env)
            sums = self._sums(prop)
            if sums: return self._apply(sums, [], env)
            return Z
        if k == "call": return self._call_taint(n, env)
        return Z                                          # funcref, other, anything not modelled: unknown

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
        nm = callee.get("name") if callee.get("k") == "ident" else callee.get("prop")
        if callee.get("k") == "ident" and self._sums(nm):      # the program's own `h` / `escape` wins
            return self._apply(self._sums(nm), args, env)      # over the catalogue's escaper of that name
        if nm in CTX_SANITIZERS:
            return _clean_for(join(*[self.taint(a, env) for a in args]), CTX_SANITIZERS[nm])
        if callee.get("k") == "ident":
            if nm in CONV_IDENTS: return self.taint(args[0], env) if args else F
            if nm in ("Integer", "Float"): return F
            return Z
        if callee.get("k") == "member":
            obj = callee.get("object")
            if nm in NUMERIC_RESULT: return F
            if nm in ARG_CONTENT: return join(self.taint(obj, env), *[self.taint(a, env) for a in args])
            if nm in RECV_TRANSPARENT or nm in CONV_IDENTS: return self.taint(obj, env)
            sums = self._sums(nm)
            if sums: return self._apply(sums, args, env)
        return Z

    def _ctx_taint(self, n, env, ctx):
        return _at(self.taint(n, env), ctx)

    # ---------- sinks ----------
    def _iter_nodes(self, n):
        if isinstance(n, dict):
            yield n
            for key, v in n.items():
                if key != "block": yield from self._iter_nodes(v)   # a block is walked on its own
        elif isinstance(n, list):
            for x in n: yield from self._iter_nodes(x)

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
        for c in self._iter_nodes(node):
            k = c.get("k")
            if k == "xstring":
                self._judge(c, "`backticks`", "shell", join(*[self.taint(e, env) for e in c.get("exprs", [])]))
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
                    elif self._sums(nm): self._apply_summary(c, nm, args, env)
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
                    elif self._sums(prop) and prop not in RECV_TRANSPARENT | ARG_CONTENT | NUMERIC_RESULT | MUTATORS:
                        self._apply_summary(c, prop, args, env)

    def _judge(self, call, name, ctx, st):
        st = _at(st, ctx)
        d = taintjudge.judge_taint(st, ctx, source="input", sink=name)   # the ONE ZTL judge
        if d in ("REFUTED", "OPEN", "EARNED"):
            self.sinks.append((call.get("line", 0), name, ctx, d))

    # ---------- effects ----------
    def _effects(self, node, env):
        """Blocks (walked zero or more times, their params bound to the receiver), and calls that store
        their argument in a local (arr << x, h.store(k, x), arr.push(x))."""
        for c in self._iter_nodes(node):
            if c.get("k") == "bin" and c.get("op") == "<<" and isinstance(c.get("x"), dict) \
                    and c["x"].get("k") == "ident" and c["x"].get("name") in env:
                env[c["x"]["name"]] = join(env[c["x"]["name"]], self.taint(c.get("y"), env))
            if c.get("k") != "call": continue
            callee = c.get("callee", {})
            if callee.get("k") == "member":
                obj = callee.get("object", {}); m = callee.get("prop")
                if isinstance(obj, dict) and obj.get("k") == "ident" and obj.get("name") in env:
                    vs = [self.taint(a, env) for a in c.get("args", [])]
                    if m in MUTATORS: env[obj["name"]] = join(env[obj["name"]], *vs)
                    elif m not in RECV_TRANSPARENT and m not in ARG_CONTENT and m not in NUMERIC_RESULT \
                            and any(x != F for x in vs):
                        env[obj["name"]] = join(env[obj["name"]], Z)     # an unknown call MAY store it
            blk = c.get("block")
            if isinstance(blk, dict):
                bv = self.taint(callee.get("object"), env) if callee.get("k") == "member" else Z
                e1 = dict(env)
                for p in blk.get("params", []): e1[p] = bv
                self._walk(blk.get("body"), e1)
                e2 = _ejoin(env, e1)
                for p in blk.get("params", []): e2[p] = bv
                self._walk(blk.get("body"), e2)
                new = _ejoin(env, e1, e2)
                for p in blk.get("params", []):
                    if p not in env: new.pop(p, None)
                _set_env(env, new)

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
                e0 = dict(env)
                e1 = dict(env); head(e1); self._walk(st.get("body"), e1)
                e2 = _ejoin(e0, e1)
                e3 = dict(e2); head(e3); self._walk(st.get("body"), e3)
                _set_env(env, _ejoin(e2, e3))                 # zero or more iterations
                continue
            if k == "switch":                                  # Ruby case: no fallthrough
                outs, has_else = [], False
                for c in st.get("cases", []):
                    if c.get("isdefault"): has_else = True
                    e = dict(env); self._walk(c.get("body"), e); outs.append(e)
                if not has_else: outs.append(dict(env))
                _set_env(env, _ejoin(*outs) if outs else env)
                continue
            if k == "try":
                e_try = dict(env); self._walk(st.get("body"), e_try)
                eh = _ejoin(env, e_try)
                for nm in st.get("param") or []: eh[nm] = Z
                self._walk(st.get("handler"), eh)
                new = _ejoin(e_try, eh) if st.get("handler") else e_try
                self._walk(st.get("finalizer"), new)
                _set_env(env, new); continue
            if k == "assign":
                self._effects(st.get("right"), env)
                left = st.get("left", {}); v = self.taint(st.get("right"), env)
                compound = st.get("op") not in (None, "=")
                if st.get("names"):
                    for nm in st["names"]: env[nm] = v
                elif left.get("k") == "ident":
                    env[left["name"]] = join(env.get(left["name"], Z), v) if compound else v
                elif left.get("k") in ("member", "aref"):          # h[:k] = v / o.attr = v
                    r = _base_ident(left)
                    if r is not None:
                        env[r] = join(env.get(r, F), v if left.get("k") == "aref" else (F if v == F else Z))
            elif k in ("return", "exprstmt"):
                self._effects(st.get("argument") if k == "return" else st.get("x"), env)
                if k == "return" and self._rets is not None:
                    a = st.get("argument")
                    self._rets.append(self.taint(a, env) if isinstance(a, dict) and a.get("k") != "nil" else F)
            self._leaf_sinks(st, env)

    # ---------- passes ----------
    def _summ_of(self, fn):
        params = [p for p in fn.get("params", [])]
        body = _tail(fn.get("body"))
        saved = (self.sinks, self._rets)
        def run(env):
            self.sinks, self._rets = [], []
            self._walk(body, env)
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
