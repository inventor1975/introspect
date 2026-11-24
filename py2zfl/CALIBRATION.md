# py2zfl — calibration

## 2026-11-24 — the seven dispositions: a CHECKED RE-READ is EARNED IF STABLE (MEASURED)
`if request.args.get("f") in ALLOWED: os.system("cat " + request.args.get("f"))` checks ONE read of the source and
uses ANOTHER. The engine said REFUTED (a false accusation: if the source gives the same value twice, the use is
covered); env-var re-reads said OPEN. Now a guard narrows a re-readable expression (call / attribute / subscript)
as well as a name; a sink that is clean ONLY through such a checked re-read is judged with the TOCTOU shape
(`~ok | ok`, `ok` dirty, two occurrences) -> EARNED IF STABLE. A local read once and checked stays plain EARNED.
Fixtures t01–t05 (t01, t04 were REFUTED, t05 OPEN on 2ecc659). Not built yet: the rule on the summary path
(a checked re-read passed into a helper) and on `_more_sinks`.
Measured, before vs after: blind round 1 and round 2 scores IDENTICAL (no re-read after a check in either corpus);
our own Python (ztlstudio, ztl-space/api, LogicBridge, gemma4-kaggle/lab, veip-use: 3,014 findings) IDENTICAL.
So the rule is exact where it applies and moves nothing else; how often it applies in the wild is NOT measured.
Scoring buckets in blind*/score.py: ON CREDIT, EARNED IF STABLE, REFUTED IF STABLE, E -> the OPEN bucket.
Real apps (cloned 2026-11-24, depth 1): pygoat @ 2aa4cc1 (26 findings: 6 R / 18 O / 2 E), flask @ 49943b5
(50: 11 R / 39 O), microblog @ a975ef6 (1 O) — IDENTICAL before and after. MEASURED frequency of a checked
re-read reaching a sink in these apps: 0. PHP differs on purpose: a re-read of `$_GET['x']` after a check is
EARNED there, because a superglobal element is a plain value whose every write the engine tracks; a Python
`request.args.get(..)` is a CALL the engine cannot prove returns the same value twice.

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
