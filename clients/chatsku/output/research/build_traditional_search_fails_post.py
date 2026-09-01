# -*- coding: utf-8 -*-
"""Build + publish (draft) ChatSKU post:
"How AI product search actually works for B2B catalogs"
slug: how-ai-product-search-works
Format B (conversational Q&A) with a Format E contrarian centre (B5/B6).

Adapted from build_erp_export_ai_ready_post.py (post 2422), which is the
canonical ChatSKU Elementor builder. Differences forced by this draft:

  - The draft marks sections as "### SECTION: Title" (not "## Title") and
    H3s as "**H3: Question?**" (not "### Question?"). Parser rewritten for
    that shape.
  - Body copy is already raw HTML (<p>, <ul>, <table>), so the markdown
    paragraph/bullet/pipe-table converters are not needed. Raw lines pass
    through untouched; only headings and image markers are transformed.
  - Draft carries two raw <table> blocks (B3 and B5). house-styles them
    (navy #1a1a2e header, alternating #f0f4ff/#ffffff rows, padded cells,
    overflow-x:auto mobile wrapper) since the source HTML is unstyled.
  - Body image placement is taken from the [BODY IMAGE: ...] markers in the
    draft itself rather than a hardcoded body_n index, so placement cannot
    drift if section order changes.
  - Images are PRE-QA'd and pre-approved. QA_DIR must point at the folder
    holding final_featured.jpg / final_body1.jpg / final_body2.jpg. There is
    no auto-sourcing path in this script at all: the three finals were
    verified at 860x452 and visually approved before this script was written.
  - Crash resilience: every irreversible step (each media upload, the post
    POST) is appended to aips_push_state.json the instant it returns. If the
    state file already carries a post_id, the script UPDATEs that post rather
    than creating a duplicate.

Run: set QA_DIR, then `python build_ai_product_search_post.py publish`.
Default is DRY_RUN (parse + checks only, no uploads, no push).
"""
import os, sys, re, io, json, base64, secrets, requests

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
U = os.environ["CHATSKU_WP_USERNAME"]          # NEVER Virtina/ImpelHub creds
A = os.environ["CHATSKU_WP_APP_PASSWORD"]
AUTH = base64.b64encode(f"{U}:{A}".encode()).decode()
H = {"Authorization": f"Basic {AUTH}", "User-Agent": UA, "Content-Type": "application/json"}
HG = {"User-Agent": UA}                        # Cloudflare 403s without the UA

TITLE = "Why traditional B2B product search fails complex catalogs"
SLUG = "traditional-b2b-product-search-fails"
PERMALINK = f"https://chatsku.com/{SLUG}/"
DRAFT = r"C:\content-intel\clients\chatsku\output\drafts\traditional-b2b-product-search-fails-2026-08-31.md"
YOAST_TITLE = "Why Traditional B2B Product Search Fails | ChatSKU"      # 50 chars
YOAST_DESC = ("Keyword site search matches text, not products. Here is why it breaks on "
              "part numbers, specs, and buyer vocabulary, and what the failures cost "
              "your sales team.")                                       # 156 chars
PUBLISH_DATE = "2026-08-31"
CATEGORY_ID = 29                               # Chatbot -- never 25 (DFW Local)

STATE_PATH = r"C:\content-intel\clients\chatsku\output\research\tsf_push_state.json"
SCRATCH = os.environ.get("SCRATCH_DIR", os.path.dirname(STATE_PATH))
QA_DIR = os.environ.get("QA_DIR", "")
NO_IMAGES = os.environ.get("NO_IMAGES") == "1"

# Alt text written against the images as they actually look (80-150 chars each,
# unique, 1-2 article keywords). Do not reuse the draft's placeholder alts.
FEATURED_ALT = ("Man at an office desk leaning over his laptop with a flat, tired expression, "
                "the moment a product search comes back empty")
BODY1_ALT = ("Close-up of a shipping carton stamped with PO number, item number and description, "
             "the catalog fields B2B buyers search on")
BODY2_ALT = ("Open plan office with one employee working alone at a desk, handling the catalog "
             "lookups the website could not answer")


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
    print("  [state] saved:", {k: kw[k] for k in kw})
    return st


STATE = load_state()
if STATE.get("post_id"):
    print(f"!! state file already carries post_id {STATE['post_id']} -- will UPDATE, not create.")


# ---------------------------------------------------------------------------
# 1. Media upload (pre-QA'd files only, no auto-sourcing in this script)
# ---------------------------------------------------------------------------
def read_qa_image(slot):
    if not QA_DIR:
        print("BLOCKING: QA_DIR is not set. This script has no auto-sourcing path; the "
              "three pre-approved finals must be supplied via QA_DIR.")
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
    save_state(**{state_key: mid})            # irreversible step -> persist NOW
    requests.post(f"{WP}/media/{mid}", headers=H,
                  data=json.dumps({"alt_text": alt_text}).encode(), timeout=60)
    print(f"  uploaded media {mid}: {media['source_url']}")
    return {"id": mid, "url": media["source_url"], "alt": alt_text}


# ---------------------------------------------------------------------------
# 2. Load + convert the draft
# ---------------------------------------------------------------------------
raw = open(DRAFT, encoding="utf-8").read()
raw = re.sub(r'^---.*?---\s*', '', raw, count=1, flags=re.S)         # YAML frontmatter
raw = re.split(r'\n---\s*\n+##\s*Publishing notes', raw)[0]          # drop publishing-notes tail
raw = re.sub(r'<!--.*?-->\s*', '', raw, flags=re.S)

# Image + CTA placement markers. FEATURED and CTA are handled structurally
# (featured_media field / button widget) so their placeholders are dropped.
raw = re.sub(r'^\[FEATURED IMAGE:[^\]]*\]\s*$', '', raw, flags=re.M)
raw = re.sub(r'^\[CTA BUTTON:[^\]]*\]\s*$', '', raw, flags=re.M)
raw = re.sub(r'^\[BODY IMAGE:[^\]]*\]\s*$', '@@BODYIMG@@', raw, flags=re.M)

TABLE_WRAP_OPEN = '<div style="overflow-x:auto;margin:16px 0;">'
TH_STYLE = 'style="background:#1a1a2e;color:#ffffff;padding:10px 14px;text-align:left;font-weight:600;"'
TD_STYLE = 'style="padding:10px 14px;border-bottom:1px solid #e0e0e0;vertical-align:top;"'
TABLE_STYLE = 'style="border-collapse:collapse;width:100%;font-size:15px;line-height:1.5;"'


def style_tables(html):
    """The draft ships bare <table> markup. ChatSKU tables render as ugly
    unstyled HTML unless inline CSS is applied (feedback_chatsku_table_styling)."""
    def one(m):
        t = m.group(0)
        t = re.sub(r'<th\b[^>]*>', f'<th {TH_STYLE}>', t)
        t = re.sub(r'<td\b[^>]*>', f'<td {TD_STYLE}>', t)

        # alternating row backgrounds inside <tbody> only
        def tbody(bm):
            inner = bm.group(1)
            n = {"i": 0}

            def tr(trm):
                bg = "#f0f4ff" if n["i"] % 2 == 0 else "#ffffff"
                n["i"] += 1
                return f'<tr style="background:{bg};">'
            return "<tbody>" + re.sub(r'<tr\b[^>]*>', tr, inner) + "</tbody>"
        t = re.sub(r'<tbody>(.*?)</tbody>', tbody, t, flags=re.S)
        t = re.sub(r'^<table\b[^>]*>', f'<table {TABLE_STYLE}>', t)
        return TABLE_WRAP_OPEN + t + "</div>"
    return re.sub(r'<table\b.*?</table>', one, html, flags=re.S)


out = []
for line in raw.split("\n"):
    s = line.strip()
    if not s:
        continue
    m = re.match(r'^###\s*SECTION:\s*(.+)$', s)
    if m:
        out.append(f"<h2>{m.group(1).strip()}</h2>")
        continue
    m = re.match(r'^\*\*H3:\s*(.+?)\*\*$', s)
    if m:
        out.append(f"<h3>{m.group(1).strip()}</h3>")
        continue
    out.append(line.rstrip())
content_html = style_tables("\n".join(out))

if "@@BODYIMG@@" not in content_html:
    print("BLOCKING: body-image markers were lost during conversion.")
    raise SystemExit(1)
if content_html.count("@@BODYIMG@@") != 2:
    print(f"BLOCKING: expected 2 body-image markers, found {content_html.count('@@BODYIMG@@')}.")
    raise SystemExit(1)


def slugify(text):
    t = re.sub(r'<[^>]+>', '', text).lower().strip()
    t = re.sub(r"[^a-z0-9\s-]", "", t)
    t = re.sub(r"\s+", "-", t).strip("-")
    return t[:60].strip("-")


# ---------------------------------------------------------------------------
# 3. Blocking pre-push checks
# ---------------------------------------------------------------------------
print("\n=== BLOCKING CHECKS ===")

# 3a. em dashes
_em = content_html.count("\u2014") + content_html.count("&mdash;")
if _em:
    print(f"BLOCKING: {_em} em dash(es) present.")
    raise SystemExit(1)
print("  em dashes: 0 OK")

# 3b. banned vocabulary
BANNED = ["just a chatbot", "AI-powered", "revolutionary", "game-changing",
          "cutting-edge", "transform your", "delve"]
BANNED_WORD = [r"\bsolutions\b", r"\bleverage\b", r"\bnavigat(?:e|es|ed|ing)\b"]
hits = []
for b in BANNED:
    if re.search(re.escape(b), content_html, re.I):
        hits.append(b)
for b in BANNED_WORD:
    if re.search(b, content_html, re.I):
        hits.append(b)
if hits:
    print("BLOCKING: banned words present:", hits)
    raise SystemExit(1)
print("  banned words: 0 OK")

# 3c. internal links -- BOTH absolute chatsku.com and relative "/path/" hrefs.
# An absolute-only regex passes vacuously on a relative-link draft.
_abs = re.findall(r'href="(https://chatsku\.com/[^"#]+)"', content_html)
_rel_paths = re.findall(r'href="(/[^"#]*)"', content_html)
_rel = ["https://chatsku.com" + p for p in _rel_paths]
hrefs = sorted(set(_abs + _rel))
if len(hrefs) < 3:
    print(f"BLOCKING: only {len(hrefs)} internal links found ({hrefs}). Regex broken or draft under-linked.")
    raise SystemExit(1)
print(f"  found {len(_rel_paths)} relative + {len(_abs)} absolute internal hrefs -> {len(hrefs)} unique")
print("  live-checking internal links with browser UA...")
bad = []
for u in hrefs:
    try:
        r = requests.get(u, headers=HG, timeout=30, allow_redirects=False)
        print(f"    {r.status_code}  {u}")
        if r.status_code != 200:
            bad.append((u, r.status_code, r.headers.get("location", "")))
    except Exception as e:
        print(f"    ERR  {u}  {e}")
        bad.append((u, "ERR", str(e)))
# CTA destination is a button widget, not an href in content -- check it too
for u in ["https://chatsku.com/ai-product-search-for-b2b/"]:
    r = requests.get(u, headers=HG, timeout=30, allow_redirects=False)
    print(f"    {r.status_code}  {u}  (CTA button target)")
    if r.status_code != 200:
        bad.append((u, r.status_code, "CTA button"))
if bad:
    print("BLOCKING: bad internal links (non-200 or redirect):")
    [print("   ", *b) for b in bad]
    raise SystemExit(1)
print("  all internal links 200 OK")

# 3d. external links -- max 2, both 200, both target=_blank rel=noopener noreferrer
_ext = sorted(set(re.findall(r'href="(https?://(?!chatsku\.com)[^"#]+)"', content_html)))
if len(_ext) > 2:
    print("BLOCKING: more than 2 external links:", _ext)
    raise SystemExit(1)
COMPETITORS = ["drift.com", "intercom", "tidio", "bigcommerce", "shopify", "zendesk", "hubspot"]
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
        if r.status_code != 200:
            print("BLOCKING: external link non-200.")
            raise SystemExit(1)
    except SystemExit:
        raise
    except Exception as e:
        print(f"    ERR  {u}  {e} (non-blocking for external, review manually)")

# 3e. slug free / existing post
sr = requests.get(f"{WP}/posts", params={"slug": SLUG, "status": "any", "context": "edit"},
                  headers=H, timeout=30)
existing = sr.json() if sr.status_code == 200 else []
if existing and not STATE.get("post_id"):
    print("BLOCKING: a post with this slug already exists but state file has no post_id:",
          [(p["id"], p["status"]) for p in existing])
    raise SystemExit(1)
print("  slug check OK" + (f" (existing post {existing[0]['id']} will be updated)" if existing else " (free)"))


# ---------------------------------------------------------------------------
# 4. Elementor helpers (post 96 structure)
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
                      r'<p style="color:#aaaacc;text-align:center;font-size:18px;max-width:720px;margin:0 auto 14px auto;"\1',
                      html)
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
    tabs = [{"_id": gid(), "tab_title": q, "tab_content": a} for q, a in qa_pairs]
    return {"id": gid(), "elType": "widget", "widgetType": "accordion", "elements": [],
            "settings": {"tabs": tabs}}


def w_html(html):
    return {"id": gid(), "elType": "widget", "widgetType": "html", "elements": [],
            "settings": {"html": html}}


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
# 5. Parse into sections
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
            if "@@BODYIMG@@" in body:                 # placement comes from the draft
                img_seen += 1
                m = BODY1 if img_seen == 1 else BODY2
                if m:
                    widgets.append(w_image(m))        # image ALWAYS last
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
                       w_button("See AI product search for B2B", "https://chatsku.com/ai-product-search-for-b2b/")]
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
                     "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', a).strip()}}
                    for q, a in faq_pairs]},
                {"@type": "BreadcrumbList", "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://chatsku.com/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://chatsku.com/blog/"},
                    {"@type": "ListItem", "position": 3, "name": TITLE, "item": PERMALINK}]}]}
            widgets.append(w_html('<script type="application/ld+json">' + json.dumps(schema) + '</script>'))
            out.append(section(widgets, "#f9f9fb"))
    return out


sections = build_sections()
kinds = [k for k, _, _ in parsed]
print(f"\nParsed {len(parsed)} H2 sections {kinds} -> {len(sections)} Elementor sections | FAQ tabs {len(faq_pairs)}")
_wc = len(re.sub(r'<[^>]+>', ' ', content_html).split())
print(f"Word count (tags stripped): {_wc}")

DRY_RUN = "publish" not in sys.argv

# ---------------------------------------------------------------------------
# 6. Upload images, rebuild with image widgets
# ---------------------------------------------------------------------------
if NO_IMAGES:
    print("  MEDIA UPLOAD SKIPPED (NO_IMAGES=1)")
    print("  Text-first push. Images attach in a follow-up run against the same post id.")
elif not DRY_RUN:
    print("\n=== MEDIA UPLOAD ===")
    st = load_state()
    if st.get("featured_media"):
        print("  featured already uploaded per state file:", st["featured_media"])
        r = requests.get(f"{WP}/media/{st['featured_media']}", headers=H, timeout=30).json()
        FEATURED = {"id": r["id"], "url": r["source_url"], "alt": FEATURED_ALT}
    else:
        FEATURED = upload_media(read_qa_image("featured"),
                                "chatsku-traditional-b2b-product-search-fails-featured.jpg",
                                FEATURED_ALT, "featured_media")
    if st.get("body1_media"):
        r = requests.get(f"{WP}/media/{st['body1_media']}", headers=H, timeout=30).json()
        BODY1 = {"id": r["id"], "url": r["source_url"], "alt": BODY1_ALT}
    else:
        BODY1 = upload_media(read_qa_image("body1"),
                             "chatsku-traditional-b2b-product-search-fails-body1.jpg",
                             BODY1_ALT, "body1_media")
    if st.get("body2_media"):
        r = requests.get(f"{WP}/media/{st['body2_media']}", headers=H, timeout=30).json()
        BODY2 = {"id": r["id"], "url": r["source_url"], "alt": BODY2_ALT}
    else:
        BODY2 = upload_media(read_qa_image("body2"),
                             "chatsku-traditional-b2b-product-search-fails-body2.jpg",
                             BODY2_ALT, "body2_media")
    for m in (FEATURED, BODY1, BODY2):
        if not m["url"].startswith("https://chatsku.com/wp-content/uploads/"):
            print("BLOCKING: media src not on chatsku uploads:", m["url"])
            raise SystemExit(1)
    for m, alt in ((FEATURED, FEATURED_ALT), (BODY1, BODY1_ALT), (BODY2, BODY2_ALT)):
        if not (80 <= len(alt) <= 150):
            print(f"BLOCKING: alt text length {len(alt)} outside 80-150: {alt}")
            raise SystemExit(1)
    if len({FEATURED_ALT, BODY1_ALT, BODY2_ALT}) != 3:
        print("BLOCKING: alt texts not unique.")
        raise SystemExit(1)
    print("  alt text lengths OK and unique")
    sections = build_sections()

elementor_json = json.dumps(sections)
content_fallback = re.sub(r'<img[^>]*?>', '', content_html).replace("@@BODYIMG@@", "")

open(os.path.join(SCRATCH, "tsf_elementor.json"), "w", encoding="utf-8").write(elementor_json)
print(f"Built {len(sections)} sections | elementor {len(elementor_json):,} chars")

# 6b. structural assertions
if re.search(r'<img\b', content_fallback):
    print("BLOCKING: bare <img> remains in the WP content field.")
    raise SystemExit(1)
print("  content field: 0 bare <img> OK")

order_violations = []
img_widget_count = 0
for sec in sections:
    for col in sec.get("elements", []):
        types = [w["widgetType"] for w in col.get("elements", []) if w["elType"] == "widget"]
        img_widget_count += types.count("image")
        if "image" in types:
            img_idx = types.index("image")
            if img_idx != len(types) - 1:
                order_violations.append(types)
            if "text-editor" in types and types.index("text-editor") > img_idx:
                order_violations.append(types)
if order_violations:
    print("BLOCKING: image widget not last / before text-editor:", order_violations)
    raise SystemExit(1)
print(f"  widget order: {img_widget_count} image widget(s), 0 violations (image always last)")

if not DRY_RUN and not NO_IMAGES and img_widget_count != 2:
    print(f"BLOCKING: expected 2 body image widgets, built {img_widget_count}.")
    raise SystemExit(1)

if DRY_RUN:
    print("\nDRY RUN complete. Pass 'publish' as argv to upload and push.")
    raise SystemExit(0)

if not NO_IMAGES and (not FEATURED or not FEATURED.get("id")):
    print("BLOCKING: refusing to push with featured_media=0.")
    raise SystemExit(1)
if len(YOAST_TITLE) > 60 or not YOAST_TITLE.endswith("| ChatSKU"):
    print("BLOCKING: Yoast title invalid:", len(YOAST_TITLE), YOAST_TITLE)
    raise SystemExit(1)
if not (150 <= len(YOAST_DESC) <= 160):
    print("BLOCKING: Yoast desc length", len(YOAST_DESC))
    raise SystemExit(1)
print(f"  Yoast title {len(YOAST_TITLE)} chars, desc {len(YOAST_DESC)} chars OK")

# ---------------------------------------------------------------------------
# 7. Push
# ---------------------------------------------------------------------------
payload = {
    "title": TITLE, "slug": SLUG, "status": "draft", "content": content_fallback,
    "excerpt": YOAST_DESC, "categories": [CATEGORY_ID],
    "meta": {"_elementor_edit_mode": "builder", "_elementor_template_type": "wp-post",
             "_elementor_data": elementor_json,
             "_yoast_wpseo_title": YOAST_TITLE, "_yoast_wpseo_metadesc": YOAST_DESC},
}

if FEATURED and FEATURED.get("id"):
    payload["featured_media"] = FEATURED["id"]

st = load_state()
pid = st.get("post_id")
print("\n=== PUSH ===")
if pid:
    r = requests.post(f"{WP}/posts/{pid}", headers=H, data=json.dumps(payload).encode(), timeout=180)
    print("UPDATE status:", r.status_code)
else:
    r = requests.post(f"{WP}/posts", headers=H, data=json.dumps(payload).encode(), timeout=180)
    print("CREATE status:", r.status_code)
if r.status_code not in (200, 201):
    print(r.text[:2000])
    raise SystemExit(1)
j = r.json()
pid = j["id"]
save_state(post_id=pid, link=j.get("link"), status=j.get("status"))   # persist IMMEDIATELY
print("POST_ID:", pid, "| status:", j["status"], "| link:", j.get("link"))
print("PREVIEW:", f"https://chatsku.com/?p={pid}")

cc = requests.delete("https://chatsku.com/wp-json/elementor/v1/cache", headers=H, timeout=90)
print("Elementor cache clear:", cc.status_code)
save_state(cache_cleared=cc.status_code)

# ---------------------------------------------------------------------------
# 8. Verify with context=edit
# ---------------------------------------------------------------------------
print("\n=== VERIFY (context=edit) ===")
vr = requests.get(f"{WP}/posts/{pid}", params={"context": "edit"}, headers=H, timeout=60).json()
vmeta = vr.get("meta", {})
yt_ok = vmeta.get("_yoast_wpseo_title") == YOAST_TITLE
yd_ok = vmeta.get("_yoast_wpseo_metadesc") == YOAST_DESC
print("  Yoast title persisted:", yt_ok)
print("  Yoast desc  persisted:", yd_ok)
try:
    ed = json.loads(vmeta.get("_elementor_data") or "[]")
except Exception as e:
    ed = []
    print("  _elementor_data JSON parse ERROR:", e)
print("  _elementor_data parses as list:", isinstance(ed, list), "| sections:", len(ed))
print("  _elementor_edit_mode:", vmeta.get("_elementor_edit_mode"),
      "| template_type:", vmeta.get("_elementor_template_type"))
v_viol = 0
v_img = 0
for sec in ed:
    for col in sec.get("elements", []):
        types = [w["widgetType"] for w in col.get("elements", []) if w.get("elType") == "widget"]
        v_img += types.count("image")
        if "image" in types and types.index("image") != len(types) - 1:
            v_viol += 1
print(f"  live image widgets: {v_img} | order violations: {v_viol}")
raw_content = vr.get("content", {}).get("raw", "")
print("  bare <img> in live content:", len(re.findall(r'<img\b', raw_content)))
print("  featured_media:", vr.get("featured_media"))
print("  status:", vr.get("status"), "| categories:", vr.get("categories"))

save_state(yoast_title_persisted=yt_ok, yoast_desc_persisted=yd_ok,
           elementor_sections=len(ed), image_widgets=v_img,
           order_violations=v_viol, featured_media_live=vr.get("featured_media"),
           categories=vr.get("categories"), verified=True)
print("\nDone.")
