# design-thinking — source digestion shell

Status: TRACK A COMPLETE (2026-08-22), nine unique cited URLs reconciled per v1.7
currency conventions. Unusual ledger shape for this shelf: no wikis, no platform
docs, no XML-namespace artifacts — the doc's entire citation surface is books,
one JSTOR paper, one press piece, two institution pages, and one practitioner
essay, all concentrated in the closing `.cite` block.

## Cited-URL reconciliation (coverage gate requirement)

| cited URL | status | source-dated |
|---|---|---|
| https://www.amazon.com/Sciences-Artificial-Herbert-Alexander-Simon/dp/0262691916 | primary canon — Simon, *The Sciences of the Artificial* (bounded rationality, satisficing) | dated(1969) |
| https://www.jstor.org/stable/40222683 | eternal paper — Rittel & Webber, "Dilemmas in a General Theory of Planning" (wicked problems coined) | dated(1973) |
| https://www.amazon.com/Change-Design-Thinking-Transforms-Organizations/dp/0061766089 | practitioner canon — Brown, *Change by Design* (the mainstreaming book) | dated(2009) |
| https://www.amazon.com/Lean-UX-Applying-Principles-Innovate/dp/1491953602 | practitioner canon — Gothelf & Seiden, *Lean UX* (hypothesis-driven in-house design) | dated(2013) |
| https://www.amazon.com/Sprint-Solve-Problems-Test-Ideas/dp/150112174X | practitioner canon — Knapp et al., *Sprint* (GV 5-day Design Sprint) | dated(2016) |
| https://www.nytimes.com/2017/07/26/technology/design-thinking.html | press coverage of Jen's "Design Thinking is Bullshit" critique — secondary source, not the primary talk | dated(2017-07-26) |
| https://jnd.org/rethinking-design-thinking/ | practitioner canon — Norman's critique essay on his living blog | dated(2019), page living |
| https://dschool.stanford.edu/resources/design-thinking-bootleg | institution canon — Stanford d.school Bootcamp Bootleg (method source: POV madlib, empathy map, Crazy 8s) | continuously updated |
| https://www.designcouncil.org.uk/our-work/skills/what-is-the-double-diamond | origin-body canon — Design Council UK's own Double Diamond page | framework dated(2005), page continuously updated |

Ledger notes: the four Amazon links are retailer pointers to dated print editions,
treated as canon-by-edition, not as living commerce pages. No wiki rows and no
markup-artifact rows were warranted this pass.

## Coverage matrix

| doc section | covered by | note |
|---|---|---|
| #sec-how-to-use-this-doc | n/a navigation | exempt |
| #sec-definition-what-design-thinking-is-and-what-it-is-not | doc-native teaching + cited canon (see ledger); three-lens Venn attributed IDEO ~1998 without direct link | eternal |
| #sec-history-five-phases-of-the-idea | doc-native timeline anchored to Simon / Rittel & Webber / Brown / Knapp canon rows | settled history · dated-once · eternal |
| #sec-evolution-from-industrial-design-to-software-and-policy | doc-native domain-shift table; policy/AI-era rows hedged as current signals | settled shifts eternal · recent rows volatile→hedged |
| #sec-migration-paths-adopting-design-thinking-in-existing-orgs | doc-native decision tables (from→to paths, triggers, risks, success signals) | R18 function · authored framework · eternal patterns |
| #sec-intersection-with-neighbors-where-it-borders-other-practices | n/a shelf-internal boundaries | exempt |
| #sec-underlying-theory-the-ideas-it-borrows-from | doc-native synthesis of Simon / Rittel & Webber / Cross / Argyris & Schön; JSTOR + Simon ledger rows carry the load | eternal |
| #sec-mental-models-how-designers-actually-reason | doc-native frames compressing the cited theory into decision contexts | authored framework · eternal |
| #sec-the-rhythm-not-the-algorithm | doc-native argument; sprint-as-timebox callout traces to Knapp ledger row | eternal |
| #sec-methodologies-the-named-frameworks | five named frameworks; origins trace to d.school / Design Council / book canon rows | named-framework facts dated-once · structure eternal |
| #sec-principles-the-shared-constants | doc-native distillation across methodologies | authored framework · eternal |
| #sec-synthesis-from-raw-field-data-to-an-insight-statement | doc-native mechanics; POV-madlib shape traces to d.school bootleg row | eternal method |
| #sec-ideation-and-prototype-catalogs-the-mechanics-behind-40-sketches | doc-native catalog; Crazy 8s/HMW mechanics trace to bootleg + Sprint canon rows | eternal techniques |
| #sec-desirability-testing-and-the-handoff-proving-value-then-transferring-it | doc-native; Mom Test rule invoked by name without a ledger row (see gaps) | eternal principles · attribution volatile→hedged |
| #sec-managing-the-room-and-the-organization | doc-native social dynamics; extractive-research framing hedged as live discourse | eternal practice · volatile→hedged |
| #sec-worked-example-reduce-missed-medication-doses | illustrative composite labeled a classic problem; numbers are teaching values, not study data | eternal teaching example |
| #sec-the-most-common-failure-modes | failure table + 2018+ academic critique traced to Jen / Norman / Nussbaum ledger rows | R15 support · critiques dated(2017–2019) · dynamics eternal |
| #sec-ecosystem-tooling-catalog-with-decision-metrics | volatile vendor landscape — hedged to categories + decision metrics | R18 function · volatile→hedged |
| #sec-the-future-where-design-thinking-is-going | signals (AI synthesis, EU AI Act, co-design) — hedged | volatile→hedged |
| #sec-summary-the-mental-checklist | derives from confirmed sections above | inherits classes |

## Gaps

| id | claim/area | hunts | status |
|---|---|---|---|
| G-mom1 | "The Mom Test rule" taught by name in desirability testing but has no ledger row | primary Mom Test source never cited; rule itself stated doc-natively | convention-tier hedge |
| G-jen1 | Natasha Jen critique reachable only via NYT press coverage, not the primary talk recording | fetch primary talk video next touch | fetch next touch |
| G-gui1 | Guilford (1967) invoked in ideation section for divergent-thinking basis with no ledger row | psychology-primary cite if the claim ever hardens beyond teaching context | convention-tier hedge |

## Content authored from this digestion

- Track B row: justified N/A this pass — rich authored doc delegating facts to
  cited canon (books, paper, institutions); recorded per SHELF-DONE rule
  (additions OR justified N/A). HTML docs untouched.
