#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dispatch — top-level shelf command. See `shelf.py --help` and `shelf.py --describe` for the full command registry."""
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
