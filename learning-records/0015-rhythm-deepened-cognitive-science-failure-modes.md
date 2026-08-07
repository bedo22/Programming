# 0015 — The rhythm deepened: cognitive science, failure modes, and enduring principles

**Date:** 2026-08-04
**Lesson:** `lessons/0015-the-rhythm-deepened.html`
**Reference:** `reference/how-developers-think-frontend.html` §1e, §12b, §13b, §13d

## Context
Lesson 7 taught the core rhythm (Model→View→Flow, rounds, data-shape sketch). The rhythm reference was expanded with 9 new sections (theory, evolution, intersection, failure modes, ecosystem, future). This lesson brings the deepening to the surface — it supplements L7, doesn't replace it.

## Key insight
The rhythm works because of **cognitive science**:
- **Working memory limits** (Miller ~7±2, Cowan ~4): you can't hold all three threads at once. The rounds are the workaround.
- **Cognitive load theory** (Sweller): the rounds are a cognitive load management strategy — each round adds one thread at a time.
- **Feedback loops**: hot reload (milliseconds) is why the loop works at feature scale. Boehm's spiral worked at project scale because the feedback loop was months.
- **Metacognition**: the "feel the friction" signal is the same metacognition from L13, applied to feature building.

The 8 failure modes (premature polishing, over-planning, skipping the sketch, storing derived state, waterfall in disguise, copy-paste without understanding, premature optimization, not feeling the friction) and the 8 principles (cycle don't waterfall, feel the friction, sketch data shape first, derived state is never stored, thinnest end-to-end slice first, structure follows state, simplest thing first, defer decisions) are the constants that survive every framework.

## Why this matters for future sessions
The Bridge movement is now complete (L12–15). The next movement is Human/product (L16–17). The rhythm deepened connects the problem-solving meta-skill (L12–14) to the feature-building skill (L7) via the shared concept of metacognition. The "enduring rhythm" insight — that the loop survives from Boehm (1986) to the React Compiler (2024) — is the key takeaway the learner should carry into the human layer: the technical skills compound, but the thinking skills compound faster.
