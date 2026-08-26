# Source Access Guide

How to find, access, and verify papers cited in the reference shelf.
This guide is for the next agent who needs to read a paper, verify a DOI, or create a new source digest.

---

## Quick reference: access by source type

| Type | Count | Primary access | Fallback |
|---|---|---|---|
| **Open-access journal** | 24 | Direct link in digest | DOI → publisher page |
| **Paywalled journal** | 108 | DOI → publisher page | Sci-Hub, LibGen, Unpaywall, library |
| **Book / chapter** | 8 | Publisher page, Google Books | Internet Archive, library |
| **Preprint** | 2 | OSF, arXiv, bioRxiv | Version of Record DOI |
| **Chinese journal** | 1 | CNKI, Wanfang | Google Scholar, translation tools |

---

## Tier system (from the trust analysis)

### Tier 1 — Top field journals (31%)
Psychological Science, Nature, Science, JPSP, American Psychologist, Psychological Review, PNAS, Neuron, eLife, New England Journal of Medicine

**Access:** DOI resolves to publisher (APA, SAGE, Nature, Cell Press, AAAS). Most are paywalled but many have free abstracts. Some (e.g., PNAS, Nature, eLife) have open-access options.

### Tier 2 — Strong specialty journals (34%)
JEP:LMC, JEP:HPP, Educational Psychology Review, Behavioral and Brain Sciences, Perspectives on Psychological Science, Journal of Occupational Health Psychology, Annual Review series, Applied Psychology, Brain Research Reviews, Trends in Cognitive Sciences

**Access:** DOI resolves to publisher (APA, SAGE, Elsevier, Wiley, Annual Reviews). Mostly paywalled. BBS and Perspectives sometimes have free access.

### Tier 3 — Open-access / newer (8%)
Frontiers in Psychology, Frontiers in Education, PLOS ONE, Scientific Reports, MDPI (Behavioral Sciences), eLife

**Access:** Free full text via publisher site. All have direct PDF downloads.

### Tier 4 — Books, chapters, preprints (27%)
Classic books and chapters: Bjork (2011), Baddeley & Hitch (1974), Miller (1956), Ericsson et al. (1993), Huizinga (1938), Brown (2009), Berridge & Robinson (1996/2009), Sutton-Smith (1997), Burghardt (2005), Caillois (1961), Panksepp, Gray (2013), etc.

**Access:** 
- Journal articles from books: DOI → publisher (often APA or Elsevier)
- Standalone books: publisher page, Google Books preview, Internet Archive
- Book chapters: DOI often works; Google Scholar shows "Cited by" count for verification

### Tier 5 — Chinese-language journals (1%)
Advances in Psychological Science (心理科学进展)

**Access:** CNKI (cnki.net), Wanfang Data, Google Scholar. Abstract often in English; full text in Chinese. May require institutional access or paid subscription.

---

## Access methods (ordered by reliability)

### 1. DOI resolution (always try first)
```
https://doi.org/{DOI}
```
- Returns 200, 301, 302, 403, or 405 = paper exists (403/405 = paywall but DOI is valid)
- Returns 404 = DOI not registered or incorrect
- Use Crossref API to verify DOI exists: `https://api.crossref.org/works/{DOI}`

### 2. Crossref API (for DOI verification)
```bash
curl -H "User-Agent: shelf-research/1.0 (mailto:you@example.com)" \
  "https://api.crossref.org/works/{DOI}"
```
- Returns JSON with title, authors, year, journal, DOI
- Use this to verify a DOI is real before adding it to a digest
- Rate limit: 1 request/second (add jitter)

### 3. Semantic Scholar API (for searching by title/author)
```bash
curl "https://api.semanticscholar.org/graph/v1/paper/search?query={title}&limit=3&fields=title,authors,year,externalIds"
```
- Good for finding DOIs when you only have author+year
- Rate limited — use sparingly

### 4. Open-access repositories
- **PubMed Central (PMC):** https://www.ncbi.nlm.nih.gov/pmc/ — free full text for many biomedical papers
- **arXiv:** https://arxiv.org — preprints in CS, physics, math, statistics
- **bioRxiv:** https://www.biorxiv.org — biology preprints
- **OSF:** https://osf.io — preprints, replications, supplementary materials
- **Semantic Scholar:** https://semanticscholar.org — free abstracts, some free full text

### 5. Paywall bypass (when legitimate access is needed)
- **Unpaywall:** browser extension that finds legal open-access versions
- **Sci-Hub:** controversial but functional; use with awareness of legal implications
- **LibGen:** mirror of Sci-Hub with book coverage
- **Google Scholar:** often links to free versions (preprints, author copies, institutional repos)
- **Institutional access:** if you have a university affiliation, many journals are free

### 6. Internet Archive / Wayback Machine
- https://web.archive.org — archived versions of paywalled pages
- https://archive.org — books, older papers, out-of-copyright works

### 7. Google Books
- Many older books (Miller 1956, Huizinga 1938, etc.) have preview pages
- Not complete but useful for verifying quotes

---

## Verification workflow

### Before creating a new source digest:

1. **Find the DOI** — use Crossref API search, Google Scholar, or the paper's own website
2. **Verify the DOI** — `curl https://api.crossref.org/works/{DOI}` should return 200
3. **Check the paper exists** — DOI resolves to a real page (not a 404)
4. **Read the paper** — via one of the access methods above
5. **Extract key findings and quotes** — use the _TEMPLATE.md format
6. **Write the digest** — save to `reference/sources/<short-key>.md`

### Before shipping changes:

1. **Run verify-links.py** — `python3 scripts/verify-links.py`
2. **Fix any failures** — update the DOI or URL in the digest
3. **Run link-sources.py** — `python3 scripts/link-sources.py` to re-link
4. **Re-verify** — run verify-links.py again

---

## Common problems and solutions

### "DOI returns 404"
- Check for typos (case-sensitive for some publishers)
- Try the Crossref API — if it finds the paper, the DOI is registered but may be inactive
- Search Google Scholar for the paper title to find the correct DOI

### "Paper is behind a paywall"
- Try Google Scholar → look for "All versions" link
- Try Unpaywall (browser extension)
- Try author's personal website or ResearchGate
- Check if the paper has a preprint version on arXiv/bioRxiv/OSF

### "Book chapter — no DOI"
- Search Google Scholar for the chapter title
- Check the publisher's website (APA, Academic Press, etc.)
- Use a stable URL (publisher page, Google Books link) instead of DOI

### "Chinese journal — can't find DOI"
- Search CNKI (cnki.net) or Google Scholar
- Use the journal's stable URL if available
- Note in the digest that the paper is from a Chinese-language journal

### "Paper seems too new to be in Crossref"
- Check arXiv/bioRxiv for a preprint version
- Search Google Scholar — it indexes papers faster than Crossref
- Use the publisher's DOI if available, even if Crossref hasn't indexed it yet

---

## Files in this directory

- `reference/sources/*.md` — source digests (one per paper)
- `reference/sources/_TEMPLATE.md` — template for new digests
- `reference/sources/SOURCE-ACCESS.md` — this file
- `reference/scripts/verify-links.py` — link verification script
- `reference/scripts/link-sources.py` — source-linking script
- `reference/scripts/.link-cache.json` — verification cache (commit this)

---

## Coverage status

As of the last batch commit (August 2026):
- **143 source digests** covering all major cited papers
- **~1,300 📄 links** across 18 shelf HTML docs
- **65% Tier 1-2** (top journals), 27% Tier 4 (books/chapters), 8% Tier 3 (open-access)
- **2 remaining gaps:** Burgess (2023), Dekker (2023) — both single-doc, minor citations
- **5 false-positive gaps:** secondary authors already covered under primary author digests
