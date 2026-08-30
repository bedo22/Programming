#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""match — tokens(), subseq(), slice_verbatim() (gap_r/miss_r from config).
Moved from _legacy.py (first logical split, behavior preserved)."""

from __future__ import annotations

import re


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
    s = re.sub(r"[\u064B-\u0652\u0670\u0640]", "", s)
    s = s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    s = s.replace("ة", "ه").replace("ى", "ي")
    s = re.sub(r"(?<![\w])ال\s+", "ال", s)
    s = re.sub(r"[«»\"“”„؛،:()…–\-—؟!\[\]]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


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
    s = re.sub(r"[\u0610-\u061A\u064B-\u065F\u0670\u0640\u06D6-\u06ED]", "", s or "")
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
    return re.findall(r"[\w]+", norm(s))


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
    if index is not None:
        keys = _first_tok_keys(qt[0])
        starts = []
        for k in keys:
            starts.extend(index.get(k, []))
        starts.sort()
    else:
        qset = set(qt)
        qset_w = set("و" + t for t in qt)
        starts = [i for i, t in enumerate(ft) if t in qset or t in qset_w]
    if len(starts) > 400:
        step = len(starts) // 400 + 1
        starts = starts[::step]
    if len(starts) > 400 or len(ft) > 5000:
        stride = max(1, gap_budget)
        starts += list(range(0, len(ft) - win + 1, stride))
    for s in starts:
        if _greedy_match(qt, ft[s:s + win], gap_budget, miss_budget):
            return True
    return False
