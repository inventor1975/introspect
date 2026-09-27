#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""owasp_score.py — java2zfl against the OWASP Benchmark for Java v1.2 (sqli / cmdi / xss: the three
categories whose sink java2zfl models; the other eight are not taint-to-these-sinks flows).

    git clone --depth 1 https://github.com/OWASP-Benchmark/BenchmarkJava.git <clone>
    python3 java2zfl/bench/owasp_score.py java2zfl/java2zfl.py <clone>             # case mode
    python3 java2zfl/bench/owasp_score.py java2zfl/java2zfl.py <clone> --project   # introspect.py's way

Scoring rule of the 2026-09 report (bench/owasp-java-2026-09, OWASP-2026-09.md): per test file, the worst
sink of the category's context; REFUTED = reported; OPEN = abstention; Benchmark score = TPR - FPR with
REFUTED as the report. Case mode indexes the Benchmark's helpers, then the test file. Any engine file can
be passed: the same script reproduces the report's numbers for the slices-1-5 engine (12 hits, 5 false
alarms, score 1.0). Nothing of the (GPL) Benchmark is copied: it reads the clone in place."""

import sys, os, glob, csv, time, importlib.util, collections
import javalang
eng, clone = sys.argv[1], sys.argv[2]; project = "--project" in sys.argv
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
spec = importlib.util.spec_from_file_location("j", eng); j = importlib.util.module_from_spec(spec); spec.loader.exec_module(j)
B = os.path.join(clone, "src/main/java/org/owasp/benchmark")
CTX = {"sqli": "sql", "cmdi": "shell", "xss": "xss"}
lab = {}
for r in csv.reader(open(os.path.join(clone, "expectedresults-1.2.csv"))):
    if r and not r[0].startswith("#") and r[1] in CTX: lab[r[0]] = (r[1], r[2] == "true")
parse = lambda p: javalang.parse.parse(open(p, encoding="utf-8", errors="replace").read())
t0 = time.time(); res = {}
if project:
    paths = sorted(glob.glob(os.path.join(clone, "src/main/java/**/*.java"), recursive=True))
    out = j.analyze_app(paths)
    by = collections.defaultdict(list)
    for o in out: by[os.path.basename(o[0])[:-5]].append(o[1:])
    for n in lab: res[n] = by.get(n, [])
else:
    helpers = [parse(p) for p in sorted(glob.glob(os.path.join(B, "helpers", "*.java")))]
    for n in sorted(lab):
        t = parse(os.path.join(B, "testcode", n + ".java"))
        e = j.Engine()
        for h in helpers: e.index(h)
        e.index(t); res[n] = e.judge(t)
V = {}
for n, recs in res.items():
    ds = [r[3] for r in recs if r[2] == CTX[lab[n][0]]]
    V[n] = "REFUTED" if "REFUTED" in ds else ("OPEN" if "OPEN" in ds else "SILENT")
print(f"{'project' if project else 'case'} mode, {len(V)} cases, {time.time()-t0:.0f}s")
for c in list(CTX) + ["ALL"]:
    ns = [n for n in V if c == "ALL" or lab[n][0] == c]
    k = {v: collections.Counter(V[n] for n in ns if lab[n][1] == v) for v in (True, False)}
    tp = k[True]["REFUTED"]; fn = sum(k[True].values()) - tp
    fp = k[False]["REFUTED"]; tn = sum(k[False].values()) - fp
    tpr, fpr = tp / max(1, tp + fn), fp / max(1, fp + tn)
    print(f"  {c:5} vuln {sum(k[True].values()):4}: REF {k[True]['REFUTED']:4} OPEN {k[True]['OPEN']:4} SILENT {k[True]['SILENT']:4} | "
          f"safe {sum(k[False].values()):4}: REF {k[False]['REFUTED']:4} OPEN {k[False]['OPEN']:4} SILENT {k[False]['SILENT']:4} | "
          f"TPR {100*tpr:5.1f} FPR {100*fpr:5.1f} score {100*(tpr-fpr):5.1f}")
if "--dump" in sys.argv:
    import json; json.dump({n: [V[n], lab[n][0], lab[n][1]] for n in V}, open(sys.argv[sys.argv.index("--dump")+1], "w"))
