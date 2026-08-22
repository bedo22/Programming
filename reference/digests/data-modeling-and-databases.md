# data-modeling-and-databases — source digestion shell

Status: TRACK A COMPLETE (2026-08-22). 6 unique cited URLs reconciled per v1.7 currency conventions.

## Cited-URL reconciliation (coverage gate requirement)

| cited URL | status | source-dated |
|---|---|---|
| https://cacm.acm.org/research/a-relational-model-of-data-for-large-shared-data-banks-2/ | canon — eternal paper (Codd's relational model, ACM reprint) | eternal |
| https://martinfowler.com/bliki/ParallelChange.html | practitioner canon — living blog (Fowler bliki; expand/contract migration pattern) | living blog |
| https://use-the-index-luke.com/ | practitioner canon — living book site (Winand, SQL indexing) | living book site |
| https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/ | canon book cite — DDIA (Kleppmann); publisher store page, not fetched | eternal book |
| https://www.postgresql.org/docs/current/indexes-types.html | platform canon — official PostgreSQL manual, continuously updated | current version |
| https://www.postgresql.org/docs/current/using-explain.html | platform canon — official PostgreSQL manual, continuously updated | current version |

## Coverage matrix

| doc section | covered by | note |
|---|---|---|
| #sec-how-to-use-this-doc | n/a navigation | exempt |
| #sec-definition-what-data-modeling-is-and-what-it-is-not | doc-native teaching + cited canon (see ledger) | eternal principles; volatile facts hedged |
| #sec-history-from-navigational-to-relational-and-back | doc-native teaching + Codd eternal paper (see ledger) | dated-once · eternal (paper fixed 1970; era narrative doc-native) |
| #sec-intersection-with-neighbors | n/a shelf-internal pointers | exempt (owner-pointers, no external claims) |
| #sec-underlying-theory-the-invariants-to-trust | doc-native teaching + Codd paper + DDIA canon (see ledger) | eternal principles |
| #sec-mental-models-frames-for-thinking-about-the-vault | doc-native frames (vault/schema-as-contract/access paths) | authored synthesis; eternal framing |
| #sec-relational-modeling-keys-constraints-and-normalization-1nf3nf | doc-native teaching + Codd-lineage normalization theory | eternal principles |
| #sec-relationship-patterns-cardinality-and-keys | doc-native pattern catalog | eternal patterns; R18 function |
| #sec-data-types-choosing-column-types | doc-native teaching + Postgres platform canon (see ledger) | eternal tradeoffs; type lists track engine versions → hedged |
| #sec-constraints-the-enforcement-toolkit | doc-native teaching + Postgres platform canon | eternal semantics; syntax per current version |
| #sec-indexing-strategies-the-read-path | doc-native teaching + use-the-index-luke + indexes-types platform canon (in-text cite) | eternal strategy; engine specifics per current version |
| #sec-reading-explain-analyze-the-tuning-loop | doc-native teaching + using-explain platform canon (in-text cite) | command shape per current version → hedged |
| #sec-schema-evolution-migrations-as-design-decisions | doc-native teaching + ParallelChange practitioner canon (expand/contract) | living practice; dated-once · eternal |
| #sec-cap-applied-to-schema-design | doc-native teaching + DDIA canon framing | eternal theory applied |
| #sec-isolation-levels-the-transaction-knob | doc-native teaching + Postgres platform canon | levels defined by SQL standard/engine docs → hedged to current version |
| #sec-beyond-the-relational-default-read-models-and-event-sourcing | doc-native teaching + DDIA canon | eternal patterns; tooling volatile → hedged |
| #sec-views-and-materialized-views-shaping-reads-without-duplicating-writes | doc-native teaching + Postgres platform canon | eternal semantics; feature details per current version |
| #sec-multi-tenancy-sharing-the-vault-safely | doc-native teaching | eternal tradeoff space (shared schema/schemas/DB-per-tenant) |
| #sec-schema-in-code-orms-query-builders-raw-sql | doc-native teaching | library landscape volatile → hedged |
| #sec-principles-the-shared-constants | doc-native principles | eternal |
| #sec-worked-example-design-the-schema-for-a-shipment-tracking-system | illustrative worked example (labeled) | derives from confirmed sections |
| #sec-most-common-failure-modes | doc-native failure diagnostics | R15 support |
| #sec-ecosystem-tooling-catalog-with-decision-metrics | doc-native catalog | volatile tooling facts → hedged; decision tables carry R18 function |
| #sec-the-future-where-data-modeling-is-going | signals — hedged | volatile |
| #sec-summary-the-complete-mental-checklist | derives from confirmed sections | checklist distillation |

## Gaps

| id | claim/area | hunts | status |
|---|---|---|---|
| G-data1 | exact version-pinned syntax for constraints/indexes/isolation (docs move with `/current/`) | pin release notes on next touch if a claim ever needs a frozen version | convention-tier hedge |

## Content authored from this digestion

- Track B row: justified N/A this pass — rich authored doc delegating facts to cited canon; recorded per SHELF-DONE rule.
