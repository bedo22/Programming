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

def find_root(start: Path | None = None) -> Path:
    """Find project root: nearest ancestor with config/project.yaml or reference/ + tools/shelf.py."""
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


def corpus_cfg(config: dict | None = None) -> dict:
    cfg = config if config is not None else load_config()
    return cfg.get("corpus", {}) if isinstance(cfg, dict) else {}


def gates_cfg(config: dict | None = None) -> dict:
    cfg = config if config is not None else load_config()
    return cfg.get("gates", {}) if isinstance(cfg, dict) else {}

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
    """Claim mass for a session key: | C# | rows / محاور / auto."""
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
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    if source == "auto":
        c = sum(1 for line in lines if re.match(r"\|\s*C\d+\s*\|", line))
        m = sum(1 for line in lines if "محور" in line)
        source = "C#" if c >= m else "محاور"
    if source == "محاور":
        return sum(1 for line in lines if "محور" in line)
    return sum(1 for line in lines if re.match(r"\|\s*C\d+\s*\|", line))


def bucket_count(key: str, root: Path | None = None, config: dict | None = None) -> int:
    nd = notes_dir(root, config)
    hits = glob.glob(str(nd / f"{key}-*.md"))
    if len(hits) != 1:
        return 0
    txt = Path(hits[0]).read_text(encoding="utf-8", errors="replace")
    return len(set(re.findall(r"\[(\d{1,2}:\d{2})\]", txt)))

# ---------- script contamination ----------

# Unicode ranges (small, no external deps)
_HAN_RANGES = [
    (0x4E00, 0x9FFF),   # CJK Unified
    (0x3400, 0x4DBF),   # Extension A
    (0x3040, 0x309F),   # Hiragana
    (0x30A0, 0x30FF),   # Katakana
    (0xAC00, 0xD7AF),   # Hangul Syllables
    (0x1100, 0x11FF),   # Hangul Jamo
]
_ARAB_RANGES = [
    (0x0600, 0x06FF),
    (0x0750, 0x077F),
    (0x08A0, 0x08FF),
    (0xFB50, 0xFDFF),
    (0xFE70, 0xFEFF),
]


def _in_ranges(cp: int, ranges: list[tuple[int, int]]) -> bool:
    return any(lo <= cp <= hi for lo, hi in ranges)


def check_allowed_scripts(text: str, mode: str = "auto", config: dict | None = None) -> list[tuple[int, str, str]]:
    """Return violations: (line_no, char, script). Han/Hang always FAIL.

    mode:
      auto  — infer from config quote style (AR «» → allow Arab+Common+Latn, EN " → Latn+Common)
      ar    — Arab + Common + Latn
      en    — Latn + Common
    """
    if mode == "auto":
        qo, _ = quote_style(config)
        mode = "ar" if qo == "«" else "en"
        # also infer from key_pattern
        kp = key_pattern(config)
        if "is-" in kp or "المجلس" in kp:
            mode = "ar"

    violations: list[tuple[int, str, str]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for ch in line:
            cp = ord(ch)
            if _in_ranges(cp, _HAN_RANGES):
                # Han/Hang always forbidden
                violations.append((lineno, ch, "Han/Hang"))
            elif mode == "en" and _in_ranges(cp, _ARAB_RANGES):
                violations.append((lineno, ch, "Arab in EN"))
            # Common (punct, digits, whitespace) always allowed — not flagged
    return violations


def check_pitfall_guards(text: str, config: dict | None = None) -> list[str]:
    """Pitfall guards (PITFALLS.md I + J): U+FFFD and header «»/"". Return GATE FAIL strings."""
    fails: list[str] = []
    qo, qc = quote_style(config)
    # I — U+FFFD replacement (silent token-breaker)
    if "\ufffd" in text:
        for lineno, line in enumerate(text.splitlines(), 1):
            if "\ufffd" in line:
                fails.append(f"U+FFFD at L{lineno}: {line.strip()[:60]} (fix the note, not the matcher — PITFALLS.md I)")
                break  # one is enough to fail the gate
        if len([l for l in text.splitlines() if "\ufffd" in l]) > 1:
            cnt = sum(1 for l in text.splitlines() if "\ufffd" in l)
            fails[0] += f" ({cnt} lines total)"
    # J — header contains verbatim quote delimiter (inherits sticky refs)
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("###") and (qo in line or qc in line):
            # Allow inline code backticks? No — headers are labels, never quotes
            fails.append(f"HEADER QUOTE at L{lineno}: {line.strip()[:80]} — headers must not contain {qo}{qc} (PITFALLS.md J, sticky refs)")
    return fails
