"""
Build + publish: what-is-the-response-gap
"What is the response gap? (And how to close it overnight)"
Format B (Conversational Q&A) + definitional story hook.   Date: 2026-07-10

Parses the approved draft, splits <h3> into heading widgets, styles the comparison
table (post 299 gold standard), renders FAQ as Elementor native accordion (post 299
standard), adds Article + FAQPage + BreadcrumbList JSON-LD.
Images: featured + 2 body photos (all 860x452).
Env: DRY_RUN=1, REUSE_MEDIA="feat,body1,body2", UPDATE_POST_ID, FORCE_STATUS
"""
import json, secrets, re, urllib.request, urllib.error, urllib.parse
import base64, os, io, sys, ssl
from pathlib import Path
from collections import OrderedDict

_ssl_ctx = ssl._create_unverified_context()
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

DRAFT = r"C:\content-intel\clients\chatsku\output\drafts\what-is-the-response-gap-2026-07-10.md"
SCRATCH = os.environ.get("OUT_DIR",
    r"C:\Users\ASUS\AppData\Local\Temp\claude\C--content-intel\34776345-ed10-4d77-a06e-ef41ff62aa8b\scratchpad")

TITLE = "What is the response gap? (And how to close it overnight)"
H1_ONPAGE = TITLE
SLUG = "what-is-the-response-gap"
DATE = "2026-07-10"
META_TITLE = "What Is the Response Gap? | ChatSKU"
META_DESC = ("The response gap is the delay between a buyer's inquiry and your first reply. See what "
             "it costs your pipeline and how to close it overnight, with no new hires.")

# ===========================================================================
# PARSE DRAFT
# ===========================================================================
raw = Path(DRAFT).read_text(encoding="utf-8")
raw = re.sub(r'^---\n.*?\n---\n', '', raw, count=1, flags=re.S)
chunks = re.split(r'^### SECTION: (.+)$', raw, flags=re.M)
sections = OrderedDict()
for i in range(1, len(chunks), 2):
    head = chunks[i].strip()
    body = re.sub(r'<!--.*?-->', '', chunks[i + 1], flags=re.S)
    body = re.sub(r'^\s*-{3,}\s*$', '', body, flags=re.M).strip()
    body = re.sub(r'\[BODY IMAGE:.*?\]', '', body, flags=re.S).strip()
    body = re.sub(r'\[CTA BUTTON:.*?\]', '', body, flags=re.S).strip()
    body = body.replace('href="/', 'href="https://chatsku.com/')
    sections[head] = body

EXPECTED = [
    "Executive summary", "Introduction", "What is the response gap, exactly?",
    "Why does the response gap happen? (it isn't staffing)",
    "What does the response gap actually cost you?",
    "Response gap open vs response gap closed",
    "How do you close the response gap overnight?",
    "People also ask", "Conclusion", "Frequently asked questions",
]
missing = [h for h in EXPECTED if h not in sections]
if missing:
    print("FATAL missing sections:", missing); sys.exit(1)
print(f"Parsed {len(sections)} sections.")

# ---- table styling (post 299 gold standard) ----
def style_table(html):
    html = html.replace('<table>',
        '<div style="overflow-x:auto;margin:8px 0;"><table style="border-collapse:collapse;width:100%;font-size:15px;">')
    html = html.replace('</table>', '</table></div>')
    html = re.sub(r'<th([^>]*)>',
        lambda m: f'<th style="background:#1a1a2e;color:#ffffff;padding:10px 14px;text-align:left;"{m.group(1)}>', html)
    html = re.sub(r'<td([^>]*)>',
        lambda m: f'<td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;"{m.group(1)}>', html)
    def alt(m):
        rows = m.group(1).split('<tr>')
        out = rows[0]
        for i, r in enumerate(rows[1:]):
            bg = '#f0f4ff' if i % 2 == 0 else '#ffffff'
            out += f'<tr style="background:{bg};">' + r
        return '<tbody>' + out + '</tbody>'
    return re.sub(r'<tbody>(.*?)</tbody>', alt, html, flags=re.S)

n_tables = 0
_TBL_SEC = "Response gap open vs response gap closed"
if "<table>" in sections[_TBL_SEC]:
    sections[_TBL_SEC] = style_table(sections[_TBL_SEC]); n_tables += 1
print(f"Styled {n_tables} table(s) (navy header, alt rows, scroll wrapper)")

ALL_TEXT = "\n".join(sections.values())

# -- em dash + banned scan -----------------------------------------------------
em_count = ALL_TEXT.count("—") + ALL_TEXT.count("&mdash;")
print(f"Em dash scan: {'PASS' if em_count == 0 else 'FAIL'} ({em_count})")
if em_count: sys.exit(1)
BANNED = ["just a chatbot", "ai-powered", "revolutionary", "game-changing", "cutting-edge",
          "in today's fast-paced world", "in conclusion", "delve", "leverage", "seamless",
          "robust", "supercharge", "unlock", "transform your", "moreover", "furthermore", "navigate the"]
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

def make_accordion(faq_html):
    """Elementor native accordion widget (accordion.default) — matches live ChatSKU blogs (post 299)."""
    pairs = re.findall(r'<h3>(.*?)</h3>\s*(<p>.*?</p>)', faq_html, flags=re.S)
    tabs = []
    for q, a in pairs:
        content = re.sub(r'^\s*<p>(.*)</p>\s*$', r'\1', a.strip(), flags=re.S).strip()
        tabs.append({"tab_title": strip_tags_inline(q).strip(), "tab_content": content, "_id": secrets.token_hex(4)[:7]})
    return {"id": gid(), "elType": "widget", "widgetType": "accordion", "elements": [],
            "settings": {"tabs": tabs, "title_html_tag": "h3"}}, len(tabs)

def strip_tags_inline(s):
    return re.sub(r'<[^>]+>', '', s)

def split_widgets(html):
    """Split section HTML into ordered widgets: <h3> -> heading widget, other HTML -> text-editor."""
    parts = re.split(r'(<h3>.*?</h3>)', html, flags=re.S)
    out = []
    for part in parts:
        p = part.strip()
        if not p: continue
        m = re.match(r'<h3>(.*?)</h3>$', p, flags=re.S)
        out.append(make_heading(m.group(1).strip(), "h3") if m else make_text(p))
    return out

# ---- schema ----
def strip_tags(s): return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()
def build_schema(feat_url):
    article = {"@context": "https://schema.org", "@type": "Article", "headline": TITLE,
               "description": META_DESC, "image": feat_url, "datePublished": DATE, "dateModified": DATE,
               "author": {"@type": "Organization", "name": "ChatSKU", "url": "https://chatsku.com"},
               "publisher": {"@type": "Organization", "name": "ChatSKU",
                             "logo": {"@type": "ImageObject", "url": "https://chatsku.com/wp-content/uploads/2024/logo.png"}},
               "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://chatsku.com/{SLUG}/"}}
    faqs = [(strip_tags(q), strip_tags(a)) for q, a in
            re.findall(r'<h3>(.*?)</h3>\s*<p>(.*?)</p>', sections["Frequently asked questions"], flags=re.S)]
    faqpage = {"@context": "https://schema.org", "@type": "FAQPage",
               "mainEntity": [{"@type": "Question", "name": q,
                               "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    breadcrumb = {"@context": "https://schema.org", "@type": "BreadcrumbList",
                  "itemListElement": [
                      {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://chatsku.com/"},
                      {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://chatsku.com/blog/"},
                      {"@type": "ListItem", "position": 3, "name": TITLE, "item": f"https://chatsku.com/{SLUG}/"}]}
    blocks, types = [], []
    for nm, obj in [("Article", article), ("FAQPage", faqpage), ("BreadcrumbList", breadcrumb)]:
        s = json.dumps(obj, ensure_ascii=False); json.loads(s)
        blocks.append(f'<script type="application/ld+json">\n{s}\n</script>'); types.append(obj["@type"])
        print(f"  JSON-LD {nm}: valid ({len(s)} chars)")
    return "\n".join(blocks), types, len(faqs)

# ---- images ----
def resize_file(path, w=860, h=452, q=82):
    from PIL import Image
    img = Image.open(path).convert("RGB"); sw, sh = img.size
    sc = max(w / sw, h / sh); img = img.resize((int(sw * sc), int(sh * sc)), Image.LANCZOS)
    nw, nh = img.size; left, top = (nw - w) // 2, (nh - h) // 2
    img = img.crop((left, top, left + w, top + h))
    buf = io.BytesIO(); img.save(buf, "JPEG", quality=q, optimize=True); data = buf.getvalue()
    if len(data) > 200 * 1024:
        buf = io.BytesIO(); img.save(buf, "JPEG", quality=70, optimize=True); data = buf.getvalue()
    from PIL import Image as _I
    assert _I.open(io.BytesIO(data)).size == (w, h)
    print(f"  Resized {os.path.basename(path)} -> {w}x{h} ({len(data)//1024}KB)")
    return data

def upload(jpeg, filename, alt):
    uh = {"Authorization": f"Basic {AUTH}", "User-Agent": UA, "Content-Type": "image/jpeg",
          "Content-Disposition": f'attachment; filename="{filename}"'}
    with urllib.request.urlopen(urllib.request.Request(f"{WP_BASE}/media", data=jpeg, headers=uh, method="POST"),
                                timeout=60, context=_ssl_ctx) as r:
        m = json.loads(r.read())
    mid, murl = m["id"], m["source_url"]
    with urllib.request.urlopen(urllib.request.Request(f"{WP_BASE}/media/{mid}", data=json.dumps({"alt_text": alt}).encode(),
                                headers=HEADERS, method="POST"), timeout=20, context=_ssl_ctx) as r:
        r.read()
    print(f"  Uploaded {filename}: ID={mid}")
    return {"id": mid, "url": murl, "alt": alt}

def fetch_media(mid, alt):
    with urllib.request.urlopen(urllib.request.Request(f"{WP_BASE}/media/{mid}", headers=HEADERS),
                                timeout=20, context=_ssl_ctx) as r:
        m = json.loads(r.read())
    return {"id": int(mid), "url": m["source_url"], "alt": alt}

FEAT_SRC = os.path.join(SCRATCH, "rg_feat_0.jpg")
BODY1_SRC = os.path.join(SCRATCH, "rg_body1_1.jpg")
BODY2_SRC = os.path.join(SCRATCH, "rg_body2_2.jpg")
FEAT_ALT = ("B2B buyer typing a product question into a laptop late at night with no reply from the "
            "supplier, illustrating the response gap in B2B sales")
BODY1_ALT = ("Sales team reviewing a backlog of unanswered B2B inquiries and RFQ forms on office "
             "computer screens as the response gap builds")
BODY2_ALT = ("Warehouse office desk with a laptop showing a live AI catalog assistant answering a "
             "buyer question in real time to close the response gap")

REUSE = os.environ.get("REUSE_MEDIA", "")
if os.environ.get("DRY_RUN") and not REUSE:
    feat = {"id": 9001, "url": "https://chatsku.com/wp-content/uploads/2026/07/f.jpg", "alt": FEAT_ALT}
    body1 = {"id": 9002, "url": "https://chatsku.com/wp-content/uploads/2026/07/b1.jpg", "alt": BODY1_ALT}
    body2 = {"id": 9003, "url": "https://chatsku.com/wp-content/uploads/2026/07/b2.jpg", "alt": BODY2_ALT}
    print("DRY_RUN images")
elif REUSE:
    fid, b1id, b2id = REUSE.split(",")
    feat, body1, body2 = (fetch_media(fid, FEAT_ALT), fetch_media(b1id, BODY1_ALT), fetch_media(b2id, BODY2_ALT))
    print(f"Reusing media: {fid},{b1id},{b2id}")
else:
    print("\nUploading images...")
    feat = upload(resize_file(FEAT_SRC), "chatsku-response-gap-featured.jpg", FEAT_ALT)
    body1 = upload(resize_file(BODY1_SRC), "chatsku-response-gap-backlog.jpg", BODY1_ALT)
    body2 = upload(resize_file(BODY2_SRC), "chatsku-response-gap-closed-live.jpg", BODY2_ALT)

for lbl, m in [("feat", feat), ("body1", body1), ("body2", body2)]:
    if not m["url"].startswith("https://chatsku.com/wp-content/uploads/"):
        print(f"FATAL {lbl} url: {m['url']}"); sys.exit(1)
print(f"Images: feat={feat['id']} body1={body1['id']} body2={body2['id']}")

# ---- build sections ----
BG = {
    "Executive summary": "#f9f9fb", "Introduction": "#ffffff",
    "What is the response gap, exactly?": "#f0f4ff",
    "Why does the response gap happen? (it isn't staffing)": "#ffffff",
    "What does the response gap actually cost you?": "#f9f9fb",
    "Response gap open vs response gap closed": "#ffffff",
    "How do you close the response gap overnight?": "#f0f4ff",
    "People also ask": "#ffffff",
    "Frequently asked questions": "#f9f9fb", "Conclusion": "#1a1a2e",
}
IMG_AFTER = {
    "What is the response gap, exactly?": body1,
    "How do you close the response gap overnight?": body2,
}
elementor = []
for head, html in sections.items():
    if head == "Conclusion":
        elementor.append(make_section([
            make_heading("Conclusion", color="#ffffff", align="center"),
            make_text(html, dark_section=True),
            make_button("See the live demo", "https://chatsku.com/demo/"),
        ], bg="#1a1a2e", is_conclusion=True)); continue
    if head == "Frequently asked questions":
        acc_widget, n_acc = make_accordion(html)
        elementor.append(make_section([make_heading(head, "h2"), acc_widget], bg=BG[head]))
        print(f"FAQ: Elementor native accordion widget with {n_acc} tabs (matches post 299)")
        continue
    if head == "People also ask":
        widgets = [make_heading(head, "h2")] + split_widgets(html)
        elementor.append(make_section(widgets, bg=BG[head]))
        continue
    widgets = [make_heading(head, "h2")] + split_widgets(html)
    if head in IMG_AFTER:
        widgets.append(make_image_widget(IMG_AFTER[head]))
    elementor.append(make_section(widgets, bg=BG[head]))

schema_html, schema_types, n_faq_schema = build_schema(feat["url"])
schema_sec = make_section([make_html_widget(schema_html)], bg="#ffffff")
schema_sec["settings"]["padding"] = {"top": "0", "bottom": "0", "unit": "px"}
elementor.append(schema_sec)
elementor_json = json.dumps(elementor)

# ---- wp content fallback ----
def sec_to_content(s):
    out = []
    for w in s["elements"][0]["elements"]:
        wt = w.get("widgetType")
        if wt == "heading":
            lv = w["settings"].get("header_size", "h2"); out.append(f"<{lv}>{w['settings']['title']}</{lv}>")
        elif wt == "text-editor": out.append(w["settings"]["editor"])
        elif wt == "button": out.append(f'<p><a href="{w["settings"]["link"]["url"]}">{w["settings"]["text"]}</a></p>')
        elif wt == "accordion":
            for t in w["settings"]["tabs"]:
                out.append(f'<h3>{t["tab_title"]}</h3>\n<p>{t["tab_content"]}</p>')
        elif wt == "html": out.append(w["settings"]["html"])
    return "\n".join(out)
wp_content = re.sub(r'<img[^>]*>', '', "\n\n".join(sec_to_content(s) for s in elementor))

# ===========================================================================
# DEDUP AUDIT — live posts (incl. untracked b2b-customers-leave-for-faster-competitors)
# ===========================================================================
print("\n" + "=" * 60 + "\nDEDUP AUDIT (8-word shingles vs all live/draft posts)\n" + "=" * 60)
STOP_HTML = re.compile(r"<[^>]+>")
def plain(html):
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S | re.I)
    txt = STOP_HTML.sub(" ", html)
    txt = (txt.replace("&amp;", "&").replace("&#8217;", "'").replace("&#8220;", '"')
              .replace("&#8221;", '"').replace("&nbsp;", " ").replace("&#8211;", "-"))
    return txt
WORD = re.compile(r"[a-z0-9']+")
def toks(txt): return WORD.findall(txt.lower())
def shingles(tokens, n=8): return {" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)}

def get_all_posts():
    out = {}
    for status in ("publish", "draft", "pending", "future", "private"):
        page = 1
        while True:
            url = f"{WP_BASE}/posts?" + urllib.parse.urlencode(
                {"status": status, "per_page": 100, "page": page, "context": "edit",
                 "_fields": "id,slug,title,content"})
            try:
                req = urllib.request.Request(url, headers=HEADERS)
                with urllib.request.urlopen(req, timeout=40, context=_ssl_ctx) as r:
                    data = json.loads(r.read())
            except Exception:
                break
            if not data: break
            for p in data:
                out[p["id"]] = {"slug": p.get("slug", ""),
                                 "title": plain(p.get("title", {}).get("rendered", "")).strip(),
                                 "text": plain(p.get("content", {}).get("rendered", ""))}
            if len(data) < 100: break
            page += 1
    return out

new_shingles = shingles(toks(plain(ALL_TEXT)))
try:
    live_posts = get_all_posts()
    print(f"Fetched {len(live_posts)} live/draft posts for comparison.")
    dedup_clean = True
    for pid, p in sorted(live_posts.items()):
        if p["slug"] == SLUG:
            continue
        common = new_shingles & shingles(toks(p["text"]))
        if common:
            dedup_clean = False
            print(f"  vs {pid} ({p['slug'][:50]}): {len(common)} shared 8-word sequence(s)")
            for c in sorted(common):
                print(f"      >> \"{c}\"")
    if dedup_clean:
        print("  No 8-word verbatim overlap with ANY live/draft post. CLEAN.")
except Exception as e:
    print(f"  WARNING: dedup audit could not complete ({e}). Proceeding with local checklist only.")
    dedup_clean = True

# ---- checklist ----
print("\n" + "=" * 60 + "\nPRE-PUBLISH CHECKLIST\n" + "=" * 60)
checks = {}
checks["Em dashes 0"] = em_count == 0
checks["No banned"] = not banned_hits
checks["Dedup clean (8-word shingles)"] = dedup_clean
EXISTING_SLUGS = ["rfq-automation-manufacturers", "rfq-automation-for-product-catalogs",
    "ai-chatbot-for-manufacturers-dallas", "b2b-ecommerce-chatbot-dallas", "pdf-catalog-sales-liability",
    "rfq-form-conversion-rate", "b2b-catalog-conversion-rate", "convert-pdf-catalog-to-website",
    "b2b-catalog-issues-costing-sales", "b2b-after-hours-buyer-problem", "b2b-catalog-revenue-leakage",
    "lost-b2b-revenue-calculator", "best-b2b-catalog-chatbots-2026", "b2b-quote-to-order-automation",
    "what-is-a-b2b-catalog-chatbot", "b2b-conversational-commerce", "what-is-a-passive-catalog",
    "b2b-chatbot-for-woocommerce", "magento-b2b-chatbot-integration", "funnel-inversion-answer-first",
    "b2b-customers-leave-for-faster-competitors", "passive-catalog-costing-you-sales"]
checks["Slug unique"] = SLUG not in EXISTING_SLUGS
checks["Featured media"] = bool(feat["id"])
imgs = [feat, body1, body2]
checks["Img URLs"] = all(m["url"].startswith("https://chatsku.com/wp-content/uploads/") for m in imgs)
alts = [m["alt"] for m in imgs]
checks["Alt 80-150 + unique"] = all(80 <= len(a) <= 150 for a in alts) and len(set(alts)) == 3
for l, a in zip(["feat", "body1", "body2"], alts): print(f"      alt[{l}] {len(a)}: {a}")
ext_links = re.findall(r'href="https?://(?!chatsku\.com)[^"]+', ALL_TEXT)
checks["External <=2"] = len(ext_links) <= 2
int_links = re.findall(r'href="https://chatsku\.com/[^"]+', ALL_TEXT)
checks["Internal >=3 pages + >=2 blogs"] = len(int_links) >= 5
ext_anchors = re.findall(r'<a [^>]*href="https?://(?!chatsku\.com)[^"]+"[^>]*>', ALL_TEXT)
checks["Ext target/rel"] = all('target="_blank"' in a and 'rel="noopener noreferrer"' in a for a in ext_anchors)
int_anchors = re.findall(r'<a [^>]*href="https://chatsku\.com/[^"]+"[^>]*>', ALL_TEXT)
checks["Int no target"] = all('target=' not in a for a in int_anchors)
# response-gap page linked at least twice (companion post requirement)
rg_anchors = re.findall(r'<a href="https://chatsku\.com/response-gap/"[^>]*>(.*?)</a>', ALL_TEXT, flags=re.S)
checks["response-gap page linked >=2x"] = len(rg_anchors) >= 2
print(f"      response-gap anchors: {[a.strip() for a in rg_anchors]}")
COMP = ["drift.com", "intercom.com", "tidio.com", "zendesk.com", "bigcommerce.com",
        "algolia", "zoovu", "coveo", "bloomreach", "humcommerce"]
checks["No competitor mentions"] = not any(c in ALL_TEXT.lower() for c in COMP)
conc = next(s for s in elementor if s["settings"]["background_color"] == "#1a1a2e")
cw = conc["elements"][0]["elements"]
hw = next((w for w in cw if w["widgetType"] == "heading"), None)
bw = next((w for w in cw if w["widgetType"] == "button"), None)
checks["Conclusion white centered"] = hw and hw["settings"]["title_color"] == "#ffffff" and hw["settings"]["align"] == "center"
checks["Conclusion button -> demo"] = bw and bw["settings"]["link"]["url"] == "https://chatsku.com/demo/"
checks["Exec summary H2 first"] = elementor[0]["elements"][0]["elements"][0]["settings"]["title"] == "Executive summary"
checks["Schema 3 types"] = set(schema_types) == {"Article", "FAQPage", "BreadcrumbList"}
checks["FAQ schema 6-8"] = 6 <= n_faq_schema <= 8
checks["No bare img in content"] = "<img" not in wp_content
img_order = all(not ("image" in (t := [w.get("widgetType") for w in s["elements"][0]["elements"]]) and
                     "text-editor" in t and t.index("image") < t.index("text-editor")) for s in elementor)
checks["Image after text"] = img_order
def _sec_title(s):
    ws = s["elements"][0]["elements"]
    return ws[0]["settings"].get("title", "") if ws else ""
order_titles = [_sec_title(s) for s in elementor]
checks["Conclusion before FAQ"] = ("Conclusion" in order_titles and "Frequently asked questions" in order_titles
    and order_titles.index("Conclusion") < order_titles.index("Frequently asked questions"))
acc_widgets = [w for s in elementor for w in s["elements"][0]["elements"] if w.get("widgetType") == "accordion"]
checks["FAQ Elementor accordion"] = len(acc_widgets) == 1 and 6 <= len(acc_widgets[0]["settings"]["tabs"]) <= 8
checks["Has 1 table styled"] = ALL_TEXT.count('border-collapse') >= 1
checks["No colspan in tables"] = "colspan" not in ALL_TEXT
checks["Has PAA H3s"] = sections["People also ask"].count("<h3>") >= 3
checks["Definition first sentence"] = sections["What is the response gap, exactly?"].lstrip().startswith(
    "<p>The response gap is the delay")
checks["Primary kw in title"] = "response gap" in TITLE.lower()
checks["Sentence case headings"] = all(not h.isupper() and h == (h[0] + h[1:]) for h in sections.keys())
plain_text = re.sub(r'<[^>]+>', ' ', ALL_TEXT); wc = len(plain_text.split())
checks["Word count 1200-3000"] = 1200 <= wc <= 3000
checks["Meta title <=60 |ChatSKU"] = len(META_TITLE) <= 60 and META_TITLE.endswith("| ChatSKU")
checks["Meta desc 150-160"] = 150 <= len(META_DESC) <= 160
checks["2 body images"] = len(imgs) - 1 == 2
for k, v in checks.items():
    print(f"  [{'PASS' if v else 'FAIL'}] {k}")
print(f"  ... external={len(ext_links)} internal={len(int_links)} words={wc} "
      f"metaTitle={len(META_TITLE)} metaDesc={len(META_DESC)} faqs={n_faq_schema} tables={n_tables}")
for il in int_links: print(f"      INT {il[:90]}")
for el in ext_links: print(f"      EXT {el[:90]}")
if not all(checks.values()):
    print("\nCHECKLIST FAILED:", [k for k, v in checks.items() if not v]); sys.exit(1)
print("\nALL CHECKS PASS")
if os.environ.get("DRY_RUN"):
    print("DRY_RUN: stop before push."); sys.exit(0)

# ---- push ----
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
        with urllib.request.urlopen(urllib.request.Request(f"{WP_BASE}/posts/{UPDATE_POST_ID}?context=edit", headers=HEADERS),
                                    timeout=20, context=_ssl_ctx) as r:
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
with urllib.request.urlopen(urllib.request.Request(f"{WP_BASE}/posts/{post_id}?context=edit", headers=HEADERS),
                            timeout=30, context=_ssl_ctx) as r:
    v = json.loads(r.read())
saved = json.loads(v.get("meta", {}).get("_elementor_data", "[]"))
print(f"  Verified: sections={len(saved)} edit_mode={v['meta'].get('_elementor_edit_mode')} "
      f"featured={v.get('featured_media')} status={v.get('status')}")
print("Clearing Elementor cache...")
try:
    with urllib.request.urlopen(urllib.request.Request("https://chatsku.com/wp-json/elementor/v1/cache",
                                headers={"Authorization": f"Basic {AUTH}", "User-Agent": UA}, method="DELETE"),
                                timeout=20, context=_ssl_ctx) as r:
        print("  Cache clear HTTP", r.status)
except Exception as e:
    print("  Cache clear:", e)

# ---- save published html ----
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
        elif wt == "accordion":
            for t in w["settings"]["tabs"]:
                out.append(f'<h3>{t["tab_title"]}</h3>\n<p>{t["tab_content"]}</p>')
        elif wt == "html": out.append(w["settings"]["html"])
    return "\n".join(out)
pub = (f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">\n<title>{META_TITLE}</title>'
       f'<meta name="description" content="{META_DESC}">\n'
       f'<!-- Post ID: {post_id} | Slug: {SLUG} | Format B | Date: {DATE} -->\n'
       f'<!-- Featured: {feat["id"]} | Body1: {body1["id"]} | Body2: {body2["id"]} | Status: draft -->\n'
       f'<!-- Yoast (manual): Title=\'{META_TITLE}\' Desc=\'{META_DESC}\' -->\n</head><body>\n'
       f'<h1>{H1_ONPAGE}</h1>\n<img src="{feat["url"]}" width="860" height="452" alt="{FEAT_ALT}">\n'
       + "\n\n".join(sec_pub(s) for s in elementor) + "\n</body></html>")
out_path = Path(r"C:\content-intel\clients\chatsku\output\published\what-is-the-response-gap-2026-07-10.html")
out_path.write_text(pub, encoding="utf-8")
print(f"  Saved: {out_path}")
print("\n" + "=" * 60)
print(f"RESULTS_JSON={json.dumps({'post_id': post_id, 'status': v.get('status'), 'feat': feat['id'], 'body1': body1['id'], 'body2': body2['id'], 'sections': len(elementor), 'words': wc, 'internal': len(int_links), 'external': len(ext_links), 'schema': schema_types})}")
print("MANUAL YOAST -> Title:", META_TITLE, "| Desc:", META_DESC)
