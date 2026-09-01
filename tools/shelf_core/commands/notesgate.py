#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""notesgate — B3 port of scripts/notes-gate.py as a registry command (`shelf notes-gate`).

GATE per-note (pins + contamination + empty-scaffold + verdict-contradictions). Exit 0 blocker.

Differences from the script (behavior-preserving):
- `import _shelf_lib as lib` → in-package gatelib (B1).
- pins keeps its direct-import primary path; the subprocess fallback only
  engages while a shelf still carries tools/shelf.py (pre-cutover), and its
  provenance print stays (P6.13: never a silent alternate path).
- _verdict_contradictions and _toks ported verbatim (P6.13 15–1000 cap).
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from shelf_core import gatelib as lib

# W4.13: config-driven label/value constants from the parse layer (the one
# source for note-metadata conventions).
from shelf_core.notes import (STATUS_LABEL, STATUS_VALUES,  # noqa: F401
                              parse_note, find_section)  # A5.3(f)


def _toks(s: str) -> list[str]:
    s = re.sub(r"[^\w\s\u0600-\u06FF]", " ", s)
    return [w for w in s.split() if len(w) > 1]


def _verdict_contradictions(text: str) -> list[str]:
    """One text must not carry two verdicts.

    A note states each religious text twice: as a researched prose verdict under نصوص وآثار
    («…quote…» then — التحقق: **STATUS**), and as a row in the "يحتاج مراجعة الشيخ" table
    (| HH:MM | «…quote…» | note | **STATUS** |). They are written at different times, so after a
    verification pass the prose carries the researched verdict while the table still says للشيخ.
    The note then contradicts itself: the reader of the table asks the sheikh about something
    already answered, and the reader of the prose never learns the table exists. Politics had 5.

    Keyed on timecode + near-identical quote. The threshold matters: at 0.55 token overlap the
    detector produced 8 candidates of which 2 were wrong (shared function words, and a header
    that merely lists quotes). At >= 0.95 it produced 8 with 0 false positives.

    P6.13: the quote-length cap is 15-1000 (was 15-220) — long verbatim texts
    (a 4-line hadith passage) were invisible to BOTH lanes, so a stale verdict
    on a long quote never contradicted. CONTROL (per PROTOCOL, a threshold
    change ships its control): the measured 8-candidate set re-run at both caps
    produces the SAME candidate list and the SAME 0 false positives at 0.95
    (recorded in reports/p613-verdict-cap-control.md).
    """
    prose = []
    for m in re.finditer(
        r"(\d{2}:\d{2})[^\n]*\n+\s*>\s*«([^»]{15,1000})»\s*\n+\s*—\s*التحقق:\s*\*\*(متحقق|للشيخ|متنازع)[^*]*\*\*",
        text,
    ):
        prose.append((m.group(1), _toks(m.group(2)), m.group(3)))
    if not prose:
        return []
    out = []
    for m in re.finditer(
        r"\|\s*(\d{2}:\d{2})\s*\|\s*«([^»]{15,1000})»[^|]*\|[^|]*\|\s*\*\*(متحقق|للشيخ|متنازع)\*\*\s*\|",
        text,
    ):
        tc, qt, st = m.group(1), _toks(m.group(2)), m.group(3)
        cands = [p for p in prose if p[0] == tc]
        if not cands:
            continue
        best = max(cands, key=lambda q: len(set(qt) & set(q[1])) / max(1, len(set(qt) | set(q[1]))))
        ov = len(set(qt) & set(best[1])) / max(1, len(set(qt) | set(best[1])))
        if ov >= 0.95 and best[2] != st:
            out.append(
                f"verdict contradiction at {tc}: table row says {st}, the researched prose verdict "
                f"says {best[2]} — one of them is stale (fix the claim site, not just the dossier)"
            )
    return out


def _pins_one(p: Path, root: Path) -> tuple[bool, str]:
    """Direct-import pins with subprocess fallback (verbatim semantics from the script)."""
    pins_ok = False
    pins_err = ""
    _use_subprocess_fallback = False
    try:
        import sys as _sys
        tools_dir = root / "tools"
        if str(tools_dir) not in _sys.path:
            _sys.path.insert(0, str(tools_dir))
        from shelf_core.commands.pins import cmd_pins as _cmd_pins
        import io
        import contextlib
        buf_out, buf_err = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
                _cmd_pins([str(p)])
            pins_ok = True
        except SystemExit as e:
            if e.code == 0 or e.code is None:
                pins_ok = True
            else:
                out = (buf_out.getvalue() + buf_err.getvalue()).strip().splitlines()
                pins_err = out[0] if out else f"exit {e.code}"
        except Exception as e:
            pins_err = str(e).splitlines()[0] if str(e) else type(e).__name__
            _use_subprocess_fallback = True
            raise
    except Exception as _e:
        _use_subprocess_fallback = True
        if not pins_err:
            pins_err = str(_e).splitlines()[0] if str(_e) else type(_e).__name__
    if _use_subprocess_fallback or not pins_ok:
        # Subprocess fallback is the source of truth when import path fails (e.g. missing globals)
        # Only re-run if not already OK
        if not pins_ok:
            shelf_py = root / "tools" / "shelf.py"
            if shelf_py.exists():
                # P6.13 provenance: the fallback is a DIFFERENT execution path —
                # say so next to the verdict, never silently.
                print(f"pins via subprocess fallback ({shelf_py}) — semantics may differ; run sync.sh")
                r = subprocess.run(["python3", str(shelf_py), "pins", str(p)], capture_output=True, text=True)
                if r.returncode == 0:
                    pins_ok = True
                    pins_err = ""
                else:
                    out = (r.stdout + r.stderr).strip().splitlines()
                    # Keep first non-empty line from subprocess as canonical error
                    pins_err = out[0] if out else 'nonzero'
    return pins_ok, pins_err


def cmd_notes_gate(paths):
    argv = list(paths)
    if not argv:
        sys.exit("Usage: shelf notes-gate <note.md> [...]")
    root = lib.find_root()
    config = lib.load_config(root)
    # Resolve notes via lib
    overall = 0
    for target in argv:
        p = Path(target)
        if not p.is_absolute():
            # try relative to root
            cand = root / target
            if cand.exists():
                p = cand
        if not p.exists():
            print(f"GATE FAIL {target}: file not found")
            overall = 1
            continue
        text = p.read_text(encoding="utf-8", errors="replace")

        # A note template is the shape notes are cast from: its Session row is a placeholder, so
        # pins cannot resolve it and every floor would measure a skeleton. Same rule as doc-gate —
        # gating a template teaches authors to pad the template. Exempt by name, loudly.
        if re.search(r"(?:قالب|template|skeleton)", p.name, re.I):
            print(f"GATE PASS {p.name} (template — floors measure notes, not skeletons)")
            continue

        problems: list[str] = []

        # 1. pins — direct import (B3: in-package, no tools/ dependency)
        pins_ok, pins_err = _pins_one(p, root)
        if not pins_ok:
            problems.append(f"pins FAILED ({pins_err or 'nonzero'})")

        # 2. empty-scaffold — W4.13: config-driven labels/values (see script for receipt)
        _draft_status = next(iter(STATUS_VALUES), "draft")
        if len(text.strip()) < 300 or (
                STATUS_LABEL in text and f"| {_draft_status} |" in text):
            if text.count("«") == 0 and text.count('"') == 0:
                problems.append("empty-scaffold (no quotes)")

        # 3. script contamination — Han/Hang always FAIL, Arab in EN fail
        violations = lib.check_allowed_scripts(text, mode="auto", config=config)
        if violations:
            # group by script
            han = [v for v in violations if "Han" in v[2]]
            if han:
                problems.append(f"FOREIGN SCRIPT Han at L{han[0][0]}: {han[0][1]!r} ({len(han)} total)")
            else:
                problems.append(f"FOREIGN SCRIPT {violations[0][2]} at L{violations[0][0]}")

        # 3b. pitfall guards — U+FFFD (I) + header «» (J) — via PITFALLS.md
        for fail in lib.check_pitfall_guards(text, config=config):
            problems.append(f"PITFALL {fail}")

        # 3c. prose verdict vs review-table row must agree (see _verdict_contradictions)
        for msg in _verdict_contradictions(text):
            problems.append(msg)

        # 4. bucket-ref validity — W4.12: DEAD check removed; time-anchoring
        # is owned by pins (check_quote). (PIPELINE.md §5 row updated Phase 8.)

        # 5. review-queue TRIAGE (never blocks) — see script for receipts.
        doc = parse_note(text)
        triage_notes: list[str] = []
        has_nusus = find_section(doc, "نصوص") is not None
        has_masadir = find_section(doc, "مصادر") is not None
        has_alam = "للشيخ" in text or "أعلام للمراجعة" in text
        # Detect religious quote without مصادر row
        if has_nusus and ("قال تعالى" in text or "قال رسول الله" in text):
            # Accepted verification evidence (see references/VERIFICATION.md):
            # quran.com/api.quran.com (verse text), dorar.net (grading),
            # ar.wikisource.org (mother-source text location when dorar is
            # Cloudflare-blocked). An _verify/ dossier path also counts.
            masadir_block = ""
            if has_masadir:
                sec = find_section(doc, "مصادر")
                masadir_block = ("\n".join([f"## {sec['header']}"] +
                                           [ln for _, ln in sec["body"]])) if sec else ""
            verified = any(s in masadir_block for s in (
                "quran.com", "dorar.net", "ar.wikisource.org",
                "api.quran.com", "_verify/"))
            if not verified:
                triage_notes.append(
                    "review-queue: نصوص دينية بلا مصدر محقق — drain per "
                    "references/VERIFICATION.md (quran.com/dorar.net/"
                    "ar.wikisource.org + _verify/ dossier) — TRIAGE")
        if has_nusus and not has_masadir:
            triage_notes.append("review-queue: ## مصادر متحققة فارغ/مفقود — TRIAGE")
        if "أعلام للمراجعة" in text and "| للشيخ |" not in text and "|للشيخ|" not in text:
            # Section exists but no Sheikh rows — still TRIAGE
            triage_notes.append("review-queue: ## أعلام بلا صف | للشيخ | — TRIAGE (drain weekly)")
        # Empty optional sections (قصص/أمانة) — TRIAGE, not GATE
        if "## قصص وأمثلة" in text:
            mm = re.search(r"## قصص وأمثلة.*?(?=\n## |\Z)", text, flags=re.S)
            if mm and len([l for l in mm.group(0).splitlines() if l.strip().startswith("-")]) == 0:
                triage_notes.append("review-queue: ## قصص وأمثلة فارغ — TRIAGE")
        if "## ملاحظات للأمانة" in text:
            mm = re.search(r"## ملاحظات للأمانة.*?(?=\n## |\Z)", text, flags=re.S)
            if mm and "clean" not in mm.group(0) and "سطر" not in mm.group(0):
                triage_notes.append("review-queue: ## أمانة بلا إشارة clean/[MM:SS] — TRIAGE")

        if problems:
            overall = 1
            print(f"GATE FAIL {p.name}:")
            for pr in problems:
                print(f"   - {pr}")
        else:
            print(f"GATE PASS {p.name}")
        if triage_notes:
            print(f"   TRIAGE (review-queue, not blocking — drain weekly if time): " + "; ".join(triage_notes))

    sys.exit(overall)
