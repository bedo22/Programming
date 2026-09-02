# `selftest` — fixture-based self test

> GENERATED from `shelf selftest --describe` (ADR 0006) — do not hand-edit;
> regenerate with `shelf render-tool-docs`.

## Usage

`shelf selftest`

## Checks performed

- 20 named guards over its OWN fixture corpus (T7.1/T7.2)
- inventory regen inside the fixture (--out)
- outer reference/ untouched

## Exit codes

- `0` — all pass
- `1` — failed list printed

## PITFALLS taxonomy tags

- fixture corpus = self-built (ADR 0004); fresh-clone capable

## ADR links

- `references/decisions/0004-*.md`
