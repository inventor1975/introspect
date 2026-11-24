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

**Lean kernel certificates:** of 102 refutations that could be written as ℝ theorems, **22** are closed by tactics
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
- **Contradictory in BOTH readings: 11.** Goedel-Prover's proof derives the conclusion from contradictory
  hypotheses.
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
