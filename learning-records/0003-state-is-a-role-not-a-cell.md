# 0003 — State is a role a variable plays, not a cell

- **Date:** 2026-07-30
- **Episode:** 3 (What Is "State"?)
- **Status:** Active

## Context
Lesson 3 closed the Atoms movement. The conceptual trap it dissolves: the word "state" sounding like a special kind of memory, when it is really a label for the role an ordinary variable plays.

## The insight
**State is an ordinary variable that persists and matters across events** — there is no special "state" cell type. The real distinction is three properties any variable has — **lifetime**, **scope**, **reachability**; a variable becomes "state" when its lifetime is long enough that later events depend on earlier values and its reachability is wide enough that more than one code path modifies it. The concept builds as a chain: **data → value → variable → state**. For UIs a plain local variable fails twice (it doesn't persist between renders; mutating it doesn't trigger a re-render); state fixes both, and is **private** to the component, unlike **props** (passed in, read-only). The history of UI is the history of *where state lives* (global → closure → class field → store → hook slot → server).

## Why it matters
This is the prequel that makes the class→hooks paradigm shift (Episode 6) legible: hooks didn't invent a new kind of state, they re-framed the contract ("this re-runs when its inputs change") while the storage underneath stayed an ordinary cell. It also gives a single test — "does it persist and matter across events?" — for spotting state in any paradigm, which surfaces again in Episodes 7 and 9.

## Evidence
- `reference/what-is-state-prequel.html` §5 (variables ≠ state), §6 (where state lives across paradigms), §7.
- `lessons/0003-what-is-state.html`.
- React docs, "State: A Component's Memory" (react.dev).

## Revisions
_(none yet)_
