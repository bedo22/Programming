# `doc-coverage` — TRIAGE ledger: per-session representation of every doc (gates.coverage_profile selects profile)

> GENERATED from `shelf doc-coverage --describe` (ADR 0006) — do not hand-edit;
> regenerate with `shelf render-tool-docs`.

## Usage

`shelf doc-coverage paths`

## Checks performed

- per-session quote/claim coverage vs floors (floor_high/low, repr_pct)
- profile fork: quotes-responsibility (_fork_main family) vs generic
- ambiguous note globs printed; bucket fallback labeled

## Exit codes

- `0` — report printed
- `1` — flagged docs
- `2` — no docs_dir configured / no docs

## PITFALLS taxonomy tags

- Politics+fqhn run the quotes-responsibility fork
- module-level exit(2) became in-command (same code, same message)

## ADR links

- `references/decisions/0002-*.md`
