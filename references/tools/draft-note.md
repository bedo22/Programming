# `draft-note` — scripted note builder from MEH.yaml (via verified matcher, PITFALLS.md A/C/H)

> GENERATED from `shelf draft-note --describe` (ADR 0006) — do not hand-edit;
> regenerate with `shelf render-tool-docs`.

## Usage

`shelf draft-note key --from-yaml --from-json --force`

## Checks performed

- MEH spec shape validated in ONE pass (title/axes/khu)
- quotes sliced from transcript by construction

## Exit codes

- `0` — note written
- `1` — no MEH input / shape invalid
- `2` — session unresolvable

## PITFALLS taxonomy tags

- Pitfall A/C/H (PITFALLS.md): never retype quotes
- never re-run --from-yaml against a finished note (clobbers polish)

## ADR links

- `references/decisions/0001-*.md`
