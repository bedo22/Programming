#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cli — argparse subparsers (help generated, not hand-written docstring)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="shelf", description="shelf — fidelity-gated pipeline (stdlib only)")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("inventory", help="index all sessions -> reference/inventory.md")
    sp = sub.add_parser("lines", help="numbered view of clean transcript")
    sp.add_argument("key"); sp.add_argument("lo", nargs="?"); sp.add_argument("hi", nargs="?")
    sp = sub.add_parser("lift", help="paste-ready quotes from stdin phrases")
    sp.add_argument("key")
    sp = sub.add_parser("pins", help="verify every quote's minute (exit 0 = clean)")
    sp.add_argument("--fix", action="store_true"); sp.add_argument("targets", nargs="+")
    sp = sub.add_parser("scaffold", help="blank session note(s) from template")
    # --from-yaml/--from-json must be accepted HERE so argv reaches
    # cmd_scaffold's shim (which forwards to draft-note). argparse would
    # otherwise reject them before the shim ever runs (dead-shim bug).
    sp.add_argument("target"); sp.add_argument("--topics", action="store_true")
    sp.add_argument("--from-yaml", dest="from_yaml"); sp.add_argument("--from-json", action="store_true")
    sp.add_argument("--from-notes", dest="from_notes"); sp.add_argument("title", nargs="?")
    sp = sub.add_parser("draft", help="doc draft from filled session note")
    sp.add_argument("key")
    sp = sub.add_parser("draft-note", help="scripted note builder from MEH.yaml (via verified matcher, PITFALLS.md A/C/H)")
    sp.add_argument("key"); sp.add_argument("--from-yaml", dest="from_yaml"); sp.add_argument("--from-json", action="store_true")
    sp = sub.add_parser("evdoc", help="evidence-doc one-write from EVIDOC.yaml (doc-side mirror of draft-note)")
    sp.add_argument("--from-yaml", dest="from_yaml"); sp.add_argument("--out", nargs="?"); sp.add_argument("--dump"); sp.add_argument("--seed")
    try:                                   # help derived from the registry, like the usage string —
        from shelf_core.commands.verify import COMMANDS as _VC   # a hand-written list here was
    except ImportError:                    # already stale twice (missing sync-docs, then shamela)
        from commands.verify import COMMANDS as _VC  # type: ignore
    sp = sub.add_parser("verify", help="verification lane: " + " | ".join(sorted(_VC)))
    sp.add_argument("action", nargs="?"); sp.add_argument("rest", nargs="*")
    sp.add_argument("--key"); sp.add_argument("--ref"); sp.add_argument("--stem")
    sp.add_argument("--phrase"); sp.add_argument("--title"); sp.add_argument("--from-json", dest="from_json")
    sp.add_argument("--find")  # verify quran --find "asr phrase" (Pitfall R: register in the SAME edit)
    sp.add_argument("--amend", action="store_true"); sp.add_argument("--out")
    sp.add_argument("--bodies", action="store_true")
    sp.add_argument("--dry", action="store_true")
    sp.add_argument("--add-section", action="store_true")
    sp.add_argument("--json", action="store_true")  # machine-readable output (shamela find)
    sp = sub.add_parser("check", help="gate: all | playlist | block | KEY | path")
    sp.add_argument("scope", nargs="?")
    sub.add_parser("quotes", help="diagnostic: extract all quoted spans")
    sub.add_parser("selftest", help="fixture-based self test")
    return p


def main(argv: list[str] | None = None):
    import sys
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        # Match dispatch: bare `python3 tools/shelf.py` prints docstring, not argparse error
        from shelf_core import dispatch as legacy
        print(legacy.__doc__)
        sys.exit(0)
    # argparse here is for HELP only -- dispatch re-reads sys.argv and the commands parse
    # their own flags. parse_args() therefore acted as a GATE: a flag not listed in
    # build_parser() was rejected before the command ever ran (the "dead-shim" bug: it bit
    # --json and --find, and Pitfall R was written and reproduced in the same session).
    # parse_known_args keeps the help and lets a command's own flags through; unrecognised
    # input is reported rather than silently swallowed, so typos stay visible.
    _ns, _extra = build_parser().parse_known_args(argv)
    if _extra:
        print("shelf: passing through unrecognised arguments: " + " ".join(_extra), file=sys.stderr)
    from shelf_core import dispatch as legacy
    sys.argv = ["shelf.py"] + argv
    legacy.main()
