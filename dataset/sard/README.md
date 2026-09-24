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

### False alarms (benchmark says *safe*, ZTL says vulnerable): 1 079 — each one MEASURED

No "vulnerable" claim here rests on reasoning. `confirm_alarms.py` runs, for every one
of the 1 079 files, the file's own input read and sanitiser on a probe of the context's
bare metacharacters, then reads whether the dangerous character **survives raw to the
point of the sink**. The sink itself never runs: function sinks
(`system`, `mysql_query`, `header`, …) are stubbed to no-ops, and the two that are
language constructs (`eval`, `include`/`require`) are cut away before they execute. The
column `false_alarm_confirmation` on each row is that measurement.

  | | measured verdict | count | reading |
  |---|---|--:|---|
  | **high confidence** | `not_neutralised` | **574** | the metacharacter reaches the sink; **the benchmark's "safe" is wrong** |
  | **high confidence** | `neutralised`     | **323** | the guard escapes/removes the character; **ZTL's alarm is conservative — our false positive, not a vulnerability** |
  | context-dependent    | either            | **182** | HTML attribute / event-handler context; **held, claimed neither way** |

- The **574 confirmed mislabels** are: SARD's `safe/` command-injection files whose
  "sanitiser" (`addslashes`, `htmlspecialchars`, `mysql_real_escape_string`, `preg_replace`,
  magic-quotes) does not touch shell metacharacters, so `;` reaches `system()` (266);
  file-inclusion files where `/` and `..` reach `include()` (238); and XSS-in-`<script>`
  files where an HTML-text escaper does not neutralise a JavaScript-string context (70).
  Included among them are **42** files whose source applies `escapeshellarg` to the
  variable `$tained` — a typo for `$tainted` — so the guard protects nothing.
- The **323 our-false-positives** are single-quoted SQL and `eval` files where the guard
  does escape (`\'`) or encode (`&#039;`) or remove the quote. **Caveat, stated:**
  `addslashes` neutralises this *specific* single-quoted construction under default MySQL,
  but is not a correct general SQL defence (multibyte and `NO_BACKSLASH_ESCAPES` edge
  cases); ZTL's refusal to credit it is defensible even though, for these exact files, the
  quote does not break out. `mysql_real_escape_string` (removed in PHP 8) is modelled by
  `addslashes`, and the removed `FILTER_SANITIZE_MAGIC_QUOTES` by `FILTER_SANITIZE_ADD_SLASHES`
  — both escape the quote identically.
- The **182 held** are HTML attribute/event-handler contexts, where exploitability turns
  on the exact quoting and the browser's decoding order; the coarse metacharacter probe is
  not authoritative there, so the dataset records the measurement but claims nothing.

What is **not** claimed: end-to-end exploitation. "not_neutralised" means the metacharacter
demonstrably reaches the sink un-neutralised (a mislabel by any static standard), measured
with the sink stubbed — it is not a fired exploit.

## Method, stated plainly

Misses were adjudicated by signatures read in the source. False alarms were **measured**
(`confirm_alarms.py`): the file's input read and sanitiser were run on a bare-metacharacter
probe, and the value reaching the sink was inspected. **No sink and no exploit ran** — every
function sink was stubbed to a no-op and every construct sink (`eval`, `include`/`require`)
was cut away before execution. So a program was run, but only the guard, never the attack.

## Contents and licence

- `sard_ztl_verdicts.jsonl` — 31 824 rows; per file: CWE, context, source, sanitizer,
  construction, the SARD **file name** (which encodes the case), the benchmark's label,
  the ZTL verdict, the named weak link, whether the two agree, a note on the disagreement,
  and for every false alarm the measured `false_alarm_confirmation` and
  `false_alarm_confidence`.
- `false_alarm_confirmation.jsonl` — the raw measurement for the 1 079 false alarms: the
  value that reaches the sink and whether the metacharacter survived.
- `summary.json` — the per-CWE counts above.
- `build.py` — regenerates the dataset from the six `CWE_*.json` runs of `bench/sard.py`,
  joining the confirmation. `confirm_alarms.py` — produces the confirmation (stubbed sinks).

**No source-file contents are included.** The SARD / Stivalet suite's licence is not
stated at its source, so only the NIST filenames and *our* verdicts travel here. The
verdicts, the categorization and any judgement of the benchmark's labels are ours and
are contestable per row.

## AI disclosure

Built by **Claude (Anthropic)** as architect and implementer, with **Vitaly Reznik**
as human curator. The ZTL logic and the introspect analyzer are his projects.
