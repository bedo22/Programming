#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""commands/lines — moved from _legacy.py."""

from __future__ import annotations
import sys
from pathlib import Path

# H2.2: flat-layout fallback removed — the package is always a package.
from shelf_core.playlists import parse_session_key, session_key_of, get_session
from shelf_core.config import ROOT


def cmd_lines(argv):
    if not argv:
        sys.exit("usage: python3 tools/shelf.py lines KEY [FROM_LINE] [TO_LINE]")
    slug, ident = parse_session_key(argv[0])
    key = session_key_of(slug, ident)
    rec = get_session(key)
    if rec is None:
        sys.exit(f"No transcript file for session {key}")
    lines = (ROOT / rec["rel"]).read_text(
        encoding="utf-8", errors="replace").split("\n")
    # P6.10: a non-numeric line range printed a traceback (int() on prose) —
    # usage message instead, the one-write loud-refusal shape.
    _usage = "usage: python3 tools/shelf.py lines KEY [FROM_LINE] [TO_LINE] — FROM/TO must be line numbers"
    for i, arg in ((1, argv[1] if len(argv) > 1 else "1"),
                   (2, argv[2] if len(argv) > 2 else None)):
        if arg is not None and not arg.isdigit():
            sys.exit(_usage)
    lo = int(argv[1]) if len(argv) > 1 else 1
    hi = int(argv[2]) if len(argv) > 2 else len(lines)
    for i in range(max(1, lo), min(hi, len(lines)) + 1):
        print(f"{i:4d}  {lines[i - 1]}")
