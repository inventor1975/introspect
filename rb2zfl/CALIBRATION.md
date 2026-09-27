# rb2zfl — calibration

## 2026-09-27 night — the first BLIND measure (cloud, PR #8) and what it changed (MEASURED)
Fresh authors who saw neither the analyzer nor its fixtures wrote a corpus (Rails and Sinatra; 257 cases,
sqli / xss / file / code) committed before the analyzer ran. On `b49bb74`, blind (reproduced locally):
sqli 63.6, xss 38.5, file 28.6, code 48.4 found — all **45.8% found, 8.9% false alarms, 51 silent** of 118
decided vulnerable.
Causes, fixed:
- the front end: `unless` / `unless_mod` were encoded as `if` — the negation was dropped, so a guard
  written `return .. unless ALLOWED.include?(x)` left x tainted after it and, worse, refined x to clean
  INSIDE `unless ALLOWED.include?(x) .. end` (a false clean). Routes in a `Sinatra::Base` class body were
  never walked (only `def`s were kept); a ternary, `if`/`case`/`begin` used as a value, a backslash-continued
  literal and `f(*args)` splats were `other`. Literal text is now kept (unescaped: Ripper hands `\"`), so
  escapers are judged by position.
- sinks: `send_file`, `FileUtils.*`, `File.delete/rename/..`, `Dir.*`, `Pathname#read` (incl. a constant
  `DOCS = Pathname.new(..)` and `Rails.root.join`); `send/public_send/method` with a request-chosen name,
  `constantize`, `const_get`, `render inline:`, Sinatra `erb(string)`, `ERB.new`, `Tilt[..].new { src }`;
  a Sinatra route's value, `halt` and `body` (unless `content_type` is not HTML); `render html:` of an
  html_safe value (`sanitize` letting an event attribute or a scripting tag through; `simple_format(..,
  sanitize: false)`); an ERB template's `<%== %>` / `raw` of request data; `where/select/order` with a
  variable string, implicit-self `where` / `find_by_sql` in a model, `Arel.sql`, `select_all/select_one/..`,
  Sequel `DB[..]` / `db.fetch`.
- no longer judged as SQL text: the bind array of `exec_query(sql, name, [x])`, `find_by_sql(["..?..", x])`
  and an array returned by a helper (`["status = ?", x]`); a hash condition.
- escapers by position, as in Java/Go: `h`/`html_escape` at an href START (unless the value's scheme was
  checked against http/https), in an unquoted attribute, an event attribute or a script do not protect;
  `escape_javascript` protects only a quoted JS string (`<img onerror>` survives it in HTML); `json_escape`
  protects a script block; `CGI.escape` anywhere. `String#delete("^a-z0-9-")` and `gsub(/[^..]/, "")` clear
  the contexts whose dangerous characters the kept set excludes.
- guards: an ANCHORED regexp (`\A..\z` — `^`/`$` are LINE anchors in Ruby) clears the contexts its
  characters cannot express (`\A[\w./-]+\z` still lets `../` through; an identifier-only pattern makes code
  Z, not clean); `key?/has_key?`; `||` of equalities; `==` against a constant; a check inside a ternary; an
  own predicate (`allowed_material?(x)` whose last expression is the check); `start_with?(ROOT +
  File::SEPARATOR)`; `x.include?("..")` rejection only caps file at Z (an absolute path still passes); `halt`/`raise`/`next`/`break` end a branch; a fixed-prefix `send("sort_by_#{x}")` is Z.
- propagation: `a || b` carries a or b; `h.fetch(k, default)` the default; `out << a << b` every operand;
  `request.headers`, `JSON.parse(request.body.read)`; `classify`/`camelize`; a helper's parameter literally
  named `params` is request params; methods resolve by their class/module (`RuleEngine.evaluate`), a
  dynamic `send("#{kind}_widget", x)` reaches every own method matching the pattern.
Fixtures w01–w12: every one fails on `b49bb74`. Stand: 30 + cross-file.
After the fixes, on the SAME corpus (fitted, not a measure): **90.7 / 0.0 / 0 silent**; expect_open cases:
vulnerable 10 — 2 REFUTED, 8 OPEN, 0 silent; safe 17 — 0 REFUTED, 7 OPEN, 10 clean.
Apps: railsgoat 5 REFUTED / 6 OPEN (was 2 / 6) — the three new are its `params[..].constantize` unsafe
reflection (api/v1/mobile_controller x2, benefit_forms_controller); sinatra (the framework, no labels) 0
REFUTED, OPEN 17 -> 87: 58 in spec/, the rest framework internals (`send`, `const_get`, `File.*`, `halt`
on values the framework receives from its caller).
A new blind round is the only way to get a number again.

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
