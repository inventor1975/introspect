# Introspect — shared semantics contract (all language modules)

The MODULAR plan (curator, 2026-09-11): a folder per language (php2zfl=PHP, py2zfl=Python, …),
each self-contained, NO shared code-core. What IS shared, to keep modules consistent, is this
SPEC + the ZFL/ztljudge verdict layer + the catalog SCHEMA. Each module implements this spec in
its own code against its own AST and its own ecosystem catalog.

## 1. Verdicts (three-valued, zero-trust)
- **REFUTED** — attacker-controlled data reaches a sink UNSUBSTITUTED (a proven-unsafe flow). An accusation.
- **OPEN** — "не знаю": a dangerous sink is reached but the origin or the neutralisation cannot be
  VERIFIED (untraced source, unknown callee, weak/unverifiable sanitiser). NOT an accusation, NOT "safe".
- **EARNED** — proven clean/neutralised (constant, verified sanitiser, whitelisted).
Rule: **silence is never "safe"**. When unsure, emit OPEN — never downgrade an unverified flow to EARNED.

## 2. Taint state: F / T / Z
F=clean, T=attacker-controlled, Z=unknown. Join (branch merge): T if any branch T, else Z if any Z, else F.

## 3. Catalog (per-language DATA, shared SCHEMA)
- **sources** — expressions producing attacker data → T (framework request objects, stdin, argv).
- **sinks** — {name → ctx} (sql/shell/code/file/deser/ssti/header/…) with the dangerous ARG index(es).
  A sink dangerous only under a condition (subprocess w/ shell=True; callable-position of dynamic call) records that.
- **sanitizers** — neutralise for a context (escapers, parameterisation, int-cast, whitelists).
- **transparent transformers** — PRESERVE taint, NOT sanitisers (decode/encode/b64/unquote/re.sub/format/.get/.read).

## 4. Flow rules every module must implement
- **Summaries**: per function/method, which PARAM reaches which sink-ctx / passes to return / is opaque.
  Built by tainting each param and WALKING the body (intra-fn dataflow through assignments). Applied at call sites; CROSS-FILE (index all files, then judge).
- **Guards**: `x in WHITELIST` (or equivalent) narrows x to F inside the guarded branch.
- **Objects — RECEIVER-AWARE**: a method call resolves to the RECEIVER's known class method; NEVER match a
  sink by bare method name when the receiver's class is known (the PHP `->execute`/Logger collision lesson).
  Bare method-name sinks (e.g. cursor `.execute`) apply ONLY when the receiver class is unknown.
- **Entry points**: framework routes/views are analysed as scopes (the source→sink often lives inside the view).
- **Branches**: if/else in SEPARATE envs, then MERGE (join) — a branch assignment must not leak into the other.

## 5. What stays shared vs per-module
Shared: this spec, the ZFL/ztljudge verdict layer, the catalog SCHEMA, a cross-language test discipline.
Per-module: the AST walker (language-native), the ecosystem catalog DATA (its frameworks/sinks/sanitisers).

## 6. Reference implementations
- PHP: tool/php2zfl/ (atoms.php + php2zfl.py) — the mature reference.
- Python: tool/py2zfl/ (py2zfl.py) — native `ast`; validated on Flask/Django/aiohttp (2026-09-11).
- C#: tool/cs2zfl/ (csast/ Roslyn dotnet helper + cs2zfl.py) — C#'s OWN Roslyn -> compact JSON; ASP.NET
  sources (Request.Query/Form/QueryString/Params, Request["x"], [FromQuery]/[FromRoute]/[FromBody],
  bare public action params returning *Result); sinks Process.Start=shell, new *Command/*DataAdapter(concat)
  + .CommandText=sql, Response.Write/Html.Raw/new HtmlString=xss, File.*=file, *.Deserialize=deser;
  HttpUtility.HtmlEncode context-aware; cross-file + guards. Calibrated 2026-09-13 (tool/cs2zfl/CALIBRATION.md):
  engine validated on MVC/Core fixtures; WebGoat.NET (WebForms) 0 FP but .Text control-sources un-modelled.
- Ruby: tool/rb2zfl/ (rbast.rb + rb2zfl.py) — Ruby's OWN Ripper (stdlib, zero install) via a thin JSON
  dumper; Rails/Sinatra sources (params/params[:x]/request.*/cookies), sinks shell/code/sql/xss(raw,
  html_safe)/file/ssrf; conditional AR methods are sinks ONLY on interpolated STRING args (where(hash)
  is safe); guards + cross-file. Calibrated 2026-09-13 (tool/rb2zfl/CALIBRATION.md): 0 FP on sinatra,
  2/2 verified-true on railsgoat.
- JS/TS: tool/js2zfl/ (jsast.js + js2zfl.py) — @babel/parser via a thin JSON dumper (JS/JSX/TS/TSX);
  Express/Koa sources (req.query/params/body/..., receiver-gated on req/request/ctx), sinks shell
  (child_process-gated: regex.exec collision avoided), code (eval/new Function), sql, xss (res.*-gated),
  file (fs.*), ssrf (HTTP clients), open-redirect; guards + cross-file; inline arrow handlers analyzed.
  Calibrated 2026-09-13 (tool/js2zfl/CALIBRATION.md): 0 FP on express core, 5/5 verified-true on NodeGoat.
- Go: tool/go2zfl/ (goast.go + go2zfl.py) — Go's OWN go/ast via a thin JSON dumper; receiver-aware via
  dumped param types (gin c.Query vs sql db.Query; w.Write via http.ResponseWriter); prepared-statement
  awareness (stmt from .Prepare passes BOUND params). Calibrated 2026-09-12 (tool/go2zfl/CALIBRATION.md):
  0 FP on gin-examples (clean), 2/2 verified-true on govwa (vuln). Motivating user: Arkady's Go projects.
- Java: tool/java2zfl/ (java2zfl.py) — `javalang`; all §4 rules (summaries+cross-file, guards+branch-join,
  receiver-aware sinks, Spring entry-point sources). Catalog: servlet + Spring (@RequestParam/@PathVariable/
  @RequestBody) sources; sinks by NAME-confidence — specific (exec/executeQuery/executeUpdate/prepareStatement/
  readObject) fire by name, GENERIC (execute/write/print/println) only on a confirmed receiver type else honest
  OPEN/skip; prepareStatement with a `?` placeholder is clean, concatenation is REFUTED. Calibrated 2026-09-12
  (tool/java2zfl/CALIBRATION.md): 0 false positives on spring-petclinic (clean), 2/2 verified-true SQLi on
  java-sec-code (vuln).

## 7. Scope boundaries (honest, per-module)
Static, AST-visible flows only. Out of scope for a source-AST module (a DIFFERENT analysis surface, not a defect):
framework-indirected sinks whose payload lives OUTSIDE the source — e.g. Java MyBatis SQL in XML mappers / `${}`
annotations, ORM query DSLs, template files. Deep cross-layer flows beyond indexed summaries resolve to OPEN
("не знаю"), never a guessed REFUTED. Precision is the contract's guarantee; recall is bounded by what the AST sees.
