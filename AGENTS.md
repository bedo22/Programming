# Teaching shelf — project constitution

Static HTML teaching shelf. English docs in `reference/<topic>.html`, Arabic RTL twins in
`reference/ar/<topic>.html`, shared assets in `assets/` (`lesson.css`, `lesson.js`).

## Governing skills

- `reference-doc` — builds new EN doc + AR twin from scratch (house template, spine order, verification).
- `translate-to-arabic` — syncs stale twins / translates EN-only docs (modes auto-detected). Read it before touching any doc.
- `scrape` — fetch real pages when research needs live sources.

## Arabic hygiene tooling (v18+) — locked, not re-derived

The hygiene mechanics have ONE implementation, in the global skill:

- `~/.agents/skills/translate-to-arabic/scripts/twin-pipeline.py <en> <ar> <N> --map maps/<doc>.json`
  (run from `reference/`) — strip numerals → positional id-pass → folds → §-remap → change report.
- `~/.agents/skills/translate-to-arabic/scripts/verify-twins.py <doc-stem>` (repo root) — the gate
  battery: h2/h3/pre balance, visible-h2 parity, ids identical in twins, numeral-free, zero stray §,
  internal + cross-doc anchors resolve, lang-switch lines, AR/EN ratio (band 0.75–0.97, canonical
  measure; out-of-band ratios FLAG with recorded exceptions in the script).
- Per-doc config (WANT map, FOLDS exceptions) is project data in `maps/<doc>.json`; the ONLY
  hand-edited hygiene artifact is a fold, and it lives there. Every WANT id must exist in the EN
  doc; folds must be applied before protection.
- The failure history and rules are in the skill's `conventions.md` — new hygiene shapes are fixed
  THERE (script + ledger), never in one-off /tmp scripts. New shelves bootstrap from the skill's
  `project-snippet.md`.

**Never re-implement the pipeline or the battery in a session.**

## Schema rules (non-negotiable)

- **No section numerals, ever.** Headings are positional; the spine order is the only ordering scheme. Legacy numerals (`5b.`, `٥ب.`) and `§`-references are being removed shelf-wide — de-numbering happens when a doc is touched.
- **Every `<h2>` carries `id="sec-<kebab>"`** — ASCII, unique per file, **identical in both twins** (language-neutral anchors). Phantom `<h2>`s inside `<pre>` code samples get NO ids and are never deleted.
- **Cross-references are anchor links only**: in-doc `#sec-…`, sibling `./name.html#sec-…`. No `§13a`, no numeric pointer of any kind.
- **Language-switch lines**: EN headers carry `./ar/<name>.html (العربية)`; AR headers carry `../<name>.html (English)`.
- **Terminology**: the ONLY coinage source is `reference/ar/glossary.html` (`<dfn>` elements). Term absent → stop and report. Never invent.
- AR twins: `lang="ar" dir="rtl"`, asset paths `../../assets/…`, headings mirror EN 1:1 (translated), h2 **visible** count parity (strip `<pre>` blocks before counting — phantom h2s mask real drift), AR/EN char ratio band ≈ 0.75–0.97 — **calibrated on the three AR-OK twins at v12** (cs-and-se 0.75, react-2024-and-beyond 0.84, glossary 0.97). The earlier 0.55–0.7 band came from one anomalous outlier (version-control 0.36 — a terse 20/21 twin that is now 0.40 by canonical measure). The canonical measure is the verify script's; exceptions are recorded there (version-control 0.40, how-developers 1.17, cs-and-se 0.98, glossary 0.99, problem-solving 0.70).

## Project state

The Arabic overhaul plan lives in `PROGRESS.md` — tiers, per-doc status, gates, checkpoint tags.
Commit convention: `Checkpoint vN: <summary>`, tagged `vN`. Gates must pass before every commit.