# Twin brief — dotnet-and-the-enterprise-lane (Wave 1)

## Task (TRANSLATE mode — no AR twin exists)
Produce the full Arabic twin + a per-doc hygiene map for `reference/dotnet-and-the-enterprise-lane.html`.
Deliverables (ONLY inside `/tmp/twin-dotnet-and-the-enterprise-lane/`):
- `en.html` — copy of the EN file (start: `cp reference/dotnet-and-the-enterprise-lane.html /tmp/twin-dotnet-and-the-enterprise-lane/en.html`)
- `ar.html` — your full AR twin (house template)
- `map.json` — `{"WANT":{...},"FOLDS":[[old,new],...]}` — WANT values are BARE ids, NO `#` prefix
- `report.md` — change report: sections translated, table rows, pipeline counts, gate result, EVERY WANT/FOLD decision with a one-line justification, unresolved tokens listed as `pending`

## Facts (from main-session survey)
- visible h2s (NH): 15 | numbered h2s still in file: 0 | chars ≈ 24181
- §-tokens in body text (outside <pre> and existing links): 1×6, 1b×1, 1d×2, 1e×4

## Mandatory reading (before writing any Arabic)
1. `~/.agents/skills/translate-to-arabic/SKILL.md` — TRANSLATE mode + rules (one file at a time; house rules link to reference-doc skill)
2. `~/.agents/skills/reference-doc/SKILL.md` — house template rules
3. `plans/twin-briefs/00-REFERENCE.md` — dfn terminology gate + target anchor index
4. Exemplar for structure/voice/ratio: `reference/ar/react-2024-and-beyond.html`

## Steps
1. Read the EN file completely (structure, then every line).
2. Terminology gate: every concept covered by a dfn in 00-REFERENCE.md uses EXACTLY that Arabic form; a needed term absent from the dfn list → STOP, list it in report.md, NEVER invent.
3. Write the whole AR twin in one pass: `lang="ar" dir="rtl"`, asset paths `../../assets/…`, lang-switch header line `../dotnet-and-the-enterprise-lane.html (English)`, h2 titles translated, **h2 ids = EN's ids verbatim** (mirror), tables row-for-row, `<pre>` blocks verbatim, `&amp;` escaping. Too big for one write → parts in /tmp, concatenate, size-check each part. Full translation (ratio band 0.75–0.97): do NOT abbreviate.
4. Hygiene on YOUR copies only:
   `python3 ~/.agents/skills/translate-to-arabic/scripts/twin-pipeline.py /tmp/twin-dotnet-and-the-enterprise-lane/en.html /tmp/twin-dotnet-and-the-enterprise-lane/ar.html 15 --map /tmp/twin-dotnet-and-the-enterprise-lane/map.json --strict-folds`
   Fold rules: §-token → `<a href="…">§N</a>`; bare `§N` → WANT (target id, verified by READING the target section — title-exact match wins over the legacy number); dotted `§4.1`-style → FOLD to parent h2 anchor; cross-doc: `./doc.html#id` when the target has a twin, `../doc.html#id` when EN-only; fold olds VERBATIM, sorted by length DESC; every WANT id must exist in 00-REFERENCE.md.
5. Gate: `python3 ~/.agents/skills/translate-to-arabic/scripts/verify-twins.py /tmp/twin-dotnet-and-the-enterprise-lane/en.html /tmp/twin-dotnet-and-the-enterprise-lane/ar.html dotnet-and-the-enterprise-lane` → target ALL GATES PASSED; an out-of-band ratio is a recorded-exception flag → note density reasoning in report.md.
6. report.md last, then STOP (no further work, no cleanup of /tmp/twin-dotnet-and-the-enterprise-lane/).

## Non-negotiable rules
- NEVER touch git (no add/commit/tag/branch/checkout) — the main session owns the repo.
- NEVER modify `reference/`, `reference/ar/`, `maps/`, `PROGRESS.md`, `AGENTS.md` — read-only except your cp source.
- No heading numerals, ever. No `§` left outside links after step 4.
- h2 ids identical EN↔AR; phantom `<h2>` inside `<pre>` stay untouched.
- Mojibake safety: verify with `python3 -c "open('/tmp/twin-dotnet-and-the-enterprise-lane/ar.html',encoding='utf-8').read()"` — never judge Arabic by terminal echo.
