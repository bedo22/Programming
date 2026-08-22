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

- **The changeability criterion, verbatim** — "There are a number of design decisions
  which are questionable and likely to change under many circumstances," followed by
  his list: input format, the decision to keep all lines in core, character-packing
  choices.
- **Decomposition goals stated** — modules should allow work "with little need for
  communication"; "product flexibility—it should be possible to make drastic changes
  to one module without a need to change others"; "comprehensibility—it should be
  possible to study the system one module at a time."
- **The efficiency cost is admitted** — the unconventional (information-hiding)
  decomposition, "if implemented with the conventional assumption that a module
  consists of one or more subroutines, will be less efficient in most cases."
  Parnas trades runtime efficiency for changeability — the paper's honest cost line.

## Source note

Typeset copy located and fully extracted (colostate mirror, 27K chars) replacing the
scan-hosted copy; original scan retained at win.tue.nl for provenance.

## Notes / caveats

- **Does NOT support:** "hide everything" readings — Parnas's criterion selects WHICH
  decisions to hide (the ones likely to change); decomposition by flow is his explicit
  contrast case.

## Related digests

- fowler-microservices-article.md · c4-model-brown.md

## Verification history

- 2026-08-22: upgraded — typeset colostate mirror found via web search, fully extracted; quotes above verbatim from extraction
