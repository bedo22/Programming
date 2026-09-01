#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""transcript — moved from helpers.py (final distribution)."""
from __future__ import annotations
import re, bisect, sys
from pathlib import Path
# H2.2: plain relative imports — the try/except-pass here predated the split
# and silently swallowed REAL import errors (the silent-failure family). The
# dependency graph is acyclic: citation -> (config, match) only.
from .config import ROOT, REF, TEMPLATES, TRANSCRIPTS, INVENTORY, corpus_cfg
from .match import norm, tokens, subseq, _token_index, normalize_for_match, _first_tok_keys
from .citation import fmt_mmss, parse_mmss   # citation defines both (line 112/116); no cycle
from .playlists import get_session           # playlists imports citation, not transcript -> no cycle
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


class RawSource:
    """Untimed raw-ASR source for one session (F4b, two-source design).

    Fork-era sessions were drafted against the raw ASR original
    (transcripts/<playlist>/raw/ — the old root Transcription/ dir, now
    tree-locked). Raw wording differs from the clean lane's (two ASR passes
    spell dialect differently), so raw-cited quotes verify against RAW:
    contiguity only — no minute buckets exist. Lane routing lives in the
    check path, decided by the note's الملف المصدر row."""

    def __init__(self, sess_key: str):
        rec = get_session(sess_key)
        self.key = sess_key
        self.rec = rec
        self.file = None
        self.all_tokens = []
        self.index = _token_index([])
        if rec:
            pl = rec.get("pl")
            rd = (corpus_cfg() or {}).get("playlists", {}).get(pl, {}).get("raw_dir")
            if rd:
                n = rec.get("num")
                if n is not None:
                    d = TRANSCRIPTS / pl / rd
                    cand = list(d.glob(f"{n:03d}*.txt")) or \
                        list(d.glob(f"*-{n:03d}-*.txt")) or \
                        list(d.glob(f"*-{n:03d}-*.txt".replace(f"-{n:03d}-", f"-{n:03d}")))
                    # de-dup, keep order
                    seen = set(); cand = [x for x in cand if not (x in seen or seen.add(x))]
                if len(cand) == 1:
                    self.file = cand[0]
                    nrm, posmap = normalize_for_match(
                        self.file.read_text(encoding="utf-8", errors="replace"))
                    self.all_tokens = nrm.split()
                    self.index = _token_index([(t, i) for i, t in enumerate(self.all_tokens)])

    def present(self, qt):
        return subseq(qt, self.all_tokens, index=self.index)


def clean_buckets(sess_key: str):
    """{marker-minute: bucket tokens} for the session's clean file (cached).

    P6.11 cache-assumption receipt: the cache is keyed by file PATH and never
    invalidated — it assumes clean transcripts are IMMUTABLE within a process
    (the shelf's own doctrine: transcripts are write-once raw evidence; only
    notes/docs mutate, and those have no token caches). A tool that edited a
    clean transcript mid-process would read stale buckets — that tool would be
    violating the doctrine, not the cache."""
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
    # Receipt (D8.11, was silent): the ائت↔ات fold is MEASURED ON THIS CORPUS
    # (the W1.x/V1.x recall suites never needed any other pair). It is a
    # corpus-specific equivalence, not a general Arabic rule; other hamza
    # spellings (أ→ا, إ→ا) are UNMEASURED and deliberately absent — widening
    # an equivalence widens every index hit, so it waits for a corpus miss
    # to prove the need. The same pair lives in match._first_tok_keys for the
    # anchor path; the two must stay in sync (same measurement, same receipt).
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
    # Receipt (V1.3): this was `ms[-1]` — the LAST match, while _slice_verbatim's
    # docstring promises "Smallest literal span"; a loose later occurrence won and
    # consumers (lift.py, selftest.py) got 249-char spans where 18-char ones existed.
    # Narrowest width is the intended reading — same doctrine as _tight_alignments below.
    s, e = min(ms, key=lambda se: se[1] - se[0])
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
    # F11b: bounded quote-token drops — the engine tolerates interleaved
    # TRANSCRIPT noise, but one variant-spelled QUOTE word (ASR/dialect) broke
    # the whole chain (measured: 55 contiguity flags where every token exists
    # somewhere yet no run completes). Drop budget scales with quote length:
    # 2 for ≥8 tokens, 1 for ≥5, else strict. A ≥8-token quote still verifies
    # ≥75% verbatim contiguity — no fabricated-quote escape hatch.
    drops_allowed = 2 if len(qt) >= 8 else (1 if len(qt) >= 5 else 0)
    starts = sorted({k for key in _first_tok_keys(qt[0]) for k in cidx.get(key, [])})
    for st in starts:
        j, last, ok, dropped = st + 1, st, True, 0
        for t in qt[1:]:
            k = _next_match_pos(cidx, t, j)
            if k is None:
                if dropped < drops_allowed:
                    dropped += 1
                    continue
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


def _minute_for_pos(mpos, markers, s):
    """Second value of the last [MM:SS] marker at or before char position s,
    or None when no marker precedes. H2.5: ONE binary search, two callers —
    transcript._found_minutes_once and citation.source_hint carried byte-twin
    closed-over copies that could silently drift."""
    lo, hi, best = 0, len(mpos) - 1, None
    while lo <= hi:
        mid = (lo + hi) // 2
        if mpos[mid] <= s:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return markers[best][1] if best is not None else None


def _found_minutes_once(sess_key: str, qt):
    pairs, c = _tight_alignments(sess_key, qt)
    if not pairs:
        return []
    _raw, _nrm, posmap, toks, _cidx, markers = c
    mpos = [p for p, _ in markers]
    mins = set()
    for st, lt in pairs:
        s = posmap[toks[st][1]]
        m = _minute_for_pos(mpos, markers, s)
        if m is not None:
            mins.add(m)
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
            "tools/shelf.py lift KEY")
    # F11a: ±2-minute tolerance (120s). The docstring claimed ±1 minute but the
    # code compared SECONDS with tolerance 1 — 2-second drifts across a minute
    # boundary flagged as wrong-minute. Measured (fqhn v9): 384/474 wrong-minute
    # flags were sub-minute drift, 72 more within 2 min; the fork wrote minutes
    # by hand. Drift beyond 120s still flags (real mislabels: 18 measured).
    for m in secs:
        if any(abs(m - x) <= 120 for x in fm):
            return "OK", None
    closest = min(fm, key=lambda x: min(abs(x - m) for m in secs))
    cited = secs[0]
    return "MISMATCH", (
        f"quote actually occurs at {fmt_mmss(closest)}, not at {fmt_mmss(cited)} — "
        f"run `python3 tools/shelf.py pins --fix {sess_key}` or correct the minute "
        f"(the same wording sits in the transcript at {fmt_mmss(closest)})")


