# go2zfl — calibration

## 2026-09-27 night — the first BLIND measure (cloud, PR #9) and what it changed (MEASURED)
Fresh authors who saw neither the analyzer nor its fixtures wrote a corpus (net/http, gin, gorilla/mux, gorm,
sqlx; 260 cases) committed before the analyzer ran. On `b49bb74`, blind (reproduced locally): sqli 51.6,
xss 19.4, file 51.6, ssrf 38.7 found — all **40.3% found, 17.2% false alarms, 51 silent** of 124 decided
vulnerable. Until this, every claim for go2zfl rested on fixtures its author wrote.
Causes, fixed:
- function literals were not parsed (`goast` encoded them as `other`): inline handlers, gorm `Transaction`
  callbacks, `go func(..){..}(x)` and proxy `Director`s were invisible. Now walked over the variables they
  capture; called-in-place literals bind their arguments.
- sinks: `fmt.Fprint*(w, ..)`, `io.WriteString(w, ..)`, gin `c.Writer.WriteString` / `c.Data` (by its content
  type) / `c.String` (only under a preset text/html), `buf.WriteTo(w)`, a tainted template SOURCE (`Parse`),
  `text/template` `Execute` (unless every action pipes `| html`), gorm `Where/Order/Raw/Having/Joins/Select`,
  sqlx `Get/Select(&dest, q)`, `Queryx`, `NamedExec`, `os.WriteFile/ReadDir/Rename/Mkdir*`, `http.ServeFile`,
  gin `c.File/FileAttachment/SaveUploadedFile`, `template.ParseFiles`, `http.NewRequest[WithContext]`,
  `Get/Post/Head` on an `*http.Client` (local, package var or struct field, via declared struct types),
  `httputil.NewSingleHostReverseProxy`, a Director's `req.URL.Host = ..`, `net.Dial*`.
- sources: gin `ShouldBind*/Bind*(&x)` (per field: `binding:"alphanum|oneof=.."` and numeric fields are
  bounded), `r.Form["x"]`, `q := r.URL.Query(); q.Get`, `r.PathValue`, `r.Host`, `r.URL.Path` (file: Z — ServeMux
  cleans `..`, other routers may not), `json.NewDecoder(r.Body).Decode(&x)`.
- honest unknowns: `Scan(&x)` (read back from the DB) and a package var written by a handler are Z, not F.
- a declared non-HTML Content-Type (text/plain, application/json, text/csv) silences xss for that handler.
- escapers by position, as in Java: `html.EscapeString` does not protect an href START, an unquoted
  attribute, an event attribute or a script; `url.QueryEscape` protects any HTML position and ssrf after a
  fixed `scheme://host/` (or a trusted leading base); `filepath.Base` and `Clean("/"+x)` clear file.
  A hand-rolled quote-doubling `strings.ReplaceAll` makes sql Z, not F. Decoding (`QueryUnescape`) after a
  check undoes the check.
- guards: `x != A && x != B` against named constants; switch cases on constants; an ANCHORED regexp
  (`^..$`, no top-level `|`; a pattern we cannot read gives Z); `filepath.IsLocal`; `HasPrefix(p, dir+"/")`
  (not a bare `dir`: 42 vs 421) and `HasPrefix(u, "https://host/")`; `slices.Contains(list, x)`;
  own bool helpers; `strings.Contains(x, "..")` rejection (file only); `allow[u.Hostname()]` and
  `HasSuffix(host, ".zone")` check the host of u; `v, err := strconv.Atoi(x); err != nil { return }`
  validates x (and the error quotes the input); an own helper that returns an error on a condition over
  its argument makes the argument and its outputs Z (checked, not proven by us). A substring
  `strings.Contains(u, "cdn.net")` is NOT a guard.
- scope: `:=` in a block shadows; a constant-false `if` is not walked; a package is a directory (same-named
  globals of two directories do not mix); an unqualified call stays in its package; `pkg.F` of a library
  never takes a user summary (`blackfriday.Run` vs a user `Run`); methods resolve by receiver type when known;
  field assignments (`req.URL = const`) are tracked per field.
Fixtures w01–w12 (+ the cross-package pair): every one fails on `b49bb74`. Stand: 33 + cross-file + cross-package.
After the fixes, on the SAME corpus (fitted, not a measure): **87.9 / 0.0 / 0 silent**; expect_open cases:
10 of 10 vulnerable OPEN, 10 safe: 6 OPEN, 4 clean, 0 refuted.
Apps: govwa 3 REFUTED / 8 OPEN (was 2 / 10: `sqli.go:49` now REFUTED, a JSON response is not xss);
gin-examples 1 REFUTED / 2 OPEN (was 0 / 0: the websocket example executes `text/template` with
`"ws://"+c.Request.Host` — request data unescaped into HTML; a Host header is hard to set cross-site, so real
but weak); go-test-bench 23 OPEN (was 10), still 0 REFUTED — its framework dispatch is the known boundary.
A new blind round is the only way to get a number again.

## 2026-09-27 — slice 5: the java2zfl soundness lesson ported (MEASURED)
10 new fixtures (u01–u10); 9 fail on the slices-1-4 engine — 5 real flows it was SILENT on (a Z helper
return read as F, switch cases walked in sequence, `m[k] = v`, a return before a reassignment, a
callee defined after its caller), the rest undecided (OPEN) where the answer is known.
- govwa: 2 REFUTED (same), OPEN 4 -> 10. The six new are REAL vulnerable sites the old engine passed
  in silence: four `template.HTML(..)` of a term that goes through `removeScriptTag()` (its unknown
  return used to read F), `csa.go:42` via `ToHTML()`, `sqli.go:49` via `UnsafeQueryGetData(uid)`.
- gin-examples 0 / 0, go-test-bench 10 OPEN — unchanged. No labelled denominator for Go.

## 2026-09-12 — calibration (MEASURED)

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
