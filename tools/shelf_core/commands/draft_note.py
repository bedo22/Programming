#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""commands/draft_note — scripted note builder (absorbed from Politics/is-040 gen040.py).

Uses verified matcher (CleanSource + subseq/_slice_verbatim) not raw.find, so PITFALLS.md A/C/H hold.
Input: MEH.yaml (list of {idx, title, khu, quotes}) or stdin JSON; Output: reference/notes/<key>-*.md with the header built from shelf_core.notes constants (same grammar the TEMPLATES session-note file encodes — no template file is read here; scaffold.py is the template reader).
"""

from __future__ import annotations
import sys, re, glob, json
from pathlib import Path

# H2.2: flat-layout fallback removed — the package is always a package.
from shelf_core.config import find_root, load_config
from shelf_core.playlists import parse_session_key, session_key_of, get_session
from shelf_core.transcript import CleanSource, clean_paragraphs
# A5.3(g): metadata labels/values resolve through the parse layer's constants.
from shelf_core.notes import (STATUS_LABEL, STATUS_VALUES, SCAFFOLD_STATUS,
                              FLAGS_LABEL, FLAGS_NO)
from shelf_core.match import tokens, subseq
from shelf_core.citation import fmt_mmss


def _sess_label() -> str:
    """Metadata row label for the session, from corpus.note_meta.session. It used to be a
    hardcoded Arabic word for "study circle" -- shelf-specific text baked into shared tooling, so
    every new Arabic shelf inherited that one shelf's vocabulary."""
    from ..config import corpus_cfg as _cc
    _c = _cc() or {}
    return ((_c.get("note_meta") or {}).get("session") or "Session").strip()


def _alam_label() -> str:
    """A5.3(g): the shelf-specific أعلام row label, config-driven
    (corpus.note_meta.alam_label; default = this shelf's Arabic convention —
    the row itself is extra data the gates do not validate)."""
    _c = load_config(find_root()) or {}
    return ((_c.get("corpus", {}) or {}).get("note_meta", {}) or {}).get(
        "alam_label", "أعلام محالة للشيخ").strip()


def _quote_verdict(src, sess_key, body: str, minute) -> str:
    """Ask the gate itself. Returns check_quote's verdict: OK | MISSING | MISMATCH | None.

    Three earlier attempts here did their own presence test -- an orthography-normalising
    substring, then tokens/subseq over the raw file, then CleanSource.present() -- and each one
    disagreed with pins on real notes, because pins decides with check_quote(), which requires the
    quote to occur CONTIGUOUSLY at (or within a minute of) the cited minute, not merely for its
    words to exist somewhere in the file. Recited hadith and verse are exactly the case that
    separates the two: the speaker's words are classical and the ASR is wreckage, so the words are
    all present and the quote is still not there.

    There is no correct second implementation of this decision, so this is not one."""
    if src is None or not body:
        return "MISSING"
    # H2.2: flat fallback removed
    from ..transcript import check_quote
    from ..citation import parse_mmss
    secs = [parse_mmss(minute)] if isinstance(minute, str) else list(minute or [])
    verdict, _msg = check_quote(src, body, secs, "", sess_key)
    return verdict


def _cite_str(key: str, minute: int) -> str:
    """Cite form for a note being written. The keyword form resolves through key_of_number(),
    which prefixes key_pattern's LITERAL playlist -- valid only for the playlist that owns
    cite_pattern. Any other playlist in the same shelf must carry its own key explicitly, or the
    cite silently points at a DIFFERENT session: writing the primary keyword into a ts- note made
    every quote resolve against is-001, and pins --fix would have "corrected" good minutes to
    wrong ones."""
    from ..citation import CITE_KEYWORD, kw_cite_allowed
    if isinstance(minute, str):
        # Two callers, two units: the axis loop passes seconds (an int), the registers carry the
        # transcript's own "MM:SS". fmt_mmss does arithmetic, so a string minute crashed the whole
        # scaffold -- and because the exception escaped after the header was built, the note looked
        # merely unchanged rather than broken. Normalise at the boundary that has to know.
        from ..citation import parse_mmss
        minute = parse_mmss(minute)
    mm = fmt_mmss(minute)
    if CITE_KEYWORD and kw_cite_allowed(key):
        num = key.split("-")[-1] if "-" in key else key
        # T9.1/ADR 0007: corpus.cite_note_form: kw — the fork-era convention on
        # shelves whose doc-coverage scanner (and house style) expects the
        # bare keyword cite «…» — المجلس N، MM:SS with no parentheses. Default
        # (unset) keeps the paren form every other shelf is calibrated on.
        try:
            from ..config import corpus_cfg
            _form = (corpus_cfg() or {}).get("cite_note_form") or ""
        except Exception:
            _form = ""
        if _form == "kw":
            return f"— {CITE_KEYWORD} {num}، {mm}"
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
    # W4.1: --force is the explicit regeneration consent (see refusal below).
    force = "--force" in argv

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
        regs = {}
        if isinstance(data, dict):
            # Everything except 'meh' is a REGISTER: قصص / نصوص / أصائل / مصادر / أمانات / أعلام.
            # These were silently dropped for the whole life of this command -- draft_note read
            # only data["meh"] and threw the rest away, so a reading agent could supply 95 items
            # and the note would render placeholder rows and claim "أعلام محالة للشيخ: لا".
            for _rk in ("qisas", "nusus", "asila", "masadir", "amana", "alam"):
                regs[_rk] = data.get(_rk) or []
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

    # Determine output path (W4.21 {key}-* grammar; header grammar itself
    # comes from shelf_core.notes constants — see module docstring)
    root = find_root()
    # Find existing note or create new
    # W4.21: {key}-* (was {key}* — matched prefixes of other keys)
    g = glob.glob(str(root / f"reference/notes/{key}-*"))
    if g and not force:
        # W4.1: regeneration DISCARDS applied verdicts — mirror of cmd_draft's
        # one-write refusal. The old behavior silently overwrote a note that
        # may carry human-applied verify verdicts.
        sys.exit(f"Already exists: {g[0]} — use --force to regenerate "
                 "(note carries applied verdicts — re-apply from _verify/ after regen)")
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
    # A5.3(g): the status row was the AR literal '| حالة الملاحظة | مسودة |'
    # (unreadable by an EN-configured shelf's gates) and the FLAGS row the
    # gates validate was MISSING entirely — fresh draft_note output failed
    # check. Both rows now come from the parse layer's note_meta resolution,
    # matching the template contract's contract (| Status | draft | /
    # | Flags open | no |) in whatever convention the shelf configures.
    out_lines.append(f"| {STATUS_LABEL} | "
                     f"{SCAFFOLD_STATUS or (STATUS_VALUES[0] if STATUS_VALUES else 'draft')} |")
    out_lines.append(f"| {FLAGS_LABEL} | {FLAGS_NO} |")
    _alam = regs.get("alam") or []
    out_lines.append(f"| {_alam_label()} | {'لا' if not _alam else str(len(_alam))} |")
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

    def _cell(v):
        """A table cell: never break the row, never smuggle markup."""
        return str(v or "").replace("|", "،").replace("\n", " ").strip()

    def _at(item, field="minute"):
        """Cite string for a register item, whatever shape the agent used."""
        if isinstance(item, dict):
            m = item.get(field)
            return _cite_str(key, m) if m else ""
        return ""

    def _txt(item, *fields):
        if isinstance(item, dict):
            for f in fields:
                if item.get(f):
                    return str(item[f]).strip()
            return ""
        return str(item).strip()

    # ## قصص وأمثلة -- the section the gate already expects but this command never emitted.
    _q = regs.get("qisas") or []
    out_lines.append("## قصص وأمثلة")
    out_lines.append("")
    if _q:
        for it in _q:
            name = _txt(it, "title", "name", "text")
            cite = _at(it)
            out_lines.append(f"- **{name}** — {cite}" if cite else f"- **{name}**")
    else:
        out_lines.append("(لم تُسجَّل قصص في طبقة القراءة — أضفها من الأصل.)")
    out_lines.append("")

    # ## نصوص وآثار -- house format: numbered, cite on the label line, quote in a blockquote.
    _n = regs.get("nusus") or []
    out_lines.append("## نصوص وآثار")
    out_lines.append("")
    if _n:
        for i, it in enumerate(_n, 1):
            label = _txt(it, "title", "label")
            cite = _at(it)
            body = _txt(it, "text", "nas") or _txt(it, "title")
            # The register's own convention is `القائل: «النص»` -- an attribution plus the quoted
            # span. Left whole, it renders nested («…«…»») and pins then reads the span from the
            # first « to the next », i.e. it verifies the attribution as if it were the quotation.
            # So split it: the span is what gets tested and quoted, the attribution becomes the label.
            attrib, gloss = "", ""
            # The span is whatever sits inside the agent's own «…»; anything before it is the
            # attribution and anything after is a gloss. Anchoring the match to the END of the
            # string missed the common `القرآن: «…» — قاعدة التفسح` shape and left the whole thing
            # as the "quote", which then nested inside the renderer's own guillemets.
            m = re.search(r"«(.+?)»", body, re.S)
            if m:
                span = m.group(1).strip()
                attrib = body[:m.start()].strip(" -:–")
                gloss = body[m.end():].strip(" -:–")
                body = span
            elif body.startswith("«") and body.endswith("»"):
                body = body[1:-1].strip()
            label = label or attrib or "نص منسوب"
            # «…» is an EVIDENCE claim on this shelf: these exact words, at this minute, present in
            # the transcript. A recited hadith or verse often is NOT -- the speaker quotes from
            # memory in correct classical Arabic while ASR mangles it, and a reading agent that
            # supplies the real text is doing the right thing for the register and the wrong thing
            # for the markup. So check it here rather than trust it: verbatim gets the house
            # "بلفظ ASR" form, everything else is labelled منسوب and gets no guillemets.
            _vv = _quote_verdict(src, key, body, (it.get("minute") if isinstance(it, dict) else None))
            if _vv in ("OK", None):   # None = too short for the gate to judge; it will never flag
                out_lines.append(f"{i}. **{label} — بلفظ ASR** — {cite}:")
                out_lines.append(f"   > «{body}»")
            else:
                out_lines.append(f"{i}. **{label} — منسوب، ليس بلفظ الأصل** — {cite}:")
                # No guillemets at all: a line that declares itself non-verbatim must not contain a
                # quote span, or pins reads it as an evidence claim and flags it -- which is exactly
                # what happened when the agent's own «…» survived into this branch.
                out_lines.append(f"   > {body.replace('«', '').replace('»', '')}")
            note = _txt(it, "note", "hay") or gloss
            if note:
                out_lines.append(f"   — {note}")
            out_lines.append("")
    else:
        out_lines.append("(لا نصوص دينية مُحصَّلة آليًا — أضفها من الأصل مع الاستشهاد المزدوج.)")
        out_lines.append("")

    # ## أعلام للمراجعة -- the للشيخ queue. Plain `للشيخ` (not bold) so the gate sees a real row.
    out_lines.append("## أعلام للمراجعة (للشيخ / للمراجع)")
    out_lines.append("")
    out_lines.append("| الموضع | النص الحرفي | الملاحظة | يُحال إلى |")
    out_lines.append("|---|---|---|---|")
    if _alam:
        for it in _alam:
            note = _txt(it, "note", "m", "text") or str(it)
            body = _txt(it, "quote", "text") if isinstance(it, dict) else ""
            cite = _at(it)
            out_lines.append(f"| {_cell(cite) or '—'} | {_cell('«'+body+'»' if body else '—')} "
                             f"| {_cell(note)} | للشيخ |")
    else:
        out_lines.append("| — | — | (أضف الشكوك هنا أثناء المراجعة) | للشيخ |")
    out_lines.append("")

    # ## مصادر متحققة / أصائل / أمانات
    _ms = regs.get("masadir") or []
    out_lines.append("## مصادر متحققة")
    out_lines.append("")
    if _ms:
        for it in _ms:
            if isinstance(it, dict) and it.get("ref"):
                # A verified source is worth its evidence trail: what the text was, what it turned
                # out to be, where, and which saved lookup says so.
                out_lines.append(f"- **{_txt(it, 'text')}** — {_txt(it, 'verdict') or 'محقق'}: "
                                 f"`{_txt(it, 'ref')}`"
                                 + (f" _(دليل: {_txt(it, 'evidence')})_" if it.get("evidence") else ""))
            else:
                out_lines.append(f"- {_txt(it, 'text', 'src', 'title') or str(it)}")
    else:
        out_lines.append("- (كل نص ديني في «نصوص وآثار» يُربط هنا أو يُحال للشيخ.)")
    out_lines.append("")

    _as = regs.get("asila") or []
    if _as:
        out_lines.append("## أصائل")
        out_lines.append("")
        for it in _as:
            out_lines.append(f"- {_txt(it, 'text', 'title') or str(it)}")
        out_lines.append("")

    out_lines.append("## ملاحظات للأمانة")
    out_lines.append("")
    out_lines.append("> **دفتر ملاحظات الأمانة:** كل خطأ نسخ/تعريف صوتي مُشتبه به يُسجَّل هنا بمؤشّر دقيق.")
    _am = regs.get("amana") or []
    for it in _am:
        cite = _at(it)
        body = _txt(it, "text", "note", "title") or str(it)
        out_lines.append(f"- {body}" + (f" — {cite}" if cite else ""))
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
