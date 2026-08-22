# payments-and-commerce — source digestion shell

Status: TRACK A COMPLETE (2026-08-22). Nine cited URLs — all PSP/platform canon
(Stripe, Adyen, PayPal, Braintree docs + PCI Security Standards). Authority anchors
per house convention; fetch-on-demand. The doc's mechanics sections are doc-native
teaching grounded in those canon references.

## Cited-URL reconciliation (coverage gate requirement)

| cited URL | status | source-dated |
|---|---|---|
| https://stripe.com/docs/payments | platform canon — Payments API | continuously updated |
| https://stripe.com/docs/payments/payment-intents | platform canon — PaymentIntents lifecycle | continuously updated |
| https://stripe.com/docs/billing | platform canon — Billing/subscriptions | continuously updated |
| https://stripe.com/docs/connect | platform canon — Connect/marketplaces | continuously updated |
| https://stripe.com/docs/webhooks | platform canon — webhook delivery/reconciliation | continuously updated |
| https://docs.adyen.com/ | platform canon — Adyen alternative PSP | continuously updated |
| https://developer.paypal.com/ | platform canon — PayPal integrations | continuously updated |
| https://www.braintreepayments.com/ | platform canon — Braintree (PayPal-owned) | continuously updated |
| https://www.pcisecuritystandards.org/ | standards body — PCI DSS authority | dated(current standard version) |

## Coverage matrix

| doc section | covered by | note |
|---|---|---|
| #sec-how-to-use-this-doc | n/a navigation | exempt |
| #sec-definition-what-taking-payment-actually-is | doc-native framing; authorization/capture/settlement mechanics | eternal |
| #sec-history-how-money-learned-to-move-digitally | history — settled eras | dated-once · eternal |
| #sec-intersection-with-neighbors-the-duplication-boundaries | n/a shelf-internal | exempt |
| #sec-underlying-theory-the-invariants-of-money-in-motion | doc-native invariants (idempotency, exactness, finality) | eternal |
| #sec-mental-models-frames-for-thinking-about-payments | doc-native frames | authored framework · eternal |
| #sec-how-payments-work-the-mechanics | PaymentIntents canon + doc-native walkthrough | eternal mechanism, versions volatile→hedged |
| #sec-multi-currency-and-international-payments-money-without-borders-rules-with-borders | PSP canon + FX hedging | volatile→hedged |
| #sec-integration-patterns-where-the-code-meets-the-money | stripe docs canon rows | eternal patterns, SDKs volatile→hedged |
| #sec-subscriptions-money-that-repeats | Billing canon | volatile→hedged (plan structures) |
| #sec-marketplaces-and-splits-other-people-s-money | Connect canon | volatile→hedged |
| #sec-refunds-chargebacks-and-disputes-the-money-that-comes-back | dispute-flow canon + doc-native lifecycle | eternal process |
| #sec-pci-dss-and-compliance-the-rules-you-inherited | pcisecuritystandards.org (standards body) | dated(current DSS version) |
| #sec-fraud-the-tax-on-trust | doc-native risk framing; radar-type tools hedged | eternal principles |
| #sec-worked-example-a-small-saas-takes-its-first-payment | illustrative (labeled) | eternal |
| #sec-testing-payments-the-free-education | test-mode canon (PSP sandboxes) | continuously updated |
| #sec-reconciliation-proving-the-numbers | webhooks canon + doc-native ledger discipline | eternal practice |
| #sec-most-common-failure-modes | traces to confirmed rows | R15 support · eternal |
| #sec-ecosystem-tooling-catalog-with-decision-metrics | volatile PSP landscape — hedged | volatile→hedged |
| #sec-the-future-where-money-movement-is-going | signals — hedged | volatile→hedged |
| #sec-summary-the-complete-mental-checklist | derives from confirmed sections | inherits classes |

## Gaps

| id | claim/area | hunts | status |
|---|---|---|---|
| G-pc1 | SCA/3DS regional mandate details | region-dependent and shifting; doc already hedges to "check your PSP" | convention-tier hedge |

## Content authored from this digestion

- Track B row: justified N/A for additions this pass — the doc is already rich,
  recently reconciled at v118 (preamble demote), and its facts delegate to live PSP
  canon by design. Recorded per SHELF-DONE rule.
