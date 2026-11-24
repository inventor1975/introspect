# Introspect — shared semantics contract (all language modules)

The MODULAR plan (curator, 2026-09-11): a folder per language (php2zfl=PHP, py2zfl=Python, …),
each self-contained, NO shared code-core. What IS shared, to keep modules consistent, is this
SPEC + the ZFL/ztljudge verdict layer + the catalog SCHEMA. Each module implements this spec in
its own code against its own AST and its own ecosystem catalog.

## 1. Verdicts — the seven dispositions of the ZTL judge (rework of 2026-11-24, DRAFT for the curator)
Modules never choose a verdict. They write a ZFL document whose ATOMS are facts read from the code, and the ONE ZTL
judge returns the disposition (via taintjudge). What each disposition means for a source → sink flow, and which
construct produces it:

| disposition | meaning for a sink | produced by (code construct) | status |
|---|---|---|---|
| **EARNED** | clean under every reading of every occurrence | constant; sanitiser verified for the sink's context; whitelist guard on an immutable value | built |
| **REFUTED** | attacker data reaches the sink unsubstituted under every reading — a proven flow. An accusation | source → sink with no substitution, every link read | built |
| **EARNED IF STABLE** | clean PROVIDED a value read at two places is one fact at both | check-then-use on a RE-READABLE value (TOCTOU): a file or path on disk, an env var, a mutable attribute or global across a call, a DB/cache/session value, a second read of the request. The cure: read once, use that copy | to build |
| **REFUTED IF STABLE** | the accusation holds PROVIDED the value read back is the one written | second-order flow: attacker data stored (DB, session, cache, file) and read back later into a sink | open: no encoding yet (MEASURED: one read-back occurrence gives OPEN) |
| **ON CREDIT** | clean as written, but resting on a NAMED unverified link; checking that link can kill it | an assumed summary of an unresolved callee; a sanitiser recognised by name only (`--assume-tree-methods`) | to rebuild (MEASURED: the current row shape gives OPEN, not the ON CREDIT php2zfl's comment promises) |
| **OPEN** | "не знаю": origin or neutralisation cannot be verified | untraced source, unknown callee, unverifiable sanitiser | built |
| **E** | no subject: the claim rests on something that does not exist in the analysed code | parse failure; a sink argument naming a symbol defined nowhere | to define |

Rules:
- **Silence is never "safe".** When unsure, OPEN — never an unverified flow downgraded to EARNED.
- **IF STABLE is not a clearance and not an accusation.** EARNED IF STABLE says what must hold (one value at check and
  at use); REFUTED IF STABLE says what the accusation rests on. Reports name the value (`if_stable`).
- **Worst-sink order** for a file or project: REFUTED > REFUTED IF STABLE > OPEN > ON CREDIT > EARNED IF STABLE >
  EARNED. E is reported apart (it is neither clean nor dirty).
- **Exit status:** nonzero on REFUTED (as now); `--strict` also on REFUTED IF STABLE.

## 2. Taint state: F / T / Z — per OCCURRENCE
F = clean, T = attacker-controlled, Z = unknown. Join (branch merge): T if any branch T, else Z if any Z, else F.
New: a value that the code reads at more than one place, and that can change between the reads, is ONE dirty atom with
SEVERAL occurrences (the check site and the use site). The module must hand the judge both occurrences; the judge reads
each on its own (→ not EARNED) and decides IF STABLE by completions. An immutable local value is one occurrence.

How each shape is written for the judge (MEASURED on ZTL @ efbbbc2, 2026-11-24):
- the claim is a formula over rows (`claim: "~ok | ok"`), or a defined row — both give the same disposition since
  ZTL @ ac71929/efbbbc2 (before that a defined row whitewashed IF STABLE to EARNED);
- TOCTOU: `ok` = "the value passes the check" (unverified, re-readable), claim `~ok | ok` → EARNED IF STABLE;
- on credit: `a` = "the assumed link holds" (unverified, named), claim `~~a` ("nothing shows the link fails") →
  ON CREDIT — the same shape as the book's NOT ( NOT (Z) ), true on credit;
- what counts as a RE-READ: re-evaluating an expression the engine cannot prove returns the same value (a call,
  an attribute or subscript of an object it does not track: Python `request.args.get("f")`, `os.environ.get(..)`).
  A plain value whose every write the engine tracks (PHP `$_GET['x']`, a local) is ONE value: plain EARNED.
  MEASURED 2026-11-24: py2zfl's rule moves 0 of 3,014 findings on our code and 0 of 77 on pygoat/flask/microblog.
- `Tr(x)` reads Z as F at each occurrence: it is right for "verified to arrive / verified substituted", and it is
  exactly what erases IF STABLE and ON CREDIT — not to be used on a re-readable or assumed atom.

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

## 8. Path checks — two judgement calls, the same in every module (2026-09-28)
- **A basename clears the file context** (`os.path.basename`, `path.basename`, `filepath.Base`, `File.basename`,
  `Path.GetFileName`). Its one surviving name, `..`, joined to a base names the base's PARENT DIRECTORY, not a
  file outside it: a read or write of it fails. This is an argued call, not a proved one. A delete of that
  directory (`rm_rf`, `Directory.Delete(.., true)`) is the case it does not cover.
- **Rejecting `..` alone is Z for the file context, not clean**, where the language's path join lets an ABSOLUTE
  path replace the base (C# `Path.Combine`, Ruby `File.expand_path` / `Pathname#join`, Python `os.path.join`).
  Where the join cannot be replaced (Go `filepath.Join`), the rejection clears the file context.
