import Mathlib
set_option maxHeartbeats 400000

namespace ZTLCert

/-- lean_workbook_10014 (false_math_nat_convention) at {'v_b': '1', 'v_a': '0'} -/
theorem cert_0 : (((1:ℝ)  ≤  (1:ℝ))) ∧ (((0:ℝ)  ≤  ((2:ℝ) * (1:ℝ)))) ∧ ¬ (((((0:ℝ) -  (1:ℝ)) * ((0:ℝ) -  ((2:ℝ) * (1:ℝ))))  ≤  (0:ℝ))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

/-- lean_workbook_18626 (false_math_both_readings) at {'v_n': '0', 'v_x': '-1/3'} -/
theorem cert_2 : ¬ ((((Real.rpow (((1:ℝ) - ((-1:ℝ)/3))) ( ((1:ℝ) /  (((2:ℝ) * (0:ℝ)) -  (1:ℝ))))) + (Real.rpow (((1:ℝ) + ((-1:ℝ)/3))) ( ((1:ℝ) /  (((2:ℝ) * (0:ℝ)) -  (1:ℝ))))))  ≤  (2:ℝ))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

/-- lean_workbook_20895 (false_math_nat_convention) at {'v_m': '0', 'v_n': '0'} -/
theorem cert_4 : ¬ (((((0:ℝ) * (0:ℝ)) /  (((0:ℝ) + (0:ℝ)) + (1:ℝ)))  ≥  ((1:ℝ) /  (3:ℝ)))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

/-- lean_workbook_49433 (false_math_nat_convention) at {'v_x': '2', 'v_y': '2'} -/
theorem cert_22 : ¬ (((((1:ℝ) -  ((2:ℝ) * (2:ℝ)))  ≥  (0:ℝ))  ↔  ((((1:ℝ) -  ((2:ℝ) * (2:ℝ))) * (((2:ℝ) -  (2:ℝ))) ^ (2:ℕ))  ≥  (0:ℝ)))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

/-- lean_workbook_50834 (false_math_nat_convention) at {'v_x': '1', 'v_y': '-1'} -/
theorem cert_23 : ¬ (((Real.rpow (((((1:ℝ)) ^ (3:ℕ) + ((-1:ℝ)) ^ (3:ℕ)) / (2:ℝ))) ( ((1:ℝ) /  (3:ℝ))))  ≥  (Real.rpow (((((1:ℝ)) ^ (2:ℕ) + ((-1:ℝ)) ^ (2:ℕ)) / (2:ℝ))) ( ((1:ℝ) /  (2:ℝ)))))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

/-- lean_workbook_5147 (false_math_nat_convention) at {'v_n': '0'} -/
theorem cert_24 : ¬ (((((((1:ℝ) /  (3:ℝ)) * ((0:ℝ)) ^ (2:ℕ)) + (((1:ℝ) /  (2:ℝ)) * (0:ℝ))) + ((1:ℝ) /  (6:ℝ)))  ≥  (((((1:ℝ) /  (4:ℝ)) * ((0:ℝ)) ^ (2:ℕ)) + (((1:ℝ) /  (2:ℝ)) * (0:ℝ))) + ((1:ℝ) /  (4:ℝ))))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

/-- lean_workbook_plus_18676 (false_math_nat_convention) at {'v_m': '0', 'v_n': '0'} -/
theorem cert_34 : ¬ (((((0:ℝ) * (0:ℝ)) /  (((0:ℝ) + (0:ℝ)) + (1:ℝ)))  ≥  ((1:ℝ) /  (3:ℝ)))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

/-- lean_workbook_plus_20099 (false_math_nat_convention) at {'v_a': '0'} -/
theorem cert_35 : ¬ ((((((Real.rpow ((0:ℝ)) ( ((1:ℝ) /  (2:ℝ)))) - (1:ℝ))) ^ (2:ℕ) * (((4:ℝ) * (Real.rpow ((0:ℝ)) ( ((1:ℝ) /  (2:ℝ))))) - (1:ℝ)))  ≥  (0:ℝ))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

/-- lean_workbook_plus_26799 (false_math_nat_convention) at {'v_n': '0'} -/
theorem cert_42 : ¬ (((((((1:ℝ) /  (3:ℝ)) * ((0:ℝ)) ^ (2:ℕ)) + (((1:ℝ) /  (2:ℝ)) * (0:ℝ))) + ((1:ℝ) /  (6:ℝ)))  ≥  (((((1:ℝ) /  (4:ℝ)) * ((0:ℝ)) ^ (2:ℕ)) + (((1:ℝ) /  (2:ℝ)) * (0:ℝ))) + ((1:ℝ) /  (4:ℝ))))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

/-- lean_workbook_plus_26988 (false_math_nat_convention) at no variables -/
theorem cert_43 : (((0:ℝ) < (2017:ℝ))) ∧ ¬ ((((2017:ℝ) -  ((2017:ℝ) /  (3:ℝ)))  =  (1345:ℝ))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

/-- lean_workbook_plus_34539 (false_math_nat_convention) at no variables -/
theorem cert_52 : ¬ ((((((1:ℝ) /  (6:ℝ)) + ((1:ℝ) /  (10:ℝ))) + ((1:ℝ) /  (8:ℝ)))  ≥  ((1:ℝ) /  (2:ℝ)))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

/-- lean_workbook_plus_34696 (false_math_both_readings) at {'v_n': '0', 'v_x': '-1/3'} -/
theorem cert_53 : ¬ ((((Real.rpow (((1:ℝ) - ((-1:ℝ)/3))) ( ((1:ℝ) /  (((2:ℝ) * (0:ℝ)) -  (1:ℝ))))) + (Real.rpow (((1:ℝ) + ((-1:ℝ)/3))) ( ((1:ℝ) /  (((2:ℝ) * (0:ℝ)) -  (1:ℝ))))))  ≤  (2:ℝ))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

/-- lean_workbook_plus_35447 (false_math_nat_convention) at {'v_wa': '8', 'v_ha': '5', 'v_wb': '10', 'v_hb': '6', 'v_wc': '7', 'v_hc': '9', 'v_a': '5/4', 'v_b': '4/3', 'v_c': '2/3'} -/
theorem cert_54 : (((((5:ℝ)/4) > (0:ℝ))  ∧  ((((4:ℝ)/3) > (0:ℝ))  ∧  ((((2:ℝ)/3) > (0:ℝ))  ∧  (((((5:ℝ)/4) + ((4:ℝ)/3)) > ((2:ℝ)/3))  ∧  (((((5:ℝ)/4) + ((2:ℝ)/3)) > ((4:ℝ)/3))  ∧  ((((4:ℝ)/3) + ((2:ℝ)/3)) > ((5:ℝ)/4)))))))) ∧ ¬ (((((((8:ℝ) /  (5:ℝ)) + ((5:ℝ) /  (8:ℝ))) * (((10:ℝ) /  (6:ℝ)) + ((6:ℝ) /  (10:ℝ)))) * (((7:ℝ) /  (9:ℝ)) + ((9:ℝ) /  (7:ℝ))))  ≥  ((((8:ℝ) /  (9:ℝ)) * ((((8:ℝ) /  (5:ℝ)) + ((10:ℝ) /  (6:ℝ))) + ((7:ℝ) /  (9:ℝ)))) * ((((5:ℝ) /  (8:ℝ)) + ((6:ℝ) /  (6:ℝ))) + ((9:ℝ) /  (7:ℝ)))))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

/-- lean_workbook_plus_4042 (false_math_both_readings) at no variables -/
theorem cert_58 : ¬ (((((((3:ℝ) /  (4:ℝ))) ^ (3:ℕ) * (((1:ℝ) /  (4:ℝ))) ^ (2:ℕ)) /  ((((2:ℝ)) ^ (5:ℕ) /  ((4:ℝ)) ^ (5:ℕ)) + ((((3:ℝ) /  (4:ℝ)) * (((1:ℝ) /  (4:ℝ))) ^ (2:ℕ)) * (((3:ℝ) /  (4:ℝ))) ^ (3:ℕ))))  =  ((27:ℝ) /  (59:ℝ)))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

/-- lean_workbook_plus_42947 (false_math_nat_convention) at no variables -/
theorem cert_60 : ¬ ((((((((2:ℝ)) ^ (4:ℕ) /  ((3:ℝ)) ^ (4:ℕ)) * (((3:ℝ)) ^ (4:ℕ) -  ((2:ℝ)) ^ (4:ℕ))) /  (((3:ℝ)) ^ (4:ℕ) -  (1:ℝ))) * (2:ℝ))  =  ((((2:ℝ)) ^ (4:ℕ) * (((3:ℝ)) ^ (4:ℕ) -  ((2:ℝ)) ^ (4:ℕ))) /  (((3:ℝ)) ^ (4:ℕ) * (((3:ℝ)) ^ (4:ℕ) -  (1:ℝ)))))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

/-- lean_workbook_plus_47031 (false_math_nat_convention) at {'v_n': '0'} -/
theorem cert_67 : ¬ ((((0:ℝ)  ≤  ((1:ℝ) /  ((((0:ℝ)) ^ (2:ℕ) + (0:ℝ)) + (2:ℝ))))  ∧  (((1:ℝ) /  ((((0:ℝ)) ^ (2:ℕ) + (0:ℝ)) + (2:ℝ)))  ≤  ((1:ℝ) /  (4:ℝ))))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

/-- lean_workbook_plus_48269 (false_math_nat_convention) at {'v_x': '-4'} -/
theorem cert_70 : ¬ ((((((((9:ℝ) /  (10:ℝ))) ^ (7:ℕ) * (((4:ℝ) /  (3:ℝ))) ^ (9:ℕ)) * (((3:ℝ) /  (5:ℝ))) ^ (6:ℕ)) * (((5:ℝ) /  (6:ℝ))) ^ (11:ℕ))  =  ((1:ℝ) /  (125:ℝ)))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

/-- lean_workbook_plus_65826 (false_math_nat_convention) at {'v_x': '1', 'v_y': '-1'} -/
theorem cert_84 : ¬ (((Real.rpow (((((1:ℝ)) ^ (3:ℕ) + ((-1:ℝ)) ^ (3:ℕ)) / (2:ℝ))) ( ((1:ℝ) /  (3:ℝ))))  ≥  (Real.rpow (((((1:ℝ)) ^ (2:ℕ) + ((-1:ℝ)) ^ (2:ℕ)) / (2:ℝ))) ( ((1:ℝ) /  (2:ℝ)))))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

/-- lean_workbook_plus_69526 (false_math_nat_convention) at {'v_x': '1', 'v_y': '3'} -/
theorem cert_88 : ¬ (((((((1:ℝ) -  (3:ℝ))) ^ (2:ℕ) * ((((((((((((1:ℝ)) ^ (4:ℕ) * ((3:ℝ)) ^ (2:ℕ)) -  (((6:ℝ) * ((1:ℝ)) ^ (3:ℕ)) * ((3:ℝ)) ^ (3:ℕ))) -  (((6:ℝ) * ((1:ℝ)) ^ (3:ℕ)) * (3:ℝ))) + (((12:ℝ) * ((1:ℝ)) ^ (2:ℕ)) * ((3:ℝ)) ^ (2:ℕ))) + ((9:ℝ) * ((1:ℝ)) ^ (2:ℕ))) + (((1:ℝ)) ^ (2:ℕ) * ((3:ℝ)) ^ (4:ℕ))) -  (((6:ℝ) * (1:ℝ)) * (3:ℝ))) -  (((6:ℝ) * (1:ℝ)) * ((3:ℝ)) ^ (3:ℕ))) + (8:ℝ)) + ((9:ℝ) * ((3:ℝ)) ^ (2:ℕ)))) /  (((1:ℝ) + ((1:ℝ) * (3:ℝ)))) ^ (2:ℕ))  ≥  (0:ℝ))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

/-- lean_workbook_plus_72738 (false_math_nat_convention) at {'v_x': '2', 'v_y': '2'} -/
theorem cert_90 : ¬ (((((1:ℝ) -  ((2:ℝ) * (2:ℝ)))  ≥  (0:ℝ))  ↔  ((((1:ℝ) -  ((2:ℝ) * (2:ℝ))) * (((2:ℝ) -  (2:ℝ))) ^ (2:ℕ))  ≥  (0:ℝ)))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

/-- lean_workbook_plus_72886 (false_math_nat_convention) at {'v_n': '0'} -/
theorem cert_91 : ¬ (((((Real.rpow ((((0:ℝ)) ^ (3:ℕ) + (3:ℝ))) ( ((1:ℝ) /  (3:ℝ)))) -  (0:ℝ)) -  ((Real.rpow ((((0:ℝ)) ^ (4:ℕ) + ((4:ℝ) * (0:ℝ)))) ( ((1:ℝ) /  (4:ℝ)))) -  (0:ℝ)))  =  (0:ℝ))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

/-- lean_workbook_plus_76820 (false_math_nat_convention) at {'v_x': '-4'} -/
theorem cert_94 : ¬ (((((1:ℝ) /  (21:ℝ)) + ((1:ℝ) /  (22:ℝ)))  =  ((1:ℝ) /  (462:ℝ)))) := by
  first | norm_num | (norm_num; done) | (constructor <;> norm_num) | (refine ⟨?_, ?_⟩ <;> norm_num) | (simp; norm_num) | (norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done) | (constructor <;> (try norm_num) <;> positivity) | (norm_num <;> nlinarith [Real.pi_gt_three])

end ZTLCert
