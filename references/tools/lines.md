# `lines` — numbered view of clean transcript

> GENERATED from `shelf lines --describe` (ADR 0006) — do not hand-edit;
> regenerate with `shelf render-tool-docs`.

## Usage

`shelf lines key lo hi`

## Checks performed

- key resolves to an indexed session

## Exit codes

- `0` — printed range
- `1` — usage (bad KEY or non-numeric lo/hi)
- `2` — no session for key

## PITFALLS taxonomy tags

- P6.10: prose lo/hi printed int() traceback — now usage

## ADR links

- `references/decisions/0002-*.md`
