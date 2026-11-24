import Mathlib
set_option maxHeartbeats 400000

namespace ZTLCert

/-- algebra_ineq_nto1onlt2m1on (false_math_both_readings) at {'v_n': '1'} -/
theorem cert_0 : ¬ (((Real.rpow ((1:ℝ)) ( ((1:ℝ) / (1:ℝ)))) < ((2:ℝ) - ((1:ℝ) / (1:ℝ))))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

end ZTLCert
