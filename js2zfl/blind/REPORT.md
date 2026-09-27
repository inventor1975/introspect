# js2zfl on a blind corpus (2026-09-27)

Until now js2zfl had no outside measure. Everything rested on fixtures written by the analyzer's own author.
This is the first held-out measure: cases written by authors who had seen neither the analyzer nor its
fixtures, **committed before js2zfl was first run on them**.

## Pre-registration

| | |
|---|---|
| corpus commit (pre-registration) | **`ac4fc49a7a661be161c50270cf08358b7c7acc46`**: `cases/`, `labels.csv`, `score.py` (the verdict rule) and `parsecheck.js` |
| analyzer measured | introspect **`e37a0c1`** (`main`; `js2zfl.py` unchanged by this branch) |
| parser | `@babel/parser` from `npm install` in `js2zfl/` (the only network access) |
| after the run | `cases/`, `labels.csv` and `score.py` unchanged; `analysis.csv` and this report added |

```bash
git checkout bench/js-blind-2026-09
(cd js2zfl && npm install)
python3 js2zfl/blind/score.py                                   # every number below (~12 s)
git diff ac4fc49 -- js2zfl/blind/cases js2zfl/blind/labels.csv js2zfl/blind/score.py   # empty
node js2zfl/blind/parsecheck.js $(find js2zfl/blind/cases -name '*.[jt]s' -o -name '*.[mc]js' -o -name '*.[jt]sx')   # 145 parsed
```

**Who wrote what.**
- **Authors:** five fresh sub-agents, one per category, with no context from the measuring session.
- **What they could read:** only `INTROSPECT-SEMANTICS.md` and `js2zfl/README.md`. They could run
  `parsecheck.js` but not read it.
- **Forbidden:** `js2zfl.py`, `jsast.js`, the fixtures, the tests, `CALIBRATION.md`, every `blind*` folder
  (including the Java corpora now on `main`), and git history.
- **Their brief:** the task's list of data paths, word for word.
- **The measuring session** wrote only `score.py`, adapted from `java2zfl/blind2/score.py`, and
  `parsecheck.js`. That script is `@babel/parser` with the plugins `jsast.js` uses, with `errorRecovery`
  switched off so the authors had to write strictly valid code.

**Limits.** The authors are the same model family that wrote the analyzer. They report reading nothing
else, which cannot be verified from outside.

**Three of the five categories are absent.** The authors of **`sqli`, `code` and `cmdi`** were each stopped
by a safety filter while generating, and wrote nothing. As the task says, these categories were skipped and
the task was **not** rephrased to get around the filter. Nothing below speaks about js2zfl's `sql`, `code`
or `shell` contexts.

**The corpus:**
- 133 labelled cases: xss 68 and file 65, split 34/34 and 32/33 between vulnerable and safe.
- 12 helper modules, plus two EJS views and a JSON config that are not parsed.
- Express, Koa and two NestJS controllers, in `.js`, `.ts`, `.mjs`, `.cjs`, `.jsx` and `.tsx`.

## How it is scored

This is the task's rule, fixed in `score.py` before the run. `js2zfl.analyze_app` runs over all 145 source
files at once, as `introspect.py` runs it. A case's verdict is the worst record of its category's context
(`xss`, `file`) **in that case file**, in the order REFUTED > OPEN > SILENT. Files in `js2zfl.UNPARSED` are
listed separately. **There are none.**

## Results

| category | label | expect_open | n | REFUTED | OPEN | SILENT |
|---|---|---|--:|--:|--:|--:|
| xss | vulnerable | no | 28 | 12 | 8 | **8** |
| xss | vulnerable | yes | 6 | 1 | 3 | 2 |
| xss | safe | no | 31 | **10** | 9 | 12 |
| xss | safe | yes | 3 | 0 | 2 | 1 |
| file | vulnerable | no | 29 | 14 | 5 | **10** |
| file | vulnerable | yes | 3 | 0 | 1 | 2 |
| file | safe | no | 29 | **4** | 10 | 15 |
| file | safe | yes | 4 | 0 | 2 | 2 |

Decided cases only (expect_open = no):

| category | vulnerable: REFUTED / OPEN / SILENT | safe: REFUTED / OPEN / SILENT | TPR | FPR |
|---|---|---|--:|--:|
| xss | 12 / 8 / **8** of 28 | **10** / 9 / 12 of 31 | 42.9% | 32.3% |
| file | 14 / 5 / **10** of 29 | **4** / 10 / 15 of 29 | 48.3% | 13.8% |
| both | 26 / 13 / **18** of 57 | **14** / 19 / 27 of 60 | 45.6% | 23.3% |

**Records outside the scored cells:**
- One OPEN in a helper file, `file/lib/storage.js:9`.
- Three REFUTED in `file` case files but under the **`xss`** context (`res.sendFile` is catalogued as an
  xss sink). By the rule fixed before the run, they are not counted for `file`:
  - `preview-switch` and `public-files` are **vulnerable** and scored SILENT; they are in §1.
  - `static-pages` is **safe** and scored SILENT. To a user, introspect would show a REFUTED (xss) on safe
    code, under the wrong context.

## 1. Every silence on a vulnerable case: 22 (18 decided + 4 expect_open)

A silence is a contract breach: it reads as "clean". **19 are lost at the sink**, meaning the call is not a
recognised sink of the context, and **3 at the source**. None is lost in propagation.

| n | stage | cause | cases |
|--:|---|---|---|
| 4 | sink | **`res.sendFile` is catalogued only as an `xss` sink** (in `XSS_M`), never a `file` sink. In two cases it *is* refuted, as xss. | `preview-switch`, `public-files`, `report-controller`, `avatar-render` (eo) |
| 4 | sink | **A function imported by name** from `fs`/`fs/promises` (`readFile`, `readFileSync`, `mkdir`/`writeFile`) is called bare. File sinks are recognised only as member calls `fs.X(..)`. | `manual-reader`, `snippet-view`, `tenant-config`, `export-session` (eo) |
| 4 | sink | APIs missing from the catalog: `fsp.unlink`, `fs.copyFile`, `res.download`, koa-send `send(ctx, file, {root:'/'})` | `attachment-remove`, `backup-copy`, `invoice-download`, `asset-send` |
| 3 | sink | **Koa's `ctx.body = …`** is an assignment. Only `res.send/write/end/render` calls are xss sinks. | `echo-snippet`, `feedback-thanks`, `wiki-heading` |
| 2 | sink | **Wrong-context escaping is credited.** `escapeHtml` in an `href` (a `javascript:` URL) and in an unquoted attribute: js2zfl has one `xss` context and no HTML sub-contexts. | `profile-link`, `theme-picker` |
| 1 | sink | `res.status(400).send(err.message)`: a chained `send` whose receiver is a call, not `res`, is not recognised. (The `catch` parameter is correctly Z.) | `locale-switch` |
| 1 | sink | `res.render(view, data)` judges argument 0, the view name, not the data. | `greeting-view` (eo) |
| 2 | source | Parameters that are not sources: a NestJS `@Query()` parameter, and a parameter destructured in the handler signature (`({ query: { name } }, res)`). | `greeting-controller`, `welcome-banner` |
| 1 | source | `req.category`, set by `router.param`, is not a catalogued request property. A member of `req` inherits `req`'s F, so it reads **clean (EARNED)** instead of Z. | `category-page` (eo) |

## 2. Every false alarm: 14 (all decided)

| n | stage | cause | cases |
|--:|---|---|---|
| 6 | guard | **Validation that is not recognised.** Guards are only `===`, `includes` and `has`. Not recognised: `!Set.has(x)` followed by a reset to a constant (2); a regex `.test` check (2, one ending in `ctx.throw`, which is not known to terminate); an allow-list inside a `.filter(..)` callback; a check in route middleware that runs before the handler. | `help-topic`, `currency-selector`, `template-render`, `koa-invoice`, `bundle-select`, `ticket-status` |
| 5 | sanitiser | **A neutraliser that is not recognised:** hand-written escapers or strippers read as transparent `replace` chains (3); an escaper applied inside a `.map(..)` callback; `encodeURIComponent`, credited only for `url`, inside a double-quoted `href` with a fixed scheme. | `app-shell`, `collection-header`, `team-directory`, `activity-feed`, `share-links` |
| 1 | propagation | **Bare-name summary collision.** A local `const card = Handlebars.compile(..)`, called as `card(..)`, resolves to an unrelated, non-escaping `function card` in `xss/lib/layout.js`. | `event-card` |
| 1 | propagation | **Block scope.** A `const title = req.query.from` inside an `if` shadows the outer constant. The environment is keyed by name, so the inner T joins into the outer `title`. Reproduced on a 6-line example. | `page-title` |
| 1 | sink | `res.send({..})` with an **object** is serialised as JSON, but it is judged as HTML. | `lookup-api` |

`analysis.csv` holds the cause per case; `score.py` prints it next to each label's reason.

## 3. Counted

- **Hits:** 26 of 57 decided vulnerable cases (xss 12/28, file 14/29), plus 1 of 9 expect_open ones.
- **OPEN, decided cases:** 13 of 57 vulnerable and 19 of 60 safe.
- **OPEN, expect_open cases:** 4 of 9 vulnerable and 4 of 7 safe.

## 4. Labels

Labels were not changed after the run. Rereading the 36 disagreements found none that is wrong.

The XSS author flagged three judgement calls:
- **`forum-signature`** (vulnerable): depends on what a sanitize-html option does.
- **`ticket-status`** (safe): safe only because of route middleware.
- **`plain-greeting`** (safe): Koa serves a body that does not start with `<` as `text/plain`.

`forum-signature` and `plain-greeting` are not disagreements. `ticket-status` is listed in §2.

## AI disclosure

The cases were written by Claude (Anthropic) sub-agents under the reading rules above. The scoring, the
analysis and this report are also by Claude, with **Vitaly Reznik** as curator. This branch changes nothing
outside `js2zfl/blind/`.
