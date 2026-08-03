# Mission — The Exploration Journey

> Build broad conceptual literacy in programming, the web, and the frontend ecosystem — the concepts, the history, the mental models, and the rhythms.

## The mission
This workspace is an **exploration journey**, not a tutorial grind or a certification track. The goal is conceptual literacy: the concepts, theory, and definitions; the **history and evolution** of the field; and the past problems and challenges that shaped the current ecosystem. Internalize the mental models and rhythms practitioners follow.

A separate workspace handles the tactical tracks (job-readiness, certifications, reading real React codebases). This one is for **understanding the map** — the story of how we got here, and the models that let you read any part of the ecosystem without panic.

## Why this matters
The learner's own framing: *"my knowledge is limited, so I think this is an exploration journey."* Knowledge here is the goal; difficulty is the enemy during acquisition. Long-term retention (storage strength) is built afterward through retrieval practice. Skip the "why bother" — the motivation is genuine curiosity about the ecosystem's shape.

## What "done" looks like
- A navigable mental map of the frontend / web / programming ecosystem.
- For any major concept (state, the event loop, prototypes, the cascade, RSC, bounded contexts…), the learner can say **what it is, why it exists, and what problem it solved.**
- The learner can open any reference doc on the shelf and read it as familiar territory.

## Scope
**In:** history, definitions, mental models, rhythms, the "why" behind the "what."
**Out:** step-by-step build tutorials, certification drills, leetcode — those live in the other workspace.

## How progress is measured
Learning records in `./learning-records/` (one per insight). Lessons in `./lessons/` walk the journey map below. The map is a backbone, not a cage — episodes can reorder as understanding deepens.

## The journey map (curriculum backbone — each episode anchors to a reference doc)

| # | Episode | Anchored to |
|---|---------|-------------|
| 1 | The Accidental Lingua Franca — how JavaScript became the web's language | `reference/javascript-the-language.html` |
| 2 | The Platform Layer — what the browser actually is (HTML & CSS) | `reference/html-and-css.html` |
| 3 | What Is "State"? — the one concept that makes the rest of frontend click | `reference/what-is-state-prequel.html` |
| 4 | JS Across Stacks — where JS runs now, and who fights it | `reference/javascript-across-stacks.html` |
| 5 | The Camps — a map of how real products ship UI today | `reference/frontend-camps-survey.html` |
| 6 | The Class→Hooks Revolution — the biggest mental-model shift in React | `reference/class-to-hooks-paradigm-shift.html` |
| 7 | The Rhythm — how developers think (Model→View→Flow loop) | `reference/how-developers-think-frontend.html` |
| 8 | The Other Path — Angular's evolution, for contrast | `reference/angular-evolution.html` |
| 9 | The Frontier — React 2024+ & Next.js, where it's heading | `reference/react-2024-and-beyond.html`, `reference/nextjs-deep-dive.html` |
| 10 | The Contract — API design, how systems speak | `reference/api-design.html` |
| 11 | The Architecture — system design, what code alone can't handle | `reference/system-design.html` |
| 12 | The Human Layer — UI/UX & web design | `reference/ui-ux-web-design.html` |
| 13 | Upstream of Code — design thinking, finding problems first | `reference/design-thinking.html` |
| 14 | The Real World — income streams & markets around the ecosystem | `reference/income-stream-landscape.html`, `reference/frontend-income-markets.html` |

> Full plan — story-arc logic, per-episode detail, and how every lesson works: see `PLAN.md`.

## Assets & conventions
- Every lesson links `../assets/lesson.css` (Tufte-ish shared stylesheet) and `../assets/lesson.js` (quiz/predict widget). Reuse is the default — never inline what a component already provides.
- Vocabulary follows `reference/glossary.html`; cite it, don't redefine its terms.
- Lessons are numbered `0001-<dash-case-name>.html`, incrementing each time.
- The `reference/ar/` subfolder holds Arabic translations of several docs.
