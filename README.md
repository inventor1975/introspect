# introspect

**Zero-trust taint analysis: prove the flow, or say "unknown" — never guess.**

`introspect` is a code taint analyzer for **PHP, Python, Java, Go, JavaScript/TypeScript,
Ruby and C#**. It reports attacker-controlled data reaching a dangerous sink — but only
when it can *prove* the flow. When it cannot verify, it says so, out loud, instead of
guessing. It is a reference implementation of **Zero-Trust Logic (ZTL)** applied to code —
not a replacement for mature scanners like Snyk or CodeQL.

## The idea: the judge's verdicts, and an honest "I don't know"

Most scanners answer a two-valued question ("vulnerable / not"). introspect hands each flow to the ZTL judge
and reports the judge's own disposition — never a verdict of its own. Three are the everyday ones:

| verdict | meaning |
|---|---|
| **REFUTED** | attacker-controlled data reaches a sink **unsubstituted** — a proven-unsafe flow (an accusation). |
| **OPEN** | *"I don't know."* A dangerous sink is reached but the origin or the neutralisation **cannot be verified**. Not an accusation, not a clearance. |
| **EARNED** | proven clean — a constant, a verified sanitiser, a whitelist. |

Since 2026-11-24 the conditional ones are reported too, where a module can produce them (they used to be
folded into OPEN):

| verdict | meaning | produced today |
|---|---|---|
| **EARNED IF STABLE** | clean **if** a value is the same at the check and at the use (time-of-check/time-of-use) | Python: a check on one read of a source, a use on a re-read (`if request.args.get("f") in ALLOWED: os.system(... request.args.get("f"))`) — it was a false REFUTED |
| **ON CREDIT** | clean as written, resting on a **named** unverified link | PHP under `--assume-tree-methods`: a call answered from the tree's definition of that name, the receiver's class unchecked |
| **REFUTED IF STABLE** | the accusation holds **if** the value read back is the one written (second-order flows) | not yet: no faithful encoding found |
| **E** | no subject: the claim rests on something absent from the code | reserved |

Measured, so the table is not over-read: the Python re-read rule changed **0** of 77 findings on pygoat, flask and
microblog and 0 of 3,014 on our own code — exact where it applies, rare in practice. ON CREDIT needs the
non-default flag. `INTROSPECT-SEMANTICS.md` §1–2 is the contract.

The guiding rule is **"absence is never an act"**: silence is never "safe". A search that
finds nothing means *"I looked here and here"*, not *"there is nothing"*. So when a flow
is unverifiable, introspect emits **OPEN**, never a false clearance and never a false
accusation. Precision — *what it accuses is real* — is the contract's guarantee; recall is
bounded by what the parser can see.

## How it works

Seven per-language modules parse source with that language's **own** parser and track taint
(`F` clean / `T` attacker-controlled / `Z` unknown) from sources to sinks, across functions
and files — no API, no tokens, no network. A single deterministic ZTL core (vendored in
`ztlcore/`) judges each flow:

```
source ──► AST ──► taint (F / T / Z) ──► ZTL core judges ──► REFUTED / OPEN / EARNED (+ IF STABLE, ON CREDIT)
                                         (AI-free, measured)
```

> Prefer to work in natural language? The **AI-assisted studio** — an LLM *translates* your
> words into ZFL and the same core judges (the translator's output is itself unverified,
> `Z` — truth is never granted on credit, not even to the translator) — lives in its own
> repo: **[ztlstudio](https://github.com/inventor1975/ztlstudio)**.

## Languages

| module | language | parser (native) | catches (sources → sinks) |
|---|---|---|---|
| `php2zfl` | PHP | PHP-Parser (+ HTML-context lexer) | superglobals → sql/shell/xss/file/… |
| `py2zfl` | Python | native `ast` | Flask/Django/FastAPI → shell/code/sql/ssti/deser/xss |
| `java2zfl` | Java | javalang | servlet + Spring → sql/shell/xss/deser |
| `go2zfl` | Go | Go's own `go/ast` | net/http + gin → sql/shell/file/ssrf/xss |
| `js2zfl` | JS/TS | @babel/parser | Express/Koa → shell/code/sql/xss/ssrf/redirect |
| `rb2zfl` | Ruby | Ruby's own Ripper | Rails/Sinatra → sql/shell/code/xss/file/ssrf |
| `cs2zfl` | C# | Roslyn | ASP.NET → sql/shell/xss/file/deser |

Every module implements the same contract ([`INTROSPECT-SEMANTICS.md`](INTROSPECT-SEMANTICS.md)):
cross-function + cross-file summaries, guards, branch-join, and **context-aware sanitisers**
(an HTML-escaper clears XSS but is transparent for SQL/shell — the escaper's context must
match the sink's).

## Lean: does a theorem say what its words say? (`lean2zfl`, 2026-11-24)

Mathlib's total functions return a conventional value outside their domain (a non-summable series sums to 0,
x / 0 = 0, √ of a negative is 0, log 0 = 0, ℕ-subtraction truncates). `∑' n : ℕ, (n : ℝ) = 0` is a theorem of
Mathlib, and the kernel is right to accept it: it checks the steps, not what the statement means. `lean2zfl` reads
every theorem from the elaborated environment and asks the ZTL judge, per junk operation in the statement:

| verdict | when |
|---|---|
| **EARNED** | every junk operation guarded — by a hypothesis, or by a domain condition PROVED at dump time (positivity / norm_cast + omega / norm_num, no error recovery, no sorry) |
| **E** | the proof takes a junk branch: the statement holds at that point only by the convention (no subject) |
| **EARNED IF STABLE** | one unguarded term occurs more than once, and the statement is PROVED for every value of it (the term abstracted to a fresh variable) — true if stable |
| **OPEN** | an unguarded operation, junk branch not seen |
| **ON CREDIT** | the proof rests on an axiom beyond propext / choice / Quot.sound (`sorry` included), named |

Measured on six Mathlib modules (480 theorems, generated equation lemmas excluded, none lost): EARNED 285, OPEN 173,
E 22 (e.g. `Real.log_pow` and `Real.log_inv` for every x, holding at 0 and below by the log convention;
`one_le_div_iff` at b = 0), IF STABLE 0. An earlier count of 342 was short: 138 theorems were silently lost to a
heartbeat limit shared by the whole command — now counted per theorem, and a theorem that cannot be read is listed
as NOT ANALYSED. Most of the remaining OPEN are honest: a convention point really is in the statement (`(↑n)⁻¹` at
n = 0 in a limit, `√(f y)` for every y in a derivative), and whether it matters is a semantic question; on our ztl-classical (45 files, 310 theorems,
read from the built .olean files in one Lean run, 40 s): EARNED 306, OPEN 4. OPEN is coarse in v1 (terms under a binder, conditions phrased otherwise,
summability known by a lemma); E is the precise part. Run: `python3 lean2zfl/lean2zfl.py FILE.lean` in a Lake
project with Mathlib, or `--module PROJECT Mathlib.X.Y` for built modules.

## Run

```bash
python3 introspect.py  path/to/project         # every language at once, routed by file extension
python3 php2zfl/php2zfl.py  path/to/app        # or one language: py2zfl / java2zfl / go2zfl / js2zfl / rb2zfl / cs2zfl
python3 <lang>2zfl/test_<lang>2zfl.py          # each module's regression gate
```

`introspect.py` walks the project, sends each file to the module for its language
(by extension), and merges the verdicts into one report — **skipping, with a reason,**
any language whose parser isn't installed (never a silent clean bill), and listing
files it doesn't cover as out-of-scope, never "safe". Exit status is nonzero when any
REFUTED is found (handy in CI); with `--strict`, on REFUTED IF STABLE too. Each language is still analysed on its own: flows that
cross **between** languages (or through a database or queue) are not tracked and stay
OPEN, never guessed.

## What's measured, and what isn't (read this before trusting a number)

- **Precision is strong, and context-aware.** On the NIST/Stivalet PHP suite, php2zfl's raw
  "false alarms" are almost all **defects in the benchmark's own oracle** — it labels a file
  "safe" whenever *any* sanitiser was applied, ignoring whether it fits the sink; introspect
  does not (an HTML-escaper does not protect a shell command). On clean real apps
  (spring-petclinic, gin examples, express core, sinatra) it raised **zero false positives**.
- **Recall is measured with a denominator for PHP and Java.** PHP: SARD/Stivalet, effectively 0 real
  misses on SQL and command once oracle defects are excluded. Java: NIST Juliet, the 1 110
  servlet-source cases of CWE78/89/80/81/83 — 0 misses, 0 false alarms, the rest honest OPEN
  (`java2zfl/CALIBRATION.md`). For the other five languages,
  recall is evidenced by **true positives verified by hand** on deliberately-vulnerable apps
  (NodeGoat, govwa, railsgoat, java-sec-code) with 0 false positives on their clean
  counterparts — not by a labelled denominator. Treat those as *"promising"*, not *"proven"*.
- **Unknown is OPEN, never a silent "clean" (2026-09-27).** The Java fix — every place a walk wrote F
  for "don't know" (a helper's unknown return, a catch overwriting a try, a loop assumed to run, `+=`,
  container stores, unparsed blocks) — was ported to Python, JS/TS, Go, Ruby and C#. Each module's
  `CALIBRATION.md` lists the fixtures that pin it (58 new, 56 fail on the previous engines) and the
  real-app deltas: new findings are real vulnerable sites the old engines passed in silence
  (railsgoat's upload-filename command injection inside a block, govwa's template.HTML flows), and
  no new REFUTED on a clean app.
- **Blind measures (27.09), the only numbers not fitted by the author.** Cloud-written corpora committed
  before the analyzer ran: Java round 1 54% found / 16% false alarms, round 2 (after its fixes) 77% / 12%;
  Python 36% / 10%; JS/TS (xss + file only) 46% / 23%. Each round's fixes are in that module's
  CALIBRATION.md; after a fix the same corpus only shows the fix holds. SQL, code and command injection in
  JS, and command injection everywhere, have no blind measure — the corpus authors were stopped by a
  safety filter.
- **Bounded by the AST.** Framework-indirected sinks whose payload lives outside the source
  (MyBatis XML mappers, custom framework dispatch, WebForms server-control `.Text`) are a
  different analysis surface and are not modelled. Deep cross-layer flows resolve to **OPEN**,
  never a guessed REFUTED.

## Dependencies

Python 3 for the engine (stdlib only; the ZTL core is vendored in `ztlcore/`, so a clone is
self-contained). Per-language parser: PHP (php + PHP-Parser), Java (`pip install javalang`),
Go (`go` toolchain), JS/TS (`npm install @babel/parser`), Ruby (stdlib Ripper), C# (.NET SDK;
the Roslyn helper builds on first use). No API keys, no network, no tokens — the static core
runs entirely offline.

## Status

**v1.0.0.** Seven languages, all with XSS, all regression gates green. A precision-first,
zero-trust research/reference tool.

## AI disclosure

Built by **Claude (Anthropic)** as architect and implementer, with **Vitaly Reznik** as human
curator and decision-maker. Every design and measurement was reviewed against the honesty
discipline this project is built on: mark boundaries honestly, measure — don't guess, and never
claim more than was verified.

## License

Dual-licensed under **MIT** and **Apache-2.0** (see `LICENSE-MIT`, `LICENSE-APACHE`).
