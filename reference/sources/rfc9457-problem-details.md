# Source digest — RFC 9457 Problem Details for HTTP APIs

> The standard error envelope: how an HTTP API says "no" in a machine-parseable way.
> Boundary source for api-design's error contract and every validation-error example.

## Identity
- **Full citation:** Nottingham, M., Wilde, E., & Anderson, R. (2023). "RFC 9457 — Problem Details for HTTP APIs." IETF.
- **DOI:** none (RFC)
- **Verified link:** https://www.rfc-editor.org/rfc/rfc9457
- **Open-access link:** same (IETF free)
- **First verified:** 2026-08-21 · **Last checked:** 2026-08-21

## What the doc(s) claim from this source
- api-design Principles #3: errors return structured envelope `type/title/status/detail/instance` — confirmed verbatim member list.
- api-design validation-errors section: field-level extension members — confirmed allowed by spec ("extension members").
- ui-ux-web-design worked example: RFC 9457 `detail` mapped to human copy.

## Key findings (one line each, with supporting quote)
- **JSON problem details use a required media type** — `application/problem+json`; this is normative, not stylistic.
- **Five core members** — `type` (URI), `title`, `status`, `detail`, `instance`; consumers MUST NOT blindly trust `title`/`detail` for logic (they are human-oriented).
- **Extensions are first-class** — additional members (e.g. `errors[]`, `retry_after`) are permitted and consumed via `type`.
- **Obsoletes RFC 7807** — same shape, refined text.

## Key quotes (with locations)
> "Problem details are a way of carrying machine-readable details of errors in an HTTP response" — Abstract.

## Notes / caveats
- **Does NOT support:** using `type` URIs as documentation links that must resolve to human pages in all cases; treating `title` as a stable machine key (that is `type`'s job).
- Pre-2023 docs citing RFC 7807 remain technically valid but outdated.

## Related digests
- fielding-rest.md — HTTP semantics foundation.
- vocke-practical-test-pyramid.md — contract-testing angle on error shapes.

## Verification history
- 2026-08-21: ok (full RFC text fetched; member/media-type claims re-grepped)
