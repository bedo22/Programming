# dotnet-and-the-enterprise-lane — source digestion shell

Status: TRACK A COMPLETE (2026-08-22), 5 unique cited URLs reconciled per v1.7 currency conventions.
All five are official product/platform docs — Microsoft Learn (ASP.NET Core, C#, EF Core,
T-SQL) plus roadmap.sh's community roadmap. Authority anchors per house convention;
fetch-on-demand. The doc's teaching is doc-native translation work that delegates facts
to those canon references by design ("the depth lives in Microsoft Learn … linked below").

## Cited-URL reconciliation (coverage gate requirement)

| cited URL | status | source-dated |
|---|---|---|
| https://learn.microsoft.com/en-us/aspnet/core/ | platform canon — ASP.NET Core documentation (Microsoft Learn) | continuously updated |
| https://learn.microsoft.com/en-us/dotnet/csharp/ | platform canon — C# language documentation | continuously updated |
| https://learn.microsoft.com/en-us/ef/core/ | platform canon — EF Core documentation | continuously updated |
| https://learn.microsoft.com/en-us/sql/t-sql/ | platform canon — T-SQL reference | continuously updated |
| https://roadmap.sh/aspnet-core | practitioner canon — community ASP.NET Core roadmap | living page |

## Coverage matrix

| doc section | covered by | note |
|---|---|---|
| #sec-how-to-use-this-doc | n/a navigation | exempt |
| #sec-definition-the-enterprise-lane-and-what-literacy-means | doc-native framing; stack anatomy + literacy contract; market-segment table is authored survey | eternal framing · market-position rows volatile→hedged |
| #sec-intersection-with-neighbors-the-duplication-boundaries | n/a shelf-internal | exempt |
| #sec-the-request-loop-c-edition | doc-native teaching mapping onto Backend Engineering loop; pipeline facts delegate to cited canon (see ledger) | eternal mechanism · attribute/API surface volatile→hedged |
| #sec-c-reading-literacy-the-typescript-translation-table | doc-native TS→C# table; language semantics delegate to cited C# docs canon | eternal semantics · async-engine divergence hedged in-doc |
| #sec-reading-linq-the-query-pipeline-at-a-glance | doc-native LINQ↔SQL/JS translation table | eternal |
| #sec-ef-core-the-orm-you-already-understand | EF Core docs canon + Backend Engineering ORM-decision mapping (see ledger) | eternal ORM concepts · CLI/tooling commands volatile→hedged |
| #sec-dependency-injection-the-framework-shape | doc-native lifetimes teaching grounded in framework shape | eternal framework shape |
| #sec-the-net-market-map-where-the-lane-actually-is | authored market analysis — deliberately qualitative, no external stats cited | volatile→hedged by design |
| #sec-decoding-the-version-what-net-means-in-a-listing | product-line naming history (Framework→Core→unified .NET) | dated-once · eternal for settled history; current-LTS row volatile→hedged |
| #sec-sql-server-the-t-sql-dialect | T-SQL reference canon + doc-native dialect-diff table (see ledger) | eternal dialect facts · feature surface volatile→hedged |
| #sec-when-not-to-pick-net | doc-native choosing guidance — mirror side of the lane map | R18 function · authored framework |
| #sec-worked-example-reading-a-net-codebase | illustrative labeled walkthrough (real-shaped endpoint) + first-three-files reading order | eternal method |
| #sec-the-literacy-pitfalls-failure-modes | traces to confirmed lane-map rows | R15 support · eternal |
| #sec-summary-the-lane-map | derives from confirmed sections | inherits classes |

## Gaps

| id | claim/area | hunts | status |
|---|---|---|---|
| G-ver1 | ".NET 8 is current, 10 is the next even line" — LTS-currency claim ages with the release train | recheck against Microsoft Learn .NET support-policy pages at next touch; doc already teaches "which .NET?" as an interview question | convention-tier hedge |
| G-mar1 | quantitative demand/salary figures for the enterprise lane | delegated to Frontend Income Markets (owner doc); this doc stays qualitative on purpose | accepted authored framework |

## Content authored from this digestion

- Track B row: justified N/A this pass — rich authored doc delegating facts to cited
  canon (Microsoft Learn platform docs + roadmap.sh); recorded per SHELF-DONE rule
  (additions OR justified N/A). HTML docs untouched.
