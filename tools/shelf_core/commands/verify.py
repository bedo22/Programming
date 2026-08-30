"""verify — the tooling half of VERIFICATION.md (doctrine lives in references/).

Why this exists: the verify lane had rules but no commands, so every drain was
hand-rolled python + raw HTTP. This makes it one-write and idempotent like
draft-note/evdoc: harvest -> channel adapters (cached) -> apply verdicts.

Usage:
  shelf verify worklist [--key is-NNN]     # open items -> deduped worklist JSON
  shelf verify quran --ref 24:11 [--stem "..."]   # api.quran.com + containment grade
  shelf verify dorar "نص الحديث"            # dorar grade cards (scrapling stealth)
  shelf verify locate "عبارة" [--book X]     # ar.wikisource search + located context
  shelf verify shamela find "<title>"        # local Shamela catalogue: edition, printed pagination, citable url (LOCATE only, never a verdict)
  shelf verify apply --from-json VERDICTS.json [--dossier is-024/slug]
                                            # write dossier + update note rows IN PLACE

Caching: every fetch is stored under _verify/.cache/<sha1>.json and reused, so
re-running a drain costs no network and cannot drift between runs.
"""
import sys, os, re, json, glob, hashlib, subprocess, time, urllib.request, urllib.parse
from pathlib import Path

from shelf_core.match import norm_uthmani as norm  # single owner: shelf_core/match.py (see the note there)

UA = {"User-Agent": "shelf-verify/1.0 (shelf-pipeline skill)"}


def _root():
    try:
        from shelf_core.config import find_root
    except ImportError:
        from config import find_root  # type: ignore
    return find_root()


def _cache_dir(root):
    d = Path(root) / "_verify" / ".cache"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _cached(key, fetch):
    """fetch() runs only on cache miss; returns parsed JSON."""
    h = hashlib.sha1(key.encode("utf-8")).hexdigest()[:16]
    p = _CACHE / f"{h}.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8")), "cache"
        except Exception:
            pass
    data = fetch()
    p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return data, "live"





# ---------------------------------------------------------------- worklist
SURA = {"الفاتحة":1,"البقرة":2,"آل عمران":3,"النساء":4,"المائدة":5,"الأنعام":6,"الأعراف":7,
 "الأنفال":8,"التوبة":9,"يونس":10,"هود":11,"يوسف":12,"الرعد":13,"إبراهيم":14,"النحل":16,
 "الإسراء":17,"الكهف":18,"مريم":19,"طه":20,"الأنبياء":21,"الحج":22,"المؤمنون":23,"النور":24,
 "الفرقان":25,"الشعراء":26,"النمل":27,"القصص":28,"العنكبوت":29,"الروم":30,"لقمان":31,
 "السجدة":32,"الأحزاب":33,"سبأ":34,"فاطر":35,"يس":36,"الصافات":37,"ص":38,"الزمر":39,
 "غافر":40,"فصلت":41,"الشورى":42,"الزخرف":43,"الدخان":44,"الجاثية":45,"الأحقاف":46,
 "محمد":47,"الفتح":48,"الحجرات":49,"ق":50,"الذاريات":51,"الطور":52,"النجم":53,"القمر":54,
 "الرحمن":55,"الواقعة":56,"الحديد":57,"المجادلة":58,"الحشر":59,"الممتحنة":60,"الصف":61,
 "الجمعة":62,"المنافقون":63,"التغابن":64,"الطلاق":65,"التحريم":66,"الملك":67,"القلم":68,
 "الحاقة":69,"المعارج":70,"نوح":71,"الجن":72,"المزمل":73,"المدثر":74,"القيامة":75,
 "الإنسان":76,"المرسلات":77,"النبأ":78,"النازعات":79,"عبس":80,"التكوير":81,"الانفطار":82,
 "المطففين":83,"الانشقاق":84,"البروج":85,"الطارق":86,"الأعلى":87,"الغاشية":88,"الفجر":89,
 "البلد":90,"الشمس":91,"الليل":92,"الضحى":93,"الشرح":94,"التين":95,"العلق":96,"القدر":97,
 "البينة":98,"الزلزلة":99,"العاديات":100,"القارعة":101,"التكاثر":102,"العصر":103,
 "الهمزة":104,"الفيل":105,"قريش":106,"الماعون":107,"الكوثر":108,"الكافرون":109,"النصر":110,
 "المسد":111,"الإخلاص":112,"الفلق":113,"الناس":114}
SURA_NUM = {v: k for k, v in SURA.items()}
DONE_RE = re.compile(r"متحقق|_verify/|api\.quran\.com|dorar\.net/hadith/\d+|quran\.com/\d+/\d+|"
                     r"ar\.wikisource\.org/wiki")
QURAN_RE = re.compile(r"آية|القرآن|سورة|quran", re.I)
HADITH_RE = re.compile(r"حديث|منسوب.*النبي|رواه|أخرجه|بخاري|مسلم|ترمذي|أبو داود|نسائي|"
                       r"ابن ماجه|مسند|dorar|sunnah|موضوع|ضعيف|صحيح|الألباني|الأرناؤوط", re.I)


def _items_of(path):
    txt = Path(path).read_text(encoding="utf-8")
    sec = re.search(r"## نصوص وآثار(.*?)(?=\n## |\Z)", txt, re.S)
    if not sec:
        return []
    out = []
    for block in re.split(r"\n(?=\s*\d+\.\s+\*\*)", sec.group(1)):
        # A row WITHOUT any verdict line is the most open row there is. Skipping it made
        # the meter report 0 while 67 rows had never entered the queue at all.
        if "التحقق" not in block and not re.search(r">\s*«", block):
            continue
        t = re.search(r"\*\*(.+?)\*\*", block)
        q = re.search(r">\s*«([^»]+)»", block)
        v = re.search(r"التحقق[:：]?\s*([^\n]+)", block)
        out.append({"title": (t.group(1) if t else "").strip(),
                    "quote": (q.group(1) if q else "").strip(),
                    "ver": (v.group(1) if v else "").strip()})
    return out


def _ayah_ref(item):
    blob = item["title"] + " " + item["ver"]
    for name, num in SURA.items():
        m = re.search(re.escape(name) + r"[^\d]{0,12}(\d{1,3})", blob)
        if m:
            return f"{num}:{m.group(1)}"
    m = re.search(r"(\d{1,3}):(\d{1,3})", blob)
    return m.group(0) if m else None


def cmd_worklist(argv):
    root = _root()
    only = argv[argv.index("--key") + 1] if "--key" in argv else None
    notes = sorted(glob.glob(str(root / "reference" / "notes" / "is-0[0-4][0-9]-*.md")),
                   key=lambda p: os.path.basename(p)[:6])
    uniq, per_note = {}, {}
    for n in notes:
        k = os.path.basename(n)[:6]
        if only and k != only:
            continue
        counts = per_note.setdefault(k, {})
        for it in _items_of(n):
            if DONE_RE.search(it["ver"]):
                counts["done"] = counts.get("done", 0) + 1
                continue
            blob = it["title"] + " " + it["ver"]
            cls = "quran" if QURAN_RE.search(blob) else ("hadith" if HADITH_RE.search(blob) else "report")
            counts[cls] = counts.get(cls, 0) + 1
            stem = norm(it["quote"]) or norm(it["title"])
            if not stem:
                continue
            rec = uniq.setdefault(stem, {"cls": cls, "quote": it["quote"] or it["title"],
                                         "notes": [], "ayah": None, "ver": it["ver"][:120]})
            rec["notes"].append(k)
            if cls == "quran" and not rec["ayah"]:
                rec["ayah"] = _ayah_ref(it)
    out = {"unique": len(uniq), "items": list(uniq.values()), "per_note": per_note}
    dest = root / "plans" / "khilafah-verification" / "worklist.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    by = {}
    for r in out["items"]:
        by[r["cls"]] = by.get(r["cls"], 0) + 1
    print(f"OPEN rows {sum(sum(v.values()) for v in per_note.values())} -> {len(uniq)} unique texts {by}")
    print(f"saved {dest.relative_to(root)}")


# ---------------------------------------------------------------- quran
def _quran_verse(root, ref):
    global _CACHE
    _CACHE = _cache_dir(root)
    data, src = _cached(f"quran:{ref}", lambda: json.loads(urllib.request.urlopen(
        urllib.request.Request(
            f"https://api.quran.com/api/v4/verses/by_key/{ref}?fields=text_uthmani", headers=UA),
        timeout=25).read().decode("utf-8")))
    return re.sub(r"\s+", " ", data["verse"]["text_uthmani"]), src


def cmd_quran(argv):
    root = _root()
    # _CACHE is module-global and _cached() reads it directly: it must be initialised HERE, at
    # the command head, not inside a helper -- the --find path calls _cached() for the search
    # before any verse fetch runs, and died with NameError when the init lived in _quran_verse.
    global _CACHE
    _CACHE = _cache_dir(root)
    ref = argv[argv.index("--ref") + 1] if "--ref" in argv else None
    stem = argv[argv.index("--stem") + 1] if "--stem" in argv else None
    find = argv[argv.index("--find") + 1] if "--find" in argv else None

    if find and not ref:
        # api.quran.com/v4/search is a WORD-level index: it PROPOSES verses, it never confirms
        # one. Measured: "ارأيت الذي ينهى" and the ASR-mangled "اراييت الذي ينهي" both return
        # 96:9 first, out of ~260 word-matched results -- tolerant enough to find a verse from a
        # garbled transcript, noisy enough that a top hit means nothing on its own. So every
        # candidate is re-read and re-graded with the SAME containment check --ref uses. A search
        # hit is a locate; the citation still has to earn the verdict.
        data, src = _cached(f"quran-search:{find}", lambda: json.loads(urllib.request.urlopen(
            urllib.request.Request("https://api.quran.com/api/v4/search?" +
                                   urllib.parse.urlencode({"q": find, "size": 5}), headers=UA),
            timeout=25).read().decode("utf-8")))
        cands = [r.get("verse_key") for r in (data.get("search") or {}).get("results") or [] if r.get("verse_key")]
        print(f"quran --find {find!r}: {len(cands)} candidate verse(s) [{src}]")
        print("  search is word-level -- these are proposals, not matches. Grading each:")
        out = []
        for k in cands[:5]:
            txt, _ = _quran_verse(root, k)
            aw = [w for w in norm(find).split() if len(w) > 2]
            u = norm(txt)
            hit = sum(1 for w in aw if w in u)
            exact = norm(find) in u
            status = "MATCH" if exact else (f"partial {hit}/{len(aw)}" if aw else "?")
            n, a = k.split(":")
            print(f"  {k:<9} {status:<14} {txt[:64]}")
            if exact:
                out.append({"ref": k, "uthmani": txt, "status": status, "via": "search"})
        if not out:
            print("  NO candidate carries the phrase contiguously -- this is NOT a verse match.")
            print("  Re-core with fewer distinctive words, or mark للشيخ. Do not cite the top hit.")
        return out

    if not ref:
        sys.exit('usage: verify quran --ref SURAH:AYAH [--stem phrase] | --find "asr phrase"')
    txt, src = _quran_verse(root, ref)
    n, a = ref.split(":")
    print(f"{SURA_NUM.get(int(n),'?')} {ref}  [{src}]")
    print(f"  uthmani: {txt}")
    if stem:
        aw = [w for w in norm(stem).split() if len(w) > 2]
        u = norm(txt)
        hit = sum(1 for w in aw if w in u)
        status = "MATCH" if norm(stem) in u else (f"partial {hit}/{len(aw)}" if aw else "?")
        print(f"  asr-stem: «{stem}» -> {status}")
        return {"ref": ref, "uthmani": txt, "status": status}


# ---------------------------------------------------------------- dorar
def _dorar_search(query, root):
    global _CACHE
    _CACHE = _cache_dir(root)
    url = "https://dorar.net/hadith/search?" + urllib.parse.urlencode({"q": query})
    def fetch():
        tmp = Path(root) / "_verify" / ".cache" / (hashlib.sha1(url.encode()).hexdigest()[:16] + ".md")
        subprocess.run(["scrapling", "extract", "stealthy-fetch", url, str(tmp)],
                       capture_output=True, timeout=120)
        return {"url": url, "text": tmp.read_text(encoding="utf-8") if tmp.exists() else ""}
    data, src = _cached(f"dorar:{query}:page", fetch)
    return data, src


def _field(chunk, label):
    """dorar cards put the label and value on separate lines, with inconsistent
    ** wrapping and `| ` separators — match the label, take the next non-empty run."""
    m = re.search(r"\*{0,2}\s*" + re.escape(label) + r"\s*[:：]\s*\n?\*{0,2}\s*\[?([^\]\n*]+)", chunk)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def cmd_dorar(argv):
    root = _root()
    q = " ".join(a for a in argv if not a.startswith("--"))
    if not q.strip():
        sys.exit("usage: verify dorar \"نص الحديث\"")
    _core = q.split()
    if len(_core) > 6:
        print(f"  QUERY TOO LONG ({len(_core)} words) — dorar matches short matn fragments; a "
              "blank here is NOT evidence. Retry with a 4-6 word core before recording a pass.")
    data, src = _dorar_search(q, root)
    t = data["text"]
    chunks = re.split(r"(?m)^#{5}\s*\d+\s*-\s*", t)
    cards = []
    for ch in chunks[1:]:
        matn = re.sub(r"\s+", " ", ch.split("\n")[0]).strip()
        grade = _field(ch, "خلاصة حكم المحدث")
        if not grade:
            continue
        link = re.search(r"\((/h/[A-Za-z0-9]+)\)", ch)
        cards.append({"matn": matn[:180], "grade": grade,
                      "rawi": _field(ch, "الراوي"), "muhaddith": _field(ch, "المحدث"),
                      "source": _field(ch, "المصدر"), "num": _field(ch, "الصفحة أو الرقم"),
                      "taghrij": _field(ch, "التخريج"),
                      "url": ("https://dorar.net" + link.group(1)) if link else "",
                      "full": ch})
    print(f"dorar [{src}] query={q!r} cards={len(cards)}")
    # dorar matches at WORD level: a 32-card result may contain none of the phrase.
    # Score every card by its longest contiguous run of the query and lead with real hits.
    qt = _tokens(q)
    for card in cards:
        # score the WHOLE card: dorar often puts the wording that matches inside
        # the "[يعني حديث: …]" expansion, which the short matn field drops
        hay = " ".join(_tokens(card.get("full", "") or card.get("matn", "")))
        run = 0
        for i in range(len(qt)):
            for j in range(len(qt), i + run, -1):
                if " ".join(qt[i:j]) in hay:
                    run = max(run, j - i)
                    break
        card["run"] = run
    # allow one inserted word: the matn rarely tracks a query token-for-token
    real = [c for c in cards if c["run"] >= max(3, len(qt) - 2)]
    print(f"  carrying the phrase as a contiguous run: {len(real)}/{len(cards)}")
    if cards and not real:
        print("  WORD-NOISE — no card contains the query contiguously: this is NOT a find,")
        print("  and not yet a pass either; re-core with fewer, more distinctive words.")
    out = []
    for card in (real or cards)[:5]:
        out.append(card)
        print(f"  - [{card['run']}/{len(qt)}] {card['grade']} | {card['rawi']} | {card['muhaddith']} — {card['source']}"
              + (f" {card['num']}" if card['num'] else ""))
        print(f"    matn: {card['matn'][:110]}")
        if card["taghrij"]:
            print(f"    taghrij: {card['taghrij'][:150]}")
        if card["url"]:
            print(f"    url: {card['url']}")
    if not cards:
        print("  NO CARDS — either a true negative or the page layout changed;")
        print("  inspect the cached page before trusting this (doctrine: never guess)")
    return out


# ---------------------------------------------------------------- wikisource
def _ws(params):
    url = "https://ar.wikisource.org/w/api.php?" + urllib.parse.urlencode(params)
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25).read().decode("utf-8"))


def cmd_locate(argv):
    root = _root()
    phrase = argv[argv.index("--phrase") + 1] if "--phrase" in argv else \
             " ".join(a for a in argv if not a.startswith("--") and not a[0].isdigit())
    if not phrase.strip():
        sys.exit("usage: verify locate --phrase \"عبارة\" [--title PageName]")
    global _CACHE
    _CACHE = _cache_dir(root)
    data, src = _cached(f"ws-search:{phrase}", lambda: _ws(
        {"action": "query", "list": "search", "srsearch": phrase, "format": "json", "srlimit": 6}))
    titles = [r["title"] for r in data.get("query", {}).get("search", [])]
    print(f"wikisource search [{src}] {phrase!r} ->")
    for t in titles:
        print(f"   {t}")
    want = argv[argv.index("--title") + 1] if "--title" in argv else None
    for t in ([want] if want else titles[:3]):
        if not t:
            continue
        try:
            pg, s2 = _cached(f"ws-page:{t}", lambda: _ws(
                {"action": "query", "prop": "revisions", "rvprop": "content",
                 "rvslots": "main", "titles": t, "format": "json"}))
            pages = pg.get("query", {}).get("pages", {})
            p = list(pages.values())[0]
            txt = p.get("revisions", [{}])[0].get("slots", {}).get("main", {}).get("*", "")
        except Exception as e:
            print(f"   !! {t}: {e}"); continue
        i = txt.find(norm(phrase)[:12]) if False else txt.find(phrase.split()[0])
        print(f"   == {t} [{s2}] chars={len(txt)}")
        if i != -1:
            print("      ...", re.sub(r"\s+", " ", txt[max(0, i-160):i+320]))
        else:
            print("      first word not found in page body")
    return titles


def _ws_body(title):
    d, _ = _cached(f"ws-page:{title}", lambda: _ws(
        {"action": "query", "prop": "revisions", "rvprop": "content", "rvslots": "main",
         "titles": title, "format": "json", "redirects": 1}))
    p = list(d.get("query", {}).get("pages", {}).values())
    if not p:
        return ""
    rev = p[0].get("revisions", [{}])[0]
    return rev.get("slots", {}).get("main", {}).get("*", "") or rev.get("content", "") or ""


def _norm_txt(s):
    # Hamza carriers differ between ASR and manuscript orthography (وطأته / وطاته);
    # dropping the standalone hamza keeps both spellings comparable.
    return norm(s).replace("ء", "")


def _tokens(s):
    return [w for w in _norm_txt(re.sub(r"\{\{[^}]*\}\}|[\[\]|#*<>/]", " ", s)).split() if w]


def _window(text, probe):
    """Source snippet around a matched token run, for the dossier."""
    nt = re.sub(r"\s+", " ", re.sub(r"\{\{[^}]*\}\}", "", text))
    i = _norm_txt(nt).find(probe)
    return nt[max(0, i - 130):i + 230] if i > 0 else ""


# Names and particles carry no wording evidence: "أن علي بن أبي طالب" matches on any
# page of any history book. A run confirms only with real content words in it.
_RUN_STOP = set("""قال قالت ان ان انما ما لا في من على عن الى إلى هو هي هذا هذه ذلك ذلك
الذي التي كان كان قد ثم كل له به عليها عليه عنهم منهم نحن أنا أنت انتم عند لدى بين
علي ابي ابو ابن بن طالب عمر عمرو عثمان معاوية يزيد الحسن الحسين عائشة ام ابي الله رسول
محمد سنة عام يوم قالوا قالو انه انها انه انهم""".split())


def _content_words(toks):
    return [w for w in toks if w not in _RUN_STOP and len(w) >= 4]


def _word_cover(quote, text, phrase=""):
    """Does the source actually carry this report?

    The test is the longest CONTIGUOUS run of the quote's tokens surviving in the
    body. Scattered word hits are not evidence — an 8-word ASR sentence of common
    religious vocabulary "covers" on any page of the same book.

    Two things this used to get wrong, both silent false negatives:
      * it scored a FILTERED token list (len>3), so the probe skipped short words
        the body still contains and could never match contiguously;
      * it required run>=3 with no canonical-phrase fallback, so ASR orthography
        (وطاته vs وطأته) broke otherwise exact hits.
    A known `phrase` (canonical wording) is therefore also tested whole.
    """
    hay = " ".join(_tokens(text))
    qw = _tokens(quote)
    best_run, best_at, best_content = 0, "", 0
    for i in range(len(qw)):
        for j in range(len(qw), i + best_run, -1):
            probe = " ".join(qw[i:j])
            if probe in hay:
                c = len(_content_words(qw[i:j]))
                if (c, j - i) > (best_content, best_run):
                    best_run, best_at, best_content = j - i, _window(text, probe), c
                break
    pw = _tokens(phrase) if phrase else []
    phrase_hit = " ".join(pw) in hay if pw else False
    run = max(best_run, len(pw) if phrase_hit else 0)
    # A run of names and particles ("أن علي بن أبي طالب") is not a wording match.
    # Confirmation needs real content words in the matched run.
    content = sum(1 for w in qw[:0] )  # placeholder, replaced below
    return {"found": sum(1 for w in qw if w in hay), "need": len(qw), "run": run,
            "phrase_hit": phrase_hit, "at": best_at or (phrase and _window(text, " ".join(pw)) or ""),
            "content": best_content,
            "confirmed": (run >= 4 and best_content >= 2) or (phrase_hit and best_run >= 3)}


def _cached_bodies(root):
    """Every wikisource page body already fetched — a local corpus, free to search."""
    bodies = {}
    for f in glob.glob(str(_cache_dir(root) / "*.json")):
        try:
            d = json.loads(Path(f).read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict) or "query" not in d:
            continue
        for pg in d.get("query", {}).get("pages", {}).values():
            b = (pg.get("revisions", [{}])[0].get("slots", {}).get("main", {}) or {}).get("*", "")
            if pg.get("title") and len(b) > 200:
                bodies[pg["title"]] = b
    return bodies


def cmd_rescan(argv):
    """Score every open worklist text against the LOCAL corpus (zero requests).

    locate/sweep only ever look at the first candidate page a search returned. The
    cache holds every page the shelf has ever fetched, so re-scoring it is free and
    repeatedly finds items the live pass missed — do it after any matcher change.
    """
    root = _root()
    out = argv[argv.index("--out") + 1] if "--out" in argv else None
    wl = root / "plans" / "khilafah-verification" / "worklist.json"
    if not wl.exists():
        sys.exit("no worklist.json — run: shelf verify worklist")
    items = json.loads(wl.read_text(encoding="utf-8")).get("items", [])
    bodies = _cached_bodies(root)
    if not bodies:
        sys.exit("cache holds no page bodies yet — run a sweep/locate first")
    found = []
    for r in items:
        best = None
        for ttl, b in bodies.items():
            cov = _word_cover(r.get("quote", ""), b, r.get("phrase", ""))
            if cov["confirmed"] and (best is None or cov["run"] > best[1]["run"]):
                best = (ttl, cov)
        if best:
            found.append({"note": r["notes"][0], "cls": r["cls"], "quote": r["quote"],
                          "title": best[0], "run": best[1]["run"], "at": best[1]["at"]})
            print(f"  run={best[1]['run']:2d} {r['notes'][0]:8s} {r['quote'][:44]}")
            print(f"          {best[0][:60]}")
    print(f"\nrescan: {len(found)} candidate matches over {len(items)} open texts "
          f"using {len(bodies)} cached pages (0 requests)")
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(json.dumps(found, ensure_ascii=False, indent=1), encoding="utf-8")
    return found


def cmd_sweep(argv):
    """Batch SEARCH-ONLY pass over many phrases (wikisource).

    Why: `locate` fetches page bodies, so N reports cost ~4N requests and wikisource
    answers 429 long before that. Sweep spends exactly one cached request per phrase,
    so the whole report tier is one pass; only the promising titles then get `locate`.
    With --bodies it also scores the top candidate's page text per phrase, so the
    "does the wording actually survive" judgement is tool output, not a hand-rolled
    loop that gets rate-limited.
    """
    src = argv[argv.index("--from-json") + 1] if "--from-json" in argv else None
    out = argv[argv.index("--out") + 1] if "--out" in argv else None
    if not src or not out:
        sys.exit("usage: verify sweep --from-json PHRASES.json --out HITS.json [--bodies]")
    want_bodies = "--bodies" in argv
    jobs = json.loads(Path(src).read_text(encoding="utf-8"))
    global _CACHE
    root = _root()
    _CACHE = _cache_dir(root)
    results, fails = [], 0
    gap = 2.5
    for j in jobs:
        phrase = j.get("phrase") or j.get("stem")
        try:
            data, src_ = _cached(f"ws-search:{phrase}", lambda: _ws(
                {"action": "query", "list": "search", "srsearch": phrase,
                 "format": "json", "srlimit": 5}))
            titles = [r["title"] for r in data.get("query", {}).get("search", [])]
        except Exception as e:
            fails += 1
            if getattr(e, "code", None) == 429:
                gap = min(gap * 2, 20); time.sleep(gap)
                try:
                    data = _ws({"action":"query","list":"search","srsearch":phrase,
                                "format":"json","srlimit":5})
                    titles = [r["title"] for r in data.get("query",{}).get("search",[])]
                    src_ = "live"
                except Exception as e2:
                    titles, src_ = [], f"ERR {e2}"
            else:
                titles, src_ = [], f"ERR {e}"
        rec = {**j, "titles": titles, "src": src_}
        if want_bodies and titles:
            try:
                cov = _word_cover(j.get("quote", ""), _ws_body(titles[0]), j.get("phrase", ""))
                rec.update({"title": titles[0], **{f"cov_{k}": v for k, v in cov.items()}})
                rec["confirmed"] = cov["confirmed"]
                gap = max(3.0, gap)
            except Exception as e:
                rec["body_err"] = str(e)
                if "429" in str(e):
                    gap = min(gap * 2, 20); time.sleep(gap)
        results.append(rec)
        line = (f"  {phrase[:38]:40s} -> {len(titles)} hits"
                + (f"  [{titles[0][:40]}]" if titles else ""))
        if "cov_run" in rec:
            line += (f"  run={rec['cov_run']} words={rec['cov_found']}/{rec['cov_need']}"
                     + ("  CONFIRMED" if rec.get("confirmed") else ""))
        print(line)
        time.sleep(gap)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    with_hits = sum(1 for r in results if r["titles"])
    conf = sum(1 for r in results if r.get("confirmed"))
    print(f"sweep: {len(results)} phrases, {with_hits} with hits, {conf} confirmed, "
          f"{fails} errors -> {out}")
    return results


# ---------------------------------------------------------------- apply
def cmd_apply(argv):
    root = _root()
    src = argv[argv.index("--from-json") + 1] if "--from-json" in argv else None
    # --amend: deliberate correction of a row that already carries evidence.
    # Doctrine says one pass per item, ever — so a rewrite must be explicit and
    # must say why (v["amend"]); it is logged, never silent. Typical case: a
    # negative search that turns out to be a query-phrasing miss.
    amend = "--amend" in argv
    if not src or not Path(src).exists():
        sys.exit("usage: verify apply --from-json VERDICTS.json [--amend]")
    verdicts = json.loads(Path(src).read_text(encoding="utf-8"))
    if isinstance(verdicts, dict):
        verdicts = [verdicts]
    touched, skipped, amended, added = {}, [], [], []
    for v in verdicts:
        note, stem = v.get("note"), v.get("stem")
        hits = glob.glob(str(root / "reference" / "notes" / f"{note}-*.md"))
        if not hits:
            skipped.append((note, "no note")); continue
        p = Path(hits[0])
        txt = p.read_text(encoding="utf-8")
        sec = re.search(r"(## نصوص وآثار.*?)(?=\n## |\Z)", txt, re.S)
        if not sec:
            skipped.append((note, "no نصوص section")); continue
        body = sec.group(1)
        parts = re.split(r"(\n(?=\s*\d+\.\s+\*\*))", body)
        done = False
        for i, part in enumerate(parts):
            qm = re.search(r">\s*«([^»]+)»", part)
            probe = norm(stem)
            hay = norm((qm.group(1) if qm else "") + " " + part)
            if not qm or probe not in hay:
                continue
            lm = re.search(r"التحقق[:：][^\n]*", part)
            if lm is None:
                # First-ever verdict on a row that never had one. The writer used to skip
                # such rows — the same blind spot that hid 67 rows from the worklist.
                parts[i] = part.rstrip("\n") + "\n\n   " + v["line"].strip() + "\n"
                added.append((note, stem))
                done = True
                break
            old_line = lm.group(0)
            if DONE_RE.search(old_line):
                if not amend or not v.get("amend"):
                    skipped.append((note, stem, "already verified — pass --amend + a reason to correct"))
                    done = True; break
                new_line = v["line"].strip()
                if "تصويب" not in new_line:
                    new_line = new_line.rstrip() + f" | **تصويب**: {v['amend']}"
                amended.append((note, stem, v["amend"]))
            else:
                new_line = v["line"].strip()
            newpart, cnt = re.subn(r"—?\s*التحقق[:：][^\n]*", new_line, part, count=1)
            if cnt:
                parts[i] = newpart
                done = True
            break
        if not done:
            skipped.append((note, stem, "stem not found in any item")); continue
        p.write_text(txt[:sec.start(1)] + "".join(parts) + txt[sec.end(1):], encoding="utf-8")
        touched[note] = touched.get(note, 0) + 1
    for n, s in added:
        print(f"  ADD  ({n}, {s[:34]}) — first verdict on this row")
    print(f"apply: updated {sum(touched.values())} rows in {len(touched)} notes")
    for a in amended:
        print("  AMEND", a)
    for s in skipped:
        print("  SKIP", s)
    return touched




# ---------------------------------------------------------------- shamela
# The local Shamela catalogue is an OFFLINE INDEX into the same id space as shamela.ws:
# book_id resolves to a citable URL, and each book's own structure db maps
# url-page-id <-> volume <-> printed page. So it answers "where is this text, in which
# edition, at which printed page" -- the locate question.
#
# It does NOT answer "is this sahih". That is a verdict: it needs the chain identified and a
# grading book cited. A wording match in a history book is not a chain match (VERIFICATION.md:
# a find on a different chain is not a verdict on this one -- the Constantinople hadith has two
# chains with opposite grades).
#
# Quoting rule: Shamela text is NEVER «…». Those marks mean "the speaker's words at a minute"
# and the checker demands verbatim presence in the timed transcript. A book title or a page's
# wording is a ‹…› mention plus a cite line.
SHAMELA_DEFAULTS = ("/mnt/e/shamela4/database", "E:/shamela4/database", "D:/shamela4/database")


def _shamela_root(root):
    """Resolve the catalogue. Returns (path_or_None, source_description).

    An absent library is a STATE about this machine, never a negative about a book. Callers
    must say so out loud -- "not found in the catalogue" and "catalogue not mounted" are
    different sentences and only one of them is evidence.
    """
    try:
        from shelf_core.config import load_config
    except ImportError:
        from config import load_config  # type: ignore
    try:
        cfg = load_config(Path(root)) or {}
    except Exception:
        cfg = {}
    explicit = (((cfg.get("verify") or {}).get("shamela") or {}).get("path")) or os.environ.get("SHEMELA_DB")
    for c in ([explicit] if explicit else list(SHAMELA_DEFAULTS)):
        if c and (Path(c) / "master.db").exists():
            return Path(c), ("config/env" if explicit else "default path")
    return None, (f"configured path {explicit!r} has no master.db" if explicit
                  else "no catalogue mounted (checked " + ", ".join(SHAMELA_DEFAULTS) + ")")


def _shamela_master(db):
    import sqlite3
    return sqlite3.connect(f"file:{Path(db)/'master.db'}?mode=ro&immutable=1", uri=True)


def _shamela_book_db(db, book_id):
    """Per-book structure db: page(id, part=volume, page=printed page) + title(id, page, parent).
    Structure only -- the text itself lives in the Lucene store, not here."""
    import sqlite3
    f = Path(db) / "book" / f"{int(book_id) % 1000:03d}" / f"{book_id}.db"
    if not f.exists():
        return None
    return sqlite3.connect(f"file:{f}?mode=ro&immutable=1", uri=True)


def cmd_shamela(argv):
    root = _root()
    args = [a for a in argv if not a.startswith("--")]
    as_json = "--json" in argv
    action = args[0] if args else "status"
    db, how = _shamela_root(root)

    if action == "status" or db is None:
        if db is None:
            print(f"SHAMELA ABSENT — {how}")
            print("  This says nothing about any book. Do NOT record a negative from here;")
            print("  mount the library or use `verify locate` / the web channel instead.")
            return {"present": False, "why": how}
        c = _shamela_master(db)
        nb = c.execute("select count(*) from book").fetchone()[0]
        na = c.execute("select count(*) from author").fetchone()[0]
        print(f"SHAMELA PRESENT {db}  (resolved by {how})")
        print(f"  catalogue: {nb} books, {na} authors")
        print("  role: LOCATE only (edition + printed page + citable url). Never a verdict.")
        return {"present": True, "path": str(db), "books": nb, "authors": na}

    c = _shamela_master(db)

    if action == "find":
        q = " ".join(args[1:]).strip()
        if not q:
            sys.exit('usage: verify shamela find "<title fragment>"')
        # List EVERY edition that matches. Picking one silently is how you cite
        # "تكملة تاريخ الطبري" (237 pages) while meaning "تاريخ الطبري" (the Tarikh itself).
        rows = c.execute("select book_id,book_name,authors,book_category from book "
                         "where book_name like ? order by book_name limit 25", (f"%{q}%",)).fetchall()
        if not rows:
            print(f"  no catalogue match for {q!r} — try a shorter core (drop 'كتاب', the editor, 'ط ...')")
            return []
        print(f"shamela find {q!r}: {len(rows)} edition(s) — pick by edition, not by title")
        out = []
        for bid, name, authors, cat in rows:
            b = _shamela_book_db(db, bid)
            npages = b.execute("select count(*) from page").fetchone()[0] if b else None
            au = c.execute("select a.author_name,a.death_text from author_book ab join author a "
                           "on a.author_id=ab.author_id where ab.book_id=? limit 1", (bid,)).fetchone()
            rec = {"id": bid, "name": name, "author": (au[0] if au else authors),
                   "death": (au[1] if au else ""), "pages": npages,
                   "url": f"https://shamela.ws/book/{bid}"}
            out.append(rec)
            print(f"  {bid:>7}  {name[:52]:<54} {('pp='+str(npages)) if npages else 'pp=?':>8}  "
                  f"{(rec['author'] or '')[:24]} {(rec['death'] or '')[:8]}")
        if len(rows) > 1:
            print("  ^ multiple editions: the edition (تحقيق/طبعة) is part of the citation.")
        if as_json:
            print(json.dumps(out, ensure_ascii=False))
        return out

    if action in ("page", "url"):
        if len(args) < 3:
            sys.exit('usage: verify shamela page <book_id> <volume> <printed_page>\n'
                     '       verify shamela url  <book_id> <url_page_id>')
        bid = int(args[1]); b = _shamela_book_db(db, bid)
        if not b:
            print(f"  book {bid} has no structure db locally (catalogued but not downloaded)")
            return []
        name = c.execute("select book_name from book where book_id=?", (bid,)).fetchone()[0]
        if action == "page":
            vol, pg = args[2], int(args[3])
            r = b.execute("select id from page where part=? and page=?", (vol, pg)).fetchone()
            if not r:
                print(f"  no printed page {vol}/{pg} in {name[:40]} — check the volume exists")
                return []
            pid = r[0]
        else:
            pid = int(args[2])
            r = b.execute("select part,page from page where id=?", (pid,)).fetchone()
            if not r:
                print(f"  url page id {pid} not in {name[:40]}")
                return []
        print(f"  {name[:56]}")
        print(f"  citation: {name.split(' - ')[0]} {r[0] if action=='url' else vol}/{r[1] if action=='url' else pg}")
        print(f"  url: https://shamela.ws/book/{bid}/{pid}")
        print("  wording must be re-read from the page before citing it; the index proves")
        print("  pagination, not content. Fetch the url, do not quote from memory.")
        return {"id": bid, "url": f"https://shamela.ws/book/{bid}/{pid}"}

    if action == "toc":
        if len(args) < 2:
            sys.exit("usage: verify shamela toc <book_id>")
        bid = int(args[1]); b = _shamela_book_db(db, bid)
        if not b:
            print(f"  book {bid} has no structure db locally"); return []
        rows = b.execute("select t.id,p.part,p.page from title t join page p on p.id=t.page "
                         "order by t.id limit 40").fetchall()
        name = c.execute("select book_name from book where book_id=?", (bid,)).fetchone()[0]
        print(f"  {name[:56]} — {len(rows)} chapter anchors (titles are not stored locally;")
        print(f"  the rendered list is at https://shamela.ws/book/{bid}")
        for tid, vol, pg in rows[:12]:
            print(f"    title {tid:>5} -> vol {vol} page {pg}")
        return rows

    sys.exit("usage: verify shamela status | find "<title>" | page <id> <vol> <pg> | "
             "url <id> <pageid> | toc <id>")


def cmd_verify(argv):
    if not argv or argv[0] not in COMMANDS:
        sys.exit("usage: shelf verify {" + "|".join(sorted(COMMANDS)) + "} ...")
    COMMANDS[argv[0]](argv[1:])


# --------------------------------------------------------------------------- sync-docs
# Notes carry the verdicts; era docs carry the reader. Until this lane existed the two
# diverged silently: a text could be متحقق in reference/notes/ and still read «للشيخ» in
# the published doc. Direction is always notes -> docs; docs are never a source.

_DOCS_DEFAULT = "reference/خلافة-إسلامية"
_Q_RE = re.compile(r"«([^»]{8,})»")


def _note_verdicts(root):
    """Parse every note's «نصوص وآثار» rows into verdicts keyed by normalised quote."""
    out = []
    ndir = os.path.join(root, "reference", "notes")
    for path in sorted(glob.glob(os.path.join(ndir, "is-*.md"))):
        note = os.path.basename(path).split("-")[0] + "-" + os.path.basename(path).split("-")[1]
        text = open(path, encoding="utf-8").read()
        m = re.search(r"## نصوص وآثار.*?(?=\n## |\Z)", text, flags=re.S)
        if not m:
            continue
        blocks = re.split(r"(?m)^\s*\d+\.\s+\*\*", m.group(0))
        for b in blocks[1:]:
            qm = _Q_RE.search(b)
            vm = re.search(r"—\s*التحقق:\s*(?:\*\*)?\s*([^*\n—]+?)\s*(?:\*\*)?\s*—?\s*(.*)", b, flags=re.S)
            if not qm or not vm:
                continue
            # Status is the bolded token (or the text up to the first dash). A lazy
            # capture here once produced <strong>ل</strong> — لشيخ — …
            raw = re.sub(r"\s+", " ", vm.group(0)).strip()
            sm = re.search(r"التحقق[:：]\s*\*\*([^*]+)\*\*", raw)
            if sm:
                status = sm.group(1).strip()
                tail = raw[sm.end():]
            else:
                sm = re.search(r"التحقق[:：]\s*", raw)
                rest = raw[sm.end():] if sm else raw
                status, _, tail = rest.partition(" —")
                status = status.strip().rstrip("—").strip()
            tail = tail.strip(" —")
            amana = ""
            if "| الأمانة:" in tail:
                tail, amana = tail.split("| الأمانة:", 1)
                amana = amana.strip()
            dossier = re.search(r"\[الدوسيه\]\(([^)]+)\)", tail)
            href = re.search(r"\((https?://[^)]+)\)", tail)
            # Drop the dossier link BEFORE flattening: converting first turns
            # «[الدوسيه](path)» into the bare word «الدوسيه», which then survived
            # into the published doc as dead text next to the real anchor.
            tail = re.sub(r"\s*[—،]\s*\[الدوسيه\]\([^)]+\)", "", tail)
            # http links become real anchors with their own label («دورار», «المصدر»);
            # anything else (a bare path) is flattened to text.
            plain = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', tail)
            plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", plain)
            plain = re.sub(r"\s*\(\s*\)", "", plain)
            plain = re.sub(r"\s*[—،]\s*[—،]", " —", plain)
            plain = re.sub(r"\*\*", "", plain).strip(" —،")
            out.append({"note": note, "quote": qm.group(1), "nq": _norm_txt(qm.group(1)),
                        "status": status, "tail": plain, "amana": amana,
                        "dossier": dossier.group(1) if dossier else "",
                        "url": href.group(1) if href else "",
                        "cite": (lambda m: "المجلس %d، %s" % (int(m.group(1)), m.group(2))
                                 if m else "")(
                            re.search(r"المجلس\s*0*(\d{1,2})[،,]?\s*(\d{2}:\d{2})", raw))})
    return out


def _run_len(a, b):
    """Longest contiguous token run shared by two normalised quotes."""
    ta, tb = a.split(), set(b.split())
    best = i = 0
    while i < len(ta):
        j = i + 1
        while j <= len(ta) and " ".join(ta[i:j]) in b:
            best = max(best, j - i)
            j += 1
        i += 1
    return best


def _match(docq, verdicts):
    n = _norm_txt(docq)
    best, score = None, 0
    for v in verdicts:
        r = _run_len(n, v["nq"])
        cov = r / max(1, len(n.split()))
        if (r, cov) > (score, 0) and (r >= 4 or (r >= 3 and cov >= 0.6)):
            best, score = v, r
    return best, score


def _truncate_html(s, limit=175):
    """Cut at a word boundary without ever splitting inside a tag or an anchor label."""
    if len(re.sub(r"<[^>]+>", "", s)) <= limit:
        return s
    out, vis, i, last_break = [], 0, 0, 0
    while i < len(s):
        if s.startswith("<a href", i):
            end = s.find(">", s.find("</a>", i)) + 1
            chunk, j = s[i:end], end   # advance PAST the anchor (was: j=i, which re-appended it)
        else:
            j = s.find("<", i)
            j = len(s) if j < 0 else j
            chunk = s[i:j]
        if vis + len(re.sub(r"<[^>]+>", "", chunk)) > limit:
            break
        out.append(chunk)
        vis += len(re.sub(r"<[^>]+>", "", chunk))
        i = j
        if " " in chunk:
            last_break = len("".join(out)) - (len(chunk) - chunk.rfind(" "))
    cut = "".join(out)
    if not cut.strip():
        # Nothing fit: the whole tail is one long text segment. Cut it on a word
        # boundary at the limit rather than emitting a bare ellipsis.
        cut = re.sub(r"<a\s[^>]*>(.*?)</a>", r"\1", s)[:limit]
        cut = cut[:cut.rfind(" ")] if " " in cut else cut
    elif last_break:
        cut = cut[:last_break]
    cut = re.sub(r"<a\s[^>]*>(.*?)</a>", r"\1", cut)
    # a cut that landed inside an anchor leaves half a tag: keep the label, drop markup
    cut = re.sub(r"<a\s[^>]*>?", "", cut).replace("</a>", "")
    return cut.rstrip(" —،") + "…"


def _compact(v):
    """Doc-sized verdict line from a note row: status, short grade, links."""
    tail = _truncate_html(v["tail"])
    # A verdict quotes BOOKS, not the transcript. The shelf's quote-check demands every
    # «…» in a doc be findable in the session audio, so source quotations are written
    # with single guillemets — visually distinct, and outside the transcript check.
    tail = tail.replace("«", "‹").replace("»", "›")
    parts = [f"<strong>{v['status']}</strong> — {tail}"]
    if v["url"] and "<a href" not in tail:
        parts[-1] += f' (<a href="{v["url"]}">المصدر</a>)'
    if v["dossier"]:
        parts.append(f'<a href="../../{v["dossier"]}">الدوسيه</a>')
    if v["amana"] and len(v["amana"]) <= 110:
        parts.append("الأمانة: " + v["amana"].replace("«", "‹").replace("»", "›"))
    return " — ".join(parts)


def cmd_sync_docs(argv):
    root = _root()
    args = [a for a in argv if not a.startswith("--")]
    dry = "--dry" in argv
    docs_dir = os.path.join(root, args[0]) if args else os.path.join(root, _DOCS_DEFAULT)
    verdicts = _note_verdicts(root)
    by_note = {}
    for v in verdicts:
        by_note.setdefault(v["note"], []).append(v)
    total_written = total_skip = total_closed = added_sections = 0
    for path in sorted(glob.glob(os.path.join(docs_dir, "*.html"))):
        name = os.path.basename(path)
        nums = re.match(r"(\d{3})(?:-(\d{3}))?-?", name)
        if not nums:
            continue
        lo = int(nums.group(1))
        hi = int(nums.group(2) or nums.group(1))
        pool = [v for n in range(lo, hi + 1) for v in by_note.get(f"is-{n:03d}", [])]
        if not pool:
            continue
        t_html = html = open(path, encoding="utf-8").read()
        # Three template wordings carry the evidence list across the shelf's history:
        # «نصوص وآثار (…)», «نصوص دينية وردت في الجلسات», «نصوص وأحاديث في الجلسات».
        # Match any نصوص-heading followed by a list, with an optional lead-in <p>.
        sec = re.search(r'(<h2[^>]*>\s*نصوص[^<]*</h2>\s*(?:<p>.*?</p>\s*)?<ul>)(.*?)(</ul>)',
                        html, flags=re.S)
        if not sec:
            # A numbered doc with notes but no evidence list at all: the oldest template
            # wove its «للشيخ» markers into prose, where no propagation can reach them.
            if "--add-section" in argv:
                rows = [v for v in pool if v["quote"]]
                if rows:
                    items = "\n".join(
                        "  <li>«" + v["quote"] + "»"
                        + (f' <span class="cite">{v["cite"]}</span>' if v.get("cite") else "")
                        + " — " + _compact(v) + ".</li>" for v in rows)
                    block = ('\n<h2 id="نصوص-وآثار">نصوص وآثار (استشهاد مزدوج)</h2>\n'
                             "<p>النصوصُ الدينيةُ التي وردت في هذه الجلسات وأحكامُها على "
                             "قنوات التحقق الثلاث؛ البطاقةُ الكاملة لكلٍّ منها في "
                             "<code>_verify/</code>.</p>\n<ul>\n" + items + "\n</ul>\n")
                    k = t_html.find('<section class="recap">')
                    if k < 0:
                        k = t_html.rfind("</main>")
                    t_html = t_html[:k] + block + t_html[k:]
                    added_sections += 1
                    if not dry:
                        open(path, "w", encoding="utf-8").write(t_html)
                    print(f"{'[dry] ' if dry else ''}{name[:44]:<46} sessions {lo:03d}-{hi:03d}: "
                          f"evidence list BUILT with {len(rows)} items")
            continue
        head, body, tail = sec.groups()
        items = re.findall(r"(?s)<li>.*?</li>", body)
        new_body, changed = body, 0
        for li in items:
            if "_verify/" in li or "المصدر</a>" in li:
                total_skip += 1
                continue
            plain = re.sub(r"<[^>]+>", " ", li)
            qm = _Q_RE.search(plain)
            if not qm:
                # older template: the item names the text without guillemets
                # («آية ونريد أن نمن … (القصص 5) — …»). Take the body before the dash run.
                body_txt = re.split(r"\s+[—–]\s+", plain.strip())[0]
                body_txt = re.sub(r"^(آية|حديث|أثر|اثر|رواية|قول|خبر)\s+", "", body_txt).strip()
                if len(body_txt) < 12:
                    continue
                class _Fake:  # keep the call-site shape identical
                    group = lambda self, i, _b=body_txt: _b
                qm = _Fake()
            v, score = _match(qm.group(1), pool)
            if not v:
                total_skip += 1
                continue
            # replace the trailing «للشيخ» marker (with any parenthetical) by the verdict
            pat = r"—\s*<strong>\s*للشيخ\s*</strong>\s*(?:\([^)]*\))?\s*\.?\s*(?=</li>)"
            if not re.search(pat, li):
                total_skip += 1
                continue
            newline = "— " + _compact(v) + "."
            new_li = re.sub(pat, newline, li)
            new_body = new_body.replace(li, new_li, 1)
            changed += 1
        out_html = html.replace(head + body + tail, head + new_body + tail, 1) if changed else html
        # --- reconcile the «ما يحتاج مراجعة الشيخ» list with the SAME verdicts.
        # A doc that marks an item متحقق above and still asks the sheikh about it below
        # contradicts itself; the review list is a queue, and finished work leaves a queue.
        closed = 0
        rev = re.search(r"(<h2[^>]*>ما يحتاج مراجعة[^<]*</h2>\s*<ul>)(.*?)(</ul>)",
                        out_html, flags=re.S)
        if rev:
            rhead, rbody, rtail = rev.groups()
            survivors = []
            for li in re.findall(r"(?s)<li>.*?</li>", rbody):
                plain = re.sub(r"<[^>]+>", " ", li)
                vs = [_match(q, pool)[0] for q in _Q_RE.findall(plain)]
                vs = [v for v in vs if v]
                if vs and all(not v["status"].startswith(("للشيخ", "متنازع")) for v in vs):
                    closed += 1
                    continue
                survivors.append(li)
            if closed:
                note = ('\n<p class="meta">وهذه القائمة كانت أوسع؛ نُقلت منها '
                        f"{closed} مادة إلى قسم النصوص والآثار أعلاه بعد أن انتهى التحقق "
                        "منها، فحكمُها ودرجتُها وموضعُها في البطاقة، والصفحة المحفوظة من "
                        "البحث في <code>_verify/</code>.</p>")
                out_html = out_html.replace(
                    rhead + rbody + rtail,
                    rhead + "\n  " + "\n  ".join(survivors) + "\n" + rtail + note, 1)
        total_written += changed
        total_closed += closed
        if (changed or closed) and not dry:
            open(path, "w", encoding="utf-8").write(out_html)
            t_html = out_html
        print(f"{'[dry] ' if dry else ''}{name[:44]:<46} sessions {lo:03d}-{hi:03d}: "
              f"{changed} verdicts propagated, {closed} closed items lifted from the "
              f"review list, {len(items) - changed} left as-is")
    print(f"\nsync-docs: {added_sections} evidence lists built, {total_written} propagated, {total_closed} closed items lifted "
          f"from review lists, {total_skip} untouched (already linked, unmatched, or no "
          f"marker) — notes are the source of truth")
    return total_written


COMMANDS = {"worklist": cmd_worklist, "quran": cmd_quran, "dorar": cmd_dorar,
            "locate": cmd_locate, "sweep": cmd_sweep, "rescan": cmd_rescan,
    "sync-docs": cmd_sync_docs, "apply": cmd_apply, "shamela": cmd_shamela}
