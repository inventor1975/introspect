# -*- coding: utf-8 -*-
"""Regression gate for js2zfl: fixture -> expected dispositions (multiset)."""
import sys, os, collections, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import js2zfl
FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
EXPECT = {
    "j1_cmd_injection.js": ["REFUTED"],
    "j2_clean.js":         [],
    "j3_sql_concat.js":    ["REFUTED"],
    "j4_eval.js":          ["REFUTED"],
    "j5_xss.js":           ["REFUTED"],
    "x1_crossfunc.js":     ["REFUTED"],
    "j6_guard.js":         ["REFUTED"],   # whitelist .includes guard narrows; unguarded call still fires
    "j7_guard_neg.js":     [],            # negated .has membership + return -> validated after
    "j8_xss_escaped.js":   ["REFUTED"],   # he.encode credited for xss; raw send REFUTED
}
def main():
    fails = []
    for name, exp in EXPECT.items():
        got = [d for _, _, _, d in js2zfl.analyze(os.path.join(FIX, name))]
        if collections.Counter(got) != collections.Counter(exp):
            fails.append(f"{name}: expected {sorted(exp)}, got {sorted(got)}")
    xf = js2zfl.analyze_app(sorted(glob.glob(os.path.join(FIX, "xfile", "*.js"))))
    if collections.Counter(o[4] for o in xf).get("REFUTED", 0) < 1:
        fails.append(f"xfile: expected cross-file REFUTED, got {[o[4] for o in xf]}")
    if fails:
        print("FAIL"); [print("  -", f) for f in fails]; sys.exit(1)
    print(f"PASS: {len(EXPECT)} JS fixtures + cross-file, dispositions as expected")
if __name__ == "__main__": main()
