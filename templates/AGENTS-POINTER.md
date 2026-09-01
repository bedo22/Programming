# AGENTS.md — this shelf runs on shelf-pipeline <X.Y.Z>

Identity: transcripts → notes → docs, config-driven registry
(`config/project.yaml` — a shelf is its config). Placement and grammar
decisions live in the skill's `references/decisions/` ADRs.

**Hard rules (violations are how shelves rot):**

1. NEVER edit `tools/` or the skill's files in place. Problems are recorded,
   not patched: write a row in `FINDINGS.md` (row grammar at its top).
2. One write per artifact, always verified (`pins`, `check`, gates).
   `Flags: 0` on zero scanned spans is a refusal, not a pass.
3. `transcripts/` is immutable — notes are claims about sources.
4. Verify before trusting: `python3 tools/shelf.py selftest` (fixture corpus,
   no live data) → `doctor` → `pins <key>` on a known session.

**Where problems go:** row in `FINDINGS.md` → promotion pass (maintainer
session) → skill `IMPROVEMENT-LEDGER.md`. Triage and fixes are done by a
maintenance session — defined by loaded doctrine (MAINTAINING.md + ledger),
NOT by a fixed session identity.

Version: `python3 tools/shelf.py --version` · notable changes: skill
`CHANGELOG.md`.
