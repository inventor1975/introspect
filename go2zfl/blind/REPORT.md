# go2zfl on a blind corpus (2026-09-27)

Until now go2zfl had no outside measure. Everything rested on fixtures written by the analyzer's own author.
This is **go2zfl's first external measure**: cases written by authors who had seen neither the analyzer nor its
fixtures, **committed before go2zfl was first run on them**.

## Pre-registration

| | |
|---|---|
| corpus commit (pre-registration) | **`fce3a17481dcc74d6b241d2c8d4f745e8801280b`**: `cases/`, `labels.csv` and `score.py` (the verdict rule) |
| analyzer measured | introspect **`b49bb74`** (`main`; `go2zfl.py` and `goast.go` unchanged by this branch) |
| environment | Go 1.24.7 (Go's own `go/parser`, through the `goast` helper that go2zfl builds on first use), Python 3.11 stdlib |
| after the run | `cases/`, `labels.csv` and `score.py` unchanged; `analysis.csv` and this report added |

```bash
git checkout bench/go-blind-2026-09
python3 go2zfl/blind/score.py                                  # every number below (~2 s)
git diff fce3a17 -- go2zfl/blind/cases go2zfl/blind/labels.csv go2zfl/blind/score.py   # empty
gofmt -e -l $(find go2zfl/blind/cases -name '*.go') >/dev/null && echo 'no syntax errors'
```

**Who wrote what.**
- **Authors:** four fresh sub-agents, one per category, with no context from the measuring session.
- **What they could read:** only `INTROSPECT-SEMANTICS.md` and `go2zfl/README.md`.
- **Forbidden:** the module source (`go2zfl.py`), its parser front end (`goast.go`), the fixtures, the tests,
  `CALIBRATION.md`, every `blind*` folder (including the earlier Java, Python and JavaScript corpora), and git
  history.
- **Their brief:** the task's list of data paths, word for word.
- **The measuring session** wrote only `score.py`, adapted from the earlier rounds, and the parse-check
  tooling. The authors checked syntax with `gofmt -e`.
- **The analysis** (this report and `analysis.csv`) was done after the run by a separate sub-agent, not
  blind, which read the analyzer and confirmed every cause. The measuring session re-checked a sample of the
  causes by reproduction before committing.

**Limits.** The authors are the same model family that wrote the analyzer. They report reading nothing
else, which cannot be verified from outside.

**No command-injection cases.** The `cmdi` author was stopped by a safety filter and wrote nothing. As the
task says, the category was skipped and the task was **not** rephrased to get around the filter. Nothing
below speaks about go2zfl's `shell` context.

**The corpus:**
- 260 labelled cases: sqli 64, xss 66, file 66 and ssrf 64, about half vulnerable (134 vulnerable, 126 safe;
  20 marked expect_open).
- 5 helper files (`sqli/lib`, `xss/lib/pagekit`, `file/lib/pathutil`, `ssrf/lib/allow`, `ssrf/lib/fetch`).
- net/http, gin and gorilla/mux handlers, with database/sql, gorm and sqlx. Each case is its own small
  package. It need not compile against real dependencies, but it is valid Go.
- All 265 files parse (`go2zfl.UNPARSED` is empty).

## How it is scored

This is the task's rule, fixed in `score.py` before the run. `go2zfl.analyze_app` runs over all 265 files at
once, as `introspect.py` runs it. A case's verdict is the worst record of its category's context **in that
case file**, in the order REFUTED > OPEN > SILENT. The contexts are `sql`, `xss`, `file` and `ssrf`.
Files in `go2zfl.UNPARSED` are listed separately. **There are none.**

## Results

| category | label | expect_open | n | REFUTED | OPEN | SILENT |
|---|---|---|--:|--:|--:|--:|
| sqli | vulnerable | no | 31 | 16 | 7 | **8** |
| sqli | vulnerable | yes | 2 | 0 | 1 | 1 |
| sqli | safe | no | 28 | **3** | 9 | 16 |
| sqli | safe | yes | 3 | **1** | 2 | 0 |
| xss | vulnerable | no | 31 | 6 | 3 | **22** |
| xss | vulnerable | yes | 3 | 0 | 0 | 3 |
| xss | safe | no | 30 | 0 | 3 | 27 |
| xss | safe | yes | 2 | 0 | 1 | 1 |
| file | vulnerable | no | 31 | 16 | 8 | **7** |
| file | vulnerable | yes | 3 | 0 | 2 | 1 |
| file | safe | no | 31 | **10** | 5 | 16 |
| file | safe | yes | 1 | 0 | 1 | 0 |
| ssrf | vulnerable | no | 31 | 12 | 5 | **14** |
| ssrf | vulnerable | yes | 2 | 0 | 0 | 2 |
| ssrf | safe | no | 27 | **7** | 7 | 13 |
| ssrf | safe | yes | 4 | **1** | 1 | 2 |

Decided cases only (expect_open = no):

| category | vulnerable: REFUTED / OPEN / SILENT | safe: REFUTED / OPEN / SILENT | TPR | FPR |
|---|---|---|--:|--:|
| sqli | 16 / 7 / **8** of 31 | **3** / 9 / 16 of 28 | 51.6% | 10.7% |
| xss | 6 / 3 / **22** of 31 | 0 / 3 / 27 of 30 | 19.4% | 0.0% |
| file | 16 / 8 / **7** of 31 | **10** / 5 / 16 of 31 | 51.6% | 32.3% |
| ssrf | 12 / 5 / **14** of 31 | **7** / 7 / 13 of 27 | 38.7% | 25.9% |
| all | 50 / 23 / **51** of 124 | **20** / 24 / 72 of 116 | 40.3% | 17.2% |

**Records outside the scored cells:**
- No REFUTED or OPEN record in any of the 5 helper files.
- One REFUTED in a case file under a context other than its category: **`file/upload_rename.go:27`, `[xss]`
  `w.Write([]byte("published " + display))`**. It is **false**. No Content-Type is set, so net/http sniffs
  the body, and a body that begins with the constant `published ` is served as `text/plain; charset=utf-8`
  (checked with `http.DetectContentType`). go2zfl does not model the content type. By the rule fixed before
  the run it is not counted. The case is vulnerable as `file` and scored SILENT (§1).
- 28 OPEN records under a context other than the category. 26 are `[xss]` on `w.Write(..)` in file, sqli and
  ssrf cases. One is `[file]` on `os.ReadFile` in `xss/maintenance_notice`. One is `[file]` on sqlx `DB.Get`
  in `sqli/device_sqlx_get`, caused by a bare-name collision (§1).

**How the causes were established.** An `Engine` subclass records every sink the judge walk evaluates: line,
sink name, context and taint letter F/T/Z, including the EARNED records the module drops. It reproduces
`analyze_app`'s 159 records exactly. For each disagreement, three things were read together: those records,
the case, and the analyzer code path.

Two further checks:
- A counterfactual run added the uncatalogued calls as sinks, to see which letter they would get. It
  separates "only the sink is missing" from a second loss behind it.
- About 30 minimal reproductions of 5 to 15 lines each were run through the analyzer, in `/tmp`, outside the
  repo. Each cause below was reproduced this way.

## 1. Every silence on a vulnerable case: 58 (51 decided + 7 expect_open)

A silence is a contract breach: it reads as "clean". **50 are lost at the sink**: the call that does the harm
is not a sink go2zfl knows, or an escaper is credited where it does not protect. **8 are lost in
propagation.** None is lost at the source alone.

The catalog explains most of the sink stage:
- **sql:** method names `Query`, `Exec`, `QueryRow` and `Prepare` (with their `Context` variants), on any
  receiver.
- **file:** `os.Open`, `OpenFile`, `ReadFile`, `Create`, `Remove`, `RemoveAll`, and `ioutil.ReadFile` and
  `WriteFile`.
- **ssrf:** the package functions `http.Get`, `Post`, `Head` and `PostForm`.
- **xss:** `template.HTML`, `JS` and `URL`, and `w.Write` on a variable typed `http.ResponseWriter`.

### Sink: 50

| n | cause | cases |
|--:|---|---|
| **13** | **XSS: `fmt.Fprintf` / `fmt.Fprint(w, ..)` is not a sink.** It is the most common way these handlers write HTML. In `color_swatch` the value would still read F, because `html.EscapeString` is credited in an unquoted attribute. In `quantity_update`, `err` from `qty, err := strconv.Atoi(..)` is F, because Atoi is numeric and its taint is spread to both targets. `locale_greeting` is also a closure (see Propagation). | `account_header` (eo), `color_swatch`, `export_format_switch`, `forum_signature`, `guestbook_entry`, `locale_greeting`, `nickname_input`, `quantity_update`, `recent_searches` (eo), `report_async_render`, `tracking_snippet`, `unsubscribe_confirm`, `welcome_banner` |
| 3 | XSS: `io.WriteString(w, ..)` is not a sink. | `coupon_code_check`, `dashboard_card`, `member_profile_route` |
| 3 | XSS: gin's `c.String`, `c.Data` and `c.Writer.WriteString` are not sinks. | `article_slug_page`, `notice_fragment`, `support_ticket_form` |
| 1 | XSS: `bytes.Buffer.WriteTo(w)` is not a sink. | `tag_filter_list` |
| 2 | XSS: template engines are not sinks. The cases are tainted template *source* (`template.New(..).Parse(src)`) and `text/template` `Execute`. | `email_template_preview`, `invoice_note_render` |
| 1 | XSS: **wrong-context escaping is credited.** `html.EscapeString` clears the whole `xss` context (`CTX_SANITIZERS`), and here it is used inside an `href`, where `javascript:` survives. `w.Write` is judged, but F. | `homepage_link_card` |
| 4 | SQL: gorm `Where`, `Order` and `Raw` are not in `SQL_METHODS`. | `dynamic_field_filter`, `member_lookup_gorm`, `report_sorting`, `ticket_status_raw` |
| 2 | SQL: sqlx `Get` and `Select` are not in `SQL_METHODS`. | `device_sqlx_get`, `inventory_select` |
| 3 | File: gin `c.File` and `c.FileAttachment` are not sinks. | `attachment_download`, `export_fetch`, `gallery_image` |
| 3 | File: **`os.WriteFile`, `os.ReadDir` and `os.Rename` are missing from `PKG_SINKS`.** Only `ioutil.WriteFile` is listed. | `config_save`, `tenant_header`, `upload_rename` |
| 1 | File: `template.ParseFiles(path)` is not a sink. | `label_template` |
| 5 | SSRF: **`http.NewRequest[WithContext]` followed by `client.Do`** is not a sink, directly or inside a helper whose summary would carry it (`proxyTo`, the cross-package `fetch.Download`). | `callback_header`, `endpoint_checker`, `fetch_chain`, `image_thumb`, `invoice_pdf` |
| 6 | SSRF: **`Get` or `Post` called on an `*http.Client` value** (local, package-level or struct field) is not a sink. Only the package functions `http.Get`, `http.Post` and the like are. | `mirror_probe`, `oembed_lookup`, `remote_loader`, `service_health`, `tenant_discovery`, `webhook_store` (eo) |
| 2 | SSRF: reverse proxies are not sinks: a `Director` that sets `req.URL.Host` (also a function literal) and `httputil.NewSingleHostReverseProxy`. | `routing_director`, `upstream_switch` |
| 1 | SSRF: `net.DialTimeout` is not a sink. | `port_check` |

**Behind some sink-stage silences there is also a source gap.** Request data arrives in forms go2zfl does not
catalogue:
- a gin `ShouldBind` / `ShouldBindJSON` struct field;
- `r.Form["x"]` and `r.URL.Query()["x"]`;
- `q := r.URL.Query(); q.Get(..)`, where only the inline `X.Query().Get(..)` form is a source.

These read **Z**, not F, so once the sink is catalogued they would give OPEN, not a silence. This applies to
`support_ticket_form`, `config_save`, `oembed_lookup`, `mirror_probe`, `dashboard_card`, `tag_filter_list`
and `archive_gorm_exec`.

In `device_sqlx_get`, the bare method name `Get` resolves to the summaries of five unrelated `Get` methods in
the corpus. Their disagreement yields an **OPEN under `file`** (from `file/blob_backend.go`), not a sql record.

### Propagation: 8

| n | cause | cases |
|--:|---|---|
| **3** | **Function literals are never analysed.** `goast` encodes a `FuncLit` as `{k: "other"}`, so a closure's body, with its sources and sinks, is invisible. The three closures are a gorm `Transaction(func(tx) ..)` callback, an inline `r.HandleFunc(.., func(w, r) ..)` handler and a `go func(..) {..}(..)` goroutine. No sink of the case is judged at all. The same gap also affects `locale_greeting` and `routing_director`, listed under Sink. | `archive_gorm_exec`, `inline_route`, `batch_fetch` |
| 3 | **Second order through `Scan(&x)`.** The write through the out-parameter is not modelled. `var x string` keeps its Go zero value F, so the sink **is judged, as F (EARNED, clean)**. The author expected OPEN. | `saved_filter_run` (eo), `recipe_reviews` (eo), `attachment_history` (eo) |
| 1 | **Package-level state.** Writes to a package variable in one handler are not tracked, and the variable's initial `nil` is F. `http.Get(u)` in the worker is judged F (EARNED) instead of Z. | `prefetch_queue` (eo) |
| 1 | **Bare-name summary collision.** `blackfriday.Run(..)` resolves to the summary of `FilterAPI.Run` in `sqli/saved_filter_run.go`, which returns nothing and so reads F. `w.Write(rendered)` is then judged F. Analysed alone, the file gives Z (OPEN). | `wiki_preview` |

Four of the seven expect_open silences are not silences by omission. go2zfl judged the sink and **claimed
EARNED** where the honest answer is "I don't know" (the `Scan` and package-variable rows above).

## 2. Every false alarm: 22 (20 decided + 2 expect_open)

| n | stage | cause | cases |
|--:|---|---|---|
| **13** | guard | **Validation that is not recognised.** `_guard` knows only `x == "literal"`, `allow[x]` and `_, ok := allow[x]; ok`, plus their negation followed by `return`. The unrecognised forms are:<br>- a negated predicate call followed by `return` (7): `!re.MatchString(x)`, `!filepath.IsLocal`, `!strings.HasPrefix`, `!slices.Contains`, and a bool HMAC helper;<br>- validation signalled by an error, `if err != nil { return }` (4): `strconv.Atoi` and helpers such as `pathutil.Contained`, `resolve` and `snapshotName`;<br>- `x != A && x != B` against **named** constants (only `==` with a literal operand counts);<br>- `x == "" \|\| strings.Contains(x, "..")`. | `column_pattern`, `blob_download`, `shipping_label`, `fixture_load`, `tenant_exports`, `callback_registry`, `signed_fetch` (eo), `order_id_check`, `contract_preview`, `project_file`, `snapshot_prune`, `status_echo`, `snippet_library` |
| 3 | sanitiser | **`url.PathEscape` and `url.QueryEscape` clear only the context `url`**, which no sink uses. They are therefore never credited, not for `file` (a single escaped path element) and not for `ssrf` (values escaped into the path or query of a fixed host). | `glossary_entry`, `geocode_address`, `mirror_index` |
| 2 | sanitiser | **`filepath.Base` is in `PKG_TRANSPARENT`** and carries T. The rejection of `.`, `..` and `/` that completes it, and an extension allow-list keyed by a call expression, are not guards. | `invoice_archive`, `print_queue` |
| 1 | sanitiser | A custom quote-doubling escaper built on `strings.ReplaceAll` (transparent) is not credited. Expected OPEN, got REFUTED. | `sqlite_quoted` (eo) |
| 1 | propagation | **Block scope.** `target := ..` inside an `if` shadows the outer `target`. The environment is keyed by name, so the inner T joins into the outer variable. | `shadowed_target` |
| 1 | propagation | A branch under the **constant-false** `if allowCustomEndpoint` is walked and joined, because conditions are not evaluated. | `debug_fetch` |
| 1 | sink | `d.byDept.Query(dept)` runs on a `*sql.Stmt` kept in a **struct field** and prepared in another function. Prepared-statement awareness covers only local variables assigned from `.Prepare` in the same function, so the bound parameter is judged as SQL text. | `prepared_lookup` |

A side note, with no effect on any verdict here: `SQL_METHODS` ignores the receiver, so gin's `c.Query("..")`
is also judged as a database/sql `Query` sink. There are 45 such records. All have literal arguments, read F
and are dropped as EARNED. A gin `c.Query(x)` with a tainted argument would be a false SQL alarm.

`analysis.csv` holds the cause per case; `score.py` prints it next to each label's reason.

## 3. Counted

- **Hits:** 50 of 124 decided vulnerable cases (sqli 16/31, xss 6/31, file 16/31, ssrf 12/31). None of the
  10 expect_open vulnerable cases was refuted.
- **OPEN, decided cases:** 23 of 124 vulnerable and 24 of 116 safe.
- **OPEN, expect_open cases:** 3 of 10 vulnerable and 5 of 10 safe. 2 of the 10 expect_open safe cases were
  REFUTED (`sqlite_quoted`, `signed_fetch`).

## 4. Labels

Labels were not changed after the run. Rereading the 80 disagreements found none that is wrong.

One label reason is imprecise but the label holds. `ssrf/service_health` gives `evil.com/#` as the example
value. A single gin path segment normally cannot carry `/`, but `evil.com#` (sent as `%23`) gives the same
result: `url.Parse` reads the host of `http://evil.com#.svc.cluster.local:8080/healthz` as `evil.com`. The gin
routing detail was not run.

The `file` author flagged four labels as depending on stdlib or library behaviour:
- **`file/public_site`** (safe): relies on `http.ServeFile` rejecting `..` in `r.URL.Path`. Scored SILENT.
- **`file/glossary_entry`** (safe): relies on `url.PathEscape` encoding `/`. Scored REFUTED; it is one of
  the `url.PathEscape` false alarms in §2.
- **`file/ticket_attachment`** (safe, `expect_open` false): relies on the validator library behind gin's
  binding tags; the author noted it could be argued `expect_open`. Scored SILENT.
- **`file/media_fetch`** (vulnerable): relies on `PathValue` returning unescaped values, so an encoded
  `../` gets through. Scored OPEN.

## AI disclosure

The cases were written by Claude (Anthropic) sub-agents under the reading rules above. The scoring, the
analysis and this report are also by Claude, with **Vitaly Reznik** as curator. This branch changes nothing
outside `go2zfl/blind/`.
