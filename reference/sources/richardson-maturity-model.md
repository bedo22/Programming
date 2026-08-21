# Source digest — Richardson/Fowler, Richardson Maturity Model

> The step-model that grades how REST an API actually is: Level 0 (RPC over HTTP)
> → 1 (resources) → 2 (HTTP verbs + status codes) → 3 (hypermedia controls).
> This is the measuring stick api-design uses for "RESTish" pragmatism.

## Identity

- **Full citation:** Richardson, L. (model, presented 2008); Fowler, M. (2010). "Richardson Maturity Model — steps toward the glory of REST." martinfowler.com, 18 March 2010.
- **DOI:** none (web article)
- **Verified link:** https://martinfowler.com/articles/richardsonMaturityModel.html
- **Open-access link:** same
- **First verified:** 2026-08-21
- **Last checked:** 2026-08-21

## What the doc(s) claim from this source

- api-design, History table ("2005–2010"): "Richardson Maturity Model (2008) grades compliance." — confirmed with dating nuance below.
- api-design, Theory table: "Four levels: RPC over HTTP → Resources → HTTP Verbs → Hypermedia. A diagnostic, not a prescription."
- api-design, Methodologies table: "REST (Level 2–3)" as the pragmatic production standard.

## Key findings (one line each, with supporting quote)

- **The model has exactly three steps plus a baseline** — Level 0 = remote procedure
  invocation over HTTP (POX); Level 1 adds resources; Level 2 adds HTTP verbs and
  status codes; Level 3 adds hypermedia controls.
- **Level 3 is aspirational, not required** — the article's subtitle calls it "steps
  toward the glory of REST"; it describes exposure to hypermedia, not a compliance bar.
- **The web itself is the existence proof** — Fowler frames REST's credibility via the
  web working at scale ("the notion that the web is an existence proof").
- **Each level builds on the previous** — resources without verbs, verbs without
  links; the levels layer, they don't branch.

## Key quotes (with locations)

> "A model (developed by Leonard Richardson) that breaks down the principal elements of a REST approach into three steps. These introduce resources, http verbs, and hypermedia controls." — article intro.

> "steps toward the glory of REST" — subtitle.

## Notes / caveats

- **Dating nuance:** model presented by Richardson at QCon 2008; canonical write-up is
  Fowler's 2010 article. Cite both when precision matters.
- **Does NOT support:** that Level 3 is mandatory for REST (Fielding would disagree);
  that the model ranks TEAMS (it grades API designs); that Level 2 APIs are "not REST"
  (they are REST-derived pragmatics).
- The article is short and example-driven (clinic appointment service); it does not
  cover versioning, pagination, or errors.

## Related digests

- fielding-rest.md — what full REST (including Level 3's HATEOAS) claims to be.
- rfc9457.md — the error-envelope spec orthogonal to maturity level.

## Verification history

- 2026-08-21: ok (HTTP 200, full text fetched to /tmp/digest-sources/api-design/)
