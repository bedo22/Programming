#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""shelf — fidelity-gated production pipeline for a transcript reference shelf.

Born on the Investing shelf (its history is in the 1.0.0 CHANGELOG entry);
now grammar- and path-configurable per shelf via `config/project.yaml`
(C3.x): key_pattern, cite keyword, quote style, playlists, gate floors.
What THIS run resolves — root, grammar, paths — prints via
`python3 tools/shelf.py doctor` (read it before asking "why did it do
that?"; the grammar-home table is `references/DESIGN.md`).

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
import sys

# H2.7 receipt: an "optional clean candidates fallback" block stood here,
# defining _CLEAN_CANDIDATES from corpus.clean_candidates — but a repo-wide
# grep found ZERO consumers (nothing ever read the name). Deleted: dead config
# surface implies a feature someone half-shipped. If multi-clean fallback is
# ever needed, reintroduce it WITH its consumer in the same commit.

# ---------------- playlists ----------------
# H2.2: the star re-export block here (`from .playlists import *` etc. plus the
# flat fallbacks) provided names to NOTHING — every shim that used them moved to
# shelf_core.commands.* (an unbound-name audit of this module returns an empty
# set without the block). Deleted: it was a fourth import surface masking errors.
# cmd_inventory moved to shelf_core.commands.inventory (via helpers)
# P6.5: the elif chain is GONE — dispatch iterates the one registry
# (shelf_core.registry.COMMANDS). A command not in the registry is unknown;
# a module missing from disk fails loudly at import (never a silent None).


def describe_command(cmd: str):
    """D8.14: print a tool's contract from the registry (ADR 0006 source)."""
    import json
    from .registry import COMMANDS
    entry = COMMANDS.get(cmd)
    if entry is None:
        sys.exit(f"Unknown command: {cmd} — run `python3 tools/shelf.py` for usage")
    d = entry.get("describe", {})
    print(json.dumps({
        "name": cmd, "module": entry["module"], "func": entry["func"],
        "help": entry["help"], "usage_args": [a for a, _ in entry["args"]],
        "checks": d.get("checks", []), "exits": d.get("exits", {}),
        "pitfalls": d.get("pitfalls", []), "adrs": d.get("adrs", []),
    }, ensure_ascii=False, indent=1))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    cmd = sys.argv[1]
    from .registry import COMMANDS
    entry = COMMANDS.get(cmd)
    if entry is None:
        sys.exit(f"Unknown command: {cmd} — run `python3 tools/shelf.py` for usage")
    # D8.14: `--describe` prints the tool's contract from the registry —
    # checks, exits, PITFALLS tags, ADR links. ADR 0006: this is the source
    # the renderer generates references/tools/<name>.md from.
    if len(sys.argv) > 2 and sys.argv[2] == "--describe":
        describe_command(cmd)
        sys.exit(0)
    import importlib
    import inspect
    mod = importlib.import_module(f".commands.{entry['module']}", package="shelf_core")
    fn = getattr(mod, entry["func"], None)
    if fn is None:
        sys.exit(f"{entry['module']}.{entry['func']} not available")
    if len(inspect.signature(fn).parameters) == 0:
        # was: dispatch passed sys.argv[2:] to every command, so zero-arg
        # commands (inventory, selftest) crashed with TypeError before ever
        # running (fixed P6.10 — the smoke read exit 1 as 'usage' and missed
        # it). The signature inspection remains because the CLASS — a
        # registry that assumes uniform command signatures — regenerates
        # whenever a new zero-arg command is registered.
        fn()                      # zero-arg commands (inventory, selftest)
    else:
        fn(sys.argv[2:])


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        # downstream closed the pipe (e.g. `... | head`) — exit quietly
        import os
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        sys.exit(0)
