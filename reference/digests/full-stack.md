# full-stack — source digestion shell

Status: TRACK A COMPLETE (2026-08-22), 3 unique cited URLs reconciled per v1.7 currency conventions.
Thin-but-honest ledger: one practitioner essay, one platform doc, one standards-body cheat
sheet. The doc's substance is doc-native teaching about the client/server seam; the cites
anchor its sync patterns, validation rule, and hard-problem naming.

## Cited-URL reconciliation (coverage gate requirement)

| cited URL | status | source-dated |
|---|---|---|
| https://martinfowler.com/bliki/TwoHardThings.html | practitioner canon — Fowler bliki; names cache invalidation among the two hard things (naming the problem this doc's §4 sync mechanisms solve) | living blog |
| https://tanstack.com/query/latest | platform canon — TanStack Query docs; optimistic/invalidate/refetch as implemented practice (path itself pins rolling latest) | continuously updated |
| https://owasp.org/www-community/controls/Input_Validation_Cheat_Sheet | standards body — OWASP Input Validation Cheat Sheet; "validate on the server, always" enforcement behind §7 | continuously updated (community-revised sheet, not version-dated) |

## Coverage matrix

| doc section | covered by | note |
|---|---|---|
| #sec-how-to-use-this-doc | n/a navigation | exempt |
| #sec-definition-what-full-stack-thinking-is-and-what-it-is-not | doc-native teaching + cited canon (see ledger) | eternal |
| #sec-history-the-boundary-keeps-moving | doc-native era teaching; LAMP/SPA/RSC moves are settled history, current drift hedged | dated-once · eternal for settled history |
| #sec-the-full-request-journey-the-frame-everything-hangs-on | doc-native frame + cited canon (see ledger) | eternal mechanism; named frameworks volatile→hedged |
| #sec-where-does-this-belong-the-central-question | doc-native decision table (Thing × Client/Server/Database with stated defaults) | R18 function · eternal defaults |
| #sec-state-across-the-boundary-who-owns-what-and-how-the-copies-sync | TanStack Query canon + doc-native sync taxonomy | volatile→hedged (library API surface) |
| #sec-the-three-shapes-of-data-same-thing-three-forms | doc-native teaching (source data / client cache / UI state) | eternal |
| #sec-tracing-and-testing-across-the-boundary | doc-native practice (contract/E2E ownership) | eternal |
| #sec-the-security-seam-the-client-is-untrusted | OWASP Input Validation canon + doc-native invariant | eternal principle · volatile→hedged (sheet revisions) |
| #sec-worked-example-tracing-one-feature-across-the-seam | illustrative walkthrough (labeled add-to-cart trace) | R20 worked-example · eternal |
| #sec-most-common-failure-modes-the-seam-anti-patterns | traces to confirmed sections + OWASP enforcement row | R15 support · eternal anti-patterns |
| #sec-principles | doc-native principle/why frames — the doc's practice-mass concentration | R14 leverage · authored framework · eternal |
| #sec-summary-the-complete-mental-checklist | derives from confirmed sections | inherits classes |
| #sec-primary-sources | the reconciliation ledger above | mirrors cited-canon statuses |
| #sec-ask-your-teacher | doc-native teaching prompts derived from confirmed sections | inherits classes |

## Gaps

| id | claim/area | hunts | status |
|---|---|---|---|
| G-fs11 | TanStack Query cite pins rolling `/latest`; exact invalidate/refetch signatures drift per release | doc deliberately teaches optimistic/invalidate/refetch as patterns, not syntax, and defers to live docs | convention-tier hedge |
| G-fs21 | OWASP cheat sheet is community-revised continuously; specific validation techniques move | doc anchors to the stable invariant ("validate on the server, always"), not sheet specifics | convention-tier hedge |
| G-fs31 | vocabulary layer (R16): no search-vocabulary block in this doc | cross-discipline terms of art owned shelf-wide by `reference/ar/glossary.html` | convention-tier hedge — glossary owns coinage |

## Content authored from this digestion

- Track B row: justified N/A this pass — rich authored doc delegating facts to cited canon
  (Fowler TwoHardThings, TanStack Query, OWASP Input Validation); recorded per SHELF-DONE
  rule (additions OR justified N/A). HTML docs untouched.
