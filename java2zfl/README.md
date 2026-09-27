# java2zfl — Java module of the introspect
Java via javalang (pure-Python parser). Implements INTROSPECT-SEMANTICS.md: zero-trust F/T/Z ->
REFUTED/OPEN/EARNED, honest OPEN.

Covers: servlet and Spring sources -> sql / shell / xss / deser sinks (receiver-aware for generic
names); cross-method and cross-file summaries resolved by class (receiver type, `new C().m()`,
inheritance); guards; context-aware escapers; constant-condition pruning; list/map element models.
Unknown stays OPEN: a bodiless method, an unknown library call, a value through a field.

Run: `python3 test_java2zfl.py` (37 fixtures + cross-file) ; `python3 java2zfl.py <File.java>`
Measured: `CALIBRATION.md` — NIST Juliet servlet variants (1 110 cases): 0 misses, 0 false alarms;
reproduce with `python3 bench/juliet.py <juliet-java/src>`.
