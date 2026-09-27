#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
owasp.py — java2zfl against the OWASP Benchmark for Java (v1.2: 2 740 servlets, each labelled by
expectedresults-1.2.csv as a real vulnerability or not, by category / CWE).

    git clone --depth 1 https://github.com/OWASP-Benchmark/BenchmarkJava.git /tmp/owasp
    pip install javalang                                   # java2zfl's parser (see java2zfl/README.md)
    python3 java2zfl/bench/owasp.py /tmp/owasp             # every number in OWASP-2026-09.md
    python3 java2zfl/bench/owasp.py /tmp/owasp --project   # + the whole-project run (introspect.py's way)
    python3 java2zfl/bench/owasp.py /tmp/owasp --list      # + one line per disagreement

Nothing of the Benchmark is copied: this reads the clone in place and prints only test names, the
expected label, our verdict and our classification.

THE ANALYZER IS NOT CHANGED. The harness runs java2zfl.Engine unmodified, through a subclass that
only OBSERVES (it records the EARNED dispositions the engine computes and drops, and snapshots the
taint environment before chosen statements). A self-check asserts that the subclass's REFUTED/OPEN
records equal the stock engine's on every file.

Run modes
  case (default)  each test file is analysed with the Benchmark's helper classes in view:
                  helpers indexed first, then the test file, then the test file judged.
  --project       java2zfl.analyze_app over every .java under src/main/java at once, the way
                  introspect.py runs a project (method summaries are keyed by bare name, so the
                  2 740 servlets' doPost / doSomething summaries collide — that is the tool as shipped).

File verdict for a category (as php2zfl/bench/sard.py): the WORST sink of that category's context in
the test file: REFUTED > OPEN > EARNED > NONE (no sink of that context recognised at all).
  hit          vulnerable -> REFUTED
  miss         vulnerable -> EARNED (the engine judged the sink clean) or NONE (nothing flagged)
  false alarm  safe -> REFUTED
  abstention   OPEN, either label — never a hit, never a miss.
java2zfl never prints EARNED (it reports REFUTED/OPEN sinks only), so to a user EARNED and NONE
look the same: silence. They are split here because EARNED is a clean verdict the engine reached.

Every miss and every false alarm is classified; a disagreement no rule explains is printed as
UNCLASSIFIED. Misses are classified by COUNTERFACTUAL on the unchanged engine, along the Benchmark's
fixed shape  source -> `param` -> propagator -> `bar` -> sink:
  SOURCE lost       `param` is not T where the propagation starts;
  PROPAGATION lost  with `param` forced to T there, `bar` is still not T where the sink part starts;
  SINK lost         with `bar` forced to T there, no sink of the context is REFUTED.
A miss may lose at several stages; its class is the FIRST stage lost, and the recovery table counts
the misses that ONE stage alone blocks.
"""
import argparse, copy, csv, glob, importlib.metadata, json, os, re, subprocess, sys, time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))                  # java2zfl/
import java2zfl                                            # noqa: E402
import javalang                                            # noqa: E402
from javalang import tree as J                             # noqa: E402

T, F, Z = java2zfl.T, java2zfl.F, java2zfl.Z

# ---------------------------------------------------------------- category -> java2zfl context
# java2zfl's catalog has four sink contexts: sql, shell, xss, deser (java2zfl.py SINK_HIGH / SINK_RECV
# / CTOR_SINKS / WRITER_PRODUCERS). A Benchmark category is MODELLED only if one of them is its sink.
CTX = {"sqli": "sql", "cmdi": "shell", "xss": "xss"}
NOT_MODELLED = {
    "pathtraver":   "taint -> file API (new File / FileInputStream / Paths.get): java2zfl has no `file` sink context",
    "ldapi":        "taint -> LDAP search filter (DirContext.search): no `ldap` sink context",
    "xpathi":       "taint -> XPath.evaluate / compile: no `xpath` sink context",
    "trustbound":   "taint -> HttpSession.setAttribute / putValue: no trust-boundary sink",
    "crypto":       "weak cipher choice (DES / ECB …): a configuration property, not a taint flow",
    "hash":         "weak digest choice (MD5 / SHA1): a configuration property, not a taint flow",
    "weakrand":     "java.util.Random / Math.random where secure randomness is needed: not a taint flow",
    "securecookie": "Cookie.setSecure(false): a configuration property, not a taint flow",
}
RANK = {"REFUTED": 3, "OPEN": 2, "EARNED": 1}
VERDICTS = ("REFUTED", "OPEN", "EARNED", "NONE")


# ---------------------------------------------------------------- the observing engine
class Probe(java2zfl.Engine):
    """java2zfl.Engine, unmodified in behaviour. Adds:
       * `earned` — sinks the engine judged and did not report (disposition EARNED);
       * statement hooks active only while judging: snapshot the env before a statement, or force a
         variable to T before it (the counterfactual). With no hooks set, the walk is the stock walk:
         Engine._walk's loop body depends only on (statement, env), so walking one statement at a
         time is the same walk (asserted against the stock engine on every file)."""

    def __init__(self):
        super().__init__()
        self.earned, self.snap_at, self.force_at, self.snaps, self.active = [], {}, {}, {}, False

    def _judge(self, inv, name, ctx, st, soft=False, fallback_line=0):
        n = len(self.sinks)
        super()._judge(inv, name, ctx, st, soft, fallback_line)
        if len(self.sinks) == n:                                   # judged, not reported: EARNED
            line = inv.position.line if getattr(inv, 'position', None) else fallback_line
            self.earned.append((line, name, ctx, "EARNED"))

    def _walk(self, body, env):
        for st in (body or []):
            if self.active:
                k = id(st)
                for var in self.force_at.get(k, ()): env[var] = T
                for label in self.snap_at.get(k, ()): self.snaps[label] = dict(env)
            super()._walk([st], env)

    def judge(self, tree):
        self.earned, self.snaps, self.active = [], {}, True
        try:
            return super().judge(tree)
        finally:
            self.active = False


def parse(path):
    return javalang.parse.parse(open(path, encoding="utf-8", errors="replace").read())


# ---------------------------------------------------------------- the Benchmark's shape, read from the AST
def _assigns(node, var):
    """Does this statement (sub)tree assign / declare `var`?"""
    for _, d in node.filter(J.VariableDeclarator):
        if d.name == var: return True
    for _, a in node.filter(J.Assignment):
        if isinstance(a.expressionl, J.MemberReference) and a.expressionl.member == var: return True
    return False


def _leaves(body):
    """Leaf statements in textual order, the way java2zfl's _walk reaches them."""
    for st in (body or []):
        if isinstance(st, J.BlockStatement): yield from _leaves(st.statements)
        elif isinstance(st, J.IfStatement):
            yield from _leaves([st.then_statement] if st.then_statement else [])
            yield from _leaves([st.else_statement] if st.else_statement else [])
        elif isinstance(st, (J.ForStatement, J.WhileStatement, J.DoStatement)):
            yield from _leaves([st.body] if st.body else [])
        elif isinstance(st, J.TryStatement):
            yield from _leaves(st.block or [])
            for c in (st.catches or []): yield from _leaves(c.block or [])
            yield from _leaves(st.finally_block or [])
        else:
            yield st


def _line(node):
    p = getattr(node, 'position', None)
    if p: return p.line
    for _, n in node.filter(J.Node) if hasattr(node, 'filter') else []:
        if getattr(n, 'position', None): return n.position.line
    return 0


def shape(tree):
    """(doPost, k_prop, k_sink, flow_var, end_line): the leaf where propagation starts (right after
    the last assignment of `param`), the leaf where the sink part starts (right after the last
    assignment of `bar`, or = k_prop when the test has no `bar`), and the variable carried into it."""
    posts = [m for _, m in tree.filter(J.MethodDeclaration) if m.name == "doPost"]
    if not posts: return None
    m = posts[0]
    lv = list(_leaves(m.body))
    ip = max((i for i, s in enumerate(lv) if _assigns(s, "param")), default=None)
    if ip is None or ip + 1 >= len(lv): return None
    ib = max((i for i, s in enumerate(lv) if _assigns(s, "bar")), default=None)
    if ib is None or ib < ip: ib, var = ip, "param"
    else: var = "bar"
    if ib + 1 >= len(lv): return None
    end = max((n.position.line for _, n in m.filter(J.Node) if getattr(n, 'position', None)), default=0)
    return m, lv[ip + 1], lv[ib + 1], var, end


# ---------------------------------------------------------------- running
class Runner:
    def __init__(self, clone, stock_check=True):
        self.S = os.path.join(clone, "src", "main", "java", "org", "owasp", "benchmark")
        self.helper_paths = sorted(glob.glob(os.path.join(self.S, "helpers", "*.java")))
        self.helpers = [parse(p) for p in self.helper_paths]
        base = java2zfl.Engine()
        for h in self.helpers: base.index(h)
        self.base_summaries = base.summaries          # == indexing the helpers first, every time
        self.stock_check = stock_check

    def engine(self, tree):
        e = Probe()
        e.summaries = copy.deepcopy(self.base_summaries)
        e.index(tree)
        return e

    def stock(self, tree):
        e = java2zfl.Engine()
        for h in self.helpers: e.index(h)
        e.index(tree)
        return e.judge(tree)

    def run_case(self, name):
        path = os.path.join(self.S, "testcode", name + ".java")
        try: tree = parse(path)
        except Exception as ex: return {"parse_error": type(ex).__name__}
        e = self.engine(tree)
        recs = [tuple(r) for r in e.judge(tree)]
        if self.stock_check:
            st = [tuple(r) for r in self.stock(tree)]
            assert recs == st, f"{name}: observing engine differs from stock java2zfl: {recs} vs {st}"
        return {"tree": tree, "recs": recs + [tuple(r) for r in e.earned]}

    def counterfactual(self, tree, ctx):
        """The three stage tests on the unchanged engine (see module docstring)."""
        sh = shape(tree)
        if sh is None: return None
        m, kp, ks, var, end = sh
        e = self.engine(tree)
        e.snap_at = {id(kp): ["prop"]}
        e.snap_at.setdefault(id(ks), []).append("sink")
        e.judge(tree)
        p0 = e.snaps.get("prop", {}).get("param", Z)
        e = self.engine(tree)
        e.snap_at, e.force_at = {id(ks): ["sink"]}, {id(kp): ["param"]}
        e.judge(tree)
        b1 = e.snaps.get("sink", {}).get(var, Z)
        e = self.engine(tree)
        e.force_at = {id(ks): [var]}
        recs = e.judge(tree) + e.earned
        lo = _line(ks)
        s2 = max((RANK[r[3]] for r in recs if r[2] == ctx and lo <= r[0] <= end), default=0)
        return {"param": p0, "flow": b1, "sink_forced": ("NONE", "EARNED", "OPEN", "REFUTED")[s2],
                "var": var, "k_prop": _line(kp), "k_sink": lo, "end": end}


def file_verdict(recs, ctx):
    w = max((RANK[r[3]] for r in recs if r[2] == ctx), default=0)
    return ("NONE", "EARNED", "OPEN", "REFUTED")[w]


# ---------------------------------------------------------------- classification (signatures read in the source)
def _text(lines, a, b):
    """Source lines a..b-1 (1-based), comments dropped, whitespace collapsed."""
    s = "\n".join(re.sub(r"//.*", "", x) for x in lines[max(a - 1, 0):max(b - 1, 0)])
    return re.sub(r"\s+", " ", s)


def regions(lines, cf):
    src = _text(lines, 1, cf["k_prop"])
    src = src[src.find("doPost(HttpServletRequest"):]
    prop = _text(lines, cf["k_prop"], cf["k_sink"])
    carrier = "inline"
    if "doSomething(request, param)" in prop:
        carrier = "inner class Test.doSomething" if "new Test().doSomething" in prop else "private method doSomething"
        i = next((n for n, x in enumerate(lines) if re.search(r"String doSomething\(HttpServletRequest", x)), None)
        if i is not None: prop += " " + _text(lines, i + 1, len(lines) + 1)
    sink = _text(lines, cf["k_sink"], cf["end"] + 1)
    return src, prop, carrier, sink


SOURCES = [   # (signature, name, how java2zfl reads it) — first match wins
    (r"getTheParameter\(|getTheCookie\(", "SeparateClassRequest.getTheParameter (request read in a helper)",
     "a method summary records param->return only; a call with a literal argument reads F, though it returns request data"),
    (r"getParameterNames\(", "request.getParameterNames() (the parameter NAME)",
     "Enumeration.nextElement() is an unknown call"),
    (r"getParameterMap\(", "request.getParameterMap() then Map.get(..)[0]", "Map.get is an unknown call"),
    (r"getParameterValues\(", "request.getParameterValues(..)[0]", "array element of a source"),
    (r"getHeaders\(", "request.getHeaders(..).nextElement() + URLDecoder.decode", "Enumeration.nextElement / URLDecoder.decode are unknown calls"),
    (r"getCookies\(", "request.getCookies() loop, Cookie.getValue() + URLDecoder.decode", "Cookie.getValue / URLDecoder.decode are unknown calls"),
    (r"getQueryString\(", "request.getQueryString().substring(..) + URLDecoder.decode", "String.substring / URLDecoder.decode are unknown calls"),
    (r"getHeader\(", "request.getHeader(..) + URLDecoder.decode", "URLDecoder.decode is an unknown call"),
    (r"getParameter\(", "request.getParameter(..)", "a catalogued source"),
]

PROPAGATORS = [   # (signature, name) — first match wins; the carrier is reported beside it
    (r"ThingFactory\.createThing", "ThingInterface.doSomething (implementation picked by reflection in ThingFactory)"),
    (r"switch \(", "switch on a constant (\"ABC\".charAt(k))"),
    (r"valuesList", "ArrayList add / remove(0) / get(k)"),
    (r"HashMap|\.put\(", "HashMap put / get"),
    (r"Base64", "Base64 encode+decode round trip"),
    (r"StringBuilder|\.append\(", "StringBuilder append"),
    (r"\? \"|\? param", "ternary on a constant condition"),
    (r"if \(\(\d+ [*/] \d+\) [-+] num > 200\)", "if on a constant condition"),
    (r"encodeForHTML|htmlEscape|escapeHtml", "HTML escaper (ESAPI / Spring / commons-lang)"),
    (r"\.split\(", "String.split(..)[0]"),
    (r"\.substring\(", "String.substring"),
    (r"\.replace\(|\.replaceAll\(", "String.replace"),
    (r"\bbar = param;|String bar = param;", "plain assignment"),
]

SINKS = {
    "sql": [
        (r"JDBCtemplate\.(\w+)\(", "Spring JdbcTemplate.{0}"),
        (r"prepareCall\(", "Connection.prepareCall"),
        (r"addBatch\(", "Statement.addBatch / executeBatch"),
        (r"prepareStatement\(", "Connection.prepareStatement"),
        (r"\.executeQuery\(sql", "Statement.executeQuery"),
        (r"\.executeUpdate\(sql", "Statement.executeUpdate"),
        (r"\.execute\(sql", "Statement.execute"),
    ],
    "shell": [
        (r"\.command\(", "ProcessBuilder.command(..)"),
        (r"new ProcessBuilder\(argList\)", "new ProcessBuilder(List)"),
        (r"new ProcessBuilder\(args\)", "new ProcessBuilder(String[])"),
        (r"String\[\] argsEnv = \{(bar|param)\}", "Runtime.exec(.., envp = {bar}) (taint in the ENVIRONMENT argument)"),
        (r"\.exec\(cmd \+ (bar|param)", "Runtime.exec(cmd + bar [, ..])"),
        (r"\.exec\(args", "Runtime.exec(String[] {.., bar})"),
    ],
    "xss": [
        (r"\.printf\(", "PrintWriter.printf"),
        (r"\.format\(", "PrintWriter.format"),
        (r"\.toCharArray\(\)", "PrintWriter.write/print(bar.toCharArray())"),
        (r"\.write\((bar|param), 0, length\)", "PrintWriter.write(bar, 0, length)"),
        (r"getWriter\(\)\.write\(", "response.getWriter().write"),
        (r"getWriter\(\)\.println\(", "response.getWriter().println"),
        (r"getWriter\(\)\.print\(", "response.getWriter().print"),
    ],
}


def match(table, text):
    for sig, name, *why in table:
        m = re.search(sig, text)
        if m:
            return (name.replace("{0}", m.group(1)) if "{0}" in name else name), (why[0] if why else "")
    return None, ""


def live_branch(prop):
    """Evaluate the Benchmark's constant conditions exactly (int arithmetic as in Java): which value
    reaches `bar` — 'param' (tainted) or a literal. None when the propagator has no such construct."""
    m = re.search(r"int num = (\d+); if \(\((\d+) ([*/]) (\d+)\) ([-+]) num > 200\) bar = (param|\"[^\"]*\"); else bar = (param|\"[^\"]*\");", prop)
    if m:
        n, a, op, b, op2 = int(m[1]), int(m[2]), m[3], int(m[4]), m[5]
        v = a * b if op == "*" else a // b
        v = v - n if op2 == "-" else v + n
        return "param" if (m[6] if v > 200 else m[7]) == "param" else "literal"
    m = re.search(r"int num = (\d+); bar = \((\d+) ([*/]) (\d+)\) ([-+]) num > 200 \? (param|\"[^\"]*\") : (param|\"[^\"]*\");", prop)
    if m:
        n, a, op, b, op2 = int(m[1]), int(m[2]), m[3], int(m[4]), m[5]
        v = a * b if op == "*" else a // b
        v = v - n if op2 == "-" else v + n
        return "param" if (m[6] if v > 200 else m[7]) == "param" else "literal"
    m = re.search(r"switchTarget = guess\.charAt\((\d)\); switch \(switchTarget\) \{(.*?)\}", prop)
    if m:
        ch = "ABC"[int(m[1])]
        cases = re.findall(r"case '(\w)': (?:case '(\w)': )?bar = (param|\"[^\"]*\"); break;", m[2])
        for c1, c2, val in cases:
            if ch in (c1, c2): return "param" if val == "param" else "literal"
        d = re.search(r"default: bar = (param|\"[^\"]*\");", m[2])
        return ("param" if d and d[1] == "param" else "literal") if d else None
    m = re.search(r"valuesList\.remove\(0\); bar = valuesList\.get\((\d)\);", prop)
    if m:   # added "safe", param, "moresafe"; remove(0) -> [param, "moresafe"]
        return "param" if m[1] == "0" else "literal"
    return None


# ---------------------------------------------------------------- the run
def labels(clone):
    lab = {}
    for r in csv.reader(open(os.path.join(clone, "expectedresults-1.2.csv"), encoding="utf-8")):
        if not r or r[0].startswith("#"): continue
        lab[r[0].strip()] = (r[1].strip(), r[2].strip() == "true", r[3].strip())
    return lab


def classify_miss(cf, lines, fv):
    """(stage, class, detail, losses) for a vulnerable case java2zfl did not REFUTE."""
    src, prop, carrier, sink = regions(lines, cf)
    losses = []
    if cf["param"] != T: losses.append("SOURCE")
    if cf["flow"] != T: losses.append("PROPAGATION")
    if cf["sink_forced"] != "REFUTED": losses.append("SINK")
    if not losses:
        return "UNCLASSIFIED", "UNCLASSIFIED: every stage carries T under the counterfactual, yet no REFUTED", "", losses
    stage = losses[0]
    if stage == "SOURCE":
        name, why = match(SOURCES, src)
        if not name: return stage, "UNCLASSIFIED source", "", losses
        return stage, f"{name}  -> param {cf['param']}", why, losses
    if stage == "PROPAGATION":
        return stage, prop_class(prop, carrier, cf["flow"]), carrier, losses
    return stage, None, sink, losses       # SINK: named by the caller (needs the context)


def prop_class(prop, carrier, state):
    """Name a lost propagation by the MECHANISM in java2zfl that loses it (template in brackets)."""
    name, _ = match(PROPAGATORS, prop)
    if not name: return f"UNCLASSIFIED propagator [{carrier}] -> bar {state}"
    if carrier.startswith("inner class"):
        return ("inner-class call `new Test().doSomething(..)`: javalang hangs the call on the constructor as a "
                "selector; java2zfl reads `new Test()` (no arguments) = F and never applies the summary")
    if name.startswith("ThingInterface"):
        return ("interface call `thing.doSomething(..)`: summaries are keyed by bare method name and the bodiless "
                "ThingInterface.doSomething (indexed after Thing1/Thing2, or the test's own doSomething) wins "
                f"-> an empty summary -> F  [{carrier}]")
    if carrier.startswith("private method"):
        return (f"{name} inside a private method: the template yields no T, and a summary records only T returns, "
                f"so the call reads F (not Z)")
    if name.startswith("switch"):
        return "switch statement: java2zfl does not walk SwitchStatement, and `String bar;` (no initializer) is F"
    return f"{name} [inline]: an unknown call / expression -> bar {state}"


# Is the Benchmark's sink call itself in java2zfl's catalog? (java2zfl.py SINK_HIGH / SINK_RECV /
# CTOR_SINKS / WRITER_PRODUCERS; read from the analyzer's own tables, not restated)
def _catalogued(api):
    if api.startswith("Spring JdbcTemplate.execute"):
        return "matched only by the generic name `execute` on an unknown receiver: soft sink, at most OPEN"
    if api.startswith(("Spring JdbcTemplate", "Connection.prepareCall", "Statement.addBatch", "ProcessBuilder.command")):
        return "not in java2zfl's catalog"
    if api.startswith("PrintWriter.printf") or api.startswith("PrintWriter.format"):
        return "not in java2zfl's catalog (printf/format are not among write/print/println)"
    if api.startswith("new ProcessBuilder(List)"):
        return "catalogued (ProcessBuilder ctor), but the List built by add(..) is F: collections are not tracked"
    if api.startswith("Runtime.exec(.., envp"):
        return "catalogued (exec), but only argument 0 is checked; the taint is in envp (argument 1)"
    if api.startswith("PrintWriter.write/print(bar.toCharArray())"):
        return "catalogued (write/print), but bar.toCharArray() is an unknown call: Z"
    return "catalogued"


def sink_class(ctx, sink_text, forced):
    name, _ = match(SINKS[ctx], sink_text)
    if not name: return "UNCLASSIFIED sink"
    how = _catalogued(name)
    if how == "catalogued": how = f"catalogued, yet the forced-T flow ends {forced} there"
    return f"{name}: {how}"


def git_head(path):
    try:
        return subprocess.run(["git", "-C", path, "rev-parse", "--short", "HEAD"], capture_output=True,
                              text=True, timeout=10).stdout.strip() or "?"
    except Exception:
        return "?"


def run_cases(clone, lab, stock_check):
    R = Runner(clone, stock_check)
    rows = {}
    for name in sorted(lab):
        cat, vuln, cwe = lab[name]
        r = R.run_case(name)
        row = {"test": name, "category": cat, "cwe": cwe, "vulnerable": vuln}
        if "parse_error" in r:
            row["verdict"] = "E"; rows[name] = row; continue
        recs = r["recs"]
        row["records"] = [list(x) for x in recs]
        ctx = CTX.get(cat)
        if ctx is None:
            row["verdict"] = "NOT MODELLED"
            row["other_ctx_refuted"] = sorted({x[2] for x in recs if x[3] == "REFUTED"})
            rows[name] = row; continue
        v = file_verdict(recs, ctx)
        row["verdict"] = v
        row["other_ctx_refuted"] = sorted({x[2] for x in recs if x[3] == "REFUTED" and x[2] != ctx})
        lines = open(os.path.join(R.S, "testcode", name + ".java"), encoding="utf-8", errors="replace").read().split("\n")
        cf = R.counterfactual(r["tree"], ctx)
        if cf:
            _, prop, carrier, _ = regions(lines, cf)
            row["live"] = live_branch(prop)
            row["const_source"] = bool(re.search(r"getTheValue\(", regions(lines, cf)[0]))
        if vuln and v != "REFUTED":
            if cf is None:
                row.update(stage="UNCLASSIFIED", cls="UNCLASSIFIED: the source/propagator/sink shape was not found", losses=[])
            else:
                stage, cls, detail, losses = classify_miss(cf, lines, v)
                if stage == "SINK": cls = sink_class(ctx, detail, cf["sink_forced"])
                row.update(stage=stage, cls=cls, losses=losses, cf=cf)
                # the stage names and the sole-blocker table name the construct at EVERY lost stage
                src, prop, carrier, sink = regions(lines, cf)
                row["at"] = {"SOURCE": match(SOURCES, src)[0] or "UNCLASSIFIED source",
                             "PROPAGATION": prop_class(prop, carrier, cf["flow"]),
                             "SINK": sink_class(ctx, sink, cf["sink_forced"])}
        elif vuln and v == "OPEN" and cf is not None:
            stage, cls, detail, losses = classify_miss(cf, lines, v)
            if stage == "SINK": cls = sink_class(ctx, detail, cf["sink_forced"])
            row.update(stage=stage, cls=cls, losses=losses)
        elif not vuln and v == "REFUTED":
            fa = "UNCLASSIFIED false alarm"
            if cf:
                _, prop, carrier, _ = regions(lines, cf)
                pname, _ = match(PROPAGATORS, prop)
                lb = row.get("live")
                if lb == "literal" and pname in ("if on a constant condition", "ternary on a constant condition",
                                                   "switch on a constant (\"ABC\".charAt(k))"):
                    fa = (f"{pname} [{carrier}]: only a literal reaches `bar` (condition evaluated here); "
                          f"java2zfl joins both branches, so the dead tainted branch keeps T")
                elif lb == "literal":
                    fa = f"{pname} [{carrier}]: only a literal reaches `bar`; java2zfl keeps T"
                elif lb == "param":
                    fa = "LABEL: the evaluated construct delivers `param` to the sink — the Benchmark's 'safe' looks wrong"
            row["cls"] = fa
        rows[name] = row
    return rows


def run_project(clone, lab):
    """java2zfl.analyze_app over every .java under src/main/java — exactly introspect.py's call."""
    root = os.path.join(clone, "src", "main", "java")
    paths = sorted(os.path.join(dp, f) for dp, _, fs in os.walk(root) for f in fs if f.endswith(".java"))
    out = java2zfl.analyze_app(paths)
    # summaries are keyed by bare method name: the LAST indexed definition of `doSomething` serves every call
    last = None
    for pth in paths:
        if re.search(r"String doSomething\(HttpServletRequest", open(pth, encoding="utf-8", errors="replace").read()):
            last = os.path.basename(pth)
    by = defaultdict(list)
    for p, line, name, ctx, d in out: by[os.path.basename(p)[:-5]].append((line, name, ctx, d))
    res = {}
    for name, (cat, vuln, _) in lab.items():
        ctx = CTX.get(cat)
        if ctx is None: continue
        w = max((RANK[r[3]] for r in by.get(name, []) if r[2] == ctx), default=0)
        res[name] = ("SILENT", "SILENT", "OPEN", "REFUTED")[w]     # no EARNED in the stock output
    return res, len(paths), last


def pct(a, b): return f"{100.0 * a / b:5.1f}%" if b else "   n/a"


def report(clone, lab, rows, dt, project=None, listing=False):
    P = print
    P(f"== java2zfl x OWASP Benchmark for Java v1.2")
    P(f"   introspect {git_head(os.path.dirname(os.path.dirname(HERE)))}, javalang {importlib.metadata.version('javalang')},"
      f" Benchmark clone {git_head(clone)}; {len(rows)} test cases, {dt:.0f} s; parse errors: "
      f"{sum(1 for r in rows.values() if r['verdict'] == 'E')}")

    P("\n== 1. Categories -> java2zfl sink context")
    cats = defaultdict(Counter)
    for r in rows.values(): cats[(r["category"], r["cwe"])][r["vulnerable"]] += 1
    for (c, cwe), n in sorted(cats.items(), key=lambda kv: (kv[0][0] not in CTX, kv[0][0])):
        where = f"ctx `{CTX[c]}`" if c in CTX else "NOT MODELLED — " + NOT_MODELLED.get(c, "no sink context")
        P(f"   {c:12} CWE-{cwe:4} vulnerable {n[True]:4}  safe {n[False]:4}   {where}")
    nm = [r for r in rows.values() if r["verdict"] == "NOT MODELLED"]
    P(f"   not modelled: {len(nm)} test cases — NO verdict is claimed for them (not 'clean'); java2zfl raised "
      f"{sum(1 for r in nm if r['other_ctx_refuted'])} REFUTED in them (any context)")

    P("\n== 2. Label x verdict per modelled category  (hit = vuln->REFUTED; miss = vuln->EARNED or NONE; "
      "false alarm = safe->REFUTED; OPEN = abstention)")
    P(f"   {'category':8} {'label':5} {'n':>4} | {'REFUTED':>7} {'OPEN':>5} {'EARNED':>6} {'NONE':>5} {'E':>2}")
    tot = defaultdict(Counter)
    for c in CTX:
        for vuln in (True, False):
            k = Counter(r["verdict"] for r in rows.values() if r["category"] == c and r["vulnerable"] == vuln)
            tot[vuln].update(k)
            P(f"   {c:8} {'vuln' if vuln else 'safe':5} {sum(k.values()):4} | {k['REFUTED']:7} {k['OPEN']:5} "
              f"{k['EARNED']:6} {k['NONE']:5} {k['E']:2}")
    for vuln in (True, False):
        k = tot[vuln]
        P(f"   {'ALL':8} {'vuln' if vuln else 'safe':5} {sum(k.values()):4} | {k['REFUTED']:7} {k['OPEN']:5} "
          f"{k['EARNED']:6} {k['NONE']:5} {k['E']:2}")
    P(f"   hits {tot[True]['REFUTED']}, misses {tot[True]['EARNED'] + tot[True]['NONE']} "
      f"({tot[True]['EARNED']} EARNED + {tot[True]['NONE']} NONE), false alarms {tot[False]['REFUTED']}, "
      f"abstentions {tot[True]['OPEN']} vuln + {tot[False]['OPEN']} safe")

    P("\n== 3. Scores (TPR = TP/(TP+FN), FPR = FP/(FP+TN), Benchmark score = TPR - FPR)")
    P(f"   {'category':8} | {'Benchmark scoring: REFUTED = reported':^38} | {'decided only (OPEN left out)':^30} | {'OPEN also counted as a report':^30}")
    for c in list(CTX) + ["ALL"]:
        rs = [r for r in rows.values() if (c == "ALL" and r["category"] in CTX) or r["category"] == c]
        cells = []
        for mode in ("bench", "decided", "open"):
            rep = {"bench": ("REFUTED",), "decided": ("REFUTED",), "open": ("REFUTED", "OPEN")}[mode]
            use = [r for r in rs if not (mode == "decided" and r["verdict"] == "OPEN")]
            tp = sum(1 for r in use if r["vulnerable"] and r["verdict"] in rep)
            fn = sum(1 for r in use if r["vulnerable"] and r["verdict"] not in rep)
            fp = sum(1 for r in use if not r["vulnerable"] and r["verdict"] in rep)
            tn = sum(1 for r in use if not r["vulnerable"] and r["verdict"] not in rep)
            tpr, fpr = tp / max(1, tp + fn), fp / max(1, fp + tn)
            cells.append(f"TPR {100*tpr:5.1f} FPR {100*fpr:5.1f} score {100*(tpr-fpr):5.1f}")
        P(f"   {c:8} | {cells[0]:^38} | {cells[1]:^30} | {cells[2]:^30}")

    misses = [r for r in rows.values() if r["vulnerable"] and r["verdict"] in ("EARNED", "NONE")]
    P(f"\n== 4. Every miss classified ({len(misses)}): the FIRST stage the flow is lost at, by counterfactual on the unchanged engine")
    by = defaultdict(Counter)
    for r in misses: by[(r["stage"], r["cls"])][r["category"]] += 1
    for stage in ("SOURCE", "PROPAGATION", "SINK", "UNCLASSIFIED"):
        ks = sorted((k for k in by if k[0] == stage), key=lambda k: -sum(by[k].values()))
        n = sum(sum(by[k].values()) for k in ks)
        P(f"   -- {stage}: {n}")
        for k in ks:
            c = by[k]
            P(f"      {sum(c.values()):4}  (sqli {c['sqli']:3} cmdi {c['cmdi']:3} xss {c['xss']:3})  {k[1]}")
    unc = sum(1 for r in misses if "UNCLASSIFIED" in (r.get("cls") or "UNCLASSIFIED"))
    P(f"   UNCLASSIFIED misses: {unc}")

    P("\n== 5. Stages lost per miss, and what ONE fix alone would recover")
    combo = Counter(" + ".join(r["losses"]) for r in misses)
    for k, n in combo.most_common(): P(f"      {n:4}  {k}")
    P("   misses whose every lost stage lies within a set of stages (what fixing that set could recover, at most):")
    for fix in (("SOURCE",), ("PROPAGATION",), ("SINK",), ("SOURCE", "PROPAGATION"), ("SOURCE", "SINK"),
                ("PROPAGATION", "SINK"), ("SOURCE", "PROPAGATION", "SINK")):
        n = sum(1 for r in misses if r["losses"] and set(r["losses"]) <= set(fix))
        P(f"      {n:4}  {' + '.join(fix)}")
    sole = Counter()
    for r in misses:
        if len(r["losses"]) == 1: sole[(r["losses"][0], r["at"][r["losses"][0]])] += 1
    P(f"   misses blocked by exactly ONE stage: {sum(sole.values())} of {len(misses)}")
    for (st, what), n in sole.most_common(): P(f"      {n:4}  {st:11} {what}")
    anyloss = Counter()
    for r in misses:
        for st in r["losses"]: anyloss[(st, r["at"][st])] += 1
    P("   every lost stage, counted once per miss it blocks (a miss can block on several):")
    for (st, what), n in anyloss.most_common(): P(f"      {n:4}  {st:11} {what}")

    fas = [r for r in rows.values() if not r["vulnerable"] and r["verdict"] == "REFUTED"]
    P(f"\n== 6. Every false alarm classified ({len(fas)})")
    for r in fas: P(f"      {r['test']}  {r['category']:5}  {r['cls']}")
    P(f"   UNCLASSIFIED false alarms: {sum(1 for r in fas if 'UNCLASSIFIED' in r['cls'])}")

    P("\n== 7. The Benchmark's labels, checked where the propagator is a constant construct we can evaluate")
    chk = Counter()
    for r in rows.values():
        lb = r.get("live")
        if lb is None: continue
        if lb == "literal": what = "only a literal reaches bar"
        elif r.get("const_source"): what = "param reaches bar, but param = getTheValue(..) = the literal \"bar\""
        else: what = "param (request data) reaches bar"
        chk[(what, r["vulnerable"])] += 1
    for (what, vuln), n in sorted(chk.items()):
        P(f"      {n:4}  {what:62} labelled {'vulnerable' if vuln else 'safe'}")
    bad = [r["test"] for r in rows.values() if r.get("live") == "literal" and r["vulnerable"]]
    P(f"   labelled vulnerable although only a literal reaches the sink: {len(bad)} {bad[:10]}")
    odd = [r["test"] for r in rows.values() if r.get("live") == "param" and not r.get("const_source") and not r["vulnerable"]]
    P(f"   labelled safe although request data reaches `bar` (safe, if at all, at the sink — not checked here): {len(odd)} {odd[:10]}")

    opens = [r for r in rows.values() if r["vulnerable"] and r["verdict"] == "OPEN"]
    P(f"\n== 8. Abstentions on vulnerable cases ({len(opens)}), for the record (never a hit, never a miss)")
    ob = Counter((r.get("stage", "UNCLASSIFIED"), r.get("cls", "UNCLASSIFIED: no shape")) for r in opens)
    for (st, cls), n in ob.most_common(): P(f"      {n:4}  {st:11} {cls}")
    oc = Counter(r["category"] for r in rows.values() if r.get("other_ctx_refuted") and r["category"] in CTX)
    P(f"   REFUTED raised in a context other than the case's own category: {sum(oc.values())} {dict(oc)}")

    if project is not None:
        res, npaths, last = project
        P(f"\n== 9. Whole-project run (introspect.py's way: java2zfl.analyze_app over {npaths} files at once)")
        P("   the stock output has no EARNED: SILENT = neither REFUTED nor OPEN for the category's context")
        for c in CTX:
            for vuln in (True, False):
                k = Counter(v for n, v in res.items() if lab[n][0] == c and lab[n][1] == vuln)
                P(f"   {c:8} {'vuln' if vuln else 'safe':5} {sum(k.values()):4} | REFUTED {k['REFUTED']:4}  "
                  f"OPEN {k['OPEN']:4}  SILENT {k['SILENT']:4}")
        for c in list(CTX) + ["ALL"]:
            ns = [n for n in res if (c == "ALL" or lab[n][0] == c)]
            tp = sum(1 for n in ns if lab[n][1] and res[n] == "REFUTED"); fn = sum(1 for n in ns if lab[n][1]) - tp
            fp = sum(1 for n in ns if not lab[n][1] and res[n] == "REFUTED"); tn = sum(1 for n in ns if not lab[n][1]) - fp
            tpr, fpr = tp / max(1, tp + fn), fp / max(1, fp + tn)
            P(f"   {c:8} Benchmark scoring: TPR {100*tpr:5.1f} FPR {100*fpr:5.1f} score {100*(tpr-fpr):5.1f}")
        diff = Counter()
        for n, v in res.items():
            pv = rows[n]["verdict"] if rows[n]["verdict"] in ("REFUTED", "OPEN") else "SILENT"
            if pv == v: continue
            txt = open(os.path.join(clone, "src", "main", "java", "org", "owasp", "benchmark", "testcode", n + ".java"),
                       encoding="utf-8", errors="replace").read()
            car = ("inner class" if "new Test().doSomething" in txt else
                   "private method doSomething" if "doSomething(request, param)" in txt else "inline")
            diff[(lab[n][0], "vuln" if lab[n][1] else "safe", pv, v, car)] += 1
        P(f"   cases whose verdict differs from the per-case run: {sum(diff.values())}; the `doSomething` summary every "
          f"call uses is {last}'s (indexed last)")
        for k, n in sorted(diff.items()): P(f"      {n:4}  {k[0]:5} {k[1]}  {k[2]} -> {k[3]}   carrier: {k[4]}")

    if listing:
        P("\n== every disagreement")
        for r in misses: P(f"   MISS         {r['test']} {r['category']:5} {r['verdict']:6} {r['stage']:11} {r['cls']}")
        for r in fas: P(f"   FALSE ALARM  {r['test']} {r['category']:5} REFUTED {r['cls']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clone", help="path to a clone of OWASP-Benchmark/BenchmarkJava")
    ap.add_argument("--project", action="store_true", help="also run the whole project at once (introspect.py's way)")
    ap.add_argument("--list", action="store_true", help="print one line per miss and false alarm")
    ap.add_argument("--json", metavar="FILE", help="write every row (test, label, verdict, records, class)")
    ap.add_argument("--no-stock-check", action="store_true", help="skip re-running the stock engine per file (2x faster)")
    a = ap.parse_args()
    lab = labels(a.clone)
    t0 = time.time()
    rows = run_cases(a.clone, lab, not a.no_stock_check)
    dt = time.time() - t0
    project = run_project(a.clone, lab) if a.project else None
    report(a.clone, lab, rows, dt, project, a.list)
    if a.json:
        for r in rows.values(): r.pop("tree", None)
        json.dump(rows, open(a.json, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
