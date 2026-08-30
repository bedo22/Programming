#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""commands/selftest — moved from _legacy.py (batch)."""
from __future__ import annotations
import sys, re
from pathlib import Path
try:
    from shelf_core.playlists import *
    from shelf_core.transcript import *
    from shelf_core.notes import *
    from shelf_core.citation import *
    from shelf_core.match import tokens, subseq
    from shelf_core.config import ROOT, REF
    from shelf_core.citation import *
except ImportError:
    from playlists import *  # type: ignore
    from transcript import *  # type: ignore
    from notes import *  # type: ignore
    from citation import *  # type: ignore
    from match import tokens, subseq  # type: ignore
    from config import ROOT, REF  # type: ignore
def cmd_selftest():
    """Fixture-based self test under plans/selftest/ (removed afterwards).
    Never touches reference/ except regenerating reference/inventory.md."""
    base = ROOT / "plans" / "selftest"
    results = []

    def ok(name, cond, detail=""):
        results.append((name, bool(cond)))
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}"
              + (f" — {detail}" if detail and not cond else ""))

    try:
        fx = base / "fixtures"
        fx.mkdir(parents=True, exist_ok=True)
        sessions = load_sessions()
        counts = {pl: sum(1 for s in sessions if s["pl"] == pl)
                  for pl in ("cs", "ex", "rr")}
        print("registry:")
        ok("94 cs sessions", counts["cs"] == 94, str(counts))
        ok("6 ex sessions", counts["ex"] == 6, str(counts))
        ok("423 rr sessions", counts["rr"] == 423, str(counts))

        import subprocess

        def run(*args):
            return subprocess.run(
                [sys.executable, str(ROOT / "tools" / "shelf.py"), *args],
                capture_output=True, text=True, cwd=str(ROOT))

        print("citation grammar:")
        paras = clean_paragraphs("cs-002")
        assert paras, "cs-002 buckets missing"
        real_phrase = real_minute = None
        for m in sorted(paras):
            units = [u for u in re.split(r"(?<=[.!?])\s+", paras[m])
                     if len(tokens(u)) >= 6]
            if units:
                real_phrase = _slice_verbatim(paras[m], tokens(units[0]))
                real_minute = m
                break
        assert real_phrase, "no usable phrase in cs-002"
        true_unit = f'"{real_phrase}" (cs-002, {fmt_mmss(real_minute)})'
        wrong_min = fmt_mmss((real_minute + 300) % 3600)

        def write_note(name, body):
            p = fx / name
            p.write_text(
                "| Field | Value |\n| --- | --- |\n"
                f"| Source file | `{get_session('cs-002')['rel']}` |\n"
                "| Session | cs-002 |\n"
                "| Playlist | Common Sense Investing |\n"
                "| Block | Foundations |\n| Type | video essay |\n"
                "| Status | draft |\n| Flags open | no |\n"
                "## Segment map\nTODO: distill from the transcript\n"
                "## Themes\n" + body +
                "\n## Papers cited\n- none\n"
                "## Fidelity flags\n\n## Fidelity log\n", encoding="utf-8")
            return p

        p1 = write_note("fx-true-only.md",
                        f"Intro.\n\n{true_unit}\n")
        r = run("pins", str(p1))
        ok("true quote passes pins (exit 0)",
           r.returncode == 0 and "Flags: 0" in r.stdout, r.stdout + r.stderr)

        p2 = write_note("fx-wrong-minute.md",
                        f"Intro.\n\n{true_unit}\n\nSecond.\n\n"
                        f'"{real_phrase}" (cs-002, {wrong_min})\n')
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
                        "Uncited case: \"cash is a poor hedge against falling "
                        "expected returns for long term investors\" ends here.\n")
        r = run("pins", str(p3))
        ok("4+-token uncited quote flags; single quotes never scanned",
           r.returncode == 1 and "UNCITED QUOTE" in r.stdout
           and "Flags: 1" in r.stdout
           and "do not scan me" not in r.stdout,
           f"rc={r.returncode}\n{r.stdout}")

        doc_good = fx / "fx-doc-good.html"
        doc_good.write_text(f"""<!DOCTYPE html>
<html lang="en" dir="ltr"><head><meta charset="utf-8"><title>fixture</title></head>
<body><main><p>Ben argues that "{real_phrase}"
<span class="cite">(cs-002, {fmt_mmss(real_minute)})</span></p>
<p><a href="#later">anchor</a> <span id="later">ok</span></p>
</main></body></html>\n""", encoding="utf-8")
        r = run("check", str(doc_good))
        ok("doc with good quote passes check (exit 0)",
           r.returncode == 0 and "failed check" not in r.stdout,
           f"rc={r.returncode}\n{r.stdout}\n{r.stderr}")

        doc_bad = fx / "fx-doc-fabricated.html"
        doc_bad.write_text(f"""<!DOCTYPE html>
<html lang="en" dir="ltr"><head><meta charset="utf-8"><title>fixture</title></head>
<body><main><p>The study found "purple elephants trade options through the
Federal Reserve window at midnight" <span class="cite">(cs-002,
{fmt_mmss(real_minute)})</span></p></main></body></html>\n""", encoding="utf-8")
        r = run("check", str(doc_bad))
        ok("fabricated quote fails check with source span printed (exit 1)",
           r.returncode == 1 and "not found anywhere" in r.stdout
           and "copy-paste this" in r.stdout,
           f"rc={r.returncode}\n{r.stdout}\n{r.stderr}")

        r = run("inventory")
        inv = INVENTORY.read_text(encoding="utf-8") if INVENTORY.exists() else ""
        ok("inventory covers 94 cs + 6 ex + 423 rr rows",
           r.returncode == 0 and inv.count("\n| cs-") == 94
           and inv.count("\n| ex-") == 6 and inv.count("\n| rr-") == 423,
           r.stdout + r.stderr)
    finally:
        import shutil
        shutil.rmtree(base, ignore_errors=True)
        print("(plans/selftest removed)")
    failed = [name for name, cond in results if not cond]
    print(f"\nSelftest: {len(results) - len(failed)}/{len(results)} passed.")
    if failed:
        print("Failed: " + ", ".join(failed))
        sys.exit(1)
    sys.exit(0)


# ---------------- main ----------------

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "inventory":
        cmd_inventory()
    elif cmd == "lines":
        cmd_lines(sys.argv[2:])
    elif cmd == "lift":
        cmd_lift(sys.argv[2:])
    elif cmd == "pins":
        cmd_pins(sys.argv[2:])
    elif cmd == "scaffold":
        cmd_scaffold(sys.argv[2:])
    elif cmd == "draft":
        cmd_draft(sys.argv[2:])
    elif cmd == "check":
        cmd_check(sys.argv[2:])
    elif cmd == "quotes":
        cmd_quotes(sys.argv[2:])
    elif cmd == "selftest":
        cmd_selftest()
    else:
        sys.exit(f"Unknown command: {cmd} — run `python3 tools/shelf.py` for usage")


