# -*- coding: utf-8 -*-
"""Regression gate for java2zfl: fixture -> expected dispositions (multiset)."""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import java2zfl
FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
EXPECT = {
    "f1_cmd_injection.java": ["REFUTED"],
    "f2_clean.java":         [],
    "f3_sql_concat.java":    ["REFUTED"],
    "x1_crossmethod.java":   ["REFUTED"],
    "f4_guarded.java":        [],           # whitelist guard narrows -> clean
    "f5_negguard.java":       [],           # negated guard + early return -> clean
    "f6_xss_response.java":   ["REFUTED","REFUTED"],  # response-writer xss (chain + typed var)
    "f7_console_ok.java":     [],           # console/logger: receiver-aware, not sinks
    "f8_execute_recv.java":   ["REFUTED"],  # execute: Statement=sql, Executor=skipped
    "f9_spring_rce.java":     ["REFUTED"],  # @RequestParam source; @AuthenticationPrincipal is not
    "f10_prepared.java":      ["REFUTED"],  # concat prepareStatement flagged; parameterised safe
    "f11_bare_param.java":     ["REFUTED"],  # bare simple handler param = implicit @RequestParam source
    "f12_processbuilder.java": ["REFUTED"],  # new ProcessBuilder(array-of-taint) ctor sink
    "f13_xss_escaped.java":   ["REFUTED"],  # escapeHtml4 credited for xss; raw write REFUTED
    "f14_array_init.java":    ["REFUTED"],  # bare array-initializer {..taint..} -> ProcessBuilder
}
def main():
    fails=[]
    for name, exp in EXPECT.items():
        got=[d for _,_,_,d in java2zfl.analyze(open(os.path.join(FIX,name),encoding="utf-8").read())]
        if collections.Counter(got)!=collections.Counter(exp):
            fails.append(f"{name}: expected {sorted(exp)}, got {sorted(got)}")
    import glob
    xf=java2zfl.analyze_app(sorted(glob.glob(os.path.join(FIX,'xfile','*.java'))))
    import collections as _c
    if _c.Counter(o[4] for o in xf).get('REFUTED',0)<1: fails.append(f'xfile: expected cross-file REFUTED, got {[o[4] for o in xf]}')
    if fails: print("FAIL"); [print("  -",f) for f in fails]; sys.exit(1)
    print(f"PASS: {len(EXPECT)} Java fixtures + cross-file, dispositions as expected")
if __name__=="__main__": main()
