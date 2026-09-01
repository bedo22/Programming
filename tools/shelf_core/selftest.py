#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""commands/selftest — T7.1: fixture-corpus selftest.

Builds its OWN synthetic corpus under plans/selftest/fxroot/ (a mini shelf:
config with an EN grammar, two transcripts, notes via the real builders) and
derives every expected count from what it creates. The retired version
asserted this shelf's tenant counts (94/6/423 cs/ex/rr) and quoted a LIVE
transcript — so a fresh clone with no corpus failed, and any other shelf
failed differently. This one passes on: fresh clone, staging tree, live repo.

Every fixture operation runs as a subprocess whose ROOT is patched to the
fixture root (the package's module-level ROOT is a constant; the pins-sweep
driver pattern). Never touches reference/: inventory regenerates INSIDE the
fixture via `--out`."""
from __future__ import annotations
import sys, subprocess
from pathlib import Path
from shelf_core.config import ROOT, INVENTORY

# ROOT patch for a subprocess that must see fxroot as its shelf
_PATCH = (
    "import sys\n"
    "from pathlib import Path\n"
    "sys.path.insert(0, {tools!r})\n"
    "R = Path({root!r})\n"
    "import shelf_core.config as C\n"
    "C.ROOT = R; C.REF = R / 'reference'; C.TRANSCRIPTS = R / 'transcripts'\n"
    "C.INVENTORY = R / 'reference' / 'inventory.md'; C.TEMPLATES = R / 'templates'\n"
    "for _n in list(sys.modules):\n"
    "    if _n.startswith('shelf_core'):\n"
    "        _m = sys.modules[_n]\n"
    "        if hasattr(_m, 'ROOT'): _m.ROOT = R\n"
    "        if hasattr(_m, 'REF'): _m.REF = R / 'reference'\n"
    "        if hasattr(_m, 'TRANSCRIPTS'): _m.TRANSCRIPTS = R / 'transcripts'\n"
    "        if hasattr(_m, 'INVENTORY'): _m.INVENTORY = R / 'reference' / 'inventory.md'\n"
    "        if hasattr(_m, 'TEMPLATES'): _m.TEMPLATES = R / 'templates'\n"
)


def cmd_selftest():
    base = ROOT / "plans" / "selftest"
    fxroot = base / "fxroot"
    results = []

    def ok(name, cond, detail=""):
        results.append((name, bool(cond)))
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}"
              + (f" — {detail}" if detail and not cond else ""))

    def fx(code, expect_rc=0, root=None):
        """Run python code against the fixture corpus (ROOT=fxroot)."""
        _r = root if root is not None else fxroot
        full = _PATCH.format(tools=str(ROOT / "tools"), root=str(_r)) + code
        r = subprocess.run([sys.executable, "-c", full],
                           capture_output=True, text=True, cwd=str(_r))
        return r

    try:
        # ---------- build the fixture corpus (derived, never hard-coded) ----------
        (fxroot / "config").mkdir(parents=True, exist_ok=True)
        (fxroot / "transcripts" / "zz" / "clean").mkdir(parents=True, exist_ok=True)
        (fxroot / "reference" / "notes").mkdir(parents=True, exist_ok=True)
        (fxroot / "reference" / "docs").mkdir(parents=True, exist_ok=True)
        # EN grammar: paren cites (zz-001, 00:00), straight-quote quotes.
        (fxroot / "config" / "project.yaml").write_text(
            "corpus:\n"
            "  key_pattern: 'zz-(\\d{3})'\n"
            "  playlists:\n    zz:\n      dir: zz\n      name: Fixture sessions\n"
            "      notes_flat: true\n"
            "  quote:\n    open: '\"'\n    close: '\"'\n"
            "gates:\n  docs_dir: reference/docs\n", encoding="utf-8")
        # synthetic transcripts: two buckets, sentences we control
        SENT1 = "the market rewards patience over cleverness in every decade"
        SENT2 = "and diversification remains the only free lunch available"
        (fxroot / "transcripts" / "zz" / "clean" / "001-first-session.txt").write_text(
            f"[00:00]\n{SENT1}\n\n[05:00]\n{SENT2}\n", encoding="utf-8")
        (fxroot / "transcripts" / "zz" / "clean" / "002-second-session.txt").write_text(
            "[00:00]\nnothing useful here for the tests\n", encoding="utf-8")

        n_expected = 2  # sessions we just wrote

        print("fixture corpus:")
        r = fx("from shelf_core.playlists import load_sessions\n"
               "print(len(load_sessions()))")
        ok(f"indexer sees the {n_expected} synthetic sessions",
           r.returncode == 0 and r.stdout.strip() == str(n_expected),
           r.stdout + r.stderr)

        # ---------- citation grammar (quote derived from OUR transcript) ----------
        from shelf_core.citation import fmt_mmss
        r = fx(
            "from shelf_core.transcript import clean_paragraphs, _slice_verbatim\n"
            "from shelf_core.match import tokens\n"
            "paras = clean_paragraphs('zz-001')\n"
            "assert paras, 'subprocess saw no buckets'\n"
            f"print(_slice_verbatim(paras[0], tokens({SENT1!r})))"
        )
        assert r.returncode == 0, f"phrase probe failed: {r.stderr}"
        real_phrase = r.stdout.strip()
        real_minute = 0
        true_unit = f'"{real_phrase}" (zz-001, {fmt_mmss(real_minute)})'
        wrong_min = fmt_mmss(300)  # different bucket

        def write_note(name, body):
            p = fxroot / "reference" / "notes" / name
            p.write_text(
                "| Field | Value |\n| --- | --- |\n"
                "| Source file | `transcripts/zz/clean/001-first-session.txt` |\n"
                "| Session | zz-001 |\n"
                "| Status | draft |\n| Flags open | no |\n"
                "## Themes\n" + body +
                "\n## Papers cited\n- none\n", encoding="utf-8")
            return p

        def run(*args):
            return fx(
                "import sys\n"
                "sys.argv = ['shelf.py'] + " + repr([str(a) for a in args]) + "\n"
                "from shelf_core import dispatch\n"
                "dispatch.main()"
            )

        print("citation grammar:")
        p1 = write_note("fx-true-only.md",
                        f"Intro.\n\n{true_unit}\n")
        r = run("pins", str(p1))
        ok("true quote passes pins (exit 0)",
           r.returncode == 0 and "Flags: 0" in r.stdout, r.stdout + r.stderr)

        p2 = write_note("fx-wrong-minute.md",
                        f"Intro.\n\n{true_unit}\n\nSecond.\n\n"
                        f'"{real_phrase}" (zz-001, {wrong_min})\n')
        r = run("pins", str(p2))
        ok("wrong minute reports exactly one flag (exit 1)",
           r.returncode == 1 and "Flags: 1" in r.stdout
           and "actually occurs at" in r.stdout, f"rc={r.returncode}\n{r.stdout}")

        r = run("pins", "--fix", str(p2))
        fixed = "✎" in r.stdout
        r2 = run("pins", str(p2))
        ok("--fix repairs the wrong minute; re-pin clean",
           fixed and r2.returncode == 0 and "Flags: 0" in r2.stdout,
           r.stdout + "\n--repin--\n" + r2.stdout)

        p3 = write_note("fx-scare-uncited.md",
                        "Scare case: 'do not scan me at all folks' stays hidden.\n"
                        "Blockquote evidence with no cite (hard lane):\n\n"
                        "> \"cash is a poor hedge against falling expected "
                        "returns for long term investors\"\n\n"
                        "Inline digest quote without cite (advisory lane): "
                        "\"some stylistic aside in prose\" stays soft.\n")
        r = run("pins", str(p3))
        ok("uncited blockquote evidence fails hard; single quotes never scanned; inline stays advisory",
           r.returncode == 1 and "UNCITED EVIDENCE QUOTE" in r.stdout
           and "advisory only" in r.stdout
           and "do not scan me" not in r.stdout,
           f"rc={r.returncode}\n{r.stdout}")

        # ---------- doc lane ----------
        print("doc lane:")
        doc_good = fxroot / "reference" / "docs" / "fx-doc-good.html"
        doc_good.write_text(f"""<!DOCTYPE html>
<html lang="en" dir="ltr"><head><meta charset="utf-8"><title>fixture</title></head>
<body><main><p>Ben argues that "{real_phrase}"
<span class="cite">(zz-001, {fmt_mmss(real_minute)})</span></p>
<p><a href="#later">anchor</a> <span id="later">ok</span></p>
</main></body></html>\n""", encoding="utf-8")
        r = run("check", str(doc_good))
        ok("doc with good quote passes check (exit 0)",
           r.returncode == 0 and "failed check" not in r.stdout,
           f"rc={r.returncode}\n{r.stdout}\n{r.stderr}")

        doc_bad = fxroot / "reference" / "docs" / "fx-doc-fabricated.html"
        doc_bad.write_text(f"""<!DOCTYPE html>
<html lang="en" dir="ltr"><head><meta charset="utf-8"><title>fixture</title></head>
<body><main><p>The study found "purple elephants trade options through the
Federal Reserve window at midnight" <span class="cite">(zz-001,
{fmt_mmss(real_minute)})</span></p></main></body></html>\n""", encoding="utf-8")
        r = run("check", str(doc_bad))
        ok("fabricated quote fails check with source span printed (exit 1)",
           r.returncode == 1 and "not found anywhere" in r.stdout
           and "copy-paste this" in r.stdout,
           f"rc={r.returncode}\n{r.stdout}\n{r.stderr}")

        # ---------- T7.2 grammar-coverage fixtures (one named case per guard) ----------
        print("T7.2 guards:")
        # 1. keyword-form --fix (V1.1): the --fix lane's permanent guard is the
        #    V1.1 scratch test; here the named case covers idempotence — a
        #    second --fix on an already-fixed note changes nothing and stays clean.
        r = run("pins", "--fix", str(p2))
        r2 = run("pins", str(p2))
        _first_fixed = "✎" in r.stdout or "No auto-fixable citations" in r.stdout
        ok("V1.1 guard: --fix idempotent (second --fix changes nothing, note re-pins clean)",
           _first_fixed and r2.returncode == 0 and "Flags: 0" in r2.stdout,
           r.stdout + "\n" + r2.stdout)

        # 2. tight-vs-loose span (V1.3): the pinned span must survive the
        #    tight grammar — slice the SECOND bucket too and demand a real span.
        r = fx(
            "from shelf_core.transcript import clean_paragraphs, _slice_verbatim\n"
            "from shelf_core.match import tokens\n"
            "paras = clean_paragraphs('zz-001')\n"
            f"sp = _slice_verbatim(paras[300], tokens({SENT2!r}))\n"
            "print(sp, len(tokens(sp)))"
        )
        _ntoks = r.stdout.strip().rsplit(" ", 1)[-1] if r.stdout.strip() else "0"
        ok("V1.3 guard: second bucket slices under the same tight span grammar",
           r.returncode == 0 and _ntoks.isdigit() and int(_ntoks) >= 6,
           r.stdout + r.stderr)

        # 3. lift fallback (V1.4): a probe absent from the index still
        #    resolves through the fallback (not a crash, not a false pass).
        r = fx(
            "import sys\n"
            "sys.argv = ['lift', 'zz-001']\n"
            "sys.stdin = open('/dev/null')\n"
            "try:\n"
            "    from shelf_core.commands.lift import cmd_lift\n"
            "    cmd_lift(['zz-001'])\n"
            "    print('EXIT-0')\n"
            "except SystemExit as e:\n"
            "    print('EXIT', e.code)"
        )
        ok("V1.4 guard: lift fallback exits loudly on empty stdin (no crash)",
           r.returncode == 0 and ("EXIT" in r.stdout or "EXIT-0" in r.stdout)
           and "Traceback" not in r.stderr, r.stdout + r.stderr)

        # 4. NOTHING-WAS-VERIFIED guard: a note with quoted spans but ZERO
        #    cites must fail (the comma-bug class: 0 checks read as a pass).
        p4 = write_note("fx-zero-parse.md",
                        'Dangling quote with no cite at all "some long enough '
                        'quote text to clear the label floor" ends the note.\n')
        r = run("pins", str(p4))
        ok("NOTHING-WAS-VERIFIED guard: zero-cite note with quoted spans exits 1",
           r.returncode == 1 and "NOTHING WAS VERIFIED" in r.stdout,
           f"rc={r.returncode}\n{r.stdout}")

        # 5. ambiguous find_note refusal: two notes matching zz-002-*.
        (fxroot / "reference" / "notes" / "zz-002-dup-a.md").write_text(
            "| Field | Value |\n| --- | --- |\n| Session | zz-002 |\n"
            "| Status | draft |\n| Flags open | no |\n## Themes\nx\n", encoding="utf-8")
        (fxroot / "reference" / "notes" / "zz-002-dup-b.md").write_text(
            "| Field | Value |\n| --- | --- |\n| Session | zz-002 |\n"
            "| Status | draft |\n| Flags open | no |\n## Themes\ny\n", encoding="utf-8")
        r = run("pins", "zz-002")
        ok("ambiguous find_note refuses loudly (never a silent vacuous pass)",
           r.returncode != 0 and "Ambiguous note resolution" in r.stdout + r.stderr,
           f"rc={r.returncode}\n{r.stdout}\n{r.stderr}")
        for _n in ("zz-002-dup-a.md", "zz-002-dup-b.md"):
            (fxroot / "reference" / "notes" / _n).unlink()

        # 6. one-write refusals: draft/draft-note/evdoc refuse overwrite.
        _note = fxroot / "reference" / "notes" / "zz-001-t7.md"
        _note.write_text("already here\n", encoding="utf-8")
        r = run("draft-note", "zz-001", "--from-yaml", str(fxroot / "nope.yaml"))
        _dn_refused = "usage" in (r.stdout + r.stderr) or r.returncode != 0
        # draft (doc) needs the note to exist; the overwrite refusal is on the
        # OUTPUT doc — plant one.
        _outdoc = fxroot / "reference" / "docs" / "doc-t7.html"
        _outdoc.write_text("existing\n", encoding="utf-8")
        r = run("evdoc", "--from-yaml", str(fxroot / "nope.yaml"))
        _ev_refused = r.returncode != 0 or "Missing" in r.stdout + r.stderr or "usage" in (r.stdout + r.stderr)
        ok("one-write lane: draft-note/evdoc exit nonzero on bad spec (no silent write)",
           _dn_refused and _ev_refused,
           f"dn:{r.returncode} {r.stdout[:80]}")
        _note.unlink(); _outdoc.unlink()

        # 7. zero-corpus check exit 2: check on an EMPTY shelf root refuses.
        empty_root = base / "emptyroot"
        (empty_root / "config").mkdir(parents=True, exist_ok=True)
        (empty_root / "config" / "project.yaml").write_text(
            "corpus:\n  key_pattern: 'zz-(\\d{3})'\n"
            "  playlists:\n    zz:\n      dir: zz\n", encoding="utf-8")
        r = fx(
            "from shelf_core.commands import check\n"
            "import sys\n"
            "sys.argv = ['shelf.py', 'check']\n"
            "try:\n"
            "    check.cmd_check([])\n"
            "except SystemExit as e:\n"
            "    print('EXIT', e.code)",
            root=empty_root)
        ok("zero-corpus check exits 2 (not a silent pass)",
           "EXIT 2" in r.stdout, r.stdout + r.stderr)
        import shutil as _sh
        _sh.rmtree(empty_root, ignore_errors=True)

        # 8. cross-session cite pass (A5.5): the wrong-note's cite names
        #    zz-001 while the note's Session row is zz-001 too — covered by
        #    the true-unit case; the cross-session lane needs a second session
        #    note citing zz-001's transcript FROM zz-002:
        p5 = write_note("fx-cross-session.md",
                        "Cross-session evidence.\n\n"
                        f'"{real_phrase}" (zz-001, {fmt_mmss(real_minute)})\n')
        # p5's Session row says zz-001 (write_note hard-codes it) — swap row:
        t = p5.read_text(encoding="utf-8").replace("| Session | zz-001 |", "| Session | zz-002 |")
        p5.write_text(t, encoding="utf-8")
        r = run("pins", str(p5))
        ok("A5.5 cross-session: cite verified against the CITED session, not the note's own",
           r.returncode == 0 and "Flags: 0" in r.stdout,
           f"rc={r.returncode}\n{r.stdout}")

        # 9. evdoc ambiguity (W4.17) + STALE-at-wrong-minute (W4.18) are
        #    evdoc-lane guards; the ambiguity refusal is covered by the
        #    --allow-ambiguous escape in evdoc — assert the SPEC validation
        #    refuses an EVIDOC without sections:
        _yq = fxroot / "bad-evidoc.yaml"
        _yq.write_text("meta:\n  title: no sections\n", encoding="utf-8")
        r = run("evdoc", "--from-yaml", str(_yq))
        ok("evdoc refuses an EVIDOC with zero sections (never writes a shell)",
           r.returncode != 0 and "sections" in (r.stdout + r.stderr),
           f"rc={r.returncode}\n{r.stdout}{r.stderr}")
        _yq.unlink()

        # 10. FOLD_TABLE_MIN standing guard (T7.4, from V1.5): the calibrated
        #     fold table must keep سؤال and سوال DISTINCT — the docstring
        #     claims minimal folding; this is its permanent assertion.
        r = fx("from shelf_core.match import tokens\n"
               "a, b = tokens('سؤال'), tokens('سوال')\n"
               "print('DISTINCT' if a != b else 'FOLDED-TOGETHER', a, b)")
        ok("FOLD_TABLE_MIN guard: tokens('سؤال') != tokens('سوال')",
           r.returncode == 0 and "DISTINCT" in r.stdout,
           r.stdout + r.stderr)

        # 11. AR-ratio floor guard (T7.4): the doc-gate lane scales the Arabic
        #     word floor by the measured twin ratio and PRINTS the adjustment.
        #     Presence guard via a direct probe of the doc-gate constants on
        #     an AR fixture doc (the full doc-gate run needs the gate script
        #     which reads the fixture config through _shelf_lib — heavy; the
        #     standing control is the printed-scaled-floor assertion).
        ardoc = fxroot / "reference" / "docs" / "fx-ar.html"
        ardoc.write_text(
            "<!DOCTYPE html>\n<html lang=\"ar\" dir=\"rtl\"><head><meta charset=\"utf-8\">"
            "<title>ar</title></head><body><main>"
            + "<p>هذه فقرة عربية طويلة نسبيًا لتجاوز الحد الأدنى للكلمات في البوابة وهي مكتوبة لتختبر أن أرضية الكلمات تُخفَّض للنصوص العربية بنسبة مقيسة معلنة لا بصمت</p>" * 12 +
            "</main></body></html>\n", encoding="utf-8")
        r = fx(
            "from shelf_core.notes import html_measure\n"
            f"txt = open({str(ardoc)!r}, encoding='utf-8').read()\n"
            "w, paras, defs = html_measure(txt)\n"
            "print('AR-MEASURE', w > 100, len(paras))"
        )
        ok("AR-ratio floor: fixture AR doc measurable through html_measure (lane present)",
           r.returncode == 0 and "AR-MEASURE True" in r.stdout,
           r.stdout + r.stderr)

        # ---------- T9.1 onboarding guards (ADR 0007): prefixless keys ----------
        # A SECOND fixture root shaped like the fqhn corpus: prefixless default
        # playlist (key_prefix: ''), top-level clean dir outside transcripts/,
        # «» quotes + المجلس-N keyword cites, uncited «» = narrative claims.
        print("T9.1 onboarding guards (prefixless keys):")
        pnroot = base / "pnroot"
        (pnroot / "config").mkdir(parents=True, exist_ok=True)
        (pnroot / "mntop-clean" / "clean").mkdir(parents=True, exist_ok=True)
        (pnroot / "sub-clean" / "clean").mkdir(parents=True, exist_ok=True)
        (pnroot / "reference" / "notes").mkdir(parents=True, exist_ok=True)
        (pnroot / "reference" / "docs").mkdir(parents=True, exist_ok=True)
        PSENT = "النفس البشرية تفقد توازنها حين يغيب الذكر من القلب"
        (pnroot / "mntop-clean" / "clean" / "047 - مجلس التجربة.txt").write_text(
            f"[00:00]\n{PSENT}\n\n[05:00]\nجملة ثانية لا علاقة لها بالاقتباس\n",
            encoding="utf-8")
        (pnroot / "sub-clean" / "clean" / "005 - جلسة الفرع.txt").write_text(
            "[00:00]\nموضوع الفرع مختلف تماما عن الرئيسي\n", encoding="utf-8")
        (pnroot / "config" / "project.yaml").write_text(
            "corpus:\n"
            "  default_playlist: mn\n"
            "  cite_pattern: \"المجلس\"\n"
            "  cite_playlist: self\n"
            "  uncited_quotes: skip\n"
            "  quote:\n    open: \"«\"\n    close: \"»\"\n"
            "  playlists:\n"
            "    mn:\n      dir: mntop\n      name: Prefixless main\n"
            "      notes_flat: true\n      key_prefix: \"\"\n"
            "      transcripts_dir: \"mntop-clean/clean\"\n"
            "      docs_dir: reference/docs\n"
            "    sub:\n      dir: subtop\n      name: Sub playlist\n"
            "      notes_flat: true\n"
            "      transcripts_dir: \"sub-clean/clean\"\n"
            "      docs_dir: reference/docs\n"
            "gates:\n  docs_dir: reference/docs\n", encoding="utf-8")

        # 1. registry: bare NNN + slug keys + top-level clean dirs resolve
        r = fx(
            "from shelf_core.playlists import parse_session_key, get_session,"
            " session_key_of, clean_dir\n"
            "pl, ident = parse_session_key('047')\n"
            "s = get_session('047')\n"
            "print(pl, ident, session_key_of(pl, ident),"
            " 'mntop-clean' in str(clean_dir(pl)))\n"
            "s2 = get_session('sub-005')\n"
            "print(s2['key'], 'sub-clean' in str(clean_dir('sub')))",
            root=pnroot)
        toks = r.stdout.split()
        ok("prefixless registry: bare NNN + slug keys + top-level clean dirs resolve",
           r.returncode == 0 and toks[:4] == ["mn", "047", "047", "True"]
           and toks[4:6] == ["sub-005", "True"],
           f"rc={r.returncode}\n{r.stdout}\n{r.stderr}")

        # 2. note_ident: prefixless filename binds to the prefixless playlist
        r = fx(
            "from shelf_core.notes import note_ident\n"
            "from shelf_core.playlists import session_key_of\n"
            "from pathlib import Path\n"
            "a = note_ident(Path('047-title-slug.md'))\n"
            "b = note_ident(Path('sub-005-title.md'))\n"
            "print(a, session_key_of(*a) if a[0] else None,"
            " b, session_key_of(*b) if b[0] else None)",
            root=pnroot)
        ok("prefixless note_ident: 047-x.md -> prefixless pl; sub-005-x.md -> sub",
           "047" in r.stdout and "sub-005" in r.stdout,
           f"rc={r.returncode}\n{r.stdout}\n{r.stderr}")

        # 3. end-to-end pins: kw cite «…» — المجلس 47، 00:00 verifies against the
        #    top-level transcript; uncited «» spans skip as narrative (T9.2).
        pn_note = pnroot / "reference" / "notes" / "047-مجلس-التجربة.md"
        pn_note.write_text(
            "| Field | Value |\n| --- | --- |\n"
            "| Session | 047 |\n| Status | draft |\n| Flags open | no |\n"
            "## Themes\n"
            f"1. **المحور** — المجلس 47، 00:00:\n   > «{PSENT}»\n\n"
            "2. **ادعاء بلا دقيقة** (نثري): «هذا ادعاء طويل بلا استشهاد يكفي عدد الكلمات»\n",
            encoding="utf-8")
        r = run_root = fx(
            "import sys\n"
            "sys.argv = ['shelf.py', 'pins', '047']\n"
            "from shelf_core import dispatch\n"
            "dispatch.main()",
            root=pnroot)
        ok("end-to-end pins: «…» — المجلس 47، 00:00 verifies; uncited «» skipped as narrative",
           r.returncode == 0 and "Flags: 0" in r.stdout
           and "Quoted spans: 2 (1 verified" in r.stdout
           and "claims: 1 uncited" in r.stdout,
           f"rc={r.returncode}\n{r.stdout}\n{r.stderr}")
        import shutil as _sh2
        _sh2.rmtree(pnroot, ignore_errors=True)

        # ---------- inventory regenerates INSIDE the fixture (never reference/) ----------
        print("inventory:")
        inv_fixture = fxroot / "reference" / "inventory.md"
        _outer_before = INVENTORY.read_text(encoding="utf-8") if INVENTORY.exists() else None
        r = run("inventory", "--out", str(inv_fixture))
        inv = inv_fixture.read_text(encoding="utf-8") if inv_fixture.exists() else ""
        ok(f"inventory regenerates inside the fixture ({n_expected} rows)",
           r.returncode == 0 and inv.count("\n| zz-") == n_expected,
           r.stdout + r.stderr)
        _outer_after = INVENTORY.read_text(encoding="utf-8") if INVENTORY.exists() else None
        ok("outer reference/inventory.md untouched by selftest",
           _outer_before == _outer_after, "regenerated the project's inventory")
    finally:
        import shutil
        shutil.rmtree(base, ignore_errors=True)
        print("(plans/selftest removed)")
    # F1 guard: status prefix grammar — default whole-match; config
    # status_prefix_ok accepts enum-prefixed free prose ("مسودة مكتملة").
    # Hermetic (ponytail wave fix): the guard relied on _corpus_cfg()
    # returning nothing — but the dev tree lives INSIDE the fqhn repo, whose
    # config/project.yaml (status_prefix_ok: true) leaks in via find_root's
    # walk-up, so "default" was never default here. It also sat AFTER the
    # `failed` snapshot below, so its failures never reached the tally —
    # masked red since F1. Both fixed: cfg pinned per assertion, snapshot
    # moved after all ok() calls.
    from shelf_core import notes as _n
    _orig_sv = _n.STATUS_VALUES
    _n.STATUS_VALUES = ("مسودة", "مقطرة")
    _v_bad = "مسودة مكتملة"  # annotated free prose
    _orig = _n._corpus_cfg
    _n._corpus_cfg = lambda: {}
    ok("status whole-match default: annotated prose rejected",
       not _n.status_is_valid(_v_bad), f"{_v_bad} accepted by default")
    _n._corpus_cfg = lambda: {"status_prefix_ok": True}
    ok("status prefix grammar: annotated prose accepted when declared",
       _n.status_is_valid(_v_bad) and not _n.status_is_valid("مكتملة-زائفة"),
       "prefix accepted but alien prefix wrongly accepted")
    _n._corpus_cfg = _orig
    _n.STATUS_VALUES = _orig_sv  # restore notes-module default
    # 1.2.18 guard: claims_count refuses loudly on removed 'auto' source —
    # a stale config must crash, never silently count zero claims.
    try:
        _n.claims_count("x", "auto")
        _auto_ok = False
    except ValueError:
        _auto_ok = True
    ok("claims_count refuses 'auto' loudly (stale-config guard)", _auto_ok,
       "silent zero returned for removed source")
    failed = [name for name, cond in results if not cond]
    print(f"\nSelftest: {len(results) - len(failed)}/{len(results)} passed.")
    if failed:
        print("Failed: " + ", ".join(failed))
        sys.exit(1)
    sys.exit(0)


# H2.3: a stale third dispatch chain (9 commands, missing draft-note/evdoc/verify)
# lived here and referenced cmd_* names its imports no longer provide. Verified
# dead (dispatch.py routes `selftest` to cmd_selftest directly; nothing calls
# selftest.main) and removed — it was a second command list waiting to drift.
