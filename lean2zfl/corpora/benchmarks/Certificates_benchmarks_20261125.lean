import Mathlib

/-! Lean kernel certificates for four benchmark statements that ZTL's reading refuted (2026-11-25).
Each theorem is the NEGATION of the statement as formalized, closed at the point the reader found. -/

-- miniF2F mathd_numbertheory_618 at n = 0, p x = x² − x + 41: gcd(p 0, p 1) = 41 > 1, yet 41 ≤ 0 fails
theorem cert_mathd_numbertheory_618 :
    ¬ ∀ (n : ℕ) (p : ℕ → ℕ), (∀ x, p x = x ^ 2 - x + 41) → 1 < Nat.gcd (p n) (p (n + 1)) → 41 ≤ n := by
  intro h
  have := h 0 (fun x => x ^ 2 - x + 41) (fun _ => rfl) (by decide)
  omega

-- miniF2F amc12a_2020_p13 at a = 4, b = 8, c = 5, n = 0: the ℕ exponents 1/c, 1/b, 1/a, 1/36 are all 0
theorem cert_amc12a_2020_p13 :
    ¬ ∀ (a b c : ℕ) (n : NNReal), n ≠ 1 → (1 < a ∧ 1 < b ∧ 1 < c) →
      (n * (n * n ^ (1 / c)) ^ (1 / b)) ^ (1 / a) = (n ^ 25) ^ (1 / 36) → b = 3 := by
  intro h
  have := h 4 8 5 0 (by norm_num) (by norm_num) (by norm_num)
  omega

-- ProofNet exercise_1_2: (−1/2 + (√3/2) i)³ is 1, not −1 (the real part)
theorem cert_exercise_1_2 : ¬ ((⟨-1/2, Real.sqrt 3 / 2⟩ : ℂ) ^ 3 = -1) := by
  intro h
  have h3 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hre := congrArg Complex.re h
  simp [pow_succ, Complex.mul_re, Complex.mul_im] at hre
  nlinarith [h3]

-- ProofNet exercise_4_11: `(s := …)` is a default argument, so s is arbitrary; p = 7, k = 2, s = 6
theorem cert_exercise_4_11 :
    ¬ ∀ {p : ℕ}, p.Prime → ∀ (k s : ℕ) (s : ℕ := ∑ n : Fin p, (n : ℕ) ^ k),
      ((¬ p - 1 ∣ k) → s ≡ 0 [MOD p]) ∧ (p - 1 ∣ k → s ≡ 0 [MOD p]) := by
  intro h
  have := (h (p := 7) (by norm_num) 2 7 6).1 (by decide)
  revert this; decide

#print axioms cert_mathd_numbertheory_618
#print axioms cert_amc12a_2020_p13
#print axioms cert_exercise_1_2
#print axioms cert_exercise_4_11
