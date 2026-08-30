#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""commands/pins — moved from _legacy.py (batch)."""
from __future__ import annotations
import sys, re, re
from pathlib import Path
try:
    from shelf_core.playlists import *
    from shelf_core.playlists import _slug_title  # underscore not exported by *
    from shelf_core.transcript import *
    from shelf_core.notes import *
    from shelf_core.notes import _scanned_region, os_rel  # underscore not exported by *
    from shelf_core.citation import *
    from shelf_core.match import tokens, subseq
    from shelf_core.config import ROOT, REF
    from shelf_core.citation import *
    from shelf_core.commands.lift import fix_note  # pins --fix reuses lift's fixer
except ImportError:
    from playlists import *  # type: ignore
    from playlists import _slug_title  # type: ignore
    from transcript import *  # type: ignore
    from notes import *  # type: ignore
    try:
        from notes import _scanned_region, os_rel  # type: ignore
    except ImportError:
        pass
    from citation import *  # type: ignore
    from match import tokens, subseq  # type: ignore
    from config import ROOT, REF  # type: ignore
    try:
        from lift import fix_note  # type: ignore
    except ImportError:
        from commands.lift import fix_note  # type: ignore
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
    if "\ufffd" in _scanned_region(txt):
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
    records = scan_lines(txt)
    c = report_records(records, src, sess_key, note.name)
    print(f"\nQuoted spans: {c['quoted']} ({c['checked']} verified, "
          f"{c['labels']} skipped as 1–3-token labels).")
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


