# Doc Improvement Rules

How to improve any shelf doc. Derived from the problem-solving.html
refactoring and informed by the shelf-review skill's criteria model,
guards, and pattern library.

## The non-negotiable rule

**No content or explanation deletion.** Only true duplication may be removed.
If a doc feels too long, the fix is better navigation, not less content.
If content teaches the wrong thing in the wrong doc, move it — don't delete it.

## The organizing principle

Every shelf doc teaches three things, and they are equally important:

1. **What** — the facts, definitions, structures, vocabulary
2. **How** — the methods, techniques, patterns, workflows
3. **Why** — the reasons, causes, mechanisms, theory that make the
   what and how *transferable*

A doc that teaches what and how but not why produces practitioners who
can follow rules but cannot adapt when conditions change. A doc that
teaches why but not how produces theorists who cannot act. The goal is
both: understanding that enables action, and action that deepens
understanding.

**The "why" is not depth added after the fact.** It is the connective
tissue that turns isolated rules into a mental model. When a reader
understands *why* DRY matters (divergence causes bugs), they don't need
to remember the rule — they can derive it. When a reader understands
*why* working memory is limited (Miller 1956, Cowan 2001), they don't
need to be told to write plans down — they reach for pen and paper
because they understand the constraint.

**Check every doc:** does the reader finish knowing *why* the method
works, not just *what* the method is?

## Phase 1 — Understand the doc before changing it

Every doc has a purpose, an audience, and a scope. Read the doc fully
before touching it. Record:

1. **What question does this doc answer?** (the one-line purpose)
2. **Who is it for?** (the audience, reading level)
3. **What should the reader be able to DO after reading?** (the objective)
4. **What does this doc own vs defer?** (the ownership map — which facts
   are exclusive to this doc, which are shared with neighbors)
5. **What prior knowledge does it assume?** (the prerequisites)
6. **What theory underpins the method?** (the causal chain: why does
   this approach work? What cognitive science, historical evidence, or
   domain logic supports it?)
7. **What mental model does this doc give the reader?** (the internal
   representation they'll carry away — not the rules, but the framework
   for deriving rules. "Trade-offs are everywhere" is a mental model.
   "Use DRY" is a rule.)
8. **What boundary conditions does each technique have?** (when does it
   work, when does it fail, what assumptions does it make?)

If you can't answer these eight, you don't understand the doc well enough
to improve it.

## Phase 2 — Analyse the narrative

### The narrative arc

A good shelf doc has a narrative arc, not just a list of sections. The
arc weaves what, how, and why together:

```
Hook (why this matters — the stakes)
→ Foundation (what it is — definitions, vocabulary)
→ Method (how to do it — the core technique)
→ Why it works (the theory — cognitive science, historical evidence,
  domain logic that makes the method trustworthy)
→ Practice (how to apply it — worked examples, edge cases)
→ Judgment (when to adapt — trade-offs, context-dependence)
→ Reference (lookup — tables, catalogs, checklists)
→ Close (so what — what changes for the reader)
```

The key insight: **theory is not a separate section at the end.** It
interleaves with the method. After introducing a technique, explain *why*
it works. After showing an example, explain *why* that example is
representative. The "why" follows the "what" and "how" immediately,
not five sections later.

Map the doc's current sections to this arc. Ask:

- **Does each section build on the previous?** Or do sections jump around?
- **Is the core method introduced early?** Or buried after history?
- **Is the "why" proximate to the "what"?** Or is theory separated from
  the practice it supports?
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

- **Theory divorced from method.** A history section that's interesting
  but doesn't explain *why* the method works. History for its own sake
  is trivia; history that shows *why this approach survived* is theory.
  If the history section doesn't connect to the method's validity, it's
  in the wrong place or missing its "why."
- **Method without "why."** A technique presented as "do X" with no
  explanation of why X works. This produces recipe-followers. Every
  technique should have a causal chain: "do X *because* Y."
- **Reference material mixed with narrative.** Paradigm tables, data
  structure catalogs, tooling lists — these are lookups, not teaching.
  Either collapse them in `<details>` or move them to the owning doc.
- **No progression.** Sections that could be in any order. The reader
  gains nothing from reading section 7 before section 3. Fix by establishing
  dependencies: "section X assumes you read section Y."
- **Duplicated framing.** Two sections that open with the same "why this
  matters" paragraph. Merge the openings.

### What makes narrative good

- **The "why" is proximate.** After introducing a concept, the explanation
  of why it works follows immediately. The reader never has to wait
  five sections for the justification.
- **Theory earns its place.** Every theoretical section connects back to
  a practical implication. "Working memory is limited" → "therefore write
  plans down." "The Einstellung effect exists" → "therefore check your
  approach periodically." Theory that doesn't connect to practice is
  trivia; theory that changes behavior is knowledge.
- **Examples embody the theory.** A worked example isn't just a
  demonstration — it's a proof that the theory works in practice. The
  best examples show *why* the method produced the result, not just
  that it did.
- **The reader can derive the rules.** After reading the "why," the
  reader should be able to reconstruct the "what" and "how" from
  first principles. If they can only follow rules but can't derive
  them, the "why" section failed.

## Phase 3 — Find the gaps

### Missing questions

Read the doc and ask: what questions does a reader naturally have that
this doc doesn't answer? Write them down. For each:

- Is the answer in another doc on the shelf? → cross-reference it
- Is the answer nowhere on the shelf? → add it here (or create a new doc)
- Is the answer implied but not stated? → state it explicitly

Pay special attention to "why" questions:
- "Why does this method work?" → needs a theoretical answer
- "Why is this better than the alternative?" → needs a comparative answer
- "Why does this fail?" → needs a causal answer
- "Why should I care?" → needs a motivational answer (the stakes)

### Missing theory — two kinds

Every method should have a supporting "why." But "why" comes in two
forms, and both are needed:

**Causal mechanism** — *why does this technique work?*
- "Use a hash map for counting" is a rule.
- "Use a hash map because O(1) lookup eliminates the nested scan" is
  knowledge. The mechanism is the "why."
- Check: does the method explain *what would go wrong without it?*
  If you can remove the technique and nothing breaks, the "why" is weak.

**Conceptual framework** — *what kind of problem is this for?*
- "Use DRY" is a rule.
- "DRY applies to knowledge duplication, not code duplication — two
  functions that look identical but serve different business rules
  should stay separate" is a framework. It tells you the *boundary*
  of the rule.
- Check: does the reader know *when this technique applies and when
  it doesn't?* If the answer is "always" or "never," the framework
  is missing.

Also check:
- **Does the method cite its evidence?** "Studies show X" without a
  citation is a claim, not knowledge. Link to the source.
- **Does the method connect to a larger framework?** "Write Input/
  Operation/Output" is a technique. "Write I/O/O because it offloads
  working memory to an external representation (Miller 1956)" is a
  technique grounded in theory. The connection makes it memorable.
- **Is the theory explained at the right level?** Not every doc needs a
  full cognitive science lecture. But every doc should have at least a
  one-sentence "why" for each major technique.

### Missing sections

Check against the house template's spine order:
1. How to use this doc (reading order, cross-links)
2. Definition (what it is, what it's not)
3. Core method (the main content)
4. Why it works (the theory — can be woven into the method, or a
   separate section if the theory is substantial)
5. Practice (how to apply it — worked examples)
6. Failure modes (what goes wrong)
7. Ecosystem (tools, resources)
8. Summary / checklist

If a doc is missing a standard section, ask whether it should have one.
Not every doc needs every section — but the absence should be deliberate.

### Missing boundary conditions

Every technique has conditions where it works and conditions where it
fails. Check:

- **Does each technique have a "when NOT to use" clause?** "Use DRY"
  is incomplete without "but not for two functions that look identical
  but represent different business rules." "Use greedy" is incomplete
  without "but prove the exchange argument first."
- **Does each technique state its assumptions?** "Use binary search"
  assumes sorted input. "Use BFS for shortest path" assumes unweighted
  edges. If the assumption isn't stated, the reader will misapply it.
- **Does each technique have a failure mode?** Not just "what goes wrong
  in general" but "what goes wrong when you apply this technique in the
  wrong context?"

### Missing transfer conditions

The ultimate test: can the reader apply this to a situation the doc
doesn't cover?

- **Does the doc teach the pattern, or just the example?** "Count word
  frequencies using a hash map" teaches an example. "Count occurrences
  of any token using a map from token to count" teaches a pattern. The
  pattern transfers; the example doesn't.
- **Does the doc give the reader a way to recognize *new* instances?**
  "This is a hash-map problem because the operation is counting" is
  recognition. "Use a hash map" is a rule. Recognition transfers;
  rules don't.
- **Does the worked example show *why* the method produced the result,
  not just *that* it did?** The reader should be able to trace the
  causal chain: "it worked because O(1) lookup eliminated the nested
  scan." If they can only say "it worked," the mental model failed.

### Missing depth

Some sections are too shallow. Signs:
- A claim without evidence ("studies show...")
- A principle without example ("decompose before solving")
- A technique without "why" ("use a hash map" — but why?)
- A table row without explanation (just a label and a link)

For each shallow section, ask: what would make this both actionable AND
understandable? Add the example AND the explanation of why the example
works.

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

When moving content, leave a pointer in the original:

```html
<p>
  This doc stops at <em>choosing</em> the technique. The companion —
  <a href="./target-doc.html#sec-anchor">Target Doc — Section Name</a>
  — is where the technique becomes a working template with code and edge
  cases. One shelf doc per question: this is the thinking, that is the
  toolkit it reaches for.
</p>
```

### Landscape awareness

Beyond ownership, check whether the reader understands the *conceptual
landscape*:

- **Does the doc place its techniques in a family?** "Hash-map counting
  is a special case of the frequency pattern" is landscape awareness.
  "Use a hash map" is an isolated rule. The family helps the reader
  recognize related techniques.
- **Does the doc show *why* one technique was chosen over another?**
  "We used DP because the sub-problems overlap" is landscape awareness.
  "Use DP" is a rule. The choice reasoning helps the reader make their
  own choices.
- **Does the doc distinguish *similar but different* techniques?**
  "D&C is for independent sub-problems; DP is for overlapping ones" is
  a conceptual boundary. Without it, the reader confuses the two.

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
  checklists, catalogs)

Note: do NOT collapse theory sections in `<details>`. Theory should
be visible and prominent, not hidden behind a toggle. Reference
material (tables, catalogs) can be collapsed; explanatory text
should not.

### Visual hierarchy

- h2 = major sections (one topic)
- h3 = subtopics within a section
- h4 = reference material within a subtopic (collapse in `<details>`)
- Tables = structured reference (clear headers, scannable rows)
- Callouts = key insights (one per section max, not every paragraph)
- Code blocks = working examples (commented, with input/output)
- Blockquote.callout = theoretical insights, key quotes, "why" explanations

### Consistency

- Same heading style as other docs (no section numerals, `id="sec-kebab"`)
- Same callout style (blockquote.callout)
- Same table format (thead + tbody, no inline styles on cells)
- Same footer structure (upstream/sibling/downstream links)

## Phase 6 — Apply changes

Order of operations (lowest risk first):

1. **Add navigation** (TOC, lookup bar, details toggles) — no content change
2. **Add missing "why"** (theory, mechanisms, evidence for existing techniques) — additive, high value
3. **Add missing content** (new sections, expanded explanations) — additive
4. **Merge overlapping sections** (dedup within doc) — removes duplication
5. **Move misplaced content** (to owning doc, leave pointer) — structural
6. **Reorder sections** (fix narrative arc) — high risk, update all refs
7. **Design improvements** (consistent formatting, visual hierarchy) — cosmetic

For each change:
- Make the change
- Verify h2 parity (EN = AR)
- Verify all anchors resolve
- Sync the AR twin (see below)
- Run verify-twins.py

**AR twin sync checklist:**
- Added TOC → add Arabic TOC with translated section names
- Added lookup bar → add Arabic lookup bar
- Added details toggles → add same toggles to AR
- Added new section → translate section and insert at matching spine slot
- Merged sections → merge in AR too
- Moved content → replace with Arabic pointer in AR
- Fixed bare §-refs in AR → link to anchors

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
11. **Every major technique has a "why"** — the reader finishes knowing
    why the method works, not just what the method is
12. **Every major technique has boundary conditions** — the reader knows
    when to use it AND when NOT to use it
13. **The doc builds a mental model, not just a rule set** — the reader
    can derive rules from the framework, not just follow them
14. **Transfer test: could the reader apply this to an uncovered case?**
    If the reader can only solve the examples shown, the doc failed

## What NOT to do

- **Don't compress explanations for brevity.** If an explanation helps
  clarity, it stays. The "why" is never optional.
- **Don't remove history/theory sections** even if they "slow the narrative."
  Move them later in the doc or interleave with the method, but don't cut.
- **Don't create new docs** for questions already answered (even partially)
  in an existing doc. Expand the existing doc instead.
- **Don't skip the AR twin.** Every structural change to EN must be mirrored.
  The verify script catches structural drift, not content drift.

## Failure modes to avoid

These come from the shelf-review guards, the problem-solving experience,
and the principle that theory and practice are equal:

- **Audit against purpose, not taste.** "I would write it differently"
  is not a finding. "The reader can't find X" is.
- **Don't sacrifice "why" for brevity.** A shorter doc that drops the
  theoretical explanation is a worse doc, not a better one. The "why"
  is what makes the method transferable. Compress the reference material,
  not the theory.
- **Don't collapse theory behind toggles.** Reference tables can be
  `<details>`; explanatory text should be visible. Theory is not optional
  reading — it's the foundation.
- **Non-destructive unless told otherwise.** Move before delete.
  Collapse before cut. Point before duplicate.
- **Numbers must be worked.** A doc that cites a number without
  showing the calculation fails the reader.
- **The reader must be able to DO it.** If the doc's objective isn't
  achievable from the doc alone, that's a finding. But "doing it" includes
  understanding *why* — blind compliance is not the goal.
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

**And specifically: the fix is never "delete the theory."** A doc that
explains *why* the method works is more valuable than a doc that only
explains *what* the method is. The "why" is what the reader carries
with them when they leave the doc — the mental model that lets them
adapt the method to new situations, recognize when it doesn't apply,
and derive new techniques from first principles. Without the "why,"
the doc is a recipe. With it, the doc is an education.
