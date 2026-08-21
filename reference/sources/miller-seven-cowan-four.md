# Source digest — Miller, 1956 (The Magical Number Seven) + Cowan, 2001 (~4 chunks)

> The two working-memory citations behind how-developers-think-frontend's claim that
> you cannot hold data shape, component tree, and event flow in mind at once.
> Together they establish both the classic capacity figure and its modern correction.

## Identity

- **Full citation:** Miller, G. A. (1956). "The Magical Number Seven, Plus or Minus Two: Some Limits on Our Capacity for Processing Information." *Psychological Review*, 63(2), 81–97. — and — Cowan, N. (2001). "The magical number 4 in short-term memory." *Behavioral and Brain Sciences*, 24(1), 87–114.
- **DOI:** Miller via APA; Cowan 10.1017/S0140525X01003922
- **Verified link:** https://en.wikipedia.org/wiki/The_Magical_Number_Seven,_Plus_or_Minus_Two · https://en.wikipedia.org/wiki/Working_memory
- **Open-access link:** Cowan 2001 is free on PMC; Miller widely mirrored
- **First verified:** 2026-08-21
- **Last checked:** 2026-08-21

## What the doc(s) claim from this source

- how-developers-think-frontend, Underlying theory: "Working memory is severely limited (Miller 1956: ~7±2 items; Cowan 2001: ~4). You cannot simultaneously hold the data shape (Model), the component tree (View), and the event flow (Flow) in working memory while also writing code."
- how-developers-think-frontend, Principles: chunking and progressive disclosure as cognitive-load levers.

## Key findings (one line each, with supporting quote)

- **Capacity is measured in chunks, not bits or items** — "Miller concluded that memory span is not limited in terms of bits but rather in terms of chunks."
- **A chunk is knowledge-dependent** — "A chunk is the largest meaningful unit in the presented material that the person recognizes—thus, what counts as a chunk depends on the knowledge of the person being tested." This is the mechanism behind expert fluency: experts have bigger chunks.
- **The modern estimate is ~4, not 7** — Cowan's review revised working-memory capacity down to about four chunks in adult humans.

## Key quotes (with locations)

> "memory span is not limited in terms of bits but rather in terms of chunks" — Wikipedia summary of Miller's conclusion.

> "~4" as adult chunk capacity — Cowan 2001 headline finding.

## Notes / caveats

- **Does NOT support:** a literal "7 things" design rule for UI (Miller's own point is
  that the number is an artifact of the chunking assumption); that capacity limits are
  the ONLY reason to cycle Model/View/Flow (the loop also manages extraneous load).
- The 7±2 figure applies to immediate serial recall of unfamiliar material — not to
  skilled recognition tasks where chunking has already compressed the content.

## Related digests

- fielding-rest.md — no relation; listed because api-design consumes different theory.
- (pending) sweller-cognitive-load — the load-theory companion citation.

## Verification history

- 2026-08-21: ok (both Wikipedia summaries fetched; primary DOIs recorded; chunk-definition quote re-grepped from fetched copy)
