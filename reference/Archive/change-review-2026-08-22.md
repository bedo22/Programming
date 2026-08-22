# Change Review — 2026-08-22

**Change set:** Checkpoints v79–v95 — PLAN v4 Track A+B passes on api-design (pilot), how-developers-think-frontend (v80), software-testing-and-debugging (v81), system-design (v88–89, Track A only), react-2024-and-beyond (v90), observability-and-operations (v91–92); Wave 1.5 key harvest (v86–89a); income-stream reclassification (v93); problem-solving seed fetch (v94). Audited for correct application of skill `improve-doc` v1.4/1.5 doctrine.

**Gate (Mode 3):** PASS — independently re-run during this review, not taken from logs:
- `digest-coverage.py` ×6 → all exit 0 (advisory short-shell flags on system-design/react/observability, accepted per goal.md)
- `verify-twins.py` ×6 → ALL PASSED (single flag: hdt ratio 1.14 = recorded exception)
- stray § refs: 0 in observability twins (de-numbering claim verified by grep)

## What changed
- **api-design (v79):** 12-seed digestion, 10 deltas both twins, dead CAP cite replaced with Gilbert&Lynch; G13 stat †-marked after 3 hunts.
- **how-developers-think-frontend (v80):** 5 deltas verified in commit diff — chunk mechanism (hdt-Δ3), risk-ranked checklist (Boehm transfer), Agile-manifesto org-scale argument, Mercury→shuttle IID lineage, XP/C3-1996 attribution; AR mirrored (+14 lines).
- **software-testing-and-debugging (v81):** Δ1 pyramid origin (Cohn/Fowler/Vocke), Δ2 unit definitional fuzziness, Δ3 SRE error-budget definition; matching source keys exist for each.
- **system-design (v88–89):** Track A only, honestly marked 🔶; Parnas key grounded from OCR'd typeset mirror after scan dead-end; Brewer/Lamport keys with provenance labels; G13 verified-unverifiable across 5 hunts → † stands.
- **react-2024-and-beyond (v90):** compiler delta (two verbatim announcement quotes) EN+AR; dead PPR cite repaired to React Labs Mar 2023 post; 16-section matrix.
- **observability-and-operations (v91–92):** 174 refs de-numbered, 41 nested-anchor repairs, obs-Δ1 USE + obs-Δ2 symptoms-vs-causes mirrored EN+AR; codeascraft JS-wall substituted by SRE postmortem chapter (documented).
- **problem-solving (v94):** seeds only — correctly NOT marked complete.

## What the change introduced
- **Finding A (minor, react):** digest shell's "Content authored" lists three items, but v90's diff contains one authored delta (+ one cite repair). The foundation-governance and signals sentences pre-existed and were *verified* against fetched seeds (Track A sweep), not authored. The ledger row is accurate; only the digest wording overstates.
- **Finding B (borderline, react):** Track B landed ONE substantive addition against the plan's two-addition floor; dispositions mark R14 SKIP + everything else =pre without an explicit benchmark-grade N/A diagnosis. Defensible if =pre claims hold at benchmark density, but strictly short of the floor as recorded.
- Open gaps honestly tracked: G-r1 (CVE unfetched), G-r2, G-ob5…G-ob13; hdt ratio density audit pending.

## Fact consistency (duplication lens on touched facts)
- React compiler quotes ("works on both React and React Native…", "battle tested on major apps at Meta") → VERIFIED VERBATIM against live react.dev fetch this review.
- USE method ("for every resource, check utilization, saturation, errors") → VERIFIED against live brendangregg.com/usemethod.com fetch.
- Blameless-postmortem grounding ("tenet of SRE culture", healthcare/avionics origin) → VERIFIED against live sre.google/sre-book/postmortem-culture fetch.
- Commit history ↔ goal.md log ↔ ledger rows ↔ digest shells: three-way consistent for every claimed checkpoint.

## Regressions / leftovers
- None broken. Deferred items are tracked, not dropped: pending gap fetches above; hdt density audit; system-design Track B; problem-solving digest+matrix+Track B (seeds warm in /tmp/digest-sources/ps — snapshot-loss risk, same class Wave 1.5 already addressed once).

## Addendum — seven-content-type disposition audit (same day)

User-directed deepening: are the seven insight types (R14–R20) actually present at benchmark density behind the `=pre` dispositions? Method went beyond literal phrase greps (brittle across HTML) to parsed `<table>` header shapes per doc.

| Type | api-design | hdt | testing | react | observability |
|---|---|---|---|---|---|
| R14 Leverage map (master-first tiers) | **ABSENT** | **ABSENT** | **ABSENT** | **ABSENT** | **ABSENT** |
| R15 Failure diagnostics | ✅ T19 symptom→why | ✅ section | ✅ T15 Failure→Why→Fix | ✅ T7 mode→fix | ✅ T-section |
| R16 Search vocabulary | ⚠️ only T1 "Confused with" disambiguation | ✅ dedicated vocabulary-map section | ⚠️ thin | ⚠️ thin | ✅ rich |
| R17 Inversions | ⚠️ light | ✅ marker | ✅ T2 Before/After table | ⚠️ light | ✅ T2 Before/After table |
| R18 Decision points + defaults | ✅✅ T7/T8/T10/T11/T14/T17 "Use when / When you reach for it" | ✅ default-posture language | ✅ T6 "When it earns its keep", T7 doubles Good use/Common abuse | ✅ T5 "Reach for / Be careful" | ✅ decision metrics |
| R19 Calibration numbers | ✅ 22 tables | ✅ WCAG/debounce | ✅ error-budget arithmetic | ✅ | ✅ burn-rate arithmetic |
| R20 War stories w/ mechanism | ✅ RPC→GraphQL history + worked example | ✅ NASA→React history | ✅ worked example unit→production | ⚠️ history only | ✅ checkout incident (labeled) |

**Finding C (systemic):** R14 leverage maps are missing from ALL five completed docs, while every ledger SKIP justification conflates R14 with R15 ("failure-modes table carries *diagnostic* function" — that is not master-first practice tiers). Either the type is genuinely inapplicable per doc (needs saying, per plan's SKIP rules) or the shelf-wide value pass under-delivered its headline content type.
**Finding D (ledger integrity):** `api-design` — the ✅v79 pilot — has NO row in `rules-compliance.md`; `git log -S` shows no commit ever added one, and v79 did not touch the ledger. Plan step B6 mandates the row (seven-disposition table included). The pilot's dispositions exist nowhere auditable.
**Correction to interim observations:** earlier zero-grep alarms on R18/R16 were partly pattern brittleness; header-level parsing shows R18 strongly present shelf-wide.

## Verdict
The improve-doc doctrine was applied substantively, not cosmetically: gates pass when re-run cold, deltas are real mechanism-bearing content present in both twins, quotes attributed to primary sources check out verbatim under live fetch, and honest terminal states (†, JS-wall substitutions, recorded exceptions) were used instead of padding. Two bookkeeping-level corrections would tighten it: fix the react digest's "authored" wording to "verified" for the two pre-existing sentences, and either land a second addition or record an explicit justification for the one-addition Track B there.
