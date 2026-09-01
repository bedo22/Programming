#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""commands/scaffold — moved from _legacy.py (batch)."""
from __future__ import annotations
import sys, re
from pathlib import Path
# H2.1/H2.2: explicit imports (tokens/subseq imported but unused here).
from shelf_core.config import REF, ROOT
from shelf_core.citation import CITE_RE, QUOTE_RE
from shelf_core.playlists import (PLAYLIST_NAMES, _slug_title, docs_dir, get_session,
                                  parse_session_key, session_key_of, topics_dir,
                                  DEFAULT_PLAYLIST)
from shelf_core.notes import _asset_prefix, os_rel, find_note, parse_note, STITCH_SECTIONS, _norm_label
from shelf_core.commands.pins import _template, _scaffold_note
def cmd_scaffold(argv):
    # scaffold --from-yaml shim → dispatch to draft-note (same verified matcher)
    if "--from-yaml" in argv:
        # H2.2: flat fallback removed
        from shelf_core.commands.draft_note import cmd_draft_note
        # scaffold is-040 --from-yaml MEH.yaml  →  draft-note is-040 --from-yaml MEH.yaml
        # Keep template as spec: draft-note stamps the section grammar from
        # shelf_core.notes constants (the TEMPLATES session-note file encodes
        # the same grammar — one owner, notes.py; A5.3)
        return cmd_draft_note(argv)
    if not argv:
        sys.exit("usage: scaffold KEY | scaffold A-B | "
                 "scaffold doc KEY [--topics] [TITLE] | "
                 "scaffold KEY --from-yaml MEH.yaml (via draft-note)")
    if re.fullmatch(r"\d{1,3}-\d{1,3}", argv[0]):   # bare range binds to the default playlist
        a, b = (int(x) for x in argv[0].split("-"))
        done = attempted = 0
        for n in range(a, b + 1):
            key = f"{DEFAULT_PLAYLIST}-{n:03d}"
            if get_session(key) is None:
                continue
            attempted += 1
            done += 1 if _scaffold_note(key) else 0
        if not attempted:
            print(f"scope bound to playlist '{DEFAULT_PLAYLIST}' — 0 files matched")
            sys.exit(2)
        print(f"Created {done} of {attempted} note scaffolds "
              "(numbers absent from the corpus skipped)")
        return
    if argv[0] == "doc":
        rest = argv[1:]
        topics = "--topics" in rest
        # --from-notes is auto-stitch mirror of draft-note (topics last step, 3–5×)
        from_notes_raw = None
        for a in list(rest):
            if a.startswith("--from-notes"):
                if "=" in a:
                    from_notes_raw = a.split("=", 1)[1]
                else:
                    idx = rest.index(a)
                    if idx + 1 < len(rest):
                        from_notes_raw = rest[idx + 1]
                        rest.remove(rest[idx + 1])
                rest.remove(a)
                break
        rest = [x for x in rest if x != "--topics"]
        if not rest:
            sys.exit("usage: scaffold doc KEY [--topics] [TITLE] [--from-notes K1,K2,..]")
        slug, ident = parse_session_key(rest[0])
        key = session_key_of(slug, ident)
        rec = get_session(key)
        if rec is None:
            sys.exit(f"No transcript file for session {key}")
        title = rest[1] if len(rest) > 1 else rec["title"]
        dest = topics_dir() if topics else docs_dir(slug)
        dest.mkdir(parents=True, exist_ok=True)
        title_slug = _slug_title(title)
        base = (rec["ident"] if rec["ident"] == title_slug
                else f"{rec['ident']}-{title_slug}")
        out = dest / f"{base}.html"
        if out.exists():
            sys.exit(f"Already exists: {os_rel(out, ROOT)}")
        tpl = _template("topic-doc.html")
        tpl = (tpl.replace("{{ASSET_PREFIX}}", _asset_prefix(dest))
                  .replace("{{TITLE}}", title)
                  .replace("{{KICKER}}", f"{rec['block']} — {PLAYLIST_NAMES[slug]}")
                  .replace("{{SESSION_KEY}}", key)
                  .replace("{{SOURCE_PATH}}", rec["rel"]))
        # Auto-stitch from notes when --from-notes given
        if from_notes_raw:
            keys = [k.strip() for k in from_notes_raw.split(",") if k.strip()]
            stitched = ["<!-- AUTO-STITCHED from notes (edit essay arc, then check) -->", ""]
            _stitched_report, _skipped_report = [], []
            for sk in keys:
                s_slug, s_ident = parse_session_key(sk)
                s_key = session_key_of(s_slug, s_ident)
                npath = None
                # W4.21: note discovery via find_note — the registry-driven,
                # ambiguity-refusing resolver (first-hit glob[0] previously
                # picked silently among duplicates).
                _np = find_note(s_key)
                if _np:
                    npath = Path(_np)
                if npath and npath.exists():
                    # A5.3(c): stitch via NoteDoc sections against the config-
                    # driven vocabulary (note_meta.stitch_sections). The retired
                    # hardcoded list carried five headers and omitted نصوص وآثار.
                    d = parse_note(npath)
                    for vocab in STITCH_SECTIONS:
                        vk = _norm_label(vocab)
                        _hit = False
                        for s in d["sections"]:
                            if not _norm_label(s["header"]).startswith(vk):
                                continue
                            _hit = True
                            block = ("\n".join([f"## {s['header']}"] +
                                               [ln for _, ln in s["body"]])).strip()
                            # No truncate — full stitch, bloat ledgered by check/doc-gate essay proxy (quote_share/words/paras)
                            # Tail often holds C7/C8 nuance; 1200-head truncation silently lost it.
                            stitched.append(f"<!-- FROM {s_key}: {s['header']} -->")
                            stitched.append(block)
                            stitched.append("")
                        # P6.9: a vocabulary entry with no matching section is a
                        # DECISION the operator makes, not a silence.
                        if not _hit:
                            _skipped_report.append(f"{s_key}: no section matching '{vocab}'")
                        else:
                            _stitched_report.append(f"{s_key}: '{vocab}' stitched")
            # Inject before </main> or append
            if "</main>" in tpl:
                tpl = tpl.replace("</main>", "\n".join(stitched) + "\n</main>")
            else:
                tpl += "\n" + "\n".join(stitched)
        out.write_text(tpl, encoding="utf-8")
        if from_notes_raw:
            print(f"Doc -> {os_rel(out, ROOT)} (auto-stitched from {from_notes_raw}, edit essay arc then verify with `check`)")
            # P6.9: what was stitched AND what was skipped by vocabulary
            for r in _stitched_report:
                print(f"  stitched: {r}")
            for r in _skipped_report:
                print(f"  skipped:  {r}")
        else:
            print(f"Doc -> {os_rel(out, ROOT)} (fill sections from the session notes, "
                  "then verify with `check`)")
        if not topics:
            print("Reminder: one topic = one doc. Cross-playlist topic docs live "
                  "in reference/topics/ (pass --topics).")
        return
    slug, ident = parse_session_key(argv[0])
    _scaffold_note(session_key_of(slug, ident))


def _parse_note_definitions(txt: str):
    """Definition entries from '## Definitions and coined terms':
        - **Term** — "verbatim definition" (cs-002, 07:31)
    Returns [{term, quote, cite}]."""
    m = re.search(r"## Definitions and coined terms(.*?)(?=\n## |\Z)", txt, flags=re.S)
    if not m:
        return []
    items = []
    for line in m.group(1).split("\n"):
        s = line.strip()
        dm = re.match(r"^[-*]\s*\*\*(.+?)\*\*\s*[—:-]?\s*(.*)$", s)
        if not dm:
            continue
        rest = dm.group(2)
        qm = QUOTE_RE.search(rest)
        if not qm:
            continue
        cm = CITE_RE.search(rest)
        items.append({"term": dm.group(1).strip(), "quote": qm.group(1).strip(),
                      "cite": cm.group(0) if cm else ""})
    return items


def _parse_note_papers(txt: str):
    m = re.search(r"## Papers cited(.*?)(?=\n## |\Z)", txt, flags=re.S)
    if not m:
        return []
    out = []
    for line in m.group(1).split("\n"):
        s = line.strip()
        if s.startswith(("-", "*")) and len(s) > 2:
            item = re.sub(r"^[-*]\s+", "", s).strip()
            if item.lower() not in ("none", "none yet", "tbd", "-"):
                out.append(item)
    return out


