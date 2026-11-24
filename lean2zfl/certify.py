# -*- coding: utf-8 -*-
"""
certify — ZTL's refutations of a statement's MATHEMATICS turned into Lean kernel facts (2026-11-24, the curator:
"Делаем все").

ZTL's floor refuted the exact mathematical reading of a Lean statement, either outright or at a witness point found
by zflread. ZTL is not Lean's kernel; this file asks the kernel. For every such reading it writes

    theorem cert_k : (hypotheses at the point) ∧ ¬ (conclusion at the point)

over ℝ, with every number a real and ℕ's `/` and `−` read exactly. That is the mathematics the statement writes, not
Lean's ℕ. The kernel proves it by tactics alone: `norm_num`, `simp`, `positivity`, `nlinarith`. No `sorry` is allowed,
and an alternative that leaves a goal fails. A refutation the tactics cannot close stays ZTL's verdict only, and is
counted as such. A claim with an integer word (`idiv mod dvd fact choose`) is not written here; it is counted apart.

    LEAN2ZFL_PROJECT=<Lake project with Mathlib> python3 certify.py findings.jsonl OUT_DIR

Output: OUT_DIR/Certificates.lean (only the closed theorems, so it rebuilds clean) and OUT_DIR/certificates.jsonl
(per finding: certified / not closed / not written, and why).
"""
import json
import os
import re
import subprocess
import sys
import tempfile

FUN = {"sqrt": "Real.sqrt", "ln": "Real.log", "exp": "Real.exp", "sin": "Real.sin", "cos": "Real.cos",
       "tan": "Real.tan", "atan": "Real.arctan", "pow": "Real.rpow", "max": "max", "min": "min",
       "log10": "Real.logb 10"}
INTWORDS = ("idiv(", "mod(", "dvd(", "fact(", "choose(", "ndiv(", "nsub(")
TACTICS = ["norm_num", "(norm_num; done)", "(constructor <;> norm_num)", "(refine ⟨?_, ?_⟩ <;> norm_num)",
           "(simp; norm_num)", "(norm_num [Real.sqrt_lt', Real.lt_sqrt, Real.sqrt_le_sqrt]; done)",
           "(constructor <;> (try norm_num) <;> positivity)", "(norm_num <;> nlinarith [Real.pi_gt_three])"]


def _num(tok):
    return f"({tok}:ℝ)"


def _split_args(s):
    out, depth, start = [], 0, 0
    for i, c in enumerate(s):
        depth += (c == "(") - (c == ")")
        if c == "," and depth == 0:
            out.append(s[start:i]); start = i + 1
    out.append(s[start:])
    return out


def to_lean(z, env):
    """a ZFL claim (the exact reading, no marks) as a Lean proposition over ℝ, every variable replaced by its value"""
    s = z.replace("↔", " ↔ ").replace("->", " → ")
    out, i = [], 0
    while i < len(s):
        m = re.match(r"[A-Za-z_][A-Za-z0-9_]*", s[i:])
        if m:
            w = m.group(0)
            j = i + len(w)
            if w in env:
                v = env[w]
                p, _, q = v.partition("/")
                out.append(f"(({p}:ℝ)/{q})" if q else _num(p))
                i = j
                continue
            if w == "pi":
                out.append("Real.pi")
                i = j
                continue
            if w in FUN and j < len(s) and s[j] == "(":
                depth, k = 1, j + 1
                while depth:
                    depth += (s[k] == "(") - (s[k] == ")")
                    k += 1
                args = [to_lean(a, env) for a in _split_args(s[j + 1:k - 1])]
                out.append(f"({FUN[w]} " + " ".join(f"({a})" for a in args) + ")")
                i = k
                continue
            raise ValueError(f"no Lean word for {w!r}")
        m = re.match(r"\*\*\s*(\d+)", s[i:])
        if m:
            out.append(f" ^ ({m.group(1)}:ℕ)")
            i += len(m.group(0))
            continue
        m = re.match(r"\d+", s[i:])
        if m:
            out.append(_num(m.group(0)))
            i += len(m.group(0))
            continue
        two = s[i:i + 2]
        if two in ("==", "!=", "<=", ">="):
            out.append({"==": " = ", "!=": " ≠ ", "<=": " ≤ ", ">=": " ≥ "}[two])
            i += 2
            continue
        c = s[i]
        out.append({"&": " ∧ ", "|": " ∨ ", "~": "¬"}.get(c, c))
        i += 1
    return "".join(out)


def build(findings):
    """(theorem texts, records) — one theorem per finding that has a refutation and no integer word"""
    thms, recs = [], []
    for k, f in enumerate(findings):
        w = f.get("witness") or {}
        rec = {"id": f["id"], "class": f["class"]}
        if f["class"] not in ("false_math_both_readings", "false_math_nat_convention"):
            continue
        env = w.get("refuted_at", {}) if "refuted_at" in w else {}
        claim = f["zfl"]
        if any(t in claim for t in INTWORDS):
            rec["status"] = "not written: an integer word"
            recs.append(rec)
            continue
        if f.get("hyps_untr"):
            rec["status"] = "not written: an untranslated hypothesis"
            recs.append(rec)
            continue
        hyps = [h for h in f.get("hyps_zfl", [])]
        try:
            concl = to_lean(claim, env)
            hl = [to_lean(h, env) for h in hyps]
        except ValueError as ex:
            rec["status"] = f"not written: {ex}"
            recs.append(rec)
            continue
        prop = " ∧ ".join([f"({h})" for h in hl] + [f"¬ ({concl})"])
        name = f"cert_{k}"
        alts = " | ".join(TACTICS)
        thms.append((name, f"/-- {f['id']} ({f['class']}) at {env or 'no variables'} -/\n"
                           f"theorem {name} : {prop} := by\n  first | {alts}\n"))
        rec.update({"theorem": name, "at": env, "prop": prop})
        recs.append(rec)
    return thms, recs


HEADER = "import Mathlib\nset_option maxHeartbeats 400000\n\nnamespace ZTLCert\n\n"


def run(thms, project):
    """elaborate every theorem; a theorem with an error line inside its range is not closed"""
    text, spans = HEADER, {}
    for name, t in thms:
        a = text.count("\n") + 1
        text += t + "\n"
        spans[name] = (a, text.count("\n"))
    text += "end ZTLCert\n"
    fd, tmp = tempfile.mkstemp(prefix="ztlcert_", suffix=".lean", dir=project)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(text)
    try:
        r = subprocess.run(["lake", "env", "lean", tmp], cwd=project, capture_output=True, text=True, timeout=3600)
    finally:
        os.unlink(tmp)
    errs = [int(m.group(1)) for m in re.finditer(r"^\S+?:(\d+):\d+: error", r.stdout, re.M)]
    sorry = [int(m.group(1)) for m in re.finditer(r"^\S+?:(\d+):\d+: warning: declaration uses 'sorry'", r.stdout, re.M)]
    return {n: not any(a <= e <= b for e in errs + sorry) for n, (a, b) in spans.items()}


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    project = os.environ.get("LEAN2ZFL_PROJECT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                                                                "ztl-classical"))
    findings = [json.loads(l) for l in open(src, encoding="utf-8") if l.strip()]
    thms, recs = build(findings)
    closed = run(thms, project) if thms else {}
    by = dict(thms)
    for r in recs:
        if "theorem" in r:
            r["status"] = "certified" if closed.get(r["theorem"]) else "not closed by the tactics"
    with open(os.path.join(out, "Certificates.lean"), "w", encoding="utf-8") as fh:
        fh.write(HEADER + "".join(by[n] + "\n" for n in by if closed.get(n)) + "end ZTLCert\n")
    with open(os.path.join(out, "certificates.jsonl"), "w", encoding="utf-8") as fh:
        for r in recs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    from collections import Counter
    print(Counter((r["class"], r["status"].split(":")[0]) for r in recs))
