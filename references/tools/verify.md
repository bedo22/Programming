# `verify` — verification lane

> GENERATED from `shelf verify --describe` (ADR 0006) — do not hand-edit;
> regenerate with `shelf render-tool-docs`.

## Usage

`shelf verify action rest --key --ref --stem --phrase --title --from-json --find --amend --out --bodies --dry --add-section --json`

## Checks performed

- quran/hadorith/history channel routing (references/VERIFICATION.md)
- worklist completion meter (0 unique = shelf verified)
- sync-docs: the ONLY notes->docs direction

## Exit codes

- `0` — lane ok
- `1` — unverified entries
- `2` — usage/config loud

## PITFALLS taxonomy tags

- sync-docs --dry idempotency
- a doc is never a source (one-way core model)

## ADR links

- `references/decisions/0001-*.md`
