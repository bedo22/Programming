# maps/ — per-doc twin hygiene configuration

Project data, not code. The mechanics live in the global skill
(`~/.agents/skills/translate-to-arabic/scripts/twin-pipeline.py`); this directory
holds only the per-doc facts: which legacy §-token maps to which anchor id, and
which fold-exceptions apply.

## Schema

```json
{
  "WANT":  { "3b": "sec-migration-paths-…", ... },   // canonical §-number → section id
  "FOLDS": [ ["old exact string", "new exact string"], ... ]   // optional
}
```

- **WANT keys** are canonical numbers (ASCII digits, optional suffix letter
  a–f). The pipeline canonicalizes AR tokens (`§٥ب` → `5b`) via its global ARF
  maps before lookup. Values must be ids that **exist in the EN doc** — the
  pipeline asserts this on unmapped tokens; the repo-side rule is: verify every
  id before committing the map.
- **FOLDS** are the ONLY hand-edited hygiene artifact. Each entry must match at
  least one twin (the pipeline asserts). Use them to merge a §-token into an
  existing anchor (`…</a> §5b` → `…§5b</a>`) or to turn a bare cross-doc
  reference into a real link.
- Cross-doc entries that point at a doc whose twin/anchor does not exist yet
  are **not** map entries — they stay plain pending refs in the docs and get
  resolved when the target doc is touched (see PROGRESS.md).

## Status (v18)

| doc | WANT | FOLDS | notes |
|---|---|---|---|
| what-is-state-prequel | 7 | – | class-to-hooks 9c/10b links live in the doc, pending containers (T2) |
| ui-ux-web-design | 2 | – | 8b map key covers the AR-lettered h2 residue scoped to final-pass hygiene |
| design-thinking | 6 | – | system-design §4 link in doc, pending container (T2) |
| api-design | 9 | – | |
| html-and-css | 8 | 2 | UI/UX §9 fold — both twins |
| how-developers-think-frontend | 21 | 6 | EN+AR variants of 2 folds |