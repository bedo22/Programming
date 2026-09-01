#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cli — argparse subparsers (help generated, not hand-written docstring)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    from shelf_core import __version__ as _version  # S0.4: version stamp (shelf_core/__init__.py)
    from shelf_core.registry import COMMANDS
    p = argparse.ArgumentParser(prog="shelf", description="shelf — fidelity-gated pipeline (stdlib only)")
    p.add_argument("--version", action="version", version=f"shelf {_version}")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, entry in COMMANDS.items():
        sp = sub.add_parser(name, help=entry["help"])
        for spec in entry["args"]:
            arg_name, kwargs = spec
            if arg_name.startswith("-"):
                sp.add_argument(arg_name, **kwargs)
            else:
                sp.add_argument(arg_name, **kwargs)
        # D8.14: --describe is accepted for EVERY command (the contract
        # printer) — argparse would otherwise reject it (or demand required
        # positionals) before dispatch could handle it.
        sp.add_argument("--describe", action="store_true",
                        help="print this tool's contract (JSON) and exit")
        if name == "verify":
            # sub-actions listed from verify's own lane registry (P6.5 keeps
            # even this derivation — the lane help is never hand-written)
            from shelf_core.commands.verify import COMMANDS as _VC
            sp.help = "verification lane: " + " | ".join(sorted(_VC))
    return p


def main(argv: list[str] | None = None):
    import sys
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        # Match dispatch: bare `python3 tools/shelf.py` prints docstring, not argparse error
        from shelf_core import dispatch as legacy
        print(legacy.__doc__)
        sys.exit(0)
    # D8.14: `--describe` (anywhere after the command) prints the tool's
    # contract from the registry and exits — BEFORE argparse, which would
    # otherwise reject it or demand required positionals. ADR 0006.
    if len(argv) >= 2 and "--describe" in argv[1:]:
        from shelf_core.dispatch import describe_command
        describe_command(argv[0])
        sys.exit(0)
    # Keep --version / --help via argparse (AGENTS.md contract)
    if "--version" in argv or "-h" in argv or "--help" in argv:
        build_parser().parse_args(argv)
    from shelf_core import dispatch as legacy
    sys.argv = ["shelf.py"] + argv
    legacy.main()
