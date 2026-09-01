# -*- coding: utf-8 -*-
"""arabic — the single authority for "is this the same Arabic text?"

Why this module exists
----------------------
Four separate normalisers had grown up in shelf_core, each folding a slightly different set of
things, and every one of them was used to decide whether a quote was verbatim:

  match.norm()        folds alef variants, ة→ه, ى→ي; strips «» ؛ ، : ( ) … – — ؟ ! [ ] and the
                      separated definite article -- but NOT the ASCII comma, and NOT ؤ/ئ.
  match.norm_uthmani()  a fifth, for Quran containment grading.
  notes._norm_label()  also folds ؤ→و and ئ→ي.
  verify._norm_txt()   also drops the standalone hamza ء.

That is the root cause of the class of bug that silently un-verified an entire batch of notes: the
generator wrote `(ts-015، 00:03)` with U+60C and the matcher's comma class accepted only U+002C, so
`pins` reported "Flags: 0" having parsed zero cites. Any place two components disagree about
whether two strings are equal, one of them is wrong.

The doctrine that constrains the design
--------------------------------------
**Normalisation belongs to the matcher, never to the stored text.** A note's «…» quote must be
exactly what the transcript says -- diacritics, hamza carriers and all -- because its whole claim is
"these words, at this minute". So nothing here may be used to rewrite a note; it exists only to
answer "would a human reading both say this is the same wording?".

What the folds mean
-------------------
Each fold is justified by ASR reality, not by taste:

  harakat / tatweel   typing conventions; the same word is written with and without them.
  أ إ آ -> ا          the four alefs are one letter; ASR picks per utterance.
  ؤ -> و  ئ -> ي      hamza carriers: the SAME sound, and ASR alternates within one sentence.
  ة -> ه              ta marbuta; ASR writes both, manuscripts prefer ه.
  ى -> ي              alef maqsura / ya; the classic ASR swap.
  ء (dropped)         a bare hamza is a glottal stop, usually a transcription artefact of a word
                      whose real spelling carries it elsewhere (وطأته / وطاته).
  ، == ,              both commas, one function. This is the one that broke cite parsing.

`keep_punct` exists because the cite grammar needs to SEE punctuation to find a cite; text
comparison wants it gone.

Optional dependency
-------------------
`pyarabic` (light_normalize) and `camel_tools` (Malihi) implement substantially these same folds,
and farasa tokenises Arabic morphologically. They are deliberately NOT required: this corpus is ASR
output, and morphological segmentation would change token identity and so change what "verbatim"
means -- the one thing the shelf cannot afford to move. If they are installed, `HAVE_PYARABIC` lets
a caller cross-check; the behaviour here never depends on it.
"""
from __future__ import annotations

import re

__all__ = ["ar_norm", "fold_commas", "HARAKAT_RE", "FOLD_TABLE", "FOLD_TABLE_MIN", "HAVE_PYARABIC"]

HARAKAT_RE = re.compile(r"[\u064B-\u0652\u0670\u0640]")  # diacritics, superscript alef, tatweel

#: ordered, explicit, and shared -- one place to argue about what "same" means
#: the FULL set -- what a human reading both spellings would call one word
FOLD_TABLE = (
    ("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ٱ", "ا"),
    ("ؤ", "و"), ("ئ", "ي"), ("ی", "ي"),
    ("ة", "ه"), ("ى", "ي"), ("ہ", "ه"),
)

#: match.norm's ORIGINAL set, preserved exactly. The extra folds above are correct in principle --
#: ؤ/ئ are one sound and ASR alternates within a sentence -- but folding them changed verdicts on
#: 23 of 41 existing notes (a quote newly matching at a different minute reads as a MISMATCH), so
#: widening the matcher is its own change with its own review. It is NOT smuggled in under a
#: refactor whose stated purpose is "same behaviour, one file".
FOLD_TABLE_MIN = (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ة", "ه"), ("ى", "ي"))

# Everything a reader would not call a difference in wording. ASCII comma is IN this class:
# excluding it is what let an Arabic note and an Arabic generator disagree in silence.
PUNCT_RE = re.compile(r"[«»\"“”„‟'’‘ـ؛،,;:(){}\[\]…\-\u2013\u2014\u061C؟?!*/<>|_`^~]")

WS_RE = re.compile(r"\s+")

try:                                            # optional cross-check only, never load-bearing
    from pyarabic.araby import light_normalize as _py_light_normalize  # type: ignore
    HAVE_PYARABIC = True
except Exception:
    _py_light_normalize = None
    HAVE_PYARABIC = False


def fold_commas(s: str) -> str:
    """Canonicalise the two commas to one. Cheap enough to call on raw text before a regex."""
    return (s or "").replace("\u060c", ",").replace("؛", ";")


def ar_norm(s: str, *, strip_punct: bool = True,
            fold_definite: bool = False, folds=FOLD_TABLE) -> str:
    """Canonical Arabic for COMPARISON. Never use this to write a note.

    strip_punct   : remove punctuation, including BOTH commas (text comparison).
    fold_definite : collapse a separately-written ``ال`` onto the word (match.norm's behaviour).
    """
    if not s:
        return ""
    s = HARAKAT_RE.sub("", s)
    for a, b in folds:
        s = s.replace(a, b)

    if fold_definite:
        s = re.sub(r"(?<![\w])ال\s+", "ال", s)
    if strip_punct:
        s = PUNCT_RE.sub(" ", s)
    return WS_RE.sub(" ", s).strip()
