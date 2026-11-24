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
partial def junkApps (e : Lean.Expr) (acc : Array Lean.Expr := #[]) : Array Lean.Expr :=
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

def ppOrRaw (e : Lean.Expr) : MetaM String := do
  if e.hasLooseBVars then return s!"{e}" else return s!"{← ppExpr e}"

/-- the explicit value arguments of a junk application (the last ones), pretty-printed -/
def valueArgs (a : Lean.Expr) : MetaM (Array Json) := do
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
def proves1 (goal : Lean.Expr) (tac : String) : TermElabM Bool := do
  match Parser.runParserCategory (← getEnv) `tactic tac with
  | .error _ => return false                      -- a tactic this environment does not have (no Mathlib): skipped
  | .ok stx =>
    -- A FAILED ATTEMPT LEAVES NO MESSAGE (MEASURED 2026-11-24): some tactics LOG their "unsolved goals" instead of
    -- throwing; ten E/OPEN theorems in one file reached Lean's 100-error limit and the whole file stopped before the
    -- dump — 1690 of 2451 came back unread. The message log is put back as it was after every attempt.
    let saved := (← getThe Core.State).messages
    let r ← proves1Core goal stx
    modifyThe Core.State fun st => { st with messages := saved }
    return r

where proves1Core (goal : Lean.Expr) (stx : Syntax) : TermElabM Bool := do
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

/-- `first | a | b | …`, but each alternative parsed and tried ON ITS OWN: one alternative this environment lacks
(positivity, norm_num, linarith without Mathlib — the ZTL repository is Lean core only) must not sink the others,
which a single `first | …` parse did. Every alternative must close the goal. -/
def proves (goal : Lean.Expr) (tac : String) : TermElabM Bool := do
  -- split at TOP-LEVEL bars only: an alternative may itself contain `first | …` inside parentheses
  let body := (tac.trim.dropPrefix "first").toString.trim
  let topSplit (s : String) : List String := Id.run do
    let mut depth : Int := 0
    let mut cur := ""
    let mut out : List String := []
    for c in s.toList do
      if c == '(' then depth := depth + 1
      if c == ')' then depth := depth - 1
      if c == '|' && depth == 0 then
        out := out ++ [cur.trim]; cur := ""
      else cur := cur.push c
    return out ++ [cur.trim]
  let alts := if tac.trim.startsWith "first" then (topSplit body).filter (· != "") else [tac]
  for alt in alts do
    if alt != "" && (← proves1 goal alt) then return true
  return false

/-- The domain condition of one junk occurrence, as a goal; none when it has loose bound variables (inside a binder
of the statement, e.g. a summand) or no condition is known. -/
def domainGoal (a : Lean.Expr) : MetaM (Option (Lean.Expr × String)) := do
  let op := a.getAppFn.constName!
  let args := a.getAppArgs
  try
    match op with
    | `HDiv.hDiv | `Inv.inv =>
      let d := args[args.size - 1]!
      if d.hasLooseBVars then return none
      let ty ← whnfR (← inferType d)
      if op == `HDiv.hDiv && (ty.isConstOf `Nat || ty.isConstOf `Int) then
        -- ℕ / ℤ division TRUNCATES: its convention is not only at 0 — 7 / 2 = 3. The guard: exact and nonzero.
        let n := args[args.size - 2]!
        if n.hasLooseBVars then return none
        let z ← mkAppOptM `OfNat.ofNat #[← inferType d, mkRawNatLit 0, none]
        return some (← mkAppM `And #[← mkAppM `Dvd.dvd #[d, n], ← mkAppM `Ne #[d, z]],
                     "first | (constructor <;> first | assumption | decide | omega | (norm_num; done)) | decide | omega | (norm_num; done)")
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
def generalizes (concl t : Lean.Expr) : TermElabM Bool := do
  if t.hasLooseBVars then return false
  let body ← kabstract concl t
  if !body.hasLooseBVars then return false
  let goal := Lean.Expr.forallE `x (← inferType t) body .default
  -- one tactic: `a; b` parses only inside parentheses (unparenthesised, the parse failed silently = "not proved")
  proves goal "first | (intro x; ring) | (intro x; simp; done) | (intro x; omega) | (intro x; rfl) | (intro x; norm_num; done)"

/-- The JUNK-domain condition of one occurrence: the argument IS at a convention point (a denominator = 0, log of
x ≤ 0 — at 0 and below Mathlib's log is a convention, √ of x < 0, ℕ-subtraction a < b, ζ at 1, a non-summable
series). PROVED from the statement's own hypotheses, it means the statement speaks about the convention there: E. -/
def junkDomainGoal (a : Lean.Expr) : MetaM (Option (Lean.Expr × String)) := do
  let op := a.getAppFn.constName!
  let args := a.getAppArgs
  let tac := "first | assumption | (norm_num; done) | linarith | omega | rfl | (exact le_of_lt (by assumption)) | (exact le_of_eq (by assumption)) | (exact (le_of_eq (by assumption)).trans le_rfl)"
  try
    match op with
    | `HDiv.hDiv | `Inv.inv =>
      let d := args[args.size - 1]!
      if d.hasLooseBVars then return none
      let ty ← whnfR (← inferType d)
      if op == `HDiv.hDiv && (ty.isConstOf `Nat || ty.isConstOf `Int) then
        let n := args[args.size - 2]!
        if n.hasLooseBVars then return none
        let z ← mkAppOptM `OfNat.ofNat #[← inferType d, mkRawNatLit 0, none]
        return some (← mkAppM `Or #[← mkAppM `Not #[← mkAppM `Dvd.dvd #[d, n]], ← mkAppM `Eq #[d, z]],
                     "first | decide | omega | (left; decide) | (left; omega) | (right; assumption) | (norm_num; done)")
      return some (← mkAppM `Eq #[d, ← mkAppOptM `OfNat.ofNat #[← inferType d, mkRawNatLit 0, none]], tac)
    | `Real.sqrt =>
      let x := args[0]!; if x.hasLooseBVars then return none
      return some (← mkAppM `LT.lt #[x, ← mkAppOptM `OfNat.ofNat #[← inferType x, mkRawNatLit 0, none]], tac)
    | `Real.log =>
      let x := args[0]!; if x.hasLooseBVars then return none
      return some (← mkAppM `LE.le #[x, ← mkAppOptM `OfNat.ofNat #[← inferType x, mkRawNatLit 0, none]], tac)
    | `HSub.hSub =>
      let x := args[4]!; let y := args[5]!
      if x.hasLooseBVars || y.hasLooseBVars then return none
      return some (← mkAppM `LT.lt #[x, y], tac)
    | `riemannZeta =>
      let s := args[0]!; if s.hasLooseBVars then return none
      return some (← mkAppM `Eq #[s, ← mkAppOptM `OfNat.ofNat #[← inferType s, mkRawNatLit 1, none]], tac)
    | _ => return none
  catch _ => return none

/-- One junk occurrence as JSON, judged IN the current local context (so a binder's fresh variable and the binder's
own hypotheses — `∀ x, 0 < x → …` — are there for the guard's proof). -/
def occJson (concl a : Lean.Expr) (under : Bool) : TermElabM Json := do
  let op := a.getAppFn.constName!
  let carrier ← if [`Real.sqrt, `Real.log, `riemannZeta].contains op then pure ""
                 else ppOrRaw a.getAppArgs[0]!
  let proved ← match ← domainGoal a with
    | some (g, tac) => proves g tac
    | none => pure false
  let gen ← if proved || under then pure false else generalizes concl a
  let atJunk ← if proved then pure false else match ← junkDomainGoal a with
    | some (g, tac) => proves g tac
    | none => pure false
  return Json.mkObj [("op", Json.str op.toString), ("type", Json.str carrier),
                     ("expr", Json.str (← ppOrRaw a)), ("args", Json.arr (← valueArgs a)),
                     ("guard_proved", Json.bool proved), ("bound", Json.bool under),
                     ("generalizes", Json.bool gen), ("junk_proved", Json.bool atJunk)]

/-- Walk a statement; UNDER A BINDER (fun / ∀ / let) the bound variable is instantiated by a fresh local, so the
occurrence is a closed term with free variables and its domain condition can be PROVED for an arbitrary value —
i.e. for all values (MEASURED 2026-11-24: 41 of 110 OPEN theorems in six Mathlib modules had only such occurrences,
which the raw walk could not even try). -/
partial def visitJunk (concl e : Lean.Expr) (under : Bool) (acc : IO.Ref (Array Json)) : TermElabM Unit := do
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

/-! ### The statement in ZFL (2026-11-24, the curator: "делаем" — Lean read by ZTL, VR as the frame)

The statement's MATHEMATICS written in ZFL's numeric language, for ZTL's numeric floor to read: + - * / as exact
rational arithmetic (ℕ's truncating `/` and `-` are written as the operations they abbreviate — the very difference
the floor then shows), `x ^ n` with a literal n as `x**n`, a real exponent as `pow`, √ ln exp sin cos tan arctan π,
|a| as max(a, -a), casts dropped (the number is the same number). What has no word in ZFL is NOT guessed: the part is
reported `untr` with the head it stopped at. Variables are named `v_<name>` (ASCII, unique), so no name of a
statement can collide with a ZFL word. -/

def zflName (s : String) (taken : List String) : String := Id.run do
  let sub := "₀₁₂₃₄₅₆₇₈₉".toList
  let mut out := "v_"
  for c in s.toList do
    if c.isAlphanum && c.toNat < 128 || c == '_' then out := out.push c
    else match (sub.zip (List.range 10)).find? (·.1 == c) with
      | some (_, i) => out := out ++ toString i
      | none => out := out.push '_'
  let mut name := out
  let mut k := 2
  while taken.contains name do
    name := out ++ "_" ++ toString k
    k := k + 1
  return name

abbrev ZNames := Std.HashMap FVarId String

partial def zTerm (names : ZNames) (e : Lean.Expr) : MetaM String := do
  let e := e.consumeMData
  match e with
  | .fvar id => match names.get? id with
    | some s => return s
    | none => throwError "untr: a variable that is not a number of the statement"
  | .lit (.natVal n) => return toString n
  | _ => pure ()
  let args := e.getAppArgs
  let bin (op : String) (a b : Lean.Expr) : MetaM String := do
    return s!"({← zTerm names a} {op} {← zTerm names b})"
  let fn1 (f : String) : MetaM String := do
    if args.size == 0 then throwError s!"untr: {f} unapplied"
    return s!"{f}({← zTerm names args[args.size - 1]!})"
  match e.getAppFn.constName? with
  | some `OfNat.ofNat =>
    let lit : Option Lean.Expr := args[1]?
    match lit.map Lean.Expr.consumeMData with
    | some (Lean.Expr.lit (Lean.Literal.natVal n)) => return toString n
    | _ => throwError "untr: a numeral that is not a literal"
  | some `HAdd.hAdd => if args.size == 6 then bin "+" args[4]! args[5]! else throwError "untr: + partially applied"
  | some `HSub.hSub => if args.size == 6 then bin "-" args[4]! args[5]! else throwError "untr: - partially applied"
  | some `HMul.hMul => if args.size == 6 then bin "*" args[4]! args[5]! else throwError "untr: * partially applied"
  | some `HDiv.hDiv => if args.size == 6 then bin "/" args[4]! args[5]! else throwError "untr: / partially applied"
  | some `Neg.neg => if args.size == 3 then return s!"(-{← zTerm names args[2]!})" else throwError "untr: neg"
  | some `Inv.inv => if args.size == 3 then return s!"(1 / {← zTerm names args[2]!})" else throwError "untr: inv"
  | some `HPow.hPow =>
    if args.size != 6 then throwError "untr: ^ partially applied"
    let b ← zTerm names args[4]!
    let x := args[5]!.consumeMData
    let lit : Option Nat := match x with
      | .lit (.natVal n) => some n
      | _ => if x.isAppOfArity `OfNat.ofNat 3 then
               (match x.getAppArgs[1]!.consumeMData with | Lean.Expr.lit (Lean.Literal.natVal n) => some n | _ => none)
             else none
    let xty ← whnfR (← inferType x)
    match lit with
    | some n => if xty.isConstOf `Nat then return s!"({b})**{n}" else return s!"pow({b}, {n})"
    | none =>
      if xty.isConstOf `Real then return s!"pow({b}, {← zTerm names x})"
      -- a CLOSED exponent (no variable): its mathematics is a number, written as one — `a ^ (1 / 3)` over ℕ is
      -- Lean's a ^ 0 and the author's cube root, and the floor reads the author's (pow, exact 1/3)
      if !x.hasFVar then return s!"pow({b}, {← zTerm names x})"
      throwError "untr: a power with a symbolic natural exponent"
  | some `Real.sqrt => fn1 "sqrt"
  | some `Real.log => fn1 "ln"
  | some `Real.exp => fn1 "exp"
  | some `Real.sin => fn1 "sin"
  | some `Real.cos => fn1 "cos"
  | some `Real.tan => fn1 "tan"
  | some `Real.arctan => fn1 "atan"
  | some `Real.pi => return "pi"
  | some `Real.logb =>
    if args.size == 2 then return s!"(ln({← zTerm names args[1]!}) / ln({← zTerm names args[0]!}))"
    else throwError "untr: logb"
  | some `abs =>
    if args.size == 0 then throwError "untr: abs"
    let a ← zTerm names args[args.size - 1]!
    return s!"max({a}, (-{a}))"
  | some `Min.min => if args.size == 4 then return s!"min({← zTerm names args[2]!}, {← zTerm names args[3]!})" else throwError "untr: min"
  | some `Max.max => if args.size == 4 then return s!"max({← zTerm names args[2]!}, {← zTerm names args[3]!})" else throwError "untr: max"
  | some `Nat.cast | some `Int.cast | some `Rat.cast | some `NNRatCast.nnratCast | some `IntCast.intCast
  | some `NatCast.natCast =>
    if args.size == 0 then throwError "untr: cast" else zTerm names args[args.size - 1]!
  | some c => throwError s!"untr: {c}"
  | none => throwError s!"untr: {e.ctorName}"

def numKind (t : Lean.Expr) : MetaM String := do
  let ty ← whnfR t
  return if ty.isConstOf `Real then "real" else if ty.isConstOf `Nat then "nat"
         else if ty.isConstOf `Int then "int" else if ty.isConstOf `Rat then "rat" else ""

/-- variables a conclusion's inner universals add to the box, and the ZFL names already taken -/
abbrev ZExtra := IO.Ref (Array Json × List String)

/-- `pol`: 1 a positive place (the conclusion, ∧ ∨, the right of →), -1 a negative one (the left of →, under ¬, a
hypothesis), 0 both (a side of ↔). A NUMERIC ∀ IN A POSITIVE PLACE adds its variable to the box (2026-11-24, the
curator: "кванторы мы делали — проверь, чтобы не делать дубли"): ZFL has no quantifier in a claim by design (zfl.py,
the `sets` note) because the box IS the universal over readings — so ∀ y, P y in a positive place is P with y one more
quantity of the box, exactly the fresh parameter of zfo's δ-rule. Anywhere else a ∀ is an ∃ in disguise, and ∃ has no
ZFL word (a `?` search proves no "none" and no "for all"): untranslated, said so. -/
partial def zProp (names : ZNames) (pol : Int) (ex : ZExtra) (e : Lean.Expr) : MetaM String := do
  let e := e.consumeMData
  if let .forallE nm t b bi := e then
    if !b.hasLooseBVars && (← isProp t) then
      return s!"({← zProp names (-pol) ex t} -> {← zProp names pol ex b})"
    if pol != 1 then throwError "untr: an inner quantifier (not in a positive place)"
    let k ← numKind t
    if k == "" then throwError "untr: an inner quantifier over a non-number"
    return ← withLocalDecl nm bi t fun x => do
      let (vs, taken) ← ex.get
      let zn := zflName nm.toString taken
      ex.set (vs.push (Json.mkObj [("name", Json.str zn), ("lean", Json.str nm.toString), ("type", Json.str k),
                                   ("inner", Json.bool true)]), zn :: taken)
      zProp (names.insert x.fvarId! zn) pol ex (b.instantiate1 x)
  let args := e.getAppArgs
  let cmp (op : String) : MetaM String := do
    if args.size != 4 then throwError s!"untr: {op} partially applied"
    return s!"({← zTerm names args[2]!} {op} {← zTerm names args[3]!})"
  match e.getAppFn.constName? with
  | some `LT.lt => cmp "<"
  | some `LE.le => cmp "<="
  | some `GT.gt => cmp ">"
  | some `GE.ge => cmp ">="
  | some `Eq =>
    if args.size != 3 then throwError "untr: ="
    if ← isProp args[1]! then throwError "untr: an equality of statements"
    return s!"({← zTerm names args[1]!} == {← zTerm names args[2]!})"
  | some `Ne =>
    if args.size != 3 then throwError "untr: ≠"
    return s!"({← zTerm names args[1]!} != {← zTerm names args[2]!})"
  | some `And => if args.size == 2 then return s!"({← zProp names pol ex args[0]!} & {← zProp names pol ex args[1]!})" else throwError "untr: ∧"
  | some `Or => if args.size == 2 then return s!"({← zProp names pol ex args[0]!} | {← zProp names pol ex args[1]!})" else throwError "untr: ∨"
  | some `Iff => if args.size == 2 then return s!"({← zProp names 0 ex args[0]!} <-> {← zProp names 0 ex args[1]!})" else throwError "untr: ↔"
  | some `Not => if args.size == 1 then return s!"(~{← zProp names (-pol) ex args[0]!})" else throwError "untr: ¬"
  | some `Exists => throwError "untr: an inner quantifier (∃)"
  | some c => throwError s!"untr: {c}"
  | none => throwError s!"untr: {e.ctorName}"

def zTry (k : MetaM String) : MetaM Json := do
  try return Json.mkObj [("zfl", Json.str (← k))]
  catch ex =>
    let m ← ex.toMessageData.toString
    return Json.mkObj [("untr", Json.str ((m.dropPrefix "untr: ").toString))]

/-- the binders of the statement: the number variables (named for ZFL), the hypotheses, the conclusion -/
def zflOf (xs : Array Lean.Expr) (concl : Lean.Expr) : MetaM Json := do
  let mut names : ZNames := {}
  let mut taken : List String := []
  let mut vars := #[]
  let mut hypTs := #[]
  let mut bad : Option String := none
  for x in xs do
    let t ← inferType x
    if ← isProp t then
      hypTs := hypTs.push t
    else
      let kind ← numKind t
      let decl ← x.fvarId!.getDecl
      if kind == "" then
        bad := bad <|> some s!"a variable of type {← ppExpr t}"
      else
        let nm := zflName decl.userName.toString taken
        taken := nm :: taken
        names := names.insert x.fvarId! nm
        vars := vars.push (Json.mkObj [("name", Json.str nm), ("lean", Json.str decl.userName.toString),
                                       ("type", Json.str kind)])
  -- a hypothesis is ASSUMED: a negative place (its ∀ is not the box's); the conclusion is the positive one
  let ex : ZExtra ← IO.mkRef (#[], taken)
  let mut hyps := #[]
  for t in hypTs do
    hyps := hyps.push (← zTry (zProp names (-1) ex t))
  let c ← zTry (zProp names 1 ex concl)
  let (inner, _) ← ex.get
  return Json.mkObj ([("vars", Json.arr (vars ++ inner)), ("hyps", Json.arr hyps), ("concl", c)] ++
                     (match bad with | some b => [("untr_vars", Json.str b)] | none => []))

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
                       ("axioms", Json.arr (axs.map (Json.str ·.toString))),
                       ("zfl", ← zflOf xs concl)]

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
