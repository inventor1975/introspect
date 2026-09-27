# py2zfl — calibration

## 2026-09-27 night — blind ROUND 2 (cloud, PR #6) on slice 5 (`b49bb74`), then slice 6 (MEASURED)
A new corpus by new authors (204 cases: sqli 66, xss 71, file 67; code and cmdi refused by the filter),
committed at `195a2d9` before the run. **Blind: 71.3% found, 5.4% false alarms, 9 silent** of 94 decided
vulnerable (sqli 80.6/3.4, xss 68.8/6.1, file 64.5/6.5). Reproduced here exactly. Round 1 was 36.1/9.8/49 —
a different corpus: two measurements, not a growth curve.
8 of the 12 silences were route returns holding an unknown value: under the curator's option (b) they are not
judged, and introspect showed only their COUNT. Now each NOT JUDGED site is listed by line (all with --open).
Fixed at the causes (fixtures w07–w09, all fail on b49bb74): summaries now see THEIR OWN file's context (a
module-level allowlist did not guard inside a helper); import-resolved names (`from urllib.parse import unquote`);
decoding after an escaper drops its credit; request.get_json; exec_driver_sql; aiohttp web.Response(text=);
tempfile prefix/suffix/dir; a method on a call's result resolved by name (only there: on a plain variable it
hijacked Path.read_bytes — caught by the round-1 corpus before it shipped); a loop that checks each of a tuple of
variables; class-level (frozenset) allowlists; UUID/Decimal/date annotations clean; tuple returns unpacked per
position. Fitted afterwards: round 2 80.9 / 0.0 / 2 silent (both listed NOT JUDGED: state on self, an exception
message), round 1 79.5 / 3.3 / 0. Apps unchanged (pygoat 10 R / 18 O, flask 11 R / 39 O, microblog 1 O).

## 2026-09-27 night — the first BLIND measure (cloud, PR #5) and what it changed (MEASURED)
Fresh authors who saw neither the analyzer nor its fixtures wrote a corpus committed before the analyzer ran.
On `e37a0c1`, blind: sqli 45.2/18.8, xss 7.1/0.0, code 59.4/16.7, file 29.0/3.4 — all **36.1% found, 9.8% false alarms, 49 silent** of 122 decided vulnerable (274 cases, cmdi refused by the filter). Until this, every claim for py2zfl rested on fixtures its author wrote.
Causes, fixed: a returned str from a Flask route IS the HTML body (judged for request values; an unknown value is listed as NOT JUDGED — the Java option (b)); make_response/Response/HTMLResponse; templates (autoescape on/off, |safe, Markup format/%/+/join); file sinks beyond open() (send_file, FileResponse, os.*/shutil.*, Path methods, save, extractall); Django raw()/extra(), execute(query=..); handler parameters as sources (Flask route vars, FastAPI Query/Path/Form, Django URL kwargs; <int:> and Literal[...] clean); `execute(tainted_text, params)` is NOT clean any more (it was: an unverified clean); guards: named sets, isdigit/fullmatch(..) is None + abort/raise/return, int() in try; HTML sub-contexts as in Java. Real apps: pygoat +2 REFUTED (its SQLi labs through objects.raw), microblog 1 OPEN (unchanged), flask tests: 11 REFUTED — test routes that echo a URL variable.
After the fixes, on the SAME corpus (fitted, not a measure): TPR / FPR / silent = 76.2 / 4.9 / 0. A new blind round is
the only way to get a number again.
