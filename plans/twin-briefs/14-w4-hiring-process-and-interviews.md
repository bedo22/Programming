# Twin brief — hiring-process-and-interviews (Wave 4)

## Task (TRANSLATE mode — no AR twin exists)
Produce the full Arabic twin + a per-doc hygiene map for `reference/hiring-process-and-interviews.html`.
Deliverables (ONLY inside `/tmp/twin-hiring-process-and-interviews/`):
- `en.html` — copy of the EN file (start: `cp reference/hiring-process-and-interviews.html /tmp/twin-hiring-process-and-interviews/en.html`)
- `ar.html` — your full AR twin (house template)
- `map.json` — `{"WANT":{...},"FOLDS":[[old,new],...]}` — WANT values are BARE ids, NO `#` prefix
- `report.md` — change report: sections translated, table rows, pipeline counts, gate result, EVERY WANT/FOLD decision with a one-line justification, unresolved tokens listed as `pending`

## Facts (from main-session survey)
- visible h2s (NH): 21 | chars ≈ 55451
- §-tokens outside pre/links: §1×5 §2×3 §3×15 §4×7 §5×5 §6×4 §7×3 §9×3 §10×6 §11×6 (57 total)
- numbered h2s 1–11 remain; ALL §-tokens are self-references to those sections — WANT maps each number to its section id via title-exact match (e.g. §3 → sec-…screening-call)

## Mandatory reading (before writing any Arabic)
1. `~/.agents/skills/translate-to-arabic/SKILL.md` — TRANSLATE mode + rules (one file at a time; house rules link to reference-doc skill)
2. `~/.agents/skills/reference-doc/SKILL.md` — house template rules
3. `plans/twin-briefs/00-REFERENCE.md` — dfn terminology gate + target anchor index
4. Exemplar for structure/voice/ratio: `reference/ar/react-2024-and-beyond.html`

## Steps
1. Read the EN file completely (structure, then every line).
2. Terminology gate: every concept covered by a dfn in 00-REFERENCE.md uses EXACTLY that Arabic form; a needed term absent from the dfn list → STOP, list it in report.md, NEVER invent.
3. Write the whole AR twin in one pass: `lang="ar" dir="rtl"`, asset paths `../../assets/…`, lang-switch header line `../hiring-process-and-interviews.html (English)`, h2 titles translated, **h2 ids = EN's ids verbatim** (mirror), tables row-for-row, `<pre>` blocks verbatim, `&amp;` escaping. Too big for one write → parts in /tmp, concatenate, size-check each part. Full translation (ratio band 0.75–0.97): do NOT abbreviate.
4. Hygiene on YOUR copies only:
   `python3 ~/.agents/skills/translate-to-arabic/scripts/twin-pipeline.py /tmp/twin-hiring-process-and-interviews/en.html /tmp/twin-hiring-process-and-interviews/ar.html 21 --map /tmp/twin-hiring-process-and-interviews/map.json --strict-folds`
   Fold rules: §-token → `<a href="…">§N</a>`; bare `§N` → WANT (target id, verified by READING the target section — title-exact match wins over the legacy number); dotted `§4.1`-style → FOLD to parent h2 anchor; cross-doc: `./doc.html#id` when the target has a twin, `../doc.html#id` when EN-only; fold olds VERBATIM, sorted by length DESC; every WANT id must exist in 00-REFERENCE.md.
5. Gate: `python3 ~/.agents/skills/translate-to-arabic/scripts/verify-twins.py /tmp/twin-hiring-process-and-interviews/en.html /tmp/twin-hiring-process-and-interviews/ar.html hiring-process-and-interviews` → target ALL GATES PASSED; an out-of-band ratio is a recorded-exception flag → note density reasoning in report.md.
6. report.md last, then STOP (no further work, no cleanup of /tmp/twin-hiring-process-and-interviews/).

## Non-negotiable rules
- NEVER touch git (no add/commit/tag/branch/checkout) — the main session owns the repo.
- NEVER modify `reference/`, `reference/ar/`, `maps/`, `PROGRESS.md`, `AGENTS.md` — read-only except your cp source.
- No heading numerals, ever. No `§` left outside links after step 4.
- h2 ids identical EN↔AR; phantom `<h2>` inside `<pre>` stay untouched.
- Mojibake safety: verify with `python3 -c "open('/tmp/twin-hiring-process-and-interviews/ar.html',encoding='utf-8').read()"` — never judge Arabic by terminal echo.

## Resilience (provider hiccups — v34+)
- Write each AR part to /tmp as soon as it is complete — NEVER hold the whole doc in one generation.
- On `403 server_error` / `Stream ended without finish_reason`: pause ~60s, retry ONCE. If it recurs 3+ times: save every completed part, write a `STATUS:` line at the top of report.md (where you stopped, what remains), and STOP. The orchestrator resumes you; do not keep hammering.
- Losing one stream costs one part — keep parts small (2–3 h2s) on docs > 20 h2.

## Fold pre-check + ratio policy (v40+)
- BEFORE the first pipeline run: verify every fold old-string — `python3 -c "import json;m=json.load(open('map.json'));en=open('en.html').read();ar=open('ar.html').read();print([o for o,_ in m['FOLDS'] if o not in en and o not in ar] or 'all folds match')"`. Fix any phantom old BEFORE running twin-pipeline; a strict-folds failure mid-run costs most when it cascades into re-translation.
- A ratio FLAG with a recorded exception is a VALID terminal state — NEVER pad/rewrite to hit the band. Density reasoning = run `python3 ~/.agents/skills/translate-to-arabic/scripts/density-audit.py en.html ar.html`, paste the per-section table into report.md, eyeball ONLY flagged outliers, then stop.
