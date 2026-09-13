# -*- coding: utf-8 -*-
"""code2py — Python module of the introspect (slices 1-3, 2026-09-11).
Native ast; zero-trust F/T/Z -> REFUTED/OPEN/EARNED; honest OPEN on the unresolved.
Slice1 single-fn taint; slice2 function SUMMARIES (cross-fn); slice3 GUARD narrowing
(if x in WHITELIST -> x is F in the branch) + shell=True refinement."""
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
SANITIZERS   = {"shlex.quote","int","float","bool","escape","html.escape","markupsafe.escape",
                "secure_filename","werkzeug.utils.secure_filename"}
TRANSPARENT_FN = {"str","bytes","bytearray","base64.b64decode","base64.b64encode",
                "base64.urlsafe_b64decode","base64.standard_b64decode","urllib.parse.unquote",
                "urllib.parse.unquote_plus","urllib.parse.unquote_to_bytes","json.loads"}
TRANSPARENT_METH = {"decode","encode","strip","lstrip","rstrip","lower","upper","title","get","read"}
TRANSPARENT_ARG = {"re.sub":2, "re.subn":2}   # transform the string at that arg -> preserve its taint
F,T,Z = "F","T","Z"
FUNC = (ast.FunctionDef, ast.AsyncFunctionDef)   # async def (aiohttp/FastAPI) counts too

def dotted(n):
    if isinstance(n, ast.Name): return n.id
    if isinstance(n, ast.Attribute):
        b = dotted(n.value); return f"{b}.{n.attr}" if b else n.attr
    return None

def literal_collection(node):
    """A constant collection literal (whitelist), e.g. ('a','b') or ['x'] or {'y'}."""
    return isinstance(node, (ast.Tuple, ast.List, ast.Set))

class Engine:
    def __init__(self):
        self.summaries = {}          # funcname -> summary
        self.classes = {}            # ClassName -> {method: FunctionDef}
        self.msums = {}              # (ClassName, method) -> summary
        self.vtype = {}              # var -> ClassName (receiver tracking)
        self.sinks = []

    # ---------- pass 1: summarise each def by probing each param ----------
    def _summ_of(self, fn):
        """Summarise by WALKING the body with each param tainted (T): intra-function dataflow
        through assignments/guards is tracked, so param->local->sink is captured (not just direct)."""
        params = [a.arg for a in fn.args.args]
        summ = {"sinks": {}, "passes": set(), "params": params}
        for i, p in enumerate(params):
            env = {p: T}
            saved, savev = self.sinks, self.vtype
            self.sinks, self.vtype = [], {}
            self._walk(fn.body, env)                      # real walk: assignments, guards, cross-calls
            ctxs = sorted({ctx for (_l,_c,ctx,d,_w) in self.sinks if d=="REFUTED"})
            self.sinks, self.vtype = saved, savev
            if ctxs: summ["sinks"][i] = ctxs
            for st in ast.walk(fn):                        # param flows to a return -> passes taint
                if isinstance(st, ast.Return) and st.value is not None and self.taint(st.value, env)==T:
                    summ["passes"].add(i); break
        return summ
    def summarise(self, fn): self.summaries[fn.name] = self._summ_of(fn)

    def _probe(self, body, env, probe, r):
        for st in self._stmts(body, env):
            if isinstance(st, ast.Return) and st.value is not None and self.taint(st.value, env)==T:
                r["ret"] = True
            for c in ast.walk(st):
                if isinstance(c, ast.Call):
                    ctx = self._sink_ctx(c)
                    if ctx and c.args and self.taint(c.args[0], env)==T \
                       and not (ctx=="sql" and len(c.args)>=2):
                        r["ctx"].append(ctx)

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
        if isinstance(node, ast.Await): return self.taint(node.value, env)
        if isinstance(node, ast.Constant): return F
        if isinstance(node, ast.Name): return env.get(node.id, Z)
        if isinstance(node, ast.BinOp):
            l,r=self.taint(node.left,env),self.taint(node.right,env)
            return T if T in (l,r) else (Z if Z in (l,r) else F)
        if isinstance(node, ast.JoinedStr):
            ts=[self.taint(v.value,env) for v in node.values if isinstance(v,ast.FormattedValue)]
            return T if T in ts else (Z if Z in ts else F)
        if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            ts=[self.taint(e,env) for e in node.elts]
            return T if T in ts else (Z if Z in ts else F)
        if isinstance(node, ast.Dict):
            ts=[self.taint(v,env) for v in node.values if v is not None]
            return T if T in ts else (Z if Z in ts else F)
        if isinstance(node, ast.Subscript):
            if dotted(node.value) in SOURCE_ATTRS: return T
            return self.taint(node.value, env)
        if isinstance(node, ast.Call):
            callee=dotted(node.func)
            if callee in SANITIZERS: return F
            if callee in SOURCE_CALLS: return T
            if callee and node.func.__class__ is ast.Attribute and node.func.attr=="get" \
               and dotted(node.func.value) in SOURCE_ATTRS: return T
            if node.func.__class__ is ast.Attribute and node.func.attr in SOURCE_METHS \
               and dotted(node.func.value)=="request": return T   # aiohttp await request.post()
            if callee in TRANSPARENT_FN and node.args: return self.taint(node.args[0], env)
            if callee in TRANSPARENT_ARG:
                i=TRANSPARENT_ARG[callee]
                if i < len(node.args): return self.taint(node.args[i], env)
            if isinstance(node.func, ast.Attribute):
                m=node.func.attr
                if m=="format":
                    ts=[self.taint(a,env) for a in node.args]
                    return T if T in ts else (Z if Z in ts else self.taint(node.func.value,env))
                if m in TRANSPARENT_METH:
                    r=self.taint(node.func.value,env)
                    if r!=F: return r          # x.decode()/.get()/.read() preserve receiver taint
            if callee in self.summaries:
                for i in self.summaries[callee]["passes"]:
                    if i<len(node.args) and self.taint(node.args[i],env)==T: return T
                return F
            return Z
        if isinstance(node, ast.Attribute):
            return T if dotted(node) in SOURCE_ATTRS else Z
        return Z

    # ---------- pass 2: walk with guard narrowing, apply summaries ----------
    def index(self, tree):
        """Pass 1 (global): accumulate function/method SUMMARIES + classes across ALL files."""
        for n in tree.body:
            if isinstance(n, FUNC): self.summarise(n)
            if isinstance(n, ast.ClassDef):
                self.classes[n.name] = {m.name: m for m in n.body if isinstance(m, FUNC)}
                for m in n.body:
                    if isinstance(m, FUNC): self.msums[(n.name, m.name)] = self._summ_of(m)

    def judge(self, tree):
        """Pass 2: judge THIS file's call sites using the (possibly cross-file) global summaries."""
        self.sinks = []
        self.vtype = {}              # receiver tracking, per file scope
        self._walk(tree.body, {})    # module-level (import-time) code
        # Walk EVERY function/method body as its own scope. Params seeded clean (F): a param->sink
        # flow is the SUMMARY's job (judged at call sites); the body-walk finds INTERNAL sources
        # (input()/request inside the body) and cross-function/cross-file calls to summarised sinks.
        for n in ast.walk(tree):
            if isinstance(n, FUNC):
                self.vtype = {}
                params = {a.arg: F for a in n.args.args}
                self._walk(n.body, params, report_earned=False)
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

    def _join(self, a, b):
        return T if T in (a,b) else (Z if Z in (a,b) else F)

    def _sinks_in(self, node, env, report_earned):
        """Report sinks reached within one leaf node/expression (given the current env)."""
        for c in ast.walk(node):
            if not isinstance(c, ast.Call): continue
            if isinstance(c.func, ast.Attribute) and isinstance(c.func.value, ast.Name):
                recv=c.func.value.id
                cls, off = (self.vtype[recv], 1) if recv in self.vtype else \
                           ((recv, 0) if recv in self.classes else (None, 0))
                if cls is not None:
                    meth=c.func.attr
                    if (cls,meth) in self.msums:
                        for i,ctxs in self.msums[(cls,meth)]["sinks"].items():
                            ai=i-off
                            if 0<=ai<len(c.args):
                                sti=self.taint(c.args[ai],env)
                                for cx in ctxs: self._judge(c, f"{cls}.{meth}()->sink", cx, sti, parameterised=False, report_earned=report_earned)
                    continue
            callee=dotted(c.func); ctx=self._sink_ctx(c)
            if ctx and c.args:
                self._judge(c, callee, ctx, self.taint(c.args[0],env), (ctx=="sql" and len(c.args)>=2), report_earned)
            elif callee in self.summaries:
                for i,ctxs in self.summaries[callee]["sinks"].items():
                    if i<len(c.args):
                        sti=self.taint(c.args[i],env)
                        for cx in ctxs: self._judge(c, f"{callee}()->sink", cx, sti, parameterised=False, report_earned=report_earned)

    def _walk(self, body, env, report_earned=True):
        """Structural walk with proper branch handling: if/else analysed in SEPARATE envs then
        MERGED (taint = join), so a branch assignment never leaks into the other branch."""
        for st in body:
            if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)): continue
            if isinstance(st, ast.If):
                self._sinks_in(st.test, env, report_earned)
                gv = st.test.left.id if self._is_whitelist_guard(st.test) else None
                e1=dict(env)
                if gv: e1[gv]=F                                  # whitelist-narrowed in the true branch
                self._walk(st.body, e1, report_earned)
                e2=dict(env); self._walk(st.orelse, e2, report_earned)
                for k in set(e1)|set(e2):
                    env[k]=self._join(e1.get(k, env.get(k,Z)), e2.get(k, env.get(k,Z)))
                continue
            if isinstance(st, ast.Try):
                self._walk(st.body, env, report_earned)
                for h in st.handlers: self._walk(h.body, env, report_earned)
                self._walk(st.orelse, env, report_earned); self._walk(st.finalbody, env, report_earned)
                continue
            if isinstance(st, (ast.For, ast.AsyncFor)):
                self._sinks_in(st.iter, env, report_earned)
                self._walk(st.body, env, report_earned); self._walk(st.orelse, env, report_earned)
                continue
            if isinstance(st, ast.While):
                self._sinks_in(st.test, env, report_earned)
                self._walk(st.body, env, report_earned); self._walk(st.orelse, env, report_earned)
                continue
            if isinstance(st, (ast.With, ast.AsyncWith)):
                for it in st.items: self._sinks_in(it.context_expr, env, report_earned)
                self._walk(st.body, env, report_earned)
                continue
            # leaf statement: track assignment, then report sinks in it
            if isinstance(st, (ast.Assign, ast.AnnAssign)):
                val = st.value
                if val is not None:
                    sv=self.taint(val, env)
                    cls = val.func.id if (isinstance(val, ast.Call) and isinstance(val.func, ast.Name) and val.func.id in self.classes) else None
                    tgts = st.targets if isinstance(st, ast.Assign) else [st.target]
                    for t in tgts:
                        if isinstance(t, ast.Name):
                            env[t.id]=sv
                            if cls: self.vtype[t.id]=cls
                            elif t.id in self.vtype: del self.vtype[t.id]
            self._sinks_in(st, env, report_earned)

    def _judge(self, c, callee, ctx, st, parameterised=False, report_earned=True):
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

def analyze_app(paths):
    """Cross-file: index every file's summaries GLOBALLY, then judge each file's call sites."""
    e=Engine(); trees=[]
    for path in paths:
        try: t=ast.parse(open(path,encoding='utf-8',errors='replace').read())
        except SyntaxError: continue
        trees.append((path,t)); e.index(t)
    out=[]
    for path,t in trees:
        for rec in e.judge(t): out.append((path,)+rec)
    return out
if __name__=="__main__":
    for ln,fn,ctx,d,w in analyze(open(sys.argv[1],encoding="utf-8").read()):
        print(f"  L{ln}: {d:8} [{ctx}] {fn}  <- {w}")
