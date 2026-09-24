#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
confirm_alarms.py — MEASURE, for every false alarm (benchmark says safe, ZTL says
vulnerable), whether the context's dangerous metacharacter actually reaches the
sink. No "vulnerable" claim is left resting on reasoning.

Safe by construction:
  * every SINK that is a FUNCTION is stubbed to a no-op (mysql_query, system,
    exec, shell_exec, passthru, popen, proc_open, header, mail, file_get_contents,
    mysql_fetch_array->false so no loop runs, ...);
  * the two SINKS that are language CONSTRUCTS (eval, include/require) cannot be
    stubbed, so the source is truncated BEFORE the first such token — it never runs;
  * legacy mysql_* (removed in PHP 8) are defined as stubs; mysql_real_escape_string
    -> addslashes (both escape the quote identically — stated, not hidden);
  * a shutdown hook dumps the global string variables; the value the sink would
    receive ($query/$tainted/$sanitized/...) is read from there.

    survives raw     -> guard did NOT neutralise -> our REFUTED stands (benchmark mislabel)
    escaped/removed  -> neutralised for this context -> our alarm is conservative,
                        NOT a confirmed vulnerability

    python3 confirm_alarms.py <run-dir> <out.jsonl>
"""
import sys, os, json, subprocess, base64, tempfile, collections, re

RUN, OUT = sys.argv[1], sys.argv[2]
CTX = {"CWE_89": "sql", "CWE_78": "shell", "CWE_95": "code",
       "CWE_98": "file", "CWE_79": "html", "CWE_601": "header"}
PROBE = "Q" + "".join(m + "Q" for m in ["'", '"', "<", ">", "&", "|", ";", "$",
                                        "`", "(", ")", "/", "\\"]) + "\r\n"
CONSTRUCT = re.compile(r"\b(eval|include|require)(_once)?\b")

PRELUDE = r'''<?php
error_reporting(0);
function __stub(){return null;}
foreach(['system','exec','shell_exec','passthru','popen','proc_open','pcntl_exec',
         'mysql_query','mysql_connect','mysql_select_db','mysql_close','mysql_num_rows',
         'mysql_error','mysqli_query','mysqli_connect','header','setcookie','mail',
         'file_get_contents','file_put_contents','fopen','readfile','curl_exec'] as $fn){
  if(!function_exists($fn)){ eval("function $fn(){ return null; }"); }
}
if(!function_exists('mysql_fetch_array')){function mysql_fetch_array($r=null){return false;}}
if(!function_exists('mysql_fetch_assoc')){function mysql_fetch_assoc($r=null){return false;}}
if(!function_exists('mysql_real_escape_string')){function mysql_real_escape_string($s,$l=null){return addslashes($s);}}
if(!function_exists('mysql_escape_string')){function mysql_escape_string($s){return addslashes($s);}}
if(!function_exists('mysqli_real_escape_string')){function mysqli_real_escape_string($c,$s){return addslashes($s);}}
if(!defined('FILTER_SANITIZE_MAGIC_QUOTES')){define('FILTER_SANITIZE_MAGIC_QUOTES', FILTER_SANITIZE_ADD_SLASHES);}
// FILTER_SANITIZE_MAGIC_QUOTES was removed in PHP 8; it was addslashes-equivalent,
// so it is modelled by FILTER_SANITIZE_ADD_SLASHES (stated in the card).
$__P = base64_decode($_SERVER['PROBE_B64']);
foreach(['UserData','userData','user_data','data','id','UserId','user_id','name'] as $k){
  $_GET[$k]=$__P; $_POST[$k]=$__P; $_REQUEST[$k]=$__P; $_COOKIE[$k]=$__P; $_SESSION[$k]=$__P;
}
$_SERVER['HTTP_USER_AGENT']=$__P; $_SERVER['HTTP_REFERER']=$__P;
register_shutdown_function(function(){
  $o=[]; foreach($GLOBALS as $k=>$v){ if(is_string($v)) $o[$k]=$v; }
  echo "\n@@VARS@@".base64_encode(json_encode($o, JSON_PARTIAL_OUTPUT_ON_ERROR|JSON_INVALID_UTF8_SUBSTITUTE));
});
?>'''

def reaches(ctx, vars_):
    order = ["tainted", "sanitized", "clean", "user", "data", "var", "url", "query"]
    for k in order:
        if isinstance(vars_.get(k), str) and PROBE[:1] in vars_[k]:
            return k, vars_[k]
    for k in order:
        if isinstance(vars_.get(k), str) and vars_[k]:
            return k, vars_[k]
    return None, ""

def raw_quote(t):
    return any(t[i] == "'" and (i == 0 or t[i-1] != "\\") for i in range(len(t)))

def survives(ctx, s):
    if ctx in ("sql", "code"):
        return raw_quote(s)
    if ctx == "shell":
        return any(c in s for c in ";|&`$()<>\n") or raw_quote(s)
    if ctx == "file":
        return "/" in s or "\\" in s or ".." in s
    if ctx == "html":
        return "<" in s or ">" in s or '"' in s
    if ctx == "header":
        return "\r" in s or "\n" in s or "/" in s
    return True

rows = []
for cwe, ctx in CTX.items():
    for rec in json.load(open(os.path.join(RUN, f"{cwe}.json"), encoding="utf-8")):
        if rec["label"] != "safe":
            continue
        worst, disp = 0, None
        for s in rec.get("sinks", []):
            r = {"REFUTED": 3, "OPEN": 2, "ON CREDIT": 2, "EARNED": 1}.get(s["d"], 0)
            if r > worst:
                worst, disp = r, s["d"]
        if disp != "REFUTED":
            continue
        src = open(rec["file"], encoding="utf-8", errors="replace").read()
        m = CONSTRUCT.search(src)
        # cut at the ';' ENDING the previous statement, so the sink statement
        # ($res = eval(...), $var = include(...)) is dropped whole, not mid-expression
        body = src[:src.rfind(';', 0, m.start()) + 1] if m else src
        script = PRELUDE + "\n" + body
        with tempfile.NamedTemporaryFile("w", suffix=".php", delete=False) as f:
            f.write(script); path = f.name
        try:
            env = dict(os.environ, PROBE_B64=base64.b64encode(PROBE.encode()).decode())
            out = subprocess.run(["php", path], capture_output=True, text=True,
                                 timeout=15, env=env).stdout
        finally:
            os.unlink(path)
        vars_ = {}
        if "@@VARS@@" in out:
            try:
                vars_ = json.loads(base64.b64decode(out.rsplit("@@VARS@@", 1)[1].strip())) or {}
            except Exception:
                vars_ = {}
        var, val = reaches(ctx, vars_)
        con_l = rec["con"].lower()
        if ctx == "html" and ("attr" in con_l or "event" in con_l or "handler" in con_l):
            confidence = "context-dependent"
        else:
            confidence = "high"
        surv = survives(ctx, val) if val else None
        verdict = ("not_neutralised" if surv else "neutralised") if val else "unmeasured"
        rows.append({"cwe": cwe, "context": ctx, "sanitizer": rec["san"],
                     "construction": rec["con"], "file": os.path.basename(rec["file"]),
                     "reaches_sink_var": var, "reaches_sink_value": val[:160],
                     "metachar_survives_raw": surv, "confirmation": verdict,
                     "confidence": confidence})

with open(OUT, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"false alarms measured: {len(rows)}")
by = collections.Counter((r["context"], r["sanitizer"].replace("func_", ""), r["confirmation"]) for r in rows)
for k, n in sorted(by.items()):
    print(f"  {n:4}  {k[0]:7} {k[1]:42} {k[2]}")
print("\nroll-up:")
for k, n in collections.Counter(r["confirmation"] for r in rows).most_common():
    print(f"  {n:5}  {k}")
