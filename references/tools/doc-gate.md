# `doc-gate` — GATE per-doc: check+responsibility+neglect+quarantine+essay-proxy+scripts

> GENERATED from `shelf doc-gate --describe` (ADR 0006) — do not hand-edit;
> regenerate with `shelf render-tool-docs`.

## Usage

`shelf doc-gate paths`

## Checks performed

- shelf check via in-process cmd_check (returncode only)
- responsibility corpus-cites floor; neglect/thin triage
- quarantine pattern; essay-proxy share/words/paras (ar_ratio, defs-aware)
- script contamination + PITFALLS I/J; template exemption

## Exit codes

- `0` — all docs pass
- `1` — GATE FAILs listed

## PITFALLS taxonomy tags

- --all sweeps reference/**/*.html (default when no paths)
- floor auto: 12 if avg-buckets>40 else 7 (freeze in config)

## ADR links

- `references/decisions/0002-*.md`
