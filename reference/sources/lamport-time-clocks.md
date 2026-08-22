# Source digest — Lamport, 1978 (Time, Clocks, and the Ordering of Events)

## Identity
- **Full citation:** Lamport, L. (1978). "Time, Clocks, and the Ordering of Events in a Distributed System." *Communications of the ACM*, 21(7), 558–565.
- **Verified link:** https://lamport.azurewebsites.net/pubs/time-clocks.pdf (scan)
- **Open-access link:** https://www.cs.ucf.edu/courses/cop6614/fall2005/lamport.pdf (seminar deck); https://h-deb.ca/UdeS/PCP/Lamport78.pdf (annotated bilingual)
- **First verified:** 2026-08-21 · **Last checked:** 2026-08-21

## What the doc(s) claim from this source
- api-design Theory table: idempotency/dedup rests on causal ordering — grounded in the happened-before relation.
- system-design event rows: ordering guarantees require explicit partition keys.

## Key findings (one line each, with supporting quote)
- **Happened-before is a PARTIAL order** — two events can be concurrent ("what if b
  'happened before' a too?"); physical clocks cannot be perfectly synchronized, so
  ordering must come from elsewhere.
- **Logical clocks need no physical basis** — "logical clocks do not require any basis
  in physical time, just a counter" (grounded via UCF seminar deck on the paper).
- **Total ordering requires an arbitrary tie-break** — the partial order is extended
  to total by external resolution.
- Grounding status: original CACM copy is a scan (unextractable); distillation above
  grounded via fetched UCF seminar deck (English) + h-deb bilingual annotated copy;
  upgrade to paper-text quotes if a typeset CACM mirror surfaces.

## Notes / caveats
- **Does NOT support:** wall-clock timestamps as ordering truth anywhere in API/event design.

## Verification history
- 2026-08-22: upgraded — original confirmed unextractable scan; UCF deck + h-deb copies fetched and used for grounding
