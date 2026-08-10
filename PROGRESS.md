# Arabic shelf overhaul — progress ledger

Rule: **every checkpoint ends by updating this file.** Status flips are visible in git history; never leave a row stale.

Counts below are **visible h2s** (outside `<pre>`); raw counts lie. At v10 the raw parser missed multi-line closers (`</pre\n >`), which falsely swallowed sections in 5 files — corrected at v11 (see Known follow-ups).

## Status legend

- ✅ AR-OK — twin is current and parity-clean
- ⏳ LAGGING — twin exists but EN has sections the twin lacks (visible h2 gap shown)
- 🔴 EN-ONLY — no twin yet

## Per-doc status (41 EN / 18 twins, measured 2026-08-10, Tier 0; corrected at v11)

### Twins — ✅ AR-OK (5)
| doc | EN h2 | AR h2 |
|---|---|---|
| cs-and-software-engineering | 23 | 23 |
| glossary | 22 | 22 |
| react-2024-and-beyond | 16 | 16 |
| problem-solving | 25 | 25 |
| version-control-ci-cd-deployment | 21 | 21 |

### Twins — ⏳ LAGGING (13, ordered by gap size)
| doc | EN h2 | AR h2 | gap | tier |
|---|---|---|---|---|
| class-to-hooks-paradigm-shift | 35 | 19 | 16 | T2 |
| software-development-process | 34 | 19 | 15 | T2 |
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
| how-developers-think-frontend | 25 | 25 | 0 | ✅ full parity (false alarm at v10) |

### EN-only — 🔴 no twin (23)
algorithms-and-data-structures, backend-engineering, beyond-the-browser, data-modeling-and-databases, dotnet-and-the-enterprise-lane, freelance-web-practice, frontend-income-markets, full-stack, hiring-process-and-interviews, income-stream-landscape, nextjs-deep-dive, observability-and-operations, open-source, payments-and-commerce, product-shapes, product-strategy, recurring-fear-of-replacement, security-and-threat-modeling, software-testing-and-debugging, sql-and-postgresql, terminal-and-deployment-substrate, terminal-applications, wordpress-and-cms-internet.

## Tiers & gates

- **T0 · anchors + bootstrap** — ✅ done (v10): ids on all EN h2s + AR parity twins; AGENTS.md + this ledger; anchor-ref conversion deferred to each doc's own pass.
- **T0 · anchors + bootstrap** — ✅ done (v10): ids on all EN h2s + AR parity twins; AGENTS.md + this ledger.
- **T0.5 · surgical fills + per-doc passes** — ✅ done (v11): problem-solving § two-sum + version-control § debugging across time translated; both twins de-numbered, id-anchored, all visible `§`-refs remapped to anchor links (incl. cross-doc: 3 Testing & Debugging anchors, 2 Problem-Solving anchors, bisect-cell + stale api-design §1d→§4 fixes); orphan §7b refs fixed (doc has no 7b); version-control AR ratio 0.36 → 0.55 (in band).
- **T1 · lettered fills** — what-is-state-prequel (first), ui-ux, design-thinking, api-design, html-and-css, how-developers-think-frontend.
- **T2 · large fills** — system-design (before SDP), software-development-process, class-to-hooks-paradigm-shift.
- **T3 · near-rebuilds** — javascript-the-language, javascript-across-stacks, frontend-camps-survey, angular-evolution.
- **P3 · new twins** — observability-and-operations, security-and-threat-modeling (+ glossary/hub/cs-and-se link sync).
- **Final pass** — re-verify every `./name.html#sec-…` shelf-wide; flip all pending links.

Per-doc gates (translate-to-arabic skill): visible h2 parity, name parity, zero `§`-refs, all `href="#…"` resolve, ids unique + identical in both twins, h3/tag balance, char-ratio band, language-switch lines, mojibake-safe verification.

## Known follow-ups

- `income-stream-landscape.html` + `what-is-state-prequel.html` carry legacy ids (`s0`–`s8`, non-`sec-` style) — kept (links may target them); rename during their own pass.
- EN `html-and-css.html` has **3 unclosed `</h2>`** in the a11y sections (`heading-structure…`, `proper-heading-hierarchy…`, `a11y-tree…`) — pre-existing at HEAD, id-backed now; repair during its T1 fill.
- **v10 parser bug (fixed)**: `<pre>` blocks closed with multi-line `</pre\n >` broke the visibility regex in 5 files (incl. problem-solving + how-developers) — v10's "16 phantom h2s" and "4 missing" claims were artifacts; 16 real EN h2s got ids at v11's re-run; problem-solving holds 5 unescaped `<h2` strings as sample text inside `pre` (harmless in HTML5 tokenizer).
- EN `problem-solving.html` still holds `§`-style pointers *inside* `<pre>` sample code (e.g., code comments) — house rule exempts pre content; visible prose is zero-`§`.
- design-thinking AR §9 has its own worked example vs EN's — parity decision pending.