# `evdoc` — evidence-doc one-write from EVIDOC.yaml (doc-side mirror of draft-note)

> GENERATED from `shelf evdoc --describe` (ADR 0006) — do not hand-edit;
> regenerate with `shelf render-tool-docs`.

## Usage

`shelf evdoc --from-yaml --out --dump --seed`

## Checks performed

- probe resolution against the note cite-pool (W4.17 ambiguity, W4.18 stale)
- frame-length lint (shared min_para_chars, P6.14)
- placeholder check BEFORE {body} (P6.14)

## Exit codes

- `0` — doc built
- `1` — probe/STALE failures
- `2` — spec/template missing

## PITFALLS taxonomy tags

- probes <12 chars warn (weak anchors)
- cite_kw defaults EMPTY — no keyword assumption

## ADR links

- `references/decisions/0001-*.md`
