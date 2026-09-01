#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""docgate — B2 port of scripts/doc-gate.py as a registry command (`shelf doc-gate`).

doc-gate v2: generic mechanical commit gate, two-tier (GATE/TRIAGE), config-driven.

Reads config/project.yaml (schema in PIPELINE.md §3).
GATE: shelf check, responsibility, neglect, quarantine, essay proxy, script-contamination.
TRIAGE: thin_ratio sessions land on deepening list.

Differences from the script (behavior-preserving):
- config state (KEY_PAT/CITE/EP_* knobs) computed inside cmd_doc_gate, not at
  import — equivalent for the CLI's one-command-per-process shape, and keeps
  selftest's config patching authoritative.
- `subprocess python3 tools/shelf.py check` → in-process cmd_check with output
  capture (returncode semantics preserved; the subprocess remains as fallback
  only while a shelf still carries tools/shelf.py, i.e. pre-cutover).
"""
from __future__ import annotations

import contextlib
import glob
import io
import re
import subprocess
import sys
from pathlib import Path

from shelf_core import gatelib as lib
from shelf_core.notes import html_measure  # A5.7: walker-based doc measurements
from shelf_core.commands.check import cmd_check


def _check_one(path: str) -> int:
    """Return cmd_check's exit code for one file, output captured (discarded —
    the gate prints its own verdict; the script only ever read returncode)."""
    buf_out, buf_err = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
            cmd_check([path])
        return 0
    except SystemExit as e:
        return 0 if e.code in (0, None) else int(e.code or 1)
    except Exception:
        return 1


def cmd_doc_gate(paths):
    if not paths:
        sys.exit("Usage: shelf doc-gate <doc.html> [...]  (default: all reference/**/*.html)")
    ROOT = lib.find_root()
    config = lib.load_config(ROOT)
    corpus = config.get("corpus", {})
    gates = config.get("gates", {})
    triage = config.get("triage", {})

    KEY_PAT = lib.key_pattern(config)
    # W4.15: the splice below must not ADD a capture group (findall would return
    # tuples). Neutralize inner groups exactly as citation._key_nc does.
    KEY_PAT_NC = re.sub(r"\((?!\?)", "(?:", KEY_PAT)
    Q_OPEN, Q_CLOSE = lib.quote_style(config)
    CITE = lib.cite_regex(config)

    QUARANTINE_PAT = gates.get("quarantine", None)
    FLOOR_CFG = gates.get("floor", "auto")
    NEGLECT_RATIO = gates.get("neglect_ratio", 0.10)
    THIN_RATIO = gates.get("thin_ratio", 0.20)
    PROMOTE_THIN = triage.get("promote_to_gate", False)
    EP = gates.get("essay_proxy", {})
    EP_QUOTE_SHARE = EP.get("quote_share", 0.55)
    EP_MIN_WORDS = EP.get("min_words", 1200)
    # The word floor is a LENGTH test wearing a substance label, and it is language-blind. Arabic
    # carries the same content in ~78% of the whitespace tokens — measured across ten EN/AR twins of
    # this shelf (0.74-0.83, median 0.78), including twins that pass comfortably. So a complete,
    # faithful Arabic translation of a passing English doc is pushed to fail a floor it cannot meet
    # without padding. Length parity is already checked where it belongs — the twin battery's ratio
    # band — so the floor is scaled for RTL docs and the adjustment is PRINTED, never silent.
    # Override per project with gates.essay_proxy.ar_ratio (set it to 1.0 to disable).
    EP_AR_RATIO = EP.get("ar_ratio", 0.78)
    EP_MIN_PARAS = EP.get("min_paras", 6)
    # P6.14: the substantive-para char threshold is CONFIGURABLE and shared with
    # evdoc's frame floor — one key (gates.essay_proxy.min_para_chars, default
    # 300 = the retired hardcode inside html_measure), both consumers.
    EP_MIN_PARA_CHARS = EP.get("min_para_chars", 300)

    if paths == ["--all"]:
        paths = sorted(glob.glob(str(ROOT / "reference/**/*.html"), recursive=True))

    def claim_mass(key): return lib.claim_mass(key, ROOT, config)
    def bucket_count(key): return lib.bucket_count(key, ROOT, config)
    def key_from_match(m): return lib.key_from_match(m, KEY_PAT)

    def strip_quotes(txt): return re.sub(r"<blockquote.*?</blockquote>", "", txt, flags=re.S | re.I)

    alldocs = glob.glob(str(ROOT / "reference/**/*.html"), recursive=True)
    cross = {}
    for d in alldocs:
        try:
            t = Path(d).read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for m in CITE.finditer(t):
            k = key_from_match(m)
            if k:
                cross[k] = cross.get(k, 0) + 1

    overall = 0
    for path in paths:
        name = Path(path).name
        problems = []
        triage_notes = []
        txt = Path(path).read_text(encoding="utf-8", errors="replace")

        # A template is the shape documents are cast from: deliberately short, deliberately
        # full of placeholders. Running the essay-proxy floors on it teaches an author to pad
        # the skeleton, which is worse than not gating it. Exempt by name, loudly.
        if re.search(r"(?:قالب|template|skeleton)", name, re.I):
            print(f"GATE PASS {name} (template — floors measure documents, not skeletons)")
            continue

        rc = _check_one(str(path))
        if rc != 0:
            # transition fallback: a shelf that still carries tools/shelf.py re-runs
            # out-of-process so a version-skewed tools/ can't hide behind the import
            shim = ROOT / "tools/shelf.py"
            if shim.exists():
                r = subprocess.run(["python3", str(shim), "check", path], capture_output=True, text=True)
                rc = r.returncode
        if rc != 0:
            problems.append("check FAILED (nonzero)")

        cites = {}
        for m in CITE.finditer(txt):
            k = key_from_match(m)
            if k:
                cites[k] = cites.get(k, 0) + 1
        keys = sorted(cites)

        if keys:
            buckets = [bucket_count(k) or 0 for k in keys]
            avg_b = sum(buckets) / len(buckets) if buckets else 0
            if FLOOR_CFG == "auto":
                floor = 12 if avg_b > 40 else 7
                if not (ROOT / "config/project.yaml").exists():
                    print(f"[calibrate] suggest gates.floor = {floor} (avg {avg_b:.0f} buckets) -> freeze in config/project.yaml")
            else:
                floor = int(FLOOR_CFG)
            uncovered = [k for k in keys if cross.get(k, 0) < floor]
            if uncovered:
                # W4.14 DECISION (recorded): KEEP corpus-sum semantics — `cross`
                # counts cites across ALL docs; the message now says what the
                # number IS (was 'max-cites-any-doc', which described nothing).
                problems.append("responsibility FAIL (corpus-cites < floor %d): %s" % (floor, ", ".join(f"{k}(cross={cross.get(k,0)})" for k in uncovered)))
            for k in keys:
                mass = claim_mass(k)
                if not mass:
                    continue
                ratio = cross.get(k, 0) / mass
                if mass >= 10 and ratio < NEGLECT_RATIO and cross.get(k, 0) < floor:
                    problems.append(f"NEGLECTED: {k}(mass={mass},cross-cites={cross.get(k,0)},ratio={ratio:.0%} < {NEGLECT_RATIO:.0%}, unclaimed)")
                elif mass >= 10 and ratio < THIN_RATIO:
                    triage_notes.append(f"{k}(mass={mass},ratio={ratio:.0%})")

        if QUARANTINE_PAT:
            q = re.findall(QUARANTINE_PAT, txt) or re.findall(r"[Vv]ictory lap is (?:un)?justified", txt)
            if q:
                problems.append(f"QUARANTINE violation: {len(q)} hits for {QUARANTINE_PAT}")

        # script contamination — Han always FAIL, Arab in EN fail
        violations = lib.check_allowed_scripts(txt, mode="auto", config=config)
        if violations:
            han = [v for v in violations if "Han" in v[2]]
            if han:
                problems.append(f"FOREIGN SCRIPT Han at L{han[0][0]} ({len(han)} total)")

        # pitfall guards — U+FFFD (I) + header «» (J)
        for fail in lib.check_pitfall_guards(txt, config=config):
            problems.append(f"PITFALL {fail}")

        if Q_OPEN == "«":
            qspans = re.findall(r"«([^»\n]{10,400})»\s*(?:—|-)?\s*(?:<span class=\"cite\">|\(" + KEY_PAT_NC + ")", txt)
        else:
            qspans = re.findall(r'"([^"\n]{10,400})"\s*(?:—|—|-)?\s*(?:<span class="cite">|\(' + KEY_PAT_NC + ")", txt)
        qwords = sum(len(q.split()) for q in qspans)
        # A5.7: the length/paragraph/definition measurements walk the document
        # with html.parser (style/script bodies never count; nesting-robust).
        # W4.15's regex pre-strip measured the same text except on docs whose
        # style/script bodies contain markup that fooled the tag stripper.
        total_words, paras, defs = html_measure(txt, para_chars=EP_MIN_PARA_CHARS)
        if total_words:
            share = qwords / total_words
            if share > EP_QUOTE_SHARE:
                problems.append(f"quote-word share {share:.0%} > {EP_QUOTE_SHARE:.0%}")
        is_ar = 'dir="rtl"' in txt or '<html lang="ar"' in txt
        floor = max(1, int(round(EP_MIN_WORDS * EP_AR_RATIO))) if is_ar else EP_MIN_WORDS
        if total_words < floor:
            note = f" (AR-scaled from {EP_MIN_WORDS} at measured twin ratio {EP_AR_RATIO})" if is_ar else ""
            problems.append(f"only {total_words} words (below {floor}{note})")
        # The paragraph floor is an ESSAY rule. A reference table cannot satisfy it honestly:
        # politics-glossary carries ~90 definitions of 80-300 chars (2,090 words of content)
        # and scored 2, because no cell reaches 300 chars and the split never saw </td>.
        # So measure the unit the document actually uses — but only when the doc really IS
        # table-dominant (>=20 substantial cells), which a thin doc cannot fake with padding.
        if len(defs) >= 20:
            units, kind = len(paras) + len(defs), "substantive paras+definitions"
        else:
            units, kind = len(paras), "substantive paras"
        if units < EP_MIN_PARAS:
            problems.append(f"only {units} {kind} (need {EP_MIN_PARAS})")

        if triage_notes and PROMOTE_THIN:
            problems.append("TRIAGE->GATE (promote_to_gate): thin " + ", ".join(triage_notes))

        if problems:
            overall = 1
            print(f"GATE FAIL {name}:")
            for p in problems:
                print(f"   - {p}")
        else:
            print(f"GATE PASS {name}")
        if triage_notes and not PROMOTE_THIN:
            print(f"   TRIAGE (deepening list, not blocking): " + ", ".join(triage_notes))
    sys.exit(overall)
