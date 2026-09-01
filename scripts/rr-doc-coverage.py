#!/usr/bin/env python3
"""rr-doc-coverage: compat shim -> doc-coverage.py (v2 two-tier). H2.6: runpy
instead of exec(open(...)) — documented semantics, correct __file__, real
tracebacks."""
import os
import runpy
import sys

sys.argv[0] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "doc-coverage.py")
runpy.run_path(sys.argv[0], run_name="__main__")
