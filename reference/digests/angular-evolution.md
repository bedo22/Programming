# angular-evolution — source digestion shell

Status: TRACK A COMPLETE (2026-08-22). Nine cited URLs, all official Angular canon
(platform documentation, continuously updated) plus one Dan Abramov essay. Platform
canon treated as authority anchors per house convention; fetch-on-demand.

## Cited-URL reconciliation (coverage gate requirement)

| cited URL | status | source-dated |
|---|---|---|
| https://angular.dev/guide/signals | platform canon — Signals guide | continuously updated |
| https://angular.dev/guide/zoneless | platform canon — Zoneless guide | continuously updated |
| https://angular.dev/guide/http/http-resource | platform canon — httpResource | experimental→stable per table in doc; volatile→hedged |
| https://angular.dev/reference/releases | platform canon — release reference | continuously updated |
| https://angular.dev/events/v22 | event page — v22 signals-era marker | dated(2026) |
| https://angular.io/guide/standalone-components | legacy-domain canon (pre-rename) | dated(legacy) |
| https://angular.io/guide/incremental-update | legacy-domain canon — update paths | continuously updated |
| https://blog.angular.dev/angular-18-zoneless-change-detection-8c235775ddec | official blog — zoneless RFC/rollout | dated(2024 post) |
| https://overreacted.io/why-isnt-x-a-hook/ | Dan Abramov essay — why Angular-style DI resists hooks | eternal essay |

All cited sources accounted for. Version-specific claims inside the doc (v17–v22 API
arrival table, signal forms stability) are already hedged in-text per v1.7.

## Coverage matrix

| doc section | covered by | note |
|---|---|---|
| #sec-how-to-use-this-doc | n/a navigation | exempt |
| #sec-definition-what-angular-evolution-is | doc-native framing | eternal |
| #sec-the-three-eras-a-timeline | blog canon + release reference | dated(2026) |
| #sec-evolution-the-constraint-inversions | synthesis across eras | R17 function · eternal |
| #sec-intersection-with-the-rest-of-the-shelf | n/a shelf-internal | exempt |
| #sec-underlying-theory-what-makes-angular-s-reactivity-work | signals guide + doc-native theory | eternal mechanism |
| #sec-era-1-angularjs-20102016-dirty-checking-and-scope | history — settled | dated-once · eternal |
| #sec-era-2-angular-2-20162023-classes-typescript-zone-js | history — settled; typescript seed corroborates TS shift | eternal |
| #sec-era-3-modern-angular-2023present-signals-standalone-zoneless | angular.dev guides (signals/zoneless/httpResource) | volatile→hedged (version table) |
| #sec-mental-models-how-to-think-in-each-era | doc-native lenses | authored framework · eternal |
| #sec-the-three-eras-through-one-lens-where-state-lives-and-who-watches-it | doc-native unifying lens | eternal |
| #sec-why-angular-didn-t-follow-react-s-hooks-path | overreacted.io essay + DI section | eternal reasoning |
| #sec-signals-vs-rxjs-which-tool-for-which-job | decision table | R18 · eternal |
| #sec-reading-angular-at-work | doc-native reading guide | eternal |
| #sec-lifecycle-translation-angularjs-angular-2-react | doc-native translation tables | eternal |
| #sec-migration-paths | update-guide canon | volatile→hedged |
| #sec-worked-example-a-counter-across-the-eras | illustrative (labeled) | eternal |
| #sec-failure-modes | traces to confirmed rows | R15 support · eternal |
| #sec-principles | doc-native principles | eternal |
| #sec-ecosystem-and-tooling-catalog | volatile tooling — hedged | volatile→hedged |
| #sec-where-angular-stands-now-2026 | signals — hedged; events/v22 anchor | volatile→hedged |
| #sec-summary-checklist | derives from confirmed sections | inherits classes |
| #sec-primary-sources-and-further-reading | reconciliation ledger above | exempt |

## Gaps

| id | claim/area | hunts | status |
|---|---|---|---|
| G-ae1 | zoneless rollout current status | blog RFC fetched-not-needed; release reference is the live authority | convention-tier (platform canon) |

## Content authored from this digestion

- Track B row: the four missing AR h3 blocks in era-3 were restored at v117
  (control flow / Signals API surface / DI / forms generations) — that sync IS this
  pass's addition work; recorded here for SHELF-DONE completeness.
