# Source digest — Lamport, 1978 (Time, Clocks, and the Ordering of Events)

## Identity
- **Full citation:** Lamport, L. (1978). "Time, Clocks, and the Ordering of Events in a Distributed System." *Communications of the ACM*, 21(7), 558–565.
- **Verified link:** https://lamport.azurewebsites.net/pubs/time-clocks.pdf
- **Open-access link:** same (author-hosted PDF)
- **First verified:** 2026-08-21 · **Last checked:** 2026-08-21

## What the doc(s) claim from this source
- api-design Theory table: idempotency/dedup rests on causal ordering — grounded in the happened-before relation.
- system-design event rows: ordering guarantees require explicit partition keys.

## Key findings (one line each, with supporting quote)
- **PDF fetched (8pp)** — happened-before partial order, logical clocks, total ordering via tie-breaks are the paper's three moves. [Deep distillation pending — PDF not yet text-extracted; treat section-level quotes as pending.]

## Notes / caveats
- **Does NOT support:** wall-clock timestamps as ordering truth anywhere in API/event design.

## Verification history
- 2026-08-21: ok (PDF fetched; deep read pending)
