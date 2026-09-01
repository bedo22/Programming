#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rendertooldocs — B7 port of scripts/render-tool-docs.py as a registry command
(`shelf render-tool-docs [--out references/tools]`).

D8.14 renderer (ADR 0006). Generates references/tools/<name>.md per tool FROM
the registry's --describe output — the same registry the dispatch consumes.
Never hand-edit the generated pages (regenerate instead); hand-maintained
per-file doc trees are a second source of truth and under "doc wins" they are
dangerous.

Differences from the script (output-preserving):
- ROOT was `Path(__file__).parents[1]` (module-location) → find_root().
- `subprocess tools/shelf.py <name> --describe` → in-process describe_command
  with stdout capture (same JSON, no process spawn, no tools/ dependency —
  this command now works on a shelf AFTER the Phase C tools/ deletion).
- The generated page wording (shelf.py references) is kept byte-identical to
  the script's output during the B-wave battery; the wording modernization to
  `shelf <name>` happens at the Phase C cutover with its own receipt.
"""
import contextlib
import io
import json
import sys
from pathlib import Path

from shelf_core import gatelib as lib


def _describe_json(name: str) -> str:
    from shelf_core.dispatch import describe_command
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        describe_command(name)
    return buf.getvalue()


def cmd_render_tool_docs(argv=None):
    argv = list(argv or [])
    ROOT = lib.find_root()
    out_dir = Path(argv[argv.index("--out") + 1]) if "--out" in argv \
        else ROOT / "references" / "tools"
    out_dir.mkdir(parents=True, exist_ok=True)
    # command list from the registry itself (one source of truth)
    from shelf_core.registry import COMMANDS
    wrote = []
    for name in sorted(COMMANDS):
        try:
            d = json.loads(_describe_json(name))
        except SystemExit as e:
            print(f"SKIP {name}: --describe exited {e.code}")
            continue
        except Exception as e:
            print(f"SKIP {name}: --describe failed: {str(e)[:80]}")
            continue
        lines = [f"# `{name}` — {d['help']}", "",
                 "> GENERATED from `shelf.py " + name + " --describe` (ADR 0006) — do not hand-edit;",
                 "> regenerate with `scripts/render-tool-docs.py`.", ""]
        lines += ["## Usage", ""]
        if d["usage_args"]:
            lines.append(f"`shelf.py {name} {' '.join(a for a in d['usage_args'])}`")
        else:
            lines.append(f"`shelf.py {name}`")
        lines += ["", "## Checks performed", ""]
        lines += [f"- {c}" for c in d["checks"]] or ["- (none — see help)"]
        lines += ["", "## Exit codes", ""]
        lines += [f"- `{code}` — {what}" for code, what in sorted(d["exits"].items())]
        if d["pitfalls"]:
            lines += ["", "## PITFALLS taxonomy tags", ""]
            lines += [f"- {p}" for p in d["pitfalls"]]
        if d["adrs"]:
            lines += ["", "## ADR links", ""]
            lines += [f"- `references/decisions/{a}-*.md`" for a in d["adrs"]]
        lines.append("")
        (out_dir / f"{name}.md").write_text("\n".join(lines), encoding="utf-8")
        wrote.append(name)
    print(f"rendered {len(wrote)} tool pages -> {out_dir}")
    print("reminder: pages are generated; regenerate after any registry change"
          " (`git -C <shelf> status` will show drift if you forgot)")
    return 0
