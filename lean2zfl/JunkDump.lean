/-! lean2zfl's dumper (appended to a COPY of the analysed file by lean2zfl.py; the analysed file itself is untouched).

For every theorem declared in this file: (1) every FULL application in its STATEMENT of an operation with a junk
branch — a total function that returns a conventional value outside its domain: tsum of a non-summable series,
x / 0, 0⁻¹, √ of a negative, log of 0 or of a negative, ℕ-subtraction below zero, ζ at 1 — with its carrier type and
its explicit arguments; (2) its hypotheses (the Prop binders), the candidates that close a junk branch; (3) the junk
LEMMAS its proof term uses directly; (4) the axioms it depends on; (5) its line. One JSON object per theorem, each on
a line starting with `LEAN2ZFL `. Facts are read from the ELABORATED environment, never from source text.
Needs Mathlib in the project (the junk lemmas are Mathlib's). -/

namespace Lean2ZFL
open Lean Meta Elab Command Term

def junkOps : Array Name := #[`tsum, `HDiv.hDiv, `Inv.inv, `Real.sqrt, `Real.log, `HSub.hSub, `riemannZeta]

def junkLemmas : Array Name := #[`tsum_eq_zero_of_not_summable, `div_zero, `inv_zero, `Real.sqrt_eq_zero_of_nonpos,
  `Real.log_zero, `Real.log_neg_eq_log, `Nat.sub_eq_zero_of_le, `tsub_eq_zero_of_le, `Nat.div_zero,
  `Int.ediv_zero, `riemannZeta_one]

/-- arity of a FULL application of each junk operation -/
def junkArity : Name → Nat
  | `tsum => 5 | `HDiv.hDiv => 6 | `Inv.inv => 3 | `Real.sqrt => 1 | `Real.log => 1 | `HSub.hSub => 6
  | `riemannZeta => 1 | _ => 0

/-- every FULL application of a junk operation, outermost first (a partial application is not an occurrence) -/
partial def junkApps (e : Expr) (acc : Array Expr := #[]) : Array Expr :=
  match e.getAppFn with
  | .const n _ =>
    if junkOps.contains n && e.getAppNumArgs ≥ junkArity n then
      e.getAppArgs.foldl (fun acc a => junkApps a acc) (acc.push e)
    else if e.isApp then
      e.getAppArgs.foldl (fun acc a => junkApps a acc) acc
    else acc
  | _ =>
    match e with
    | .app f a => junkApps a (junkApps f acc)
    | .lam _ t b _ => junkApps b (junkApps t acc)
    | .forallE _ t b _ => junkApps b (junkApps t acc)
    | .letE _ t v b _ => junkApps b (junkApps v (junkApps t acc))
    | .mdata _ b => junkApps b acc
    | .proj _ _ b => junkApps b acc
    | _ => acc

def ppOrRaw (e : Expr) : MetaM String := do
  if e.hasLooseBVars then return s!"{e}" else return s!"{← ppExpr e}"

/-- the explicit value arguments of a junk application (the last ones), pretty-printed -/
def valueArgs (a : Expr) : MetaM (Array Json) := do
  let op := a.getAppFn.constName!
  let k : Nat := match op with
    | `HDiv.hDiv => 2 | `HSub.hSub => 2 | `Inv.inv => 1 | `tsum => 1 | _ => 1
  let args := a.getAppArgs
  let start := if op == `tsum then 4 else args.size - k
  let mut out := #[]
  for i in [start:min args.size (start + k)] do
    out := out.push (Json.str (← ppOrRaw args[i]!))
  return out

/-- Every alternative must CLOSE the goal: `norm_num` alone may only simplify it, and `first` would stop there (an
"unsolved goals" that reads as a failed guard). MEASURED 2026-11-24 on ℂ denominators `↑k + 1`, `2 * ↑k + 1`,
`↑(2 * k)!` (now proved) and on `x ≠ 0` for an arbitrary `x` (correctly NOT proved); `-↑k ≠ 1` (ζ at a negative
integer) is not proved by these: such an occurrence stays OPEN.
Try to PROVE a goal with a tactic given as text (parsed at run time against the current environment, so the
dumper compiles without Mathlib and uses Mathlib's tactics when they are there). A small heartbeat budget. -/
def proves (goal : Expr) (tac : String) : TermElabM Bool := do
  match Parser.runParserCategory (← getEnv) `tactic tac with
  | .error _ => return false
  | .ok stx =>
    let g ← mkFreshExprMVar goal
    try
      -- NO ERROR RECOVERY (MEASURED 2026-11-24): with it, a failing tactic is logged and the goal is closed by
      -- `sorryAx`, which read as a PROVED guard (`m ≤ n` for arbitrary naturals came back "proved"). So: errors are
      -- exceptions here, and the proof term must contain neither a sorry nor an unassigned metavariable.
      Term.withoutErrToSorry <| withOptions (fun o => maxHeartbeats.set o 20000) do
        let gs ← Tactic.run g.mvarId! (Tactic.withoutRecover (Tactic.evalTactic stx))
        if !gs.isEmpty then return false
        let pf ← instantiateMVars g
        return !(pf.hasSorry || pf.hasExprMVar)
    catch _ => return false

/-- The domain condition of one junk occurrence, as a goal; none when it has loose bound variables (inside a binder
of the statement, e.g. a summand) or no condition is known. -/
def domainGoal (a : Expr) : MetaM (Option (Expr × String)) := do
  let op := a.getAppFn.constName!
  let args := a.getAppArgs
  try
    match op with
    | `HDiv.hDiv | `Inv.inv =>
      let d := args[args.size - 1]!
      if d.hasLooseBVars then return none
      return some (← mkAppM `Ne #[d, ← mkAppOptM `OfNat.ofNat #[← inferType d, mkRawNatLit 0, none]],
                   "first | positivity | assumption | (intro h; norm_cast at h) | (intro h; norm_cast at h; omega) | (intro h; norm_num at h) | (intro h; norm_num at h; norm_cast at h; omega) | (intro h; norm_cast at h; simp [Nat.factorial_ne_zero] at h) | (norm_num; done)")
    | `Real.sqrt =>
      let x := args[0]!; if x.hasLooseBVars then return none
      return some (← mkAppM `LE.le #[← mkAppOptM `OfNat.ofNat #[← inferType x, mkRawNatLit 0, none], x],
                   "first | positivity | assumption | (norm_num; done)")
    | `Real.log =>
      let x := args[0]!; if x.hasLooseBVars then return none
      return some (← mkAppM `LT.lt #[← mkAppOptM `OfNat.ofNat #[← inferType x, mkRawNatLit 0, none], x],
                   "first | positivity | assumption | (norm_num; done)")
    | `HSub.hSub =>
      let x := args[4]!; let y := args[5]!
      if x.hasLooseBVars || y.hasLooseBVars then return none
      return some (← mkAppM `LE.le #[y, x], "first | assumption | omega | (norm_num; done)")
    | `riemannZeta =>
      let s := args[0]!; if s.hasLooseBVars then return none
      return some (← mkAppM `Ne #[s, ← mkAppOptM `OfNat.ofNat #[← inferType s, mkRawNatLit 1, none]],
                   "first | assumption | (norm_num; done) | (intro h; norm_cast at h) | (intro h; norm_cast at h; omega)")
    | _ => return none
  catch _ => return none

def dumpOne (n : Name) : TermElabM Json := do
  let ci ← getConstInfo n
  let used := (ci.value?.map (·.getUsedConstants)).getD #[]
  let lemmas := used.filter (junkLemmas.contains ·)
  let axs ← collectAxioms n
  let line ← do
    match ← findDeclarationRanges? n with
    | some r => pure r.range.pos.line
    | none => pure 0
  -- the statement AS WRITTEN: the reducing telescope unfolded `Monotone (fun x => x / c)` into `∀ a b, …`, and two
  -- different bound terms then printed alike (MEASURED 2026-11-24: 16 false IF STABLE in Mathlib.Algebra.Order.Field.Basic)
  forallTelescope ci.type fun xs concl => do
    let mut hyps := #[]
    for x in xs do
      let t ← inferType x
      if ← isProp t then hyps := hyps.push (Json.str s!"{← ppExpr t}")
    let mut ops := #[]
    for a in junkApps concl do
      let op := a.getAppFn.constName!
      let carrier ← if [`Real.sqrt, `Real.log, `riemannZeta].contains op then pure ""
                     else ppOrRaw a.getAppArgs[0]!
      let proved ← match ← domainGoal a with
        | some (g, tac) => proves g tac
        | none => pure false
      ops := ops.push (Json.mkObj [("op", Json.str op.toString), ("type", Json.str carrier),
                                   ("expr", Json.str (← ppOrRaw a)), ("args", Json.arr (← valueArgs a)),
                                   ("guard_proved", Json.bool proved), ("bound", Json.bool a.hasLooseBVars)])
    return Json.mkObj [("name", Json.str n.toString), ("line", Json.num line),
                       ("statement", Json.str s!"{← ppExpr concl}"),
                       ("hyps", Json.arr hyps), ("junk_ops", Json.arr ops),
                       ("junk_lemmas", Json.arr (lemmas.map (Json.str ·.toString))),
                       ("axioms", Json.arr (axs.map (Json.str ·.toString)))]

/-- every theorem declared in THIS file (not imported), auxiliary declarations skipped -/
elab "#lean2zfl_dump_here" : command => liftTermElabM do
  let env ← getEnv
  for (n, ci) in env.constants.map₂.toList do
    if n.isInternal || (`Lean2ZFL).isPrefixOf n then continue
    match ci with
    | .thmInfo _ => IO.println ("LEAN2ZFL " ++ (← dumpOne n).compress)
    | _ => pure ()

/-- every theorem of an IMPORTED, already built module (read from its .olean; nothing is re-elaborated) -/
elab "#lean2zfl_dump_module " m:ident : command => liftTermElabM do
  let env ← getEnv
  let some idx := env.getModuleIdx? m.getId | throwError s!"module {m.getId} is not imported"
  for (n, ci) in env.constants.map₁.toList do
    if n.isInternal || env.getModuleIdxFor? n != some idx then continue
    match ci with
    | .thmInfo _ => IO.println ("LEAN2ZFL " ++ (← dumpOne n).compress)
    | _ => pure ()

end Lean2ZFL
