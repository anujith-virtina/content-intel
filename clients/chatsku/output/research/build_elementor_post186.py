"""
Build proper Elementor _elementor_data structure for post 186
and push it via the WordPress REST API so it renders like post 151.
"""
import json, secrets, re, urllib.request, urllib.error, base64

WP_BASE = "https://chatsku.com/wp-json/wp/v2"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
AUTH = base64.b64encode(b"admin:fL5q VbD3 20Nt sOjx 86wb 94iS").decode()
HEADERS = {"Authorization": f"Basic {AUTH}", "User-Agent": UA, "Content-Type": "application/json"}

# Media info (uploaded in Stage 4)
IMAGES = {
    "featured": {"id": 183, "url": "https://chatsku.com/wp-content/uploads/2026/05/chatsku-after-hours-featured.jpg",
                 "alt": "B2B buyer working late at night on laptop researching products, representing after-hours purchasing behavior"},
    "body1":    {"id": 184, "url": "https://chatsku.com/wp-content/uploads/2026/05/chatsku-after-hours-body1.jpg",
                 "alt": "B2B business professional at computer researching product options, representing buyer self-service research behavior outside business hours"},
    "body2":    {"id": 185, "url": "https://chatsku.com/wp-content/uploads/2026/05/chatsku-after-hours-body2.jpg",
                 "alt": "B2B sales team reviewing catalog data and pricing on computer screens, showing B2B catalog query complexity and customer group pricing"},
}

def gid(): return secrets.token_hex(4)

def section(widgets, bg="#f9f9fb"):
    return {"id": gid(), "elType": "section", "isInner": False,
            "settings": {"background_background": "classic", "background_color": bg,
                         "padding": {"top": "20", "bottom": "20", "right": "15", "left": "15", "unit": "px"}},
            "elements": [{"id": gid(), "elType": "column", "isInner": False,
                          "settings": {"_column_size": 100, "width": "100"},
                          "elements": widgets}]}

def heading(title, level="h2"):
    size = 28 if level == "h2" else 22
    s = {"title": title, "align": "left", "title_color": "#1a1a2e",
         "typography_font_size": {"size": size, "unit": "px"}}
    if level != "h2":
        s["header_size"] = level
    return {"id": gid(), "elType": "widget", "widgetType": "heading", "elements": [], "settings": s}

def text_editor(html):
    # Fix relative URLs to absolute
    html = re.sub(r'href="/([\w/\-]+)"', r'href="https://chatsku.com/\1"', html)
    # Remove figure wrappers (images handled separately)
    html = re.sub(r'<figure[^>]*>.*?</figure>', '', html, flags=re.DOTALL).strip()
    return {"id": gid(), "elType": "widget", "widgetType": "text-editor", "elements": [],
            "settings": {"editor": html}}

def image_widget(img_key):
    img = IMAGES[img_key]
    return {"id": gid(), "elType": "widget", "widgetType": "image", "elements": [],
            "settings": {"image": {"id": img["id"], "url": img["url"], "alt": img["alt"],
                                   "source": "library", "size": ""},
                         "align": "center",
                         "width": {"size": 100, "unit": "%"},
                         "border_radius": {"top": "10", "right": "10", "bottom": "10", "left": "10", "unit": "px"}}}

# ── Fetch current post content ────────────────────────────────────────────────
req = urllib.request.Request(f"{WP_BASE}/posts/186?context=edit", headers=HEADERS)
with urllib.request.urlopen(req) as r:
    post = json.loads(r.read())
raw = post["content"]["raw"]

# ── Parse HTML into sections ──────────────────────────────────────────────────
# Split on H2 boundaries
parts = re.split(r'(?=<h2[^>]*>)', raw.strip())

def strip_h2(chunk):
    m = re.match(r'<h2[^>]*>(.*?)</h2>(.*)', chunk, re.DOTALL)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return None, chunk

elementor_sections = []

for chunk in parts:
    chunk = chunk.strip()
    if not chunk:
        continue

    h2_text, body = strip_h2(chunk)
    if not h2_text:
        continue

    # Check if this is People Also Ask or FAQ (contain H3 sub-items)
    has_h3 = bool(re.search(r'<h3', body))

    if h2_text.lower() in ("people also ask",):
        # PAA: H2 heading + (H3 + text-editor) pairs
        widgets = [heading(h2_text, "h2")]
        # Split body into H3+answer pairs
        sub_parts = re.split(r'(?=<h3[^>]*>)', body.strip())
        for sp in sub_parts:
            sp = sp.strip()
            if not sp: continue
            hm = re.match(r'<h3[^>]*>(.*?)</h3>(.*)', sp, re.DOTALL)
            if hm:
                widgets.append(heading(hm.group(1).strip(), "h3"))
                ans = hm.group(2).strip()
                if ans:
                    widgets.append(text_editor(ans))
        elementor_sections.append(section(widgets))

    elif h2_text.lower() in ("frequently asked questions",):
        # FAQ: H2 heading + (H3 + text-editor) pairs
        widgets = [heading(h2_text, "h2")]
        sub_parts = re.split(r'(?=<h3[^>]*>)', body.strip())
        for sp in sub_parts:
            sp = sp.strip()
            if not sp: continue
            hm = re.match(r'<h3[^>]*>(.*?)</h3>(.*)', sp, re.DOTALL)
            if hm:
                widgets.append(heading(hm.group(1).strip(), "h3"))
                ans = hm.group(2).strip()
                if ans:
                    widgets.append(text_editor(ans))
        elementor_sections.append(section(widgets))

    else:
        # Regular section: H2 heading + optional image + text-editor
        # Check for body images in this chunk (the figure tags)
        has_body1 = 'chatsku-after-hours-body1' in body
        has_body2 = 'chatsku-after-hours-body2' in body

        # Clean body of figure tags for text_editor
        clean_body = re.sub(r'<figure[^>]*>.*?</figure>', '', body, flags=re.DOTALL).strip()

        widgets = [heading(h2_text, "h2")]

        if has_body1:
            widgets.append(image_widget("body1"))
        elif has_body2:
            widgets.append(image_widget("body2"))

        if clean_body:
            widgets.append(text_editor(clean_body))

        elementor_sections.append(section(widgets))

print(f"Built {len(elementor_sections)} Elementor sections")
for i, s in enumerate(elementor_sections):
    widgets = s["elements"][0]["elements"]
    widget_types = [w.get("widgetType","?") + ("("+w["settings"].get("title","")[:30]+")" if w.get("widgetType")=="heading" else "") for w in widgets]
    print(f"  Section {i}: {' | '.join(widget_types)}")

# ── Build meta payload ────────────────────────────────────────────────────────
elementor_data_json = json.dumps(elementor_sections)

# Rebuild clean post_content from sections (standard fallback)
clean_content_parts = []
for s in elementor_sections:
    for widget in s["elements"][0]["elements"]:
        wt = widget.get("widgetType")
        if wt == "heading":
            lvl = widget["settings"].get("header_size", "h2")
            title = widget["settings"].get("title", "")
            clean_content_parts.append(f"<{lvl}>{title}</{lvl}>")
        elif wt == "text-editor":
            clean_content_parts.append(widget["settings"].get("editor", ""))
        elif wt == "image":
            img = widget["settings"]["image"]
            clean_content_parts.append(f'<img width="860" height="452" src="{img["url"]}" alt="{img["alt"]}" />')
clean_post_content = "\n\n".join(p for p in clean_content_parts if p.strip())

# ── Push to WordPress ─────────────────────────────────────────────────────────
payload = {
    "content": clean_post_content,
    "meta": {
        "_elementor_edit_mode": "builder",
        "_elementor_template_type": "wp-post",
        "_elementor_data": elementor_data_json,
    }
}

print(f"\nPushing to post 186...")
print(f"  Elementor data: {len(elementor_data_json)} chars ({len(elementor_sections)} sections)")

body_bytes = json.dumps(payload).encode()
req2 = urllib.request.Request(f"{WP_BASE}/posts/186", data=body_bytes, headers=HEADERS, method="POST")
try:
    with urllib.request.urlopen(req2) as r:
        resp = json.loads(r.read())
        print(f"  HTTP 200  status={resp.get('status')}  slug={resp.get('slug')}")
        meta_back = resp.get('meta', {})
        print(f"  _elementor_edit_mode: {meta_back.get('_elementor_edit_mode','NOT SET')}")
        print(f"  _elementor_data set: {bool(meta_back.get('_elementor_data',''))}")
except urllib.error.HTTPError as e:
    print(f"  HTTP ERROR {e.code}: {e.read()[:400]}")
    raise

# ── Verify ────────────────────────────────────────────────────────────────────
req3 = urllib.request.Request(f"{WP_BASE}/posts/186?context=edit", headers=HEADERS)
with urllib.request.urlopen(req3) as r:
    verified = json.loads(r.read())

meta_v = verified.get('meta', {})
edit_mode = meta_v.get('_elementor_edit_mode', '')
ed_data = meta_v.get('_elementor_data', '')
print(f"\nVerified:")
print(f"  _elementor_edit_mode: {edit_mode!r}")
print(f"  _elementor_data length: {len(ed_data)} chars")
print(f"  featured_media: {verified.get('featured_media')}")
print(f"  status: {verified.get('status')}")

if edit_mode == "builder" and len(ed_data) > 1000:
    print("\n[PASS] Elementor data set correctly — post will render like post 151")
else:
    print("\n[WARN] Elementor meta may not have been set — check WP dashboard")
    print("  Note: some WP configs protect _elementor_data from REST API writes.")
    print("  If not set, use the Elementor template import approach instead.")
