# Source digest — Fielding, 2000 (REST, ch.5 of dissertation)

> "Representational State Transfer (REST)" — the chapter that DERIVED the Web's
> architecture by adding constraints one at a time and naming the properties each
> induces. This is the boundary-test source behind api-design's REST rows: what
> REST actually claims versus what "RESTish" APIs practice.

## Identity

- **Full citation:** Fielding, R. T. (2000). *Architectural Styles and the Design of Network-based Software Architectures*. Doctoral dissertation, University of California, Irvine — Chapter 5: "Representational State Transfer (REST)".
- **DOI:** none (dissertation)
- **Verified link:** https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm
- **Open-access link:** same (author-hosted, free)
- **First verified:** 2026-08-21
- **Last checked:** 2026-08-21

## What the doc(s) claim from this source

- api-design, History table ("2000 / Roy Fielding's dissertation — REST"): "Six constraints: client-server, stateless, cacheable, uniform interface, layered system, code-on-demand." — confirmed; note CoD is the one constraint Fielding marks optional.
- api-design, Theory table (HATEOAS row): hypermedia as discoverability constraint; doc adds "rarely fully implemented" — a deviation from Fielding, recorded as tension below.
- api-design, Evolution table (REST+JSON row): HTTP semantics + JSON + URL versioning as the pragmatic package — synthesis, not Fielding's own claim.

## Key findings (one line each, with supporting quote)

- **REST is derived, not described** — each constraint is added to null-style and its induced properties named; the derivation method itself is transferable to contract design. Supported by §5.1: "By examining the impact of each constraint as it is added to the evolving style, we can identify the properties induced by the Web's constraints."
- **Statelessness is a trade, not a free win** — induces visibility, reliability, and scalability, at the cost of "increasing the repetitive data (per-interaction overhead) sent in a series of requests" (§5.1.3).
- **Code-on-demand is optional** — "REST allows client functionality to be downloaded… these extensions only improve the extensibility" but the style works without them (§5.1.7).
- **Uniform interface has four sub-constraints** — identification of resources; manipulation through representations; self-descriptive messages; HATEOAS (§5.2.1.1–5.2.1.2).

## Key quotes (with locations)

> "The central feature that distinguishes the REST architectural style from other network-based styles is its emphasis on a uniform interface between components" — §5.1.5.

> "HATEOAS … A REST API should be entered with no prior knowledge beyond the initial URI" — paraphrase of §5.1.5/Hypermedia discussion; treat as paraphrase unless quote re-verified.

## Notes / caveats

- **Does NOT support:** "REST = any JSON over HTTP." The dissertation's REST includes
  hypermedia and self-descriptive messages; production "Level 2" APIs are REST-derived
  by Richardson's model, not REST per se.
- Fielding later (2008 blog comment) complained about REST being misused for Level-2
  APIs — the doc's pragmatic framing is Richardson/Fowler's, not Fielding's.
- Chapter is prose-heavy; the constraint table in §5.5.1 ("REST Application Program
  Interface") is not present in this chapter fetch — do not cite section numbers
  without re-checking.

## Related digests

- richardson-maturity-model.md — the step-model that grades REST adherence (Fowler 2010).
- rfc9457.md — error-envelope spec orthogonal to REST style.
- miller-seven.md — cognitive grounding used by how-developers-think-frontend.

## Verification history

- 2026-08-21: ok (HTTP 200; full chapter text fetched to /tmp/digest-sources/api-design/; quotes above re-grepped from fetched copy)
