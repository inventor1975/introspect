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

## Finite sums, 2026-11-25 (measured)

`Finset.sum` / `Finset.prod` over an interval (`range`, `Icc`, `Ico`, `Ioc`, `Ioo`) now translate to `fsum` / `fprod`.
zflread reads them exactly: it writes out a concrete interval term by term, and it uses closed forms for Σ P(i) r^i
over a variable bound (Faulhaber; the telescoping form for r ≠ 1). The closed form needs the guard hi ≥ lo − 1, and
the floor decides that guard on the box. ZTL got an exact polynomial-identity path, needed for Faulhaber's cubics,
which its parabola reading had left OPEN.

The fixtures pass: Gauss 5050, Σ i², Σ 2^i, 5! = 120, and two refutations (Σ (2i+1) = n² + 1 at n = 0; Σ i/2^i ≤ 1 at
n = 3).

**On the corpora the gain is zero:**
- **Lean Workbook:** of 44 statements with `∑`/`∏`, none became readable. Every one sums a family of variables
  (`a : Fin n → ℝ`), or ranges over a `Finset`, a matrix or a type.
- **PutnamBench:** none of the 11 statements that `Finset.sum` had blocked became readable. Each now stops at the
  next blocker: a sum over a non-interval set, a body where the bound appears (`choose n r`, `n^i / i!`), `floor`,
  or a function.

The next boundary is function variables, not finite sums.

## The benchmarks re-read with the 2026-11-25 reader (measured)

The reader is the frozen code at introspect c064442 with ZTL 505bff2, plus the point-free vacuity fix. Rows are in
`*_rows_v5.jsonl.gz`.

| benchmark | translated before → now | refuted at an admissible point |
|---|---|---|
| miniF2F (488) | 267 → 362 | 3 |
| ProofNet (371) | 9 → 17 | 2 |
| PutnamBench (672) | 13 → 39 | 0 |

**Four new refutations, each certified by Lean's kernel** in `Certificates_benchmarks_20261125.lean` (the negation
of the statement as formalized, closed by tactics, no `sorry`):
- **miniF2F `mathd_numbertheory_618`.** `p x = x² − x + 41` and `1 < gcd(p n, p(n+1))` ⊢ `41 ≤ n` fails at n = 0:
  gcd(41, 41) = 41. The informal "smallest positive n" lost "positive". `[propext, Quot.sound]`.
- **miniF2F `amc12a_2020_p13`.** The exponents `1 / c`, `1 / b`, `1 / a`, `1 / 36` are ℕ divisions, all 0, so at
  n = 0 the hypothesis holds for every a, b, c and `b = 3` does not follow. DeepSeek-V1.5's jsonl; other versions use
  real exponents.
- **ProofNet `exercise_1_2`.** `(−1/2 + (√3/2) i)^3 = −1` is false: the cube is 1. Axler's exercise asks for a cube
  root of 1.
- **ProofNet `exercise_4_11`.** `(s := ∑ n : Fin p, n ^ k)` is a DEFAULT ARGUMENT, so s is arbitrary; at p = 7, k = 2
  and s = 6 the statement fails. Lean warns that the first `s` is unused.

Whether these are already listed in the benchmarks' errata was not checked. The earlier miniF2F refutation
(`algebra_ineq_nto1onlt2m1on`) stands. PutnamBench remains almost entirely out of reach: 39 of 672 translate.
