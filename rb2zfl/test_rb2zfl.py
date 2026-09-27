# -*- coding: utf-8 -*-
"""Regression gate for rb2zfl: fixture -> expected dispositions (multiset)."""
import sys, os, collections, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rb2zfl
FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
EXPECT = {
    "r1_cmd_injection.rb": ["REFUTED"],
    "r2_clean.rb":         [],
    "r3_sql_concat.rb":    ["REFUTED"],
    "r4_eval.rb":          ["REFUTED"],
    "r5_xss.rb":           ["REFUTED"],
    "r6_backtick.rb":      ["REFUTED"],
    "x1_crossmethod.rb":   ["REFUTED"],
    "r7_xss_escaped.rb":   ["REFUTED"],   # ERB::Util.html_escape credited for xss; raw REFUTED
    # slice 2 (2026-09-27): each was silent (or undecided) on the slice-1 engine
    "u01_implicit_return.rb": ["REFUTED"],  # the last expression is the return value
    "u02_block.rb":        ["REFUTED"],   # block bodies are walked (were not parsed)
    "u03_rescue.rb":       ["REFUTED"],   # rescue bodies are walked (were dropped)
    "u04_opassign.rb":     ["REFUTED"],   # += joins (was read as =)
    "u05_massign.rb":      ["REFUTED"],   # a, b = v assigns
    "u06_shovel.rb":       ["REFUTED"],   # arr << v folds into the array
    "u07_hash_store.rb":   ["REFUTED"],   # h[:k] = v folds into the hash
    "u08_case.rb":         ["REFUTED"],   # case/when joined, not walked in sequence
    "u09_zreturn.rb":      ["OPEN"],      # the program's own `h` wins over the catalogue escaper `h`
    "u10_to_i.rb":         [],            # to_i gives a number
}
def main():
    fails = []
    for name, exp in EXPECT.items():
        got = [d for _, _, _, d in rb2zfl.analyze(os.path.join(FIX, name))]
        if collections.Counter(got) != collections.Counter(exp):
            fails.append(f"{name}: expected {sorted(exp)}, got {sorted(got)}")
    xf = rb2zfl.analyze_app(sorted(glob.glob(os.path.join(FIX, "xfile", "*.rb"))))
    if collections.Counter(o[4] for o in xf).get("REFUTED", 0) < 1:
        fails.append(f"xfile: expected cross-file REFUTED, got {[o[4] for o in xf]}")
    if fails:
        print("FAIL"); [print("  -", f) for f in fails]; sys.exit(1)
    print(f"PASS: {len(EXPECT)} Ruby fixtures + cross-file, dispositions as expected")
if __name__ == "__main__": main()
