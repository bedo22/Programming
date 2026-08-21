# software-testing-and-debugging — source digestion

Fetched: 2026-08-21 · Status: 7 fetched OK / 0 dead (property-based wiki failed → substituted by sw-testing article; property-based content rests on fast-check/Hypothesis docs pending)
Gate: digest-coverage.py PASS.

## Fetch ledger (every cited seed URL)

| cited URL | status |
|---|---|
| https://standards.ieee.org/standard/1012-2016.html | OK (119KB) — V&V framing confirmed |
| https://junit.org/junit5/ | OK (22KB) |
| https://martinfowler.com/bliki/TestPyramid.html | OK (20KB) — **etymology: Mike Cohn, Succeeding with Agile, 2009** |
| https://martinfowler.com/articles/practical-test-pyramid.html | OK (114KB) — Vocke; E2E maintenance-cost argument; "what is a unit" nuance |
| https://en.wikipedia.org/wiki/Test-driven_development | OK (42KB) — Beck red-green-refactor |
| https://en.wikipedia.org/wiki/Property-based_testing | FAILED (curl) → substituted by Software-testing article + pending fast-check docs |
| https://sre.google/sre-book/service-level-objectives/ | OK (45KB) — error budget = "an SLO for meeting other SLOs"; nines terminology |

Supplementary: Wikipedia Software testing (67KB).

## Sources — read

### Practical Test Pyramid, Vocke (martinfowler.com/articles/practical-test-pyramid.html) — tier: primary
- Establishes: pyramid as shape-heuristic; E2E tests have the highest maintenance
  cost ("aim to reduce… to a bare minimum"); "what is a unit?" has no canonical answer;
  test doubles at boundaries; don't connect to live third parties.
- Δ Doc delta:
  - **std-Δ2** the definitional nuance — three people, four answers for "unit" —
    grounds the doc's levels table in honest terminology uncertainty.
- Maps to: #sec-testing-levels-from-one-unit-to-the-whole-system,
  #sec-test-strategy-what-to-automate-and-what-not-to.
- Tensions: none with doc; doc's pyramid-as-heuristic stance matches.

### Test Pyramid bliki, Fowler (martinfowler.com/bliki/TestPyramid.html) — tier: primary
- Establishes: **etymology — Mike Cohn described it in Succeeding with Agile (2009)**;
  cost/speed arrows idea; definitional drift caveat.
- Δ Doc delta:
  - **std-Δ1** Cohn attribution missing from doc's pyramid mentions.
- Maps to: #sec-mental-models-how-senior-engineers-think-about-tests (pyramid bullet),
  #sec-test-strategy-what-to-automate-and-what-not-to.

### Google SRE Book, SLO chapter (sre.google/sre-book/service-level-objectives/) — tier: primary
- Establishes: error budget defined as "an SLO for meeting other SLOs", tracked daily/
  weekly; "nines" terminology; 99.95% GCE target example; motives against over-conservatism.
- Δ Doc delta:
  - **std-Δ3** T1 source now exists for the doc's 99.9%→43min arithmetic (upgrades it
    from T2-derived to sourced-backed); "nines" vocabulary worth adding.
- Maps to: #sec-production-verification-testing-does-not-stop-at-deployment.

### IEEE 1012 / JUnit5 / TDD wiki / Software-testing wiki — tier: supporting
- Establishes: V&V definitions (verification vs validation) ✓ already used;
  JUnit lineage ✓ used; TDD origin ✓ used; property-based testing pointer pending.
- Δ Doc delta: std-Δ4 property-based section could cite fast-check/Hypothesis docs
  directly (currently only tooling table names them). Minor.

## Coverage matrix

| doc section | covered by source | note |
|---|---|---|
| #sec-how-to-use-this-doc | n/a navigation | exempt |
| #sec-definition-what-testing-is-and-what-it-is-not | IEEE 1012 ✓ | |
| #sec-history-from-debugging-to-continuous-and-ai-era-testing | JUnit/TDD wikis; sw-testing | |
| #sec-evolution-the-constraint-inversions | synthesis of fetched histories | pattern-level |
| #sec-intersection-with-neighbors-evidence-at-every-boundary | n/a shelf-internal | exempt |
| #sec-underlying-theory-oracles-isolation-determinism-and-risk | sw-testing article (oracle concept) | |
| #sec-mental-models-how-senior-engineers-think-about-tests | Fowler bliki | std-Δ1 here |
| #sec-testing-levels-from-one-unit-to-the-whole-system | Vocke | std-Δ2 here |
| #sec-testing-techniques-how-to-choose-inputs-that-matter | sw-testing; property-based → G1 | |
| #sec-test-doubles-mocks-stubs-fakes-and-spies | Vocke (test doubles) | Meszaros origin → G2 |
| #sec-test-driven-development-tests-as-design-pressure | TDD wiki | |
| #sec-test-strategy-what-to-automate-and-what-not-to | Vocke | |
| #sec-non-functional-testing-proving-the-qualities-that-users-feel | gap → G3 | OWASP/audit sources pending |
| #sec-testing-metrics-how-to-know-whether-the-evidence-is-useful | gap → G4 | DORA metrics source pending |
| #sec-production-verification-testing-does-not-stop-at-deployment | SRE book | std-Δ3 here |
| #sec-debugging-the-evidence-when-a-test-fails | owner-pointer to problem-solving | cross-doc |
| #sec-ai-era-testing-generated-code-and-nondeterministic-systems | gap → G5 | emerging area, hedged |
| #sec-worked-example-a-feature-tested-from-unit-to-production | illustrative (labeled) | |
| #sec-tooling-ecosystem-how-the-concepts-land-in-practice | tool pages volatile — hedged | |
| #sec-the-most-common-failure-modes | traces to confirmed sections | |
| #sec-the-complete-mental-checklist | derives from confirmed sections | |

## Gaps

| id | claim/area | where | hunts | status |
|---|---|---|---|---|
| G1 | property-based testing theory | techniques | en-wiki curl failed; fast-check docs pending | fetch next pass |
| G2 | "test double" term origin (Meszaros 2007) | doubles section | xunitpatterns.com pending | fetch next pass |
| G3 | non-functional testing canon (OWASP ASVS etc.) | non-functional | pending | fetch next pass |
| G4 | DORA four-keys metrics provenance | metrics | pending (dora.dev) | fetch next pass |
| G5 | AI-era eval practice sources | ai-era section | emerging, few primaries | hedged language already |

## Content authored from this digestion

- pass v81 (Track B): std-Δ1 → pyramid bullet (Cohn 2009 attribution, EN+AR) ·
  std-Δ2 → practical-rule paragraph (unit definitional nuance) · std-Δ3 → SLO bullet
  (SRE book definition + "nines"; upgrades the 43-min figure's grounding).
- Declined: std-Δ4 (property-based citations — deferred to G1 fetch); E2E-cost delta
  (already carried by strategy section).
