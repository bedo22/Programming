#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""buildmeh — B6 port of scripts/build_meh.py as a registry command
(`shelf build-meh <session-key> <agent-json> <out-yaml>`).

Build a MEH.yaml from an agent's structured reading of one lecture.

Division of labour is deliberate: the agent supplies JUDGMENT (which محاور the lecture has, their
titles, a one-sentence هضم each, and WHERE each quote sits: minute + an exact start phrase). This
command supplies the QUOTE TEXT by slicing the transcript itself, so a quote can never be
paraphrased, re-vowelled, or "corrected" into a gate failure. Every string that ends up inside
«…» is an exact substring of the source by construction, and that is asserted here before
anything is written.

The transcript location is resolved through shelf_core (corpus config -> playlist -> clean dir),
NOT by a path baked into this file. The first version hardcoded one shelf's playlist directory,
and the moment it was reused it pointed at `transcripts/clean/clean` and reported "no transcript"
for a file that was sitting right there.

Differences from the script: ROOT was `Path(__file__).parents[1]` — module-location, the exact
bug class the lazy-ROOT wave killed — now find_root() (cwd-walk). argv comes from the dispatch
(sys.argv[2:]) instead of sys.argv[1:].
"""
import json
import re
import sys
import pathlib

# P6.7: import at the top so a missing PyYAML fails BEFORE any transcript
# resolution or slicing work, not after minutes of it.
import yaml

from shelf_core import gatelib as lib

MIN_WORDS, MAX_WORDS = 6, 16   # shelf convention: median 9, p90 18 across 4,815 existing quotes


def _resolve_transcript(key: str, ROOT) -> pathlib.Path:
    """Find the clean transcript for a session key, via the shelf's own config."""
    try:
        from shelf_core.playlists import parse_session_key, clean_dir, get_session
        from shelf_core.config import ROOT as _R
        rec = get_session(key)
        if rec and rec.get("rel"):
            f = pathlib.Path(_R) / rec["rel"]
            if f.exists():
                return f
        slug, ident = parse_session_key(key)
        d = clean_dir(slug)
        if d and d.exists():
            # W4.6(b): the loose `*{ident}*` fallback is dropped — a transcript
            # named "other-006-something.txt" matched for ts-006. Precision only.
            hits = sorted(d.glob(f"{int(ident):03d}*.txt"))
            if hits:
                return hits[0]
    except Exception as e:                                   # noqa: BLE001 - fall through to glob
        print(f"  (shelf_core resolution unavailable: {e})", file=sys.stderr)
    num = re.search(r"(\d+)", key)
    if num:
        for d in sorted((ROOT / "transcripts").glob("*/clean")) + [ROOT / "transcripts"]:
            if d.exists():
                hits = sorted(d.glob(f"{int(num.group(1)):03d}*.txt"))
                if hits:
                    return hits[0]
    sys.exit(f"no clean transcript resolves for session key {key!r}")


def _segments(path):
    """{ 'MM:SS': text } in file order. Markers are standalone lines in this corpus.
    P6.7: accepts \\d{1,3} minutes and an optional :SS tail (HH:MM:SS labels) —
    the old strict MM:SS silently dropped every segment past 99:59 or with seconds."""
    txt = path.read_text(encoding="utf-8", errors="replace")
    parts = re.split(r"\n?\[(\d{1,3}:\d{2}(?::\d{2})?)\]\n?", txt)
    out = {}
    for i in range(1, len(parts) - 1, 2):
        body = (parts[i + 1] or "").strip()
        if body:
            out.setdefault(parts[i], []).append(body)
    return {k: " ".join(v) for k, v in out.items()}


def _plain(s: str) -> str:
    """Strip «»/‹› from a title or digest. Those marks are load-bearing notation in this shelf --
    'these exact words were spoken, at the cited minute' -- and the gate requires each one on a
    line carrying a minute (PITFALL HEADER QUOTE). Reading agents reach for them as ordinary
    quotation, so the phrase is kept and the markup dropped here rather than trusting the rule."""
    for ch in "«»‹›":
        s = s.replace(ch, "")
    return re.sub(r"\s+", " ", s).strip()


def cmd_build_meh(argv):
    if len(argv) < 3:
        sys.exit("Usage: shelf build-meh <session-key> <agent-json> <out-yaml>   e.g. ts-004")
    key, aj, out = argv[0], argv[1], argv[2]
    ROOT = lib.find_root()
    # A bare number is ambiguous on a multi-playlist shelf: "006" exists in both playlists here,
    # and the resolver only picked the right one because a fallback glob happened to sort that
    # way. Force the unambiguous form instead of relying on ordering — UNLESS the shelf's own
    # config declares a PREFIXLESS default playlist (T9.1/ADR 0007: key_prefix ''), in which
    # case the bare-NNN form IS the canonical key.
    if not re.fullmatch(r"[A-Za-z]{2,4}-\d{2,4}", key):
        _bare_ok = False
        try:
            from shelf_core.playlists import DEFAULT_PLAYLIST, KEY_PREFIXES
            _bare_ok = KEY_PREFIXES.get(DEFAULT_PLAYLIST, DEFAULT_PLAYLIST + "-") == ""
        except Exception:
            _bare_ok = False
        if not (_bare_ok and re.fullmatch(r"\d{1,3}", key)):
            sys.exit(f"session key must look like ts-006 (playlist prefix + number), got {key!r}")
    f = _resolve_transcript(key, ROOT)
    S = _segments(f)
    spec = json.loads(pathlib.Path(aj).read_text(encoding="utf-8"))
    raw = f.read_text(encoding="utf-8", errors="replace")

    axes, problems, notes = [], [], []

    # P6.7: ONE-PASS spec-shape validation — every shape problem is reported
    # together (a missing title used to KeyError after the transcript work, and
    # a missing axes list exited before the operator learned anything else).
    shape_problems = []
    if not isinstance(spec, dict):
        shape_problems.append("spec is not a JSON object")
        spec = {}
    if not spec.get("title"):
        shape_problems.append("spec: missing 'title'")
    if not (spec.get("axes") or []):
        shape_problems.append("spec: missing 'axes' (no axes to build)")
    for a in (spec.get("axes") or []):
        if not isinstance(a, dict):
            shape_problems.append(f"spec axes entry is not an object: {a!r}")
        else:
            for fld in ("title", "khu"):
                if not a.get(fld):
                    shape_problems.append(f"spec axis {a.get('minute', '?')}: missing {fld!r}")
    if shape_problems:
        print(json.dumps({"session": key, "ok": False, "axes": 0,
                          "problems": shape_problems}))
        sys.exit(1)

    for i, a in enumerate(spec.get("axes") or [], 1):
        ts, phrase, ln = a.get("minute"), (a.get("start_phrase") or "").strip(), int(a.get("words", 11))
        ln = max(MIN_WORDS, min(MAX_WORDS, ln))
        body = S.get(ts)
        if not body:
            problems.append(f"axis {i}: minute {ts} is not a marker in this file")
            continue
        if not phrase:
            problems.append(f"axis {i}: no start_phrase")
            continue
        w = body.split()
        # locate the phrase by its own word list, so spacing variants in the agent's JSON cannot
        # produce a near-miss: the phrase's words must appear consecutively in this segment.
        pw = phrase.split()
        off = next((j for j in range(len(w) - len(pw) + 1) if w[j:j + len(pw)] == pw), -1)
        if off < 0:
            problems.append(f"axis {i}: start_phrase {phrase[:34]!r} not found in segment {ts}")
            continue
        quote = " ".join(w[off:off + ln])
        # P6.7: the substring assertion compares against WHITESPACE-NORMALIZED
        # raw text — the slice's words come verbatim from the segment, but the
        # raw file may separate them with newlines/multiple spaces (a line-wrap
        # inside the quoted run made the strict assertion fail falsely). Safe
        # direction stays safe: only whitespace varies, never the words.
        raw_n = re.sub(r"\s+", " ", raw)
        if re.sub(r"\s+", " ", quote) not in raw_n:   # construction guarantee, not trust
            problems.append(f"axis {i}: slice is not a substring of the transcript")
            continue
        # A bracketed tag is NOT SPEECH. This corpus carries [موسيقى] / [تصفيق] / [ضحك] INLINE
        # inside a segment body, not only on their own lines, so a slice that crosses one ships a
        # quote containing text nobody said -- and it stays a verbatim substring, so every existing
        # check passes. Found by a reading agent on ts-014, where the chosen anchor's 12-word slice
        # swallowed a [موسيقى] tag and the builder accepted it silently.
        tag = re.search(r"\[[^\]]{1,24}\]", quote)
        if tag:
            trimmed = quote[:tag.start()].strip()
            if len(trimmed.split()) >= MIN_WORDS:
                notes.append(f"axis {i}: slice trimmed at a non-speech tag "
                             f"{tag.group(0)!r} ({len(quote.split())} -> {len(trimmed.split())} words)")
                quote = trimmed
            else:
                problems.append(f"axis {i}: slice hits a non-speech tag {tag.group(0)!r} with only "
                                f"{len(trimmed.split())} usable words before it — choose an anchor "
                                f"whose run of speech is clean")
                continue
        if len(quote.split()) < MIN_WORDS:
            problems.append(f"axis {i}: only {len(quote.split())} words — too short to cite")
            continue
        for fld in ("title", "khu"):
            if any(c in str(a.get(fld, "")) for c in "«»‹›"):
                notes.append(f"axis {i}: quote-markup stripped from {fld}")
        axes.append({"idx": len(axes) + 1, "title": _plain(a["title"]), "khu": _plain(a["khu"]),
                     "quotes": [quote]})

    # Validate the minutes in the OPTIONAL sections too. The axes are checked because their quotes
    # are sliced from the segment, but qisas/nusus carry only a minute -- and an invented or drifted
    # minute there is invisible to every downstream gate. A reading agent caught this by hand and
    # reported it; it should not depend on the agent's diligence.
    bad_minutes = []
    for sect in ("qisas", "nusus", "asila", "masadir", "amana"):
        for j, item in enumerate(spec.get(sect) or []):
            m = item.get("minute") if isinstance(item, dict) else None
            if m is None:
                continue
            if m not in S:
                bad_minutes.append(f"{sect}[{j+1}]: minute {m} is not a marker in this file")
    if bad_minutes:
        problems.extend(bad_minutes)

    if not axes:
        print(json.dumps({"session": key, "ok": False, "axes": 0, "problems": problems}))
        sys.exit(1)

    doc = {"meh": axes,
           "qisas": spec.get("qisas") or [],
           "nusus": spec.get("nusus") or [],
           "asila": spec.get("asila") or [],
           "masadir": spec.get("masadir") or [],
           "amana": spec.get("amana") or [],
           "alam": spec.get("alam") or []}
    p = pathlib.Path(out); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False), encoding="utf-8")
    # W4.6(a): partial builds are REAL — the file is written (a partial draft
    # beats no draft) but the exit is nonzero and the JSON says partial:true,
    # so a caller cannot mistake it for a clean build. W4.6(c): provenance.
    print(json.dumps({"session": key, "ok": True, "partial": bool(problems),
                      "source": str(f), "axes": len(axes),
                      "words": [len(a["quotes"][0].split()) for a in axes],
                      "problems": problems, "notes": sorted(set(notes)),
                      "bad_minutes": [x for x in problems if "is not a marker" in x]},
                     ensure_ascii=False))
    sys.exit(1 if problems else 0)
