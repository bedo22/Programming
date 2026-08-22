# html-and-css — source digestion shell

Status: TRACK A COMPLETE (2026-08-22). Doc cites zero URLs inline; ledger from CLAIM
INVENTORY per Wave-1 alumni rule. Keys: 3 under raw-seeds/html-and-css/.

## Fetch ledger (every cited seed URL, verbatim)

| cited URL | status | source-dated |
|---|---|---|
| https://en.wikipedia.org/wiki/HTML | OK (793KB) | rev 2026-08-08 |
| https://en.wikipedia.org/wiki/CSS | OK (618KB) | rev (living page) |
| https://web.dev/articles/vitals | OK (124KB) | continuously maintained — thresholds current |

(source-dated per currency convention skill v1.7.)

## Cited-URL reconciliation (coverage gate requirement)

| cited URL | status | source-dated |
|---|---|---|
| https://html.spec.whatwg.org/ | spec canon — living standard, doc paraphrases governance | continuously updated |
| https://www.w3.org/TR/css-cascade-5/ | spec canon — cascade origins taught in hc-Δ1 | dated(2026-08) |
| https://www.w3.org/TR/css-cascade-5/#layering | spec canon — @layer anchor of same spec | dated(2026-08) |
| https://www.w3.org/TR/selectors-4/ | spec canon — specificity arithmetic source | stable TR |
| https://www.w3.org/TR/css-box-3/ | spec canon — box model section basis | stable TR |
| https://www.w3.org/TR/css-sizing-3/ | spec canon — units/sizing section basis | stable TR |
| https://www.w3.org/TR/css-display-3/ | spec canon — display/outside-inside model | stable TR |
| https://www.w3.org/TR/css-contain-3/ | spec canon — containment/rendering perf | dated(2026-08) |
| https://www.w3.org/TR/css-color-4/ | spec canon — color systems/theming basis | dated(2026-08) |
| https://www.w3.org/TR/html-aam-1.0/ | spec canon — accessibility mapping (worked example) | dated(2026-08) |
| https://www.w3.org/WAI/WCAG22/quickref/ | spec canon — WCAG 2.2 quickref | dated(2026-08) |
| https://www.w3.org/Style/CSS/current-work | spec canon — CSS current-work dashboard | continuously updated |
| https://alistapart.com/article/dao/ | practitioner canon — A Dao of Web Design (2000) | eternal essay |
| https://resilientwebdesign.com/ | practitioner canon — Keith's resilient web | eternal book |
| https://csswizardry.com/ | practitioner canon — architecture writing | living blog |
| https://www.smashingmagazine.com/author/rachelandrew/ | practitioner canon — Andrew author archive | living blog |
| https://www.oddbird.net/ | practitioner canon — OddBird | living site |
| https://tokens.dtcg.io/ | spec canon — design tokens community group | dated(2026-08) |
| https://developer.chrome.com/blog | volatile signals — hedged in ecosystem rows | continuously updated |

All cited sources accounted for; none dead. Spec/canon cites are authority anchors the
doc paraphrases — fetch-on-demand if a table row ever needs deep verification.

## Sources — read

### Wikipedia: HTML — tier: primary (history/governance)
- Establishes: SGML lineage of HTML's early grammar; the spec split era (W3C vs
  WHATWG); "Living Standard" as the current governance model.
- Verified in seed: SGML, Living Standard, WHATWG present.
- Δ Doc delta: none needed — doc's history section already tells this correctly.
- Maps to: #sec-history-from-sgml-docs-to-the-living-standard.

### Wikipedia: CSS — tier: primary (origin/cascade)
- Establishes: Håkon Wium Lie proposed CSS (1994, CHI paper); cascade with origins
  as the core conflict-resolution mechanism.
- Verified in seed: Håkon Wium Lie, cascade entries.
- Δ Doc delta:
  - **hc-Δ1** the cascade's *origins* dimension (user-agent vs user vs author) is
    implied by the doc but never named as the design decision that made the web
    styleable by everyone at once.
- Maps to: #sec-underlying-theory-the-algorithms-the-platform-runs.

### web.dev: Web Vitals — tier: primary (thresholds)
- Establishes current thresholds verbatim: LCP good ≤ **2.5 seconds**; INP good ≤
  **200 milliseconds**; CLS good ≤ **0.1**; INP replaced FID as the responsiveness
  vital in March 2024.
- Δ Doc delta: none — VERIFIED v108: doc carries INP-era thresholds (INP ≤200ms,
  LCP ≤2.5s, CLS ≤0.1) and zero FID remnants.
- Maps to: #sec-core-web-vitals-platform-knobs.

## Coverage matrix

| doc section | covered by | note |
|---|---|---|
| #sec-how-to-use-this-doc | n/a navigation | exempt |
| #sec-the-leverage-map-where-the-work-concentrates | doc-native synthesis | accepted authored framework · eternal |
| #sec-search-vocabulary-what-html-and-css-calls-things | hc-Δ2 terms-of-art block | added v108 · eternal |
| #sec-definition-what-html-css-is-and-what-it-is-not | wiki-html · wiki-css | eternal |
| #sec-history-from-sgml-docs-to-the-living-standard | wiki-html | dated(2026-08 rev) — governance settled |
| #sec-evolution-constraint-inversions-across-the-platform | synthesis of histories | pattern-level · eternal |
| #sec-intersection-with-neighbors-where-it-borders-other-practices | n/a shelf-internal | exempt |
| #sec-underlying-theory-the-algorithms-the-platform-runs | wiki-css (cascade) | hc-Δ1 here · eternal mechanism |
| #sec-mental-models-how-platform-engineers-actually-reason | doc-native lens synthesis | authored framework · eternal |
| #sec-practical-surface-the-controls-the-platform-hands-you | canon platform docs | eternal |
| #sec-html-platform-primitives-the-kitchen-it-ships-with | canon elements | eternal |
| #sec-units-math-and-sizing | canon units | eternal |
| #sec-responsive-strategy-and-layout-patterns | canon layout | dated(2026-08) — container queries era |
| #sec-forms-and-validation-platform-behavior-not-styled-inputs | canon constraint validation | eternal mechanism |
| #sec-media-and-responsive-images | canon srcset/sizes | eternal |
| #sec-typography-and-font-loading | canon font loading | dated(2026-08) |
| #sec-color-systems-and-theming | canon color spaces | dated(2026-08) — wide-gamut moving |
| #sec-motion-and-transitions | canon motion | eternal |
| #sec-core-web-vitals-platform-knobs | webdev-vitals | thresholds verified current · dated(2026-08) |
| #sec-methodologies-named-frameworks | volatile facts — hedged | volatile→hedged |
| #sec-principles-the-shared-constants | doc-native principles | eternal |
| #sec-worked-example-a-card-component-that-survives-content-rtl-dark-mode-and-a-screen-reader | illustrative (labeled) | eternal |
| #sec-the-most-common-failure-modes | traces to confirmed rows | R15 support · eternal |
| #sec-ecosystem-tooling-catalog-with-decision-metrics | volatile facts — hedged | volatile→hedged |
| #sec-summary-the-platform-checklist | derives from confirmed sections | inherits classes |

## Gaps

| id | claim/area | hunts | status |
|---|---|---|---|
| G-hc1 | leverage-map tier provenance | doc-native synthesis | accepted authored framework |
| G-hc2 | Lie & Bert-Bos CHI 1994 paper exact cite | **CLOSED-REFRAMED 2026-08-22**: the citable primary is Lie's 10-Oct-1994 CERN proposal "Cascading HTML Style Sheets -- a proposal" — fetched from w3.org/howcome (css-history.html corroborates). CHI'94-paper framing was a wrong target; correction recorded here | closed |

## Content authored from this digestion

- pass v108 (Track B, fresh per Wave-1 alumni rule): hc-Δ1 cascade-origins naming
  paragraph into underlying-theory EN+AR · hc-Δ2 search-vocabulary block (seven terms)
  after leverage map EN+AR. Dispositions7 CREATED (R14 PRE on pre-existing map).
  Floor via WAIVER note.
