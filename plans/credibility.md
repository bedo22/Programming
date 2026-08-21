# Content Credibility Mechanism — reference shelf

Status: ACTIVE (2026-08-21). Companion to improve-doc skill v1.3 provenance rule.
Principle: trust is proportionate — spec numbers get citations, arithmetic gets shown,
conventions get hedges, volatile facts get verified live or left out. Nothing else is
required; nothing less is acceptable.

## The three tiers (every claim an edit ADDS)

| Tier | Definition | Obligation at insertion |
|---|---|---|
| **T1 spec-grade** | Fixed by a standard/spec/primary source (WCAG ratios, HTTP semantics, algorithmic complexity) | Live-verify against the primary source (curl/scrape, ~1 request); cite inline `<a>` or in the doc's existing `.cite` section |
| **T2 workable arithmetic** | Derivable from numbers already in the doc (99.9% × 30 days → 43 min) | Recompute at insertion; keep derivation trivially checkable in-text |
| **T3 labeled convention** | Industry rule of thumb (~300ms debounce, <10min PR gates) | Hedge word IN THE TEXT ("typically", "common budgets") — not just in the author's head |

**Volatile facts** (version numbers, benchmarks, market shares, release dates, "current"
tool landscapes): restate ONLY from the doc's existing text, mirror between twins, or
verify live. Never from model memory.

## The claims ledger

`reference/Archive/rules-compliance.md` → "New-claims audit" section.
Row per claim: `| claim | pass/tag | tier | source-or-derivation | verified date |`.
The ledger is the review surface: a reviewer checks the ledger, not 41 docs.

## Verification procedure

1. **At insertion (every pass)**: tier the claim → T1 live-verify + cite, T2 recompute,
   T3 hedge-check. Un-tiered added claim = gate failure (skill verify pass).
2. **On doc touch**: T1 inline links must resolve (fold into shelf-review link checks).
3. **No periodic blanket re-verification**: static teaching content about stable
   fundamentals (CAP, Fitts, ACID) doesn't rot on a months scale; the ledger makes
   spot-checks targeted instead of panicked.

## What this deliberately does NOT do

- No per-sentence citations — teaching prose stays readable; the `.cite` sections and
  inline T1 links carry the burden.
- No external fact-check service — the author IS the fact-checker, with the ledger as
  the audit trail.
- No re-litigating pre-campaign content — scope is *added* claims; legacy content gets
  corrected only when a pass touches it and finds a defect (as with nested anchors).

## Pilot run (already executed)

- WCAG AA 4.5:1/3:1 → live-verified against w3.org Understanding/contrast-minimum (2026-08-21). ✓
- SLO error budget 43 min/month → recomputed (0.001 × 43,200 min). ✓
- Debounce/suite budgets → hedge words confirmed in-text. ✓
