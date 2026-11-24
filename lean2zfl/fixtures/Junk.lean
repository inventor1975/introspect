import Mathlib
/-! lean2zfl fixtures: one theorem per disposition (the expected one in the comment). Needs Mathlib. -/

namespace L2ZFix

-- EXPECT EARNED: no operation with a junk branch
theorem plain_ok : (2 : ℝ) + 2 = 4 := by norm_num

-- EXPECT EARNED: the division is guarded by b ≠ 0
theorem div_guarded (a b : ℝ) (hb : b ≠ 0) : a / b * b = a := div_mul_cancel₀ a hb

-- EXPECT OPEN: 0 ≤ r < 1 does make the series summable, but no hypothesis SAYS Summable (nor 1 - r ≠ 0):
-- v1 reads guards from the hypotheses only, so it cannot see this, and says it does not know
theorem geom_guarded (r : ℝ) (h0 : 0 ≤ r) (h1 : r < 1) : ∑' n : ℕ, r ^ n = (1 - r)⁻¹ :=
  tsum_geometric_of_lt_one h0 h1

-- EXPECT E: "1 + 2 + 3 + … = 0" — true of Mathlib's convention (a non-summable series sums to 0), not of a sum
theorem nat_sum_is_zero : ∑' n : ℕ, (n : ℝ) = 0 := by
  apply tsum_eq_zero_of_not_summable
  intro h
  have := (h.tendsto_atTop_zero).eventually (gt_mem_nhds (show (0:ℝ) < 1 by norm_num))
  obtain ⟨N, hN⟩ := Filter.eventually_atTop.mp this
  have := hN (N + 1) (by omega); push_cast at this; linarith

-- EXPECT E: x / 0 = 0 is the convention itself
theorem div_by_zero (a : ℝ) : a / 0 = 0 := div_zero a

-- EXPECT EARNED IF STABLE: true whatever a / b is, provided it is ONE value at both occurrences (no b ≠ 0)
theorem same_quotient (a b : ℝ) : a / b - a / b = 0 := sub_self _

-- EXPECT OPEN: an unguarded ℕ-subtraction, and no junk lemma in the proof (n - m might be the truncation)
theorem nat_sub_open (n m : ℕ) : n - m + m ≥ m := Nat.le_add_left m (n - m)

-- EXPECT ON CREDIT: a clean statement whose proof is a `sorry` (the axiom sorryAx is named)
theorem on_credit_sorry : (3 : ℝ) * 3 = 9 := by sorry

-- EXPECT EARNED: no hypothesis says ↑k + 1 ≠ 0 in ℂ, but the dumper PROVES it (positivity fails in ℂ; the cast
-- to ℕ and omega do) — a guard by proof, checked to contain no sorry
theorem cplx_den (k : ℕ) : (1 : ℂ) / ((k : ℂ) + 1) * ((k : ℂ) + 1) = 1 :=
  div_mul_cancel₀ (1 : ℂ) (Nat.cast_add_one_ne_zero k)

-- EXPECT EARNED: √x twice, guarded by PROOF — positivity uses the hypothesis 0 < x for both 0 ≤ x and √x ≠ 0
theorem sqrt_guarded_by_hyp (x : ℝ) (hx : 0 < x) : (1 / Real.sqrt x) * Real.sqrt x = 1 := by
  rw [one_div, inv_mul_cancel₀ (Real.sqrt_pos.mpr hx).ne']

-- EXPECT OPEN: `1 / f 1` twice and unguarded — `f 1 ≠ 0` follows from the ∀-hypothesis, which no dump-time tactic
-- uses — and the statement holds only for the term's real value (0 would give 0 = 2): a repeated term is NOT "true
-- if stable" (KS23.unit_of's shape)
theorem repeated_not_general (f : ℝ → ℝ) (hf : ∀ y, 0 < f y) : 1 / f 1 * f 1 + 1 / f 1 * f 1 = 2 := by
  have h := (hf 1).ne'
  rw [one_div_mul_cancel h]; norm_num

-- EXPECT E: log of a negative is Mathlib's convention (log x = log |x|): the hypothesis x < 0 PROVES the argument is at
-- a convention point, and no junk branch of the definition is even taken (Real.exp_log_of_neg's shape)
theorem log_of_negative (x : ℝ) (hx : x < 0) : Real.exp (Real.log x) = -x := Real.exp_log_of_neg hx

-- EXPECT E: log 0 = 0 is the convention itself, proved by unfolding the definition (no junk LEMMA in the proof)
theorem log_at_zero : Real.log 0 = 0 := by simp [Real.log]

end L2ZFix
