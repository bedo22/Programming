#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""commands/draft_note — scripted note builder (absorbed from Politics/is-040 gen040.py).

Uses verified matcher (CleanSource + subseq/_slice_verbatim) not raw.find, so PITFALLS.md A/C/H hold.
Input: MEH.yaml (list of {idx, title, khu, quotes}) or stdin JSON; Output: reference/notes/<key>-*.md via templates/session-note.md header.
"""

from __future__ import annotations
import sys, re, glob, json
from pathlib import Path

try:
    from shelf_core.config import find_root, load_config
    from shelf_core.playlists import parse_session_key, session_key_of, get_session
    from shelf_core.transcript import CleanSource, clean_paragraphs
    from shelf_core.match import tokens, subseq
    from shelf_core.citation import fmt_mmss
except ImportError:
    from config import find_root, load_config  # type: ignore
    from playlists import parse_session_key, session_key_of, get_session  # type: ignore
    from transcript import CleanSource, clean_paragraphs  # type: ignore
    from match import tokens, subseq  # type: ignore
    from citation import fmt_mmss  # type: ignore


def _sess_label() -> str:
    """Metadata row label for the session, from corpus.note_meta.session. It used to be a
    hardcoded Arabic word for "study circle" -- shelf-specific text baked into shared tooling, so
    every new Arabic shelf inherited that one shelf's vocabulary."""
    try:
        from ..config import corpus_cfg as _cc
    except ImportError:
        from config import corpus_cfg as _cc
    _c = _cc() or {}
    return ((_c.get("note_meta") or {}).get("session") or "Session").strip()


def _cite_str(key: str, minute: int) -> str:
    """Cite form for a note being written. The keyword form resolves through key_of_number(),
    which prefixes key_pattern's LITERAL playlist -- valid only for the playlist that owns
    cite_pattern. Any other playlist in the same shelf must carry its own key explicitly, or the
    cite silently points at a DIFFERENT session: writing the primary keyword into a ts- note made
    every quote resolve against is-001, and pins --fix would have "corrected" good minutes to
    wrong ones."""
    try:
        from ..citation import CITE_KEYWORD, kw_cite_allowed
    except ImportError:
        from citation import CITE_KEYWORD, kw_cite_allowed
    mm = fmt_mmss(minute)
    if CITE_KEYWORD and kw_cite_allowed(key):
        num = key.split("-")[-1] if "-" in key else key
        return f"({_sess_label()} {num}، {mm})"
    return f"({key}، {mm})"


def _minute_at(src: CleanSource, qt: str) -> str | None:
    # Use CleanSource's minute buckets via subseq
    qt_toks = tokens(qt)
    if not qt_toks:
        return None
    # Search buckets for qt
    for minute, bucket_toks in sorted(src.buckets.items()):
        if subseq(qt_toks, bucket_toks):
            # minute is already MM:SS string from bucket key
            return minute
    return None


def cmd_draft_note(argv):
    if not argv:
        sys.exit("usage: python3 tools/shelf.py draft-note <key> [--from-yaml MEH.yaml] [--from-json -]")
    key_arg = argv[0]
    # Parse key
    slug, ident = parse_session_key(key_arg)
    key = session_key_of(slug, ident)
    rec = get_session(key)
    # Determine input source
    yaml_path = None
    json_input = False
    if "--from-yaml" in argv:
        idx = argv.index("--from-yaml")
        if idx + 1 < len(argv):
            yaml_path = Path(argv[idx+1])
    if "--from-json" in argv:
        json_input = True

    # Load MEH data
    meh = []
    if yaml_path and yaml_path.exists():
        try:
            import yaml  # type: ignore
            data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
        except Exception as e:
            sys.exit(f"Failed to load YAML {yaml_path}: {e}")
        # Accept BOTH documented forms: top-level "meh:" key (templates/MEH.yaml)
        # and a bare list. A dict without "meh" is a user error — fail loudly
        # (a silent 0-item parse previously wrote a skeleton note, exit 0).
        if isinstance(data, dict):
            meh = data.get("meh") or []
            if not meh:
                sys.exit("MEH parsed to 0 items: YAML is a dict without a "
                         "non-empty top-level 'meh:' key (see templates/MEH.yaml)")
        else:
            meh = data or []
    elif json_input or not sys.stdin.isatty():
        try:
            meh = json.load(sys.stdin)
        except Exception:
            # Try to read as text
            pass
    else:
        sys.exit("No MEH input: provide --from-yaml MEH.yaml or pipe JSON")
    if not meh:
        sys.exit("MEH parsed to 0 items — refusing to write a skeleton note")

    # Normalize MEH: expect list of {idx, title, khu, quotes} or tuple
    normalized = []
    for item in meh:
        if isinstance(item, (list, tuple)) and len(item) == 4:
            idx, title, khu, quotes = item
            normalized.append((idx, title, khu, quotes))
        elif isinstance(item, dict):
            normalized.append((item.get("idx"), item.get("title"), item.get("khu"), item.get("quotes", [])))
        else:
            continue

    # Determine output path via templates/session-note.md
    root = find_root()
    # Find existing note or create new
    g = glob.glob(str(root / f"reference/notes/{key}*"))
    if g:
        out_path = Path(g[0])
    else:
        # Use transcripts clean filename to derive
        if rec and rec.get("rel"):
            base = Path(rec["rel"]).stem
            base = re.sub(r"^\d+\s*-\s*", "", base).replace(".ar-orig", "")
            out_path = root / f"reference/notes/{key}-{base}.md"
        else:
            out_path = root / f"reference/notes/{key}-draft.md"

    # Build note
    src = CleanSource(key) if rec else None
    paras = clean_paragraphs(key) if rec else None

    out_lines = []
    # Header via template (simplified)
    out_lines.append(f"# ملاحظة جلسة {key} — {normalized[0][1] if normalized else ''}")
    out_lines.append("")
    out_lines.append("> **ملاحظة التقطير** (طبقة المشتقات) — كل اقتباس حرفي من الأصل مع دقيقته. لا تُعدَّل النصوص الأصلية أبدًا.")
    out_lines.append("")
    out_lines.append("## بيانات")
    out_lines.append("")
    out_lines.append("| الحقل | القيمة |")
    out_lines.append("|---|---|")
    out_lines.append(f"| الملف المصدر | `{rec['rel'] if rec else ''}` |")
    out_lines.append(f"| {_sess_label()} | {key} |")
    out_lines.append("| حالة الملاحظة | مسودة |")
    out_lines.append("| أعلام محالة للشيخ | لا |")
    out_lines.append("")

    fails = []
    for idx, title, khu, quotes in normalized:
        out_lines.append(f"### المحور {idx}: {title}")
        out_lines.append(f"- خلاصة (هضم) — {khu}")
        for q in quotes:
            minute = None
            if src:
                minute = _minute_at(src, q)
            if minute:
                out_lines.append(f'- اقتباس حرفي: > «{q}» {_cite_str(key, minute)}')
            else:
                # Try fallback via paras
                if paras:
                    for m, para_toks in paras.items():
                        if subseq(tokens(q), para_toks if isinstance(para_toks, list) else tokens(para_toks)):
                            minute = m
                            break
                if minute:
                    out_lines.append(f'- اقتباس حرفي: > «{q}» {_cite_str(key, minute)}')
                else:
                    fails.append((idx, q))
                    out_lines.append(f'- اقتباس حرفي: > «{q}» **FAIL** (لم يُعثر في clean — PITFALLS.md A/C)')
        out_lines.append("")

    # Trailing template sections: without these the note fails the gate
    # (metadata row, أعلام, مصادر) and the review-queue has nothing to read.
    num = key.split("-")[-1] if "-" in key else key
    out_lines.append("## نصوص وآثار")
    out_lines.append("")
    out_lines.append("(لا نصوص دينية مُحصَّلة آليًا — أضفها من الأصل مع الاستشهاد المزدوج.)")
    out_lines.append("")
    out_lines.append("## أعلام للمراجعة (للشيخ / للمراجع)")
    out_lines.append("")
    out_lines.append("| الموضع | النص الحرفي | الملاحظة | يُحال إلى |")
    out_lines.append("|---|---|---|---|")
    out_lines.append("| — | — | (أضف الشكوك هنا أثناء المراجعة) | للشيخ |")
    out_lines.append("")
    out_lines.append("## مصادر متحققة")
    out_lines.append("")
    out_lines.append("- (كل نص ديني في «نصوص وآثار» يُربط هنا أو يُحال للشيخ.)")
    out_lines.append("")
    out_lines.append("## ملاحظات للأمانة")
    out_lines.append("")
    out_lines.append("> **دفتر ملاحظات الأمانة:** كل خطأ نسخ/تعريف صوتي مُشتبه به يُسجَّل هنا بمؤشّر دقيق.")
    out_lines.append("")

    # Write
    out_path.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"BUILT -> {out_path} ({len(normalized)} محاور)")
    if fails:
        print(f"fails: {len(fails)}")
        for idx, q in fails:
            print(f"  FAIL محور {idx}: {q[:60]}")
        sys.exit(1)
    else:
        print("All quotes located — run: python3 tools/shelf.py pins {} && python3 scripts/notes-gate.py {}".format(out_path, out_path))
