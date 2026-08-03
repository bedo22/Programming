# Notes — working scratchpad

## Learner context (session 1)
- Has a **separate** teaching repo for the tactical tracks (HackerRank JS Basic cert, job-readiness, reading real React codebases). This repo ("Programming") is the **exploration journey** — conceptual literacy only. Don't mix the two.
- The reference shelf here was produced by an earlier brainstorming session with an agent. `reference/ar/` holds Arabic translations of ~11 docs.
- Brought the assets (`lesson.css`, `lesson.js`) over from the other repo so reference docs render styled. Confirmed present: `assets/lesson.css` (6.9 KB), `assets/lesson.js` (3.1 KB).
- `React Summary.pdf` (7.9 MB) sits at root — likely belongs to the other repo's React-reading track; not part of this journey unless the learner asks.

## Teaching preferences
- **Knowledge-first, story-driven.** Difficulty is the enemy during acquisition; build storage strength afterward via retrieval practice (the quiz widget).
- **Cite high-trust external sources; never trust parametric memory.** Verify URLs before recommending.
- **Adhere to `reference/glossary.html` vocabulary** in every lesson — don't redefine its terms.
- Lessons short, one concept, completable in one sitting.

## Conventions discovered (from existing assets + reference docs)
- **Lesson HTML structure:** `header.lesson-head` (`.kicker` / `h1` / `.meta`), `section.recap`, `blockquote.callout`, `details.quiz`, `section.win`, `section.next`, `section.teacher`, `footer.lesson-foot`. Link `../assets/lesson.css`; include `../assets/lesson.js` before `</body>`.
- **Quiz markup contract** (from `lesson.js`): `<details class="quiz" data-answer="VALUE" data-explain="EXPLANATION">` → `<summary>` (the question) → `.quiz-body` → `ul.quiz-options` of `<label><input type="radio" name="..." value="VALUE"></label>` → `.quiz-feedback` → `.quiz-reveal`. The correct option's `value` must equal `data-answer`. On correct, `data-explain` fills `.quiz-reveal`.
- **Predict widget:** `.predict` with `data-expected`, an `input[type=text]`, `button`, `.predict-feedback`, `.predict-reveal`.
- **RTL:** handled via `lang="ar"` on `<html>`; the JS swaps messages. Code blocks stay LTR.
- Existing reference docs already link `../assets/lesson.css` (so they render styled now that assets exist) and `../assets/lesson.js`. Some also link forward to `../lessons/0001-scope-and-hoisting.html` etc. — aspirational links from the brainstorming; our lessons use a fresh numbering tied to the journey map.

## Open questions / TODO
- **Atoms (Ep 1–3), Ecosystem (Ep 4–6), Practice (Ep 7–9), and System (Ep 10–11) complete.** Next: Bridge movement (4 lessons — problem-solving + rhythm deepened), then Human/product (Ep 12–13), then Economic reality (Ep 14). 7 lessons total remaining.
- **Rhythm lesson (0007) assessment:** Does NOT need rewriting — it's the right introductory scope (three threads, rounds, data shape). The expanded rhythm reference (§1e theory, §13b failure modes, §12b principles, §13d future) deserves a SECOND lesson (0015 — The Rhythm Deepened), not a rewrite of 0007.
- **Problem-solving reference created and expanded** (`reference/problem-solving.html`, 823 lines, 24 sections, 17 tables). Now follows the same structural template as the other reference docs: Definition → History → Evolution → Intersection → Underlying theory → Mental models → Methodology (Pólya, CT, heuristics, metacognition, stepwise refinement, paradigms) → Principles → Worked example → Failure modes → Ecosystem → Future → Summary. Glossary updated with 12 new terms. RESOURCES.md updated with 12 sources (Pólya, Schoenfeld, Wing, Hunt & Thomas, Wirth, Dromey, Agans, competitive programming, Luchins/Einstellung, Sweller/cognitive load, Simon & Chase/expertise, Ericsson/deliberate practice). **Lessons TBD** — learner will decide whether it needs a full episode or a bridge lesson.
- **`.cite` rule (learned):** the `.cite` class auto-prepends "Primary source → ", so use it ONLY for the single primary-source block in each lesson's `.next` section — never on inline attributions (that caused a double prefix in Lesson 1, now fixed). Apply to all future lessons.
- Re-verify `speakingjs.com` reachability before using it as a primary-read recommendation.
