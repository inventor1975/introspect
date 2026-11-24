import Mathlib
/-! zflread fixtures: a Lean statement READ BY ZTL's numeric floor. Each theorem's expected reading is in its comment:
`ZTL <disposition>` for the conclusion over the box, `WITNESS refuted` / `WITNESS none` for the point search,
`UNTR` for a statement with no ZFL word. `sorry` is fine here: what is read is the statement, not the proof. -/

namespace ZFLReadFix

-- ZTL EARNED: 0 < x ≤ 2 is the box (0, 2]; ln is defined on all of it (the strict bound) and ln 2 < 1
theorem t_log (x : ℝ) (hx : 0 < x) (h2 : x ≤ 2) : Real.log x ≤ 1 := by sorry

-- ZTL REFUTED: ℕ's 7 / 2 is 3, the mathematics' 7/2 is not
theorem t_nat : (7 : ℕ) / 2 = 3 := by norm_num

-- WITNESS refuted: ℕ's 1 / 3 is 0 (Lean: a ^ 0 = 1); the cube root of 1/4 is not 1
theorem t_cube (a : ℝ) (ha : 0 < a) : a ^ ((1:ℕ) / 3) = 1 := by sorry

-- WITNESS none: TRUE for every b ≠ 0 — no point may refute it (the other side of the bracket)
theorem t_div (a b : ℝ) (hb : b ≠ 0) : a / b * b = a := by sorry

-- ZTL EARNED: x^2 - 2x + 1 = (x - 1)^2 >= 0 on the whole line, read exactly
theorem t_pow (x : ℝ) : x ^ 2 - 2 * x + 1 ≥ 0 := by nlinarith [sq_nonneg (x - 1)]

-- ZTL EARNED: 0 < n in ℕ reads n >= 1, so 1/n > 0
theorem t_cast (n : ℕ) (h : 0 < n) : (1 : ℝ) / n > 0 := by positivity

-- ZTL EARNED: a leading ∃ — a witness is exhibited (x = 1 or any positive point)
theorem t_ex : ∃ x : ℝ, x > 0 := ⟨1, one_pos⟩

-- WITNESS none: the triangle inequality is true, |a| read as max(a, -a)
theorem t_abs (x y : ℝ) : |x + y| ≤ |x| + |y| := by sorry

-- ZTL REFUTED: 1/21 + 1/22 is 43/462 (Lean_workbook_plus_76820's shape: ℕ makes both sides 0)
theorem t_sum : (1 : ℕ) / 21 + 1 / 22 = 1 / 462 := by norm_num

-- ZTL EARNED: an inner ∀ in a positive place joins the box: for every y, y^2 + 1 > 0
theorem t_inner_all (x : ℝ) (hx : 0 < x) : x > 0 ∧ ∀ y : ℝ, y ^ 2 + 1 > 0 := by sorry

-- WITNESS refuted: an inner ∀ that is false — some y has y^2 < 1 (e.g. y = 1/2)
theorem t_inner_false : ∀ y : ℝ, 0 < y → y ^ 2 ≥ 1 := by sorry

-- UNTR: a ∀ on the left of → INSIDE the conclusion is an ∃ in disguise (at the top, Lean makes it a hypothesis)
theorem t_inner_neg (x : ℝ) : x > 0 ∧ ((∀ y : ℝ, y ≤ x) → x > 1) := by sorry

-- UNTR: ¬¬∀ is not positive here — classical ¬¬p = p falls in ZTL on a marked atom
theorem t_notnot_all : ¬¬ (∀ y : ℝ, y ^ 2 ≥ 0) := by sorry

-- ZTL EARNED: x > 1 and n a natural: x ^ n >= 1 for every n (the power over the exponent's integer range)
theorem t_npow (x : ℝ) (n : ℕ) (hx : 1 < x) : x ^ n ≥ 1 := by sorry

-- WITNESS refuted: 2 ^ n >= n + 2 fails at n = 0 (1 >= 2)
theorem t_npow_false (n : ℕ) : 2 ^ n ≥ n + 2 := by sorry

-- NATCONV: the mathematics (exact /) is refuted, Lean's floor holds — the author's ⌊2017/3⌋ (lean_workbook_plus_26988)
theorem t_floor_conv : (2017 : ℕ) - 2017 / 3 = 1345 := by norm_num

-- ZTL EARNED: the integer words, read as VR defines them (VR/Numbers/Division.lean)
theorem t_mod : (7 : ℕ) % 3 = 1 := by norm_num

-- ZTL EARNED: a witnessed divisibility
theorem t_dvd : (3 : ℕ) ∣ 12 := by norm_num

-- ZTL EARNED: C(10, 3)
theorem t_choose : Nat.choose 10 3 = 120 := by decide

-- ZTL EARNED: 5!
theorem t_fact : Nat.factorial 5 = 120 := by decide

-- ZTL EARNED: 17 ≡ 2 [MOD 5] is 5 ∣ 17 - 2
theorem t_modeq : 17 ≡ 2 [MOD 5] := by decide

-- WITNESS refuted: 3 ∣ n is false at n = 1
theorem t_dvd_false (n : ℕ) : 3 ∣ n := by sorry

-- VACUOUS: the hypothesis IS the conclusion and both are false mathematics — the statement is vacuously true, not a
-- refutation (lean_workbook_53067's shape)
theorem t_vacuous (h : (1 : ℕ) / 3 * 3 = 1) : (1 : ℕ) / 3 * 3 = 1 := h

-- ZTL REFUTED: ∃ x, x^2 < 0 — no witness anywhere: refuted over the whole box
theorem t_ex_false : ∃ x : ℝ, x ^ 2 + 1 < 0 := by sorry

-- WITNESS none: an ∃ whose conclusion fails at many points is NOT refuted by one of them (x = 3 works)
theorem t_ex_somewhere : ∃ x : ℕ, x * x = 9 := ⟨3, rfl⟩

-- UNTR: an ∃ under a connective
theorem t_ex_inner (y : ℝ) : y = y ∧ ∃ x : ℝ, x > y := by sorry

end ZFLReadFix
