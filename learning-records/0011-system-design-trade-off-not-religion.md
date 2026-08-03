# 0011 — System design structures across boundaries; monolith vs services is a trade-off

- **Date:** 2026-07-30
- **Episode:** 11 (The Architecture)
- **Status:** Active

## Context
Lesson 11 closed the System movement. The trap it dissolves: assuming "architecture" is either enterprise bureaucracy or a 45-minute interview exercise — and assuming microservices are always the right answer.

## The insight
System design is the architectural layer that **structures a solution across trust, consistency, and scaling boundaries** — producing *decisions not code* about decomposition (independent units), data ownership (source of truth), consistency models, failure domains, and capacity. Like API design, its defining trait is **high reversal cost**: service boundaries are expensive to change. It operates at two scales — **architectural** (macro: services, events, scaling, failure) and **component** (micro: bounded contexts, API contracts, trust boundaries); both are system design, neither is complete alone. The big reframe: **monolith vs microservices is a trade-off, not a religion** — a URL shortener is fine as a CRUD monolith (one team, simple domain); a multi-team order system needs event-driven services with compensation (saga). The right answer is driven by team boundaries, domain complexity, and scale. History: Parnas information hiding (1972) → distributed systems (Lamport) → SOA → Amazon two-pizza teams (2006) → 12-Factor (2011) → microservices (2015) → DDD/event-driven.

## Why it matters
This is the layer that makes Lesson 10's contracts meaningful — system design decides the boundaries; API design materializes them. It also closes the technical spine of the journey (atoms → ecosystem → practice → system) before the Human/product movement turns outward to the user. The "high reversal cost" thread now connects Lessons 10 and 11: both API and system decisions are expensive to reverse, which is what makes them *design* rather than *coding*.

## Evidence
- `reference/system-design.html` §0 (two layers), §1 (definition + what it is not), §2 (history), §9–10 (worked examples: URL shortener, event-driven orders).
- `lessons/0011-the-architecture.html`.

## Revisions
_(none yet)_
