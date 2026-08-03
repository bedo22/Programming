# 0001 — The exploration journey is knowledge-first, story-driven

- **Date:** 2026-07-30
- **Episode:** Establishes the journey (precedes Episode 1)
- **Status:** Active

## Context
The workspace held a rich `reference/` shelf (≈20 English HTML docs plus `reference/ar/` Arabic translations and a `React Summary.pdf`) produced by an earlier brainstorming session, but **no teaching scaffolding**: no `MISSION.md`, no `lessons/`, no `learning-records/`, no `RESOURCES.md`, no `NOTES.md`. The `assets/` folder (`lesson.css`, `lesson.js`) existed but was nearly missed on first inspection. The learner clarified the mission: this repo is the **exploration journey** — broad conceptual literacy (concepts, theory, definitions, history, mental models, rhythms) — distinct from a *separate* repo handling certs/job-readiness/React-reading.

## The insight
This is a **knowledge-heavy, story-driven** mission, which inverts the usual skill-first teaching default: here **difficulty is the enemy during acquisition** (storytelling, low cognitive load, easy to absorb), and **storage strength is built afterward** through retrieval practice (effortful recall, spacing). The existing reference shelf is the *knowledge source*; lessons are the *story + retrieval loop* that turns that knowledge into retained understanding. The curriculum is a 14-episode journey map walking from the atoms (the JS language) outward to the economic reality (income/markets), each episode anchoring to one reference doc.

A secondary insight: the reference docs already share an asset contract (`../assets/lesson.css` + `../assets/lesson.js`) and a glossary (`reference/glossary.html`). Reuse is mandatory — lessons must use the same stylesheet, the same quiz-widget markup contract, and the same vocabulary, or the course fragments into one-offs.

## Why it matters
This record is the charter for every future lesson. It fixes the **method** (knowledge-first → retrieval practice), the **backbone** (the 14-episode map in `MISSION.md`), and the **conventions** (assets + glossary). Any later lesson that drifts from these should be checked against this record. It also explains *why* lessons will be short and story-shaped rather than tutorial-shaped: the goal is a mental map, not a build portfolio.

## Evidence
- `MISSION.md` — the mission statement and the 14-episode journey map.
- `assets/lesson.js` — defines the quiz/predict widget markup contract every lesson must follow.
- `reference/glossary.html` — the shared vocabulary every lesson must adhere to.
- `lessons/0001-the-accidental-lingua-franca.html` — the first lesson, exemplifying the method.
- `RESOURCES.md` — high-trust sources grounding the claims (MDN, Wikipedia, the 1995 Netscape/Sun press release, ECMA-262, the HOPL IV paper).

## Revisions
_(none yet)_
