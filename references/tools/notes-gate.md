# `notes-gate` — GATE per-note: pins+contamination+empty-scaffold+verdict-contradictions

> GENERATED from `shelf notes-gate --describe` (ADR 0006) — do not hand-edit;
> regenerate with `shelf render-tool-docs`.

## Usage

`shelf notes-gate paths`

## Checks performed

- pins in-process (fallback: tools/shelf.py subprocess while present)
- empty-scaffold via config-driven status labels (W4.13)
- FOREIGN SCRIPT + PITFALLS I/J; verdict contradictions >=0.95 overlap
- review-queue TRIAGE (never blocks); template exemption

## Exit codes

- `0` — all notes pass
- `1` — GATE FAILs listed

## PITFALLS taxonomy tags

- templates (قالب/template/skeleton) exempt loudly
- bucket-ref validity owned by pins (W4.12 dead-check removed)

## ADR links

- `references/decisions/0002-*.md`
