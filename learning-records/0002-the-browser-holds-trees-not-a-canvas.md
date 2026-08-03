# 0002 — The browser holds trees, not a canvas

- **Date:** 2026-07-30
- **Episode:** 2 (The Platform Layer)
- **Status:** Active

## Context
Lesson 2 established the platform layer. The recurring confusion it dissolves: treating the page as a flat canvas to "draw on" rather than as in-memory trees the browser holds and JavaScript mutates.

## The insight
The browser is **not a canvas** — it builds **three trees** from one source (the HTML you write): the **DOM** (parsed HTML, structure), the **CSSOM** (parsed CSS, styles), and the **render tree** (their merge into boxes, where layout/paint/composite happen). A parallel **accessibility tree** is what screen readers actually traverse. The **cascade** — origin, importance, specificity, source order, scope, layers — is the *deterministic, inspectable* algorithm that picks the winning style. JavaScript never paints pixels; it mutates the DOM/CSSOM and lets the platform render. Every framework is a different abstraction over this same substrate; the substrate doesn't change, only the leakiness does.

## Why it matters
This is the mental model that turns "a layout broke" into a *platform* problem you can locate, not a mystery. It also grounds the later camps survey (Episode 5) and the rendering-strategy choices in system design (Episode 11): SSR / RSC / Islands / SPA are all answers to "who emits the initial HTML and when CSS arrives" against this substrate.

## Evidence
- `reference/html-and-css.html` §0 (the two-tree answer), §1 (definition + cascade), §4 (intersections).
- `lessons/0002-the-platform-layer.html`.
- MDN, "How CSS works" (DOM / CSSOM / render tree).

## Revisions
_(none yet)_
