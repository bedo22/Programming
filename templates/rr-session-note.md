# RR session note — {{SESSION}} — {{TITLE}}

> **Claims-first format (Phase 2).** Long-form podcast (~60–90 min). Completeness is enforced by
> the SEGMENT MAP: every transcript bucket lands in exactly one segment row or an explicit
> "skipped: boilerplate" row. Nothing else may be dropped silently — when in doubt, it goes in.
>
> Bucket semantics: [MM:SS] markers are ASR chunk labels, not minutes of runtime; runtime =
> last label read as MM:SS. Segment ranges must use literal labels. Sections exempt from
> pins scanning: Papers cited, Fidelity flags/log; every other double-quoted span needs a cite —
> including Open questions (use single quotes for garbled text there).

## Metadata

| Key | Value |
| --- | --- |
| Source file | `{{SOURCE_PATH}}` |
| Title | {{TITLE}} |
| Session | {{SESSION}} |
| Playlist | Rational Reminder |
| Block | {{BLOCK}} |
| Type | solo | interview | Q&A |
| Status | draft |

- Runtime ≈ <from last bucket> · Guest: <name, credential — as spoken; flag if garbled>
- One-line premise: <what the episode argues>
- Flags open: no

## Segment map

| Bucket range | Segment | What happens (1–2 lines) |
|---|---|---|
| [00:00]–[02:14] | Intro/housekeeping | … |
| … | … | every bucket accounted for; mark "boilerplate" rows explicitly |

## Claims-and-evidence

| # | Claim | Who states it | Evidence/numbers given | Minute | Flag |
|---|---|---|---|---|---|
| C1 | … | Ben / guest | stat, study, mechanism | [MM:SS] | — |

(Verdict-style flags where the claim is contested in-episode: "guest disputes at [MM:SS]".)

## Verbatim quotes

Load-bearing statements AND memorable phrasings — pasted from `lift`, never typed,
same-line minute cite `(rr-NNN, MM:SS)`; ranges allowed for spillover sentences.

## Stories & anecdotes register

Pure claims-format would lose these; this register prevents that.

| Story/example | What it shows | Minute |
|---|---|---|
| … | … | [MM:SS] |

## Fidelity flags

Open strictly `yes(N)` | `no`. ASR garbles, name spellings, truncated sentences — same discipline as Phase 1.

## Papers cited

As-spoken citations only (author/title/year as heard); garbled names recorded verbatim in quotes.
Registry/dedup happens centrally, not here.

## Open questions

Anything ambiguous, contradictory, or needing audio recheck — routed `needs review`.
