# java2zfl — Java module of the introspect (slice 1, 2026-09-12)
Java via javalang (pure-Python parser). Implements tool/INTROSPECT-SEMANTICS.md:
zero-trust F/T/Z -> REFUTED/OPEN/EARNED, honest OPEN. Slice 1: source (Servlet getParameter/
getHeader/...) -> sink (exec/executeQuery/readObject/write) taint, string-concat propagation.
Run: python3 test_java2zfl.py ; python3 java2zfl.py <File.java>
Roadmap: summaries (cross-method/file), guards, receiver-aware objects, Spring (@RequestParam/
@PathVariable/@RequestBody), PreparedStatement sanitiser, calibrate on a real Java app.
