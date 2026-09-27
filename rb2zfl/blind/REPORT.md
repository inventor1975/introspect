# rb2zfl on a blind corpus (2026-09-27)

`rb2zfl/README.md` and `CALIBRATION.md` describe the module, and the fixtures that back them were written by
the analyzer's own author. This is rb2zfl's **first external measure**: cases written by authors who had seen
neither the analyzer nor its fixtures, **committed before rb2zfl was first run on them**.

## Pre-registration

| | |
|---|---|
| corpus commit (pre-registration) | **`6c20e701ab5032eadc9e47260e0cdc86086577f8`**: `cases/`, `labels.csv` and `score.py` (the verdict rule) |
| analyzer measured | introspect **`b49bb74`** (`main`; `rb2zfl.py`, `rbast.rb` and `taintjudge.py` unchanged by this branch) |
| environment | Ruby 3.3.6 with its stdlib Ripper (the parser rb2zfl uses); no network, nothing installed |
| after the run | `cases/`, `labels.csv` and `score.py` unchanged; `analysis.csv` and this report added |

```bash
git checkout bench/ruby-blind-2026-09
python3 rb2zfl/blind/score.py                                   # every number below (~20 s)
git diff 6c20e70 -- rb2zfl/blind/cases rb2zfl/blind/labels.csv rb2zfl/blind/score.py   # empty
for f in $(find rb2zfl/blind/cases -name '*.rb'); do ruby -c "$f" >/dev/null || echo "$f"; done   # prints nothing (270 files)
```

**Who wrote what.**
- **Authors:** fresh sub-agents, one per category, with no context from the measuring session.
- **What they could read:** only `INTROSPECT-SEMANTICS.md` and `rb2zfl/README.md`.
- **Forbidden:** `rb2zfl.py`, its parser front end `rbast.rb`, the fixtures, the tests, `CALIBRATION.md`,
  every `blind*` folder, and git history.
- **The measuring session** wrote only `score.py`, adapted from the earlier rounds' `score.py`, and the parse
  check (`ruby -c` on every file, the command above).
- **The analysis** (this report and `analysis.csv`) was done after the run by a separate sub-agent, not
  blind, which read the analyzer and confirmed every cause. The measuring session re-checked a sample of the
  causes by reproduction before committing.

**Limits.** The authors are the same model family that wrote the analyzer. They report reading nothing
else, which cannot be verified from outside.

**No command-injection cases.** The `cmdi` author was stopped by a safety filter partway through. The
measuring session deleted the partial, unlabelled files; they were never used. The task was **not** rephrased
to get around the filter. Nothing below speaks about rb2zfl's `shell` context.

**The corpus:**
- 257 labelled cases: sqli 69 (34 vulnerable / 35 safe), xss 60 (30/30), file 62 (31/31), code 66 (33/33).
- 13 helper files under `*/lib/`.
- Rails controllers and models, Sinatra (classic top-level routes and modular `Sinatra::Base` classes), and a
  few Sequel queries.
- All 270 files pass `ruby -c` (Ruby 3.3.6).

## How it is scored

This is the task's rule, fixed in `score.py` before the run. `rb2zfl.analyze_app` runs over all 270 files at
once, as `introspect.py` runs it. A case's verdict is the worst record of its category's context (`sql`,
`xss`, `file`, `code`) **in that case file**, in the order REFUTED > OPEN > SILENT. Files in
`rb2zfl.UNPARSED` are listed separately. **There are none.**

## Results

| category | label | expect_open | n | REFUTED | OPEN | SILENT |
|---|---|---|--:|--:|--:|--:|
| sqli | vulnerable | no | 33 | 21 | 0 | **12** |
| sqli | vulnerable | yes | 1 | 0 | 0 | 1 |
| sqli | safe | no | 32 | **5** | 1 | 26 |
| sqli | safe | yes | 3 | 0 | 2 | 1 |
| xss | vulnerable | no | 26 | 10 | 6 | **10** |
| xss | vulnerable | yes | 4 | 0 | 3 | 1 |
| xss | safe | no | 27 | **2** | 13 | 12 |
| xss | safe | yes | 3 | 0 | 2 | 1 |
| file | vulnerable | no | 28 | 8 | 5 | **15** |
| file | vulnerable | yes | 3 | 0 | 1 | 2 |
| file | safe | no | 27 | **3** | 9 | 15 |
| file | safe | yes | 4 | 0 | 1 | 3 |
| code | vulnerable | no | 31 | 15 | 2 | **14** |
| code | vulnerable | yes | 2 | 0 | 2 | 0 |
| code | safe | no | 26 | 0 | 6 | 20 |
| code | safe | yes | 7 | **2** | 3 | 2 |

Decided cases only (expect_open = no):

| category | vulnerable: REFUTED / OPEN / SILENT | safe: REFUTED / OPEN / SILENT | TPR | FPR |
|---|---|---|--:|--:|
| sqli | 21 / 0 / **12** of 33 | **5** / 1 / 26 of 32 | 63.6% | 15.6% |
| xss | 10 / 6 / **10** of 26 | **2** / 13 / 12 of 27 | 38.5% | 7.4% |
| file | 8 / 5 / **15** of 28 | **3** / 9 / 15 of 27 | 28.6% | 11.1% |
| code | 15 / 2 / **14** of 31 | 0 / 6 / 20 of 26 | 48.4% | 0.0% |
| all | 54 / 13 / **51** of 118 | **10** / 29 / 73 of 112 | 45.8% | 8.9% |

**Records outside the scored cells:**
- Four OPEN in helper files, each the helper's own sink walked with its parameters F. The Z comes from:
  - `code/lib/discount_rule.rb:12` (eval): the attribute reader `template` is an unknown identifier.
  - `code/lib/rule_engine.rb:7` (instance_eval): the regex literal argument of `gsub(/\s+/, " ")` is encoded
    `other`, so the result is Z even for an F input (reproduced).
  - `file/lib/report_template.rb:7` (File.read): the constant `TEMPLATE_DIR` is an unknown identifier.
  - `file/lib/report_template.rb:11` (`body_for()->sink`): the attribute reader `name` is an unknown identifier.
- **No REFUTED in any case file outside its own category.** The only cross-context record in a scored
  disagreement is an xss OPEN (`html_safe`, Z) in `code/template_preview_controller`.

## Method

A subclass of `Engine` recorded every sink the judge walk evaluated (line, sink name, context and the taint
letter F/T/Z, including the EARNED ones the module drops), over the whole corpus, exactly as `analyze_app` runs
it. For each disagreement we checked whether any sink of the case's context was judged and with what letter,
read the case and the code path, and in most cases ran a minimal variant through the analyzer. The variants
were throwaway files outside the repo. `analysis.csv` notes "(repro)" where a cause rests on such a run.

- **Silences:** in 51 of the 55, no sink of the case's context was judged at all. In the other 4 (all xss), an
  `html_safe` was judged **F**.
- **False alarms:** in all 12, the sink was judged **T**.

## 1. Every silence on a vulnerable case: 55 (51 decided + 4 expect_open)

A silence is a contract breach: it reads as "clean". **50 are lost at the sink**: the call that does the harm
is not a sink rb2zfl judges, or an escaper is credited in a context it does not protect. **5 are filed as
propagation.** Three of those are lost in the **front end** (`rbast.rb`), which never hands the code to the
engine. The stage scheme has no separate column for this. The source catalogue loses no case on its own.

### Sink: 50

| n | cause | cases |
|--:|---|---|
| **16** | **File: the only file sinks are `File`/`IO` `.open/.read/.write/.new/.readlines/.binread`.** Not sinks: `send_file` (11), `FileUtils.cp/rm_f/rm_rf` (3), `File.delete` (1) and `Pathname#read` (1). With the call replaced by `File.read`, 12 are REFUTED and 4 are OPEN. The 4 OPEN come from an instance variable set in a `before_action`, a `case` used as an expression (encoded `other`), and `File.expand_path` (twice, unmodelled). | `attachments_controller`, `backups_controller`, `downloads_app`, `exports_controller`, `folder_listing_controller`, `media_stream`, `raw_downloads_controller`, `sheet_downloads`, `thumbnails`, `crash_reports_controller` (eo), `private_files_controller` (eo); `copy_assets_controller`, `user_avatars_controller`, `workspace_cleanup`; `exports_archive`; `docs_preview` |
| **13** | **Code: only `eval`, `instance_eval`, `class_eval` and `module_eval` are code sinks.** Not sinks: reflective dispatch `send`/`public_send`/`method(..).call` (6); constant lookup plus instantiation `constantize`/`safe_constantize`/`const_get` (3); template compilation from request text: `render inline:`, Sinatra `erb(string)`, `ERB.new(..).result`, `Tilt[..].new` (4). | `bulk_actions_controller`, `chained_ops_controller`, `command_alias_app`, `method_object_app`, `rpc_endpoint`, `subscription_transitions_controller`; `importers_controller`, `notification_kinds_controller`, `plugin_dispatch_app`; `inline_render_controller`, `sinatra_page_render`, `template_preview_controller`, `tilt_layout_app` |
| **7** | **XSS: the response itself is not a sink.** The only xss sinks are `raw(..)` and `.html_safe`. Not sinks: `render html:` (with `helpers.sanitize` or `simple_format(.., sanitize: false)`); `render inline:` with an ERB template, whose `<%= raw .. %>` is template text the analyzer does not parse; Sinatra `erb "<inline template>"`; a Sinatra route that returns an HTML string or sends it with `halt`/`body`. In `announcements_controller`, `sanitize` is also credited as an xss escaper whatever its allow-list (`raw(cleaned)` is judged F, reproduced). | `announcements_controller`, `listing_descriptions_controller`, `notes_preview_controller`, `guestbook_app`, `pages_app`, `search_app`, `widget_app` |
| **4** | **SQL: `where`/`select` with a variable argument.** The `SQL_COND` rule judges only an **inline** interpolated or concatenated first argument. `Model.where(fragment)`, where `fragment` holds the interpolated string, is never judged, although the variable is T: `find_by_sql(fragment)` is REFUTED (reproduced; for `vendor_ledger` the cross-file summary of `ReportQueries.status_fragment` carries T). | `document_archive`, `media_gallery`, `vendor_ledger`, `warehouse_stock` |
| 3 | SQL: `connection.select_all(sql)` is not in `SQL_RAW` (`find_by_sql`, `execute`, `exec_query`). With `find_by_sql`, 2 are REFUTED. The third is OPEN: in `sales_dashboard` the backslash-continued literal (`string_concat`) is encoded `other`, so it reads Z. | `reports_export`, `payroll_query`, `sales_dashboard` |
| 2 | SQL: **implicit-self** `where(..)`/`find_by_sql(..)` inside a model class method. SQL sinks are matched only on a member call (`X.where`); a bare call is not. `.order(Arel.sql(params[:sort]))` has a call, not a template, as its argument, so it is not judged either. | `transaction_ledger`, `vendor_catalog` |
| 2 | SQL: Sequel is not catalogued (`DB["..#{x}.."]`, `db.fetch(..)`). | `geo_lookup`, `metrics_endpoint` |
| 2 | **Wrong-context escaping is credited.** `html_escape` in an `href` (a `javascript:` URL passes) and `ERB::Util.h` in an **unquoted** attribute. Both are in `CTX_SANITIZERS` for the single `xss` context, so the `html_safe` is judged F. | `continue_links_controller`, `report_filters_controller` |
| 1 | SQL, eo: `@severity` is set in a `before_action`, so in the action it reads Z, which is honest. But the `where` rule reports **only T** and drops Z, so there is no record. With `find_by_sql` it is OPEN, the expected answer (reproduced). | `incident_timeline` (eo) |

### Propagation: 5

| n | cause | cases |
|--:|---|---|
| **2** | **Front end: routes in a `Sinatra::Base` class are never walked.** `rbast.rb` handles a `class`/`module` body with `collect_defs`, which keeps only `def`/`defs`. A route block `get "/x" do .. end` inside the class is dropped. Nothing is judged; with the class wrapper removed, both are REFUTED (reproduced). | `device_registry`, `log_viewer` |
| 1 | **Front end: the ternary is not encoded.** In `rule.present? ? eval(rule) : false`, Ripper's `ifop` becomes `other`, so the `eval` is never visited. Separately, `request.headers[..]` is not a source (`headers` is not in `REQ_SOURCE_MEMBERS`), so it reads Z: written as `if`/`else`, the case is OPEN, not REFUTED (reproduced). | `rollout_header_controller` |
| 1 | **Chained append.** In `out << '<p>' << line << '</p>'`, the `<<` effect folds into `out` only when its left operand is an identifier, so only `'<p>'` reaches `out`; `html_safe` is judged F. With the appends unchained, the case is OPEN, because `Array(..)` and `squish` are unmodelled (Z); with `params[..].each` and a bare `line` it is REFUTED (reproduced). | `weekly_report_controller` |
| 1 | **Dynamic dispatch.** `send("#{kind}_widget", params[:value])` is not resolved to `note_widget`. That method is judged on its own with its parameter F, so its `html_safe` is F. A direct `note_widget(params[:value])` is REFUTED through its summary (reproduced). | `dashboard_widgets_controller` (eo) |

**Behind other silences too.**
- The `Sinatra::Base` gap sits behind 6 of the sink-stage silences: `metrics_endpoint`, `guestbook_app`,
  `widget_app`, `command_alias_app`, `rpc_endpoint` and `tilt_layout_app`. There, fixing the sink alone would
  change nothing.
- All 13 case files with a `Sinatra::Base` class are SILENT. That includes 5 safe ones (`job_control_app`,
  `course_materials`, `forum_threads`, `feedback_board_app`, `shoutbox_app`), which count as agreements but
  were never analysed.
- In 8 of the 55, fixing the stated cause alone would give OPEN, not REFUTED, because an unmodelled
  expression reads Z. These are `sales_dashboard`, `media_stream`, `thumbnails`, `rollout_header_controller`,
  `weekly_report_controller`, and the eo cases `crash_reports_controller`, `private_files_controller` and
  `incident_timeline`, for which OPEN is the expected answer.

## 2. Every false alarm: 12 (10 decided + 2 expect_open)

| n | stage | cause | cases |
|--:|---|---|---|
| **8** | guard | **Validation that is not recognised.** `_guard` knows only `x == lit` / `x != lit`, `coll.include?/member?/cover?(x)` and their negation, and the only statement that ends a branch is `return`. Not recognised: a regex check `RE.match?(x)` or `x =~ /\A..\z/` (4); `Hash#key?` (1); a reset to a constant, `x = "c" unless ok` (1; the fall-through branch is never refined, and `if !..` gives T too, reproduced); an `\|\|` of equalities (1; a single `==` is credited, reproduced); and `halt` is not a terminator (2 of the regex cases). **In 7 of the 8 the check is written with `unless`, and `rbast.rb` encodes `unless`/`unless_mod` exactly like `if`, dropping the negation.** For `region_selector` that is the only cause. `return head(..) unless VALID_REGIONS.include?(region)` is the documented guard, but it is read as `if include?(..) then return`, so the fall-through keeps T. The same guard written `if !VALID_REGIONS.include?(region)` is judged F (reproduced). | `region_selector`, `wiki_pages_controller`, `label_printer`, `attribute_readers_controller` (eo), `anchored_regex_calc` (eo), `export_formats_controller`, `permission_matrix`, `locale_switch_controller` |
| 3 | sink | **Bind parameters are judged as SQL text.** The `SQL_RAW` rule judges the join of **all** arguments. The bind array of `exec_query(sql, name, [x])` (2) and the array-bind form `find_by_sql(["..?..", x])` (1) make it T, although the SQL text is constant. | `contact_list`, `price_history`, `order_status` |
| 1 | sanitiser | `String#delete("^a-z0-9-")` removes every character outside the set, but `delete` is in `RECV_TRANSPARENT`: it carries the receiver's taint. | `blog_posts_controller` |

**The dropped `unless` also cuts the other way.** Inside `unless ALLOWED.include?(x) .. end`, which is the
branch where the check failed, `x` is refined to F. A `find_by_sql("..#{x}..")` there is judged F (EARNED), a
false clean (reproduced on a 6-line example). No scored disagreement shows it. 42 case files use `unless`; we
did not check whether any verdict that agrees with its label depends on it (not confirmed either way).

`analysis.csv` holds the cause per case; `score.py` prints it next to each label's reason.

## 3. Counted

- **Hits:** 54 of 118 decided vulnerable cases (sqli 21/33, xss 10/26, file 8/28, code 15/31). None of the 10
  expect_open vulnerable cases was refuted.
- **OPEN, decided cases:** 13 of 118 vulnerable and 29 of 112 safe.
- **OPEN, expect_open cases:** 6 of 10 vulnerable and 8 of 17 safe.
- **False alarms:** 10 of 112 decided safe cases, plus 2 of 17 expect_open safe cases, both `code`.

## 4. Labels

Labels were not changed after the run. Rereading the 67 disagreements found none that is wrong. Two
`code` labels are debatable. Both are unsafe reflection, but the case does not show code execution:
- **`notification_kinds_controller`** (vulnerable): `safe_constantize` plus `klass.new(params[:payload])`.
  Harm needs a class whose constructor, or whose `deliver_later`, acts on the string.
- **`subscription_transitions_controller`** (vulnerable): `@subscription.send(event)` passes **no
  arguments**. It reaches any zero-argument method, private ones included, but not `eval` or `system` with
  an attacker string.

Two authors flagged labels:
- **`xss/feedback_board_app`** (safe): holds only if Tilt renders with Erubi, which makes
  `escape_html: true` take effect; with plain ERB the option is ignored. Scored SILENT (it is one of the
  `Sinatra::Base` files that are never analysed).
- **`code/multiline_regex_calc`** (vulnerable, `expect_open` false: `^`/`$` match per line in Ruby) and
  **`code/anchored_regex_calc`** (safe, `expect_open` true: depends on regex reasoning). Scored REFUTED
  and REFUTED; the second is one of the expect_open false alarms in §2.

## AI disclosure

The cases were written by Claude (Anthropic) sub-agents under the reading rules above. The scoring, the
analysis and this report are also by Claude, with **Vitaly Reznik** as curator. This branch changes nothing
outside `rb2zfl/blind/`.
