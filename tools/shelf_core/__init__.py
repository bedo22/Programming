"""shelf package — split from god file tools/shelf.py (1977 lines).

Import side-effects free; use `from shelf_core.config import load_config` etc.
The file tools/shelf.py remains the CLI shim for `python3 tools/shelf.py ...`.
"""

# Version of the IMPROVEMENT-PLAN.md effort (shelf-analysis/IMPROVEMENT-PLAN.md):
# 1.0.x = the pre-plan skill; 1.1.0-dev = plan execution in staging (Phases 0-8),
# released 1.1.0 at the S9.2 promotion gate. S0.4.
#         (1.2.6 = adjacency priority: bare-minutes outranks preceding cite)
# 1.2.5 = F8: bare-minutes parenthetical «q» (MM:SS) = the note's own session
#         (fork shorthand; stops follow-up quotes inheriting neighbour cites)
# 1.2.4 = F7: raw-lane sessions join the registry (raw-only sessions resolve;
#         routing verifies their notes against the raw lane)
# 1.2.3 = F6: parse_note threads own_pl into scan_lines — keyword self-cites
#         resolve to the note's own playlist; unicode pad-tolerant fallback
# 1.2.2 = F3c/F4b: pad-tolerant get_session (fork unpadded cites) + RawSource
#         lane routing (raw-cited notes verify against raw ASR originals)
# 1.2.1 = F3b: status prefix grammar (status_prefix_ok config gate) — fork
#         free-prose statuses validate as enum-value + annotation; 2 selftest guards
# 1.2.0 = T9.1/T9.2 onboarding (ADR 0007): prefixless keys, per-playlist
# top-level transcript dirs, self-resolving keyword cites, claims contract.
__version__ = "1.2.22"
