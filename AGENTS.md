# Teaching shelf — project constitution

Static HTML teaching shelf. English docs in `reference/<topic>.html`, Arabic RTL twins in
`reference/ar/<topic>.html`, shared assets in `assets/` (`lesson.css`, `lesson.js`).

## Governing skills

- `reference-doc` — builds new EN doc + AR twin from scratch (house template, spine order, verification).
- `translate-to-arabic` — syncs stale twins / translates EN-only docs (modes auto-detected). Read it before touching any doc.
- `scrape` — fetch real pages when research needs live sources.

## Schema rules (non-negotiable)

- **No section numerals, ever.** Headings are positional; the spine order is the only ordering scheme. Legacy numerals (`5b.`, `٥ب.`) and `§`-references are being removed shelf-wide — de-numbering happens when a doc is touched.
- **Every `<h2>` carries `id="sec-<kebab>"`** — ASCII, unique per file, **identical in both twins** (language-neutral anchors). Phantom `<h2>`s inside `<pre>` code samples get NO ids and are never deleted.
- **Cross-references are anchor links only**: in-doc `#sec-…`, sibling `./name.html#sec-…`. No `§13a`, no numeric pointer of any kind.
- **Language-switch lines**: EN headers carry `./ar/<name>.html (العربية)`; AR headers carry `../<name>.html (English)`.
- **Terminology**: the ONLY coinage source is `reference/ar/glossary.html` (`<dfn>` elements). Term absent → stop and report. Never invent.
- AR twins: `lang="ar" dir="rtl"`, asset paths `../../assets/…`, headings mirror EN 1:1 (translated), h2 **visible** count parity (strip `<pre>` blocks before counting — phantom h2s mask real drift), AR/EN char ratio band ≈ 0.55–0.7.

## Project state

The Arabic overhaul plan lives in `PROGRESS.md` — tiers, per-doc status, gates, checkpoint tags.
Commit convention: `Checkpoint vN: <summary>`, tagged `vN`. Gates must pass before every commit.