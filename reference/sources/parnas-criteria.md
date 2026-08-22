# Source digest — Parnas, 1972 (On the Criteria To Be Used in Decomposing Systems into Modules)

> The origin of information hiding as THE decomposition criterion: modules should be
> split by difficult/change-relevant design decisions, not by execution flow.

## Identity

- **Full citation:** Parnas, D. L. (1972). "On the Criteria To Be Used in Decomposing Systems into Modules." *Communications of the ACM*, 15(12), 1053–1058.
- **DOI:** 10.1145/361598.361623
- **Verified link:** https://www.win.tue.nl/~wstomv/edu/2ip30/references/criteria_for_modularization.pdf
- **Open-access link:** same (university-hosted copy)
- **First verified:** 2026-08-22 · **Last checked:** 2026-08-22

## What the doc(s) claim from this source

- system-design History table: "Modules should hide design decisions likely to change. The origin of 'encapsulation' as architectural principle." — matches canonical reading.
- system-design Theory table (Information Hiding row): "Not 'hide data' — hide the reason for the data structure."

## Key findings (one line each, with supporting quote)

- [OCR PENDING] — the hosted copy is scan-quality (pdf-inspector: all 6 pages need OCR,
  zero extractable text). Thesis statements above rest on the canonical summary until
  OCR or a typeset copy is obtained. Do NOT quote page numbers.

## Notes / caveats

- **Does NOT support:** "hide everything" readings — Parnas's criterion selects WHICH
  decisions to hide (the ones likely to change); decomposition by flow is his explicit
  contrast case.

## Related digests

- fowler-microservices-article.md · c4-model-brown.md

## Verification history

- 2026-08-22: partial (PDF fetch ok; scan-quality, OCR pending)
