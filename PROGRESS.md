# Arabic shelf overhaul — progress ledger

Rule: **every checkpoint ends by updating this file.** Status flips are visible in git history; never leave a row stale.

Counts below are **visible h2s** (outside `<pre>`); raw counts lie. At v10 the raw parser missed multi-line closers (`</pre\n >`), which falsely swallowed sections in 5 files — corrected at v11 (see Known follow-ups).

## Status legend

- ✅ AR-OK — twin is current and parity-clean
- ⏳ LAGGING — twin exists but EN has sections the twin lacks (visible h2 gap shown)
- 🔴 EN-ONLY — no twin yet

## Per-doc status (41 EN / 18 twins, measured 2026-08-10, Tier 0; corrected at v11)

### Twins — ✅ AR-OK (8)
| doc | EN h2 | AR h2 |
|---|---|---|
| cs-and-software-engineering | 23 | 23 |
| glossary | 22 | 22 |
| react-2024-and-beyond | 16 | 16 |
| problem-solving | 25 | 25 |
| version-control-ci-cd-deployment | 21 | 21 |
| what-is-state-prequel | 15 | 15 |
| design-thinking | 20 | 20 |
| ui-ux-web-design | 18 | 18 |
| design-thinking | 20 | 20 |

### Twins — ⏳ LAGGING (10, ordered by gap size)
| doc | EN h2 | AR h2 | gap | tier |
|---|---|---|---|---|
| class-to-hooks-paradigm-shift | 35 | 19 | 16 | T2 |
| software-development-process | 34 | 19 | 15 | T2 |
| html-and-css | 26 | 18 | 8 | T1 |
| api-design | 25 | 16 | 9 | T1 |
| system-design | 24 | 16 | 8 | T2 |
| angular-evolution | 23 | 10 | 13 | T3 |
| javascript-the-language | 19 | 12 | 7 | T3 |
| javascript-across-stacks | 19 | 9 | 10 | T3 |
| frontend-camps-survey | 21 | 11 | 10 | T3 |
| what-is-state-prequel | 15 | 15 | 0 | ✅ full parity (v12) |
| how-developers-think-frontend | 25 | 25 | 0 | ✅ full parity (false alarm at v10) |

### EN-only — 🔴 no twin (23)
algorithms-and-data-structures, backend-engineering, beyond-the-browser, data-modeling-and-databases, dotnet-and-the-enterprise-lane, freelance-web-practice, frontend-income-markets, full-stack, hiring-process-and-interviews, income-stream-landscape, nextjs-deep-dive, observability-and-operations, open-source, payments-and-commerce, product-shapes, product-strategy, recurring-fear-of-replacement, security-and-threat-modeling, software-testing-and-debugging, sql-and-postgresql, terminal-and-deployment-substrate, terminal-applications, wordpress-and-cms-internet.

## Tiers & gates

- **T0 · anchors + bootstrap** — ✅ done (v10): ids on all EN h2s + AR parity twins; AGENTS.md + this ledger; anchor-ref conversion deferred to each doc's own pass.
- **T0.5 · surgical fills + per-doc passes** — ✅ done (v11): problem-solving § two-sum + version-control § debugging across time translated; both twins de-numbered, id-anchored, all visible `§`-refs remapped to anchor links (incl. cross-doc: 3 Testing & Debugging anchors, 2 Problem-Solving anchors, bisect-cell + stale api-design §1d→§4 fixes); orphan §7b refs fixed (doc has no 7b); version-control AR ratio 0.36 → 0.55.
- **T1 · lettered fills** — what-is-state-prequel (first), ui-ux, design-thinking, api-design, html-and-css, how-developers-think-frontend.
- **T1.0 · what-is-state-prequel — ✅ done (v12)**: 8 sections translated (3b definition+2 tables, 3c state-changes w/ verbatim pre, 5b mental-models table, 6b lifecycle/ownership, 6c derived/cache/config w/ React setCount pre, 6d identity vs state, 6e failure modes, 6f principles) + §5 examples+test para, §6 lifetime-table 5 rows (DB/URL/cookie·localStorage/server session/cache), stateful-vs-stateless paras, continue-reading para replacing 2 stale §7 refs; ENIAC-bullet factual sync; stale refs fixed („باقي §0“, §1, §4, §6) + tanwin-order normalization; both twins de-numbered (h2+h3), AR id pass 15/15 identical, all visible §/&sect; remapped (EN: von-Neumann + types links, 4 §-links, 9c/10b cross-doc); gates green (h2 15/15, h3 8/8, zero visible-§, ids identical, tags balanced, ratio 0.80 in calibrated band) — pending-only: 2 cross-doc frags into class-to-hooks AR twin (T2).
- **T1.1 · ui-ux-web-design — ✅ done (v13)**: 3 sections translated (8b common interface patterns: 12 decision-table rows + state-matrix 15 rows + forms/IA/loading/visual-fundamentals/motion; 8c research methods 10-row + usability metrics + severity/triage + a11y testing workflow; 8d dark patterns 9-row + permission UX + localization/i18n + inclusive design 10-row); pre-existing drift fixed: AR §9 was missing Steps 5–6 (token mapping w/ verbatim tokens.json pre + naive-vs-designed table) — inserted; de-numbered both twins (h2+h3), AR h2 id pass 18/18 identical to EN, EN §9×2 + §8b remapped to anchors, AR reversed-token (٩§) → anchor; gates green (h2 18/18, h3 28/28, zero visible-§, ids identical, tags balanced, ratio 0.80).
- **T1.2 · design-thinking — ✅ done (v14)**: 4 sections translated (8b synthesis: affinity/empathy/journey/POV-madlib tables; 8c ideation + prototype taxonomy: HMW/Crazy 8s/Worst-idea/roleplay/scale-matrix + concierge/Wizard-of-Oz/painted-door/concept-video; 8d desirability testing + handoff artifacts + layered-handoff callout; 8e room & org: HiPPO/buyer-vs-user/extractive research); AR §9 REPLACED by EN's full worked example (5 stages + verbatim insight pre + artifacts para) — flagged revert option if the old condensed table was intentional; pre-existing drift fixed: AR §10 academic-critique para upgraded to h3+3 bullets+thread (Norman year corrected 2023→2019), AR §12 future table +co-design row + heading subtitle «— أين يتجه»; stale EN §1d×2 → system-design #sec-intersection-with-neighbors (doc has no 1d) + §3b/§6/§7/§9/§10/§12 remapped; de-numbered both twins (h2 numeric; AR latin-letter suffixes 8b-8e too), AR h2 id pass 20/20; gates green (h2 20/20, h3 15/15, ids identical, zero visible-§, tags balanced, ratio 0.79) — pending: 2 cross-doc frags → system-design AR twin (T2).
- **T2 · large fills** — system-design (before SDP), software-development-process, class-to-hooks-paradigm-shift.
- **T3 · near-rebuilds** — javascript-the-language, javascript-across-stacks, frontend-camps-survey, angular-evolution.
- **P3 · new twins** — observability-and-operations, security-and-threat-modeling (+ glossary/hub/cs-and-se link sync).
- **Final pass** — re-verify every `./name.html#sec-…` shelf-wide; flip all pending links.

Per-doc gates (translate-to-arabic skill): visible h2 parity, name parity, zero `§`-refs, all `href="#…"` resolve, ids unique + identical in both twins, h3/tag balance, char-ratio band (calibrated 0.75–0.97), language-switch lines, mojibake-safe verification.

## Known follow-ups

- `income-stream-landscape.html` + (legacy `s0`–`s8` ids were **not found** in what-is-state twins at v12 — line can be dropped; income-stream-landscape still carries them) — kept (links may target them); rename during their own pass.
- EN `html-and-css.html` has **3 unclosed `</h2>`** in the a11y sections (`heading-structure…`, `proper-heading-hierarchy…`, `a11y-tree…`) — pre-existing at HEAD, id-backed now; repair during its T1 fill.
- **v12 pair hygiene**: what-is-state EN+AR de-numbered (h2/h3), AR twin got full 15-id set, all visible `§`/`&sect;` remapped (4 new links: §1→theories, §5→distinction, §6→lifetime, §6c→derived + cross-doc 9c/10b → class-to-hooks anchors); **PENDING** `ar/what-is-state-prequel.html` → `./class-to-hooks-paradigm-shift.html#sec-…` (10b/9c ids) — land at T2; EN ratio 0.80 (in calibrated band), version-control 0.55 stays flagged until its own density audit.
- EN `problem-solving.html` still holds `§`-style pointers *inside* `<pre>` sample code (e.g., code comments) — house rule exempts pre content; visible prose is zero-`§`.
- design-thinking AR §9 has its own worked example vs EN's — parity decision pending.