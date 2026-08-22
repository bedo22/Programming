# Source digest — Postel, RFC 791 (Robustness Principle)

## Identity
- **Full citation:** Postel, J. (ed.) (1981). "RFC 791 — Internet Protocol." IETF.
- **Verified link:** https://www.rfc-editor.org/rfc/rfc791.txt
- **First verified:** 2026-08-21 · **Last checked:** 2026-08-21

## What the doc(s) claim from this source
- api-design Theory table: "Be liberal in what you accept, conservative in what you send" applied to schema evolution — quote VERIFIED VERBATIM in §INTRODUCTION.

## Key findings (one line each, with supporting quote)
- **The principle exists in RFC 791 itself** — "an implementation must be conservative in its sending behavior, and liberal in its receiving behavior."

## Notes / caveats
- **Does NOT support:** unlimited input leniency (modern security reading narrows it); it is about protocol implementations, not user-input validation.

## Related digests
- openapi-spec-3-1.md — schema-evolution rules where the principle is applied today.

## Verification history
- 2026-08-21: ok (quote re-grepped verbatim from fetched .txt)
