# 0018 — The SDLC and methodology: the project-scale process layer

**Date:** 2026-08-06
**Lesson:** `lessons/0018-the-software-development-process.html`
**Reference:** `reference/software-development-process.html` §1–§3, §6–§7, §10

## Context
The learner asked "I heard about Agile methodology — what entity is this, is it project management, does it need its own reference doc?" During planning we realised the gap: our map had The Rhythm (the micro — one feature) but not the macro — the project-scale process that contains it. The term that finally landed was "Software Development Lifecycle" (SDLC), and the correct entity name for Agile is a **methodology** — one way of navigating the SDLC. We built a new reference (`software-development-process.html`) covering the full template and two lessons (L18–L19). This closes the Agile/SDLC question completely.

## Key insight
There are **two distinct layers** that people conflate: the **SDLC** is *what* six phases happen (Requirements → Design → Implementation → Testing → Deployment → Maintenance) — relatively stable since the 1970s; a **methodology** (Waterfall, Spiral, Agile, Scrum, Kanban, Lean, DevOps) is *how* you navigate them. Agile is one methodology, not a synonym for SDLC. The history is a 55-year inversion: **processes that embrace change beat processes that resist it** (Waterfall → Spiral 1986 → XP 1999 → Agile Manifesto 2001 → Lean/DevOps). Deeper: **The Rhythm is the micro within the macro** — a sprint contains features, and each feature is built with Model→View→Flow. The two reference docs (rhythm + SDLC) are the same iterative idea at two different scales.

## Why this matters for future sessions
This connects the whole map. The Rhythm (L7, micro) now has its macro counterpart. Agile Principle 10 *is* YAGNI (CS & SE L16), Principle 12 *is* metacognition (Problem-Solving L13) — the process validates the methodological principles we learned as standalone ideas. The SDLC history threads through the whole exploration: it's the story of the same constraint inversion (embrace change) seen at every layer. Next: L19 covers Scrum/Kanban in practice and the AI frontier.
