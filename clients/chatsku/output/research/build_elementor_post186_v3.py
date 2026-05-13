"""
Rebuild post 186 Elementor data matching post 96 (b2b-ecommerce-chatbot-dallas) EXACTLY.

Verified from post 96:
  - Section padding: top/bottom 60px, NO left/right (0px or omitted)
  - Column inner padding: {top:20, right:20, bottom:20, left:20, isLinked:true, unit:px}
  - Color sequence: #f9f9fb -> #ffffff -> #f0f4ff -> #ffffff -> #f9f9fb -> #ffffff -> #f0f4ff -> ...
  - Conclusion: #1a1a2e, heading white, body #aaaacc centered
  - FAQ: #f9f9fb

Post 96 section structure (JSON exact):
  section.settings = {
    background_background: "classic",
    background_color: "<color>",
    padding: {top:"60", bottom:"60", unit:"px"}   <- no right/left keys
  }
  column.settings = {
    _column_size: 100,
    width: "100",
    padding: {unit:"px", top:"20", right:"20", bottom:"20", left:"20", isLinked:true}
  }
"""
import json, secrets, re, urllib.request, urllib.error, base64, os

WP_BASE = "https://chatsku.com/wp-json/wp/v2"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
USERNAME = os.environ.get("CHATSKU_WP_USERNAME", "admin")
PASSWORD = os.environ.get("CHATSKU_WP_APP_PASSWORD", "fL5q VbD3 20Nt sOjx 86wb 94iS")
AUTH = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
HEADERS = {"Authorization": f"Basic {AUTH}", "User-Agent": UA, "Content-Type": "application/json"}

IMAGES = {
    "body1": {"id": 184, "url": "https://chatsku.com/wp-content/uploads/2026/05/chatsku-after-hours-body1.jpg",
              "alt": "B2B business professional at computer researching product options, representing buyer self-service research behavior outside business hours"},
    "body2": {"id": 185, "url": "https://chatsku.com/wp-content/uploads/2026/05/chatsku-after-hours-body2.jpg",
              "alt": "B2B sales team reviewing catalog data and pricing on computer screens, showing B2B catalog query complexity and customer group pricing"},
}

def gid():
    return secrets.token_hex(4)

def make_button(text, url):
    return {
        "id": gid(), "elType": "widget", "widgetType": "button", "elements": [],
        "settings": {
            "text": text,
            "link": {"url": url, "is_external": "true"},
            "align": "center",
            "background_color": "#e94560",
            "button_text_color": "#ffffff",
            "border_radius": {"size": 6, "unit": "px"},
            "_margin": {"unit": "px", "top": "20", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
        }
    }

def make_section(widgets, bg, is_conclusion=False):
    """Build section matching post 96 structure exactly."""
    if is_conclusion:
        # Conclusion: top:20 bottom:30 right:0 left:0 — exact match to post 96
        section_padding = {"top": "20", "bottom": "30", "unit": "px", "right": "0", "left": "0"}
    else:
        # All other sections: 60px top/bottom, NO left/right keys
        section_padding = {"top": "60", "bottom": "60", "unit": "px"}

    # Column has its own 20px inner padding on all sides
    column_padding = {"unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20", "isLinked": True}

    return {
        "id": gid(),
        "elType": "section",
        "isInner": False,
        "settings": {
            "background_background": "classic",
            "background_color": bg,
            "padding": section_padding
        },
        "elements": [{
            "id": gid(),
            "elType": "column",
            "isInner": False,
            "settings": {
                "_column_size": 100,
                "width": "100",
                "padding": column_padding
            },
            "elements": widgets
        }]
    }

def make_heading(title, level="h2", color="#1a1a2e", align="left"):
    size = 28 if level == "h2" else 22
    s = {
        "title": title,
        "align": align,
        "title_color": color,
        "typography_font_size": {"size": size, "unit": "px"}
    }
    if level != "h2":
        s["header_size"] = level
    return {"id": gid(), "elType": "widget", "widgetType": "heading", "elements": [], "settings": s}

def make_text(html, dark_section=False):
    html = re.sub(r'href="/([\w/\-]+)"', r'href="https://chatsku.com/\1"', html)
    html = re.sub(r'<figure[^>]*>.*?</figure>', '', html, flags=re.DOTALL).strip()
    # Strip bare <img> tags — images are rendered via explicit Elementor image widgets
    html = re.sub(r'<img[^>]*/>', '', html).strip()
    html = re.sub(r'<img[^>]*></img>', '', html).strip()
    if dark_section:
        html = re.sub(
            r'<p([ >])',
            r'<p style="color:#aaaacc;text-align:center;font-size:18px;max-width:720px;margin:0 auto;"\1',
            html
        )
    return {"id": gid(), "elType": "widget", "widgetType": "text-editor", "elements": [],
            "settings": {"editor": html}}

def make_image(key):
    img = IMAGES[key]
    return {
        "id": gid(), "elType": "widget", "widgetType": "image", "elements": [],
        "settings": {
            "image": {"id": img["id"], "url": img["url"], "alt": img["alt"], "source": "library", "size": ""},
            "align": "center",
            "width": {"size": 100, "unit": "%"},
            "border_radius": {"top": "10", "right": "10", "bottom": "10", "left": "10", "unit": "px"}
        }
    }

def strip_h2(chunk):
    m = re.match(r'<h2[^>]*>(.*?)</h2>(.*)', chunk, re.DOTALL)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return None, chunk

# ── Fetch post content ────────────────────────────────────────────────────────
print("Fetching post 186 content...")
req = urllib.request.Request(f"{WP_BASE}/posts/186?context=edit", headers=HEADERS)
with urllib.request.urlopen(req) as r:
    post = json.loads(r.read())
raw = post["content"]["raw"]
print(f"  Content: {len(raw)} chars")

# ── Parse sections ────────────────────────────────────────────────────────────
parts = [p.strip() for p in re.split(r'(?=<h2[^>]*>)', raw.strip()) if p.strip()]
print(f"  Found {len(parts)} H2 sections")

parsed = []
for chunk in parts:
    h2_text, body = strip_h2(chunk)
    if not h2_text:
        continue
    label = h2_text.lower().strip()
    has_body1 = 'chatsku-after-hours-body1' in body
    has_body2 = 'chatsku-after-hours-body2' in body
    clean_body = re.sub(r'<figure[^>]*>.*?</figure>', '', body, flags=re.DOTALL).strip()
    clean_body = re.sub(r'<img[^>]*/>', '', clean_body).strip()

    # Image assignment: match by heading keywords since img tags were stripped from content
    BODY1_KEYWORDS = ["dead end after hours", "after-hours-body1"]
    BODY2_KEYWORDS = ["catalog-aware ai assistant", "after-hours-body2"]
    img_key = None
    if any(kw in label for kw in BODY1_KEYWORDS) or has_body1:
        img_key = "body1"
    elif any(kw in label for kw in BODY2_KEYWORDS) or has_body2:
        img_key = "body2"

    if label == "executive summary":
        parsed.append(("exec_summary", h2_text, clean_body, None))
    elif label == "introduction":
        parsed.append(("introduction", h2_text, clean_body, None))
    elif label == "people also ask":
        parsed.append(("paa", h2_text, body, None))
    elif label == "conclusion":
        parsed.append(("conclusion", h2_text, clean_body, None))
    elif label == "frequently asked questions":
        parsed.append(("faq", h2_text, body, None))
    else:
        parsed.append(("body", h2_text, clean_body, img_key))

print(f"\nParsed {len(parsed)} sections:")
for kind, title, _, img in parsed:
    print(f"  [{kind:12}] {title[:50]}" + (f" + IMG({img})" if img else ""))

# ── Color sequence (matches post 96 pattern) ─────────────────────────────────
# Post 96 verified sequence: f9f9fb, ffffff, f0f4ff, ffffff, f9f9fb, ffffff, f0f4ff, 1a1a2e, f9f9fb
# Pattern for body sections: cycle through [#f9f9fb, #ffffff, #f0f4ff, #ffffff]
# Exec Summary always #f9f9fb, Introduction always #ffffff
# Conclusion always #1a1a2e, FAQ always #f9f9fb
BODY_COLORS = ["#f9f9fb", "#ffffff", "#f0f4ff", "#ffffff"]

# ── Build Elementor sections ──────────────────────────────────────────────────
elementor_sections = []
body_color_idx = 0  # starts at #f9f9fb (post 96 body 1 is #f0f4ff, index 2 in cycle)

# Looking at post 96: after intro (#ffffff), body sections go #f0f4ff, #ffffff, #f9f9fb, #ffffff, #f0f4ff
# So body color index starts at 2 (f0f4ff)
body_color_idx = 2

for kind, h2_text, body, img_key in parsed:

    if kind == "exec_summary":
        widgets = [make_heading(h2_text), make_text(body)]
        elementor_sections.append(make_section(widgets, bg="#f9f9fb"))

    elif kind == "introduction":
        widgets = [make_heading(h2_text), make_text(body)]
        elementor_sections.append(make_section(widgets, bg="#ffffff"))

    elif kind == "body":
        bg = BODY_COLORS[body_color_idx % len(BODY_COLORS)]
        body_color_idx += 1
        widgets = [make_heading(h2_text)]
        if body:
            widgets.append(make_text(body))
        if img_key:
            widgets.append(make_image(img_key))
        elementor_sections.append(make_section(widgets, bg=bg))

    elif kind == "paa":
        bg = BODY_COLORS[body_color_idx % len(BODY_COLORS)]
        body_color_idx += 1
        widgets = [make_heading(h2_text)]
        sub_parts = re.split(r'(?=<h3[^>]*>)', body.strip())
        for sp in sub_parts:
            sp = sp.strip()
            if not sp:
                continue
            hm = re.match(r'<h3[^>]*>(.*?)</h3>(.*)', sp, re.DOTALL)
            if hm:
                widgets.append(make_heading(hm.group(1).strip(), "h3"))
                ans = hm.group(2).strip()
                if ans:
                    widgets.append(make_text(ans))
        elementor_sections.append(make_section(widgets, bg=bg))

    elif kind == "conclusion":
        widgets = [
            make_heading(h2_text, color="#ffffff", align="center"),
            make_text(body, dark_section=True),
            make_button("See how ChatSKU handles catalog queries live", "https://chatsku.com/demo/"),
        ]
        elementor_sections.append(make_section(widgets, bg="#1a1a2e", is_conclusion=True))

    elif kind == "faq":
        widgets = [make_heading(h2_text)]
        sub_parts = re.split(r'(?=<h3[^>]*>)', body.strip())
        for sp in sub_parts:
            sp = sp.strip()
            if not sp:
                continue
            hm = re.match(r'<h3[^>]*>(.*?)</h3>(.*)', sp, re.DOTALL)
            if hm:
                widgets.append(make_heading(hm.group(1).strip(), "h3"))
                ans = hm.group(2).strip()
                if ans:
                    widgets.append(make_text(ans))
        elementor_sections.append(make_section(widgets, bg="#f9f9fb"))

print(f"\nBuilt {len(elementor_sections)} Elementor sections:")
for i, s in enumerate(elementor_sections):
    bg = s["settings"]["background_color"]
    pad_top = s["settings"]["padding"]["top"]
    col = s["elements"][0]
    col_pad = col["settings"].get("padding", {}).get("top", "?")
    widgets = col["elements"]
    h = next((w["settings"].get("title", "")[:35] for w in widgets if w.get("widgetType") == "heading"), "?")
    print(f"  {i:2}: bg={bg}  sec_pad={pad_top}px  col_pad={col_pad}px  [{h}]")

# ── Push ──────────────────────────────────────────────────────────────────────
elementor_data_json = json.dumps(elementor_sections)
payload = {
    "meta": {
        "_elementor_edit_mode": "builder",
        "_elementor_template_type": "wp-post",
        "_elementor_data": elementor_data_json,
    }
}

print(f"\nPushing to post 186 ({len(elementor_data_json):,} chars, {len(elementor_sections)} sections)...")
body_bytes = json.dumps(payload).encode()
req2 = urllib.request.Request(f"{WP_BASE}/posts/186", data=body_bytes, headers=HEADERS, method="POST")
try:
    with urllib.request.urlopen(req2) as r:
        resp = json.loads(r.read())
    print(f"  HTTP 200  status={resp.get('status')}  featured_media={resp.get('featured_media')}")
except urllib.error.HTTPError as e:
    print(f"  HTTP ERROR {e.code}: {e.read()[:400]}")
    raise

# ── Verify ────────────────────────────────────────────────────────────────────
print("\nVerifying...")
req3 = urllib.request.Request(f"{WP_BASE}/posts/186?context=edit", headers=HEADERS)
with urllib.request.urlopen(req3) as r:
    verified = json.loads(r.read())
meta_v = verified.get("meta", {})
ed = json.loads(meta_v.get("_elementor_data", "[]"))
print(f"  Sections saved: {len(ed)}")
print(f"  edit_mode: {meta_v.get('_elementor_edit_mode')!r}")
print(f"  featured_media: {verified.get('featured_media')}")
print(f"  status: {verified.get('status')}")

print("\nSection color/padding audit:")
for i, s in enumerate(ed):
    bg = s["settings"].get("background_color", "?")
    pad_top = s["settings"].get("padding", {}).get("top", "?")
    col_pad_top = ""
    for col in s.get("elements", []):
        col_pad = col.get("settings", {}).get("padding", {})
        col_pad_top = col_pad.get("top", "?")
        break
    h = ""
    for col in s.get("elements", []):
        for w in col.get("elements", []):
            if w.get("widgetType") == "heading":
                h = w["settings"].get("title", "")[:35]
                break
        if h:
            break
    print(f"  {i:2}: bg={bg}  sec={pad_top}px  col={col_pad_top}px  [{h}]")

print("\nDone. Post 186 rebuilt matching post 96 structure.")
