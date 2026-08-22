# SHELF CAMPAIGN — PLAN v4 (autonomous, 2026-08-21)

Supersedes v3. Purpose: let a goal-mode agent run the ENTIRE shelf without user input.
Every decision rule is written here; if a situation isn't covered, the agent logs it in
goal.md under "Open questions" and moves to the next doc rather than blocking.

Mechanisms referenced (read once per session):
- `plans/source-digestion-workflow.md` — pipeline
- `plans/credibility.md` — T1/T2/T3 claim tiers
- skill `improve-doc` v1.4+: `sources.md`, `insight.md`, `digest-coverage.py`, `doc-profile.py`
- `translate-to-arabic` skill: twin pipeline + `verify-twins.py`
- Host constitution: AGENTS.md (schema rules — non-negotiable)

## COMMIT AUTHORITY

Commits RESUME automatically while this plan executes under goal mode:
`Checkpoint vN: <summary>` + tag `vN`, gates green before every commit.
Never commit `Archive/What's missing.txt`. If the user suspends goal mode,
return to stage-only until told otherwise.

## SESSION PROTOCOL (every session)

1. Read `goal.md` progress log tail + this plan's status table.
2. Pick first doc whose Track A or B is not ✅.
3. Run its remaining track(s). One doc at a time; finish or reach a clean pause
   (gates green, log line written) before switching.
4. Append progress-log line; tick the status table; commit + tag.
5. If blocked >1 doc in a row by the same cause → stop, write diagnosis in goal.md.

## PER-DOC PIPELINE

### Track A — Digestion (source-grounding)
1. Seed from doc `.cite` (none → obvious primaries). Fetch ALL live; mirrors allowed;
   failures recorded. Dead cited link → replace with fetch-verified accessible primary
   (keep old attribution), mark replacement note.
2. Unified Digestion Architecture (skill sources.md UDA v1) — three artifacts:
   a. `reference/sources/<short-key>.md` source-key distillation (house `_TEMPLATE.md`:
      Identity w/ verified DOI+dates, claims-from-docs, key findings w/ quotes,
      Does-NOT-support caveats, related-digests graph, verification history);
      primaries get teaching-grade prose. Grep-first reuse.
   b. Thin doc shell `reference/digests/<stem>.md`: fetch ledger, coverage matrix
      over every visible h2, Gaps (≥3 hunts before `†`), Δ ids → source keys.
   c. Ecosystem: SOURCE-ACCESS.md + digest-coverage.py gate + maintenance duties
      (claims-list updates on consumption; migration debt tracked in skill sources.md).
3. Gate: `digest-coverage.py <doc> <digest>` exit 0.
4. Wire digest link into cite section, EN (`../digests/<stem>.md`) + AR
   (`../../digests/<stem>.md`, translated label).
5. Sweep doc-vs-digest: confirmed / hunted / `†`-marked. **Never delete** unsourced
   content; specific numbers that stay unlocated after hunts get `†`.

### Track B — Value pass (only after A)
1. Full read (mandatory even if profiled before). Classify Diátaxis type.
2. Author from Δ deltas. Declined deltas: skip WITH reason in digest. No silent drops.
3. **Content-type disposition table (mandatory, goes in the ledger row):**
   every one of the seven types gets an explicit disposition — ADD (citing its
   delta id), EXISTS=pre (point at where), or SKIP (justified by Diátaxis type +
   insight tests, not vibes):

   | Type | Core for which Diátaxis types |
   |---|---|
   | R15 Failure diagnostics ("common problems") | ALL — how-to, guide, reference |
   | R16 Search vocabulary / keywords | ALL — especially reference & guide |
   | R18 Decision points + defaults | how-to & guide (task docs) |
   | R19 Calibration numbers | ALL — wherever a qualitative claim has magnitude |
   | R14 Leverage map | guides & explanations |
   | R17 Inversions | history/theory-bearing docs |
   | R20 War stories w/ mechanism | guides; host-context or labeled illustrative |

   Rules: R15 and R16 are near-universal — SKIP requires the strongest justification
   (typically: exists=pre at benchmark density, verified in sweep). A doc whose
   Diátaxis type makes a type structurally inapplicable (e.g., inversions in a pure
   reference sheet) skips cleanly. The dispositions together ARE the value pass;
   "minimum two additions" remains as floor, not as permission to ignore the rest.
4. Per-type quality bars come from the skill's `diataxis.md` digest (type compass +
   quality expectations); the digest's Δ items are the raw material for ADDs.
4. Mirror everything to AR twin (pipeline; direct patches for prose, splice for structure).
5. Gates: `verify-twins.py` ALL PASSED + parse integrity both twins + coverage gate still 0.
6. Ledger row in `reference/Archive/rules-compliance.md` (R-id 4-status notation +
   new-claims tiering + the seven-disposition table). Progress log line. Commit + tag.

## TERMINAL STATES — never ask the user, just record and move on
- Ratio/h3 parity exceptions already recorded → VALID final state. Never pad.
- Doc diagnosed benchmark-grade → Track B = "confirmed, N/A" row. That IS success.
- Claim unlocatable after 3 hunts → `†` marker + Gaps row. Done.
- Contradictory authoritative sources → prefer spec/RFC over blog; record tension in digest.
- Source proves doc content WRONG → correct the doc (this overrides preservation),
  note correction in digest + ledger.
- Tool-catalog volatility → leave as-is unless touched by an edit; volatile claims there
  get hedges, not rewrites.
- Glossary: Track A only (it derives from other docs); do LAST.
- index.html: excluded entirely.

## WAVE 1.5 — KEY HARVEST (inserted before Wave 2)

The four pre-UDA shells ground their extractions in /tmp snapshots that will not
survive indefinitely. Before Wave 2, convert that knowledge into permanent source
keys (`reference/sources/`), re-fetching only where a snapshot is lost. Raw material:
the shells' triage entries + the snapshots themselves. Target ~20 keys across the
four docs; each key follows _TEMPLATE.md (distillation-grade for primaries).
Shells are NOT redone — they already comply; only their Δ pointers gain key targets.
Order: api-design keys → hdt keys → std keys → system-design keys.

## DOC ORDER (interleave A+B per doc before next)

Wave 1 — alumni: mechanical layer pre-clean, but FULL A+B like everyone else.
Prior passes (v60–77) count ONLY as Phase-A hygiene credit (numerals/corruption
already handled). Their Track B is fresh: author from THIS doc's extraction deltas,
minimum two substantive additions per the normal rule. Prior template-era additions
(vocabulary blocks, teacher sections, markers) are existing content — swept and
verified during A like everything else; they do NOT count toward B's minimum.
1 api-design ✅(pilot — the only completed A+B) · 2 how-developers-think-frontend ·
3 software-testing-and-debugging · 4 system-design · 5 javascript-the-language ·
6 class-to-hooks-paradigm-shift · 7 html-and-css · 8 what-is-state-prequel ·
9 ui-ux-web-design · 10 javascript-across-stacks

Wave 2 — high-deficiency, full A+B:
11 react-2024-and-beyond ✅v90 · 12 observability-and-operations ✅v91-92 ·
13 income-stream-landscape ⚠️RECLASSIFIED: interactive personal worksheet
(localStorage cells s0–s3), not a reference doc — light factual Track A only,
user data OFF-LIMITS, flagged for async review · 14 problem-solving ·
15 cs-and-software-engineering ·
16 version-control-ci-cd-deployment · 17 software-development-process ·
18 data-modeling-and-databases · 19 sql-and-postgresql · 20 security-and-threat-modeling

Wave 3 — remaining core:
21 backend-engineering · 22 full-stack · 23 frontend-camps-survey · 24 nextjs-deep-dive ·
25 angular-evolution · 26 algorithms-and-data-structures · 27 design-thinking ·
28 beyond-the-browser · 29 terminal-and-deployment-substrate · 30 terminal-applications

Wave 4 — career/business tier (lighter sources; interviews/blog posts acceptable as
supporting tier):
31 freelance-web-practice · 32 frontend-income-markets · 33 income-stream-landscape
(dup guard: if already done at #13, mark here) · 34 hiring-process-and-interviews ·
35 product-strategy · 36 product-shapes · 37 payments-and-commerce · 38 open-source ·
39 recurring-fear-of-replacement · 40 dotnet-and-the-enterprise-lane ·
41 wordpress-and-cms-internet · 42 glossary (A only, LAST)

## SHELF DONE = all of:
- Every doc: digest exists, coverage gate 0, digest links wired EN+AR, sweep logged
- Every doc: Track B row in ledger (additions OR justified N/A)
- All twins: verify-twins green at last touch
- goal.md log shows one line per doc per track
- Final checkpoint: `Checkpoint vX: shelf campaign complete` + tag

## OPEN QUESTIONS POLICY
Anything genuinely ambiguous (e.g., two specs conflict, source paywalled everywhere,
AR translation of a new coinage missing from glossary): apply constitution → glossary
rule (never invent terms) → log in goal.md "Open questions" → continue next doc.
User reviews Open questions async; agent NEVER waits.
