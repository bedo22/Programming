"""shelf package — split from god file tools/shelf.py (1977 lines).

Import side-effects free; use `from shelf_core.config import load_config` etc.
The file tools/shelf.py remains the CLI shim for `python3 tools/shelf.py ...`.
"""

# 1.2.21 = F18 text-source lanes (vtable + التحقق:; doc-lane advisory parity)
# 1.2.20 = normalize_for_match casefold (verdict lane; posmap-exact)
# 1.2.19 = tokens() casefold (EN-shelf silent-zero)
# 1.2.22 = F19 text-source lanes (broadened markers + vtable wrap fix)
# Version of the IMPROVEMENT-PLAN.md effort (shelf-analysis/IMPROVEMENT-PLAN.md):
# 1.0.x = the pre-plan skill; 1.1.0-dev = plan execution in staging (Phases 0-8),
# released 1.1.0 at the S9.2 promotion gate. S0.4.
# 1.2.0 = T9.1/T9.2 onboarding (ADR 0007): prefixless keys, per-playlist
# top-level transcript dirs, self-resolving keyword cites, claims contract.
# 1.2.23 = B-wave CLI migration: gates + coverage + build-meh + render-tool-docs
#          as registry commands (shelf_core/gatelib.py one home; scripts/ become
#          re-export shims); PEP 562 lazy-ROOT consumers (build-meh resolver)
__version__ = "1.2.23"
