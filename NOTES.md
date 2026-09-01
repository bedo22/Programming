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
- **Atoms (Ep 1–3), Ecosystem (Ep 4–6), Practice (Ep 7–9), System (Ep 10–11), and Bridge (L12–17) complete.** Next: Human/product movement (L18–19), then Economic reality (L20). 3 lessons total remaining.
- **Rhythm lesson (0007) assessment:** Does NOT need rewriting — it's the right introductory scope (three threads, rounds, data shape). The expanded rhythm reference (§1e theory, §13b failure modes, §12b principles, §13d future) deserves a SECOND lesson (0015 — The Rhythm Deepened), not a rewrite of 0007.
- **CS & SE reference created** (`reference/cs-and-software-engineering.html`, 550 lines, 20 sections, 18 tables) — the umbrella discipline. Covers the 90-year lineage (Turing → Knuth → NATO → SOLID → ISO 25010), the theory (computability, complexity, information), the evaluation skill (Big O, quality attributes, trade-offs, judgment), and the engineering principles (DRY, SOLID, KISS, YAGNI). Glossary updated with 15 new terms. RESOURCES.md updated with 6 new sources.
- **Problem-solving reference created and expanded** (`reference/problem-solving.html`, 823 lines, 24 sections, 17 tables). Now follows the same structural template as the other reference docs: Definition → History → Evolution → Intersection → Underlying theory → Mental models → Methodology (Pólya, CT, heuristics, metacognition, stepwise refinement, paradigms) → Principles → Worked example → Failure modes → Ecosystem → Future → Summary. Glossary updated with 12 new terms. RESOURCES.md updated with 12 sources (Pólya, Schoenfeld, Wing, Hunt & Thomas, Wirth, Dromey, Agans, competitive programming, Luchins/Einstellung, Sweller/cognitive load, Simon & Chase/expertise, Ericsson/deliberate practice). **Lessons TBD** — learner will decide whether it needs a full episode or a bridge lesson.
- **`.cite` rule (learned):** the `.cite` class auto-prepends "Primary source → ", so use it ONLY for the single primary-source block in each lesson's `.next` section — never on inline attributions (that caused a double prefix in Lesson 1, now fixed). Apply to all future lessons.
- Re-verify `speakingjs.com` reachability before using it as a primary-read recommendation.

## 2026-09-01 — shelf-pipeline 1.2.18 sync (wave 1)

- claim_source `auto` → `محاور` (notes carry ### المحور headers, 3/note; C# rows absent — behavior-neutral, was 0+3=3).
- New 1.2.18 guard: `claims_count` refuses loudly on removed/unknown sources — stale configs crash instead of silently counting zero.
- `assets/lesson.css`: sync overwrote the local Tufte design; **restored from git** — divergence intentional, protect on future syncs.
- Gates: selftest 26/26, doctor clean, pins yt-001 Flags: 0 (6 verified).
- Full check: 63 failures — **pre-existing doc debt newly visible** (47 broken links: flat `reference/*.html` docs use `../digests/…` paths that overshoot; 16 Unmapped-block docs). Notes lane green. Link fix = future mini-wave.

### Link-fix mini-wave closed (2026-09-01, later same day)

- 45/47 broken links fixed mechanically (../ overshoot from flat reference/
  docs — stripped after verifying every target + anchor exists). 47 -> 2.
- Remaining 2 = literal {image}/{url} template placeholders in
  html-and-css.html — content gap, needs the real asset/URL (doc backlog).
- Metadata verdicts (16 -> 0): config note_meta mapping added (AR labels,
  status_values census 8/8 = جاهزة). Notes untouched.
- Full check: 63 -> 3 (the two placeholders + one duplicate). Sessions 8/8
  with notes, all citations/quotes/links/statuses intact per-note.
