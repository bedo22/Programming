# LEARNING-RECORD-FORMAT.md

The format for files in `./learning-records/`. These are ADR-style records: they capture
**non-obvious lessons and key insights** that may need revision later or drive future
sessions. Not a log of "what I read" — a record of "what changed in my understanding."

## Filename
`NNNN-<dash-case-name>.md` — number increments each time (`0001-`, `0002-`, …).

## Required sections

```
# NNNN — <title>

- **Date:** YYYY-MM-DD
- **Episode/lesson:** which journey-map episode this belongs to (if any)
- **Status:** Active / Revised / Superseded

## Context
What triggered this record — a lesson, a question, a realization, a mission change.

## The insight
The non-obvious thing learned, stated precisely. The thing you'd want your past self to
know. This is the core.

## Why it matters
How this changes how you read/build/think about the ecosystem. What it unlocks downstream.

## Evidence
Links to reference docs, lessons, or external sources that back the insight.

## Revisions
Leave empty initially. When understanding deepens or the insight is corrected, append a
dated revision note here rather than rewriting — preserve the history of your thinking.
```

## Rules
- One insight per record. If a lesson taught three things, that's three records (or one
  record naming the single most important one).
- Status starts **Active**. Flip to **Superseded** if a later record corrects it; link
  the superseding record.
- These drive the zone of proximal development: read them before designing the next lesson.
