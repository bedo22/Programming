# `inventory` — index all sessions -> reference/inventory.md (--out PATH for T7.1 selftest)

> GENERATED from `shelf inventory --describe` (ADR 0006) — do not hand-edit;
> regenerate with `shelf render-tool-docs`.

## Usage

`shelf inventory --out`

## Checks performed

- session index vs config playlists
- note presence + status per session

## Exit codes

- `0` — wrote the inventory
- `2` — no config/gates resolution (loud)

## PITFALLS taxonomy tags

- two-truths: PLAYLIST_DIRS drives the rendered list (P6.10 header receipt)

## ADR links

- `references/decisions/0002-*.md`
