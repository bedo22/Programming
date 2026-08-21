# Goal
Finish this plan Plan: improve-doc campaign — 10 docs (passes 1–10)                                                                                                                                           

 ### A. Standard pass procedure (applied to every doc, in this order)

 1. Profile with doc-profile.py --classes teacher,recap + batch flags (thin w/sec, numerals, missing devices). Record the deficiency fingerprint before reading.
 2. Read the doc in full (understand.md worksheet: purpose, audience, objective, ownership, prerequisites, theory, mental model, boundaries) + classify Diátaxis type.
 3. Diagnose → select modules; record findings as reader-visible symptoms with R-id citations.
 4. De-numbering sweep: build the numeral→named-link replacement from maps/<doc>.json WANT ids + h2 titles (EN names from EN titles, Arabic names from AR titles); handle malformed residuals
    manually; empty WANT/FOLDS afterward.
 5. Additive content set (only what the diagnosis justifies): audience/currency markers (R11/R12), leverage map section (R14), search-vocabulary details block (R16), calibration numbers
    where qualitative claims lack magnitudes (R19), teacher device if missing (R9).
 6. AR twin sync: prose patches direct on twin; any structural insert via splice-sections.py on a work copy; never cp over a work copy mid-pass (v61 lesson).
 7. Gates: verify-twins.py <stem> (now incl. visible-h3 parity) + profiler parse-integrity on both twins. Recorded ratio exceptions are terminal states.
 8. Ledger row in reference/Archive/rules-compliance.md using the 4-status notation (id / id=pre / id→doc / id=N/A(type)); tick the queue checkbox in plans/improve-doc-queue.md.
 9. Commit Checkpoint vN: <summary> + tag vN. Never commit Archive/What's missing.txt.

 ### B. The queue (measured fingerprints → planned change sets)

 ┌────┬───────────────────────────────────┬──────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ #  │ Doc                               │ Fingerprint                  │ Specific work beyond standard set                                                                                │
 ├────┼───────────────────────────────────┼──────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
 │ 1  │ javascript-the-language           │ ✅ v62 done                  │ —                                                                                                                │
 ├────┼───────────────────────────────────┼──────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
 │ 2  │ class-to-hooks-paradigm-shift (in │ 59 numerals, no              │ De-number from WANT (21 keys incl. subsection forms §9c/§10b/§13f); fix malformed "appears in §§6–12" markup;    │
 │    │ progress)                         │ markers/teacher/vocab, 35    │ leverage map (T1 useState/useEffect/rules-of-hooks/keys · T2 useReducer/Context/memoization/custom hooks · T3    │
 │    │                                   │ sections                     │ Suspense/use/transitions/RSC); vocabulary block (HOC, render props, reconciliation, hydration…); teacher device. │
 │    │                                   │                              │ Skip catalog collapse this pass — structural churn too high alongside de-numbering; logged as design follow-up   │
 ├────┼───────────────────────────────────┼──────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
 │ 3  │ react-2024-and-beyond             │ 46 numerals, 261w/sec,       │ Same set; check sibling overlap with #2 (boundaries.md pass — pointer audit both directions)                     │
 │    │                                   │ PROGRESS.md debt list member │                                                                                                                  │
 ├────┼───────────────────────────────────┼──────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
 │ 4  │ javascript-across-stacks          │ 30 numerals, open catalogs   │ Standard set + collapse clearly lookup-shaped catalogs into <details> (design.md boundary rules)                 │
 ├────┼───────────────────────────────────┼──────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
 │ 5  │ what-is-state-prequel             │ recently reworked; verify    │ Lighter pass: markers + vocabulary only if diagnosis confirms; don't invent gaps                                 │
 │    │                                   │ first                        │                                                                                                                  │
 ├────┼───────────────────────────────────┼──────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
 │ 6  │ ui-ux-web-design                  │ AR h2s still numbered        │ Standard set + AR-side numeral strip via pipeline                                                                │
 │    │                                   │ (PROGRESS.md debt)           │                                                                                                                  │
 ├────┼───────────────────────────────────┼──────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
 │ 7  │ how-developers-think-frontend     │ passed most device checks    │ Verify-first pass: markers, vocabulary, leverage map only where flat                                             │
 ├────┼───────────────────────────────────┼──────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
 │ 8  │ software-testing-and-debugging    │ 240w/sec, 18 numerals        │ Standard set; failure-modes table likely already strong (=pre for R15)                                           │
 ├────┼───────────────────────────────────┼──────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
 │ 9  │ system-design                     │ architecture anchor          │ Standard set; leverage map especially valuable here (flat 28-section doc)                                        │
 ├────┼───────────────────────────────────┼──────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
 │ 10 │ api-design                        │ contracts tier               │ Standard set                                                                                                     │
 └────┴───────────────────────────────────┴──────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

 ### C. Cross-cutting items carried from pass 1

 - h3-parity gate is live — expect it to surface more pre-existing twin asymmetries; each one gets the P3 treatment (merge unique content to the lacking twin, never delete).
 - Parse-integrity gate runs on every doc; any unescaped raw-text tags found get escaped in the same checkpoint.
 - Catalog collapsing (<details> for lookup-shaped sections) is deliberately deferred to a dedicated design pass after the 10 content passes — mixing structural churn with content passes
   doubles twin-sync risk.
 - Batch-2 candidates logged: income-stream-landscape (156w/sec, worst thin score), observability-and-operations (87 numerals!), angular-evolution, beyond-the-browser, full-stack, glossary,
   frontend-camps-survey.

 ### D. Feedback loop

 Each pass ends with a defect note: anything the tooling missed or made hard goes into the skill (script fix / module edit / MODIFICATIONS entry) before the next pass starts — so
 improvements compound instead of repeating manual workarounds.

## Progress log
(append one line per step)
- 2026-08-21: v68 — pass 3/10 react-2024-and-beyond ✅: de-numbered 61 refs, repaired 12 nested-anchor folds + 2 base64-corrupted folds (both twins), markers/vocabulary/teacher added; gates all green, ratio 0.85.
- 2026-08-21: v69 — pass 4/10 javascript-across-stacks ✅: 54 refs de-numbered both twins, markers/vocabulary/teacher added; h3-parity gate caught missing AR 'other backend lanes' section → translated + inserted (22/22); gates green ratio 0.77.
- 2026-08-21: v60–v67 — passes 1–2 complete (javascript-the-language, class-to-hooks incl. uniqueness audit/prune/full AR reconciliation); skill hardened mid-campaign (h3-parity gate, parse-integrity gate, bilingual markers, ledger notation).
