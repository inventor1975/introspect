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
    # slice 6 (2026-09-27): the OWASP Benchmark run's silent-EARNED mechanisms, each pinned
    "f15_newcall.java":        ["REFUTED"],  # new Test().doSomething(param): read as the call, not as new Test()
    "f16_switch.java":         ["REFUTED"],  # switch is walked (a case assigns the source)
    "f17_switch_dead.java":    [],           # switch on a constant char: only the live case
    "f18_ternary_dead.java":   ["REFUTED"],  # constant ?: -> safe arm; the other ?: picks the source
    "f19_if_dead.java":        [],           # constant if: the tainted else is dead
    "f20_list.java":           ["REFUTED"],  # list model: get(1) after remove(0) is safe, get(0) is the source
    "f21_map.java":            ["REFUTED"],  # map model: get("keyA") safe, get("keyB") the source
    "f22_escaped_sql.java":    ["REFUTED"],  # htmlEscape tags clean for xss ONLY: sql REFUTED, print clean
    "f23_decode.java":         ["REFUTED"],  # URLDecoder.decode passes taint (was Z)
    "f24_iface.java":          ["OPEN"],     # bodiless interface method: unknown, never an empty summary
    "f25_zreturn.java":        ["OPEN"],     # a helper returning an unknown value: Z, not F
    "f26_builder.java":        ["REFUTED","REFUTED"],  # list.add + pb.command(list); sb.append chain + printf
    "f27_trycatch.java":       ["REFUTED","REFUTED"],  # catch does not overwrite the try path; += joins
    "f28_cookies.java":        ["REFUTED"],  # cookie loop: the state at `break` reaches the loop exit
    "f29_uninit_unknown.java": ["OPEN"],     # an uninitialised local is Z
    "f30_helper_source.java":  ["REFUTED"],  # a helper that reads the request itself is a source (summary base)
    "f31_break_overwrite.java":["REFUTED"],  # a later overwrite does not erase the state that left by break
    "f32_exact_alloc.java":    ["REFUTED"],  # dispatch on the allocated class, not every subclass
    "f33_forever_loop.java":   ["REFUTED"],  # while(true){..break;}: exit only by break
    "f34_senderror.java":      ["OPEN"],     # sendError: container-dependent, soft
    "f35_matcher_guard.java":  [],           # P.matcher(x).matches() + early return is a whitelist guard
    "f36_process_stream.java": ["OPEN"],     # getInputStream on a Process is not a request source
    "f37_iface_impls.java":    ["REFUTED"],  # interface call: implementations vote, the bodiless declaration does not
    "f38_anon_impl.java":      ["OPEN"],     # an anonymous implementation is a candidate too: disagreement -> OPEN
    "f39_exec_dir.java":       ["REFUTED"],  # exec: command + envp carry the payload, the working dir does not
    "f40_lib_constant.java":   ["REFUTED","OPEN"],  # Locale.US is clean; an unknown lower-case field stays OPEN
    # slice 7 (2026-09-27, from the cloud's blind corpus, PR #2)
    "f41_outparam.java":       ["REFUTED"],  # a helper stores into the caller's StringBuilder (was EARNED)
    "f42_spring_return.java":  ["REFUTED","OPEN","REFUTED"],  # handler return = body: html / undeclared / entity
    "f43_view_name.java":      [],           # @Controller returning a view name is not a body
    "f44_subcontext.java":     ["REFUTED","REFUTED","REFUTED"],  # escaper credited only in its safe sub-context
    "f45_guards_tables.java":  ["REFUTED"],  # compound whitelist guard; literal-only lookup table
    "f46_neutralisers.java":   ["REFUTED"],  # URLEncoder.encode and a [^..] strip are clean; [<>] is not
    "f47_plaintext.java":      [],           # text/plain + nosniff is not HTML
    "f48_append_chain.java":   ["REFUTED"],  # PrintWriter.append returns the writer: the chain is a sink
    "f49_lambda_store.java":   ["OPEN"],     # a lambda's store into an outer builder is kept
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
