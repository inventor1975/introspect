#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""introspect — one command, every language in a project, routed by file extension.

Point it at a project. It walks the tree, sends each file to the module for its
language (by extension), runs every language present, and merges the verdicts
into a single report:

    REFUTED  attacker-controlled data reaches a sink unsubstituted — a proven flow
    OPEN     a dangerous sink is reached but origin/neutralisation is unverifiable
    EARNED   proven clean

Honest boundaries, stated so no number is over-read:
  * Each language is analysed ON ITS OWN. Data flowing from one language into
    another — a PHP page shelling to a Python script, a JS front end posting to a
    Go service, anything passing through a database or a queue — is NOT tracked;
    such cross-language flows stay OPEN, never guessed.
  * A language whose parser is not installed is SKIPPED with a reason. It is
    never silently reported clean.
  * A file in a language introspect does not cover is listed as out-of-scope —
    not as "safe".

Usage:
    python3 introspect.py <project-dir> [--json report.json] [--open] [--quiet]

Exit status is nonzero when any REFUTED is found (useful in CI).
"""
import os
import sys
import json
import argparse
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)          # taintjudge / zfl (the core) live at the repo root

# file extension -> (module directory, human label)
LANGS = {
    ".php":  ("php2zfl",  "php"),
    ".py":   ("py2zfl",   "python"),
    ".go":   ("go2zfl",   "go"),
    ".java": ("java2zfl", "java"),
    ".js":   ("js2zfl",   "js/ts"), ".jsx": ("js2zfl", "js/ts"),
    ".ts":   ("js2zfl",   "js/ts"), ".tsx": ("js2zfl", "js/ts"),
    ".mjs":  ("js2zfl",   "js/ts"), ".cjs": ("js2zfl", "js/ts"),
    ".rb":   ("rb2zfl",   "ruby"),
    ".cs":   ("cs2zfl",   "c#"),
}
LABEL = {d: lbl for (d, lbl) in LANGS.values()}

# directories never worth walking into
SKIP_DIRS = {".git", "node_modules", "vendor", "__pycache__", ".venv", "venv",
             "env", "dist", "build", "target", ".idea", ".vscode", "bin", "obj",
             ".mypy_cache", ".pytest_cache"}

# source extensions introspect does NOT cover — reported as out-of-scope (not "safe")
UNCOVERED_SRC = {".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".rs", ".swift",
                 ".kt", ".kts", ".scala", ".pl", ".pm", ".lua", ".r", ".m",
                 ".mm", ".ex", ".exs", ".dart", ".sh", ".bash", ".ps1", ".sql",
                 ".vb", ".groovy", ".clj", ".erl", ".hs", ".ml", ".jl"}

# a friendly hint per language when its parser is missing
PARSER_HINT = {
    "php2zfl":  "PHP + PHP-Parser (composer install in php2zfl/)",
    "java2zfl": "javalang (pip install javalang)",
    "go2zfl":   "the Go toolchain (`go`)",
    "js2zfl":   "@babel/parser (npm install in js2zfl/)",
    "rb2zfl":   "Ruby (its stdlib Ripper)",
    "cs2zfl":   "the .NET SDK (the Roslyn helper builds on first use)",
    "py2zfl":   "Python (native ast — should always be present)",
}


def _load(moddir):
    """Import <moddir>/<moddir>.py as a module named <moddir>."""
    path = os.path.join(HERE, moddir, moddir + ".py")
    spec = importlib.util.spec_from_file_location(moddir, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[moddir] = mod
    spec.loader.exec_module(mod)
    return mod


def _norm(d):
    """Normalise a module's disposition to REFUTED / OPEN / EARNED."""
    return {"ON CREDIT": "OPEN", "R": "REFUTED", "O": "OPEN", "F": "EARNED",
            "E": "OPEN"}.get(d, d)


def _classify(full, by_module, uncovered):
    ext = os.path.splitext(full)[1].lower()
    if ext in LANGS:
        by_module.setdefault(LANGS[ext][0], []).append(full)
    elif ext in UNCOVERED_SRC:
        uncovered[ext] = uncovered.get(ext, 0) + 1


def walk(root):
    """Return (by_module: {moddir: [paths]}, uncovered: {ext: count})."""
    by_module, uncovered = {}, {}
    if os.path.isfile(root):                       # a single file is a valid target too
        _classify(root, by_module, uncovered)
        return by_module, uncovered
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            _classify(os.path.join(dp, fn), by_module, uncovered)
    return by_module, uncovered


def run_language(moddir, files):
    """Run one language module over its files. Return a list of findings, each
    {file, line, name, ctx, disp}. Raises on a missing parser / broken toolchain."""
    mod = _load(moddir)
    findings = []
    if moddir == "php2zfl":
        out = mod.run(files, ctx="all")          # ctx='all' judges every sink context
        for f in out.get("files", []):
            if f.get("parse_error") or f.get("disposition") == "E":
                continue
            for s in f.get("sinks", []):
                findings.append({"file": f["file"], "line": s.get("line"),
                                 "name": s.get("fn"), "ctx": s.get("ctx"),
                                 "disp": _norm(s.get("disposition"))})
    else:
        for t in mod.analyze_app(files):         # (path, line, name, ctx, disp, [why])
            findings.append({"file": t[0], "line": t[1], "name": t[2],
                             "ctx": t[3], "disp": _norm(t[4])})
    return findings


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", help="path to the project directory (or a single file)")
    ap.add_argument("--json", metavar="FILE", help="also write the full report as JSON")
    ap.add_argument("--open", action="store_true", help="list OPEN findings too, not just count them")
    ap.add_argument("--quiet", action="store_true", help="print only the summary line")
    args = ap.parse_args()

    if not os.path.exists(args.project):
        sys.exit(f"no such path: {args.project}")

    by_module, uncovered = walk(args.project)
    report = {"project": os.path.abspath(args.project), "languages": {},
              "skipped": {}, "uncovered": uncovered}

    for moddir in sorted(by_module):
        files = by_module[moddir]
        try:
            findings = run_language(moddir, files)
        except (Exception, SystemExit) as e:      # a missing parser is not a clean bill
            # (a module may sys.exit on a missing toolchain — that is a skip, not a crash)
            report["skipped"][moddir] = {"files": len(files), "files_list": files,
                                         "reason": f"{type(e).__name__}: {e}",
                                         "needs": PARSER_HINT.get(moddir, "")}
            continue
        counts = {"REFUTED": 0, "OPEN": 0, "EARNED": 0}
        for f in findings:
            counts[f["disp"]] = counts.get(f["disp"], 0) + 1
        report["languages"][moddir] = {"files": len(files), "counts": counts,
                                       "findings": findings}

    total_refuted = sum(v["counts"].get("REFUTED", 0) for v in report["languages"].values())
    report["total_refuted"] = total_refuted

    _print(report, show_open=args.open, quiet=args.quiet)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2)
        if not args.quiet:
            print(f"\n(full report written to {args.json})")

    sys.exit(1 if total_refuted else 0)


def _print(report, show_open=False, quiet=False):
    langs, skipped = report["languages"], report["skipped"]
    line = "=" * 72
    if not quiet:
        print(line)
        print(f"introspect — {report['project']}")
        print(line)
        for moddir in sorted(langs):
            v = langs[moddir]
            c = v["counts"]
            print(f"  {LABEL[moddir]:<8} {v['files']:>5} files    "
                  f"REFUTED {c.get('REFUTED',0):<4} OPEN {c.get('OPEN',0):<4} "
                  f"EARNED {c.get('EARNED',0)}")
        for moddir in sorted(skipped):
            s = skipped[moddir]
            # A skip is NOT always a missing parser: a path bug, a timeout or a crash
            # lands here too. Printing only the hint turned a real coverage hole into a
            # wrong diagnosis (2026-09-19: a relative-path ENOENT was reported as
            # "needs @babel/parser", so installing the parser changed nothing).
            # Print BOTH — what happened, then what would fix it. Deciding which of the
            # two to show would mean classifying the exception text, and the six modules
            # word their failures differently ("missing", "not found", "need Go
            # toolchain", "No module named ..."), so any such test is wrong for some.
            msg = f"  {LABEL[moddir]:<8} {s['files']:>5} files    SKIPPED — {s['reason'][:110]}"
            if s["needs"]:
                msg += f"\n  {'':<8} {'':>5}                 needs {s['needs']}"
            print(msg)          # NOT `line` — that name holds the "=" separator below

        refuted = [(LABEL[m], f) for m in sorted(langs) for f in langs[m]["findings"]
                   if f["disp"] == "REFUTED"]
        if refuted:
            print("-" * 72)
            print("REFUTED — attacker-controlled data reaches a sink unsubstituted (accusations):")
            for lbl, f in refuted:
                print(f"  [{lbl}] {f['file']}:{f['line']}  {f['name']}  ({f['ctx']})")

        if show_open:
            openf = [(LABEL[m], f) for m in sorted(langs) for f in langs[m]["findings"]
                     if f["disp"] == "OPEN"]
            if openf:
                print("-" * 72)
                print("OPEN — a sink is reached but the flow is unverifiable (not cleared, not accused):")
                for lbl, f in openf:
                    print(f"  [{lbl}] {f['file']}:{f['line']}  {f['name']}  ({f['ctx']})")

        if report["uncovered"]:
            print("-" * 72)
            outs = ", ".join(f"{e} ({n})" for e, n in sorted(report["uncovered"].items()))
            print(f"Out of scope — NOT analysed, NOT 'safe': {outs}")
        print(line)

    analysed = len(langs)
    n_skipped = len(skipped)
    print(f"{analysed} language(s) analysed, {n_skipped} skipped; "
          f"{report['total_refuted']} REFUTED across the project.")
    if not quiet:
        print("Each language is analysed on its own — cross-language flows are not "
              "tracked and stay OPEN, never guessed.")


if __name__ == "__main__":
    main()
