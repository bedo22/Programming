# class-to-hooks-paradigm-shift — source digestion shell

Status: TRACK A COMPLETE (2026-08-22). Doc cites zero URLs inline (practitioner-narrative
style); ledger built from CLAIM INVENTORY per Wave-1 alumni rule (v60-77 passes count as
hygiene credit only). Keys: 3 under raw-seeds/class-to-hooks-paradigm-shift/ + reusable
cross-doc keys abramov-two-reacts / rules-of-react / react-compiler-v1 (react shell).

## Fetch ledger (every cited seed URL, verbatim)

| cited URL | status | source-dated |
|---|---|---|
| https://en.wikipedia.org/wiki/React_(software) | OK (516KB) | rev 2026-08-21 |
| https://legacy.reactjs.org/docs/hooks-intro.html | OK (132KB) | frozen legacy site — dated(2019-era content), canonical motivation text |
| https://legacy.reactjs.org/docs/hooks-rules.html | OK (130KB) | frozen legacy site — dated(2019-era content) |

(source-dated per currency convention skill v1.7.)

## Sources — read

### Wikipedia: React (software) — tier: primary (history claims)
- Establishes: Jordan Walke at Facebook built the prototype (F-Bolt → **FaxJS**),
  deployed on Facebook's news feed; public announcement May 2013; hooks shipped in
  **16.8, February 2019** ("16.8 was released to the public, introducing React Hooks").
- Δ Doc delta:
  - **ch-Δ1** pre-history paragraph absent from the four-eras timeline — Walke/FaxJS/
    news-feed lineage grounds where eras begin.
- Maps to: #sec-the-four-eras-a-timeline, #sec-era-3-hooks-2018-making-functions-first-class.

### legacy.reactjs.org: Hooks Intro — tier: primary (motivation, verbatim)
- Establishes VERBATIM: "**Classes confuse both people and machines**"; classes are "a
  **barrier to learning React**"; adoption framing "**No Breaking Changes**".
- Δ Doc delta:
  - **ch-Δ2** era-3 section states hooks shipped without carrying WHY the team broke
    with classes — the two verbatim lines are the founding rationale.
- Maps to: #sec-era-3-hooks-2018-making-functions-first-class.

### legacy.reactjs.org: Rules of Hooks — tier: supporting
- Establishes: the two rules verbatim ("Call Hooks at the Top Level", "Call Hooks from
  React Functions"). Doc already teaches both plus the linked-list rationale.
- Δ Doc delta: none — terminology aligned.
- Maps to: #sec-the-rules-of-hooks-and-where-the-design-came-from.

## Coverage matrix

| doc section | covered by | note |
|---|---|---|
| #sec-the-leverage-map-where-the-work-concentrates | doc-native synthesis | accepted authored framework · eternal |
| #sec-search-vocabulary-what-class-to-hooks-calls-things | ch-Δ3 terms-of-art block | added v107 · eternal |
| #sec-before-the-classes-a-word-on-foundations | derives from shelf prequels | pointer section · eternal |
| #sec-oop-the-paradigm-classes-came-from | canon CS (class paradigm) | prose-canonical · eternal |
| #sec-what-is-state-a-prequel-before-we-can-talk-about-react-s-choices | owner-pointer to what-is-state-prequel | cross-doc · eternal |
| #sec-the-four-eras-a-timeline | wiki-react | ch-Δ1 here · dated(2026-08 rev) |
| #sec-the-version-markers-which-react-are-you-reading | wiki-react (16.8 marker) | dated(2026-08 rev) |
| #sec-era-1-class-components-the-original-model | wiki-react · hooks-intro (contrast) | eternal history |
| #sec-era-2-function-components-appear-but-they-re-second-class-2015 | hooks-intro (function-components context) | eternal history |
| #sec-mental-models-how-react-developers-actually-reason | doc-native synthesis | authored framework · eternal |
| #sec-era-3-hooks-2018-making-functions-first-class | wiki-react (16.8 Feb 2019) · hooks-intro quotes | ch-Δ2 here · dated(2026-08 rev) |
| #sec-the-modern-hooks-catalog | rules page + doc-native catalog | dated(2026-08) — catalog grows |
| #sec-the-stale-closure-problem-and-why-it-isn-t-one | doc-native semantics teaching | eternal |
| #sec-effects-vs-event-handlers-two-places-that-do-something-opposite-rules | doc-native | eternal |
| #sec-data-fetching-patterns-where-the-data-comes-from | doc-native patterns | dated(2026-08) — patterns move |
| #sec-the-rules-of-hooks-and-where-the-design-came-from | hooks-rules verbatim | eternal (design rationale) |
| #sec-the-storage-models-three-places-state-can-live-in-react | doc-native model | accepted authored · eternal |
| #sec-strict-mode-and-batching-two-extra-renders-that-are-the-engine-working | cross-doc react-19-2/compiler keys | dated(2026-08) |
| #sec-reconciliation-keys-and-component-identity | doc-native engine teaching | eternal mechanism |
| #sec-suspense-and-use-declarative-waiting-and-reading-resources-in-render | cross-doc react shell keys | dated(2026-08) |
| #sec-the-classic-bugs-and-which-storage-model-fixes-each | doc-native diagnostics | R15 function · eternal |
| #sec-derived-state-compute-during-render-don-t-store | doc-native principle | eternal |
| #sec-context-the-mental-model-for-shared-state | doc-native | eternal |
| #sec-forms-and-actions-submission-becomes-a-first-class-shape | cross-doc react-19 keys | dated(2026-08) |
| #sec-state-design-where-state-should-live | doc-native decision tables | R18 function · eternal |
| #sec-refs-in-depth-and-memoization-the-remaining-manual-doors | cross-doc compiler-v1 key | dated(2026-08) |
| #sec-why-not-just-use-functional-programming-without-hooks | doc-native inversion analysis | R17 function · eternal |
| #sec-era-4-the-react-compiler-and-beyond | cross-doc react-compiler-v1 key | dated(2026-08) |
| #sec-where-classes-still-live-and-whether-to-learn-them | doc-native boundary guidance | eternal |
| #sec-reading-at-work-the-era-recognition-checklist | doc-native checklist | eternal |
| #sec-legacy-patterns-the-old-code-you-ll-read | doc-native | eternal |
| #sec-failure-modes-when-modern-react-just-doesn-t-work | traces to semantics rows | R15 support · eternal |
| #sec-principles-the-invariants-every-pattern-obeys | doc-native principles | eternal |
| #sec-hydration-server-html-meets-client-state | cross-doc two-reacts key | dated(2026-08) |
| #sec-the-lifecycle-to-hooks-translation-table | doc-native translation table | R18 support · eternal |
| #sec-the-current-state-and-what-you-ll-write | volatile framing — hedged | volatile→hedged |
| #sec-a-recommended-reading-order-from-react-s-own-writing | pointers to fetched docs | eternal |

## Gaps

| id | claim/area | hunts | status |
|---|---|---|---|
| G-ch1 | leverage-map tier provenance | doc-native synthesis | accepted authored framework |
| G-ch2 | "Making Sense of React Hooks" talk transcript | medium/dev.to mirrors JS-walled this pass | hunt next touch |
| G-ch3 | Fiber reconciler internals deep source | canon papers known, unfetched | fetch next touch |

## Content authored from this digestion

- pass v107 (Track B, fresh per Wave-1 alumni rule): ch-Δ1 pre-history paragraph
  (Walke/FaxJS/news-feed → May 2013) into four-eras timeline EN+AR · ch-Δ2 verbatim
  motivation quotes ("Classes confuse both people and machines" / "barrier to learning
  React") + no-breaking-changes framing into era-3 EN+AR · ch-Δ3 search-vocabulary
  block (seven terms of art) after leverage map EN+AR. Dispositions7 CREATED (R14 PRE
  on pre-existing leverage map). Floor via WAIVER note (three prose-patch additions,
  all grounded).
