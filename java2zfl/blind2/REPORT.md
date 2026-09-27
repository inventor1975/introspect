# java2zfl on a blind corpus, round 2 (2026-09-27)

Round 1 (PR #2, corpus `9c110c2`) measured java2zfl `a9695f2`. The analyzer was then fixed from that
round's analysis (slice 7, `4cb8988`), so the round-1 corpus is now training data. This round is a new
corpus that nobody had seen: not the analyzer, not its author, not the round-1 authors.

## Pre-registration

| | |
|---|---|
| corpus commit (pre-registration) | **`4f0624c7aba345c036b376c98d76a260cbe1167d`**: `cases/`, `labels.csv`, `stubs/` and `score.py` (the per-case-file verdict rule was fixed there, before the run) |
| analyzer measured | introspect **`4cb8988`** (`main`, java2zfl slice 7; `java2zfl.py` unchanged by this branch) |
| parser | javalang 0.13.0 (`pip install javalang`, the only network access) |
| after the run | `cases/`, `labels.csv` and `score.py` unchanged; `analysis.csv` and this report added |

```bash
git checkout bench/java-blind2-2026-09
pip install javalang
python3 java2zfl/blind2/score.py                          # every number below (~6 s)
git diff 4f0624c -- java2zfl/blind2/cases java2zfl/blind2/labels.csv java2zfl/blind2/score.py   # empty
javac -d /tmp/b2 -sourcepath java2zfl/blind2/stubs $(find java2zfl/blind2/cases -name '*.java')  # compiles
```

**Who wrote what.**
- **The cases:** three fresh sub-agents with no context from the measuring session. They could read only
  `INTROSPECT-SEMANTICS.md`, `java2zfl/README.md` and the stubs. Forbidden: `java2zfl.py`, the fixtures,
  the tests, `CALIBRATION.md`, `bench/`, any `blind` folder, and git history.
- **Their brief** asked for realistic, varied data paths chosen by the authors. It carried no list of paths,
  unlike round 1, whose list came from the curator's round-1 specification.
- **The measuring session** wrote the base stubs (API signatures) and took round 1's `score.py` unchanged
  except for its header. The base stubs are round 1's own 49 files; the stubs round-1 authors had added
  (jsoup, commonmark, an ESAPI codec) were left out.
- **The round-1 corpus** is not on `main`, and this branch starts from `main`, so it was not in the authors'
  tree.

**Limits.**
- The authors are the same model family that wrote the analyzer and its fixes.
- The current `java2zfl/README.md` names the slice-7 fixes in one line.
- The authors report reading nothing else. That cannot be verified from outside.

**No command-injection cases.** The `cmdi` author was stopped by a safety filter while generating and wrote
nothing. As the task says, the category was skipped and the task was **not** rephrased to get around the
filter. Nothing below speaks about the `shell` context.

**The corpus:**
- 221 labelled cases: sqli 111, xss 110.
- 51 helper files (DAOs, services, repositories, interfaces with several implementations, base classes,
  DTOs, records), analysed but not scored.
- 4 templates: two Thymeleaf, two JSP.
- The Java compiles against the stubs (Java 17).
- XSS sinks: servlet writers, Spring `String`/`ResponseEntity` bodies, `@ExceptionHandler` bodies, and
  views (Model → template).

## How it is scored (`score.py`, round 1's)

The analyzer runs as `introspect.py` runs it: `java2zfl.analyze_app` over all 272 `.java` files at once. A
case's verdict is the worst record of its category's context **in that case file**, in the order REFUTED >
OPEN > SILENT. This rule was fixed before the run. The SQL author noted that some cases keep their sink in
a helper. A record raised only in a helper is shown in §6 of the score output and named in the breakdown,
but not counted. A file javalang cannot parse is UNPARSED, which is not a miss.

## Results

### Label × verdict

| category | label | expect_open | n | REFUTED | OPEN | SILENT | UNPARSED |
|---|---|---|--:|--:|--:|--:|--:|
| sqli | vulnerable | no | 50 | 42 | 5 | **1** | 2 |
| sqli | vulnerable | yes | 6 | 0 | 4 | 2 | 0 |
| sqli | safe | no | 49 | **5** | 8 | 35 | 1 |
| sqli | safe | yes | 6 | 0 | 5 | 1 | 0 |
| xss | vulnerable | no | 42 | 27 | 10 | **5** | 0 |
| xss | vulnerable | yes | 13 | 1 | 8 | 4 | 0 |
| xss | safe | no | 45 | **6** | 8 | 31 | 0 |
| xss | safe | yes | 10 | **3** | 4 | 3 | 0 |

### Scores on the decided cases (expect_open = no, parsed)

| category | vulnerable: REFUTED / OPEN / SILENT | safe: REFUTED / OPEN / SILENT | TPR | FPR |
|---|---|---|--:|--:|
| sqli | 42 / 5 / **1** of 48 | **5** / 8 / 35 of 48 | 87.5% | 10.4% |
| xss | 27 / 10 / **5** of 42 | **6** / 8 / 31 of 45 | 64.3% | 13.3% |
| both | 69 / 15 / **6** of 90 | **11** / 16 / 66 of 93 | 76.7% | 11.8% |

**Not parsed by javalang:** 3 cases and 4 helpers. The analyzer's own `UNPARSED` list names the same 7
files that `score.py` finds.

| file | kind | construct |
|---|---|---|
| sqli `SkuLookupController` | case, vulnerable | text block |
| sqli `BulkPriceController` | case, vulnerable | a record declared inside it |
| sqli `InventoryReportController` | case, safe | switch expression |
| sqli `data/CustomerRecord` | helper | record |
| sqli `data/Vehicle` | helper | record |
| xss `support/ContactRequest` | helper | record |
| xss `support/StatusLabels` | helper | switch expression |

## 1. Every silence on a vulnerable case: 12 (6 decided + 6 expect_open)

A silence is a contract breach: it reads as "clean". **All 6 decided silences lose the taint in
propagation.**

| case | eo | stage | cause |
|---|:-:|---|---|
| sqli `PropertyListingController` | | propagation | A `@ModelAttribute` bean's getter (`getSortBy()`) returns a field, which reads **Z for any receiver**. So the service's sink is OPEN with and without taint, and its summary passes nothing to the caller. OPEN is raised in the helper (`ListingService:21`), not in the case. |
| xss `spring/AdvancedSearchController` | | propagation | The same bean-getter Z, plus the soft Spring sink (see the note below the table): `@ResponseBody` without `produces` is judged only for T and stays silent on Z. |
| xss `spring/AliasController` | | propagation | `Optional.ofNullable(..)` is not catalogued (`of` is), so the value is Z, and the soft sink stays silent on Z. |
| xss `web/RichTitleServlet` | | propagation | `unescapeHtml4` is catalogued as transparent and **keeps the escaper's "clean for xss" tag**, so `escapeHtml4` undone by `unescapeHtml4` still counts as escaped. |
| xss `web/SharedLinkServlet` | | propagation | **`byte[]` is typed as the scalar `byte`** (the array dimension is dropped), and `byte` is a clean numeric type. A Base64-decoded payload held in a `byte[]` reads F. |
| xss `web/StatusPageServlet` | | propagation | The same: `byte[] bytes = html.getBytes(..)` gives F, so `os.write(bytes)` is judged clean. Written inline, `write(html.getBytes())` **is** refuted. |
| sqli `TenantReportServlet` | ✓ | source | `req.getAttribute(..)` is catalogued as transparent. Over a clean request parameter it reads **F**, so an attribute set elsewhere (by a binder, from a header) is judged clean (EARNED) where Z was the honest answer. |
| xss `spring/WizardController` | ✓ | source | `session.getAttribute(..)` gives F in the same way: a value stored by another handler is judged clean. |
| sqli `AdminActionServlet` | ✓ | propagation | `Method.invoke(..)`: the reflective callee is unknown and the sink inside it is never attributed. Nothing is reported in any file. |
| xss `spring/SkuController` | ✓ | sink | An **`@ExceptionHandler`** is not an entry point, and its exception parameter reads F. The message carrying the path variable reaches a `text/html` body that is judged clean. |
| xss `spring/LegacyAccountController` | ✓ | sink | A view/template sink (a Model attribute printed by JSP raw EL) is not modelled. |
| xss `spring/ResultsPageController` | ✓ | sink | A view/template sink (Thymeleaf `th:utext`) is not modelled. |

**The soft sink is a design choice.** It is documented in `java2zfl.py`: "an unknown value into a
maybe-sink is not reported (measured: 78 such OPEN on java-sec-code)". Here it turns two Z values into
silence. INTROSPECT-SEMANTICS §1 says "silence is never safe". Whether that trade-off stands is the
curator's call; the report only counts it.

**"Don't know" turned into "clean" (EARNED):** 6 of the 12 silences.
- `getAttribute` reads F: 2.
- `byte[]` reads as a clean scalar: 2.
- An `@ExceptionHandler` parameter reads F: 1.
- `unescape` keeps the escaper's credit: 1.

## 2. Every false alarm: 14 (11 decided + 3 expect_open)

| n | cause | cases |
|--:|---|---|
| **6** | **Validation that is not recognised as a guard:** | |
| | the program's own validator `!isPlainWord(x)` + return | sqli `HashtagServlet` |
| | `!StringUtils.isNumeric(x)` + return | sqli `LoyaltyPointsServlet` |
| | `!StringUtils.isAlphanumeric(x)` + return | xss `web/CouponServlet` |
| | parse-to-validate: `Long.parseLong(x)` in a `try` whose `catch` returns | sqli `ReceiptServlet` |
| | a URL-scheme check chaining `startsWith` + a reset to a constant | xss `web/BackLinkServlet` |
| | a negated, parenthesised OR of `equalsIgnoreCase` + a reset | xss `web/SortOrderServlet` |
| **3** | **Propagation too coarse:** | |
| | a literal lookup table reached through an overridden accessor (`sortColumns().get(k)`) | sqli `MaintenanceListServlet` |
| | a helper that escapes only when a flag is `true` (`fragment(x, true)`); summaries are not specialised on constant arguments | xss `web/ForumSignatureServlet` |
| | a map **key** used as the `replace` search string taints the result, though only escaped values are inserted | xss `spring/VenuePageController` |
| **1** | **Source:** `@RequestParam List<Long>`, where the numeric element type of a collection is not considered | sqli `BulkArchiveController` |
| **1** | **An escaper passed as a method reference** in a stream (`.map(Encode::forHtml)`) | xss `web/FilterChipsServlet` |
| **3** | **A hand-written escaper or filter** (a `replace` chain, a character-whitelist loop) read as a transparent chain, giving **REFUTED**. These are expect_open: the author judged "I don't know" honest, and the analyzer **accuses** safe code. | xss `web/AddressLabelServlet`, `web/GuestNoteServlet`, `web/HandleNormalizerServlet` |

`analysis.csv` holds one line per case; `score.py` prints it next to each label's reason.

## 3. Counted

- **Hits:** 69 of 90 decided vulnerable cases (sqli 42/48, xss 27/42), plus 1 of 19 expect_open ones.
- **OPEN, decided cases:** 15 of 90 vulnerable and 16 of 93 safe.
- **OPEN, expect_open cases:** 12 of 19 vulnerable and 9 of 16 safe.
- **Other records:** one record in a helper file, the OPEN at `ListingService:21` from §1. No REFUTED in
  any case file outside its own category.

## 4. Round 1 next to round 2

The corpora differ (different authors, different briefs), so the rows are not a before-and-after of the
same test. No conclusion about growth is drawn.

| | round 1 | round 2 |
|---|---|---|
| corpus, analyzer | `9c110c2`, `a9695f2` | `4f0624c`, `4cb8988` |
| cases (sqli / xss / cmdi) | 106 / 110 / 0 | 111 / 110 / 0 |
| sqli TPR / FPR (decided) | 82.6% / 16.7% | 87.5% / 10.4% |
| xss TPR / FPR (decided) | 26.1% / 14.9% | 64.3% / 13.3% |
| both TPR / FPR (decided) | 54.3% / 15.7% | 76.7% / 11.8% |
| silent on vulnerable (decided + expect_open) | 32 + 4 | 6 + 6 |
| false alarms (decided + expect_open) | 14 + 0 | 11 + 3 |
| not parsed (cases + helpers) | 6 + 1 | 3 + 4 |

## 5. Labels

Labels were not changed after the run. Rereading the 26 disagreements found none that is wrong.

Two readings the author chose, noted:
- **A Spring `String` returned without `produces`** counts as HTML to a browser, the same reading as round
  1. The analyzer treats it as a maybe-sink.
- **`LoyaltyPointsServlet`:** `StringUtils.isNumeric` also accepts non-ASCII Unicode digits. Such a value
  can break the query's syntax, but it cannot change the query's structure, so "safe" stands.

## AI disclosure

The cases were written by Claude (Anthropic) sub-agents under the reading rules above. The scoring, the
analysis and this report are also by Claude, with **Vitaly Reznik** as curator. This branch changes nothing
outside `java2zfl/blind2/`.
