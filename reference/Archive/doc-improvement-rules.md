# Doc Improvement Rules

Lessons from refactoring problem-solving.html and algorithms-and-data-structures.html.
Apply these when improving any shelf doc.

## The non-negotiable rule

**No content or explanation deletion.** Only true duplication may be removed.
If a doc feels too long, the fix is better navigation, not less content.

## When content is in the wrong doc

If content teaches *technique* (templates, code, data structures, paradigms)
but lives in a doc that teaches *thinking*, move it to the technique doc.
Leave a pointer in the original:

```html
<p>
  This doc stops at <em>choosing</em> the technique. The companion —
  <a href="./target-doc.html#sec-anchor">Target Doc — Section Name</a>
  — is where the technique becomes a working template with code and edge cases.
  One shelf doc per question: this is the thinking, that is the toolkit it
  reaches for.
</p>
```

The content stays on the shelf. It's just in the doc that teaches it.

## When sections overlap within a doc

If two sections cover the same failure mode, trap, or concept (like "Einstellung"
appearing in both a "failure modes" table and an "emotional regulation" table),
merge them into one section. Keep every unique row from both. Remove only the
rows that are true duplicates.

## Navigation for long docs (>2000 lines)

### Sticky TOC

Add a `<nav class="doc-toc">` after the recap section, before the first
substantive content. Style it sticky so it stays visible while scrolling.

```html
<nav class="doc-toc" style="position: sticky; top: 0; z-index: 10;
  background: var(--bg, #fff); border-bottom: 1px solid #ddd;
  padding: 0.5rem 1rem; margin-bottom: 1rem; font-size: 0.9rem;">
  <details open>
    <summary style="cursor: pointer; font-weight: bold;">Jump to section</summary>
    <ul style="columns: 2; column-gap: 2rem; list-style: none;
      padding: 0.5rem 0 0 0; margin: 0;">
      <li><a href="#sec-anchor">Section Name</a></li>
      <!-- one <li> per h2 -->
    </ul>
  </details>
</nav>
```

### Quick-reference lookup bar

For methodology docs (like problem-solving), add a compact lookup bar that
answers "what are the core moves?" in 5 seconds. Place it between the recap
and the TOC.

### Details toggles for reference subsections

Wrap long tables, checklists, and catalogs in `<details><summary>` so they're
present but collapsed. The reader expands when they need the detail.

Good candidates for `<details>`:
- Constraint checklists
- Complexity budgets
- Edge case catalogs
- Verification strategy tables
- Tooling/ecosystem catalogs
- History tables (when placed after the method, not before)

**Always preserve the `id` attribute on h2/h3 tags inside `<details><summary>`:**

```html
<details>
  <summary><h2 id="sec-my-section" style="display: inline;">Section Title</h2></summary>
  <!-- content -->
</details>
```

If the id is lost, cross-references and the verify script will fail.

## AR twin sync

Every structural change to the EN doc must be mirrored in the AR twin:
- Added TOC → add Arabic TOC with translated section names
- Added lookup bar → add Arabic lookup bar
- Added details toggles → add same toggles to AR
- Merged sections → merge in AR too
- Moved content → replace with Arabic pointer in AR

Run `verify-twins.py` after every sync. Check h2 parity, id symmetry, and
anchor resolution.

## What NOT to do

- **Don't reorder sections** unless the benefit is clear and the risk is low.
  Reordering breaks cross-references and is hard to verify. The sticky TOC
  solves navigation without reordering.
- **Don't compress explanations** for brevity. If an explanation helps
  clarity, it stays.
- **Don't remove history/theory sections** even if they "slow the narrative."
  Move them later in the doc or wrap in `<details>`, but don't cut them.
- **Don't create new docs** for questions already answered (even partially)
  in an existing doc. Expand the existing doc instead.

## Verification checklist

After every doc improvement:
1. `grep -c '<h2'` EN and AR — must match (h2 parity)
2. All `id` attributes on h2/h3 tags are present and unique
3. All internal `#sec-*` anchors resolve
4. All cross-doc anchors resolve (note: verify script has a `./` prefix limitation)
5. No stray `§` numerals in headings
6. EN→AR and AR→EN lang-switch links present
7. `verify-twins.py` passes (except known limitations)
