# Plan — build the `improve-doc` skill (modular router architecture)

**Prototype:** `reference/Archive/doc-improvement-rules.md` (18.9 KB, unversioned)
**Approved:** name `improve-doc`; architecture must match the major-skill pattern in
`~/.agents/skills/` (anti-ui-slop, hallmark, ui-design): **SKILL.md is a thin router,
details live in reference modules inside the skill, own scripts, fully self-contained.**
**Motivation (user):** shelf-review / translate-to-arabic accumulated shelf-specific
clutter and aren't generalized. improve-doc must be **general in its router base** and
**thoroughly comprehensive in its reference modules**, so it's easy to improve and
iterate in isolation.

---

## 0. The exemplar pattern (extracted from anti-ui-slop + hallmark)

| Property | How the exemplars do it |
|---|---|
| Router | SKILL.md 51–58 lines (anti-ui-slop); description routes, body never teaches doctrine |
| Loading discipline | "Load at most one matching module from `reference/`"; explicit *do-not-load* rules |
| Modules | Need-shaped, self-contained files (`product.md`, `brand.md`, `polish.md`, `distill.md`…); hallmark scales to 106 files in categorized subdirs (`genres/`, `themes/`, `verbs/`) |
| Self-containment | All doctrine travels with the skill; no dependency on repo docs for method |
| Change tracking | `MODIFICATIONS.md` + metadata version (`uizze-version: quiet-expert-v5`) |
| Scripts | Only for deterministic operations |

---

## 1. Findings on the prototype (unchanged — these drive module content)

**F1** Explanations-vs-concepts rule triplicated verbatim (Phase 4 ×2, meta-rule ×1),
already diverging. → one canonical copy in the directives module.
**F2** No version/changelog → redo rule unenforceable. → MODIFICATIONS.md + ledger.
**F3** Local 8-step spine conflicts with AGENTS.md's fixed spine (all 41 docs follow
the constitution; verified via h2 ids). → delete local spine; defer.
**F4** § policy weaker than constitution ("headings only"); CS doc carries ~127 visible
§-refs that pass the battery but violate AGENTS.md. → de-number-on-touch directive.
**F5** Restates shelf-review material (~80% overlap in pre-work questions; private
duplication wording vs the skill's taxonomy/verdicts). → contract, not restatement.
**F6** Missing pipeline machinery (splice-sections, WANT maps, folds); its reorder
instructions would cause hand-splicing, which AGENTS.md forbids. → integration module.
**F7** No learning-science self-check devices (objective↔assessment, retrieval design,
two tiers, scaffold summary). → gaps module check.
**F8** Slogans without procedures (stale guidance, cultural fit, numbers worked). →
procedural hooks in gaps/verify modules.
**F9** Contradictions: callout budget (CS has 9, PS 12 vs "one per section max";
callouts defined as both "insight" and "theory"); `<details>` boundary undefined;
arbitrary ~1500-line TOC threshold; generic nav vs actual nav system.
**F10** Blind spots: `.dd-figure` conventions, ratio-ledger etiquette (never pad),
glossary `<dfn>` coinage gate, commit discipline.
**F11** No trigger surface (why it sat unused). → description owns apply-verbs;
review-verbs route to shelf-review.
**F12** ~350 lines intermixed — wrong shape for a router. → the split below.

---

## 2. Skill tree

```
~/.agents/skills/improve-doc/
├── SKILL.md                      # router, ≤80 lines: directives + module table
├── MODIFICATIONS.md              # changelog (exemplar convention)
├── reference/
│   ├── directives.md             # P1–P6 prime directives, full text (F1 canonical copy)
│   ├── understand.md             # build the worksheet BEFORE touching (8 questions)
│   ├── narrative.md              # arc analysis, bad-narrative signs, reorder procedure
│   ├── gaps.md                   # missing why/theory/boundaries/questions/depth/
│   │                             #   transfer/connections + R-id checks (F7, F8)
│   ├── boundaries.md             # duplication taxonomy, ownership, pointer-crafting
│   ├── design.md                 # nav, visual hierarchy, details-boundary, callouts (F9)
│   ├── apply.md                  # risk-ordered operations + locale-twin sync procedure
│   ├── verify.md                 # gate checklist, R-id registry (F2's mechanical redo)
│   └── integration.md            # THE ONLY shelf-specific module (see §4)
├── scripts/
│   └── doc-profile.py            # deterministic doc inventory (see §5)
└── examples/
    └── worked-example.md         # problem-solving refactor, method-level only
```

---

## 3. The router (SKILL.md shape)

Frontmatter: name, description (apply-verb triggers, ≤1024 chars, review-verbs
explicitly deferred to shelf-review), `metadata: improve-doc-version: 1.0`.

Body sections, mirroring anti-ui-slop's rhetoric:

1. **Prime directives** — six one-liners, always in context (full text in
   `reference/directives.md`):
   - No deletion. Relocate or merge; only true duplication goes.
   - The why is never optional (What/How/Why equality).
   - Never point where you haven't merged explanations.
   - Every locale twin syncs through its pipeline — never hand-edited.
   - The host repo's schema doc outranks this skill.
   - One doc at a time.
2. **Workflow loop** — understand → diagnose → load modules → apply → verify. State
   that `understand.md` is mandatory before any edit; `apply.md` + `verify.md` are
   mandatory whenever files change.
3. **Module table** — "Load only the modules matching the diagnosis":

| Need | Module |
|---|---|
| First contact with the doc | `understand.md` |
| Sections feel out of order / no arc | `narrative.md` |
| Doc feels shallow / reader can't DO it | `gaps.md` |
| Content overlaps sibling docs | `boundaries.md` |
| Navigation / hierarchy / formatting | `design.md` |
| Changing files (always) | `apply.md` |
| Before declaring done (always) | `verify.md` |
| Working in a repo with twin/locale pipeline | `integration.md` |

4. **Do-not rules** (exemplar-style): don't load every module; don't run audits
   (shelf-review's job); don't create new docs; don't collapse explanatory prose in
   `<details>`; don't pad translations to hit metrics.

---

## 4. Generalization strategy — the clutter question

The user's complaint: existing skills carry shelf-specific debt. The fix is **layering,
not omission**:

- **Doctrine modules (general):** directives, understand, narrative, gaps, boundaries,
  design, apply, verify — written repo-agnostically ("locale twin", "host schema doc",
  "improvement ledger") so they work on any doc set in any repo.
- **`integration.md` (isolated specifics):** everything about THIS shelf in one file —
  AGENTS.md deference points (spine, ids, § de-numbering), translate-to-arabic tool
  table (twin-pipeline / splice-sections / WANT maps / folds / battery), ratio-ledger
  etiquette, `.dd-figure` conventions, glossary `<dfn>` coinage gate, commit
  discipline (Checkpoint vN, PROGRESS.md row, Archive exclusions). The router loads it
  only when the host repo has those conventions. When the shelf's mechanics change,
  exactly one module edits — the clutter can't leak into the doctrine.
- **Repo-owned state stays out of the skill:** the compliance ledger lives in the host
  repo (`reference/Archive/rules-compliance.md` here); the skill merely instructs
  "append a row if the host keeps an improvement ledger".

---

## 5. Script: `scripts/doc-profile.py`

One deterministic profiler (write-a-skill rule: scripts only for deterministic ops),
replacing the grep-sprawl every session currently re-derives:

```
python3 doc-profile.py <doc.html> [--json]
```

Output: h2/h3 id list + counts, per-section word counts, tables/pre/callout/recap
counts, visible §-refs outside `<pre>` (with locations), internal + cross-doc anchor
inventory, presence of taught devices (worked example, summary checklist, self-check
questions, scope line), lang/dir attributes. `--json` for machine use.

This is deliberately general (any HTML doc), feeds `understand.md` and `verify.md`,
and becomes the one place shelf-aware lint rules (§ counting) live as flags rather
than prose.

---

## 6. Build steps

1. Scaffold the tree; write `MODIFICATIONS.md` (v1.0 entry: promoted from prototype).
2. Write `directives.md` — merge F1's tripled rule into the canonical copy here.
3. Port prototype Phases 1–3 → `understand.md` / `narrative.md` / `gaps.md`,
   generalizing vocabulary, adding R-ids (stable check identifiers; new check = new id =
   ledger rows lacking it are due for re-check — F2 made mechanical), adding F7/F8 hooks.
4. Port Phase 4 → `boundaries.md` using shelf-review's taxonomy by name (contract, F5).
5. Port Phase 5 → `design.md`, resolving F9's contradictions (callout taxonomy split
   from budget; details boundary defined; h2/table-count TOC trigger).
6. Write `apply.md` (risk-ordered ops, twin-sync decision table) and `verify.md`
   (gate checklist + R-id registry).
7. Write `integration.md` (all F3/F4/F6/F10 shelf specifics in one place).
8. Write `doc-profile.py` + test on cs-and-software-engineering and problem-solving.
9. Write SKILL.md router + description; smoke-test in pi (loads clean, no conflicts,
   description ≤1024).
10. Pilot on problem-solving (audit already half-done this session); fill first two
    ledger rows; then retire the prototype (stub pointing at the skill).

---

## 7. Acceptance criteria

1. Loads in pi with zero conflict warnings; apply-verbs route here, review-verbs to
   shelf-review.
2. SKILL.md ≤80 lines; no doctrine in the router; every module self-contained.
3. Grep for shelf-specific tokens (pipeline names, AGENTS.md, glossary, Checkpoint)
   across `reference/*.md`: hits ONLY in `integration.md`.
4. Exactly one canonical copy of the explanations-rule; zero restatement of
   shelf-review criteria (named references only).
5. Every apply step names its tool; no step hand-edits twin HTML.
6. Every slogan has an R-id or module hook; R-ids stable and registered in verify.md.
7. `doc-profile.py` runs on both pilot docs without error; output matches manual greps.
8. Ledger exists in the host repo; pilot fills rows citing version + R-ids.
