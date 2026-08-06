# -*- coding: utf-8 -*-
"""Build + publish (draft) ChatSKU post: "Agentic commerce glossary: what
manufacturers actually need to know" (Format B variant / definitional
reference glossary).

Elementor structure mirrors post 96 / post 186 (build_elementor_post186_v3.py)
and the FAQ-accordion convention established in posts 299/685/1056/1300/1538/
1684/1880. PAA rendered as heading+text pairs (not accordion), matching
Format A/B convention. TOC rendered as a plain text-editor widget (simple
<ul><li><a href="#anchor">) per MUST-FOLLOW-RULES.md section 4 -- no
!important, no SVG arrows. Each H2 heading widget gets a matching
_element_id so the TOC anchors actually resolve.

Comparison table converted from the draft's markdown pipe-table into the
house-standard styled HTML table (navy #1a1a2e header, alternating
#f0f4ff/#ffffff rows, padded cells, mobile overflow-x wrapper) -- exact
pattern confirmed from published posts (b2b-chatbot-for-woocommerce,
magento-b2b-chatbot-integration, what-is-the-response-gap, etc.).

Conclusion = 3 widgets: white centered heading + dark centered text-editor
(no inline CTA link) + #e94560 button -> https://chatsku.com/demo/.

Images: 1 featured + 2 body, all 860x452, sourced Pexels > Openverse(cc0, NO
source=stocksnap -- dead) > Wikimedia. Subject: B2B sales/office scenes
(vendor-email scenario, catalog/data review). Visually QA before selecting.

NOTE: this script was authored in a session with NO code-execution tool
available (Read/Write/Edit/Glob/Grep/WebFetch only -- no shell, no requests
library access). It has NOT been run. All internal/external link checks in
this task were instead performed via WebFetch against the live site (see
task summary). Before treating this post as pushed:
  1. Run this script in a Python environment with `requests` + `Pillow`,
     network access, and CHATSKU_WP_USERNAME / CHATSKU_WP_APP_PASSWORD set.
  2. Default is DRY_RUN (parses + prints, no image sourcing, no push).
     Pass "publish" as the only argv to source/upload images and push.
  3. Manually visually QA every candidate image before accepting -- this
     script's auto-picker takes the first image that downloads and resizes
     cleanly; do not trust it blindly (see feedback_image_visual_qa).
"""
import os, sys, re, io, json, time, secrets, base64, requests

WP = "https://chatsku.com/wp-json/wp/v2"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
U = os.environ["CHATSKU_WP_USERNAME"]
A = os.environ["CHATSKU_WP_APP_PASSWORD"]
AUTH = base64.b64encode(f"{U}:{A}".encode()).decode()
H = {"Authorization": f"Basic {AUTH}", "User-Agent": UA, "Content-Type": "application/json"}
HG = {"User-Agent": UA}
SCRATCH = os.environ.get("SCRATCH_DIR", os.getcwd())

TITLE = "Agentic commerce glossary: what manufacturers actually need to know"
SLUG = "agentic-commerce-glossary"
PERMALINK = f"https://chatsku.com/{SLUG}/"
DRAFT = r"C:\content-intel\clients\chatsku\output\drafts\agentic-commerce-glossary-2026-08-06.md"
YOAST_TITLE = "Agentic Commerce Glossary for B2B Manufacturers | ChatSKU"
YOAST_DESC = ("A plain-English glossary of agentic commerce terms for B2B manufacturers: "
              "which protocols are shipped, which are still just announced, and what to "
              "track first.")
PUBLISH_DATE = "2026-08-06"

# ---------------------------------------------------------------------------
# 1. Image sourcing (Pexels -> Openverse cc0 -> Wikimedia). 860x452, JPEG q82.
# ---------------------------------------------------------------------------
PEXELS_KEY = os.environ.get("PEXELS_API_KEY", "")

IMG_QUERIES = {
    "featured": ["B2B sales team office meeting", "manufacturer office buyer computer",
                 "sales director office discussion"],
    "body1": ["B2B sales conversation meeting", "sales team computer screens office",
              "office team discussing laptop"],
    "body2": ["product catalog spreadsheet office", "inventory SKU computer office",
              "warehouse desk data entry"],
}

def pexels_search(query):
    if not PEXELS_KEY:
        return []
    try:
        r = requests.get("https://api.pexels.com/v1/search",
                          params={"query": query, "orientation": "landscape", "per_page": 5},
                          headers={"Authorization": PEXELS_KEY, "User-Agent": UA}, timeout=25)
        return [p["src"]["large2x"] for p in r.json().get("photos", [])]
    except Exception as e:
        print("  pexels err", query, e)
        return []

def openverse_search(query):
    try:
        r = requests.get("https://api.openverse.org/v1/images/",
                          params={"q": query, "license": "cc0,pdm", "page_size": 10,
                                   "aspect_ratio": "wide"},
                          headers={"User-Agent": UA}, timeout=25)
        return [res["url"] for res in r.json().get("results", []) if res.get("url")]
    except Exception as e:
        print("  openverse err", query, e)
        return []

def wikimedia_search(query):
    try:
        r = requests.get("https://commons.wikimedia.org/w/api.php", params={
            "action": "query", "format": "json", "list": "search",
            "srsearch": f"{query} filetype:bitmap", "srnamespace": 6, "srlimit": 10
        }, headers={"User-Agent": UA}, timeout=25)
        titles = [it["title"] for it in r.json().get("query", {}).get("search", [])]
        urls = []
        for t in titles:
            time.sleep(1)
            ir = requests.get("https://commons.wikimedia.org/w/api.php", params={
                "action": "query", "format": "json", "titles": t, "prop": "imageinfo",
                "iiprop": "url", "iiurlwidth": 1600
            }, headers={"User-Agent": UA}, timeout=25)
            pages = ir.json().get("query", {}).get("pages", {})
            for p in pages.values():
                info = p.get("imageinfo", [{}])[0]
                u = info.get("thumburl") or info.get("url")
                if u:
                    urls.append(u)
        return urls
    except Exception as e:
        print("  wikimedia err", query, e)
        return []

def download_candidate(url):
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=25)
        data = r.content
        if len(data) < 8000:
            return None
        if not (data[:2] == b"\xff\xd8" or data[:8] == b"\x89PNG\r\n\x1a\n"):
            return None
        return data
    except Exception:
        return None

def fit_860x452(data):
    from PIL import Image
    im = Image.open(io.BytesIO(data)).convert("RGB")
    target_w, target_h = 860, 452
    src_w, src_h = im.size
    scale = max(target_w / src_w, target_h / src_h)
    new_w, new_h = int(src_w * scale + 0.5), int(src_h * scale + 0.5)
    im = im.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    im = im.crop((left, top, left + target_w, top + target_h))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=82, optimize=True)
    return buf.getvalue()

def source_image(slot):
    """AUTO-PICKER -- do not trust blindly. Visually QA the chosen candidate
    (print the URL and review it) before running with 'publish' for real."""
    for query in IMG_QUERIES[slot]:
        for fn in (pexels_search, openverse_search, wikimedia_search):
            for url in fn(query):
                raw = download_candidate(url)
                if not raw:
                    continue
                try:
                    resized = fit_860x452(raw)
                except Exception:
                    continue
                if len(resized) > 200_000:
                    continue
                return resized, url
    return None, None

def upload_media(image_bytes, filename, alt_text):
    r = requests.post(f"{WP}/media", headers={
        "Authorization": H["Authorization"], "User-Agent": UA,
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "image/jpeg"
    }, data=image_bytes, timeout=60)
    r.raise_for_status()
    media = r.json()
    mid = media["id"]
    requests.post(f"{WP}/media/{mid}", headers=H,
                  data=json.dumps({"alt_text": alt_text}).encode(), timeout=30)
    return {"id": mid, "url": media["source_url"], "alt": alt_text}

# ---------------------------------------------------------------------------
# 2. Load + clean draft
# ---------------------------------------------------------------------------
raw = open(DRAFT, encoding="utf-8").read()
raw = re.sub(r'^---.*?---\s*', '', raw, flags=re.S)          # strip YAML frontmatter
raw = re.sub(r'```.*?```\s*', '', raw, flags=re.S)            # strip fenced SEO-metadata block
raw = re.sub(r'^#\s+.*\n', '', raw, count=1).strip()           # drop leading H1 (title set via post field)

def slugify(text):
    t = re.sub(r'<[^>]+>', '', text).lower().strip()
    t = re.sub(r"[^a-z0-9\s-]", "", t)
    t = re.sub(r"\s+", "-", t).strip("-")
    return t

def md_table_to_html(block):
    rows = [r.strip() for r in block.strip().split("\n") if r.strip()]
    rows = [r for r in rows if not re.match(r'^\|[\s:|-]+\|$', r)]  # drop separator row
    cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
    head, body = cells[0], cells[1:]
    th = "".join(f'<th style="background:#1a1a2e;color:#ffffff;padding:10px 14px;text-align:left;">{h}</th>' for h in head)
    trs = []
    for i, row in enumerate(body):
        bg = "#f0f4ff" if i % 2 == 0 else "#ffffff"
        tds = "".join(f'<td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">{c}</td>' for c in row)
        trs.append(f'<tr style="background:{bg};">{tds}</tr>')
    return ('<div style="overflow-x:auto;margin:8px 0;"><table style="border-collapse:collapse;width:100%;font-size:15px;">'
            f'<thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>')

# Line-based converter: handles ## / ### headings, blank-line paragraphs,
# a raw <ul>...</ul> block (the TOC, already HTML in the draft), and a
# markdown pipe-table block (the protocol comparison table).
lines = raw.split("\n")
html_out = []
para = []
i = 0

def flush_para():
    if para:
        text = " ".join(x.strip() for x in para if x.strip())
        if text:
            html_out.append(f"<p>{text}</p>")
        para.clear()

while i < len(lines):
    line = lines[i]
    s = line.strip()
    if s.startswith("<ul>"):
        flush_para()
        buf = [line]
        i += 1
        while i < len(lines) and "</ul>" not in lines[i]:
            buf.append(lines[i]); i += 1
        if i < len(lines):
            buf.append(lines[i]); i += 1
        html_out.append("\n".join(buf))
        continue
    if s.startswith("|"):
        flush_para()
        buf = [line]
        i += 1
        while i < len(lines) and lines[i].strip().startswith("|"):
            buf.append(lines[i]); i += 1
        html_out.append(md_table_to_html("\n".join(buf)))
        continue
    if s.startswith("### "):
        flush_para(); html_out.append(f"<h3>{s[4:].strip()}</h3>"); i += 1; continue
    if s.startswith("## "):
        flush_para(); html_out.append(f"<h2>{s[3:].strip()}</h2>"); i += 1; continue
    if s == "":
        flush_para(); i += 1; continue
    para.append(s); i += 1
flush_para()
content_html = "\n".join(html_out)

# ---------------------------------------------------------------------------
# 3. Blocking live-link + slug checks
# NOTE: already performed manually via WebFetch for this task (see summary).
# One dead link found and fixed in the draft before this script was written:
# /product-information-management-software/ (post 1538 is still WP-draft-only,
# 404s publicly) -> replaced with a second, differently-anchored link to the
# live /what-is-a-b2b-catalog-chatbot/ page. Re-run this block anyway before
# any real push, in case site state changed since.
# ---------------------------------------------------------------------------
# Catch BOTH absolute chatsku.com links and relative "/path/" links. The draft
# uses relative hrefs (house rule: no target attr on internal links), so an
# absolute-only regex matches nothing and this check passes vacuously.
_abs = re.findall(r'href="(https://chatsku\.com/[^"#]+)"', content_html)
_rel = ["https://chatsku.com" + p for p in re.findall(r'href="(/[^"#]*)"', content_html)]
hrefs = sorted(set(_abs + _rel))
if not hrefs:
    print("BLOCKING: link checker found 0 internal links. Regex is broken or the")
    print("draft has no internal links. Both are failures. Not pushing.")
    raise SystemExit(1)
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
    print("BLOCKING: bad internal links:")
    [print("  ", *b) for b in bad]
    raise SystemExit(1)
print("  all internal links 200 OK")

sr = requests.get(f"{WP}/posts", params={"slug": SLUG}, headers=HG, timeout=30)
if sr.status_code == 200 and sr.json():
    print("BLOCKING: a post with this slug already exists:", sr.json())
    raise SystemExit(1)
print("  slug is free")

# ---------------------------------------------------------------------------
# 4. Elementor helpers (mirrors build_elementor_post186_v3.py / post 96)
# ---------------------------------------------------------------------------
def gid(): return secrets.token_hex(4)

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
    html = re.sub(r'<img[^>]*?>', '', html).strip()
    if dark:
        html = re.sub(r'<p([ >])',
                       r'<p style="color:#aaaacc;text-align:center;font-size:18px;max-width:720px;margin:0 auto 14px auto;"\1',
                       html)
    return {"id": gid(), "elType": "widget", "widgetType": "text-editor", "elements": [],
            "settings": {"editor": html}}

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

# ---------------------------------------------------------------------------
# 5. Parse draft into sections (order preserved exactly as authored)
# ---------------------------------------------------------------------------
parts = [p.strip() for p in re.split(r'(?=<h2>)', content_html) if p.strip()]
parsed = []
for chunk in parts:
    m = re.match(r'<h2>(.*?)</h2>(.*)', chunk, re.S)
    if not m:
        continue
    title = m.group(1).strip(); body = m.group(2).strip()
    label = re.sub(r'<[^>]+>', '', title).lower().strip()
    if label == "executive summary":
        parsed.append(("exec", title, body))
    elif label == "table of contents":
        parsed.append(("toc", title, body))
    elif label == "introduction":
        parsed.append(("intro", title, body))
    elif label == "people also ask":
        parsed.append(("paa", title, body))
    elif label == "conclusion":
        parsed.append(("concl", title, body))
    elif label == "frequently asked questions":
        parsed.append(("faq", title, body))
    else:
        parsed.append(("body", title, body))

def split_qa(body):
    out = []
    for sp in re.split(r'(?=<h3>)', body.strip()):
        sp = sp.strip()
        hm = re.match(r'<h3>(.*?)</h3>(.*)', sp, re.S)
        if hm:
            out.append((hm.group(1).strip(), hm.group(2).strip()))
    return out

BODY_COLORS = ["#f0f4ff", "#ffffff", "#f9f9fb", "#ffffff"]
sections = []
ci = 0
body_n = 0
faq_pairs = []

FEATURED = BODY1 = BODY2 = None  # populated after sourcing, referenced below

def build_sections():
    global ci, body_n, faq_pairs
    out = []
    ci = 0; body_n = 0
    for kind, title, body in parsed:
        eid = slugify(title)
        if kind == "exec":
            out.append(section([w_heading(title), w_text(body)], "#f9f9fb"))
        elif kind == "toc":
            # Plain TOC per MUST-FOLLOW-RULES section 4: no !important, no SVG
            # arrows -- the raw <ul><li><a href="#anchor"> already in the draft.
            out.append(section([w_heading(title), w_text(body)], "#ffffff"))
        elif kind == "intro":
            out.append(section([w_heading(title, element_id=eid), w_text(body)], "#ffffff"))
        elif kind == "body":
            body_n += 1
            bg = BODY_COLORS[ci % len(BODY_COLORS)]; ci += 1
            widgets = [w_heading(title, element_id=eid), w_text(body)]
            if body_n == 1 and BODY1:
                widgets.append(w_image(BODY1))
            elif body_n == 4 and BODY2:
                widgets.append(w_image(BODY2))
            out.append(section(widgets, bg))
        elif kind == "paa":
            bg = BODY_COLORS[ci % len(BODY_COLORS)]; ci += 1
            widgets = [w_heading(title, element_id=eid)]
            for q, a in split_qa(body):
                widgets.append(w_heading(q, "h3")); widgets.append(w_text(a))
            out.append(section(widgets, bg))
        elif kind == "concl":
            widgets = [w_heading(title, color="#ffffff", align="center", element_id=eid), w_text(body, dark=True),
                       w_button("Talk to ChatSKU about your catalog", "https://chatsku.com/demo/")]
            out.append(section(widgets, "#1a1a2e", conclusion=True))
        elif kind == "faq":
            faq_pairs = split_qa(body)
            widgets = [w_heading(title, element_id=eid), w_accordion(faq_pairs)]
            schema = {"@context": "https://schema.org", "@graph": [
                {"@type": "Article", "headline": TITLE, "description": YOAST_DESC,
                 "image": (FEATURED or {}).get("url", ""), "datePublished": PUBLISH_DATE, "dateModified": PUBLISH_DATE,
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
            out.append(section(widgets, "#f9f9fb"))
    return out

sections = build_sections()
print(f"Parsed {len(parsed)} H2 sections -> {len(sections)} Elementor sections | FAQ tabs {len(faq_pairs)}")

# ---------------------------------------------------------------------------
# 6. Source + upload images, then rebuild sections with image widgets
# ---------------------------------------------------------------------------
DRY_RUN = "publish" not in sys.argv

# Pre-QA'd images. The auto-picker takes the first image that downloads and
# resizes cleanly, which is exactly how generic mismatched stock gets shipped
# (see feedback_image_visual_qa). If QA_DIR holds final_{slot}.jpg files that
# were visually reviewed, use those and skip auto-sourcing entirely.
QA_DIR = os.environ.get("QA_DIR", "")

def get_image(slot):
    if QA_DIR:
        p = os.path.join(QA_DIR, f"final_{slot}.jpg")
        if os.path.exists(p):
            from PIL import Image as _I
            with open(p, "rb") as fh:
                data = fh.read()
            w, h = _I.open(io.BytesIO(data)).size
            if (w, h) != (860, 452):
                print(f"BLOCKING: {p} is {w}x{h}, expected 860x452."); raise SystemExit(1)
            print(f"  using pre-QA'd {slot}: {p} ({w}x{h}, {len(data)//1024} KB)")
            return data, f"local:{p}"
    return source_image(slot)

if not DRY_RUN:
    print("Sourcing featured image...")
    fb, fu = get_image("featured")
    if not fb:
        print("BLOCKING: could not source a featured image."); raise SystemExit(1)
    print("  source:", fu)
    FEATURED = upload_media(fb, "chatsku-agentic-commerce-glossary-featured.jpg",
        "Sales team reviewing an agentic commerce vendor question in a B2B manufacturer office")

    print("Sourcing body image 1 (protocols section)...")
    b1, u1 = get_image("body1")
    if b1:
        print("  source:", u1)
        BODY1 = upload_media(b1, "chatsku-agentic-commerce-glossary-body1.jpg",
            "Two colleagues comparing agentic commerce protocol notes and laptop research at a B2B office desk")

    print("Sourcing body image 2 (data standards section)...")
    b2, u2 = get_image("body2")
    if b2:
        print("  source:", u2)
        BODY2 = upload_media(b2, "chatsku-agentic-commerce-glossary-body2.jpg",
            "Manufacturer catalog and SKU data reviewed on a computer screen for GTIN and UNSPSC readiness")

    sections = build_sections()

elementor_json = json.dumps(sections)
content_fallback = re.sub(r'<img[^>]*?>', '', content_html)  # no bare <img> in content field

print(f"\nBuilt {len(sections)} sections | elementor {len(elementor_json):,} chars")
open(os.path.join(SCRATCH, "agentic_commerce_glossary_elementor.json"), "w", encoding="utf-8").write(elementor_json)

if DRY_RUN:
    print("\nDRY RUN. Image sourcing/upload skipped. Pass 'publish' as argv to run for real.")
    print("Prerequisites before running with 'publish': requests, Pillow installed; "
          "CHATSKU_WP_USERNAME / CHATSKU_WP_APP_PASSWORD set; network access to "
          "chatsku.com, api.pexels.com (optional), api.openverse.org, commons.wikimedia.org.")
    raise SystemExit(0)

if not FEATURED:
    print("BLOCKING: featured_media could not be sourced. Refusing to push with featured_media=0.")
    raise SystemExit(1)

# ---------------------------------------------------------------------------
# 7. Push post as draft + clear Elementor cache
# ---------------------------------------------------------------------------
payload = {
    "title": TITLE, "slug": SLUG, "status": "draft", "content": content_fallback,
    "excerpt": YOAST_DESC, "featured_media": FEATURED["id"], "categories": [29],
    "meta": {"_elementor_edit_mode": "builder", "_elementor_template_type": "wp-post",
              "_elementor_data": elementor_json,
              "_yoast_wpseo_title": YOAST_TITLE, "_yoast_wpseo_metadesc": YOAST_DESC}
    # NOTE: yoast meta IS attempted via REST here (per posts 1880/2044 findings
    # that it now persists on chatsku.com) but verify with context=edit after
    # push, and set manually in WP Admin if it did not persist.
}

r = requests.post(f"{WP}/posts", headers=H, data=json.dumps(payload).encode(), timeout=120)
print("POST status:", r.status_code)
if r.status_code not in (200, 201):
    print(r.text[:1500]); raise SystemExit(1)
j = r.json(); pid = j["id"]
print("POST_ID:", pid, "| status:", j["status"], "| link:", j.get("link"))

cc = requests.delete("https://chatsku.com/wp-json/elementor/v1/cache", headers=H, timeout=60)
print("Elementor cache clear:", cc.status_code)

json.dump({"id": pid, "link": j.get("link"), "slug": j.get("slug"),
           "featured_media": FEATURED["id"], "body1_media": (BODY1 or {}).get("id"),
           "body2_media": (BODY2 or {}).get("id")},
          open(os.path.join(SCRATCH, "agentic_commerce_glossary_result.json"), "w"))
print("\nDone. Verify featured_media, body image widget order, TOC anchor IDs "
      "resolve, table renders styled (not bare HTML), and Yoast fields persisted "
      "(check context=edit; set manually in WP Admin if not) before treating "
      "this post as fully checklist-complete.")
