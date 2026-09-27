# rb2zfl — calibration

## 2026-09-27 — slice 2: the java2zfl soundness lesson ported (MEASURED)
10 new fixtures (u01–u10), all fail on the slice-1 engine; 8 were SILENT on a real flow. The parser
(rbast.rb) now keeps block bodies (`method_add_block` was dropped whole), rescue/ensure, the `+=`
operator, multiple-assignment names, `for x in`, index stores, `case ... else`. A method's last
expression is its return value (implicit return was never read). The program's own `h`/`escape` now
wins over the catalogue escaper of that name.
- railsgoat: 2 REFUTED (same), OPEN 1 -> 6. The new ones include `app/models/benefits.rb:15` —
  railsgoat's command injection through an uploaded file name, `system("cp .. #{file.original_filename}")`
  inside `silence_streams(STDERR) { .. }`: the old engine never parsed that block. OPEN, not REFUTED:
  the caller `Benefits.save` collides with ActiveRecord's `save` by bare name.
- sinatra: OPEN 2 -> 17, lib: a config path into File.read, a command into system — neither from the
  request; the rest in spec/. No labelled denominator for Ruby.

## 2026-09-13 — calibration (MEASURED)

Parser is Ruby's own Ripper (rbast helper) — no API/LLM calls, no token spend.
Verdicts: REFUTED (tainted reaches sink) / OPEN (не знаю) / clean.

## sinatra (the framework itself, clean) — false-positive check
- 56 .rb (spec/test excluded). **0 REFUTED, 1 OPEN (shell, honest).** Zero false positives on clean code.

## railsgoat (OWASP deliberately-vulnerable Rails) — true-positive check
- 86 .rb. **2 REFUTED (both verified TRUE), 1 OPEN.**
- REFUTED (verified by reading source):
  - users_controller.rb:29 [sql] User.where("id = '#{params[:user][:id]}'") — string-interpolation SQLi.
  - password_resets_controller.rb:36 [xss] "...#{params[:email]}".html_safe — XSS via html_safe on interpolated input.
- OPEN: 1 file sink with untraced source (honest не знаю).

## Precision fix found DURING calibration (Rails hash-vs-string)
First pass flagged where(id: params[:id]) / find_by(id: params[:admin_id]) — HASH conditions that Rails
PARAMETERIZES (safe even with a tainted value). Fixed: conditional AR methods (where/order/find_by/...)
are sinks ONLY when the argument is an interpolated/concatenated STRING (template/bin), never a hash/array.
Raw-SQL methods (find_by_sql/execute) remain always-sinks. This removed 4 false positives; the real
string-interpolation SQLi stayed. Same discipline as the Go prepared-statement / php `->execute` lessons.

## Contract parity
All INTROSPECT-SEMANTICS.md §4 rules: sources (params/params[:x]/request.*/cookies), sinks
shell(system/exec/`backticks`/IO.popen) / code(eval/instance_eval) / sql(raw + interpolated-condition) /
xss(raw/html_safe) / file(File.*) / ssrf(open/Net::HTTP); string-interpolation + concat propagation,
guards (== / .include? / negated), cross-method + cross-file summaries, branch-join.

## Gate
7 fixtures + cross-file green. Fixtures r1-r6 + x1 + xfile/. Ruby (stdlib Ripper) required; zero install.
