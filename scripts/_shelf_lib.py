#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_shelf_lib — merged common for all shelf gates/ledgers (small, stdlib only).

Absorbs the 4 things previously copy-pasted between doc-gate.py / doc-coverage.py:
  load_config(), KEY_PAT / CITE, key_from_match(), allowed_scripts, claim_mass().

Config-driven via config/project.yaml (corpus.* / gates.*), fallback to EN
defaults (Investing: rr-XXX, "text" (rr-002, 07:31)) so zero-config stays green.
"""

from __future__ import annotations

import os
import re
import glob
from pathlib import Path

# ---------- config ----------

# C3.2: find_root/load_config/corpus_cfg/gates_cfg used to be a byte-near-
# identical copy of shelf_core.config here — THREE loaders reading the same
# file was exactly how two components could disagree silently. The scripts
# always ship beside tools/ (sync.sh copies the pair), so the package import
# is always available; re-export so `from _shelf_lib import load_config`
# keeps working in every gate script.
import sys

_TOOLS = Path(__file__).resolve().parent.parent / "tools"
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from shelf_core.config import (find_root, load_config, corpus_cfg, gates_cfg)  # noqa: E402,F401

# ---------- key / cite ----------

def key_pattern(config: dict | None = None) -> str:
    return corpus_cfg(config).get("key_pattern", r"rr-(\d{3})")


def quote_style(config: dict | None = None) -> tuple[str, str]:
    q = corpus_cfg(config).get("quote", {})
    if isinstance(q, dict):
        return q.get("open", '"'), q.get("close", '"')
    return '"', '"'


def cite_regex(config: dict | None = None) -> re.Pattern:
    pat = key_pattern(config)
    # HH:MM must follow the key directly — no floating HH:MM (Quran 49:12 guard)
    return re.compile(pat + r"\s*[,(]\s*\d{1,2}:\d{2}")


def key_from_match(m: re.Match, key_pat: str | None = None) -> str | None:
    """Extract normalized key from a CITE match."""
    g = m.group(0)
    pat = key_pat or r"rr-(\d{3})"
    mm = re.search(pat, g)
    if not mm:
        return None
    if mm.groups():
        # rr-(\d{3}) style: prefix + captured number
        prefix = g[: g.find(mm.group(1))].rstrip(" (,")
        return (prefix + mm.group(1)).strip()
    return mm.group(0).split(",")[0].split("(")[0].strip()

# ---------- notes / claim mass ----------

def notes_dir(root: Path | None = None, config: dict | None = None) -> Path:
    root = Path(root or find_root()).resolve()
    cfg = corpus_cfg(config)
    td = cfg.get("transcripts_dir", "")
    if not td:
        # default: Investing layout
        return root / "reference" / "rational-reminder" / "notes"
    if td.startswith("reference"):
        return root / td
    if "clean" in td:
        return root / Path(td.replace("/clean", "/notes").replace("transcripts", "reference"))
    return root / td


def claim_mass(key: str, root: Path | None = None, config: dict | None = None) -> int | None:
    """Claim mass for a session key: | C# | rows / محاور / auto.
    A5.3(d): the branch counting is notes.claims_count (one grammar home);
    this wrapper keeps its own pick-the-dominant-form 'auto' semantics."""
    from shelf_core.notes import claims_count
    root = Path(root or find_root()).resolve()
    cfg = corpus_cfg(config)
    source = cfg.get("claim_source", "auto")
    nd = notes_dir(root, config)
    hits = glob.glob(str(nd / f"{key}-*.md"))
    if len(hits) != 1:
        # also search recursively (AR fallback)
        hits = glob.glob(str((root / "reference").rglob(f"{key}-*.md")))  # type: ignore
        # fallback glob already handled above; if still not 1, give up
        if len(hits) != 1:
            return None
        p = Path(hits[0])
    else:
        p = Path(hits[0])
    raw = p.read_text(encoding="utf-8", errors="replace")
    if source == "auto":
        c = claims_count(raw, "C#")
        m = claims_count(raw, "محاور")
        source = "C#" if c >= m else "محاور"
    return claims_count(raw, source)


def bucket_count(key: str, root: Path | None = None, config: dict | None = None) -> int:
    nd = notes_dir(root, config)
    hits = glob.glob(str(nd / f"{key}-*.md"))
    if len(hits) != 1:
        return 0
    txt = Path(hits[0]).read_text(encoding="utf-8", errors="replace")
    return len(set(re.findall(r"\[(\d{1,2}:\d{2})\]", txt)))

# ---------- script contamination ----------
# A5.4 hoist: the implementation lives in shelf_core.scriptcheck (one home);
# these names are re-exports so every gate script keeps its import.
from shelf_core.scriptcheck import (  # noqa: E402,F401
    check_allowed_scripts, check_pitfall_guards)
