#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""playlists — moved from helpers.py (final distribution)."""
from __future__ import annotations
import re, bisect, sys
from pathlib import Path
try:
    from .config import ROOT, REF, TEMPLATES, TRANSCRIPTS, INVENTORY
    from .match import norm, tokens, subseq, _token_index
    from .citation import fmt_mmss, parse_mmss  # may be circular, handle
except ImportError:
    pass
PLAYLIST_DIRS = {"cs": "common-sense", "ex": "extras", "rr": "rational-reminder"}
PLAYLIST_NAMES = {
    "cs": "Common Sense Investing",
    "ex": "Extras",
    "rr": "Rational Reminder",
}
DEFAULT_PLAYLIST = "cs"   # a bare number like `pins 002` means cs-002

# ---- config-driven flat single-playlist shelves (reusable across shelves) ----
# A corpus.key_pattern of the form "<slug>-(\d{3})" (e.g. "is-(\d{3})",
# "fiqh-(\d{3})") registers <slug> as a FLAT playlist: transcripts live at
# <transcripts_dir>, notes at reference/notes, docs at corpus.docs_dir. No shelf
# specifics below — the next Arabic shelf only edits config/project.yaml.
_CORPUS: dict = {}
FLAT_PLAYLISTS: set = set()
try:
    from pathlib import Path as _P
    _cfg_path = ROOT / "config" / "project.yaml"
    if _cfg_path.exists():
        try:
            import yaml as _yaml  # type: ignore
            _cfg = _yaml.safe_load(_cfg_path.read_text(encoding="utf-8")) or {}
            _CORPUS = _cfg.get("corpus", {}) if isinstance(_cfg, dict) else {}
            _kp = (_CORPUS.get("key_pattern") or "").strip()
            _td = (_CORPUS.get("transcripts_dir") or "").strip()
            _m = re.match(r"^([A-Za-z][A-Za-z0-9]*)-\(", _kp)
            if _m:
                _slug = _m.group(1).lower()
                if _slug not in PLAYLIST_DIRS:
                    PLAYLIST_DIRS[_slug] = _P(_td).parent.name if _td else _slug
                    PLAYLIST_NAMES[_slug] = _CORPUS.get("playlist_name", _slug)
                    FLAT_PLAYLISTS.add(_slug)
            # A shelf may hold MORE THAN ONE playlist (Investing: cs/ex/rr). corpus.key_pattern
            # describes only the primary flat one, so additional playlists are declared here and
            # registered NON-flat: transcripts/<dir>/clean, notes at reference/<dir>/notes,
            # docs at reference/<dir> -- each playlist keeps its own layout and its own prefix.
            for _e in (_CORPUS.get("extra_playlists") or []):
                try:
                    if not isinstance(_e, dict) or not _e.get("slug"):
                        continue
                    _s = str(_e["slug"]).lower()
                    PLAYLIST_DIRS.setdefault(_s, _e.get("dir") or _s)
                    PLAYLIST_NAMES.setdefault(_s, _e.get("name") or _s)
                except Exception:
                    pass
        except Exception:
            pass
except Exception:
    pass


def playlist_keys() -> tuple:
    """Ordered registered playlist slugs (base cs/ex/rr, then config-driven)."""
    base = ["cs", "ex", "rr"]
    return tuple(base + [k for k in PLAYLIST_DIRS if k not in base])


def numeric_slugs() -> str:
    """Regex alternation of numeric-session playlists (all registered except ex)."""
    return "|".join(k for k in playlist_keys() if k != "ex")

# Extras sessions: explicit ordered registry (alphabetical by filename).
# Filenames contain fullwidth characters (：｜？) — matched exactly as on disk.
EX_SESSIONS = [
    ("are-your-etfs-causing-market-bubbles",
     "Are Your ETFs Causing Market Bubbles？.en.txt"),
    ("case-for-buying-home-peter-guay",
     "The Case for Buying a Home (Rent VS Buy) ｜ Peter Guay.en.txt"),
    ("renting-vs-buying-the-case-for-owning",
     "Renting vs. Buying a Home： The Case for Owning.en.txt"),
    ("renting-vs-buying-what-people-get-wrong",
     "Renting vs. Buying a Home： What People Get Wrong.en.txt"),
    ("should-i-borrow-to-invest-part-1",
     "Should I Borrow to Invest？ Part 1.en.txt"),
    ("using-your-money-to-be-happier",
     "Using Your Money To Be Happier.en.txt"),
]

# Blocks per playlist. The cs map is the APPROVED structure from
# reference/DOMAIN-MAP.md (non-contiguous session lists — do not turn into
# ranges). rr has no approved map yet ("phase 2"); its mechanical batches are
# provisional scoping aids until that lands. Every cs session 001–095 (no 016)
# is covered by exactly one block.
CS_BLOCK_MEMBERSHIP = [
    ("Why beating the market is so hard",
     [40, 45, 54, 33, 93, 92, 55, 48, 90]),
    ("Active management fails", [13, 68, 77, 31]),
    ("The case for index funds", [70, 19, 47, 42, 84, 94, 95]),
    ("Risk, returns & asset allocation",
     [23, 59, 69, 4, 60, 39, 29, 37]),
    ("Behaviour, timing & downturns",
     [18, 24, 74, 87, 25, 32, 26, 41, 44, 30, 9]),
    ("Factor investing", [8, 34, 46, 49, 52, 63]),
    ("Income strategies & dividends", [22, 53, 79, 80]),   # 080 = alias of 079
    ("Fixed income, cash & rates", [2, 50, 56, 86, 28]),
    ("Housing & mortgage debt", [17, 58, 67, 71, 72, 20]),
    ("Alternative assets & products",
     [1, 5, 10, 21, 35, 38, 61, 81, 82, 91, 3]),
    ("Implementation: ETFs & portfolios", [15, 43, 73, 83]),
    ("Tax & registered accounts", [51, 57, 64, 65, 85]),
    ("Retirement funding", [27, 62]),
    ("Advice industry & regulation", [7, 11, 66, 78, 88, 89, 36]),
    ("Money & happiness (CS side)", [6]),
    ("Crypto", [75, 76]),
    ("Specials (no topical doc)", [12, 14]),
]
CS_BLOCKS = [((min(members), max(members)), name)
             for name, members in CS_BLOCK_MEMBERSHIP]
RR_BLOCKS = [
    ((1, 85), "RR batch 1 (001-085)"),
    ((86, 170), "RR batch 2 (086-170)"),
    ((171, 255), "RR batch 3 (171-255)"),
    ((256, 340), "RR batch 4 (256-340)"),
    ((341, 430), "RR batch 5 (341-430)"),
]
BLOCKS = {
    "cs": CS_BLOCKS,
    "rr": RR_BLOCKS,
    "ex": [],
}
_CS_MEMBER_OF = {}
for _name, _members in CS_BLOCK_MEMBERSHIP:
    for _n in _members:
        _CS_MEMBER_OF[_n] = _name

# Registered duplicates (reference/DOMAIN-MAP.md, corpus anomaly #2):
# cs-080 is a byte-identical re-release of cs-079 — one note (cs-079),
# inventory marks 080 as duplicate.
DUPLICATE_SESSIONS = {"cs-080": "cs-079"}

# DOMAIN-MAP.md refers to extras sessions by short display keys; these aliases
# resolve to the canonical EX_SESSIONS slugs used by the tools.
EXTRA_ALIASES = {
    "ex-rentbuy-case-for-owning": "ex-renting-vs-buying-the-case-for-owning",
    "ex-rentbuy-get-wrong": "ex-renting-vs-buying-what-people-get-wrong",
    "ex-guay-case-for-buying": "ex-case-for-buying-home-peter-guay",
    "ex-using-money-to-be-happier": "ex-using-your-money-to-be-happier",
}

STATUSES = ("draft", "ready-for-review", "reviewed")

# ---------------- citation grammar ----------------
# A minute is a cite ONLY right after a session key + ","/whitespace — never a
# floating HH:MM (times inside quotes, paper titles, [MM:SS] pointers etc.).
_NUM_PREFIX_RE = re.compile(r"^\s*(\d{1,3})\s*-\s*")


def clean_dir(pl: str) -> Path:
    if pl in FLAT_PLAYLISTS:
        return ROOT / PLAYLIST_DIRS[pl] / "clean"
    return TRANSCRIPTS / PLAYLIST_DIRS[pl] / "clean"


_EXTRA_CFG = {str(e.get("slug", "")).lower(): e for e in (_CORPUS.get("extra_playlists") or [])
              if isinstance(e, dict)}


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
    if pl in FLAT_PLAYLISTS:
        _d = (_CORPUS.get("docs_dir") or "").strip()
        return ROOT / _d if _d else REF
    return REF / PLAYLIST_DIRS[pl]


def topics_dir() -> Path:
    return REF / "topics"


def _display_title(stem: str, pl: str) -> str:
    t = stem
    if pl in ("cs", "rr"):
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
        if pl != "ex":
            seen = {}
            for f in sorted(d.glob("*.txt")) if d.is_dir() else []:
                m = _NUM_PREFIX_RE.match(f.name)
                if not m:
                    continue
                seen[int(m.group(1))] = f
            for n in sorted(seen):
                f = seen[n]
                title = _display_title(f.stem, pl)
                sessions.append({"key": f"{pl}-{n:03d}", "pl": pl, "num": n,
                                 "ident": f"{n:03d}", "title": title,
                                 "fname": f.name, "rel": str(f.relative_to(ROOT)),
                                 "block": block_of(n, pl)})
        else:
            by_name = {f.name: f for f in sorted(d.glob("*.txt"))} if d.is_dir() else {}
            for slug, fname in EX_SESSIONS:
                f = by_name.get(fname)
                if f is None:
                    continue
                title = _display_title(f.stem, pl)
                sessions.append({"key": f"ex-{slug}", "pl": pl, "num": None,
                                 "ident": slug, "title": title,
                                 "fname": f.name, "rel": str(f.relative_to(ROOT)),
                                 "block": "Extras"})
    _sessions_cache = sessions
    return sessions


def get_session(key: str):
    key = EXTRA_ALIASES.get(key, key)
    for s in load_sessions():
        if s["key"] == key:
            return s
    return None


def parse_session_key(arg: str) -> tuple:
    """Command-line session key -> (slug, ident). Bare NNN = cs."""
    # Config-driven numeric slugs (cs/rr + any registered flat shelf, e.g. is)
    m = re.fullmatch(rf"({numeric_slugs()})-(\d{{1,3}})", arg)
    if m:
        return m.group(1), f"{int(m.group(2)):03d}"
    m = re.fullmatch(r"ex-([a-z0-9-]+)", arg)
    if m:
        return "ex", m.group(1)
    m = re.fullmatch(r"(\d{1,3})", arg)
    if m:
        return DEFAULT_PLAYLIST, f"{int(m.group(1)):03d}"
    _exp = ", ".join(f"{k}-NNN" for k in playlist_keys() if k != "ex") + ", or ex-<slug>"
    sys.exit(f"Unknown session key: {arg!r} — expected NNN (cs default), {_exp}")


def session_key_of(pl: str, ident: str) -> str:
    return f"{pl}-{ident}"


def block_of(n: int, pl: str = DEFAULT_PLAYLIST) -> str:
    if pl == "cs":
        return _CS_MEMBER_OF.get(n, "Unmapped")
    for (lo, hi), name in BLOCKS.get(pl, []):
        if lo <= n <= hi:
            return name
    return "Unmapped"


# ---------------- matching engine (moved to shelf_core.match, re-exported) ----------------
try:
    from .match import norm, normalize_for_match, tokens, _greedy_match, _first_tok_keys, _token_index, subseq
except ImportError:
    from match import norm, normalize_for_match, tokens, _greedy_match, _first_tok_keys, _token_index, subseq  # type: ignore


_EXEMPT_SECTIONS = {"papers cited", "fidelity flags", "fidelity log"}


_ATTR_STRIP_RE = re.compile(r"\s[\w-]+=\"[^\"]*\"")
_TAG_STRIP_RE = re.compile(r"<[^>]+>")


STATUS_ROW_RE = re.compile(r"^\|\s*Status\s*\|\s*([^|\n]+?)\s*\|", re.M)
FLAGS_ROW_RE = re.compile(r"^\|\s*Flags open\s*\|\s*([^|\n]+?)\s*\|", re.M)
SESSION_ROW_RE = re.compile(r"^\|\s*Session\s*\|\s*([^|\n]+?)\s*\|", re.M)
TITLE_ROW_RE = re.compile(r"^\|\s*Title\s*\|\s*([^|\n]+?)\s*\|", re.M)

_EMPTY_TYPE = re.compile(r"\|\s*Type\s*\|\s*\(type:")
_EMPTY_TODO = re.compile(r"TODO: distill from the transcript")


