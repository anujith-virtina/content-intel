"""
Build + publish: b2b-conversational-commerce
"B2B conversational commerce: definition, use cases, and ROI"
Format B (Conversational Q&A)   Date: 2026-06-25

Parses the approved draft (clients/chatsku/output/drafts/b2b-conversational-commerce-2026-06-25.md)
into Elementor sections. Splits embedded <h3> into separate heading widgets (gold-standard post 96/353).
Adds Article + FAQPage + BreadcrumbList + HowTo JSON-LD.
Images: featured + 1 body photo + 1 ROI infographic (all 860x452).

Template: build_what_is_b2b_catalog_chatbot_post.py
Env knobs: DRY_RUN=1 (no network), REUSE_MEDIA="feat,body,info", UPDATE_POST_ID, FORCE_STATUS
"""
import json, secrets, re, urllib.request, urllib.error
import base64, os, io, sys, ssl
from pathlib import Path
from collections import OrderedDict

_ssl_ctx = ssl._create_unverified_context()

# -- .env ----------------------------------------------------------------------
_env_path = r"C:\content-intel\.env"
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

WP_BASE = "https://chatsku.com/wp-json/wp/v2"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
USERNAME = os.environ.get("CHATSKU_WP_USERNAME", "")
PASSWORD = os.environ.get("CHATSKU_WP_APP_PASSWORD", "")
if not USERNAME or not PASSWORD:
    print("ERROR: CHATSKU_WP creds not set"); sys.exit(1)
AUTH = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
HEADERS = {"Authorization": f"Basic {AUTH}", "User-Agent": UA, "Content-Type": "application/json"}

DRAFT = r"C:\content-intel\clients\chatsku\output\drafts\b2b-conversational-commerce-2026-06-25.md"
SCRATCH = os.environ.get("OUT_DIR",
    r"C:\Users\ASUS\AppData\Local\Temp\claude\C--content-intel\20ac4360-d65c-4c3a-b26e-9e06509d2276\scratchpad")

TITLE = "B2B conversational commerce: definition, use cases, and ROI"
H1_ONPAGE = TITLE
SLUG = "b2b-conversational-commerce"
DATE = "2026-06-25"
META_TITLE = "B2B Conversational Commerce: Uses & ROI | ChatSKU"
META_DESC = ("B2B conversational commerce lets buyers price, quote, and order through chat tied to "
             "your catalog. See the definition, 7 use cases, and ROI for distributors.")

# ===========================================================================
# PARSE DRAFT
# ===========================================================================
raw = Path(DRAFT).read_text(encoding="utf-8")
# drop frontmatter
raw = re.sub(r'^---\n.*?\n---\n', '', raw, count=1, flags=re.S)
chunks = re.split(r'^### SECTION: (.+)$', raw, flags=re.M)
sections = OrderedDict()
for i in range(1, len(chunks), 2):
    head = chunks[i].strip()
    body = chunks[i + 1]
    body = re.sub(r'<!--.*?-->', '', body, flags=re.S)          # strip comments
    body = re.sub(r'^\s*-{3,}\s*$', '', body, flags=re.M)        # strip --- separators
    body = body.strip()
    # convert relative internal links to absolute chatsku.com
    body = body.replace('href="/', 'href="https://chatsku.com/')
    sections[head] = body

EXPECTED = [
    "Executive summary", "Introduction", "What is B2B conversational commerce?",
    "How is B2B conversational commerce different from B2C conversational commerce?",
    "How is conversational commerce different from chatbots and AI search?",
    "What does a B2B conversational commerce conversation actually look like?",
    "What are the main use cases for B2B conversational commerce?",
    "What ROI can B2B distributors expect from conversational commerce?",
    "How fast can a B2B distributor deploy conversational commerce?",
    "Who should and should not use B2B conversational commerce?",
    "People also ask", "Conclusion", "Frequently asked questions",
]
missing = [h for h in EXPECTED if h not in sections]
if missing:
    print("FATAL missing sections:", missing); sys.exit(1)
print(f"Parsed {len(sections)} sections.")

# minor uniqueness safety: vary the example SKU token
sections["What is B2B conversational commerce?"] = \
    sections["What is B2B conversational commerce?"].replace("SKU 4471-B", "SKU 7730-S")

# style the comparison table to match the gold-standard post 299 (navy header band,
# alternating row backgrounds, padded cells, bottom borders) + mobile scroll wrapper.
def style_table(html):
    html = html.replace(
        '<table>',
        '<div style="overflow-x:auto;margin:8px 0;"><table style="border-collapse:collapse;width:100%;font-size:15px;">')
    html = html.replace('</table>', '</table></div>')
    html = html.replace(
        '<th>',
        '<th style="background:#1a1a2e;color:#ffffff;padding:11px 14px;text-align:left;font-weight:600;border:1px solid #1a1a2e;">')
    html = html.replace(
        '<td>',
        '<td style="padding:11px 14px;border-bottom:1px solid #e6e8ef;vertical-align:top;">')
    def alt(m):
        rows = m.group(1).split('<tr>')
        out = rows[0]
        for i, r in enumerate(rows[1:]):
            bg = '#f0f4ff' if i % 2 == 0 else '#ffffff'
            out += f'<tr style="background:{bg};">' + r
        return '<tbody>' + out + '</tbody>'
    return re.sub(r'<tbody>(.*?)</tbody>', alt, html, flags=re.S)

_TBL_SEC = "How is conversational commerce different from chatbots and AI search?"
if "<table>" in sections[_TBL_SEC]:
    sections[_TBL_SEC] = style_table(sections[_TBL_SEC])
    print("Comparison table: styled (navy header, alt rows, scroll wrapper)")

ALL_TEXT = "\n".join(sections.values())

# -- em dash + banned scan -----------------------------------------------------
em_count = ALL_TEXT.count("—") + ALL_TEXT.count("&mdash;")
print(f"Em dash scan: {'PASS' if em_count == 0 else 'FAIL'} ({em_count})")
if em_count: sys.exit(1)
BANNED = ["just a chatbot", "ai-powered", "revolutionary", "game-changing", "cutting-edge",
          "in today's fast-paced world", "in conclusion", "delve", "leverage", "seamless",
          "robust", "supercharge", "unlock", "transform your", "moreover", "furthermore"]
banned_hits = [b for b in BANNED if b in ALL_TEXT.lower()]
print(f"Banned scan: {'PASS' if not banned_hits else 'FAIL ' + str(banned_hits)}")
if banned_hits: sys.exit(1)

# ===========================================================================
# ELEMENTOR BUILDERS
# ===========================================================================
def gid(): return secrets.token_hex(4)

def make_heading(title, level="h2", color="#1a1a2e", align="left"):
    size = 28 if level == "h2" else 22
    s = {"title": title, "align": align, "title_color": color,
         "typography_typography": "custom", "typography_font_size": {"size": size, "unit": "px"}}
    if level != "h2": s["header_size"] = level
    return {"id": gid(), "elType": "widget", "widgetType": "heading", "elements": [], "settings": s}

def make_text(html, dark_section=False):
    if dark_section:
        html = re.sub(r'<p([ >])',
                      r'<p style="color:#aaaacc;text-align:center;font-size:18px;max-width:720px;margin:0 auto;"\1',
                      html)
    return {"id": gid(), "elType": "widget", "widgetType": "text-editor", "elements": [], "settings": {"editor": html}}

def make_image_widget(img):
    return {"id": gid(), "elType": "widget", "widgetType": "image", "elements": [],
            "settings": {"image": {"id": img["id"], "url": img["url"], "alt": img["alt"], "source": "library", "size": ""},
                         "align": "center", "width": {"size": 100, "unit": "%"},
                         "border_radius": {"top": "10", "right": "10", "bottom": "10", "left": "10", "unit": "px"}}}

def make_button(text, url):
    return {"id": gid(), "elType": "widget", "widgetType": "button", "elements": [],
            "settings": {"text": text, "link": {"url": url, "is_external": "", "nofollow": ""}, "align": "center",
                         "background_color": "#e94560", "button_text_color": "#ffffff",
                         "border_radius": {"size": 6, "unit": "px"},
                         "_margin": {"unit": "px", "top": "20", "right": "0", "bottom": "0", "left": "0", "isLinked": False}}}

def make_html_widget(html):
    return {"id": gid(), "elType": "widget", "widgetType": "html", "elements": [], "settings": {"html": html}}

def make_section(widgets, bg, is_conclusion=False):
    sec_pad = {"top": "20", "bottom": "30", "unit": "px", "right": "0", "left": "0"} if is_conclusion \
        else {"top": "60", "bottom": "60", "unit": "px"}
    col_pad = {"unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20", "isLinked": True}
    return {"id": gid(), "elType": "section", "isInner": False,
            "settings": {"background_background": "classic", "background_color": bg, "padding": sec_pad},
            "elements": [{"id": gid(), "elType": "column", "isInner": False,
                          "settings": {"_column_size": 100, "width": "100", "padding": col_pad}, "elements": widgets}]}

FAQ_CSS = (
    "<style>\n"
    ".csku-faq details{border:1px solid #e6e8ef;border-radius:8px;margin:0 0 12px;background:#fff;overflow:hidden;}\n"
    ".csku-faq summary{cursor:pointer;list-style:none;padding:16px 20px;font-weight:600;font-size:17px;"
    "color:#1a1a2e;display:flex;justify-content:space-between;align-items:center;gap:16px;}\n"
    ".csku-faq summary::-webkit-details-marker{display:none;}\n"
    ".csku-faq .csku-ic{color:#00C9B1;font-size:24px;line-height:1;flex-shrink:0;transition:transform .15s ease;}\n"
    ".csku-faq details[open] summary .csku-ic{transform:rotate(45deg);}\n"
    ".csku-faq details[open] summary{border-bottom:1px solid #eef0f5;}\n"
    ".csku-faq .csku-a{padding:14px 20px 18px;color:#444;font-size:16px;line-height:1.6;}\n"
    ".csku-faq .csku-a p{margin:0;}\n"
    "</style>"
)

def build_faq_accordion(faq_html):
    """Render FAQ Q&As as collapsible native <details> toggles (user-requested accordion)."""
    pairs = re.findall(r'<h3>(.*?)</h3>\s*(<p>.*?</p>)', faq_html, flags=re.S)
    items = []
    for q, a in pairs:
        items.append(
            f'<details><summary><span>{q.strip()}</span><span class="csku-ic">+</span></summary>'
            f'<div class="csku-a">{a.strip()}</div></details>')
    return FAQ_CSS + '\n<div class="csku-faq">\n' + "\n".join(items) + '\n</div>', len(pairs)

def split_widgets(html):
    """Split section HTML into ordered widgets: <h3> -> heading widget, other HTML -> text-editor."""
    parts = re.split(r'(<h3>.*?</h3>)', html, flags=re.S)
    out = []
    for part in parts:
        p = part.strip()
        if not p: continue
        m = re.match(r'<h3>(.*?)</h3>$', p, flags=re.S)
        if m:
            out.append(make_heading(m.group(1).strip(), "h3"))
        else:
            out.append(make_text(p))
    return out

# ===========================================================================
# SCHEMA
# ===========================================================================
def strip_tags(s): return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()

def faq_pairs(html):
    return [(strip_tags(q), strip_tags(a)) for q, a in
            re.findall(r'<h3>(.*?)</h3>\s*<p>(.*?)</p>', html, flags=re.S)]

def build_schema(feat_url):
    article = {"@context": "https://schema.org", "@type": "Article", "headline": TITLE,
               "description": META_DESC, "image": feat_url, "datePublished": DATE, "dateModified": DATE,
               "author": {"@type": "Organization", "name": "ChatSKU", "url": "https://chatsku.com"},
               "publisher": {"@type": "Organization", "name": "ChatSKU",
                             "logo": {"@type": "ImageObject", "url": "https://chatsku.com/wp-content/uploads/2024/logo.png"}},
               "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://chatsku.com/{SLUG}/"}}
    faqs = faq_pairs(sections["Frequently asked questions"])
    faqpage = {"@context": "https://schema.org", "@type": "FAQPage",
               "mainEntity": [{"@type": "Question", "name": q,
                               "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    breadcrumb = {"@context": "https://schema.org", "@type": "BreadcrumbList",
                  "itemListElement": [
                      {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://chatsku.com/"},
                      {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://chatsku.com/blog/"},
                      {"@type": "ListItem", "position": 3, "name": TITLE, "item": f"https://chatsku.com/{SLUG}/"}]}
    deploy = sections["How fast can a B2B distributor deploy conversational commerce?"]
    lis = re.findall(r'<li>(.*?)</li>', deploy, flags=re.S)
    steps = []
    for li in lis:
        b = re.search(r'<strong>(.*?)</strong>', li, flags=re.S)
        name = strip_tags(b.group(1)).rstrip('.') if b else strip_tags(li)[:60]
        steps.append({"@type": "HowToStep", "name": name, "text": strip_tags(li)})
    howto = {"@context": "https://schema.org", "@type": "HowTo",
             "name": "How to deploy B2B conversational commerce", "step": steps}
    blocks, types = [], []
    for nm, obj in [("Article", article), ("FAQPage", faqpage), ("BreadcrumbList", breadcrumb), ("HowTo", howto)]:
        s = json.dumps(obj, ensure_ascii=False); json.loads(s)
        blocks.append(f'<script type="application/ld+json">\n{s}\n</script>'); types.append(obj["@type"])
        print(f"  JSON-LD {nm}: valid ({len(s)} chars)")
    return "\n".join(blocks), types, len(steps)

# ===========================================================================
# IMAGES
# ===========================================================================
def resize_file(path, w=860, h=452, q=88):
    from PIL import Image
    img = Image.open(path).convert("RGB")
    sw, sh = img.size
    sc = max(w / sw, h / sh)
    img = img.resize((int(sw * sc), int(sh * sc)), Image.LANCZOS)
    nw, nh = img.size
    left, top = (nw - w) // 2, (nh - h) // 2
    img = img.crop((left, top, left + w, top + h))
    buf = io.BytesIO(); img.save(buf, "JPEG", quality=q, optimize=True)
    data = buf.getvalue()
    if len(data) > 200 * 1024:
        buf = io.BytesIO(); img.save(buf, "JPEG", quality=72, optimize=True); data = buf.getvalue()
    from PIL import Image as _I
    assert _I.open(io.BytesIO(data)).size == (w, h)
    print(f"  Resized {os.path.basename(path)} -> {w}x{h} ({len(data)//1024}KB)")
    return data

def upload(jpeg, filename, alt):
    uh = {"Authorization": f"Basic {AUTH}", "User-Agent": UA, "Content-Type": "image/jpeg",
          "Content-Disposition": f'attachment; filename="{filename}"'}
    req = urllib.request.Request(f"{WP_BASE}/media", data=jpeg, headers=uh, method="POST")
    with urllib.request.urlopen(req, timeout=60, context=_ssl_ctx) as r:
        m = json.loads(r.read())
    mid, murl = m["id"], m["source_url"]
    req2 = urllib.request.Request(f"{WP_BASE}/media/{mid}", data=json.dumps({"alt_text": alt}).encode(),
                                  headers=HEADERS, method="POST")
    with urllib.request.urlopen(req2, timeout=20, context=_ssl_ctx) as r:
        r.read()
    print(f"  Uploaded {filename}: ID={mid}")
    return {"id": mid, "url": murl, "alt": alt}

def fetch_media(mid, alt):
    req = urllib.request.Request(f"{WP_BASE}/media/{mid}", headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20, context=_ssl_ctx) as r:
        m = json.loads(r.read())
    return {"id": int(mid), "url": m["source_url"], "alt": alt}

FEAT_SRC = os.path.join(SCRATCH, "cand_featured_0.jpg")
BODY_SRC = os.path.join(SCRATCH, "cand_featured_1.jpg")
INFO_SRC = os.path.join(SCRATCH, "conv_commerce_infographic_860x452.jpg")

FEAT_ALT = ("Two B2B buyers reviewing a product catalog and quote on laptops at an office desk, "
            "the moment B2B conversational commerce answers and prices instantly")
BODY_ALT = ("B2B distributor sales team reviewing catalog inquiries and customer quotes on laptops, "
            "a core conversational commerce use case for distributors")
INFO_ALT = ("B2B conversational commerce ROI infographic: lead response from 42 hours to under 2 minutes "
            "and chat conversion from 3.1 to 12.3 percent")

REUSE = os.environ.get("REUSE_MEDIA", "")
if os.environ.get("DRY_RUN") and not REUSE:
    feat = {"id": 9001, "url": "https://chatsku.com/wp-content/uploads/2026/06/f.jpg", "alt": FEAT_ALT}
    body = {"id": 9002, "url": "https://chatsku.com/wp-content/uploads/2026/06/b.jpg", "alt": BODY_ALT}
    info = {"id": 9003, "url": "https://chatsku.com/wp-content/uploads/2026/06/i.jpg", "alt": INFO_ALT}
    print("DRY_RUN images")
elif REUSE:
    fid, bid, iid = REUSE.split(",")
    feat, body, info = fetch_media(fid, FEAT_ALT), fetch_media(bid, BODY_ALT), fetch_media(iid, INFO_ALT)
    print(f"Reusing media: {fid},{bid},{iid}")
else:
    print("\nUploading images...")
    feat = upload(resize_file(FEAT_SRC), "chatsku-b2b-conversational-commerce-featured.jpg", FEAT_ALT)
    body = upload(resize_file(BODY_SRC), "chatsku-b2b-conversational-commerce-use-cases.jpg", BODY_ALT)
    info = upload(resize_file(INFO_SRC), "chatsku-b2b-conversational-commerce-roi-infographic.jpg", INFO_ALT)

for lbl, m in [("feat", feat), ("body", body), ("info", info)]:
    if not m["url"].startswith("https://chatsku.com/wp-content/uploads/"):
        print(f"FATAL {lbl} url: {m['url']}"); sys.exit(1)
print(f"Images: feat={feat['id']} body={body['id']} info={info['id']}")

# ===========================================================================
# BUILD SECTIONS
# ===========================================================================
BG = {
    "Executive summary": "#f9f9fb", "Introduction": "#ffffff",
    "What is B2B conversational commerce?": "#f0f4ff",
    "How is B2B conversational commerce different from B2C conversational commerce?": "#ffffff",
    "How is conversational commerce different from chatbots and AI search?": "#f9f9fb",
    "What does a B2B conversational commerce conversation actually look like?": "#ffffff",
    "What are the main use cases for B2B conversational commerce?": "#f0f4ff",
    "What ROI can B2B distributors expect from conversational commerce?": "#ffffff",
    "How fast can a B2B distributor deploy conversational commerce?": "#f9f9fb",
    "Who should and should not use B2B conversational commerce?": "#ffffff",
    "People also ask": "#f0f4ff", "Conclusion": "#1a1a2e", "Frequently asked questions": "#f9f9fb",
}
IMG_AFTER = {
    "What are the main use cases for B2B conversational commerce?": body,
    "What ROI can B2B distributors expect from conversational commerce?": info,
}

elementor = []
for head, html in sections.items():
    if head == "Conclusion":
        elementor.append(make_section([
            make_heading("Conclusion", color="#ffffff", align="center"),
            make_text(html, dark_section=True),
            make_button("Book a demo", "https://chatsku.com/demo/"),
        ], bg="#1a1a2e", is_conclusion=True))
        continue
    if head == "Frequently asked questions":
        faq_acc_html, n_faq = build_faq_accordion(html)
        elementor.append(make_section([make_heading(head, "h2"), make_html_widget(faq_acc_html)], bg=BG[head]))
        print(f"FAQ: rendered {n_faq} collapsible <details> toggles")
        continue
    widgets = [make_heading(head, "h2")] + split_widgets(html)
    if head in IMG_AFTER:
        widgets.append(make_image_widget(IMG_AFTER[head]))
    elementor.append(make_section(widgets, bg=BG[head]))

schema_html, schema_types, n_steps = build_schema(feat["url"])
schema_sec = make_section([make_html_widget(schema_html)], bg="#ffffff")
schema_sec["settings"]["padding"] = {"top": "0", "bottom": "0", "unit": "px"}
elementor.append(schema_sec)

elementor_json = json.dumps(elementor)
print(f"\nBuilt {len(elementor)} sections; verifying image order...")
for i, s in enumerate(elementor):
    types = [w.get("widgetType") for w in s["elements"][0]["elements"]]
    if "image" in types and "text-editor" in types and types.index("image") < types.index("text-editor"):
        print(f"  FATAL image before text in section {i}"); sys.exit(1)
print("  image-order OK")

# ===========================================================================
# WP CONTENT FALLBACK
# ===========================================================================
def sec_to_content(s):
    out = []
    for w in s["elements"][0]["elements"]:
        wt = w.get("widgetType")
        if wt == "heading":
            lv = w["settings"].get("header_size", "h2"); out.append(f"<{lv}>{w['settings']['title']}</{lv}>")
        elif wt == "text-editor": out.append(w["settings"]["editor"])
        elif wt == "button": out.append(f'<p><a href="{w["settings"]["link"]["url"]}">{w["settings"]["text"]}</a></p>')
        elif wt == "html": out.append(w["settings"]["html"])
    return "\n".join(out)
wp_content = re.sub(r'<img[^>]*>', '', "\n\n".join(sec_to_content(s) for s in elementor))

# ===========================================================================
# PRE-PUBLISH CHECKLIST
# ===========================================================================
print("\n" + "=" * 60 + "\nPRE-PUBLISH CHECKLIST\n" + "=" * 60)
checks = {}
checks["Em dashes 0"] = em_count == 0
checks["No banned"] = not banned_hits
EXISTING_SLUGS = ["rfq-automation-manufacturers", "rfq-automation-for-product-catalogs",
    "ai-chatbot-for-manufacturers-dallas", "b2b-ecommerce-chatbot-dallas", "pdf-catalog-sales-liability",
    "rfq-form-conversion-rate", "b2b-catalog-conversion-rate", "convert-pdf-catalog-to-website",
    "b2b-catalog-issues-costing-sales", "b2b-after-hours-buyer-problem", "b2b-catalog-revenue-leakage",
    "lost-b2b-revenue-calculator", "best-b2b-catalog-chatbots-2026", "b2b-quote-to-order-automation",
    "what-is-a-b2b-catalog-chatbot"]
checks["Slug unique"] = SLUG not in EXISTING_SLUGS
checks["Featured media"] = bool(feat["id"])
checks["Img URLs"] = all(m["url"].startswith("https://chatsku.com/wp-content/uploads/") for m in [feat, body, info])
alts = [feat["alt"], body["alt"], info["alt"]]
checks["Alt 80-150 + unique"] = all(80 <= len(a) <= 150 for a in alts) and len(set(alts)) == 3
for l, a in zip(["feat", "body", "info"], alts): print(f"      alt[{l}] {len(a)}: {a}")

ext_links = re.findall(r'href="https?://(?!chatsku\.com)[^"]+', ALL_TEXT)
checks["External <=2"] = len(ext_links) <= 2
int_links = re.findall(r'href="https://chatsku\.com/[^"]+', ALL_TEXT)
checks["Internal >=5"] = len(int_links) >= 5
ext_anchors = re.findall(r'<a [^>]*href="https?://(?!chatsku\.com)[^"]+"[^>]*>', ALL_TEXT)
checks["Ext target/rel"] = all('target="_blank"' in a and 'rel="noopener noreferrer"' in a for a in ext_anchors)
int_anchors = re.findall(r'<a [^>]*href="https://chatsku\.com/[^"]+"[^>]*>', ALL_TEXT)
checks["Int no target"] = all('target=' not in a for a in int_anchors)
COMP = ["drift.com", "intercom.com", "tidio.com", "zendesk.com", "bigcommerce.com",
        "algolia.com", "zoovu.com", "coveo.com", "bloomreach.com", "humcommerce.com"]
checks["No competitor links"] = not any(c in ALL_TEXT.lower() for c in COMP)

conc = next(s for s in elementor if s["settings"]["background_color"] == "#1a1a2e")
cw = conc["elements"][0]["elements"]
hw = next((w for w in cw if w["widgetType"] == "heading"), None)
bw = next((w for w in cw if w["widgetType"] == "button"), None)
checks["Conclusion white centered"] = hw and hw["settings"]["title_color"] == "#ffffff" and hw["settings"]["align"] == "center"
checks["Conclusion button -> demo"] = bw and bw["settings"]["link"]["url"] == "https://chatsku.com/demo/" and bw["settings"]["background_color"] == "#e94560"
checks["Exec summary H2 first"] = elementor[0]["elements"][0]["elements"][0]["settings"]["title"] == "Executive summary"

checks["Schema 4 types"] = set(schema_types) == {"Article", "FAQPage", "BreadcrumbList", "HowTo"}
checks["HowTo steps>=4"] = n_steps >= 4
checks["No bare img in content"] = "<img" not in wp_content
img_order = all(not ("image" in (t := [w.get("widgetType") for w in s["elements"][0]["elements"]]) and "text-editor" in t and t.index("image") < t.index("text-editor")) for s in elementor)
checks["Image after text"] = img_order
checks["Has comparison table"] = "<table" in ALL_TEXT
checks["Has HowTo ol"] = "<ol>" in ALL_TEXT
faq_section_json = json.dumps([s for s in elementor if any(
    w.get("widgetType") == "html" and "csku-faq" in w["settings"].get("html", "")
    for w in s["elements"][0]["elements"])])
checks["FAQ accordion built"] = ALL_TEXT.count("<h3>") and "csku-faq" in faq_section_json and faq_section_json.count("<details>") >= 6
checks["Definition first sentence"] = sections["What is B2B conversational commerce?"].lstrip().startswith("<p>B2B conversational commerce is ")

plain = re.sub(r'<[^>]+>', ' ', ALL_TEXT); wc = len(plain.split())
checks["Word count"] = 1900 <= wc <= 3600
checks["Meta title <=60 |ChatSKU"] = len(META_TITLE) <= 60 and META_TITLE.endswith("| ChatSKU")
checks["Meta desc 150-160"] = 150 <= len(META_DESC) <= 160

for k, v in checks.items():
    print(f"  [{'PASS' if v else 'FAIL'}] {k}")
print(f"  ... external={len(ext_links)} internal={len(int_links)} words={wc} "
      f"metaTitle={len(META_TITLE)} metaDesc={len(META_DESC)} steps={n_steps}")
for il in int_links: print(f"      INT {il[:75]}")
for el in ext_links: print(f"      EXT {el[:75]}")

if not all(checks.values()):
    print("\nCHECKLIST FAILED:", [k for k, v in checks.items() if not v]); sys.exit(1)
print("\nALL CHECKS PASS")

if os.environ.get("DRY_RUN"):
    print("DRY_RUN: stop before push."); sys.exit(0)

# ===========================================================================
# PUSH
# ===========================================================================
print("\n" + "=" * 60 + "\nPUSHING (draft)\n" + "=" * 60)
UPDATE_POST_ID = os.environ.get("UPDATE_POST_ID", "")
payload = {"title": TITLE, "slug": SLUG, "content": wp_content, "featured_media": feat["id"],
           "meta": {"_elementor_edit_mode": "builder", "_elementor_template_type": "wp-post",
                    "_elementor_data": elementor_json}}
if UPDATE_POST_ID:
    forced = os.environ.get("FORCE_STATUS", "")
    if forced:
        payload["status"] = forced
    else:
        rq = urllib.request.Request(f"{WP_BASE}/posts/{UPDATE_POST_ID}?context=edit", headers=HEADERS)
        with urllib.request.urlopen(rq, timeout=20, context=_ssl_ctx) as r:
            print("Preserving live status:", json.loads(r.read()).get("status"))
else:
    payload["status"] = "draft"

url = f"{WP_BASE}/posts/{UPDATE_POST_ID}" if UPDATE_POST_ID else f"{WP_BASE}/posts"
req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=HEADERS, method="POST")
try:
    with urllib.request.urlopen(req, timeout=120, context=_ssl_ctx) as r:
        resp = json.loads(r.read())
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read()[:600]}"); sys.exit(1)
post_id = resp["id"]
print(f"  Post ID: {post_id}  status: {resp.get('status')}  link: {resp.get('link')}")

rq = urllib.request.Request(f"{WP_BASE}/posts/{post_id}?context=edit", headers=HEADERS)
with urllib.request.urlopen(rq, timeout=30, context=_ssl_ctx) as r:
    v = json.loads(r.read())
saved = json.loads(v.get("meta", {}).get("_elementor_data", "[]"))
print(f"  Verified: sections={len(saved)} edit_mode={v['meta'].get('_elementor_edit_mode')} "
      f"featured={v.get('featured_media')} status={v.get('status')}")

print("Clearing Elementor cache...")
creq = urllib.request.Request("https://chatsku.com/wp-json/elementor/v1/cache",
                              headers={"Authorization": f"Basic {AUTH}", "User-Agent": UA}, method="DELETE")
try:
    with urllib.request.urlopen(creq, timeout=20, context=_ssl_ctx) as r:
        print("  Cache clear HTTP", r.status)
except Exception as e:
    print("  Cache clear:", e)

# ===========================================================================
# SAVE PUBLISHED HTML
# ===========================================================================
def sec_pub(s):
    out = []
    for w in s["elements"][0]["elements"]:
        wt = w.get("widgetType")
        if wt == "heading":
            lv = w["settings"].get("header_size", "h2"); out.append(f"<{lv}>{w['settings']['title']}</{lv}>")
        elif wt == "text-editor": out.append(w["settings"]["editor"])
        elif wt == "image":
            im = w["settings"]["image"]; out.append(f'<img src="{im["url"]}" alt="{im["alt"]}" width="860" height="452">')
        elif wt == "button": out.append(f'<p><a href="{w["settings"]["link"]["url"]}">{w["settings"]["text"]}</a></p>')
        elif wt == "html": out.append(w["settings"]["html"])
    return "\n".join(out)
body_html = "\n\n".join(sec_pub(s) for s in elementor)
pub = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>{META_TITLE}</title><meta name="description" content="{META_DESC}">
<!-- Post ID: {post_id} | Slug: {SLUG} | Format B | Date: {DATE} -->
<!-- Featured: {feat['id']} | Body: {body['id']} | Infographic: {info['id']} | Status: draft -->
<!-- Yoast (manual): Title='{META_TITLE}' Desc='{META_DESC}' -->
</head><body>
<h1>{H1_ONPAGE}</h1>
<img src="{feat['url']}" width="860" height="452" alt="{FEAT_ALT}">
{body_html}
</body></html>"""
out_path = Path(r"C:\content-intel\clients\chatsku\output\published\b2b-conversational-commerce-2026-06-25.html")
out_path.write_text(pub, encoding="utf-8")
print(f"  Saved: {out_path}")

print("\n" + "=" * 60)
print(f"RESULTS_JSON={json.dumps({'post_id': post_id, 'status': v.get('status'), 'feat': feat['id'], 'body': body['id'], 'info': info['id'], 'sections': len(elementor), 'words': wc, 'internal': len(int_links), 'external': len(ext_links), 'schema': schema_types, 'howto_steps': n_steps})}")
print("MANUAL YOAST -> Title:", META_TITLE, "| Desc:", META_DESC)
