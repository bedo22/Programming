# Raw seeds — _debt-harvest (2026-08-22)

Closing fetch pass for every open G-* hunt across reference/digests/*.md.
All fetched live via scrapling per the scrape skill (light default; Wayback Machine
for pages that block or stall; Crossref API for DOI identities; NVD API for CVE).
Output extension rules respected (.html/.md/.txt).

| file | hunt | verifies |
|---|---|---|
| shannon-1948.html | G-st1 | "1948 article by Claude S[hannon]" — A Mathematical Theory of Communication |
| church-lambda.html | G-st2 | Alonzo Church, lambda calculus, 1930s origin |
| self-language.html | G-js1 | prototype-based lineage; ECOOP'96 "Prototype-Based Languages" ref |
| littles-law.html | G-sd4 | L = λW verbatim; Little's 1961 proof ("no such situation exists") |
| css-history.html | G-hc2 | Lie 10-Oct-1994 CERN proposal citation chain |
| lie-cascade-1994.html | G-hc2 | PRIMARY SOURCE: "Cascading HTML Style Sheets -- A Proposal" (CERN) |
| cache-stampede.html | G-sd5 | cache stampede concept + Vattani "Cache Stampede Prevention" cite |
| outbox.md | G-sd6 | Transactional outbox pattern (microservices.io) |
| dlq-azure.md | G-sd6 | Dead-letter queues canonical doc (Azure Service Bus) |
| adr-nygard.html | G-sd8 | Michael Nygard, "Documenting Architecture Decisions", 2011 |
| cve-nvd.txt | G-r1 | CVE-2025-55183: RSC information leak, affected versions 19.0.0–19.2.1 |
| r-useactionstate.html + r-form.html | G-r2 | React Actions canon (pending state, form action semantics) |
| doi-54411-full / cr-54411.txt / cr-55392.txt | G-ux2 | Crossref identities — **found mis-link**: h0054411 is a Kinsey-study paper, NOT Hick; true Hick 1952 DOI = 10.1080/17470215208416600 (QJEP). Fitts 1954 link confirmed correct |
| swillison-hooks.html | G-ch2 | Dan Abramov "Making Sense of React Hooks" canonical medium URL + dated third-party confirmation; original Cloudflare-walled |
| rn-wayback.html | G-jas2 | New Architecture overview via Wayback (Fabric verified) |
| pd-roles-wayback.html | G-ob5 | PagerDuty roles at corrected path /before/different_roles/ (IC/Deputy/Scribe/SME ×39) |

Corrections issued to shelf docs this pass:
- ui-ux-web-design EN+AR bibliography: Hick DOI replaced with the correct QJEP link
  (journal/volume/pages added). Found only because Crossref identity check was run —
  the harvest paid for itself.
