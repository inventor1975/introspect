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
      -- the budget counts from HERE (withCurrHeartbeats): without it the 20000 were measured from the start of the
      -- whole command, so on later theorems of a module every attempt "ran out" at once = a false "not proved"
      Term.withoutErrToSorry <| withCurrHeartbeats <| withOptions (fun o => maxHeartbeats.set o 20000) do
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
                   "first | positivity | assumption | (intro h; norm_cast at h) | (intro h; norm_cast at h; omega) | (intro h; norm_num at h) | (intro h; norm_num at h; norm_cast at h; omega) | (intro h; norm_cast at h; simp [Nat.factorial_ne_zero] at h) | (intro h; linarith) | (norm_num; done)")
    | `Real.sqrt =>
      let x := args[0]!; if x.hasLooseBVars then return none
      return some (← mkAppM `LE.le #[← mkAppOptM `OfNat.ofNat #[← inferType x, mkRawNatLit 0, none], x],
                   "first | positivity | assumption | linarith | (norm_num; done)")
    | `Real.log =>
      let x := args[0]!; if x.hasLooseBVars then return none
      return some (← mkAppM `LT.lt #[← mkAppOptM `OfNat.ofNat #[← inferType x, mkRawNatLit 0, none], x],
                   "first | positivity | assumption | linarith | (norm_num; done)")
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

/-- Does the statement hold for EVERY value of the term `t`, provided one value at all its occurrences? Abstract
every occurrence of `t` into a fresh variable and try to PROVE the generalised statement (no recovery, no sorry).
This is what EARNED IF STABLE claims; a repeated term alone does not establish it (MEASURED 2026-11-24:
`KS23.unit_of`, `1 / √(u·u)` twice, holds only for the term's real value — 0 would give 0 = 1). -/
def generalizes (concl t : Expr) : TermElabM Bool := do
  if t.hasLooseBVars then return false
  let body ← kabstract concl t
  if !body.hasLooseBVars then return false
  let goal := Expr.forallE `x (← inferType t) body .default
  -- one tactic: `a; b` parses only inside parentheses (unparenthesised, the parse failed silently = "not proved")
  proves goal "(intro x; first | ring | (simp; done) | omega | rfl | (norm_num; done))"

/-- One junk occurrence as JSON, judged IN the current local context (so a binder's fresh variable and the binder's
own hypotheses — `∀ x, 0 < x → …` — are there for the guard's proof). -/
def occJson (concl a : Expr) (under : Bool) : TermElabM Json := do
  let op := a.getAppFn.constName!
  let carrier ← if [`Real.sqrt, `Real.log, `riemannZeta].contains op then pure ""
                 else ppOrRaw a.getAppArgs[0]!
  let proved ← match ← domainGoal a with
    | some (g, tac) => proves g tac
    | none => pure false
  let gen ← if proved || under then pure false else generalizes concl a
  return Json.mkObj [("op", Json.str op.toString), ("type", Json.str carrier),
                     ("expr", Json.str (← ppOrRaw a)), ("args", Json.arr (← valueArgs a)),
                     ("guard_proved", Json.bool proved), ("bound", Json.bool under),
                     ("generalizes", Json.bool gen)]

/-- Walk a statement; UNDER A BINDER (fun / ∀ / let) the bound variable is instantiated by a fresh local, so the
occurrence is a closed term with free variables and its domain condition can be PROVED for an arbitrary value —
i.e. for all values (MEASURED 2026-11-24: 41 of 110 OPEN theorems in six Mathlib modules had only such occurrences,
which the raw walk could not even try). -/
partial def visitJunk (concl e : Expr) (under : Bool) (acc : IO.Ref (Array Json)) : TermElabM Unit := do
  match e.getAppFn with
  | .const n _ =>
    if junkOps.contains n && e.getAppNumArgs ≥ junkArity n then
      let j ← occJson concl e under
      acc.modify (·.push j)
    if e.isApp then
      for x in e.getAppArgs do visitJunk concl x under acc
    return
  | _ => pure ()
  match e with
  | .app f a => visitJunk concl f under acc; visitJunk concl a under acc
  | .lam nm t b bi =>
    visitJunk concl t under acc
    withLocalDecl nm bi t fun x => visitJunk concl (b.instantiate1 x) true acc
  | .forallE nm t b bi =>
    visitJunk concl t under acc
    withLocalDecl nm bi t fun x => visitJunk concl (b.instantiate1 x) true acc
  | .letE nm t v b _ =>
    visitJunk concl t under acc; visitJunk concl v under acc
    withLetDecl nm t v fun x => visitJunk concl (b.instantiate1 x) true acc
  | .mdata _ b => visitJunk concl b under acc
  | .proj _ _ b => visitJunk concl b under acc
  | _ => pure ()

/-- The junk lemmas a theorem's proof reaches ANYWHERE in its chain of lemmas (theorems only: a definition is a term
the statement talks about, not a step of the proof). Memoised for the whole run. Its blind spot, stated: a junk value
reached by unfolding a definition, with no named lemma, is not seen. -/
abbrev JunkMemo := IO.Ref (Std.HashMap Name (Array Name))

partial def junkReach (junkMemo : JunkMemo) (c : Name) : CoreM (Array Name) := do
  if let some r := (← junkMemo.get).get? c then return r
  junkMemo.modify (·.insert c #[])               -- guard (the constant graph is acyclic; this only stops re-entry)
  let env ← getEnv
  let mut out : Array Name := #[]
  match env.find? c with
  | some (.thmInfo v) =>
    for u in v.value.getUsedConstants do
      if junkLemmas.contains u then
        unless out.contains u do out := out.push u
      else
        for x in ← junkReach junkMemo u do
          unless out.contains x do out := out.push x
  | _ => pure ()
  junkMemo.modify (·.insert c out)
  return out

def dumpOne (memo : JunkMemo) (n : Name) : TermElabM Json := do
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
    let acc ← IO.mkRef #[]
    visitJunk concl concl false acc
    let ops ← acc.get
    return Json.mkObj [("name", Json.str n.toString), ("line", Json.num line),
                       ("statement", Json.str s!"{← ppExpr concl}"),
                       ("hyps", Json.arr hyps), ("junk_ops", Json.arr ops),
                       ("junk_lemmas", Json.arr (lemmas.map (Json.str ·.toString))),
                       ("junk_reach", Json.arr ((← junkReach memo n).map (Json.str ·.toString))),
                       ("axioms", Json.arr (axs.map (Json.str ·.toString)))]

/-- every theorem declared in THIS file (not imported), auxiliary declarations skipped -/
elab "#lean2zfl_dump_here" : command => liftTermElabM do
  let env ← getEnv
  let memo : JunkMemo ← IO.mkRef {}
  for (n, ci) in env.constants.map₂.toList do
    if n.isInternal || (`Lean2ZFL).isPrefixOf n then continue
    match ci with
    | .thmInfo _ =>
      if (← findDeclarationRanges? n).isNone then continue   -- generated (equation lemmas): not the author's theorem
      -- a theorem the dumper cannot read is REPORTED, never dropped (MEASURED 2026-11-24: 4 of 342 vanished silently)
      -- runtime exceptions too (heartbeats, recursion depth): a plain `try` does not catch them and the command stops
      tryCatchRuntimeEx (withCurrHeartbeats do IO.println ("LEAN2ZFL " ++ (← dumpOne memo n).compress))
        (fun e => do IO.println s!"LEAN2ZFL_FAIL {n} {(← e.toMessageData.toString).replace "\n" " "}")
    | _ => pure ()

/-- every theorem of an IMPORTED, already built module (read from its .olean; nothing is re-elaborated) -/
elab "#lean2zfl_dump_module " m:ident : command => liftTermElabM do
  let env ← getEnv
  let memo : JunkMemo ← IO.mkRef {}
  let some idx := env.getModuleIdx? m.getId | throwError s!"module {m.getId} is not imported"
  IO.println s!"LEAN2ZFL_MODULE {m.getId}"
  for (n, ci) in env.constants.map₁.toList do
    if n.isInternal || env.getModuleIdxFor? n != some idx then continue
    match ci with
    | .thmInfo _ =>
      if (← findDeclarationRanges? n).isNone then continue   -- generated (equation lemmas): not the author's theorem
      -- a theorem the dumper cannot read is REPORTED, never dropped (MEASURED 2026-11-24: 4 of 342 vanished silently)
      -- runtime exceptions too (heartbeats, recursion depth): a plain `try` does not catch them and the command stops
      tryCatchRuntimeEx (withCurrHeartbeats do IO.println ("LEAN2ZFL " ++ (← dumpOne memo n).compress))
        (fun e => do IO.println s!"LEAN2ZFL_FAIL {n} {(← e.toMessageData.toString).replace "\n" " "}")
    | _ => pure ()

end Lean2ZFL
