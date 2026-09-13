# java2zfl — calibration on real Java apps (2026-09-12, MEASURED)

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
