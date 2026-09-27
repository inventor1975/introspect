# java2zfl — calibration

## 2026-09-27 — slice 6: soundness, then a labelled denominator (MEASURED)

**Why.** The OWASP Benchmark v1.2 run (branch `bench/owasp-java-2026-09`, report `OWASP-2026-09.md`)
found 293 vulnerable cases judged EARNED — silent — by the slices-1-5 engine. Every one came from a
place where the walk wrote F for "don't know": a summary that kept only T returns; a bodiless interface
method with an empty summary; `new C().m(..)` read as `new C()`; an uninitialised local; an unwalked
`switch`; `add()` into a container not tracked. The contract (INTROSPECT-SEMANTICS §1) says the
opposite: when unsure, OPEN. Slice 6 fixes each at its cause (list in the java2zfl.py docstring) and
pins each with a fixture (f15–f36; 19 of the 22 fail on the old engine, 11 of them by staying silent
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
- NOT measured yet: the OWASP Benchmark itself with this engine (needs a local clone; the harness on
  the bench branch reads the old engine's internals and needs adapting).

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
