"""evdoc — evidence-doc one-write from EVIDOC.yaml (doc-side mirror of MEH.yaml).

Usage:
  shelf evdoc --seed KEY,KEY          # frame pre-draft: khu digests + longest
                                      # pool quotes per note, to humanize
  shelf evdoc --dump KEY,KEY          # blueprint authoring: print cite-pool,
                                      # pre-verified per quote (ok/STALE)
  shelf evdoc --from-yaml EVIDOC.yaml [--out name.html]

Contract (mirrors draft-note):
  - quotes resolve from the note cite-pool by probe prefix; a bad probe
    FAILS LOUDLY with the closest candidates (never a silent skeleton)
  - every resolved quote is re-verified against the transcript BEFORE
    writing (a stale note cite fails the build, not the doc)
  - the pool is harvested with the SAME parser the note gate uses
    (shelf_core.notes.scan_lines) — no regex fork that can drift from
    the gate's grammar
  - frames shorter than the substantive-prose threshold (300 chars) warn
    before doc-gate does
  - HTML comes from templates/<corpus.doc_template> (default
    evidence-doc.html) with {placeholders}; shelves can drop their own
"""
import sys, re, glob as _glob
from pathlib import Path


def _imports():
    # H2.2: flat fallback removed
    from shelf_core.config import load_config, find_root, corpus_cfg
    from shelf_core.playlists import docs_dir
    from shelf_core.match import tokens
    from shelf_core.transcript import found_minutes
    from shelf_core.notes import scan_lines, find_note, khu_rows
    from shelf_core.transcript import check_quote, CleanSource
    from shelf_core.citation import fmt_cite, fmt_mmss
    return (load_config, find_root, corpus_cfg, docs_dir, tokens, found_minutes, khu_rows,
            scan_lines, fmt_mmss, find_note, check_quote, CleanSource)


def parse_any(secs):
    if isinstance(secs, str) and ":" in secs:
        parts = [int(x) for x in secs.split(":")]
        while len(parts) < 3:
            parts.insert(0, 0)
        return parts[-1] + parts[-2] * 60 + parts[-3] * 3600
    return int(secs)


def _note_files(root, sk):
    # W4.21: resolve via find_note (registry + loud ambiguity refusal) instead
    # of a first-hit glob that silently picked among duplicate notes.
    p = find_note(sk)
    return [str(p)] if p else []


def _harvest(root, scan_lines):
    """quote -> (key, secs) using the gate's own parser. First occurrence wins."""
    pool = {}
    for n in _glob.glob(str(root / "reference" / "notes" / "*.md")):
        for rec in scan_lines(Path(n).read_text(encoding="utf-8")):
            q = rec.get("quote") or ""
            if not rec.get("cited") or len(q) < 12 or len(q) > 240:
                continue
            pool.setdefault(q, (rec["key"], rec["secs"]))
    return pool


def _seed(keys_raw, root, scan_lines, tokens, found_minutes):
    """Frame pre-draft: per note, khu digest lines + 3 longest pool quotes —
    scaffolding for the author to humanize into frames (never shipped)."""
    for sk in [k.strip() for k in keys_raw.split(",") if k.strip()]:
        hits = _note_files(root, sk)
        if not hits:
            print(f"== {sk}: no note")
            continue
        txt = Path(hits[0]).read_text(encoding="utf-8")
        print(f"== {sk}")
        # khu digest via the parse layer (A5.3 audit: the numbered-table row
        # grammar lives in notes.khu_rows alone).
        for ktext in khu_rows(txt):
            print(f"  [khu] {ktext}")
        recs = [r for r in scan_lines(txt) if r.get("cited")]
        for r in sorted(recs, key=lambda r: -len(r["quote"]))[:3]:
            key = r["key"] if r["key"].startswith(("is-", "rr-")) else f"is-{int(r['key']):03d}"
            ok = "ok" if found_minutes(key, tokens(r["quote"])) else "STALE"
            print(f"  [q {ok} {r['key']} {r['secs']}] {r['quote'][:90]}")


def _pool_dump(keys_raw, root, scan_lines, tokens, found_minutes):
    """Blueprint-authoring helper: print the cite-pool for notes, each entry
    pre-verified against the transcript (ok/STALE), so probes are PICKED
    from a menu instead of grepped by hand."""
    for sk in [k.strip() for k in keys_raw.split(",") if k.strip()]:
        hits = _note_files(root, sk)
        if not hits:
            print(f"== {sk}: no note")
            continue
        print(f"== {sk}")
        seen = set()
        for r in scan_lines(Path(hits[0]).read_text(encoding="utf-8")):
            q = r.get("quote") or ""
            if not r.get("cited") or q in seen:
                continue
            seen.add(q)
            key = r["key"] if r["key"].startswith(("is-", "rr-")) else f"is-{int(r['key']):03d}"
            ok = "ok   " if found_minutes(key, tokens(q)) else "STALE"
            print(f"  [{ok} {r['key']} {r['secs']}] {q[:96]}")


def cmd_evdoc(argv):
    (load_config, find_root, corpus_cfg, docs_dir, tokens, found_minutes, khu_rows,
     scan_lines, fmt_mmss, find_note, check_quote, CleanSource) = _imports()
    yaml_path, out_override, dump_keys, seed_keys = None, None, None, None
    allow_ambiguous = False   # W4.17: explicit escape hatch for cross-key probes
    i = 0
    while i < len(argv):
        if argv[i] == "--allow-ambiguous":
            allow_ambiguous = True; i += 1; continue
        if argv[i] == "--from-yaml" and i + 1 < len(argv):
            yaml_path = Path(argv[i + 1]); i += 2; continue
        if argv[i] == "--out" and i + 1 < len(argv):
            out_override = argv[i + 1]; i += 2; continue
        if argv[i] == "--dump" and i + 1 < len(argv):
            dump_keys = argv[i + 1]; i += 2; continue
        if argv[i] == "--seed" and i + 1 < len(argv):
            seed_keys = argv[i + 1]; i += 2; continue
        i += 1
    cfg = load_config()
    root = find_root()
    if seed_keys:
        return _seed(seed_keys, root, scan_lines, tokens, found_minutes)
    if dump_keys:
        return _pool_dump(dump_keys, root, scan_lines, tokens, found_minutes)
    if not yaml_path or not yaml_path.exists():
        sys.exit("usage: evdoc --from-yaml EVIDOC.yaml [--out name.html] | "
                 "evdoc --dump KEY,KEY | evdoc --seed KEY,KEY")

    try:
        import yaml
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    except Exception as e:
        sys.exit(f"Failed to load YAML {yaml_path}: {e}")
    if not isinstance(data, dict) or "sections" not in data:
        sys.exit("EVIDOC must be a mapping with top-level 'sections:' (see templates/EVIDOC.yaml)")
    sections = data.get("sections") or []
    meta = data.get("meta") or {}
    if not sections:
        sys.exit("EVIDOC parsed to 0 sections — refusing to write a shell")

    # C3.8: corpus section via the ONE loader helper (was cfg.get re-derivation)
    corpus = corpus_cfg(cfg, root)
    # P6.14: cite_kw defaults EMPTY — a shelf that hasn't configured a keyword
    # gets no keyword assumption (the retired 'المجلس' default was another
    # shelf's vocabulary leaking into every build).
    cite_kw = corpus.get("cite_pattern", "")
    anchor = meta.get("anchor", "is")

    pool = _harvest(root, scan_lines)
    if not pool:
        sys.exit("cite-pool empty: scan_lines found no cited quotes in reference/notes/")

    QO = corpus.get("quote", {}).get("open", "«")
    QC = corpus.get("quote", {}).get("close", "»")
    # P6.14: shared with doc-gate — one key, one threshold (default 300).
    frame_min = int(((cfg.get("gates") or {}).get("essay_proxy") or {}).get("min_para_chars", 300))
    fails, warns, num_q, paras = [], [], 0, 0
    body = []
    for sec in sections:
        title = sec.get("title") or "?"
        kind = sec.get("kind", "quotes")
        per_para = int(sec.get("per_para", 2))
        slug = re.sub(r"[^\w-]", "-", title)[:30]
        body.append(f'\n<h2 id="{slug}">{title}</h2>')
        frame = (sec.get("frame") or "").strip()
        if len(frame) < frame_min:
            warns.append(f"frame < {frame_min} chars: {title[:40]} (doc-gate substantive para)")
        if frame:
            body.append(f"<p>{frame}</p>"); paras += 1
        if kind == "prose":
            continue
        if kind == "list":
            body.append("<ul>")
            for it in sec.get("items", []):
                # list items are free text: «» without a same-line cite would
                # fail check (doc hard lane) — warn at generation time. Only
                # well-defined when a cite keyword IS configured (P6.14: the
                # empty default would make the containment test vacuous).
                if cite_kw:
                    for qq in re.findall(r"«([^»]+)»", it):
                        if cite_kw not in it.split(qq)[-1][:80]:
                            warns.append(f"list item has «» without same-line cite: …{qq[:40]}… "
                                         "(de-quote or add cite)")
                body.append(f"  <li>{it}</li>"); paras += 1
            body.append("</ul>")
            continue
        meta_bits = []
        for item in sec.get("quotes", []):
            probe, intro = item.get("probe", ""), item.get("intro", "")
            # P6.14: a probe under 12 chars is a weak anchor — it prefix-matches
            # half the pool and the nearest-3 suggestion on a miss is noise.
            # Warn, don't fail: a deliberate short probe is the author's call.
            if len(probe) < 12:
                warns.append(f"probe < 12 chars ({probe!r}) in {title[:40]} — weak anchor, "
                             "prefix-matches broadly; extend it to the distinctive span")
            # W4.17: optional per-item `key:` scope; unscoped probes that span
            # MULTIPLE session keys refuse loudly (or run with --allow-ambiguous)
            # — silent first-hit-wins across sessions wrote the wrong session's
            # words into the doc under this section's frame.
            scope = item.get("key")
            hits = [(qq, v) for qq, v in pool.items()
                    if qq.startswith(probe) and (not scope or str(v[0]) == scope)]
            if not hits:
                close = sorted(pool, key=lambda q: sum(1 for a, b in zip(q, probe) if a == b), reverse=True)[:3]
                fails.append((title[:30], probe[:40], close))
                continue
            keys_hit = sorted({str(v[0]) for _q, v in hits})
            if len(keys_hit) > 1 and not allow_ambiguous:
                fails.append((title[:30],
                              f"AMBIGUOUS probe {probe[:40]!r}: {' / '.join(keys_hit)}"
                              " — add 'key: <session>' to the item or run with --allow-ambiguous",
                              []))
                continue
            qq, (nkey, secs) = hits[0]
            # pre-verify: note cite must still locate the quote in the transcript
            # W4.19: was nkey.startswith(("is-","rr-")) — hardcoded prefixes
            # crashed int() on any other slug ("fx-001" -> ValueError). A key
            # containing "-" is already whole; only bare numbers get the anchor.
            key = nkey if "-" in nkey else f"{anchor}-{int(nkey):03d}"
            # W4.18: pre-verify via the GATE (check_quote — gate-asking), not a
            # presence-only found_minutes probe: a quote present elsewhere at
            # the wrong minute is MISMATCH and refuses the build, parity with
            # draft_note's receipted doctrine.
            verdict, _msg = check_quote(CleanSource(key), qq, secs or [], "", key)
            if verdict in ("MISSING", "MISMATCH"):
                fails.append((title[:30], f"STALE note cite {nkey} {secs}: {qq[:60]} ({verdict})", []))
                continue
            num_q += 1
            sec = secs[0] if isinstance(secs, list) else parse_any(secs)
            meta_bits.append(f'{intro} {QO}{qq}{QC} <span class="cite">{cite_kw} {key.split("-")[-1]}، {fmt_mmss(sec)}</span>')
            if len(meta_bits) >= per_para:
                body.append("<p>" + " ".join(meta_bits) + "</p>"); paras += 1; meta_bits = []
        if meta_bits:
            body.append("<p>" + " ".join(meta_bits) + "</p>"); paras += 1
    if fails:
        sys.exit("PROBE/STALE FAILURES (loud, see templates/EVIDOC.yaml):\n" + "\n".join(
            f"  [{t}] {p} — closest: {[c[:30] for c in cl]}" for t, p, cl in fails))

    html = _render(root, corpus, meta, cite_kw, "\n".join(body))
    dest = docs_dir(anchor)
    if out_override:
        out = dest / out_override
    else:
        raw = re.sub(r"[^\w\u0600-\u06FF]+", "-", meta.get("title", ""))
        slug = raw.strip("-")[:48] or "doc"
        out = dest / f"{meta.get('range', 'doc')}-{slug}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and "--force" not in argv:
        # W4.2: same one-write doctrine as cmd_draft/W4.1 — a rebuilt doc
        # silently replaced whatever edits landed on the rendered file.
        sys.exit(f"Already exists: {out} — use --force to regenerate")
    out.write_text(html, encoding="utf-8")
    print(f"BUILT -> {out} ({len(sections)} sections, {num_q} quotes, {paras} paras)")
    for w in warns:
        print(f"  WARN {w}")
    print(f"next: python3 tools/shelf.py check {out} && python3 scripts/doc-gate.py {out}")


def _render(root, corpus, meta, cite_kw, body):
    tpl_name = corpus.get("doc_template", "evidence-doc.html")
    tpl_path = Path(root) / "templates" / tpl_name
    if not tpl_path.exists():
        sys.exit(f"doc template missing: {tpl_path} (corpus.doc_template={tpl_name!r})")
    tpl = tpl_path.read_text(encoding="utf-8")
    html = (tpl.replace("{title}", meta.get("title", ""))
               .replace("{kicker}", meta.get("kicker", ""))
               .replace("{range}", meta.get("range", ""))
               .replace("{source}", meta.get("source_range", ""))
               .replace("{date}", meta.get("review_date", ""))
               .replace("{cite}", cite_kw))
    # P6.14: the unresolved-placeholder check runs BEFORE {body} insertion —
    # a quote containing {word} (a code sample, a shell snippet) must not kill
    # the build; only TEMPLATE placeholders count as unresolved. {body} itself
    # is a template placeholder and is excluded (it is about to be filled).
    left = [x for x in re.findall(r"\{\w+\}", html) if x != "{body}"]
    if left:
        sys.exit(f"template placeholders unresolved: {left[:5]}")
    return html.replace("{body}", body)
