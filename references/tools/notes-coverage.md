# `notes-coverage` — TRIAGE ledger: how completely each note distills its transcript

> GENERATED from `shelf notes-coverage --describe` (ADR 0006) — do not hand-edit;
> regenerate with `shelf render-tool-docs`.

## Usage

`shelf notes-coverage paths`

## Checks performed

- buckets/quotes/cited/claims per note; quotes-per-claim density
- SCAFFOLD/THIN/ZERO flags (gate.thin_quotes_per_claim)

## Exit codes

- `0` — report printed
- `2` — no notes found

## PITFALLS taxonomy tags

- claim grammar = notes.claims_count (A5.3, one home)

## ADR links

- `references/decisions/0002-*.md`
