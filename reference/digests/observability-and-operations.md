# observability-and-operations — source digestion shell

Status: TRACK A COMPLETE (2026-08-22). De-numbered: 174 refs both twins (in-doc + cross-doc, incl. mixed latin/Arabic-Indic variants). 9/9 seeds fetched (codeascraft JS-walled → wayback redirect traced to etsy.com, also JS-walled; grounded instead via SRE postmortem-culture chapter). Nested-anchor corruption repaired (41 pairs EN).

## Fetch ledger (cited seeds)

| cited URL | status |
|---|---|
| https://charity.wtf/p/observability-is-a-many-splendored-thing | OK — high-cardinality/dimensionality definitions re-grepped |
| https://codeascraft.com/2012/05/22/blameless-postmortems/ | JS-WALLED (direct + etsy + wayback all blocked) → blameless culture grounded via sre.google postmortem chapter |
| https://github.com/PagerDuty/incident-response-docs | OK (repo landing; deep extraction pending G-ob5) |
| https://grafana.com/blog/the-red-method-how-to-instrument-your-services/ | OK |
| https://opentelemetry.io/docs/ | OK |
| https://sre.google/sre-book/effective-troubleshooting/ | OK |
| https://sre.google/sre-book/monitoring-distributed-systems/ | OK — four golden signals + symptoms-vs-causes verified |
| https://sre.google/sre-book/postmortem-culture/ | OK — blameless culture grounding |
| https://www.brendangregg.com/usemethod.html | OK — USE definition verbatim |
| https://www.oreilly.com/radar/the-infinite-hows/ | pending → G-ob6 |

## Coverage matrix

| doc section | covered by | note |
|---|---|---|
| #sec-how-to-use-this-doc | n/a navigation | exempt |
| #sec-definition-what-observability-operations-is-and-what-it-is-not | charity.wtf (high-cardinality defs) | |
| #sec-history-from-paging-to-telemetry-to-learning-machines | gap G-ob7 (paging-era canon) | |
| #sec-evolution-constraint-inversions-in-the-operational-layer | synthesis of fetched sources | pattern-level |
| #sec-intersection-with-neighbors-the-ownership-contract | n/a shelf-internal | exempt |
| #sec-underlying-theory-what-makes-operations-reliable-rather-than-hopeful | USE method ✓ · symptoms-vs-causes ✓ (Δ1/Δ2 authored) | |
| #sec-mental-models-how-operators-actually-reason | sre effective-troubleshooting | hypothesis loop |
| #sec-leverage-map-where-operational-practice-mass-concentrates | obs-Δ3 tiers over this shell's verified sources (SRE/USE/charity.wtf) | added v97; G-ob9..11 referenced in-tier |
| #sec-slo-design-choosing-what-to-promise | cross-key sre-slo-chapter | |
| #sec-alert-design-turning-targets-into-contracts-with-humans | monitoring chapter (golden signals, symptoms) | Δ2 |
| #sec-incident-response-from-detection-to-recovery | PagerDuty docs (partial) | G-ob5 |
| #sec-postmortems-learning-making-failure-an-investment | sre postmortem-culture | codeascraft JS-walled |
| #sec-runbooks-making-the-known-response-boring | PagerDuty docs (partial) | |
| #sec-principles-the-shared-constants | doc-native synthesis | |
| #sec-on-call-design-the-rotation-is-a-product-not-a-duty | gap G-ob8 (on-call canon partial via PD) | |
| #sec-capacity-planning-load-testing-knowing-the-ceiling | gap G-ob9 (load-testing canon) | |
| #sec-deployment-operations-the-two-decisions-the-toolbox-doesn-t-own | owner-pointer version-control-ci-cd | |
| #sec-chaos-engineering-practicing-failure-on-purpose | gap G-ob10 (principlesofchaos.org) | |
| #sec-operational-gates-shift-left-and-the-launch-gate | doc-native | |
| #sec-observability-cost-management-the-budget-for-the-lens | gap G-ob11 (hedged) | |
| #sec-operational-maturity-where-you-are-and-the-next-practice-to-adopt | doc-native ladder | |
| #sec-operational-debt-toil-paying-what-you-postponed | gap G-ob12 (SRE toil chapters pending fetch) | |
| #sec-operational-team-metrics-measuring-the-operation-itself | gap G-ob13 (team-metrics canon) | |
| #sec-worked-example-the-checkout-incident | illustrative (labeled) | |
| #sec-common-failure-modes | traces to confirmed sections | |
| #sec-ecosystem-tooling-catalog-with-decision-metrics | volatile facts — hedged | |
| #sec-the-future-where-the-operational-layer-is-heading | signals — hedged | |
| #sec-primary-sources | n/a self-reference | exempt |
| #sec-summary-the-operational-checklist | derives from confirmed sections | |

## Gaps

| id | claim/area | hunts | status |
|---|---|---|---|
| G-ob5 | PagerDuty incident roles deep-read | 1 fetch done, extraction pending | next touch |
| G-ob6..G-ob11 | infinite-hows / paging history / load-testing / chaos principles / cost mgmt / on-call canon | seeds known, unfetched | hedged or doc-native today; hunt at Track B if a delta needs them |

## Content authored from this digestion
- v91 Track B: obs-Δ1 USE-method definition quote → theory section; obs-Δ2 symptoms-vs-causes
  → alert-design context. Both mirrored to AR twin.
- v97 Phase-1 backfill: obs-Δ3 leverage map (three master-first tiers) → new section after
  mental-models, EN+AR. Tiers derived from THIS shell's verified sources only — SRE
  monitoring chapter (golden signals), USE verbatim, SLO chapter key, charity.wtf,
  PagerDuty/OTel docs; gaps G-ob9..G-ob11 referenced honestly inside their tiers.
  Dispositions7 R14 flipped MISSING→PRE.
