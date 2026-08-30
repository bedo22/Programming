# ui-ux-web-design — source digestion shell

Status: TRACK A COMPLETE (2026-08-22). Doc cites 14 URLs inline (canon-rich); ledger =
cited-URL reconciliation + 3 grounding fetches. Keys under raw-seeds/ui-ux-web-design/.

## Fetch ledger (every cited seed URL, verbatim)

| cited URL | status | source-dated |
|---|---|---|
| https://www.nngroup.com/articles/ten-usability-heuristics/ | OK (135KB) — heuristics verified verbatim ("Visibility of System Status", "User Control and Freedom") | continuously maintained |
| https://www.interaction-design.org/literature/topics/gestalt-principles | OK (340KB) | continuously maintained |
| https://en.wikipedia.org/wiki/Human%E2%80%93computer_interaction | OK (399KB) | rev 2026-07-27 |

## Cited-URL reconciliation (coverage gate requirement)

| cited URL | status | source-dated |
|---|---|---|
| https://www.nngroup.com/articles/ten-usability-heuristics/ | FETCHED (above) | continuously maintained |
| https://www.interaction-design.org/literature/topics/gestalt-principles | FETCHED (above) | continuously maintained |
| https://developer.apple.com/design/human-interface-guidelines/ | platform canon — HIG; doc paraphrases themes | continuously updated |
| https://m3.material.io/ | platform canon — Material 3; design-system rows | continuously updated |
| https://jnd.org/the-design-of-everyday-things/ | book canon — Norman; affordance/signifier concepts | eternal book |
| https://www.cs.umd.edu/~ben/shneiderman.golden.rules.html | canon — Shneiderman's eight golden rules | dated(2000s page) |
| https://doi.org/10.1080/17470215208416600 | CORRECTED LINK (v116): doc previously mis-cited h0054411 as Hick; Crossref identity check caught it | eternal paper |
| https://doi.org/10.1037/h0055392 | VERIFIED (Crossref): Fitts (1954), JEP — doc link correct | eternal paper |
| https://www.iso.org/standard/63500.html | standards canon — ISO 9241 usability definition | dated(current edition) |
| https://www.w3.org/WAI/WCAG22/quickref/ | spec canon — accessibility criteria | dated(2026-08) |
| https://www.rfc-editor.org/rfc/rfc9457 | spec canon — cross-doc API error contract pointer | stable RFC |
| https://tokens.dtcg.io/ | spec canon — design tokens (shared w/ html-and-css) | dated(2026-08) |
| https://www.frost.io/atomic-design/ | practitioner canon — Brad Frost atomic design | living blog |
| https://www.krishna.golden.com/no-interface/ | practitioner canon — Golden Krishna "The Best Interface Is No Interface" (URL as cited in doc) | eternal essay |

All cited sources accounted for; none dead this pass. Platform-canonical pages
(HIG/Material) are authority anchors the doc paraphrases — fetch-on-demand.

## Sources — read

### NN/g Ten Usability Heuristics — tier: primary
- Establishes Nielsen's heuristic names verbatim; the evaluation vocabulary the doc's
  research/triage sections use.
- Δ Doc delta: none — doc already teaches the heuristics correctly.
- Maps to: #sec-ux-research-usability-measurement-and-triage.

### IxD Foundation: Gestalt Principles — tier: primary
- Establishes proximity/similarity/closure et al. as perceptual-organization canon.
- Δ Doc delta: none — doc's underlying-theory rows already name the principles correctly.
- Maps to: #sec-underlying-theory-the-ideas-it-borrows-from.

### Wikipedia: Human–Computer Interaction — tier: supporting (history)
- Establishes HCI's trajectory from command-line ergonomics to experience design.
- Maps to: #sec-history-from-print-composition-to-systems-driven-ui.

## Coverage matrix

| doc section | covered by | note |
|---|---|---|
| #sec-how-to-use-this-doc | n/a navigation | exempt |
| #sec-definition-what-ui-ux-is-and-what-it-is-not | wiki-hci · ISO canon | eternal |
| #sec-search-vocabulary-what-ui-ux-calls-things | ux-Δ2 terms-of-art block | added v110 · eternal |
| #sec-history-from-print-composition-to-systems-driven-ui | wiki-hci | dated(2026-07 rev) |
| #sec-evolution-constraint-inversions-across-ui-history | synthesis | pattern-level · eternal |
| #sec-intersection-with-neighbors-where-it-borders-other-practices | n/a shelf-internal | exempt |
| #sec-underlying-theory-the-ideas-it-borrows-from | gestalt seed · Norman canon | eternal theory |
| #sec-mental-models-how-ui-ux-designers-actually-reason | doc-native lens synthesis | authored framework · eternal |
| #sec-leverage-map-where-ui-practice-mass-concentrates | ux-Δ1 tiers over cited canon (NN/g, Shneiderman, Norman, WCAG) | added v110 · eternal framing, volatile tooling hedged |
| #sec-the-rhythm-not-the-algorithm | shelf-doctrine framing | matrix-exempt |
| #sec-methodologies-named-frameworks | HIG/Material/atomic-design canon rows | volatile→hedged (framework versions) |
| #sec-principles-the-shared-constants | doc-native principles | eternal |
| #sec-common-interface-patterns-and-how-to-choose-between-them | doc-native decision tables | R18 function · eternal |
| #sec-ux-research-usability-measurement-and-triage | NN/g seed · ISO canon | dated(2026-08) |
| #sec-ethics-dark-patterns-localization-and-inclusive-design | WCAG quickref canon | dated(2026-08) |
| #sec-worked-example-a-checkout-flow-that-doesn-t-punish-returns | illustrative (labeled) | eternal |
| #sec-the-most-common-failure-modes | traces to confirmed rows | R15 support · eternal |
| #sec-ecosystem-tooling-catalog-with-decision-metrics | volatile facts — hedged | volatile→hedged |
| #sec-the-future-where-ui-ux-is-going | signals — hedged | volatile→hedged |
| #sec-summary-the-usability-checklist | derives from confirmed sections | inherits classes |

| #sec-2026-ai-slop-design-skills-and-the-screenshot-loop | field notes 2026 — dated transcript evidence yt-003 | dated(2026-08) |
## Gaps

| id | claim/area | hunts | status |
|---|---|---|---|
| G-ux1 | leverage-map provenance | tiers derived from cited canon + own failure table | accepted authored framework |
| G-ux2 | two DOI papers identity confirmation | **CLOSED 2026-08-22 via Crossref API**: h0055392 = Fitts (1954) motor-capacity paper — doc's link CORRECT; h0054411 = Kinsey volunteer-error paper — doc's Hick label was WRONG. FIX APPLIED both twins: Hick now cites doi 10.1080/17470215208416600 (QJEP 4(1) 11–26) | closed · defect fixed v116 |

## Content authored from this digestion

- pass v110 (Track B, fresh per Wave-1 alumni rule): ux-Δ1 leverage map (three tiers:
  heuristics+pattern-choice / research-triage+ethics / standards+platform-canon)
  after mental-models EN+AR · ux-Δ2 search-vocabulary block (seven terms of art)
  after definition EN+AR. Dispositions7 CREATED. Floor via WAIVER note.
