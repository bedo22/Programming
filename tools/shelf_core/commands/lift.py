#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""commands/lift — moved from _legacy.py (batch)."""
from __future__ import annotations
import sys, re
from pathlib import Path
try:
    from shelf_core.playlists import *
    from shelf_core.transcript import *
    from shelf_core.notes import *
    from shelf_core.notes import _EXEMPT_SECTIONS  # underscore not exported by *
    from shelf_core.citation import *
    from shelf_core.match import tokens, subseq
    from shelf_core.transcript import _slice_verbatim
    from shelf_core.config import ROOT, REF
    from shelf_core.citation import *
except ImportError:
    from playlists import *  # type: ignore
    from transcript import *  # type: ignore
    from notes import *  # type: ignore
    try:
        from notes import _EXEMPT_SECTIONS  # type: ignore
    except ImportError:
        pass
    from citation import *  # type: ignore
    from match import tokens, subseq  # type: ignore
    from transcript import _slice_verbatim  # type: ignore
    from config import ROOT, REF  # type: ignore
def cmd_lift(argv):
    """Turn candidate phrases (stdin, one per line) into paste-ready units:
        "verbatim span from the transcript" — (KEY, MM:SS)
    The tool supplies exact text and minute; you select among outputs."""
    if not argv:
        sys.exit("usage: python3 tools/shelf.py lift KEY  (phrases on stdin)")
    slug, ident = parse_session_key(argv[0])
    key = session_key_of(slug, ident)
    paras = clean_paragraphs(key)
    if paras is None:
        sys.exit(f"No clean transcript for session {key}")
    n_ok = n_nf = 0
    for line in sys.stdin:
        p = line.strip()
        if not p:
            continue
        qt = tokens(p)
        if len(qt) < 3:
            print(f"  SKIP(short): {p[:50]}")
            continue
        hit = None
        for m in sorted(paras):
            if subseq(qt, tokens(paras[m]), gap_r=0.85, miss_r=0.30):
                hit = m
                break
        if hit is None and len(qt) >= 6:   # fallback: first 8 tokens
            head = qt[:min(8, len(qt))]
            for m in sorted(paras):
                if subseq(head, tokens(paras[m]), gap_r=1.0, miss_r=0.0):
                    hit = m
                    break
        if hit is None:
            print(f"  NOTFOUND: {p[:60]}")
            n_nf += 1
            continue
        span = _slice_verbatim(paras[hit], qt)
        if span is None:   # phrase straddling a minute boundary — try neighbors
            for m2 in (hit - 1, hit + 1):
                if m2 in paras:
                    span = _slice_verbatim(paras[m2], qt)
                    if span is not None:
                        hit = m2
                        break
        if span is None:
            print(f"  NOSLICE @{fmt_mmss(hit)}: {p[:60]}  "
                  "(a word of the phrase is not in the transcript — fix the phrase)")
            n_nf += 1
            continue
        print(f'"{span}" — ({key}, {fmt_mmss(hit)})')
        n_ok += 1
    print(f"\nResult: {n_ok} lifted, {n_nf} unusable.")


def _pair_line_events(s):
    """Quote/cite pairing for one line -> [(quote_match, cite_match_or_None)].
    Offsets refer to `s` exactly as given."""
    events = []
    for qm in QUOTE_RE.finditer(s):
        events.append((qm.start(), "q", qm))
    for cm in CITE_RE.finditer(s):
        events.append((cm.start(), "c", cm))
    events.sort(key=lambda ev: ev[0])
    pairs = []
    for i, (pos, kind, m) in enumerate(events):
        if kind != "q":
            continue
        nxt_q = next((p for p, k, _ in events[i + 1:] if k == "q"), len(s))
        cite = next((mm for p, k, mm in events[i + 1:] if k == "c" and p < nxt_q),
                    None)
        pairs.append((m, cite))
    return pairs


def _annotation_offset_map(raw: str):
    """Map offsets of the annotation-stripped line back onto the raw line."""
    pos = []
    i = 0
    while i < len(raw):
        if raw[i] == "[":
            j = raw.find("]", i)
            if j != -1:
                i = j + 1
                pos.append(min(i, len(raw) - 1))   # collapsed slot
                continue
        pos.append(i)
        i += 1
    return pos


def _minute_range(fm, secs):
    """Corrected minute range: true occurrences nearest the cited ones."""
    closest = min(fm, key=lambda x: min(abs(x - m) for m in secs))
    spread = sorted(x for x in set(fm) if abs(x - closest) <= 1) or [closest]
    return fmt_mmss(spread[0]) + (
        f"–{fmt_mmss(spread[-1])}" if spread[-1] != spread[0] else "")


_MINUTE_TAIL = re.compile(r"\s*[و\-–—]\s*\d{1,2}:\d{2}")


def _swallow_minute_tails(target: str, te: int) -> int:
    """Extend te across trailing dual-minute tails (" و00:27" / "-00:27").
    fix_note fires only on MISMATCH — every cited minute was wrong — so the
    corrected range must replace all of them (else "00:27 و00:27" remains)."""
    while True:
        mt = _MINUTE_TAIL.match(target, te)
        if not mt:
            return te
        te = mt.end()


def fix_note(note: Path) -> int:
    """Rewrite wrong-minute cites where the quote is verbatim elsewhere in the
    same transcript. Covers both grammars scan_lines pairs: the same-line form
    (quote + cite on one line) and the نصوص blockquote-carry form (cite on the
    item line above a "> «quote»" line). Prints each edit; returns fix count."""
    txt = note.read_text(encoding="utf-8")
    sess_key = note_source_key(txt, note)
    if sess_key is None:
        print("✗ cannot fix: no resolvable Session key in the note metadata")
        return 0
    src = CleanSource(sess_key)
    lines = txt.split("\n")
    edits = []   # (line_idx, start, end, replacement, description)
    carry = None  # (line_idx, target_str, cite_match) — last item-line cite
    exempt = False
    for li, raw in enumerate(lines):
        s = raw.strip()
        if s.startswith("#"):
            if s.startswith("## "):
                exempt = header_is_exempt(s[3:].strip())
            continue
        if exempt:
            continue
        stripped = re.sub(r"\[[^\]]*\]", "", raw)
        if stripped == raw:
            target = raw                       # offsets already raw
        else:
            target = stripped                  # remap through the offset map
        is_bq = s.startswith(">")
        pairs = _pair_line_events(target)
        for qm, cm in pairs:
            if cm is None:
                continue
            qt = tokens(qm.group(1))
            if len(qt) < QUOTE_MIN_TOKENS:
                continue
            _ckey, secs = cite_match_parts(cm)
            if _ckey is None or not secs:
                continue
            verdict, _ = check_quote(src, qm.group(1), secs, "fix", sess_key)
            if verdict != "MISMATCH":
                continue
            fm = found_minutes(sess_key, qt)
            if not fm:
                continue
            rng = _minute_range(fm, secs)
            # Preserve the original cite form (paren vs keyword) in the rewrite,
            # and swallow wrapper parens around a keyword cite "(المجلس N، MM:SS)"
            # so the replacement doesn't leave "((" double parens.
            ts, te = cm.start(), cm.end()
            wrapped = (ts > 0 and te < len(target)
                       and target[ts - 1] == "(" and target[te] == ")")
            if cm.group(1) is not None:          # paren form (KEY, MM:SS)
                new_cite = f"({sess_key}, {rng})"
            elif kw_cite_allowed(sess_key):       # keyword form المجلس N، MM:SS
                num = sess_key.split("-")[-1]
                inner = f"{CITE_KEYWORD, kw_cite_allowed} {num}، {rng}"
                new_cite = f"({inner})" if wrapped else inner
                if wrapped:
                    ts -= 1
                    te += 1
            else:
                # A playlist that does not own cite_pattern keeps the explicit key form.
                new_cite = f"({sess_key}, {rng})"
            te = _swallow_minute_tails(target, te)
            if target is raw:
                cs, ce = ts, te
            else:
                base = _annotation_offset_map(raw)
                cs, ce = base[ts], base[te - 1] + 1
            edits.append((li, cs, ce, new_cite,
                          f'"{qm.group(1)[:40]}…" {cm.group(0)} → {new_cite}'))
        # نصوص blockquote-carry form: a "> «quote»" line with no same-line cite
        # takes the item-line cite above it. scan_lines pairs it that way — a
        # same-line-only fixer would silently skip these notes.
        if is_bq and carry is not None:
            _cl, _ctarget, _ccm = carry
            for qm, cm in pairs:
                if cm is not None:
                    continue
                qt = tokens(qm.group(1))
                if len(qt) < QUOTE_MIN_TOKENS:
                    continue
                _ckey, secs = cite_match_parts(_ccm)
                if _ckey is None or not secs:
                    continue
                verdict, _ = check_quote(src, qm.group(1), secs, "fix", sess_key)
                if verdict != "MISMATCH":
                    continue
                fm = found_minutes(sess_key, qt)
                if not fm:
                    continue
                rng = _minute_range(fm, secs)
                if kw_cite_allowed(_ckey):
                    num = _ckey.split("-")[-1]
                    new_cite = f"{CITE_KEYWORD} {num}، {rng}"
                else:
                    new_cite = f"({_ckey}, {rng})"
                ts = _ccm.start()
                te = _swallow_minute_tails(_ctarget, _ccm.end())
                if _ctarget is lines[_cl]:
                    cs, ce = ts, te
                else:
                    base = _annotation_offset_map(lines[_cl])
                    cs, ce = base[ts], base[te - 1] + 1
                edits.append((_cl, cs, ce, new_cite,
                              f'"{qm.group(1)[:40]}…" (carry) '
                              f'{_ccm.group(0)} → {new_cite}'))
        # Carry bookkeeping mirrors scan_lines: a line with a cite refreshes it;
        # a non-blockquote line without one resets it (new item).
        line_cites = list(CITE_RE.finditer(target))
        if line_cites:
            carry = (li, target, line_cites[-1])
        elif not is_bq:
            carry = None
    if not edits:
        return 0
    by_line = {}
    for li, cs, ce, new_cite, desc in edits:
        by_line.setdefault(li, []).append((cs, ce, new_cite, desc))
    n = 0
    for li, subs in by_line.items():
        for cs, ce, new_cite, desc in sorted(subs, key=lambda e: -e[0]):
            lines[li] = lines[li][:cs] + new_cite + lines[li][ce:]
            print(f"  ✎ line {li + 1}: {desc}")
            n += 1
    note.write_text("\n".join(lines), encoding="utf-8")
    return n


