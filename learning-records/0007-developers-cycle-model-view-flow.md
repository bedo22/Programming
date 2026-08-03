# 0007 — Developers cycle Model→View→Flow; sketch the data shape first

- **Date:** 2026-07-30
- **Episode:** 7 (The Rhythm)
- **Status:** Active

## Context
Lesson 7 opened the Practice movement. The trap it dissolves: staring at a blank file with no process, or following a waterfall (structure→style→logic) that doesn't match how seniors actually work.

## The insight
Experienced frontend developers hold **three threads — Model (data/state shape), View (structure/layout), Flow (events/logic) — and cycle through them as a loop, each pass deeper.** It is a rhythm, not a sequence. The single most important upfront decision is to **sketch the data shape first**: the nouns, their fields and types, the collection type, the operations, where state lives, and what's derived (not stored). Getting that right surfaces traps — like "loading" vs "loaded but empty" — while they cost minutes, not days. The loop has a history: Boehm's spiral model (1986), iterative/incremental development, XP, Agile, the Lean Startup MVP — all the same idea, that you build in narrowing spirals and let friction tell you when to deepen.

## Why it matters
This is the transferable thinking process that works in any camp (Episode 5) and any framework. It also reframes "where do I even start?" into a concrete checklist (the reference doc's §14 table): nouns → fields → collection → operations → where state lives → what's derived → thinnest end-to-end slice. The data-shape-first habit directly uses Episode 3's state concept and previews Episode 10 (API contracts are the data shape's upstream boundary).

## Evidence
- `reference/how-developers-think-frontend.html` §1 (three threads), §14 (the checklist table), the primary-sources block (Boehm 1986, Larman & Basili 2003, Beck 1999, Agile Manifesto, Ries 2011).
- `lessons/0007-the-rhythm.html`.

## Revisions
_(none yet)_
