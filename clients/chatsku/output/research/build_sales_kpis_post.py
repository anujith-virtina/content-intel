# -*- coding: utf-8 -*-
"""Build + publish (draft) ChatSKU post:

    "What changes in your sales KPIs, comp plan, and ramp-up once AI handles first-touch"
    slug: sales-kpis-comp-ramp-ai-catalog-assistant
    Format A (standard explanatory). Support post for the live
    /will-ai-replace-b2b-sales-reps/ (3010): prescriptive, not narrative, three
    concrete levers (KPIs, comp, ramp curriculum), deliberately NOT a rehash of
    3010's four-persona narrative.

Adapted from build_moq_post.py (post 3281), the current canonical ChatSKU
Elementor builder with the full blocking-check suite. Differences forced by
this draft:

  - Stats discipline is bespoke: the BCG 2025 survey may appear ONLY as hedged,
    unlinked, no-number-attached evidence that a gap exists. The SalesCookie
    5-12% pay-premium figure and any Mindtickle ramp-time percentage must never
    appear at all (brief explicitly rejected both as inapplicable/unsourced).
  - Product-claims fence: "deflection rate", "qualified-handoff rate", and
    "time-to-quota" must be framed as the post's OWN proposed framework, never
    as a named ChatSKU dashboard feature.
  - Mandatory link to /will-ai-replace-b2b-sales-reps/ (the post this one
    supports) at least once, not twice -- this is a sibling blog post, not a
    money page, and the brief asked for a single natural mention.
  - 8-gram phrasing-uniqueness check against post 3010 added (rules s1.D),
    since the MOQ script didn't need one (different cluster).

Run:
    python build_sales_kpis_post.py                               # DRY RUN
    QA_DIR=... ALT_CONFIRMED=1 python build_sales_kpis_post.py publish
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

try:
    U = os.environ["CHATSKU_WP_USERNAME"]
    A = os.environ["CHATSKU_WP_APP_PASSWORD"]
except KeyError as e:
    print(f"BLOCKING: missing credential {e}. Expected CHATSKU_WP_USERNAME / "
          f"CHATSKU_WP_APP_PASSWORD in {ENV_PATH}.")
    raise SystemExit(1)
AUTH = base64.b64encode(f"{U}:{A}".encode()).decode()
H = {"Authorization": f"Basic {AUTH}", "User-Agent": UA, "Content-Type": "application/json"}
HG = {"User-Agent": UA}

TITLE = "What changes in your sales KPIs, comp plan, and ramp-up once AI handles first-touch"
SLUG = "sales-kpis-comp-ramp-ai-catalog-assistant"
PERMALINK = f"https://chatsku.com/{SLUG}/"
DRAFT = r"C:\content-intel\clients\chatsku\output\drafts\sales-kpis-comp-ramp-ai-catalog-assistant-2026-10-05.md"
YOAST_TITLE = 'Sales KPIs, Comp, and Ramp After an AI Assistant | ChatSKU'   # 58 chars
YOAST_DESC = ("Once an AI catalog assistant handles first-touch, your old sales KPIs, "
              "comp plan, and ramp curriculum measure a job that no longer exists. Here's the fix.")  # 158 chars
PUBLISH_DATE = "2026-10-05"
CATEGORIES = [22, 29]   # B2B Commerce, Chatbot -- verified live 2026-10-05, matches sibling post 3010 minus Catalog Optimization (not a catalog topic)

BASE = os.path.dirname(os.path.abspath(__file__))
STATE_PATH = os.path.join(BASE, "sales_kpis_push_state.json")
SCRATCH = os.environ.get("SCRATCH_DIR", BASE)
QA_DIR = os.environ.get("QA_DIR", "")
MODE = os.environ.get("MODE", "").lower()
NO_IMAGES = os.environ.get("NO_IMAGES") == "1"
REUSE_MEDIA = os.environ.get("REUSE_MEDIA") == "1"
UPDATE_POST_ID = os.environ.get("UPDATE_POST_ID", "").strip()
FORCE_STATUS = os.environ.get("FORCE_STATUS", "").strip()
ALT_CONFIRMED = os.environ.get("ALT_CONFIRMED") == "1"

# ---------------------------------------------------------------------------
# 0a. ALT TEXT -- rewritten against the images ACTUALLY chosen and visually QA'd.
# ---------------------------------------------------------------------------
FEATURED_ALT = "A sales manager smiles while reviewing performance metrics on a laptop at his desk in a modern office."
BODY1_ALT = "A sales manager explains new performance metrics to his team gathered around a laptop in a meeting."
BODY2_ALT = "A sales manager points to a laptop screen while coaching a colleague through a handoff review together."


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


def read_qa_image(slot):
    if not QA_DIR:
        print("BLOCKING: QA_DIR is not set.")
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
    save_state(**{state_key: mid})
    requests.post(f"{WP}/media/{mid}", headers=H,
                  data=json.dumps({"alt_text": alt_text}).encode(), timeout=60)
    print(f"  uploaded media {mid}: {media['source_url']}")
    return {"id": mid, "url": media["source_url"], "alt": alt_text}


def fetch_media(mid, alt):
    r = requests.get(f"{WP}/media/{mid}", headers=H, timeout=30).json()
    return {"id": r["id"], "url": r["source_url"], "alt": alt}


# ---------------------------------------------------------------------------
# 1. Load + convert the draft
# ---------------------------------------------------------------------------
raw = open(DRAFT, encoding="utf-8").read()
raw = re.sub(r'^---.*?---\s*', '', raw, count=1, flags=re.S)
raw = re.sub(r'<!--.*?-->\s*', '', raw, flags=re.S)

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
# 2. BLOCKING pre-push checks
# ---------------------------------------------------------------------------
print("\n=== BLOCKING CHECKS ===")

_em = content_html.count("\u2014") + content_html.count("&mdash;")
if _em:
    print(f"BLOCKING: {_em} em dash(es) present in body content.")
    raise SystemExit(1)
print("  em dashes in content: 0 OK")

BANNED = ["just a chatbot", "AI-powered", "revolutionary", "game-changing", "cutting-edge",
          "transform your", "delve", "world-class", "best-in-class",
          "replaces your sales team", "in today's fast-paced world",
          "it's important to note", "innovative solution"]
BANNED_RE = [r"\bsolutions\b", r"\bleverage\b", r"\bnavigat(?:e|es|ed|ing)\b",
             r"\brealm\b", r"\becosystem\b"]
hits = [b for b in BANNED if re.search(re.escape(b), content_html, re.I)]
hits += [b for b in BANNED_RE if re.search(b, content_html, re.I)]
if hits:
    print("BLOCKING: banned words present:", hits)
    raise SystemExit(1)
print("  banned words: 0 OK")

# 2a. STATS DISCIPLINE -- bespoke to this post, per the brief's binding rules.
FORBIDDEN_STATS = [
    r"5\s*[-to]+\s*12\s*%",          # SalesCookie pay-premium figure, no methodology
    r"\bSalesCookie\b",
    r"\bMindtickle\b",               # wrong-industry case studies, must not be cited
    r"\bJanssen\b", r"\bRadNet\b", r"\bChowNow\b",
    r"20\s*[-to]+\s*60\s*%",         # Mindtickle's ramp-time range
    r"\b400\s*(?:US\s*)?(?:sales\s*)?reps\b",   # BCG sample size must not be quoted as a hard number
]
sh = [s for s in FORBIDDEN_STATS if re.search(s, content_html, re.I)]
if sh:
    print("BLOCKING: forbidden statistic/source present (stats-discipline fence):", sh)
    raise SystemExit(1)
print("  forbidden stats (SalesCookie/Mindtickle/BCG sample size): 0 OK")

# 2b. PRODUCT-CLAIMS FENCE -- "deflection rate" etc. must read as the post's own
# proposed framework, never as a named ChatSKU dashboard feature. Heuristic:
# none of the three terms may appear within 60 chars of "ChatSKU" + a possessive
# "dashboard"/"report" construction implying it ships out of the box.
_plain_check = re.sub(r'<[^>]+>', ' ', content_html)
_CLAIM_PATTERNS = [
    r"ChatSKU[^.]{0,60}(?:dashboard|report)[^.]{0,30}(?:deflection rate|qualified-handoff rate|time-to-quota)",
    r"(?:deflection rate|qualified-handoff rate|time-to-quota)[^.]{0,30}ChatSKU[^.]{0,30}dashboard",
]
_claim_hits = [p for p in _CLAIM_PATTERNS if re.search(p, _plain_check, re.I)]
if _claim_hits:
    print("BLOCKING: KPI framework phrased as a named ChatSKU out-of-the-box feature:", _claim_hits)
    raise SystemExit(1)
print("  product-claims fence (KPI framework stays the post's own, not a ChatSKU feature): OK")

# 2c. mandatory support link -- this post exists to support 3010, must link it.
if "/will-ai-replace-b2b-sales-reps/" not in content_html:
    print("BLOCKING: this post supports /will-ai-replace-b2b-sales-reps/ and must link it.")
    raise SystemExit(1)
print("  mandatory link to /will-ai-replace-b2b-sales-reps/ present: OK")

_COMPETITORS = [r"\bDrift\b", r"\bIntercom\b", r"\bTidio\b", r"\bLiveChat\b", r"\bZendesk\b"]
_cm = sorted({m.group(0) for c in _COMPETITORS for m in re.finditer(c, content_html, re.I)})
if _cm:
    print("BLOCKING: competitor named in prose:", _cm)
    raise SystemExit(1)
print("  no competitor names in prose: OK")

# 2d. internal links -- relative AND absolute
_abs = re.findall(r'href="(https://chatsku\.com/[^"#]+)"', content_html)
_rel_paths = re.findall(r'href="(/[^"#]*)"', content_html)
_rel = ["https://chatsku.com" + p for p in _rel_paths]
hrefs = sorted(set(_abs + _rel))
print(f"  found {len(_rel_paths)} relative + {len(_abs)} absolute internal hrefs -> {len(hrefs)} unique")
if not hrefs:
    print("BLOCKING: 0 internal links found.")
    raise SystemExit(1)
if len(hrefs) < 5:
    print(f"BLOCKING: only {len(hrefs)} internal links. Rules s6 wants 3+ pages and 2+ blog posts.")
    raise SystemExit(1)

DEAD = ["/pricing/", "/revenue-calculator", "/product-information-management-software/",
        "/lost-b2b-revenue-calculator/", "/rfq-automation-for-product-catalogs/",
        "/what-is-a-passive-catalog/",
        "/the-response-gap-is-costing-you-deals-3-steps-to-quote-in-under-1-hour/",
        "/ai-product-search-b2b/", "/ai-agents-b2b-catalog-audit/"]
for d in DEAD:
    if d in content_html:
        print("BLOCKING: known-dead/redirecting URL in content:", d)
        raise SystemExit(1)
print("  known-dead URL blacklist: clean")

_BLOG_SLUGS = ("/will-ai-replace-b2b-sales-reps/", "/what-is-agentic-commerce/",
               "/b2b-quote-to-order-automation/")
def _is_blog(h):
    return any(h.endswith(b) for b in _BLOG_SLUGS)
_posts = {h for h in hrefs if _is_blog(h)}
_pages = {h for h in hrefs if not _is_blog(h)}
if len(_pages) < 3 or len(_posts) < 2:
    print(f"BLOCKING: need >=3 pages and >=2 blog posts. Found {len(_pages)} page(s) "
          f"{sorted(_pages)} and {len(_posts)} post(s) {sorted(_posts)}.")
    raise SystemExit(1)
print(f"  internal link split: {len(_pages)} pages + {len(_posts)} blog posts OK")

_ANCHOR_RE = r'<a\b[^>]*href="((?:/|https://chatsku\.com)[^"]*)"[^>]*>(.*?)</a>'
for _href, _anchor in re.findall(_ANCHOR_RE, content_html, re.S):
    _txt = re.sub(r'<[^>]+>', '', _anchor).strip()
    _n = len(_txt.split())
    if _n > 6:
        print(f"BLOCKING: internal anchor is {_n} words (max 6): {_txt!r} -> {_href}")
        raise SystemExit(1)
    if re.search(r'\b(our|check out|click here|learn more|read more)\b', _txt, re.I):
        print(f"BLOCKING: promotional/vague anchor text: {_txt!r} -> {_href}")
        raise SystemExit(1)
print("  internal anchor text: clean")

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
    print("BLOCKING: bad internal links:")
    for b in bad:
        print("   ", *b)
    raise SystemExit(1)
print("  all internal links 200 OK (no redirects followed)")

for a in re.findall(r'<a\b[^>]*href="(?:/|https://chatsku\.com)[^"]*"[^>]*>', content_html):
    if "target=" in a:
        print("BLOCKING: internal link carries a target attribute:", a)
        raise SystemExit(1)
print("  internal links: no target attribute OK")

_ext = sorted(set(re.findall(r'href="(https?://(?!chatsku\.com)[^"#]+)"', content_html)))
if len(_ext) > 2:
    print("BLOCKING: more than 2 external links:", _ext)
    raise SystemExit(1)
print(f"  external links: {len(_ext)} (<=2) OK")

# 2e. word count
_wc_src = content_html.replace("@@BODYIMG@@", " ")
_wc_prose = re.sub(r'<h[1-6][^>]*>.*?</h[1-6]>', ' ', _wc_src, flags=re.S | re.I)
_wc = len(re.sub(r'<[^>]+>', ' ', _wc_prose).split())
print(f"  body word count (prose, excl. headings): {_wc}")
if not (1200 <= _wc <= 2100):
    print(f"BLOCKING: word count {_wc} outside the 1200-2100 range (house standard is 1200-2000, "
          f"small buffer allowed).")
    raise SystemExit(1)

# 2f. readability -- logged, not blocking (this post wasn't briefed as zero-jargon
# like 2831/3010, but worth knowing where it lands on the corpus).
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
_prose = re.sub(r'</(?:p|li|td|th|div|blockquote)>', '. ', _prose, flags=re.I)
_prose = _prose.replace('@@BODYIMG@@', '. ')
_prose = _html.unescape(re.sub(r'<[^>]+>', ' ', _prose))
_prose = re.sub(r'\s+', ' ', _prose).strip()
_sents = [x.strip() for x in re.split(r'(?:(?<=[.!?])|(?<=[.!?]")|(?<=[.!?]\u201d))\s+', _prose)
          if len(x.split()) >= 3]
_words = re.findall(r"[A-Za-z']+", _prose)
_syl = sum(_syllables(w) for w in _words)
if _sents and _words:
    _asl = len(_words) / len(_sents)
    _asw = _syl / len(_words)
    _flesch = 206.835 - 1.015 * _asl - 84.6 * _asw
else:
    _asl = _asw = _flesch = 0
print(f"  readability (informational): Flesch {_flesch:.1f} | avg sentence {_asl:.1f} words")

# 2g. Yoast field shape
if len(YOAST_TITLE) > 60 or not YOAST_TITLE.endswith("| ChatSKU"):
    print("BLOCKING: Yoast title invalid:", len(YOAST_TITLE), YOAST_TITLE)
    raise SystemExit(1)
if not (150 <= len(YOAST_DESC) <= 160):
    print("BLOCKING: Yoast desc length", len(YOAST_DESC), "(need 150-160)")
    raise SystemExit(1)
print(f"  Yoast title {len(YOAST_TITLE)} chars, desc {len(YOAST_DESC)} chars OK")

# 2h. alt text shape
_alts = [("FEATURED_ALT", FEATURED_ALT), ("BODY1_ALT", BODY1_ALT), ("BODY2_ALT", BODY2_ALT)]
for name, alt in _alts:
    if not (80 <= len(alt) <= 150):
        print(f"BLOCKING: {name} length {len(alt)} outside 80-150.")
        raise SystemExit(1)
if len({a for _, a in _alts}) != len(_alts):
    print("BLOCKING: alt texts are not unique.")
    raise SystemExit(1)
print(f"  alt text: {len(_alts)} unique, all 80-150 chars OK")

# 2i. slug / existing post
sr = requests.get(f"{WP}/posts", params={"slug": SLUG, "status": "any", "context": "edit"},
                  headers=H, timeout=30)
existing = sr.json() if sr.status_code == 200 else []
if existing and not STATE.get("post_id"):
    print("BLOCKING: a post with this slug already exists but no post_id in state:",
          [(p["id"], p["status"]) for p in existing])
    raise SystemExit(1)
print("  slug check OK" + (f" (post {existing[0]['id']} will be updated)" if existing else " (free)"))

# 2j. 8-gram phrasing uniqueness against post 3010 (the post this one supports,
# so overlap risk is highest here) -- rules s1.D.
print("  8-gram phrasing check against post 3010...")
def _words_for_gram(x):
    return re.sub(r'[^a-z0-9 ]', ' ', x.lower()).split()
try:
    rr = requests.get(f"{WP}/posts/3010", params={"context": "edit", "_fields": "id,slug,content"},
                      headers=H, timeout=60)
    other_raw = rr.json()["content"]["raw"]
    other_plain = re.sub(r'\s+', ' ', _html.unescape(re.sub(r'<[^>]+>', ' ', other_raw)))
    mine_plain = re.sub(r'\s+', ' ', _html.unescape(re.sub(r'<[^>]+>', ' ', content_html)))
    mine_w = _words_for_gram(mine_plain)
    other_w = _words_for_gram(other_plain)
    mine_grams = set(tuple(mine_w[i:i+8]) for i in range(len(mine_w) - 7))
    other_grams = set(tuple(other_w[i:i+8]) for i in range(len(other_w) - 7))
    common = mine_grams & other_grams
    if common:
        print("BLOCKING: verbatim 8+ word sequence(s) shared with post 3010:")
        for c in list(common)[:5]:
            print("    ::", " ".join(c))
        raise SystemExit(1)
    print(f"  no shared 8-word sequences with post 3010 (checked {len(mine_grams)} grams)")
except SystemExit:
    raise
except Exception as e:
    print(f"  WARNING: could not fetch post 3010 for phrasing check ({e}). Proceeding, "
          f"but this check did not actually run.")

# ---------------------------------------------------------------------------
# 3. Elementor helpers (post 96 structure)
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


def w_text(html_frag, dark=False):
    html_frag = re.sub(r'<img[^>]*?>', '', html_frag)
    html_frag = html_frag.replace("@@BODYIMG@@", "").strip()
    if dark:
        html_frag = re.sub(r'<p([ >])',
                      r'<p style="color:#aaaacc;text-align:center;font-size:18px;'
                      r'max-width:720px;margin:0 auto 14px auto;"\1', html_frag)
    return {"id": gid(), "elType": "widget", "widgetType": "text-editor", "elements": [],
            "settings": {"editor": html_frag}}


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
    tabs = [{"_id": gid(), "tab_title": q, "tab_content": a} for q, a in qa_pairs]
    return {"id": gid(), "elType": "widget", "widgetType": "accordion", "elements": [],
            "settings": {"tabs": tabs}}


def w_html(html_frag):
    return {"id": gid(), "elType": "widget", "widgetType": "html", "elements": [],
            "settings": {"html": html_frag}}


def section(widgets, bg, conclusion=False):
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
# 4. Parse into sections
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
            if "@@BODYIMG@@" in body:
                img_seen += 1
                m = BODY1 if img_seen == 1 else BODY2
                if m:
                    widgets.append(w_image(m))
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
print(f"\nParsed {len(parsed)} H2 sections -> {len(sections)} Elementor sections | FAQ tabs {len(faq_pairs)}")
if len(faq_pairs) < 4:
    print(f"BLOCKING: FAQ needs 4-6 Q&As, got {len(faq_pairs)}.")
    raise SystemExit(1)

DRY_RUN = "publish" not in sys.argv

# ---------------------------------------------------------------------------
# 5. Upload images, rebuild with image widgets
# ---------------------------------------------------------------------------
if NO_IMAGES:
    print("  MEDIA UPLOAD SKIPPED (NO_IMAGES=1).")
elif not DRY_RUN:
    if not ALT_CONFIRMED:
        print("BLOCKING: set ALT_CONFIRMED=1 only after visually confirming the alt text matches "
              "the images actually chosen.")
        raise SystemExit(1)
    print("\n=== MEDIA UPLOAD ===")
    st = load_state()
    for slot, key, alt, fn, var in (
            ("featured", "featured_media", FEATURED_ALT, f"chatsku-{SLUG}-featured.jpg", "FEATURED"),
            ("body1", "body1_media", BODY1_ALT, f"chatsku-{SLUG}-body1.jpg", "BODY1"),
            ("body2", "body2_media", BODY2_ALT, f"chatsku-{SLUG}-body2.jpg", "BODY2")):
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

open(os.path.join(SCRATCH, "sales_kpis_elementor.json"), "w", encoding="utf-8").write(elementor_json)
print(f"Built {len(sections)} sections | elementor {len(elementor_json):,} chars")

if re.search(r'<img\b', content_fallback):
    print("BLOCKING: bare <img> remains in the WP content field.")
    raise SystemExit(1)
print("  content field: 0 bare <img> OK")

if ("\u2014" in elementor_json or "&mdash;" in elementor_json or "\\u2014" in elementor_json):
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
print(f"  widget order: {img_widget_count} image widget(s), 0 violations")

if concl_widgets != ["heading", "text-editor", "button"]:
    print("BLOCKING: Conclusion must be exactly heading + text-editor + button, got:", concl_widgets)
    raise SystemExit(1)
print("  Conclusion: 3 widgets OK")

if not DRY_RUN and not NO_IMAGES and img_widget_count != N_BODY:
    print(f"BLOCKING: expected {N_BODY} body image widgets, built {img_widget_count}.")
    raise SystemExit(1)

if DRY_RUN:
    print("\nDRY RUN complete. Nothing uploaded, nothing pushed.")
    print("Next: set QA_DIR + ALT_CONFIRMED=1 -> re-run with 'publish'.")
    raise SystemExit(0)

if not NO_IMAGES and (not FEATURED or not FEATURED.get("id")):
    print("BLOCKING: refusing to push with featured_media=0.")
    raise SystemExit(1)

# ---------------------------------------------------------------------------
# 6. Push
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

if pid:
    print("\n=== PUSH (UPDATE) ===")
    live = requests.get(f"{WP}/posts/{pid}", params={"context": "edit"}, headers=H, timeout=60).json()
    print("  live status is", live.get("status"), "-- leaving it untouched")
    payload.pop("status", None)
    r = requests.post(f"{WP}/posts/{pid}", headers=H, data=json.dumps(payload).encode(), timeout=180)
    print("UPDATE status:", r.status_code)
else:
    payload["status"] = FORCE_STATUS or "draft"
    print("\n=== PUSH (CREATE) ===")
    r = requests.post(f"{WP}/posts", headers=H, data=json.dumps(payload).encode(), timeout=180)
    print("CREATE status:", r.status_code)

if r.status_code not in (200, 201):
    print(r.text[:2000])
    raise SystemExit(1)
j = r.json()
pid = j["id"]
save_state(post_id=pid, link=j.get("link"), status=j.get("status"))
print("POST_ID:", pid, "| status:", j["status"], "| link:", j.get("link"))
print("EDIT URL:", f"https://chatsku.com/wp-admin/post.php?post={pid}&action=edit")
print("PREVIEW :", f"https://chatsku.com/?p={pid}")

cc = requests.delete("https://chatsku.com/wp-json/elementor/v1/cache", headers=H, timeout=90)
print("Elementor cache clear:", cc.status_code)
save_state(cache_cleared=cc.status_code)

# ---------------------------------------------------------------------------
# 7. Post-push verification
# ---------------------------------------------------------------------------
print("\n=== VERIFY (context=edit) ===")
vr = requests.get(f"{WP}/posts/{pid}", params={"context": "edit"}, headers=H, timeout=60).json()
vmeta = vr.get("meta", {})
yt_ok = vmeta.get("_yoast_wpseo_title") == YOAST_TITLE
yd_ok = vmeta.get("_yoast_wpseo_metadesc") == YOAST_DESC
print("  Yoast title persisted:", yt_ok)
print("  Yoast desc  persisted:", yd_ok)
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

raw_content = vr.get("content", {}).get("raw", "")
print("  bare <img> in live content:", len(re.findall(r'<img\b', raw_content)))
print("  em dashes in live content:", raw_content.count("\u2014"))
print("  featured_media:", vr.get("featured_media"))
print("  status:", vr.get("status"), "| categories:", vr.get("categories"), "| slug:", vr.get("slug"))

save_state(yoast_title_persisted=yt_ok, yoast_desc_persisted=yd_ok,
           elementor_sections=len(ed), featured_media_live=vr.get("featured_media"),
           categories=vr.get("categories"), live_status=vr.get("status"), verified=True)
print("\nDone.")
