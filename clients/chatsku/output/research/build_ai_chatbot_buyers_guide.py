# -*- coding: utf-8 -*-
"""Build + publish (draft) ChatSKU post: AI chatbot buyer's guide (Format C).
Elementor structure matches post 96/186. FAQ = native accordion widget.
Conclusion = 3 widgets (white centered heading + dark centered body + #e94560 button -> /demo/).
Schema (Article+FAQPage+BreadcrumbList) via html widget. Live-link check is blocking.
Reads media IDs from media_cs.json. Dry-run unless 'publish' passed.
"""
import os, sys, re, json, secrets, base64, requests

WP = "https://chatsku.com/wp-json/wp/v2"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
U = os.environ["CHATSKU_WP_USERNAME"]; A = os.environ["CHATSKU_WP_APP_PASSWORD"]
AUTH = base64.b64encode(f"{U}:{A}".encode()).decode()
H = {"Authorization": f"Basic {AUTH}", "User-Agent": UA, "Content-Type": "application/json"}
HG = {"User-Agent": UA}
SCRATCH = r"C:\Users\ASUS\AppData\Local\Temp\claude\C--content-intel\a2138730-61a8-4dd4-8f74-ba5ab9d92c6f\scratchpad"

TITLE = "Buyer's guide: the questions to ask before buying an AI chatbot"
SLUG = "ai-chatbot-buyers-guide"
PERMALINK = f"https://chatsku.com/{SLUG}/"
DRAFT = r"C:\content-intel\clients\chatsku\output\drafts\ai-chatbot-buyers-guide-2026-07-27.md"
YOAST_TITLE = "AI Chatbot Buyer's Guide: Questions to Ask | ChatSKU"
YOAST_DESC = "A B2B buyer's guide to the 8 questions to ask before buying an AI chatbot, from catalog ingestion and pricing logic to accuracy, security, and cost."

media = json.load(open(os.path.join(SCRATCH, "media_cs.json")))
FEATURED = media["featured"]; BODY1 = media["body1"]; BODY2 = media["body2"]

# ---------- load + clean draft ----------
raw = open(DRAFT, encoding="utf-8").read()
raw = re.sub(r'<!--.*?-->', '', raw, flags=re.S).strip()

# ---------- blocking live-link check ----------
hrefs = sorted(set(re.findall(r'href="(https://chatsku\.com/[^"]+)"', raw)))
print("Live-checking", len(hrefs), "internal links...")
bad = []
for u in hrefs:
    try:
        r = requests.get(u, headers=HG, timeout=25, allow_redirects=False)
        if r.status_code != 200:
            bad.append((u, r.status_code, r.headers.get("location", "")))
    except Exception as e:
        bad.append((u, "ERR", str(e)))
if bad:
    print("BLOCKING: bad internal links:"); [print("  ", *b) for b in bad]; raise SystemExit(1)
print("  all internal links 200 OK")

# ---------- Elementor helpers ----------
def gid(): return secrets.token_hex(4)

def w_heading(title, level="h2", color="#1a1a2e", align="left"):
    s = {"title": title, "align": align, "title_color": color,
         "typography_typography": "custom",
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

def w_accordion(qa_pairs):
    tabs = [{"_id": gid(), "tab_title": q, "tab_content": a} for q, a in qa_pairs]
    return {"id": gid(), "elType": "widget", "widgetType": "accordion", "elements": [], "settings": {"tabs": tabs}}

def w_html(html):
    return {"id": gid(), "elType": "widget", "widgetType": "html", "elements": [], "settings": {"html": html}}

def section(widgets, bg, conclusion=False):
    pad = {"top": "20", "bottom": "30", "unit": "px", "right": "0", "left": "0"} if conclusion else {"top": "60", "bottom": "60", "unit": "px"}
    return {"id": gid(), "elType": "section", "isInner": False,
            "settings": {"background_background": "classic", "background_color": bg, "padding": pad},
            "elements": [{"id": gid(), "elType": "column", "isInner": False,
                          "settings": {"_column_size": 100, "width": "100",
                                       "padding": {"unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20", "isLinked": True}},
                          "elements": widgets}]}

# ---------- parse draft into sections ----------
parts = [p.strip() for p in re.split(r'(?=<h2>)', raw) if p.strip()]
parsed = []
for chunk in parts:
    m = re.match(r'<h2>(.*?)</h2>(.*)', chunk, re.S)
    if not m: continue
    title = m.group(1).strip(); body = m.group(2).strip()
    label = re.sub(r'<[^>]+>', '', title).lower().strip()
    if label == "executive summary": parsed.append(("exec", title, body))
    elif label == "introduction": parsed.append(("intro", title, body))
    elif label == "people also ask": parsed.append(("paa", title, body))
    elif label == "conclusion": parsed.append(("concl", title, body))
    elif label == "frequently asked questions": parsed.append(("faq", title, body))
    else: parsed.append(("body", title, body))

def split_qa(body):
    out = []
    for sp in re.split(r'(?=<h3>)', body.strip()):
        sp = sp.strip()
        hm = re.match(r'<h3>(.*?)</h3>(.*)', sp, re.S)
        if hm: out.append((hm.group(1).strip(), hm.group(2).strip()))
    return out

# body-image assignment: body1 -> 2nd body question, body2 -> 7th body question
BODY_COLORS = ["#f0f4ff", "#ffffff", "#f9f9fb", "#ffffff"]
sections = []; ci = 0; body_n = 0
faq_pairs = []
for kind, title, body in parsed:
    if kind == "exec":
        sections.append(section([w_heading(title), w_text(body)], "#f9f9fb"))
    elif kind == "intro":
        sections.append(section([w_heading(title), w_text(body)], "#ffffff"))
    elif kind == "body":
        body_n += 1
        bg = BODY_COLORS[ci % len(BODY_COLORS)]; ci += 1
        widgets = [w_heading(title), w_text(body)]
        if body_n == 2: widgets.append(w_image(BODY1))
        elif body_n == 7: widgets.append(w_image(BODY2))
        sections.append(section(widgets, bg))
    elif kind == "paa":
        bg = BODY_COLORS[ci % len(BODY_COLORS)]; ci += 1
        widgets = [w_heading(title)]
        for q, a in split_qa(body):
            widgets.append(w_heading(q, "h3")); widgets.append(w_text(a))
        sections.append(section(widgets, bg))
    elif kind == "concl":
        widgets = [w_heading(title, color="#ffffff", align="center"), w_text(body, dark=True),
                   w_button("See how ChatSKU answers your buyers", "https://chatsku.com/demo/")]
        sections.append(section(widgets, "#1a1a2e", conclusion=True))
    elif kind == "faq":
        faq_pairs = split_qa(body)
        widgets = [w_heading(title), w_accordion(faq_pairs)]
        # schema JSON-LD appended as html widget in FAQ section
        schema = {"@context": "https://schema.org", "@graph": [
            {"@type": "Article", "headline": TITLE, "description": YOAST_DESC,
             "image": FEATURED["url"], "datePublished": "2026-07-27", "dateModified": "2026-07-27",
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
        widgets.append(w_html('<script type="application/ld+json">' + json.dumps(schema) + '</script>'))
        sections.append(section(widgets, "#f9f9fb"))

elementor_json = json.dumps(sections)
# content fallback: strip imgs (none), keep semantic HTML
content_fallback = re.sub(r'<img[^>]*?>', '', raw)

print(f"Built {len(sections)} sections | elementor {len(elementor_json):,} chars | body imgs at #2,#7 | FAQ tabs {len(faq_pairs)}")

# fetch category from supported Dallas post 113 to match
cat = [1]
try:
    d = requests.get(f"{WP}/posts/113?_fields=categories", headers=HG, timeout=30).json()
    if d.get("categories"): cat = d["categories"]
except Exception: pass
print("categories:", cat)

payload = {"title": TITLE, "slug": SLUG, "status": "draft", "content": content_fallback,
           "excerpt": YOAST_DESC, "featured_media": FEATURED["id"], "categories": cat,
           "meta": {"_elementor_edit_mode": "builder", "_elementor_template_type": "wp-post",
                    "_elementor_data": elementor_json,
                    "_yoast_wpseo_title": YOAST_TITLE, "_yoast_wpseo_metadesc": YOAST_DESC}}

open(os.path.join(SCRATCH, "buyers_guide_elementor.json"), "w", encoding="utf-8").write(elementor_json)
if "publish" not in sys.argv:
    print("DRY RUN. pass 'publish' to POST."); raise SystemExit(0)

r = requests.post(f"{WP}/posts", headers=H, data=json.dumps(payload).encode(), timeout=120)
print("POST status:", r.status_code)
if r.status_code not in (200, 201): print(r.text[:1500]); raise SystemExit(1)
j = r.json(); pid = j["id"]
print("POST_ID:", pid, "| status:", j["status"], "| link:", j.get("link"))
# clear Elementor cache (mandatory)
cc = requests.delete("https://chatsku.com/wp-json/elementor/v1/cache", headers=H, timeout=60)
print("Elementor cache clear:", cc.status_code)
json.dump({"id": pid, "link": j.get("link"), "slug": j.get("slug")}, open(os.path.join(SCRATCH, "buyers_guide_result.json"), "w"))
