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
- **Problem-solving lessons TBD** — the reference (`reference/problem-solving.html`) is complete; lessons will be built based on its size and the learner's decision on whether it needs a full episode or a bridge lesson.
- Verify any URL before first use in a lesson; mark paywalled/inaccessible ones.
