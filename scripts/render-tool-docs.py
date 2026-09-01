#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render-tool-docs.py — D8.14 renderer (ADR 0006).

Generates references/tools/<name>.md per tool FROM `tools/shelf.py <name>
--describe` output — the same registry the dispatch consumes. Never hand-edit
the generated pages (regenerate instead); hand-maintained per-file doc trees
are a second source of truth and under "doc wins" they are dangerous.

Usage: python3 scripts/render-tool-docs.py [--out references/tools]
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELF = ROOT / "tools" / "shelf.py"


def main(argv=None):
    argv = list(argv or [])
    out_dir = Path(argv[argv.index("--out") + 1]) if "--out" in argv \
        else ROOT / "references" / "tools"
    out_dir.mkdir(parents=True, exist_ok=True)
    # command list from the registry itself (one source of truth)
    sys.path.insert(0, str(ROOT / "tools"))
    from shelf_core.registry import COMMANDS
    wrote = []
    for name in sorted(COMMANDS):
        r = subprocess.run([sys.executable, str(SHELF), name, "--describe"],
                            capture_output=True, text=True, cwd=str(ROOT))
        if r.returncode != 0:
            print(f"SKIP {name}: --describe exited {r.returncode}: {r.stderr.strip()[:80]}")
            continue
        d = json.loads(r.stdout)
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


if __name__ == "__main__":
    sys.exit(main())
