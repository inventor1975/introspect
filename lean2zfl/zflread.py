# -*- coding: utf-8 -*-
"""
zflread — a Lean statement READ BY ZTL's numeric floor (2026-11-24, the curator: "делаем"; VR as the frame).

The dumper (JunkDump.lean, `zfl` field) writes the statement's mathematics in ZFL: + - * / exact, ℕ's truncating
`/` and `-` as the operations they abbreviate, √ ln exp … as ZTL's partial functions. This module puts it in front
of the floor:

  BOX       every number variable is a quantity; its interval comes from the hypotheses that bound it by a constant
            (`0 < x` -> (0, inf] — the strict bound is a witnessed gap, zgap.py; `x ≤ 2` -> ... 2]); ℕ is an int on
            [0, inf], ℤ an int, ℝ/ℚ continuous. Every OTHER hypothesis is NOT used: the box is WIDER than the theorem's
            region — sound for what the floor forces (a verdict on the wider box holds on the region), and the reason
            an OPEN may be the box's and not the statement's (`context_unused` counts them).
  CONCL     the conclusion as a ZFL claim over the box: EARNED / REFUTED / OPEN / E (no readings).
  DOMAIN    for every partial operation in the conclusion — ln a, sqrt a, a / d, pow(b, non-integer) — the floor's
            answer to ITS domain over the box: GUARDED (every reading inside), NOWHERE (no reading inside: the value Lean
            computes there is its convention, everywhere), OPEN.

What it is for: Lean has PROVED the statement. Where ZTL reads the same mathematics as REFUTED or without a subject,
the proof rests on a convention (ℕ's 1/3 = 0, log of a negative, x/0 = 0), not on the mathematics the words state.

ZTL is imported from its repository (ZTL_REPO, default the sibling checkout): the floor with the strict bound is
ZTL commit 7db7e7e or later.
"""
import os
import re
import sys

ZTL_REPO = os.environ.get("ZTL_REPO", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "ZTL"))
sys.path.insert(0, os.path.abspath(ZTL_REPO))
import znum                                                       # noqa: E402
from znumjudge import extract_comparisons, judge_sheet_claim, parse_quantities   # noqa: E402

_NUM = r"\(?-?\d+(?:/\d+)?\)?"
_CMP = {"<": "lt", "<=": "le", ">": "gt", ">=": "ge", "==": "eq"}
_FLIP = {"lt": "gt", "le": "ge", "gt": "lt", "ge": "le", "eq": "eq"}


def _strip(s):
    """drop parentheses that wrap the WHOLE text"""
    s = s.strip()
    while s.startswith("(") and s.endswith(")"):
        depth = 0
        for i, c in enumerate(s):
            depth += (c == "(") - (c == ")")
            if depth == 0 and i < len(s) - 1:
                return s
        s = s[1:-1].strip()
    return s


def _conjuncts(s):
    s, out, depth, start = _strip(s), [], 0, 0
    for i, c in enumerate(s):
        depth += (c == "(") - (c == ")")
        if c == "&" and depth == 0:
            out.append(s[start:i]); start = i + 1
    out.append(s[start:])
    return [_strip(x) for x in out]


def _const(s):
    s = s.strip().replace(" ", "")
    while s.startswith("(") and s.endswith(")"):
        s = s[1:-1]
    try:
        from fractions import Fraction
        return Fraction(s)
    except (ValueError, ZeroDivisionError):
        return None


def box(zfl):
    """{name: [lo, hi, lo_open, hi_open, type]} from the variables and the hypotheses bounding one variable by a
    constant; plus the hypotheses left unused."""
    INF = float("inf")
    b = {}
    for v in zfl.get("vars", []):
        lo = 0 if v["type"] == "nat" else -INF
        b[v["name"]] = [lo, INF, False, True, v["type"]]
    unused = 0
    for h in zfl.get("hyps", []):
        if "zfl" not in h:
            unused += 1
            continue
        for c in _conjuncts(h["zfl"]):
            m = re.match(r"^(\S+)\s*(<=|>=|<|>|==)\s*(\S+)$", c.replace("(-", "(-").strip())
            if not m:
                unused += 1
                continue
            l, op, r = m.group(1), _CMP[m.group(2)], m.group(3)
            if l in b and _const(r) is not None:
                name, k = l, _const(r)
            elif r in b and _const(l) is not None:
                name, k, op = r, _const(l), _FLIP[op]
            else:
                unused += 1
                continue
            q = b[name]
            if op in ("gt", "ge", "eq") and (k > q[0] or (k == q[0] and op == "gt")):
                q[0], q[2] = k, op == "gt"
            if op in ("lt", "le", "eq") and (k < q[1] or (k == q[1] and op == "lt")):
                q[1], q[3] = k, op == "lt"
    return b, unused


def _end(x):
    return ("inf" if x > 0 else "-inf") if isinstance(x, float) else (
        str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}")


def sheet(b):
    parts = []
    for n, (lo, hi, lo_o, hi_o, ty) in b.items():
        lb = "(" if lo_o or isinstance(lo, float) else "["
        rb = ")" if hi_o or isinstance(hi, float) else "]"
        parts.append(f"{n}={lb}{_end(lo)},{_end(hi)}{rb} earned:hyp" + (" int" if ty in ("nat", "int") else ""))
    return ", ".join(parts)


def _partials(e, acc):
    """(op, argument tree) for every partial operation in a parsed side"""
    if isinstance(e, tuple):
        op = e[0]
        if op == "ln" or op == "log10":
            acc.append(("ln", e[1]))
        elif op == "sqrt":
            acc.append(("sqrt", e[1]))
        elif op == "div":
            acc.append(("div", e[2]))
        elif op == "pow":
            ex = e[2]
            if not (isinstance(ex, znum.Fraction) and ex.denominator == 1):
                acc.append(("pow", e[1]))
        for a in (e[1] if op == "sum" else e[1:]):
            _partials(a, acc)
    return acc


def domain(op, arg, quantities):
    """GUARDED / NOWHERE / OPEN / E for one partial operation over the box"""
    zero = znum.Fraction(0)
    if op == "div":
        v = znum.compare("eq", arg, zero, quantities)[0]          # d == 0 ?
        return {"T": "NOWHERE", "F": "GUARDED", "Z": "OPEN"}.get(v, "E")
    kind = "lt" if op in ("ln", "pow") else "le"                   # 0 < a  /  0 <= a
    v = znum.compare(kind, zero, arg, quantities)[0]
    return {"T": "GUARDED", "F": "NOWHERE", "Z": "OPEN"}.get(v, "E")


_CANDS = sorted({znum.Fraction(n) for n in range(-4, 11)} | {znum.Fraction(p, q) for p in range(-3, 8)
                for q in (2, 3, 4) if p % q})
WITNESS_TRIES = 300


def _inside(x, q):
    lo, hi, lo_o, hi_o, ty = q
    if ty in ("nat", "int") and x.denominator != 1:
        return False
    return (x > lo or (x == lo and not lo_o)) and (x < hi or (x == hi and not hi_o))


def witness(z, b, seed=20261124):
    """A POINT where every translated hypothesis holds (EARNED there) and the conclusion is REFUTED, or has no
    reading (E): a counterexample to the mathematics the statement writes, or a place where it says nothing. Exact
    at rational points (a transcendental bracket that cannot decide leaves the point unused). None when no
    hypothesis is untranslated and no tried point decides; 'context' when an untranslated hypothesis makes a point
    unverifiable."""
    import itertools
    import random
    if any("zfl" not in h for h in z.get("hyps", [])):
        return {"skipped": "an untranslated hypothesis: a point cannot be checked against it"}
    names = list(b)
    pools = [[x for x in _CANDS if _inside(x, b[n])] for n in names]
    if any(not p for p in pools):
        return None
    rnd = random.Random(seed)
    size = 1
    for p in pools:
        size *= len(p)
    if size <= WITNESS_TRIES:
        combos = list(itertools.product(*pools)) if names else [()]
    else:
        # DRAWN, never listed: the full product of 16 variables' candidates is ~40^16 points (MEASURED 2026-11-24:
        # listing it took the reader to 25-40 GB on 29 Lean Workbook statements)
        seen, combos = set(), []
        while len(combos) < WITNESS_TRIES and len(seen) < 20 * WITNESS_TRIES:
            pt = tuple(rnd.choice(p) for p in pools)
            if pt not in seen:
                seen.add(pt)
                combos.append(pt)
    nosub = None
    for pt in combos:
        text = ", ".join(f"{n}={_end(x)} earned:pt" for n, x in zip(names, pt))
        try:
            qs, marks = parse_quantities(text) if text else ({}, {})
            if not all(judge_sheet_claim(h["zfl"], dict(qs), marks)["disposition"] == "EARNED"
                       for h in z.get("hyps", [])):
                continue
            r = judge_sheet_claim(z["concl"]["zfl"], dict(qs), marks)
        except Exception:
            continue
        at = {n: _end(x) for n, x in zip(names, pt)}
        if r["disposition"] == "REFUTED":
            return {"refuted_at": at}
        if r["disposition"] == "E" and nosub is None:
            nosub = {"no_subject_at": at, "why": r.get("why")}
    # a counterexample outranks a point without a subject: the search goes on after the first E (MEASURED 2026-11-24,
    # lean_workbook_29168: an E at c = 0 — ZTL's pow(0, 7/8), a floor gap, not the statement's — hid the refutation at
    # a = b = c = 1/4)
    return nosub


def _unmark(text, conv):
    """ℕ's marked conventions (the dumper's `ndiv(a, b)`, `nsub(a, b)`) read one way: the MATHEMATICS (conv False:
    exact a / b, a - b) or LEAN'S CONVENTION (conv True: idiv(a, b) — the floor —, max(a - b, 0)). The curator's
    variant В, 2026-11-24: read both, say when a verdict rests on the difference — which the formal text alone cannot
    settle (lean_workbook_plus_26988: the author's ⌊2017/3⌋ is Lean's 2017 / 3)."""
    out, i = [], 0
    while i < len(text):
        m = re.match(r"(ndiv|nsub)\(", text[i:])
        if m and not (i and (text[i - 1].isalnum() or text[i - 1] == "_")):
            name, j = m.group(1), i + len(m.group(0))
            depth, k, comma = 1, j, None
            while depth:
                c = text[k]
                depth += (c == "(") - (c == ")")
                if c == "," and depth == 1 and comma is None:
                    comma = k
                k += 1
            a, b = _unmark(text[j:comma], conv), _unmark(text[comma + 1:k - 1], conv)
            if name == "ndiv":
                out.append(f"idiv({a}, {b})" if conv else f"({a} / {b})")
            else:
                out.append(f"max(({a} - {b}), 0)" if conv else f"({a} - {b})")
            i = k
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def _reading(z, conv):
    import copy
    z = copy.deepcopy(z)
    parts = [z.get("concl", {})] + list(z.get("hyps", []))
    for part in parts:
        if "zfl" in part:
            part["zfl"] = _unmark(part["zfl"], conv)
    if any(_has_fsum(p.get("zfl", "")) for p in parts):
        try:                                             # the box decides a closed form's guard hi >= lo - 1
            b, _ = box(z)
            text = sheet(b)
            qs, marks = parse_quantities(text) if text else ({}, {})
        except Exception:
            qs = marks = None
        for part in parts:
            if _has_fsum(part.get("zfl", "")):
                r = _fsum_reading(part["zfl"], qs, marks)
                if r is None:
                    del part["zfl"]
                    part["untr"] = "a finite sum outside the readable classes"
                else:
                    part["zfl"] = r
    return z


def _marked(z):
    return any(re.search(r"\b(ndiv|nsub)\(", p.get("zfl", "")) for p in [z.get("concl", {})] + list(z.get("hyps", [])))


def _core_arrows(z):
    """`<->` -> the core's `↔` in every formula: the comparison reader takes the `<` of `<->` for a comparison
    (MEASURED 2026-11-24: 20 of 810 readings stopped at "stray character '<'")"""
    import copy
    z = copy.deepcopy(z)
    for part in [z.get("concl", {})] + list(z.get("hyps", [])):
        if "zfl" in part:
            part["zfl"] = part["zfl"].replace("<->", "↔")
    return z


def exists_witness(z, b, seed=20261124, only=None):
    """a point of the box where every translated hypothesis holds and the conclusion is EARNED (the ∃'s witness);
    `only`: pin just these names, the others keep their whole box (a witness uniform in them)"""
    import itertools
    import random
    names = list(b) if only is None else [n for n in b if n in only]
    rest = "" if only is None else sheet({n: q for n, q in b.items() if n not in only})
    pools = [[x for x in _CANDS if _inside(x, b[n])] for n in names]
    if any(not p for p in pools):
        return None
    rnd = random.Random(seed)
    combos = list(itertools.product(*pools)) if names else [()]
    if len(combos) > WITNESS_TRIES:
        combos = rnd.sample(combos, WITNESS_TRIES)
    for pt in combos:
        text = ", ".join([f"{n}={_end(x)} earned:pt" for n, x in zip(names, pt)] + ([rest] if rest else []))
        try:
            qs, marks = parse_quantities(text) if text else ({}, {})
            if all(judge_sheet_claim(h["zfl"], dict(qs), marks)["disposition"] == "EARNED" for h in z.get("hyps", [])
                   if "zfl" in h) and judge_sheet_claim(z["concl"]["zfl"], dict(qs), marks)["disposition"] == "EARNED":
                return {n: _end(x) for n, x in zip(names, pt)}
        except Exception:
            continue
    return None


# ------------------------------------------------------------------ LEAN'S OWN SEMANTICS, a third reading
# (2026-11-24, the curator on aime_1984_p5: "log x = log|x| — это в Lean; а прибором ZFL/ZTL мы видим?"). The exact
# reading cannot see a statement that is false ONLY in Lean: there, log of a negative has no value and the hypotheses
# do not hold. This reading rewrites the statement into Lean's conventions — log x = log|x| and log 0 = 0, √x = 0 for
# x ≤ 0, x / 0 = 0, n / 0 = 0, n % 0 = n (ℕ's floor and truncation: the convention reading) — with ZTL's `ifpos`
# (a decided condition reads only its branch), and searches a point where the hypotheses hold and the conclusion fails
# IN LEAN. rpow of a negative base (Lean: exp(y log x) cos(y pi)) is not rewritten: it stays the exact reading.
from fractions import Fraction as _Fr  # noqa: E402

_ZERO = _Fr(0)


def _lean_tree(e):
    if isinstance(e, tuple):
        op = e[0]
        args = [[_lean_tree(x) for x in e[1]]] if op == "sum" else [_lean_tree(x) for x in e[1:]]
        e = (op, *args)
        neg = lambda x: ("sub", _ZERO, x)                                    # noqa: E731
        if op in ("ln", "log10"):
            x = e[1]
            return ("ifpos", x, (op, x), ("ifpos", neg(x), (op, neg(x)), _ZERO))
        if op == "sqrt":
            return ("ifpos", e[1], e, _ZERO)
        if op == "div":
            d = e[2]
            return ("ifpos", d, e, ("ifpos", neg(d), e, _ZERO))
        if op == "idiv":
            return ("ifpos", e[2], e, _ZERO)
        if op == "mod":
            return ("ifpos", e[2], e, e[1])
    return e


def _print(e):
    if isinstance(e, _Fr):
        return (f"(0 - {_print(-e)})" if e < 0 else
                (str(e.numerator) if e.denominator == 1 else f"({e.numerator} / {e.denominator})"))
    if isinstance(e, (int, float)):
        return str(e)
    if isinstance(e, str):
        return e
    op = e[0]
    sym = {"add": "+", "sub": "-", "mul": "*", "div": "/"}
    if op in sym:
        return f"({_print(e[1])} {sym[op]} {_print(e[2])})"
    if op == "sum":
        return "sum(" + ", ".join(_print(x) for x in e[1]) + ")"
    return f"{op}(" + ", ".join(_print(x) for x in e[1:]) + ")"


def _lean_formula(text, qs):
    """a ZFL formula rewritten into Lean's conventions, comparison by comparison"""
    core, atoms = extract_comparisons(text, dict(qs))
    sign = {"le": "<=", "lt": "<", "eq": "=="}
    out = core
    for name, (kind, e1, e2, _) in sorted(atoms.items(), key=lambda kv: -len(kv[0])):
        out = out.replace(f" {name} ", f" ({_print(_lean_tree(e1))} {sign[kind]} {_print(_lean_tree(e2))}) ")
    return out


_LEAN_POOL = sorted(set(_CANDS) | {_Fr(sg * k ** j) for sg in (1, -1) for k in (2, 3, 5) for j in range(0, 11)
                                   if k ** j <= 1024})
LEAN_EXHAUSTIVE = 6400


def lean_witness(zc, b):
    """a point where, in LEAN'S semantics, every hypothesis is EARNED and the conclusion REFUTED; or None. zc is the
    convention reading of the statement (ℕ's / and − as Lean has them)."""
    import itertools
    import random
    if any("zfl" not in h for h in zc.get("hyps", [])):
        return None
    names = list(b)
    pools = [[x for x in _LEAN_POOL if _inside(x, b[n])] for n in names]
    if any(not p for p in pools):
        return None
    size = 1
    for p in pools:
        size *= len(p)
    if size <= LEAN_EXHAUSTIVE:
        combos = list(itertools.product(*pools)) if names else [()]
    else:
        rnd = random.Random(20261124)
        combos = list({tuple(rnd.choice(p) for p in pools) for _ in range(WITNESS_TRIES)})
    for pt in combos:
        text = ", ".join(f"{n}={_end(x)} earned:pt" for n, x in zip(names, pt))
        try:
            qs, marks = parse_quantities(text) if text else ({}, {})
            if not all(judge_sheet_claim(_lean_formula(h["zfl"], qs), dict(qs), marks)["disposition"] == "EARNED"
                       for h in zc.get("hyps", [])):
                continue
            if judge_sheet_claim(_lean_formula(zc["concl"]["zfl"], qs), dict(qs), marks)["disposition"] == "REFUTED":
                return {n: _end(x) for n, x in zip(names, pt)}
        except Exception:
            continue
    return None


# ------------------------------------------------------------------ THE CONVENTIONS AS DIRTY PARAMETERS
# (2026-11-25, the curator: "Надо делать как я понял… будет ровненько"; the article on 1 + 2 + 3 + … = −1/12). A Lean
# notation hides a choice no one names: which summation method ∑' is, what x/0 and log of a negative are, whether ℕ's
# − and / truncate. ZTL reads each choice as a DIRTY PARAMETER of the claim and judges the claim under every reading:
#     N  ℕ's arithmetic           exact | lean (floor, truncation)
#     P  partial functions        none (no value at the edge) | lean (x/0 = 0, log|x|, √ of x ≤ 0 = 0)
#     M  summation method of ∑'   limit | mathlib | abel | cesaro | zeta        (zsummation: P(n), (−1)^n P(n) series)
# True under every reading: EARNED; false under every one (at an admissible point): REFUTED; otherwise the claim
# DEPENDS on the convention, and the table says which reading gives what. (First version: div, log and √ are one
# parameter P; a per-occurrence choice — the IF STABLE question for conventions — is not read yet.)
import zsummation as _zs  # noqa: E402

_NOVALUE = "nv_novalue"
_zfun_words = {"exp", "ln", "log10", "sin", "cos", "tan", "atan", "pow", "min", "max", "sqrt", "ifpos", "idiv", "mod",
               "dvd", "fact", "choose", "sum", "integral", "pi"}           # a quantity with no reading: a series with no value under a method reads E


def _calls(text, name):
    """(start, end, inner) for every top-level call name(...) in text"""
    out, i = [], 0
    while True:
        j = text.find(name + "(", i)
        if j < 0:
            return out
        if j and (text[j - 1].isalnum() or text[j - 1] == "_"):
            i = j + 1
            continue
        depth, k = 1, j + len(name) + 1
        while depth:
            depth += (text[k] == "(") - (text[k] == ")")
            k += 1
        out.append((j, k, text[j + len(name) + 1:k - 1]))
        i = k


def _series_poly(var, body):
    """the body of series(var, body) as (P, r) — Σ P(n) r^n, P {degree: Fraction}, r a Fraction or a tree in the
    claim's other variables (a ratio that is a variable) — or None. (−1)^n is r = −1; c^(a n + b) gives r = c^a."""
    try:
        from znumjudge import _parse_arith
        from znum import names_in, _ev as _zev
        names = {w: {} for w in re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", body)
                 if w not in _zfun_words}
        names[var] = {}
        tree = _parse_arith(body, names)
    except Exception:
        return None
    ONE = _Fr(1)

    def fold(t):
        """a subtree with no name at all, read to its exact value by the floor (1/2, idiv(1, 2), 2^3)"""
        if not isinstance(t, tuple) or names_in(t):
            return t
        try:
            iv = _zev(t, {})[0]
        except Exception:
            return t
        if iv is not None and iv[0] == iv[1] and not isinstance(iv[0], float):
            return _Fr(iv[0])
        return t

    def walk(t):
        if isinstance(t, tuple):
            args = [[walk(x) for x in t[1]]] if t[0] == "sum" else [walk(x) for x in t[1:]]
            return fold((t[0], *args))
        return t
    tree = walk(tree)

    def rmul(a, b):
        if isinstance(a, _Fr) and isinstance(b, _Fr):
            return a * b
        if a == ONE:
            return b
        if b == ONE:
            return a
        return ("mul", a, b)

    def rinv(a):
        return 1 / a if isinstance(a, _Fr) else ("div", ONE, a)

    def lin(t):
        """t as a n + b with integers a >= 1, b, or None"""
        if t == var:
            return (1, 0)
        if isinstance(t, tuple) and t[0] in ("add", "sub") and isinstance(t[2], _Fr) and t[2].denominator == 1:
            inner = lin(t[1])
            if inner:
                return (inner[0], inner[1] + (int(t[2]) if t[0] == "add" else -int(t[2])))
        if isinstance(t, tuple) and t[0] == "mul" and isinstance(t[1], _Fr) and t[1].denominator == 1 and t[1] > 0:
            inner = lin(t[2])
            if inner:
                return (inner[0] * int(t[1]), inner[1] * int(t[1]))
        return None

    def poly(t):
        if isinstance(t, (_Fr, int)):
            return ({0: _Fr(t)}, ONE)
        if t == var:
            return ({1: ONE}, ONE)
        if not isinstance(t, tuple):
            return None
        if var not in names_in(t):                       # a factor free of n: a constant, or a symbolic one
            return None
        op = t[0]
        if op in ("add", "sub"):
            a, b = poly(t[1]) if var in names_in(t[1]) or isinstance(t[1], _Fr) else None, \
                poly(t[2]) if var in names_in(t[2]) or isinstance(t[2], _Fr) else None
            if a is None or b is None:
                return None
            if a[0] and b[0] and a[1] != b[1]:
                return None
            r = a[1] if a[0] else b[1]
            out = dict(a[0])
            for k, v in b[0].items():
                out[k] = out.get(k, 0) + (v if op == "add" else -v)
            return ({k: v for k, v in out.items() if v != 0}, r)
        if op == "mul":
            for x, y in ((t[1], t[2]), (t[2], t[1])):
                if isinstance(x, _Fr):
                    b = poly(y)
                    return None if b is None else ({k: v * x for k, v in b[0].items()}, b[1])
            a, b = poly(t[1]), poly(t[2])
            if a is None or b is None:
                return None
            out = {}
            for i, u in a[0].items():
                for j, v in b[0].items():
                    out[i + j] = out.get(i + j, 0) + u * v
            return ({k: v for k, v in out.items() if v != 0}, rmul(a[1], b[1]))
        if op == "div":
            a = poly(t[1]) if (var in names_in(t[1])) else ({0: _Fr(t[1])}, ONE) if isinstance(t[1], _Fr) else None
            if isinstance(t[2], _Fr):
                return None if a is None else ({k: v / t[2] for k, v in a[0].items()}, a[1])
            b = poly(t[2])
            if a is None or b is None or set(b[0]) != {0}:
                return None
            return ({k: v / b[0][0] for k, v in a[0].items()}, rmul(a[1], rinv(b[1])))
        if op == "pow":
            ab = lin(t[2])
            base = t[1]
            if ab is None or var in names_in(base):
                return None
            a, b = ab
            if isinstance(base, _Fr):
                return ({0: base ** b}, base ** a)
            if b != 0:
                return None                               # a symbolic coefficient base^b: not read
            return ({0: ONE}, base if a == 1 else ("pow", base, _Fr(a)))
        return None
    # ℕ's FLOOR MAKES A FINITE SERIES (2026-11-25, Lean Workbook: ∑' i, 1 / 2^i in ℕ is 1 + 0 + 0 + …):
    # idiv(A(n), b^(a n + e)), b >= 2 an integer, a >= 1, e >= 0, A a polynomial with non-negative coefficients. Once
    # b^(a n0 + e) > A(n0) at some n0 >= 1.45 deg A, every later term is 0: the divisor at least doubles each step and
    # A(n+1)/A(n) <= (1 + 1/n)^deg <= 2 there — so the sum is the finite sum of the first terms, under EVERY method.
    if isinstance(tree, tuple) and tree[0] == "idiv" and isinstance(tree[2], tuple) and tree[2][0] == "pow":
        b, ab = tree[2][1], lin(tree[2][2])
        num = poly(tree[1]) if var in names_in(tree[1]) else (({0: _Fr(tree[1])}, ONE) if isinstance(tree[1], _Fr) else None)
        if (isinstance(b, _Fr) and b.denominator == 1 and b >= 2 and ab and ab[0] >= 1 and ab[1] >= 0 and num
                and num[1] == ONE and all(c >= 0 and c.denominator == 1 for c in num[0].values())):
            A = lambda n: int(sum(c * n ** k for k, c in num[0].items()))          # noqa: E731
            deg = max(num[0]) if num[0] else 0
            start = int(1.45 * deg) + 1
            for n0 in range(start, start + 10000):
                if int(b) ** (ab[0] * n0 + ab[1]) > A(n0):
                    total = sum(A(n) // int(b) ** (ab[0] * n + ab[1]) for n in range(n0))
                    return ("finite", _Fr(total))
    r = poly(tree)
    if r is None or not r[0]:
        return None if r is None else ({}, ONE)
    return r


def _sum_reading(text, method):
    """every series(...) in text replaced by its value under `method` — exact for a rational ratio, a piecewise
    ZFL expression for a ratio that is a variable — or by a no-value quantity; None if a series is not readable"""
    out, last = [], 0
    for j, k, inner in _calls(text, "series"):
        var, _, body = inner.partition(",")
        pr = _series_poly(var.strip(), body.strip())
        if pr is None:
            return None
        out.append(text[last:j])
        if pr[0] == "finite":                            # finitely many non-zero terms: every method sums them
            out.append(_print(pr[1]))
            last = k
            continue
        p, r = pr
        if isinstance(r, _Fr):
            v = _zs.value_geo(p, r, method)
            out.append(_NOVALUE if v is None else _print(v))
        else:
            R = _print(r)
            closed = _zs.closed_text(p, R)
            inside = f"(1 - max({R}, (0 - {R})))"         # > 0 exactly when |r| < 1
            if method == "zeta":
                out.append(closed)                       # the continuation (no value at r = 1: a division by 0)
            elif method == "mathlib":
                out.append(f"ifpos({inside}, {closed}, 0)")
            else:                                        # limit, abel, cesaro: a value only where |r| < 1
                out.append(f"ifpos({inside}, {closed}, {_NOVALUE})")
        last = k
    out.append(text[last:])
    return "".join(out)


def _zeta_exact(text):
    """zeta(k) at an integer k ≤ 0 -> its exact value (ζ(−j) = −B_{j+1}/(j+1), ζ(0) = −1/2); None if another zeta"""
    out, last = [], 0
    for j, k, inner in _calls(text, "zeta"):
        try:
            from znumjudge import _parse_arith
            from znum import _ev_exact
            v = _ev_exact(_parse_arith(inner, {}), {})
        except Exception:
            return None
        if not isinstance(v, _Fr) or v.denominator != 1 or v > 0:
            return None
        out += [text[last:j], _print(_zs.zeta_neg(int(-v)))]
        last = k
    out.append(text[last:])
    return "".join(out)


# FINITE SUMS (2026-11-25): the dumper's fsum(i, lo, hi, body) / fprod(...) is Lean's Finset.sum / Finset.prod over an
# interval of ℕ or ℤ, hi INCLUSIVE. Ordinary mathematics — no convention and no method: the empty interval sums to 0
# (multiplies to 1). Read three ways, each exact:
#   * concrete bounds, at most _FSUM_EXPAND terms: written out term by term (any body, other variables included);
#   * concrete bounds, more terms, a body with no other name: summed exactly term by term (at most _FSUM_EXACT);
#   * otherwise Σ P(i) r^i with r rational ≠ 0: zsummation's closed form (Faulhaber for r = 1, the telescoping Q for
#     r ≠ 1), valid for hi ≥ lo − 1 — that guard is DECIDED on the box by the floor itself; undecided, it stays an
#     ifpos the floor reads as a mark. Anything else (a product with a variable bound, a body with other names under a
#     variable bound, ℕ's floor in the body): not read — the part goes untranslated, never guessed.
_FSUM_EXPAND = 300
_FSUM_EXACT = 20000
_NAME = r"\b[A-Za-z_][A-Za-z0-9_]*\b"


def _split_top(inner):
    parts, depth, last = [], 0, 0
    for k, ch in enumerate(inner):
        depth += (ch == "(") - (ch == ")")
        if ch == "," and depth == 0:
            parts.append(inner[last:k])
            last = k + 1
    parts.append(inner[last:])
    return [x.strip() for x in parts]


def _exact_of(text):
    """the exact rational value of a text with no name, or None"""
    try:
        from znumjudge import _parse_arith
        from znum import _ev_exact
        v = _ev_exact(_parse_arith(text, {}), {})
    except Exception:
        v = None
    if not isinstance(v, _Fr):                           # min / max / idiv …: the floor's interval, when pinned
        try:
            from znumjudge import _parse_arith
            iv = znum._ev(_parse_arith(text, {}), {})[0]
        except Exception:
            return None
        if iv is None or iv[0] != iv[1] or isinstance(iv[0], float):
            return None
        v = _Fr(iv[0])
    return v


def _ptext(p, x):
    terms = [f"({_print(c)} * ({x})**{k})" if k else _print(c) for k, c in sorted(p.items())]
    return "(" + " + ".join(terms) + ")" if terms else "0"


def _fsum_one(name, var, lo, hi, body, qs, marks):
    a, b = _exact_of(lo), _exact_of(hi)
    a = int(a) if a is not None and a.denominator == 1 else None
    b = int(b) if b is not None and b.denominator == 1 else None
    empty = "0" if name == "fsum" else "1"
    others = [w for w in re.findall(_NAME, body) if w not in _zfun_words and w != var]
    sub = lambda i: re.sub(rf"\b{re.escape(var)}\b", f"({i})", body)          # noqa: E731
    if a is not None and b is not None:
        if b < a:
            return empty
        if b - a + 1 <= _FSUM_EXPAND:
            return "(" + (" + " if name == "fsum" else " * ").join(f"({sub(i)})" for i in range(a, b + 1)) + ")"
        if not others and b - a + 1 <= _FSUM_EXACT:
            acc = _Fr(0) if name == "fsum" else _Fr(1)
            for i in range(a, b + 1):
                v = _exact_of(sub(i))
                if v is None:
                    return None
                acc = acc + v if name == "fsum" else acc * v
            return _print(acc)
    if name != "fsum":
        return None
    pr = _series_poly(var, body)
    if pr is None or pr[0] == "finite":
        return None
    p, r = pr
    if not isinstance(r, _Fr) or r == 0:
        return None
    if r == 1:
        F = _zs.faulhaber(p)
        closed = f"({_ptext(F, hi)} - {_ptext(F, f'({lo}) - 1')})"
    else:
        Q, R = _zs.geo_q(p, r), _print(r)
        closed = f"(({_ptext(Q, lo)} * pow({R}, {lo})) - ({_ptext(Q, f'({hi}) + 1')} * pow({R}, (({hi}) + 1))))"
    if a is not None and b is not None:
        return closed                                    # b >= a here
    guard = f"((({hi}) - ({lo})) + 1)"
    if qs is not None:
        try:
            if judge_sheet_claim(f"{guard} >= 0", dict(qs), marks)["disposition"] == "EARNED":
                return closed
            if judge_sheet_claim(f"{guard} < 0", dict(qs), marks)["disposition"] == "EARNED":
                return empty
        except Exception:
            pass
    return f"ifpos(({guard} + (1 / 2)), {closed}, 0)"


def _fsum_reading(text, qs=None, marks=None):
    """every fsum / fprod in text read as ordinary mathematics (innermost first); None if one cannot be read"""
    for name in ("fsum", "fprod"):
        out, last = [], 0
        for j, k, inner in _calls(text, name):
            parts = _split_top(inner)
            if len(parts) != 4:
                return None
            var, rest = parts[0], [_fsum_reading(x, qs, marks) for x in parts[1:]]
            if None in rest:
                return None
            r = _fsum_one(name, var, *rest, qs, marks)
            if r is None:
                return None
            out += [text[last:j], f"({r})"]
            last = k
        out.append(text[last:])
        text = "".join(out)
    return text


def _has_fsum(t):
    return bool(re.search(r"\bf(sum|prod)\(", t))


def _map_texts(z, f):
    import copy
    z = copy.deepcopy(z)
    for part in [z.get("concl", {})] + list(z.get("hyps", [])):
        if "zfl" in part:
            r = f(part["zfl"])
            if r is None:
                return None
            part["zfl"] = r
    return z


def readings(raw):
    """the claim under every reading of its conventions: [{N, P, M, verdict, at}] and the overall disposition"""
    texts = [raw.get("concl", {}).get("zfl", "")] + [h.get("zfl", "") for h in raw.get("hyps", [])]
    has = lambda w: any(w in t for t in texts)                       # noqa: E731
    Ns = ("exact", "lean") if (has("ndiv(") or has("nsub(")) else ("exact",)
    Ps = ("none", "lean") if any(re.search(r"/|ln\(|log10\(|sqrt\(", t) for t in texts) else ("none",)
    Ms = _zs.METHODS if has("series(") else (None,)
    if len(Ns) * len(Ps) * len(Ms) == 1:
        return None
    rows = []
    for n_ in Ns:
        for p_ in Ps:
            for m_ in Ms:
                z = _reading(raw, n_ == "lean")
                z = _map_texts(z, _zeta_exact) if z else None
                if z is not None and m_ is not None:
                    z = _map_texts(z, lambda t: _sum_reading(t, m_))
                if z is None:
                    rows.append({"N": n_, "P": p_, "M": m_, "verdict": "UNTR"})
                    continue
                r = _read(z, partial_lean=(p_ == "lean"))
                w = r.get("witness") or {}
                v = ("T" if r.get("ztl") == "EARNED" else "F" if "refuted_at" in w else
                     "E" if r.get("ztl") == "E" else "Z")
                rows.append({"N": n_, "P": p_, "M": m_, "verdict": v, "at": w.get("refuted_at")})
    # a parameter whose readings change nothing is dropped from the table (a literal −1/12 is not a division at 0)
    for dim in ("P", "N"):
        others = [k for k in ("N", "P", "M") if k != dim]
        groups = {}
        for r in rows:
            groups.setdefault(tuple(r[k] for k in others), set()).add(r["verdict"])
        if all(len(v) == 1 for v in groups.values()):
            seen, kept = set(), []
            for r in rows:
                key = tuple(r[k] for k in others)
                if key not in seen:
                    seen.add(key)
                    kept.append({**r, dim: "any"})
            rows = kept
    vs = {r["verdict"] for r in rows}
    if vs == {"UNTR"}:
        return {"rows": rows, "overall": "UNTR"}
    partial = "UNTR" in vs                               # an unread reading does not vote; it is said
    vs.discard("UNTR")
    overall = ("EARNED" if vs == {"T"} else "REFUTED" if vs == {"F"} else "E" if vs == {"E"} else
               "DEPENDS" if ({"T", "F"} & vs) else "OPEN")
    return {"rows": rows, "overall": overall, "partial": partial}


def read(t):
    """the floor's reading of one dumped theorem: the MATHEMATICS (ℕ's / and − exact); where the statement uses ℕ's
    conventions, also LEAN'S reading of them (`ztl_conv`), and the mark `rests_on_nat_convention` when the mathematics
    is refuted (or refuted at a point) and Lean's convention holds there"""
    raw = _core_arrows(t.get("zfl") or {})
    if raw and not raw.get("untr_vars") and any(v["type"].startswith("seq:") for v in raw.get("vars", [])):
        # SEQUENCES (2026-11-25, the curator's "да"): computed from the hypotheses that define them, refuted at a
        # point, never EARNED (zflseq). Lean's ℕ conventions read as the second reading, at the same point.
        import zflseq
        out = zflseq.read_seq(raw, False)
        w = out.get("witness") or {}
        if _marked(raw):
            if "refuted_at" in w:
                lr = zflseq.read_seq(raw, True, only=w["refuted_at"])
                lw = lr.get("witness") or {}
                # only a CHECKED point counts: a Lean reading that could not compute the values says nothing
                w["conv_at_point"] = ("REFUTED" if "refuted_at" in lw else "HOLDS"
                                      if lr.get("sequence", {}).get("points_checked") else "UNREAD")
                if w["conv_at_point"] == "HOLDS":
                    out["rests_on_nat_convention"] = True
            else:
                lw = zflseq.read_seq(raw, True).get("witness") or {}
                if "refuted_at" in lw:
                    out["lean_refuted_at"] = lw["refuted_at"]
        return out
    if raw and not raw.get("untr_vars") and "zfl" in raw.get("concl", {}) and \
            any(w in p.get("zfl", "") for p in [raw["concl"]] + list(raw.get("hyps", [])) for w in ("series(", "zeta(")):
        # a series or zeta: no single "mathematical" reading exists — the method is the claim's dirty parameter
        rd = readings(raw)
        if rd is None:                                   # zeta at integer points only: one reading
            z = _map_texts(_reading(raw, False), _zeta_exact)
            if z is None:
                return {"translated": False, "untr": "zeta at a point that is not an integer ≤ 0"}
            return _read(z)
        if rd["overall"] == "UNTR":                      # no method could read the series: not translated
            return {"translated": False, "untr": "a series outside the readable classes (Σ P(n) r^n)"}
        return {"translated": True, "claim": raw["concl"]["zfl"], "ztl": rd["overall"], "readings": rd["rows"],
                "readings_partial": rd.get("partial", False)}
    math = _reading(raw, False) if raw else raw
    out = _read(math)
    if out.get("translated") and not out.get("exists") and "refuted_at" not in (out.get("witness") or {}) \
            and any(d[1] in ("OPEN", "NOWHERE") for d in out.get("domain", [])):
        # the mathematics is not refuted, and some partial operation is not guarded: is the statement false IN LEAN?
        try:
            zc = _reading(raw, True)
            bc, _ = box(zc)
            lw = lean_witness(zc, bc)
            if lw is not None:
                out["lean_refuted_at"] = lw
        except Exception as ex:
            out["lean_reading"] = f"UNREAD: {ex}"[:120]
    if out.get("translated"):
        # the hypotheses in the exact reading: what a certificate must show at a witness point (certify.py)
        out["hyps_zfl"] = [h["zfl"] for h in math.get("hyps", []) if "zfl" in h]
        out["hyps_untr"] = sum(1 for h in math.get("hyps", []) if "zfl" not in h)
    if out.get("translated") and _marked(raw):
        zc = _reading(raw, True)
        try:
            b, _ = box(zc)
            qs, marks = parse_quantities(sheet(b)) if b else ({}, {})
            out["ztl_conv"] = judge_sheet_claim(zc["concl"]["zfl"], qs, marks)["disposition"]
            w = out.get("witness") or {}
            if "refuted_at" in w:
                at = ", ".join(f"{n}={v} earned:pt" for n, v in w["refuted_at"].items())
                q2, m2 = parse_quantities(at) if at else ({}, {})
                w["conv_at_point"] = judge_sheet_claim(zc["concl"]["zfl"], q2, m2)["disposition"]
            if w.get("conv_at_point") == "EARNED":       # only at an admissible point (the empty one included)
                out["rests_on_nat_convention"] = True
        except Exception as ex:                          # the second reading is information; it never sinks the first
            out["ztl_conv"] = f"UNREAD: {ex}"[:120]
    return out


def _read(z, partial_lean=False):
    """the floor's reading of one translated statement (no marks left); `partial_lean`: partial functions read as
    Lean has them (x/0 = 0, log|x|, √ of x ≤ 0 = 0)"""
    if not z:
        return {"translated": False, "untr": "no zfl field (dumper before 2026-11-24)"}
    if "untr_vars" in z:
        return {"translated": False, "untr": z["untr_vars"]}
    c = z.get("concl", {})
    if "zfl" not in c:
        return {"translated": False, "untr": c.get("untr", "?")}
    b, unused = box(z)
    text = sheet(b)
    if any(_NOVALUE in (h.get("zfl") or "") for h in [c] + list(z.get("hyps", []))):
        # a series with no value under the method in force: a quantity with NO reading (ZTL: E wherever it is read)
        text = (text + ", " if text else "") + f"{_NOVALUE}=(1,1] earned:convention"
    try:
        qs, marks = parse_quantities(text) if text else ({}, {})
        if partial_lean:
            z = _map_texts(z, lambda t: _lean_formula(t, qs))
            c = z["concl"]
        r = judge_sheet_claim(c["zfl"], qs, marks)
        doms = []
        # the conclusion AND the hypotheses (2026-11-24: aime_1984_p5's logarithms are all in its hypotheses, over a
        # box that lets a be negative — the domain check had looked at the conclusion only). (op, verdict, where)
        for where, text_ in [("concl", c["zfl"])] + [(f"hyp{i + 1}", h["zfl"]) for i, h in enumerate(z.get("hyps", []))
                                                      if "zfl" in h]:
            try:
                _, atoms = extract_comparisons(text_, dict(qs))
            except Exception:
                continue
            for _, (kind, e1, e2, chunk) in atoms.items():
                for op, arg in _partials(e1, []) + _partials(e2, []):
                    try:
                        doms.append((op, domain(op, arg, qs), where))
                    except Exception as ex:                   # an argument the floor cannot read: say so
                        doms.append((op, f"UNREAD: {ex}"[:80], where))
    except Exception as ex:
        return {"translated": True, "claim": c["zfl"], "sheet": text, "ztl": "UNREAD",
                "why": f"{type(ex).__name__}: {ex}"[:200]}
    out = {"translated": True, "claim": c["zfl"], "sheet": text, "ztl": r["disposition"],
           "why": r.get("why"), "domain": doms, "context_unused": unused}
    ex_vars = [v["name"] for v in z.get("vars", []) if v.get("exists")]
    if ex_vars:
        # ∃ (Brouwer's, VR's): EARNED over the box is stronger than ∃ and REFUTED over it leaves no witness — both
        # stand; OPEN looks for a WITNESS where the conclusion is EARNED. A refuting point refutes nothing here, so
        # no counterexample search. With a universal variable not pinned to a point, the witness would have to depend
        # on it: OPEN stays OPEN.
        out["exists"] = ex_vars
        univ = [v["name"] for v in z.get("vars", []) if not v.get("exists")]
        pinned = all(b[n][0] == b[n][1] and not isinstance(b[n][0], float) for n in univ)
        if r["disposition"] == "OPEN" and pinned:
            w = exists_witness(z, b)
            if w:
                out["exists_witness"] = w
                out["ztl"] = "EARNED"
        elif r["disposition"] == "OPEN":
            # A UNIFORM WITNESS (2026-11-25): pin only the ∃ variables, keep every universal's whole box — EARNED there
            # is ∀ … ∃ with one witness for all, stronger than the claim, so it stands (∃x∀y ⊨ ∀y∃x, zfo-valid)
            w = exists_witness(z, b, only=ex_vars)
            if w:
                out["exists_witness"] = w
                out["exists_uniform"] = True
                out["ztl"] = "EARNED"
        return out
    if r["disposition"] in ("OPEN", "E", "REFUTED"):
        # A REFUTED CONCLUSION IS NOT A FALSE STATEMENT until a point satisfies the hypotheses (MEASURED 2026-11-24:
        # lean_workbook_53067's hypothesis IS its conclusion — both false, the statement vacuously true; Lean's kernel
        # refused the certificate "hypotheses ∧ ¬ conclusion"). A refutation counts only with `refuted_at`, the
        # empty point included for a statement with no variables; hypotheses refuted over the box: `vacuous`.
        w = witness(z, b)
        if w:
            out["witness"] = w
        if r["disposition"] == "REFUTED" and "refuted_at" not in (w or {}):
            hs = []
            for h in z.get("hyps", []):
                if "zfl" in h:
                    try:
                        hs.append(judge_sheet_claim(h["zfl"], dict(qs), marks)["disposition"])
                    except Exception:
                        hs.append("?")
            out["vacuous"] = any(d == "REFUTED" for d in hs)
            out["admissible_unknown"] = not out["vacuous"]
    return out


def read_safe(t, mem_bytes=3 << 30, seconds=120):
    """`read` in a forked child under a memory and a time limit. MEASURED 2026-11-24: on some Lean Workbook statements
    the exact rational arithmetic of a reading grew to 25-40 GB in the scanning process itself (the kernel's OOM log:
    python3, anon-rss 39 GB) and took the whole scan down; here such a statement costs its own row only, and says so."""
    import multiprocessing as mp
    import resource
    ctx = mp.get_context("fork")
    rd, wr = ctx.Pipe(duplex=False)

    def work():
        # the limit is ON TOP of what the forked child already maps (MEASURED 2026-11-24: a flat 3 GB inside a scan that
        # holds 29750 proofs and pyarrow left nothing — 15 of 1000 readings died as an empty MemoryError at once)
        try:
            base = int(open("/proc/self/statm").read().split()[0]) * resource.getpagesize()
        except OSError:
            base = 0
        resource.setrlimit(resource.RLIMIT_AS, (base + mem_bytes, base + mem_bytes))
        try:
            wr.send(read(t))
        except MemoryError:
            wr.send({"translated": True, "ztl": "UNREAD", "why": f"the reading ran past {mem_bytes >> 30} GB"})
        except BaseException as ex:                       # noqa: BLE001 — every failure becomes the row's answer
            wr.send({"translated": True, "ztl": "UNREAD", "why": f"{type(ex).__name__}: {ex}"[:200]})

    p = ctx.Process(target=work, daemon=True)
    p.start()
    res = rd.recv() if rd.poll(seconds) else {"translated": True, "ztl": "UNREAD",
                                              "why": f"no answer in {seconds} s"}
    p.join(1)
    if p.is_alive():
        p.kill()
        p.join()
    return res


if __name__ == "__main__":
    import json
    for line in sys.stdin:
        if line.startswith("LEAN2ZFL "):
            t = json.loads(line[len("LEAN2ZFL "):])
            print(t["name"], json.dumps(read(t), ensure_ascii=False, default=str))
