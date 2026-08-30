#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""shelf — fidelity-gated production pipeline for the investing reference shelf.

Stdlib only. Immutable transcripts in, distilled notes and HTML topic docs out,
with a mechanical check gate over every verbatim quote.

Usage:
    python3 tools/shelf.py inventory              # index all sessions -> reference/inventory.md
    python3 tools/shelf.py lines KEY [LO] [HI]    # numbered view of a session's clean transcript
    python3 tools/shelf.py lift KEY               # paste-ready quotes from stdin phrases
    python3 tools/shelf.py pins [--fix] KEY|NOTE.md
                                                  # verify every quote's minute (exit 0 = clean)
    python3 tools/shelf.py scaffold KEY|A-B       # blank session note(s) from the template
    python3 tools/shelf.py scaffold doc KEY [--topics] [TITLE]
                                                  # topic-doc skeleton from the house template
    python3 tools/shelf.py draft KEY              # doc draft from a filled session note
    python3 tools/shelf.py check [SCOPE]          # the gate: all | cs|ex|rr | block | KEY | A-B
                                                  # | a direct path to one .md/.html file
    python3 tools/shelf.py quotes KEY              # diagnostic: extract all quoted spans with locations
    python3 tools/shelf.py selftest               # fixture-based self test (cleans up after itself)

Session keys: bare NNN means cs (e.g. ``pins 002`` == ``pins cs-002``);
``cs-NNN`` / ``rr-NNN`` are zero-padded 3-digit; extras are slugs: ``ex-<slug>``.
Scopes for check (and bare A-B scaffolding): nothing (= all), a playlist slug
(cs/ex/rr), a block name, a single key, or A-B (bare A-B applies to cs).

Citation grammar: verbatim quotes use straight DOUBLE quotes "..." with a
trailing same-line cite — "text" (cs-002, 07:31) or a range
(cs-002, 07:31–07:58); the comma-less form "text" (cs-002 07:31) is accepted
too. Single-quoted '...' is scare quoting and is never scanned. A floating
HH:MM is never a cite; minutes count only right after a session key. Every
double-quoted span of >=4 tokens without a same-line cite is flagged ("uncited
quote"); 1–3-token quoted spans are labels and skipped.

This script never writes under transcripts/ — read-only there.
"""
import bisect
import re
import sys
from pathlib import Path

try:
    from .config import ROOT, REF, TEMPLATES, TRANSCRIPTS, INVENTORY
except ImportError:
    from config import ROOT, REF, TEMPLATES, TRANSCRIPTS, INVENTORY  # type: ignore

# --- config-driven overrides (generic source of truth, absorbs AR fork) ---
# If config/project.yaml exists, corpus.* overrides EN defaults so the same
# binary works for Investing (rr/cs/ex, "text" (rr-002, 07:31)) and فقه-النفس
# (is-NNN, «text» — المجلس N، HH:MM / سطر M, multi-clean fallback).
CONFIG_PATH = ROOT / "config" / "project.yaml"
CONFIG: dict = {}
if CONFIG_PATH.exists():
    try:
        import yaml  # type: ignore
        CONFIG = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}
    except Exception:
        CONFIG = {}
_corpus = CONFIG.get("corpus", {}) if isinstance(CONFIG, dict) else {}
if _corpus.get("transcripts_dir"):
    # e.g. "نص-ألف-باء-الزواج/clean" or "transcripts/rational-reminder/clean"
    td = _corpus["transcripts_dir"]
    TRANSCRIPTS = ROOT / td if not str(td).startswith("/") else Path(td)
# Optional clean candidates fallback (AR multi-clean)
_CLEAN_CANDIDATES: list[Path] | None = None
if _corpus.get("clean_candidates"):
    _CLEAN_CANDIDATES = [ROOT / p for p in _corpus["clean_candidates"]]
# Quote style (AR: «» vs EN: "")
QUOTE_OPEN = _corpus.get("quote", {}).get("open", '"') if isinstance(_corpus.get("quote"), dict) else '"'
QUOTE_CLOSE = _corpus.get("quote", {}).get("close", '"') if isinstance(_corpus.get("quote"), dict) else '"'
# AR-specific regexes (always defined, used when quote style is «» or key_pattern is is-)
LINE_RE = re.compile(r"سطر\s+([\d\s–\-،,]+)")
MIN_RE_AR = re.compile(r"(?:المجلس\s+\d{1,3}\s*[،,]\s*|المجلس\s+|—\s*)(\d{1,2}:\d{2})(?:[–\-]\s*(\d{1,2}:\d{2}))?(?!\d)")

# ---------------- playlists ----------------
# slug -> directory name under reference/ and transcripts/, plus display name.
# Helpers moved to shelf_core.helpers (batch, 818 lines) — re-exported
try:
    from .playlists import *
    from .transcript import *
    from .notes import *
    from .citation import *
except ImportError:
    from playlists import *  # type: ignore
    from transcript import *  # type: ignore
    from notes import *  # type: ignore
    from citation import *  # type: ignore
# cmd_inventory moved to shelf_core.commands.inventory (via helpers)
try:
    from .commands.inventory import cmd_inventory
except ImportError:
    from commands.inventory import cmd_inventory  # type: ignore


# cmd_lines moved to shelf_core.commands.lines
try:
    from .commands.lines import cmd_lines
except ImportError:
    from commands.lines import cmd_lines  # type: ignore


# cmd_lift moved to shelf_core.commands.lift
try:
    from .commands.lift import cmd_lift
except ImportError:
    from commands.lift import cmd_lift  # type: ignore
# cmd_pins moved to shelf_core.commands.pins
try:
    from .commands.pins import cmd_pins
except ImportError:
    from commands.pins import cmd_pins  # type: ignore
# cmd_scaffold moved to shelf_core.commands.scaffold
try:
    from .commands.scaffold import cmd_scaffold
except ImportError:
    from commands.scaffold import cmd_scaffold  # type: ignore
# cmd_draft moved to shelf_core.commands.draft
try:
    from .commands.draft import cmd_draft
except ImportError:
    from commands.draft import cmd_draft  # type: ignore
# cmd_check moved to shelf_core.commands.check
try:
    from .commands.check import cmd_check
except ImportError:
    from commands.check import cmd_check  # type: ignore
# cmd_selftest moved to shelf_core.commands.selftest
try:
    from .commands.selftest import cmd_selftest
except ImportError:
    from commands.selftest import cmd_selftest  # type: ignore
# cmd_quotes moved to shelf_core.commands.quotes
try:
    from .commands.quotes import cmd_quotes
except ImportError:
    from commands.quotes import cmd_quotes  # type: ignore
# draft-note (absorbed from Politics/is-040 builder, verified matcher)
try:
    from .commands.draft_note import cmd_draft_note
except ImportError:
    try:
        from commands.draft_note import cmd_draft_note  # type: ignore
    except ImportError:
        cmd_draft_note = None  # type: ignore

# evdoc (evidence-doc one-write from EVIDOC.yaml — doc-side mirror of draft-note)
try:
    from .commands.evdoc import cmd_evdoc
except ImportError:
    try:
        from commands.evdoc import cmd_evdoc  # type: ignore
    except ImportError:
        cmd_evdoc = None  # type: ignore

# verify (verification lane tooling: worklist | quran | dorar | locate | apply)
try:
    from .commands.verify import cmd_verify
except ImportError:
    try:
        from commands.verify import cmd_verify  # type: ignore
    except ImportError:
        cmd_verify = None  # type: ignore


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "inventory":
        cmd_inventory()
    elif cmd == "lines":
        cmd_lines(sys.argv[2:])
    elif cmd == "lift":
        cmd_lift(sys.argv[2:])
    elif cmd == "pins":
        cmd_pins(sys.argv[2:])
    elif cmd == "scaffold":
        cmd_scaffold(sys.argv[2:])
    elif cmd == "draft":
        cmd_draft(sys.argv[2:])
    elif cmd == "draft-note":
        if cmd_draft_note is None:
            sys.exit("draft-note not available")
        cmd_draft_note(sys.argv[2:])
    elif cmd == "evdoc":
        if cmd_evdoc is None:
            sys.exit("evdoc not available")
        cmd_evdoc(sys.argv[2:])
    elif cmd == "verify":
        if cmd_verify is None:
            sys.exit("verify not available")
        cmd_verify(sys.argv[2:])
    elif cmd == "check":
        cmd_check(sys.argv[2:])
    elif cmd == "quotes":
        cmd_quotes(sys.argv[2:])
    elif cmd == "selftest":
        cmd_selftest()
    else:
        sys.exit(f"Unknown command: {cmd} — run `python3 tools/shelf.py` for usage")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        # downstream closed the pipe (e.g. `... | head`) — exit quietly
        import os
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        sys.exit(0)
