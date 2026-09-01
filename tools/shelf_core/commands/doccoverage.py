#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""doccoverage — B4 port of scripts/doc-coverage.py as a registry command
(`shelf doc-coverage`).

TRIAGE ledger: per-session representation of every doc. Port rules:
- ALL module-level config state (ROOT/CFG/NOTES/CLEAN/DOCS_DIR/cite grammar)
  is computed inside cmd_doc_coverage — the script computed it at import and
  even sys.exit(2)'d at import when gates.docs_dir was missing; the command
  keeps the same message and exit code, just at call time.
- BOTH engines ported verbatim as closures: the generic engine (fx/investing
  controls byte-identical, P6.11/P6.12 receipts stay valid) and the S9.3
  quotes-responsibility fork (Politics + fqhn). `gates.coverage_profile`
  selects between them INSIDE the command (the script chose in __main__).
- scripts/_shelf_lib → shelf_core.gatelib (B1). The script's `import yaml`
  was dead (W4.5 removed its last use); not carried over.
"""
from __future__ import annotations

import glob
import os
import re
import sys

from shelf_core import gatelib as lib
from shelf_core.notes import claims_count as _claims_count  # noqa: F401 (A5.3(d))

DEFAULTS = {
    "floor_high": 12,
    "floor_low": 7,
    "bucket_avg_threshold": 40,
    "repr_pct": 0.30,
    "repr_pct_multi": 0.12,
    "min_claims": 10,
}
# A5.6: the tenant paths (reference/خلافة-إسلامية, نص-politics-islamism/clean)
# are GONE from the defaults. notes/clean derive from the corpus config's
# transcripts_dir (shape-generic, the parse layer's own derivation); docs_dir
# comes from gates.docs_dir — when absent the run is LOUD, never Politics-fragile.

_FORK_DEFAULTS = {
    "floor_high": 12, "floor_low": 7, "bucket_avg_threshold": 40,
    "neglect_pct": 0.10, "thin_pct": 0.20, "min_quotes": 10,
}


def cmd_doc_coverage(paths):
    ROOT = str(lib.find_root())
    CFG_PATH = os.path.join(ROOT, "config", "project.yaml")

    # W4.5: the gate section via the shared loader (loud on corruption, silent
    # on absence); the fork's private yaml read is gone with its silent pass.
    CFG = dict(DEFAULTS)
    CFG.update(lib.gates_cfg())
    _CORPUS = lib.corpus_cfg()
    _TD = str((_CORPUS or {}).get("transcripts_dir") or "transcripts/clean")
    NOTES = str(lib.notes_dir(ROOT))
    CLEAN = os.path.join(ROOT, _TD.replace("/clean", "") + "/clean") if "/clean" not in _TD \
        else os.path.join(ROOT, _TD)
    _docs_cfg = CFG.get("docs_dir")
    if not _docs_cfg:
        # A5.6 acceptance: a run without a configured docs dir says so, in the
        # shelf's own words, instead of silently sweeping Politics paths.
        print("doc-coverage: no gates.docs_dir in config — pass --config or run from "
              "a shelf with config/project.yaml (docs_dir)", file=sys.stderr)
        sys.exit(2)
    DOCS_DIR = os.path.join(ROOT, str(_docs_cfg))

    # corpus identity — config-driven via the shared loader (A5.6: the private
    # silent-pass yaml read and the tenant defaults المجلس/is-(\d{3}) are gone;
    # the fallback is the parse layer's generic key pattern).
    _CITE_KW = re.escape(str((_CORPUS or {}).get("cite_pattern", "") or "المجلس"))
    _KEY_PAT = str((_CORPUS or {}).get("key_pattern", "") or r"(?:cs|ex|rr)-[a-z0-9]+(?:-[a-z0-9]+)*")
    _KEY_SLUG = _KEY_PAT.split("-", 1)[0] if "-" in _KEY_PAT else "is"
    _CLAIM_SOURCE = str((_CORPUS or {}).get("claim_source", "auto"))

    # Two cite grammars: keyword (المجلس N، HH:MM) and paren ((is-017, 00:48)).
    CITE = re.compile(
        r"(?:%s\s*(\d{1,3})\s*[،,]\s*(\d{1,2}:\d{2})|(\w+)-(\d{3})\s*[،,]\s*(\d{1,2}:\d{2}))"
        % _CITE_KW)

    _ambiguous_globs: list = []
    _bucket_fallback: list = []

    def key_of(num, slug=None):
        return "%s-%03d" % (slug or _KEY_SLUG, int(num))

    def note_path(key):
        # P6.12: template exemption copied from the gates — a template's Session
        # row is a placeholder and its claims/bucket reads are noise.
        hits = [h for h in glob.glob(os.path.join(NOTES, key + "-*.md"))
                if not re.search(r"(?:قالب|template|skeleton)", os.path.basename(h), re.I)]
        if len(hits) > 1:
            # P6.12: an ambiguous glob used to silently return None (the session
            # then read as note-less) — print it.
            print("doc-coverage: ambiguous note glob for %s: %s" % (key, hits), file=sys.stderr)
            _ambiguous_globs.append(key)
        return hits[0] if len(hits) == 1 else None

    def claims_rows(key):
        # A5.3(d): the claims grammar lives in the parse layer (notes.claims_count);
        # the fork's private C#/محاور counting is gone. The محاور match is now
        # diacritic-tolerant over ### headers (was the strict regex).
        p = note_path(key)
        if not p:
            return None
        with open(p, encoding="utf-8", errors="replace") as f:
            return _claims_count(f.read(), _CLAIM_SOURCE)

    def bucket_count(key):
        nnn = key.split("-")[1]
        hits = glob.glob(os.path.join(CLEAN, nnn + " *.ar-orig.txt")) or \
               glob.glob(os.path.join(CLEAN, nnn + "*.ar-orig.txt"))
        if len(hits) == 1:
            txt = open(hits[0], encoding="utf-8", errors="replace").read()
            return len(set(re.findall(r"\[(\d{1,2}:\d{2})\]", txt)))
        # P6.12: the note-cite fallback (no transcript found) measures cites, not
        # buckets — keep the floor math but LABEL it in the summary.
        p = note_path(key)
        if not p:
            return 0
        if key not in _bucket_fallback:
            _bucket_fallback.append(key)
        txt = open(p, encoding="utf-8", errors="replace").read()
        return len(set(re.findall(r"[،,]\s*(\d{1,2}:\d{2})\)", txt)))

    def doc_stats(path):
        txt = open(path, encoding="utf-8", errors="replace").read()
        cites = {}
        for m in CITE.finditer(txt):
            try:
                if m.group(1) is not None:        # keyword form: المجلس N، HH:MM
                    k = key_of(m.group(1))
                else:                              # paren form: (is-017, 00:48)
                    # was: key_of(m.group(5)) ran int("00:30") and ValueError'd
                    # EVERY paren cite into the loud-skip lane, silently zeroing
                    # those docs' counts (measured: fx-001's six paren cites all
                    # SKIPped; fixed in P6.12). The guard shape remains because
                    # the CLASS — a regex group drift between grammar lanes —
                    # regenerates whenever a lane is widened.
                    # The paren branch's groups are (\w+)=3, (\d{3})=4, (time)=5:
                    k = key_of(m.group(4), slug=m.group(3))
            except ValueError:
                # W4.5 companion: correct cwd-rooted resolution now runs this fork
                # on foreign corpora too; a cite form its grammar can't parse is
                # skipped LOUDLY (once) instead of crashing the whole sweep.
                print(f"  skip unparseable cite {m.group(0)[:40]!r} in {os.path.basename(path)}",
                      file=sys.stderr)
                continue
            cites[k] = cites.get(k, 0) + 1
        return cites

    # ------------------------------------------------------------------
    # generic engine (was main()) — fx/investing controls byte-identical
    # ------------------------------------------------------------------
    def main_engine(argv):
        if argv:
            docs = [os.path.abspath(p) for p in argv]
        else:
            docs = sorted(glob.glob(os.path.join(DOCS_DIR, "*.html")))
            if not docs:
                # W4.5: the 0/0-green — 'DOCS FLAGGED: 0/0' with exit 0 on a corpus
                # the fork could not see. Empty is loud now, with resolved paths.
                print(f"no docs under {DOCS_DIR} (root {ROOT}; notes {NOTES}) — "
                      "run from the shelf root or sync tools/", file=sys.stderr)
                sys.exit(2)
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
        if _bucket_fallback:
            print("buckets≈cites for %d sessions (transcript not found; counted note cites): %s" % (
                len(_bucket_fallback), ", ".join(sorted(_bucket_fallback))))
        return 1 if fail else 0

    # ------------------------------------------------------------------
    # S9.3 PORT — the quotes-responsibility profile (was the فقه-النفس fork).
    #
    # The fork (adapted 2026-08 on the real corpus, recalibration 2 dated
    # 2026-08-24) encodes measured semantics the generic engine does not
    # express: timeless + ranged keyword cites, «»-span claims-equivalent, a
    # claimed-at-floor responsibility rule (a session cited by ANY doc at that
    # doc's floor is covered — giant Q&A notes deflate raw ratios, 12-24%
    # measured, so no single percentage separates the populations), NEGLECTED/
    # THIN ratio tiers for unclaimed sessions only, a per-playlist measurement
    # mode, and a configured doc-skip set (index/template/glossary + the
    # اقرأ-001-027 umbrella — user decision 2026-08-24). Per the plan (S9.3),
    # that adaptation is ported HERE so one script serves both shelves, selected
    # by `gates.coverage_profile: quotes-responsibility` in config/project.yaml.
    # The generic engine above remains the default — fx/investing controls are
    # byte-identical (P6.11/P6.12 receipts stay valid).
    # ------------------------------------------------------------------

    def _fork_cfg():
        c = dict(_FORK_DEFAULTS)
        c.update(CFG)
        return c

    def _fork_regex(kw):
        # The fork's cite grammar: keyword + number, zero-padded ok, optional
        # en-dash/hyphen range crediting BOTH endpoints; time/سطر suffixes ignored.
        return re.compile(
            r"%s\s*0*(\d{1,3})(?:\s*[–-]\s*(?:%s\s*)?0*(\d{1,3}))?" % (kw, kw))

    def _fork_note_path(notes_dir, prefix, n):
        hits = glob.glob(os.path.join(notes_dir, "%s%03d-*.md" % (prefix, n)))
        return hits[0] if len(hits) == 1 else None

    def _fork_make_note_quotes(notes_dir, prefix):
        cache = {}

        def note_quotes(n):
            if n in cache:
                return cache[n]
            p = _fork_note_path(notes_dir, prefix, n)
            q = _claims_count(open(p, encoding="utf-8", errors="replace").read(),
                              "quotes") if p else 0
            cache[n] = q
            return q

        return note_quotes

    def _fork_doc_stats(path, session_max, kw):
        txt = open(path, encoding="utf-8", errors="replace").read()
        cites = {}
        for m in _fork_regex(kw).finditer(txt):
            for g in (m.group(1), m.group(2)):
                if g:
                    n = int(g)
                    if 1 <= n <= session_max:
                        cites[n] = cites.get(n, 0) + 1
        return cites

    def _fork_analyze(universe, report, note_quotes, session_max, kw, cfg):
        """Ported verbatim from the fork's analyze() — same logic, same output."""
        all_stats = {d: _fork_doc_stats(d, session_max, kw) for d in universe}
        cross = {}
        for c in all_stats.values():
            for k, v in c.items():
                cross[k] = cross.get(k, 0) + v

        # Responsibility rule (recalibration 2, 2026-08-24): the percentage is a
        # FALLBACK, not the primary test — see the S9.3 PORT block above.
        doc_floors = {}
        for d, c in all_stats.items():
            ks = list(c)
            if not ks:
                doc_floors[d] = cfg["floor_high"]
                continue
            avg_q = sum(note_quotes(k) for k in ks) / len(ks)
            doc_floors[d] = cfg["floor_high"] if avg_q > cfg["bucket_avg_threshold"] \
                else cfg["floor_low"]
        claimed = set()
        for d, c in all_stats.items():
            fl = doc_floors[d]
            for k, v in c.items():
                if v >= fl:
                    claimed.add(k)

        fail = 0
        triage_all = {}
        lines = []
        for d in report:
            c = all_stats.get(d) or _fork_doc_stats(d, session_max, kw)
            name = os.path.basename(d)
            keys = sorted(c)
            if not keys:
                lines.append("%s: NO CITED SESSIONS?!" % name)
                fail += 1
                continue
            quotes = [note_quotes(k) for k in keys]
            avg_q = sum(quotes) / len(quotes)
            floor = cfg["floor_high"] if avg_q > cfg["bucket_avg_threshold"] \
                else cfg["floor_low"]
            thin = [k for k in keys if c[k] < floor and k not in claimed]
            neglected, triage = [], []
            for k in keys:
                q = note_quotes(k)
                tot = cross.get(k, 0)
                if q < cfg["min_quotes"]:
                    continue
                r = tot / q
                if k in claimed:
                    # (c) claimed but ratio <neglect_pct = floor-masked shallow ->
                    # triage, never gate-fail
                    if r < cfg["neglect_pct"]:
                        triage.append((k, q, tot, "claimed x%d but %.0f%%" % (
                            max(v for dd, cc in all_stats.items()
                                for v in [cc.get(k, 0)] if v), r * 100)))
                elif r < cfg["neglect_pct"]:
                    neglected.append((k, q, tot))
                elif r < cfg["thin_pct"]:
                    triage.append((k, q, tot, "orphan %.0f%%" % (r * 100)))
            problems = []
            if thin:
                problems.append("floor<%d touches (unclaimed elsewhere): " % floor +
                                ", ".join("%03d(x%d)" % (k, c[k]) for k in thin))
            if neglected:
                problems.append("NEGLECTED (unclaimed, <10%% of note quotes): " +
                                ", ".join("%03d(quotes=%d,all-doc-cites=%d)"
                                          % (k, q, t) for k, q, t in neglected))
            if problems:
                fail += 1
                lines.append("%s: FLAG  [%d sessions, avg %.0f note-quotes, floor %d]"
                             % (name, len(keys), avg_q, floor))
                for p in problems:
                    lines.append("   - " + p)
            else:
                lines.append("%s: OK  [%d sessions, avg %.0f note-quotes, floor %d]"
                             % (name, len(keys), avg_q, floor))
            if triage:
                # (b) THIN tier = triage list only, never a gate failure
                lines.append("   ~ triage (deepen; not gate-fail): " +
                             ", ".join("%03d(%s;q=%d,cites=%d)" % (k, note, q, t)
                                       for k, q, t, note in triage))
                for k, q, t, note in triage:
                    triage_all.setdefault(k, (q, t, note))
        return fail, lines, triage_all

    def _fork_playlists(cfg, kw):
        pl = {}
        for slug, spec in (cfg.get("playlists") or {}).items():
            if isinstance(spec, dict):
                pl[slug] = (spec.get("docs", ""), spec.get("prefix", ""),
                            int(spec.get("max", 0) or 10 ** 6))
            else:  # shorthand: [docs, prefix, max]
                pl[slug] = (spec[0], spec[1], int(spec[2]))
        return pl

    def _fork_main(argv):
        cfg = _fork_cfg()
        kw = re.escape(str((_CORPUS or {}).get("cite_pattern", "") or "المجلس"))
        notes = (_CORPUS or {}).get("notes_dir")
        notes_dir = os.path.join(ROOT, str(notes)) if notes else NOTES
        skip = set(CFG.get("docs_skip") or [])
        session_max = int(CFG.get("session_max", 10 ** 6))

        def all_docs():
            return sorted(f for f in glob.glob(os.path.join(DOCS_DIR, "*.html"))
                          if os.path.basename(f) not in skip)

        if "--playlists" in argv:
            pls = _fork_playlists(cfg, kw)
            if not pls:
                print("doc-coverage: --playlists but no gates.playlists configured",
                      file=sys.stderr)
                return 2
            grand_triage = {}
            for slug, (subdir, prefix, smax) in pls.items():
                # fork layout receipt: playlist doc subdirs live UNDER reference/
                # (the config value is the subdir name, not a root-relative path)
                base = subdir if subdir.startswith("reference") \
                    else os.path.join("reference", subdir)
                docs = sorted(glob.glob(os.path.join(ROOT, base, "*.html")))
                note_quotes = _fork_make_note_quotes(notes_dir, prefix)
                fail, lines, triage = _fork_analyze(docs, docs, note_quotes, smax,
                                                    kw, cfg)
                print("\n=== %s — %d docs ===" % (slug, len(docs)))
                for l in lines:
                    print(l)
                print("   docs flagged (would-be gate): %d/%d" % (fail, len(docs)))
                if triage:
                    print("   deepening triage (%d sessions):" % len(triage))
                    for k in sorted(triage):
                        q, t, note = triage[k]
                        print("      %03d: %d/%d = %.0f%% — %s"
                              % (k, t, q, t / q * 100, note))
                        grand_triage.setdefault((slug, k), (q, t, note))
            print("\nPLAYLISTS MEASURED: %d (informational; main gate unchanged)"
                  % len(pls))
            return 0

        if not all_docs() and not argv:
            print("no docs under %s (root %s) — nothing measured" % (DOCS_DIR, ROOT),
                  file=sys.stderr)
            return 2
        paths_ = [os.path.abspath(p) for p in argv] or all_docs()
        main_note_quotes = _fork_make_note_quotes(notes_dir, "")
        fail, lines, triage_all = _fork_analyze(all_docs(), paths_,
                                                main_note_quotes, session_max,
                                                kw, cfg)
        for l in lines:
            print(l)
        print("\nDOCS FLAGGED (hard gate): %d/%d" % (fail, len(paths_)))
        if triage_all:
            print("DEEPENING TRIAGE (%d sessions — wave list, not failures):"
                  % len(triage_all))
            for k in sorted(triage_all):
                q, t, note = triage_all[k]
                print("   %03d: %d/%d = %.0f%% — %s" % (k, t, q, t / q * 100, note))
        return 1 if fail else 0

    argv = list(paths)
    if CFG.get("coverage_profile") == "quotes-responsibility":
        sys.exit(_fork_main(argv))
    sys.exit(main_engine(argv))
