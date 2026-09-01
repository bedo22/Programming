#!/usr/bin/env python3
"""rr-doc-gate: compat shim -> doc-gate.py (v2 two-tier). Investing keeps rr-
defaults via no-config fallback. H2.6: runpy instead of exec(open(...)) —
documented semantics, correct __file__, real tracebacks."""
import os
import runpy
import sys

sys.argv[0] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "doc-gate.py")
runpy.run_path(sys.argv[0], run_name="__main__")
