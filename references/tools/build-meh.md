# `build-meh` — draft a MEH.yaml from an agent's structured reading of one lecture

> GENERATED from `shelf build-meh --describe` (ADR 0006) — do not hand-edit;
> regenerate with `shelf render-tool-docs`.

## Usage

`shelf build-meh`

## Checks performed

- MEH.yaml shape; transcript segment slicing by construction

## Exit codes

- `0` — yaml written
- `1` — invalid input

## PITFALLS taxonomy tags

- ROOT was __file__-derived in the script; now find_root (cwd)

## ADR links

- `references/decisions/0001-*.md`
