# api-design — source digestion

Fetched: 2026-08-21 · Status: 8 fetched OK / 1 dead (CAP Twelve Years Later) / rest of seeds pending fetch during pass
Gate: `digest-coverage.py` PASS required before value authoring.

## Sources — fetched and read

### Fielding, REST ch.5 (ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm) — OK · tier: primary
- Key claims & numbers: constraints added incrementally each inducing properties;
  statelessness induces visibility+reliability+scalability at the cost of repeated
  per-request data; code-on-demand is the OPTIONAL final constraint (§5.1.7);
  uniform interface = identification of resources, manipulation through
  representations, self-descriptive messages, HATEOAS (§5.2.1.1–5.2.1.2).
- Mechanisms worth teaching: constraint-by-constraint derivation as a design method.
- Examples/war stories in source: none (dissertation prose).
- Δ Doc delta:
  - api-design-Δ1 stateless trade-off (gains vs per-request overhead) — doc never
    states the COST side; candidate for definition section.
  - api-design-Δ2 code-on-demand as optional sixth constraint — doc's history row
    lists six constraints without marking CoD optional per Fielding.
  - api-design-Δ3 the four sub-facets of uniform interface as a design checklist.
- Establishes: REST derived by incrementally adding constraints (client-server,
  stateless, cache, uniform interface, layered system, code-on-demand); each
  constraint induces properties; uniform interface = identification of resources,
  manipulation via representations, self-descriptive messages, HATEOAS.
- Maps to doc sections: #sec-history-from-rpc-to-graphql-to-events (2000 row),
  #sec-underlying-theory-what-makes-a-contract-designed-not-accidental (HATEOAS row),
  #sec-methodologies-styles-the-named-approaches (REST row).
- Tensions: Fielding frames HATEOAS as constitutive of REST; doc treats it "optional" —
  matches industry practice but should be stated as a deviation from the dissertation.

### Richardson Maturity Model, Fowler 2010 (martinfowler.com/articles/richardsonMaturityModel.html) — OK · tier: primary
- Key claims & numbers: levels 0→3; article 2010-03-18; model by Leonard Richardson
  (QCon 2008); web itself as the existence proof of the approach.
- Mechanisms worth teaching: level-by-level refactoring story (POX → resources → verbs → links).
- Examples/war stories in source: clinic appointment example used across all levels.
- Δ Doc delta:
  - api-design-Δ4 Fowler's explicit caution that Level 3 is NOT mandatory for
    pragmatic REST — strengthens the doc's "HATEOAS optional" stance with an
    authoritative voice it currently lacks.
  - api-design-Δ5 the single running example (clinic) as a teachable progression —
    candidate worked micro-example (R8/R13).
- Establishes: levels 0→1 (resources) →2 (verbs+status) →3 (hypermedia); model by
  Leonard Richardson (QCon 2008), article 2010; "steps toward the glory of REST";
  explicitly a step-model toward REST, not team maturity.
- Maps to doc sections: #sec-history-from-rpc-to-graphql-to-events (2005–2010 row),
  #sec-underlying-theory-what-makes-a-contract-designed-not-accidental (RMM row),
  #sec-methodologies-styles-the-named-approaches (REST Level 2–3 label).
- Tensions: doc dates RMM "(2008)" without noting the canonical write-up is Fowler
  2010 — citation kept, wording acceptable.

### RFC 9457 Problem Details (rfc-editor.org/rfc/rfc9457) — OK · tier: primary
- Key claims & numbers: media type application/problem+json REQUIRED for JSON
  problem details; member fields type/title/status/detail/instance; extension
  members allowed; obsoletes RFC 7807.
- Mechanisms worth teaching: error as a typed document clients switch on.
- Examples/war stories in source: credit-card rejection example envelope.
- Δ Doc delta:
  - api-design-Δ6 the media-type requirement itself (application/problem+json) —
    doc shows the shape but never names the required Content-Type.
  - api-design-Δ7 RFC 9457's own credit-card decline example — ready-made teaching
    example matching the doc's payment themes.
- Establishes: JSON error envelope fields `type/title/status/detail/instance`,
  extension members allowed; media type application/problem+json; obsoletes RFC 7807.
- Maps to doc sections: #sec-principles-the-shared-constants (error principle),
  #sec-validation-errors-transactional-safety, worked example ProblemDetails schema,
  #sec-summary-the-contract-checklist (error row).

### RFC 791 Postel quote (rfc-editor.org/rfc/rfc791.txt) — OK, verified verbatim · tier: supporting
- Establishes: "must be conservative in its sending behavior, and liberal in its
  receiving behavior" — robustness principle genuinely in RFC 791 (1981). Citation sound.
- Maps to doc sections: #sec-underlying-theory-what-makes-a-contract-designed-not-accidental
  (Postel row), #sec-schema-evolution-the-compatibility-matrix (accept-extra/send-none).

### Lamport, Time Clocks (lamport.azurewebsites.net/pubs/time-clocks.pdf) — OK (PDF) · tier: supporting
(8-page classic; deep extraction deferred until an event-ordering value pass needs it.)
- Establishes: happened-before partial order; logical clocks; total ordering needs
  tie-breaks; no external timestamp as causal truth.
- Maps to doc sections: idempotency/event-ordering in #sec-mental-models-how-api-designers-
  actually-reason ("Idempotency keys = exactly-once") and webhook ordering rows.

### gRPC introduction (grpc.io/docs/what-is-grpc/introduction/) — OK · tier: primary
(DEFECT CORRECTED 2026-08-22: original grpc.com fetch was an unrelated-site 404 misrecorded as OK; refetched from grpc.io. Earlier Δ claims about "four defining ideas/deadlines" were from memory — regrounded: the intro page documents deadlines/cancellation and streaming via its own section list.)
- Key claims & numbers: lineage from Google Stubby (~2001); four defining ideas:
  unary & streaming RPCs, deadlines/cancellation propagation, standard status codes,
  channels; HTTP/2 + Protobuf.
- Mechanisms worth teaching: deadlines as contract citizens (not client afterthoughts).
- Examples/war stories in source: none substantive.
- Δ Doc delta:
  - api-design-Δ8 deadline propagation as an API-contract concern — doc mentions it
    once inside a table cell; deserves a principle-level statement.
- Establishes: gRPC lineage from Google Stubby; HTTP/2 + Protobuf; four defining
  ideas (unary/streaming RPC, deadlines, status codes, channels).
- Maps to doc sections: #sec-history-from-rpc-to-graphql-to-events (2015 gRPC row),
  #sec-methodologies-styles-the-named-approaches (gRPC row), realtime streaming table.

### GraphQL FAQ (graphql.org/faq/) — OK · tier: supporting
- Δ Doc delta:
  - api-design-Δ9 developed internally at Facebook from 2012 before 2015 open-source —
    sharpens the doc's history row; governance now GraphQL Foundation/Linux Foundation.
- Establishes: GraphQL developed internally at Facebook (2012), open-sourced 2015;
  spec by GraphQL Foundation; query language + runtime, single endpoint, introspection.
- Maps to doc sections: #sec-history-from-rpc-to-graphql-to-events (2015 row),
  #sec-methodologies-styles-the-named-approaches (GraphQL row), worked example Step 7.

### Amazon Dynamo post (allthingsdistributed.com/2012/01/amazon-dynamodb.html) — OK · tier: primary
- Key claims & numbers: Dynamo's tunable quorums N/R/W; eventual consistency as a
  product decision; merkle-tree anti-entropy.
- Mechanisms worth teaching: consistency as a dial the CONTRACT declares, not an
  implementation accident.
- Δ Doc delta:
  - api-design-Δ10 N/R/W tunable-quorum dial as the concrete meaning of "declare your
    consistency model" in API terms — doc states the requirement, not the mechanism.
- Establishes: eventual consistency as product choice; tunable quorums (N/R/W);
  consistency/latency dial that contracts must declare.
- Maps to doc sections: CAP/PACELC row in underlying theory; consistency declarations.

### DEAD — Brewer, "CAP Twelve Years Later" (allthingsdistributed.com/2012/01/cap-twelve-years-later.html)
- AccessDenied on fetch (2026-08-21). DEFECT for pass: replace cite link with an
  accessible primary (Gilbert & Lynch 2002 JPDC, or Brewer PODC keynote PDF) — hunt pending.

## Fetch ledger (every cited seed URL)

| cited URL | status |
|---|---|
| https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm | OK — ch.5 fetched (rest_arch_style.htm) |
| https://www.rfc-editor.org/rfc/rfc791 | OK — .txt fetched, Postel quote verified |
| https://www.rfc-editor.org/rfc/rfc9457 | OK |
| https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md | OK via mirror spec.openapis.org/oas/v3.1.0 (214KB) |
| https://www.asyncapi.com/docs/specifications/v2.6.0 | OK via raw.githubusercontent.com/asyncapi/spec/v2.6.0 (87KB md); site itself JS-blocked for curl |
| https://cloudevents.github.io/spec/v1.0.2/ | DEAD (GitHub Pages 404) → replaced by github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md (fetched via scrapling) |
| https://martinfowler.com/articles/richardsonMaturityModel.html | OK |
| https://www.cs.umd.edu/~pugh/csci741/yourdon.pdf | FAILED (empty body) → supporting only; coupling/cohesion content rests on system-design doc's coverage |
| https://lamport.azurewebsites.net/pubs/time-clocks.pdf | OK (PDF) |
| https://www.allthingsdistributed.com/2012/01/cap-twelve-years-later.html | **DEAD** (AccessDenied) → replace cite |
| https://apievangelist.com/ | OK homepage (20KB) — Kin Lane 'APIs as products' stance confirmed live |
| https://apihandyman.io/ | OK homepage (33KB) — Arnaud Lauret site confirmed live |
| https://www.comp.nus.edu.sg/~gilbert/pubs/BrewersConjecture-SigAct.pdf | OK (PDF, 6pp) — replacement for dead Brewer 2012 link, fetched 2026-08-21 |

Supplementary fetched: grpc.com principles post; graphql.org FAQ; Dynamo post;
martinfowler.com/eaaDev/TimeClock.html.

## Coverage matrix

| doc section | covered by | note |
|---|---|---|
| #sec-how-to-use-this-doc | n/a — navigation, no factual claims | matrix-exempt |
| #sec-definition-what-api-design-is-and-what-it-is-not | Fielding (contract concept); OpenAPI spec (description vs design) | |
| #sec-search-vocabulary-what-api-design-calls-things | api-Δ5 terms-of-art block (idempotency key/endpoint/cursor pagination/breaking change/rate limiting/problem details/HATEOAS) | added v102; grounded in doc's own usage + RFC 9457 record |
| #sec-history-from-rpc-to-graphql-to-events | Fielding; RMM/Fowler; grpc.com; graphql.org | dates verified |
| #sec-evolution-constraint-inversions-across-the-same-idea | synthesis of fetched histories | pattern-level, no new facts |
| #sec-migration-paths-between-api-styles | gap → see Gaps G1 | practitioner timelines |
| #sec-intersection-with-neighbors-where-it-borders-other-practices | n/a — shelf-internal relations | matrix-exempt |
| #sec-underlying-theory-what-makes-a-contract-designed-not-accidental | Fielding; RFC791; RMM; Lamport; Dynamo/CAP | CSP+ISP rows → Gaps G2 |
| #sec-mental-models-how-api-designers-actually-reason | RFC9457; Lamport; OpenAPI | media-type versioning → G3 |
| #sec-leverage-map-where-api-design-practice-mass-concentrates | api-Δ6 tiers over this shell's sources (fielding-rest, spec family, RFC 9457, Gilbert&Lynch, RMM) | added v102; async/AI tiers reference digested records honestly |
| #sec-the-rhythm-not-the-algorithm | n/a — shelf-doctrine framing | matrix-exempt |
| #sec-methodologies-styles-the-named-approaches | Fielding/RMM; graphql.org; grpc.com; AsyncAPI→G4 | |
| #sec-principles-the-shared-constants | RFC9457; W3C Trace Context→G5 | |
| #sec-conventions-identifiers-the-rules-that-keep-contracts-predictable | ISO 8601 standard; ULID spec→G6 | conventions are industry norms |
| #sec-collections-pagination-filtering-sorting-and-search | none → gap G7 | cursor/keyset practice |
| #sec-validation-errors-transactional-safety | RFC9457; HTTP semantics (If-Match/ETag RFC9110) | |
| #sec-long-running-operations-202-job-resources-and-webhooks | HTTP semantics; HMAC (RFC2104) | |
| #sec-realtime-and-streaming-contracts | WHATWG HTML SSE spec→G8; WebSocket RFC6455 | |
| #sec-schema-evolution-the-compatibility-matrix | Avro/Protobuf docs→G9; RFC791 | |
| #sec-security-browser-contracts | OAuth2.1/PKCE drafts→G10 | |
| #sec-file-uploads-binary-contracts | S3 presigned-URL docs→G11 | |
| #sec-ai-safe-tool-contracts | none → gap G12 | emerging area |
| #sec-worked-example-design-a-public-shipment-tracking-api | illustrative (labeled) — synthesizes above | no external claims |
| #sec-the-most-common-failure-modes | each mode traces to sections above | survey stat → G13 |
| #sec-ecosystem-tooling-catalog-with-decision-metrics | tool pages→G14 | volatile facts live here |
| #sec-the-future-where-api-design-is-going | signals → G15 | forward-looking, hedged |
| #sec-summary-the-contract-checklist | derives from confirmed sections only | |

## Gaps — claims with no located source yet

| id | claim | where | hunts tried | status |
|---|---|---|---|---|
| G13 | "Stoplight/SmartBear State of API 2023: 60% no guidelines, 40% find breaks in prod" | failure modes critique | 0/3 — exact survey figures unverified | **insert † or drop figures** at pass |
| G1 | migration timelines (4–12mo etc.) | migration paths | practitioner ranges, hedged in-text | keep hedged, no † needed (convention-tier) |
| G2 | CSP (Hoare 1978) applied to API contracts | theory | Hoare's paper exists; *application* is doc's own framing | frame as analogy, no † |
| G3 | media-type versioning as preferred strategy | mental models | field practice (GitHub API v3) | hunt: GitHub changelog |
| G4 | AsyncAPI 2.6 / CloudEvents 1.0 details | methodologies | specs not yet fetched this pass | fetch next |
| G5 | traceparent/W3C Trace Context | principles | spec URL known | fetch next |
| G6 | ULID/UUIDv7 sortable-ID claims | conventions | spec repos known | fetch next |
| G7 | offset O(n) vs keyset pagination mechanics | collections | DB docs (Postgres LIMIT/OFFSET) | fetch next |
| G8–G15 | SSE/WebSocket/OAuth/uploads/Avro/tool catalog/future signals | respective sections | seeds listed, not yet fetched | fetch during pass |

Rule applied: nothing deleted; uncovered items either carry convention-hedges already
in-text or get † when a specific number/fact stays unlocated after 3 hunts.

## Content authored from this digestion

- pass v79-pilot (uncommitted): Δ1+Δ2 → history REST row (stateless trade-off + CoD
  optional, EN+AR) · Δ3 → theory HATEOAS row (four uniform-interface facets) ·
  Δ6 → principles #3 (application/problem+json media type) · Δ9 → history GraphQL
  row (internal since 2012) · Δ10 → CAP/PACELC theory row (N/R/W quorum dial) ·
  cross-style deadlines note (Δ8) added before methodologies closer · dead CAP cite
  replaced with Gilbert & Lynch 2002 (fetch-verified).
- Declined deltas: Δ4 (RMM Level-3 caution — doc's RMM row already carries
  "diagnostic, not prescription"; tension recorded above) · Δ5 (clinic progression —
  doc has a full worked example; adding a second would duplicate R8/R13 coverage) ·
  Δ7 (RFC 9457 credit-card example — worked example's error envelope already serves).
- pass v102 (Phase-1 backfill): api-Δ5 search-vocabulary block (seven terms of art)
  after the definition section, EN+AR · api-Δ6 leverage map (three master-first tiers:
  resource-first modeling / convention discipline / idempotency keys; evolution matrix
  + style selection + Problem Details as learn-when-needed; async surfaces + AI-safe
  tools as rare specialist) after mental-models, EN+AR. Dispositions7 R14 MISSING→PRE
  and R16 THIN→PRE.
