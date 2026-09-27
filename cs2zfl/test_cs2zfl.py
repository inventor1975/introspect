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
    # slice 2 (2026-09-27): each was silent (or undecided) on the slice-1 engine
    "u01_zreturn.cs":       ["OPEN"],      # a helper returning an unknown value: Z, not F
    "u02_trycatch.cs":      ["REFUTED"],   # catch does not overwrite the try path
    "u03_switch.cs":        ["REFUTED"],   # switch sections joined
    "u04_loop_zero.cs":     ["REFUTED"],   # a foreach may run zero times
    "u05_plus_eq.cs":       ["REFUTED"],   # += joins (was read as =)
    "u06_builder.cs":       ["REFUTED"],   # sb.Append(v) folds into the builder
    "u07_replace_recv.cs":  ["REFUTED"],   # s.Replace("a","b") keeps s's taint (read only its argument)
    "u08_member_store.cs":  ["REFUTED"],   # o.Cmd = v; o.Cmd reads v
    "u09_callee_after.cs":  ["REFUTED"],   # summaries to a fixpoint
    "u10_parse_int.cs":     [],            # int.Parse gives a number
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
