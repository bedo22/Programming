# problem-solving — source digestion shell

Status: TRACK A COMPLETE (2026-08-22). Ten rescued Wikipedia seeds under
raw-seeds/problem-solving/ (re-fetched after /tmp loss; provenance in that dir's
README). Doc cites these as its external canon; one-to-one mapping below.

## Fetch ledger (every cited seed URL, verbatim)

Raw seeds live in sources/raw-seeds/problem-solving/*.md (markdown snapshots of the
same pages); file sizes there are the canonical record. All living pages.

| cited URL | status | source-dated |
|---|---|---|
| https://en.wikipedia.org/wiki/How_to_Solve_It | OK — 1945 verified | living page |
| https://en.wikipedia.org/wiki/Alan_Schoenfeld | OK — 1985 *Mathematical Problem Solving* + "Control" verified | living page |
| https://en.wikipedia.org/wiki/Computational_thinking | OK — pillars verified | living page |
| https://en.wikipedia.org/wiki/Einstellung_effect | OK — effect verified | living page |
| https://en.wikipedia.org/wiki/Expertise | OK — **Ericsson deliberate practice + 10,000-hour framing present** | living page |
| https://en.wikipedia.org/wiki/Practice_(learning_method) | OK — companion lane | living page |
| https://en.wikipedia.org/wiki/Rubber_duck_debugging | OK — attributed to *The Pragmatic Programmer* (Hunt & Thomas) | living page |
| https://en.wikipedia.org/wiki/Cognitive_load | OK — theory canon | living page |
| https://en.wikipedia.org/wiki/Stepwise_refinement | OK — Wirth lineage | living page |
| https://en.wikipedia.org/wiki/Competitive_programming | OK — context lane | living page |

Also cited by the doc: https://en.wikipedia.org/wiki/Debugging (general canon, no
dedicated seed needed).

(source-dated per currency convention skill v1.7; all living pages.)

## Sources — read

### How to Solve It (Pólya) — tier: primary
- Establishes: 1945 publication; the four phases (understand → plan → execute → look
  back); heuristic dictionary moves.
- Δ Doc delta: none needed — doc's meta-rhythm section is built on it faithfully.
- Maps to: #sec-the-universal-meta-rhythm-polya-s-four-phases, #sec-polya-s-heuristic-dictionary-the-moves, #sec-the-look-back-phase-in-depth-what-everyone-skips.

### Schoenfeld — tier: primary
- Establishes VERBATIM: 1985 *Mathematical Problem Solving*; the "Control" decisions
  band (what to do at each minute of work) as the metacognition extension.
- Δ Doc delta:
  - **ps-Δ1** the metacognition section can name the 1985 volume and the Control-band
    terminology as sourced anchors rather than paraphrase-only.
- Maps to: #sec-schoenfeld-s-extension-metacognition-the-missing-fifth-element.

### Expertise / Practice seeds — tier: primary (cross-doc payoff)
- Establishes: **Ericsson's deliberate-practice research and the 10,000-hour popular
  framing** — present in both seeds.
- Δ Doc delta:
  - **ps-Δ2** fluency-vs-storage section gains the Ericsson grounding line.
  - CROSS-DOC: this ALSO closes G2 in digests/how-developers-think-frontend.md
    ("Ericsson literature not yet located") — record the pointer there at Track B.
- Maps to: #sec-fluency-vs-storage-strength-in-problem-solving.

### Computational thinking — tier: primary
- Establishes: the four pillars naming (decomposition, pattern recognition,
  abstraction, algorithms).
- Δ Doc delta: none — lens section already faithful.
- Maps to: #sec-the-lens-computational-thinking-s-four-pillars.

### Rubber duck debugging — tier: supporting
- Establishes: origin attribution to *The Pragmatic Programmer* (1999, Hunt & Thomas).
- Δ Doc delta:
  - **ps-Δ3 candidate** debugging section may lack the attribution — verify at Track B.
- Maps to: #sec-debugging-as-problem-solving-the-same-four-phases-inverted.

### Einstellung / Cognitive load / Stepwise refinement / Competitive programming — tier: supporting
- Establishes: Einstellung effect naming; cognitive-load theory canon; Wirth's stepwise
  refinement; competitive-programming context lane.
- Δ Doc delta: none — failure-modes and refinement sections already aligned.
- Maps to: #sec-the-most-common-failure-modes, #sec-underlying-theory-the-cognitive-science-behind-why-the-method-works, #sec-stepwise-refinement-top-down-decomposition-for-programming, #sec-ecosystem-tooling-catalog-with-decision-metrics.

## Coverage matrix

| doc section | covered by | note |
|---|---|---|
| #sec-how-to-use-this-doc | n/a navigation | exempt |
| #sec-search-vocabulary-what-problem-solving-calls-things | ps-Δ3 terms-of-art block | planned Track B · eternal |
| #sec-definition-what-problem-solving-is-and-what-it-is-not | polya + CT seeds | eternal |
| #sec-history-from-mathematics-to-programming-1945present | polya 1945 · schoenfeld 1985 · wirth | dated-once history · eternal |
| #sec-evolution-constraint-inversions-across-the-same-idea | synthesis across seeds | pattern-level · eternal |
| #sec-intersection-with-neighbors-where-it-borders-other-practices | n/a shelf-internal | exempt |
| #sec-underlying-theory-the-cognitive-science-behind-why-the-method-works | cognitive-load seed · expertise seed | eternal theory |
| #sec-mental-models-how-expert-problem-solvers-actually-reason | schoenfeld Control · expertise | authored framework over canon · eternal |
| #sec-leverage-map-where-problem-solving-practice-mass-concentrates | planned ps-Δ4 tiers over seeds | Track B |
| #sec-the-universal-meta-rhythm-polya-s-four-phases | polya seed | eternal |
| #sec-the-lens-computational-thinking-s-four-pillars | CT seed | eternal |
| #sec-polya-s-heuristic-dictionary-the-moves | polya seed | eternal |
| #sec-schoenfeld-s-extension-metacognition-the-missing-fifth-element | schoenfeld seed | ps-Δ1 here · eternal |
| #sec-stepwise-refinement-top-down-decomposition-for-programming | stepwise seed | eternal |
| #sec-algorithm-design-paradigms-the-technique-catalog | doc-native catalog (canon techniques) | eternal |
| #sec-the-role-of-examples-concrete-before-abstract | polya + worked-example structure | eternal |
| #sec-debugging-as-problem-solving-the-same-four-phases-inverted | rubber-duck seed | ps-Δ3c verify attribution · eternal |
| #sec-the-look-back-phase-in-depth-what-everyone-skips | polya seed | eternal |
| #sec-fluency-vs-storage-strength-in-problem-solving | expertise · practice seeds | ps-Δ2 here (+ closes hdt G2 cross-doc) |
| #sec-the-right-questions-a-catalog | doc-native catalog | R18 function · eternal |
| #sec-principles-the-shared-constants | doc-native principles | eternal |
| #sec-worked-example-your-hackerrank-word-frequency-counter-traced-through-polya | illustrative (labeled) | eternal |
| #sec-a-second-worked-example-two-sum-traced-through-polya | illustrative (labeled); competitive-programming context | eternal |
| #sec-the-most-common-failure-modes | einstellung seed | R15 support · eternal |
| #sec-ecosystem-tooling-catalog-with-decision-metrics | competitive-programming seed · volatile tools hedged | volatile→hedged |
| #sec-the-future-where-problem-solving-methodology-is-heading | signals — hedged | volatile→hedged |
| #sec-summary-the-complete-mental-checklist | derives from confirmed sections | inherits classes |

## Gaps

| id | claim/area | hunts | status |
|---|---|---|---|
| G-ps1 | leverage-map provenance | tiers derived from seeds + own catalogs | accepted authored framework |
| G-ps2 | Wing 2006 CT paper exact cite | canon known, paper unlocated this pass | fetch next touch |

## Content authored from this digestion

- Track B plan (v113): ps-Δ1 Schoenfeld sourcing line · ps-Δ2 Ericsson grounding +
  cross-doc G2 closure note in hdt digest · ps-Δ3 search-vocabulary block ·
  ps-Δ4 leverage map. Dispositions7 to be CREATED at Track B commit.
