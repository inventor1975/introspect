#!/usr/bin/env python3
"""ledger — ONE ROW PER FINDING, every reading kept apart (2026-11-25, closing Verax's review of 24.11 and 25.11).

Verax asked for "an immutable row-level table" with the source, a statement hash, the class, the witness and the
certificate status, with the readings never collapsed into one boolean. This script builds it from the files in
this folder; it reads nothing else and runs nothing.

    python3 ledger.py            -> ledger.jsonl, ledger_summary.md

LABELS (Verax's taxonomy, 2026-11-25). Each refers to the FORMAL statement as written, never to the author's intent:
  FALSE_IN_LEAN            refuted at an admissible point in Lean's own semantics too (both readings)
  FALSE_IN_EXACT_READING   refuted at an admissible point with ℕ's / and − exact; Lean's convention holds there
                           (…_LEAN_UNREAD: Lean's reading at the point was not computed — not "holds in Lean").
                           Intent: INTENDED_DISCRETE when the informal text names a floor (⌊, \\lfloor, "floor",
                           "integer part"), otherwise INTENT_UNKNOWN. SEMANTIC_MISMATCH_CONFIRMED needs a human who did
                           not write the translator: never set here
  FALSE_FORMAL             a sequence refutation with the existence premise met (a sequence satisfying every
                           hypothesis exists, by recursion)
  COUNTEREXAMPLE_IF_SAT    a sequence or function refutation without that premise: false, or vacuously true
  VACUOUS                  no assignment satisfies the hypotheses (in the exact reading; `vacuous_in_lean` says
                           whether Lean's reading is contradictory too, when known)
  ADMISSIBILITY_UNKNOWN    the conclusion is refuted, but untranslated hypotheses leave open whether a point is
                           admissible
  UNDEFINED_ONLY_IN_ALTERNATE_READING   an operation has no value at an admissible point (x/0, ln of a non-positive)
  TRUE_EXACT_LEAN_VIA_CONVENTION        the exact mathematics is EARNED; Lean's proof went through a convention lemma
                                        (the lemma's PRESENCE in the proof term, not shown to be necessary)
PROOF: `compiled` means the AI's proof elaborated on our Mathlib (Lean 4.29). `not compiled` means only the
statement was read, with `sorry`; such a row says nothing about an accepted proof. `none` is a benchmark statement.
DUPLICATES: `cluster` is the sha256 of the translated claim with its hypotheses, whitespace removed; identical
mathematics in different rows shares a cluster.
"""
import gzip
import hashlib
import json
import os
import re
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
G = os.path.join(HERE, "goedel")
B = os.path.join(HERE, "benchmarks")
FLOOR = re.compile(r"⌊|\\lfloor|\bfloor\b|integer part|\[\s*x\s*\]|greatest integer", re.I)


def rows(path):
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                yield json.loads(line)


def h(text):
    return hashlib.sha256(re.sub(r"\s+", "", text or "").encode()).hexdigest()[:16]


def cluster(z):
    claim = (z or {}).get("claim") or ""
    hyps = (z or {}).get("hyps_zfl") or []
    return h(claim + "|" + "|".join(sorted(hyps)))


out = {}


def put(key, row):
    """the latest reading of a row wins (files are read oldest first)"""
    out[key] = row


# 1. the 24.11 classified readings of the 2,451 E/OPEN (findings.jsonl), with their certificates
cert = {c["id"]: c for c in rows(os.path.join(G, "certificates.jsonl"))}
CLASS = {"false_math_both_readings": "FALSE_IN_LEAN", "false_math_nat_convention": "FALSE_IN_EXACT_READING",
         "vacuous_hypotheses": "VACUOUS", "refuted_admissibility_unknown": "ADMISSIBILITY_UNKNOWN",
         "no_value_at_admissible_point": "UNDEFINED_ONLY_IN_ALTERNATE_READING",
         "true_math_lean_via_convention": "TRUE_EXACT_LEAN_VIA_CONVENTION"}
for f in rows(os.path.join(G, "findings.jsonl")):
    lab = CLASS[f["class"]]
    c = cert.get(f["id"], {})
    put(("goedel", f["id"]), {
        "dataset": "Goedel-LM/Lean-workbook-proofs", "id": f["id"], "proof": "compiled", "label": lab,
        "intent": ("INTENDED_DISCRETE" if FLOOR.search(f.get("informal") or "") else "INTENT_UNKNOWN")
        if lab == "FALSE_IN_EXACT_READING" else None,
        "witness": (f.get("witness") or {}).get("refuted_at"), "statement_hash": h(f.get("statement")),
        "cluster": h(json.dumps(f.get("zfl"), sort_keys=True, ensure_ascii=False)),
        "certificate": c.get("status"), "certificate_theorem": c.get("theorem"),
        "source": "goedel/findings.jsonl (reader v3, 2026-11-24)", "statement": f.get("statement")})


def from_reading(dataset, pid, r, proof, source):
    z = r.get("ztl") or {}
    w = z.get("witness") or {}
    lab = None
    if z.get("vacuous"):
        lab = "VACUOUS"
    elif "refuted_at" in w:
        if w.get("label"):
            lab = w["label"]
        elif w.get("conv_at_point") == "REFUTED" or (not z.get("rests_on_nat_convention") and "conv_at_point" not in w):
            lab = "FALSE_IN_LEAN"
        elif w.get("conv_at_point") == "UNREAD":
            lab = "FALSE_IN_EXACT_READING_LEAN_UNREAD"        # Lean's reading not computed: not "holds in Lean"
        else:
            lab = "FALSE_IN_EXACT_READING"
    if lab is None:
        return
    put((dataset, pid), {
        "dataset": dataset, "id": pid, "proof": proof, "label": lab,
        "intent": ("INTENDED_DISCRETE" if FLOOR.search(r.get("informal") or "") else "INTENT_UNKNOWN")
        if lab.startswith("FALSE_IN_EXACT_READING") else None,
        "witness": w.get("refuted_at"), "existence_premise": w.get("existence_premise"),
        "why": w.get("vacuous_why"), "statement_hash": h(r.get("statement")), "cluster": cluster(z),
        "certificate": None, "source": source, "statement": r.get("statement")})


# 2. later readings: the targeted rescans, then the current re-read of sequences/functions/words (the latest wins)
for name in ("seq_rows", "rescan_fn_rows", "rescan_iw_rows", "rescan_st_rows", "rescan_cx_rows", "rescan_ex_rows",
             "rescan_v6_rows"):
    p = os.path.join(G, name + ".jsonl.gz")
    if os.path.exists(p):
        for r in rows(p):
            if r["disp"] != "NOT COMPILED":
                key = ("Goedel-LM/Lean-workbook-proofs", r["id"])
                if ("goedel", r["id"]) in out:          # a 24.11 class row: the newer reading replaces it
                    del out[("goedel", r["id"])]
                if key in out:
                    del out[key]
                from_reading(key[0], r["id"], r, "compiled", f"goedel/{name}.jsonl.gz")
# 3. the 7,168 whose proofs did not compile: the statement only (the flagged rows re-read after the vacuity fix)
for r in rows(os.path.join(G, "not_compiled_flagged_reread.jsonl.gz")):
    from_reading("Goedel-LM/Lean-workbook-proofs", r["id"], r, "not compiled (statement read with sorry)",
                 "goedel/not_compiled_flagged_reread.jsonl.gz")
# 4. benchmarks (statements only)
KNOWN = {"mathd_numbertheory_618": "known: github.com/dafny-lang/miniF2F/issues/8; Kimina-Prover",
         "amc12a_2020_p13": "known: github.com/jonwashburn/anchor README",
         "exercise_1_2": "known: ProofNet-Verified states = 1",
         "exercise_4_11": "flagged for other defects: HF formalanon/semantic-lean-errors (index, constant)",
         "algebra_ineq_nto1onlt2m1on": "known: miniF2F-rocq audit.txt; DeepSeek-Prover-V2 uses ≤"}
BCERT = {"mathd_numbertheory_618", "amc12a_2020_p13", "exercise_1_2", "exercise_4_11"}
for name, ds in (("minif2f_rows_v5", "miniF2F (DeepSeek-Prover-V1.5 jsonl)"),
                 ("proofnet_rows_v5", "ProofNet (DeepSeek-Prover-V1.5 jsonl)"),
                 ("putnam_rows_v5", "PutnamBench")):
    for r in rows(os.path.join(B, name + ".jsonl.gz")):
        from_reading(ds, r["id"], r, "none (benchmark statement)", f"benchmarks/{name}.jsonl.gz")
        if (ds, r["id"]) in out:
            out[(ds, r["id"])]["known"] = KNOWN.get(r["id"])
            if r["id"] in BCERT:
                # Lean's kernel proves the NEGATION of the formal statement: false in Lean, whatever ZTL's second
                # reading could compute (mathd_numbertheory_618's Lean reading was UNREAD)
                out[(ds, r["id"])]["certificate"] = "certified"
                out[(ds, r["id"])]["certificate_theorem"] = "Certificates_benchmarks_20261125.lean"
                out[(ds, r["id"])]["label"] = "FALSE_IN_LEAN"
                out[(ds, r["id"])]["intent"] = None
            elif r["id"] == "algebra_ineq_nto1onlt2m1on":
                out[(ds, r["id"])]["certificate"] = "certified"
                out[(ds, r["id"])]["certificate_theorem"] = "Certificates_minif2f.lean"

ledger = sorted(out.values(), key=lambda x: (x["dataset"], x["label"], x["id"]))
with open(os.path.join(HERE, "ledger.jsonl"), "w", encoding="utf-8") as fh:
    for x in ledger:
        fh.write(json.dumps(x, ensure_ascii=False) + "\n")

# summary: counts per dataset and label, distinct clusters, certificates
by = defaultdict(Counter)
clusters = defaultdict(set)
certs = defaultdict(Counter)
intent = Counter()
for x in ledger:
    k = (x["dataset"], x["proof"].split(" (")[0])
    by[k][x["label"]] += 1
    clusters[(k, x["label"])].add(x["cluster"])
    if x.get("certificate"):
        certs[(k, x["label"])][x["certificate"]] += 1
    if x.get("intent"):
        intent[(k[0], x["intent"])] += 1
lines = ["# Ledger summary (generated by ledger.py; do not edit by hand)", "",
         "| dataset | proof | label | rows | distinct (clusters) | certificates |", "|---|---|---|---|---|---|"]
for k in sorted(by):
    for lab, n in sorted(by[k].items()):
        cs = ", ".join(f"{s}: {m}" for s, m in sorted(certs[(k, lab)].items())) or "—"
        lines.append(f"| {k[0]} | {k[1]} | {lab} | {n} | {len(clusters[(k, lab)])} | {cs} |")
lines += ["", "Intent of FALSE_IN_EXACT_READING (the informal text names a floor, or not):", ""]
for (ds, it), n in sorted(intent.items()):
    lines.append(f"- {ds}: {it} {n}")
open(os.path.join(HERE, "ledger_summary.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("\n".join(lines))
