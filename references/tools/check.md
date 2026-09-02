# `check` — gate: all | playlist | block | KEY | path

> GENERATED from `shelf check --describe` (ADR 0006) — do not hand-edit;
> regenerate with `shelf render-tool-docs`.

## Usage

`shelf check scope`

## Checks performed

- every doc quote vs transcript
- links resolve
- note statuses valid
- unrecognized note-name grammar announced (P6.4)

## Exit codes

- `0` — intact
- `1` — fails listed
- `2` — no corpus resolved / scoped zero-match (W4.4, P6.2)

## PITFALLS taxonomy tags

- file branch sets n_docs/n_notes (T7.1 was: UnboundLocalError)

## ADR links

- `references/decisions/0002-*.md`
- `references/decisions/0004-*.md`
