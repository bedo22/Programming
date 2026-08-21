# Source digest — {Author(s) Last Name, Year}

> One file per paper the shelf actually cites. The digest is what accumulates:
> next time a doc needs "what does {author} say about {claim}?", grep this file
> instead of re-scraping the web. Save under `reference/sources/<short-key>.md`.
> Follow this template exactly — every field is load-bearing for the
> verification pipeline.

## Identity

- **Full citation:** {Full author list, Year, Title, Journal/Publisher, Vol(Issue), pages}
- **DOI:** {10.xxxx/yyyy} — must be a real registered DOI (verify: `python3 scripts/verify-links.py`)
- **Verified link:** https://doi.org/{doi} (or publisher/PMC URL if no DOI)
- **Open-access link (if any):** {URL to free full text}
- **First verified:** {YYYY-MM-DD}
- **Last checked:** {YYYY-MM-DD}

## What the doc(s) claim from this source

- {Doc name} claims: "{the claim as stated in the doc}" (doc section/line ref)
- {Doc name} claims: ...

## Key findings (one line each, with supporting quote)

> The deep-question answers this paper supports, each tied to a quote above.
> A future agent should be able to read THIS section and answer, not hunt quotes.

- **{finding, declarative one-line answer}** — supported by quote: "{short quote snippet or its location above}".
- {finding}: {one-line answer} — {which quote above supports it}.

## Key quotes (with locations)

> "{exact quote from the paper}" — {section/para/page marker}

## Notes / caveats

- {anything the doc must NOT overclaim: correlational, small sample, replication record, contested mechanism}
- **Does NOT support:** {explicit negative space — what a future agent must not use this paper to claim}

## Related digests

- {short-key}.md — {relationship: quotes it / cited by it / same cluster}

## Verification history

- {YYYY-MM-DD}: {ok / FAIL — detail} (run: `python3 scripts/verify-links.py`)
