#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""notes — moved from helpers.py (final distribution)."""
from __future__ import annotations
import re, bisect, sys
from pathlib import Path
try:
    from .config import ROOT, REF, TEMPLATES, TRANSCRIPTS, INVENTORY
    from .match import norm, tokens, subseq, _token_index
    from .citation import (fmt_mmss, parse_mmss, QUOTE_RE, CITE_RE,
                           QUOTE_MIN_TOKENS, fmt_cite, source_hint, iter_cites,
                           KEY_PATTERN)
    from .transcript import check_quote  # notes->transcript->playlists->citation: no cycle
except ImportError:
    pass
try:
    from .playlists import DUPLICATE_SESSIONS, get_session, notes_dir, session_key_of, block_of, load_sessions  # playlists is leaf, safe
except ImportError:
    pass
# Local definitions to break circular import with playlists (notes is leaf, playlists imports nothing from notes)
_EXEMPT_SECTIONS = {"papers cited", "fidelity flags", "fidelity log"}
# HTML scan helpers — moved from playlists.py so notes is self-contained (was NameError after split)
_ATTR_STRIP_RE = re.compile(r"\s[\w-]+=\"[^\"]*\"")
_TAG_STRIP_RE = re.compile(r"<[^>]+>")
import re as _re

# ---------------- config-driven note metadata (reusable across shelves) ----------------
# Labels/values come from corpus.note_meta; defaults = Investing EN. Matching is
# diacritic-tolerant (Arabic harakat stripped) so ASR/typo variants of a label still
# resolve. A new shelf only edits its config/project.yaml corpus.note_meta block.
try:
    from .config import corpus_cfg as _corpus_cfg
except ImportError:
    from config import corpus_cfg as _corpus_cfg  # type: ignore
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

_HARAKAT_RE = _re.compile(r"[\u064B-\u0652\u0640\u0670]")


def _norm_label(s: str) -> str:
    """Normalize a metadata label/value for tolerant comparison: strip Arabic
    harakat + tatweel, fold alef/ta-marbuta/etc. No shelf specifics here."""
    s = _HARAKAT_RE.sub("", s or "")
    for a, b in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ة", "ه"),
                 ("ى", "ي"), ("ؤ", "و"), ("ئ", "ي")):
        s = s.replace(a, b)
    return s.strip()


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
    v = _norm_label(value)
    return any(_norm_label(ok) and _norm_label(ok) in v for ok in STATUS_VALUES)


def flags_is_valid(value: str) -> bool:
    v = _norm_label(value)
    no = _norm_label(FLAGS_NO)
    yes = _norm_label(FLAGS_YES)
    return v == no or (yes and v.startswith(yes))


# Legacy row regexes kept for back-compat with Investing-EN callers; the tolerant
# find_meta_row() above is the reusable path.
SESSION_ROW_RE = _re.compile(r"^\|\s*Session\s*\|\s*([^|\n]+?)\s*\|", _re.M)
STATUS_ROW_RE = _re.compile(r"^\|\s*Status\s*\|\s*([^|\n]+?)\s*\|", _re.M)
FLAGS_ROW_RE = _re.compile(r"^\|\s*Flags open\s*\|\s*([^|\n]+?)\s*\|", _re.M)
TITLE_ROW_RE = _re.compile(r"^\|\s*Title\s*\|\s*([^|\n]+?)\s*\|", _re.M)
_EMPTY_TYPE = _re.compile(r"\|\s*Type\s*\|\s*\(type:")
_EMPTY_TODO = _re.compile(_note_meta.get("scaffold_marker", "TODO: distill from the transcript"))
# Lazy import for playlists-dependent helpers to avoid circular top-level import
def _lazy_playlists():
    try:
        from .playlists import SESSION_ROW_RE as _S, session_key_of as _sko, get_session as _gs, DUPLICATE_SESSIONS as _dup, load_sessions as _ls, clean_dir as _cd, notes_dir as _nd
        return _S, _sko, _gs, _dup, _ls, _cd, _nd
    except ImportError:
        from playlists import SESSION_ROW_RE as _S, session_key_of as _sko, get_session as _gs, DUPLICATE_SESSIONS as _dup, load_sessions as _ls, clean_dir as _cd, notes_dir as _nd  # type: ignore
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


def scan_lines(txt):
    """Extract quoted spans + their cites from plain/markdown text.

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
        line_cites = list(iter_cites(s))
        for key, secs, cstart, _cend in line_cites:
            events.append((cstart, "c", (key, secs)))
        events.sort(key=lambda ev: ev[0])
        is_bq = s.startswith(">")
        for i, (pos, kind, val) in enumerate(events):
            if kind != "q":
                continue
            nxt_q = next((p for p, k, _ in events[i + 1:] if k == "q"), len(s))
            cite = next((v for p, k, v in events[i + 1:]
                         if k == "c" and p < nxt_q), None)
            if cite is None:
                # nearest preceding cite (handles a line where one cite serves
                # several quotes, e.g. قصص: "— المجلس N، MM:SS: … «q1» و«q2»")
                cite = next((v for p, k, v in reversed(events[:i])
                             if k == "c"), None)
            if cite is None and is_bq and carry is not None:
                cite = carry
            if cite:
                records.append({"line": line_no, "quote": val[0],
                                "key": cite[0], "secs": cite[1], "cited": True,
                                "bq": is_bq})
            else:
                records.append({"line": line_no, "quote": val[0],
                                "key": None, "secs": [], "cited": False,
                                "bq": is_bq})
        # Update the carry for subsequent blockquote lines: a line with a cite
        # refreshes it; a non-blockquote line without one resets it (new item).
        if line_cites:
            carry = (line_cites[-1][0], line_cites[-1][1])
        elif not is_bq:
            carry = None
    return records


def scan_html(html_txt: str):
    """Same extraction over an HTML topic doc. Text blocks live in
    p/li/dd/dt/td elements before the <section class="cite"> sources list."""
    import html as _h
    body = html_txt.split('<section class="cite"')[0]
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

# ---------------- note plumbing ----------------

def note_ident(note_path: Path):
    """(playlist, ident) from a note filename. Numeric notes derive the playlist
    prefix generically (is-015-*, cs-079-*, rr-002-*) so any shelf works without
    editing this file; extras keep the ex-<slug> grammar. (None, None) when the
    filename carries no key."""
    m = re.match(r"^([A-Za-z]+)-(\d{3})-", note_path.name)
    if m:
        return m.group(1).lower(), m.group(2)
    m = re.match(r"^ex-([a-z0-9-]+)\.md$", note_path.name)
    if m:
        return "ex", m.group(1)
    return None, None


def note_source_key(txt: str, note_path: Path):
    """Resolve a note's own session key: the | Session | metadata row first
    (works for fixtures outside reference/), then the filename grammar."""
    sm = SESSION_ROW_RE.search(txt)
    if sm:
        k = sm.group(1).strip()
        if get_session(k):
            return k
    pl, ident = note_ident(note_path)
    if pl:
        k = session_key_of(pl, ident)
        if get_session(k):
            return k
    return None


def note_is_empty(note: Path) -> str | None:
    """Reason string when the note is still an unfilled scaffold (an empty
    template contains no quotes and would pass vacuously), else None. Config-
    driven: corpus.note_meta.scaffold_marker / scaffold_status extend the check
    beyond the Investing-EN defaults."""
    text = note.read_text(encoding="utf-8", errors="replace")
    if _EMPTY_TODO.search(text):
        return "empty scaffold: distillation placeholder still present"
    if _EMPTY_TYPE.search(text):
        return "empty scaffold: Metadata Type row not filled"
    if SCAFFOLD_STATUS:
        st = meta_status(text)
        if st is not None and _norm_label(st) == _norm_label(SCAFFOLD_STATUS):
            return f"unfinished scaffold: {STATUS_LABEL} still '{st.strip()}' — distill the note"
    return None


def note_status_of(note: Path) -> str:
    txt = note.read_text(encoding="utf-8")
    v = meta_status(txt)
    return v.strip() if v is not None else "no status row"


def _scanned_region(txt: str) -> str:
    """Note text minus exempt sections — the region the U+FFFD guard applies to
    (fidelity tables legitimately document corrupted source characters)."""
    out, exempt = [], False
    for raw in txt.split("\n"):
        s = raw.strip()
        if s.startswith("## "):
            exempt = s[3:].strip().lower() in _EXEMPT_SECTIONS
        if exempt:
            continue
        out.append(raw)
    return "\n".join(out)

# ---------------- reporting ----------------

def report_records(records, src, sess_key, where, verbose=True):
    """Check scanned records against the source; print ✓/✗ per real quote.

    Two lanes (records carry "bq" = evidence blockquote vs inline digest text):
      hard  -> c["fails"]:  evidence-lane violations that gate — minute
               mismatch/not-found, and a blockquote quote with no cite at all
               (an evidence claim that cannot be verified).
      soft  -> c["soft"]:   «…» quotes inside digest prose (خلاصة هضم etc.)
               without a cite — stylistic quoting in the writer's own summary;
               printed as ⚠ but NOT gating.
    Returns {fails, soft, checked, labels, uncited, uncited_inline, mismatch,
    missing, quoted}."""
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
        verdict, vmsg = check_quote(src, q, rec["secs"], where, rec["key"])
        if verdict is None:
            continue
        if verdict == "OK":
            if verbose and (q, tuple(rec["secs"])) not in seen_ok:
                seen_ok.add((q, tuple(rec["secs"])))
                print(f'  ✓ "{disp}" {fmt_cite(rec["key"], rec["secs"])}')
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
    try:
        return str(p.resolve().relative_to(base.resolve()))
    except ValueError:
        return str(p)


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

