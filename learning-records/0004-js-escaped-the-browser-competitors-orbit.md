# 0004 — JS escaped the browser; competitors orbit, not replace

- **Date:** 2026-07-30
- **Episode:** 4 (JS Across Stacks)
- **Status:** Active

## Context
Lesson 4 opened the Ecosystem movement. The trap it dissolves: assuming that because JS is "everywhere," it must have displaced every other language — when in fact each stack keeps its own winners.

## The insight
In **2009 Ryan Dahl built Node.js on Google's V8 engine**, pulling JS out of the browser and onto the server (Wikipedia). That made JS a general-purpose, cross-stack language. Yet five other major languages survive because each stack has a different dominant constraint, and the rule across the data is: **extend when the constraint is unchanged, invent when it inverts.** On the frontend the browser monopoly is absolute — no language replaces JS; you compile *to* it, and TypeScript *extends* it (compiles away, zero runtime) because the browser constraint never inverted. On other stacks the constraint did invert, so new languages won: Go (concurrency-first), Rust (memory safety without GC), Kotlin/Swift (modern mobile). JS sits at the center; the competitors orbit it.

## Why it matters
This reframes "why are there so many languages?" from confusion to a single test: does the new constraint invert the old language's design bet? It also explains why TypeScript is the special case the learner must understand — it's the one that extends rather than replaces, precisely because the browser constraint holds. Feeds Episode 5 (camps are abstractions over the same JS substrate) and Episode 9 (the compiler continues extending, not replacing).

## Evidence
- `reference/javascript-across-stacks.html` §0 (the pattern), §1 (frontend), §8 (the rule + table).
- `lessons/0004-js-across-stacks.html`.
- Wikipedia, "Node.js" (Ryan Dahl, 2009, V8).

## Revisions
_(none yet)_
