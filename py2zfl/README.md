# py2zfl — Python-language module of the introspect (POC, 2026-09-11)

Native `ast`; zero-trust three-valued verdicts (F/T/Z -> REFUTED / OPEN / EARNED); honest OPEN
on the unresolved. Ports the PHP engine's SEMANTICS (php2zfl) to Python; shares the philosophy,
not code — per the modular "folder per language" plan.

Capabilities: single-fn taint, cross-fn SUMMARIES, guard/whitelist narrowing, receiver-aware
objects (no bare method-name collision), entry-point views (Flask routes), CROSS-FILE analysis.
Catalog: flask/django/aiohttp sources; shell/code/sql/deser/file/ssti sinks; sanitizers + shell=True.

Run:   python3 test_code2py.py           # regression gate (15 fixtures + cross-file)
       python3 py2zfl.py <file.py>      # single file
       analyze_app([paths])              # cross-file (see module)

Calibration (2026-09-11): pygoat(Django) 3 real REFUTED incl. cross-function; DSVW 9 vuln sinks
as OPEN; microblog/flask 0 false accusations. NOT yet: full aiohttp/fastapi, file-sink precision.
