# `doctor` — diagnose: resolved root, config, grammar, paths, playlists (read-only)

> GENERATED from `shelf doctor --describe` (ADR 0006) — do not hand-edit;
> regenerate with `shelf render-tool-docs`.

## Usage

`shelf doctor`

## Checks performed

- config resolution (present/absent/corrupt-loud)
- grammar values active
- data paths exist
- why-pointers to DESIGN (D8.10)

## Exit codes

- `0` — report printed (additive — never a gate, ADR 0005)

## PITFALLS taxonomy tags

- config absence is silent EN defaults BY DESIGN (C3.3)

## ADR links

- `references/decisions/0002-*.md`
- `references/decisions/0005-*.md`
