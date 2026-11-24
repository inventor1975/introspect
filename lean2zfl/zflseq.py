# -*- coding: utf-8 -*-
"""
zflseq — A SEQUENCE IS COMPUTED FROM THE HYPOTHESES THAT DEFINE IT (2026-11-25, the curator's "да").

A Lean statement about `u : ℕ → K` (K a number type) is usually a recurrence:
    u 1 = 2,  ∀ n, u (n + 1) = 3 * u n + 4   ⊢   u n = 4 * 3 ^ (n - 1) - 2.
The dumper writes `u t` as app(q_u, t) and a hypothesis ∀ n, … as a RULE (bound names r_…). Read here as VR reads a
sequence — an operation, not an arbitrary function:

  FORCED VALUES. Every fact and every rule instance (n = 0 … N) is an equation about finitely many values. One with
  exactly ONE unknown value, linear in it with a non-zero coefficient (znum._mpoly, exact), FORCES that value —
  forward (u(n+1) from u(n)) or backward (u 0 from u 1 = 3 u 0 + 4). Iterated to a fixed point. A value outside the
  codomain (u : ℕ → ℕ forced to 3/2, or −1) means NO sequence satisfies the hypotheses: vacuous, never a refutation.
  An instance with no unknown left is CHECKED; false means vacuous.

  A POINT. The other variables are drawn as in zflread.witness; at a point every value the conclusion reads must be
  forced, every non-rule hypothesis EARNED, the conclusion REFUTED — then it is a counterexample: any sequence that
  satisfies the hypotheses has these values.

  EXISTENCE. "Any sequence that satisfies them" might be none: a statement whose hypotheses no sequence satisfies is
  vacuously true. Existence is GUARANTEED (`existence: recursion`) only when each rule is a forward recurrence
  u(r + k) = RHS(r, values at indices below r + k) — one per sequence, a guard at most `r >= c`, an RHS of + − ×
  and integer powers (for ℕ/ℤ codomains: + × with no −, or + − ×, so the values stay in the codomain) — and nothing
  was left unchecked. Otherwise the refutation is `existence: conditional`: false, or vacuously true.

  NEVER EARNED (the curator's word): a prefix proves nothing about every n; the disposition stays OPEN.
"""
import re
from fractions import Fraction

PREFIX = 40                 # rule instances n = 0 … PREFIX (more when a concrete index asks for it)
INDEX_CAP = 2100            # Lean Workbook asks u 2023: computed up to here, never past it
POINT_TRIES = 120

_APP = "app("


def _zr():
    import zflread
    return zflread


def _top_split(text, sep):
    """text split at `sep` at parenthesis depth 0 (after stripping one pair of outer parentheses)"""
    t = text.strip()
    while t.startswith("(") and t.endswith(")"):
        depth, ok = 0, True
        for k, ch in enumerate(t):
            depth += (ch == "(") - (ch == ")")
            if depth == 0 and k < len(t) - 1:
                ok = False
                break
        if not ok:
            break
        t = t[1:-1].strip()
    parts, depth, last, k = [], 0, 0, 0
    while k < len(t):
        ch = t[k]
        depth += (ch == "(") - (ch == ")")
        if depth == 0 and t.startswith(sep, k):
            parts.append(t[last:k])
            last = k + len(sep)
            k += len(sep)
            continue
        k += 1
    parts.append(t[last:])
    return [p.strip() for p in parts]


def _subst(text, names):
    """names {name: Fraction} substituted (word boundaries)"""
    zr = _zr()
    for n, v in sorted(names.items(), key=lambda kv: -len(kv[0])):
        text = re.sub(rf"\b{re.escape(n)}\b", f"({zr._print(Fraction(v))})", text)
    return text


def _apps(text, vals, idx_of):
    """every app(q, t) in text: replaced by its forced value when known; returns (text, unknown [(q, i)]) or None when
    an index is not an integer (or not read)"""
    zr = _zr()
    out, last, unknown = [], 0, []
    for j, k, inner in zr._calls(text, "app"):
        q, _, t = inner.partition(",")
        q, t = q.strip(), t.strip()
        t2, unk2 = _apps(t, vals, idx_of) or (None, None)
        if t2 is None or unk2:
            return None                                  # an index that itself reads an unknown value
        i = idx_of(t2)
        if i is None:
            return None
        out.append(text[last:j])
        if i in vals.get(q, {}):
            out.append(f"({zr._print(vals[q][i])})")
        else:
            out.append(_xname(q, i))
            unknown.append((q, i))
        last = k
    out.append(text[last:])
    return "".join(out), unknown


def _xname(q, i):
    i = Fraction(i)
    t = f"{abs(i.numerator)}" + (f"_{i.denominator}" if i.denominator != 1 else "")
    return f"X__{q}__{'m' if i < 0 else ''}{t}"


def _idx(text):
    """an argument's exact rational value (an integer for a sequence), or None"""
    v = _zr()._exact_of(text)
    if v is None:
        return None
    return int(v) if v.denominator == 1 else v


def _arg_ok(i, dom):
    """an argument inside the variable's domain and inside the caps"""
    i = Fraction(i)
    if dom == "nat":
        return i.denominator == 1 and 0 <= i <= INDEX_CAP
    if dom == "int":
        return i.denominator == 1 and abs(i) <= INDEX_CAP
    return abs(i.numerator) <= 10 ** 6 and i.denominator <= 10 ** 6


_REALS = sorted({Fraction(n) for n in range(-6, 7)} | {Fraction(p, 2) for p in (-3, -1, 1, 3)} |
                {Fraction(p, 3) for p in (-1, 1)})
_REALS_SMALL = [Fraction(n) for n in range(-2, 3)]


def _truth(text):
    """EARNED / REFUTED / other for a formula with no name left"""
    from znumjudge import judge_sheet_claim
    try:
        return judge_sheet_claim(text, {}, {})["disposition"]
    except Exception:
        return "UNREAD"


def _solve_one(lhs, rhs, xname):
    """the value of xname forced by lhs == rhs, when the difference is linear in it with a non-zero coefficient"""
    import znum
    from znumjudge import _parse_arith
    try:
        tree = _parse_arith(f"({lhs}) - ({rhs})", {xname: {}})
        p = znum._mpoly(tree, {xname: {"lo": float("-inf"), "hi": float("inf")}})
    except Exception:
        return None
    lin = ((xname, 1),)
    if set(p) - {(), lin} or lin not in p:
        return None
    return -p.get((), Fraction(0)) / p[lin]


def _in_codomain(v, cod):
    if cod == "nat":
        return v.denominator == 1 and v >= 0
    if cod == "int":
        return v.denominator == 1
    return True


def solve(seqs, facts, rules, need=0, seen=()):
    """forced values {q: {i: Fraction}} from facts (texts) and rules [(bound names, text)], or 'vacuous', plus the
    instances left unchecked. seqs: {q: (domain, codomain)}. A rule is instantiated at ℕ indices 0 … top (one binder),
    at integers, and at a fixed set of rationals plus the arguments `seen` (a function at points); several binders
    over a smaller set; more than three binders: not read."""
    import itertools
    top = min(INDEX_CAP, max(PREFIX, need + 2))
    extra = sorted({Fraction(x) for x in seen})
    insts = list(facts)
    for bound, text in rules:
        k = len(bound)
        if k > 3:
            return None, None
        pools = []
        for b_ in bound:
            name, kind = b_.split(":")
            if kind == "nat":
                pools.append([Fraction(n) for n in range(0, (top if k == 1 else 12) + 1)])
            elif kind == "int":
                m = min(top, 30) if k == 1 else 6
                pools.append([Fraction(n) for n in range(-m, m + 1)])
            else:
                base = _REALS if k <= 2 else _REALS_SMALL
                pools.append(sorted(set(base) | set(extra)))
        names = [b_.split(":")[0] for b_ in bound]
        for combo in itertools.product(*pools):
            insts.append(_subst(text, dict(zip(names, combo))))
    vals = {q: {} for q in seqs}
    pending = []
    for inst in insts:                                   # split guards and conjunctions once
        stack = [inst]
        while stack:
            t = stack.pop()
            imp = _top_split(t, "->")
            if len(imp) == 2 and _APP not in imp[0]:
                g = _truth(imp[0])
                if g == "REFUTED":
                    continue                             # the guard fails: the instance says nothing
                if g != "EARNED":
                    pending.append(t)
                    continue
                t = imp[1]
            conj = _top_split(t, "&")
            if len(conj) > 1:
                stack += conj
                continue
            pending.append(t)
    progress = True
    while progress:
        progress = False
        left = []
        for t in pending:
            r = _apps(t, vals, _idx)
            if r is None:
                left.append(t)
                continue
            text, unknown = r
            if any(not _arg_ok(i, seqs[q][0]) for q, i in unknown):
                left.append(t)                           # an argument outside the domain (n − 1 at 0 in ℕ): unread
                continue
            if not unknown:
                v = _truth(text)
                if v == "REFUTED":
                    return "vacuous", t
                if v != "EARNED":
                    left.append(t)
                continue
            if len(set(unknown)) == 1:
                eq = _top_split(text, "==")
                if len(eq) == 2:
                    q, i = unknown[0]
                    x = _solve_one(eq[0], eq[1], _xname(q, i))
                    if x is not None:
                        if not _in_codomain(x, seqs[q][1]):
                            return "vacuous", f"{q}({i}) = {x} is not in its codomain {seqs[q][1]}"
                        vals[q][i] = x
                        progress = True
                        continue
            left.append(t)
        pending = left
        if not progress:                                 # one at a time is stuck: solve the LINEAR SYSTEM exactly
            r = _system(pending, vals, seqs)
            if r == "vacuous":
                return "vacuous", "the linear system of the instances is inconsistent"
            if r:
                progress = True
    return vals, pending


SYSTEM_ROWS = 600


def _system(pending, vals, seqs):
    """the pending equations linear in their unknown values, eliminated exactly (Gauss–Jordan over ℚ): every unknown
    the system DETERMINES is assigned (True), an inconsistent system is 'vacuous', otherwise False. An unknown
    determined only up to a free one is left unknown — never guessed."""
    import znum
    from znumjudge import _parse_arith
    rows, cols = [], {}
    for t in pending:
        r = _apps(t, vals, _idx)
        if r is None:
            continue
        text, unknown = r
        if not unknown or any(not _arg_ok(i, seqs[q][0]) for q, i in unknown):
            continue
        eq = _top_split(text, "==")
        if len(eq) != 2:
            continue
        xs = {_xname(q, i): (q, i) for q, i in unknown}
        try:
            tree = _parse_arith(f"({eq[0]}) - ({eq[1]})", {x: {} for x in xs})
            p = znum._mpoly(tree, {x: {"lo": float("-inf"), "hi": float("inf")} for x in xs})
        except Exception:
            continue
        if any(len(m) > 1 or (m and m[0][1] != 1) for m in p):
            continue                                     # not linear in the unknowns
        row = {m[0][0]: c for m, c in p.items() if m}
        if not row:
            continue
        for x in row:
            cols.setdefault(x, xs[x])
        rows.append((row, -p.get((), Fraction(0))))
        if len(rows) >= SYSTEM_ROWS:
            break
    if not rows:
        return False
    # Gauss–Jordan on sparse rows
    piv = {}                                             # column -> (row, rhs) with that column's coefficient 1
    for row, rhs in rows:
        row = dict(row)
        for c, (pr, prhs) in piv.items():
            if c in row:
                k = row.pop(c)
                for c2, v2 in pr.items():
                    if c2 != c:
                        nv = row.get(c2, 0) - k * v2
                        if nv:
                            row[c2] = nv
                        else:
                            row.pop(c2, None)
                rhs = rhs - k * prhs
        if not row:
            if rhs != 0:
                return "vacuous"
            continue
        c = next(iter(row))
        k = row[c]
        row = {c2: v / k for c2, v in row.items()}
        rhs = rhs / k
        for c0, (pr, prhs) in list(piv.items()):         # eliminate c from the earlier pivots
            if c in pr:
                kk = pr[c]
                npr = {c2: pr.get(c2, 0) - kk * row.get(c2, 0) for c2 in set(pr) | set(row)}
                piv[c0] = ({c2: v for c2, v in npr.items() if v}, prhs - kk * rhs)
        piv[c] = (row, rhs)
    done = False
    for c, (pr, prhs) in piv.items():
        if set(pr) == {c}:                               # the row names this unknown alone: DETERMINED
            q, i = cols[c]
            if not _in_codomain(prhs, seqs[q][1]):
                return "vacuous"
            if i not in vals[q]:
                vals[q][i] = prhs
                done = True
    return done


_POLY_OPS = re.compile(r"/|ndiv|idiv|sqrt|ln\(|log10|exp\(|sin\(|cos\(|tan\(|min\(|max\(|ifpos|mod\(|fact\(|choose")


def existence_by_recursion(seqs, rules):
    """True when every rule is a forward recurrence for its own sequence (see the module note)"""
    if any(d != "nat" for d, _ in seqs.values()):
        return False                                     # a function at points: no recursion builds it
    owner = {}
    for bound, text in rules:
        if len(bound) != 1:
            return False
        r = bound[0].split(":")[0]
        imp = _top_split(text, "->")
        body = text
        if len(imp) == 2:
            if not re.fullmatch(rf"\(?\s*{re.escape(r)}\s*(>=|>)\s*\(?\d+\)?\s*\)?", imp[0].strip()):
                return False
            body = imp[1]
        eq = _top_split(body, "==")
        if len(eq) != 2:
            return False
        m = re.fullmatch(rf"app\((q_\w+),\s*\(?\s*{re.escape(r)}(?:\s*\+\s*(\d+))?\s*\)?\)", eq[0].strip())
        if not m or m.group(1) in owner:
            return False
        q, k = m.group(1), int(m.group(2) or 0)
        owner[q] = True
        rhs = eq[1]
        bare = re.sub(r"app\([^()]*(\([^()]*\))*[^()]*\)", "A", rhs)        # the indices' own − do not count
        if _POLY_OPS.search(bare) or re.search(r"\bnsub\(|\bpow\(\s*[^,]*,\s*[^)]*-", bare):
            return False
        if seqs[q][1] == "nat" and "-" in bare:
            return False
        g = re.search(r"(>=|>)\s*\(?(\d+)", imp[0]) if len(imp) == 2 else None
        lowest = (int(g.group(2)) + (g.group(1) == ">")) if g else 0          # the smallest r the rule applies at
        for j, kk, inner in _zr()._calls(rhs, "app"):
            _, _, t = inner.partition(",")
            mm = re.fullmatch(rf"\(?\s*{re.escape(r)}(?:\s*([+-])\s*(\d+))?\s*\)?", t.strip())
            if not mm:
                return False
            off = int(mm.group(2) or 0) * (-1 if mm.group(1) == "-" else 1)
            if off >= k or lowest + off < 0:
                return False                             # not below the head, or below index 0 where it applies
    return True


def read_seq(raw, conv=False, only=None):
    """zflread's reading of a statement with sequence variables (raw: the dumper's zfl, ℕ marks unread)"""
    zr = _zr()
    import itertools
    import random
    z = zr._reading(raw, conv)
    seqs = {}
    for v in z.get("vars", []):
        if v["type"].startswith("seq:"):
            seqs[v["name"]] = ("nat", v["type"].split(":", 1)[1])
        elif v["type"].startswith("fun:"):
            _, d, cod = v["type"].split(":")
            seqs[v["name"]] = (d, cod)
    scal = {"vars": [v for v in z.get("vars", []) if v["name"] not in seqs], "hyps": []}
    c = z.get("concl", {})
    if "zfl" not in c:
        return {"translated": False, "untr": c.get("untr", "?")}
    if any(v.get("exists") for v in z.get("vars", [])):
        # ∃ k, P k: a point refutes P at ONE k, never ∃ — and EARNED is not given here (MEASURED 2026-11-25: the first
        # version took the ∃ variable for a box variable and "refuted" ∃ k, v 10 = k at k = −3)
        return {"translated": True, "claim": c["zfl"], "ztl": "OPEN", "witness": None,
                "sequence": {"seqs": seqs, "skipped": "a leading ∃: a point cannot refute it"}}
    facts, rules, point_hyps = [], [], []
    for h in z.get("hyps", []):
        if "zfl" not in h:
            return {"translated": True, "claim": c["zfl"], "ztl": "OPEN",
                    "witness": {"skipped": "an untranslated hypothesis: a point cannot be checked against it"},
                    "sequence": {"seqs": seqs}}
        if "rule" in h:
            rules.append((h["rule"], h["zfl"]))
        elif _APP in h["zfl"] and not re.search(r"\bv_\w+", h["zfl"]):
            facts.append(h["zfl"])
        else:
            point_hyps.append(h["zfl"])
            scal["hyps"].append(h)
    b, _ = zr.box(scal)
    for n in list(b):
        if n not in {v["name"] for v in scal["vars"]}:
            del b[n]
    names = list(b)
    pools = []
    for n in names:
        lo, hi, lo_o, hi_o, ty = b[n]
        cands = [Fraction(i) for i in range(-6, 25)] if ty in ("nat", "int") else list(zr._CANDS)
        pools.append([x for x in cands if zr._inside(x, b[n])])
    if any(not p for p in pools):
        return {"translated": True, "claim": c["zfl"], "ztl": "OPEN", "witness": None, "sequence": {"seqs": seqs}}
    texts = [c["zfl"]] + point_hyps
    concrete = [_idx(t) for tx in texts + facts for _, _, inner in zr._calls(tx, "app")
                for t in [inner.partition(",")[2]]]
    need = max([int(i) for i in concrete if i is not None and Fraction(i).denominator == 1 and i >= 0] + [0])
    rnd = random.Random(20261125)
    size = 1
    for p in pools:
        size *= len(p)
    combos = list(itertools.product(*pools)) if size <= POINT_TRIES else \
        list({tuple(rnd.choice(p) for p in pools) for _ in range(POINT_TRIES)})
    if only is not None:                                 # one given point (Lean's reading at the exact refutation)
        combos = [tuple(Fraction(only[n]) for n in names)] if all(n in only for n in names) else []
    rec = existence_by_recursion(seqs, rules)
    cache, found, checked, vac = {}, None, 0, None
    for pt in combos:
        at = dict(zip(names, pt))
        rs = [(bd, _subst(t, at)) for bd, t in rules]
        fs = [_subst(t, at) for t in facts]
        key = (tuple(t for _, t in rs), tuple(fs))
        if key not in cache:
            need_pt = max([need] + [int(x) for x in pt if x.denominator == 1 and 0 <= x <= INDEX_CAP])
            seen = set()
            for tx in [_subst(t, at) for t in texts] + fs:
                for _, _, inner in zr._calls(tx, "app"):
                    a = _idx(inner.partition(",")[2].strip())
                    if a is not None and abs(Fraction(a)) <= 64:
                        seen.add(Fraction(a))
            cache[key] = solve(seqs, fs, rs, need_pt + 2, seen)
        vals, left = cache[key]
        if vals is None:
            return {"translated": False, "untr": "a rule over more than one index"}
        if vals == "vacuous":
            vac = left
            continue
        ok = True
        for t in point_hyps:
            r = _apps(_subst(t, at), vals, _idx)
            if r is None or r[1] or _truth(r[0]) != "EARNED":
                ok = False
                break
        if not ok:
            continue
        r = _apps(_subst(c["zfl"], at), vals, _idx)
        if r is None or r[1]:
            continue                                     # a value the hypotheses do not force
        checked += 1
        v = _truth(r[0])
        if v == "REFUTED":
            used = {}
            for _, _, inner in zr._calls(_subst(c["zfl"], at), "app"):
                q, _, t = inner.partition(",")
                i = _idx(t.strip())
                if i is not None and i in vals.get(q.strip(), {}):
                    used.setdefault(q.strip(), {})[str(i)] = zr._end(vals[q.strip()][i])
            found = {"refuted_at": {n: zr._end(x) for n, x in at.items()}, "values": used,
                     "existence": "recursion" if rec and not left else "conditional"}
            break
    seq = {"seqs": seqs, "points_checked": checked, "existence_by_recursion": rec}
    out = {"translated": True, "claim": c["zfl"], "ztl": "OPEN", "sequence": seq}
    if found:
        out["witness"] = found
    elif vac is not None and checked == 0:
        out["vacuous"] = True
        out["witness"] = {"vacuous_why": str(vac)[:160]}
    else:
        out["witness"] = None
    return out
