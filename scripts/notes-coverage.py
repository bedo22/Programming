#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""notes-coverage — TRIAGE ledger: how completely each session note distills
its transcript. Corpus report, never gates.

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

Usage: python3 scripts/notes-coverage.py [note.md ...]   (default: all)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from shelf_core.config import load_config, find_root  # noqa: E402
from shelf_core.notes import scan_lines  # noqa: E402
from shelf_core.transcript import clean_buckets  # noqa: E402
from shelf_core.playlists import notes_dir, playlist_keys  # noqa: E402


def main(argv: list[str] | None = None):
    root = find_root()
    cfg = load_config(root)
    gate = cfg.get("gate", {}) or {}
    corpus = cfg.get("corpus", {}) or {}
    claim_source = str(corpus.get("claim_source", "auto"))
    meta = corpus.get("note_meta", {}) or {}
    scaffold_status = str(meta.get("scaffold_status", "مسودة"))
    status_label = str(meta.get("status", "حالة الملاحظة"))
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

    def claims(txt: str) -> int:
        n = 0
        for line in txt.splitlines():
            if claim_source in ("C#", "auto") and re.match(r"\|\s*C\d+\s*\|", line):
                n += 1
            elif claim_source in ("محاور", "auto") and re.match(r"###\s*المحور", line):
                n += 1
        return n

    rows, flagged = [], 0
    print(f"{'note':10} {'status':7} {'claims':>6} {'buckets':>7} {'quotes':>6} "
          f"{'cited':>6} {'q/claim':>7}  flag")
    for p in files:
        k = ""
        m = re.search(r"\w+-(\d{3})", p.name)
        if m:
            k = f"{p.name.split('-')[0]}-{m.group(1)}"
        txt = p.read_text(encoding="utf-8", errors="replace")
        recs = scan_lines(txt)
        quoted = [r for r in recs if len(r["quote"].split()) >= 4]
        cited = [r for r in quoted if r["cited"]]
        st_m = re.search(rf"^\|\s*{re.escape(status_label)}\s*\|([^|]*)\|", txt, re.M)
        status = st_m.group(1).strip() if st_m else "?"
        claims_n = claims(txt)
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


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
