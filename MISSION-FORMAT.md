# MISSION-FORMAT.md

The format for `MISSION.md` — the document that grounds every lesson in *why* the learner is here.

## Required sections

```
# Mission — <short title>

> One-sentence mission statement.

## The mission
2–4 paragraphs. What the learner is after, in their own framing. Quote them where useful.

## Why this matters
The deeper "why." What breaks if the mission is ignored. Keep it honest, not motivational.

## What "done" looks like
Bullet list of observable outcomes. Concrete enough to tell when the journey is advancing.

## Scope
**In:** what this workspace teaches.
**Out:** what lives elsewhere (other repos, communities, certs).

## How progress is measured
Learning records in `./learning-records/`, lessons in `./lessons/`. Name the backbone.

## The journey map (optional but recommended)
A table: episode # | title | anchored reference doc. The curriculum backbone; episodes
may reorder as understanding deepens.

## Assets & conventions
Stylesheet, widget script, glossary adherence, lesson numbering scheme.
```

## Rules
- The mission is the *reason*, not a syllabus. Keep it about motivation and outcomes.
- If the mission changes, confirm with the learner, update this file, and add a learning
  record capturing the change (an ADR-style decision record).
- Keep it short — one screen. The journey map is the detailed plan, not the mission.
