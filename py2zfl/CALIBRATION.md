# py2zfl — calibration

## 2026-09-27 night — the first BLIND measure (cloud, PR #5) and what it changed (MEASURED)
Fresh authors who saw neither the analyzer nor its fixtures wrote a corpus committed before the analyzer ran.
On `e37a0c1`, blind: sqli 45.2/18.8, xss 7.1/0.0, code 59.4/16.7, file 29.0/3.4 — all **36.1% found, 9.8% false alarms, 49 silent** of 122 decided vulnerable (274 cases, cmdi refused by the filter). Until this, every claim for py2zfl rested on fixtures its author wrote.
Causes, fixed: a returned str from a Flask route IS the HTML body (judged for request values; an unknown value is listed as NOT JUDGED — the Java option (b)); make_response/Response/HTMLResponse; templates (autoescape on/off, |safe, Markup format/%/+/join); file sinks beyond open() (send_file, FileResponse, os.*/shutil.*, Path methods, save, extractall); Django raw()/extra(), execute(query=..); handler parameters as sources (Flask route vars, FastAPI Query/Path/Form, Django URL kwargs; <int:> and Literal[...] clean); `execute(tainted_text, params)` is NOT clean any more (it was: an unverified clean); guards: named sets, isdigit/fullmatch(..) is None + abort/raise/return, int() in try; HTML sub-contexts as in Java. Real apps: pygoat +2 REFUTED (its SQLi labs through objects.raw), microblog 1 OPEN (unchanged), flask tests: 11 REFUTED — test routes that echo a URL variable.
After the fixes, on the SAME corpus (fitted, not a measure): TPR / FPR / silent = 76.2 / 4.9 / 0. A new blind round is
the only way to get a number again.
