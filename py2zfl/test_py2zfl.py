# -*- coding: utf-8 -*-
"""Regression gate for code2py: each fixture -> expected dispositions (order-independent multiset)."""
import sys, os, collections, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import py2zfl
FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
EXPECT = {
    "f1_tainted_shell.py":     ["REFUTED"],
    "f2_sanitized_shell.py":   ["EARNED"],
    "f3_unknown_source.py":    ["OPEN"],
    "f4_sql_param.py":         ["EARNED","REFUTED"],
    "f5_flask_eval.py":        ["REFUTED"],
    "g1_whitelist.py":         ["EARNED","REFUTED"],
    "g2_subprocess.py":        ["REFUTED"],
    "s1_ssti.py":              ["REFUTED"],
    "x3_xss_marksafe.py":      ["REFUTED"],   # mark_safe(raw)=xss; mark_safe(escape(x)) clean (no finding)
    "s2_pickle_cookie.py":     ["REFUTED"],
    "s3_secure_filename.py":   ["EARNED"],
    "x1_crossfn.py":           ["REFUTED","EARNED"],
    "x2_passthrough.py":       ["EARNED","REFUTED"],
    "c1_method_sink.py":       ["REFUTED","EARNED"],
    "c2_name_collision.py":    ["REFUTED"],
    "v1_flask_view.py":        ["REFUTED"],
    "v2_fastapi.py":           ["REFUTED"],
    # slice 4 (2026-09-27): each was EARNED (a false "clean") or silent on the slices-1-3 engine
    "u01_zreturn.py":          ["OPEN"],     # a helper returning an unknown value: Z, not F
    "u02_return_before_reassign.py": ["REFUTED"],  # returns captured where they happen
    "u03_trycatch.py":         ["REFUTED"],  # except does not overwrite the try path
    "u04_loop_zero.py":        ["REFUTED"],  # a loop may run zero times
    "u05_augassign.py":        ["REFUTED"],  # += joins
    "u06_unpack.py":           ["REFUTED"],  # a, b = v assigns
    "u07_list_append.py":      ["REFUTED"],  # append folds into the list; " ".join passes it
    "u08_dict_store.py":       ["REFUTED"],  # d[k] = v folds into the dict
    "u09_escape_ctx.py":       ["REFUTED"],  # html.escape is clean for xss only
    "u10_kwargs.py":           ["REFUTED"],  # a keyword argument reaches its parameter
    "u11_callee_after.py":     ["REFUTED"],  # summaries to a fixpoint: callee defined after the caller
    "u12_safe_int.py":         ["EARNED"],   # int(...) is clean
    "u13_walrus.py":           ["REFUTED"],  # := assigns
    "u14_self_method.py":      ["REFUTED"],  # self.method resolves to the enclosing class
    # slice 5 (2026-09-27, from the cloud's blind corpus, PR #5)
    "w01_flask_return.py":     ["REFUTED"],  # a route variable returned as HTML; <int:> and a dict are clean
    "w02_fastapi.py":          ["REFUTED"],  # FastAPI Query param is input; Literal[...] is validated
    "w03_file_sinks.py":       ["REFUTED","REFUTED","REFUTED"],  # send_file, Path(..).read_text, os.remove
    "w04_sql.py":              ["REFUTED","REFUTED"],  # bind params do not clean a tainted text; objects.raw
    "w05_guards.py":           ["REFUTED"],  # isdigit/not in NAMED/fullmatch is None + abort; int() in try
    "w06_templates.py":        ["REFUTED","REFUTED","REFUTED"],  # autoescape off, |safe, escape(quote=False)
}
def main():
    fails=[]
    for name, exp in EXPECT.items():
        src=open(os.path.join(FIX,name),encoding="utf-8").read()
        got=[d for _,_,_,d,_ in py2zfl.analyze(src)]
        if collections.Counter(got)!=collections.Counter(exp):
            fails.append(f"{name}: expected {sorted(exp)}, got {sorted(got)}")
    # cross-file fixture
    xf=py2zfl.analyze_app(sorted(glob.glob(os.path.join(FIX,"xfile","*.py"))))
    xd=collections.Counter(o[4] for o in xf)
    if xd.get("REFUTED",0)<1: fails.append(f"xfile: expected a cross-file REFUTED, got {dict(xd)}")
    if fails:
        print("FAIL"); [print("  -",f) for f in fails]; sys.exit(1)
    print(f"PASS: {len(EXPECT)} fixtures + cross-file, all dispositions as expected")
if __name__=="__main__": main()
