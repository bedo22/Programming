# 0014 — Six paradigms, debugging as inverted problem-solving, and pattern filing

**Date:** 2026-08-04
**Lesson:** `lessons/0014-problem-solving-paradigms-and-debugging.html`
**Reference:** `reference/problem-solving.html` §7, §9–§10

## Context
Lesson 13 gave the lens, moves, and monitor. This lesson gives the tools (six algorithm paradigms) and the application (debugging + the look-back phase).

## Key insight
There is no single optimal algorithm for all problems — there are six paradigms, each fitting a different class:
- **Brute force** (always start here, optimize later)
- **Greedy** (local optimum = global optimum)
- **Divide & conquer** (independent sub-problems)
- **Dynamic programming** (overlapping sub-problems — the critical D&C vs DP distinction)
- **Backtracking** (explore all possibilities, prune early)
- **Hash table** (fast lookup, counting, deduplication — the learner's word-frequency counter)

Debugging is the same four phases inverted: you start from the symptom and work backwards. Rubber duck debugging = Phase 1 applied to your own code. Hypothesis-driven debugging = the scientific method. Binary search debugging = D&C applied to bugs.

**The deepest insight:** pattern recognition isn't built by reading about patterns — it's built by **filing** them after solving. Each filed pattern is an entry in your mental lookup table. After 50 problems, you recognize categories from the problem statement. After 200, from the first sentence.

## Why this matters for future sessions
This is the final problem-solving lesson. The paradigm categories will be referenced whenever the learner works on HackerRank challenges. The pattern-filing habit is the bridge between problem-solving (L12–14) and the rhythm deepened (L15) — both build storage strength through effortful retrieval.
