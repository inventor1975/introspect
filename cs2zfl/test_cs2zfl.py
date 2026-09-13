# -*- coding: utf-8 -*-
"""Regression gate for cs2zfl: fixture -> expected dispositions (multiset)."""
import sys, os, collections, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cs2zfl
FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
EXPECT = {
    "k1_cmd.cs":         ["REFUTED"],
    "k2_clean.cs":       [],
    "k3_sql.cs":         ["REFUTED"],
    "k4_xss.cs":         ["REFUTED"],   # HtmlEncode(msg) clean; raw msg xss
    "k5_deser.cs":       ["REFUTED"],   # BinaryFormatter.Deserialize of base64(tainted)
    "x1_crossmethod.cs": ["REFUTED"],   # cross-method summary (RunCmd param -> shell)
}
def main():
    fails = []
    for name, exp in EXPECT.items():
        got = [d for _, _, _, d in cs2zfl.analyze(os.path.join(FIX, name))]
        if collections.Counter(got) != collections.Counter(exp):
            fails.append(f"{name}: expected {sorted(exp)}, got {sorted(got)}")
    xf = cs2zfl.analyze_app(sorted(glob.glob(os.path.join(FIX, "xfile", "*.cs"))))
    if collections.Counter(o[4] for o in xf).get("REFUTED", 0) < 1:
        fails.append(f"xfile: expected cross-file REFUTED, got {[o[4] for o in xf]}")
    if fails:
        print("FAIL"); [print("  -", f) for f in fails]; sys.exit(1)
    print(f"PASS: {len(EXPECT)} C# fixtures + cross-file, dispositions as expected")
if __name__ == "__main__": main()
