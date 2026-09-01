#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""citation — moved from helpers.py (final distribution)."""
from __future__ import annotations
import re, bisect, sys
from pathlib import Path
# H2.2: plain relative imports. The removed try/except-pass contained a
# SELF-import (`from .citation import fmt_mmss, parse_mmss`) — fmt_mmss is
# defined in THIS module (line 112); the self-import was dead weight whose
# failure was silently swallowed (H2.4/W4.16 receipt).
from .config import ROOT, REF, TEMPLATES, TRANSCRIPTS, INVENTORY
from .match import norm, tokens, subseq, _token_index
_MINUTE = r"(\d{1,2}:\d{2})(?:\s*[–—-]\s*(\d{1,2}:\d{2}))?(?!\d)"
# ---------------- config-driven citation grammar (reusable across shelves) ----------------
# corpus.key_pattern is loaded DIRECTLY as a regex; corpus.quote.open/close set the
# verbatim delimiter; corpus.cite_pattern (optional) adds a keyword cite form such as
# "المجلس N، HH:MM". No shelf name is hardcoded here — a new shelf only edits its
# config/project.yaml corpus block. Default (no corpus block) = Investing EN grammar.
from .config import corpus_cfg as _corpus_cfg
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


def _cite_playlist() -> str:
    """T9.1/ADR 0007: which playlist keyword cites (cite_pattern N) resolve to.
    corpus.cite_playlist if set; else key_pattern's literal prefix; else the
    unique empty-key_prefix playlist (prefixless shelf); else the default.
    Lazy playlists import — playlists imports citation's fmt_mmss/parse_mmss."""
    cp = (_corp.get("cite_playlist") or "").strip().lower()
    if cp:
        return cp
    if _PRIMARY:
        return _PRIMARY
    try:
        from .playlists import KEY_PREFIXES, DEFAULT_PLAYLIST
        empty = [p for p, pre in KEY_PREFIXES.items() if pre == ""]
        if len(empty) == 1:
            return empty[0]
        return DEFAULT_PLAYLIST
    except Exception:
        return ""


def _kw_prefix_ok(sess_key: str) -> bool:
    """True when the keyword form is safe for sess_key. Fixed cite playlist:
    the key must start with its key_prefix (exact digits for an empty prefix —
    it must not swallow slug keys like abtr-073). cite_playlist=self: the key
    must resolve to ANY registered playlist's prefix+NNN — own_pl threading
    then guarantees the keyword resolves inside the note's own playlist (the
    silent-cross-session bug class can't fire by construction)."""
    pl = _cite_playlist()
    if not pl:
        return False
    try:
        from .playlists import KEY_PREFIXES
        prefixes = sorted(KEY_PREFIXES.values(), key=len, reverse=True)
    except Exception:
        prefixes = []
    k = str(sess_key).strip().lower()
    if pl == "self":
        for pre in prefixes:
            if pre == "":
                if re.fullmatch(r"\d{1,3}", k):
                    return True
            elif k.startswith(pre):
                return True
        return False
    try:
        from .playlists import KEY_PREFIXES as _KP
        pre = _KP.get(pl, pl + "-")
    except Exception:
        pre = pl + "-"
    if pre == "":
        return bool(re.fullmatch(r"\d{1,3}", k))
    return k.startswith(pre)


def kw_cite_allowed(sess_key: str) -> bool:
    """True only when sess_key belongs to the playlist cite_pattern resolves to."""
    if not (CITE_KEYWORD and (_PRIMARY or _cite_playlist())):
        return False
    return _kw_prefix_ok(sess_key)


def key_of_number(n, own_pl=None) -> str:
    """Map a keyword-cite number to a session key. T9.1/ADR 0007 resolution
    order: corpus.cite_playlist=self -> the NOTE'S OWN playlist (own_pl) —
    the fork-era convention where المجلس N inside a <pl>-NNN note means that
    playlist's session N; else the configured/derived cite playlist's
    key_prefix + 3 digits (an empty prefix yields bare NNN); else the legacy
    key_pattern literal prefix + digit width (is-(\\d{3}) + 15 -> is-015)."""
    n = int(n)
    if not _PRIMARY:
        pl = _cite_playlist()
        if pl == "self" and own_pl:
            try:
                from .playlists import KEY_PREFIXES
                return KEY_PREFIXES.get(own_pl, own_pl + "-") + f"{n:03d}"
            except Exception:
                pass
        if pl and pl != "self":
            try:
                from .playlists import KEY_PREFIXES
                return KEY_PREFIXES.get(pl, pl + "-") + f"{n:03d}"
            except Exception:
                pass
    m = re.match(r"^([^(]*?)\(\s*\\d\{(\d+)\}\s*\)", KEY_PATTERN)
    if m:
        return f"{m.group(1)}{n:0{int(m.group(2))}d}"
    return KEY_PATTERN.split("(")[0] + str(n)


# CITE forms. A: (KEY, HH:MM)/(KEY HH:MM). B (optional keyword): <cite_pattern> N، HH:MM.
# The comma class has to accept BOTH commas. The keyword branch below always did; this branch
# only ever accepted the ASCII one, while draft_note's _cite_str emits the Arabic "،" -- so every
# cite the scaffold wrote into a note was unparseable, pins verified 0 quotes, and "Flags: 0" was
# the sound of a gate looking at nothing. Arabic text takes an Arabic comma; a matcher for Arabic
# notes that requires U+002C is matching a language it is not reading.
_CITE_PAREN = rf"\(\s*{_KEY_WHOLE}\s*(?:[،,]\s*|\s+){_MINUTE}\s*\)"
if CITE_KEYWORD:
    _CITE_KW = rf"{re.escape(CITE_KEYWORD)}\s*(\d{{1,3}})\s*[،,]\s*{_MINUTE}"
    CITE_RE = re.compile(rf"(?:{_CITE_PAREN}|{_CITE_KW})")
    CITE_HAS_KEYWORD = True
else:
    CITE_RE = re.compile(_CITE_PAREN)
    CITE_HAS_KEYWORD = False


QUOTE_MIN_TOKENS = 4   # >=4 tokens => real quote; fewer => label, skipped


def fmt_mmss(sec: int) -> str:
    return f"{sec // 60:02d}:{sec % 60:02d}"


def parse_mmss(s: str) -> int:
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def cite_match_parts(m, own_pl=None):
    """(key, secs) from a single CITE_RE match — encapsulates the group layout so
    no caller touches group indices. Returns (None, []) if the match is unusable.
    Group map: paren form g1=key/g2=start/g3=end; keyword form g4=num/g5/g6.
    T9.1: own_pl threads the NOTE'S playlist through for cite_playlist=self."""
    if m.group(1) is not None:
        key, gs, ge = m.group(1), 2, 3
        # F14: an EMPTY-key paren cite — «(5:17)» — is prose notation (a Quran
        # surah:ayah ref in the fork's detail cells), not a session cite. With
        # no key the old path self-bound it to the note's playlist and its
        # phantom minutes outranked the row's real cell (measured: abtr-118:205
        # «(5:17)» twice in the detail cell vs the row's own | 01:25 |).
        if key == "":
            return None, []
    elif CITE_HAS_KEYWORD and m.group(4) is not None:
        key, gs, ge = key_of_number(m.group(4), own_pl), 5, 6
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


# F6/F11c: a TEXT-source cite — canonical religious/quoted text verified
# against a text authority (hadith collection, Quran, the shelf's مصادر
# متحققة), NOT the spoken transcript. Whole-word parenthetical forms only; the
# session cite marks WHERE it was discussed, this marks WHAT the text is.
TEXT_CITE_RE = re.compile(
    r"\((?:رواه|أخرجه|خرّجه|روي|سورة|قرآن|مصادر متحققة|صحّه|صححه|صحوه|حديث|أثر|المرجع)[^)]{0,80}\)")


def iter_cites(line, own_pl=None):
    """Yield (key, secs, start, end) for each same-line cite in `line`.
    Encapsulates the CITE_RE group layout so no caller touches group indices.
    Group map: paren form g1=key/g2=start/g3=end; keyword form g4=num/g5/g6.
    T9.1: own_pl threads through for corpus.cite_playlist=self resolution."""
    for m in CITE_RE.finditer(line):
        key, secs = cite_match_parts(m, own_pl)
        if key is None:
            continue
        yield key, secs, m.start(), m.end()


def fmt_cite(key: str, secs) -> str:
    secs = sorted(set(secs))
    if len(secs) > 1:
        return f"({key}, {fmt_mmss(secs[0])}–{fmt_mmss(secs[-1])})"
    return f"({key}, {fmt_mmss(secs[0])})"



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
    # here would be circular. Resolved at call time instead. _minute_for_pos is
    # the one shared marker binary search (H2.5 — this file carried a twin).
    from .transcript import (_session_normalized, _tight_alignments,
                             clean_paragraphs, _minute_for_pos)
    c = _session_normalized(sess_key)
    if c is None or not qt:
        return None
    raw, _nrm, posmap, toks, cidx, markers = c
    mpos = [p for p, _ in markers]

    def minute_at(start):
        m = _minute_for_pos(mpos, markers, start)
        return m if m is not None else 0

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
