#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""juliet.py — java2zfl against the NIST Juliet Test Suite for Java, servlet-source variants.

    python3 java2zfl/bench/juliet.py <juliet-java/src>                 # the table in CALIBRATION.md
    python3 java2zfl/bench/juliet.py <juliet-java/src> --engine old.py # the same table for another engine file

Scope: CWE78 (OS command), CWE89 (SQL), CWE80 / CWE83 (XSS), CWE81 (XSS in an error page), and within
them only the variants whose source is a servlet request (getParameter_Servlet, getCookies_Servlet,
getQueryString_Servlet). Juliet's other sources (environment, console, sockets, files, properties) are
not request input and java2zfl does not model them as sources — including them would score a model
the tool does not claim.

A test case = the files sharing a stem (_54a.._54e, _81a + _81_bad/_81_base/..), analysed together
with testcasesupport/ (analyze_app, the way introspect.py runs a project). Juliet labels METHODS:
bad* is vulnerable, good* is safe. A report is attributed to the method whose declaration precedes its
line. Per case and family, the worst disposition:
  bad:   REFUTED = hit      OPEN = abstain     silent = MISS (EARNED or no sink seen)
  good:  REFUTED = FALSE ALARM   OPEN = abstain   silent = correct
"""
import argparse, collections, glob, importlib.util, os, re, sys, time
import javalang
from javalang import tree as J

HERE = os.path.dirname(os.path.abspath(__file__))
CWES = ["CWE78_OS_Command_Injection", "CWE89_SQL_Injection", "CWE80_XSS", "CWE83_XSS_Attribute",
        "CWE81_XSS_Error_Message"]
SRC = re.compile(r"getCookies_Servlet|getParameter_Servlet|getQueryString_Servlet")
STEM = re.compile(r"(_\d+)(?:[a-e]|_[A-Za-z0-9]+)?\.java$")
RANK = {"OPEN": 1, "REFUTED": 2}


def load(engine):
    sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))        # repo root: taintjudge, zfl
    spec = importlib.util.spec_from_file_location("java2zfl_under_test", engine)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def method_starts(path):
    t = javalang.parse.parse(open(path, encoding="utf-8", errors="replace").read())
    return sorted((m.position.line, m.name) for _, m in t.filter(J.MethodDeclaration) if m.position)


def owner(starts, line):
    name = None
    for l, n in starts:
        if l <= line: name = n
    return name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", help="juliet-java/src (holds testcases/ and testcasesupport/)")
    ap.add_argument("--engine", default=os.path.join(os.path.dirname(HERE), "java2zfl.py"))
    ap.add_argument("--list", action="store_true", help="print every miss and false alarm")
    a = ap.parse_args()
    j = load(a.engine)
    support = sorted(glob.glob(os.path.join(a.root, "testcasesupport", "*.java")))
    tot, per, notes, t0 = collections.Counter(), collections.defaultdict(collections.Counter), [], time.time()
    for cwe in CWES:
        files = sorted(f for f in glob.glob(os.path.join(a.root, "testcases", cwe, "**", "*.java"), recursive=True)
                       if SRC.search(f))
        groups = collections.defaultdict(list)
        for f in files: groups[STEM.sub(r"\1", f)].append(f)
        for g, fs in sorted(groups.items()):
            out = j.analyze_app(support + fs)
            starts = {f: method_starts(f) for f in fs}
            worst = {"bad": None, "good": None}
            for (p, line, name, ctx, d) in out:
                if p not in starts: continue
                m = (owner(starts[p], line) or "").lower()
                fam = "bad" if m.startswith("bad") else ("good" if m.startswith("good") else None)
                if fam and (worst[fam] is None or RANK[d] > RANK[worst[fam]]): worst[fam] = d
            b = {"REFUTED": "hit", "OPEN": "bad-OPEN", None: "MISS"}[worst["bad"]]
            gd = {"REFUTED": "FALSE-ALARM", "OPEN": "good-OPEN", None: "good-clean"}[worst["good"]]
            for k in (b, gd): per[cwe][k] += 1; tot[k] += 1
            if b == "MISS" or gd == "FALSE-ALARM": notes.append(f"{b:5} {gd:11} {os.path.basename(g)}")
    keys = ["hit", "MISS", "bad-OPEN", "good-clean", "FALSE-ALARM", "good-OPEN"]
    print(f"  {'':30}" + "".join(f"{k:>12}" for k in keys))
    for cwe in CWES: print(f"  {cwe:30}" + "".join(f"{per[cwe][k]:>12}" for k in keys))
    print(f"  {'TOTAL':30}" + "".join(f"{tot[k]:>12}" for k in keys) + f"   ({time.time() - t0:.0f}s)")
    if a.list:
        for n in notes: print("   ", n)


if __name__ == "__main__":
    main()
