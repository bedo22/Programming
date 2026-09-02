# `lint` — intake check: categorized note findings (key/status/flags/ufffd/script/cite)

> GENERATED from `shelf lint --describe` (ADR 0006) — do not hand-edit;
> regenerate with `shelf render-tool-docs`.

## Usage

`shelf lint targets`

## Checks performed

- key grammar
- status/flags whole-value (A5.6)
- U+FFFD
- script convention
- cite-like timecodes without cite

## Exit codes

- `0` — no findings
- `1` — findings listed (additive intake, ADR 0005)

## PITFALLS taxonomy tags

- template notes exempt (قالب/template/skeleton)

## ADR links

- `references/decisions/0005-*.md`
