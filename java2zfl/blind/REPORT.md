# java2zfl on a blind corpus (2026-09-27)

The OWASP Benchmark (644/644, 0 false alarms) and NIST Juliet (0 misses) numbers for java2zfl are **not blind**:
the fixes of 27.09 (`5fbd0c3`, `88adab7`) were made by reading those suites. This is a measure that was not
fitted: cases written by authors who had seen neither the analyzer's code nor its fixtures, **committed before
the analyzer was first run on them**.

## Pre-registration

| | |
|---|---|
| corpus commit (pre-registration) | **`9c110c211545e5358caa68de9d3a0c4d358b5e5e`**: `cases/`, `labels.csv`, `stubs/`; java2zfl had not been run on any of these files at that commit |
| analyzer measured | introspect `a9695f2` (the branch base; `java2zfl.py` unchanged by this branch) |
| parser | javalang 0.13.0 (`pip install javalang`, the only network access) |
| after the run | `labels.csv` and `cases/` unchanged; `score.py`, `analysis.csv` and this report added |

```bash
git checkout bench/java-blind-2026-09
pip install javalang
python3 java2zfl/blind/score.py                    # every number below (5 s)
git diff 9c110c2 -- java2zfl/blind/cases java2zfl/blind/labels.csv   # empty: nothing changed after the run
javac -d /tmp/blind-out -sourcepath java2zfl/blind/stubs $(find java2zfl/blind/cases -name '*.java')   # the corpus compiles
```

**How blind the corpus is, stated plainly.** The session that measured this was *not* blind. Earlier the same
day it had read the pre-fix `java2zfl.py` line by line and written the OWASP analysis that preceded the fixes. So
it did not write the cases:
- **Who wrote the cases.** Three fresh sub-agents, one per category, with no context from that session.
- **What the authors could read.** Only `INTROSPECT-SEMANTICS.md`, `java2zfl/README.md` and the API stubs.
- **What they were told.** Their brief was the curator's specification (the list of data paths in the task),
  and nothing about the analyzer's weak spots.
- **What the measuring session did.** It wrote the stubs (API signatures only) and `score.py`. It read the
  current `java2zfl.py` only after commit `9c110c2`.

Limits worth knowing:
- The authors are the same model family that built the analyzer.
- `java2zfl/README.md`, which the task allows as reading, describes the 27.09 fixes in one paragraph.
- The authors report reading nothing else. That cannot be verified from outside.

**The corpus is two-thirds of what was asked.** The command-injection author (`cmdi`) was stopped by a safety
filter while generating and wrote nothing. That was not worked around. **There are no cmdi cases**, and nothing
below speaks about the `shell` context.

**The corpus as committed:**
- 216 labelled cases: sqli 106, xss 110.
- 36 helper files: DAOs, services, interfaces with 2–3 implementations, base classes. They are analysed but not
  scored.
- 106 servlet-style and 110 Spring-style cases.
- Every file compiles against the stubs with `javac` (Java 17).
- Labels were set by the meaning of the code. `expect_open=true` marks where "I don't know" is the honest answer.

## How it is scored (`score.py`)

The analyzer runs exactly as `introspect.py` runs it: `java2zfl.analyze_app` over **all 252 files at once**. A
case's verdict is the worst record of its category's context (sqli → `sql`, xss → `xss`) **in that file**, in
the order REFUTED > OPEN > SILENT, where SILENT means neither. A file javalang cannot parse is UNPARSED: that is
the parser's limit, not a miss, and it has its own line. Records raised in helper files are printed too, so no
alarm is hidden.

## Results

### Label × verdict

| category | label | expect_open | n | REFUTED | OPEN | SILENT | UNPARSED |
|---|---|---|--:|--:|--:|--:|--:|
| sqli | vulnerable | no | 48 | 38 | 6 | **2** | 2 |
| sqli | vulnerable | yes | 5 | 1 | 4 | 0 | 0 |
| sqli | safe | no | 45 | **7** | 9 | 26 | 3 |
| sqli | safe | yes | 8 | 0 | 6 | 2 | 0 |
| xss | vulnerable | no | 46 | 12 | 4 | **30** | 0 |
| xss | vulnerable | yes | 9 | 0 | 5 | 4 | 0 |
| xss | safe | no | 48 | **7** | 4 | 36 | 1 |
| xss | safe | yes | 7 | 0 | 1 | 6 | 0 |

### Scores on the decided cases (expect_open = no, parsed)

| category | vulnerable: REFUTED / OPEN / SILENT | safe: REFUTED / OPEN / SILENT | TPR | FPR | TPR−FPR |
|---|---|---|--:|--:|--:|
| sqli | 38 / 6 / **2** of 46 | **7** / 9 / 26 of 42 | 82.6% | 16.7% | 65.9 |
| xss | 12 / 4 / **30** of 46 | **7** / 4 / 36 of 47 | 26.1% | 14.9% | 11.2 |
| both | 50 / 10 / **32** of 92 | **14** / 13 / 62 of 89 | 54.3% | 15.7% | 38.6 |

For comparison, on the suites the fixes were made from the analyzer scores OWASP 644/644 with 0 false alarms,
and Juliet with 0 misses. **Blind, it finds 54% of real flows, and 16% of safe cases raise a false alarm.** SQL
holds up well. XSS does not, almost entirely because of one sink the analyzer does not model (below).

## 1. Every silence on a vulnerable case: 36 (32 decided + 4 expect_open)

A silence is a contract breach: silence reads as "clean". Each case is broken down by the stage at which the
taint is lost. **None of the 36 loses the taint at the source.**

| n | stage | cause |
|--:|---|---|
| **25** | sink | **An HTML String returned from a Spring handler is not a sink.** This covers `@ResponseBody`, `@RestController` and `ResponseEntity<String>`. java2zfl's xss sinks are writer methods only (`getWriter()/getOutputStream()` `.write/print/…`). All 50 Spring-return xss cases in the corpus are silent, vulnerable and safe alike. |
| **7** | sink | **Wrong-context escaping credited as clean.** java2zfl has one `xss` context, so any HTML/JS escaper clears it whatever the HTML sub-context. |
| 1 | sink | `resp.getWriter().append(c).append(x)`: only the first `append` is recognised. `PrintWriter.append`'s result type is not catalogued, so the chained `append(x)` has an unknown receiver and is skipped. |
| 1 | propagation | A helper appends the tainted value to the **caller's** `StringBuilder` (an out-parameter). A summary carries returns and inner sinks, not side effects on arguments, so the value reads F and the sink is judged **EARNED**. This is an unknown turned into clean, the pattern slice 6 set out to remove. |
| 2 | (reported elsewhere) | **OPEN is raised, but in a helper file, not in the case.** For `LegacyPromoServlet` the sink is in the base class (`PromoServletBase:31`, and `formatCode` has disagreeing overrides, so the result is Z). For `ProductSearchController` the sink is in `ProductSearchService:26/29`: the `@RequestBody` DTO is a record that javalang cannot parse, so its accessors are Z. Per-file scoring counts both as silent. A user of the whole-project report would see the OPEN at the helper's line. |

The seven wrong-context escapes:

| case | escaper → where it lands |
|---|---|
| `xss/account/NicknameServlet` | `escapeHtml4` (leaves `'`) → a single-quoted attribute |
| `xss/catalog/SearchResultsServlet` | `escapeHtml4` → a single-quoted JS string |
| `xss/support/TicketActionServlet` | `Encode.forHtml` → a JS string inside `onclick` (entities are decoded before the script runs) |
| `xss/catalog/ContinueShoppingServlet` | `escapeHtml4` → `href` (a `javascript:` URL) |
| `xss/account/RedirectNoticeServlet` | `Encode.forJavaScript` → `location.href` (a `javascript:` URL) |
| `xss/catalog/FilterChipServlet` | `Encode.forHtmlAttribute` → an unquoted attribute (spaces not encoded) |
| `xss/catalog/ProductWidgetServlet` | `escapeEcmaScript` (leaves `< >`) → the `<h3>` body |

The per-case list, with each label's reason and cause, is printed by `score.py` §3. The causes are in
`analysis.csv`.

## 2. Every false alarm: 14

| n | cause | cases |
|--:|---|---|
| **6** | **A whitelist inside a compound condition is not a guard.** The shape is `x == null \|\| !P.matcher(x).matches()` with a return, or `!A.contains(a) \|\| !B.contains(b)`, or a reset to a constant. `_guard` recognises a single call only. | sqli `TagCloudServlet`, `LoyaltyPointsController`, `VendorListController`; xss `LocaleBannerServlet`, `PasswordResetServlet`, `UnsubscribeServlet` |
| **4** | **A lookup in a constant static map** (`MAP.get(k)`, `getOrDefault(k, "lit")`) can only yield constants. `get`/`getOrDefault` are catalogued as transparent, so the tainted key taints the result. | sqli `InvoiceSearchController`, `StatsSummaryController`, `TenantUsageController`; xss `CurrencyServlet` |
| 1 | A numeric round trip through a stream, `.map(Long::parseLong).map(String::valueOf)`: method references are not modelled and `map` is transparent. | sqli `RoleMembersController` |
| 2 | A real neutraliser is catalogued as transparent: `URLEncoder.encode` (no HTML metacharacters survive), and `replaceAll("[^A-Za-z0-9 .,-]", "")` (strips them). | xss `DownloadPageServlet`, `SummaryFooterServlet` |
| 1 | `text/plain` + `X-Content-Type-Options: nosniff`: the content type is not modelled, and every writer is an HTML sink. | xss `HealthTextServlet` |

## 3. Counted, not listed

- **Hits:** 50 of 92 decided vulnerable cases (sqli 38/46, xss 12/46), plus 1 of 14 expect_open ones.
- **OPEN, decided cases:** 10 of 92 vulnerable and 13 of 89 safe.
- **OPEN, expect_open cases:** 9 of 14 vulnerable and 7 of 15 safe. The other expect_open cases are 4 silent
  vulnerable ones (all Spring returns, counted in §1), 8 silent safe ones, and 1 REFUTED vulnerable one.
- **XSS by sink kind:**
  - **Writer-based cases** (vulnerable, decided): 12 REFUTED, 4 OPEN and 9 silent of 25, a TPR of 48%. The 9
    silences are the 7 wrong-context escapes, the chained `append`, and `LegacyPromoServlet` (OPEN in
    its base class).
  - **Spring-return cases:** 0 of 21 flagged.

## 4. Not parsed by javalang (not misses): 6 cases + 1 helper

javalang 0.13.0 does not parse:
- **Switch expressions (`case … ->`):** sqli `CalendarController` (vulnerable), `CalendarViewController` (safe)
  and `ExportSortController` (safe); xss `LoginHintController` (safe).
- **Text blocks (`"""`):** sqli `TicketController` (vulnerable) and `TicketQueueController` (safe).
- **Records:** the helper `sqli/api/SearchRequest`, which is behind one silence in §1.

`analyze_app` skips such files without a word, so on modern Java some files are never looked at.
`introspect.py` does not list them either.

## 5. Labels

The labels were not changed after the run. Rereading the 50 disagreements found **no label that is wrong**.
Two need a note:
- **`HealthTextServlet` (safe):** it relies on `nosniff` + `text/plain`, which is right for current browsers.
- **The Spring-return cases:** a `String` from `@RestController` is served as `text/html` when the browser's
  `Accept` asks for it and no `produces` narrows it. That is the usual reading, and the one the author used.

One finding beyond the labels:
- **`sqli/AccountBalanceServlet`** (labelled for SQL only) also echoes the `ccy` parameter raw into the
  response. java2zfl REFUTES that as xss, and the finding is **true**. The author did not label it, and it is
  not scored.

## 6. What this says

- **SQL.** Blind SQL detection is good: 83% of flows found, and only 2 silences, both through helper plumbing
  (an out-parameter builder, and a record DTO). The price is a 17% false-alarm rate.
- **XSS.** Blind XSS detection is poor, and for a narrow reason: the one sink shape that neither the OWASP
  Benchmark nor Juliet contains, a Spring handler returning HTML, is not modelled at all. That fits a tool fitted
  to servlet-only suites.
- **False alarms.** These are almost all validation the analyzer cannot read: compound conditions and
  constant-map lookups. They are not flows it misjudges.

In priority order, as findings rather than fixes (fixes are decided separately):
1. **Spring handler return values as xss sinks.** They cover 25 of the 36 silences, plus the 25 safe cases that
   are silent today for the wrong reason.
2. **HTML sub-contexts for escapers:** body, quoted and unquoted attribute, JS string, URL. They cover 7
   silences.
3. **Compound guards** (6 false alarms) and **constant-map lookups** (4).
4. **Side effects on arguments in summaries.** Mutating the caller's builder is today an EARNED on an unverified
   flow.
5. **Say which files were not parsed**, rather than skipping them silently.

## AI disclosure

The cases were written by Claude (Anthropic) sub-agents under the reading rules above. The scoring, the analysis
and this report are also by Claude, with **Vitaly Reznik** as curator. This branch changes nothing outside
`java2zfl/blind/`.
