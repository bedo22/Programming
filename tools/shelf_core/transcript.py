#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""transcript — moved from helpers.py (final distribution)."""
from __future__ import annotations
import re, bisect, sys
from pathlib import Path
try:
    from .config import ROOT, REF, TEMPLATES, TRANSCRIPTS, INVENTORY
    from .match import norm, tokens, subseq, _token_index, normalize_for_match, _first_tok_keys
    from .citation import fmt_mmss, parse_mmss  # may be circular, handle
    from .playlists import get_session  # playlists imports citation, not transcript -> no cycle
except ImportError:
    pass
class CleanSource:
    """Minute-bucketed source for one session's clean transcript.

    Buckets come from the [MM:SS]-marked paragraphs of
    transcripts/<playlist>/clean/<file>. Every source in this repo is timed;
    verification is by minute."""

    def __init__(self, sess_key: str):
        rec = get_session(sess_key)
        self.key = sess_key
        self.rec = rec
        self.file = (ROOT / rec["rel"]) if rec else None
        self.buckets = clean_buckets(sess_key) or {}
        self.timed = bool(self.buckets)
        self.all_tokens = [t for b in self.buckets.values() for t in b]
        self.index = _token_index([(t, i) for i, t in enumerate(self.all_tokens)])

    def present(self, qt):
        return subseq(qt, self.all_tokens, index=self.index)


_bucket_cache: dict = {}


def clean_buckets(sess_key: str):
    """{marker-minute: bucket tokens} for the session's clean file (cached)."""
    rec = get_session(sess_key)
    if rec is None:
        return None
    f = ROOT / rec["rel"]
    if f not in _bucket_cache:
        buckets = {}
        current = None
        for line in f.read_text(encoding="utf-8", errors="replace").split("\n"):
            hm = re.match(r"^\[(\d{1,2}):(\d{2})\]\s*$", line.strip())
            if hm:
                current = int(hm.group(1)) * 60 + int(hm.group(2))
                buckets.setdefault(current, [])
                continue
            if current is not None and line.strip():
                buckets[current].extend(tokens(line))
        _bucket_cache[f] = buckets
    return _bucket_cache[f]


_para_cache: dict = {}


def clean_paragraphs(sess_key: str):
    """{minute: raw paragraph text} between [MM:SS] markers (cached)."""
    rec = get_session(sess_key)
    if rec is None:
        return None
    f = ROOT / rec["rel"]
    if f not in _para_cache:
        paras = {}
        current = None
        buf = []
        for line in f.read_text(encoding="utf-8", errors="replace").split("\n"):
            hm = re.match(r"^\[(\d{1,2}):(\d{2})\]\s*$", line.strip())
            if hm:
                if current is not None and buf:
                    paras[current] = " ".join(buf)
                current = int(hm.group(1)) * 60 + int(hm.group(2))
                buf = []
                continue
            if current is not None and line.strip():
                buf.append(line.strip())
        if current is not None and buf:
            paras[current] = " ".join(buf)
        _para_cache[f] = paras
    return _para_cache[f]


_norm_cache: dict = {}


def _session_normalized(sess_key: str):
    """(raw, normalized, position map, [(token, pos)], token index,
    [(marker pos, minute)]) for the session's clean file — cached per session.
    Normalizing once per session instead of once per quote is what keeps
    whole-block checks fast; the position map is what guarantees every sliced
    span is a literal substring of the original file."""
    if sess_key in _norm_cache:
        return _norm_cache[sess_key]
    rec = get_session(sess_key)
    if rec is None:
        return None
    raw = (ROOT / rec["rel"]).read_text(encoding="utf-8", errors="replace")
    nrm, posmap = normalize_for_match(raw)
    toks = [(m.group(0), m.start()) for m in re.finditer(r"[\w]+", nrm)]
    markers = [(hm.start(), int(hm.group(1)) * 60 + int(hm.group(2)))
               for hm in re.finditer(r"^\[(\d{1,2}):(\d{2})\]\s*$", raw, re.M)]
    entry = (raw, nrm, posmap, toks, _token_index(toks), markers)
    _norm_cache[sess_key] = entry
    return entry


def _tok_eq(a: str, b: str) -> bool:
    if a == b:
        return True
    for x, y in ((a, b), (b, a)):
        if x.startswith("ائت") and y.startswith("ات") and x[3:] == y[2:]:
            return True
    return False


def _next_match_pos(index, t, j):
    best = None
    for k in _first_tok_keys(t):
        lst = index.get(k)
        if not lst:
            continue
        i = bisect.bisect_left(lst, j)
        if i < len(lst):
            v = lst[i]
            if best is None or v < best:
                best = v
    return best


def _scan_next(toks, t, j):
    """No-index path: linear scan from j for the next token matching t."""
    k = j
    while k < len(toks) and not _tok_eq(toks[k][0], t) and toks[k][0] != "و" + t:
        k += 1
    return k if k < len(toks) else None


def _verbatim_matches_toks(toks, posmap, qt, index=None):
    """All (start, end) raw-text spans where qt occurs contiguously (every hit).
    Positions are indices into the original raw text via the position map."""
    if index is not None:
        starts = []
        for k in _first_tok_keys(qt[0]):
            starts.extend(index.get(k, []))
        starts.sort()
    else:
        starts = [k for k, (t, _) in enumerate(toks)
                  if _tok_eq(t, qt[0]) or t == "و" + qt[0]]
    out = []
    for st in starts:
        j, matched = st + 1, [st]
        ok = True
        for t in qt[1:]:
            k = (_next_match_pos(index, t, j) if index is not None
                 else _scan_next(toks, t, j))
            if k is None:
                ok = False
                break
            matched.append(k)
            j = k + 1
        if not ok:
            continue
        ft, lt = toks[matched[0]], toks[matched[-1]]
        s, e = posmap[ft[1]], posmap[lt[1] + len(lt[0]) - 1]
        if s is None or e is None:
            continue
        out.append((s, e))
    return out


def _verbatim_matches(raw: str, qt):
    nrm, posmap = normalize_for_match(raw)
    toks = [(m.group(0), m.start()) for m in re.finditer(r"[\w]+", nrm)]
    return _verbatim_matches_toks(toks, posmap, qt)


def _verbatim_span_and_pos(raw: str, qt):
    ms = _verbatim_matches(raw, qt)
    if not ms:
        return None, None
    s, e = ms[-1]
    return re.sub(r"\s+", " ", raw[s:e + 1]).strip(), s


def _slice_verbatim(raw: str, qt):
    """Smallest literal span of raw covering qt's words in order — always a
    substring of the original text, or None."""
    span, _ = _verbatim_span_and_pos(raw, qt)
    return span


def _tight_alignments(sess_key, qt):
    """[(first_tok_idx, last_tok_idx)] for every completed left-to-right
    alignment of qt over the session's normalized token stream, keeping ONLY
    the tightest width(s). The engine's matcher permits gapped alignments
    (deliberate: interleaved noise like [Music] or interjections); without
    width selection, phrases of common words also 'complete' from spurious
    early anchors and poison minute attribution. The tightest alignment is the
    intended reading — anything wider merely proves the words exist somewhere."""
    c = _session_normalized(sess_key)
    if c is None or not qt:
        return [], None
    _raw, _nrm, posmap, toks, cidx, markers = c
    by_width = {}
    starts = sorted({k for key in _first_tok_keys(qt[0]) for k in cidx.get(key, [])})
    for st in starts:
        j, last, ok = st + 1, st, True
        for t in qt[1:]:
            k = _next_match_pos(cidx, t, j)
            if k is None:
                ok = False
                break
            last = k
            j = k + 1
        if ok:
            by_width.setdefault(last - st, []).append((st, last))
    if not by_width:
        return [], c
    return by_width[min(by_width)], c


def found_minutes(sess_key: str, qt):
    """Minutes whose bucket holds the quote's tightest verbatim occurrence.
    Fallback chain mirrors source_hint's "source span" levels (full quote ->
    longest prefix -> any >=4-token window) so the fixer trusts exactly what
    the checker's hint can locate — one finder, no drift. The final
    "transcript paragraph" level of source_hint is deliberately NOT mirrored:
    context text is not a verbatim occurrence, so it must never drive a
    minute rewrite."""
    for sub in (qt, *(qt[:s] for s in range(len(qt) - 1, 2, -1))):
        mins = _found_minutes_once(sess_key, sub)
        if mins:
            return mins
    for width in range(len(qt) - 1, 3, -1):
        for i in range(0, len(qt) - width + 1):
            mins = _found_minutes_once(sess_key, qt[i:i + width])
            if mins:
                return mins
    return []


def _found_minutes_once(sess_key: str, qt):
    pairs, c = _tight_alignments(sess_key, qt)
    if not pairs:
        return []
    _raw, _nrm, posmap, toks, _cidx, markers = c
    mpos = [p for p, _ in markers]
    mins = set()
    for st, lt in pairs:
        s = posmap[toks[st][1]]
        lo, hi, best = 0, len(mpos) - 1, None
        while lo <= hi:
            mid = (lo + hi) // 2
            if mpos[mid] <= s:
                best = mid
                lo = mid + 1
            else:
                hi = mid - 1
        if best is not None:
            mins.add(markers[best][1])
    return sorted(mins)


def check_quote(src, quote, secs, where, sess_key):
    """Verify one quote against its session's clean transcript.
    Returns (verdict, message): OK | MISSING | MISMATCH | None (label/short).
    A ±1-minute tolerance around bucket boundaries is preserved deliberately."""
    qt = tokens(quote)
    if len(qt) < 3:
        return None, None
    if not src.present(qt):
        return "MISSING", "quote not found anywhere in the source transcript"
    if not secs:
        return None, None
    fm = found_minutes(sess_key, qt)
    if not fm:
        return "MISMATCH", (
            "quote does not occur contiguously in the clean transcript — "
            "copy the wording exactly from transcripts/ and locate it with "
            "tools/findmin.py")
    for m in secs:
        if any(abs(m - x) <= 1 for x in fm):
            return "OK", None
    closest = min(fm, key=lambda x: min(abs(x - m) for m in secs))
    cited = secs[0]
    return "MISMATCH", (
        f"quote actually occurs at {fmt_mmss(closest)}, not at {fmt_mmss(cited)} — "
        f"run `python3 tools/shelf.py pins --fix {sess_key}` or correct the minute "
        f"(the same wording sits in the transcript at {fmt_mmss(closest)})")


