# nextjs-deep-dive — source digestion shell

Status: TRACK A COMPLETE (2026-08-22), 9 unique cited URLs reconciled per v1.7 currency
conventions. Canon set is small and entirely first-party: Next.js official docs + release
announcements, the Next.js repo, one Vercel AI SDK reference, and one practitioner essay
(overreacted.io). The doc's mechanics sections are doc-native teaching grounded in those
canon references; version-sensitive behavior is hedged in-doc ("always check the version").

## Cited-URL reconciliation (coverage gate requirement)

| cited URL | status | source-dated |
|---|---|---|
| https://nextjs.org/docs | platform canon — official Next.js docs root | continuously updated |
| https://nextjs.org/docs/app/build-pipeline | platform canon — build pipeline reference | continuously updated |
| https://nextjs.org/blog/next-13 | platform canon — release announcement: App Router (beta) | dated-once (release post) |
| https://nextjs.org/blog/next-14 | platform canon — release announcement: App Router + Server Actions stable | dated-once (release post) |
| https://nextjs.org/blog/next-15 | platform canon — release announcement: React 19 support, Turbopack dev stable | dated-once (release post) |
| https://github.com/vercel/next.js | platform canon — official repo (source of truth for behavior) | continuously updated |
| https://sdk.vercel.ai/docs | platform canon — Vercel AI SDK reference | continuously updated |
| https://overreacted.io/the-two-reacts/ | practitioner canon — Dan Abramov's RSC essay | living blog |
| https://api.example.com/users/${id}` | markup artifact — placeholder URL inside a `<pre>` fetch example | not a source |

## Coverage matrix

| doc section | covered by | note |
|---|---|---|
| #sec-how-to-use-this-doc | n/a navigation | exempt |
| #sec-definition-what-next-js-is-and-is-not | doc-native framing; meta-framework boundary table (what React still owns vs what Next decides) | eternal |
| #sec-history-the-10-year-line | settled timeline + release-post canon (next-13/14/15 blogs) | dated-once · eternal for settled history |
| #sec-evolution-constraint-inversions | doc-native shelf doctrine (constraint inversions) applied to Next | authored framework · eternal |
| #sec-intersection-with-neighbors-where-it-borders-other-practices | n/a shelf-internal | exempt |
| #sec-underlying-theory-the-models-next-builds-on | doc-native theory map delegating RSC model to cited canon (see ledger) | eternal |
| #sec-mental-models-six-that-cover-90-of-next-reading | doc-native frames ("Which React am I in?" et al.) | authored framework · eternal |
| #sec-pages-router-vs-app-router | doc-native comparison grounded in release canon; recognition guide, not a choice guide | volatile→hedged |
| #sec-app-router-file-conventions-the-vocabulary | platform canon (nextjs.org/docs) + doc-native vocabulary walkthrough | eternal conventions, API surface volatile→hedged |
| #sec-server-components-vs-client-components | RSC model canon (overreacted.io/the-two-reacts) + doc-native teaching | eternal mechanism, directive details volatile→hedged |
| #sec-data-fetching-patterns | patterns canon + doc-native walkthrough; fetch-cache drift hedged in-doc | volatile→hedged |
| #sec-caching-mental-model-including-cache-components | doc-native cache-layer model; Cache Components explicitly evolving, hedged to version checks | volatile→hedged |
| #sec-middleware-next-image-next-font-and-metadata | platform canon (nextjs.org/docs) rows + doc-native catalog | continuously updated, volatile→hedged |
| #sec-turbopack-and-the-build-toolchain | build-pipeline canon (nextjs.org/docs/app/build-pipeline); rollout pace hedged | volatile→hedged |
| #sec-navigation-streaming-and-ux-primitives | platform canon + doc-native primitives catalog (<Link>, streaming) | eternal primitives, API surface volatile→hedged |
| #sec-auth-env-and-security-frontend-adjacent | doc-native security framing; NEXT_PUBLIC_* invariant | eternal principle, examples volatile→hedged |
| #sec-ai-readiness-product-features-not-hype | AI SDK canon (sdk.vercel.ai/docs) + streaming mechanics doc-native | volatile→hedged |
| #sec-deployment-targets | decision table over hosting targets; hosting landscape volatile — hedged | volatile→hedged · R18 function |
| #sec-testing-in-next-js | platform canon + doc-native split-aware test strategy | volatile→hedged |
| #sec-worked-example-a-product-page-with-reviews-and-streaming | illustrative (labeled), doc-native end-to-end route | eternal as teaching artifact |
| #sec-failure-modes | traces to confirmed rows; failure diagnostics table | R15 support · eternal |
| #sec-principles | derives from confirmed sections | inherits classes |
| #sec-ecosystem-a-tooling-catalog | volatile tooling landscape — hedged | volatile→hedged |
| #sec-the-future-signals-to-watch | signals — hedged | volatile→hedged |
| #sec-what-you-will-actually-read-at-work-the-checklist | checklist deriving from confirmed sections | inherits classes |
| #sec-how-this-ties-back-to-the-lessons | n/a shelf-internal | exempt |

## Gaps

| id | claim/area | hunts | status |
|---|---|---|---|
| G-next1 | Exact fetch-caching semantics per major (13 → 15 → Cache Components) | behavior drifted across majors; doc already hedges to "always check the version"; nextjs.org/docs is the live arbiter | convention-tier hedge |
| G-turbo1 | Turbopack production-default rollout pace | doc hedges "increasingly default … in current majors"; no fixed date claimed | convention-tier hedge |

## Content authored from this digestion

- Track B row: justified N/A this pass — rich authored doc delegating facts to cited canon;
  recorded per SHELF-DONE rule (additions OR justified N/A).
