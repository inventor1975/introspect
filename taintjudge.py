# -*- coding: utf-8 -*-
"""taintjudge — the shared taint->ZFL->judge adapter for the language modules.

Every module computes a net taint state for a sink argument: F (clean) / T (attacker-controlled reaches
unsubstituted) / Z (unknown). Instead of each module mapping that to a verdict itself, it hands the state
here; this builds the SAME 3-row ZFL document php2zfl feeds the core (tainted, sanitized, and the claim
`safe := ~Tr(tainted) | Tr(sanitized)`) and asks the ONE ZTL judge (`zfl.run`) for the disposition. So all
seven languages are judged by the same measured core, not by seven private copies of the verdict rule."""
import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)          # so `import zfl` (the ZTL core) resolves next to this file
import zfl                             # noqa: E402

F, T, Z = "F", "T", "Z"


def _slug(s):
    """A validator-safe ground token: letters/digits/_/- only (the readable text lives in `means`)."""
    return "".join(c if (c.isalnum() or c in "_-") else "_" for c in str(s))[:40] or "x"


def _doc(st, ctx, source, sink):
    gsrc, gsink = _slug(source), _slug(sink)
    if st == T:
        tainted = {"name": "tainted", "ground_kind": "act", "status": "verified",
                   "ground": f"src-{gsrc}", "means": f"attacker-controlled value reaches the sink: {source}"}
        sanitized = {"name": "sanitized", "ground_kind": "act", "status": "refuted",
                     "ground": f"ast-sink-{gsink}", "means": "reaches the sink unsubstituted"}
    elif st == Z:
        tainted = {"name": "tainted", "status": "unverified",
                   "means": f"origin not visible in this file: {source}"}
        sanitized = {"name": "sanitized", "status": "unverified", "means": "no substitution seen"}
    else:  # F
        tainted = {"name": "tainted", "ground_kind": "act", "status": "refuted",
                   "ground": f"ast-sink-{gsink}", "means": "nothing attacker-controlled reaches the sink"}
        sanitized = {"name": "sanitized", "status": "unverified", "means": "not needed: nothing attacker-controlled arrives"}
    safe = {"name": "safe", "status": "defined", "ground": "~Tr(tainted) | Tr(sanitized)",
            "means": f"the {ctx} sink {sink} cannot be driven by an attacker"}
    return {"rows": [tainted, sanitized, safe], "claim": "safe"}


def judge_taint(st, ctx, source="input", sink="sink"):
    """Return the ZTL core's disposition (REFUTED / OPEN / EARNED) for a taint state st over ctx."""
    r = zfl.run(_doc(st, ctx, source, sink))
    errs = [i for i in r.get("issues", []) if i.get("level") == "error"]
    if errs or not r.get("ok", True):
        return "OPEN"                  # a refused document -> honest не-знаю, never a false clear/accusation
    disp = r["report"]["judge"]["disposition"]
    return {"ON CREDIT": "OPEN"}.get(disp, disp)
