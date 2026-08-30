#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""commands/scaffold — moved from _legacy.py (batch)."""
from __future__ import annotations
import sys, re
from pathlib import Path
try:
    from shelf_core.playlists import *
    # star-import skips underscore names — pull explicitly (doc-branch needs them)
    from shelf_core.playlists import _slug_title
    from shelf_core.commands.pins import _template, _scaffold_note
    from shelf_core.notes import _asset_prefix
    from shelf_core.transcript import *
    from shelf_core.notes import *
    from shelf_core.citation import *
    from shelf_core.match import tokens, subseq
    from shelf_core.config import ROOT, REF
    from shelf_core.citation import *
except ImportError:
    from playlists import *  # type: ignore
    from playlists import _slug_title  # type: ignore
    from pins import _template, _scaffold_note  # type: ignore
    from notes import _asset_prefix  # type: ignore
    from transcript import *  # type: ignore
    from notes import *  # type: ignore
    from citation import *  # type: ignore
    from match import tokens, subseq  # type: ignore
    from config import ROOT, REF  # type: ignore
def cmd_scaffold(argv):
    # scaffold --from-yaml shim → dispatch to draft-note (same verified matcher)
    if "--from-yaml" in argv:
        try:
            from shelf_core.commands.draft_note import cmd_draft_note
        except ImportError:
            from commands.draft_note import cmd_draft_note  # type: ignore
        # scaffold is-040 --from-yaml MEH.yaml  →  draft-note is-040 --from-yaml MEH.yaml
        # Keep template as spec: draft-note already stamps templates/session-note.md sections
        return cmd_draft_note(argv)
    if not argv:
        sys.exit("usage: scaffold KEY | scaffold A-B | "
                 "scaffold doc KEY [--topics] [TITLE] | "
                 "scaffold KEY --from-yaml MEH.yaml (via draft-note)")
    if re.fullmatch(r"\d{1,3}-\d{1,3}", argv[0]):   # bare range applies to cs
        a, b = (int(x) for x in argv[0].split("-"))
        done = attempted = 0
        for n in range(a, b + 1):
            key = f"cs-{n:03d}"
            if get_session(key) is None:
                continue
            attempted += 1
            done += 1 if _scaffold_note(key) else 0
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
            for sk in keys:
                s_slug, s_ident = parse_session_key(sk)
                s_key = session_key_of(s_slug, s_ident)
                npath = None
                # Find note file via glob reference/notes/<key>-*.md
                import glob as _glob
                hits = _glob.glob(str(REF / f"*/notes/{s_key}-*.md")) + _glob.glob(str(REF / f"notes/{s_key}-*.md"))
                if hits:
                    npath = Path(hits[0])
                if npath and npath.exists():
                    txt = npath.read_text(encoding="utf-8", errors="replace")
                    # Extract Themes / Claims blocks (trimmed 6+2, old aliases tolerated)
                    for hdr in ["## Themes", "## Claims and evidence", "## Sources", "## محاور", "## قصص"]:
                        m = re.search(rf"{re.escape(hdr)}.*?(?=\n## |\Z)", txt, flags=re.S)
                        if m:
                            block = m.group(0).strip()
                            # No truncate — full stitch, bloat ledgered by check/doc-gate essay proxy (quote_share/words/paras)
                            # Tail often holds C7/C8 nuance; 1200-head truncation silently lost it.
                            stitched.append(f"<!-- FROM {s_key}: {hdr} -->")
                            stitched.append(block)
                            stitched.append("")
            # Inject before </main> or append
            if "</main>" in tpl:
                tpl = tpl.replace("</main>", "\n".join(stitched) + "\n</main>")
            else:
                tpl += "\n" + "\n".join(stitched)
        out.write_text(tpl, encoding="utf-8")
        if from_notes_raw:
            print(f"Doc -> {os_rel(out, ROOT)} (auto-stitched from {from_notes_raw}, edit essay arc then verify with `check`)")
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


