# Twin brief — observability-and-operations (Wave 2)

## Task (TRANSLATE mode — no AR twin exists)
Produce the full Arabic twin + a per-doc hygiene map for `reference/observability-and-operations.html`.
Deliverables (ONLY inside `/tmp/twin-observability-and-operations/`):
- `en.html` — copy of the EN file (start: `cp reference/observability-and-operations.html /tmp/twin-observability-and-operations/en.html`)
- `ar.html` — your full AR twin (house template)
- `map.json` — `{"WANT":{...},"FOLDS":[[old,new],...]}` — WANT values are BARE ids, NO `#` prefix
- `report.md` — change report: sections translated, table rows, pipeline counts, gate result, EVERY WANT/FOLD decision with a one-line justification, unresolved tokens listed as `pending`

## Facts (from main-session survey)
- visible h2s (NH): 28 | numbered h2s still in file: 28 | chars ≈ 47366
- §-tokens in body text (outside <pre> and existing links): 1×1, 10.×1, 11×1, 11.×1, 1b×1, 1c×1, 1e×6, 1f×6, 2×8, 3×3, 3.×1, 4×3, 4.×1, 5×7, 6×4, 6b×1, 6e×1, 6f×6, 6f.×1, 6g×8, 7×4, 7.×1, 7b×1, 7c×1, 7h×1, 7i×1, 7j×1, 8×3, 8b×2, 9×2, 9.×2, 9d×1, 9h×4, 9i.×1

## Mandatory reading (before writing any Arabic)
1. `~/.agents/skills/translate-to-arabic/SKILL.md` — TRANSLATE mode + rules (one file at a time; house rules link to reference-doc skill)
2. `~/.agents/skills/reference-doc/SKILL.md` — house template rules
3. `plans/twin-briefs/00-REFERENCE.md` — dfn terminology gate + target anchor index
4. Exemplar for structure/voice/ratio: `reference/ar/react-2024-and-beyond.html`

## Steps
1. Read the EN file completely (structure, then every line).
2. Terminology gate: every concept covered by a dfn in 00-REFERENCE.md uses EXACTLY that Arabic form; a needed term absent from the dfn list → STOP, list it in report.md, NEVER invent.
3. Write the whole AR twin in one pass: `lang="ar" dir="rtl"`, asset paths `../../assets/…`, lang-switch header line `../observability-and-operations.html (English)`, h2 titles translated, **h2 ids = EN's ids verbatim** (mirror), tables row-for-row, `<pre>` blocks verbatim, `&amp;` escaping. Too big for one write → parts in /tmp, concatenate, size-check each part. Full translation (ratio band 0.75–0.97): do NOT abbreviate.
4. Hygiene on YOUR copies only:
   `python3 ~/.agents/skills/translate-to-arabic/scripts/twin-pipeline.py /tmp/twin-observability-and-operations/en.html /tmp/twin-observability-and-operations/ar.html 28 --map /tmp/twin-observability-and-operations/map.json --strict-folds`
   Fold rules: §-token → `<a href="…">§N</a>`; bare `§N` → WANT (target id, verified by READING the target section — title-exact match wins over the legacy number); dotted `§4.1`-style → FOLD to parent h2 anchor; cross-doc: `./doc.html#id` when the target has a twin, `../doc.html#id` when EN-only; fold olds VERBATIM, sorted by length DESC; every WANT id must exist in 00-REFERENCE.md.
5. Gate: `python3 ~/.agents/skills/translate-to-arabic/scripts/verify-twins.py /tmp/twin-observability-and-operations/en.html /tmp/twin-observability-and-operations/ar.html observability-and-operations` → target ALL GATES PASSED; an out-of-band ratio is a recorded-exception flag → note density reasoning in report.md.
6. report.md last, then STOP (no further work, no cleanup of /tmp/twin-observability-and-operations/).

## Non-negotiable rules
- NEVER touch git (no add/commit/tag/branch/checkout) — the main session owns the repo.
- NEVER modify `reference/`, `reference/ar/`, `maps/`, `PROGRESS.md`, `AGENTS.md` — read-only except your cp source.
- No heading numerals, ever. No `§` left outside links after step 4.
- h2 ids identical EN↔AR; phantom `<h2>` inside `<pre>` stay untouched.
- Mojibake safety: verify with `python3 -c "open('/tmp/twin-observability-and-operations/ar.html',encoding='utf-8').read()"` — never judge Arabic by terminal echo.

## Resilience (provider hiccups — v34+)
- Write each AR part to /tmp as soon as it is complete — NEVER hold the whole doc in one generation.
- On `403 server_error` / `Stream ended without finish_reason`: pause ~60s, retry ONCE. If it recurs 3+ times: save every completed part, write a `STATUS:` line at the top of report.md (where you stopped, what remains), and STOP. The orchestrator resumes you; do not keep hammering.
- Losing one stream costs one part — keep parts small (2–3 h2s) on docs > 20 h2.

## Fold pre-check + ratio policy (v40+)
- BEFORE the first pipeline run: verify every fold old-string — `python3 -c "import json;m=json.load(open('map.json'));en=open('en.html').read();ar=open('ar.html').read();print([o for o,_ in m['FOLDS'] if o not in en and o not in ar] or 'all folds match')"`. Fix any phantom old BEFORE running twin-pipeline; a strict-folds failure mid-run costs most when it cascades into re-translation.
- A ratio FLAG with a recorded exception is a VALID terminal state — NEVER pad/rewrite to hit the band. Report the density reasoning and stop.
