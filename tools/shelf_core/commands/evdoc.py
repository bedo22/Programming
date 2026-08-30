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
    try:
        from shelf_core.config import load_config, find_root
        from shelf_core.playlists import docs_dir
        from shelf_core.match import tokens
        from shelf_core.transcript import found_minutes
        from shelf_core.notes import scan_lines
        from shelf_core.citation import fmt_mmss
    except ImportError:
        from config import load_config, find_root  # type: ignore
        from playlists import docs_dir  # type: ignore
        from match import tokens  # type: ignore
        from transcript import found_minutes  # type: ignore
        from notes import scan_lines  # type: ignore
        from citation import fmt_mmss  # type: ignore
    return load_config, find_root, docs_dir, tokens, found_minutes, scan_lines, fmt_mmss


def parse_any(secs):
    if isinstance(secs, str) and ":" in secs:
        parts = [int(x) for x in secs.split(":")]
        while len(parts) < 3:
            parts.insert(0, 0)
        return parts[-1] + parts[-2] * 60 + parts[-3] * 3600
    return int(secs)


def _note_files(root, sk):
    return _glob.glob(str(root / "reference" / "notes" / f"{sk}-*.md"))


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
        # khu digest: المحاور table rows / bold titles
        for line in txt.splitlines():
            if "المحاور" in line or re.match(r"^\| *المحور", line):
                continue
            m = re.match(r"^\|\s*\d+\s*\|\s*([^|]{10,80})\|", line)
            if m:
                print(f"  [khu] {m.group(1).strip()}")
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
    (load_config, find_root, docs_dir, tokens, found_minutes, scan_lines, fmt_mmss) = _imports()
    yaml_path, out_override, dump_keys, seed_keys = None, None, None, None
    i = 0
    while i < len(argv):
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

    corpus = cfg.get("corpus", {})
    cite_kw = corpus.get("cite_pattern", "المجلس")
    anchor = meta.get("anchor", "is")

    pool = _harvest(root, scan_lines)
    if not pool:
        sys.exit("cite-pool empty: scan_lines found no cited quotes in reference/notes/")

    QO = corpus.get("quote", {}).get("open", "«")
    QC = corpus.get("quote", {}).get("close", "»")
    frame_min = 300  # mirrors doc-gate substantive-para threshold
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
                # fail check (doc hard lane) — warn at generation time
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
            hits = [(qq, v) for qq, v in pool.items() if qq.startswith(probe)]
            if not hits:
                close = sorted(pool, key=lambda q: sum(1 for a, b in zip(q, probe) if a == b), reverse=True)[:3]
                fails.append((title[:30], probe[:40], close))
                continue
            qq, (nkey, secs) = hits[0]
            # pre-verify: note cite must still locate the quote in the transcript
            key = nkey if nkey.startswith(("is-", "rr-")) else f"{anchor}-{int(nkey):03d}"
            if not found_minutes(key, tokens(qq)):
                fails.append((title[:30], f"STALE note cite {nkey} {secs}: {qq[:60]}", []))
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
               .replace("{cite}", cite_kw)
               .replace("{body}", body))
    if "{" in html and "}" in html and re.search(r"\{\w+\}", html):
        left = re.findall(r"\{\w+\}", html)
        sys.exit(f"template placeholders unresolved: {left[:5]}")
    return html
