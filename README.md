# introspect

**Zero-trust taint analysis: prove the flow, or say "unknown" — never guess.**

`introspect` is a code taint analyzer for **PHP, Python, Java, Go, JavaScript/TypeScript,
Ruby and C#**. It reports attacker-controlled data reaching a dangerous sink — but only
when it can *prove* the flow. When it cannot verify, it says so, out loud, instead of
guessing. It is a reference implementation of **Zero-Trust Logic (ZTL)** applied to code —
not a replacement for mature scanners like Snyk or CodeQL.

## The idea: three verdicts, and an honest "I don't know"

Most scanners answer a two-valued question ("vulnerable / not"). introspect answers a
**three-valued, zero-trust** one:

| verdict | meaning |
|---|---|
| **REFUTED** | attacker-controlled data reaches a sink **unsubstituted** — a proven-unsafe flow (an accusation). |
| **OPEN** | *"I don't know."* A dangerous sink is reached but the origin or the neutralisation **cannot be verified**. Not an accusation, not a clearance. |
| **EARNED** | proven clean — a constant, a verified sanitiser, a whitelist. |

The guiding rule is **"absence is never an act"**: silence is never "safe". A search that
finds nothing means *"I looked here and here"*, not *"there is nothing"*. So when a flow
is unverifiable, introspect emits **OPEN**, never a false clearance and never a false
accusation. Precision — *what it accuses is real* — is the contract's guarantee; recall is
bounded by what the parser can see.

## Two ways in

- **Static core (free, no API, no tokens).** Seven per-language modules parse source with
  that language's **own** parser and track taint (`F` clean / `T` attacker-controlled /
  `Z` unknown) from sources to sinks, across functions and files.
- **AI-assisted front-end (optional).** A human states a claim or pastes code in natural
  language; the **LLM only *translates*** it into ZFL (the formal intermediate) — it never
  judges. A deterministic, measured **core does the judging**. The LLM's output is itself an
  unverified input (the mark `Z`): truth is never granted on credit, not even to the
  translator.

```
input ──AI translates──► ZFL ──validator──► deterministic core judges ──► verdict
        (LLM = unverified Z)                 (AI-free, measured)          REFUTED/OPEN/EARNED
```

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

## Run

```bash
python3 php2zfl/php2zfl.py  path/to/app        # or py2zfl / java2zfl / go2zfl / js2zfl / rb2zfl / cs2zfl
python3 <lang>2zfl/test_<lang>2zfl.py          # each module's regression gate
python3 ztlstudio.py                           # the AI-translate / core-judge studio → http://localhost:8190
```

## What's measured, and what isn't (read this before trusting a number)

- **Precision is strong, and context-aware.** On the NIST/Stivalet PHP suite, php2zfl's raw
  "false alarms" are almost all **defects in the benchmark's own oracle** — it labels a file
  "safe" whenever *any* sanitiser was applied, ignoring whether it fits the sink; introspect
  does not (an HTML-escaper does not protect a shell command). On clean real apps
  (spring-petclinic, gin examples, express core, sinatra) it raised **zero false positives**.
- **Recall is measured with a denominator only for PHP** (SARD/Stivalet: effectively 0 real
  misses on SQL and command once oracle defects are excluded). For the other six languages,
  recall is evidenced by **true positives verified by hand** on deliberately-vulnerable apps
  (NodeGoat, govwa, railsgoat, java-sec-code) with 0 false positives on their clean
  counterparts — not by a labelled denominator. Treat those as *"promising"*, not *"proven"*.
- **Bounded by the AST.** Framework-indirected sinks whose payload lives outside the source
  (MyBatis XML mappers, custom framework dispatch, WebForms server-control `.Text`) are a
  different analysis surface and are not modelled. Deep cross-layer flows resolve to **OPEN**,
  never a guessed REFUTED.

## Dependencies

Static core: Python 3. Per-language parser: PHP (php + PHP-Parser), Java (`pip install
javalang`), Go (`go` toolchain), JS/TS (`npm install @babel/parser`), Ruby (stdlib Ripper),
C# (.NET SDK; the Roslyn helper builds on first use). The AI front-end reads its API key from
a local, git-ignored `.<provider>_key` file or environment variable — **no keys are bundled**.

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
