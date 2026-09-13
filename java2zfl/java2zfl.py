# -*- coding: utf-8 -*-
"""java2zfl — Java module of the introspect (slices 1-5 + recall pass, 2026-09-12).
javalang parser; shared contract INTROSPECT-SEMANTICS.md: zero-trust F/T/Z -> REFUTED/OPEN/EARNED,
honest OPEN. Slice1 source->sink taint; slice2 cross-method + cross-file SUMMARIES;
slice3 GUARD narrowing (whitelist.contains(x) / x.equals/matches(..) -> x is F) + branch-join
(if/else analysed in SEPARATE envs then MERGED; a terminating then-branch narrows the negated guard);
slice4 RECEIVER-AWARE sinks (the php2zfl bare-name lesson): specific names (exec/executeQuery/
executeUpdate/readObject) sink by name; generic names (execute/write/print/println) fire only on a
confirmed receiver type -- unknown receiver is honest OPEN (execute) or skipped (writers)."""
import sys, os, javalang
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import taintjudge
from javalang import tree as J
F, T, Z = "F", "T", "Z"
SOURCE_METHODS = {"getParameter","getParameterValues","getParameterMap","getQueryString",
                  "getHeader","getHeaders","getCookies","getInputStream","getReader","getRequestURI"}
# Spring MVC parameter annotations: an annotated handler param IS user input (entry-point source)
SPRING_SOURCES = {"RequestParam","PathVariable","RequestBody","RequestHeader",
                  "CookieValue","RequestPart","MatrixVariable","ModelAttribute"}
# a @*Mapping handler auto-binds its BARE simple-type params from the request (implicit @RequestParam)
MAPPING_ANNOS = {"GetMapping","PostMapping","RequestMapping","PutMapping","DeleteMapping","PatchMapping"}
SIMPLE_TYPES = {"String","int","Integer","long","Long","short","Short","byte","Byte","boolean","Boolean",
                "char","Character","double","Double","float","Float","BigDecimal","BigInteger"}
# constructor sinks: new ProcessBuilder(taint) is command execution (the injection is the ctor arg)
CTOR_SINKS = {"ProcessBuilder":"shell"}
# specific method names: the name alone is enough to call it a sink (zero-trust confident).
# prepareStatement is SQL-specific: a CONSTANT arg (parameterised, uses ?) is clean, a CONCATENATED
# arg is tainted -> REFUTED; parameterised queries are safe automatically (executeQuery() has no arg).
SINK_HIGH = {"exec":"shell","executeQuery":"sql","executeUpdate":"sql",
             "prepareStatement":"sql","readObject":"deser"}
WRITER_TYPES = {"PrintWriter","Writer","ServletOutputStream","OutputStream","PrintStream"}
SQL_RECV     = {"Statement","PreparedStatement","CallableStatement","Connection"}
# generic method names collide across libraries -> confirm by receiver type.
# (ctx, receiver-types-that-confirm, open_if_unknown): unknown receiver -> OPEN if True else skip.
SINK_RECV = {"execute": ("sql", SQL_RECV, True),
             "write":   ("xss", WRITER_TYPES, False),
             "print":   ("xss", WRITER_TYPES, False),
             "println": ("xss", WRITER_TYPES, False)}
WRITER_PRODUCERS = {"getWriter","getOutputStream"}   # chain X.getWriter().write(..) -> response sink
SANITIZERS = set()
# CONTEXT-AWARE sanitizers (like php2zfl): an escaper neutralises ONE context, not all. A value wrapped by
# an html-escaper is clean for xss but NOT for sql/shell -- so it is checked against the sink's context.
CTX_SANITIZERS = {"escapeHtml":"xss","escapeHtml4":"xss","escapeHtml3":"xss","htmlEscape":"xss",
                  "forHtml":"xss","forHtmlContent":"xss","forHtmlAttribute":"xss","encodeForHTML":"xss",
                  "escapeXml":"xss","escapeXml10":"xss","escapeXml11":"xss","forJavaScript":"xss",
                  "encodeForJavaScript":"xss","escapeEcmaScript":"xss"}
GUARD_ARG  = {"contains","containsKey","containsValue"}   # validated var is the ARGUMENT
GUARD_RECV = {"equals","equalsIgnoreCase","matches"}      # validated var is the QUALIFIER

def _is_spring_source(param):
    return any(getattr(a,'name',None) in SPRING_SOURCES for a in (getattr(param,'annotations',None) or []))

def _is_handler(meth):
    return any(getattr(a,'name',None) in MAPPING_ANNOS for a in (getattr(meth,'annotations',None) or []))

def _typename(ty):
    """Simple (last) name of a possibly-qualified/nested javalang type: java.sql.Statement -> 'Statement'."""
    if ty is None: return None
    n = getattr(ty,'name',None); sub = getattr(ty,'sub_type',None)
    while sub is not None:
        n = getattr(sub,'name',n) or n; sub = getattr(sub,'sub_type',None)
    return n

def _stmts(body):
    """Flat statement stream (for return-scanning in summaries); branch structure is lost here."""
    for st in (body or []):
        if isinstance(st, J.BlockStatement): yield from _stmts(st.statements)
        elif isinstance(st, J.IfStatement):
            yield from _stmts([st.then_statement] if st.then_statement else [])
            yield from _stmts([st.else_statement] if st.else_statement else [])
        elif isinstance(st, (J.ForStatement, J.WhileStatement, J.DoStatement)):
            yield from _stmts([st.body] if st.body else [])
        elif isinstance(st, J.TryStatement):
            yield from _stmts(st.block or [])
            for c in (st.catches or []): yield from _stmts(c.block or [])
            yield from _stmts(st.finally_block or [])
        else:
            yield st

class Engine:
    def __init__(self):
        self.summaries = {}   # method name -> {sinks:{i:[ctx]}, passes:set, params:[names]}
        self.sinks = []
        self.vt = {}          # per-method: var name -> simple type name (receiver-aware sinks)

    def taint(self, node, env):
        if node is None: return F
        if isinstance(node, J.Literal): return F
        if isinstance(node, J.MemberReference): return env.get(node.member, Z)
        if isinstance(node, J.BinaryOperation):
            l,r = self.taint(node.operandl,env), self.taint(node.operandr,env)
            return T if T in (l,r) else (Z if Z in (l,r) else F)
        if isinstance(node, J.Cast): return self.taint(node.expression, env)
        if isinstance(node, J.ArrayCreator):                   # new String[]{...}: tainted if any element is
            ini=getattr(node,'initializer',None)
            elts=getattr(ini,'initializers',None) if ini else None
            if elts:
                ts=[self.taint(e,env) for e in elts]
                return T if T in ts else (Z if Z in ts else F)
            return F
        if isinstance(node, J.ArrayInitializer):               # bare String[] x = {a,b,taint} (no `new`)
            ts=[self.taint(e,env) for e in (node.initializers or [])]
            return T if T in ts else (Z if Z in ts else F)
        if isinstance(node, J.ClassCreator):                   # transparent ctor: new StringBuilder(taint) etc.
            ts=[self.taint(a,env) for a in (node.arguments or [])]
            if not ts: return F
            return T if T in ts else (Z if Z in ts else F)
        if isinstance(node, J.MethodInvocation):
            if node.member in SANITIZERS: return F
            if node.member in SOURCE_METHODS: return T
            if node.member in self.summaries:                 # cross-method: passes taint?
                for i in self.summaries[node.member]["passes"]:
                    if i < len(node.arguments) and self.taint(node.arguments[i],env)==T: return T
                return F
            return Z
        return Z

    # ---------- guard / branch-join helpers (slice 3) ----------
    def _guard(self, cond):
        """Return (var, negated) if cond validates a single variable, else (None, False).
        whitelist.contains(x) -> ('x',False); x.equals("ok") -> ('x',False); !ALLOWED.contains(x) -> ('x',True)."""
        if not isinstance(cond, J.MethodInvocation): return (None, False)
        neg = "!" in (cond.prefix_operators or [])
        if cond.member in GUARD_ARG:
            for a in (cond.arguments or []):
                if isinstance(a, J.MemberReference): return (a.member, neg)
        if cond.member in GUARD_RECV and cond.qualifier:
            return (cond.qualifier, neg)
        return (None, False)

    def _join(self, a, b): return T if T in (a,b) else (Z if Z in (a,b) else F)

    def _terminates(self, st):
        if st is None: return False
        if isinstance(st, (J.ReturnStatement, J.ThrowStatement)): return True
        if isinstance(st, J.BlockStatement):
            return bool(st.statements) and self._terminates(st.statements[-1])
        return False

    def _types_of(self, meth):
        """Var -> simple type name for one method: params + local declarations."""
        vt = {}
        for p in (meth.parameters or []): vt[p.name] = _typename(p.type)
        for st in _stmts(meth.body):
            if isinstance(st, J.LocalVariableDeclaration):
                for d in st.declarators: vt[d.name] = _typename(st.type)
        return vt

    def _summ_of(self, meth):
        self.vt = self._types_of(meth)
        params = [p.name for p in (meth.parameters or [])]
        summ = {"sinks":{}, "passes":set(), "params":params}
        for i,p in enumerate(params):
            saved=self.sinks; self.sinks=[]
            env={p:T}; self._walk(meth.body, env)
            ctxs=sorted({ctx for (_l,_m,ctx,d) in self.sinks if d=="REFUTED"})
            self.sinks=saved
            if ctxs: summ["sinks"][i]=ctxs
            for st in _stmts(meth.body):
                if isinstance(st, J.ReturnStatement) and st.expression is not None and self.taint(st.expression,env)==T:
                    summ["passes"].add(i); break
        return summ

    def index(self, tree):
        for _, m in tree.filter(J.MethodDeclaration): self.summaries[m.name]=self._summ_of(m)

    def _ctx_taint(self, node, env, ctx):
        """Taint of an argument for a sink of context `ctx`. A context-aware escaper neutralises ONLY its own
        context (escapeHtml -> clean for xss) and is TRANSPARENT for others (escapeHtml before exec still shell)."""
        if isinstance(node, J.MethodInvocation) and node.member in CTX_SANITIZERS:
            if CTX_SANITIZERS[node.member] == ctx: return F
            return self.taint(node.arguments[0], env) if node.arguments else F   # transparent for other contexts
        if isinstance(node, J.BinaryOperation):                                  # "a" + escapeHtml(x) + "b"
            return self._join(self._ctx_taint(node.operandl, env, ctx), self._ctx_taint(node.operandr, env, ctx))
        return self.taint(node, env)

    def _leaf_sinks(self, node, env):
        """Report sinks reached within one leaf node/expression, given env (direct sink or summary sink)."""
        if node is None: return
        for _, inv in (node.filter(J.MethodInvocation) if hasattr(node,'filter') else []):
            if inv.member in SINK_HIGH and inv.arguments:        # specific name: sink by name
                self._judge(inv, inv.member, SINK_HIGH[inv.member], self._ctx_taint(inv.arguments[0],env,SINK_HIGH[inv.member]))
            elif inv.member in SINK_RECV and inv.arguments:      # generic name: confirm by receiver type
                ctx, types, open_unknown = SINK_RECV[inv.member]
                q = inv.qualifier
                if q and q.startswith("System."): pass          # console stream, not a web sink
                else:
                    rt = self.vt.get(q) if q else None
                    if rt in types:                             # confirmed sink-bearing receiver
                        self._judge(inv, inv.member, ctx, self._ctx_taint(inv.arguments[0],env,ctx))
                    elif rt is not None: pass                    # known type, not a sink-bearer -> skip
                    elif open_unknown:                           # unknown receiver: honest "не знаю"
                        self._judge(inv, inv.member, ctx, self._ctx_taint(inv.arguments[0],env,ctx), soft=True)
            if inv.member in WRITER_PRODUCERS:                   # chain: response.getWriter().write(taint)
                for sel in (inv.selectors or []):
                    if isinstance(sel, J.MethodInvocation) and sel.member in ("write","print","println") and sel.arguments:
                        self._judge(sel, sel.member, "xss", self._ctx_taint(sel.arguments[0],env,"xss"))
            if inv.member in self.summaries:                     # cross-method summary sink
                for i,ctxs in self.summaries[inv.member]["sinks"].items():
                    if i < len(inv.arguments):
                        sti=self.taint(inv.arguments[i],env)
                        for cx in ctxs: self._judge(inv, inv.member+"()->sink", cx, sti)
        for _, cc in (node.filter(J.ClassCreator) if hasattr(node,'filter') else []):
            ctx = CTOR_SINKS.get(cc.type.name if cc.type else None)   # new ProcessBuilder(taint) -> shell
            if ctx and cc.arguments:
                ts=[self.taint(a,env) for a in cc.arguments]
                st = T if T in ts else (Z if Z in ts else F)
                fb = node.position.line if getattr(node,'position',None) else 0   # ClassCreator has no position
                self._judge(cc, "new "+cc.type.name, ctx, st, fallback_line=fb)

    def _walk(self, body, env):
        """Structural walk: if/else in SEPARATE envs then MERGED (join); a terminating then-branch
        does not reach the continuation, and a negated guard over it narrows the var afterwards."""
        for st in (body or []):
            if isinstance(st, J.BlockStatement):
                self._walk(st.statements, env); continue
            if isinstance(st, J.IfStatement):
                self._leaf_sinks(st.condition, env)
                var, neg = self._guard(st.condition)
                then_term = self._terminates(st.then_statement)
                e1=dict(env); e2=dict(env)
                if var and not neg: e1[var]=F                 # positive guard narrows the THEN branch
                self._walk([st.then_statement] if st.then_statement else [], e1)
                self._walk([st.else_statement] if st.else_statement else [], e2)
                if then_term:
                    for k in set(e2): env[k]=e2[k]            # continuation follows else/fallthrough
                    if var and neg: env[var]=F               # !guard{return} => clean after the if
                else:
                    for k in set(e1)|set(e2):
                        env[k]=self._join(e1.get(k, env.get(k,Z)), e2.get(k, env.get(k,Z)))
                continue
            if isinstance(st, (J.ForStatement, J.WhileStatement, J.DoStatement)):
                self._walk([st.body] if st.body else [], env); continue
            if isinstance(st, J.TryStatement):
                self._walk(st.block or [], env)
                for c in (st.catches or []): self._walk(c.block or [], env)
                self._walk(st.finally_block or [], env)
                continue
            # leaf statement: track assignment, then report sinks in it
            if isinstance(st, J.LocalVariableDeclaration):
                for d in st.declarators: env[d.name]=self.taint(d.initializer,env)
            elif isinstance(st, J.StatementExpression) and isinstance(st.expression, J.Assignment) \
                 and isinstance(st.expression.expressionl, J.MemberReference):
                env[st.expression.expressionl.member]=self.taint(st.expression.value,env)
            self._leaf_sinks(st, env)

    def _judge(self, inv, name, ctx, st, soft=False, fallback_line=0):
        eff = Z if (soft and st == T) else st         # soft generic sink, unknown receiver -> honest Z
        d = taintjudge.judge_taint(eff, ctx, source="input", sink=name)   # the ONE ZTL judge
        if d in ("REFUTED", "OPEN"):
            line = inv.position.line if getattr(inv,'position',None) else fallback_line
            self.sinks.append((line, name, ctx, d))

    def judge(self, tree):
        self.sinks=[]
        for _, m in tree.filter(J.MethodDeclaration):
            self.vt = self._types_of(m)
            # params clean by default (their flows are the summary's job) EXCEPT entry-point sources:
            # Spring-annotated params, and (on a @*Mapping handler) BARE simple-type params, which Spring
            # auto-binds from the request (implicit @RequestParam). Complex/annotated params stay clean.
            handler = _is_handler(m)
            def _src(p):
                if _is_spring_source(p): return T
                if handler and not (getattr(p,'annotations',None)) and _typename(p.type) in SIMPLE_TYPES: return T
                return F
            env={p.name: _src(p) for p in (m.parameters or [])}
            self._walk(m.body, env)
        return self.sinks

    def run(self, tree): self.index(tree); return self.judge(tree)

def analyze(code): return Engine().run(javalang.parse.parse(code))
def analyze_app(paths):
    e=Engine(); trees=[]
    for p in paths:
        try: t=javalang.parse.parse(open(p,encoding="utf-8",errors="replace").read())
        except Exception: continue
        trees.append((p,t)); e.index(t)
    out=[]
    for p,t in trees:
        for rec in e.judge(t): out.append((p,)+rec)
    return out

if __name__=="__main__":
    for ln,m,ctx,d in analyze(open(sys.argv[1],encoding="utf-8").read()):
        print(f"  L{ln}: {d:8} [{ctx}] {m}")
