# -*- coding: utf-8 -*-
"""registry — the ONE command table (P6.5).

Name -> module:function + help + argparse spec. cli.build_parser iterates it
for help; dispatch.main iterates it for execution. Adding a command is one
entry here — help and dispatch follow by construction, so the hand-written
lists that went stale twice (missing sync-docs, then shamela) cannot exist.

Args spec: (name, kwargs) tuples; a leading '-' makes it an option.

D8.14: each entry may carry a `describe` contract — checks performed, exit
codes, PITFALLS taxonomy tags, ADR links. `--describe` (dispatch) emits it;
the skill's renderer generates references/tools/<name>.md from the SAME
table (ADR 0006: the per-file view is generated, never hand-kept).
"""
from __future__ import annotations

COMMANDS = {
    "inventory": {
        "module": "inventory", "func": "cmd_inventory",
        "help": "index all sessions -> reference/inventory.md (--out PATH for T7.1 selftest)",
        "args": [("--out", {"nargs": 1})],
        "describe": {
            "checks": ["session index vs config playlists", "note presence + status per session"],
            "exits": {"0": "wrote the inventory", "2": "no config/gates resolution (loud)"},
            "pitfalls": ["two-truths: PLAYLIST_DIRS drives the rendered list (P6.10 header receipt)"],
            "adrs": ["0002"],
        },
    },
    "lines": {
        "module": "lines", "func": "cmd_lines",
        "help": "numbered view of clean transcript",
        "args": [("key", {}), ("lo", {"nargs": "?"}), ("hi", {"nargs": "?"})],
        "describe": {
            "checks": ["key resolves to an indexed session"],
            "exits": {"0": "printed range", "1": "usage (bad KEY or non-numeric lo/hi)", "2": "no session for key"},
            "pitfalls": ["P6.10: prose lo/hi printed int() traceback — now usage"],
            "adrs": ["0002"],
        },
    },
    "lift": {
        "module": "lift", "func": "cmd_lift",
        "help": "paste-ready quotes from stdin phrases",
        "args": [("key", {})],
        "describe": {
            "checks": ["stdin phrases -> verbatim spans via CleanSource/subseq (V1.4 fallback)"],
            "exits": {"0": "units printed", "1": "NOTFOUND/NOSLICE phrases reported"},
            "pitfalls": ["never retype ASR — spans are sliced (correctness-by-construction)"],
            "adrs": ["0001"],
        },
    },
    "pins": {
        "module": "pins", "func": "cmd_pins",
        "help": "verify every quote's minute (exit 0 = clean)",
        "args": [("--fix", {"action": "store_true"}), ("targets", {"nargs": "+"})],
        "describe": {
            "checks": ["cited quote spans vs transcript (minute + presence)",
                       "uncited blockquote evidence (hard)", "uncited inline (advisory)",
                       "NOTHING-WAS-VERIFIED: 0 checks with quoted spans = exit 1"],
            "exits": {"0": "all flags clean", "1": "flags raised", "2": "note/session unresolvable (loud)"},
            "pitfalls": ["comma bug class -> NOTHING-WAS-VERIFIED guard",
                         "ambiguous find_note refuses, never silent"],
            "adrs": ["0001", "0004"],
        },
    },
    "scaffold": {
        "module": "scaffold", "func": "cmd_scaffold",
        "help": "blank session note(s) from template",
        # --from-yaml/--from-json must be accepted HERE so argv reaches
        # cmd_scaffold's shim (which forwards to draft-note). argparse would
        # otherwise reject them before the shim ever runs (dead-shim bug).
        "args": [("target", {}), ("--topics", {"action": "store_true"}),
                 ("--from-yaml", {"dest": "from_yaml"}),
                 ("--from-json", {"action": "store_true"}),
                 ("--from-notes", {"dest": "from_notes"}), ("title", {"nargs": "?"})],
        "describe": {
            "checks": ["one-write: refuses existing note/doc without --force",
                       "doc --from-notes: reports stitched AND skipped sections (P6.9)",
                       "bare range binds DEFAULT_PLAYLIST (P6.1)"],
            "exits": {"0": "note/doc written", "1": "usage", "2": "zero-match scope (loud, P6.1/P6.2)"},
            "pitfalls": ["W4.21: note discovery via find_note (ambiguity-refusing)"],
            "adrs": ["0002"],
        },
    },
    "draft": {
        "module": "draft", "func": "cmd_draft",
        "help": "doc draft from filled session note",
        "args": [("key", {})],
        "describe": {
            "checks": ["one-write: refuses existing output doc"],
            "exits": {"0": "doc drafted", "1": "note missing/unusable"},
            "pitfalls": [],
            "adrs": [],
        },
    },
    "draft-note": {
        "module": "draft_note", "func": "cmd_draft_note",
        "help": "scripted note builder from MEH.yaml (via verified matcher, PITFALLS.md A/C/H)",
        "args": [("key", {}), ("--from-yaml", {"dest": "from_yaml"}),
                 ("--from-json", {"action": "store_true"}),
                 ("--force", {"action": "store_true",
                              "help": "regenerate an existing note (discard applied verdicts)"})],
        "describe": {
            "checks": ["MEH spec shape validated in ONE pass (title/axes/khu)",
                       "quotes sliced from transcript by construction"],
            "exits": {"0": "note written", "1": "no MEH input / shape invalid",
                      "2": "session unresolvable"},
            "pitfalls": ["Pitfall A/C/H (PITFALLS.md): never retype quotes",
                         "never re-run --from-yaml against a finished note (clobbers polish)"],
            "adrs": ["0001"],
        },
    },
    "evdoc": {
        "module": "evdoc", "func": "cmd_evdoc",
        "help": "evidence-doc one-write from EVIDOC.yaml (doc-side mirror of draft-note)",
        "args": [("--from-yaml", {"dest": "from_yaml"}), ("--out", {"nargs": "?"}),
                 ("--dump", {}), ("--seed", {})],
        "describe": {
            "checks": ["probe resolution against the note cite-pool (W4.17 ambiguity, W4.18 stale)",
                       "frame-length lint (shared min_para_chars, P6.14)",
                       "placeholder check BEFORE {body} (P6.14)"],
            "exits": {"0": "doc built", "1": "probe/STALE failures", "2": "spec/template missing"},
            "pitfalls": ["probes <12 chars warn (weak anchors)",
                         "cite_kw defaults EMPTY — no keyword assumption"],
            "adrs": ["0001"],
        },
    },
    "verify": {
        "module": "verify", "func": "cmd_verify",
        "help": "verification lane",  # sub-actions listed from verify.COMMANDS
        "args": [("action", {"nargs": "?"}), ("rest", {"nargs": "*"}),
                 ("--key", {}), ("--ref", {}), ("--stem", {}),
                 ("--phrase", {}), ("--title", {}), ("--from-json", {"dest": "from_json"}),
                 ("--find", {}),  # verify quran --find "asr phrase" (Pitfall R: register in the SAME edit)
                 ("--amend", {"action": "store_true"}), ("--out", {}),
                 ("--bodies", {"action": "store_true"}), ("--dry", {"action": "store_true"}),
                 ("--add-section", {"action": "store_true"}),
                 ("--json", {"action": "store_true"})],  # machine-readable output (shamela find)
        "describe": {
            "checks": ["quran/hadorith/history channel routing (references/VERIFICATION.md)",
                       "worklist completion meter (0 unique = shelf verified)",
                       "sync-docs: the ONLY notes->docs direction"],
            "exits": {"0": "lane ok", "1": "unverified entries", "2": "usage/config loud"},
            "pitfalls": ["sync-docs --dry idempotency",
                         "a doc is never a source (one-way core model)"],
            "adrs": ["0001"],
        },
    },
    "check": {
        "module": "check", "func": "cmd_check",
        "help": "gate: all | playlist | block | KEY | path",
        "args": [("scope", {"nargs": "?"})],
        "describe": {
            "checks": ["every doc quote vs transcript", "links resolve", "note statuses valid",
                       "unrecognized note-name grammar announced (P6.4)"],
            "exits": {"0": "intact", "1": "fails listed", "2": "no corpus resolved / scoped zero-match (W4.4, P6.2)"},
            "pitfalls": ["file branch sets n_docs/n_notes (T7.1 was: UnboundLocalError)"],
            "adrs": ["0002", "0004"],
        },
    },
    "doctor": {
        "module": "doctor", "func": "cmd_doctor",
        "help": "diagnose: resolved root, config, grammar, paths, playlists (read-only)",
        "args": [],
        "describe": {
            "checks": ["config resolution (present/absent/corrupt-loud)", "grammar values active",
                       "data paths exist", "why-pointers to DESIGN (D8.10)"],
            "exits": {"0": "report printed (additive — never a gate, ADR 0005)"},
            "pitfalls": ["config absence is silent EN defaults BY DESIGN (C3.3)"],
            "adrs": ["0002", "0005"],
        },
    },
    "lint": {
        "module": "lint", "func": "cmd_lint",
        "help": "intake check: categorized note findings (key/status/flags/ufffd/script/cite)",
        "args": [("targets", {"nargs": "*"})],
        "describe": {
            "checks": ["key grammar", "status/flags whole-value (A5.6)", "U+FFFD",
                       "script convention", "cite-like timecodes without cite"],
            "exits": {"0": "no findings", "1": "findings listed (additive intake, ADR 0005)"},
            "pitfalls": ["template notes exempt (قالب/template/skeleton)"],
            "adrs": ["0005"],
        },
    },
    "quotes": {
        "module": "quotes", "func": "cmd_quotes",
        "help": "diagnostic: extract all quoted spans",
        "args": [],
        "describe": {
            "checks": ["quoted spans extracted per config quote style (read-only diagnostic)"],
            "exits": {"0": "spans printed"},
            "pitfalls": [],
            "adrs": [],
        },
    },
    "selftest": {
        "module": "selftest", "func": "cmd_selftest",
        "help": "fixture-based self test",
        "args": [],
        "describe": {
            "checks": ["20 named guards over its OWN fixture corpus (T7.1/T7.2)",
                       "inventory regen inside the fixture (--out)",
                       "outer reference/ untouched"],
            "exits": {"0": "all pass", "1": "failed list printed"},
            "pitfalls": ["fixture corpus = self-built (ADR 0004); fresh-clone capable"],
            "adrs": ["0004"],
        },
    },
}
