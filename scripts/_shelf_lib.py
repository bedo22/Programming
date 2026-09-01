#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_shelf_lib — re-export shim over shelf_core.gatelib (B1, CLI wave).

The 7 helpers' ONE implementation is shelf_core/gatelib.py; this shim keeps
`import _shelf_lib` working in the scripts/ copies (which still ship beside
tools/ until the Phase C cutover deletes them). Behavior byte-identical:
every name below is the same object gatelib exports.
"""

from __future__ import annotations

# gatelib imports shelf_core relatively; make it importable from scripts/.
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent.parent / "tools"
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from shelf_core.gatelib import (  # noqa: E402,F401
    find_root, load_config, corpus_cfg, gates_cfg,
    key_pattern, quote_style, cite_regex, key_from_match,
    notes_dir, claim_mass, bucket_count,
    check_allowed_scripts, check_pitfall_guards,
)
