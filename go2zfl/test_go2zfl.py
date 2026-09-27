# -*- coding: utf-8 -*-
"""Regression gate for go2zfl: fixture -> expected dispositions (multiset)."""
import sys, os, collections, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import go2zfl
FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
EXPECT = {
    "g1_cmd_injection.go": ["REFUTED"],
    "g2_clean.go":         [],
    "g3_sql_concat.go":    ["REFUTED"],
    "g4_query_get.go":     ["REFUTED"],   # r.URL.Query().Get chain source
    "x1_crossfunc.go":     ["REFUTED"],   # cross-function summary (runCmd param -> shell)
    "g6_gin_multi.go":     ["REFUTED","REFUTED","REFUTED","REFUTED"],  # gin src -> shell/file/ssrf/xss
    "g7_write_xss.go":     ["REFUTED"],   # receiver-typed w.Write; constant db.Query not flagged
    "g8_prepared.go":      ["REFUTED"],   # concat Query flagged; prepared stmt.QueryRow(bound) not
    "g9_const_ddl.go":     ["REFUTED"],   # package-level const DDL -> clean (not OPEN); tainted concat flagged
    "g10_guard_eq.go":     ["REFUTED"],   # equality guard narrows then-branch; unguarded call still fires
    "g11_guard_neg.go":    [],            # negated map-membership + return -> validated after
    "g12_xss_escaped.go":  ["REFUTED"],   # html.EscapeString credited for xss; raw Write REFUTED
    # slice 5 (2026-09-27): each was silent (or undecided) on the slices-1-4 engine
    "u01_zreturn.go":       ["OPEN"],      # a helper returning an unknown value: Z, not F
    "u02_switch.go":        ["REFUTED"],   # switch cases joined, not walked in sequence
    "u03_loop_zero.go":     ["REFUTED"],   # a range may run zero times
    "u04_plus_eq.go":       ["REFUTED"],   # += joins
    "u05_map_store.go":     ["REFUTED"],   # m[k] = v folds into the map
    "u06_builder.go":       ["REFUTED"],   # b.WriteString(v) folds into the builder
    "u07_append_join.go":   ["REFUTED"],   # append + strings.Join pass it
    "u08_return_before.go": ["REFUTED"],   # returns captured where they happen
    "u09_callee_after.go":  ["REFUTED"],   # summaries to a fixpoint
    "u10_atoi.go":          [],            # strconv.Atoi / Itoa give numbers
}
def main():
    fails = []
    for name, exp in EXPECT.items():
        got = [d for _, _, _, d in go2zfl.analyze(os.path.join(FIX, name))]
        if collections.Counter(got) != collections.Counter(exp):
            fails.append(f"{name}: expected {sorted(exp)}, got {sorted(got)}")
    xf = go2zfl.analyze_app(sorted(glob.glob(os.path.join(FIX, "xfile", "*.go"))))
    if collections.Counter(o[4] for o in xf).get("REFUTED", 0) < 1:
        fails.append(f"xfile: expected cross-file REFUTED, got {[o[4] for o in xf]}")
    if fails:
        print("FAIL"); [print("  -", f) for f in fails]; sys.exit(1)
    print(f"PASS: {len(EXPECT)} Go fixtures + cross-file, dispositions as expected")
if __name__ == "__main__": main()
