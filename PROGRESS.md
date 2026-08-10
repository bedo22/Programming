# Arabic shelf overhaul — progress ledger

Rule: **every checkpoint ends by updating this file.** Status flips are visible in git history; never leave a row stale.

Counts below are **visible h2s** (outside `<pre>`); raw counts lie (phantom h2s — e.g., how-developers-think-frontend's AR looked at parity at raw 25=25 but is 4 sections short at visible 25 vs 21).

## Status legend

- ✅ AR-OK — twin is current and parity-clean
- ⏳ LAGGING — twin exists but EN has sections the twin lacks (visible h2 gap shown)
- 🔴 EN-ONLY — no twin yet

## Per-doc status (41 EN / 18 twins, measured 2026-08-10, Tier 0)

### Twins — ✅ AR-OK (3)
| doc | EN h2 | AR h2 |
|---|---|---|
| cs-and-software-engineering | 23 | 23 |
| glossary | 22 | 22 |
| react-2024-and-beyond | 16 | 16 |

### Twins — ⏳ LAGGING (15, ordered by gap size)
| doc | EN h2 | AR h2 | gap | tier |
|---|---|---|---|---|
| software-development-process | 34 | 19 | 15 | T2 |
| class-to-hooks-paradigm-shift | 35 | 19 | 16 | T2 |
| html-and-css | 26 | 18 | 8 | T1 |
| api-design | 25 | 16 | 9 | T1 |
| system-design | 24 | 16 | 8 | T2 |
| design-thinking | 20 | 16 | 4 | T1 |
| ui-ux-web-design | 18 | 15 | 3 | T1 |
| angular-evolution | 23 | 10 | 13 | T3 |
| javascript-the-language | 19 | 12 | 7 | T3 |
| javascript-across-stacks | 19 | 9 | 10 | T3 |
| frontend-camps-survey | 21 | 11 | 10 | T3 |
| what-is-state-prequel | 15 | 7 | 8 | T1 (prereq — do first) |
| version-control-ci-cd-deployment | 21 | 20 | 1 | T0.5 surgical |
| problem-solving | 9 | 4 | 5 | T0.5 surgical (16 phantom h2s in pre — the worked-example appendix) |
| how-developers-think-frontend | 25 | 21 | 4 | T1 |

### EN-only — 🔴 no twin (23)
algorithms-and-data-structures, backend-engineering, beyond-the-browser, data-modeling-and-databases, dotnet-and-the-enterprise-lane, freelance-web-practice, frontend-income-markets, full-stack, hiring-process-and-interviews, income-stream-landscape, nextjs-deep-dive, observability-and-operations, open-source, payments-and-commerce, product-shapes, product-strategy, recurring-fear-of-replacement, security-and-threat-modeling, software-testing-and-debugging, sql-and-postgresql, terminal-and-deployment-substrate, terminal-applications, wordpress-and-cms-internet.

## Tiers & gates

- **T0 · anchors + bootstrap** — ✅ done (v10): ids on all EN h2s + AR parity twins; AGENTS.md + this ledger; anchor-ref conversion deferred to each doc's own pass.
- **T0.5 · surgical fills** — problem-solving (§ two-sum), version-control (§ debugging across time).
- **T1 · lettered fills** — what-is-state-prequel (first), ui-ux, design-thinking, api-design, html-and-css, how-developers-think-frontend.
- **T2 · large fills** — system-design (before SDP), software-development-process, class-to-hooks-paradigm-shift.
- **T3 · near-rebuilds** — javascript-the-language, javascript-across-stacks, frontend-camps-survey, angular-evolution.
- **P3 · new twins** — observability-and-operations, security-and-threat-modeling (+ glossary/hub/cs-and-se link sync).
- **Final pass** — re-verify every `./name.html#sec-…` shelf-wide; flip all pending links.

Per-doc gates (translate-to-arabic skill): visible h2 parity, name parity, zero `§`-refs, all `href="#…"` resolve, ids unique + identical in both twins, h3/tag balance, char-ratio band, language-switch lines, mojibake-safe verification.

## Known follow-ups

- `income-stream-landscape.html` + `what-is-state-prequel.html` carry legacy ids (`s0`–`s8`, non-`sec-` style) — kept (links may target them); rename during their own pass.
- EN `html-and-css.html` has **3 unclosed `</h2>`** in the a11y sections (`heading-structure…`, `proper-heading-hierarchy…`, `a11y-tree…`) — pre-existing at HEAD, id-backed now; repair during its T1 fill.
- EN `problem-solving.html` worked-example appendix holds 16 phantom h2s in `<pre>` — parity gates must count visible only.
- version-control AR char ratio 0.36 — density audit later, no silent expansion.
- design-thinking AR §9 has its own worked example vs EN's — parity decision pending.