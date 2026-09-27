# js2zfl — calibration

## 2026-09-27 night — the first BLIND measure (cloud, PR #4) and what it changed (MEASURED)
Fresh authors who saw neither the analyzer nor its fixtures wrote a corpus committed before the analyzer ran.
On `e37a0c1`, blind: xss 42.9/32.3, file 48.3/13.8 — all **45.6% found, 23.3% false alarms, 18 silent** of 57 decided vulnerable (133 cases; sqli, code and cmdi refused by the filter). Until this, every claim for js2zfl rested on fixtures its author wrote.
Causes, fixed: res.sendFile/download are FILE sinks (root: confines unless '/'); fs functions imported by name; koa-send; Koa ctx.body; res.send(object|array) is JSON; the view data of res.render; request properties set by middleware are Z (were F); NestJS @Query/@Param/@Body and destructured request parameters as sources; class-property arrow handlers were never parsed; callbacks are linked to their bodies (filter(guard), map(escaper), map(-> array) as JSON); anchored-only regex guards, reset-to-constant, ctx.throw terminates; compiled Handlebars/Pug templates escape unless the template has a raw marker; hand-written and single-replace escapers, [^..] strips; text/plain; let/const block scope; HTML sub-contexts as in Java. Two of the seven new fixtures (y03, y07) also pass on the old engine by count only — it made one wrong call for one missed one.
After the fixes, on the SAME corpus (fitted, not a measure): TPR / FPR / silent = 66.7 / 5.0 / 0. A new blind round is
the only way to get a number again.

## 2026-09-27 — slice 3: the java2zfl soundness lesson ported (MEASURED)
14 new fixtures (u01–u14), all 14 fail on the slices-1-2 engine: 9 real flows it was SILENT on (a Z
helper return read as F, catch overwriting try, switch cases walked in sequence, a loop assumed to
run, `c += x` read as `c = x`, `o.cmd = v`, a return before a reassignment, a callee defined after
its caller) — plus 1 false REFUTED (`Number(x)`), and 4 OPEN that are now decided. Parser (jsast.js)
now keeps assignment operators, destructuring names, loop heads, break/continue, switch defaults.
- NodeGoat: 5 REFUTED, 3 OPEN — unchanged.
- express, outside test/: 6 REFUTED (same set), OPEN 15 -> 16. Two false REFUTED that an early version
  of this slice raised (`req.pet.name = body..` then `res.redirect('/pet/' + req.pet.id)`) are OPEN:
  a field store taints that field and makes the object only Z.
- express test/: +~180 OPEN, nearly all `request(createApp())` — supertest's `request` collides with
  the bare-name SSRF sink `request`, and `createApp()`'s return used to be read as F (the bug fixed
  here). A precision issue of the bare-name sink, left open and named, not tuned away.
- No labelled denominator for JS.

## 2026-09-13 — calibration on real Node apps (MEASURED)

Parser is @babel/parser (jsast helper) — no API/LLM calls, no token spend.
Verdicts: REFUTED (tainted reaches sink) / OPEN (не знаю) / clean.

## express core lib/ (the framework itself, mature/clean) — false-positive check
- 6 lib files. **0 findings.** Zero false positives on clean framework code.
  (express EXAMPLES contain real request-echoing patterns, so they are not a clean target — see below.)

## NodeGoat (OWASP deliberately-vulnerable Express app) — true-positive check
- ~30 app .js (vendored/minified assets excluded). **5 REFUTED (all verified TRUE), 2 OPEN.**
- REFUTED (verified by reading source):
  - contributions.js:32-34 [code] eval(req.body.preTax/afterTax/roth) — SSJS injection (source comment: "Insecure use of eval()").
  - research.js:16 [ssrf] needle.get(req.query.url + req.query.symbol) — server-side request forgery.
  - index.js:72 [redirect] res.redirect(req.query.url) — open redirect (source comment: "Insecure ... redirects").
- OPEN (honest не знаю): Gruntfile.js exec (build tooling, not request-handling) + 1 xss with untraced source.
- express example examples/vhost/index.js:30 res.send('requested ' + req.params.sub) — a REAL reflected-XSS
  pattern in an illustrative example; correctly REFUTED (not a false positive).

## Precision fix found DURING calibration
`regex.exec(str)` (RegExp.prototype.exec, e.g. jQuery) collided with child_process `exec` -> flagged shell.
Fixed: member-form shell sinks are gated on a child_process receiver (cp/child_process/...); a bare
destructured `exec()` still counts. Same bare-method-name lesson as php `->execute` / java / go.

## Contract parity
All INTROSPECT-SEMANTICS.md §4 rules: summaries (cross-fn + cross-file), guards (=== / .includes/.has /
negated-early-return) + branch-join, receiver-gated sinks (res.* xss, HTTP-client ssrf, child_process shell,
fs.* file), Express/Koa entry-point handlers (incl. inline arrows). Sinks: shell/code/sql/xss/file/ssrf/redirect.

## Gate
8 fixtures + cross-file green. Fixtures j1-j7 + x1 + xfile/. Needs `npm install` (@babel/parser).
