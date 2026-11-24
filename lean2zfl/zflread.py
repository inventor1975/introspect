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
    for part in [z.get("concl", {})] + list(z.get("hyps", [])):
        if "zfl" in part:
            part["zfl"] = _unmark(part["zfl"], conv)
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


def read(t):
    """the floor's reading of one dumped theorem: the MATHEMATICS (ℕ's / and − exact); where the statement uses ℕ's
    conventions, also LEAN'S reading of them (`ztl_conv`), and the mark `rests_on_nat_convention` when the mathematics
    is refuted (or refuted at a point) and Lean's convention holds there"""
    raw = _core_arrows(t.get("zfl") or {})
    math = _reading(raw, False) if raw else raw
    out = _read(math)
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


def _read(z):
    """the floor's reading of one translated statement (no marks left)"""
    if not z:
        return {"translated": False, "untr": "no zfl field (dumper before 2026-11-24)"}
    if "untr_vars" in z:
        return {"translated": False, "untr": z["untr_vars"]}
    c = z.get("concl", {})
    if "zfl" not in c:
        return {"translated": False, "untr": c.get("untr", "?")}
    b, unused = box(z)
    text = sheet(b)
    try:
        qs, marks = parse_quantities(text) if text else ({}, {})
        r = judge_sheet_claim(c["zfl"], qs, marks)
        _, atoms = extract_comparisons(c["zfl"], dict(qs))
        doms = []
        for _, (kind, e1, e2, chunk) in atoms.items():
            for op, arg in _partials(e1, []) + _partials(e2, []):
                try:
                    doms.append((op, domain(op, arg, qs)))
                except Exception as ex:                       # an argument the floor cannot read: say so
                    doms.append((op, f"UNREAD: {ex}"[:80]))
    except Exception as ex:
        return {"translated": True, "claim": c["zfl"], "sheet": text, "ztl": "UNREAD",
                "why": f"{type(ex).__name__}: {ex}"[:200]}
    out = {"translated": True, "claim": c["zfl"], "sheet": text, "ztl": r["disposition"],
           "why": r.get("why"), "domain": doms, "context_unused": unused}
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
