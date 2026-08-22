# Source digest — OpenAPI Specification 3.1

## Identity
- **Full citation:** OpenAPI Initiative (2021). "OpenAPI Specification 3.1.0."
- **Verified link:** https://spec.openapis.org/oas/v3.1.0 (mirror of cited GitHub version)
- **First verified:** 2026-08-21 · **Last checked:** 2026-08-21

## What the doc(s) claim from this source
- api-design history/theory: Schema object aligned with JSON Schema — verified: the spec states the Schema Object dialect is based on JSON Schema and "RECOMMENDED along with some additional constraints".
- api-design conventions: YAML or JSON authoring — verified ("APIs may be defined by OpenAPI documents in either YAML or JSON format").

## Key findings (one line each, with supporting quote)
- **JSON Schema is the base dialect** — Schema Object uses the JSON Schema ruleset with added constraints.
- **Webhooks/callbacks/link objects** are first-class spec objects in 3.1.

## Notes / caveats
- Full 214KB spec not line-read; structural claims above re-grepped from fetched copy.

## Related digests
- rfc9457-problem-details.md · asyncapi-spec-2-6.md

## Verification history
- 2026-08-21: ok (fetched via spec.openapis.org mirror; GitHub URL cited by doc returns identical content)
