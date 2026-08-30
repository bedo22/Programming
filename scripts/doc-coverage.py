#!/usr/bin/env python3
"""doc-coverage.py — quantified ledger of how well Politics topic docs cover
their notes (port of the shelf-pipeline rr-doc-coverage, Politics grammar).

For each topic doc in gate.docs_dir:
  - contributing sessions = every is-NNN key cited via المجلس N، HH:MM
  - citations per session = count of cite spans
  - per session: | C# | claim rows in its note vs total cites across ALL docs
  - flag sessions whose cross-doc citation mass < repr_pct of claims rows
  - floor rule: floor_high if contributing sessions avg > bucket_avg_threshold
    buckets else floor_low
Era/canon docs with zero session cites are SKIPPED.

Usage: python3 scripts/doc-coverage.py            (all docs in gate.docs_dir)
       python3 scripts/doc-coverage.py doc.html   (subset)
"""
import glob
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG_PATH = os.path.join(ROOT, "config", "project.yaml")

DEFAULTS = {
    "notes_dir": "reference/notes",
    "docs_dir": "reference/خلافة-إسلامية",
    "clean_dir": "نص-politics-islamism/clean",
    "floor_high": 12,
    "floor_low": 7,
    "bucket_avg_threshold": 40,
    "repr_pct": 0.30,
    "repr_pct_multi": 0.12,
    "min_claims": 10,
}


def load_cfg():
    cfg = dict(DEFAULTS)
    try:
        with open(CFG_PATH, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        cfg.update(data.get("gate", {}) or {})
    except FileNotFoundError:
        pass
    return cfg


CFG = load_cfg()
NOTES = os.path.join(ROOT, CFG["notes_dir"])
DOCS_DIR = os.path.join(ROOT, CFG["docs_dir"])
CLEAN = os.path.join(ROOT, CFG["clean_dir"])

# corpus identity (config-driven; no hardcoded المجلس/is grammar)
_CORPUS = {}
try:
    with open(CFG_PATH, encoding="utf-8") as f:
        _CORPUS = (yaml.safe_load(f) or {}).get("corpus", {}) or {}
except FileNotFoundError:
    pass
_CITE_KW = re.escape(str(_CORPUS.get("cite_pattern", "المجلس")))
_KEY_PAT = _CORPUS.get("key_pattern", "is-(\\d{3})")
_KEY_SLUG = _KEY_PAT.split("-", 1)[0] if "-" in _KEY_PAT else "is"
_CLAIM_SOURCE = str(_CORPUS.get("claim_source", "auto"))

# Two cite grammars: keyword (المجلس N، HH:MM) and paren ((is-017, 00:48)).
CITE = re.compile(
    r"(?:%s\s*(\d{1,3})\s*[،,]\s*(\d{1,2}:\d{2})|(\w+)-(\d{3})\s*[،,]\s*(\d{1,2}:\d{2}))"
    % _CITE_KW)


def key_of(num, slug=None):
    return "%s-%03d" % (slug or _KEY_SLUG, int(num))


def note_path(key):
    hits = glob.glob(os.path.join(NOTES, key + "-*.md"))
    return hits[0] if len(hits) == 1 else None


def claims_rows(key):
    p = note_path(key)
    if not p:
        return None
    n = 0
    with open(p, encoding="utf-8", errors="replace") as f:
        for line in f:
            # claim_source: "C#" -> | C# | table rows; "محاور" -> ### المحور
            # headers; "auto" -> either.
            if _CLAIM_SOURCE in ("C#", "auto") and re.match(r"\|\s*C\d+\s*\|", line):
                n += 1
            elif _CLAIM_SOURCE in ("محاور", "auto") and re.match(r"###\s*المحور", line):
                n += 1
    return n


def bucket_count(key):
    nnn = key.split("-")[1]
    hits = glob.glob(os.path.join(CLEAN, nnn + " *.ar-orig.txt")) or \
           glob.glob(os.path.join(CLEAN, nnn + "*.ar-orig.txt"))
    if len(hits) == 1:
        txt = open(hits[0], encoding="utf-8", errors="replace").read()
        return len(set(re.findall(r"\[(\d{1,2}:\d{2})\]", txt)))
    p = note_path(key)
    if not p:
        return 0
    txt = open(p, encoding="utf-8", errors="replace").read()
    return len(set(re.findall(r"[،,]\s*(\d{1,2}:\d{2})\)", txt)))


def doc_stats(path):
    txt = open(path, encoding="utf-8", errors="replace").read()
    cites = {}
    for m in CITE.finditer(txt):
        if m.group(1) is not None:            # keyword form: المجلس N، HH:MM
            k = key_of(m.group(1))
        else:                                  # paren form: (is-017, 00:48)
            k = key_of(m.group(5), slug=m.group(4))
        cites[k] = cites.get(k, 0) + 1
    return cites


def main(argv):
    if argv:
        docs = [os.path.abspath(p) for p in argv]
    else:
        docs = sorted(glob.glob(os.path.join(DOCS_DIR, "*.html")))

    per_doc = []
    cross = {}
    for d in docs:
        c = doc_stats(d)
        for k, v in c.items():
            cross[k] = cross.get(k, 0) + v
        per_doc.append((d, c))

    # cross-doc totals need the WHOLE docs dir, not just the subset
    if argv:
        for d in sorted(glob.glob(os.path.join(DOCS_DIR, "*.html"))):
            for k, v in doc_stats(d).items():
                cross[k] = cross.get(k, 0) + v

    fail = 0
    skipped = 0
    for d, c in per_doc:
        name = os.path.basename(d)
        keys = sorted(c)
        if not keys:
            print("%s: SKIP (era/canon doc — no session cites)" % name)
            skipped += 1
            continue
        buckets = [bucket_count(k) or 0 for k in keys]
        avg_b = sum(buckets) / len(buckets)
        floor = CFG["floor_high"] if avg_b > CFG["bucket_avg_threshold"] else CFG["floor_low"]
        thin = [k for k in keys if c[k] < floor]
        # repr_pct was tuned for 1-2 session docs; a digest doc spanning 3+
        # sessions can't cite 30% of each note's full claim archive without
        # bloat (notes are the archive, docs the digest). repr_pct_multi
        # applies when the doc covers more than 2 sessions.
        thr = CFG["repr_pct_multi"] if len(keys) > 2 else CFG["repr_pct"]
        underrep = []
        for k in keys:
            r = claims_rows(k)
            tot = cross.get(k, 0)
            if r and r >= CFG["min_claims"] and tot < thr * r:
                underrep.append((k, r, tot))
        problems = []
        if thin:
            problems.append("floor<%d touches: %s" % (
                floor, ", ".join("%s(x%d)" % (k, c[k]) for k in thin)))
        if underrep:
            problems.append("under-represented across ALL docs (<%d%% of claims rows): %s" % (
                int(thr * 100),
                ", ".join("%s(claims=%d,all-doc-cites=%d)" % u for u in underrep)))
        if problems:
            fail += 1
            print("%s: FLAG  [%d sessions, avg %.0f buckets, floor %d]" % (
                name, len(keys), avg_b, floor))
            for p in problems:
                print("   - " + p)
        else:
            print("%s: OK  [%d sessions, avg %.0f buckets, floor %d]" % (
                name, len(keys), avg_b, floor))

    print("\nDOCS FLAGGED: %d/%d  (skipped %d era/canon)" % (fail, len(per_doc), skipped))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
