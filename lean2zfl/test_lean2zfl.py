# -*- coding: utf-8 -*-
"""Regression gate for lean2zfl: every theorem in fixtures/*.lean carries `-- EXPECT <DISPOSITION>` right above it.
Needs a Lake project with Mathlib to elaborate the fixtures in: LEAN2ZFL_PROJECT (default ../ztl-classical)."""
import glob, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("LEAN2ZFL_PROJECT", os.path.join(os.path.dirname(os.path.dirname(HERE)), "ztl-classical"))
import lean2zfl  # noqa: E402

if not os.path.isdir(os.path.join(os.environ["LEAN2ZFL_PROJECT"], ".lake", "packages", "mathlib")):
    print(f"SKIPPED: no Mathlib project at {os.environ['LEAN2ZFL_PROJECT']} (not a pass)")
    sys.exit(2)
fails, n = [], 0
for fx in sorted(glob.glob(os.path.join(HERE, "fixtures", "*.lean"))):
    expect, pending = {}, None
    for line in open(fx, encoding="utf-8"):
        m = re.match(r"--\s*EXPECT\s+([A-Z][A-Z ]*?)\s*[:—]", line)
        if m: pending = m.group(1).strip(); continue
        t = re.match(r"theorem\s+(\S+)", line)
        if t and pending: expect[t.group(1)] = pending; pending = None
    got = {r[2].split(".")[-1]: r[4] for r in lean2zfl.analyze_app([fx])}
    if lean2zfl.UNPARSED: fails.append(f"{fx}: not analysed: {lean2zfl.UNPARSED}")
    for name, want in expect.items():
        n += 1
        if got.get(name) != want: fails.append(f"{os.path.basename(fx)} {name}: expected {want}, got {got.get(name)}")
if fails:
    print("FAIL"); [print("  -", f) for f in fails]; sys.exit(1)
print(f"PASS: {n} theorems, every disposition as expected")
