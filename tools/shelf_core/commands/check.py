#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""commands/check — moved from _legacy.py (batch)."""
from __future__ import annotations
import sys, re
from pathlib import Path
try:
    from shelf_core.playlists import *
    from shelf_core.transcript import *
    from shelf_core.notes import *
    from shelf_core.citation import *
    from shelf_core.match import tokens, subseq
    from shelf_core.config import ROOT, REF
    from shelf_core.citation import *
    # check helpers live in draft.py after split — no cycle (draft imports same base)
    from shelf_core.commands.draft import parse_scope, playlist_docs, doc_in_scope, note_in_scope, check_doc, check_note
except ImportError:
    from playlists import *  # type: ignore
    from transcript import *  # type: ignore
    from notes import *  # type: ignore
    from citation import *  # type: ignore
    from match import tokens, subseq  # type: ignore
    from config import ROOT, REF  # type: ignore
    from draft import parse_scope, playlist_docs, doc_in_scope, note_in_scope, check_doc, check_note  # type: ignore
def cmd_check(argv=None):
    argv = argv or []
    scope = parse_scope(argv[0]) if argv else None
    fails = []
    if scope is not None and scope[0] == "file":
        p = scope[1]
        print(f"Checking single file: {os_rel(p, ROOT)}")
        if p.suffix == ".html":
            check_doc(p, "adhoc", fails)
        else:
            check_note(p, fails)
    else:
        for doc, pl in playlist_docs():
            if not doc_in_scope(doc, pl, scope):
                continue
            print(f"Doc: {os_rel(doc, ROOT)}")
            check_doc(doc, pl, fails)
        # config-driven playlists (cs/ex/rr + any registered flat shelf, e.g. is)
        for pl in playlist_keys():
            d = notes_dir(pl)
            for note in sorted(d.glob("*.md")) if d.is_dir() else []:
                if note.name == "README.md":
                    continue
                note_pl, ident = note_ident(note)
                if note_pl is None:
                    continue
                if not note_in_scope(note_pl, ident, scope):
                    continue
                print(f"Note: {os_rel(note, ROOT)}")
                check_note(note, fails)
    sessions = load_sessions()
    if fails:
        print(f"\n--- summary: {len(fails)} failed check(s) ---")
        hist = {}
        for f in fails:
            m = re.search(rf"\b({numeric_slugs()})-(\d{{3}})", f)
            if m:
                b = block_of(int(m.group(2)), m.group(1))
            elif "ex-" in f:
                b = "Extras"
            else:
                b = "other"
            hist[b] = hist.get(b, 0) + 1
        print("--- flags by block ---")
        for b, c in sorted(hist.items(), key=lambda kv: -kv[1]):
            print(f"  {b}: {c}")
    else:
        print("\n✓ all citations, quotes, links and statuses intact")
    noted = sum(1 for s in sessions if find_note(s["key"]))
    print(f"Sessions: {len(sessions)} | with notes: {noted} | "
          f"without notes: {len(sessions) - noted}")
    sys.exit(1 if fails else 0)

# ---------------- command: selftest ----------------

