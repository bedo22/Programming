# how-developers-think-frontend — source digestion

Fetched: 2026-08-21 · Status: 8 fetched OK / 1 dead-substituted / 2 book-sites skipped (covered by wikis)
Gate: digest-coverage.py PASS required before value authoring.

## Fetch ledger (every cited seed URL)

| cited URL | status |
|---|---|
| https://www.sei.cmu.edu/publications/1986-spiral-model/ | DEAD as cited → SEI project page fetched instead (sei-spiral.html, 102KB) |
| https://ieeexplore.ieee.org/document/1188961 | DEAD (0 bytes, paywall) → substituted by Wikipedia IID article which summarizes Larman & Basili 2003 |
| https://www.amazon.com/Extreme-Programming-Explained-Embrace-Change/dp/0321278658 | retail page skipped — covered by Wikipedia Extreme Programming |
| https://agilemanifesto.org/ | OK (manifesto text verified verbatim) |
| https://theleanstartup.com/ | landing page, low content — covered by Wikipedia The Lean Startup |
Supplementary: Wikipedia Spiral model · IID · XP · The Lean Startup · Working memory · Miller 7±2.

## Sources — read

### Spiral model (en.wikipedia.org/wiki/Spiral_model) + SEI page — tier: primary
- Establishes: spiral is explicitly **risk-driven** ("Based on the unique risk patterns
  of a given project…"); Boehm 1986; quadrants determine cycle depth.
- Mechanisms worth teaching: depth-of-cycle set by risks-to-resolve.
- Δ Doc delta:
  - **hdt-Δ1** the doc's rounds are *friction-driven* (feel-the-friction); Boehm's
    ancestor is *risk-driven*. Candidate: Round-0 checklist could rank items by risk
    (likelihood × impact × invisibility) so the deepest round targets the biggest risk.
- Maps to: #sec-history-of-this-loop-from-nasa-to-react, #sec-round-0-the-three-
  clarifying-questions-the-hardest-part, #sec-underlying-theory-why-the-loop-works-the-cognitive-science.
- Tensions: none — doc already calls spiral "the named ancestor".

### Iterative & Incremental Development (en.wikipedia.org/wiki/Iterative_and_incremental_development) — tier: primary
- Establishes: Larman & Basili 2003 traced IID to the 1950s; earliest example NASA's
  1960s Project Mercury; Mercury engineers later formed IBM division that built the
  space shuttle's software — "another early and striking example of a major IID success".
- Examples/war stories in source: Mercury + shuttle onboard software.
- Δ Doc delta:
  - **hdt-Δ2** the shuttle-software sequel to the Mercury story — doc's history says
    only "Project Mercury"; the shuttle detail makes the lineage concrete and memorable.
- Maps to: #sec-history-of-this-loop-from-nasa-to-react, #sec-underlying-theory-why-the-loop-works-the-cognitive-science.

### Miller 7±2 (en.wikipedia.org/wiki/The_Magical_Number_Seven,_Plus_or_Minus_Two) — tier: primary
- Establishes: memory span is limited in **chunks, not bits**; a chunk is "the largest
  meaningful unit the person recognizes" — chunk size depends on the knower's knowledge.
- Δ Doc delta:
  - **hdt-Δ3** chunk-knowledge dependence explains WHY senior devs hold more per pass:
    their chunks are bigger, so the same three threads fit more easily. Deepens the
    working-memory paragraph from citation to mechanism.
- Maps to: #sec-underlying-theory-why-the-loop-works-the-cognitive-science,
  #sec-the-honest-truth-about-how-senior-devs-work.
- Tensions: doc cites "Cowan 2001: ~4"; Working-memory article confirms Cowan's estimate
  and adds Baddeley's 2000 episodic buffer (hdt-Δ5, minor — declined for scope).

### Agile Manifesto (agilemanifesto.org/) — tier: primary (short primary text, verified verbatim)
- Establishes: the four value pairs, incl. "Individuals and interactions over processes
  and tools", "Responding to change over following a plan".
- Δ Doc delta:
  - **hdt-Δ4** the manifesto's first value pair IS the rhythm argument at org scale —
    quotable grounding for "why a rhythm, not an algorithm".
- Maps to: #sec-why-is-it-a-rhythm-not-a-structured-algorithm.

### Extreme Programming (en.wikipedia.org/wiki/Extreme_programming) — tier: supporting
- Establishes: Beck refined XP on the Chrysler C3 payroll project, became lead March
  1996, published XP Explained 1999.
- Δ Doc delta:
  - **hdt-Δ5** XP's concrete origin (C3 payroll, 1996) — history row currently dates
    XP Explained without the project story; small but humanizing.
- Maps to: #sec-history-of-this-loop-from-nasa-to-react.

### The Lean Startup (en.wikipedia.org/wiki/The_Lean_Startup) — tier: supporting
- Establishes: build-measure-learn loop; MVP concept attribution to Ries.
- Δ Doc delta: none beyond what doc already uses (vocabulary map + terminology rows).
- Maps to: #sec-the-vocabulary-map-sketch-wireframe-mockup-prototype-spike-mvp,
  #sec-what-is-this-process-called-entity-types-and-terminology.

## Coverage matrix

| doc section | covered by source | note |
|---|---|---|
| #sec-how-to-use-this-doc | n/a navigation | exempt |
| #sec-definition-what-the-dev-loop-is-and-what-it-is-not | Spiral+IID+XP | micro-process framing doc-native |
| #sec-evolution-constraint-inversions-across-the-same-idea | Spiral; IID; XP | |
| #sec-intersection-with-neighbors-where-it-borders-other-practices | n/a shelf-internal | exempt |
| #sec-underlying-theory-why-the-loop-works-the-cognitive-science | Miller; Working-memory | Δ3 here |
| #sec-the-three-thread-mental-model-not-a-sequence-a-loop | gap → G1 | doc-native synthesis |
| #sec-round-0-the-three-clarifying-questions-the-hardest-part | gap → G1; Δ1 enriches | |
| #sec-round-1-skeleton-pass-the-thinnest-end-to-end-slice | gap → G1 | practice synthesis |
| #sec-round-2-deepening-pass-make-it-real | gap → G1 | |
| #sec-round-3-edge-cases-and-polish-the-difference-between-works-and-ships | gap → G1 | |
| #sec-frontend-state-decisions-the-taxonomy | n/a owner: ui-ux state matrix | cross-doc |
| #sec-mental-models-how-developers-actually-reason-across-rounds | gap → G1 | |
| #sec-leverage-map-where-the-loop-practice-mass-concentrates | hdt-Δ6 tiers over this shell's digested sources (Miller/Cowan, SEI, Manifesto, XP/IID/LeanStartup) | added v99; tier-one rows cite G1 accepted-framework basis |
| #sec-where-data-structures-algorithms-actually-show-up-in-frontend | gap → G1 | |
| #sec-the-honest-truth-about-how-senior-devs-work | gap → G1; Δ3 supports | |
| #sec-your-takeaway-the-deliberate-practice-loop | CLOSED v115: Ericsson located via problem-solving seeds (expertise/practice, raw-seeds/problem-solving/) + ps doc already teaches deliberate practice 9x | Δ-ps-cross |
| #sec-what-is-this-process-called-entity-types-and-terminology | Lean Startup | |
| #sec-why-is-it-a-rhythm-not-a-structured-algorithm | Agile Manifesto | Δ4 |
| #sec-history-of-this-loop-from-nasa-to-react | Spiral; IID; XP | Δ2, Δ5 |
| #sec-the-vocabulary-map-sketch-wireframe-mockup-prototype-spike-mvp | Lean Startup | |
| #sec-principles-the-shared-constants | doc-native synthesis | G1 class |
| #sec-sketching-the-data-shape-what-it-actually-means-with-a-full-worked-example | illustrative (labeled) | |
| #sec-the-most-common-failure-modes | practitioner synthesis; Pólya pointer lives in problem-solving doc (owner) | |
| #sec-ecosystem-tooling-catalog-with-decision-metrics | volatile facts — hedged | |
| #sec-the-future-where-the-dev-loop-is-heading | volatile signals — hedged; owners react-2024/nextjs | |
| #sec-summary-the-complete-mental-checklist | derives from confirmed sections | |

## Gaps

| id | claim/area | where | hunts | status |
|---|---|---|---|---|
| G1 | Three-thread model + rounds taxonomy provenance | core sections | doc presents as own synthesized framework (consistent w/ "it doesn't have one canonical name" row) | accepted as authored framework — no † needed (no factual assertion) |
| G2 | "build it 50 times"/deliberate-practice efficacy claim | takeaway loop | **CLOSED 2026-08-22 (v115)**: Ericsson literature located — reference/sources/raw-seeds/problem-solving/{expertise,practice}.md contain deliberate-practice canon; sibling problem-solving doc grounds it in its fluency section. Cross-doc owner-pointer: problem-solving owns the practice-science depth. | closed |

## Content authored from this digestion

- pass v80 (Track B): Δ3 → theory working-memory paragraph (chunk-not-item mechanism
  of senior fluency) · Δ2 → history cell (Mercury→IBM→shuttle IID lineage) ·
  Δ4 → rhythm section (Agile Manifesto value-pairs as org-scale argument) ·
  Δ5 → history closer (XP from Chrysler C3, 1996) · Δ1 → Round-0 close
  (rank checklist by risk; spiral was risk-driven). All mirrored to AR twin.
- Declined: hdt-Δ5b (Baddeley episodic buffer — scope creep for this doc's claim);
  G2 left open pending Ericsson hunt (prescriptive "50 times" is low-risk).
- pass v99 (Phase-1 backfill): hdt-Δ6 leverage map (three master-first tiers) → new
  section after mental-models, EN+AR. Tiers drawn only from THIS shell's digested
  sources — Miller/Working-memory pages, SEI spiral, Manifesto verbatim,
  XP/IID/Lean Startup records; tier-one rows cite G1 accepted-framework basis.
  Dispositions7 R14 flipped THIN→PRE.
