#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""commands/quotes — diagnostic: extract all quoted spans with locations.

W4.22: the [NO CITE] flag uses iter_cites() — the gate's own grammar — instead
of a hardcoded «المجلس» substring plus a floating-time regex that disagreed
with pins (a bare "07:00" after a quote marked it cited; a configured
non-Majlis keyword cite did not). W4.21: note discovery goes through
notes.find_note, inheriting the loud ambiguity refusal (first-hit glob[0]
previously picked silently). A5.3(e): spans come from parse_note (scan_lines)
— the width-filtered private pattern and the per-line loop are gone; heading
and exempt-section lines (fidelity tables' documented corruptions) no longer
pollute the diagnostic."""
from __future__ import annotations

import sys
from pathlib import Path

from shelf_core.config import find_root, load_config, corpus_cfg
from shelf_core.notes import find_note, parse_note

_root = find_root()
_cfg = load_config(_root)
_q = corpus_cfg(_cfg, _root).get("quote", {})
QUOTE_OPEN = _q.get("open", '"') if isinstance(_q, dict) else '"'
QUOTE_CLOSE = _q.get("close", '"') if isinstance(_q, dict) else '"'
REF = _root / "reference"


def cmd_quotes(argv):
    """quotes KEY — diagnostic: list all quoted spans with their line/cite
    locations, exactly as the gate's scan_lines pairs them."""
    if not argv:
        sys.exit("Usage: python3 tools/shelf.py quotes KEY|NOTE.md")
    target = argv[0]
    if "/" in target or target.endswith(".md"):
        note_path = Path(target)
        if not note_path.exists():
            sys.exit(f"No note found for {target}")
    else:
        note_path = find_note(target)
        if note_path is None:
            sys.exit(f"No note found for {target}")
    d = parse_note(note_path)
    for r in d["quotes"]:
        # A5.3(e): cited-ness is the parse record's own verdict (the gate's
        # pairing) — a cite is whatever the citation grammar pairs with the
        # line; floating times don't count.
        flag = "" if r["cited"] else " [NO CITE]"
        print(f"{note_path.name}:{r['line']}: {QUOTE_OPEN}{r['quote'][:60]}...{QUOTE_CLOSE}{flag}")
