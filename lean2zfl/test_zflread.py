# -*- coding: utf-8 -*-
"""test_zflread — the Lean statement read by ZTL's numeric floor, tested from both sides (fixtures/Translate.lean).

    LEAN2ZFL_PROJECT=<a Lake project with Mathlib> python3 test_zflread.py

A false statement must be REFUTED or get a counterexample; a TRUE one must get none — a witness on t_div or t_abs is a
bug of the translator or of the floor, never a finding."""
import os
import re
import sys

import lean2zfl
import zflread

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "fixtures", "Translate.lean")
os.environ.setdefault("LEAN2ZFL_PROJECT", os.path.join(HERE, "..", "..", "ztl-classical"))
want = {}
lines = open(SRC, encoding="utf-8").read().splitlines()
for i, l in enumerate(lines):
    m = re.match(r"^-- (ZTL \w+|WITNESS \w+|UNTR|NATCONV|VACUOUS|HYPDOMAIN|LEANFALSE|SEQREFUTED|SEQVACUOUS|READINGS [^:]+)", l)
    if m:
        j = i + 1                                    # the comment may run over several lines
        while not re.search(r"theorem (\w+)", lines[j]):
            j += 1
        name = re.search(r"theorem (\w+)", lines[j]).group(1)
        want[name] = m.group(1)
fails = []
got_names = set()
for t in lean2zfl.dump_file(SRC):
    if "name" not in t:
        fails.append(f"dump failed: {t}")
        continue
    short = t["name"].split(".")[-1]
    if short not in want:
        continue
    got_names.add(short)
    r = zflread.read_safe(t)
    w, exp = r.get("witness") or {}, want[short]
    if exp == "UNTR":
        ok = not r.get("translated")
    elif exp.startswith("READINGS"):                 # the conventions as dirty parameters: overall + per-method verdicts
        parts = exp.split()
        want_overall, cells = parts[1], dict(x.split("=") for x in parts[2:])
        got = {row["M"]: row["verdict"] for row in r.get("readings", [])}
        ok = r.get("ztl") == want_overall and all(got.get(m) == v for m, v in cells.items())
    elif exp == "SEQREFUTED":                        # a sequence: refuted at a point, a sequence exists, never EARNED
        ok = w.get("existence") == "recursion" and "refuted_at" in w and r.get("ztl") == "OPEN"
    elif exp == "SEQVACUOUS":                        # no sequence satisfies the hypotheses: no refutation
        ok = r.get("vacuous") is True and "refuted_at" not in w
    elif exp == "LEANFALSE":                         # false in Lean's semantics only: no exact counterexample
        ok = r.get("lean_refuted_at") is not None and "refuted_at" not in w
    elif exp == "HYPDOMAIN":                         # an unguarded partial operation reported IN A HYPOTHESIS
        ok = any(d[2].startswith("hyp") and d[1] in ("OPEN", "NOWHERE") for d in r.get("domain", []) if len(d) > 2) \
            and "refuted_at" not in w
    elif exp == "VACUOUS":                           # hypotheses refuted: no admissible point, no refutation
        ok = r.get("vacuous") is True and "refuted_at" not in w and r.get("ztl") != "EARNED"
    elif exp == "NATCONV":                           # the mathematics refuted, Lean's ℕ convention holds (variant В)
        ok = r.get("rests_on_nat_convention") is True
    elif exp.startswith("ZTL "):
        ok = r.get("ztl") == exp[4:]
    elif exp == "WITNESS refuted":
        ok = "refuted_at" in w
    else:                                            # WITNESS none
        ok = "refuted_at" not in w and "no_subject_at" not in w and r.get("ztl") != "REFUTED"
    print(f"{'ok  ' if ok else 'FAIL'} {short:8} want {exp:16} got {r.get('ztl')} {w}")
    if not ok:
        fails.append(short)
missing = set(want) - got_names
if missing:
    fails.append(f"not dumped: {sorted(missing)}")
print(f"ZFLREAD GREEN — {len(want)} statements" if not fails else f"ZFLREAD RED: {fails}")
sys.exit(1 if fails else 0)
