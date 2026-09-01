# -*- coding: utf-8 -*-
"""shelf_core.scriptcheck — text-level script/pitfall classification.

A5.4 hoist: these lived only in scripts/_shelf_lib.py, so the tool-side lint
could not reuse them (and a reimplementation would have been a fork). The
gate scripts keep their import names via _shelf_lib re-exports.
"""
from __future__ import annotations

from .config import corpus_cfg, load_config, find_root


def key_pattern(config: dict | None = None) -> str:
    return (corpus_cfg(config) or {}).get("key_pattern", r"rr-(\d{3})")


def quote_style(config: dict | None = None) -> tuple[str, str]:
    q = (corpus_cfg(config) or {}).get("quote", {})
    if isinstance(q, dict):
        return q.get("open", '"'), q.get("close", '"')
    return '"', '"'


def _cfg(config):
    if config is not None:
        return config
    root = find_root()
    return load_config(root)


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


def _in_ranges(cp: int, ranges) -> bool:
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
