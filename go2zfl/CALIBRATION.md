# go2zfl — calibration on real Go apps (2026-09-12, MEASURED)

Parser is Go's own go/ast (goast helper) — no API/LLM calls, no token spend.
Verdicts: REFUTED (tainted reaches sink) / OPEN (не знаю) / clean.

## gin-examples (gin-gonic official examples, clean idiomatic Go) — false-positive check
- 52 .go (non-test). **0 REFUTED, 0 OPEN.** Zero false positives on real idiomatic code.

## govwa (0c34/govwa — Go Vulnerable Web App, idiomatic net/http + gorilla) — true-positive check
- 20 .go. **2 REFUTED (both verified TRUE), 4 OPEN (honest не знаю).**
- REFUTED (verified by reading source):
  - sqli/function.go UnsafeQueryGetData — fmt.Sprintf(...uid...) -> DB.Query(sql): real SQLi.
  - xss/xss.go:100 template.HTML — fmt.Sprintf(js, uid,...) -> template.HTML(inlineJS): real reflected XSS
    (source's own comment: "value ... came from client request").
- Correctly NOT accused (found + fixed a real FALSE POSITIVE during calibration):
  - SafeQueryGetData / checkUserQuery — constant SQL with `?` -> db.Prepare -> stmt.QueryRow(uid/username).
    A prepared statement's Query/Exec/QueryRow pass BOUND parameters, NOT SQL. First pass flagged these
    (bare method-name match); fixed by tracking vars bound from .Prepare(..) and skipping bound-param calls
    on them. This is the Go form of the php2zfl `->execute` / Java prepareStatement receiver lesson.
- OPEN (not REFUTED): sinks reached but taint unverified — mostly struct-field flows (`p.Uid = uid` then
  used) which field-access does not yet track -> honest не-знаю, never a false accusation.

## go-test-bench (Contrast — deliberately vulnerable) — a FRAMEWORK-BOUNDARY case
- 121 .go. 0 REFUTED, 10 OPEN. NOT a go2zfl defect: its handlers are dispatched through a bespoke
  framework contract (`Handler: execHandler` struct field, called by its own harness with the user input
  as a plain `string` param). The engine BUILT THE CORRECT SUMMARY (`execHandler: sinks={1:['shell']}`) but
  the taint origin enters through the custom dispatch, invisible in std-lib terms — same class of boundary
  as Java MyBatis. On idiomatic net/http / gin (FormValue / c.Query), the flow IS caught (see govwa).

## Honest verdict
- **Precision: strong.** 0 FP on clean; every REFUTED verified true; calibration itself caught+fixed the
  prepared-statement FP; parameterised queries not accused.
- **Recall: bounded by the AST.** Catches idiomatic net/http + gin + gorilla/mux sources -> shell/sql/file/
  ssrf/xss sinks, cross-function + cross-file. Bounded by: struct-field taint (-> OPEN) and bespoke
  framework dispatch (custom handler contracts -> OPEN), both honest не-знаю, not false accusation.

## Slice-3 refinement (global constants)
Package-level const/var strings are resolved (goast dumps top-level decls; go2zfl seeds a package env).
This turned 6 `DB.Exec(DropUsersTable)`-style constant-DDL OPENs into clean on govwa (OPEN 10 -> 4)
with no new FP on gin-examples. Constant queries are genuinely clean, not не-знаю.

## Gate
9 fixtures + cross-file green. Fixtures g1-g8 + x1 + xfile/. goast built on first use (needs Go toolchain).
