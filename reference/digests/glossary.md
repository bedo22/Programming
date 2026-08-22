# glossary — source digestion shell

Status: TRACK A COMPLETE (2026-08-22), 0 unique cited URLs reconciled per v1.7 currency conventions.
Claim-inventory mode: the doc contains no external citations at all (zero `http(s)` strings, no
`class="cite"` section). Its authority model is owner-pointer delegation — every term row ends in
anchor links into the sibling doc that owns the term, so the sourcing ledgers live in those docs'
digests, not here.

## Cited-URL reconciliation (coverage gate requirement)

Zero cited URLs in `reference/glossary.html` — stated plainly per convention; table omitted.
Nothing to reconcile against fetch-status lines.

## Coverage matrix

| doc section | covered by | note |
|---|---|---|
| #sec-shelf-map-the-complete-curriculum-at-a-glance | n/a navigation | exempt |
| #sec-design-thinking-owner-design-thinking-html | doc-native one-line definitions + owner-pointer canon (design-thinking.md ledger) | eternal · R15 support (Design Theater → owner failure modes) |
| #sec-system-design-owner-system-design-html | doc-native definitions + owner-pointer canon (system-design.md ledger) | eternal · R15 support (Failure Domain / circuit breaker rows) |
| #sec-api-design-owner-api-design-html | doc-native definitions + owner-pointer canon (api-design.md ledger) | eternal patterns · tooling/metrics rows volatile→hedged · R15 support (failure-modes pointer) |
| #sec-ui-ux-web-design-owner-ui-ux-web-design-html | doc-native definitions + owner-pointer canon (ui-ux-web-design.md ledger) | dated-once · eternal for settled history (regulation dates DSA/Delete Act) |
| #sec-html-css-owner-html-and-css-html | doc-native definitions + owner-pointer canon (html-and-css.md ledger) | eternal |
| #sec-javascript-the-language-owner-javascript-the-language-html | doc-native definitions + owner-pointer canon (javascript-the-language.md ledger) | eternal |
| #sec-frontend-camps-survey-owner-frontend-camps-survey-html | doc-native definitions + survey canon via owner (frontend-camps-survey.md ledger) | volatile→hedged (camp gravity shifts) |
| #sec-developer-loop-how-developers-think-owner-how-developers-think-frontend-html | doc-native definitions + owner-pointer canon (how-developers-think-frontend.md ledger) | authored framework · eternal |
| #sec-problem-solving-owner-problem-solving-html | doc-native definitions (Pólya, heuristics) + owner-pointer canon | eternal |
| #sec-algorithms-data-structures-owner-algorithms-and-data-structures-html | doc-native definitions + owner-pointer canon (algorithms-and-data-structures.md ledger) | eternal |
| #sec-computer-science-software-engineering | doc-native definitions naming ISO 25010 / Turing 1936 / NATO 1968 without cites — sourcing delegated to owner doc | eternal · standards reference dated(current version) |
| #sec-software-development-process | doc-native definitions (SDLC, Agile, Scrum, Kanban, ADLC) + owner-pointer canon (software-development-process.md ledger) | dated-once · eternal for settled history; ADLC/AI-augmented volatile→hedged |
| #sec-security-threat-modeling-owner-security-and-threat-modeling-html | doc-native definitions + owner-pointer canon (security-and-threat-modeling.md ledger) | eternal |
| #sec-cross-cutting-terms-appear-in-multiple-disciplines | multi-owner sense rows, both senses noted + all owner pointers | eternal · ops metrics (SLO/MTTR/postmortem) inherit owner hedging · R15 support |
| #sec-wordpress-the-cms-internet-owner-wordpress-and-cms-internet-html | doc-native definitions + owner-pointer canon (wordpress-and-cms-internet.md ledger) | volatile→hedged (plugin/platform landscape) |
| #sec-payments-commerce-owner-payments-and-commerce-html | doc-native definitions + PSP/PCI canon via owner (payments-and-commerce.md ledger) | eternal process · PCI dated(current DSS version) |
| #sec-freelance-web-practice-owner-freelance-web-practice-html | doc-native definitions + owner-pointer canon (freelance-web-practice.md ledger) | convention-tier hedge (scoping/rates market-dependent) |
| #sec-hiring-process-interviews-owner-hiring-process-and-interviews-html | doc-native definitions + owner-pointer canon (hiring-process-and-interviews.md ledger) | volatile→hedged (market/funnel shifts) |
| #sec-terminal-the-deployment-substrate-owner-terminal-and-deployment-substrate-html | doc-native definitions + owner-pointer canon (terminal-and-deployment-substrate.md ledger) | eternal mental models · cloud-era framing dated-once |
| #sec-sql-postgresql-owner-sql-and-postgresql-html | doc-native definitions + owner-pointer canon (sql-and-postgresql.md ledger) | eternal |
| #sec-net-the-enterprise-lane-owner-dotnet-and-the-enterprise-lane-html | doc-native definitions + owner-pointer canon (dotnet-and-the-enterprise-lane.md ledger) | eternal literacy · framework versions volatile→hedged |

## Gaps

| id | claim/area | hunts | status |
|---|---|---|---|
| G-glos1 | Inline attributions carry no citations (ISO 25010, Rittel & Webber 1973, Argyris & Schön 1978, GV 2016…) — sourcing deliberately delegated to the owning docs | convention-tier hedge — owner docs' digests hold the reconciliation ledgers | accepted |
| G-glos2 | Owner-pointer anchors can rot when an owner doc restructures its spine | mechanical: verify-twins.py resolves internal + cross-doc anchors every run | gated, accepted |

## Content authored from this digestion

- Track B row: justified N/A this pass — rich authored doc delegating facts to cited canon;
  recorded per SHELF-DONE rule (additions OR justified N/A). Do NOT edit the HTML docs themselves.
