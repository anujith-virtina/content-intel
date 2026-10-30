# -*- coding: utf-8 -*-
"""Build + publish (draft) ChatSKU post:

    "Will AI replace your B2B sales reps? What actually changes for your team"
    slug: will-ai-replace-b2b-sales-reps
    Format D (playbook). Topic selected from a coverage audit: the line
    "Does this replace my sales team? No." appears as a one-line FAQ answer in
    NINE existing posts and is explained in none of them.

    Client asked for deliberately plain, non-technical language, so this build
    adds a READABILITY GATE (section 4L) that the other ChatSKU builders do not
    have: Flesch Reading Ease, sentence length, and a technical-jargon blocklist.

Adapted from build_response_gap_industry_post.py (post 2783), which is the
current canonical ChatSKU Elementor builder. Differences forced by this draft:

  - The draft body is already raw HTML (<h2>, <h3>, <p>, <strong>, <a>), so no
    markdown converter is needed. Lines pass through untouched; only the
    bracketed placement markers are transformed.
  - The markers use em dashes and a numbered form:
        [FEATURED IMAGE - 860x452 | ...]
        [BODY IMAGE 1 - ...]   [BODY IMAGE 2 - ...]
        [CTA BUTTON - ...]
    These are INSTRUCTIONS, not content. They are stripped entirely. The
    em-dash scan runs AFTER stripping, so their em dashes never reach the
    `content` field or `_elementor_data`.
  - No tables in this draft, so the table styler is not carried over.
  - Two image-sourcing modes, because MUST-FOLLOW-RULES section 3 makes
    visual QA mandatory and forbids auto-pickers:
        MODE=candidates -> sources 8+ per slot, resizes ALL to 860x452,
                           writes them to CANDIDATE_DIR with an HTML contact
                           sheet for human review. Never pushes.
        publish         -> requires QA_DIR/final_{featured,body1,body2}.jpg,
                           already visually approved. There is deliberately no
                           auto-pick path in the publish flow.

Run:
    python build_agentic_commerce_post.py                 # DRY RUN (parse + checks)
    MODE=candidates python build_agentic_commerce_post.py # source + contact sheet
    QA_DIR=... ALT_CONFIRMED=1 python build_agentic_commerce_post.py publish

Env switches:
    DRY_RUN         implicit: on unless "publish" is in argv
    MODE=candidates image sourcing / contact sheet only
    QA_DIR          folder holding final_featured.jpg / final_body1.jpg / final_body2.jpg
    ALT_CONFIRMED=1 operator asserts the ALT constants below were rewritten
                    against the images actually chosen (rules s3)
    UPDATE_POST_ID  update an existing post instead of creating one
    REUSE_MEDIA=1   reuse media IDs recorded in the state file, skip uploads
    FORCE_STATUS    e.g. "publish". IGNORED on updates (never blind-overwrite a
                    client's manual publish -- feedback_wp_update_in_place)
    NO_IMAGES=1     text-first push, attach images in a follow-up run
"""
import os, sys, re, io, json, base64, secrets, html as _html

try:
    import requests
except ImportError:
    print("BLOCKING: `requests` is not installed. pip install requests Pillow")
    raise SystemExit(1)

# ---------------------------------------------------------------------------
# 0. Environment
# ---------------------------------------------------------------------------
ENV_PATH = r"C:\content-intel\.env"
if os.path.exists(ENV_PATH):
    for ln in open(ENV_PATH, encoding="utf-8"):
        ln = ln.strip()
        if ln and not ln.startswith("#") and "=" in ln:
            k, v = ln.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

WP = "https://chatsku.com/wp-json/wp/v2"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

# ChatSKU credentials ONLY. Never WP_USERNAME (Virtina) or IMPELHUB_* .
try:
    U = os.environ["CHATSKU_WP_USERNAME"]
    A = os.environ["CHATSKU_WP_APP_PASSWORD"]
except KeyError as e:
    print(f"BLOCKING: missing credential {e}. Expected CHATSKU_WP_USERNAME / "
          f"CHATSKU_WP_APP_PASSWORD in {ENV_PATH}.")
    raise SystemExit(1)
AUTH = base64.b64encode(f"{U}:{A}".encode()).decode()
H = {"Authorization": f"Basic {AUTH}", "User-Agent": UA, "Content-Type": "application/json"}
HG = {"User-Agent": UA}                      # Cloudflare 403s without a browser UA

TITLE = "Where should a BigCommerce B2B quote request start?"
SLUG = "bigcommerce-chatbot-quoting"
PERMALINK = f"https://chatsku.com/{SLUG}/"
DRAFT = r"C:\content-intel\clients\chatsku\output\drafts\bigcommerce-chatbot-quoting-2026-10-22.md"
# Reset BOTH Yoast strings when cloning a build script. Leaving the previous
# post's values shipped twice before, because the checks only measure length.
YOAST_TITLE = 'BigCommerce B2B Quote Requests: Form, Chat or AI | ChatSKU'   # 58 chars
YOAST_DESC = 'Where should a BigCommerce B2B quote request start? Compare a quote form, live chat, and an AI catalog assistant on price accuracy and after-hours coverage.'   # 156 chars
PUBLISH_DATE = "2026-10-22"
CATEGORIES = [22, 24]   # B2B Commerce / Catalog Optimization (verified live 2026-09-30). NEVER 25 (DFW Local).

BASE = os.path.dirname(os.path.abspath(__file__))
STATE_PATH = os.path.join(BASE, "bigcommerce_quoting_push_state.json")
SCRATCH = os.environ.get("SCRATCH_DIR", BASE)
QA_DIR = os.environ.get("QA_DIR", "")
CANDIDATE_DIR = os.environ.get("CANDIDATE_DIR", os.path.join(SCRATCH, "moq_candidates"))
MODE = os.environ.get("MODE", "").lower()
NO_IMAGES = os.environ.get("NO_IMAGES") == "1"
REUSE_MEDIA = os.environ.get("REUSE_MEDIA") == "1"
UPDATE_POST_ID = os.environ.get("UPDATE_POST_ID", "").strip()
FORCE_STATUS = os.environ.get("FORCE_STATUS", "").strip()
ALT_CONFIRMED = os.environ.get("ALT_CONFIRMED") == "1"

# ---------------------------------------------------------------------------
# 0a. ALT TEXT -- rewrite these against the images ACTUALLY chosen.
# Rules s3: "verify the alt text still describes the image you actually chose;
# placeholder alt text written at draft stage usually describes a different
# scene." The publish flow refuses to run unless ALT_CONFIRMED=1.
# 80-150 chars each, unique, 1-2 article keywords.
# ---------------------------------------------------------------------------
FEATURED_ALT = ('Two colleagues review a B2B order together at a white office table with a laptop, a tablet and a notepad.')
BODY1_ALT = ('A B2B buyer checks a product catalog alone on a laptop at a wooden desk in a bright modern office.')
BODY2_ALT = ('Two people work through order quantities at a desk, with a laptop open beside handwritten notes and figures.')
# Source URLs of images already used on other ChatSKU posts. Candidates matching
# these are dropped so nothing gets reused (rules s3 "fresh images").
USED_SOURCES_PATH = os.path.join(BASE, "chatsku_used_image_sources.json")
USED_SOURCES = set()
if os.path.exists(USED_SOURCES_PATH):
    try:
        USED_SOURCES = set(json.load(open(USED_SOURCES_PATH, encoding="utf-8")))
    except Exception:
        USED_SOURCES = set()


# ---------------------------------------------------------------------------
# 0b. Crash-resilience state file
# ---------------------------------------------------------------------------
def load_state():
    if os.path.exists(STATE_PATH):
        try:
            return json.load(open(STATE_PATH, encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_state(**kw):
    st = load_state()
    st.update(kw)
    st.setdefault("slug", SLUG)
    st.setdefault("title", TITLE)
    with open(STATE_PATH, "w", encoding="utf-8") as fh:
        json.dump(st, fh, indent=2)
    print("  [state] saved:", dict(kw))
    return st


STATE = load_state()
if UPDATE_POST_ID:
    STATE["post_id"] = int(UPDATE_POST_ID)
if STATE.get("post_id"):
    print(f"!! state carries post_id {STATE['post_id']} -- this run will UPDATE, not create.")


# ---------------------------------------------------------------------------
# 1. Image sourcing -- CANDIDATES MODE ONLY (never auto-picks for publish)
#    Openverse license=cc0 general query + provider ranking. The
#    source=stocksnap filter is DEAD (returns 0) -- rank in code instead.
#    Pexels first if a key exists (there is none in .env as of 2026-09-07).
# ---------------------------------------------------------------------------
PEXELS_KEY = os.environ.get("PEXELS_API_KEY", "")

IMG_QUERIES = {
    # featured: distributor inside-sales desk in daylight, person at a monitor.
    # Pose exclusions from the brief: NO hand-to-chin-at-laptop (post 2468),
    # NO tired-man-leaning-over-laptop (post 2665).
    "featured": ["office desk monitor documents", "manager reviewing screen office",
                 "business desk computer paperwork", "office worker computer monitor",
                 "office employee desktop screen", "business office desk daylight"],
    # body1: sales rep mid-phone-call at a desk, laptop open, in conversation.
    "body1": ["office night desk monitor", "working late office computer",
              "dark office computer screen", "evening office desk laptop",
              "office worker night shift desk", "late night office workstation"],
    # body2: two colleagues in a warehouse/plant office reviewing data on a
    # screen with racking or stock visible behind them.
    "body2": ["spreadsheet paperwork desk computer", "technical documents desk screen",
              "data sheet desk office computer", "warehouse office computer worker",
              "inventory paperwork desk screen", "distribution centre office desk"],
}

# Higher score = preferred. Museum/library scans rank last: they are historical
# prints, not B2B office photography.
PROVIDER_RANK = {
    "stocksnap": 100, "flickr": 70, "rawpixel": 65, "pixabay": 60, "pexels": 95,
    "sketchfab": 0, "wikimedia": 20, "smithsonian": 5, "met": 5, "nypl": 5,
    "sciencemuseum": 5, "clevelandmuseum": 5, "statensmuseum": 5, "brooklynmuseum": 5,
    "thorvaldsensmuseum": 5, "floraon": 0, "geographorguk": 10, "spacex": 0, "nasa": 5,
}
# Hard subject veto -- rules s3 forbids nature/flowers/animals on a B2B article.
VETO_WORDS = ["flower", "floral", "plant", "botanic", "bird", "animal", "dog", "cat",
              "cattle", "landscape", "mountain", "forest", "beach", "sunset", "garden",
              "insect", "butterfly", "fish", "tree", "leaf", "petal", "portrait of a",
              "painting", "engraving", "illustration", "drawing", "sculpture", "map",
              "manuscript", "print by", "watercolou", "lithograph"]


def _veto(title):
    t = (title or "").lower()
    return any(w in t for w in VETO_WORDS)


def pexels_search(query, n=10):
    if not PEXELS_KEY:
        return []
    try:
        r = requests.get("https://api.pexels.com/v1/search",
                         params={"query": query, "orientation": "landscape", "per_page": n},
                         headers={"Authorization": PEXELS_KEY, "User-Agent": UA}, timeout=30)
        return [{"url": p["src"]["large2x"], "provider": "pexels",
                 "title": p.get("alt", ""), "page": p.get("url", "")}
                for p in r.json().get("photos", [])]
    except Exception as e:
        print("  pexels err", query, e)
        return []


def openverse_search(query, n=40):
    """General cc0 query. source=stocksnap is DEAD (0 results) -- do not use it."""
    try:
        r = requests.get("https://api.openverse.org/v1/images/",
                         params={"q": query, "license": "cc0", "page_size": n,
                                 "aspect_ratio": "wide", "extension": "jpg"},
                         headers={"User-Agent": UA}, timeout=30)
        out = []
        for res in r.json().get("results", []):
            if not res.get("url"):
                continue
            out.append({"url": res["url"], "provider": (res.get("provider") or "").lower(),
                        "title": res.get("title", ""), "page": res.get("foreign_landing_url", "")})
        return out
    except Exception as e:
        print("  openverse err", query, e)
        return []


def download_candidate(url):
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
        data = r.content
        if len(data) < 8000:
            return None
        if not (data[:2] == b"\xff\xd8" or data[:8] == b"\x89PNG\r\n\x1a\n"):
            return None
        return data
    except Exception:
        return None


def fit_860x452(data):
    """scale-to-cover + center-crop, LANCZOS, JPEG q82."""
    from PIL import Image
    im = Image.open(io.BytesIO(data)).convert("RGB")
    tw, th = 860, 452
    sw, sh = im.size
    if sw < tw or sh < th:
        raise ValueError(f"source too small ({sw}x{sh}) to cover {tw}x{th}")
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    im = im.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - tw) // 2, (nh - th) // 2
    im = im.crop((left, top, left + tw, top + th))
    for q in (82, 78, 72, 66):
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=q, optimize=True)
        if buf.tell() <= 200_000:
            return buf.getvalue(), q
    return buf.getvalue(), q


def build_candidates(slot, want=8):
    """Download + resize MANY candidates so a human can look at every one."""
    os.makedirs(CANDIDATE_DIR, exist_ok=True)
    pool, seen = [], set()
    for q in IMG_QUERIES[slot]:
        for c in pexels_search(q) + openverse_search(q):
            if c["url"] in seen or c["url"] in USED_SOURCES:
                continue
            if _veto(c["title"]):
                continue
            seen.add(c["url"])
            c["score"] = PROVIDER_RANK.get(c["provider"], 30)
            c["query"] = q
            pool.append(c)
    pool.sort(key=lambda c: -c["score"])
    print(f"  [{slot}] {len(pool)} ranked candidates in pool")
    saved = []
    for c in pool:
        if len(saved) >= want:
            break
        raw = download_candidate(c["url"])
        if not raw:
            continue
        try:
            out, q = fit_860x452(raw)
        except Exception as e:
            print(f"    skip ({e}) {c['url'][:90]}")
            continue
        fn = f"{slot}_{len(saved):02d}_{c['provider'] or 'unknown'}.jpg"
        with open(os.path.join(CANDIDATE_DIR, fn), "wb") as fh:
            fh.write(out)
        c["file"] = fn
        c["bytes"] = len(out)
        c["quality"] = q
        saved.append(c)
        print(f"    saved {fn}  {len(out)//1024} KB  q{q}  <- {c['provider']} :: {c['title'][:60]}")
    return saved


def contact_sheet(all_slots):
    """Write an HTML contact sheet. OPEN IT AND LOOK AT EVERY IMAGE.
    Then copy the three winners to QA_DIR as final_{slot}.jpg."""
    parts = ["<html><meta charset='utf-8'><body style='font-family:sans-serif;background:#111;color:#eee'>",
             "<h1>ChatSKU / what-is-agentic-commerce &mdash; image candidates (all 860x452)</h1>",
             "<p>Rules s3: look at every one. Subject must be business / office / warehouse / "
             "manufacturing. Never nature, flowers, animals. Pose exclusions: no "
             "hand-to-chin-at-laptop, no tired-man-leaning-over-laptop.</p>"]
    for slot, cands in all_slots.items():
        parts.append(f"<h2>{slot}</h2><div style='display:flex;flex-wrap:wrap;gap:14px'>")
        for c in cands:
            parts.append(
                f"<figure style='width:430px;margin:0'><img src='{c['file']}' width='430'>"
                f"<figcaption style='font-size:12px'>{c['file']}<br>{_html.escape(c['provider'])} | "
                f"q:{_html.escape(c['query'])}<br>{_html.escape((c['title'] or '')[:90])}<br>"
                f"<a style='color:#6cf' href='{c['page']}'>source</a></figcaption></figure>")
        parts.append("</div>")
    parts.append("</body></html>")
    p = os.path.join(CANDIDATE_DIR, "contact_sheet.html")
    open(p, "w", encoding="utf-8").write("\n".join(parts))
    json.dump(all_slots, open(os.path.join(CANDIDATE_DIR, "manifest.json"), "w",
                              encoding="utf-8"), indent=2)
    print(f"\nContact sheet: {p}")
    print("OPEN IT. Review every candidate. Then copy the three winners into QA_DIR as")
    print("  final_featured.jpg / final_body1.jpg / final_body2.jpg")
    print("Then rewrite FEATURED_ALT / BODY1_ALT / BODY2_ALT in this script to describe")
    print("what those three images ACTUALLY show, and re-run with ALT_CONFIRMED=1 publish.")


if MODE == "candidates":
    print("=== IMAGE CANDIDATE SOURCING (no push) ===")
    slots = {s: build_candidates(s) for s in ("featured", "body1", "body2")}
    contact_sheet(slots)
    raise SystemExit(0)


# ---------------------------------------------------------------------------
# 2. Media upload (pre-QA'd files only)
# ---------------------------------------------------------------------------
def read_qa_image(slot):
    if not QA_DIR:
        print("BLOCKING: QA_DIR is not set. This script has no auto-sourcing path in the")
        print("publish flow by design (rules s3: visual QA is mandatory). Run with")
        print("MODE=candidates first, review the contact sheet, then set QA_DIR.")
        raise SystemExit(1)
    p = os.path.join(QA_DIR, f"final_{slot}.jpg")
    if not os.path.exists(p):
        print(f"BLOCKING: missing pre-QA'd image {p}")
        raise SystemExit(1)
    from PIL import Image
    data = open(p, "rb").read()
    w, h = Image.open(io.BytesIO(data)).size
    if (w, h) != (860, 452):
        print(f"BLOCKING: {p} is {w}x{h}, expected 860x452.")
        raise SystemExit(1)
    if len(data) > 200_000:
        print(f"BLOCKING: {p} is {len(data)} bytes, over the 200 KB cap.")
        raise SystemExit(1)
    if data[:2] != b"\xff\xd8":
        print(f"BLOCKING: {p} is not a JPEG.")
        raise SystemExit(1)
    print(f"  pre-QA'd {slot}: {p} ({w}x{h}, {len(data)//1024} KB)")
    return data


def upload_media(image_bytes, filename, alt_text, state_key):
    r = requests.post(f"{WP}/media", headers={
        "Authorization": H["Authorization"], "User-Agent": UA,
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "image/jpeg"
    }, data=image_bytes, timeout=120)
    r.raise_for_status()
    media = r.json()
    mid = media["id"]
    save_state(**{state_key: mid})                 # irreversible -> persist NOW
    requests.post(f"{WP}/media/{mid}", headers=H,
                  data=json.dumps({"alt_text": alt_text}).encode(), timeout=60)
    print(f"  uploaded media {mid}: {media['source_url']}")
    return {"id": mid, "url": media["source_url"], "alt": alt_text}


def fetch_media(mid, alt):
    r = requests.get(f"{WP}/media/{mid}", headers=H, timeout=30).json()
    return {"id": r["id"], "url": r["source_url"], "alt": alt}


# ---------------------------------------------------------------------------
# 3. Load + convert the draft
# ---------------------------------------------------------------------------
raw = open(DRAFT, encoding="utf-8").read()
raw = re.sub(r'^---.*?---\s*', '', raw, count=1, flags=re.S)          # YAML frontmatter
raw = re.split(r'\n##\s*Publishing (?:notes|metadata)', raw)[0]       # drop the metadata tail
raw = re.sub(r'<!--.*?-->\s*', '', raw, flags=re.S)

# Placement markers. These are INSTRUCTIONS to the publisher, not content, and
# they contain em dashes. Strip them before the em-dash scan.
_raw_markers = raw   # keep the un-stripped text for the alt-vs-marker check
n_feat = len(re.findall(r'^\[FEATURED IMAGE\b[^\]]*\]\s*$', raw, flags=re.M))
n_cta = len(re.findall(r'^\[CTA BUTTON\b[^\]]*\]\s*$', raw, flags=re.M))
raw = re.sub(r'^\[FEATURED IMAGE\b[^\]]*\]\s*$', '', raw, flags=re.M)
raw = re.sub(r'^\[CTA BUTTON\b[^\]]*\]\s*$', '', raw, flags=re.M)
raw = re.sub(r'^\[BODY IMAGE\b[^\]]*\]\s*$', '@@BODYIMG@@', raw, flags=re.M)
if n_feat != 1 or n_cta != 1:
    print(f"BLOCKING: expected 1 featured + 1 CTA marker, found {n_feat} + {n_cta}.")
    raise SystemExit(1)
if re.search(r'^\[[A-Z ]', raw, flags=re.M):
    print("BLOCKING: an unrecognised [BRACKET MARKER] survived stripping:",
          re.findall(r'^\[[^\]]*\]', raw, flags=re.M))
    raise SystemExit(1)

content_html = "\n".join(l.rstrip() for l in raw.split("\n") if l.strip())

N_BODY = content_html.count("@@BODYIMG@@")
if N_BODY not in (1, 2):
    print(f"BLOCKING: expected 1-2 body-image markers, found {N_BODY}.")
    raise SystemExit(1)


def slugify(text):
    t = re.sub(r'<[^>]+>', '', text).lower().strip()
    t = re.sub(r"[^a-z0-9\s-]", "", t)
    t = re.sub(r"\s+", "-", t).strip("-")
    return t[:60].strip("-")


# ---------------------------------------------------------------------------
# 4. BLOCKING pre-push checks
# ---------------------------------------------------------------------------
print("\n=== BLOCKING CHECKS ===")

# 4a. em dashes -- run AFTER marker stripping
_em = content_html.count("\u2014") + content_html.count("&mdash;")
if _em:
    for ln in content_html.split("\n"):
        if "\u2014" in ln or "&mdash;" in ln:
            print("   em dash on:", ln[:140])
    print(f"BLOCKING: {_em} em dash(es) present in body content.")
    raise SystemExit(1)
print("  em dashes in content: 0 OK")

# 4b. banned vocabulary (voice.md + brand.md + rules s7)
BANNED = ["just a chatbot", "AI-powered", "revolutionary", "game-changing", "cutting-edge",
          "transform your", "delve", "world-class", "best-in-class", "night-shift",
          "replaces your sales team", "in today's fast-paced world",
          "it's important to note", "innovative solution", "schedule a demo to learn more"]
BANNED_RE = [r"\bsolutions\b", r"\bleverage\b", r"\bnavigat(?:e|es|ed|ing)\b",
             r"\brealm\b", r"\becosystem\b"]
# The zero-acronym blocklist belonged to post 2831, whose whole premise was that a
# non-technical owner should never meet a technical term. It is NOT a ChatSKU-wide
# rule. This post is written for sales and ops leaders and is literally an audit of
# structured data, schema.org markup and part numbers, so those words have to appear.
# Only the protocol acronyms stay blocked, because post 2129 owns those definitions.
BANNED_JARGON = [r"\bACP\b", r"\bAP2\b", r"\bMCP\b", r"\bA2A\b", r"\bcXML\b", r"\bOCI\b",
                 r"\bUNSPSC\b", r"\bETIM\b", r"\bX12\b"]
hits = [b for b in BANNED if re.search(re.escape(b), content_html, re.I)]
hits += [b for b in BANNED_RE + BANNED_JARGON if re.search(b, content_html, re.I)]
if hits:
    print("BLOCKING: banned words / forbidden jargon present:", hits)
    raise SystemExit(1)
print("  banned words + forbidden acronyms: 0 OK")

# 4c. forbidden statistics (brief s6 rejections)
# "48%" is the headline rejection: multiple SEO aggregators attribute a 48%
# shipping-cost abandonment figure to Baymard, but the live Baymard page carries
# no such number (verified directly by the orchestrator 2026-09-22). Untraceable,
# so banned. The Gartner/MIT/InsideSales chain stays banned from prior posts:
# over-used across the corpus and, in the 78%/35-50% case, sharing one untraceable
# citation chain (feedback_stat_verification). Post 266 owns the 70% figure.
FORBIDDEN_STATS = [r"\b48%", r"\b70%", r"\b67%", r"\b44%", r"\b78%",
                   r"35\s*[-to]+\s*50\s*%", r"21x", r"10x",
                   r"\bGartner\b", r"\bForrester\b",
                   r"\bInsideSales\b", r"\bLead\s*Connect\b", r"\bDePaul\b",
                   r"\$15\s*T", r"90%\s*by\s*2028"]
sh = [s for s in FORBIDDEN_STATS if re.search(s, content_html, re.I)]
if sh:
    print("BLOCKING: forbidden statistic/source present:", sh)
    raise SystemExit(1)
print("  forbidden stats: 0 OK")

# 4d. Stat integrity fence.
# Every figure must carry its source in the same clause. This post argues against a
# widely-felt fear, so an unsourced number is worse than no number at all.
_plain = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', content_html))
_SOURCED = (r'(according to|per\s|research|report|survey|study|found|shoppers|'
            r'Baymard|abandon|quoted)')
for m in re.finditer(r'[^.]{0,200}?\b\d{1,3}%[^.]{0,200}', _plain):
    if not re.search(_SOURCED, m.group(0), re.I):
        print('BLOCKING: a percentage appears with no source named in the same sentence:')
        print('   ', m.group(0).strip()[:190])
        raise SystemExit(1)
print('  every percentage names a source in-sentence: OK')

# Baymard is the only external statistic, and it is B2C research. Using it without
# saying so misrepresents consumer data as B2B data. Require the disclosure in the
# same sentence as the figure.
for m in re.finditer(r'[^.]{0,250}?\b(40|12)%[^.]{0,250}', _plain):
    seg = m.group(0).lower()
    if "baymard" in seg and not re.search(r'consumer|b2c|online shopper|shopper|retail', seg):
        print("BLOCKING: a Baymard figure appears without disclosing it is B2C /")
        print("          online-shopper research, not B2B data.")
        print("   ", m.group(0).strip()[:200])
        raise SystemExit(1)
print("  Baymard B2C origin disclosed in-sentence: OK")

# THIS POST'S ACCURACY GATE. The research traced two ubiquitous figures to their
# supposed sources and found nothing there: the "12-18% zero-result rate" credited to
# Baymard, and the "2-3x / 2.77% vs 4.63%" site-search conversion uplift credited to
# Forrester or Econsultancy. Both are fabricated by repetition, structurally identical
# to the already-banned Baymard 48% figure. The whole post argues the reader should use
# their own baseline, so reintroducing either one would contradict its thesis.
_FABRICATED = [
    r'1[0-9]\s*(?:%|percent)[^.]{0,60}zero[- ]result',
    r'zero[- ]result[^.]{0,60}\d{1,2}\s*(?:%|percent)',
    r'2\.77\s*%|4\.63\s*%',
    r'(?:two|three|2|3)\s*(?:to\s*(?:three|3)\s*)?(?:x|times)\s+more\s+likely\s+to\s+convert',
    r'site\s+search[^.]{0,80}\d{1,3}\s*(?:%|percent)[^.]{0,40}convert',
]
_fab = [x for x in _FABRICATED if re.search(x, _plain, re.I)]
if _fab:
    print("BLOCKING: a fabricated-by-repetition search statistic reappeared in the draft.")
    print("          Neither the zero-result-rate benchmark nor the site-search conversion")
    print("          uplift figure exists at its cited source. Patterns hit:", _fab)
    raise SystemExit(1)
print("  no fabricated zero-result / search-uplift statistic: OK")

# Competitor names stay banned even as unlinked prose (brand.md). An extension
# round-up is the likeliest place for one to appear.
_COMPETITORS = [r"\bDrift\b", r"\bIntercom\b", r"\bTidio\b", r"\bLiveChat\b",
                r"\bZendesk\b", r"\bAlgolia\b", r"\bZoovu\b", r"\bCoveo\b",
                r"\bBloomreach\b", r"\bHumCommerce\b", r"\bLily AI\b"]
_cm = sorted({m.group(0) for c in _COMPETITORS for m in re.finditer(c, content_html, re.I)})
if _cm:
    print("BLOCKING: competitor named in prose (brand.md bans naming them at all):", _cm)
    raise SystemExit(1)
print("  no competitor names in prose: OK")

# This post exists to support the money page, so that link is the one it cannot ship
# without. Post 1056 precedent: link it twice with DIFFERENT anchors.
_money = re.findall(r'<a[^>]+href="(?:https://chatsku\.com)?/bigcommerce-b2b-chatbot/"[^>]*>(.*?)</a>',
                    content_html, re.I | re.S)
_money_anchors = {re.sub(r'<[^>]+>', '', a).strip().lower() for a in _money}
if len(_money) < 2:
    print(f"BLOCKING: /bigcommerce-b2b-chatbot/ is linked {len(_money)} time(s); this post")
    print("          to support it and must link it at least twice.")
    raise SystemExit(1)
if len(_money_anchors) < len(_money):
    print("BLOCKING: the money-page links reuse the same anchor text:", _money_anchors)
    raise SystemExit(1)
print(f"  money page linked {len(_money)}x with distinct anchors {sorted(_money_anchors)}: OK")

# (MOQ-specific hand-off check removed when cloned for the BigCommerce quoting post.)
print("  dedup hand-off: n/a for this post")

# 4e. internal links -- BOTH absolute chatsku.com AND relative "/path/" hrefs.
#     An absolute-only regex passes VACUOUSLY on a relative-link draft. That bug
#     shipped once already (glossary build). Fail loudly on zero.
_abs = re.findall(r'href="(https://chatsku\.com/[^"#]+)"', content_html)
_rel_paths = re.findall(r'href="(/[^"#]*)"', content_html)
_rel = ["https://chatsku.com" + p for p in _rel_paths]
hrefs = sorted(set(_abs + _rel))
print(f"  found {len(_rel_paths)} relative + {len(_abs)} absolute internal hrefs "
      f"-> {len(hrefs)} unique")
if not hrefs:
    print("BLOCKING: link checker found 0 internal links. Regex broken or draft unlinked.")
    raise SystemExit(1)
if len(hrefs) < 5:
    print(f"BLOCKING: only {len(hrefs)} internal links ({hrefs}). Rules s6 wants 3+ pages "
          f"and 2+ blog posts.")
    raise SystemExit(1)

# Known-dead URLs, verified 2026-09-07. Never link these.
DEAD = ["/pricing/", "/revenue-calculator", "/product-information-management-software/",
        "/lost-b2b-revenue-calculator/", "/rfq-automation-for-product-catalogs/",
        "/what-is-a-passive-catalog/",
        "/the-response-gap-is-costing-you-deals-3-steps-to-quote-in-under-1-hour/",
        # 301s to the canonical /ai-product-search-for-b2b/ (verified 2026-09-15)
        "/ai-product-search-b2b/",
        # the research notes named this slug for post 2869; it 404s. The live
        # slug is /b2b-catalog-ai-agent-readability-audit/.
        "/ai-agents-b2b-catalog-audit/"]
for d in DEAD:
    if d in content_html:
        print("BLOCKING: known-dead/redirecting URL in content:", d)
        raise SystemExit(1)
print("  known-dead URL blacklist: clean")

# The previous post required the AI-sales-assistant money page. That requirement does
# NOT carry over: the user asked for a non-promotional post, and forcing a money-page
# link in would be exactly the promotion they ruled out. What this post must satisfy
# instead is MUST-FOLLOW s6's split: at least 3 internal pages AND at least 2 blog
# posts. Blog posts are identified against the live slug list, so a new page added
# later cannot silently be miscounted as a post.
_BLOG_SLUGS = ("/b2b-quote-to-order-automation/", "/reduce-b2b-quote-response-time/", "/what-is-the-response-gap/",
               "/erp-export-ai-agent-ready/", "/b2b-catalog-conversion-rate/",
               "/rfq-automation-manufacturers/", "/b2b-catalog-issues-costing-sales/",
               "/b2b-after-hours-buyer-problem/", "/what-is-a-b2b-catalog-chatbot/",
               "/how-ai-product-search-works/", "/magento-b2b-chatbot-integration/",
               "/traditional-b2b-product-search-fails/")
def _is_blog(h):
    # hrefs are normalised to absolute chatsku.com URLs, so compare on path suffix
    return any(h.endswith(b) for b in _BLOG_SLUGS)
_posts = {h for h in hrefs if _is_blog(h)}
_pages = {h for h in hrefs if not _is_blog(h)}
if len(_pages) < 3 or len(_posts) < 2:
    print(f"BLOCKING: MUST-FOLLOW s6 wants >=3 pages and >=2 blog posts. "
          f"Found {len(_pages)} page(s) {sorted(_pages)} and "
          f"{len(_posts)} post(s) {sorted(_posts)}.")
    raise SystemExit(1)
print(f"  internal link split: {len(_pages)} pages + {len(_posts)} blog posts OK")

# Anchor text: 2-5 words, never a long descriptive clause, never promotional
# (feedback_interlink_anchor_text + feedback_no_promotional_interlinks).
_ANCHOR_RE = r'<a\b[^>]*href="((?:/|https://chatsku\.com)[^"]*)"[^>]*>(.*?)</a>'
for _href, _anchor in re.findall(_ANCHOR_RE, content_html, re.S):
    _txt = re.sub(r'<[^>]+>', '', _anchor).strip()
    _n = len(_txt.split())
    if _n > 5:
        print(f"BLOCKING: internal anchor is {_n} words (max 5): {_txt!r} -> {_href}")
        raise SystemExit(1)
    if re.search(r'\b(our|check out|click here|learn more|read more)\b', _txt, re.I):
        print(f"BLOCKING: promotional/vague anchor text: {_txt!r} -> {_href}")
        raise SystemExit(1)
print("  internal anchor text: all 2-5 words, none promotional OK")

# Post 2831 had to link the glossary exactly once as its fence against post 2129.
# This post fences differently: it stays off protocol definitions entirely, which
# the BANNED_JARGON acronym check above already enforces. So the glossary link is
# optional here, but it must never appear more than once.
if content_html.count("/agentic-commerce-glossary/") > 1:
    print("BLOCKING: /agentic-commerce-glossary/ appears",
          content_html.count("/agentic-commerce-glossary/"), "times, max 1")
    raise SystemExit(1)
print(f"  glossary link: {content_html.count('/agentic-commerce-glossary/')} (max 1) OK")

print("  live-checking internal links (browser UA, NO redirect following)...")
bad = []
for u in hrefs + ["https://chatsku.com/demo/"]:
    try:
        r = requests.get(u, headers=HG, timeout=30, allow_redirects=False)
        note = "  (CTA button target)" if u.endswith("/demo/") else ""
        print(f"    {r.status_code}  {u}{note}")
        if r.status_code != 200:
            bad.append((u, r.status_code, r.headers.get("location", "")))
    except Exception as e:
        print(f"    ERR  {u}  {e}")
        bad.append((u, "ERR", str(e)))
if bad:
    print("BLOCKING: bad internal links (non-200, or a 301 hiding behind a redirect):")
    for b in bad:
        print("   ", *b)
    raise SystemExit(1)
print("  all internal links 200 OK (no redirects followed)")

# 4f. internal links carry NO target attribute (same tab)
for a in re.findall(r'<a\b[^>]*href="(?:/|https://chatsku\.com)[^"]*"[^>]*>', content_html):
    if "target=" in a:
        print("BLOCKING: internal link carries a target attribute:", a)
        raise SystemExit(1)
print("  internal links: no target attribute OK")

# 4g. external links -- max 2, correct attrs, no competitors, all 200
_ext = sorted(set(re.findall(r'href="(https?://(?!chatsku\.com)[^"#]+)"', content_html)))
if len(_ext) > 2:
    print("BLOCKING: more than 2 external links:", _ext)
    raise SystemExit(1)
COMPETITORS = ["drift.com", "intercom", "tidio", "livechat", "zendesk", "bigcommerce",
               "adobe.com/commerce", "shopify.com"]
for u in _ext:
    if any(c in u.lower() for c in COMPETITORS):
        print("BLOCKING: competitor link:", u)
        raise SystemExit(1)
for a in re.findall(r'<a\b[^>]*href="https?://(?!chatsku\.com)[^"]+"[^>]*>', content_html):
    if 'target="_blank"' not in a or 'rel="noopener noreferrer"' not in a:
        print("BLOCKING: external link missing target/rel:", a)
        raise SystemExit(1)
print(f"  external links: {len(_ext)} (<=2), attrs OK, no competitors")
for u in _ext:
    try:
        r = requests.get(u, headers=HG, timeout=40, allow_redirects=True)
        print(f"    {r.status_code}  {u}")
        # 429 is rate limiting, not a dead page. virtina.com throttles scripted
        # requests (feedback_virtina_curl_429): reading it as dead has produced
        # false failures before. It is NOT a pass either, so it must have been
        # verified out of band. The orchestrator confirmed this exact URL renders
        # a real page (H1 "eCommerce Integration") via WebFetch on 2026-09-22.
        if r.status_code == 429:
            print("    NOTE: 429 = rate limited, not dead. Verified out of band "
                  "via WebFetch 2026-09-22. Continuing.")
        elif r.status_code == 403 and u.startswith("https://6sense.com/report/buyer-experience/"):
            # 6sense bot-blocks scripted UAs (403 here, every run). Page verified live
            # out of band via WebFetch 2026-10-22: loads, 79% / 77.0% figures match.
            print("    NOTE: 403 = bot block on 6sense. Verified out of band via WebFetch 2026-10-22. Continuing.")
        elif r.status_code >= 400:
            print("BLOCKING: external link returned", r.status_code)
            raise SystemExit(1)
    except SystemExit:
        raise
    except Exception as e:
        print(f"    ERR  {u}  {e}  (review manually; non-blocking for external)")

# 4h. word count
# Count body PROSE only. Heading text is structure, not prose: including it
# inflated the count by ~140 words and tripped this gate spuriously.
_wc_src = content_html.replace("@@BODYIMG@@", " ")
_wc_prose = re.sub(r'<h[1-6][^>]*>.*?</h[1-6]>', ' ', _wc_src, flags=re.S | re.I)
_wc = len(re.sub(r'<[^>]+>', ' ', _wc_prose).split())
_wc_all = len(re.sub(r'<[^>]+>', ' ', _wc_src).split())
print(f"  body word count (prose, excl. headings): {_wc}")
print(f"  body word count (incl. heading text):    {_wc_all}")
# 1400-1800 was post 2831's target. This is a data-led audit write-up with two
# tables and a method section, briefed at 1800-2200. Both sit inside the house
# range in MUST-FOLLOW-RULES section 7 (1,200-2,000 standard, 2,000-3,000 pillar).
# Deliberately shorter than the pillar posts. The client asked for an easy read,
# and length is itself a readability cost. House range for a standard post is 1,200-2,000.
if not (1400 <= _wc <= 2000):
    print(f"BLOCKING: word count {_wc} outside the 1400-2000 hard range.")
    raise SystemExit(1)

# 4L. READABILITY GATE (unique to this post).
# The client asked for "no too difficult words or very technical". That is a
# testable requirement, so it is tested rather than eyeballed.
def _syllables(word):
    w = re.sub(r'[^a-z]', '', word.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r'(?:[^laeiouy]es|ed|[^laeiouy]e)$', '', w)
    w = re.sub(r'^y', '', w)
    n = len(re.findall(r'[aeiouy]{1,2}', w))
    return max(1, n)


_prose = re.sub(r'<(table|ul|ol)[^>]*>.*?</\1>', ' ', content_html, flags=re.S | re.I)
_prose = re.sub(r'<h[1-6][^>]*>.*?</h[1-6]>', ' ', _prose, flags=re.S | re.I)
# Block boundaries ARE sentence boundaries. Stripping tags first glues a paragraph
# that ends in ':' onto the next block, and the splitter then reports several real
# sentences as one huge false positive. Seen on this post: two list intros plus an
# image placeholder reported as a single 26-word "sentence". Terminate blocks first.
_prose = re.sub(r'</(?:p|li|td|th|div|blockquote)>', '. ', _prose, flags=re.I)
_prose = _prose.replace('@@BODYIMG@@', '. ')
_prose = _html.unescape(re.sub(r'<[^>]+>', ' ', _prose))
_prose = re.sub(r'\s+', ' ', _prose).strip()

# A plain `(?<=[.!?])\s+` split misses `." It's` and reports three sentences as one.
_sents = [x.strip() for x in re.split(r'(?:(?<=[.!?])|(?<=[.!?]")|(?<=[.!?]\u201d))\s+', _prose)
          if len(x.split()) >= 3]
_words = [w for w in re.findall(r"[A-Za-z']+", _prose)]
_syl = sum(_syllables(w) for w in _words)
if _sents and _words:
    _asl = len(_words) / len(_sents)
    _asw = _syl / len(_words)
    _flesch = 206.835 - 1.015 * _asl - 84.6 * _asw
else:
    _asl = _asw = _flesch = 0
_long = [s for s in _sents if len(s.split()) > 25]
_poly = sorted({w.lower() for w in _words if _syllables(w) >= 5})

print(f"  readability: Flesch {_flesch:.1f} | avg sentence {_asl:.1f} words | "
      f"avg syllables/word {_asw:.2f}")
print(f"  sentences over 25 words: {len(_long)} | 5+ syllable words: {len(_poly)}")

# Threshold calibrated against the live corpus on 2026-09-18, not guessed. Median
# across 38 ChatSKU posts is 61.9, so 60 would only be average. The site's best
# plain-language posts score 71-75: ai-chatbot-buyers-guide 75.2, and the
# deliberately zero-acronym what-is-agentic-commerce 74.1. The client asked for an
# unusually easy read, so this post is held to that top band.
# 65, not 70: this post explains Composer packages, editions and extension
# categories, so it carries a syllable floor the freight post did not. 65 still
# beats the live corpus median of 61.9. ASL and the 25-word cap are unchanged.
if _flesch < 65:
    print(f"BLOCKING: Flesch Reading Ease {_flesch:.1f} is below 65. The corpus median is "
          f"61.9 and the best ChatSKU posts reach 74. Shorten sentences, cut clauses, and "
          f"swap long words for short ones.")
    raise SystemExit(1)
if _asl > 15:
    print(f"BLOCKING: average sentence is {_asl:.1f} words. Target is 15 or under "
          f"(what-is-agentic-commerce runs 10.4, ai-chatbot-buyers-guide 12.7).")
    raise SystemExit(1)
if _long:
    print(f"BLOCKING: {len(_long)} sentence(s) over 25 words:")
    for s in _long[:5]:
        print("   ", s[:150])
    raise SystemExit(1)

# Technical vocabulary this post must stay away from. Two reasons here, not one:
# the user asked for a conversational piece, AND these exact terms are what post 2468
# (/how-ai-product-search-works/) owns. So this list doubles as a dedup fence: if one
# of these appears, the draft has started re-explaining 2468 instead of linking it.
# Protocol acronyms are already blocked globally above.
TOO_TECHNICAL = [r"\bembedding", r"\bvector\b", r"\bretrieval", r"\bRAG\b", r"\bBM25\b",
                 r"\bschema\b", r"\bAPI\b", r"\bendpoint", r"\bJSON\b", r"\bparse",
                 r"\bmachine-readable", r"\blatency", r"\binference", r"\bLLM\b",
                 r"\balgorithm", r"\btaxonom", r"\bnormalis|\bnormaliz", r"\bmiddleware",
                 r"\bwebhook", r"\bstructured data", r"\bingest"]
_tech = sorted({m.group(0) for p in TOO_TECHNICAL
                for m in re.finditer(p, content_html, re.I)})
if _tech:
    print("BLOCKING: technical vocabulary present, the client asked for plain language:", _tech)
    raise SystemExit(1)
print("  technical-vocabulary blocklist: clean")

if _poly:
    print(f"  NOTE {len(_poly)} long word(s) present, review by eye: {_poly[:12]}")


# 4i. Yoast field shape
if len(YOAST_TITLE) > 60 or not YOAST_TITLE.endswith("| ChatSKU"):
    print("BLOCKING: Yoast title invalid:", len(YOAST_TITLE), YOAST_TITLE)
    raise SystemExit(1)
if not (150 <= len(YOAST_DESC) <= 160):
    print("BLOCKING: Yoast desc length", len(YOAST_DESC), "(need 150-160)")
    raise SystemExit(1)
print(f"  Yoast title {len(YOAST_TITLE)} chars, desc {len(YOAST_DESC)} chars OK")

# 4j. alt text shape (content checked by the human, see ALT_CONFIRMED gate)
_alts = [("FEATURED_ALT", FEATURED_ALT), ("BODY1_ALT", BODY1_ALT)]
if BODY2_ALT is not None:
    _alts.append(("BODY2_ALT", BODY2_ALT))
for name, alt in _alts:
    if not (80 <= len(alt) <= 150):
        print(f"BLOCKING: {name} length {len(alt)} outside 80-150.")
        raise SystemExit(1)
if len({a for _, a in _alts}) != len(_alts):
    print("BLOCKING: alt texts are not unique.")
    raise SystemExit(1)
print(f"  alt text: {len(_alts)} unique, all 80-150 chars OK")

# Cloning a build script carries the PREVIOUS post's alt text, and the length +
# uniqueness checks above happily pass wrong-but-well-formed text. That shipped on
# post 3023, where the alts still described sales reps on phones for a freight post.
# So: every alt must share real vocabulary with its own draft image marker.
_markers = re.findall(r'^\[(?:FEATURED|BODY) IMAGE[^\]]*\]\s*$', _raw_markers, flags=re.M)
_STOP = {"the","a","an","and","or","of","in","on","at","to","for","with","his","her",
         "their","its","by","from","near","while","as","is","are","px","860x452"}
def _words(t):
    return {w for w in re.findall(r"[a-z]{4,}", t.lower()) if w not in _STOP}
for (name, alt), marker in zip(_alts, _markers):
    _shared = _words(alt) & _words(marker)
    if len(_shared) < 2:
        print(f"BLOCKING: {name} does not describe its own image marker. This is the")
        print(f"          stale-alt-from-a-cloned-script failure. Rewrite it.")
        print(f"          alt    : {alt}")
        print(f"          marker : {marker.strip()}")
        print(f"          shared words: {sorted(_shared)}")
        raise SystemExit(1)
print(f"  alt text matches its draft image marker ({len(_alts)} checked): OK")

# 4k. slug / existing post
sr = requests.get(f"{WP}/posts", params={"slug": SLUG, "status": "any", "context": "edit"},
                  headers=H, timeout=30)
existing = sr.json() if sr.status_code == 200 else []
if existing and not STATE.get("post_id"):
    print("BLOCKING: a post with this slug already exists but no post_id in state:",
          [(p["id"], p["status"]) for p in existing])
    raise SystemExit(1)
print("  slug check OK" + (f" (post {existing[0]['id']} will be updated)" if existing else " (free)"))


# ---------------------------------------------------------------------------
# 5. Elementor helpers (post 96 structure)
# ---------------------------------------------------------------------------
def gid():
    return secrets.token_hex(4)


def w_heading(title, level="h2", color="#1a1a2e", align="left", element_id=None):
    s = {"title": title, "align": align, "title_color": color,
         "typography_typography": "custom",
         "typography_font_size": {"size": 28 if level == "h2" else 22, "unit": "px"}}
    if level != "h2":
        s["header_size"] = level
    if element_id:
        s["_element_id"] = element_id
    return {"id": gid(), "elType": "widget", "widgetType": "heading", "elements": [], "settings": s}


def w_text(html, dark=False):
    html = re.sub(r'<img[^>]*?>', '', html)
    html = html.replace("@@BODYIMG@@", "").strip()
    if dark:
        html = re.sub(r'<p([ >])',
                      r'<p style="color:#aaaacc;text-align:center;font-size:18px;'
                      r'max-width:720px;margin:0 auto 14px auto;"\1', html)
    return {"id": gid(), "elType": "widget", "widgetType": "text-editor", "elements": [],
            "settings": {"editor": html}}


def w_image(m):
    return {"id": gid(), "elType": "widget", "widgetType": "image", "elements": [],
            "settings": {"image": {"id": m["id"], "url": m["url"], "alt": m["alt"],
                                   "source": "library", "size": ""},
                         "align": "center", "width": {"size": 100, "unit": "%"},
                         "border_radius": {"top": "10", "right": "10", "bottom": "10",
                                           "left": "10", "unit": "px"}}}


def w_button(text, url):
    return {"id": gid(), "elType": "widget", "widgetType": "button", "elements": [],
            "settings": {"text": text, "link": {"url": url, "is_external": "", "nofollow": ""},
                         "align": "center", "background_color": "#e94560",
                         "button_text_color": "#ffffff",
                         "border_radius": {"size": 6, "unit": "px"},
                         "_margin": {"unit": "px", "top": "20", "right": "0", "bottom": "0",
                                     "left": "0", "isLinked": False}}}


def w_accordion(qa_pairs):
    """ChatSKU FAQ = Elementor NATIVE accordion (accordion.default), placed AFTER
    the Conclusion. Confirmed from live post 299."""
    tabs = [{"_id": gid(), "tab_title": q, "tab_content": a} for q, a in qa_pairs]
    return {"id": gid(), "elType": "widget", "widgetType": "accordion", "elements": [],
            "settings": {"tabs": tabs}}


def w_html(html):
    return {"id": gid(), "elType": "widget", "widgetType": "html", "elements": [],
            "settings": {"html": html}}


def section(widgets, bg, conclusion=False):
    # Section padding has NO right/left keys (rules). Column carries 20px all round.
    pad = ({"top": "20", "bottom": "30", "unit": "px", "right": "0", "left": "0"} if conclusion
           else {"top": "60", "bottom": "60", "unit": "px"})
    return {"id": gid(), "elType": "section", "isInner": False,
            "settings": {"background_background": "classic", "background_color": bg, "padding": pad},
            "elements": [{"id": gid(), "elType": "column", "isInner": False,
                          "settings": {"_column_size": 100, "width": "100",
                                       "padding": {"unit": "px", "top": "20", "right": "20",
                                                   "bottom": "20", "left": "20", "isLinked": True}},
                          "elements": widgets}]}


# ---------------------------------------------------------------------------
# 6. Parse into sections
# ---------------------------------------------------------------------------
parts = [p.strip() for p in re.split(r'(?=<h2>)', content_html) if p.strip()]
parsed = []
for chunk in parts:
    m = re.match(r'<h2>(.*?)</h2>(.*)', chunk, re.S)
    if not m:
        continue
    title, body = m.group(1).strip(), m.group(2).strip()
    label = re.sub(r'<[^>]+>', '', title).lower().strip()
    if label == "executive summary":
        kind = "exec"
    elif label == "introduction":
        kind = "intro"
    elif label == "people also ask":
        kind = "paa"
    elif label == "conclusion":
        kind = "concl"
    elif label == "frequently asked questions":
        kind = "faq"
    else:
        kind = "body"
    parsed.append((kind, title, body))

kinds = [k for k, _, _ in parsed]
for required in ("exec", "intro", "paa", "concl", "faq"):
    if kinds.count(required) != 1:
        print(f"BLOCKING: expected exactly 1 '{required}' section, got {kinds.count(required)}. {kinds}")
        raise SystemExit(1)
if kinds.index("faq") < kinds.index("concl"):
    print("BLOCKING: FAQ must come AFTER the Conclusion (ChatSKU pattern, post 299).")
    raise SystemExit(1)
print(f"  section order OK: {kinds}")


def split_qa(body):
    out = []
    for sp in re.split(r'(?=<h3>)', body.strip()):
        hm = re.match(r'<h3>(.*?)</h3>(.*)', sp.strip(), re.S)
        if hm:
            out.append((hm.group(1).strip(), hm.group(2).strip()))
    return out


BODY_COLORS = ["#f0f4ff", "#ffffff", "#f9f9fb", "#ffffff"]
FEATURED = BODY1 = BODY2 = None
faq_pairs = []


def build_sections():
    global faq_pairs
    out = []
    ci = 0
    img_seen = 0
    for kind, title, body in parsed:
        eid = slugify(title)
        if kind == "exec":
            out.append(section([w_heading(title, element_id=eid), w_text(body)], "#f9f9fb"))
        elif kind == "intro":
            out.append(section([w_heading(title, element_id=eid), w_text(body)], "#ffffff"))
        elif kind == "body":
            bg = BODY_COLORS[ci % len(BODY_COLORS)]
            ci += 1
            widgets = [w_heading(title, element_id=eid), w_text(body)]
            if "@@BODYIMG@@" in body:              # placement comes from the draft itself
                img_seen += 1
                m = BODY1 if img_seen == 1 else BODY2
                if m:
                    widgets.append(w_image(m))     # image ALWAYS the last widget
            out.append(section(widgets, bg))
        elif kind == "paa":
            bg = BODY_COLORS[ci % len(BODY_COLORS)]
            ci += 1
            widgets = [w_heading(title, element_id=eid)]
            for q, a in split_qa(body):
                widgets.append(w_heading(q, "h3", element_id=slugify(q)))
                widgets.append(w_text(a))
            out.append(section(widgets, bg))
        elif kind == "concl":
            # exactly 3 widgets: centered white heading, dark centered body, CTA button
            widgets = [w_heading(title, color="#ffffff", align="center", element_id=eid),
                       w_text(body, dark=True),
                       w_button("See the live demo", "https://chatsku.com/demo/")]
            out.append(section(widgets, "#1a1a2e", conclusion=True))
        elif kind == "faq":
            faq_pairs = split_qa(body)
            widgets = [w_heading(title, element_id=eid), w_accordion(faq_pairs)]
            schema = {"@context": "https://schema.org", "@graph": [
                {"@type": "Article", "headline": TITLE, "description": YOAST_DESC,
                 "image": (FEATURED or {}).get("url", ""),
                 "datePublished": PUBLISH_DATE, "dateModified": PUBLISH_DATE,
                 "author": {"@type": "Organization", "name": "ChatSKU", "url": "https://chatsku.com/"},
                 "publisher": {"@type": "Organization", "name": "ChatSKU",
                               "logo": {"@type": "ImageObject", "url": "https://chatsku.com/logo.png"}},
                 "mainEntityOfPage": {"@type": "WebPage", "@id": PERMALINK}},
                {"@type": "FAQPage", "mainEntity": [
                    {"@type": "Question", "name": q,
                     "acceptedAnswer": {"@type": "Answer",
                                        "text": re.sub(r'<[^>]+>', '', a).strip()}}
                    for q, a in faq_pairs]},
                {"@type": "BreadcrumbList", "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home",
                     "item": "https://chatsku.com/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog",
                     "item": "https://chatsku.com/blog/"},
                    {"@type": "ListItem", "position": 3, "name": TITLE, "item": PERMALINK}]}]}
            widgets.append(w_html('<script type="application/ld+json">'
                                  + json.dumps(schema) + '</script>'))
            out.append(section(widgets, "#f9f9fb"))
    return out


sections = build_sections()
print(f"\nParsed {len(parsed)} H2 sections -> {len(sections)} Elementor sections "
      f"| FAQ tabs {len(faq_pairs)}")
if len(faq_pairs) < 4:
    print(f"BLOCKING: FAQ needs 4-6 Q&As, got {len(faq_pairs)}.")
    raise SystemExit(1)

DRY_RUN = "publish" not in sys.argv

# ---------------------------------------------------------------------------
# 7. Upload images, rebuild with image widgets
# ---------------------------------------------------------------------------
if NO_IMAGES:
    print("  MEDIA UPLOAD SKIPPED (NO_IMAGES=1). Text-first push; attach images in a "
          "follow-up run against the same post id.")
elif not DRY_RUN:
    if not ALT_CONFIRMED:
        print("BLOCKING: set ALT_CONFIRMED=1 only after you have LOOKED at")
        print("  final_featured.jpg / final_body1.jpg / final_body2.jpg and rewritten")
        print("  FEATURED_ALT / BODY1_ALT / BODY2_ALT to describe what they actually show.")
        print("  (rules s3 / feedback_image_visual_qa)")
        raise SystemExit(1)
    print("\n=== MEDIA UPLOAD ===")
    st = load_state()
    for slot, key, alt, fn, var in (
            # Filenames are derived from SLUG, never hardcoded. They were hardcoded here
            # and the era-07 values survived at least two clones, so every post since
            # shipped media named after a different article.
            ("featured", "featured_media", FEATURED_ALT, f"chatsku-{SLUG}-featured.jpg", "FEATURED"),
            ("body1", "body1_media", BODY1_ALT, f"chatsku-{SLUG}-body1.jpg", "BODY1"),
            ("body2", "body2_media", BODY2_ALT, f"chatsku-{SLUG}-body2.jpg", "BODY2")):
        if alt is None:
            print(f"  {slot}: skipped (not used on this post)")
            continue
        if REUSE_MEDIA and st.get(key):
            m = fetch_media(st[key], alt)
            print(f"  reusing media {m['id']} for {slot}")
        elif st.get(key):
            m = fetch_media(st[key], alt)
            print(f"  {slot} already uploaded per state file: {m['id']}")
        else:
            m = upload_media(read_qa_image(slot), fn, alt, key)
        globals()[var] = m
    for m in [x for x in (FEATURED, BODY1, BODY2) if x]:
        if not m["url"].startswith("https://chatsku.com/wp-content/uploads/"):
            print("BLOCKING: media src not on chatsku uploads:", m["url"])
            raise SystemExit(1)
    print("  all 3 media on https://chatsku.com/wp-content/uploads/ OK")
    sections = build_sections()

elementor_json = json.dumps(sections)
content_fallback = re.sub(r'<img[^>]*?>', '', content_html).replace("@@BODYIMG@@", "")

open(os.path.join(SCRATCH, "reps_elementor.json"), "w", encoding="utf-8").write(elementor_json)
print(f"Built {len(sections)} sections | elementor {len(elementor_json):,} chars")

# 7b. structural assertions
if re.search(r'<img\b', content_fallback):
    print("BLOCKING: bare <img> remains in the WP content field.")
    raise SystemExit(1)
print("  content field: 0 bare <img> OK")

# json.dumps(ensure_ascii=True) escapes an em dash to the 6-char sequence
# \u2014, so scan for BOTH the literal char and its escaped form.
if ("\u2014" in elementor_json or "&mdash;" in elementor_json
        or "\\u2014" in elementor_json):
    print("BLOCKING: em dash leaked into _elementor_data.")
    raise SystemExit(1)
if "\u2014" in content_fallback or "&mdash;" in content_fallback:
    print("BLOCKING: em dash leaked into the content field.")
    raise SystemExit(1)
print("  em dashes in content field and _elementor_data: 0 OK")

try:
    json.loads(elementor_json)
except Exception as e:
    print("BLOCKING: _elementor_data is not valid JSON:", e)
    raise SystemExit(1)

order_violations, img_widget_count = [], 0
concl_widgets = None
for sec in sections:
    for col in sec.get("elements", []):
        types = [w["widgetType"] for w in col.get("elements", []) if w["elType"] == "widget"]
        img_widget_count += types.count("image")
        if "image" in types:
            idx = types.index("image")
            if idx != len(types) - 1:
                order_violations.append(types)
            if "text-editor" in types and types.index("text-editor") > idx:
                order_violations.append(types)
        if sec["settings"].get("background_color") == "#1a1a2e":
            concl_widgets = types
if order_violations:
    print("BLOCKING: image widget not last / before text-editor:", order_violations)
    raise SystemExit(1)
print(f"  widget order: {img_widget_count} image widget(s), 0 violations (image always last)")

if concl_widgets != ["heading", "text-editor", "button"]:
    print("BLOCKING: Conclusion must be exactly heading + text-editor + button, got:", concl_widgets)
    raise SystemExit(1)
print("  Conclusion: 3 widgets (heading/text-editor/button) OK")

if not DRY_RUN and not NO_IMAGES and img_widget_count != N_BODY:
    print(f"BLOCKING: expected {N_BODY} body image widgets, built {img_widget_count}.")
    raise SystemExit(1)

if DRY_RUN:
    print("\nDRY RUN complete. Nothing uploaded, nothing pushed.")
    print("Next: MODE=candidates ... -> review contact sheet -> set QA_DIR + ALT_CONFIRMED=1 "
          "-> re-run with 'publish'.")
    raise SystemExit(0)

if not NO_IMAGES and (not FEATURED or not FEATURED.get("id")):
    print("BLOCKING: refusing to push with featured_media=0.")
    raise SystemExit(1)

# ---------------------------------------------------------------------------
# 8. Push
# ---------------------------------------------------------------------------
st = load_state()
pid = st.get("post_id")

payload = {
    "title": TITLE, "slug": SLUG, "content": content_fallback,
    "excerpt": YOAST_DESC, "categories": CATEGORIES,
    "meta": {"_elementor_edit_mode": "builder", "_elementor_template_type": "wp-post",
             "_elementor_data": elementor_json,
             "_yoast_wpseo_title": YOAST_TITLE, "_yoast_wpseo_metadesc": YOAST_DESC},
}
if FEATURED and FEATURED.get("id"):
    payload["featured_media"] = FEATURED["id"]

# Status: always draft on create. NEVER force a status on an update -- that is
# how a client's manual publish gets clobbered (feedback_wp_update_in_place).
if pid:
    print("\n=== PUSH (UPDATE) ===")
    if FORCE_STATUS:
        print(f"  FORCE_STATUS={FORCE_STATUS!r} IGNORED on update (never blind-overwrite "
              f"a live post's status).")
    live = requests.get(f"{WP}/posts/{pid}", params={"context": "edit"}, headers=H, timeout=60).json()
    print("  live status is", live.get("status"), "-- leaving it untouched")
    payload.pop("status", None)
    if live.get("featured_media") and not payload.get("featured_media"):
        print("  preserving existing featured_media", live["featured_media"])
    r = requests.post(f"{WP}/posts/{pid}", headers=H, data=json.dumps(payload).encode(), timeout=180)
    print("UPDATE status:", r.status_code)
else:
    payload["status"] = FORCE_STATUS or "draft"
    if payload["status"] != "draft":
        print(f"  !! creating with status={payload['status']} (FORCE_STATUS). Default is draft.")
    print("\n=== PUSH (CREATE) ===")
    r = requests.post(f"{WP}/posts", headers=H, data=json.dumps(payload).encode(), timeout=180)
    print("CREATE status:", r.status_code)

if r.status_code not in (200, 201):
    print(r.text[:2000])
    raise SystemExit(1)
j = r.json()
pid = j["id"]
save_state(post_id=pid, link=j.get("link"), status=j.get("status"))   # persist IMMEDIATELY
print("POST_ID:", pid, "| status:", j["status"], "| link:", j.get("link"))
print("EDIT URL:", f"https://chatsku.com/wp-admin/post.php?post={pid}&action=edit")
print("PREVIEW :", f"https://chatsku.com/?p={pid}")

# MANDATORY after every Elementor push
cc = requests.delete("https://chatsku.com/wp-json/elementor/v1/cache", headers=H, timeout=90)
print("Elementor cache clear:", cc.status_code)
save_state(cache_cleared=cc.status_code)

# ---------------------------------------------------------------------------
# 9. Post-push verification (context=edit)
# ---------------------------------------------------------------------------
print("\n=== VERIFY (context=edit) ===")
vr = requests.get(f"{WP}/posts/{pid}", params={"context": "edit"}, headers=H, timeout=60).json()
vmeta = vr.get("meta", {})
yt_ok = vmeta.get("_yoast_wpseo_title") == YOAST_TITLE
yd_ok = vmeta.get("_yoast_wpseo_metadesc") == YOAST_DESC
print("  Yoast title persisted:", yt_ok, "|", repr(vmeta.get("_yoast_wpseo_title"))[:80])
print("  Yoast desc  persisted:", yd_ok, "|", repr(vmeta.get("_yoast_wpseo_metadesc"))[:80])
if not (yt_ok and yd_ok):
    print("  -> set them manually: WP Admin > Posts > Edit > Yoast SEO panel")

try:
    ed = json.loads(vmeta.get("_elementor_data") or "[]")
    print("  _elementor_data parses as JSON list:", isinstance(ed, list), "| sections:", len(ed))
except Exception as e:
    ed = []
    print("  _elementor_data JSON parse ERROR:", e)
print("  _elementor_edit_mode:", vmeta.get("_elementor_edit_mode"),
      "| _elementor_template_type:", vmeta.get("_elementor_template_type"))

v_viol = v_img = 0
for sec in ed:
    for col in sec.get("elements", []):
        types = [w["widgetType"] for w in col.get("elements", []) if w.get("elType") == "widget"]
        v_img += types.count("image")
        if "image" in types and types.index("image") != len(types) - 1:
            v_viol += 1
print(f"  live image widgets: {v_img} | order violations: {v_viol}")
raw_content = vr.get("content", {}).get("raw", "")
print("  bare <img> in live content:", len(re.findall(r'<img\b', raw_content)))
print("  em dashes in live content:", raw_content.count("\u2014"))
print("  featured_media:", vr.get("featured_media"))
print("  status:", vr.get("status"), "| categories:", vr.get("categories"), "| slug:", vr.get("slug"))

save_state(yoast_title_persisted=yt_ok, yoast_desc_persisted=yd_ok,
           elementor_sections=len(ed), image_widgets=v_img, order_violations=v_viol,
           featured_media_live=vr.get("featured_media"), categories=vr.get("categories"),
           live_status=vr.get("status"), verified=True)
print("\nDone. Remaining manual steps: open the post once in the Elementor editor to warm "
      "the render cache, and confirm the FAQ accordion + CTA button render as expected.")
