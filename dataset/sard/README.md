# ZTL verdicts over the SARD / Stivalet PHP vulnerability suite

This dataset records what the **introspect** analyzer (the ZTL zero-trust judge over
a deterministic PHP atomizer) returns on the public NIST **SARD / Stivalet** PHP test
suite — one row per test file, the verdict and the *named weak link* behind it. It is
a measurement of a static analyzer against a labelled benchmark, published so the
disagreements can be inspected rather than taken on trust.

## What a verdict means

Three outcomes, never two:

- **REFUTED** — a tainted value reaches a sink un-neutralized for that sink's context.
- **EARNED** — every tainted value is neutralized before the sink (verified clean).
- **OPEN** — the judge does **not** decide, and says what is missing. This is not a
  failure: it is the zero-trust answer when the input's origin is a database, a
  session, or an unknown call that ZTL will not credit or blame on faith.

`OPEN` is counted as an **abstention** here, never as a hit and never as a miss.

## The runs behind it (measured, not recalled)

- Instrument: `github.com/inventor1975/introspect` at commit **3f3205f**, PHP atomizer
  `nikic/php-parser v5.7.0`. No network, no API keys — the static core runs offline.
- Corpus: the SARD / Stivalet suite (42 212 synthetic PHP files), run **2026-09-24**.
- Six CWE classes are modelled, each judged in one sink context:

  | CWE | context | files | unsafe→REFUTED | unsafe→OPEN | unsafe→EARNED (miss) | safe→EARNED/NONE | safe→OPEN | safe→REFUTED (false alarm) |
  |---|---|--:|--:|--:|--:|--:|--:|--:|
  | CWE_89 SQL injection      | sql    | 9 552  | 357  | 555  | **0**    | 7 680 | 750 | 210 |
  | CWE_78 command injection  | shell  | 2 496  | 224  | 384  | **16**   | 1 200 | 406 | 266 |
  | CWE_95 code injection      | code   | 1 632  | 119  | 213  | **4**    | 420   | 763 | 113 |
  | CWE_98 file inclusion      | file   | 3 264  | 238  | 402  | **32**   | 1 920 | 434 | 238 |
  | CWE_79 cross-site scripting| html   | 10 080 | 1 134| 2 034| **1 184**| 4 768 | 708 | 252 |
  | CWE_601 open redirect      | header | 4 800  | 896  | 1 344| **352**  | 2 080 | 128 | 0   |
  | **total**                  |        | **31 824** | 2 968 | 4 932 | **1 588** | 18 068 | 3 189 | 1 079 |

  The other SARD classes (LDAP and XPath injection, IDOR, sensitive-data exposure,
  session management) are **not modelled** and are absent from this dataset — never
  reported as "safe".

## The large OPEN column is by design, not by weakness

SARD draws its tainted value from sixteen sources. Only three — `$_GET`, `$_POST`,
`$_GET` through an array — are inputs ZTL treats as attacker-controlled. The other
thirteen (`$_SESSION`, the output of `fopen`/`exec`/`unserialize`, in-file getter
objects, …) are **Z by policy**: a database, a session or an unknown call is not
visible, so the honest verdict is OPEN, never EARNED and never REFUTED. So a large
part of every OPEN count is those thirteen sources answered correctly with a
non-answer. Recall against the label is meaningful **only on the three measured
sources**; the rest are measured against *silence*, where an OPEN is right and an
EARNED would be a lie.

## The disagreements — this is the point of publishing

### Misses (benchmark says *unsafe*, ZTL says clean): 1 588, and every one is a defect of the benchmark

Not a sample — all 1 588 are classified mechanically by a signature read in the source
(`build.py`), with **zero** left unclassified. The categories (a file that carries two
defects is attributed to the first matching signature, so a sub-count may shift by
match order; the total and the zero do not):

- **whitelists that really whitelist** — a ternary or `in_array` that assigns a safe
  literal in *every* branch, or a `FILTER_VALIDATE_INT/FLOAT` gate with an empty-string
  else. The `unsafe/` directory and the `//flaw` comment are the generator's template,
  stamped whether or not the guard closes the hole.
- **`sprintf("…%d…", $tainted)`** — the value is coerced to an integer; nothing injects
  through a number. (One file's name even says `%s` while its body uses `%d`.)
- **whitelist to `/^[a-zA-Z]*$/` or `/^[a-zA-Z0-9]*$/`, else empty**, and
  **`preg_replace('/\W/si','')`** — for an open redirect, a value with no `:` `/` `.`
  cannot point off-site.
- **email validated then printed as body/div text** — `FILTER_SANITIZE_EMAIL` +
  `FILTER_VALIDATE_EMAIL`, output in ordinary HTML text.
- **the sink prints the bare constant `checked_data`** — a generator slip: the tainted
  variable never reaches the output at all.

So on the modelled classes, **no miss survives inspection**: the instrument is not
silent where this generator plants a flaw it actually plants. That is a statement about
this synthetic corpus and nothing more.

### False alarms (benchmark says *safe*, ZTL says vulnerable): 1 079 — grouped by mechanism, **not** fully adjudicated

Each row carries the tool's own receipt. Grouped by that receipt:

- **595** — the applied function does not substitute the value for this sink's context,
  so it reaches the sink unchanged. This bucket is **mixed** and is the honest boundary
  of this dataset: it contains both genuine mislabels (e.g. `addslashes` or
  `mysql_real_escape_string` before an OS command — the shell does not read SQL/C
  escaping) **and** ZTL's own conservatism (e.g. stripping the quote for a
  single-quoted SQL string does neutralize it, but ZTL's catalogue does not credit that
  removal for the sql context). Separating the two per file is case work **not done
  here**.
- **358** — a sanitizer for a *different* context than the sink (an HTML escaper before
  a SQL/shell/file sink); SARD labelled the file safe because *some* sanitizer ran.
- **112** — the value is escaped but lands in an HTML attribute-name or event-handler
  context, which ZTL refuses by policy (the browser decodes entities before the script
  parser runs). A position held on purpose, listed so no one counts it as an accident.
- **14** — other; read the per-row receipt.

Of the false alarms, **42** are files whose source applies `escapeshellarg` to the
variable `$tained` — a typo for `$tainted` — so the guard protects nothing and the
value reaches `system()` unescaped. There the benchmark's "safe" is wrong.

## Method, stated plainly

Disagreements were adjudicated by **reading each case against established security
semantics** (what an escaper does and does not neutralize in a given sink context) and
by mechanical signatures over the source — **not** by executing the files with attack
payloads. Nothing in producing this dataset was run as a program under attacker input.

## Contents and licence

- `sard_ztl_verdicts.jsonl` — 31 824 rows; per file: CWE, context, source, sanitizer,
  construction, the SARD **file name** (which encodes the case), the benchmark's label,
  the ZTL verdict, the named weak link, whether the two agree, and a note on the
  disagreement.
- `summary.json` — the per-CWE counts above.
- `build.py` — regenerates both from the six `CWE_*.json` runs of `bench/sard.py`.

**No source-file contents are included.** The SARD / Stivalet suite's licence is not
stated at its source, so only the NIST filenames and *our* verdicts travel here. The
verdicts, the categorization and any judgement of the benchmark's labels are ours and
are contestable per row.

## AI disclosure

Built by **Claude (Anthropic)** as architect and implementer, with **Vitaly Reznik**
as human curator. The ZTL logic and the introspect analyzer are his projects.
