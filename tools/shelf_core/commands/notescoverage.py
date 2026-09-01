#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""notescoverage — B5 port of scripts/notes-coverage.py as a registry command
(`shelf notes-coverage`).

TRIAGE ledger: how completely each session note distills its transcript.
Corpus report, never gates.

Per note it reports: transcript buckets, ≥4-token quotes, cited quotes,
claim units (claim_source: | C# | rows or ### محاور headers — config
corpus.claim_source), quotes-per-claim density, and status (scaffold detected
via corpus.note_meta.scaffold_status).

Flags:
  SCAFFOLD  — status still equals scaffold_status (distillation never ran)
  THIN      — quotes/claim < thin_quotes_per_claim (gate.thin_quotes_per_claim,
              default 2.0) — partial distillation: the note exists, passes the
              verbatim gate, but covers only a fraction of its transcript
  ZERO      — no verbatim quotes at all

Differences from the script: the sys.path tools/ bootstrap is gone (in-package
imports); playlist defaults come from the same shelf_core APIs the script used.
"""
from __future__ import annotations

import sys
from pathlib import Path

from shelf_core.config import load_config, find_root
from shelf_core.notes import parse_note, claims_count
from shelf_core.transcript import clean_buckets
from shelf_core.playlists import notes_dir, playlist_keys


def cmd_notes_coverage(paths):
    argv = list(paths)
    root = find_root()
    cfg = load_config(root)
    gate = cfg.get("gate", {}) or {}
    corpus = cfg.get("corpus", {}) or {}
    claim_source = str(corpus.get("claim_source", "auto"))
    meta = corpus.get("note_meta", {}) or {}
    scaffold_status = str(meta.get("scaffold_status", "مسودة"))
    thin_thr = float(gate.get("thin_quotes_per_claim", 2.0))

    files: list[Path] = []
    if argv:
        files = [Path(a) for a in argv]
    else:
        for pl in playlist_keys():
            d = notes_dir(pl)
            if d and d.is_dir():
                files.extend(sorted(d.glob("is-*.md")) or sorted(d.glob("*.md")))
    if not files:
        print("no notes found")
        return 2

    def claims(d) -> int:
        # A5.3(a)+(d): the claims grammar has ONE home — notes.claims_count
        # (| C# | rows + diacritic-tolerant ### المحاور headers). draft_note's
        # confirmed header format is recorded there: '### المحور {idx}: {title}'.
        return claims_count(d["raw"], claim_source)

    rows, flagged = [], 0
    print(f"{'note':10} {'status':7} {'claims':>6} {'buckets':>7} {'quotes':>6} "
          f"{'cited':>6} {'q/claim':>7}  flag")
    for p in files:
        d = parse_note(p)
        k = f"{d['ident'][0]}-{d['ident'][1]}" if d["ident"][0] else ""
        quoted = [r for r in d["quotes"] if len(r["quote"].split()) >= 4]
        cited = [r for r in quoted if r["cited"]]
        status = d["status"] if d["status"] else "?"
        claims_n = claims(d)
        buckets = len(clean_buckets(k) or {}) if k else 0
        dens = (len(quoted) / claims_n) if claims_n else 0.0
        flag = ""
        if status == scaffold_status:
            flag = "SCAFFOLD"
        elif claims_n and dens < thin_thr:
            flag = "THIN"
        elif not quoted:
            flag = "ZERO"
        if flag:
            flagged += 1
        rows.append((p.name[:10], status, claims_n, buckets, len(quoted),
                     len(cited), dens, flag))
    for r in rows:
        print(f"{r[0]:10} {r[1]:7} {r[2]:6} {r[3]:7} {r[4]:6} {r[5]:6} "
              f"{r[6]:7.2f}  {r[7]}")
    print(f"\nnotes: {len(rows)}  flagged: {flagged} "
          f"(THIN < {thin_thr:.1f} quotes/claim; SCAFFOLD = status "
          f"'{scaffold_status}')")
    return 0
