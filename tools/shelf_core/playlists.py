#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""playlists — moved from helpers.py (final distribution)."""
from __future__ import annotations
import re, sys
from pathlib import Path
# H2.2: plain relative imports — try/except-pass swallowed real import errors;
# citation defines fmt_mmss/parse_mmss itself and the graph is acyclic.
from .config import ROOT, REF, TRANSCRIPTS, corpus_cfg
from .match import norm, tokens, subseq, _token_index
from .citation import fmt_mmss, parse_mmss

# ---- P6.1: the registry is DATA, this file is generic machinery ----
# Investing's corpus facts (playlist names/dirs, extras sessions, aliases,
# duplicates, block structure) moved to the shipped profile
# config/project.yaml.investing; sync.sh copies it into an Investing project
# as config/project.yaml. The keys read below are generic: a shelf is its
# config, not its code. `grep` for a session title or author here must come
# up empty — that is the acceptance.
#
# Shapes (all optional, validated loudly):
#   corpus.playlists          slug -> {dir, name, notes_flat, key_prefix,
#                             transcripts_dir, docs_dir}; the key_pattern slug
#                             auto-registers FLAT unless declared here
#   corpus.default_playlist   bare-NNN keys and unscoped drafts bind to it
#   corpus.cite_playlist      the playlist keyword cites (cite_pattern N) resolve
#                             to; default: key_pattern's literal prefix, else the
#                             unique empty-key_prefix playlist, else the default
#   corpus.listed_sessions    pl -> [[slug, filename], ...] (explicitly listed
#                             playlists, e.g. extras — not numeric scanning)
#   corpus.extra_aliases      alias -> canonical session key
#   corpus.duplicate_sessions duplicate key -> canonical key (one note)
#   corpus.block_membership   pl -> [[name, [nums...]], ...] (non-contiguous)
#   corpus.blocks             pl -> [[lo, hi, name], ...] (mechanical batches)

_PLAYLISTS_CFG: dict = {}
FLAT_PLAYLISTS: set = set()
PLAYLIST_DIRS: dict = {}
PLAYLIST_NAMES: dict = {}
# T9.1 (onboarding, 1.2.0): a playlist's session key = key_prefix + NNN.
# Default stays the P6.1 form (slug + "-") so every existing shelf is
# byte-identical; key_prefix: "" declares PREFIXLESS numeric keys (bare-NNN
# corpora that predate the slug grammar). Valid only on the DEFAULT playlist —
# a non-default empty prefix would make its keys unreachable (bare-NNN binds
# to the default), so registration refuses it loudly.
KEY_PREFIXES: dict = {}
# Per-playlist clean dir (ROOT-relative, e.g. "نص-ألف-باء/clean") — the
# tree-locked TRANSCRIPTS model's single config-gated exception (ADR 0007):
# shelves whose sub-playlist transcripts live at top level, outside
# transcripts/. Absent → the C3.6 derivation below, unchanged.
PLAYLIST_TRANSCRIPTS: dict = {}
EXTRA_ALIASES: dict = {}
DUPLICATE_SESSIONS: dict = {}
LISTED_SESSIONS: dict = {}
BLOCKS: dict = {}
_MEMBER_OF: dict = {}

# C3.2/C3.3: the ONE loader reads (cwd-rooted), corruption is loud, and a
# registration failure is announced — never a silent EN fallback.
try:
    _CORPUS = corpus_cfg() or {}
    for _slug, _e in (_CORPUS.get("playlists") or {}).items():
        if not isinstance(_e, dict) or not str(_slug).strip():
            continue
        _s = str(_slug).lower()
        _PLAYLISTS_CFG[_s] = _e
        PLAYLIST_DIRS[_s] = str(_e.get("dir") or _s)
        PLAYLIST_NAMES[_s] = str(_e.get("name") or _s)
        KEY_PREFIXES[_s] = str(_e.get("key_prefix", _s + "-"))
        _ptd = str(_e.get("transcripts_dir") or "").strip()
        if _ptd:
            PLAYLIST_TRANSCRIPTS[_s] = _ptd
    _empty_pref = [s for s, pre in KEY_PREFIXES.items() if pre == ""]
    if len(_empty_pref) > 1:
        print(f"playlists: key_prefix '' declared on {_empty_pref} — only the "
              f"DEFAULT playlist may be prefixless; their keys would collide",
              file=sys.stderr)
    elif _empty_pref and _empty_pref[0] != str(
            (_CORPUS.get("default_playlist") or "cs")).lower():
        print(f"playlists: key_prefix '' on playlist '{_empty_pref[0]}' is not "
              f"the default_playlist — its bare-NNN keys are unreachable "
              f"(bare NNN binds to the default); refusing the registration",
              file=sys.stderr)
        KEY_PREFIXES[_empty_pref[0]] = _empty_pref[0] + "-"
    _kp = (_CORPUS.get("key_pattern") or "").strip()
    _td = (_CORPUS.get("transcripts_dir") or "").strip()
    _m = re.match(r"^([A-Za-z][A-Za-z0-9]*)-\(", _kp)
    if _m:
        _slug = _m.group(1).lower()
        if _slug not in PLAYLIST_DIRS:
            # flat layout: transcripts_dir itself, notes at reference/notes,
            # docs at corpus.docs_dir
            PLAYLIST_DIRS[_slug] = Path(_td).parent.name if _td else _slug
            PLAYLIST_NAMES[_slug] = _CORPUS.get("playlist_name", _slug)
            KEY_PREFIXES.setdefault(_slug, _slug + "-")
            FLAT_PLAYLISTS.add(_slug)
    for _pl, _rows in (_CORPUS.get("listed_sessions") or {}).items():
        _lst = []
        for _r in (_rows if isinstance(_rows, list) else []):
            if isinstance(_r, (list, tuple)) and len(_r) >= 2:
                _lst.append((str(_r[0]), str(_r[1])))
        LISTED_SESSIONS[str(_pl).lower()] = _lst
    EXTRA_ALIASES = {str(k): str(v) for k, v in (_CORPUS.get("extra_aliases") or {}).items()}
    DUPLICATE_SESSIONS = {str(k): str(v) for k, v in (_CORPUS.get("duplicate_sessions") or {}).items()}
    # non-contiguous membership -> derived (min,max) display blocks + member-of
    for _pl, _groups in (_CORPUS.get("block_membership") or {}).items():
        _lst = BLOCKS.setdefault(str(_pl).lower(), [])
        _mo = _MEMBER_OF.setdefault(str(_pl).lower(), {})
        for _g in (_groups if isinstance(_groups, list) else []):
            try:
                _name, _members = str(_g[0]), [int(n) for n in (_g[1] or [])]
            except (TypeError, ValueError, IndexError):
                print(f"playlists: ignoring malformed block_membership entry for {_pl}: {_g!r}")
                continue
            if _members:
                _lst.append(((min(_members), max(_members)), _name))
                for _n in _members:
                    _mo[_n] = _name
    for _pl, _rows in (_CORPUS.get("blocks") or {}).items():
        _rows = _rows if isinstance(_rows, list) else []
        _lst = BLOCKS.setdefault(str(_pl).lower(), [])
        for _r in _rows:
            try:
                _lst.append(((int(_r[0]), int(_r[1])), str(_r[2])))
            except (TypeError, ValueError, IndexError):
                print(f"playlists: ignoring malformed corpus.blocks entry for {_pl}: {_r!r}")
except Exception as _e:
    print(f"playlist registration from config failed: {_e} — empty registry",
          file=sys.stderr)

DEFAULT_PLAYLIST = (corpus_cfg() or {}).get("default_playlist") or "cs"


def playlist_keys() -> tuple:
    """Ordered registered playlist slugs (config order — P6.1: no hardcoded base)."""
    return tuple(PLAYLIST_DIRS)


def numeric_slugs() -> str:
    """Regex alternation of numeric-session playlists (registered minus listed)."""
    return "|".join(k for k in playlist_keys() if k not in LISTED_SESSIONS)

# ---------------- citation grammar ----------------
# A minute is a cite ONLY right after a session key + ","/whitespace — never a
# floating HH:MM (times inside quotes, paper titles, [MM:SS] pointers etc.).
_NUM_PREFIX_RE = re.compile(r"^\s*(\d{1,3})\s*-\s*")


def clean_dir(pl: str) -> Path:
    # ADR 0007: per-playlist transcripts_dir (ROOT-relative) is the ONE
    # config-gated exception to the tree-locked TRANSCRIPTS model — a shelf
    # whose sub-playlist clean dirs sit at top level declares them here.
    if pl in PLAYLIST_TRANSCRIPTS:
        return ROOT / PLAYLIST_TRANSCRIPTS[pl]
    if pl in FLAT_PLAYLISTS:
        return ROOT / PLAYLIST_DIRS[pl] / "clean"
    return TRANSCRIPTS / PLAYLIST_DIRS[pl] / "clean"


# P6.1: per-playlist flags come from corpus.playlists entries (was
# corpus.extra_playlists, an Investing-specific list shape).
_EXTRA_CFG = _PLAYLISTS_CFG


def notes_dir(pl: str) -> Path:
    if pl in FLAT_PLAYLISTS:
        return REF / "notes"
    # A secondary playlist may still share the shelf's flat notes folder (Politics keeps every
    # note in reference/notes and separates playlists by KEY PREFIX, not by directory). Without
    # this, inventory looked for reference/<dir>/notes/, never found the note, and reported the
    # session as still without-notes after a successful scaffold.
    if _EXTRA_CFG.get(pl, {}).get("notes_flat"):
        return REF / "notes"
    return REF / PLAYLIST_DIRS[pl] / "notes"


def docs_dir(pl: str) -> Path:
    # Per-playlist override first (top-level doc dirs like reference/<ar-name>
    # vs the flat docs_dir); absent -> the C3.6 derivation, unchanged.
    _od = str(_EXTRA_CFG.get(pl, {}).get("docs_dir") or "").strip()
    if _od:
        return ROOT / _od
    if pl in FLAT_PLAYLISTS:
        _d = (_CORPUS.get("docs_dir") or "").strip()
        return ROOT / _d if _d else REF
    return REF / PLAYLIST_DIRS[pl]


def topics_dir() -> Path:
    return REF / "topics"


def _display_title(stem: str, pl: str) -> str:
    t = stem
    if pl not in LISTED_SESSIONS:   # numeric playlists carry NN- prefixes
        m = _NUM_PREFIX_RE.match(t)
        if m:
            t = t[m.end():]
    t = re.sub(r"\.en$", "", t)   # transcription suffix never reaches the title
    return t.strip()


def _slug_title(title: str, cap: int = 64) -> str:
    """Filename-safe kebab slug; fullwidth punctuation folded away."""
    s = title.lower()
    for fw, asc in (("？", " "), ("：", " "), ("｜", " "), ("＂", ""),
                    ("⧸", " "), ("＊", ""), ("’", ""), ("‘", "")):
        s = s.replace(fw, asc)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    if len(s) > cap:
        cut = s[:cap]
        s = cut[:cut.rfind("-")] if "-" in cut else cut
    return s or "session"


_sessions_cache: list | None = None


def load_sessions() -> list:
    """Index every session across playlists (cached). Numeric playlists list
    only the numbers that exist on disk (cs 016 is absent — by design)."""
    global _sessions_cache
    if _sessions_cache is not None:
        return _sessions_cache
    sessions = []
    for pl in playlist_keys():
        d = clean_dir(pl)
        if pl not in LISTED_SESSIONS:
            seen = {}
            for f in sorted(d.glob("*.txt")) if d.is_dir() else []:
                m = _NUM_PREFIX_RE.match(f.name)
                if not m:
                    continue
                seen[int(m.group(1))] = f
            for n in sorted(seen):
                f = seen[n]
                title = _display_title(f.stem, pl)
                sessions.append({"key": session_key_of(pl, f"{n:03d}"), "pl": pl,
                                 "num": n, "ident": f"{n:03d}", "title": title,
                                 "fname": f.name, "rel": str(f.relative_to(ROOT)),
                                 "block": block_of(n, pl)})
        else:
            by_name = {f.name: f for f in sorted(d.glob("*.txt"))} if d.is_dir() else {}
            for slug, fname in LISTED_SESSIONS.get(pl, []):
                f = by_name.get(fname)
                if f is None:
                    continue
                title = _display_title(f.stem, pl)
                sessions.append({"key": f"ex-{slug}", "pl": pl, "num": None,
                                 "ident": slug, "title": title,
                                 "fname": f.name, "rel": str(f.relative_to(ROOT)),
                                 "block": "Extras"})
    # F7: raw-lane sessions — a session with NO clean file but a raw one still
    # exists (the two-source design). Registry entries point at the raw file;
    # the check's source-row routing (F4b) then verifies those notes against
    # the raw lane. Clean files always win when both exist.
    for pl in playlist_keys():
        rd = (corpus_cfg() or {}).get("playlists", {}).get(pl, {}).get("raw_dir")
        if not rd:
            continue
        rawd = TRANSCRIPTS / pl / rd
        if not rawd.is_dir():
            continue
        have = {s["num"] for s in sessions if s["pl"] == pl and s["num"] is not None}
        seen = {}
        for f in sorted(rawd.glob("*.txt")):
            m = _NUM_PREFIX_RE.match(f.name) or \
                re.search(r"-(\d{1,3})-", f.name)
            if m:
                seen.setdefault(int(m.group(1)), f)
        for n in sorted(seen):
            if n in have:
                continue
            f = seen[n]
            sessions.append({"key": session_key_of(pl, f"{n:03d}"), "pl": pl,
                             "num": n, "ident": f"{n:03d}",
                             "title": _display_title(f.stem, pl),
                             "fname": f.name, "rel": str(f.relative_to(ROOT)),
                             "block": block_of(n, pl)})
    _sessions_cache = sessions
    return sessions


# P6.3: O(1) session lookup — the index is built beside the list cache.
# check/inventory/find_note loop over get_session per file, so the linear
# scan made whole-corpus runs quadratic in the session count.
_SESSIONS_BY_KEY: dict = {}


def get_session(key: str):
    key = EXTRA_ALIASES.get(key, key)
    if not _SESSIONS_BY_KEY:
        for s in load_sessions():
            _SESSIONS_BY_KEY.setdefault(s["key"], s)
    hit = _SESSIONS_BY_KEY.get(key)
    if hit is not None:
        return hit
    # F3c (fqhn receipt): fork-era cites write UNPADDED keys — «المجلس 47»
    # parses to cite-key '47' while the registry canonical key is '047'. Every
    # downstream consumer (found_minutes, _session_normalized, source_hint,
    # src_for) resolves its session through get_session, so ONE pad-tolerant
    # fallback here repairs the whole class: bare digits resolve against the
    # default playlist, slug-prefixed forms against their own playlist.
    # Whole-value grammar only (fullmatch) — '470' can never reach '047'.
    m = re.fullmatch(r"([\w]+-)?(\d{1,3})", key, re.UNICODE)
    if m:
        pl = m.group(1).rstrip("-") if m.group(1) else DEFAULT_PLAYLIST
        try:
            ck = session_key_of(pl, f"{int(m.group(2)):03d}")
        except Exception:
            return None
        return _SESSIONS_BY_KEY.get(ck)
    return None


def parse_session_key(arg: str) -> tuple:
    """Command-line session key -> (slug, ident). Bare NNN = default playlist.
    T9.1: on a prefixless-default shelf (key_prefix ''), the bare-NNN form IS
    the canonical key — resolution goes through get_session so bare NNN and
    any scoped spelling of the same session unify."""
    # Config-driven numeric slugs (cs/rr + any registered flat shelf, e.g. is)
    m = re.fullmatch(rf"({numeric_slugs()})-(\d{{1,3}})", arg)
    if m:
        return m.group(1), f"{int(m.group(2)):03d}"
    # P6.1: listed-session playlists (extras) parse <pl>-<slug>
    _listed = "|".join(LISTED_SESSIONS) or r"(?!)"
    m = re.fullmatch(rf"({_listed})-([a-z0-9-]+)", arg)
    if m:
        return m.group(1), m.group(2)
    m = re.fullmatch(r"(\d{1,3})", arg)
    if m:
        return DEFAULT_PLAYLIST, f"{int(m.group(1)):03d}"
    # T9.1: a prefixless-default shelf also accepts its sub-playlist keys as
    # spelled on disk (abtr-073) — resolve by the SESSION INDEX, not by grammar.
    if KEY_PREFIXES.get(DEFAULT_PLAYLIST) == "" and get_session(arg):
        for s in load_sessions():
            if s["key"] == arg:
                return s["pl"], s["ident"]
    _exp = ", ".join(f"{k}-NNN" for k in playlist_keys() if k not in LISTED_SESSIONS)
    if LISTED_SESSIONS:
        _exp += ", or " + "/".join(f"{k}-<slug>" for k in LISTED_SESSIONS)
    sys.exit(f"Unknown session key: {arg!r} — expected NNN (default {DEFAULT_PLAYLIST}), {_exp}")


def session_key_of(pl: str, ident: str) -> str:
    """Session key = the playlist's key_prefix + ident. The default prefix
    (slug + "-") reproduces the P6.1 grammar byte-for-byte; key_prefix: ""
    (default playlist only) yields PREFIXLESS keys (T9.1/ADR 0007)."""
    return KEY_PREFIXES.get(pl, pl + "-") + ident


def block_of(n: int, pl: str = DEFAULT_PLAYLIST) -> str:
    if pl in _MEMBER_OF:
        return _MEMBER_OF[pl].get(n, "Unmapped")
    for (lo, hi), name in BLOCKS.get(pl, []):
        if lo <= n <= hi:
            return name
    return "Unmapped"




