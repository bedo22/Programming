# Resources

High-trust sources that ground the teaching. **Never trust parametric knowledge** — every claim in a lesson traces back to an entry here. See `RESOURCES-FORMAT.md` for the entry shape.

## Language & history (anchors Episode 1)

### MDN Web Docs — JavaScript
- **Type:** Docs
- **URL:** https://developer.mozilla.org/en-US/docs/Web/JavaScript
- **Trust:** High — Mozilla-maintained, the canonical web-platform reference.
- **Grounds:** Episode 1 (what JS is), and every language-level claim across the journey.
- **Notes:** Free, reachable. Verified definition: *"a lightweight interpreted (or just-in-time compiled) programming language with first-class functions… prototype-based, garbage-collected, dynamic language, supporting multiple paradigms."* Explicitly warns: "Do not confuse JavaScript with the Java programming language."

### Wikipedia — JavaScript
- **Type:** Reference article (secondary, well-sourced)
- **URL:** https://en.wikipedia.org/wiki/JavaScript
- **Trust:** Medium-High — its history section cites primary sources (the 1995 press release, Eich interviews, Rauschmayer).
- **Grounds:** Episode 1 timeline (creation 1995, Netscape/Sun deal, ECMAScript standardization 1997, ES5/ES2015).
- **Notes:** Free, reachable. Use for dates and the citation trail, not as the final word.

### "JavaScript: The First 20 Years" — Wirfs-Brock & Eich, HOPL IV (2020)
- **Type:** Paper (peer-reviewed academic history)
- **URL:** https://dl.acm.org/doi/10.1145/3386327 (DOI 10.1145/3386327)
- **Trust:** Highest — authored by the language's creator (Brendan Eich) and its lead spec editor (Allen Wirfs-Brock).
- **Grounds:** Episode 1 and the deeper history of language design decisions.
- **Notes:** ACM paywalled (returned HTTP 403 when fetched). Cite by name + DOI; treat as the definitive primary source even when the full text isn't accessible.

### "Netscape and Sun announce JavaScript" — joint press release (4 December 1995)
- **Type:** Primary source (press release)
- **URL:** Archived copy referenced by Wikipedia (en.wikipedia.org/wiki/JavaScript, ref 1).
- **Trust:** High — the actual naming announcement.
- **Grounds:** Episode 1 — the LiveScript → JavaScript rename and the Sun/Netscape marketing deal.
- **Notes:** The "Java is to the enterprise as JavaScript is to the browser" framing originates here.

### ECMA-262 — ECMAScript Language Specification
- **Type:** Spec
- **URL:** https://tc39.es/ecma262/ (and https://ecma-intl.org/publications-and-standards/standards/ecma-262/)
- **Trust:** Highest — the standard JS is defined by.
- **Grounds:** Episode 1 (standardization), the TC39 stage process, every language feature across the journey.
- **Notes:** Free, authoritative. TC39 process docs at https://tc39.es.

### Speaking JavaScript — Axel Rauschmayer
- **Type:** Book (free online)
- **URL:** https://speakingjs.com/ (Chapter 4, "How JavaScript Was Created")
- **Trust:** High — Dr. Rauschmayer is a recognized JS expert; the chapter is an accessible primary-ish history.
- **Grounds:** Episode 1 narrative.
- **Notes:** **Reachability to verify** — fetch failed from this environment (site unreachable); confirm the link resolves from the learner's machine before recommending as the lesson's primary read.

## Problem-Solving (cross-cutting — anchors the problem-solving reference)

### Pólya, G. — How to Solve It (1945)
- **Type:** Book (foundational)
- **URL:** https://en.wikipedia.org/wiki/How_to_Solve_It
- **Trust:** Highest — the foundational text of problem-solving methodology. Over 1 million copies, 15+ translations.
- **Grounds:** The four-phase framework (Understand → Plan → Execute → Look back) that underpins the entire problem-solving reference.
- **Notes:** Wikipedia article verified reachable. The book itself is the primary source; Wikipedia is the accessible summary.

### Schoenfeld, A. — Mathematical Problem Solving (1985)
- **Type:** Book (empirical research)
- **URL:** https://en.wikipedia.org/wiki/Alan_Schoenfeld
- **Trust:** High — UC Berkeley education researcher who empirically tested Pólya's strategies and found them weak without metacognition.
- **Grounds:** The metacognition extension (§5 of the reference) — the fifth element that Pólya didn't emphasize enough.
- **Notes:** Wikipedia verified reachable. Key finding: strategies alone are weak; need domain-specific tactics + metacognitive control.

### Wing, J. — "Computational Thinking" (2006)
- **Type:** Essay (Communications of the ACM)
- **URL:** https://en.wikipedia.org/wiki/Computational_thinking
- **Trust:** High — the essay that brought computational thinking to prominence. Papert coined the term (1980); Wing popularized it.
- **Grounds:** The four pillars (decomposition, pattern recognition, abstraction, algorithm design) in §3 of the reference.
- **Notes:** Wikipedia verified reachable. Wing: "thinking computationally is a fundamental skill for everyone, not just computer scientists."

### Hunt, A. & Thomas, D. — The Pragmatic Programmer (1999)
- **Type:** Book
- **URL:** https://en.wikipedia.org/wiki/Rubber_duck_debugging
- **Trust:** High — the origin of rubber duck debugging, a widely adopted technique.
- **Grounds:** The debugging-as-problem-solving section (§9) of the reference.
- **Notes:** Wikipedia verified reachable. Key insight: explaining code step by step forces articulation of assumptions.

### Wirth, N. — "Program Development by Stepwise Refinement" (1971)
- **Type:** Paper (Communications of the ACM)
- **URL:** https://en.wikipedia.org/wiki/Stepwise_refinement
- **Trust:** High — the foundational text on top-down decomposition for programming.
- **Grounds:** The stepwise refinement section (§6) of the reference.
- **Notes:** Wikipedia verified reachable. Wirth is the creator of Pascal.

### Dromey, R.G. — How to Solve It by Computer (1982)
- **Type:** Book
- **Trust:** High — the direct adaptation of Pólya's framework for computer programming.
- **Grounds:** The programming-specific application of Pólya's heuristics.
- **Notes:** Referenced by the Polya Wikipedia article. ISBN 978-0134339955.

### Agans, D. — Debugging: The Nine Indispensable Rules (2002)
- **Type:** Book
- **Trust:** High — the definitive systematic debugging methodology.
- **Grounds:** The debugging-as-problem-solving section (§9) of the reference.
- **Notes:** Referenced by the debugging Wikipedia article. ISBN 0-8144-7168-4.

### Competitive Programming — Wikipedia
- **Type:** Reference article
- **URL:** https://en.wikipedia.org/wiki/Competitive_programming
- **Trust:** Medium-High — well-sourced overview of the problem-solving methodology in competitive programming.
- **Grounds:** The two-step process (construct algorithm → implement) and the technique categories in §7.
- **Notes:** Verified reachable. Problem categories: combinatorics, number theory, graph theory, computational geometry, string analysis, data structures.

### Luchins, A. — "Mechanization in problem solving: The effect of Einstellung" (1942)
- **Type:** Paper (Psychological Monographs)
- **URL:** https://en.wikipedia.org/wiki/Einstellung_effect
- **Trust:** High — foundational experiment in cognitive psychology. The Einstellung effect is a well-established finding.
- **Grounds:** The Einstellung effect in §1e (underlying theory) and §13b (failure modes) — the tendency to apply a familiar method even when better ones exist.
- **Notes:** Wikipedia verified reachable. The water-jar experiment is the classic demonstration.

### Sweller, J. — Cognitive load theory (1988)
- **Type:** Theory (cognitive psychology)
- **URL:** https://en.wikipedia.org/wiki/Cognitive_load
- **Trust:** High — developed in the late 1980s out of a study of problem solving. Well-established in instructional design.
- **Grounds:** The three types of cognitive load (intrinsic, extraneous, germane) in §1e — explains why planning before coding reduces extraneous load.
- **Notes:** Wikipedia verified reachable. Sweller argued instructional design can reduce cognitive load.

### Simon & Chase — "Skill in chess" (1973)
- **Type:** Paper (American Scientist)
- **URL:** https://en.wikipedia.org/wiki/Expertise
- **Trust:** High — foundational expertise research. Herbert Simon (Nobel laureate) and William Chase.
- **Grounds:** Schema theory and chunking in §1e and §1f — experts don't have better raw memory, they have richer schemas that allow chunking.
- **Notes:** Wikipedia verified reachable. The key finding: experts' advantage disappeared with random chess positions — they recognize patterns, not memorize squares.

### Ericsson, A. — Deliberate practice theory
- **Type:** Research program
- **URL:** https://en.wikipedia.org/wiki/Practice_(learning_method)
- **Trust:** High — the leading theory of expertise acquisition. Ericsson's work on deliberate practice is widely cited.
- **Grounds:** The deliberate practice principle in §11 (fluency vs storage strength) and §12b (principles).
- **Notes:** Wikipedia verified reachable. Key components: specific, effortful, with feedback. The 10,000-hour rule is a popularization; the real finding is about the quality of practice, not just the quantity.

## TODO
- Expand per episode as lessons are written. Each lesson adds the sources it cited.
- **Problem-solving reference complete** (`reference/problem-solving.html`, 826 lines, 24 sections). Bridge lessons L12–15 written.
- **CS & SE reference complete** (`reference/cs-and-software-engineering.html`, 550 lines, 20 sections, 18 tables). Lessons L16–17 planned.
- **Observability & Operations reference created** (`reference/observability-and-operations.html`, now 28 sections incl. 7b–7j operational practices). Glossary map updated (Process & Delivery row + Beyond the Curriculum band), cross-links added in System Design/Backend/SDP/Security. **Outside review received** (`Archive/Observability and Operations.txt`) and folded in: error-budget math corrected; on-call design, capacity/load testing, deployment ops, chaos, readiness reviews, cost management, maturity model, shift-left, debt/toil, team metrics added; primary-sources section added; summary checklist extended.
- Verify any URL before first use in a lesson; mark paywalled/inaccessible ones.

## Software Development Process (macro-process — anchors the SDP reference)

### The Agile Manifesto (2001)
- **Type:** Founding document
- **URL:** https://agilemanifesto.org/
- **Trust:** Highest — the foundational statement of Agile philosophy. 17 signatories.
- **Grounds:** §3 (the 4 values + 12 principles).
- **Notes:** Verified reachable. The canonical source.

### Scrum Guide — Schwaber & Sutherland
- **Type:** Reference document (free, maintained)
- **URL:** https://www.scrumguides.org/scrum-guide.html
- **Trust:** Highest — the definitive Scrum definition by its co-creators. Updated periodically (latest: 2020).
- **Grounds:** §4 (3 roles, 5 events, 3 artifacts).
- **Notes:** Verified reachable. The single source of truth for Scrum.

### Software Development Process (Wikipedia)
- **Type:** Encyclopedia article
- **URL:** https://en.wikipedia.org/wiki/Software_development_process
- **Trust:** High — comprehensive overview of the SDLC and methodologies.
- **Grounds:** §1–§2 (SDLC phases, methodology definition), §1b (history).
- **Notes:** Verified reachable.

### Agile Software Development (Wikipedia)
- **Type:** Encyclopedia article
- **URL:** https://en.wikipedia.org/wiki/Agile_software_development
- **Trust:** High — covers the history, values, principles, methods, and common pitfalls (15 listed).
- **Grounds:** §3, §9b (failure modes).
- **Notes:** Verified reachable.

### Scrum (Wikipedia)
- **Type:** Encyclopedia article
- **URL:** https://en.wikipedia.org/wiki/Scrum_(software_development)
- **Trust:** High — covers roles, events, artifacts, history, criticism.
- **Grounds:** §4.
- **Notes:** Verified reachable.

### Kanban (Wikipedia)
- **Type:** Encyclopedia article
- **URL:** https://en.wikipedia.org/wiki/Kanban_(development)
- **Trust:** High — covers the 6 practices, origin (Toyota Production System), evolution.
- **Grounds:** §5, §1e (Lean manufacturing).
- **Notes:** Verified reachable.

### AI Agent (Wikipedia)
- **Type:** Encyclopedia article
- **URL:** https://en.wikipedia.org/wiki/AI_agent
- **Trust:** High — covers the definition, history, architecture, applications, concerns.
- **Grounds:** §9d (Agent Development Lifecycle).
- **Notes:** Verified reachable. The ADLC is emerging (2024–present); this article covers the agent concept that the ADLC builds upon.

### Knuth, D. — The Art of Computer Programming (1968)
- **Type:** Book (foundational, multi-volume)
- **URL:** https://en.wikipedia.org/wiki/Analysis_of_algorithms
- **Trust:** Highest — Knuth coined the term "analysis of algorithms." The definitive work on algorithm efficiency.
- **Grounds:** §5 (Big O, complexity classes), §7 (Knuth's "premature optimization" principle), §1b (history — the birth of solution evaluation).
- **Notes:** Wikipedia article on analysis of algorithms verified reachable. The books themselves are dense; for the learner, the Wikipedia summary + the reference doc are the accessible entry.

### Turing, A. — "On Computable Numbers" (1936)
- **Type:** Paper (foundational)
- **URL:** https://en.wikipedia.org/wiki/Alan_Turing
- **Trust:** Highest — the founding document of computer science. Defined the Turing machine and computability.
- **Grounds:** §1b (history — the science thread begins here), §1e (underlying theory — computability, the halting problem).
- **Notes:** Wikipedia verified reachable. The paper itself is highly technical; the Wikipedia summary is the accessible entry.

### NATO Software Engineering Conference (1968)
- **Type:** Conference proceedings (historical)
- **URL:** https://en.wikipedia.org/wiki/Software_engineering
- **Trust:** High — the event that named software engineering as a discipline, in response to the "software crisis."
- **Grounds:** §1b (history — the engineering thread begins here), §3 (what SE is).
- **Notes:** Wikipedia verified reachable. The proceedings are the primary source; Wikipedia is the accessible summary.

### ISO/IEC 25010 — Software Quality Model (2011)
- **Type:** International standard
- **URL:** https://en.wikipedia.org/wiki/ISO/IEC_25010
- **Trust:** Highest — the formal international standard for software quality evaluation. Superseded ISO 9126 (1991).
- **Grounds:** §4 (the 8 quality attributes/parameters), §1b (history — the formalization of "what makes a solution good").
- **Notes:** Wikipedia (redirects from ISO 25010 to ISO 9126 article) verified reachable.

### SOLID Principles — Robert C. Martin (2000)
- **Type:** Design principles
- **URL:** https://en.wikipedia.org/wiki/SOLID
- **Trust:** High — Robert C. Martin ("Uncle Bob") introduced the principles in 2000; acronym coined by Michael Feathers (~2004).
- **Grounds:** §8 (engineering principles — the five SOLID principles).
- **Notes:** Wikipedia verified reachable. Each principle has its own Wikipedia article for deeper reading.

### Big O Notation
- **Type:** Mathematical notation
- **URL:** https://en.wikipedia.org/wiki/Big_O_notation
- **Trust:** Highest — the standard notation for algorithm complexity classification. Origin: Bachmann (1894), Landau; adopted for CS by Knuth.
- **Grounds:** §5 (the measures — complexity classes, how to analyze an algorithm).
- **Notes:** Wikipedia verified reachable. The article is mathematically dense; the reference doc's §5 is the accessible version.

## Observability & Operations (operational layer — anchors the observability-and-operations reference)

### "Site Reliability Engineering" — Google SRE Book (Beyer, Jones, Petoff & Murphy, 2016)
- **Type:** Book (foundational, free online)
- **URL:** https://sre.google/sre-book/table-of-contents/
- **Trust:** Highest — authored by Google SRE; the primary source for error budgets, on-call, and incident response practice.
- **Grounds:** Ops reference §1c (SRE era), §2 (error-budget policy), §3 (alert design), §4 (incident response), §5 (postmortems).
- **Notes:** Free online (verified reachable). Read first: "Service Level Objectives", "Alerting on SLOs", "Being On-Call", "Postmortem Culture".

### "The Site Reliability Workbook" — Google (Hine et al., 2018)
- **Type:** Book (free online)
- **URL:** https://sre.google/workbook/table-of-contents/
- **Trust:** Highest — the practical companion to the SRE book, with worked SLO and alerting examples.
- **Grounds:** Ops reference §2 (SLI selection, multi-window burn-rate alerting), §8 (the checkout incident).
- **Notes:** Free online (verified reachable). Chapter "Alerting on SLOs" is the primary-read candidate for §3.

### OpenTelemetry — official documentation
- **Type:** Docs / Spec (vendor-neutral standard)
- **URL:** https://opentelemetry.io/docs/
- **Trust:** Highest — the merged OpenTracing/OpenCensus standard (2019), the industry baseline for trace propagation.
- **Grounds:** Ops reference §1b (OpenTelemetry era), §10 (traces tooling); pairs with System Design §6g (trace propagation).
- **Notes:** Free (verified reachable). The W3C trace context spec is the deeper primary source.

### Prometheus — "Alerting" documentation
- **Type:** Docs
- **URL:** https://prometheus.io/docs/alerting/latest/overview/
- **Trust:** High — the reference implementation of dimensional metrics and SLO-style alerting.
- **Grounds:** Ops reference §3 (alert shapes, multi-window burn-rate), §10 (metrics/alerting tooling).
- **Notes:** Free (verified reachable). The Google blog post "Alerting on SLOs" is a strong secondary source — verify reachability before citing.

### PagerDuty — Incident Response Documentation (open-source repo)
- **Type:** Docs (open-source, vendor-maintained)
- **URL:** https://github.com/PagerDuty/incident-response-docs
- **Trust:** Medium-High — the public de-facto reference for severity taxonomy and incident roles (Incident Commander, Scribe, Comms).
- **Grounds:** Ops reference §4 (incident command, lifecycle), §3 (severity).
- **Notes:** Free (verified reachable). Vendor-published; cross-check role definitions against the SRE book before recommending as a primary read.

### The USE Method — Brendan Gregg
- **Type:** Article/technique (primary author)
- **URL:** https://www.brendangregg.com/usemethod.html
- **Trust:** High — Brendan Gregg is the author of the method; the canonical resource-analysis framework.
- **Grounds:** Ops reference §1e (underlying theory), §7c (capacity planning).
- **Notes:** Free (verified reachable from this environment).

### The RED Method — Tom Wilkie
- **Type:** Article/technique (primary author)
- **URL:** https://grafana.com/blog/the-red-method-how-to-instrument-your-services/
- **Trust:** High — Tom Wilkie (Grafana Labs); the service-level metrics counterpart to USE.
- **Grounds:** Ops reference §1e (rate/errors/duration for request services).
- **Notes:** Free (verified reachable; note the URL redirects from the 2018 blog path).

### Charity Majors — "Observability is a Many-Splendored Thing"
- **Type:** Article (practitioner primary source)
- **URL:** https://charity.wtf/p/observability-is-a-many-splendored-thing
- **Trust:** High — a founding voice of the observability movement (Honeycomb); the observability-vs-monitoring framing.
- **Grounds:** Ops reference §1 (definition), §1f (mental models).
- **Notes:** Free (verified reachable from this environment).

### John Allspaw — "Blameless PostMortems and a Just Culture"
- **Type:** Article (practitioner primary source)
- **URL:** https://codeascraft.com/2012/05/22/blameless-postmortems/
- **Trust:** High — Etsy's VP of Ops; the origin of blameless culture in engineering.
- **Grounds:** Ops reference §5 (postmortems).
- **Notes:** Etsy redirects automated fetches (HTTP 403 from this environment) — verify the link resolves in a browser before recommending.

### John Allspaw — "The Infinite Hows"
- **Type:** Article
- **URL:** https://www.oreilly.com/radar/the-infinite-hows/
- **Trust:** High — Allspaw; why the first question of a postmortem should not be "what happened".
- **Grounds:** Ops reference §5 (postmortem craft).
- **Notes:** O'Reilly returned 403 to automated fetches — verify in a browser before recommending.
