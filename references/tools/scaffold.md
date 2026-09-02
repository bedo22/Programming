# `scaffold` — blank session note(s) from template

> GENERATED from `shelf scaffold --describe` (ADR 0006) — do not hand-edit;
> regenerate with `shelf render-tool-docs`.

## Usage

`shelf scaffold target --topics --from-yaml --from-json --from-notes title`

## Checks performed

- one-write: refuses existing note/doc without --force
- doc --from-notes: reports stitched AND skipped sections (P6.9)
- bare range binds DEFAULT_PLAYLIST (P6.1)

## Exit codes

- `0` — note/doc written
- `1` — usage
- `2` — zero-match scope (loud, P6.1/P6.2)

## PITFALLS taxonomy tags

- W4.21: note discovery via find_note (ambiguity-refusing)

## ADR links

- `references/decisions/0002-*.md`
