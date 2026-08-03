# 0005 — Frontend ships UI in camps; labels are centers of gravity

- **Date:** 2026-07-30
- **Episode:** 5 (The Camps)
- **Status:** Active

## Context
Lesson 5 mapped how real products ship UI. The trap it dissolves: assuming every frontend is a React SPA, then panicking when a codebase isn't.

## The insight
There are roughly five frontend **camps** — CMS/classic server (server owns the document, JS optional), HTML-first (documents + small islands, ship almost no framework), SPA (client app shell, large initial JS), meta-framework (route + data + UI, server/browser split), and WASM/systems UI (compiled module, JS as glue). They differ most by **unit of work and JS load strategy** — where the JS lives and how much ships. Critically, camps *overlap*: a Next.js app can be a meta-framework yet behave like an SPA on some routes. Labels are **centers of gravity, not exclusive walls**. The goal at work is recognition — "this is HTML-first with Preact islands" — not converting every project to one favorite camp.

## Why it matters
This is the orientation that prevents the learner from forcing one mental model onto every codebase. It also previews why Episode 6 (React's class→hooks shift) is only one camp's internal story — Angular, Svelte, Solid each took a different path (Episode 8 contrast). And it grounds Episode 11: rendering strategy (SSR/RSC/Islands/SPA) is itself a camp-level decision about who emits the initial HTML.

## Evidence
- `reference/frontend-camps-survey.html` §0 (the camps table), §1–5 (each camp), mission-fit callout.
- `lessons/0005-the-camps.html`.

## Revisions
_(none yet)_
