# js2zfl on a blind corpus, round 2 (2026-09-27)

This is the second held-out measure of js2zfl. Round 1 (`js2zfl/blind/`) covered only `xss` and `file`. This round adds `sqli` and `cmdi`, so it also measures js2zfl's `sql` and `shell` contexts. As before, the cases were written by authors who had seen neither the analyzer nor its fixtures, and they were **committed before js2zfl was first run on them**.

## Pre-registration

| | |
|---|---|
| corpus commit (pre-registration) | **`0f38ea0ac3caaea0c00f8745a08a9e8f9ad0b735`**: `cases/`, `labels.csv`, `score.py` (the verdict rule) and `parsecheck.js` |
| analyzer measured | introspect **`b49bb74`** (`main`; `js2zfl.py` unchanged by this branch) |
| environment | `@babel/parser` 8.0.5 from `npm install` in `js2zfl/` (the only network access); node v22, Python 3.11. `js2zfl/blind2/parsecheck.js` is the authors' parse check: the plugins `jsast.js` uses, with `errorRecovery` off |
| after the run | `cases/`, `labels.csv` and `score.py` unchanged; `analysis.csv` and this report added |

```bash
git checkout bench/js-blind2-2026-09
(cd js2zfl && npm install)
python3 js2zfl/blind2/score.py                                  # every number below (~20 s)
git diff 0f38ea0 -- js2zfl/blind2/cases js2zfl/blind2/labels.csv js2zfl/blind2/score.py   # empty
node js2zfl/blind2/parsecheck.js $(find js2zfl/blind2/cases -name '*.[jt]s' -o -name '*.[mc]js' -o -name '*.[jt]sx')   # 288 parsed, 0 failed
```

**Who wrote what.**
- **Authors:** fresh sub-agents, one per category, with no context from the measuring session.
- **What they could read:** only `INTROSPECT-SEMANTICS.md` and `js2zfl/README.md`.
- **Forbidden:** the module source (`js2zfl.py`), its parser front end (`jsast.js`), the fixtures, the tests, `CALIBRATION.md`, every `blind*` folder, and git history.
- **The measuring session** wrote only `score.py` and the parse-check tooling (`parsecheck.js`).
- **The analysis** (this report and `analysis.csv`) was done after the run by a separate sub-agent, not
  blind, which read the analyzer and confirmed every cause. The measuring session re-checked a sample of the
  causes by reproduction before committing.

**Limits.** The authors are the same model family that wrote the analyzer. They report reading nothing else, which cannot be verified from outside.

**Categories produced:** `sqli` 66, `xss` 68, `file` 66 and `cmdi` 73 cases.

**One category is absent.** The author of **`code`** was stopped by a safety filter while generating and wrote nothing. The same happened in round 1 to `sqli`, `code` and `cmdi`; this round `sqli` and `cmdi` were produced. The category was skipped and the task was **not** rephrased to get around the filter. Nothing below speaks about js2zfl's `code` context.

**The corpus:**
- 273 labelled cases: sqli 33/33, xss 34/34, file 33/33 and cmdi 39/34 (vulnerable/safe).
- 15 helper modules, plus one JSON config that is not parsed.
- Express, Koa, NestJS and React (JSX/TSX) server code, in `.js`, `.ts`, `.mjs`, `.cjs`, `.jsx` and `.tsx`.

## How it is scored

This is the task's rule, fixed in `score.py` before the run. `js2zfl.analyze_app` runs over all 288 source files at once, as `introspect.py` runs it. A case's verdict is the worst record of its category's context (`sql`, `xss`, `file`, `shell`) **in that case file**, in the order REFUTED > OPEN > SILENT. Files in `js2zfl.UNPARSED` are listed separately. **There are none.**

## Results

| category | label | expect_open | n | REFUTED | OPEN | SILENT |
|---|---|---|--:|--:|--:|--:|
| sqli | vulnerable | no | 31 | 21 | 0 | **10** |
| sqli | vulnerable | yes | 2 | 0 | 2 | 0 |
| sqli | safe | no | 31 | **1** | 3 | 27 |
| sqli | safe | yes | 2 | 0 | 2 | 0 |
| xss | vulnerable | no | 30 | 17 | 10 | **3** |
| xss | vulnerable | yes | 4 | 0 | 4 | 0 |
| xss | safe | no | 33 | **3** | 14 | 16 |
| xss | safe | yes | 1 | 0 | 1 | 0 |
| file | vulnerable | no | 29 | 19 | 10 | 0 |
| file | vulnerable | yes | 4 | 0 | 3 | **1** |
| file | safe | no | 28 | **6** | 20 | 2 |
| file | safe | yes | 5 | **1** | 4 | 0 |
| cmdi | vulnerable | no | 36 | 22 | 5 | **9** |
| cmdi | vulnerable | yes | 3 | 0 | 2 | **1** |
| cmdi | safe | no | 31 | **4** | 7 | 20 |
| cmdi | safe | yes | 3 | **1** | 2 | 0 |

Decided cases only (expect_open = no):

| category | vulnerable: REFUTED / OPEN / SILENT | safe: REFUTED / OPEN / SILENT | TPR | FPR |
|---|---|---|--:|--:|
| sqli | 21 / 0 / **10** of 31 | **1** / 3 / 27 of 31 | 67.7% | 3.2% |
| xss | 17 / 10 / **3** of 30 | **3** / 14 / 16 of 33 | 56.7% | 9.1% |
| file | 19 / 10 / **0** of 29 | **6** / 20 / 2 of 28 | 65.5% | 21.4% |
| cmdi | 22 / 5 / **9** of 36 | **4** / 7 / 20 of 31 | 61.1% | 12.9% |
| all | 79 / 25 / **22** of 126 | **14** / 44 / 65 of 123 | 62.7% | 11.4% |

**Records outside the scored cells:**
- Six OPEN in helper files. Two carry a real flow of a silent case (see §1): `cmdi/lib/archive.js:12` (`project-export`) and `sqli/lib/mysql-store.js:17` (`catalog-service`). Four are OPEN on code with no request value: `sqli/lib/mysql-store.js:25` (a constant, parameterised query in a `Promise` executor), `cmdi/lib/maintenance.js:7` (a constant command) and `file/lib/userFiles.js:12` and `:16`. In all six the judged value is Z: a closure variable or a module-level name read inside a function is unknown.
- Seven REFUTED in case files under a context other than the case's category. By the rule fixed before the run, they are not counted. Four are true and three are false:

| record | true? | why |
|---|---|---|
| `cmdi/bundle-download.js:20` [xss] `send` | true | `res.status(400).send('unsupported format: ' + kind)` reflects `req.query.kind` into an HTML response. |
| `cmdi/feedback-submit.js:11` [xss] `send` | true | Reflects up to 50 characters of `req.body.message` into HTML. That is enough for a tag with an event handler. |
| `cmdi/log-head.js:9` [xss] `send` | true | Reflects `req.query.n` raw in the error message. |
| `sqli/template-from-file.js:13` [file] `readFileSync` | true | `'./queries/' + req.params.name + '.sql'`: Express decodes `%2F` in route parameters, so any readable `.sql` file can be chosen. The case's `sql` label (safe, expect_open) is about the query text, which is judged OPEN. |
| `xss/invoice-note.js:14` [shell] `render()->sink` | **false** | **Bare-name summary collision.** `ejs.render(..)` has no response receiver, so it falls through to the summary of *any* function named `render`. The only one is `QrCodeService.render` in `cmdi/qr-code.controller.ts`, which runs `execSync`. |
| `xss/signature-preview.js:14` [shell] `render()->sink` | **false** | The same collision. The case is vulnerable in `xss` (an EJS `<%-` tag) and is scored OPEN there. |
| `xss/remote-profile.ts:12` [ssrf] `fetch` | **false** | The URL is a constant `https://directory.example.org/api/profiles/` plus `encodeURIComponent(req.params.user)`. The host is fixed and `/` is encoded, so at most a same-host path change is possible (`..` is not encoded). js2zfl credits `encodeURIComponent` only for `xss` (`CTX_SANITIZERS`) and does not consider the constant prefix. |

## Method

For every case of §1 and §2 the cause was confirmed in three ways:
- A diagnostic subclass of `Engine` recorded every sink the judge walk evaluated (line, sink, context, and the taint letter F/T/Z, including the F ones the module drops as EARNED). It ran over the corpus exactly as `analyze_app` does.
- The case and the analyzer's code path were read.
- Most causes were also reproduced. A copy of the case, changed in the one construct named, was run through `analyze_app` in `/tmp`. For example, renaming the sink to `.query(` gave REFUTED, and a single anchored `.test` guard in place of the unrecognised one removed the record.

Every cause below was confirmed this way. None is a guess.

## 1. Every silence on a vulnerable case: 24 (22 decided + 2 expect_open)

A silence is a contract breach: it reads as "clean". **18 are lost at the sink, 5 in propagation and 1 at the source.** In every sink-stage case the request value *is* tainted T at the call. Replacing the call with a catalogued sink gives REFUTED.

### Sink: 18

| n | cause | cases |
|--:|---|---|
| **8** | **SQL APIs missing from the catalog.** The only SQL sinks are method calls named `query` or `execute` (`SQL_M`). Not sinks: prisma `$queryRawUnsafe` and `$executeRawUnsafe` (2), knex `whereRaw` and `knex.raw` (2), TypeORM `createQueryBuilder().where(..)`, sequelize `literal(..)`, sqlite3 `db.all`, and better-sqlite3 `db.prepare`. | `audit-log`, `notification-purge`, `price-range`, `tag-filter`, `article-query`, `geo-search`, `comment-thread`, `session-store` |
| **5** | **Only argument 0 of a shell sink is judged.** `spawn('sh'/'bash', ['-c', script])` (2) and `execFile('/bin/sh', ['-c', ..])` judge the constant shell name (F). `execSync('/bin/bash -s', {input: body})` does not judge the stdin option. `execFile('git', ['ls-remote', remote, ..])` does not judge the argv, and argument injection (`--upload-pack=`) is not modelled. `dns-tools` also calls `execFile` through a `promisify` alias (next row). | `transcode-queue`, `video-duration`, `dns-tools`, `maintenance-runner`, `remote-check` |
| **3** | **Shell calls in a form the catalog does not match.** A bare `execa(cmd, {shell: true})`: bare-call sinks are only the `SHELL_M` names, and `execa` is listed only as a member-call receiver. A `util.promisify(cp.exec)` alias called as `run(..)`. `require('child_process').exec(..)`, whose receiver base is `require`, not one of `CHILD_PROC_BASES`. | `asset-optimizer`, `disk-usage`, `remote-health` |
| **2** | **A NestJS handler's return value is not an xss sink,** even with `@Header('Content-Type', 'text/html')`. The source is recognised: the `@Query`/`@Body` parameter is T, and the cross-file service `register` returns T. | `welcome.controller`, `newsletter.controller` |

(`dns-tools` is counted once, under argument 0.)

### Propagation: 5

| n | cause | cases |
|--:|---|---|
| **2** | **A sink inside a `new Promise((resolve, reject) => ..)` executor in a cross-file helper.** `_walk` skips nested functions, so the helper's summary has no sink effect and the call is not judged in the case file. The executor, judged on its own, sees the closure variable as Z. The flow shows only as an OPEN **in the helper file** (`cmdi/lib/archive.js:12`, `sqli/lib/mysql-store.js:17`). Without the wrapper, both give REFUTED at the call in the case file. | `project-export`, `catalog-service` |
| 1 | **`Map.forEach` callback.** `fields.set(k, req.body[k])` makes the Map T (`set` is a mutator). But the `forEach` callback is judged as an independent function with its parameters F. Only `map`/`flatMap`/`filter`/`find` callbacks are tied to their receiver. A `for..of` over `fields.values()` gives REFUTED. | `profile-fields` |
| 1 | **Middleware to handler through `res.locals`.** A middleware stores the body value in `res.locals.environment`. In the handler, `res.locals.x` takes the taint of the parameter `res`, which is F. The command is judged F (EARNED) instead of Z. | `deploy-hooks` (eo) |
| 1 | **Dynamic dispatch through an operations map.** In `operations[req.body.op](path)`, the callee is a local, so no summary applies. The anonymous arrows in the object literal have no name, so they have no summary either. Their `fs` calls are judged with the parameter F. | `file_ops` (eo) |

### Source: 1

**`member-panel`:** the parameter of a `'use server'` function (`loadMember(email)`) is not a source. Every parameter is seeded F; only NestJS parameter decorators and request-shaped destructuring are sources. The sink, prisma `$queryRawUnsafe`, is also missing from `SQL_M`. Renaming only the sink gives OPEN, through the component's destructured prop (Z). Fixing both gives REFUTED.

## 2. Every false alarm: 16 (14 decided + 2 expect_open)

| n | stage | cause | cases |
|--:|---|---|---|
| **10** | guard | **Validation that is not recognised.** `_guard` knows `===`/`!==` against a literal, `.includes`/`.has`, and an anchored regex `.test` on a literal or a `const` name, one test at a time. Not recognised: a **compound `\|\|` test** (3: `typeof x !== 'string' \|\| !RE.test(x)` twice, and `!regions.includes(r) \|\| ..`); a **validator call** that is a bare function or a method other than `includes`/`has`/`test` (4: uuid `validate`, `validator.isUUID`, and the helpers `insideRoot` and `isPlainFileName`); an anchored regex held in a **static class property** (`MarkdownStore.SLUG.test`); **NestJS validation**, either a `ParseUUIDPipe` inside `@Param(..)`, of which jsast keeps only the decorator name, or class-validator DTO decorators under `ValidationPipe` (2). Replacing each with a single recognised guard removes the REFUTED. | `handle-preview`, `statement_pdf`, `region_report` (eo), `session-cleanup`, `order-link`, `static_guard`, `strict_name`, `markdown_store`, `qr-code.controller`, `audio-convert.controller` (eo) |
| **5** | sanitiser | **A neutraliser that is not credited in the context it protects.** A whitelist strip `replace(/[^a-z0-9_-]/g, '')` is credited only for `xss`, so it stays T for `shell` and `file` (2). mysql2 `conn.escape(x)` is credited only for `xss` (`CTX_SANITIZERS['escape']`). A single-quote shell escaper: js2zfl has no shell escaper, and `replace` is transparent. A JSON-in-`<script>` serialiser that escapes only `<` (and U+2028/2029): the `js_json` family needs `<`, `>` and `&` all as `\u` escapes. | `site-provision`, `scratch_write`, `keyword-scan`, `archive-list`, `hydrate-shell` |
| 1 | sink | **`res.download(file, name, {root}, cb)`.** The options are read only at argument 1, which is `sendFile`'s position. `download`'s options are argument 2, so `root` is not seen and the path is judged unconfined. With the options at argument 1 there is no record. | `report_download` |

`analysis.csv` holds the cause per case; `score.py` prints it next to each label's reason.

## 3. Counted

- **Hits:** 79 of 126 decided vulnerable cases (sqli 21/31, xss 17/30, file 19/29, cmdi 22/36). None of the 13 expect_open vulnerable cases was refuted.
- **OPEN, decided cases:** 25 of 126 vulnerable and 44 of 123 safe.
- **OPEN, expect_open cases:** 11 of 13 vulnerable and 9 of 11 safe.

## 4. Round 1 next to round 2

The corpora differ, so these numbers are shown side by side and not compared.

| | round 1 | round 2 |
|---|---|---|
| PR / corpus / analyzer | PR #4, `ac4fc49`, `e37a0c1` | this branch, `0f38ea0`, `b49bb74` |
| categories | xss, file | sqli, xss, file, cmdi |
| decided TPR / FPR, sqli | — | 67.7 / 3.2 |
| decided TPR / FPR, xss | 42.9 / 32.3 | 56.7 / 9.1 |
| decided TPR / FPR, file | 48.3 / 13.8 | 65.5 / 21.4 |
| decided TPR / FPR, xss + file | 45.6 / 23.3 | 61.0 / 14.8 |
| decided TPR / FPR, cmdi | — | 61.1 / 12.9 |
| decided TPR / FPR, all categories | 45.6 / 23.3 | 62.7 / 11.4 |
| silent on vulnerable | 18 decided + 4 expect_open | 22 decided + 2 expect_open |
| false alarms | 14 decided | 14 decided + 2 expect_open |
| not parsed | 0 | 0 |

Round 1's report is `js2zfl/blind/REPORT.md` on this branch. The round-2 "xss + file" row is 36/59 and 9/61, from the two category rows above.

## 5. Labels

Labels were not changed after the run. Rereading the 40 disagreements found none that is wrong. One is debatable:
- **`sqli/member-panel.tsx`** (vulnerable): the SQL is injectable if `loadMember` is called with an attacker-chosen `email`. In the file, it is called only by the server component, with the component's `email` prop, and it is never handed to a client component. Whether it is reachable as a server action with arbitrary arguments depends on code outside the case. This is not confirmed.

The `cmdi` author noted two argument-injection judgement calls:
- **`cmdi/remote-check`** (vulnerable): `git ls-remote` with no shell, harmful through `--upload-pack`.
  Scored SILENT (§1, only argument 0 is judged).
- **`cmdi/domain-whois`** (safe): `whois` option injection with no shell, where no command can run.
  Scored SILENT, an agreement.

## AI disclosure

The cases were written by Claude (Anthropic) sub-agents under the reading rules above. The scoring, the analysis and this report are also by Claude, with **Vitaly Reznik** as curator. This branch changes nothing outside `js2zfl/blind2/`.