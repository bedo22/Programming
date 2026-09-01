#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""match — tokens(), subseq(), slice_verbatim() (gap_r/miss_r from config).
Moved from _legacy.py (first logical split, behavior preserved)."""

from __future__ import annotations

import re

from .arabic import ar_norm, FOLD_TABLE_MIN


# ---------------------------------------------------------------------------
# TWO normalisers live here ON PURPOSE, and they are not interchangeable.
# A third copy is how the Quran lane silently under-reported real matches for
# the whole life of the shelf: match.norm already stripped U+0670 (superscript
# alef) and verify.norm did not, and nothing noticed until a canonical stem
# graded "partial 4/5" against its own verse.
#
#   norm()        -> TRANSCRIPT matching (pins/check). Keeps hamza carriers
#                    distinct, keeps case, strips only a known punctuation set,
#                    and folds the "ال " prefix. ASR transcripts are messy but
#                    the marks are real signal there.
#   norm_uthmani()-> CANONICAL-TEXT containment (Quran API, book editions).
#                    Folds every hamza carrier to its base and drops all marks,
#                    because printed Uthmani orthography (ٱ , ء , ٰ) never
#                    matches how a stem or a transcript is written.
#
# If you discover a new normalisation rule, decide it for BOTH and say so here.
# ---------------------------------------------------------------------------
def norm(s: str) -> str:
    """Arabic canonicalisation for matching. Delegates to shelf_core.arabic -- one authority.

    Behaviour note: FOLD_TABLE_MIN (arabic.py) is the calibrated truth and it does NOT
    fold hamza carriers — ؤ stays ؤ and ئ stays ئ (norm('مؤمن') == 'مؤمن'), matching the
    header above. Widening the fold table moved verdicts on 23/41 corpus notes; that
    measurement is why the table stays minimal (see arabic.py's calibration comment).
    This docstring previously claimed carriers fold to their bases — a reverted intent
    left in prose (receipt V1.5). The ASCII comma is in the punctuation class alongside
    the Arabic one: that asymmetry is what let a generator and a matcher disagree in
    silence (Pitfall Y)."""
    return ar_norm(s, drop_hamza=False, fold_definite=True, folds=FOLD_TABLE_MIN)


def uth_variants(s):
    """Both defensible readings of the superscript alef, as a set.

    U+0670 marks a long /a:/, and the Uthmani text spells that sound two different ways: a plain
    one (مَجَٰلِس → مجالس) and the historic waw-spelling (صَلَوٰة → صلوة, standard صلاة). Folding
    to alef fixes the first and breaks the second; deleting it does the reverse. Neither single
    choice is right, so the grader tries both -- and because every variant is a lossy canonicaliser,
    adding variants can only ever turn a miss into a match, never the reverse.
    """
    fold = norm_uthmani(s)
    s2 = re.sub(r"[\u0610-\u061A\u064B-\u065F\u0670\u0640\u06D6-\u06ED]", "", s or "")
    # both readings: the folded form + the superscript-alef-DELETED form. The old
    # __wrapped__ arm was dead (the attribute never exists) (H2.4 receipt).
    return {fold, _uth_delete(s)}


def _uth_delete(s):
    """norm_uthmani with U+0670 deleted rather than folded -- the other reading."""
    s = re.sub(r"[\u0610-\u061A\u064B-\u065F\u0670\u0640\u06D6-\u06ED]", "", s or "")
    return _uth_tail(s)


def norm_uthmani(s):
    r"""Canonicalise Arabic for containment grading -- used to decide a QUOTE MATCHES.

    Two defects fixed here, both of which made the Quran lane UNDER-report real matches:
    - U+0670 (superscript alef, ``ٰ``) is outside \u064B-\u0652, so it survived the diacritic
      strip and was then turned into a SPACE by the [^\w\s] pass: ``ٱلْـٰـه`` became "ال ه",
      breaking containment on ordinary Uthmani text. Quran.com's text_uthmani is full of them.
    - standalone hamza (ء, U+0621) had no mapping, so ``أَرَءَيْتَ`` normalised to "ارءيت"
      while any sane stem writes "ارايت".
    Strip the whole harakat/tatweel/Quran-annotation range, then fold hamza carriers to their
    base letters. This is deliberately lossy: it can only ever turn a MISS into a MATCH, never
    the reverse, so a false negative here silently sends real citations back to للشيخ.
    """
    # U+0670 goes FIRST, and it folds to ا rather than being deleted with the other harakat.
    # The superscript alef is not a vowel mark in the way a fatha is: it carries a long /a:/ that
    # standard orthography writes as a real alef. Deleting it silently shortens words --
    # ٱلْمَجَٰلِسِ came out as المجلس, so the plural of مجالس could never match any ordinary
    # spelling of it, and 58:11 graded 5/6 against a query that quotes it verbatim. Folding it
    # keeps the lossy direction the docstring promises: miss -> match, never match -> miss.
    # The historic waw-spelling of /ā/ is waw + superscript alef (صَلَوٰة for standard صلاة), so
    # that PAIR is one alef -- folding the marker alone yields صلواه and still misses its own word.
    # Matching on the pair is precise: a real وا with no superscript alef (أواه) is untouched, which
    # a word-final rewrite would have corrupted. يٰ is the same phenomenon for ى (يَٰٓأَيُّهَا).
    s = (s or "").replace("\u0648\u0670", "ا").replace("\u064A\u0670", "ى")
    s = s.replace("\u0670", "ا")
    s = re.sub(r"[\u0610-\u061A\u064B-\u065F\u0670\u0640\u06D6-\u06ED]", "", s)
    return _uth_tail(s)


def _uth_tail(s):
    for a, b in (("أ","ا"),("إ","ا"),("آ","ا"),("ٱ","ا"),("ء","ا"),("ؤ","و"),("ئ","ي"),("ة","ه"),("ى","ي")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s)).strip().lower()


def normalize_for_match(s: str):
    DIAC = set("\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652\u0670\u0640")
    out, pos = [], []
    i, n = 0, len(s)
    while i < n:
        ch = s[i]
        if ch in DIAC:
            i += 1
            continue
        if ch in "أإآ":
            out.append("ا"); pos.append(i); i += 1; continue
        if ch == "ة":
            out.append("ه"); pos.append(i); i += 1; continue
        if ch == "ى":
            out.append("ي"); pos.append(i); i += 1; continue
        if ch == "ا" and i + 2 < n and s[i + 1] == "ل" and s[i + 2] == " " and (i == 0 or not s[i - 1].isalnum()):
            out.append("ا"); out.append("ل"); pos.append(i); pos.append(i + 1); i += 3; continue
        out.append(ch); pos.append(i); i += 1
    return "".join(out), pos


def tokens(s: str) -> list:
    # 1.2.19: casefold here, at the ONE token gate every comparison flows
    # through (pins/check/lift/coverage). Arabic is case-free so this is a
    # no-op on the AR shelves; on EN shelves the missing fold made the
    # matcher case-sensitive — cs-001 measured 34 cited spans, 0 verified,
    # because the note's title-case cannot meet ASR's lowercase (the exact
    # "Flags: 0 is a refusal" class).
    return re.findall(r"[\w]+", norm(s).casefold())


# P6.8: the ONE tolerance set — findmin/lift's "same tolerance as the shelf"
# docstring is now literally true (both import these names; the literals live
# here alone).
TOL = dict(gap_r=0.85, miss_r=0.30)          # phrase-in-bucket tolerance
TOL_HEAD = dict(gap_r=1.0, miss_r=0.0)       # exact-prefix (anchor head) tolerance


def _greedy_match(qt, w, gap_budget, miss_budget):
    j, gaps, missed = 0, 0, 0
    for t in qt:
        k = j
        while k < len(w) and w[k] != t and w[k] != "و" + t:
            k += 1
        if k < len(w):
            gaps += k - j
            j = k + 1
        else:
            missed += 1
        if gaps > gap_budget or missed > miss_budget:
            return False
    return True


def _first_tok_keys(qt0: str):
    # P6.11 receipt (اائت/ات hamza variants): MEASURED ON THIS CORPUS — the
    # matcher's recall tests (W1.x/V1.x scratch suites) only ever needed the
    # ائت↔ات pair; و-conjunction is handled above it. Whether OTHER hamza
    # spellings (أ→ا, إ→ا) need the same expansion is UNKNOWN (never measured);
    # adding keys here widens every index lookup, so it is left until a corpus
    # miss proves the need. Corpus-specific, not a general Arabic rule.
    keys = {qt0, "و" + qt0}
    for x in (qt0, "و" + qt0):
        if x.startswith("ائت"):
            keys.add("ات" + x[3:])
        elif x.startswith("ات"):
            keys.add("ائت" + x[2:])
    return keys


def _token_index(toks):
    idx = {}
    for k, (t, _) in enumerate(toks):
        idx.setdefault(t, []).append(k)
    return idx


def subseq(qt, ft, gap_r=0.8, miss_r=0.25, index=None):
    if not qt:
        return True
    gap_budget = max(2, int(gap_r * len(qt)))
    miss_budget = max(0, int(miss_r * len(qt)))
    win = len(qt) + gap_budget + 1
    grid_cap = False
    if index is not None:
        keys = _first_tok_keys(qt[0])
        starts = []
        for k in keys:
            starts.extend(index.get(k, []))
        starts.sort()
        # was: the 400-start cap subsampled these TRUE anchors, so a common
        # first token (>400 positions) false-negatived present quotes
        # (measured: 900-anchor probe, OLD false / NEW true, P6.11; fx and
        # investing pins sweeps byte-identical — zero live verdict moves).
        # The no-subsampling rule remains because the CLASS — sampling away
        # the only exact positions a presence check has — regenerates any
        # time a performance cap is added to an anchor list.
        # P6.11: index-derived starts are TRUE anchors — real positions of the
        # quote's first token. The old 400-cap subsampled them, so a common
        # first token (appearing >400 times) dropped true presence matches.
        # No subsampling here. The synthetic grid windows below may sample.
    else:
        qset = set(qt)
        qset_w = set("و" + t for t in qt)
        starts = [i for i, t in enumerate(ft) if t in qset or t in qset_w]
        if len(starts) > 400:
            # no-anchor scan: candidates are ANY quote token's positions —
            # sampling this scan is the point of the cap
            step = len(starts) // 400 + 1
            starts = starts[::step]
            grid_cap = True
    if grid_cap or len(ft) > 5000:
        stride = max(1, gap_budget)
        starts += list(range(0, len(ft) - win + 1, stride))
    for s in starts:
        if _greedy_match(qt, ft[s:s + win], gap_budget, miss_budget):
            return True
    return False
