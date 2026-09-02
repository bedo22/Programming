# `lift` — paste-ready quotes from stdin phrases

> GENERATED from `shelf lift --describe` (ADR 0006) — do not hand-edit;
> regenerate with `shelf render-tool-docs`.

## Usage

`shelf lift key`

## Checks performed

- stdin phrases -> verbatim spans via CleanSource/subseq (V1.4 fallback)

## Exit codes

- `0` — units printed
- `1` — NOTFOUND/NOSLICE phrases reported

## PITFALLS taxonomy tags

- never retype ASR — spans are sliced (correctness-by-construction)

## ADR links

- `references/decisions/0001-*.md`
