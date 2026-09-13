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
