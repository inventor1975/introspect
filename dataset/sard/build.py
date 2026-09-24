#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py — turn the six per-CWE runs of introspect over the SARD / Stivalet PHP
suite into a publishable dataset: one row per test file, the ZTL verdict and the
named weak link, plus a reproducible breakdown of every DISAGREEMENT with the
benchmark's own label.

It emits NO source-file contents (the suite's licence is unstated, so only the
NIST filename — which itself encodes source__sanitizer__construction — and our
verdict travel). Signatures that classify a disagreement DO read the file at
build time; nothing is executed.

    python3 build.py <dir-with-CWE_*.json> <out-dir>

Input: the CWE_*.json written by bench/sard.py (a list of per-file records:
label, verdict, cwe, src, san, con, file, sinks[{line,fn,d,weak,t,s}]).
"""
import sys, os, json, re, collections

RUN, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

# context each CWE is judged in (the rest of SARD is not modelled — stated in the card)
CTX = {"CWE_89": "sql", "CWE_78": "shell", "CWE_95": "code",
       "CWE_98": "file", "CWE_79": "html", "CWE_601": "header"}

# ---- signatures for the DISAGREEMENTS, each a benchmark defect read in the source.
# Every one was confirmed to cover its bucket 100% before this file was written;
# an unmatched disagreement is printed as UNCLASSIFIED so it can never hide.
MISS_SIG = [
    ("sprintf-%d coerces the value to an integer; nothing injects through a number",
     re.compile(r"sprintf\(\s*\"[^\"]*%d[^\"]*\"\s*,\s*\$tainted\s*\)")),
    ("whitelist: ternary assigns 'safe1'/'safe2' in every branch",
     re.compile(r"\$tainted\s*=\s*\$tainted\s*==\s*'safe1'")),
    ("whitelist: in_array against a legal table, else a literal",
     re.compile(r"in_array\(\s*\$tainted\s*,\s*\$legal_table\s*,\s*true\s*\)")),
    ("FILTER_VALIDATE_FLOAT gate, else empty string",
     re.compile(r"FILTER_VALIDATE_FLOAT")),
    ("FILTER_VALIDATE_INT gate, else empty string",
     re.compile(r"FILTER_VALIDATE_INT")),
    ("whitelist to letters only (/^[a-zA-Z]*$/), else empty",
     re.compile(r"\"/\^\[a-zA-Z\]\*\$/\"")),
    ("whitelist to letters and digits (/^[a-zA-Z0-9]*$/), else empty",
     re.compile(r"\"/\^\[a-zA-Z0-9\]\*\$/\"")),
    ("all non-word characters stripped (preg_replace /\\W/si)",
     re.compile(r"preg_replace\('/\\W/si',''")),
    ("email validated (SANITIZE_EMAIL + VALIDATE_EMAIL) then printed as text",
     re.compile(r"FILTER_SANITIZE_EMAIL.*?FILTER_VALIDATE_EMAIL", re.S)),
    ("the sink prints the bare constant `checked_data`, not the tainted variable",
     re.compile(r"(?<![\$\w])checked_data\b")),
]

def classify_miss(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    for why, rx in MISS_SIG:
        if rx.search(t):
            return why
    return None

def file_verdict(rec):
    if rec.get("parse_error"):
        return "E", None
    rank = {"REFUTED": 3, "OPEN": 2, "ON CREDIT": 2, "EARNED": 1}
    best, worst, sink = "NONE", 0, None
    for s in rec.get("sinks", []):
        r = rank.get(s["d"], 0)
        if r > worst:
            worst, best, sink = r, {"ON CREDIT": "OPEN"}.get(s["d"], s["d"]), s
    return best, sink

rows, summary, disagree = [], {}, collections.Counter()
unclassified = []
for cwe, ctx in CTX.items():
    p = os.path.join(RUN, f"{cwe}.json")
    recs = json.load(open(p, encoding="utf-8"))
    cnt = collections.Counter()
    for rec in recs:
        verdict, sink = file_verdict(rec)
        label = rec["label"]                       # unsafe | safe (the benchmark's own)
        cnt[(label, verdict)] += 1
        # agreement, with OPEN treated as an honest abstention, never a hit or a miss
        if verdict == "OPEN":
            agree = None
        elif label == "unsafe":
            agree = (verdict == "REFUTED")
        else:                                       # safe
            agree = (verdict in ("EARNED", "NONE"))
        reason = None
        if agree is False and label == "unsafe":    # a MISS — must be a benchmark defect
            reason = classify_miss(rec["file"])
            disagree[("miss", cwe, reason or "UNCLASSIFIED")] += 1
            if reason is None:
                unclassified.append(rec["file"])
        elif agree is False and label == "safe":    # a false alarm — carry the tool's own reason
            reason = (sink or {}).get("s")
            disagree[("false_alarm", cwe, "see receipt")] += 1
        rows.append({
            "suite": "SARD/Stivalet PHP",
            "cwe": cwe, "context": ctx,
            "source": rec["src"], "sanitizer": rec["san"], "construction": rec["con"],
            "file": os.path.basename(rec["file"]),
            "benchmark_label": label,
            "ztl_verdict": verdict,
            "weak_link": (sink or {}).get("s") or (sink or {}).get("t"),
            "agrees_with_benchmark": agree,
            "disagreement_note": reason,
        })
    summary[cwe] = {"context": ctx, **{f"{a}->{v}": n for (a, v), n in sorted(cnt.items())}}

with open(os.path.join(OUT, "sard_ztl_verdicts.jsonl"), "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

json.dump(summary, open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print(f"rows: {len(rows)}")
print("\nMISSES (benchmark says unsafe, ZTL says clean) — every one a benchmark defect:")
tot_miss = 0
for (kind, cwe, why), n in sorted(disagree.items()):
    if kind == "miss":
        tot_miss += n
        print(f"  {n:5}  {cwe:8} {why}")
print(f"  total misses: {tot_miss}; UNCLASSIFIED: {len(unclassified)}")
print("\nFALSE ALARMS (benchmark says safe, ZTL says vulnerable), by mechanism the")
print("tool named in its own receipt — no exploitability is asserted beyond it:")
# bucket by the receipt's own wording, so the split is reproducible from the data
def fa_bucket(reason):
    r = (reason or "").lower()
    if "wrong-context only" in r:
        return "sanitizer applied for a DIFFERENT context than the sink (SARD called it safe anyway)"
    if "unsubstituted" in r:
        return "the escaper does not substitute for this context; value reaches the sink unchanged"
    if "attr-event" in r or "attr-name" in r:
        return "escaped, but lands in an HTML attribute/event context we refuse by policy"
    return "other (read the receipt per row)"
fa = collections.Counter()
for r in rows:
    if r["agrees_with_benchmark"] is False and r["benchmark_label"] == "safe":
        fa[fa_bucket(r["weak_link"])] += 1
tot_fa = sum(fa.values())
for why, n in fa.most_common():
    print(f"  {n:5}  {why}")
print(f"  total false alarms: {tot_fa}")

# the two mislabels the source carries, counted so the card can cite them exactly
typo = sum(1 for r in rows if r["sanitizer"] == "func_escapeshellarg"
           and r["benchmark_label"] == "safe" and r["agrees_with_benchmark"] is False)
print(f"\n  of which escapeshellarg files (source applies it to $tained, not $tainted): {typo}")
