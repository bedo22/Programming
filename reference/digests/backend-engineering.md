# backend-engineering — source digestion shell

Status: TRACK A COMPLETE (2026-08-22). 5 unique cited URLs reconciled per v1.7
currency conventions — platform canon (Express guide, MDN HTTP caching), canon wiki
(race condition, database transaction/ACID), one practitioner essay (Fowler session
boundaries). No XML-namespace artifacts; no zero-cite case. The doc's mechanics are
doc-native teaching grounded in those canon references, with facts delegated to
sibling owner docs by design.

## Cited-URL reconciliation (coverage gate requirement)

| cited URL | status | source-dated |
|---|---|---|
| https://expressjs.com/en/guide/writing-middleware.html | platform canon — official Express middleware guide (onion ordering) | continuously updated |
| https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching | platform canon — MDN HTTP caching reference (Cache-Control, ETag) | continuously updated |
| https://en.wikipedia.org/wiki/Race_condition | canon wiki — what two concurrent requests collide on | living page |
| https://en.wikipedia.org/wiki/Database_transaction | canon wiki — atomic reads/writes, ACID definition | living page |
| https://martinfowler.com/articles/sessionBoundaryPatterns.html | practitioner canon — Fowler on session/state boundary patterns | living blog |

## Coverage matrix

| doc section | covered by | note |
|---|---|---|
| #sec-how-to-use-this-doc | n/a navigation | exempt |
| #sec-definition-what-backend-engineering-is-and-is-not | doc-native framing of the discipline-as-loop | eternal |
| #sec-history-the-constraint-inversions | doc-native settled history (stateful→stateless, monolith→service, sync→async, SQL→ORM) | dated-once · eternal |
| #sec-intersection-with-the-other-shelves | n/a shelf-internal boundaries | exempt |
| #sec-underlying-theory-the-invariants-to-trust | doc-native invariants (relational model, ACID, C10K, 12-Factor, backpressure, idempotency); ACID mechanics trace to transaction canon (see ledger) | eternal |
| #sec-mental-models-frames-for-thinking-about-the-server | doc-native frames table | authored framework · eternal |
| #sec-rhythm-not-algorithm-the-update-the-loop-discipline | doc-native discipline, aligned to sibling Rhythm doc | eternal |
| #sec-the-backend-mental-model-one-request-at-a-time | doc-native teaching + Fowler session-boundary canon (see ledger) | eternal |
| #sec-the-request-lifecycle-the-timeline-inside-the-brackets | Express middleware-onion canon + doc-native lifecycle timeline | eternal mechanism; framework APIs volatile→hedged |
| #sec-evolution-the-constraint-inversions | doc-native settled inversion history (incl. serverless turn) | dated-once · eternal |
| #sec-authentication-vs-authorization-identity-then-permission | doc-native authn/authz split and IDOR rule; provider landscape hedged to vendor docs | eternal principles · volatile→hedged (provider table) |
| #sec-data-access-orms-vs-raw-sql | doc-native fence-line doctrine; ORM/tool names volatile→hedged | eternal fence · volatile→hedged |
| #sec-the-three-rounds-how-a-server-feature-actually-gets-built | doc-native rounds mapped onto the Rhythm | authored framework · eternal |
| #sec-background-work-queues-jobs-and-why-you-defer | doc-native pattern table with when-to-reach-for column | R18 function · eternal patterns, brokers volatile→hedged |
| #sec-caching-the-three-layers-where-latency-hides | MDN HTTP caching canon + doc-native invalidation discipline | eternal |
| #sec-transactions-and-concurrency-the-row-changed-since-i-read-it | wikipedia DB-transaction/ACID canon + doc-native optimistic locking | eternal |
| #sec-worked-example-trace-the-loop-end-to-end | illustrative (labeled) three-round walkthrough | eternal |
| #sec-state-the-identity-and-session-decision | doc-native revoke-driven decision table; Fowler boundary canon (see ledger) | R18 function · eternal decision rule |
| #sec-crud-the-shape-of-most-web-apps | doc-native verb-by-verb discipline | eternal |
| #sec-ecosystem-tooling-catalog-with-decision-metrics | trigger→target + decision-metric columns are doc-native; tool lists volatile — hedged | R18 function · volatile→hedged |
| #sec-observability-see-the-loop-not-just-run-it | doc-native signal table; operations delegated to Observability & Operations owner doc | eternal practice |
| #sec-error-handling-the-error-is-part-of-the-contract | doc-native status/error contract | eternal |
| #sec-the-most-common-failure-modes | traces back to confirmed sections; concurrency collisions ground in race-condition canon (see ledger) | R15 support · eternal |
| #sec-summary-the-complete-mental-checklist | derives from confirmed sections | inherits classes |

## Gaps

| id | claim/area | hunts | status |
|---|---|---|---|
| G-pool1 | Pool arithmetic (~10MB/connection, PgBouncer transaction- vs session-mode trade-offs) is doc-native approximation, uncited in-doc | verify against current PostgreSQL/PgBouncer docs next touch | convention-tier hedge |
| G-auth1 | Managed-auth feature lists (Auth0/Clerk/Auth.js/devise rows) shift quarterly | doc already routes specifics to provider docs + Security & Threat Modeling | volatile→hedged · fetch next touch |

## Content authored from this digestion

- Track B row: justified N/A this pass — rich authored doc delegating facts to
  cited canon and sibling owner docs; recorded per SHELF-DONE rule
  (additions OR justified N/A). HTML docs untouched.
