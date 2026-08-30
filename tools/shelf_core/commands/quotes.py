#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""commands/quotes — diagnostic: extract all quoted spans with locations.
Moved from _legacy.py (logical split, behavior preserved)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    from shelf_core.config import load_config, find_root
    _root = find_root()
    _cfg = load_config(_root)
    _corpus = _cfg.get("corpus", {}) if isinstance(_cfg, dict) else {}
    _q = _corpus.get("quote", {}) if isinstance(_corpus, dict) else {}
    QUOTE_OPEN = _q.get("open", '"') if isinstance(_q, dict) else '"'
    QUOTE_CLOSE = _q.get("close", '"') if isinstance(_q, dict) else '"'
    REF = _root / "reference"
except Exception:
    QUOTE_OPEN, QUOTE_CLOSE = '"', '"'
    REF = Path.cwd() / "reference"


def cmd_quotes(argv):
    """quotes KEY — diagnostic: list all quoted spans with their line/cite locations.
    Generic; respects QUOTE_OPEN/CLOSE and cite style from config."""
    if not argv:
        sys.exit("Usage: python3 tools/shelf.py quotes KEY|NOTE.md")
    target = argv[0]
    note_path = None
    if "/" in target or target.endswith(".md"):
        note_path = Path(target)
    else:
        cands = list((REF / "notes").glob(f"{target}-*.md"))
        if not cands:
            cands = list(REF.rglob(f"{target}-*.md"))
        if cands:
            note_path = cands[0]
    if note_path is None or not note_path.exists():
        sys.exit(f"No note found for {target}")
    text = note_path.read_text(encoding="utf-8", errors="replace")
    qo = re.escape(QUOTE_OPEN)
    qc = re.escape(QUOTE_CLOSE)
    pat = re.compile(qo + r"(.{10,400}?)" + qc)
    for i, line in enumerate(text.splitlines(), 1):
        for m in pat.finditer(line):
            span = m.group(1).strip()
            rest = line[m.end():]
            has_cite = "المجلس" in rest or re.search(r"\d{1,2}:\d{2}", rest)
            flag = "" if has_cite else " [NO CITE]"
            print(f"{note_path.name}:{i}: {QUOTE_OPEN}{span[:60]}...{QUOTE_CLOSE}{flag}")
