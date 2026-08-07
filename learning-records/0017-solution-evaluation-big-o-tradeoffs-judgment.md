# 0017 — Solution evaluation: Big O, quality attributes, trade-offs, and judgment

**Date:** 2026-08-04
**Lesson:** `lessons/0017-solution-evaluation.html`
**Reference:** `reference/cs-and-software-engineering.html` §4–§7, §9

## Context
This is the practical lesson that teaches the evaluation skill the learner asked about — "it's not enough to solve with brute force, you look at time complexity, the abstraction, and other concerns." The reference provides the full framework; this lesson distills it into the four layers (parameters, measures, trade-offs, judgment), Big O complexity classes, the standard trade-offs, Knuth's premature optimization principle, and a worked example (firstNonRepeat brute force → hash map upgrade).

## Key insight
The same two solutions (brute force O(n²) and hash map O(n)) get different answers depending on context. HackerRank with large n: the O(n) upgrade is mandatory. Production with small n: the brute force is simpler, uses less memory, and is instantly fast. Interview: start with brute force, then evaluate — "this is O(n²), for large n I'd use a hash map for O(n)." The evaluation skill IS the interview signal. Knuth's principle: don't optimize before you know it matters — measure first, optimize only the critical path.

## Why this matters for future sessions
This is the last Bridge lesson (L12–17 complete). The Bridge movement is now 6 lessons: problem-solving (L12–14), rhythm deepened (L15), CS & SE discipline (L16), solution evaluation (L17). The evaluation skill connects to every existing reference: Problem-Solving Phase 4, System Design trade-offs (CAP), API Design trade-offs (REST vs GraphQL), and The Rhythm's "simplest thing first" (KISS + YAGNI). Next: the Human/product movement (L18–19), then Economic reality (L20).
