# js2zfl — calibration on real Node apps (2026-09-13, MEASURED)

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
