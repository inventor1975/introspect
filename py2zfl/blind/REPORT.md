# py2zfl on a blind corpus (2026-09-27)

Until now py2zfl had no outside measure. Everything rested on fixtures written by the analyzer's own author.
This is the first held-out measure: cases written by authors who had seen neither the analyzer nor its
fixtures, **committed before py2zfl was first run on them**.

## Pre-registration

| | |
|---|---|
| corpus commit (pre-registration) | **`3d832335ee8b143e17effe00b842eea4e420a179`**: `cases/`, `labels.csv` and `score.py` (the verdict rule) |
| analyzer measured | introspect **`e37a0c1`** (`main`; `py2zfl.py` unchanged by this branch), stdlib only |
| after the run | `cases/`, `labels.csv` and `score.py` unchanged; `analysis.csv` and this report added |

```bash
git checkout bench/python-blind-2026-09
python3 py2zfl/blind/score.py                                  # every number below (~1 s)
git diff 3d83233 -- py2zfl/blind/cases py2zfl/blind/labels.csv py2zfl/blind/score.py   # empty
python3 -c "import ast,sys,glob; [ast.parse(open(f).read(),f) for f in glob.glob('py2zfl/blind/cases/**/*.py',recursive=True)]"
```

**Who wrote what.**
- **Authors:** five fresh sub-agents, one per category, with no context from the measuring session.
- **What they could read:** only `INTROSPECT-SEMANTICS.md` and `py2zfl/README.md`.
- **Forbidden:** `py2zfl.py`, the fixtures, the tests, `CALIBRATION.md`, `NIGHT-DIGEST.md`, every `blind*`
  folder (including the Java corpora now on `main`), and git history.
- **Their brief:** the task's list of data paths, word for word.
- **The measuring session** wrote only `score.py`, adapted from `java2zfl/blind2/score.py`. For the `code`
  category it counts both `code` and `ssti`, as the task says.

**Limits.** The authors are the same model family that wrote the analyzer. They report reading nothing
else, which cannot be verified from outside.

**No command-injection cases.** The `cmdi` author was stopped by a safety filter while generating and wrote
nothing. As the task says, the category was skipped and the task was **not** rephrased to get around the
filter. Nothing below speaks about py2zfl's `shell` context.

**The corpus:**
- 274 labelled cases: sqli 70, xss 68, code 70 and file 66, about half vulnerable.
- 17 helper modules.
- Flask, Django (function and class-based views, DRF) and FastAPI, plus one aiohttp handler.
- All 291 files parse with `ast.parse` (Python 3.11).

## How it is scored

This is the task's rule, fixed in `score.py` before the run. `py2zfl.analyze_app` runs over all 291 files at
once, as `introspect.py` runs it. A case's verdict is the worst record of its category's context **in that
case file**, in the order REFUTED > OPEN > SILENT. The contexts are `sql`, `xss`, `code`+`ssti` and `file`.
Files in `py2zfl.UNPARSED` are listed separately. **There are none.**

## Results

| category | label | expect_open | n | REFUTED | OPEN | SILENT |
|---|---|---|--:|--:|--:|--:|
| sqli | vulnerable | no | 31 | 14 | 12 | **5** |
| sqli | vulnerable | yes | 3 | 0 | 3 | 0 |
| sqli | safe | no | 32 | **6** | 9 | 17 |
| sqli | safe | yes | 4 | 0 | 1 | 3 |
| xss | vulnerable | no | 28 | 2 | 5 | **21** |
| xss | vulnerable | yes | 5 | 0 | 2 | 3 |
| xss | safe | no | 32 | 0 | 6 | 26 |
| xss | safe | yes | 3 | 0 | 3 | 0 |
| code | vulnerable | no | 32 | 19 | 7 | **6** |
| code | vulnerable | yes | 4 | 0 | 2 | 2 |
| code | safe | no | 30 | **5** | 16 | 9 |
| code | safe | yes | 4 | 0 | 4 | 0 |
| file | vulnerable | no | 31 | 9 | 5 | **17** |
| file | vulnerable | yes | 2 | 0 | 1 | 1 |
| file | safe | no | 29 | **1** | 13 | 15 |
| file | safe | yes | 4 | **1** | 1 | 2 |

Decided cases only (expect_open = no):

| category | vulnerable: REFUTED / OPEN / SILENT | safe: REFUTED / OPEN / SILENT | TPR | FPR |
|---|---|---|--:|--:|
| sqli | 14 / 12 / **5** of 31 | **6** / 9 / 17 of 32 | 45.2% | 18.8% |
| xss | 2 / 5 / **21** of 28 | 0 / 6 / 26 of 32 | 7.1% | 0.0% |
| code | 19 / 7 / **6** of 32 | **5** / 16 / 9 of 30 | 59.4% | 16.7% |
| file | 9 / 5 / **17** of 31 | **1** / 13 / 15 of 29 | 29.0% | 3.4% |
| all | 44 / 29 / **49** of 122 | **12** / 44 / 67 of 123 | 36.1% | 9.8% |

**Records outside the scored cells:** four OPEN in helper files: `code/lib/formulas.py:15`,
`code/lib/reports.py:20`, and `file/lib/storage.py:33` and `:37`. No REFUTED in any case file outside its
own category.

## 1. Every silence on a vulnerable case: 55 (49 decided + 6 expect_open)

A silence is a contract breach: it reads as "clean". **51 are lost at the sink**: the call that does the
harm is not a sink py2zfl knows. 3 are lost at the source and 1 in propagation.

### Sink: 51

| n | cause | cases |
|--:|---|---|
| **24** | **XSS: the response itself is not a sink.** py2zfl's xss sinks are only `mark_safe`, `Markup` and `HttpResponse`. Not sinks: a view that **returns an HTML string** (12, among them `shoutbox` and `coupon_errors`, both eo), `make_response` (5, among them `export_formats`, eo), flask `Response` (2), FastAPI `HTMLResponse` (3), context passed into a `render_template_string` template that uses `\|safe`, and a jinja2 `Environment(autoescape=False)`. | `announcement`, `card_widget`, `greet_user`, `homepage_link`, `notice_board`, `pager`, `roundtrip`, `sort_header`, `tag_list`, `tooltip_attr`, `shoutbox`, `coupon_errors`, `contact_form`, `docs_viewer`, `page_builder`, `search_page`, `export_formats`, `filter_tags`, `legacy_params`, `feedback_form`, `member_page`, `preview_api`, `bio_editor`, `name_plate` |
| **18** | **File: the only file sink is `open()`.** Not sinks: `send_file` (5), `FileResponse` (FastAPI 2, aiohttp 1), `os.remove`/`os.rename`/`os.stat`/`shutil.*` (5), `pathlib` `read_bytes`/`read_text` (3), `FileStorage.save`, and `tarfile.extractall`. | every silent `file/*` case; see `score.py` §3 |
| 3 | Django `raw()` (2) and `QuerySet.extra(where=..)` are not SQL sinks. | `article_archive`, `author_totals`, `price_ceiling_listing` |
| 1 | **`execute()` with any second argument counts as parameterised** and is judged F, even though the query *text* is tainted: attacker-chosen keys become column names. An unverified clean. | `listing_filters` |
| 1 | `cur.execute(query=f"..")`: the query is passed by **keyword**, and only positional arguments are judged. | `warehouse_bins` |
| 4 | Template or code execution sinks that are not catalogued: Django `Engine.from_string`, jinja2 `env.from_string`, `sympify` (eo), and `eval` taken from a dispatch table (eo). | `agent_banner`, `email_template_editor`, `symbolic_solver`, `value_parser_modes` |

### Source: 3

**A handler's parameters are not sources.** Every function is walked with its parameters F.
- **`math_path_view`:** a Django URL parameter.
- **`pricing_rules_api`:** a FastAPI `Query`.
- **`decorated_widgets`:** a keyword argument a decorator injects.

The same gap sits **behind 13 of the sink-stage silences too**: FastAPI path, query and form parameters,
Django URL parameters, Flask route variables, and decorator-injected keyword arguments. In those cases,
fixing the sink alone would still leave the value F.

### Propagation: 1

**`formula_service`:** `engine.evaluate(..)` is called on a **module-level** instance. Receiver types are
tracked only for local variables, so the call does not resolve to `FormulaEngine.evaluate`, and the `eval`
inside it is never attributed.

## 2. Every false alarm: 13 (12 decided + 1 expect_open)

| n | stage | cause | cases |
|--:|---|---|---|
| **11** | guard | **Validation that is not recognised.** The only guard is `if x in <literal collection>:`, narrowing inside the true branch. Not recognised: membership in a **named** set or tuple (`ALLOWED_OPS`, `SORTABLE`, `ALLOWED_SORT`, `ROLES`); any negated check followed by `return`, `abort` or `raise` (`not x.isdigit()`, `not RE.fullmatch(x)`, `.. is None`, `not in`); a reset to a constant; validation by `int()` inside `try`/`except`. `abort()` and `raise Http404` are not treated as ending the branch. | `binary_operator`, `order_quantity`, `quick_sum`, `table_sorter`, `snippet_regex_guard`, `custom_field_sort`, `employee_directory`, `feed_items`, `member_roles`, `ticket_status`, `listing_membership` (eo: expected OPEN, got REFUTED) |
| 1 | sink | **`string.Template(x)`** matches the bare name `Template`, catalogued as a template (ssti) sink. `string.Template` executes nothing. | `status_notice` |
| 1 | sink | **`queue.execute(job)`** on an in-memory `JobQueue` matches `execute` by method name. The receiver is a module-level instance whose class is not tracked, so the receiver-aware skip does not apply. | `report_jobs` |

`analysis.csv` holds the cause per case; `score.py` prints it next to each label's reason.

## 3. Counted

- **Hits:** 44 of 122 decided vulnerable cases (sqli 14/31, xss 2/28, code 19/32, file 9/31). None of the 14
  expect_open vulnerable cases was refuted.
- **OPEN, decided cases:** 29 of 122 vulnerable and 44 of 123 safe.
- **OPEN, expect_open cases:** 8 of 14 vulnerable and 9 of 15 safe.

## 4. Labels

Labels were not changed after the run. Rereading the 68 disagreements found none that is wrong.

The file author noted a Python-version dependency:
- **`bundle_tar_import`** is labelled vulnerable because `extractall` has no default filter on 3.11. It is a
  silence in §1.
- **`bundle_tar_filter`** passes `filter="data"`, which needs 3.11.4 or later. It is SILENT on a safe case,
  so it is not a disagreement.

## AI disclosure

The cases were written by Claude (Anthropic) sub-agents under the reading rules above. The scoring, the
analysis and this report are also by Claude, with **Vitaly Reznik** as curator. This branch changes nothing
outside `py2zfl/blind/`.
