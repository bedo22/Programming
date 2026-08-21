# Doc Improvement Rules

How to improve any shelf doc. Derived from the problem-solving.html
refactoring and informed by the shelf-review skill's criteria model,
guards, and pattern library.

## Phase 1 — Understand the doc before changing it

Every doc has a purpose, an audience, and a scope. Read the doc fully
before touching it. Record:

1. **What question does this doc answer?** (the one-line purpose)
2. **Who is it for?** (the audience, reading level)
3. **What should the reader be able to DO after reading?** (the objective)
4. **What does this doc own vs defer?** (the ownership map — which facts
   are exclusive to this doc, which are shared with neighbors)
5. **What prior knowledge does it assume?** (the prerequisites)

If you can't answer these five, you don't understand the doc well enough
to improve it.

## Phase 2 — Analyse the narrative

### The narrative arc

A good shelf doc has a narrative arc, not just a list of sections. The
arc is:

```
Hook (why this matters) → Foundation (what it is) → Core (the method)
→ Practice (how to use it) → Depth (why it works) → Reference (lookup)
→ Close (so what, what's next)
```

Map the doc's current sections to this arc. Ask:

- **Does each section build on the previous?** Or do sections jump around?
- **Is the core method introduced early?** Or buried after history/theory?
- **Does the reader know where they are?** Is there a "you are here" moment?
- **Does later content reference earlier content correctly?**
- **Is there a clear "so what?" at the end?**

### Reordering

Reordering improves narrative. Do it when the analysis shows sections are
out of the arc. The risk is broken cross-references — so:

1. Map every internal cross-reference (`#sec-*` link) before reordering
2. Move sections
3. Update every cross-reference
4. Verify with `grep -c '<h2'` (h2 parity) and anchor resolution

The sticky TOC helps navigation but doesn't fix narrative. A doc with
bad section order and a good TOC is a doc with bad section order and a
good table of contents. Fix the order.

### What makes narrative bad

- **Theory before method.** History and cognitive science before Pólya's
  four phases. The reader wants to solve problems, not read a literature
  review. Theory goes after the method, or in a collapsible `<details>`.
- **Reference material mixed with narrative.** Paradigm tables, data
  structure catalogs, tooling lists — these are lookups, not teaching.
  Either collapse them in `<details>` or move them to the owning doc.
- **No progression.** Sections that could be in any order. The reader
  gains nothing from reading section 7 before section 3. Fix by establishing
  dependencies: "section X assumes you read section Y."
- **Duplicated framing.** Two sections that open with the same "why this
  matters" paragraph. Merge the openings.

## Phase 3 — Find the gaps

### Missing questions

Read the doc and ask: what questions does a reader naturally have that
this doc doesn't answer? Write them down. For each:

- Is the answer in another doc on the shelf? → cross-reference it
- Is the answer nowhere on the shelf? → add it here (or create a new doc)
- Is the answer implied but not stated? → state it explicitly

### Missing sections

Check against the house template's spine order:
1. How to use this doc (reading order, cross-links)
2. Definition (what it is, what it's not)
3. Core method (the main content)
4. Practice (how to apply it)
5. Failure modes (what goes wrong)
6. Ecosystem (tools, resources)
7. Summary / checklist

If a doc is missing a standard section, ask whether it should have one.
Not every doc needs every section — but the absence should be deliberate.

### Missing depth

Some sections are too shallow. Signs:
- A claim without evidence ("studies show...")
- A principle without example ("decompose before solving")
- A table row without explanation (just a label and a link)

For each shallow section, ask: what would make this actionable? Add
the example, the worked trace, the concrete scenario.

### Missing connections

Does the doc reference its neighbors? Check:

- **Upstream:** does it say what feeds into it? (e.g., "Design Thinking
  produces the problem; this doc solves it")
- **Downstream:** does it say what it feeds? (e.g., "This doc produces
  a verified solution; the dev loop implements it")
- **Sibling:** does it distinguish itself from nearby docs? (e.g.,
  "System Design structures across boundaries; this doc structures
  within a boundary")

If a doc doesn't explain its relationship to neighbors, the reader
doesn't know when to switch docs.

## Phase 4 — Check cross-doc boundaries

### Duplication detection

For every claim, table, or framework in the doc:

1. Grep the shelf for the same claim/table/framework
2. If it appears in another doc, ask: **which doc owns this?**
3. If the other doc owns it → leave a pointer, remove from this doc
4. If this doc owns it → check the other doc for a pointer
5. If neither clearly owns it → pick one based on which doc teaches it
   more deeply

The rule: **one doc owns each piece of knowledge.** The other docs
reference it. Never have two docs teaching the same thing independently.

### Boundary clarity

After checking duplication, verify:

- The ownership map (Phase 1) is accurate
- Every cross-reference points to the owning doc
- The doc says what it does NOT cover (scope exclusion)

## Phase 5 — Analyse the design

### Navigation

For docs over ~1500 lines:
- **Sticky TOC** with links to every h2
- **Quick-reference lookup bar** for returning readers (methodology docs)
- **`<details>` toggles** for long reference subsections (tables,
  checklists, catalogs, history sections)

### Visual hierarchy

- h2 = major sections (one topic)
- h3 = subtopics within a section
- h4 = reference material within a subtopic (collapse in `<details>`)
- Tables = structured reference (clear headers, scannable rows)
- Callouts = key insights (one per section max, not every paragraph)
- Code blocks = working examples (commented, with input/output)

### Consistency

- Same heading style as other docs (no section numerals, `id="sec-kebab"`)
- Same callout style (blockquote.callout)
- Same table format (thead + tbody, no inline styles on cells)
- Same footer structure (upstream/sibling/downstream links)

## Phase 6 — Apply changes

Order of operations (lowest risk first):

1. **Add navigation** (TOC, lookup bar, details toggles) — no content change
2. **Add missing content** (new sections, expanded explanations) — additive
3. **Merge overlapping sections** (dedup within doc) — removes duplication
4. **Move misplaced content** (to owning doc, leave pointer) — structural
5. **Reorder sections** (fix narrative arc) — high risk, update all refs
6. **Design improvements** (consistent formatting, visual hierarchy) — cosmetic

For each change:
- Make the change
- Verify h2 parity (EN = AR)
- Verify all anchors resolve
- Sync the AR twin
- Run verify-twins.py

## Phase 7 — Verify and report

After all changes:

1. `grep -c '<h2'` EN and AR — must match
2. All `id` attributes on h2/h3 tags present and unique
3. All internal `#sec-*` anchors resolve
4. All cross-doc anchors resolve
5. No stray `§` numerals in headings
6. EN→AR and AR→EN lang-switch links present
7. `verify-twins.py` passes (except known limitations)
8. No content was deleted (only true duplication removed)
9. Every section has a clear purpose in the narrative arc
10. Every cross-reference points to the owning doc

## Failure modes to avoid

These come from the shelf-review guards and the problem-solving experience:

- **Audit against purpose, not taste.** "I would write it differently"
  is not a finding. "The reader can't find X" is.
- **Operational beats theoretical.** "What do I do?" outranks
  "Why does it work?" — but don't delete the "why," just put it
  after the "what."
- **Non-destructive unless told otherwise.** Move before delete.
  Collapse before cut. Point before duplicate.
- **Numbers must be worked.** A doc that cites a number without
  showing the calculation fails the reader.
- **The reader must be able to DO it.** If the doc's objective isn't
  achievable from the doc alone, that's a finding.
- **Stale guidance is debt.** A dated claim without a date is worse
  than no claim.
- **The AR twin must fit Arabic readers.** Translation is not enough —
  examples, norms, and cultural references must fit the audience.

## The meta-rule

Improvement is not the same as making the doc shorter. A doc that is
long because the topic is deep is a good doc. A doc that is long
because content is misplaced, duplicated, or poorly organized is a doc
that needs work. The fix for misplacement is relocation. The fix for
duplication is merging. The fix for poor organization is reordering and
navigation. The fix is never "delete the explanation."
