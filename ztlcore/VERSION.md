# ZTL core — vendored copy

These files are the ZTL logic kernel (the judge), vendored from the ZTL repository so introspect
clones and runs self-contained. **Source of truth: https://github.com/inventor1975/ZTL**

Vendored: 2026-11-23 every core file re-synced from inventor1975/ZTL @ c1bf15f — the pure branch (2026-11-22: the
Kleene/lazy register removed; EARNED/REFUTED/IF STABLE from ZTL's own readings, NEW zread.py; the judge's field
`lazy` is `forced`, T/F/N; grounding by the stable step, N hardened to the mark Z outward) — plus the modules the
newer line imports (zpy, zfunc, zexpcert, zseries, zatancert, zbackward_tree, zcertify, zintegral, zreach, ztrigcert,
zaffine, zaffinecert, zleibcert, zmonocert, ztaylorcert). introspect's zfl.py: the same four lines as ZTL's zfl.py.
Tests: py/js/go/java/rb GREEN as before; cs and php do not run here (no dotnet / no php vendor), as before.
Before it 2026-09-27 from inventor1975/ZTL @ ea05959 (the judge's worst cases closed: nested -> no longer doubles, the
reverse pass memoised, new caps); zfl.py from the same commit. Before it 7a432ce (the warranty grade exact and
seed-independent; a constant is not an atom in the lazy register). Before it: 2026-09-26 @ 99f8592 (the header said
18cb1f2, but zfl.py was already 99f8592's), which replaced 2026-09-13 @ f0a2f50 — two weeks of numeric fixes,
including the red team's LIE-1 (a sum's lattice), present here since the first copy.
To refresh: copy fixedpoint/zbackward/zbook/zmodal/znum/znumjudge/znumsolve/zpassport/ztime/ztl/ztljudge/zverify.py
from the ZTL repo root into this directory.
