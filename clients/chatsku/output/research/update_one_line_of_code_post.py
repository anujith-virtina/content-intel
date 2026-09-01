# -*- coding: utf-8 -*-
"""UPDATE existing ChatSKU post 2044 in place with the reframed, expanded draft.
Reuses already-uploaded media (2041 featured / 2042 setup / 2043 typing) - no
re-upload. Rebuilds Elementor from the 12-section draft, places the two body
images in the most relevant sections, sets Yoast meta (REST-writable, confirmed),
and clears the Elementor cache. Pass 'publish' to actually write.
"""
import os, sys, re, json, secrets, base64, requests

WP = "https://chatsku.com/wp-json/wp/v2"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
U = os.environ["CHATSKU_WP_USERNAME"]; A = os.environ["CHATSKU_WP_APP_PASSWORD"]
AUTH = base64.b64encode(f"{U}:{A}".encode()).decode()
H = {"Authorization": f"Basic {AUTH}", "User-Agent": UA, "Content-Type": "application/json"}
HG = {"User-Agent": UA}

POST_ID = 2044
TITLE = "One line of code: what that actually means for your website"
SLUG = "one-line-of-code"
PERMALINK = f"https://chatsku.com/{SLUG}/"
DRAFT = r"C:\content-intel\clients\chatsku\output\drafts\one-line-of-code-2026-08-03.md"
YOAST_TITLE = "One Line of Code, Explained | ChatSKU"
YOAST_DESC = ('What does "one line of code" really mean? A plain-English guide to snippets, '
              'embeds, and how website tools get installed without touching a single page.')
PUBLISH_DATE = "2026-08-03"

# Reuse already-uploaded, visually-QA'd media (no duplicate uploads).
BASE = "https://chatsku.com/wp-content/uploads/2026/08/"
FEATURED = {"id": 2041, "url": BASE + "chatsku-one-line-of-code-featured.jpg",
            "alt": "Confident B2B business owner smiling while reviewing their website on a laptop after adding a one-line code snippet"}
IMG_TYPING = {"id": 2043, "url": BASE + "chatsku-one-line-of-code-body2.jpg",
              "alt": "Close-up of hands typing on a laptop, pasting a short code snippet into a website the same way an analytics tag is added"}
IMG_SETUP = {"id": 2042, "url": BASE + "chatsku-one-line-of-code-body1.jpg",
             "alt": "Business owner working at a laptop while setting up an AI catalog assistant, uploading a product catalog before going live"}

# --- load + clean draft ---
raw = open(DRAFT, encoding="utf-8").read()
raw = re.sub(r'^---.*?---\s*', '', raw, flags=re.S)      # frontmatter
raw = re.sub(r'<!--.*?-->', '', raw, flags=re.S).strip() # self-check comment
raw = re.sub(r'^#\s+.*\n', '', raw, count=1).strip()      # leading H1
# markdown internal links -> absolute, same-tab (no target attr, house rule)
raw = re.sub(r'\[([^\]]+)\]\((/[^)]+)\)', r'<a href="https://chatsku.com\2">\1</a>', raw)

lines = raw.split("\n"); html_out = []; para = []
def flush():
    if para:
        txt = " ".join(x.strip() for x in para if x.strip())
        if txt: html_out.append(f"<p>{txt}</p>")
        para.clear()
for line in lines:
    s = line.strip()
    if s.startswith("### "): flush(); html_out.append(f"<h3>{s[4:].strip()}</h3>")
    elif s.startswith("## "): flush(); html_out.append(f"<h2>{s[3:].strip()}</h2>")
    elif s == "": flush()
    else: para.append(s)
flush()
content_html = "\n".join(html_out)

# --- blocking internal-link 200 check ---
hrefs = sorted(set(re.findall(r'href="(https://chatsku\.com/[^"]+)"', content_html)))
print("Live-checking", len(hrefs), "internal links...")
bad = []
for u in hrefs:
    try:
        r = requests.get(u, headers=HG, timeout=25, allow_redirects=False)
        if r.status_code != 200: bad.append((u, r.status_code))
    except Exception as e: bad.append((u, f"ERR {e}"))
if bad:
    print("BLOCKING bad links:", bad); raise SystemExit(1)
print("  all internal links 200 OK")

# --- Elementor helpers (mirror post 96 / build_one_line_of_code_post.py) ---
def gid(): return secrets.token_hex(4)
def w_heading(title, level="h2", color="#1a1a2e", align="left"):
    s = {"title": title, "align": align, "title_color": color, "typography_typography": "custom",
         "typography_font_size": {"size": 28 if level == "h2" else 22, "unit": "px"}}
    if level != "h2": s["header_size"] = level
    return {"id": gid(), "elType": "widget", "widgetType": "heading", "elements": [], "settings": s}
def w_text(html, dark=False):
    html = re.sub(r'<img[^>]*?>', '', html).strip()
    if dark:
        html = re.sub(r'<p([ >])', r'<p style="color:#aaaacc;text-align:center;font-size:18px;max-width:720px;margin:0 auto 14px auto;"\1', html)
    return {"id": gid(), "elType": "widget", "widgetType": "text-editor", "elements": [], "settings": {"editor": html}}
def w_image(m):
    return {"id": gid(), "elType": "widget", "widgetType": "image", "elements": [],
            "settings": {"image": {"id": m["id"], "url": m["url"], "alt": m["alt"], "source": "library", "size": ""},
                         "align": "center", "width": {"size": 100, "unit": "%"},
                         "border_radius": {"top": "10", "right": "10", "bottom": "10", "left": "10", "unit": "px"}}}
def w_button(text, url):
    return {"id": gid(), "elType": "widget", "widgetType": "button", "elements": [],
            "settings": {"text": text, "link": {"url": url, "is_external": "", "nofollow": ""}, "align": "center",
                         "background_color": "#e94560", "button_text_color": "#ffffff",
                         "border_radius": {"size": 6, "unit": "px"},
                         "_margin": {"unit": "px", "top": "20", "right": "0", "bottom": "0", "left": "0", "isLinked": False}}}
def w_accordion(qa):
    return {"id": gid(), "elType": "widget", "widgetType": "accordion", "elements": [],
            "settings": {"tabs": [{"_id": gid(), "tab_title": q, "tab_content": a} for q, a in qa]}}
def w_html(html):
    return {"id": gid(), "elType": "widget", "widgetType": "html", "elements": [], "settings": {"html": html}}
def section(widgets, bg, conclusion=False):
    pad = {"top": "20", "bottom": "30", "unit": "px"} if conclusion else {"top": "60", "bottom": "60", "unit": "px"}
    return {"id": gid(), "elType": "section", "isInner": False,
            "settings": {"background_background": "classic", "background_color": bg, "padding": pad},
            "elements": [{"id": gid(), "elType": "column", "isInner": False,
                          "settings": {"_column_size": 100, "width": "100",
                                       "padding": {"unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20", "isLinked": True}},
                          "elements": widgets}]}

# --- parse sections ---
parts = [p.strip() for p in re.split(r'(?=<h2>)', content_html) if p.strip()]
parsed = []
for chunk in parts:
    m = re.match(r'<h2>(.*?)</h2>(.*)', chunk, re.S)
    if not m: continue
    title = m.group(1).strip(); body = m.group(2).strip()
    label = re.sub(r'<[^>]+>', '', title).lower().strip()
    if label == "executive summary": parsed.append(("exec", title, body))
    elif label == "introduction": parsed.append(("intro", title, body))
    elif label == "conclusion": parsed.append(("concl", title, body))
    elif label == "frequently asked questions": parsed.append(("faq", title, body))
    else: parsed.append(("body", title, body))

def split_qa(body):
    out = []
    for sp in re.split(r'(?=<h3>)', body.strip()):
        hm = re.match(r'<h3>(.*?)</h3>(.*)', sp.strip(), re.S)
        if hm: out.append((hm.group(1).strip(), hm.group(2).strip()))
    return out

BODY_COLORS = ["#f0f4ff", "#ffffff", "#f9f9fb", "#ffffff"]
sections = []; ci = 0; faq_pairs = []
for kind, title, body in parsed:
    tl = re.sub(r'<[^>]+>', '', title).lower()
    if kind == "exec":
        sections.append(section([w_heading(title), w_text(body)], "#f9f9fb"))
    elif kind == "intro":
        sections.append(section([w_heading(title), w_text(body)], "#ffffff"))
    elif kind == "body":
        bg = BODY_COLORS[ci % len(BODY_COLORS)]; ci += 1
        widgets = [w_heading(title), w_text(body)]
        # place the two images in the most relevant sections, image AFTER text-editor
        if "one line of code" in tl and "actually mean" in tl:
            widgets.append(w_image(IMG_TYPING))
        elif "how this works for an ai catalog assistant" in tl:
            widgets.append(w_image(IMG_SETUP))
        sections.append(section(widgets, bg))
    elif kind == "faq":
        faq_pairs = split_qa(body)
        schema = {"@context": "https://schema.org", "@graph": [
            {"@type": "Article", "headline": TITLE, "description": YOAST_DESC, "image": FEATURED["url"],
             "datePublished": PUBLISH_DATE, "dateModified": PUBLISH_DATE,
             "author": {"@type": "Organization", "name": "ChatSKU", "url": "https://chatsku.com/"},
             "publisher": {"@type": "Organization", "name": "ChatSKU",
                           "logo": {"@type": "ImageObject", "url": "https://chatsku.com/logo.png"}},
             "mainEntityOfPage": {"@type": "WebPage", "@id": PERMALINK}},
            {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
              "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', a).strip()}} for q, a in faq_pairs]},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://chatsku.com/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://chatsku.com/blog/"},
                {"@type": "ListItem", "position": 3, "name": TITLE, "item": PERMALINK}]}]}
        widgets = [w_heading(title), w_accordion(faq_pairs),
                   w_html('<script type="application/ld+json">' + json.dumps(schema) + '</script>')]
        sections.append(section(widgets, "#f9f9fb"))
    elif kind == "concl":
        widgets = [w_heading(title, color="#ffffff", align="center"), w_text(body, dark=True),
                   w_button("Book a live demo", "https://chatsku.com/demo/")]
        sections.append(section(widgets, "#1a1a2e", conclusion=True))

img_count = json.dumps(sections).count('"widgetType": "image"')
print(f"Parsed {len(parsed)} H2 -> {len(sections)} sections | FAQ tabs {len(faq_pairs)} | image widgets {img_count}")
elementor_json = json.dumps(sections)
content_fallback = re.sub(r'<img[^>]*?>', '', content_html)
print(f"YOAST_DESC length: {len(YOAST_DESC)} chars")

if "publish" not in sys.argv:
    print("\nDRY RUN. Pass 'publish' to update post", POST_ID); raise SystemExit(0)

# --- update post in place (fetch first to confirm it's still a draft we own) ---
cur = requests.get(f"{WP}/posts/{POST_ID}", params={"context": "edit"}, headers=H, timeout=30).json()
print("current status:", cur.get("status"), "| slug:", cur.get("slug"))
if cur.get("status") != "draft":
    print("SAFETY STOP: post is no longer a draft (status=%s). Not overwriting." % cur.get("status")); raise SystemExit(1)

payload = {
    "title": TITLE, "slug": SLUG, "status": "draft", "content": content_fallback,
    "excerpt": YOAST_DESC, "featured_media": FEATURED["id"], "categories": [29],
    "meta": {"_elementor_edit_mode": "builder", "_elementor_template_type": "wp-post",
             "_elementor_data": elementor_json,
             "_yoast_wpseo_title": YOAST_TITLE, "_yoast_wpseo_metadesc": YOAST_DESC}
}
r = requests.post(f"{WP}/posts/{POST_ID}", headers=H, data=json.dumps(payload).encode(), timeout=120)
print("UPDATE status:", r.status_code)
if r.status_code not in (200, 201): print(r.text[:1500]); raise SystemExit(1)
cc = requests.delete("https://chatsku.com/wp-json/elementor/v1/cache", headers=H, timeout=60)
print("Elementor cache clear:", cc.status_code)
# verify yoast persisted
v = requests.get(f"{WP}/posts/{POST_ID}", params={"context": "edit"}, headers=H, timeout=30).json()
print("verified yoast title:", v.get("yoast_head_json", {}).get("title"))
print("verified yoast desc:", (v.get("yoast_head_json", {}).get("description") or "")[:80])
print("DONE. Post", POST_ID, "updated as draft.")
