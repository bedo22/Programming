#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""config — load_config with validation, no import side-effects."""

from __future__ import annotations

import sys
from pathlib import Path


def find_root(start: Path | None = None) -> Path:
    cur = Path(start or Path.cwd()).resolve()
    for _ in range(6):
        if (cur / "config" / "project.yaml").exists():
            return cur
        if (cur / "reference").is_dir() and (cur / "tools" / "shelf.py").exists():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return Path.cwd().resolve()


def load_config(root: Path | None = None) -> dict:
    root = Path(root or find_root()).resolve()
    p = root / "config" / "project.yaml"
    if not p.exists():
        return {}
    try:
        import yaml  # type: ignore
        return yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except Exception as e:
        # C3.3: a MALFORMED config used to be silently swallowed to {} — the shelf
        # then ran EN defaults with no hint why (verified: malformed YAML, silent
        # {}). Absence stays silent (a zero-config shelf is legitimate);
        # corruption is announced once, on stderr.
        print(f"config at {p} unreadable: {e} — running EN defaults", file=sys.stderr)
        return {}


def corpus_cfg(config: dict | None = None, root: Path | None = None) -> dict:
    cfg = config if config is not None else load_config(root)
    if not isinstance(cfg, dict):
        print(f"config unreadable: top-level YAML is {type(cfg).__name__}, "
              "expected a mapping — running EN defaults", file=sys.stderr)
        return {}
    c = cfg.get("corpus", {})
    if not isinstance(c, dict):
        print(f"config 'corpus' section is {type(c).__name__}, "
              "expected a mapping — running EN defaults", file=sys.stderr)
        return {}
    return c


def gates_cfg(config: dict | None = None, root: Path | None = None) -> dict:
    cfg = config if config is not None else load_config(root)
    if not isinstance(cfg, dict):
        return {}
    g = cfg.get("gates", {})
    return g if isinstance(g, dict) else {}


# Paths — single source, resolved LAZILY per process (PEP 562 __getattr__).
# Was: ROOT = Path(__file__).parent³ — module-location-derived, correct only
# while the package always ran as synced files *inside* a shelf. With the
# installed `shelf` CLI (editable venv pointing at the dev tree), __file__
# names the dev tree no matter where the command runs, so `doctor` from a
# shelf reported the dev tree's paths (witnessed red, 2026-09-01).
# Now: first attribute access resolves find_root() (cwd walk-up to
# config/project.yaml — the shelf the command was invoked from), then freezes
# into module globals for the process. Consumers keep binding
# `from .config import ROOT` unchanged: they import at process start (one
# shelf per invocation) and dereference only at call time (CodeGraph:
# ROOT 15 callers, TEMPLATES 7, INVENTORY 8, TRANSCRIPTS 5, REF 1; no
# import-time joins anywhere).
# Selftest's _PATCH still shadows these: it assigns real module attributes
# BEFORE consumer imports, and its subprocesses also run cwd=fxroot, so both
# mechanisms agree on the fixture root.
def _resolve_paths():
    root = find_root()
    return root, root / "reference", root / "templates", root / "transcripts"


def __getattr__(name):
    if name == "ROOT":
        root, _, _, _ = _resolve_paths()
        globals()["ROOT"] = root  # freeze for the process
        return root
    if name in ("REF", "TEMPLATES", "TRANSCRIPTS", "INVENTORY"):
        root, ref, tpl, tr = _resolve_paths()
        globals()["ROOT"] = root
        globals()["REF"] = ref
        globals()["TEMPLATES"] = tpl
        globals()["TRANSCRIPTS"] = tr
        globals()["INVENTORY"] = ref / "inventory.md"
        return globals()[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
