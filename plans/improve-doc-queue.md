# Improve-doc campaign — PLAN v2 (2026-08-21)

Supersedes v1. v1's center of gravity was mechanical hygiene; v2's center of gravity is
**valuable content addition under a credibility regime**. Mechanical work is now just
Phase A of every pass. Governing mechanism: `plans/credibility.md`.

## Pass template (every doc, all five phases)

**Phase A — Mechanical sweep.** Profile (`doc-profile.py --classes`), de-number § refs
via maps/<doc>.json WANT ids (both twins, incl. prettier-split closers and bare-textual
refs), corruption scan (nested `<a><a>`, stray tags, `</a\n>` closers), empty map after.

**Phase B — Deep diagnosis.** FULL read (no profiling shortcuts — v71 lesson). Classify
Diátaxis type. Score against insight tests (veteran / cost-of-ignorance / action-change)
and R1–R20 registry. Record reader-visible symptoms, not vibes. Honest N/A verdicts are
allowed and must be justified in the ledger (v75 precedent).

**Phase C — Value authoring.** Minimum TWO substantive additions unless diagnosis proves
fewer suffice. Menu: leverage map (R14), failure diagnostics w/ mechanisms (R15),
decision points + defaults (R18), calibration numbers (R19), war story + causal chain
(R20), worked micro-example (R8/R13). Template blocks (markers/vocab/teacher) are
hygiene, not additions — they don't count toward the two.

**Phase D — Provenance.** Tier every added claim (T1/T2/T3 per plans/credibility.md).
T1 → live-verify against primary source + cite. T2 → recompute. T3 → hedge in text.
Ledger rows in rules-compliance.md new-claims audit. Volatile facts: doc-text or live
scrape only.

**Phase E — Twin sync + gates.** AR mirror (direct patches; splice for structural).
verify-twins.py ALL GATES PASSED + parse integrity both twins. Compliance row (4-status
R-notation + new-claims rows) → commit `Checkpoint vN:` + tag.

## Queue

| # | Doc | Why it's here | State |
|---|-----|---------------|-------|
| 1 | **api-design** | Carried from v1 (#10 untouched) | pending |
| 2 | **react-2024-and-beyond depth-delta** | v68 ran pre-correction: full de-number + corruption repair done, but content diagnosis was template-era. Re-run Phases B–D only | pending |
| 3 | **observability-and-operations** | 87 numerals (worst on shelf); neighbor of system-design | pending |
| 4 | **income-stream-landscape** | Thinnest doc measured (156w/sec) | pending |
| 5+ | Remaining shelf by thin-score | From batch profile table | queued |

## Already complete (do NOT redo)

- Passes 1–2 deep (v60–67) · react-2024 mechanical (v68) · across-stacks (v69)
- prequel light-by-design (v70) · ui-ux REDO verified benchmark-grade (v75)
- how-developers-think deep (v72) · testing-and-debugging deep (v76)
- system-design deep + full twin reconciliation (v77)

## Standing rules

- Two-review rule for twin divergence: unique gems mirror INTO EN first, then prune/translate.
- Recorded ratio/h3 exceptions = terminal states; never pad to gates.
- Work-copy hygiene: never cp over a work copy mid-pass.
- Never commit `Archive/What's missing.txt`.
