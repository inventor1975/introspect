# lean2zfl over Goedel-Prover's Lean Workbook proofs — the run of 2026-11-24

What `lean2zfl` said about **29,750 AI-found Lean 4 proofs**, and what ZTL's numeric floor said about the mathematics
of their statements. These files are the evidence for the counts below. The dataset itself is not copied here.

## Sources

- Proofs: Hugging Face `Goedel-LM/Lean-workbook-proofs`, 29,750 rows (`problem_id`, `full_proof`), MIT licence.
  The informal statement is taken from the comment inside each proof.
- Problems: Hugging Face `internlm/Lean-Workbook` (Lean Workbook and Lean Workbook Plus), Apache-2.0.
- Elaborated with Lean 4 v4.29.1 and Mathlib v4.29.1, in a Lake project of our own (`LEAN2ZFL_PROJECT`).
- The tools: this repository at the commits of the run (`lean2zfl` 9947124 / c86913e), and inventor1975/ZTL 365cfde.

## Files

| file | what |
|---|---|
| `scan_goedel.py` | The scan. `python3 scan_goedel.py OUT N BATCH PARALLEL`. `SCAN_IDS=<file>` selects a subset. `GOEDEL_PARQUET`, `LEAN2ZFL_PROJECT` and `LEAN2ZFL_DUMPER` are paths. |
| `full_rows.jsonl.gz` | All 29,750 rows: lean2zfl's disposition per theorem and why. |
| `ids_e_open.txt`, `ztl_e_open_rows.jsonl.gz` | The 2,451 E / OPEN / IF STABLE theorems, with ZTL's reading (`ztl`). |
| `ids_control_earned.txt`, `ztl_control_rows.jsonl.gz` | The control: 1,000 EARNED theorems, randomly drawn (seed 20261124), with ZTL's reading. |
| `findings.jsonl` | The classified readings below, one per line: statement, ZFL claim, box, witness, informal text. |

## The counts

**lean2zfl's dispositions over the 29,750 proofs:**

| EARNED | not compiled on our Mathlib | OPEN | E | EARNED IF STABLE | not read |
|---|---|---|---|---|---|
| 20,116 | 7,168 | 1,492 | 915 | 44 | 15 |

**ZTL's reading of the 2,451 E / OPEN / IF STABLE theorems** (`findings.jsonl`, field `class`):

| class | count | meaning |
|---|---|---|
| `false_math_both_readings` | 9 | A point satisfies every translated hypothesis and refutes the conclusion, both in the exact reading and in Lean's ℕ convention. |
| `false_math_nat_convention` | 101 | The conclusion is refuted in the exact reading of ℕ's `/` and `−`; Lean's convention (floor, truncation) holds there. Whether the author meant the floor is a question for the informal text: `lean_workbook_plus_26988` (⌊2017/3⌋) is such a case. |
| `true_math_lean_via_convention` | 112 | lean2zfl said E (a convention was used), yet ZTL proves the exact mathematics. |
| `no_value_at_admissible_point` | 270 | At an admissible point an operation has no value, for example `x / 0` with no `x ≠ 0` hypothesis. |

Untranslated: 470 (`∃` 186, function variables about 150, `tsum` 41, `ℂ` 21, and others).

**Control:** of the 1,000 EARNED theorems, 0 got a counterexample.

## Limits

- **24% did not compile.** Our Mathlib renamed lemmas the proofs use. Those 7,168 are not judged at all.
- **The box drops some hypotheses.** It uses only hypotheses that bound one variable by a constant, so an OPEN may
  belong to the box and not to the statement. A counterexample is accepted only at a point where every translated
  hypothesis holds; with an untranslated hypothesis, the search is skipped.
- **The exact reading is ours.** An auto-bound variable meant as a product (`abc`), an intended floor, or `n = 0`
  excluded only in words can make a "false" statement the author's correct one. The class says which reading
  refuted it; the informal text decides what was meant.
