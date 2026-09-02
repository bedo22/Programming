# `pins` — verify every quote's minute (exit 0 = clean)

> GENERATED from `shelf pins --describe` (ADR 0006) — do not hand-edit;
> regenerate with `shelf render-tool-docs`.

## Usage

`shelf pins --fix targets`

## Checks performed

- cited quote spans vs transcript (minute + presence)
- uncited blockquote evidence (hard)
- uncited inline (advisory)
- NOTHING-WAS-VERIFIED: 0 checks with quoted spans = exit 1

## Exit codes

- `0` — all flags clean
- `1` — flags raised
- `2` — note/session unresolvable (loud)

## PITFALLS taxonomy tags

- comma bug class -> NOTHING-WAS-VERIFIED guard
- ambiguous find_note refuses, never silent

## ADR links

- `references/decisions/0001-*.md`
- `references/decisions/0004-*.md`
