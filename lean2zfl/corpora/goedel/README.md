# lean2zfl over Goedel-Prover's Lean Workbook proofs — the run of 2026-11-24

What `lean2zfl` said about **29,750 AI-found Lean 4 proofs**, and what ZTL's numeric floor said about the mathematics
of their statements. These files are the evidence for the counts below. The dataset itself is not copied here.

## Sources

- Proofs: Hugging Face `Goedel-LM/Lean-workbook-proofs`, 29,750 rows (`problem_id`, `full_proof`), MIT licence.
  The informal statement is taken from the comment inside each proof.
- Problems: Hugging Face `internlm/Lean-Workbook` (Lean Workbook and Lean Workbook Plus), Apache-2.0.
- Elaborated with Lean 4 v4.29.1 and Mathlib v4.29.1, in a Lake project of our own (`LEAN2ZFL_PROJECT`).
- The tools: this repository at the run's commits (the ZTL readings are "v3": an admissible point required, a
  leading ∃ read as a witness), and inventor1975/ZTL 365cfde.

## Files

| file | what |
|---|---|
| `scan_goedel.py` | The scan. `python3 scan_goedel.py OUT N BATCH PARALLEL`. `SCAN_IDS=<file>` selects a subset. `GOEDEL_PARQUET`, `LEAN2ZFL_PROJECT` and `LEAN2ZFL_DUMPER` are paths. |
| `full_rows.jsonl.gz` | All 29,750 rows: lean2zfl's disposition per theorem and why. |
| `ids_e_open.txt`, `ztl_e_open_rows.jsonl.gz` | The 2,451 E / OPEN / IF STABLE theorems, with ZTL's reading (`ztl`). |
| `ids_control_earned.txt`, `ztl_control_rows.jsonl.gz` | The control: 1,000 EARNED theorems, randomly drawn (seed 20261124), with ZTL's reading. |
| `findings.jsonl` | The classified readings below, one per line: statement, ZFL claim, hypotheses, box, witness, informal text. |
| `false_math_rows.jsonl.gz`, `Certificates.lean`, `certificates.jsonl` | The refutations re-read and turned into Lean theorems over ℝ ("hypotheses at the point ∧ ¬ conclusion"), closed by tactics with no `sorry` (`../../certify.py`). |

## The counts

**lean2zfl's dispositions over the 29,750 proofs:**

| EARNED | not compiled on our Mathlib | OPEN | E | EARNED IF STABLE | not read |
|---|---|---|---|---|---|
| 20,116 | 7,168 | 1,492 | 915 | 44 | 15 |

**ZTL's reading of the 2,451 E / OPEN / IF STABLE theorems** (`findings.jsonl`, field `class`):

| class | count | meaning |
|---|---|---|
| `false_math_both_readings` | 7 | At an ADMISSIBLE point (every translated hypothesis holds; the empty point for a closed statement) the conclusion is refuted both in the exact reading and in Lean's ℕ convention. |
| `false_math_nat_convention` | 99 | Refuted at an admissible point in the exact reading of ℕ's `/` and `−`; Lean's convention (floor, truncation) holds there. Whether the author meant the floor is a question for the informal text: `lean_workbook_plus_26988` (⌊2017/3⌋) is such a case. |
| `vacuous_hypotheses` | 3 | The conclusion is refuted, but so are the hypotheses: the statement is vacuously true (`lean_workbook_53067`: its hypothesis IS its false conclusion). |
| `refuted_admissibility_unknown` | 2 | The conclusion is refuted; untranslated hypotheses leave open whether any point is admissible. |
| `true_math_lean_via_convention` | 114 | lean2zfl said E (a convention was used), yet ZTL proves the exact mathematics. |
| `no_value_at_admissible_point` | 270 | At an admissible point an operation has no value, for example `x / 0` with no `x ≠ 0` hypothesis. |

Untranslated: 366 (function variables about 150, `tsum` 58, `∃` under a connective 43, `ℂ` 21, and others).

**Lean kernel certificates:** of 103 refutations that could be written as ℝ theorems (102 on 24.11; `plus_78600` added 25.11, not closed), **22** are closed by tactics
(`Certificates.lean`, `[propext, Classical.choice, Quot.sound]`); most of the rest involve `rpow` with fractional
exponents and stay ZTL's verdict only.

**Control:** of the 1,000 EARNED theorems, 0 got a counterexample.

An earlier reading (v2) counted 101 and 9: it took a conclusion refuted over the box as a refutation without
asking whether any point satisfies the hypotheses. Lean's kernel exposed it: the certificate "hypotheses ∧ ¬
conclusion" for `lean_workbook_53067` would not close.

## Limits

- **24% did not compile.** Our Mathlib renamed lemmas the proofs use. Those 7,168 are not judged at all.
- **The box drops some hypotheses.** It uses only hypotheses that bound one variable by a constant, so an OPEN may
  belong to the box and not to the statement. A counterexample is accepted only at a point where every translated
  hypothesis holds; with an untranslated hypothesis, the search is skipped.
- **The exact reading is ours.** An auto-bound variable meant as a product (`abc`), an intended floor, or `n = 0`
  excluded only in words can make a "false" statement the author's correct one. The class says which reading
  refuted it; the informal text decides what was meant.

## Sequences, 2026-11-25 (the curator's "да": computed from their hypotheses, refuted at a point, never EARNED)

A variable `u : ℕ → K` is now read as a **sequence** (`../../zflseq.py`). The hypotheses force its values: a fact,
or a rule instance with one unknown value, linear in it, solved exactly forward or backward. A value outside the
codomain, or a checked instance that is false, means **no sequence satisfies the hypotheses**.
- **Rescanned:** the 100 E/OPEN statements and the 24 control statements whose only blocker was `ℕ → …`
  (`ids_seq.txt`, `seq_rows.jsonl.gz`, dumper frozen).

| class | E/OPEN (100) | control EARNED (24) |
|---|---|---|
| vacuous: no sequence satisfies the hypotheses | **17** | 0 |
| refuted at a point, existence conditional | 6 | 1 |
| checked at points, not refuted | 15 | 5 |
| translated, no value forced | 47 | 9 |
| untranslated (∃, `Nat.Prime`, two-index rules, …) | 15 | 9 |

**The 17 vacuous statements**, each read by hand, fall into two kinds.
- **Contradictory in BOTH readings: 11.** The statement is vacuously true, so Goedel-Prover's accepted proof needed
  nothing about the conclusion. Its proof terms were NOT inspected, so how the proof did it is not claimed.
  - Example: `lean_workbook_11466` gives `u : ℕ → ℕ`, `u 1 = 2` and `u (n+1) = 3 u n + 4` for every n. At n = 0
    the exact reading gives u 0 = −2/3, not in ℕ; in Lean, `u 1 = 3 u 0 + 4 ≥ 4`.
  - The same: `28753`, `plus_32061`, `plus_64920`, `plus_55264` (u 0 = −1/5), `plus_28363` (−5/2), `plus_58839`
    (99/2), `56529` (1/2), `plus_79707` (b 0 = −1), and `20690` (in Lean `(0 − 1)/1 · f 0 = 0 ≠ 2000`).
  - `plus_64022` (a 1 = a 0, yet 1 ≠ 2) is the same in both readings.
- **Contradictory in the EXACT reading only: 5.** Lean's floor or truncation makes them consistent.
  - `14608` and `plus_41806`: b 2 = 1/7 exactly, 0 in Lean.
  - `48498`: c 2 = 1/2.
  - `30373` and `plus_10087`: f 2 = 1 − 2 = −1 exactly, 0 in Lean.
  - These are the ℕ-convention class: the informal text decides what was meant.
- **`plus_47435`: not classified by hand.** A rule guarded by `m ≠ 2^n − 1` over a free n.

**The 7 conditional refutations** (`19623`, `64941`, `25727`, `plus_11170`, `plus_41341`, `5663`, `plus_66017`)
share one shape:
- the rule's instance at n = 0 has **no value** in the mathematics: the index `n − 1` at 0, or `k / k` at 0;
- the next instances force values that contradict the conclusion;
- in Lean the n = 0 instance is read through a convention (`0 − 1 = 0`, `x / 0 = 0`), and it contradicts the other
  hypotheses, so the proof is vacuous.

Example: `lean_workbook_5663` is in the control (Lean proved it). It gives `a 1 = 5`, yet the conclusion says
`a 1 = (2 + 4)/3 = 2`. Lean proves it only because `a 1 = 6 a 0 − 4 a (0 − 1) = 2` at n = 0.

"Conditional" means: false, or vacuously true; the reader does not decide which. By the curator's word, nothing here is
EARNED: a prefix of a sequence proves nothing about every n.

## ∃ under a connective, 2026-11-25 (measured)

The rules come from ZTL's own first-order tableau (`zfo.prove`):
- For ∧, ∨ and the consequent of →, moving the ∃ to the front is valid in both directions. In a positive place, x
  becomes the leading ∃.
- In a negative place only `∀x (P → C) ⊨ (∃x P) → C` holds; the converse has a countermodel with Z. There x joins
  the box as a universal.
- Under ¬ or ↔ the ∃ stays untranslated.
- A witness may pin only the ∃ variables and keep every universal's whole box (a uniform witness).

Rescanned: the 61 statements (43 E/OPEN, 18 control) whose only blocker was an inner ∃.
- **10 now translate.** All are OPEN or ON CREDIT; none is refuted.
- **31 are blocked by an ∃ over a non-number** (a set, a function, ℂ).
- **18 are blocked by an ∃ under ¬ or ↔.**

## Complex numbers, 2026-11-25 (measured)

`z : ℂ` is read as its two real parts (VR's GaussQ), by the field's rules: the product, the quotient with divisor
c² + d², the binomial theorem for zⁿ, conj, ‖z‖ = √(re² + im²), ζ at a real point. `z = w` is both parts equal;
`z ≠ w` is apartness in some part.

Rescanned: the 33 statements (21 E/OPEN, 12 control) blocked by a `ℂ` variable. **30 now translate.** None is
refuted, and all but one stay OPEN. They are algebraic identities under hypotheses: a + b + c = 0 ⇒ 2(a⁵+b⁵+c⁵) =
…; partial fractions; the triangle inequality. Proving them needs elimination (algebra), not reading.

The box now folds a side that has no name (`re == 3 + 4·0 − 0·1`), and it splits a comparison whose sides have spaces.

## Functions at points, 2026-11-25 (the curator's "да"; measured)

`f : D → K` with D ≠ ℕ (ℝ, ℤ, ℚ) is read like a sequence.
- **Instantiation.** A rule `∀ x y, …` is instantiated at a fixed set of rationals, plus the arguments the
  statement names.
- **Forced values.** An instance with one unknown value forces it. When that is stuck, the instances that are
  linear in their unknowns are eliminated as a system, exactly (Gauss–Jordan over ℚ), so
  `2 f x + f (1 − x) = x²` forces f 2 = 7/3.
- **Verdicts.** No recursion builds a function, so every refutation is `conditional`: false, or no f satisfies the
  hypotheses. A contradiction found among the instances is exact: no function satisfies them.

Rescanned: 80 statements (51 E/OPEN, 29 control) whose blocker was a variable `ℝ/ℤ/ℚ → ℝ/ℤ/ℚ`.
- **0 refuted.**
- **2 vacuous.** `lean_workbook_17594` and `plus_7201` take the hypothesis `∀ x, x ≠ 1 ∧ x ≠ -1`, which is false at
  x = 1, in Lean as well. The intended reading was presumably x ∉ {1, −1}.
- 11 checked at points without a refutation.
- 46 translated with no value forced.
- 21 untranslated (`ite`, λ, ∃ over a non-number, `sinh`).

## Concrete sets, 2026-11-25 (measured)

A set the statement writes is read as the condition it names:
- an interval is its bounds, `{x | P x}` is P, `{a, b, c}` is x = a ∨ x = b ∨ x = c, and `range n` is x < n;
- `#{i ∈ [lo, hi] | P i}` over a concrete interval is counted;
- a set VARIABLE (`∀ S`) is not read, which is the higher-order limit.

Rescanned: the 16 statements (12 E/OPEN, 4 control) blocked by `∈` or `card`.
- **12 translate.** One is EARNED by ZTL: `lean_workbook_7425`, the count 143. The rest are OPEN and none is refuted.
  Most of them are ε-δ limits, `∃ δ > 0, ∀ x ∈ (1, δ), …`, where δ depends on ε, so no single witness exists.
- **4 untranslated**: `Set.range` (3) and `Nat.digits` (2), one statement having both.

## More integer words, decimals, ℝ≥0, 2026-11-25 (measured)

New readings:
- ZTL's floor now reads gcd, lcm, fib, totient and isprime, and ⌊x⌋ and ⌈x⌉ of a real.
- `Nat.floor` is max(⌊x⌋, 0) by its definition; `Even` and `Odd` are 2 ∣ n.
- A decimal literal is its exact rational.
- `NNReal` is a real with the box's lower end at 0, and its truncating − is marked like ℕ's.

Rescanned: the 74 statements blocked by these words in the full v4 rescan.
- **69 now translate.** 9 are EARNED by ZTL; most of the rest are OPEN.
- **1 refuted, resting on the ℕ convention.** In `plus_9312`, `(0.5 · x² · y)^(1/3)` is refuted at x = 6, y = 8 in
  the exact reading, but `1/3` in ℕ is 0, which makes the statement trivial in Lean.
- **1 vacuous.** In `plus_4012`, `a 2 = a 1 + a 0 + 2` forces a 0 = −1 ∉ ℕ, in Lean as well.

## The full v4 rescan (2026-11-25, reader at introspect 51ff7fc)

All 3,451 statements (2,451 E/OPEN plus the 1,000 control) were re-read after the box began folding constant sides.
- **No refutation was lost.** All 106 earlier refutations stand.
- **New refutations:** only the 7 conditional sequence refutations listed above. One of them, `5663`, is in the
  control set; Lean proves it vacuously.
- **Translation:** 151 E/OPEN and 27 control statements now translate that did not before. One that translated
  before, `plus_36928`, now does not: a hypothesis became an unreadable series.

## The 7,168 statements whose proofs did not compile, 2026-11-25 (measured)

Only the statement matters to ZTL's reading. The 7,168 rows that were "not compiled" on our Mathlib, 24% of the
corpus and never judged before, were re-read with `sorry` in place of the proof (`corpora/benchmarks/
scan_statements.py`). The reader was the frozen code at introspect c064442 with ZTL 505bff2. Files:
`not_compiled_statements_rows.jsonl.gz`, and `not_compiled_flagged_reread.jsonl.gz` for the flagged rows re-read
after the fix below.

- **948 still do not compile, and 11 were not read**: the STATEMENT itself fails on our Mathlib.
- **6,137 translate**; 102 are EARNED by ZTL.
- **14 are refuted, all resting on the ℕ convention.** `x ^ (1 / 3)` with ℕ's 1/3 = 0 is a cube root in the
  exact reading. `1/6 + 1/10 + 1/8 ≥ 1/2` is 0 ≥ 0 in ℕ but false in ℚ (`lean_workbook_53456`). An auto-bound
  `abc` stands for a product. In every case the informal text decides what was meant.
- **5 are vacuous, each checked by hand.** These proofs did not compile on our Mathlib, so nothing is said about an
  accepted proof; the STATEMENTS are vacuous.
  - `plus_24332` and `plus_38408`: untyped variables were auto-bound to ℕ, so `x + y = 1` with x, y > 0 and
    `8abc ≤ 1` with a, b, c > 0 are impossible.
  - `plus_70503` assumes `logb 2 256 < logb 2 243`, which is false.
  - `plus_78160`: an even f with `f(2x) = 3 f x + x` gives 1 = −1 at x = ±1.
  - `plus_80224`: `f x = x²` and `2 f x = 3 f (1/x)` give 8 = 3/4 at x = 2.

**A fix found here.** A contradiction among the instances of a rule that depends on the point's other variables
(`f x = a x + b` at a = 7, b = 8) made the first version call the statement vacuous. The fix: vacuity is claimed only
when the facts and rules are free of the point (`zflseq.pointfree`). One NC row (`plus_14020`) and four miniF2F rows
lost the false label. The 17 Goedel sequence statements called vacuous above have no point variable in their rules,
except `plus_47435`, the one already left unclassified.


## Closing Verax's review (2026-11-25; Verax's answers of that night, both questions)

Verax's verdict: GO for research on a differential semantic audit; NO-GO for priority, accuracy or public counts
until the obligations below are met. This section records what each one became. No paper is planned (the
curator, 2026-11-25).

**One row per finding.** `../ledger.py` writes `../ledger.jsonl` and `../ledger_summary.md` from the files here and
runs nothing. Each row carries:
- the dataset and the id;
- whether the AI's proof compiled;
- the label in Verax's taxonomy, and the intent where the label is an exact-reading refutation;
- the witness and the existence premise;
- a statement hash, and a CLUSTER: identical translated mathematics shares one;
- the certificate status, and the source file.

**The numbers, reconciled.**
- **98 against 99.** The ℕ-convention class has 99 rows in `findings.jsonl`. The certificate run had taken 98; the
  missing one, `plus_78600`, was certified afterwards and was not closed by the tactics (rpow).
- **102 against 105.** There are 106 refutations, 7 + 99. 3 cannot be written as ℝ theorems (integer words), which
  leaves 103 attempts: 22 certified and 81 not closed. The 24.11 text's "22 of 102" lacked `plus_78600`.
- **Duplicates** (from the ledger):
  - the 100 exact-reading refutations are **82** distinct statements;
  - the 7 that are false in Lean too are **3** (the `abc` cluster has 4 copies);
  - the 23 vacuous are **16**.

**Labels, in place of the blanket "rests on the ℕ convention".**
- `FALSE_IN_LEAN`, `FALSE_IN_EXACT_READING` (plus `…_LEAN_UNREAD` when Lean's reading was not computed),
  `FALSE_FORMAL` and `COUNTEREXAMPLE_IF_SAT` (formerly "conditional").
- `VACUOUS`, `ADMISSIBILITY_UNKNOWN`, `UNDEFINED_ONLY_IN_ALTERNATE_READING` and `TRUE_EXACT_LEAN_VIA_CONVENTION`.
- Intent: `INTENDED_DISCRETE` when the informal text names a floor (1 row, the `2017 − 2017/3` false alarm), otherwise
  `INTENT_UNKNOWN` (113 rows). `SEMANTIC_MISMATCH_CONFIRMED` needs a human who did not write the translator, and it
  is never set automatically.

**Proofs.**
- "Proved by an AI from a contradiction" is withdrawn wherever it appeared. The statement is vacuous, and the proof
  terms were not inspected.
- The first layer's E means that a convention lemma is PRESENT in the proof term, not that it is necessary.
- The 14 refutations and 5 vacuous among the 7,168 non-compiling rows concern statements only.

**Existence of a sequence** is now a machine-checked premise, printed with every sequence refutation
(`existence_premise`): a forward recurrence (`zflseq.existence_by_recursion`) AND zero unchecked instances.
Verax's counterexample, `u 0 = 1, u 1 = 3, u (n+1) = 2 u n`, is a fixture: VACUOUS, never "existence: recursion".

**Re-read with the current code** (`rescan_v6_rows.jsonl.gz`: the sequence, function and integer-word sets, 273
statements). Sequence, function and word vacuities: 20.
- `plus_47435` is no longer vacuous: its rules depend on the point.
- `plus_66265` is newly vacuous: `∀ m n, m ≥ n ∧ …` is a conjunction, false at m = 0, n = 1. A two-index rule,
  readable since 2026-11-25; it is in the control set.

**Semantics, stated.** `z ≠ w` in ℂ is read as apartness in a real part, VR's reading, which classically is the same
as ¬(z = w). For an ∃ in an antecedent, `(∃x P) → C ⟺ ∀x (P → C)` holds classically and intuitionistically. ZTL
rejects one direction, but the tool uses only the direction ZTL accepts, so this is a divergence of semantics, not a
claim about Lean.

**Priority.** The classes are known: Ammanamanchi et al., Ground False / ProofNet-Verified, Anchor. Of the four
benchmark refutations, three were already public (see `../benchmarks/README.md`). We claim no first discovery.
