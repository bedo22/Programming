# system-design — source digestion shell

Status: TRACK A — matrix complete (2026-08-22). Keys: 6 written (twelve-factor-app,
reactive-manifesto, fowler-microservices-article, c4-model-brown, team-topologies-book
[partial], parnas-criteria [via fetched PDF]) + cross-doc keys (lamport-time-clocks,
gilbert-lynch-brewers-conjecture, amazon-dynamo-post, sre-slo-chapter).

## Fetch ledger (every cited seed URL, verbatim)

| cited URL | status |
|---|---|
| https://www.cs.umd.edu/~pugh/csci741/yourdon.pdf | FAILED empty → coupling/cohesion rests on cs-and-se doc |
| https://www.win.tue.nl/~wstomv/edu/2ip30/references/criteria_for_modularization.pdf | OK (PDF 6pp, extracted) — REPLACEMENT for dead cs.cmu.edu ParnasCriteria.pdf (404), repaired in both twins |
| https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612 | book cite skipped — GoF canon |
| https://www.amazon.com/Distributed-Systems-Principles-Paradigms-Andrew-Tanenbaum/dp/0132392275 | book cite skipped — Tanenbaum canon |
| https://www.microsoft.com/en-us/research/publication/paxos-made-simple/ | PENDING fetch → G-sd2 |
| https://www.allthingsdistributed.com/2006/06/you_build_it_you_run_it.html | PENDING fetch → G-sd9 |
| https://12factor.net/ | OK → key twelve-factor-app |
| https://www.reactivemanifesto.org/ | OK → key reactive-manifesto |
| https://martinfowler.com/articles/microservices.html | OK → key fowler-microservices-article |
| https://www.amazon.com/Building-Microservices-Designing-Fine-Grained-Systems/dp/1491950358 | book cite skipped — Newman canon |
| https://www.domainlanguage.com/ddd/ | book/site cite skipped — Evans canon → G-sd7 |
| https://www.amazon.com/Implementing-Domain-Driven-Design-Vaughn-Vernon/dp/0321834577 | book cite skipped — Vernon canon → G-sd7 |
| https://cognitect.com/blog/2011/8/12/architecture-decision-records | PENDING fetch → G-sd8 |
| https://teamtopologies.com/ | OK → key team-topologies-book (extraction partial) |
| https://www.usenix.org/conference/atc16/technical-sessions/presentation/woodward | PENDING fetch → G-sd10 (C4 USENIX paper; c4model.com already keyed) |

Supplementary fetched: c4model.com; parnas replacement PDF (extracted).

## Coverage matrix

| doc section | covered by | note |
|---|---|---|
| #sec-how-to-use-this-doc | n/a navigation | exempt |
| #sec-search-vocabulary-what-system-design-calls-things | sd-Δ1 terms-of-art block (bounded context/idempotency/sharding/eventual consistency/circuit breaker/backpressure/hot key/cache stampede) | added v105; grounded in doc's own usage |
| #sec-definition-what-system-design-is-and-what-it-is-not | fowler-microservices-article ("no precise definition… suites of independently deployable services") | |
| #sec-history-from-flowcharts-to-distributed-systems | twelve-factor-app · reactive-manifesto · fowler-microservices-article | book rows (GoF/Tanenbaum) = canon cites, skipped |
| #sec-evolution-paradigms-through-one-lens | fowler-microservices-article | pattern synthesis doc-native |
| #sec-migration-paths-between-architectures | gap G-sd1 | practitioner timelines, hedged |
| #sec-intersection-with-neighbors | n/a shelf-internal | exempt |
| #sec-underlying-theory-what-makes-a-system-designed-not-assembled | parnas-criteria (information hiding, PDF-extracted) · gilbert-lynch-brewers-conjecture (CAP proof) · lamport-time-clocks (scanned; ordering claims rest on canon summary) | CSP/Amdahl/erasure rows → G-sd2 |
| #sec-mental-models-how-architects-actually-reason | gap G-sd3 (doc-native lens synthesis) | |
| #sec-leverage-map-where-system-design-practice-mass-concentrates | sd-Δ2 tiers over this shell's sources (parnas-criteria PDF, Gilbert&Lynch CAP, fowler-microservices, Dynamo, SRE SLO) | added v105; pending-fetch tiers honestly hedged (G-sd2/4/7) |
| #sec-architectural-layer-macro-patterns-with-consequences | fowler-microservices-article | |
| #sec-capacity-planning-how-to-estimate-load-storage-and-latency | gap G-sd4 (Little's Law primary unlocated; formulas standard) | |
| #sec-data-architecture-storage-partitioning-replication-and-evolution | amazon-dynamo-post (eventual-consistency passage) | |
| #sec-caching-architecture-where-to-cache-what-to-cache-and-how-to-invalidate | gap G-sd5 (cache patterns practitioner canon) | |
| #sec-event-and-queue-reliability-the-operational-layer-under-async | asyncapi keys via api-design? no → gap G-sd6 (outbox/DLQ canon pending); cloudevents-spec covers envelope only | |
| #sec-reliability-and-disaster-recovery-slos-degradation-and-recovery | sre-slo-chapter | |
| #sec-observability-designing-systems-that-can-be-understood-in-production | owner-pointer to observability-and-operations doc | |
| #sec-component-layer-micro-where-system-design-meets-code | gap G-sd7 (Evans/Vernon DDD books skipped) | bounded-context canon |
| #sec-why-it-is-a-method-not-an-algorithm | gilbert-lynch-brewers-conjecture (CAP forbids CP+AP row) | |
| #sec-worked-example-design-a-url-shortener | illustrative (labeled) | |
| #sec-worked-example-design-an-event-driven-order-system | illustrative (labeled) | |
| #sec-methodologies-heuristics | twelve-factor-app · reactive-manifesto · c4-model-brown · team-topologies-book(partial) | ADR origin → G-sd8 (Nygard fetch pending) |
| #sec-common-failure-modes | traces to confirmed sections | |
| #sec-ecosystem-tooling-catalog-with-decision-metrics | volatile facts — hedged | |
| #sec-the-future-where-system-design-is-going | signals — hedged | |
| #sec-summary-the-architectural-checklist | derives from confirmed sections | |

## Gaps

| id | claim/area | hunts | status |
|---|---|---|---|
| G-sd1 | migration timeline ranges | hedged conventions in-text | convention-tier, no † needed |
| G-sd2 | CSP/Amdahl/erasure-coding theory rows | canon papers known but unfetched | fetch on next touch |
| G-sd3 | six mental-model lenses provenance | doc-native synthesis (no external assertion) | accepted authored framework |
| G-sd4 | Little's Law L=λW attribution | **CLOSED 2026-08-22**: _debt-harvest/littles-law.html — L=λW verbatim + Little's 1961 proof noted | closed |
| G-sd5 | cache stampede/hot-key patterns | **CLOSED 2026-08-22**: _debt-harvest/cache-stampede.html concept page + Vattani "Cache Stampede Prevention" citation; Zhang candidate superseded (not needed) | closed |
| G-sd6 | outbox/DLQ canonical write-ups | **CLOSED 2026-08-22**: microservices.io transactional-outbox + Azure Service Bus dead-letter queues docs fetched | closed |
| G-sd7 | DDD strategic design (Evans/Vernon) | books skipped | accepted as canon cite |
| G-sd8 | ADR origin (Nygard 2011 blog) | **CLOSED 2026-08-22**: Nygard "Documenting Architecture Decisions" (2011) fetched, title/author/date verbatim | closed |

## DEFECTS found & fixed
- Parnas cite dead 404 → replaced with win.tue.nl PDF; text EXTRACTED via pdf-inspector
  (6pp): confirms information-hiding thesis — "modules should hide design decisions
  likely to change" framing grounded.

## Content authored from this digestion
- v77 additions predate UDA; grounding migration tracked in skill sources.md.
- pass v105 (Track B under dispositions7 discipline): sd-Δ1 search-vocabulary block
  (eight terms of art) after definition EN+AR · sd-Δ2 leverage map (three tiers:
  information-hiding / CAP-as-constraint / pattern-consequences) after mental-models
  EN+AR. Dispositions7 block CREATED (all seven types registered PRE with anchors;
  R19 hedged pending G-sd4 fetch). Pending fetches remain open gaps: G-sd2 (Paxos),
  G-sd8 (ADR Nygard), G-sd9 (you-build-it), G-sd10 (C4 USENIX).
