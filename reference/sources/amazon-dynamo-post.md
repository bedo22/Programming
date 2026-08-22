# Source digest — DeCandia et al./Vogels — Amazon Dynamo (allthingsdistributed post)

## Identity
- **Full citation:** DeCandia, D. et al. (2007). "Dynamo: Amazon's Highly Available Key-value Store" (SOSP); context post on allthingsdistributed.com (2012 era).
- **Verified link:** https://www.allthingsdistributed.com/2012/01/amazon-dynamodb.html
- **First verified:** 2026-08-21 · **Last checked:** 2026-08-21

## What the doc(s) claim from this source
- api-design/system-design consistency rows: eventual consistency as a product decision.

## Key findings (one line each, with supporting quote)
- **Consistency windows confuse developers when extreme** — SimpleDB's "eventually consistent" extremes produced windows "up to a second", which the post reports was "not intuitive to use" versus traditional expectations — the empirical case for declaring consistency in contracts.

## Notes / caveats
- Post discusses DynamoDB vs SimpleDB evolution; pure-Dynamo-paper claims (N/R/W quorums) come from the 2007 SOSP paper, not this post — cite the paper separately if needed.

## Related digests
- gilbert-lynch-brewers-conjecture.md — CAP formalization behind the tradeoff.

## Verification history
- 2026-08-21: ok (eventually-consistent passage re-grepped from fetched copy)
