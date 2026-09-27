#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
score.py — java2zfl on the BLIND corpus, round 2 (java2zfl/blind2/cases, labels in java2zfl/blind2/labels.csv).
(Round 1 score.py, unchanged apart from this line and the paths in the usage lines.)

    pip install javalang
    python3 java2zfl/blind2/score.py                 # the tables in REPORT.md
    python3 java2zfl/blind2/score.py --json out.json # + every case's records

The corpus was committed BEFORE the analyzer was first run on it (the commit is named in REPORT.md);
labels.csv is not changed after that run. The analyzer runs exactly as introspect.py runs it:
java2zfl.analyze_app over EVERY .java file under cases/ at once (cases and their helper files).

File verdict = the worst record of the case's category context IN THAT FILE:
REFUTED > OPEN > SILENT (neither). Category -> context: sqli -> sql, cmdi -> shell, xss -> xss.
A file javalang cannot parse is UNPARSED — its own line, never a miss.

  SILENT on vulnerable      the contract breach: listed one by one (with expect_open=true too, where
                            OPEN was the honest answer and silence is still a clean bill)
  REFUTED on safe           false alarm: listed one by one
  hits, OPEN                counted per category; an expect_open case is neither hit nor miss
The per-case explanation (where the taint is lost, or why the alarm is false) is read from
analysis.csv when present: written AFTER the run, from reading the case and the analyzer.
"""
import argparse, csv, json, os, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))               # java2zfl/
import javalang                                         # noqa: E402
import java2zfl                                         # noqa: E402

CTX = {"sqli": "sql", "cmdi": "shell", "xss": "xss"}
RANK = {"REFUTED": 2, "OPEN": 1}


def load_labels(path):
    rows = {}
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows[r["file"]] = {"category": r["category"], "vulnerable": r["vulnerable"] == "true",
                               "expect_open": r["expect_open"] == "true", "why": r["why"]}
    return rows


def load_notes(path):
    if not os.path.exists(path): return {}
    with open(path, encoding="utf-8") as f:
        return {r["file"]: r for r in csv.DictReader(f)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cases", default=os.path.join(HERE, "cases"))
    ap.add_argument("--labels", default=os.path.join(HERE, "labels.csv"))
    ap.add_argument("--notes", default=os.path.join(HERE, "analysis.csv"))
    ap.add_argument("--json", metavar="FILE")
    a = ap.parse_args()
    lab, notes = load_labels(a.labels), load_notes(a.notes)
    paths = sorted(os.path.join(dp, f) for dp, _, fs in os.walk(a.cases) for f in fs if f.endswith(".java"))
    rel = lambda p: os.path.relpath(p, a.cases).replace(os.sep, "/")

    unparsed = {}
    for p in paths:
        try: javalang.parse.parse(open(p, encoding="utf-8", errors="replace").read())
        except Exception as ex: unparsed[rel(p)] = f"{type(ex).__name__}: {getattr(ex, 'description', '') or ex}"[:120]

    out = java2zfl.analyze_app(paths)
    recs = defaultdict(list)
    for t in out:
        d = {"ON CREDIT": "OPEN", "R": "REFUTED", "O": "OPEN", "F": "EARNED", "E": "OPEN"}.get(t[4], t[4])  # as introspect.py
        recs[rel(t[0])].append({"line": t[1], "name": t[2], "ctx": t[3], "disp": d,
                                "why": (t[5] if len(t) > 5 else "")})

    missing = sorted(set(lab) - {rel(p) for p in paths})
    helpers = sorted({rel(p) for p in paths} - set(lab))
    rows = {}
    for f, L in sorted(lab.items()):
        ctx = CTX[L["category"]]
        if f in unparsed: v = "UNPARSED"
        else:
            w = max((RANK.get(r["disp"], 0) for r in recs.get(f, []) if r["ctx"] == ctx), default=0)
            v = ("SILENT", "OPEN", "REFUTED")[w]
        rows[f] = dict(L, file=f, verdict=v, records=recs.get(f, []), note=notes.get(f, {}))

    P = print
    P("== java2zfl on the blind corpus")
    P(f"   {len(paths)} .java files under cases/: {len(lab)} labelled cases + {len(helpers)} helper files; "
      f"unparsed by javalang: {len(unparsed)}; labelled but missing: {len(missing)} {missing}")

    P("\n== 1. Label x verdict  (exp_open = the author marked 'I don't know' as the honest answer)")
    P(f"   {'category':8} {'label':5} {'exp_open':8} {'n':>4} | {'REFUTED':>7} {'OPEN':>5} {'SILENT':>6} {'UNPARSED':>8}")
    for c in list(CTX) + ["ALL"]:
        for vuln in (True, False):
            for eo in (False, True):
                k = Counter(r["verdict"] for r in rows.values() if (c == "ALL" or r["category"] == c)
                            and r["vulnerable"] == vuln and r["expect_open"] == eo)
                if not k: continue
                P(f"   {c:8} {'vuln' if vuln else 'safe':5} {str(eo).lower():8} {sum(k.values()):4} | "
                  f"{k['REFUTED']:7} {k['OPEN']:5} {k['SILENT']:6} {k['UNPARSED']:8}")

    P("\n== 2. Scores on the decided cases (expect_open=false, parsed)")
    for c in list(CTX) + ["ALL"]:
        rs = [r for r in rows.values() if (c == "ALL" or r["category"] == c) and not r["expect_open"]
              and r["verdict"] != "UNPARSED"]
        v = [r for r in rs if r["vulnerable"]]; s = [r for r in rs if not r["vulnerable"]]
        hit = sum(r["verdict"] == "REFUTED" for r in v); vo = sum(r["verdict"] == "OPEN" for r in v)
        sil = sum(r["verdict"] == "SILENT" for r in v)
        fa = sum(r["verdict"] == "REFUTED" for r in s); so = sum(r["verdict"] == "OPEN" for r in s)
        tpr, fpr = hit / max(1, len(v)), fa / max(1, len(s))
        P(f"   {c:5} vulnerable {len(v):3}: REFUTED {hit:3}  OPEN {vo:3}  SILENT {sil:3}   |   safe {len(s):3}: "
          f"REFUTED {fa:3}  OPEN {so:3}   |  TPR {100*tpr:5.1f}  FPR {100*fpr:5.1f}  TPR-FPR {100*(tpr-fpr):5.1f}")

    def listing(title, sel):
        rs = [r for r in rows.values() if sel(r)]
        P(f"\n== {title}: {len(rs)}")
        for r in sorted(rs, key=lambda r: r["file"]):
            n = r["note"]
            P(f"   {r['file']}  [{r['category']}, expect_open={str(r['expect_open']).lower()}]  label: {r['why']}")
            if n: P(f"      stage: {n.get('stage', '')} — {n.get('cause', '')}")
            else: P("      (no analysis note)")
    listing("3. SILENT on a vulnerable case — contract breach", lambda r: r["vulnerable"] and r["verdict"] == "SILENT")
    listing("4. REFUTED on a safe case — false alarm", lambda r: not r["vulnerable"] and r["verdict"] == "REFUTED")
    listing("5. UNPARSED by javalang (not a miss of the analyzer)", lambda r: r["verdict"] == "UNPARSED")
    for f in sorted(unparsed): P(f"   parse error {f}: {unparsed[f]}")

    P("\n== 6. Records in helper files (not scored; shown so no alarm is hidden)")
    for h in helpers:
        for r in recs.get(h, []):
            if r["disp"] in RANK: P(f"   {h}:{r['line']}  {r['disp']:7} [{r['ctx']}] {r['name']}")
    other = [(f, r) for f, row in rows.items() for r in row["records"]
             if r["disp"] == "REFUTED" and r["ctx"] != CTX[row["category"]]]
    P(f"   REFUTED in a case file in a context other than its category: {len(other)}")
    for f, r in other: P(f"      {f}:{r['line']} [{r['ctx']}] {r['name']}")

    if a.json:
        json.dump(rows, open(a.json, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
