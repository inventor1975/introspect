# Calibration on benchmarks others have audited — 2026-11-24

lean2zfl was also run on the STATEMENTS of two benchmarks audited by others: miniF2F (488) and ProofNet (371), in
DeepSeek-Prover-V1.5's jsonl (MIT). Every proof was replaced by `sorry`; `scan_statements.py` is the scanner.
ZTL's reading is "v3" (see `../goedel/README.md`).

| benchmark | statements | not compiled | ZTL refutations at an admissible point |
|---|---|---|---|
| miniF2F | 488 | 65 | 1: `algebra_ineq_nto1onlt2m1on` (`Certificates_minif2f.lean`, kernel-certified) |
| ProofNet | 371 | 164 | 0 (mostly untranslated: abstract algebra and analysis) |
| PutnamBench (trishullab, Apache-2.0, Lean v4.33 read on our v4.29) | 672 | 14 | 0 — 644 (96%) untranslated: functions as variables ~120, general types 27, ∃ 37, sets 16, Euclidean plane 14, `Finset.sum` 10, polynomials 9, limits 9 |

**Where the instrument works, and where it does not (measured).** It reads computational and olympiad mathematics:
Lean Workbook's ℕ conventions, series and logarithms. It cannot read Putnam or Mathlib's general theory, where almost
every statement quantifies over functions, sets or types. That is the boundary of ZTL's numeric floor, and partly
VR's: a quantifier over all functions ℝ → ℝ does not range over a box. Mathlib's series and zeta modules
(`../mathlib/`) have 109 theorems that mention `∑'`. Five are concrete enough to read (geometric series); the rest
range over any type `ι` and any `f`. The first layer still maps them: seven theorems there are proved through the
convention "a divergent sum is 0" (`tsum_mem`, `tendsto_sum_nat_add`, and others). That is Mathlib's design, not an
error.

**The one refutation is already known.** The formal statement has a strict `<` and no hypothesis `0 < n`; the informal
statement says `≤` and "n positive". At n = 1 the formal statement reads `1 < 1`. DeepSeek-Prover-V2's miniF2F has
`≤`, and miniF2F-rocq's `audit.txt` lists the problem.

**What we do NOT see, by design.** Rajasekaran's refutation of `aime_1984_p5` takes a = −64, b = 8: the hypotheses
`log₈ a + log₄ b² = 5` and `log₈ b + log₄ a² = 7` hold only because Mathlib's `log` reads `log x = log |x|`. In the
exact mathematics the logarithm of a negative number has no value. The hypotheses cannot hold there, so lean2zfl
reports OPEN. Their tools answer "is the Lean statement false in Lean's semantics?"; this one answers "is the
mathematics the statement writes false?". The findings complement each other rather than overlap.

## Prior art read (2026-11-24)

- **Rajasekaran, "A Guard-Aware Junk-Value Linter for Lean 4"** (NeurIPS 2026 MATH-AI). A statement-only linter
  with a 1,056-declaration registry. Its counterexamples came from agent review, each with a Lean check.
- **Ammanamanchi, Bhat, Biderman, "Faults in our formal benchmarking"** (ICML 2026; arXiv 2606.29493, code at
  Shashi456/atp-checkers). It already **searches for counterexamples automatically**: a `decide` sweep over small
  ℕ/ℤ values plus Plausible random testing, in Lean's own semantics (2/0 = 0, truncating subtraction), with no reals.
  Lean Workbook was not audited.
- **FormalRx** (arXiv 2607.04655): an LLM diagnoser. Lean is used to compile only.
- **An et al., "Ground False"**: abstracts only (OpenReview blocked us). Errors are confirmed by proving the negation;
  how those proofs were found was not visible to us.

What may be ours, unconfirmed:
- counterexamples to the **exact** mathematical reading (ℚ points, partial functions, a box from the hypotheses);
- reading ℕ's conventions **twice**, so a refutation that rests on them is labelled as such;
- convention lemmas found **inside AI proof terms**, on Lean Workbook through Goedel-Prover's proofs.
