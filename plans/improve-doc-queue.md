# SHELF CAMPAIGN — PLAN v4 (autonomous, 2026-08-21)

Supersedes v3. Purpose: let a goal-mode agent run the ENTIRE shelf without user input.
Every decision rule is written here; if a situation isn't covered, the agent logs it in
goal.md under "Open questions" and moves to the next doc rather than blocking.

Mechanisms referenced (read once per session):
- `plans/source-digestion-workflow.md` — pipeline
- `plans/credibility.md` — T1/T2/T3 claim tiers
- skill `improve-doc` v1.6+: `sources.md`, `insight.md`, `digest-coverage.py`, `doc-profile.py`, `content-types.py`
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
   Dispositions are RECORDED MECHANICALLY: a `dispositions7` block in
   `maps/<stem>.json` (statuses PRE w/ anchor · ADD w/ delta id · SKIP w/ why ·
   THIN = present-but-below-density, gate-red) — the ledger table mirrors it;
   `~/.agents/skills/improve-doc/scripts/content-types.py` validates anchors, delta ids, and the floor.
4. Per-type quality bars come from the skill's `diataxis.md` digest (type compass +
   quality expectations); the digest's Δ items are the raw material for ADDs.
4. Mirror everything to AR twin (pipeline; direct patches for prose, splice for structure).
5. Gates: `verify-twins.py` ALL PASSED + parse integrity both twins + coverage gate still 0
   + `python3 ~/.agents/skills/improve-doc/scripts/content-types.py <stem>` exit 0 (seven-type gate: THIN/MISSING
   anywhere = red; two-addition floor enforced; advisory weak-signature flags allowed).
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

## REMEDIATION PHASES (inserted 2026-08-22, after the change-review audit)

Phase 0 (DONE, v96): content-types gate shipped in skill v1.6; dispositions7 seeded
honestly in five maps; api-design ledger row reconstructed; react digest
authored-vs-verified corrected; problem-solving raw seeds re-fetched into
reference/sources/raw-seeds/problem-solving/ after the /tmp loss.

### Phase 1 — seven-type backfill ✅ COMPLETE (v97–v103, 2026-08-22)
Order: observability → how-developers-think → software-testing-and-debugging →
api-design → react-2024-and-beyond. One doc at a time; full twin hygiene.
Per doc:
1. R14 leverage map authored from THAT doc's own digest/seeds — evidence-derived
   master-first tiers ("master first / learn when needed / rare specialist");
   ratios cited T1 or hedged labeled-convention (insight.md forbids unsourced ones).
   New section, `sec-leverage-map-<context>` id identical both twins, spine-safe slot.
2. R16 where THIN: terms-of-art block ("this is called X when…") grounded in seeds;
   or explicit glossary-owner disposition via boundaries rule.
3. react only: second Track B addition (from Δ backlog or G-r2 Actions deep-read)
   + one distilled war story (R20) from fetched sources — clears its floor deviation.
4. Mirror via twin pipeline (splice for structure); update digest shell Δ list and
   dispositions7 (THIN/MISSING → PRE w/ anchor or ADD w/ delta id).

OUTCOME: all five docs gates-green (twins/coverage/content-types exit 0). Leverage
Map / خريطة الرافعة coined in glossary cross-cutting tables per user ruling (v100).
react floor deviation closed via WAIVER-form note citing Δ1 (v90) + Δ2 (v103).
Terminology policy now standing: new terms get a glossary dfn first, then reuse.
5. Gates: verify-twins ALL PASSED + coverage exit 0 + content-types exit 0.
6. Ledger row statuses flip; goal.md line; commit + tag.
PHASE 1 DONE = `content-types.py` exit 0 on all five completed docs.

### Phase 2 — resume campaign queue
DOC ORDER resumes at #4 system-design Track B (owed since v89) under dispositions7
discipline, then #5 javascript-the-language onward. problem-solving (#14): Track A
resumes from rescued raw-seeds — carve source keys per _TEMPLATE.md, build shell +
matrix, then Track B with dispositions7. Wave 1.5 leftovers (lamport/brewer scans,
team-topologies extraction) remain tracked debt, not blockers.

## DOC ORDER (interleave A+B per doc before next)

Wave 1 — alumni: mechanical layer pre-clean, but FULL A+B like everyone else.
Prior passes (v60–77) count ONLY as Phase-A hygiene credit (numerals/corruption
already handled). Their Track B is fresh: author from THIS doc's extraction deltas,
minimum two substantive additions per the normal rule. Prior template-era additions
(vocabulary blocks, teacher sections, markers) are existing content — swept and
verified during A like everything else; they do NOT count toward B's minimum.
1 api-design ✅v79 (full A+B pilot) · 2 how-developers-think-frontend ✅v80 (A+B) ·
3 software-testing-and-debugging ✅v81 (A+B) · 4 system-design ✅v105 (Track B) ·
5 javascript-the-language ✅v106 · 6 class-to-hooks-paradigm-shift ✅v107 ·
7 html-and-css ✅v108 · 8 what-is-state-prequel ✅v109 · 9 ui-ux-web-design ✅v110 ·
10 javascript-across-stacks ✅v111 — **WAVE 1 COMPLETE**

Wave 1.5 KEY HARVEST — ✅ COMPLETE (v86–v89): ~27 source keys in reference/sources/;
remaining deep-reads: lamport/brewer formal proofs (scans), team-topologies extraction.
Migration debt tracker lives in skill sources.md.

Wave 2 — high-deficiency, full A+B:
11 react-2024-and-beyond ✅v90 (full A+B) · 12 observability-and-operations ✅v91–92
(full A+B; 174 refs de-numbered, 41 nested-anchor pairs repaired) ·
13 income-stream-landscape ✅v112 reclassified worksheet (light Track A) +
✅v119 user-directed content upgrade is-Δ1 (sourced ground-rules block, both twins;
user data cells untouched) ·
14 problem-solving ✅v113–v115 full A+B (+ twin repairs v114; G-ps2 closed v116) ·
15 cs-and-software-engineering ✅v121 digest + justified-N/A ·
16 version-control-ci-cd-deployment ✅v117 sync + v121 digest ·
17 software-development-process ✅v117 sync + v121 digest ·
18 data-modeling-and-databases 🔄 digest in flight (durable subagent) ·
19 sql-and-postgresql 🔄 digest in flight (durable subagent) ·
20 security-and-threat-modeling 🔄 digest in flight (durable subagent)

Wave 3 — remaining core:
21 backend-engineering ✅v122 · 22 full-stack ✅v122 · 23 frontend-camps-survey ✅v118 sync + v120 digest · 24 nextjs-deep-dive ✅v122 ·
25 angular-evolution ✅v117 sync + v120 digest · 26 algorithms-and-data-structures ✅v114 AR-restore + v122 digest · 27 design-thinking ✅v122 ·
28 beyond-the-browser ✅v118 + v122 · 29 terminal-and-deployment-substrate 🔄 in flight · 30 terminal-applications 🔄 in flight

Wave 4 — career/business tier (lighter sources; interviews/blog posts acceptable as
supporting tier):
31 freelance-web-practice ✅v122 · 32 frontend-income-markets 🔄 in flight ·
33 income-stream-landscape ✅ (dup of #13 — see above) · 34 hiring-process-and-interviews 🔄 in flight ·
35 product-strategy ✅v122 · 36 product-shapes ✅v122 · 37 payments-and-commerce ✅v118 + v120 digest ·
38 open-source 🔄 in flight ·
39 recurring-fear-of-replacement 🔄 in flight · 40 dotnet-and-the-enterprise-lane ✅v122 ·
41 wordpress-and-cms-internet 🔶 EN-only doc (no AR twin) — digest pending, LAST ·
42 glossary ✅v122 (A only as planned)

## SHELF DONE = all of:
- Every doc: digest exists, coverage gate 0, digest links wired EN+AR, sweep logged
- Every doc: Track B row in ledger (additions OR justified N/A)
- Every doc: `content-types.py` exit 0 — all seven types PRE/ADD/SKIP(justified), zero THIN/MISSING
- All twins: verify-twins green at last touch
- goal.md log shows one line per doc per track
- Final checkpoint: `Checkpoint vX: shelf campaign complete` + tag

## OPEN QUESTIONS POLICY
Anything genuinely ambiguous (e.g., two specs conflict, source paywalled everywhere,
AR translation of a new coinage missing from glossary): apply constitution → glossary
rule (never invent terms) → log in goal.md "Open questions" → continue next doc.
User reviews Open questions async; agent NEVER waits.
