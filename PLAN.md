# Plan — The Exploration Journey (agreed)

> The agreed plan for the whole course: the story arc, the per-episode map, how every lesson works, and the conventions that keep it consistent. The mission lives in `MISSION.md`; this is the operating plan.

## 1. The story arc — why this order

The journey walks **from the atoms outward to the economic reality**, in seven movements. Each movement assumes the one before it — it's a dependency chain of *concepts*, not a syllabus of tutorials:

1. **Atoms** (Ep 1–3) — the irreducible concepts everything else is made of: the language (JS), the platform (HTML & CSS), and the single idea (state) that makes frontend make sense.
2. **Ecosystem** (Ep 4–6) — the landscape that grew on those atoms: where JS runs, the "camps" that ship UI, and React's class→hooks revolution.
3. **Practice** (Ep 7–9) — the mental models and rhythms developers use daily: the Model→View→Flow loop, Angular for contrast, and the React/Next frontier.
4. **System** (Ep 10–11) — how the bigger machine fits: API contracts and system design, crossing from frontend into architecture.
5. **Bridge** (Lessons 12–17) — the meta-skill layer: problem-solving (Pólya's four phases, computational thinking, algorithm paradigms), the rhythm deepened (theory, failure modes, principles), CS &amp; SE (the umbrella discipline), and solution evaluation (Big O, quality attributes, trade-offs, judgment). This is the connective tissue between the technical spine and the human layer — the "how do I think before I code?" and "how do I know if my solution is good?" that make the rest click.
6. **Human / product** (Ep 12–13) — upstream of code: UI/UX and design thinking, the layers that decide what code gets written.
7. **Economic reality** (Ep 14) — income and markets: why any of this exists as a livelihood.

Read in order, each episode gives you the vocabulary the next one assumes. You can't appreciate the camps (Ep 5) without the language (Ep 1) and the platform (Ep 2); you can't read React's revolution (Ep 6) without "state" (Ep 3); the practice layer (Ep 7) presumes you know the ecosystem; the system layer (Ep 10) presumes you know how frontends consume contracts; the bridge (L12–17) presumes you know the technical spine and deepens the thinking and evaluation skills; the human layer (Ep 12) presumes you know what's being built; the economic layer (Ep 14) presumes the whole stack exists.

## 2. The 14-episode map

**Episode 1 — The Accidental Lingua Franca** — *how JavaScript became the web's language.* Anchors `reference/javascript-the-language.html`. The 1995 origin, the ten-day sprint, the Mocha→LiveScript→JavaScript naming accident. Unlocks: why one language sits under every framework. *(✅ lesson written)*

**Episode 2 — The Platform Layer** — *what the browser actually is.* Anchors `reference/html-and-css.html`. The DOM, the CSSOM, the cascade, semantic primitives. Unlocks: the substrate that JS manipulates — you can't read frontend without it.

**Episode 3 — What Is "State"?** — *the one concept that makes the rest of frontend click.* Anchors `reference/what-is-state-prequel.html`. State vs props, the mental-model prequel. Unlocks: every framework conversation after this.

**Episode 4 — JS Across Stacks** — *where JS runs now, and who fights it.* Anchors `reference/javascript-across-stacks.html`. Browser, Node, edge, the TypeScript shift. Unlocks: why "the frontend" is no longer just the browser.

**Episode 5 — The Camps** — *a map of how real products ship UI today.* Anchors `reference/frontend-camps-survey.html`. CMS, HTML-first/islands, SPA, meta-frameworks, WASM. Unlocks: opening any repo and recognizing its camp without panic.

**Episode 6 — The Class→Hooks Revolution** — *the biggest mental-model shift in React.* Anchors `reference/class-to-hooks-paradigm-shift.html`. Why functions replaced classes, and what that changed. Unlocks: reading modern React.

**Episode 7 — The Rhythm** — *how developers think when building a feature.* Anchors `reference/how-developers-think-frontend.html`. The Model→View→Flow loop, the data-shape decision. Unlocks: the rhythm to follow, not just the syntax.

**Episode 8 — The Other Path** — *Angular's evolution, for contrast.* Anchors `reference/angular-evolution.html`. The class, the rewrite, signals. Unlocks: breadth — not every frontend is React.

**Episode 9 — The Frontier** — *where React is heading.* Anchors `reference/react-2024-and-beyond.html` + `reference/nextjs-deep-dive.html`. The compiler, RSC, the meta-framework. Unlocks: the current edge of the ecosystem.

**Episode 10 — The Contract** — *API design, how systems speak.* Anchors `reference/api-design.html`. Contracts, idempotency, consistency models. Unlocks: the boundary between frontend and backend.

**Episode 11 — The Architecture** — *system design, what code alone can't handle.* Anchors `reference/system-design.html`. Bounded contexts, failure domains, CAP. Unlocks: the bigger machine your code lives in.

**Bridge Lesson 12 — Problem-Solving: Pólya's Four Phases** — *the universal meta-rhythm.* Anchors `reference/problem-solving.html` §1–§2. Understand → Plan → Execute → Look back. Well-defined vs wicked problems. The key insight: problem-solving is a rhythm that produces an algorithm. Unlocks: the thinking skill that connects the technical spine to everything upstream. *(bridge — not a numbered episode in the original arc)*

**Bridge Lesson 13 — Problem-Solving: Computational Thinking + Heuristics** — *the lens and the moves.* Anchors `reference/problem-solving.html` §3–§5. The four pillars (decomposition, pattern recognition, abstraction, algorithm design) + Pólya's heuristic strategies + Schoenfeld's metacognition. Unlocks: how to devise a plan when you're stuck. *(bridge)*

**Bridge Lesson 14 — Problem-Solving: Paradigms + Debugging** — *the tools and the application.* Anchors `reference/problem-solving.html` §7, §9–§10. The six algorithm paradigms (brute force, greedy, D&C, DP, backtracking, hash table) + hypothesis-driven debugging + the "Look back" phase. Unlocks: recognizing which technique a problem needs. *(bridge)*

**Bridge Lesson 15 — The Rhythm Deepened** — *why the loop works, how it fails, what stays constant.* Anchors `reference/how-developers-think-frontend.html` §1e, §12b, §13b, §13d. Working memory and cognitive load (why you can't hold all three threads), the 8 failure modes, the 8 principles, and where the loop is heading (React Compiler, RSC, AI). Unlocks: the deepening you come back to after trying the loop on a real feature. *(bridge — supplements Lesson 7, does not replace it)*

**Bridge Lesson 16 — CS &amp; SE: The Discipline** — *the umbrella behind everything.* Anchors `reference/cs-and-software-engineering.html` §1–§3, §8. What CS is (the science of computation, Turing 1936), what SE is (the engineering of software, NATO 1968), how they differ, the 90-year lineage, and the engineering principles (DRY, SOLID, KISS, YAGNI). Unlocks: why HackerRank (CS) and your React job (SE) feel different. *(bridge)*

**Bridge Lesson 17 — Solution Evaluation** — *Big O, quality attributes, and trade-offs.* Anchors `reference/cs-and-software-engineering.html` §4–§7, §9. The parameters (ISO 25010 quality attributes), the measures (Big O notation, complexity classes), the trade-offs (time vs space, readability vs performance), and the judgment (which parameters matter when, when to stop). Traced through a brute-force firstNonRepeat solution and its upgrade. Unlocks: knowing whether your solution is good enough — and when to optimize. *(bridge)*

**Episode 12 — The Human Layer** — *UI/UX & web design.* Anchors `reference/ui-ux-web-design.html`. Habitability over decoration, a11y, motion. Unlocks: the rendering layer's guardrails.

**Episode 13 — Upstream of Code** — *design thinking, finding problems first.* Anchors `reference/design-thinking.html`. Wicked problems, the Double Diamond. Unlocks: what decides what code gets written.

**Episode 14 — The Real World** — *income streams & markets around the ecosystem.* Anchors `reference/income-stream-landscape.html` + `reference/frontend-income-markets.html`. Why this exists as a livelihood.

## 3. How every lesson works

Each lesson is **one self-contained HTML file** in `./lessons/`, named `NNNN-<dash-case-name>.html` (the number increments each time). It is short — one tightly-scoped concept, completable in one sitting, kept inside working memory. But each lesson delivers **one tangible win** you can build on.

**Method — knowledge first, then retrieval:**
1. **Knowledge** (low difficulty, story-driven): the concept, told as a story with the minimum needed to understand it. Difficulty is the enemy here — it eats the working memory you need for understanding.
2. **Retrieval practice** (effortful recall → storage strength): a "Retrieve it" section of auto-grading quizzes. The effort is what makes it stick long-term — fluency (in-the-moment "I get it") gives an illusory sense of mastery; storage strength is the real goal. Each lesson ends by nudging you to re-answer the questions from memory, *without the options*, the next day (spacing).

**Lesson structure** (built from the shared `assets/lesson.css` + `assets/lesson.js`):
- `header.lesson-head` — kicker, title, one-line meta.
- `section.recap` — where this fits in the journey + links to `MISSION.md` and the next lesson.
- Narrative `h2` sections + `blockquote.callout` for primary-source quotes.
- `h2` "Retrieve it" → `details.quiz` widgets.
- `section.win` — the single tangible takeaway.
- `section.next` — go-deeper link to the owning reference doc + next lesson + a reinforce-later nudge + the recommended primary source.
- `section.teacher` — prompt to ask follow-up questions.
- `footer.lesson-foot` — nav.

**Quiz widget contract** (powered by `assets/lesson.js`): a `<details class="quiz" data-answer="VALUE" data-explain="EXPLANATION">` whose `.quiz-body > .quiz-options` holds radio `<label>`s; the correct option's `value` must equal `data-answer`; on a correct answer, `data-explain` fills `.quiz-reveal`. Options are the same length on purpose — no clues from formatting. (A second widget, `.predict`, takes free-text input against `data-expected` — used for code-output skills, not history lessons.)

## 4. Conventions that keep the course consistent
- **Reuse is the default.** Every lesson links `../assets/lesson.css` and `../assets/lesson.js`. New reusable things (styles, widgets, diagram helpers) go in `assets/` as components and are linked — never inlined where a later lesson would duplicate them.
- **One vocabulary.** Terms follow `reference/glossary.html`; cite it, don't redefine its terms. Once a glossary term exists, every lesson uses it the same way.
- **Citations over memory.** Claims link to high-trust sources tracked in `RESOURCES.md`; each lesson names one primary source (the most high-quality, high-trust resource on the topic). Never trust parametric knowledge — verify.
- **Links everywhere.** Lessons anchor to sibling lessons and their owning reference docs, so the whole journey map is navigable.
- **Arabic.** `reference/ar/` holds translations of several docs; RTL is handled by `lang="ar"` on `<html>` (the JS swaps messages, code blocks stay LTR).
- **Numbering.** `0001-`, `0002-`, … incrementing each time, for both lessons (`./lessons/`) and learning records (`./learning-records/`).

## 5. How progress is tracked
- `./learning-records/` — ADR-style records, one per *insight* (not per lesson read). They capture non-obvious lessons and key decisions that may need revision later.
- Read the records before designing the next lesson to find your **zone of proximal development** — the "just enough" challenge.
- The journey map is a **backbone, not a cage**: episodes can reorder as understanding deepens. Record any reorder or mission change as a learning record (and confirm mission changes with the learner first).

## 6. Status
- ✅ **Atoms complete** — Episodes 1–3 written:
  - `lessons/0001-the-accidental-lingua-franca.html` (JS origin)
  - `lessons/0002-the-platform-layer.html` (DOM / CSSOM / cascade)
  - `lessons/0003-what-is-state.html` (state as a role)
- ✅ **Ecosystem complete** — Episodes 4–6 written:
  - `lessons/0004-js-across-stacks.html` (Node 2009, extend-vs-invent, TypeScript exception)
  - `lessons/0005-the-camps.html` (five camps, centers of gravity)
  - `lessons/0006-the-class-to-hooks-revolution.html` (hooks give functions state/effects)
- ✅ **Practice complete** — Episodes 7–9 written:
  - `lessons/0007-the-rhythm.html` (Model→View→Flow loop, sketch data shape first)
  - `lessons/0008-the-other-path.html` (Angular's three eras, same direction/different mechanism)
  - `lessons/0009-the-frontier.html` (compiler, Server Components, framework-default)
- ✅ **System complete** — Episodes 10–11 written:
  - `lessons/0010-the-contract.html` (API as contract, high reversal cost, styles are tools)
  - `lessons/0011-the-architecture.html` (system design, monolith vs services is a trade-off)
- ✅ **References expanded** — two references expanded to follow the standard template:
  - `reference/problem-solving.html` (826 lines, 24 sections, 17 tables) — created and expanded
  - `reference/how-developers-think-frontend.html` (893 lines, 24 sections, 13 tables) — expanded with theory, evolution, intersection, failure modes, ecosystem, future
- ✅ **Bridge complete** — 8 lessons written (L12–L19):
  - `lessons/0012-problem-solving-polyas-four-phases.html` (Pólya's four phases, three-layer model, well-defined vs wicked)
  - `lessons/0013-problem-solving-computational-thinking.html` (CT four pillars, seven heuristics, Schoenfeld's metacognition)
  - `lessons/0014-problem-solving-paradigms-and-debugging.html` (six paradigms, D&C vs DP, debugging, look-back phase)
  - `lessons/0015-the-rhythm-deepened.html` (cognitive science, 8 failure modes, 8 principles, the future)
  - `lessons/0016-cs-and-se-the-discipline.html` (CS vs SE, 90-year history, Turing to Agile, DRY/SOLID/KISS/YAGNI)
  - `lessons/0017-solution-evaluation.html` (Big O, ISO 25010 quality attributes, trade-offs, judgment, worked example)
- ✅ **CS & SE reference created** — `reference/cs-and-software-engineering.html` (550 lines, 20 sections, 18 tables) — the umbrella discipline. Glossary updated with 15 new terms. RESOURCES.md updated with 6 new sources.
- ✅ **Software Development Process (macro) complete** — 1 reference + 2 bridge lessons written (the "Agile is project management?" question answered through a full template doc):
  - `reference/software-development-process.html` (19 sections, valid close) — the SDLC six phases, Agile Manifesto (4 values/12 principles), Scrum, Kanban, XP/Lean/DevOps, the macro/micro table (SDLC ↔ The Rhythm), failure modes, ecosystem, and the AI-augmented SDLC vs **Agent Development Lifecycle (ADLC)** distinction.
  - `lessons/0018-the-software-development-process.html` (SDLC phases vs methodology; Agile; The Rhythm is the micro within the macro)
  - `lessons/0019-scrum-kanban-and-the-ai-frontier.html` (Scrum 3-5-3, Kanban flow/WIP, failure modes, AI-augmented SDLC vs ADLC)
  - Learning records `0018` and `0019` written.
- ✅ **Human/product & Economic reality complete** — journey finished (22 lessons):
  - `lessons/0020-the-human-layer.html` (UI/UX: four disciplines, usability, state visibility, accessibility baseline) — anchors `ui-ux-web-design.html`; learning record `0020`
  - `lessons/0021-upstream-of-code.html` (Design Thinking: desirability/feasibility/viability Venn, five phases, design theater) — anchors `design-thinking.html`; learning record `0021`
  - `lessons/0022-the-real-world.html` (seven income streams, USD band reading, AI-field evaluation skill, sequencing) — anchors `frontend-income-markets.html` + `income-stream-landscape.html`; learning record `0022`
- ✅ **Journey complete** — 22 lessons, six movements (Atoms 1–3, Ecosystem 4–6, Practice 7–9, System 10–11, Bridge 12–19, Human/product & Economic reality 20–22). Mission (exploration, conceptual literacy) fulfilled. Further sessions become depth on any node, not new breadth.
- 🔧 **Open:** verify `speakingjs.com` reachability before recommending it as a primary read.

