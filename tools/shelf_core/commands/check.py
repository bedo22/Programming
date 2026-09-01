#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""commands/check — moved from _legacy.py (batch)."""
from __future__ import annotations
import sys, re
from pathlib import Path
# H2.1/H2.2: explicit imports — the star-import blocks shadowed each other
# (two `from ...citation import *` copies) and the flat fallbacks masked real
# import errors. Lists derived from AST usage + grep audit (reports/h2-import-map.txt).
from shelf_core.config import ROOT, find_root
from shelf_core.playlists import (block_of, load_sessions, notes_dir, numeric_slugs,
                                  playlist_keys, DEFAULT_PLAYLIST)
from shelf_core.notes import find_note, note_ident, os_rel
# check helpers live in draft.py after split — no cycle (draft imports same base)
from shelf_core.commands.draft import parse_scope, playlist_docs, doc_in_scope, note_in_scope, check_doc, check_note
def cmd_check(argv=None):
    argv = argv or []
    scope = parse_scope(argv[0]) if argv else None
    fails = []
    n_docs = n_notes = 0
    if scope is not None and scope[0] == "file":
        p = scope[1]
        print(f"Checking single file: {os_rel(p, ROOT)}")
        # T7.1 find: the file branch never set the counters, so the scoped
        # zero-match guard below read undefined names — a single-file check
        # CRASHED (UnboundLocalError) whenever the file had no fails.
        if p.suffix == ".html":
            n_docs += 1
            check_doc(p, "adhoc", fails)
        else:
            n_notes += 1
            check_note(p, fails)
    else:
        for doc, pl in playlist_docs():
            if not doc_in_scope(doc, pl, scope):
                continue
            n_docs += 1
            print(f"Doc: {os_rel(doc, ROOT)}")
            check_doc(doc, pl, fails)
        # config-driven playlists (cs/ex/rr + any registered flat shelf, e.g. is)
        # F12: flat shelves share ONE notes dir across all playlists — without
        # a seen-set the sweep visited reference/notes once PER PLAYLIST
        # (measured: fqhn 9 playlists → the whole corpus checked 9×, every
        # census count inflated 9×, check runtime likewise).
        _seen_notes = set()
        for pl in playlist_keys():
            d = notes_dir(pl)
            for note in sorted(d.glob("*.md")) if d.is_dir() else []:
                if note.name == "README.md":
                    continue
                if note in _seen_notes:
                    continue
                _seen_notes.add(note)
                # T9.1: note templates live in the notes dir on some shelves
                # (قالب-ملاحظة-جلسة.md) — same exemption pins applies; never a
                # session to gate, announced so it is not a silent skip.
                if re.search(r"(?:قالب|template|skeleton)", note.name, re.I):
                    print(f"note template skipped (no session to gate): {note.name}")
                    continue
                note_pl, ident = note_ident(note)
                if not note_in_scope(note_pl, ident, scope):
                    continue
                n_notes += 1
                print(f"Note: {os_rel(note, ROOT)}")
                check_note(note, fails)
    sessions = load_sessions()
    # W4.4: zero-corpus refusal — a whole-corpus check that resolved NOTHING is
    # not a pass, it is a wrong-directory run (the recorded staging false-green:
    # "Sessions: 0" with exit 0 on a tree with no data dirs). Scoped checks are
    # exempt: a typo'd KEY must report "no match", not "no corpus".
    if scope is None and n_docs == 0 and n_notes == 0 and not sessions:
        print(f"no corpus resolved under {ROOT} — run from the shelf root or sync tools/",
              file=sys.stderr)
        sys.exit(2)
    # P6.2: a SCOPED run that matched nothing is not a pass either — say what
    # the scope bound to (was: exit 0 with no output at all).
    if scope is not None and n_docs == 0 and n_notes == 0:
        _bound = scope[1] if scope[0] == "sess" else DEFAULT_PLAYLIST
        print(f"scope bound to playlist '{_bound}' — 0 files matched", file=sys.stderr)
        sys.exit(2)
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
    # A note can silently lag the spec it was built from: the spec is an input, the note is
    # generated output, and nothing in the pipeline compared them. A worker corrected 8 register
    # minutes in ts-017.json AFTER its note had been scaffolded and committed, and the stale note
    # passed pins and notes-gate exactly as cleanly as the correct one would have.
    # C3.5: was a private __file__-walk looking for `reference/` — a fourth root
    # idiom that could disagree with everything else. find_root() is THE root now.
    _root = find_root()
    stale = []
    for s in sessions:
        npath = find_note(s["key"])
        if not npath:
            continue
        npath = Path(npath)
        if not npath.is_absolute():
            npath = _root / npath
        if not npath.exists():
            continue
        nt = npath.stat().st_mtime
        for cand in (_root / "_verify" / "meh" / f"{s['key']}.json",
                     _root / "_verify" / "meh" / f"{s['key']}.yaml"):
            if cand.exists() and cand.stat().st_mtime > nt + 1:
                stale.append(f"{s['key']} — {cand.name} is newer than the note")
                break
    if stale:
        print(f"STALE NOTES ({len(stale)}) — re-scaffold from the current spec (blocks: W4.11 decision):")
        for x in stale:
            print(f"  {x}")
        print()
        # W4.11 DECISION (recorded in shelf-improvements/DECISIONS.md): stale
        # notes GATE. A stale note is wrong content already committed — the
        # detector was printing evidence of a defect and then passing the gate.
        fails.extend(f"STALE {x}" for x in stale)
    noted = sum(1 for s in sessions if find_note(s["key"]))
    print(f"Sessions: {len(sessions)} | with notes: {noted} | "
          f"without notes: {len(sessions) - noted}")
    sys.exit(1 if fails else 0)

# ---------------- command: selftest ----------------

