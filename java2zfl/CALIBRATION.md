# java2zfl — calibration

## 2026-09-27 evening — slice 7: the BLIND corpus (cloud, PR #2) and what it changed (MEASURED)

**The honest number came from outside.** Three fresh cloud sub-agents that had seen neither the code nor the
fixtures wrote 216 labelled cases (sqli 106, xss 110; the cmdi author was stopped by a safety filter and
that was not worked around), committed at `9c110c2` BEFORE the analyzer ran. On `a9695f2` — the engine that
scores 644/644 on OWASP and 0 misses on Juliet — the blind result was **TPR 54.3%, FPR 15.7%, 32 silent on
vulnerable cases**. Reproduced here exactly before anything was changed. The OWASP/Juliet figures measured
fit, not strength.

What the silences were, and the fix (fixtures f41–f49; 8 of 9 fail on `a9695f2`):
- 25 — a String returned from a Spring handler (`@RestController` / `@ResponseBody` / `ResponseEntity`) IS
  the response body; only writer calls were sinks. Now: declared HTML (`produces = TEXT_HTML_VALUE`,
  `.contentType(MediaType.TEXT_HTML)`) is a sink like a writer; undeclared is judged only for a value
  known to come from the request (T -> OPEN) — an unknown value into a maybe-sink is not reported
  (measured: that alone raised 78 OPEN on java-sec-code); JSON / text/plain is not HTML.
- 7 — an escaper credited in a sub-context it does not protect. Escapers now carry a family; the HTML
  sub-context at the value (from the literals before it in the concatenation / format string and from
  what the method already wrote) decides: escapeHtml4 in a single-quoted attribute, anything but URL
  encoding at the start of href/src, anything in on*/style/bare script, a JS string that becomes
  location.href — not clean.
- 1 — a helper appending into the CALLER's StringBuilder (summaries now carry side effects on
  parameters); an unknown call handed a tainted value next to a local object makes it Z.
- 1 — `getWriter().append(a).append(x)`: append returns the writer.
- lambdas: a lambda body's stores into outer locals are kept (`forEach((k, v) -> sb.append(k))`).
False alarms fixed: compound whitelist guards (`x == null || !P.matcher(x).matches()` + return, `a && b`,
reset-to-constant in the THEN branch), lookups in literal-only tables (`Map.of(..)`, static-block puts),
URLEncoder.encode and `replaceAll("[^A-Za-z0-9 ...]", "")` strips, text/plain + nosniff, `.map(Long::parseLong)`.
Files javalang cannot parse (records, switch expressions, text blocks) are now LISTED by introspect as
NOT PARSED — not analysed, not clean — in every language module.

| engine | blind: vuln REFUTED / OPEN / silent (of 92) | safe REFUTED / OPEN (of 89) | TPR | FPR |
|---|---|---|--:|--:|
| `a9695f2` (blind) | 50 / 10 / **32** | 14 / 13 | 54.3 | 15.7 |
| slice 7 (**fitted to this corpus — not a measure**) | 73 / 17 / **2** | 7 / 18 | 79.3 | 7.9 |

The two silences left raise OPEN in another file (a base class; a `record` javalang cannot parse); the
per-file scoring counts them silent. Unchanged by slice 7: OWASP 644/644 0 FP (both modes), Juliet
918/0/0, petclinic 0/0. java-sec-code: 7 REFUTED (same), OPEN 2 -> 20 — the new ones are its
reflected-XSS endpoints (`XSS.java /reflect`, cookie and header echoes) returned from @ResponseBody
without a declared content type: real, previously invisible.
**Next measure: round 2, a new blind corpus** (TZ written 27.09) — the only way to get a number again.

## 2026-09-27 — slice 6: soundness, then a labelled denominator (MEASURED)

**Why.** The OWASP Benchmark v1.2 run (branch `bench/owasp-java-2026-09`, report `OWASP-2026-09.md`)
found 293 vulnerable cases judged EARNED — silent — by the slices-1-5 engine. Every one came from a
place where the walk wrote F for "don't know": a summary that kept only T returns; a bodiless interface
method with an empty summary; `new C().m(..)` read as `new C()`; an uninitialised local; an unwalked
`switch`; `add()` into a container not tracked. The contract (INTROSPECT-SEMANTICS §1) says the
opposite: when unsure, OPEN. Slice 6 fixes each at its cause (list in the java2zfl.py docstring) and
pins each with a fixture (f15–f40; 19 of the 22 fail on the old engine, 11 of them by staying silent
where the answer is REFUTED or OPEN).

**Labelled denominator: NIST Juliet for Java, servlet-source variants** — CWE78/89/80/83/81 whose source
is `getParameter` / `getCookies` / `getQueryString` (1 110 test cases; Juliet's other sources —
environment, console, sockets, files — are not request input and are not modelled).
`python3 java2zfl/bench/juliet.py <juliet-java/src> [--engine <file>]`. Per case: the worst verdict in
the `bad*` methods and in the `good*` methods.

| engine | hit | **miss** | bad OPEN | good clean | **false alarm** | good OPEN |
|---|---:|---:|---:|---:|---:|---:|
| slices 1-5 (d675028) | 366 | **306** | 438 | 843 | **8** | 259 |
| slice 6, first run (before any Juliet-driven change) | 903 | **111** | 96 | 876 | **0** | 123 |
| slice 6, final | 918 | **0** | 192 | 1 020 | **0** | 90 |

- The first-run 111 misses are all CWE81 (`response.sendError(code, msg)`, not a sink then).
  Three changes were made AFTER seeing Juliet, so the final row is not held-out: `sendError` became a
  SOFT sink (whether the error page is escaped depends on the container, so it is OPEN at worst — the
  111 CWE81 cases moved from miss to OPEN, not to hit); `while(true){..break;}` exits only by break
  (variant 16 goods were OPEN); a local allocated as `new C()` and never reassigned dispatches on C
  (variant 81). The held-out figure is the first run: **0 misses and 0 false alarms outside CWE81.**
- The remaining OPEN is one shape: data through a field (variant 45), a static field of another
  class (68), or a serialisation round-trip (75) — 30 cases each, bad and good alike. Fields are not
  tracked; OPEN there is the honest answer, not a gap to tune away.
- Real apps, same day: spring-petclinic **0 / 0** (unchanged); java-sec-code **7 REFUTED, 2 OPEN**,
  every REFUTED verified: the six from 2026-09-12 plus `TomcatFilterMemShell:82`
  (`if ((cmd = req.getParameter(..)) != null) exec(cmd)` — an assignment inside a condition, missed
  before). `CommandInject.codeInjectSec` is no longer accused: its `cmdFilter` is a
  `P.matcher(x).matches()` whitelist with an early return (the old engine said REFUTED here; this file
  claimed OPEN, which was stale).

**OWASP Benchmark v1.2** (sqli / cmdi / xss — the 1 210 of 2 740 tests whose sink java2zfl models),
`python3 java2zfl/bench/owasp_score.py <engine> <clone> [--project]`, the report's scoring rule
(REFUTED = reported; TPR - FPR). The script reproduces the report's old-engine row exactly.

| engine | vuln: REFUTED / OPEN / silent | safe: REFUTED / OPEN / silent | score |
|---|---|---|---:|
| slices 1-5 (report, 2026-09-27 12:18) | 12 / 114 / 518 | 5 / 110 / 451 | 1.0 |
| slice 6 as pushed in 5fbd0c3 | 558 / 86 / 0 | 0 / 166 / 400 | 86.6 |
| slice 6, final (case and project mode alike) | **644 / 0 / 0** | **0** / 34 / 532 | 100.0 |

**Read this before quoting the 100.** It is NOT a held-out result. The slice was designed from the
report's miss mechanisms, and four changes after 5fbd0c3 were made while looking at OWASP cases:
an interface's bodiless declaration no longer votes against its implementations (`ThingInterface`,
with anonymous `new I(){..}` classes registered as implementations so none is left out); exec's third
argument, the working directory, is not a command; library UPPER_CASE constants (`Locale.US`) are
clean; an untyped receiver asks the library catalogue before every user class that defines
`toString()` (project mode had turned 27 xss hits into OPEN that way). Each is a general rule with a
fixture (f37–f40), and none moved Juliet — but OWASP is now a training set for this engine, and its
score says the tool fits the Benchmark's shapes, not that it finds 100% of real injections. The
34 safe-cmdi OPEN are commands read from a resource file (`Utils.getInsecureOSCommandString`) whose
content the analysis cannot see — honest, left alone. The other 8 categories (pathtraver, ldapi,
xpathi, trustbound, crypto, hash, weakrand, securecookie) are not modelled.

## 2026-09-12 — calibration on real Java apps (MEASURED)

Parser is pure static (javalang) — no API/LLM calls, no token spend. Run:
`analyze_app(all *.java)`; verdicts REFUTED (tainted reaches sink) / OPEN (не знаю) / clean.

## spring-petclinic (clean, maintained Spring app) — false-positive check
- 50 .java files, 49 parsed, 1 parse-fail (a TEST file using modern Java syntax javalang can't parse).
- **0 REFUTED, 0 OPEN.** Zero false positives on real clean code (unchanged across every slice).

## java-sec-code (JoyChou93 — deliberately vulnerable Spring Boot) — true-positive check
- 80 .java files, 80 parsed, 0 parse-fail.
- **6 REFUTED (all verified TRUE), 3 OPEN (honest не знаю).**
- REFUTED (verified by reading source):
  - SQLI.java:67  [sql] executeQuery — raw-JDBC string-concat SQLi.
  - SQLI.java:150 [sql] prepareStatement — the "fake prepared statement": SQL concatenated THEN prepareStatement.
  - Rce.java:36   [shell] exec — Runtime.exec RCE.
  - CommandInject.java x2 [shell] new ProcessBuilder — codeInject (bare param) + codeInjectHost (getHeader),
    each via `new String[]{"sh","-c","..."+src}` -> ProcessBuilder (array taint + ctor sink + bare-param source).
- Correctly NOT accused (the discipline working):
  - SQLI.java:107 — SECURE prepared statement (`?` placeholder + setString): clean.
  - CommandInject codeInjectSec — SANITIZED via SecurityUtil.cmdFilter (unknown callee): **OPEN, not REFUTED**.
    Zero-trust: an unverifiable sanitiser yields не-знаю, never a false accusation on the secure endpoint.

## Progression (recall on the Java-AST-visible surface)
- Slices 1-5 (taint, cross-file, guards+join, receiver-aware, Spring/prepared): 2 REFUTED, 5 OPEN.
- + ProcessBuilder ctor sink, array-literal taint, bare simple handler params (implicit @RequestParam):
  **6 REFUTED, 3 OPEN.** Every added REFUTED verified true; petclinic stayed 0/0.

## Honest verdict
- **Precision: strong.** 0 FP on clean; every REFUTED verified true; sanitised/parameterised paths not accused.
- **Recall: bounded by the AST.** Catches Java-visible flows: raw JDBC, Runtime.exec, ProcessBuilder (incl. through
  a String[]), direct servlet/Spring param -> sink, cross-method + cross-file summaries. Does NOT catch:
  - MyBatis SQLi — the SQL lives in XML mappers / `${}` annotations, OUTSIDE the Java AST (a different surface).
  - Deep cross-layer flows beyond indexed summaries -> come back OPEN (не знаю), not REFUTED.
- Same zero-trust posture as php2zfl/py2zfl. The receiver-aware slice removes the bare-name-collision FPs
  (console println, Executor.execute, Logger) that a naive name-match raises on any real app.
- Constructor sinks (ProcessBuilder) fall back to the enclosing statement's line (javalang gives ClassCreator no position of its own).

## Gate
13 fixtures + cross-file green. Fixtures f1-f12 + x1 + xfile/.
