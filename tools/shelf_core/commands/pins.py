#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""commands/pins — moved from _legacy.py (batch)."""
from __future__ import annotations
import sys, re
from pathlib import Path
# H2.1/H2.2: explicit imports (tokens/subseq were imported but unused here).
from shelf_core.config import ROOT, TEMPLATES
from shelf_core.playlists import (DUPLICATE_SESSIONS, PLAYLIST_NAMES, _slug_title,
                                  get_session, notes_dir, parse_session_key, session_key_of)
from shelf_core.notes import (scanned_region, find_note, note_source_key, os_rel,
                              report_records, scan_lines, note_ident)
from shelf_core.transcript import CleanSource
from shelf_core.commands.lift import fix_note  # pins --fix reuses lift's fixer

def cmd_pins(argv):
    """pins [--fix] KEY|NOTE.md [KEY|NOTE.md ...] — extract every double-quoted span,
    verify its same-line cite against the transcript, flag uncited quotes.
    Multiple keys are all checked (earlier versions silently used only the first).
    Exit codes: 0 clean, 1 flagged."""
    fix = bool(argv) and argv[0] == "--fix"
    if fix:
        argv = argv[1:]
    if not argv:
        sys.exit("usage: python3 tools/shelf.py pins [--fix] KEY|NOTE.md [KEY|NOTE.md ...]")
    worst = 0
    for arg in argv:
        worst |= _pins_one(arg, fix)
    sys.exit(worst)


def _pins_one(arg, fix):
    if arg.endswith(".md"):
        note = Path(arg)
        if not note.exists():
            sys.exit(f"Note not found: {arg}")
        txt = note.read_text(encoding="utf-8")
        # A note TEMPLATE has a placeholder Session row by design, so no transcript can be
        # resolved against it -- and sys.exit() here killed an entire `pins reference/notes/*.md`
        # run on the template alone. notes-gate already exempts it loudly; pins must not be the
        # one command that leaves a permanent red line in every full sweep, because a red line
        # everyone learns to ignore hides the one that matters.
        if re.search(r"(?:قالب|template|skeleton)", note.name, re.I):
            print(f"PINS SKIP {note.name} (template — no session to pin against)")
            return 0
        sess_key = note_source_key(txt, note)
        if sess_key is None:
            sys.exit(f"Cannot resolve session for {note.name}: fill the | Session | metadata row "
                     "(or name the file cs-NNN-/rr-NNN-/ex-slug-…)")
    else:
        slug, ident = parse_session_key(arg)
        sess_key = session_key_of(slug, ident)
        note = find_note(sess_key)
        if note is None:
            sys.exit(f"No note for session {sess_key} — run `scaffold {sess_key}` first")
        txt = note.read_text(encoding="utf-8")
    if "\ufffd" in scanned_region(txt):
        print("✗ Note contains U+FFFD replacement characters in the scanned region "
              "— tokens silently shatter and quotes read as 'not found'; fix the "
              "word from the source first.")
        sys.exit(1)
    src = CleanSource(sess_key)
    if src.rec is None:
        sys.exit(f"No transcript file for session {sess_key}")
    if fix:
        n_fixed = fix_note(note)
        if n_fixed:
            print(f"Fixed {n_fixed} cite(s) in {note.name} — re-run pins (without "
                  "--fix) to confirm.\n")
        else:
            print("No auto-fixable citations.\n")
        txt = note.read_text(encoding="utf-8")
    # T9.1: the note's own playlist feeds keyword-cite resolution
    # (corpus.cite_playlist=self) — compute BEFORE scan_lines.
    _own_pl = None
    _ni = note_ident(note)
    if _ni and _ni[0]:
        _own_pl = _ni[0]
    records = scan_lines(txt, own_pl=_own_pl)
    from shelf_core.notes import _uncited_quotes_skip as _uq
    _skip = _uq()
    # T9.2: claims contract — with corpus.uncited_quotes=skip the uncited «»
    # records must not reach report_records (its summary still counts them).
    # Count them BEFORE the filter so the skip is loud, never silent.
    _narrative = 0
    if _skip:
        _narrative = sum(1 for r in records if not r["cited"])
        records = [r for r in records if r["cited"]]
    c = report_records(records, src, sess_key, note.name, uncited_skip=_skip)
    _n_total = c["quoted"] + _narrative   # claims lane is measured, not verified
    if _skip and _narrative:
        print(f"  (claims: {_narrative} uncited «» spans skipped as narrative "
              f"per corpus.uncited_quotes=skip — measured by doc-coverage, "
              f"not pins)")
    print(f"\nQuoted spans: {_n_total} ({c['checked']} verified, "
          f"{c['labels']} skipped as 1–3-token labels).")
    # A gate that examined nothing must not report green. Every cite in this shelf's ts- notes was
    # unparseable for the whole life of the batch -- an ASCII-vs-Arabic comma mismatch between the
    # generator and the matcher -- and every run said "Flags: 0" while quietly reporting
    # "0 verified". Zero flags with zero checks is not a pass, it is the tool not looking.
    _unverified_cited = c["quoted"] and not c["checked"]
    _all_empty = not _n_total
    if _unverified_cited or _all_empty:
        _n = sum(1 for r in records if r["cited"]) if _skip else c["quoted"]
        print(f"\n✗ NOTHING WAS VERIFIED in {note.name}: {_n} cited spans found, 0 verified. "
              f"'Flags: 0' here means the matcher saw nothing -- check that the cite form this "
              f"note writes is the form CITE_RE accepts (comma, keyword, key width).")
        return 1
    parts = []
    if c["uncited"]:
        parts.append(f"{c['uncited']} uncited")
    if c["mismatch"]:
        parts.append(f"{c['mismatch']} wrong minute/text")
    if c["missing"]:
        parts.append(f"{c['missing']} not found")
    cls = f" ({', '.join(parts)})" if parts else ""
    print(f"Flags: {len(c['fails'])}{cls}.")
    if c["soft"]:
        print(f"Advisory (digest-text «», not gating): {len(c['soft'])}.")
    return 1 if c["fails"] else 0


def _template(name: str) -> str:
    return (TEMPLATES / name).read_text(encoding="utf-8")


def _scaffold_note(key: str):
    if key in DUPLICATE_SESSIONS:
        print(f"{key} is a registered duplicate of "
              f"{DUPLICATE_SESSIONS[key]} (DOMAIN-MAP anomaly #2) — distill one "
              f"note under {DUPLICATE_SESSIONS[key]}")
        return False
    rec = get_session(key)
    if rec is None:
        print(f"No transcript file for session {key}")
        return False
    name = (f"{key}-{_slug_title(rec['title'])}.md" if rec["num"] is not None
            else f"{key}.md")
    out = notes_dir(rec["pl"]) / name
    if out.exists():
        print(f"Already exists: {os_rel(out, ROOT)}")
        return False
    tpl_name = "rr-session-note.md" if rec["pl"] == "rr" else "session-note.md"
    tpl = _template(tpl_name)
    tpl = (tpl.replace("{{SOURCE_PATH}}", rec["rel"])
              .replace("{{SESSION}}", key)
              .replace("{{PLAYLIST_NAME}}", PLAYLIST_NAMES[rec["pl"]])
              .replace("{{TITLE}}", rec["title"])
              .replace("{{BLOCK}}", rec["block"]))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(tpl, encoding="utf-8")
    print(f"Note -> {os_rel(out, ROOT)} (blank scaffold awaiting distillation)")
    return True


