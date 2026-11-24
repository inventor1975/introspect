#!/usr/bin/env python3
"""scan_statements — lean2zfl over a benchmark's STATEMENTS (proofs replaced by `sorry`): DeepSeek-Prover's jsonl
format (name, formal_statement, header, informal_prefix), e.g. miniF2F and ProofNet (2026-11-24, the calibration
against the benchmarks Rajasekaran and Ammanamanchi et al. audited). Derived from scan_goedel.py; only the input differs.

    python3 scan_goedel.py OUT_DIR N_PROOFS BATCH PARALLEL

Each batch: one Lean file (one `import Mathlib`), the proofs' bodies, then lean2zfl's dumper. A theorem whose proof
does not elaborate on our Mathlib is NOT COMPILED (an error line inside its range) — never read as ON CREDIT.
Output: OUT_DIR/rows.jsonl (one per theorem: disposition, why, the informal statement from the proof's comment).
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor


HERE = os.path.dirname(os.path.abspath(__file__))
L2Z = os.path.abspath(os.path.join(HERE, "..", ".."))          # lean2zfl/ of this repository
sys.path.insert(0, L2Z)
import lean2zfl  # noqa: E402
import zflread  # noqa: E402  (ZTL's numeric floor reads the statement's mathematics, 2026-11-24)
if os.environ.get("LEAN2ZFL_DUMPER"):            # a frozen copy: a scan must not read a dumper being edited
    lean2zfl.DUMPER = os.environ["LEAN2ZFL_DUMPER"]

PROJECT = os.environ.get("LEAN2ZFL_PROJECT", os.path.join(L2Z, "..", "..", "ztl-classical"))   # a Lake project with Mathlib
HEADER = "import Mathlib\nimport Aesop\nset_option maxHeartbeats 400000\nopen BigOperators Real Nat Topology Rat\n\n"
out_dir, n_proofs, batch, par = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
os.makedirs(out_dir, exist_ok=True)

import random
_src = os.environ["STATEMENTS_JSONL"]           # name, formal_statement, header, informal_prefix
_all = []
for _l in open(_src, encoding="utf-8"):
    if _l.strip():
        _r = json.loads(_l)
        _all.append({"problem_id": _r["name"],
                     "full_proof": (_r.get("informal_prefix") or "") + _r["formal_statement"].rstrip() + "\n  sorry\n"})
rows = _all[:n_proofs] if os.environ.get("SCAN_HEAD") else random.Random(20261124).sample(_all, min(n_proofs, len(_all)))
if os.environ.get("SCAN_IDS"):                   # a chosen subset (one id per line), e.g. the E/OPEN of a full scan
    _want = {l.strip() for l in open(os.environ["SCAN_IDS"], encoding="utf-8") if l.strip()}
    rows = [r for r in _all if r["problem_id"] in _want]


def body(src):
    """the proof without its header lines (imports, set_option maxHeartbeats, open)"""
    keep = [l for l in src.splitlines() if not re.match(r"^(import |set_option maxHeartbeats|open )", l)]
    return "\n".join(keep).strip() + "\n"


def informal(src):
    m = re.search(r"/-\s*(.*?)\s*-/", src, re.S)
    return m.group(1).strip()[:600] if m else ""


def run_batch(k):
    chunk = rows[k * batch:(k + 1) * batch]
    if not chunk:
        return []
    dumper = open(lean2zfl.DUMPER, encoding="utf-8").read()
    text, spans = "import Lean\n" + HEADER, []
    for r in chunk:
        start = text.count("\n") + 1
        text += body(r["full_proof"]) + "\n"
        spans.append((r["problem_id"], start, text.count("\n"), informal(r["full_proof"])))
    text += "\n" + dumper + "\n#lean2zfl_dump_here\n"
    fd, tmp = tempfile.mkstemp(prefix="lean2zfl_goedel_", suffix=".lean", dir=PROJECT)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(text)
    try:
        r = subprocess.run(["lake", "env", "lean", tmp], cwd=PROJECT, capture_output=True, text=True, timeout=3600)
        out = r.stdout
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
    finally:
        os.unlink(tmp)
    err_lines = [int(m.group(1)) for m in re.finditer(r"^\S+?:(\d+):\d+: error", out, re.M)]
    dumped = {}
    for l in out.splitlines():
        if l.startswith("LEAN2ZFL "):
            t = json.loads(l[len("LEAN2ZFL "):])
            dumped[t["name"]] = t
    res = []
    for pid, a, b, inf in spans:
        bad = any(a <= e <= b for e in err_lines)
        t = dumped.get(pid)
        if bad or t is None:
            res.append({"id": pid, "disp": "NOT COMPILED" if bad else "NOT READ", "informal": inf})
            continue
        d, why, claim, marking = lean2zfl.judge_theorem(t)
        row = {"id": pid, "disp": d, "why": why, "statement": t.get("statement", ""), "informal": inf,
               "ops": t.get("junk_ops", [])}
        if t.get("zfl"):
            try:
                row["ztl"] = zflread.read_safe(t)           # a forked child under a memory/time limit
            except Exception as ex:                      # the reading is reported, never a reason to lose the row
                row["ztl"] = {"translated": False, "untr": f"zflread failed: {ex}"[:200]}
        res.append(row)
    return res


done_ids = set()
if os.environ.get("SCAN_RETRY_NOT_READ") and os.path.exists(os.path.join(out_dir, "rows.jsonl")):
    # RETRY the unread (2026-11-24: batches that ran while the dumper was being edited came back NOT READ): drop
    # those rows, keep a copy of the file, and read them again — run with BATCH 1, so one proof cannot sink another
    import shutil
    src = os.path.join(out_dir, "rows.jsonl")
    shutil.copy(src, src + ".before_retry")
    kept = [l for l in open(src, encoding="utf-8") if l.strip() and json.loads(l)["disp"] != "NOT READ"]
    open(src, "w", encoding="utf-8").writelines(kept)
if os.path.exists(os.path.join(out_dir, "rows.jsonl")):          # RESUME: what is already judged is not redone
    done_ids = {json.loads(l)["id"] for l in open(os.path.join(out_dir, "rows.jsonl"), encoding="utf-8") if l.strip()}
    rows = [r for r in rows if r["problem_id"] not in done_ids]
print("resume: already", len(done_ids), "to do", len(rows), flush=True)
n_batches = (len(rows) + batch - 1) // batch
with ThreadPoolExecutor(par) as ex, open(os.path.join(out_dir, "rows.jsonl"), "a", encoding="utf-8") as fh:
    for res in ex.map(run_batch, range(n_batches)):
        for x in res:
            fh.write(json.dumps(x, ensure_ascii=False) + "\n")
        fh.flush()
print("done", len(rows))
