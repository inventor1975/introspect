#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lean2zfl — does a Lean theorem say what its words say, or what a convention says?

Mathlib's total functions return a CONVENTIONAL value outside their domain: tsum of a non-summable series is 0,
x / 0 = 0, 0⁻¹ = 0, √ of a negative is 0, log 0 = 0 and log (-x) = log x, ℕ-subtraction truncates at 0, ζ 1 is a
chosen constant. A theorem can be true BECAUSE of such a value — `∑' n : ℕ, (n : ℝ) = 0` is a theorem of Mathlib —
and the kernel accepts it, correctly: it checks the steps, not what the statement means. This module reads every
theorem of a file from the ELABORATED environment (JunkDump.lean, appended to a COPY of the file) and hands the ZTL
judge one atom per junk operation in the statement:

  guarded by a hypothesis (b ≠ 0, Summable f, 0 ≤ x, m ≤ n, s ≠ 1) or a literal outside the junk point -> T
  unguarded, and the proof directly uses that operation's junk lemma (the junk branch is TAKEN)        -> E (no subject)
  unguarded, the same term more than once, and the statement PROVED for every value of that term (the term
  abstracted to a fresh variable, proved by ring / simp / omega at dump time)    -> one dirty atom, `q <-> q`
  unguarded otherwise                                                                                    -> Z
  and the axioms: anything beyond propext / Classical.choice / Quot.sound (sorryAx included) -> `~~ax`, named.

The judge's disposition is the verdict (introspect contract §1): EARNED, E, EARNED IF STABLE, OPEN, ON CREDIT;
REFUTED and REFUTED IF STABLE are not produced (a checked theorem is not false). Limits, plainly: guards are read
from the hypotheses' TEXT (`0 ≤ r < 1` does not count as `Summable`); junk lemmas are seen only when the proof term
names them DIRECTLY (a junk value reached by unfolding a definition is not seen: such a theorem is OPEN, never
EARNED); the catalogue is seven operations.

    python3 lean2zfl.py FILE.lean [...]                    (a copy of each file is elaborated with the dumper)
    python3 lean2zfl.py --module PROJECT Mod.A [Mod.B ...]  (built modules read from their .olean files)
"""
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
for p in (ROOT, os.path.join(ROOT, "ztlcore")):
    if p not in sys.path:
        sys.path.insert(0, p)
import ztljudge  # noqa: E402  (the ONE judge)

DUMPER = os.path.join(HERE, "JunkDump.lean")
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
# which junk lemma takes which operation's junk branch
FAMILY = {"tsum": {"tsum_eq_zero_of_not_summable"},
          "HDiv.hDiv": {"div_zero", "inv_zero", "Nat.div_zero", "Int.ediv_zero"},
          "Inv.inv": {"inv_zero"},
          "Real.sqrt": {"Real.sqrt_eq_zero_of_nonpos"},
          "Real.log": {"Real.log_zero", "Real.log_neg_eq_log"},
          "HSub.hSub": {"Nat.sub_eq_zero_of_le", "tsub_eq_zero_of_le"},
          "riemannZeta": {"riemannZeta_one"}}
TRUNCATING_SUB = {"ℕ", "Nat", "ℝ≥0", "NNReal", "ℝ≥0∞", "ENNReal"}

# NOT ADOPTED (MEASURED 2026-11-24): "no junk lemma of the family anywhere in the proof's chain -> EARNED" moved 75 of
# 173 OPEN in six Mathlib modules, and some were FALSE clears — Real.log_zero itself (proved by `simp [log]`),
# Real.exp_log_of_neg, inv_nonpos'. The convention is also reached by unfolding a definition and through class fields
# (GroupWithZero.inv_zero), which a lemma-name chain does not see. The chain is kept in the dump (`junk_reach`) as
# information only; it decides nothing.

UNPARSED = []     # files that did not elaborate: NOT analysed, NOT clean


def lake_root(path):
    d = os.path.dirname(os.path.abspath(path))
    while d != "/":
        if any(os.path.exists(os.path.join(d, f)) for f in ("lakefile.toml", "lakefile.lean")):
            return d
        d = os.path.dirname(d)
    return None


def _norm(s):
    return re.sub(r"\s+", " ", str(s)).strip()


def _num(s):
    s = _norm(s).strip("()")
    try:
        return float(s)
    except ValueError:
        return None


def guarded(op, args, typ, hyps):
    """Is this occurrence's junk branch closed — by a hypothesis's text, or by a literal argument?"""
    H = {_norm(h) for h in hyps}
    a = [_norm(x) for x in args]
    if op == "tsum":
        return any(h.startswith(("Summable", "HasSum")) for h in H)
    if op in ("HDiv.hDiv", "Inv.inv"):
        d = a[-1]
        v = _num(d)
        return (v is not None and v != 0) or any(h in H for h in (f"{d} ≠ 0", f"0 ≠ {d}", f"0 < {d}", f"{d} < 0"))
    if op == "Real.sqrt":
        v = _num(a[0])
        return (v is not None and v >= 0) or any(h in H for h in (f"0 ≤ {a[0]}", f"0 < {a[0]}"))
    if op == "Real.log":
        v = _num(a[0])
        return (v is not None and v > 0) or f"0 < {a[0]}" in H
    if op == "HSub.hSub":
        if _norm(typ) not in TRUNCATING_SUB:
            return True                      # a ring's subtraction has no junk branch
        x, y = _num(a[0]), _num(a[1])
        return (x is not None and y is not None and x >= y) or any(h in H for h in (f"{a[1]} ≤ {a[0]}", f"{a[1]} < {a[0]}"))
    if op == "riemannZeta":
        v = _num(a[0])
        return (v is not None and v != 1) or f"{a[0]} ≠ 1" in H
    return False


def judge_theorem(t):
    """One theorem's dump -> (disposition, why, the claim and marking handed to the judge)."""
    parts, marking, notes, seen = [], {}, [], {}
    lemmas = set(t.get("junk_lemmas", []))
    for o in t.get("junk_ops", []):
        op, typ, args = o["op"], o.get("type", ""), o.get("args", [])
        if op == "HSub.hSub" and _norm(typ) not in TRUNCATING_SUB:
            continue
        if o.get("guard_proved") or guarded(op, args, typ, t.get("hyps", [])):
            continue                         # the domain condition PROVED at dump time (positivity / norm_num / omega /
                                             # assumption), or stated by a hypothesis
        key = _norm(o["expr"])
        if o.get("bound"):                   # under a binder of the statement: its text names no fixed term, so two
            key = f"{key}#{len(seen)}"       # alike-printing occurrences are NOT one term (never grouped as IF STABLE)
        if o.get("junk_proved"):              # the hypotheses PROVE the argument is at a convention point: the
            seen[key] = ("E", op)            # statement speaks about the convention there (2026-11-24)
        elif lemmas & FAMILY.get(op, set()):
            seen.setdefault(key, ("E", op))
        elif key in seen and o.get("generalizes"):
            seen[key] = ("ZZ", op)            # the statement PROVED for every value of the term: true if stable
        else:
            seen.setdefault(key, ("Z", op))
    i = 0
    for key, (kind, op) in seen.items():
        i += 1
        a = f"o{i}"
        if kind == "E":
            marking[a] = "E"; parts.append(a); notes.append(f"{key}: at a convention point ({op}) — no subject")
        elif kind == "ZZ":
            marking[a] = "Z"; parts.append(f"({a} <-> {a})"); notes.append(f"{key}: unguarded, occurs more than once")
        else:
            marking[a] = "Z"; parts.append(a); notes.append(f"{key}: unguarded, junk branch not seen")
    extra = sorted(set(t.get("axioms", [])) - STANDARD_AXIOMS)
    if extra:
        marking["ax"] = "Z"; parts.append("~~ax"); notes.append(f"rests on the axioms {extra}")
    if not parts:
        marking["g"] = "T"; parts.append("g"); notes.append("no unguarded junk operation; standard axioms only")
    claim = " & ".join(parts)
    r = ztljudge.judge(claim, marking)
    return r["disposition"], "; ".join(notes), claim, marking


def dump_file(path, timeout=600):
    """Elaborate a COPY of the file with the dumper appended; return the theorems' JSON, or raise."""
    root = lake_root(path) or os.environ.get("LEAN2ZFL_PROJECT")   # a loose file: elaborate it in a named project
    if not root:
        raise RuntimeError(f"{path}: not inside a Lake project (set LEAN2ZFL_PROJECT to a project with Mathlib)")
    src = open(path, encoding="utf-8").read()
    dumper = open(DUMPER, encoding="utf-8").read()
    fd, tmp = tempfile.mkstemp(prefix="lean2zfl_", suffix=".lean", dir=root)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        # the dumper needs Lean's meta namespaces: `import Lean` goes FIRST (imports precede everything), so every
        # reported line is one too high and is corrected below
        fh.write("import Lean\n" + src.rstrip("\n") + "\n\n" + dumper + "\n#lean2zfl_dump_here\n")
    try:
        r = subprocess.run(["lake", "env", "lean", tmp], cwd=root, capture_output=True, text=True, timeout=timeout)
    finally:
        os.unlink(tmp)
    out = [json.loads(l[len("LEAN2ZFL "):]) for l in r.stdout.splitlines() if l.startswith("LEAN2ZFL ")]
    for t in out:
        t["line"] = max(0, int(t.get("line", 0)) - 1)
    out += [{"_fail": l[len("LEAN2ZFL_FAIL "):][:300]} for l in r.stdout.splitlines() if l.startswith("LEAN2ZFL_FAIL ")]
    errs = [l for l in r.stdout.splitlines() if ": error" in l]
    if errs and not out:
        raise RuntimeError(f"{path}: does not elaborate: {errs[0][:300]}")
    return out


def dump_module(module, project, timeout=1800):
    """Read every theorem of an already BUILT module from its .olean (the Lean module system's files — Mathlib's —
    cannot be re-elaborated as a loose copy; reading the built module re-elaborates nothing)."""
    dumper = open(DUMPER, encoding="utf-8").read()
    fd, tmp = tempfile.mkstemp(prefix="lean2zfl_", suffix=".lean", dir=project)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(f"import Lean\nimport {module}\n\n" + dumper + f"\n#lean2zfl_dump_module {module}\n")
    try:
        r = subprocess.run(["lake", "env", "lean", tmp], cwd=project, capture_output=True, text=True, timeout=timeout)
    finally:
        os.unlink(tmp)
    out = [json.loads(l[len("LEAN2ZFL "):]) for l in r.stdout.splitlines() if l.startswith("LEAN2ZFL ")]
    out += [{"_fail": l[len("LEAN2ZFL_FAIL "):][:300]} for l in r.stdout.splitlines() if l.startswith("LEAN2ZFL_FAIL ")]
    if not out and r.returncode != 0:
        raise RuntimeError(f"{module}: {(r.stdout + r.stderr)[-300:]}")
    return out


def analyze_modules(modules, project):
    """(module, line, name, ctx, disposition, why) for every theorem of each built module."""
    rows = []
    for m in modules:
        try:
            ths = dump_module(m, project)
        except Exception as e:  # noqa: BLE001
            UNPARSED.append((m, str(e)[:300]))
            continue
        for t in ths:
            if "_fail" in t:
                UNPARSED.append((m, "theorem not read: " + t["_fail"]))
                continue
            d, why, _c, _m = judge_theorem(t)
            fams = sorted({o["op"] for o in t.get("junk_ops", [])})
            rows.append((m, t.get("line", 0), t["name"], "junk:" + (",".join(fams) or "none"), d, why))
    return rows


def _built_module(path, root):
    """The module name of a file whose BUILD is current (.olean at least as new as the source), else None."""
    rel = os.path.relpath(os.path.abspath(path), root)
    if rel.startswith("..") or not rel.endswith(".lean"):
        return None
    mod = rel[:-5].replace(os.sep, ".")
    olean = os.path.join(root, ".lake", "build", "lib", "lean", rel[:-5] + ".olean")
    if os.path.exists(olean) and os.path.getmtime(olean) >= os.path.getmtime(path):
        return mod
    return None


def dump_modules(modules, project, timeout=1800):
    """ONE Lean run for many built modules: import them all, dump each (MEASURED 2026-11-24: re-elaborating 46 files
    of ztl-classical one by one did not finish in 50 minutes)."""
    dumper = open(DUMPER, encoding="utf-8").read()
    fd, tmp = tempfile.mkstemp(prefix="lean2zfl_", suffix=".lean", dir=project)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write("import Lean\n" + "".join(f"import {m}\n" for m in modules) + "\n" + dumper + "\n"
                 + "".join(f"#lean2zfl_dump_module {m}\n" for m in modules))
    try:
        r = subprocess.run(["lake", "env", "lean", tmp], cwd=project, capture_output=True, text=True, timeout=timeout)
    finally:
        os.unlink(tmp)
    out, cur = {}, None
    for l in r.stdout.splitlines():
        if l.startswith("LEAN2ZFL_MODULE "):
            cur = l.split(" ", 1)[1].strip(); out.setdefault(cur, [])
        elif l.startswith("LEAN2ZFL ") and cur:
            out[cur].append(json.loads(l[len("LEAN2ZFL "):]))
        elif l.startswith("LEAN2ZFL_FAIL ") and cur:
            out[cur].append({"_fail": l[len("LEAN2ZFL_FAIL "):][:300]})
    if not out and r.returncode != 0:
        raise RuntimeError((r.stdout + r.stderr)[-300:])
    return out


def analyze_app(paths, file_timeout=600):
    """introspect's interface: (path, line, name, ctx, disposition, why) per theorem. Built modules are read from
    their .olean in one Lean run per project; only files whose build is missing or stale are re-elaborated."""
    UNPARSED.clear()
    rows, by_root, loose = [], {}, []
    for p in paths:
        root = lake_root(p)
        mod = _built_module(p, root) if root else None
        if mod:
            by_root.setdefault(root, {})[mod] = p
        else:
            loose.append(p)

    def emit(p, ths):
        for t in ths:
            if "_fail" in t:
                UNPARSED.append((p, "theorem not read: " + t["_fail"]))
                continue
            d, why, _c, _m = judge_theorem(t)
            fams = sorted({o["op"] for o in t.get("junk_ops", [])})
            rows.append((p, t.get("line", 0), t["name"], "junk:" + (",".join(fams) or "none"), d, why))

    for root, mods in by_root.items():
        try:
            got = dump_modules(sorted(mods), root)
        except Exception as e:  # noqa: BLE001
            for p in mods.values():
                UNPARSED.append((p, str(e)[:300]))
            continue
        for m, p in mods.items():
            if m in got:
                emit(p, got[m])
            else:
                UNPARSED.append((p, "module not dumped"))
    for p in loose:
        try:
            emit(p, dump_file(p, timeout=file_timeout))
        except Exception as e:  # noqa: BLE001
            UNPARSED.append((p, str(e)[:300]))
    return rows


if __name__ == "__main__":
    if sys.argv[1:2] == ["--module"]:       # lean2zfl.py --module PROJECT Mod.A Mod.B ...
        rows = analyze_modules(sys.argv[3:], sys.argv[2])
    else:
        rows = analyze_app(sys.argv[1:])
    for row in rows:
        print(f"{row[0]}:{row[1]}  {row[2]}  {row[4]}  — {row[5]}")
    for p, why in UNPARSED:
        print(f"NOT ANALYSED (not 'clean'): {p}: {why}")
