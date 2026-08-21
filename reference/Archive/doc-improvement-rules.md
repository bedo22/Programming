# Doc Improvement Rules

How to improve any shelf doc. Derived from the problem-solving.html
refactoring and informed by the shelf-review skill's criteria model,
guards, and pattern library.

## The non-negotiable rule

**No content or explanation deletion.** Only true duplication may be removed.
If a doc feels too long, the fix is better navigation, not less content.
If content teaches the wrong thing in the wrong doc, move it — don't delete it.
**The "why" is never optional.** A shorter doc that drops the theoretical
explanation is a worse doc. Theory is the foundation, not optional reading.

## The organizing principle

Every shelf doc teaches three things, and they are equally important:

1. **What** — the facts, definitions, structures, vocabulary
2. **How** — the methods, techniques, patterns, workflows
3. **Why** — the reasons, causes, mechanisms, theory that make the
   what and how *transferable*

A doc that teaches what and how but not why produces practitioners who
can follow rules but cannot adapt. A doc that teaches why but not how
produces theorists who cannot act. The goal is both: understanding that
enables action, and action that deepens understanding.

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

Read the doc fully before touching it. Record:

1. **What question does this doc answer?** (the one-line purpose)
2. **Who is it for?** (the audience, reading level)
3. **What should the reader be able to DO after reading?** (the objective)
4. **What does this doc own vs defer?** (ownership map)
5. **What prior knowledge does it assume?** (prerequisites)
6. **What theory underpins the method?** (causal chain: why does this
   approach work? What cognitive science, historical evidence, or
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

A good shelf doc has a narrative arc, not just a list of sections:

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

**Theory is not a separate section at the end.** It interleaves with the
method. After introducing a technique, explain *why* it works. After
showing an example, explain *why* that example is representative.

Map the doc's current sections to this arc. Ask:

- Does each section build on the previous? Or do sections jump around?
- Is the core method introduced early? Or buried after history?
- Is the "why" proximate to the "what"? Or is theory separated from
  the practice it supports?
- Does the reader know where they are? Is there a "you are here" moment?
- Does later content reference earlier content correctly?
- Is there a clear "so what?" at the end?

### What makes narrative bad

- **Theory divorced from method.** History that doesn't explain *why the
  method survived* is trivia; history that shows *why this approach
  persisted* is theory. If the history section doesn't connect to the
  method's validity, it's missing its "why."
- **Method without "why."** A technique presented as "do X" with no
  explanation of why X works. Every technique should have a causal chain:
  "do X *because* Y."
- **Reference material mixed with narrative.** Paradigm tables, data
  structure catalogs, tooling lists — these are lookups, not teaching.
  Either collapse them in `<details>` or move them to the owning doc.
- **No progression.** Sections that could be in any order. Fix by
  establishing dependencies: "section X assumes you read section Y."
- **Duplicated framing.** Two sections that open with the same "why this
  matters" paragraph. Merge the openings.

### Reordering

Reordering improves narrative. Do it when the analysis shows sections are
out of the arc. The sticky TOC helps navigation but doesn't fix narrative.
A doc with bad section order and a good TOC is still a doc with bad section
order. Fix the order.

The risk is broken cross-references — so:
1. Map every internal cross-reference (`#sec-*` link) before reordering
2. Move sections
3. Update every cross-reference
4. Verify with `grep -c '<h2'` (h2 parity) and anchor resolution

## Phase 3 — Find the gaps

### Missing questions

Read the doc and ask: what questions does a reader naturally have that
this doc doesn't answer? For each:
- Is the answer in another doc? → cross-reference it
- Is the answer nowhere on the shelf? → add it here
- Is the answer implied but not stated? → state it explicitly

Pay special attention to "why" questions:
- "Why does this method work?" → needs a theoretical answer
- "Why is this better than the alternative?" → needs a comparative answer
- "Why does this fail?" → needs a causal answer
- "Why should I care?" → needs a motivational answer (the stakes)

### Missing theory — two kinds

**Causal mechanism** — *why does this technique work?*
- "Use a hash map for counting" is a rule.
- "Use a hash map because O(1) lookup eliminates the nested scan" is
  knowledge. The mechanism is the "why."
- Check: does the method explain *what would go wrong without it?*

**Conceptual framework** — *what kind of problem is this for?*
- "Use DRY" is a rule.
- "DRY applies to knowledge duplication, not code duplication — two
  functions that look identical but serve different business rules
  should stay separate" is a framework. It tells you the *boundary*
  of the rule.
- Check: does the reader know *when this technique applies and when
  it doesn't?*

Also check:
- Does the method cite its evidence? "Studies show X" without a citation
  is a claim, not knowledge.
- Does the method connect to a larger framework? The connection makes
  it memorable.
- Is the theory explained at the right level? Not every doc needs a
  full cognitive science lecture. But every doc should have at least a
  one-sentence "why" for each major technique.

### Missing sections

Check against the house template's spine order:
1. How to use this doc (reading order, cross-links)
2. Definition (what it is, what it's not)
3. Core method (the main content)
4. Why it works (the theory)
5. Practice (worked examples)
6. Failure modes (what goes wrong)
7. Ecosystem (tools, resources)
8. Summary / checklist

Not every doc needs every section — but the absence should be deliberate.

### Missing boundary conditions

- **Does each technique have a "when NOT to use" clause?** "Use DRY"
  is incomplete without "but not for two functions that look identical
  but represent different business rules."
- **Does each technique state its assumptions?** "Use binary search"
  assumes sorted input. If the assumption isn't stated, the reader
  will misapply it.
- **Does each technique have a failure mode?** Not just "what goes wrong
  in general" but "what goes wrong when you apply this technique in the
  wrong context?"

### Missing depth (examples, evidence, explanations)

Some sections are too shallow. Signs:
- A claim without evidence ("studies show...") — needs a citation
- A principle without example ("decompose before solving") — needs a
  concrete demonstration of the principle in action
- A technique without "why" ("use a hash map" — but why?) — already
  caught by "Missing theory" above
- A table row without explanation (just a label and a link) — the reader
  doesn't know *why* this row matters or *when* to apply it

For each shallow section, ask: what would make this both actionable AND
understandable? Add the example AND the explanation of why the example
works. The example proves the theory works in practice; the explanation
of *why* it works is what makes it transferable.

### Missing transfer conditions

The ultimate test: can the reader apply this to a situation the doc
doesn't cover?

- **Does the doc teach the pattern, or just the example?** "Count word
  frequencies using a hash map" teaches an example. "Count occurrences
  of any token using a map from token to count" teaches a pattern.
- **Does the doc give the reader a way to recognize *new* instances?**
  "This is a hash-map problem because the operation is counting" is
  recognition. "Use a hash map" is a rule. Recognition transfers; rules
  don't.
- **Does the worked example show *why* the method produced the result?**
  The reader should be able to trace the causal chain. If they can only
  say "it worked," the mental model failed.

### Missing connections

Does the doc reference its neighbors?
- **Upstream:** what feeds into it? ("Design Thinking produces the
  problem; this doc solves it")
- **Downstream:** what does it feed? ("This doc produces a verified
  solution; the dev loop implements it")
- **Sibling:** does it distinguish itself from nearby docs? ("System
  Design structures across boundaries; this doc structures within")

## Phase 4 — Check cross-doc boundaries

### Duplication detection

For every claim, table, or framework:
1. Grep the shelf for the same claim/table/framework
2. If it appears in another doc: **which doc owns this?**
3. Other doc owns it → leave a pointer, remove from this doc
4. This doc owns it → check the other doc for a pointer
5. Neither clearly owns it → pick one based on depth

**One doc owns each piece of knowledge.** The other docs reference it.

**Before replacing content with a pointer, verify the target doc has the
same EXPLANATIONS, not just the same CONCEPTS.** A concept appearing in
another doc (e.g. "feature flags exist") is not the same as the
doc's explanation (e.g. "feature flags decouple deploy from release,
but they don't undo data writes"). If the target doc lacks the
explanations, MERGE them into the target doc FIRST, then replace with
a pointer. Never replace detailed content with a pointer to a doc that
only mentions the concept in passing.

When moving content, leave a pointer:

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

- **Does the doc place its techniques in a family?** "Hash-map counting
  is a special case of the frequency pattern" is landscape awareness.
  "Use a hash map" is an isolated rule.
- **Does the doc show *why* one technique was chosen over another?**
  "We used DP because the sub-problems overlap" is landscape awareness.
- **Does the doc distinguish *similar but different* techniques?**
  "D&C is for independent sub-problems; DP is for overlapping ones" is
  a conceptual boundary.

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
- **`<details>` toggles** for long reference subsections

**Do NOT collapse theory in `<details>`.** Reference material can be
collapsed; explanatory text should be visible and prominent.

### Visual hierarchy

- h2 = major sections (one topic)
- h3 = subtopics within a section
- h4 = reference material within a subtopic (collapse in `<details>`)
- Tables = structured reference (clear headers, scannable rows)
- Callouts = key insights (one per section max)
- Code blocks = working examples (commented, with input/output)
- Blockquote.callout = theoretical insights, "why" explanations

### Consistency

- Same heading style (no section numerals, `id="sec-kebab"`)
- Same callout style (blockquote.callout)
- Same table format (thead + tbody)
- Same footer structure (upstream/sibling/downstream links)

## Phase 6 — Apply changes

Order of operations (lowest risk first):

1. **Add navigation** (TOC, lookup bar, details toggles) — no content change
2. **Add missing "why"** (theory, mechanisms, evidence) — additive, high value
3. **Add missing content** (new sections, expanded explanations) — additive
4. **Merge overlapping sections** (dedup within doc) — removes duplication
5. **Move misplaced content** (to owning doc, leave pointer) — structural
6. **Reorder sections** (fix narrative arc) — high risk, update all refs
7. **Design improvements** (formatting, visual hierarchy) — cosmetic

For each change:
- Verify h2 parity (EN = AR)
- Verify all anchors resolve
- Sync the AR twin (see below)
- Run verify-twins.py

**AR twin sync checklist:**
- Added TOC → add Arabic TOC with translated section names
- Added lookup bar → add Arabic lookup bar
- Added details toggles → add same toggles to AR
- Added new section → translate and insert at matching spine slot
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

## What NOT to do

- **Don't create new docs** for questions already answered (even partially)
  in an existing doc. Expand the existing doc instead.
- **Don't skip the AR twin.** Every structural change to EN must be mirrored.
  The verify script catches structural drift, not content drift.

## Failure modes to avoid

These come from the shelf-review guards, the problem-solving experience,
and the principle that theory and practice are equal:

- **Audit against purpose, not taste.** "I would write it differently"
  is not a finding. "The reader can't find X" is.
- **Numbers must be worked.** A doc that cites a number without showing
  the calculation fails the reader.
- **The reader must be able to DO it.** If the doc's objective isn't
  achievable from the doc alone, that's a finding. But "doing it" includes
  understanding *why* — blind compliance is not the goal.
- **Stale guidance is debt.** A dated claim without a date is worse
  than no claim.
- **The AR twin must fit Arabic readers.** Translation is not enough —
  examples, norms, and cultural references must fit the audience.

## The meta-rule

**Don't be lazy.** If you previously added only navigation to a doc and
said "the doc is already good," go back and redo the analysis with the
full rules file. A TOC fixes navigation, not content gaps. Every doc
must be analysed for: missing theory, missing boundary conditions,
duplication, misplaced content, mental models, transfer conditions.
Do one doc at a time so you don't overload your context. If you don't
have enough knowledge to fill a gap, search for it.

Improvement is not the same as making the doc shorter. A doc that is
long because the topic is deep is a good doc. A doc that is long
because content is misplaced, duplicated, or poorly organized is a doc
that needs work. The fix for misplacement is relocation. The fix for
duplication is merging. The fix for poor organization is reordering and
navigation. **The fix is never "delete the explanation."**

A doc that explains *why* the method works is more valuable than a doc
that only explains *what* the method is. The "why" is what the reader
carries with them — the mental model that lets them adapt the method to
new situations, recognize when it doesn't apply, and derive new
techniques from first principles. Without the "why," the doc is a
recipe. With it, the doc is an education.
