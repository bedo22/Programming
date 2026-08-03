# 0010 — An API is a contract with high reversal cost; styles are tools

- **Date:** 2026-07-30
- **Episode:** 10 (The Contract)
- **Status:** Active

## Context
Lesson 10 opened the System movement. The trap it dissolves: treating "API" as "an endpoint I call" rather than as a contract whose decisions are expensive to reverse — and treating REST/GraphQL/gRPC as a religion rather than as tools for different constraints.

## The insight
An API is a **contract** — a stable, evolvable boundary between independent deployables, producing *decisions not code* (resources, operation semantics, error contract, versioning, evolution guarantees). Its defining characteristic is **high reversal cost**: wire and interface changes are multi-week efforts. It has two layers — **interface** (macro: resources, versioning, errors, pagination, idempotency) and **wire** (micro: serialization, schema evolution, nullability, transport) — both needed. The styles (REST Fielding 2000, GraphQL 2015 for over/under-fetching, gRPC 2015 for contract-first codegen) are tools chosen for different constraints, not a religion; the core idea (a stable boundary) never changed while the winning style did. Critically, a bad contract doesn't stay at the boundary — it forces "paper-over code" downstream (loading states, retries, type assertions, toast storms), which is exactly the friction Lesson 7's developer loop absorbs.

## Why it matters
This reframes API work from "writing endpoints" to "making promises that are expensive to break," and connects the system layer to the frontend: every dead state and invisible failure in the UI often traces back to a contract that should have been designed. It pairs with Episode 11 (system design decides the boundaries; API design materializes them) and previews the Human/product movement (awkward contracts intrude on the UI as dead states).

## Evidence
- `reference/api-design.html` §0 (two-layer answer), §1 (definition + what it is not), §2 (history), §10 (failure modes).
- `lessons/0010-the-contract.html`.

## Revisions
_(none yet)_
