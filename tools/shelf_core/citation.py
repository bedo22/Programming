#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""citation — moved from helpers.py (final distribution)."""
from __future__ import annotations
import re, bisect, sys
from pathlib import Path
try:
    from .config import ROOT, REF, TEMPLATES, TRANSCRIPTS, INVENTORY
    from .match import norm, tokens, subseq, _token_index
    from .citation import fmt_mmss, parse_mmss  # may be circular, handle
except ImportError:
    pass
_MINUTE = r"(\d{1,2}:\d{2})(?:\s*[–—-]\s*(\d{1,2}:\d{2}))?(?!\d)"
# ---------------- config-driven citation grammar (reusable across shelves) ----------------
# corpus.key_pattern is loaded DIRECTLY as a regex; corpus.quote.open/close set the
# verbatim delimiter; corpus.cite_pattern (optional) adds a keyword cite form such as
# "المجلس N، HH:MM". No shelf name is hardcoded here — a new shelf only edits its
# config/project.yaml corpus block. Default (no corpus block) = Investing EN grammar.
try:
    from .config import corpus_cfg as _corpus_cfg
except ImportError:
    from config import corpus_cfg as _corpus_cfg  # type: ignore
_corp = _corpus_cfg() or {}
KEY_PATTERN = (_corp.get("key_pattern") or "").strip() or r"(?:cs|ex|rr)-[a-z0-9]+(?:-[a-z0-9]+)*"
_qstyle = _corp.get("quote") or {}
CITE_KEYWORD = (_corp.get("cite_pattern") or "").strip()


def _key_nc(kp: str) -> str:
    """key_pattern -> non-capturing whole-key matcher (inner groups neutralized)."""
    return re.sub(r"\((?!\?)", "(?:", kp)


def _key_whole(kp: str) -> str:
    """key_pattern -> ONE capture group holding the whole key (e.g. 'is-015')."""
    return "(" + _key_nc(kp) + ")"


_KEY_NC = _key_nc(KEY_PATTERN)
_KEY_WHOLE = _key_whole(KEY_PATTERN)

# Extra playlists in the same shelf widen the MATCHERS but never KEY_PATTERN itself:
# key_of_number() parses KEY_PATTERN's literal prefix to turn "المجلس 15" into is-015, so an
# alternation there would produce "(?:is|ts)-015". Slugs come from config, NOT from
# PLAYLIST_DIRS -- that map still carries the other shelves' defaults (cs/ex/rr), and matching
# those here would let a bogus cite pass the gate.
_EXTRA_PL = [e for e in (_corp.get("extra_playlists") or []) if isinstance(e, dict) and e.get("slug")]
_EXTRA_KEYS = [rf"{str(e['slug']).lower()}-\d{{{int(e.get('width', 3))}}}" for e in _EXTRA_PL]
if _EXTRA_KEYS:
    _KEY_NC = r"(?:" + "|".join([_KEY_NC] + _EXTRA_KEYS) + r")"
    _KEY_WHOLE = "(" + _KEY_NC + ")"
    KEY_ALTS = tuple(rf"{str(e['slug']).lower()}-" for e in _EXTRA_PL)
else:
    KEY_ALTS = ()

# QUOTE_RE: exactly ONE capture group (the quoted text), delimiter from corpus.quote.
if isinstance(_qstyle, dict) and _qstyle.get("open") and _qstyle.get("close"):
    QUOTE_RE = re.compile(re.escape(_qstyle["open"]) + r"([^" + re.escape(_qstyle["close"]) + r"]+)" + re.escape(_qstyle["close"]))
else:
    QUOTE_RE = re.compile(r'"([^"]+)"')


# The keyword cite form belongs to ONE playlist: corpus.cite_pattern (e.g. المجلس) plus a bare
# number is resolved by key_of_number(), which prefixes key_pattern's literal -- so writing
# "المجلس 1" inside a ts- note silently re-points the cite at is-001. lift.py used to do exactly
# that to every cite it rewrote, and pins --fix reuses that fixer, so it corrupted correct notes
# rather than fixing them. Multi-playlist shelves must keep the explicit (ts-001، MM:SS) form.
PRIMARY_PREFIX = (re.match(r"^\s*([A-Za-z][A-Za-z0-9]*)-\(", KEY_PATTERN) or
                  re.match(r"^\(\?:([A-Za-z][A-Za-z0-9]*)-", KEY_PATTERN))
_PRIMARY = PRIMARY_PREFIX.group(1).lower() if PRIMARY_PREFIX else ""


def kw_cite_allowed(sess_key: str) -> bool:
    """True only when sess_key's own prefix is the one cite_pattern resolves to."""
    if not (CITE_KEYWORD and _PRIMARY):
        return False
    return str(sess_key).split("-")[0].strip().lower() == _PRIMARY


def key_of_number(n) -> str:
    """Map a keyword-cite number to a session key via key_pattern's literal prefix
    + digit width (is-(\\d{3}) + 15 -> is-015). Generic — derives from key_pattern."""
    n = int(n)
    m = re.match(r"^([^(]*?)\(\s*\\d\{(\d+)\}\s*\)", KEY_PATTERN)
    if m:
        return f"{m.group(1)}{n:0{int(m.group(2))}d}"
    return KEY_PATTERN.split("(")[0] + str(n)


# CITE forms. A: (KEY, HH:MM)/(KEY HH:MM). B (optional keyword): <cite_pattern> N، HH:MM.
_CITE_PAREN = rf"\(\s*{_KEY_WHOLE}\s*(?:,\s*|\s+){_MINUTE}\s*\)"
if CITE_KEYWORD:
    _CITE_KW = rf"{re.escape(CITE_KEYWORD)}\s*(\d{{1,3}})\s*[،,]\s*{_MINUTE}"
    CITE_RE = re.compile(rf"(?:{_CITE_PAREN}|{_CITE_KW})")
    CITE_HAS_KEYWORD = True
else:
    CITE_RE = re.compile(_CITE_PAREN)
    CITE_HAS_KEYWORD = False

MIN_RE = re.compile(rf"\b{_KEY_NC}(?:\s*,\s*|\s+){_MINUTE}")
# Back-compat alias (older code referenced _KEY).
_KEY = _KEY_NC

QUOTE_MIN_TOKENS = 4   # >=4 tokens => real quote; fewer => label, skipped


def fmt_mmss(sec: int) -> str:
    return f"{sec // 60:02d}:{sec % 60:02d}"


def parse_mmss(s: str) -> int:
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def cite_match_parts(m):
    """(key, secs) from a single CITE_RE match — encapsulates the group layout so
    no caller touches group indices. Returns (None, []) if the match is unusable.
    Group map: paren form g1=key/g2=start/g3=end; keyword form g4=num/g5/g6."""
    if m.group(1) is not None:
        key, gs, ge = m.group(1), 2, 3
    elif CITE_HAS_KEYWORD and m.group(4) is not None:
        key, gs, ge = key_of_number(m.group(4)), 5, 6
    else:
        return None, []
    try:
        secs = [parse_mmss(m.group(gs))]
    except Exception:
        return None, []
    try:
        if m.group(ge):
            secs.append(parse_mmss(m.group(ge)))
    except (IndexError, TypeError):
        pass
    return key, secs


def iter_cites(line):
    """Yield (key, secs, start, end) for each same-line cite in `line`.
    Encapsulates the CITE_RE group layout so no caller touches group indices.
    Group map: paren form g1=key/g2=start/g3=end; keyword form g4=num/g5/g6."""
    for m in CITE_RE.finditer(line):
        key, secs = cite_match_parts(m)
        if key is None:
            continue
        yield key, secs, m.start(), m.end()


def fmt_cite(key: str, secs) -> str:
    secs = sorted(set(secs))
    if len(secs) > 1:
        return f"({key}, {fmt_mmss(secs[0])}–{fmt_mmss(secs[-1])})"
    return f"({key}, {fmt_mmss(secs[0])})"


def refs_from(text: str):
    """Free-text minute references via MIN_RE: [("min", seconds), ...].
    Dormant helper (line-era citations do not exist in this repo); kept because
    free-text minute scanning may be useful to tooling callers."""
    out = []
    for m in MIN_RE.finditer(text):
        out.append(("min", parse_mmss(m.group(1))))
        if m.group(2):
            out.append(("min", parse_mmss(m.group(2))))
    return out

# ---------------- session registry ----------------



# Moved from transcript.py (to hit <300)
def source_hint(sess_key: str, qt, near=None):
    """Copy-paste hint for a failed check. Tries, in order:
    1. the full quote verbatim (+ its true minute),
    2. the longest matching prefix,
    3. any >=4-token contiguous window of the quote,
    4. the transcript paragraph at the claimed minute (`near` seconds).
    Returns (label, span_text, minute) or None. label is "source span" when a
    piece of the quote genuinely occurs, "transcript" for minute context."""
    # Lazy import: transcript imports playlists->citation, so a top-level import
    # here would be circular. Resolved at call time instead.
    try:
        from .transcript import _session_normalized, _tight_alignments, clean_paragraphs
    except ImportError:
        from transcript import _session_normalized, _tight_alignments, clean_paragraphs  # type: ignore
    c = _session_normalized(sess_key)
    if c is None or not qt:
        return None
    raw, _nrm, posmap, toks, cidx, markers = c
    mpos = [p for p, _ in markers]

    def minute_at(start):
        lo, hi, best = 0, len(mpos) - 1, None
        while lo <= hi:
            mid = (lo + hi) // 2
            if mpos[mid] <= start:
                best = mid
                lo = mid + 1
            else:
                hi = mid - 1
        return markers[best][1] if best is not None else 0

    def span_of(sub):
        pairs, _c = _tight_alignments(sess_key, sub)
        if not pairs:
            return None
        st, lt = pairs[0]
        s = posmap[toks[st][1]]
        e = posmap[toks[lt][1] + len(toks[lt][0]) - 1]
        if s is None or e is None:
            return None
        return re.sub(r"\s+", " ", raw[s:e + 1]).strip(), minute_at(s)

    got = span_of(qt)
    if got:
        return ("source span", got[0], got[1])
    for size in range(len(qt) - 1, 2, -1):
        got = span_of(qt[:size])
        if got:
            return ("source span", got[0], got[1])
    for width in range(len(qt) - 1, 3, -1):
        for i in range(0, len(qt) - width + 1):
            got = span_of(qt[i:i + width])
            if got:
                return ("source span", got[0], got[1])
    if near is not None:
        paras = clean_paragraphs(sess_key) or {}
        if near in paras:
            txt = re.sub(r"\s+", " ", paras[near]).strip()
            shown = txt if len(txt) <= 160 else txt[:157] + "…"
            return ("transcript", shown, near)
    return None

# ---------------- quote scanning (one extractor for notes AND docs) ----------------

# Sections exempt from quote scanning: papers are informational (never gate-
# enforced); fidelity tables/log quote suspected ASR errors by design.
