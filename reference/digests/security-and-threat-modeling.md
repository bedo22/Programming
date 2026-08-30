# security-and-threat-modeling — source digestion shell

Status: TRACK A COMPLETE (2026-08-22). 8 unique cited URLs reconciled per v1.7
currency conventions — three standards-body anchors (OWASP Top 10, OWASP Password
Storage Cheat Sheet, NIST CSF), two spec/platform canons (OAuth 2.1, SLSA), one
eternal standard document (RFC 8446 / TLS 1.3 — immutable once published), and
two canon-wiki anchors (STRIDE, Log4Shell). No practitioner blogs or markup
artifacts in the citation set.

## Cited-URL reconciliation (coverage gate requirement)

| cited URL | status | source-dated |
|---|---|---|
| https://owasp.org/Top10/ | standards body — OWASP Top 10, the application-risk taxonomy | dated(current edition) — 2021 edition |
| https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html | standards body — OWASP Password Storage Cheat Sheet (Argon2/bcrypt guidance) | continuously updated current version |
| https://www.nist.gov/cyberframework | standards body — NIST Cybersecurity Framework | dated(current version) — CSF 2.0, 2024-02 |
| https://oauth.net/2.1/ | platform canon — OAuth 2.1 official spec home consolidating current best practice | living draft — volatile→hedged |
| https://slsa.dev/ | platform canon — SLSA, OpenSSF supply-chain integrity levels, versioned spec | dated(current version) — v1.x |
| https://www.rfc-editor.org/rfc/rfc8446 | eternal standard document — RFC 8446, TLS 1.3; immutable once published | dated-once · eternal |
| https://en.wikipedia.org/wiki/STRIDE_(security) | canon wiki — STRIDE threat model (Kohnfelder & Garg, Microsoft, 2003 per doc ledger) | living page · model dated-once |
| https://en.wikipedia.org/wiki/Log4Shell | canon wiki — Log4Shell (CVE-2021-44228) case anchor for supply-chain/surface teaching | living page · event dated-once |

(source-dated per v1.7 currency conventions.)

## Coverage matrix

| doc section | covered by | note |
|---|---|---|
| #sec-how-to-use-this-doc | n/a navigation | exempt |
| #sec-definition-security-as-the-cia-triad | doc-native teaching + NIST CSF canon (see ledger) | definitional · eternal |
| #sec-history-the-constraint-inversions | doc-native inversion table anchored on Log4Shell (2021) case | R17 support · events dated-once · inversions eternal |
| #sec-intersection-with-neighbors-the-duplication-boundaries | n/a shelf-internal | exempt |
| #sec-underlying-theory-threat-modeling | STRIDE canon (four/threat-category model) + doc-native theory | doc-native teaching + cited canon (see ledger) · eternal |
| #sec-running-a-threat-model-the-process | STRIDE process steps + doc-native walkthrough | process eternal · tooling names volatile→hedged |
| #sec-risk-management-the-decision-framework | NIST CSF functions as decision scaffold | R18 function · framework eternal, thresholds hedged |
| #sec-mental-models-frames-for-thinking-about-security | doc-native frames over canon | R14 function · authored framework · eternal |
| #sec-identity-access-management-iam | OAuth 2.1 spec canon | spec draft volatile→hedged |
| #sec-cryptography-data-protection | OWASP Password Storage Cheat Sheet + RFC 8446 TLS 1.3 | algorithms eternal · parameter guidance dated(current version) |
| #sec-application-security-the-owasp-taxonomy | OWASP Top 10 taxonomy | dated(2021 edition) |
| #sec-infrastructure-network-security | RFC 8446/TLS canon + doc-native hardening teaching | principles eternal · versions volatile→hedged |
| #sec-the-ai-era-attack-surface | doc-native thesis, no settled canon cited yet | volatile→hedged |
| #sec-compliance-when-security-becomes-auditable | NIST CSF + SLSA level canon | frameworks dated(current version) |
| #sec-principles-the-shared-constants | doc-native principles | eternal |
| #sec-worked-example-threat-modeling-a-file-upload-endpoint | illustrative worked example applying STRIDE (labeled) | R20 function · eternal |
| #sec-the-security-checklist-the-gate | doc-native checklist over confirmed sections | R20 function · inherits classes |
| #sec-most-common-failure-modes | doc-native failure table with fixes | R15 support · eternal |
| #sec-ecosystem-tooling-catalog-with-decision-metrics | doc-native tool catalog inside details disclosure | R19 support · volatile tools hedged |
| #sec-the-future-where-security-is-going | doc-native signals, hedged | volatile→hedged |
| #sec-summary-the-complete-mental-checklist | derives from confirmed sections | inherits classes |

| #sec-2026-screenshot-loop-eyes-yt-003 | field notes 2026 — dated transcript evidence yt-003 | dated(2026-08) |
## Gaps

| id | claim/area | hunts | status |
|---|---|---|---|
| G-stm1 | AI-era attack-surface claims cite nothing — prompt-injection and agent-abuse taxonomy not yet settled canon | no durable standard exists at Track A time; doc hedges explicitly; re-check on future touch | accepted hedge, revisit |
| G-stm2 | OAuth 2.1 remains an unpublished draft consolidation | track IETF publication; doc already flags draft status | tracked volatility |

## Content authored from this digestion

- Track B row: justified N/A this pass — rich authored doc delegating facts to
  cited canon (standards bodies + spec homes + one immutable RFC); recorded per
  SHELF-DONE rule. NEVER edit any .html file. Dispositions7 merged into
  maps/security-and-threat-modeling.json with WAIVER floor_note at Track A time.
