# Arabic shelf overhaul — progress ledger

Rule: **every checkpoint ends by updating this file.** Status flips are visible in git history; never leave a row stale.

Counts below are **visible h2s** (outside `<pre>`); raw counts lie. At v10 the raw parser missed multi-line closers (`</pre\n >`), which falsely swallowed sections in 5 files — corrected at v11 (see Known follow-ups).

## Status legend

- ✅ AR-OK — twin is current and parity-clean
- ⏳ LAGGING — twin exists but EN has sections the twin lacks (visible h2 gap shown)
- 🔴 EN-ONLY — no twin yet

## Per-doc status (41 EN / 18 twins, measured 2026-08-10, Tier 0; corrected at v11)

### Twins — ✅ AR-OK (37)
| doc | EN h2 | AR h2 |
|---|---|---|
| cs-and-software-engineering | 23 | 23 |
| glossary | 22 | 22 |
| react-2024-and-beyond | 16 | 16 |
| problem-solving | 25 | 25 |
| version-control-ci-cd-deployment | 21 | 21 |
| what-is-state-prequel | 15 | 15 |
| design-thinking | 20 | 20 |
| api-design | 25 | 25 |
| ui-ux-web-design | 18 | 18 |
| html-and-css | 23 | 23 |
| how-developers-think-frontend | 25 | 25 |
| system-design | 24 | 24 |
| software-development-process | 34 | 34 |
| class-to-hooks-paradigm-shift | 35 | 35 |
| angular-evolution | 23 | 23 |
| javascript-across-stacks | 19 | 19 |
| frontend-camps-survey | 21 | 21 |
| javascript-the-language | 19 | 19 |
| terminal-and-deployment-substrate | 14 | 14 |
| terminal-applications | 18 | 18 |
| algorithms-and-data-structures | 14 | 14 |
| dotnet-and-the-enterprise-lane | 15 | 15 |
| backend-engineering | 24 | 24 |
| data-modeling-and-databases | 25 | 25 |
| nextjs-deep-dive | 26 | 26 |
| observability-and-operations | 28 | 28 |
| security-and-threat-modeling | 21 | 21 |
| software-testing-and-debugging | 21 | 21 |
| payments-and-commerce | 21 | 21 |
| sql-and-postgresql | 20 | 20 |
| frontend-income-markets | 10 | 10 |
| freelance-web-practice | 19 | 19 |
| wordpress-and-cms-internet | 21 | 21 |
| product-strategy | 24 | 24 |
| product-shapes | 18 | 18 |
| open-source | 21 | 21 |
| hiring-process-and-interviews | 21 | 21 |

> **Hygiene NOTE (v18 gate battery):** parity ✔ ≠ hygiene ✔. The debt inventory is EMPTY as of v30:
> cs-and-se (v27: 46 numerals + 178 §-tokens resolved; v27-fix retargeted §10 → look-back), glossary (v28: 297 §-tokens → 232 cross-doc fold patterns, per-doc legacy-number maps recovered from v6/v10 history + ~35 content-verified deviations), react-2024 (v29: 54 numerals + §1–§8 + dotted 4.1–4.4 → parent anchor + c2h cross-doc), problem-solving + ui-ux (v30: last h2/h3 numeral residues). Full shelf: 18/18 twins ALL GATES GREEN (v-sk7: boundary class B gains U+2018/U+2019 — the `§9b’s` possessive case).

### Twins — ⏳ LAGGING (empty)
| doc | EN h2 | AR h2 | gap | tier |
|---|---|---|---|---|
*(none — all 18 docs have matching twins; 18/18 twins green)*

### EN-only — 🔴 no twin (4)
— none — 41/41 complete.

> **Coverage policy FLIPPED (v44):** the old Tier-C line (career/income docs stay EN-only) is void — shelf owner is an Egyptian local-market profile (Arabic interviews, local companies, Arabic client market). ALL docs get twins.
> **Orchestration model v2 (v50):** watchdog+pager `plans/wave-watch.sh` (detached, 120s poll) — DETECTION (free) logs DONE/FAILED to /tmp/waves/LOG and WAKE-injects a message into the MAIN pi session (orca-ide terminal send, debounced 30 min/doc), so the orchestrator with full context does integration + judgment + respawns. The wave-integrate automation (v47) was REMOVED (its stateless agent couldn't judge; race risk on tags). Fallback if the main pane is ever closed: `orca-ide automations create --name wave-integrate --trigger '*/20 * * * *' --provider pi --repo name:Programming --precheck 'bash plans/wave-precheck.sh' --prompt <integration protocol, v50+ numbering>`.
> Legacy: watchdog `plans/wave-watch.sh` (detached, 120s poll, logs DONE lines to /tmp/waves/LOG) plus Orca automation `wave-integrate` (cron */20, precheck `plans/wave-precheck.sh`, pi agent, v48+ numbering). Main session scans /tmp/waves/LOG as its FIRST tool call each turn.
> W4 (local-market cluster): frontend-income-markets, hiring-process-and-interviews, wordpress-and-cms-internet, freelance-web-practice — briefs 13–16. W5: product-shapes, recurring-fear-of-replacement, open-source. W6: beyond-the-browser, full-stack, income-stream-landscape.

## Tiers & gates

- **T0 · anchors + bootstrap** — ✅ done (v10): ids on all EN h2s + AR parity twins; AGENTS.md + this ledger; anchor-ref conversion deferred to each doc's own pass.
- **T0.5 · surgical fills + per-doc passes** — ✅ done (v11): problem-solving § two-sum + version-control § debugging across time translated; both twins de-numbered, id-anchored, all visible `§`-refs remapped to anchor links (incl. cross-doc: 3 Testing & Debugging anchors, 2 Problem-Solving anchors, bisect-cell + stale api-design §1d→§4 fixes); orphan §7b refs fixed (doc has no 7b); version-control AR ratio 0.36 → 0.55.
- **T1 · lettered fills** — what-is-state-prequel (first), ui-ux, design-thinking, api-design, html-and-css, how-developers-think-frontend.
- **T1.4 · html-and-css — ✅ done (v16)**: 10 sections translated (6 practical-surface intro (was missing — AR §6 was the interlude promoted to an h2), 6b platform primitives 9-row + 10-row decision table + div≠button callout, 6c units 9-row + math functions 5-row + verbatim clamp pre, 6d responsive 7-row + layout patterns 11-row + mobile-first para, 6e forms 15-row + 9-item checklist, 6f media 7-row + video para, 6g typography 7-row + verbatim pre + 3 bullets, 6h color 4+4 tables + 4 bullets, 6i motion 6-row + 4 bullets, 6j CWV 3-row + owned-elsewhere para); **v10 anchor-pass regression root-caused + repaired**: EN code-sample h2s (`<code><h2>` in §9 tail list + step-6 table) had giant id-attrs swallowing ~7KB of visible content — restored as escaped `&lt;h2&gt;` samples (no refs targeted them); same author-original unclosed samples escaped in AR; AR interlude «٦. الإيقاع» h2 DEMOTED (EN has it as an unheaded standalone para) and missing §6 practical-surface inserted; author-invented «١٢. المستقبل» h2 DEMOTED (EN keeps its future table inside §11) + ملخص renumbered ١٣→١٢; both twins' «§9 in UI/UX» cross-ref text → real links to ui-ux worked-example anchor; EN §1.3/§5×3/§6e/§6f/§7/§8/§6h/§6i remapped, AR cross-doc prefix fix (`../javascript-the-language` → `./` — twin exists); de-numbered both, AR id pass 23/23; gates green (h2 23/23 visible, h3 17/17, pre 7/7, ids identical, zero stray § (all inside links), ratio 0.84).
- **T1.0 · what-is-state-prequel — ✅ done (v12)**: 8 sections translated (3b definition+2 tables, 3c state-changes w/ verbatim pre, 5b mental-models table, 6b lifecycle/ownership, 6c derived/cache/config w/ React setCount pre, 6d identity vs state, 6e failure modes, 6f principles) + §5 examples+test para, §6 lifetime-table 5 rows (DB/URL/cookie·localStorage/server session/cache), stateful-vs-stateless paras, continue-reading para replacing 2 stale §7 refs; ENIAC-bullet factual sync; stale refs fixed („باقي §0“, §1, §4, §6) + tanwin-order normalization; both twins de-numbered (h2+h3), AR id pass 15/15 identical, all visible §/&sect; remapped (EN: von-Neumann + types links, 4 §-links, 9c/10b cross-doc); gates green (h2 15/15, h3 8/8, zero visible-§, ids identical, tags balanced, ratio 0.80 in calibrated band) — pending-only: 2 cross-doc frags into class-to-hooks AR twin (T2).
- **T1.1 · ui-ux-web-design — ✅ done (v13)**: 3 sections translated (8b common interface patterns: 12 decision-table rows + state-matrix 15 rows + forms/IA/loading/visual-fundamentals/motion; 8c research methods 10-row + usability metrics + severity/triage + a11y testing workflow; 8d dark patterns 9-row + permission UX + localization/i18n + inclusive design 10-row); pre-existing drift fixed: AR §9 was missing Steps 5–6 (token mapping w/ verbatim tokens.json pre + naive-vs-designed table) — inserted; de-numbered both twins (h2+h3), AR h2 id pass 18/18 identical to EN, EN §9×2 + §8b remapped to anchors, AR reversed-token (٩§) → anchor; gates green (h2 18/18, h3 28/28, zero visible-§, ids identical, tags balanced, ratio 0.80).
- **T1.2 · design-thinking — ✅ done (v14)**: 4 sections translated (8b synthesis: affinity/empathy/journey/POV-madlib tables; 8c ideation + prototype taxonomy: HMW/Crazy 8s/Worst-idea/roleplay/scale-matrix + concierge/Wizard-of-Oz/painted-door/concept-video; 8d desirability testing + handoff artifacts + layered-handoff callout; 8e room & org: HiPPO/buyer-vs-user/extractive research); AR §9 REPLACED by EN's full worked example (5 stages + verbatim insight pre + artifacts para) — flagged revert option if the old condensed table was intentional; pre-existing drift fixed: AR §10 academic-critique para upgraded to h3+3 bullets+thread (Norman year corrected 2023→2019), AR §12 future table +co-design row + heading subtitle «— أين يتجه»; stale EN §1d×2 → system-design #sec-intersection-with-neighbors (doc has no 1d) + §3b/§6/§7/§9/§10/§12 remapped; de-numbered both twins (h2 numeric; AR latin-letter suffixes 8b-8e too), AR h2 id pass 20/20; gates green (h2 20/20, h3 15/15, ids identical, zero visible-§, tags balanced, ratio 0.79) — pending: 2 cross-doc frags → system-design AR twin (T2).
- **T1.3 · api-design — ✅ done (v15)**: 9 sections translated (8b conventions & identifiers 13-row + identifier-design 5-row tables; 8c collections pagination/filter/sort w/ verbatim GET pre; 8d validation errors w/ verbatim 422 pre + optimistic locking (If-Match/412); 8e 202/job-resources/webhooks w/ 3 verbatim pres + 8-row webhook table; 8f realtime/SSE/WebSocket; 8g compatibility matrix 10-row; 8h security & browser contracts (AR: security-and-threat-modeling link → ../ per EN-only rule) + a11y of scope discipline; 8i file uploads/binary; 8j AI-safe tool contracts); AR §9 (shipment tracking) already full 9-h3 mirror — kept; de-numbered both twins (h2+h3 incl latin suffixes), AR h2 id pass 25/25, EN 18 §-tokens remapped (8d×3, 8e×3, 8f×2, 8g, 8h, 10×3, 3, 5b, 11×2), AR reversed (٩§) ×3 fixed; gates green (h2 25/25, h3 23/23, ids identical, zero visible-§, pre 7/7, ratio 0.81).
- **T1.5 · how-developers-think-frontend — ✅ done (v17)**: hygiene + §-remap only (25/25 parity already). **New: shared pipeline `/tmp/pipeline.py`** (doc-pair → de-number → AR id-pass → fold-exceptions → anchor-protected remap → verify) replaces the per-doc mutated scripts — dry-run on copies first, then real files; the v16-style script bugs (rest-capture eating text runs, pre-mask dropping content, first-char digit maps) are now one-time fixes in the pipeline. Repairs: AR had **2 multi-line `</pre>` closers** (v10-era residue — one of the files “corrected at v11” still carried 2) — normalized, pre-blocks now balance 10/10; EN+AR de-numbered (h2+h3), AR id-pass 25/25 identical; EN 40+ §-tokens remapped (incl. ranges §2–§5, §1b/1e/5a/5b/12b/13b/13c/13d); AR Arabic-Indic tokens + **letter suffixes أ/ب/ج/د/هـ/و mapped to a/b/c/d/e/f**; existing cross-doc labels folded correctly: “HTML & CSS §5b” into its anchor, bare “(Problem-Solving §6/§1f)” → real links (stepwise-refinement / mental-models anchors — legacy numbering resolved from §6≡stepwise, §11≡fluency); gates green (h2 25/25, h3 33/33, pre 10/10, ids identical, zero stray §, cross-doc anchors resolve). **AR ratio 1.17 > band 0.75–0.97** — flagged: the twin's long-standing authoring style is verbose (density audit pending, like version-control 0.55).
- **v18 · tooling consolidation — ✅ done**: the hygiene mechanics are **locked, global, versioned**. `~/.agents/skills/translate-to-arabic/` is now a git repo (v-sk2): `scripts/twin-pipeline.py` (strip → id-pass → folds → §-remap; reads `maps/<doc>.json`; includes the `</pre\s*>` normalization; **proven by reproducing the v17 hdft commit byte-for-byte from its pre-v17 state**, idempotent on re-runs) + `scripts/verify-twins.py` (the gate battery: balance, visible-h2 parity, ids identical, numeral-free, zero stray §, internal+cross-doc anchors, lang-switch, ratio 0.75–0.97 with recorded-exception FLAGs) + `conventions.md` (failure ledger) + `project-snippet.md` (new-shelf AGENTS.md bootstrap). Repo side: per-doc config moved to `maps/<doc>.json` (6 docs; every WANT id validated against the EN file; dt 3b id corrected to `…-in-existing-orgs`); AGENTS.md gates now point at the scripts. **The first global run exposed the true hygiene debt** (see table note + follow-ups): only the six pipeline-processed pairs are gate-clean. Ratio exceptions re-measured canonical (script): version-control 0.40, how-developers 1.17, cs-and-se 0.98, glossary 0.99, problem-solving 0.70.
- **T2 · large fills — ✅ done (v22)**: system-design (v20, 24/24: 9 sections translated 6b–6g/7/8/9, AR-only serverless demoted to h3, §6 h3-patch 41/41), software-development-process (v21, 34/34: 15 sections 9e–9s, Problem-Solving §10 fold), class-to-hooks-paradigm-shift (v22, 35/35: full rebuild 19→35 — 17 sections translated, 11 h2 retitles, empty AR shell dropped, §9.3→9c fold, splice-sections.py manifest rebuild; ratio 1.34 recorded exception: legacy 65K 0.x depth preserved in AR §1). **T2 cross-doc pendings all resolved:** what-is-state 9c/10b → class-to-hooks ids, design-thinking → system-design — battery green on both since v22.
- **T3 · fills — DONE ✅**: angular-evolution (v23, 23/23)؛ javascript-across-stacks (v24, 19/19)؛ frontend-camps-survey (v25, 21/21)؛ javascript-the-language (v26, 19/19). All remaining docs translated; LAGGING table empty. P3 items now: observability-and-operations + security-and-threat-modeling new twins, AR glossary ../→./ flips, hub index, cs-and-se link sync.
- **P3 · new twins** — observability-and-operations, security-and-threat-modeling (+ glossary/hub/cs-and-se link sync).
- **Final pass** — re-verify every `./name.html#sec-…` shelf-wide; flip all pending links.

Per-doc gates (translate-to-arabic skill): run `scripts/verify-twins.py <doc>` — visible h2 parity, name parity, zero `§`-refs, all `href="#…"` resolve, ids unique + identical in both twins, h3/tag balance, char-ratio band (0.75–0.97 canonical measure + recorded exceptions in the script), language-switch lines, mojibake-safe verification.

## Known follow-ups

- `income-stream-landscape.html` + (legacy `s0`–`s8` ids were **not found** in what-is-state twins at v12 — line can be dropped; income-stream-landscape still carries them) — kept (links may target them); rename during their own pass.
- **v16 html-and-css**: the 3 „unclosed `</h2>`“ were **v10 anchor-pass corruption** of code-sample text (giant id blobs swallowing visible content, `a11y-tree` section id was also one) — fixed by escaping the sample tags (`&lt;h2&gt;`); also escaped AR's author-original unclosed samples. **Shelf-wide `<code><h2` scan pending in final pass** (this was the only doc carrying code-sample h2s so far: EN 3 sites + AR 3 sites, all fixed).
- **v12 pair hygiene**: what-is-state EN+AR de-numbered (h2/h3), AR twin got full 15-id set, all visible `§`/`&sect;` remapped (4 new links: §1→theories, §5→distinction, §6→lifetime, §6c→derived + cross-doc 9c/10b → class-to-hooks anchors); **PENDING** `ar/what-is-state-prequel.html` → `./class-to-hooks-paradigm-shift.html#sec-…` (10b/9c ids) — land at T2; EN ratio 0.80 (in calibrated band), version-control 0.55 stays flagged until its own density audit.
- EN `problem-solving.html` still holds `§`-style pointers *inside* `<pre>` sample code (e.g., code comments) — house rule exempts pre content; visible prose is zero-`§`.
- design-thinking AR §9 has its own worked example vs EN's — parity decision pending.
- EN html-and-css (v16) remapped «§5 "State lives in attributes" / "Tokens over magic numbers"» quotes keep the §-link text only outside quotes — cosmetic, fine.
- AR html-and-css (v16) — interlude & future-table demotions are content-preserving (no text lost); revert = re-add h2s if ever wanted.
- **AR how-developers ratio 1.17** — verbose twin style (band 0.75–0.97); density audit before final pass, don't rewrite yet.
- **Hygiene debt — final-pass sweep (v18 battery)**: cs-and-software-engineering (46 numerals + §1–§9 both twins; facts were fixed at v10 without hygiene), glossary (§0–§9 both twins), react-2024-and-beyond (54 numerals + §1–§8 both twins), problem-solving (h3 «7a. Choosing the data structure» + «7b. Paradigm recognition» in both twins), ui-ux-web-design (AR h2s «8b.–8d.» still numbered). Each = pipeline run with its map (maps exist for 6 docs; make maps for these five at their pass). Ratio exceptions recorded in the script: version-control 0.40 (canonical measure of the terse twin), how-developers 1.17, cs-and-se 0.98, glossary 0.99, problem-solving 0.70 — density audits pending, not rewrite triggers.
- **Pipeline/Tooling (v18)**: mechanics live in the global skill (`~/.agents/skills/translate-to-arabic/scripts/{twin-pipeline,verify-twins}.py`, git repo v-sk1/v-sk2); per-doc config in `maps/<doc>.json` (WANT + FOLDS — the only hand-edited hygiene artifact). Usage: from `reference/` run `twin-pipeline.py <en> <ar> <N> --map ../maps/<doc>.json`, then `verify-twins.py` from the repo root (or explicit paths). New shapes → fix script + `conventions.md`, never one-off scripts. New shelves: `project-snippet.md`.
## Repo location (moved v31+)
Working repo is now ~/projects/Programming (Linux-native, canonical history + tags v10-v31); the old /mnt/e/Freelancer/Frontend Mentor/General teach/Programming copy is redundant (stale lineage merged via upstream remote; 18/18 gates re-verified at the new location).
- **improve-doc pilot (v60)** — html-and-css first pass: leverage map section added (R14, both twins via splice), CWV thresholds calibrated (R19), search-vocabulary details block (R16), who-this-is-for + Last reviewed markers (R11/R12), all 12 positional § refs de-numbered EN+AR and maps/html-and-css.json WANT/FOLDS emptied. **Bug found by profiler:** unescaped `<code><style></code>` in failure-modes table swallowed the rest of the doc at parse time in BOTH twins (zero `</style>` in file) — fixed by escaping; battery had no parse-integrity gate (noted for skill). Ledger: reference/Archive/rules-compliance.md.
- **v61 repair** — v60's AR patches (audience/currency markers, §9 rename, CWV thresholds, vocabulary block) were silently lost when a hotfix `cp` overwrote the work copy pre-splice; re-applied directly. Tooling hardened: verify-twins.py gained a real **visible h3 parity** gate (old "h3 balance" only checked tag well-formedness — twin asymmetries were invisible); doc-profile.py gained **parse-integrity gate** + bilingual EN/AR marker detection; ledger notation formalized in the skill (id / id=pre / id→doc / id=N/A(type)).
- **v66 class-to-hooks reconciliation COMPLETE** — six EN h3 sections translated into the AR twin (four-pillars, pivot, good/painful, why-hooks-solve+why-2019, deeper-reason capture-vs-mutate); visible h3 parity 26/26 strict, H3_PARITY_EXCEPTIONS entry removed (ledger now empty). Ratio 1.14 stays a recorded verbose-twin exception. First doc in the shelf with zero twin debt after improve-doc pass.
- **Correction (v67)** — v66's note called class-to-hooks "first doc with zero twin debt"; inaccurate. html-and-css has been at zero debt since v61 AND carries zero exceptions (ratio 0.84 in band, h3 parity 18/18 strict). Accurate statement: html-and-css = zero debt, zero exceptions; class-to-hooks = zero debt after reconciliation, one recorded ratio exception.

## improve-doc CAMPAIGN v4 (2026-08-21 → 08-22, checkpoints v96–v123)

- Phase 0 audit + Phase 1 backfill (v96–v103) and DOC ORDER #4–#10 full A+B
  (v104–v111): every reference doc carries a digest shell, dispositions7 board,
  evidence-grounded additions mirrored to AR twins via the locked pipeline.
- User rulings institutionalized: Archive deletions accepted (v98); glossary-first
  coinage (Leverage Map / خريطة الرافعة, v100); income-stream worksheet user-data
  cells OFF-LIMITS (v112) with a sourced teaching block added by directive (v119).
- Skill improved: v1.6 content-types gate; v1.7 currency conventions
  (source-dated ledger column, claim-class coverage rows). Debt harvest closed ALL
  open G-* hunts (v116; 16 sources via scrape-skill escalation) and caught a real
  mis-citation (ui-ux Hick DOI fixed both twins).
- Twin debt zeroed: full-shelf sweep 41/41 verify-twins PASSED (v118) after
  reconciling six docs (angular ×4 h3 blocks, cs, swdp, vc DORA+nav repoints,
  frontend-camps EN camp E/F triples, payments preamble).
- Digest-completion campaign (v120→): shells for all remaining docs; 31/42 at v123;
  final 9 in flight via durable subagents. wordpress-and-cms-internet documented as
  EN-only tier (G-wp2 defers AR decision to owner).
- Ratio exceptions unchanged and recorded in verify-twins.py. Open questions logged
  in goal.md; nothing blocks.
