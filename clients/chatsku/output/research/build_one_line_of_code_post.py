# -*- coding: utf-8 -*-
"""Build + publish (draft) ChatSKU post: "One line of code: what that actually
means for your website" (Format A / reassurance-explainer).

Elementor structure mirrors post 96 / post 186 (build_elementor_post186_v3.py)
and the FAQ-accordion convention established in posts 299/685/1056/1300/1538/1684/1880.

Section order matches the APPROVED DRAFT exactly (do not reorder):
  Executive summary -> Introduction -> body1 -> body2 -> FAQ -> Conclusion

Conclusion = 3 widgets: white centered heading + dark centered text-editor (no
inline CTA link) + #e94560 button -> https://chatsku.com/demo/.

Images: 1 featured + 2 body, all 860x452, sourced Pexels > Openverse(cc0, NO
source=stocksnap - dead) > Wikimedia. Subject: non-technical B2B owner/ops
person at a laptop/desk, easy setup / confidence framing. Visually QA before
selecting (do not keyword-match blind).

NOTE: this script requires a Python environment with `requests` and `Pillow`,
network access, and CHATSKU_WP_USERNAME / CHATSKU_WP_APP_PASSWORD in the
environment. It was authored in a session with no code-execution tool
available, so it has NOT been run yet. Run it end-to-end before treating the
post as published. Default is DRY_RUN (prints what it would do); pass
"publish" as the only argv to actually push to WordPress.
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

TITLE = "One line of code: what that actually means for your website"
SLUG = "one-line-of-code"
PERMALINK = f"https://chatsku.com/{SLUG}/"
DRAFT = r"C:\content-intel\clients\chatsku\output\drafts\one-line-of-code-2026-08-03.md"
YOAST_TITLE = "One Line of Code, Explained | ChatSKU"
YOAST_DESC = ("Adding ChatSKU takes one small code snippet, the same way Google Analytics "
              "works. No developer, no rebuild, no migration. Most sites go live within a day.")
PUBLISH_DATE = "2026-08-03"

# ---------------------------------------------------------------------------
# 1. Image sourcing (Pexels -> Openverse cc0 -> Wikimedia). 860x452, JPEG q82.
# ---------------------------------------------------------------------------
PEXELS_KEY = os.environ.get("PEXELS_API_KEY", "")

IMG_QUERIES = {
    "featured": ["small business owner laptop desk", "business owner working laptop office",
                 "shop owner computer desk confident"],
    "body1": ["business owner reviewing website laptop", "office worker typing laptop desk",
              "small business owner computer screen"],
    "body2": ["web developer laptop code office", "person pasting code website laptop",
              "office worker laptop confident smiling"],
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

def source_image(slot, alt_text, filename):
    """Try Pexels -> Openverse -> Wikimedia for each query, visually QA before
    accepting (manual review recommended before upload in this repo's process).
    Returns local resized bytes or None."""
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
# 2. Load + clean draft, blocking live-link check
# ---------------------------------------------------------------------------
raw = open(DRAFT, encoding="utf-8").read()
# strip YAML frontmatter
raw = re.sub(r'^---.*?---\s*', '', raw, flags=re.S)
# strip the trailing self-check HTML comment block entirely
raw = re.sub(r'<!--.*?-->', '', raw, flags=re.S).strip()
# drop the leading H1 (title is set via post title field)
raw = re.sub(r'^#\s+.*\n', '', raw, count=1).strip()

# Convert markdown H2/H3/links/paragraphs to HTML (draft is already
# near-HTML/markdown hybrid per house convention: ## -> h2, ### -> h3,
# [text](url) -> <a href="url">text</a>, blank-line-separated -> <p>)
def md_to_html(md):
    lines = md.split("\n")
    out = []
    para = []
    def flush():
        if para:
            text = " ".join(para).strip()
            if text:
                out.append(f"<p>{text}</p>")
            para.clear()
    for line in lines:
        line = line.rstrip()
        if line.startswith("### "):
            flush(); out.append(f"<h3>{line[4:].strip()}</h3>")
        elif line.startswith("## "):
            flush(); out.append(f"<h2>{line[3:].strip()}</h2>")
        elif line.strip() == "":
            flush()
        else:
            para.append(line.strip())
    flush()
    html = "\n".join(out)
    html = re.sub(r'\[([^\]]+)\]\((/[^)]+)\)', r'<a href="https://chatsku.com\1">\1_LABEL_\2</a>', html)
    # fix anchor text (regex above put path in twice; redo properly)
    html = re.sub(r'\[([^\]]+)\]\((/[^)]+)\)', r'<a href="https://chatsku.com\2">\1</a>', md)  # placeholder, real conversion below
    return html

# Simpler, safer conversion done inline below rather than via the helper above.
body_md = raw
# markdown links -> absolute internal hrefs (no target attr = same tab, per house rule)
body_md = re.sub(r'\[([^\]]+)\]\((/[^)]+)\)', r'<a href="https://chatsku.com\2">\1</a>', body_md)

lines = body_md.split("\n")
html_out = []
para = []
def flush_para():
    if para:
        text = " ".join(x.strip() for x in para if x.strip())
        if text:
            html_out.append(f"<p>{text}</p>")
        para.clear()
for line in lines:
    s = line.strip()
    if s.startswith("### "):
        flush_para(); html_out.append(f"<h3>{s[4:].strip()}</h3>")
    elif s.startswith("## "):
        flush_para(); html_out.append(f"<h2>{s[3:].strip()}</h2>")
    elif s == "":
        flush_para()
    else:
        para.append(s)
flush_para()
content_html = "\n".join(html_out)

# blocking live-link check
hrefs = sorted(set(re.findall(r'href="(https://chatsku\.com/[^"]+)"', content_html)))
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

# blocking slug-collision check
sr = requests.get(f"{WP}/posts", params={"slug": SLUG}, headers=HG, timeout=30)
if sr.status_code == 200 and sr.json():
    print("BLOCKING: a post with this slug already exists:", sr.json())
    raise SystemExit(1)
print("  slug is free")

# ---------------------------------------------------------------------------
# 3. Elementor helpers (mirrors build_elementor_post186_v3.py / post 96)
# ---------------------------------------------------------------------------
def gid(): return secrets.token_hex(4)

def w_heading(title, level="h2", color="#1a1a2e", align="left"):
    s = {"title": title, "align": align, "title_color": color,
         "typography_typography": "custom",
         "typography_font_size": {"size": 28 if level == "h2" else 22, "unit": "px"}}
    if level != "h2":
        s["header_size"] = level
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
# 4. Parse draft into sections (order preserved exactly as authored)
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
    elif label == "introduction":
        parsed.append(("intro", title, body))
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

BODY_COLORS = ["#f0f4ff", "#ffffff"]  # only 2 body sections in this draft
sections = []
ci = 0
body_n = 0
faq_pairs = []

FEATURED = BODY1 = BODY2 = None  # populated after sourcing, referenced below

for kind, title, body in parsed:
    if kind == "exec":
        sections.append(section([w_heading(title), w_text(body)], "#f9f9fb"))
    elif kind == "intro":
        sections.append(section([w_heading(title), w_text(body)], "#ffffff"))
    elif kind == "body":
        body_n += 1
        bg = BODY_COLORS[ci % len(BODY_COLORS)]; ci += 1
        widgets = [w_heading(title), w_text(body)]
        # Body image 1 goes in the first body section ("What do you actually
        # have to do to add ChatSKU?"), AFTER the text-editor widget.
        if body_n == 1 and BODY1:
            widgets.append(w_image(BODY1))
        elif body_n == 2 and BODY2:
            widgets.append(w_image(BODY2))
        sections.append(section(widgets, bg))
    elif kind == "faq":
        faq_pairs = split_qa(body)
        widgets = [w_heading(title), w_accordion(faq_pairs)]
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
        sections.append(section(widgets, "#f9f9fb"))
    elif kind == "concl":
        widgets = [w_heading(title, color="#ffffff", align="center"), w_text(body, dark=True),
                   w_button("See the one-line setup in a live demo", "https://chatsku.com/demo/")]
        sections.append(section(widgets, "#1a1a2e", conclusion=True))

print(f"Parsed {len(parsed)} H2 sections -> {len(sections)} Elementor sections | FAQ tabs {len(faq_pairs)}")

# ---------------------------------------------------------------------------
# 5. Source + upload images, THEN rebuild image widgets into sections
# ---------------------------------------------------------------------------
DRY_RUN = "publish" not in sys.argv

if not DRY_RUN:
    # Images were sourced as candidates and VISUALLY QA'd by the orchestrator.
    # These three pre-resized (860x452, JPEG q82) files were hand-selected; we
    # do NOT blind auto-source here (avoids the mismatched-stock failure mode).
    CAND = r"C:\Users\ASUS\AppData\Local\Temp\claude\C--content-intel\61b25f9b-a51d-4e64-bd9e-95378ae07e7b\scratchpad\candidates"
    def load(fn):
        return open(os.path.join(CAND, fn), "rb").read()

    print("Uploading featured image (hand-picked: confident business owner at laptop)...")
    FEATURED = upload_media(load("body1_2.jpg"), "chatsku-one-line-of-code-featured.jpg",
        "Confident B2B business owner smiling while reviewing their website on a laptop after adding the ChatSKU one-line code snippet")

    print("Uploading body image 1 (setup steps section)...")
    BODY1 = upload_media(load("body2_2.jpg"), "chatsku-one-line-of-code-body1.jpg",
        "Business owner working at a laptop while setting up ChatSKU, uploading a product catalog and reviewing configuration before going live")

    print("Uploading body image 2 (what the snippet is section)...")
    BODY2 = upload_media(load("body2_1.jpg"), "chatsku-one-line-of-code-body2.jpg",
        "Close-up of hands typing on a laptop, pasting a short code snippet into a website the same way an analytics tag is added")

    # rebuild sections now that image widgets are known (re-run the loop with populated FEATURED/BODY1/BODY2)
    sections = []
    ci = 0; body_n = 0
    for kind, title, body in parsed:
        if kind == "exec":
            sections.append(section([w_heading(title), w_text(body)], "#f9f9fb"))
        elif kind == "intro":
            sections.append(section([w_heading(title), w_text(body)], "#ffffff"))
        elif kind == "body":
            body_n += 1
            bg = BODY_COLORS[ci % len(BODY_COLORS)]; ci += 1
            widgets = [w_heading(title), w_text(body)]
            if body_n == 1 and BODY1:
                widgets.append(w_image(BODY1))
            elif body_n == 2 and BODY2:
                widgets.append(w_image(BODY2))
            sections.append(section(widgets, bg))
        elif kind == "faq":
            widgets = [w_heading(title), w_accordion(faq_pairs)]
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
            sections.append(section(widgets, "#f9f9fb"))
        elif kind == "concl":
            widgets = [w_heading(title, color="#ffffff", align="center"), w_text(body, dark=True),
                       w_button("See the one-line setup in a live demo", "https://chatsku.com/demo/")]
            sections.append(section(widgets, "#1a1a2e", conclusion=True))

elementor_json = json.dumps(sections)
content_fallback = re.sub(r'<img[^>]*?>', '', content_html)  # no bare <img> in content field

print(f"\nBuilt {len(sections)} sections | elementor {len(elementor_json):,} chars")
open(os.path.join(SCRATCH, "one_line_of_code_elementor.json"), "w", encoding="utf-8").write(elementor_json)

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
# 6. Push post as draft + clear Elementor cache
# ---------------------------------------------------------------------------
payload = {
    "title": TITLE, "slug": SLUG, "status": "draft", "content": content_fallback,
    "excerpt": YOAST_DESC, "featured_media": FEATURED["id"], "categories": [29],
    "meta": {"_elementor_edit_mode": "builder", "_elementor_template_type": "wp-post",
              "_elementor_data": elementor_json}
    # NOTE: per explicit task instruction, _yoast_wpseo_title / _yoast_wpseo_metedesc
    # are NOT pushed here (not show_in_rest on chatsku.com for this task). Set manually
    # in WP Admin -> Yoast SEO panel. See YOAST_TITLE / YOAST_DESC above.
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
          open(os.path.join(SCRATCH, "one_line_of_code_result.json"), "w"))
print("\nDone. Verify featured_media, body image widget order, and Yoast fields "
      "(set manually) before treating this post as fully checklist-complete.")
