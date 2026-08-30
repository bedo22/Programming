#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""config — load_config with validation, no import side-effects."""

from __future__ import annotations

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
    except Exception:
        return {}


def corpus_cfg(config: dict | None = None, root: Path | None = None) -> dict:
    cfg = config if config is not None else load_config(root)
    return cfg.get("corpus", {}) if isinstance(cfg, dict) else {}


def gates_cfg(config: dict | None = None, root: Path | None = None) -> dict:
    cfg = config if config is not None else load_config(root)
    return cfg.get("gates", {}) if isinstance(cfg, dict) else {}


# Paths — single source (was hardcoded in _legacy.py, now here)
# _legacy.py lived at tools/shelf.py (2 levels to root), now at tools/shelf_core/_legacy.py (3 levels)
ROOT = Path(__file__).resolve().parent.parent.parent
REF = ROOT / "reference"
TEMPLATES = ROOT / "templates"
TRANSCRIPTS = ROOT / "transcripts"
INVENTORY = REF / "inventory.md"
