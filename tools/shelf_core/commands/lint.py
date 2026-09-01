#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""commands/lint — intake check for notes (A5.4). A check, never a rewrite.

One categorized list per note over the parse layer's own NoteDoc:
  key     — session key unresolvable (registry-verified)
  status  — status row missing or not a whole configured value
  flags   — flags row missing or not 'no'/'yes…'
  ufffd   — U+FFFD inside the scanned region (exempt sections excluded)
  script  — script contamination (check_allowed_scripts, config-inferred mode)
  cite    — cite-LOOKING text the configured CITE grammar cannot parse (the
            NOTHING-WAS-VERIFIED class at intake: the row will never pair)
  comma   — INFO census: mixed Arabic/ASCII commas inside cite-like spans

Usage: shelf lint KEY|NOTE.md [...] [--corpus]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from shelf_core.config import find_root, load_config
from shelf_core.notes import parse_note, scanned_region, find_note, status_is_valid, flags_is_valid
from shelf_core.scriptcheck import check_allowed_scripts, key_pattern, quote_style
from shelf_core.citation import iter_cites


def _lint_one(path: Path, cfg) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    d = parse_note(path)
    name = path.name
    if d["key"] is None:
        findings.append(("key", "session key unresolvable — fill the Session row "
                                 "or rename to <pl>-NNN-<slug>.md"))
    if d["status"] is None:
        findings.append(("status", "status row missing"))
    elif not status_is_valid(d["status"]):
        findings.append(("status", f"invalid status {d['status']!r} (whole-value match)"))
    if d["flags"] is None:
        findings.append(("flags", "flags row missing"))
    elif not flags_is_valid(d["flags"]):
        findings.append(("flags", f"invalid flags {d['flags']!r}"))
    if "\ufffd" in scanned_region(d["raw"]):
        findings.append(("ufffd", "U+FFFD in the scanned region — fix the word "
                                  "from the source, not the matcher"))
    for lineno, ch, script in check_allowed_scripts(d["raw"]):
        findings.append(("script", f"L{lineno}: {script} character {ch!r}"))
    # cite-LOOKING spans the grammar cannot parse — the NOTHING-WAS-VERIFIED
    # class: the text reads like a citation but will never pair.
    kp = key_pattern(cfg)
    _time = r"[0-9\u0660-\u0669]{1,2}:[0-9\u0660-\u0669]{2}"
    cite_like = re.compile(rf"(?:{kp}|\S+\s*\d{{1,3}})\s*[،,]\s*{_time}")
    ar_time = re.compile(rf"\S+\s*\d{{0,3}}\s*[،,]?\s*[0-9\u0660-\u0669]*[\u0660-\u0669][0-9\u0660-\u0669]*:[0-9\u0660-\u0669]{{2}}")
    commas = set()
    for ln, line in enumerate(d["raw"].splitlines(), 1):
        for m in cite_like.finditer(line):
            span = m.group(0)
            sep = "،" if "،" in span else ","
            commas.add(sep)
            if next(iter_cites(span), None) is None:
                findings.append(("cite", f"L{ln}: {span!r} is not parseable by the "
                                         f"configured cite grammar — fix to "
                                         f"'<keyword> N، MM:SS' or '(KEY, MM:SS)'"))
        for m in ar_time.finditer(line):
            span = m.group(0)
            if next(iter_cites(span), None) is None:
                findings.append(("cite", f"L{ln}: {span!r} — Arabic-Indic digits in a "
                                         f"time; the grammar parses ASCII digits "
                                         f"(convert ٤:٣٠ -> 4:30)"))
    if len(commas) > 1:
        findings.append(("comma", f"INFO: mixed comma classes inside cite-like "
                                  f"spans: {' / '.join(sorted(commas))}"))
    return findings


def cmd_lint(argv):
    if not argv:
        sys.exit("usage: shelf lint KEY|NOTE.md [...] [--corpus]")
    root = find_root()
    cfg = load_config(root)
    targets: list[Path] = []
    if "--corpus" in argv:
        from shelf_core.playlists import playlist_keys, notes_dir
        for pl in playlist_keys():
            nd = notes_dir(pl)
            if nd and nd.is_dir():
                targets.extend(sorted(nd.glob("*.md")))
        argv = [a for a in argv if a != "--corpus"]
        if not targets:
            print("lint: no notes found under the registry", file=sys.stderr)
            return 2
    argv = [a for a in argv if a != "--corpus"]
    for a in argv:
        if "/" in a or a.endswith(".md"):
            p = Path(a)
            if not p.exists():
                sys.exit(f"lint: no note found for {a}")
            targets.append(p)
        else:
            np = find_note(a)
            if np is None:
                sys.exit(f"lint: no note found for {a}")
            targets.append(Path(np))
    total, tally = 0, {}
    for p in targets:
        findings = _lint_one(p, cfg)
        if findings:
            print(f"{p.name}:")
            for cat, msg in findings:
                print(f"  [{cat}] {msg}")
                tally[cat] = tally.get(cat, 0) + 1
            total += len(findings)
    cats = ", ".join(f"{k}={v}" for k, v in sorted(tally.items())) or "clean"
    print(f"\nlint: {len(targets)} note(s), {total} finding(s) ({cats})")
    sys.exit(1 if total else 0)
