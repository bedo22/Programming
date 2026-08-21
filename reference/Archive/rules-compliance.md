# Doc improvement compliance ledger

One row per improved doc. Cites the skill version and the R-ids satisfied or
deferred (registry: `~/.agents/skills/improve-doc/reference/verify.md`).
A row lacking an id introduced after its date is **due for re-check**.

| Doc | Skill version | Date | Gates | R-ids satisfied | Deferred |
|---|---|---|---|---|---|
| html-and-css (+AR twin) | improve-doc v1.2 | 2026-08-21 | ALL GATES PASSED, ratio 0.81; repaired v61 (AR patches lost to work-copy overwrite, re-applied + h3-parity gate added) | R4 R10 R11 R12 R14 R15=pre R16 R18=pre R19 | R17 partial (inversions implicit in mental-models table); R20=N/A(explanation-type: teacher questions carry war stories) |
| javascript-the-language (+AR twin) | improve-doc v1.2 | 2026-08-21 | ALL GATES PASSED, ratio 0.86 | R9(teacher device) R11 R12 R14 R16 R19 | R15=pre (failure-modes table) R17=pre (four-wrong-models table is inversion content) R20=N/A(explanation-type; teacher Q1 elicits war stories) |
| class-to-hooks-paradigm-shift (+AR twin) | improve-doc v1.2 | 2026-08-21 | ALL GATES PASSED (h3 parity = recorded legacy divergence, SYNC pending); ratio 1.32 exception | R9 R11 R12 R14 R15=pre(failure-modes+classic-bugs tables) R16 R17=pre(capture-vs-mutate + stale-closure inversions) R18=pre(decision tables throughout) | R20=N/A(explanation-type); h3 reconciliation → translate-to-arabic SYNC queue |
