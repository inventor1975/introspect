# ZTL core — vendored copy

These 12 files are the ZTL logic kernel (the judge), vendored from the ZTL repository so introspect
clones and runs self-contained. **Source of truth: https://github.com/inventor1975/ZTL**

Vendored: 2026-09-27 from inventor1975/ZTL @ 7a432ce (the warranty grade exact and seed-independent; a constant is
not an atom in the lazy register); zfl.py from the same commit. Before it: 2026-09-26 @ 99f8592 (the header said
18cb1f2, but zfl.py was already 99f8592's), which replaced 2026-09-13 @ f0a2f50 — two weeks of numeric fixes,
including the red team's LIE-1 (a sum's lattice), present here since the first copy.
To refresh: copy fixedpoint/zbackward/zbook/zmodal/znum/znumjudge/znumsolve/zpassport/ztime/ztl/ztljudge/zverify.py
from the ZTL repo root into this directory.
