#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""notes — moved from helpers.py (final distribution)."""
from __future__ import annotations
import os, re, bisect, sys
from html.parser import HTMLParser
from pathlib import Path
from .arabic import ar_norm
# H2.2: plain relative imports — try/except-pass swallowed real import errors.
# Verified acyclic: notes -> (config, match, citation, transcript, playlists);
# transcript/playlists never import notes.
from .config import ROOT, REF, TEMPLATES, TRANSCRIPTS, INVENTORY
from .match import norm, tokens, subseq, _token_index
from .citation import (fmt_mmss, parse_mmss, QUOTE_RE, CITE_RE, TEXT_CITE_RE,
                       QUOTE_MIN_TOKENS, fmt_cite, source_hint, iter_cites,
                       KEY_PATTERN)
from .transcript import check_quote, CleanSource   # notes->transcript->playlists->citation: no cycle
from .playlists import DUPLICATE_SESSIONS, get_session, notes_dir, session_key_of, block_of, load_sessions
# Local definitions to break circular import with playlists (notes is leaf, playlists imports nothing from notes)
# A5.2: the divergent private exempt list is gone — header_is_exempt
# (config-driven, diacritic-tolerant) is the one vocabulary.
# HTML scan helpers — moved from playlists.py so notes is self-contained (was NameError after split)
_ATTR_STRIP_RE = re.compile(r"\s[\w-]+=\"[^\"]*\"")
_TAG_STRIP_RE = re.compile(r"<[^>]+>")

# ---------------- config-driven note metadata (reusable across shelves) ----------------
# ================= NoteDoc parse record (A5.1 spec) =================
# NoteDoc is the ONE parsed representation of a note. It is a dict-spec (the
# codebase carries no dataclasses). parse_note(path|text) builds it from the
# existing primitives ONLY — _iter_note_lines, scan_lines, find_meta_row,
# header_is_exempt — no new grammars. No consumer keeps a private note-grammar
# regex (the A5.3 grep audit: المحور / التحقق / نصوص regexes exist in
# notes.py alone).
#
# {
#   "path":  Path | None,        # raw handle; None when parsed from text
#   "raw":   str,                # full note text (fixer line-backing)
#   "ident": (pl|None, ident|None),  # WIDENED grammar: unicode slug + \d{2,4}
#                                #  — is-015, cs-79, rr-0002, AR slug names
#   "key":   str | None,         # note_source_key (Session row first, then
#                                #  filename grammar; registry-verified)
#   "meta":  {label_norm: {"label": str, "value": str, "line": int}},
#                                # tolerant-matched rows via find_meta_row; the
#                                #  EN row regexes (SESSION_ROW_RE etc.) survive
#                                #  ONLY here, as legacy fallbacks behind the
#                                #  tolerant matcher
#   "status": str|None, "flags": str|None,     # resolved (stripped) values
#   "status_valid": bool, "flags_valid": bool, # whole-value (A5.6)
#   "scaffold_reason": str|None,               # note_is_empty reason, computed
#   "sections": [{"header": str, "line": int, "exempt": bool,
#                 "body": [(line_no, text)]}], # ALL ## and ### sections
#   "items": [{"line": int, "text": str, "spans": [(s, e)]}],
#                                # numbered/bold rows with bold-span offsets
#   "quotes": scan_lines(txt),   # {line, quote, key, secs, cited, bq} — lines
#                                #  are raw-text lines so edits apply back
# }
#
# Consumer checklist (the A5.1 acceptance):
#  - verify worklist/apply: quotes[].line + items[].spans replace _items_of
#    and _note_verdicts' private regexes (incl. the lazy-capture ل receipt).
#  - coverage counting: meta + status + sections (### المحور is a section)
#    + quotes cover key/status/claims counting; the ### MEH-miss dies.
#  - stitch: sections[].header + body cover scaffold --from-notes with a
#    config-driven section vocabulary (the نصوص وآثار literal dies).
#  - gates: resolved meta fields + scaffold_reason + sections[].exempt (via
#    header_is_exempt) cover check_note/notes-gate metadata checks and the
#    U+FFFD region — _scanned_region's divergent private exempt list is
#    DELETED once its callers port.
#  - fixer offsets: quotes[].bq/.line + raw cover pins --fix line surgery.

# ================= end NoteDoc spec =================

# Labels/values come from corpus.note_meta; defaults = Investing EN. Matching is
# diacritic-tolerant (Arabic harakat stripped) so ASR/typo variants of a label still
# resolve. A new shelf only edits its config/project.yaml corpus.note_meta block.
from .config import corpus_cfg as _corpus_cfg
_note_meta = (_corpus_cfg() or {}).get("note_meta", {}) or {}
SESSION_LABEL = _note_meta.get("session", "Session")
STATUS_LABEL = _note_meta.get("status", "Status")
FLAGS_LABEL = _note_meta.get("flags", "Flags open")
TITLE_LABEL = _note_meta.get("title", "Title")
STATUS_VALUES = tuple(_note_meta.get("status_values", []) or ()) or (
    "draft", "ready-for-review", "reviewed")
FLAGS_NO = _note_meta.get("flags_no", "no")
FLAGS_YES = _note_meta.get("flags_yes", "yes")
SCAFFOLD_STATUS = _note_meta.get("scaffold_status", "")
# Section headers exempt from quote scanning (informational, never gate-enforced).
# Config-driven; defaults = Investing EN. Matched by normalized prefix (a header may
# carry a parenthetical, e.g. "أعلام للمراجعة (للشيخ / للمراجع)").
EXEMPT_SECTION_KEYWORDS = tuple(_note_meta.get("exempt_sections", []) or ()) or (
    "papers cited", "fidelity flags", "fidelity log")
# A5.3(c): scaffold --from-notes stitches THESE sections (normalized prefix
# match over NoteDoc sections). Config: corpus.note_meta.stitch_sections. The
# retired hardcoded list omitted نصوص وآثار — notes' primary content never
# stitched — so the default carries it.
STITCH_SECTIONS = tuple(_note_meta.get("stitch_sections", []) or ()) or (
    "Themes", "Claims and evidence", "Sources", "محاور", "قصص", "نصوص وآثار")

_HARAKAT_RE = re.compile(r"[\u064B-\u0652\u0640\u0670]")


def _norm_label(s: str) -> str:
    """Normalize a metadata label/value for tolerant comparison: strip Arabic
    harakat + tatweel, fold alef/ta-marbuta/etc. No shelf specifics here."""
    return ar_norm(s or "", drop_hamza=False, strip_punct=False)  # exactly the old fold set


# ---------------- verdict grammar (A5.3(b): the ONE home) ----------------
# التحقق is the house verdict keyword; consumers reference these constants
# instead of private regex forks. verdict_of() is the status/tail extractor —
# the lazy-capture receipt's home: a bare lazy span once captured the lone
# 'ل' of 'لشيخ', so bold is tried FIRST and a dash-partition is the fallback.
VERDICT_KW = "التحقق"
VERDICT_VAL_RE = re.compile(r"التحقق[:：]?\s*([^\n]+)")
VERDICT_LINE_RE = re.compile(r"—?\s*التحقق[:：][^\n]*")


def verdict_of(block: str):
    """(status, tail) from a block's التحقق line; ("", "") when none."""
    m = VERDICT_VAL_RE.search(block)
    if not m:
        return "", ""
    raw = re.sub(r"\s+", " ", m.group(0)).strip()
    sm = re.search(r"التحقق[:：]\s*\*\*([^*]+)\*\*", raw)
    if sm:
        return sm.group(1).strip(), raw[sm.end():]   # unstripped: caller's tail chain strips
    sm = re.search(r"التحقق[:：]\s*", raw)
    rest = raw[sm.end():] if sm else raw
    status, _, tail = rest.partition(" —")
    return status.strip().rstrip("—").strip(), tail.strip(" —")


def find_section(doc, kw: str):
    """First NoteDoc section whose header (diacritic-tolerant) starts with kw."""
    k = _norm_label(kw)
    for s in doc["sections"]:
        if _norm_label(s["header"]).startswith(k):
            return s
    return None


# A5.3 audit: the numbered-table digest row grammar's one home (used by the
# evdoc pre-draft seed; header rows are skipped exactly as before).
KHU_ROW_RE = re.compile(r"^\|\s*\d+\s*\|\s*([^|]{10,80})\|")


def khu_rows(raw: str):
    """Numbered-table digest rows (| N | text |) from a note."""
    out = []
    for line in raw.splitlines():
        s = line.strip()
        if "المحاور" in s or re.match(r"^\| *المحور", s):
            continue
        m = KHU_ROW_RE.match(s)
        if m:
            out.append(m.group(1).strip())
    return out


def claims_count(raw: str, source: str) -> int:
    """Claim units in a note — the ONE home of the claims grammar (A5.3(a)/(d)):
    '| C# |' table rows (source 'C#') and/or '### المحور…' headers (source
    'محاور', diacritic-tolerant prefix match). Claim-mass's pick-the-dominant-
    form logic stays in claim_mass, which delegates each branch here.
    ('auto' branch removed, ponytail T1: all call sites pass explicit source.)

    S9.3 port (receipt): the فقه-النفس fork measured claims-equivalent as the
    count of « quoted spans (the pinnable units — giant Q&A notes carry 165-214
    of them and no C#/محاور table), so source 'quotes' counts them here rather
    than in a gate script. A gate asks for it via corpus.claim_source: quotes."""
    # 1.2.18: refuse loudly on unknown source. The 'auto' removal (1.2.17)
    # silently returned 0 on shelves whose config still declared it
    # (measured: Programming) — a config error must crash, never read as an
    # empty corpus (AGENTS.md: Flags: 0 on zero scanned spans is a refusal).
    if source not in ("C#", "محاور", "quotes", "«"):
        raise ValueError(
            f"claims_count: unknown source {source!r} — config.claim_source "
            "must be a concrete grammar ('C#', 'محاور', or 'quotes'); "
            "'auto' was removed in 1.2.17")
    n = 0
    if source in ("quotes", "«"):
        return raw.count("«")
    if source == "C#":
        n += sum(1 for line in raw.splitlines() if re.match(r"\|\s*C\d+\s*\|", line))
    if source == "محاور":
        mk = _norm_label("المحور")
        n += sum(1 for line in raw.splitlines()
                 if line.strip().startswith("### ") and
                 _norm_label(line.strip()[4:]).startswith(mk))
    return n


def find_meta_row(txt: str, label: str):
    """Value cell of the first markdown table row whose label cell contains
    `label` (diacritic-tolerant substring match), else None."""
    kw = _norm_label(label)
    for line in txt.split("\n"):
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) >= 2 and kw and kw in _norm_label(cells[0]):
            return cells[1]
    return None


def meta_status(txt: str):
    return find_meta_row(txt, STATUS_LABEL)


def meta_flags(txt: str):
    return find_meta_row(txt, FLAGS_LABEL)


def status_is_valid(value: str) -> bool:
    # A5.6: WHOLE-value match — the substring form validated 'drafted'
    # ('draft' is a substring) and any superset of a configured value, so a
    # typo'd compound passed as a valid status.
    # F1/fqhn exception (prefix grammar): fork-era shelves write FREE-PROSE
    # statuses that are enum-value + annotation ("مسودة مكتملة",
    # "مكتملة — بانتظار ضبط الأعلام للشيخ (5 مواضع)"). An enum value at
    # position 0 is a declared status; text after it is workflow annotation.
    # Receipt: fqhn values census, FINDINGS.md F1. Config gates off
    # (default whole-match) until a shelf declares it, like other [B-config].
    v = _norm_label(value)
    if (_corpus_cfg() or {}).get("status_prefix_ok"):
        if any(v.startswith(_norm_label(ok)) for ok in STATUS_VALUES):
            return True
        # F16b: truncated-enum + paren annotation — `جاهزة (clean-only، …)`
        # writes the enum's HEAD (جاهزة) then annotates in parens; the enum is
        # جاهزة للمراجعة. Value-head that is a prefix OF an enum value, with a
        # paren present, is a declared status (measured: the last 2 invalid-
        # values in fqhn v15, both this exact shape).
        head = re.split(r"[(\uff08]", v, 1)[0].strip()
        if head and head != v and "(" in value:
            return any(_norm_label(ok).startswith(head) for ok in STATUS_VALUES)
        return False
    return any(_norm_label(ok) == v for ok in STATUS_VALUES)


def flags_is_valid(value: str) -> bool:
    # F16: the generator writes the COUNT form (`| أعلام محالة للشيخ | 12 |`,
    # draft_note._alam) and the fork writes `value (annotation)` — `لا
    # (تفصيلها في «أعلام للمراجعة»)`, `8 (انظر قسم أعلام المراجعة)`. The old
    # whole-value check rejected the generator's OWN numeric output and every
    # annotated form (measured: 29 invalid-values in fqhn v14, 21 distinct
    # shapes, all value+paren). Parallel to the F1 status prefix grammar:
    # accepted value at position 0 (لا / نعم / digits), paren annotation after.
    v = _norm_label(value)
    no = _norm_label(FLAGS_NO)
    yes = _norm_label(FLAGS_YES)
    head = re.split(r"[(\uff08]", v, 1)[0].strip()
    if head in (no, yes):
        return True
    if re.fullmatch(r"\d+", head):
        return True
    return v == no or (yes and v.startswith(yes))


# Legacy row regexes kept for back-compat with Investing-EN callers; the tolerant
# find_meta_row() above is the reusable path.
SESSION_ROW_RE = re.compile(r"^\|\s*Session\s*\|\s*([^|\n]+?)\s*\|", re.M)
STATUS_ROW_RE = re.compile(r"^\|\s*Status\s*\|\s*([^|\n]+?)\s*\|", re.M)
FLAGS_ROW_RE = re.compile(r"^\|\s*Flags open\s*\|\s*([^|\n]+?)\s*\|", re.M)
TITLE_ROW_RE = re.compile(r"^\|\s*Title\s*\|\s*([^|\n]+?)\s*\|", re.M)
_EMPTY_TYPE = re.compile(r"\|\s*Type\s*\|\s*\(type:")
# A5.6: the marker comes from config — escape it (regex metachars in a
# shelf's custom marker must match literally, not explode).
_EMPTY_TODO = re.compile(re.escape(_note_meta.get("scaffold_marker", "TODO: distill from the transcript")))
# Lazy import for playlists-dependent helpers to avoid circular top-level import
def _lazy_playlists():
    # H2.2: call-time import kept (import-time cycle avoidance), flat fallback removed —
    # a failure here must be loud, not silently swallowed.
    from .playlists import (SESSION_ROW_RE as _S, session_key_of as _sko, get_session as _gs,
                            DUPLICATE_SESSIONS as _dup, load_sessions as _ls, clean_dir as _cd,
                            notes_dir as _nd)
    return _S, _sko, _gs, _dup, _ls, _cd, _nd
def header_is_exempt(header: str) -> bool:
    """True when a '## ' section header matches a config exempt keyword
    (diacritic-tolerant normalized prefix). Reused by scan + pins --fix."""
    h = _norm_label(header)
    return any(h.startswith(_norm_label(kw))
               for kw in EXEMPT_SECTION_KEYWORDS if kw)


def _iter_note_lines(txt):
    """Yield (line_no, annotation-stripped line), skipping headings and the
    exempt sections (resuming after them)."""
    exempt = False
    for line_no, raw in enumerate(txt.split("\n"), 1):
        s = raw.strip()
        if s.startswith("#"):
            if s.startswith("## "):
                exempt = header_is_exempt(s[3:].strip())
            continue
        if exempt:
            continue
        yield line_no, re.sub(r"\[[^\]]*\]", "", s)


BARE_MIN_RE = re.compile(r"\(\s*(\d{1,2}:\d{2})(?:\s*[–-]\s*\d{1,2}:\d{2})?\s*\)")
# F13: fork table-row minute cell — the row opens with `| 01:25 |`
ROW_MIN_RE = re.compile(r"^\s*\|\s*(\d{1,2}:\d{2})\s*\|")
# F15: fork bracket-minute marker — `- \`clean/064 [00:13]\`: «q»` (a source-path
# segment marker inside backticks, BEFORE the quote)
BRACKET_MIN_RE = re.compile(r"\[\s*(\d{1,2}:\d{2})\s*\]")


def scan_lines(txt, own_pl=None, own_key=None):
    """Extract quoted spans + their cites from plain/markdown text.
    T9.1: own_pl threads the note's playlist into keyword-cite resolution
    (corpus.cite_playlist=self -> المجلس N inside a <pl>-NNN note = that
    playlist's session N).

    Pairing (config-driven grammar via iter_cites / QUOTE_RE):
      1. a quote takes the FIRST cite AFTER it on the same line (before the next
         quote) — the canonical «quote» (KEY, MM:SS) form;
      2. else the last cite BEFORE it on the same line — the story form
         "**title** — المجلس N، MM:SS: … «quote»";
      3. else, on a blockquote line ("> «quote»"), the most recent cite carried
         from a preceding item line — the نصوص/آثار form where the cite sits on
         the numbered item line above the quoted text.
    Yields {line, quote, key, secs, cited}."""
    records = []
    carry = None  # (key, secs) from the last item line, for blockquote quotes
    for line_no, s in _iter_note_lines(txt):
        events = []
        for qm in QUOTE_RE.finditer(s):
            # QUOTE_RE is config-driven and always has ONE group = the quote text.
            if qm.group(1) is None:
                continue
            events.append((qm.start(), "q", (qm.group(1).strip(), qm.start(1), qm.end(1))))
        # iter_cites encapsulates the CITE_RE group layout (config-driven grammar).
        line_cites = list(iter_cites(s, own_pl))
        for key, secs, cstart, _cend in line_cites:
            events.append((cstart, "c", (key, secs)))
        events.sort(key=lambda ev: ev[0])
        is_bq = s.startswith(">")
        digest_item = "(هضم)" in s or "(هضم" in s
        for i, (pos, kind, val) in enumerate(events):
            if kind != "q":
                continue
            nxt_q = next((p for p, k, _ in events[i + 1:] if k == "q"), len(s))
            cite = next((v for p, k, v in events[i + 1:]
                         if k == "c" and p < nxt_q), None)
            # F8: bare-minutes parenthetical — «q» (01:32) with no key means
            # the note's OWN session (fork shorthand for a follow-up quote
            # sharing the line's session cite). It sits ADJACENT to the quote,
            # so it outranks the nearest preceding line cite (without this the
            # quote inherited the neighbour's cite — the wrong-minute receipt:
            # fleet-1a 58/63 unchanged all had this shape).
            if cite is None and own_key:
                # F14: ADJACENT only — the fork's shorthand is «q» (01:32). with
                # the paren IMMEDIATELY after the closing «». A windowed match
                # refuses prose parentheticals deeper in the line (measured:
                # table detail cells carrying Quran refs like (5:17) were read
                # as the quote's minute and outranked the row's real cell).
                bm = re.match(r"[\s.)\u060C\u061B—-]{0,4}" + BARE_MIN_RE.pattern,
                              s[val[2]:val[2] + 10])
                if bm:
                    mins = parse_mmss(bm.group(1))
                    if mins is not None:
                        cite = (own_key, [mins])
            # F13: fork table-row form — `| 01:25 | «q» | detail |` carries the
            # row's own minute in a cell BEFORE the quote. scan_lines didn't
            # parse the cell as a cite, so the quote fell through to the
            # nearest PRECEDING line cite (e.g. 05:17) and read as wrong-minute
            # while the note was right all along (measured: the last 2
            # wrong-minute verdicts in fqhn v11, both table rows).
            if cite is None and own_key:
                # F13 row cell first, then F15: the LAST minute marker before
                # the quote on the same line (row cell or bracket marker).
                pre = s[:val[1]]
                bm2 = ROW_MIN_RE.search(s) or None
                if bm2 is None:
                    bms = list(BRACKET_MIN_RE.finditer(pre))
                    bm2 = bms[-1] if bms else None
                if bm2:
                    mins2 = parse_mmss(bm2.group(1))
                    if mins2 is not None:
                        cite = (own_key, [mins2])
            if cite is None:
                # nearest preceding cite (handles a line where one cite serves
                # several quotes, e.g. قصص: "— المجلس N، MM:SS: … «q1» و«q2»")
                cite = next((v for p, k, v in reversed(events[:i])
                             if k == "c"), None)
            if cite is None and is_bq and carry is not None:
                cite = carry
            if cite:
                rec = {"line": line_no, "quote": val[0],
                       "key": cite[0], "secs": cite[1], "cited": True,
                       "bq": is_bq, "digest": digest_item}
                # F11c: text-source cite adjacent to the quote — (رواه مسلم),
                # (سورة …), (مصادر متحققة) — marks a CANONICAL-text quote: the
                # fork quotes the book over the sheikh's spoken paraphrase. The
                # transcript cite only locates the discussion; verification
                # target is the text authority, so transcript mismatch parks
                # as advisory (claims lane), never gating.
                nxt2 = next((p3 for p3, k3, _ in events[i + 1:] if k3 == "q"), len(s))
                if TEXT_CITE_RE.search(s[val[2]:nxt2]):
                    rec["text"] = True
                records.append(rec)
            else:
                records.append({"line": line_no, "quote": val[0],
                                "key": None, "secs": [], "cited": False,
                                "bq": is_bq, "digest": digest_item})
        # Update the carry for subsequent blockquote lines: a line with a cite
        # refreshes it; a non-blockquote line without one resets it (new item).
        if line_cites:
            carry = (line_cites[-1][0], line_cites[-1][1])
        elif not is_bq:
            carry = None
    return records


def scan_html(html_txt: str, walker: bool = False):
    """Same extraction over an HTML topic doc. Text blocks live in
    p/li/dd/dt/td elements before the <section class="cite"> sources list.

    A5.7: walker=True routes through the html.parser text walker (nesting-
    robust; default off so the regex path stays the proven baseline)."""
    import html as _h
    body = html_txt.split('<section class="cite"')[0]
    if walker:
        w = _TextWalker(); w.feed(body); w.close()
        records = []
        # tag-major order + post-bracket re-collapse — exactly the regex
        # path's semantics (bracket removal can open a double space).
        for want_tag in ("p", "li", "dd", "dt", "td"):
            for tag, b in w.block_texts():
                if tag != want_tag:
                    continue
                b = re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", "", b)).strip()
                if not (QUOTE_RE.search(b) or CITE_RE.search(b)):
                    continue
                records.extend(scan_lines(b))
        return records
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", body, flags=re.S)
    body = _ATTR_STRIP_RE.sub(" ", body)
    records = []
    for tag in ("p", "li", "dd", "dt", "td"):
        for bm in re.finditer(rf"<{tag}\b[^>]*>(.*?)</{tag}>", body, flags=re.S):
            b = _TAG_STRIP_RE.sub(" ", bm.group(1))
            b = _h.unescape(b)
            b = re.sub(r"\[[^\]]*\]", "", b)
            b = re.sub(r"\s+", " ", b).strip()
            if not (QUOTE_RE.search(b) or CITE_RE.search(b)):
                continue
            records.extend(scan_lines(b))
    return records


class _TextWalker(HTMLParser):
    """A5.7: html.parser text-node walker — the doc gate's measurement basis.

    Collects (no stored doc object — the walker is consumed in one pass):
      text()         full visible text, style/script bodies skipped;
                     blockquote text IS included (it counts as words)
      block_texts()  [(tag, text)] for p/li/dd/dt/td with blockquote content
                     EXCLUDED (the gate measures the author's prose, and the
                     retired regex path measured quote-stripped prose too)"""

    SKIP = ("script", "style")
    BLOCKS = ("p", "li", "dd", "dt", "td")

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._skip = 0
        self._bq = 0
        self._parts = []
        self._stack = []
        self._done = []

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self._skip += 1
        elif tag == "blockquote":
            self._bq += 1
        elif tag in self.BLOCKS:
            self._stack.append([])

    def handle_endtag(self, tag):
        if tag in self.SKIP and self._skip:
            self._skip -= 1
        elif tag == "blockquote" and self._bq:
            self._bq -= 1
        elif tag in self.BLOCKS and self._stack:
            self._done.append((tag, "".join(self._stack.pop())))

    def handle_data(self, data):
        if self._skip:
            return
        self._parts.append(data)
        if not self._bq:
            for buf in self._stack:
                buf.append(data)

    def close(self):
        super().close()
        while self._stack:            # unclosed blocks still count
            self._done.append((self.BLOCKS[0], "".join(self._stack.pop())))

    def text(self):
        return re.sub(r"\s+", " ", "".join(self._parts))

    def block_texts(self):
        return [(t, re.sub(r"\s+", " ", x).strip()) for t, x in self._done]


def html_measure(html_txt: str, para_chars: int = 300, def_chars: int = 80):
    """A5.7: (total_words, paras, defs) via one _TextWalker pass — the doc
    gate's length/paragraph/definition measurements. paras: p/li/dd texts
    over `para_chars`; defs: td texts over `def_chars` (the retired
    thresholds). P6.14: para_chars is read from gates.essay_proxy.
    min_para_chars by doc-gate and evdoc — one key, both consumers."""
    body = html_txt.split('<section class="cite"')[0]
    w = _TextWalker(); w.feed(body); w.close()
    total_words = len(w.text().split())
    paras = [x for t, x in w.block_texts() if t in ("p", "li", "dd") and len(x) > para_chars]
    defs = [x for t, x in w.block_texts() if t == "td" and len(x) >= def_chars]
    return total_words, paras, defs

# ---------------- note plumbing ----------------

def note_ident(note_path: Path):
    """(playlist, ident) from a note filename. P6.4: the grammar is the WIDE
    one (unicode slug + 2-4 digit idents — is-015, cs-79, rr-0002, AR slugs),
    shared with parse_note since A5.2; the narrow ASCII/3-digit form silently
    skipped every Arabic-named note in check's sweep. (None, None) when the
    filename carries no key."""
    return _note_ident_wide(note_path.name)


def _note_ident_wide(name: str):
    """A5.1 widened note-ident grammar: unicode slug (\\w matches Arabic)
    + 2-4 digit number — is-015, cs-79, rr-0002, AR slug names. Falls back to
    the ex-<slug> extras grammar. T9.1: PREFIXLESS numeric notes (047-title.md
    — a corpus that predates the slug grammar) bind to the unique empty-
    key_prefix playlist, checked BEFORE the wide grammar so 047-52-title.md is
    never mis-parsed as playlist '047'."""
    try:
        from .playlists import KEY_PREFIXES
        _pless = [p for p, pre in KEY_PREFIXES.items() if pre == ""]
    except Exception:
        _pless = []
    if len(_pless) == 1:
        m = re.match(r"^(\d{2,4})-", name)
        if m:
            return _pless[0], m.group(1)
    m = re.match(r"^(\w+)-(\d{2,4})-", name)
    if m:
        return m.group(1).lower(), m.group(2)
    m = re.match(r"^ex-([\w-]+)\.md$", name)
    if m:
        return "ex", m.group(1)
    return None, None


def _meta_rows(raw: str):
    """Every markdown table row as {norm-label: {label, value, line}} — the
    ONE walk parse_note uses; find_meta_row stays the single-row public API."""
    rows = {}
    for ln, line in enumerate(raw.split("\n"), 1):
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 2 or not cells[0] or cells[0].startswith("-"):
            continue
        key = _norm_label(cells[0])
        if key and key not in rows:
            rows[key] = {"label": cells[0], "value": cells[1], "line": ln}
    return rows


def parse_note(source):
    """Parse a note into a NoteDoc (A5.1 spec above). `source` is a Path
    (or note text). Built from the existing primitives — no new grammars."""
    if isinstance(source, Path):
        path = source
        raw = source.read_text(encoding="utf-8", errors="replace")
    else:
        path, raw = None, str(source)

    ident = _note_ident_wide(path.name) if path is not None else (None, None)
    meta = _meta_rows(raw)

    def _mval(label):
        row = meta.get(_norm_label(label))
        return row["value"] if row else None

    # resolved fields — tolerant matcher first; the EN row regexes are the
    # legacy fallback behind it (only reached when the configured label is
    # absent but an Investing-EN row exists).
    status = _mval(STATUS_LABEL)
    if status is None:
        sm = STATUS_ROW_RE.search(raw)
        status = sm.group(1).strip() if sm else None
    # F17: a second fork template carries status in YAML frontmatter
    # (`status: "…"` at line start) instead of a metadata table — the table
    # walk and the EN fallback both miss it, so the note reads as having NO
    # status at all (measured: fqhn note 150 — YAML template, 0 table rows).
    if status is None and raw.startswith("---"):
        fm = re.search(r'^status:\s*(.+)$', raw, re.M)
        status = fm.group(1).strip().strip('"') if fm else None
    flags = _mval(FLAGS_LABEL)
    if flags is None:
        fm = FLAGS_ROW_RE.search(raw)
        flags = fm.group(1).strip() if fm else None
    if flags is None and raw.startswith("---"):
        fm2 = re.search(r'^flags:\s*(.+)$', raw, re.M)
        flags = fm2.group(1).strip().strip('"') if fm2 else None

    # sections: ALL ## and ### blocks, exempt flag via header_is_exempt.
    # `end` (exclusive, raw-line index) stops at the NEXT LEVEL-2 header —
    # the consumers' historical body extent; ### blocks nest inside it.
    sections = []
    cur = None
    for ln, line in enumerate(raw.split("\n"), 1):
        s = line.strip()
        if s.startswith("## ") or s.startswith("### "):
            header = s[3:].strip()
            cur = {"header": header, "line": ln, "level": 2 if s.startswith("## ") else 3,
                   "exempt": header_is_exempt(header), "body": []}
            sections.append(cur)
        elif cur is not None:
            cur["body"].append((ln, line))
    _ends = [s["line"] for s in sections if s["level"] == 2] + [len(raw.split("\n")) + 1]
    for s in sections:
        nxt = min((e for e in _ends if e > s["line"]), default=len(raw.split("\n")) + 1)
        s["end"] = max(nxt - 1, s["line"])   # exclusive index into raw lines

    # items: numbered/bold rows — the block extends to the next item line.
    # title/quote/verdict are RESOLVED here so no consumer keeps a private
    # التحقق/«» grammar (A5.3(b): the lazy-capture receipt's home).
    lines = raw.split("\n")
    item_lns = [ln for ln, line in enumerate(lines, 1)
                if re.match(r"^(?:[-*]|\d+[.)])\s+", line.strip())]
    items = []
    for i, ln in enumerate(item_lns):
        end = item_lns[i + 1] - 1 if i + 1 < len(item_lns) else len(lines)
        block = "\n".join(lines[ln - 1:end])
        t = re.search(r"\*\*(.+?)\*\*", block)
        q = re.search(r">\s*«([^»]+)»", block)
        vm = VERDICT_VAL_RE.search(block)
        items.append({"line": ln, "text": lines[ln - 1].strip(),
                      "spans": [(m.start(1), m.end(1)) for m in re.finditer(r"\*\*(.+?)\*\*", lines[ln - 1])],
                      "block": block,
                      "title": t.group(1).strip() if t else "",
                      "quote": q.group(1).strip() if q else "",
                      "verdict": vm.group(1).strip() if vm else ""})

    key = note_source_key(raw, path)
    return {
        "path": path, "raw": raw, "ident": ident, "key": key,
        "meta": meta,
        "status": status.strip() if status is not None else None,
        "flags": flags.strip() if flags is not None else None,
        "status_valid": status_is_valid(status) if status is not None else False,
        "flags_valid": flags_is_valid(flags) if flags is not None else False,
        "scaffold_reason": _scaffold_reason(raw),
        "sections": sections, "items": items,
        # F6 root fix: the note's OWN playlist threads into keyword-cite
        # resolution (cite_playlist=self) — without it, «المجلس 28» inside an
        # abtr note parsed bare and downstream resolution sent it to the
        # default playlist's session 028 (wrong transcript, mass MISSING).
        "quotes": scan_lines(raw, own_pl=ident[0], own_key=key),
    }


def note_source_key(txt: str, note_path: Path | None = None):
    """Resolve a note's own session key: the tolerant-matched Session row
    first (works for any configured label), then the legacy EN row regex,
    then the filename grammar. Registry-verified either way."""
    sm = find_meta_row(txt, SESSION_LABEL)
    if sm is None:                        # legacy fallback: EN row regex
        m = SESSION_ROW_RE.search(txt)
        sm = m.group(1).strip() if m else None
    if sm:
        k = sm.strip()
        if get_session(k):
            return k
    if note_path is not None:
        pl, ident = note_ident(note_path)
        if pl:
            k = session_key_of(pl, ident)
            if get_session(k):
                return k
    return None


def _scaffold_reason(raw: str) -> str | None:
    """note_is_empty's reason for a TEXT (parse_note + Path wrapper share it)."""
    if _EMPTY_TODO.search(raw):
        return "empty scaffold: distillation placeholder still present"
    if _EMPTY_TYPE.search(raw):
        return "empty scaffold: Metadata Type row not filled"
    if SCAFFOLD_STATUS:
        st = find_meta_row(raw, STATUS_LABEL)
        if st is not None and _norm_label(st) == _norm_label(SCAFFOLD_STATUS):
            return f"unfinished scaffold: {STATUS_LABEL} still '{st.strip()}' — distill the note"
    return None


def note_is_empty(note: Path) -> str | None:
    """Reason string when the note is still an unfilled scaffold (an empty
    template contains no quotes and would pass vacuously), else None. Config-
    driven: corpus.note_meta.scaffold_marker / scaffold_status extend the check
    beyond the Investing-EN defaults."""
    return _scaffold_reason(note.read_text(encoding="utf-8", errors="replace"))


def note_status_of(note: Path) -> str:
    txt = note.read_text(encoding="utf-8")
    v = meta_status(txt)
    return v.strip() if v is not None else "no status row"


def scanned_region(txt: str) -> str:
    """Note text minus exempt sections — the region the U+FFFD guard applies to
    (fidelity tables legitimately document corrupted source characters).
    A5.2: the exemption vocabulary is header_is_exempt (config-driven,
    diacritic-tolerant) — the divergent private EN list is gone."""
    out, exempt = [], False
    for raw in txt.split("\n"):
        s = raw.strip()
        if s.startswith("## "):
            exempt = header_is_exempt(s[3:].strip())
        if exempt:
            continue
        out.append(raw)
    return "\n".join(out)

# ---------------- reporting ----------------

def _default_src_for():
    """A5.5: per-key CleanSource cache — the doc-side `src_for` pattern hoisted
    so NOTES verify each cite against ITS session (a note citing another
    session verbatim used to read as MISSING because every record was checked
    against the note's own source). T9.1: a key that resolves to NO session
    (e.g. a cross-playlist cite the registry can't see) returns None so the
    caller falls back to the note's own source instead of a hollow one whose
    present() is always False."""
    cache = {}

    def _get(key):
        if key not in cache:
            cs = CleanSource(key)
            cache[key] = cs if cs.rec is not None else None
        return cache[key]

    return _get



def _uncited_quotes_skip() -> bool:
    """T9.2/ADR 0007: corpus.uncited_quotes: skip — on the fqhn corpus every
    «» span is a claim measured by doc-coverage (claims source "quotes"), and
    the pins contract is the MONOLITH's: only REF'd spans (same-line
    المجلس-N، MM:SS cite) are minute-verified; a «» span with no cite is
    narrative and is skipped, not flagged. Default (unset) = the EN grammar
    this file was calibrated on, unchanged."""
    try:
        from .config import corpus_cfg
        return (corpus_cfg() or {}).get("uncited_quotes") == "skip"
    except Exception:
        return False


def report_records(records, src, sess_key, where, verbose=True, src_for=None,
                   uncited_skip=None, secs_override=None):
    """Check scanned records against the source; print ✓/✗ per real quote.

    Two lanes (records carry "bq" = evidence blockquote vs inline digest text):
      hard  -> c["fails"]:  evidence-lane violations that gate — minute
               mismatch/not-found, and a blockquote quote with no cite at all
               (an evidence claim that cannot be verified).
      soft  -> c["soft"]:   «…» quotes inside digest prose (خلاصة هضم etc.)
               without a cite — stylistic quoting in the writer's own summary;
               printed as ⚠ but NOT gating.
    T9.2: uncited_skip=True (config corpus.uncited_quotes: skip) switches the
    pins contract to the monolith's: uncited «» spans are narrative claims —
    skipped silently, never flagged, never counted as checked.
    Returns {fails, soft, checked, labels, uncited, uncited_inline, mismatch,
    missing, quoted}."""
    if uncited_skip is None:
        uncited_skip = _uncited_quotes_skip()
    c = {"fails": [], "soft": [], "checked": 0, "labels": 0, "uncited": 0,
         "uncited_inline": 0, "mismatch": 0, "missing": 0, "quoted": 0}
    seen_ok = set()
    for rec in records:
        q = rec["quote"]
        qt = tokens(q)
        if len(qt) < QUOTE_MIN_TOKENS:
            c["labels"] += 1
            continue
        c["quoted"] += 1
        disp = q if len(q) <= 60 else q[:57] + "…"
        if not rec["cited"]:
            if uncited_skip:
                continue
            c["uncited"] += 1
            if rec.get("bq"):
                msg = (f'{where}: UNCITED EVIDENCE QUOTE (line {rec["line"]}, '
                       f'{len(qt)} tokens): "{disp}" — add a same-line cite like '
                       f'({sess_key or "KEY"}, MM:SS); paste units from '
                       f'`lift {sess_key or "KEY"}`, never from memory')
                print(f"  ⚠ {msg}")
                c["fails"].append(msg)
            else:
                c["uncited_inline"] += 1
                msg = (f'{where}: uncited quote in digest text (line '
                       f'{rec["line"]}, {len(qt)} tokens): "{disp}" — advisory '
                       f'only (stylistic «» in summary prose, not the evidence '
                       f'lane)')
                print(f"  ⚠ {msg}")
                c["soft"].append(msg)
            continue
        c["checked"] += 1
        # A5.5: verify against the record's OWN session; the note's own source
        # remains the fallback (uncited rows never reach here, so a cited
        # record always carries a key).
        if src_for is None:
            src_for = _default_src_for()
        rec_src = src
        if rec["key"] and rec["key"] != sess_key:
            rec_src = src_for(rec["key"]) or src
        rec_secs = rec["secs"] if secs_override is None else secs_override
        # F9 blockquote contract: the fork's evidence blocks carry ONE item-line
        # cite covering the whole «» block — per-line minutes were never claimed.
        # A blockquote record verifies PRESENCE + contiguity in its session
        # (fabricated wording still fails; minute drift inside the block is the
        # item cite's business, not a per-line violation). Config-gated.
        if (rec.get("bq") and rec["key"] == sess_key
                and (_corpus_cfg() or {}).get("bq_item_minute")):
            rec_secs = None
        verdict, vmsg = check_quote(rec_src, q, rec_secs, where, rec["key"])
        if verdict is None:
            continue
        if verdict == "OK":
            if verbose and (q, tuple(rec["secs"])) not in seen_ok:
                seen_ok.add((q, tuple(rec["secs"])))
                print(f'  ✓ "{disp}" {fmt_cite(rec["key"], rec["secs"])}')
            continue
        if rec.get("text") and verdict in ("MISSING", "MISMATCH"):
            # F11c: canonical-text quote with a text-authority cite — advisory.
            msg = (f'{where}: "{disp}" {fmt_cite(rec["key"], rec["secs"])} — '
                   f'{vmsg} — advisory only (text-source quote, text cite present)')
            print(f"  ⚠ {msg}")
            c["soft"].append(msg)
            continue
        if rec.get("digest"):
            # F10: digest-item quotes are claims-lane (T9.2) — advisory.
            msg = (f'{where}: "{disp}" {fmt_cite(rec["key"], rec["secs"])} — '
                   f'{vmsg} — advisory only (digest item (هضم), claims lane)')
            print(f"  ⚠ {msg}")
            c["soft"].append(msg)
            continue
        msg = f'{where}: "{disp}" {fmt_cite(rec["key"], rec["secs"])} — {vmsg}'
        print(f"  ✗ line {rec['line']}: {vmsg}")
        print(f'      quote: "{disp}"')
        hint = source_hint(rec["key"], qt,
                           near=(rec["secs"][0] if rec["secs"] else None))
        if hint:
            label, span, minute = hint
            shown = span if len(span) <= 160 else span[:157] + "…"
            print(f'      {label} @{fmt_mmss(minute)} (copy-paste this): "{shown}"')
        c["fails"].append(msg)
        if verdict == "MISSING":
            c["missing"] += 1
        else:
            c["mismatch"] += 1
    return c


# ---------------- shared helpers ----------------

def os_rel(p: Path, base: Path) -> str:
    # ponytail T1: try/except relative_to -> stdlib relpath (same output on
    # POSIX; the ValueError path was reachable only for p outside base).
    return os.path.relpath(p, base)


def _asset_prefix(docs_path: Path) -> str:
    """Correct relative depth from a docs directory back to assets/.
    reference/<dir>/x.html and reference/topics/x.html both need ../../assets;
    a doc sitting directly in reference/ would need ../assets."""
    try:
        rel = str(docs_path.resolve().relative_to(REF.resolve()))
    except ValueError:
        rel = ""
    depth = 0 if rel in ("", ".") else len(rel.split("/"))
    return "/".join([".."] * (depth + 1)) + "/assets"


def find_note(key: str) -> Path | None:
    key = DUPLICATE_SESSIONS.get(key, key)   # duplicates share the canonical note
    rec = get_session(key)
    if rec is None:
        return None
    d = notes_dir(rec["pl"])
    pattern = f"{key}-*.md" if rec["num"] is not None else f"{key}.md"
    files = sorted(d.glob(pattern))
    if len(files) > 1:
        # Ambiguous resolution previously caused silent vacuous passes (pins scanning
        # an empty scaffold while the real note sat unscanned). Refuse loudly instead.
        sys.exit(f"Ambiguous note resolution for {key}: {len(files)} candidates —\n  "
                 + "\n  ".join(f.name for f in files)
                 + "\nDelete or merge duplicates so exactly one note remains.")
    return files[0] if files else None


def _cell(s: str) -> str:
    return s.replace("|", "\\|")

# ---------------- commands ----------------

