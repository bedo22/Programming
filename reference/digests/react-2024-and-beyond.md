# react-2024-and-beyond — source digestion shell

Status: TRACK A COMPLETE (2026-08-22). 11/11 seeds fetched (1 dead cite repaired) via scrapling.

## Fetch ledger (every cited seed URL, verbatim)

| cited URL | status |
|---|---|
| https://overreacted.io/the-two-reacts/ | OK → key abramov-two-reacts |
| https://overreacted.io/why-isnt-x-a-hook/ | OK → key abramov-why-not-hooks |
| https://preactjs.com/about/project-goals | OK |
| https://preactjs.com/blog/introducing-signals/ | OK → key preact-signals |
| https://preactjs.com/guide/v10/differences-to-react | OK |
| https://react.dev/blog/2023/10/04/partial-prerendering | DEAD (404) → REPLACED with react.dev React Labs March 2023 post (fetched) |
| https://react.dev/blog/2025/02/14/sunsetting-create-react-app | OK → key cra-sunset |
| https://react.dev/blog/2025/10/01/react-19-2 | OK |
| https://react.dev/blog/2025/10/07/react-compiler-1 | OK → key react-compiler-v1 |
| https://react.dev/blog/2026/02/24/the-react-foundation | OK → key react-foundation |
| https://react.dev/reference/rules | OK → key rules-of-react |
| https://www.cve.org/CVERecord?id=CVE-2025-55183 | pending → G-r1 |

## Coverage matrix

| doc section | covered by | note |
|---|---|---|
| #sec-how-to-use-this-doc | n/a navigation | exempt |
| #sec-search-vocabulary-what-react-2024-calls-things | react-Δ3 terms-of-art block (Server Component/hydration/memoization/Suspense/signal/partial prerendering/form action) | added v103; grounded in doc's own usage |
| #sec-react-19-the-platform-shift | cra-sunset · react-19-2 · react-compiler-v1 | |
| #sec-actions-and-forms-progressive-enhancement-returns | rules-of-react | actions deep-dive → G-r2 |
| #sec-the-react-compiler-is-stable-oct-2025-and-ship-by-default-2026 | react-compiler-v1 | Δ verified verbatim |
| #sec-react-server-components-split-rendering-across-two-processes | abramov-two-reacts | |
| #sec-the-security-boundary-rsc-changed-what-a-trust-boundary-means-dec-2025-jan-2026 | gap G-r1 (CVE record unfetched) | |
| #sec-the-react-foundation-feb-2026-meta-is-no-longer-the-sole-owner | react-foundation | governance quote grounded |
| #sec-react-19-2-and-the-framework-routing-era | react-19-2 | |
| #sec-the-signals-question-and-why-react-didn-t-adopt-them | preact-signals | fine-grained reactivity quote grounded |
| #sec-preact-the-structural-branch-that-asks-what-if-react-were-3-5-kb | preact goals + differences pages | |
| #sec-migration-paths-into-react-2024 | cra-sunset | |
| #sec-failure-modes | traces to confirmed sections | |
| #sec-principles | rules-of-react | |
| #sec-leverage-map-where-react-practice-mass-concentrates | react-Δ4 tiers over this shell's fetched sources (two-reacts, compiler-v1, rules-of-react, cra-sunset, foundation, preact pages) | added v103; CVE tier honestly hedged → G-r1 |
| #sec-ecosystem-the-tools-worth-naming | volatile — hedged | |
| #sec-the-future-signals-to-watch | signals — hedged | |
| #sec-summary-checklist | derives from confirmed sections | |

## Gaps

| id | claim/area | hunts | status |
|---|---|---|---|
| G-r1 | CVE-2025-55183 security incident details | cve.org link cited but not yet fetched | fetch next touch |
| G-r2 | Actions/form-actions primary docs | react.dev reference pending | fetch next touch |

## Content authored from this digestion
- v90 Track B AUTHORED (one addition): compiler ship-by-default grounding via two
  verbatim announcement quotes ("works on both React and React Native, and
  automatically optimizes components and hooks without requiring rewrites";
  "battle tested on major apps at Meta"). FLOOR DEVIATION: second addition owed —
  tracked in maps/react-2024-and-beyond.json dispositions7 floor_note (un-waived).
- v103 Phase-1 backfill (deviation CLOSED): react-Δ2 war story — CRA sunset Feb
  2025 (cra-sunset fetch) distilled into migration-paths section EN+AR ·
  react-Δ3 search-vocabulary block (seven terms of art) after how-to-use EN+AR ·
  react-Δ4 leverage map (three tiers: two-Reacts model / rules-as-contract /
  compiler-era defaults) after principles EN+AR. Dispositions7 R14 MISSING→PRE,
  R16 THIN→PRE, R20 THIN→ADD(react-Δ2); floor_note now SATISFIED.
- VERIFIED PRE-EXISTING (not authored here): the foundation-governance facts
  (Linux Foundation launch 2026-02-24, Platinum board incl. Amazon/Callstack/Expo/
  Huawei/Meta/Microsoft/Software Mansion/Vercel, Seth Webster as ED) and the
  fine-grained-signals definition. This digestion grounded them against fetched
  seeds; re-verified live 2026-08-22 against the foundation post and Preact
  signals announcement (all names/terms confirmed present).
