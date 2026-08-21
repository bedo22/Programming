# Source-Digestion Workflow — shelf-wide content grounding

Status: ACTIVE (2026-08-21). Answers: "how do we ensure content isn't fabricated?"
Method: every doc gets real sources covering its content; those sources are digested
into first-class artifacts; docs reference their own digestion; valuable additions are
authored FROM the digestion, never from memory. This is the diataxis.md pattern
(scrape every core page, then write) applied to the whole shelf. NO COMMITS until user allows.

## Per-doc pipeline

1. **Seed**: harvest the doc's existing `.cite` section — the author already declared
   what the doc is built on.
2. **Fetch**: download every seed source live (`curl` / scrape skill). Raw snapshots
   kept under `/tmp/digest-sources/<stem>/` during the pass (not committed).
   Dead/moved links get recorded as defects and repaired in the doc.
3. **Digest**: write `reference/digests/<stem>.md` — a structured reading of the
   sources ONLY: per-source summary of what it actually establishes, mapped to the
   doc's sections that lean on it. No memory-authored "facts" enter here; anything not
   in a fetched source is marked `[unverified — needs source]`.
4. **Reference back**: the doc's cite section gains a line:
   "Working digests: <a href="../digests/<stem>.md">source digestion</a>" (EN + AR twin,
   AR path `../../digests/`).
5. **Author from the digestion**: Phase-C value content (leverage maps, failure
   diagnostics, calibration, war stories w/ mechanism) is written with the digestion
   open; each addition traceable to a digest entry. Illustrative examples labeled.
6. **Gates + ledger** as in PLAN v2 Phases D–E.

## Digest format (fixed)

```
# <stem> — source digestion
Sources fetched: <date>; list with URLs + fetch status
## <Source name> (<url>)
- Establishes: …
- Maps to doc sections: #sec-…
- Corrections/tensions found: …
## Gaps the sources don't cover  → candidate content OR explicit N/A
## Content authored from this digestion  (added in pass vX)
```

## Order

Queue order from PLAN v2 stands; each pass now starts with steps 1–4 above.
Pilot: api-design.
