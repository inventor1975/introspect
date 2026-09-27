# py2zfl — Python-language module of the introspect (POC, 2026-09-11)

Native `ast`; zero-trust three-valued verdicts (F/T/Z -> REFUTED / OPEN / EARNED); honest OPEN
on the unresolved. Ports the PHP engine's SEMANTICS (php2zfl) to Python; shares the philosophy,
not code — per the modular "folder per language" plan.

Capabilities: single-fn taint, cross-fn SUMMARIES, guard/whitelist narrowing, receiver-aware
objects (no bare method-name collision), entry-point views (Flask routes), CROSS-FILE analysis.
Catalog: flask/django/aiohttp sources; shell/code/sql/deser/file/ssti sinks; sanitizers + shell=True.

Run:   python3 test_py2zfl.py            # regression gate (31 fixtures + cross-file)
       python3 py2zfl.py <file.py>      # single file
       analyze_app([paths])              # cross-file (see module)

Calibration (2026-09-11): pygoat(Django) 3 real REFUTED incl. cross-function; DSVW 9 vuln sinks
as OPEN; microblog/flask 0 false accusations. NOT yet: full aiohttp/fastapi, file-sink precision.

Slice 4 (2026-09-27, MEASURED): the java2zfl soundness lesson ported. 14 new fixtures (u01-u14);
13 of them fail on the slices-1-3 engine, 10 of those by a false EARNED ("clean") on a real flow:
a Z return read as F, a return before a reassignment lost, except overwriting try, a loop assumed to
run, `+=`, tuple unpacking, `d[k]=v`, html.escape trusted before os.system, a callee defined after
its caller; one silent (keyword argument). Real apps, same day: pygoat 7 -> 8 REFUTED (+ views.py:927,
`open(os.path.join(dir, request.POST["blog"]))`, verified), flask 20 -> 23 OPEN (the three were
false-clean: `prepare_import()`'s unknown return into `__import__`, an environment variable into
from_pyfile), dvpwa 1 REFUTED, microblog 1 OPEN, DSVW 9 OPEN — unchanged. No labelled denominator
for Python yet.
