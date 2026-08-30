#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Minute-map helper for the shelf-build workflow.

Given a session key (argv[1]) and candidate phrases (one per line on stdin),
print the transcripts/<playlist>/clean/ [MM:SS] bucket that contains each
phrase (tolerant subsequence match, same tolerance as tools/shelf.py).

Why: a cite like (cs-002, 07:31) must point at the EXACT phrase's location in
the clean transcript. This tool returns that minute — run it on the literal
string you will quote, so the cite is the only safe one. Or skip it entirely:
`python3 tools/shelf.py lift KEY` slices paste-ready verbatim units itself.

Session keys: bare NNN = cs default; cs-NNN, rr-NNN; extras ex-<slug>.

Run from repo root:
    python3 tools/findmin.py cs-002 <<'EOF'
    cash feels good because its nominal value is stable
    the risk-free asset for a long-term investor
    EOF
"""
import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)          # tools/ -> repo root
os.chdir(REPO)
sys.path.insert(0, os.path.join(REPO, "tools"))
try:
    from shelf_core.playlists import (parse_session_key, session_key_of,
                                      playlist_keys, get_session)
    from shelf_core.transcript import clean_buckets
    from shelf_core.match import tokens, subseq
    from shelf_core.citation import fmt_mmss
except ImportError:                    # flat layout fallback
    from playlists import (parse_session_key, session_key_of,  # type: ignore
                           playlist_keys, get_session)
    from transcript import clean_buckets  # type: ignore
    from match import tokens, subseq  # type: ignore
    from citation import fmt_mmss  # type: ignore


def find_min(qt, buckets):
    # search every bucket for the phrase
    for m, toks in buckets.items():
        if subseq(qt, toks, gap_r=0.85, miss_r=0.30):
            return m
    # looser fallback: any bucket containing the first 8 tokens
    if len(qt) >= 6:
        head = qt[:min(8, len(qt))]
        for m, toks in buckets.items():
            if shelf.subseq(head, toks, gap_r=1.0, miss_r=0.0):
                return m
    return None


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    slug, ident = parse_session_key(sys.argv[1])
    # Bare "017" parses to the default playlist (cs) — on a flat shelf that is
    # wrong, so walk every registered playlist until one holds the session
    # (is-017 in Politics, cs-017 in Investing); the parsed slug goes first.
    candidates = [slug] + [pl for pl in playlist_keys() if pl != slug]
    key = None
    for pl in candidates:
        k = session_key_of(pl, ident)
        if get_session(k) is not None:
            key = k
            break
    if key is None:
        print(f"No session for {sys.argv[1]!r} in any playlist: "
              f"{' / '.join(playlist_keys())}", file=sys.stderr)
        return 2
    buckets = clean_buckets(key)
    if not buckets:
        print(f"No clean transcript ([MM:SS] buckets) for session {key}",
              file=sys.stderr)
        return 2
    for line in sys.stdin:
        p = line.strip()
        if not p:
            continue
        qt = tokens(p)
        if len(qt) < 3:
            print(f"  SKIP(short): {p[:50]}")
            continue
        m = find_min(qt, buckets)
        if m is None:
            print(f"  NOTFOUND: {p[:60]}")
        else:
            print(f"  [{fmt_mmss(m)}]  | {p[:70]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
