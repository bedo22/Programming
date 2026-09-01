#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""commands/doctor — what am I actually running against? (C3.4, read-only)

The config family's failure mode was never a crash; it was silence: the shelf
ran EN defaults against a corpus it could not see (staging `check` false-greened
at Sessions: 0 on a 184-note corpus; `pins` could not resolve an AR note), and
nothing on screen said why. doctor makes every resolution explicit — root,
config, grammar, paths, playlists — so a "why did it do that?" moment has a
starting pointer. Pairs with the C3.6 decision record (data stays tree-locked).
"""
from __future__ import annotations

from shelf_core import __version__
from shelf_core.config import (find_root, load_config, corpus_cfg,
                               ROOT, REF, TEMPLATES, TRANSCRIPTS, INVENTORY)
from shelf_core.citation import KEY_PATTERN, CITE_KEYWORD, CITE_HAS_KEYWORD, _PRIMARY
from shelf_core.playlists import (DEFAULT_PLAYLIST, PLAYLIST_NAMES, PLAYLIST_DIRS,
                                  FLAT_PLAYLISTS, playlist_keys, load_sessions,
                                  KEY_PREFIXES, PLAYLIST_TRANSCRIPTS, clean_dir)


def cmd_doctor(argv=None):
    root = find_root()
    cfg = load_config(root)
    corp = corpus_cfg(cfg, root)
    cfg_path = root / "config" / "project.yaml"
    print("shelf doctor — resolved runtime configuration")
    print(f"  version        : {__version__}")
    how = ("config/project.yaml" if cfg_path.exists()
           else "reference/ + tools/shelf.py markers (no config found)")
    print(f"  root           : {root}")
    print(f"  root resolved via: {how}")
    print(f"  config file    : {cfg_path} -> {'present' if cfg else 'ABSENT (EN defaults)'}")
    if cfg:
        print(f"  top-level keys : {', '.join(sorted(cfg))}")
    q = corp.get("quote", {}) if isinstance(corp.get("quote"), dict) else {}
    print("  --- grammar (what cites/quotes the gates expect) ---")
    print(f"  key_pattern    : {corp.get('key_pattern', '(default rr-(\\d{3}))')}")
    print(f"  cite keyword   : {corp.get('cite_pattern', '(none — bare keys only)')}")
    print(f"  quote style    : {q.get('open', '\"')!r} … {q.get('close', '\"')!r}")
    print(f"  primary prefix : {_PRIMARY or '(none)'} | keyword cites allowed: {CITE_HAS_KEYWORD}")
    print("  (why these values: references/DESIGN.md § tree-locked model; the")
    print("   grammar-home table says which file owns each line above)")
    print("  --- playlists ---")
    print(f"  default        : {DEFAULT_PLAYLIST}")
    print(f"  registered     : {', '.join(playlist_keys())}  "
          f"(flat from config: {', '.join(sorted(FLAT_PLAYLISTS)) if FLAT_PLAYLISTS else 'none'})")
    _pre = {p: KEY_PREFIXES.get(p, p + "-") for p in playlist_keys()}
    _np = {p: d for p, d in _pre.items() if d != p + "-"}
    print(f"  key prefixes   : {', '.join(f'{p}={d or '(empty)'!r}' for p, d in _pre.items()) or '(none)'}")
    if _np:
        print("  (non-default key_prefix — T9.1/ADR 0007: session key = prefix + NNN)")
    if PLAYLIST_TRANSCRIPTS:
        print("  top-level clean dirs (ADR 0007 exception):")
        for _p, _td in PLAYLIST_TRANSCRIPTS.items():
            _cd = clean_dir(_p)
            print(f"    {_p:<10}: {_td}{'  [exists]' if _cd.exists() else '  [MISSING]'}")
    print("  --- data paths (tree-locked by design — C3.6) ---")
    for name, pth in (("ROOT", ROOT), ("REF", REF), ("TEMPLATES", TEMPLATES),
                      ("TRANSCRIPTS", TRANSCRIPTS), ("INVENTORY", INVENTORY)):
        print(f"  {name:<11}: {pth}{'  [exists]' if pth.exists() else '  [MISSING]'}")
    try:
        n = len(load_sessions())
        print(f"  sessions loaded: {n}")
        if n == 0:
            print("  (zero sessions — if a corpus was expected, check transcripts_dir "
                  "and the tree above; W4.4 will make `check` exit 2 on this)")
    except Exception as e:
        print(f"  sessions loaded: ERROR {e}")
    print("doctor is read-only; it changes nothing.")
