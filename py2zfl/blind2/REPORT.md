# py2zfl on a blind corpus, round 2 (2026-09-27)

Round 1 (`py2zfl/blind/`) gave py2zfl its first outside measure, and slice 5 of the analyzer was built on what
it showed. That corpus can no longer measure the analyzer fairly. This round is a new held-out corpus: cases
written by authors who had seen neither the analyzer nor its fixtures, **committed before py2zfl was first run
on them**. The corpus and the rule were fixed first; this report explains every disagreement.

## Pre-registration

| | |
|---|---|
| corpus commit (pre-registration) | **`195a2d91f9e1bfbfeda27ea53768cb892fe337d6`**: `cases/`, `labels.csv` and `score.py` (the verdict rule) |
| analyzer measured | introspect **`b49bb74`** (`main`; `py2zfl.py` unchanged by this branch) |
| environment | Python 3.11.15, stdlib only, no network |
| after the run | `cases/`, `labels.csv` and `score.py` unchanged; `analysis.csv` and this report added |

```bash
git checkout bench/python-blind2-2026-09
python3 py2zfl/blind2/score.py                                  # every number below (~1 s)
git diff 195a2d9 -- py2zfl/blind2/cases py2zfl/blind2/labels.csv py2zfl/blind2/score.py   # empty
python3 -c "import ast,glob; [ast.parse(open(f).read(),f) for f in glob.glob('py2zfl/blind2/cases/**/*.py',recursive=True)]"
```

**Who wrote what.**
- **Authors:** fresh sub-agents, one per category, with no context from the measuring session.
- **What they could read:** only `INTROSPECT-SEMANTICS.md` and `py2zfl/README.md`.
- **Forbidden:** `py2zfl.py`, the fixtures, the tests, `CALIBRATION.md`, `NIGHT-DIGEST.md`, every `blind*`
  folder (including round 1's `py2zfl/blind/`), and git history.
- **The measuring session** wrote only `score.py`, adapted from the earlier rounds.
- **The analysis** (this report and `analysis.csv`) was done after the run by a separate sub-agent, not blind.
  It read the analyzer and confirmed every cause. The measuring session checked a sample of causes by
  reproduction before committing.

**Limits.** The authors are the same model family that wrote the analyzer. They report reading nothing else,
which cannot be verified from outside. The `xss` author reported that one `ls` of its own output folder showed
that `score.py` exists; it reports that it did not open it.

**No `code` or `cmdi` cases.** The authors of both categories were stopped by a safety filter while generating
and wrote nothing. The categories were skipped and the task was **not** rephrased to get around the filter.
Nothing below speaks about py2zfl's `code`, `ssti` or `shell` contexts.

**The corpus:**
- 204 labelled cases: sqli 66, xss 71 and file 67, split 33/33, 36/35 and 34/33 between vulnerable and safe.
- 14 helper modules under `cases/*/lib/`.
- Mostly Flask, Django (function and class-based views) and FastAPI, plus six aiohttp files.
- All 218 files parse with `ast.parse` (Python 3.11).

## How it is scored

This is the rule fixed in `score.py` before the run. `py2zfl.analyze_app` runs over all 218 files at once, as
`introspect.py` runs it. A case's verdict is the worst record of its category's context **in that case file**,
in the order REFUTED > OPEN > SILENT. The contexts are `sql`, `xss` and `file`. Files in `py2zfl.UNPARSED` are
listed separately. **There are none.**

## Results

| category | label | expect_open | n | REFUTED | OPEN | SILENT |
|---|---|---|--:|--:|--:|--:|
| sqli | vulnerable | no | 31 | 25 | 4 | **2** |
| sqli | vulnerable | yes | 2 | 0 | 2 | 0 |
| sqli | safe | no | 29 | **1** | 10 | 18 |
| sqli | safe | yes | 4 | 0 | 4 | 0 |
| xss | vulnerable | no | 32 | 22 | 4 | **6** |
| xss | vulnerable | yes | 4 | 0 | 1 | 3 |
| xss | safe | no | 33 | **2** | 6 | 25 |
| xss | safe | yes | 2 | 0 | 2 | 0 |
| file | vulnerable | no | 31 | 20 | 10 | **1** |
| file | vulnerable | yes | 3 | 0 | 3 | 0 |
| file | safe | no | 31 | **2** | 25 | 4 |
| file | safe | yes | 2 | 0 | 2 | 0 |

Decided cases only (expect_open = no):

| category | vulnerable: REFUTED / OPEN / SILENT | safe: REFUTED / OPEN / SILENT | TPR | FPR |
|---|---|---|--:|--:|
| sqli | 25 / 4 / **2** of 31 | **1** / 10 / 18 of 29 | 80.6% | 3.4% |
| xss | 22 / 4 / **6** of 32 | **2** / 6 / 25 of 33 | 68.8% | 6.1% |
| file | 20 / 10 / **1** of 31 | **2** / 25 / 4 of 31 | 64.5% | 6.5% |
| all | 67 / 18 / **9** of 94 | **5** / 41 / 47 of 93 | 71.3% | 5.4% |

**Records outside the scored cells:**
- Helper files: no REFUTED or OPEN record.
- No REFUTED in any case file outside its own category.
- Seven OPEN records sit in case files under another context. None is scored:
  - xss `HttpResponse`: `file/catalog_pages:15`, `file/legal_pages:19`, `file/preview_cache:18` and `:23`.
  - file: `sqli/named_query_runner:13` and `:21`, and `xss/flask_maintenance_notice:19`.

**How the causes were found.** An `Engine` subclass recorded every sink the judge walk evaluated: line, sink,
context and taint letter, including the EARNED ones the module drops. It also listed the route returns the module
puts in `py2zfl.UNJUDGED`. The subclass ran over the corpus exactly as `analyze_app` does. For each case, the
cause below was then confirmed two ways:
- by reading the analyzer's code path;
- by a reproduction run through `analyze_app`: a minimal example, or a copy of the corpus with the one
  construct changed.

Those experiments stayed outside the repository.

## 1. Every silence on a vulnerable case: 12 (9 decided + 3 expect_open)

A silence is a contract breach: it reads as "clean". **3 are lost at the sink, 6 in propagation and 3 at the
source.**

Eight of the twelve are xss handlers whose returned string holds a **Z**, an unknown value. The module puts
such a return in `py2zfl.UNJUDGED` and writes no record. `score.py` therefore sees nothing, and the case scores
SILENT, not OPEN. A user of `introspect.py` sees the same silence. None of the twelve has a record of its own
context anywhere else.

### Sink: 3

| case | cause |
|---|---|
| `file/scratch_upload` | **`tempfile.NamedTemporaryFile(prefix=<header>, dir=..)`** is not a file sink: it is in neither `FILE_FN` nor `SINK_CALLS`. The FastAPI `Header()` parameter is correctly T: an `open()` of it in the same handler is REFUTED. |
| `sqli/ledger_totals` | **SQLAlchemy `conn.exec_driver_sql(f"..")`** is not a SQL sink. `SQL_METHODS` holds only `execute`, `executemany` and `executescript`. Renamed to `execute`, the case is REFUTED. |
| `xss/aiohttp_hello` | **`web.Response(text=..., content_type="text/html")`**: only `args[0]` and the keywords `query`, `sql`, `operation`, `content` and `body` are judged, not `text`. With `body=`, the case is REFUTED. |

### Propagation: 6

| case | cause |
|---|---|
| `sqli/warehouse_stock` | **`repository().search(q)`**: the receiver is a call result, so no class is known. The summary of `StockRepository.search`, where the parameter reaches `cur.execute`, is never applied. Written as `r = StockRepository(..); r.search(q)`, the case is REFUTED. |
| `xss/flask_invoice_builder` | **State on `self`.** `add_line` stores the text in `self.lines`, and `render()` reads it back. Method summaries do not model the receiver's state, so `inv.render()` is Z. The value was already Z earlier: `zip(..)` is an unknown call. |
| `xss/flask_pagination_error` | **The exception text.** The `except ValueError as exc` name is bound Z, with no link to the request value that `int()` rejected. So `f"..{exc}.."` is Z. |
| `xss/flask_redirect_notice` | **Bare `unquote`** (`from urllib.parse import unquote`). `TRANSPARENT_FN` lists only the dotted `urllib.parse.unquote`, and imports are not resolved, so the call is unknown (Z). The dotted form is REFUTED. |
| `xss/flask_referral_note` | **Bare `unquote_plus(escape(x))`** is unknown (Z). The dotted `urllib.parse.unquote_plus` is transparent and **keeps `escape`'s xss credit**. Checked: that gives EARNED, a false clean. `unquote_plus` is not in `UNESCAPERS`, which lists a non-existent `urllib.parse.unquote_plus_unescape`. |
| `xss/flask_format_dispatch` (eo) | **Dynamic dispatch.** `getattr(formatters, style)` makes `formatter(text)` an unknown call (Z). A module-attribute call such as `formatters.rich(text)` is not resolved either (checked). A direct `from lib.formatters import rich` is resolved. |

### Source: 3

| case | cause |
|---|---|
| `xss/flask_json_widget` | **`request.get_json(force=True)`** is not a source: `SOURCE_METHS` has `json`, not `get_json`. With `request.json`, the case is REFUTED at the return. |
| `xss/flask_guestbook` (eo) | **Stored XSS.** Rows from `db.execute(..).fetchall()` are Z. `render_template_string` with a `\|safe` template passes that Z on. |
| `xss/flask_session_welcome` (eo) | **Flask `session.get(..)`** is not a source, and `session` is not in `SOURCE_ATTRS`. The value is set by another route and reads Z here. |

## 2. Every false alarm: 5 (all decided)

| n | stage | cause | cases |
|--:|---|---|---|
| 1 | guard | **A guard on a loop variable.** `for value in (current, desired): if not RE.fullmatch(value): return` narrows only `value`. A loop is also joined with its zero-iteration state, so even a guard naming `current` and `desired` inside the loop leaves both T at `os.replace`. Checked; without the loop it is OPEN. | `file/label_rename` |
| 1 | guard | **`if name not in self.pages: raise`**: a class attribute is not a whitelist. Only literal collections and module-level names in `const_coll` count. Checked: even a module-level `frozenset` name does not narrow inside a summarised helper, because summaries are computed before `_file_context` fills `const_coll`. | `file/legal_pages` |
| 1 | guard | **`order_id: UUID`** is validated by FastAPI. Only `int`, `float` and `bool` annotations (and `Literal`) are treated as clean. With `int`, the case is OPEN. | `xss/fastapi_order_page` |
| 2 | propagation | **A tuple return, unpacked.** In `a, b = f(..)`, each name gets the taint of the whole tuple, so a constant beside a tainted element becomes T: the SQL clause beside `[region]`, and the status beside `filename`. Checked: a constant-only return gives no record. | `sqli/revenue_view`, `xss/flask_upload_status` |

`analysis.csv` holds the cause per case; `score.py` prints it next to each label's reason.

## 3. Counted

- **Hits:** 67 of 94 decided vulnerable cases (sqli 25/31, xss 22/32, file 20/31). None of the 9 expect_open
  vulnerable cases was refuted.
- **OPEN, decided cases:** 18 of 94 vulnerable and 41 of 93 safe.
- **OPEN, expect_open cases:** 6 of 9 vulnerable and 8 of 8 safe.

## 4. Round 1 next to round 2

These are the numbers only. The corpora differ in authors, cases and categories, so this table does not show
how much the analyzer grew.

| | round 1 | round 2 |
|---|---|---|
| PR / corpus / analyzer | PR #5, `3d83233`, `e37a0c1` | this branch, `195a2d9`, `b49bb74` |
| sqli decided TPR / FPR | 45.2 / 18.8 | 80.6 / 3.4 |
| xss decided TPR / FPR | 7.1 / 0.0 | 68.8 / 6.1 |
| code decided TPR / FPR | 59.4 / 16.7 | not measured (no cases) |
| file decided TPR / FPR | 29.0 / 3.4 | 64.5 / 6.5 |
| all decided TPR / FPR | 36.1 / 9.8 | 71.3 / 5.4 |
| silent on vulnerable | 49 decided + 6 expect_open | 9 decided + 3 expect_open |
| false alarms | 12 decided + 1 expect_open | 5 decided + 0 expect_open |
| not parsed | 0 | 0 |

Round 1's report is `py2zfl/blind/REPORT.md`.

## 5. Labels

Labels were not changed after the run. Rereading the 17 disagreements found none that is wrong. Two were
checked on Python 3.11:
- **`file/scratch_upload`:** `NamedTemporaryFile(prefix="../x", dir=d)` creates the file outside `d`.
- **`xss/flask_pagination_error`:** the `int()` `ValueError` message repeats the raw input, `<b>` included.

The `sqli` author flagged one label. **`sqli/report_plugins.py`** is labelled vulnerable (and `expect_open`) on
the assumption that the unknown backend, loaded with importlib from settings, passes request data into its
fragment. The code alone cannot settle that. It scored OPEN, which is neither a hit nor a miss.

## AI disclosure

The cases were written by Claude (Anthropic) sub-agents under the reading rules above. The scoring, the analysis
and this report are also by Claude, with **Vitaly Reznik** as curator. This branch changes nothing outside
`py2zfl/blind2/`.
