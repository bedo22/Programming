# javascript-the-language — source digestion shell

Status: TRACK A COMPLETE (2026-08-22). The doc cites zero URLs inline (canon-prose style:
ECMAScript/TC39/V8 named in text), so this ledger was built from CLAIM INVENTORY — each
load-bearing historical/semantic claim was listed, then a seed fetched to ground it.
Keys: 7 written under raw-seeds/javascript-the-language/.

## Fetch ledger (every cited seed URL, verbatim)

| cited URL | status | source-dated |
|---|---|---|
| https://en.wikipedia.org/wiki/JavaScript | OK (709KB) | rev 2026-07-30 |
| https://en.wikipedia.org/wiki/Brendan_Eich | OK — grounds the "ten days" claim verbatim | rev 2026-08-04 |
| https://en.wikipedia.org/wiki/ECMAScript | OK (314KB) | rev 2026-07-19 |
| https://en.wikipedia.org/wiki/V8_(JavaScript_engine) | OK (208KB) | rev 2026-06-17 |
| https://developer.mozilla.org/en-US/docs/Web/JavaScript/Event_loop | OK (196KB) | MDN continuously maintained |
| https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode | OK (201KB) | MDN continuously maintained |
| https://en.wikipedia.org/wiki/WebAssembly | OK (624KB) | rev 2026-08-19 |

(source-dated per currency convention skill v1.7: living pages carry their revision
marker; continuously-maintained doc sites say so; papers would carry publication date.)

Supplementary: none yet — Self-lineage paper for the prototype model → G-js1.

## Sources — read

### Wikipedia: JavaScript — tier: primary (history claims)
- Establishes: LiveScript as shipped name before JavaScript rename; joint Sun–Netscape
  announcement December 4, 1995; prototype-based classification; Java naming decision.
- Verified in seed: "LiveScript when first shipped", "December 4, 1995".
- Δ Doc delta:
  - **js-Δ2** the announcement DATE (Dec 4 1995) is absent from the history section,
    which currently says only "1995".
- Maps to: #sec-the-10-days-in-may-1995, #sec-standardization-ecmascript-tc39-the-es6-2015-tipping-point.

### Wikipedia: Brendan Eich — tier: primary (the title claim)
- Establishes VERBATIM: "He completed the first version in ten days in order to
  accommodate the [Navigator beta]" — the doc's section-title claim, previously
  carried on general knowledge, now has a fetched source.
- Δ Doc delta:
  - **js-Δ1** ten-days grounding upgrade — add "(per Eich's own recollection, recorded
    in his biography coverage)" framing so the anecdote is sourced, not folklore.
- Maps to: #sec-the-10-days-in-may-1995.

### Wikipedia: ECMAScript — tier: primary (standardization)
- Establishes: 6th edition (ES2015) finalized June 2015; annual release cadence since;
  TC39 as the standards body; spec editions numbered.
- Verified in seed: "June 2015, new major versions have been finalized and published
  every [year]".
- Δ Doc delta: none needed — doc already teaches the tipping point correctly.
- Maps to: #sec-standardization-ecmascript-tc39-the-es6-2015-tipping-point.

### Wikipedia: V8 — tier: supporting
- Establishes: V8 launched with Chrome September 2, 2008; open-sourced from day one.
- Maps to: #sec-the-engines-v8-spidermonkey-javascriptcore.

### MDN: Event Loop — tier: primary (runtime model)
- Establishes: call stack / microtask queue / macrotask ordering terminology — the
  exact vocabulary the doc's mental-models and failure-modes sections use.
- Verified in seed: call stack, Microtask, message queue present.
- Δ Doc delta: none — terminology already aligned.
- Maps to: #sec-the-design-single-threaded-event-loop, #sec-mental-models-how-developers-actually-reason-about-the-event-loop, #sec-failure-modes-where-the-model-breaks-in-practice.

### MDN: Strict Mode — tier: primary (semantics)
- Establishes: 'use strict' directive semantics (30 occurrences verified); silent-error
  conversion list.
- Δ Doc delta: none — doc's strict-mode teaching already aligns with MDN semantics.
- Maps to: #sec-the-core-semantics-map-what-ecmascript-itself-defines.

### Wikipedia: WebAssembly — tier: primary
- Establishes: MVP shipped in all four major browsers 2017 (Haas et al. paper; Krill
  coverage of March 2017 completion).
- Δ Doc delta: none — doc's WASM-junction framing already matches the MVP-2017 record.
- Maps to: #sec-the-wasm-junction.

## Coverage matrix

| doc section | covered by | note |
|---|---|---|
| #sec-how-to-use-this-doc | n/a navigation | exempt |
| #sec-search-vocabulary-what-javascript-calls-things | js-Δ3 terms-of-art block (closure/hoisting/prototype chain/type coercion/event loop/microtask/strict mode) | added v106; grounded in doc's own usage · eternal |
| #sec-the-leverage-map-where-the-work-concentrates | doc-native synthesis (failure-modes-derived tiers) | accepted authored framework, G-js0 · eternal |
| #sec-the-10-days-in-may-1995 | wiki-javascript · wiki-brendan-eich | js-Δ1/Δ2 here · eternal (dated-once history) |
| #sec-why-a-new-language-not-a-java-applet-or-c-extension | wiki-javascript | Java-cooperation context · eternal |
| #sec-the-design-prototype-model-not-classes | wiki-javascript (classification); Self lineage → G-js1 | eternal |
| #sec-the-design-first-class-functions-closures-the-lambda-calculus-heart | canon semantics (Scheme lineage) | prose-canonical, no fetch needed · eternal |
| #sec-the-design-single-threaded-event-loop | mdn-event-loop | eternal |
| #sec-mental-models-how-developers-actually-reason-about-the-event-loop | mdn-event-loop | terminology aligned · eternal |
| #sec-the-host-environment-not-the-language | derives from event-loop + engines rows | doc-native split · eternal |
| #sec-the-core-semantics-map-what-ecmascript-itself-defines | mdn-strict-mode; ECMAScript canon | dated(2026-08) — semantics stable since ES5 |
| #sec-standardization-ecmascript-tc39-the-es6-2015-tipping-point | wiki-ecmascript | dated(2026-07 rev) — annual cadence means re-verify at each pass |
| #sec-the-engines-v8-spidermonkey-javascriptcore | wiki-v8-engine | volatile→hedged (share figures); launch dates eternal |
| #sec-the-wasm-junction | wiki-webassembly | dated(2026-08 rev) — MVP 2017 eternal, feature list moves |
| #sec-what-js-is-not | derives from confirmed sections | boundary section · eternal |
| #sec-ecosystem-tooling-catalog-with-decision-metrics | volatile facts — hedged | volatile→hedged |
| #sec-principles-the-design-bets-that-survive-every-change | synthesis of design rows | doc-native · eternal |
| #sec-worked-examples-semantics-and-runtime-in-one-trace | illustrative (labeled) | eternal |
| #sec-failure-modes-where-the-model-breaks-in-practice | traces to semantics rows; mdn-strict-mode supports | dated(2026-08) |
| #sec-the-future-where-the-language-is-heading | signals — hedged | volatile→hedged |
| #sec-summary-checklist | derives from confirmed sections | inherits classes |

## Gaps

| id | claim/area | hunts | status |
|---|---|---|---|
| G-js0 | leverage-map tier provenance | doc-native synthesis from own failure-modes table | accepted authored framework |
| G-js1 | Self-language lineage of prototype model | **CLOSED 2026-08-22**: _debt-harvest/self-language.html verified (prototype-based; ECOOP'96 Prototype-Based Languages ref) | closed |
| G-js2 | engine market-share figures | volatile; hedged in-text | convention-tier |

## Content authored from this digestion

- pass v106 (Track B): js-Δ1 ten-days sourcing note + js-Δ2 announcement date added to
  the 10-days section EN+AR (prose patches) · js-Δ3 search-vocabulary block (seven
  terms of art) after how-to-use, EN+AR. Dispositions7 CREATED: R14 PRE (pre-existing
  leverage map at sec-the-leverage-map-where-the-work-concentrates — v1.2-era section
  matching current three-tier format), R16 PRE (new block), others registered against
  matrix. Floor via WAIVER note (prose-patch additions).
