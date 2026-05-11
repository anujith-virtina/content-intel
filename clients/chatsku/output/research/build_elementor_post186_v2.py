"""
Rebuild post 186 Elementor data with correct section colors and spacing,
matching the design pattern from post 151 (rfq-automation-manufacturers).

Color scheme verified from post 151:
  Executive Summary : #f9f9fb, padding 20px
  Introduction      : #ffffff, padding 0  ← fixes "unwanted spaces" issue
  Body sections     : alternate #f0f4ff / #ffffff, padding 20px
  PAA section       : #f0f4ff, padding 20px
  Conclusion        : #1a1a2e (dark), padding 60px, heading white, text #aaaacc centered
  FAQ               : #f9f9fb, padding 20px
"""
import json, secrets, re, urllib.request, urllib.error, base64

WP_BASE = "https://chatsku.com/wp-json/wp/v2"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
AUTH = base64.b64encode(b"admin:fL5q VbD3 20Nt sOjx 86wb 94iS").decode()
HEADERS = {"Authorization": f"Basic {AUTH}", "User-Agent": UA, "Content-Type": "application/json"}

IMAGES = {
    "body1": {"id": 184, "url": "https://chatsku.com/wp-content/uploads/2026/05/chatsku-after-hours-body1.jpg",
              "alt": "B2B business professional at computer researching product options, representing buyer self-service research behavior outside business hours"},
    "body2": {"id": 185, "url": "https://chatsku.com/wp-content/uploads/2026/05/chatsku-after-hours-body2.jpg",
              "alt": "B2B sales team reviewing catalog data and pricing on computer screens, showing B2B catalog query complexity and customer group pricing"},
}

def gid(): return secrets.token_hex(4)

def make_section(widgets, bg, pad_v="20", pad_h="15"):
    return {
        "id": gid(), "elType": "section", "isInner": False,
        "settings": {
            "background_background": "classic",
            "background_color": bg,
            "padding": {"top": pad_v, "bottom": pad_v, "right": pad_h, "left": pad_h, "unit": "px"}
        },
        "elements": [{"id": gid(), "elType": "column", "isInner": False,
                      "settings": {"_column_size": 100, "width": "100"},
                      "elements": widgets}]
    }

def make_heading(title, level="h2", color="#1a1a2e"):
    size = 28 if level == "h2" else 22
    s = {"title": title, "align": "left", "title_color": color,
         "typography_font_size": {"size": size, "unit": "px"}}
    if level != "h2":
        s["header_size"] = level
    return {"id": gid(), "elType": "widget", "widgetType": "heading", "elements": [], "settings": s}

def make_text(html, dark_section=False):
    # Fix relative URLs
    html = re.sub(r'href="/([\w/\-]+)"', r'href="https://chatsku.com/\1"', html)
    # Remove figure wrappers
    html = re.sub(r'<figure[^>]*>.*?</figure>', '', html, flags=re.DOTALL).strip()
    # For dark sections, wrap each <p> with color styling
    if dark_section:
        html = re.sub(r'<p([ >])',
                      r'<p style="color:#aaaacc;text-align:center;font-size:18px;max-width:720px;margin:0 auto;"\1',
                      html)
    return {"id": gid(), "elType": "widget", "widgetType": "text-editor", "elements": [],
            "settings": {"editor": html}}

def make_image(key):
    img = IMAGES[key]
    return {"id": gid(), "elType": "widget", "widgetType": "image", "elements": [],
            "settings": {
                "image": {"id": img["id"], "url": img["url"], "alt": img["alt"], "source": "library", "size": ""},
                "align": "center",
                "width": {"size": 100, "unit": "%"},
                "border_radius": {"top": "10", "right": "10", "bottom": "10", "left": "10", "unit": "px"}
            }}

def strip_h2(chunk):
    m = re.match(r'<h2[^>]*>(.*?)</h2>(.*)', chunk, re.DOTALL)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return None, chunk

# ── Fetch post content ────────────────────────────────────────────────────────
req = urllib.request.Request(f"{WP_BASE}/posts/186?context=edit", headers=HEADERS)
with urllib.request.urlopen(req) as r:
    post = json.loads(r.read())
raw = post["content"]["raw"]

# ── Parse sections ────────────────────────────────────────────────────────────
parts = [p.strip() for p in re.split(r'(?=<h2[^>]*>)', raw.strip()) if p.strip()]

# Identify section types
parsed = []
for chunk in parts:
    h2_text, body = strip_h2(chunk)
    if not h2_text:
        continue
    label = h2_text.lower().strip()
    has_body1 = 'chatsku-after-hours-body1' in body
    has_body2 = 'chatsku-after-hours-body2' in body
    clean_body = re.sub(r'<figure[^>]*>.*?</figure>', '', body, flags=re.DOTALL).strip()

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
        img_key = "body1" if has_body1 else ("body2" if has_body2 else None)
        parsed.append(("body", h2_text, clean_body, img_key))

print(f"Parsed {len(parsed)} sections:")
for kind, title, _, img in parsed:
    print(f"  [{kind}] {title[:50]}" + (f" + IMG({img})" if img else ""))

# ── Build Elementor sections ──────────────────────────────────────────────────
elementor_sections = []
body_idx = 0  # for alternating colors
BODY_COLORS = ["#f0f4ff", "#ffffff"]

for kind, h2_text, body, img_key in parsed:

    if kind == "exec_summary":
        widgets = [make_heading(h2_text), make_text(body)]
        elementor_sections.append(make_section(widgets, bg="#f9f9fb"))

    elif kind == "introduction":
        widgets = [make_heading(h2_text), make_text(body)]
        # Introduction: white bg, zero vertical padding (matches post 151)
        elementor_sections.append(make_section(widgets, bg="#ffffff", pad_v="00"))

    elif kind == "body":
        bg = BODY_COLORS[body_idx % 2]
        body_idx += 1
        widgets = [make_heading(h2_text)]
        if img_key:
            widgets.append(make_image(img_key))
        if body:
            widgets.append(make_text(body))
        elementor_sections.append(make_section(widgets, bg=bg))

    elif kind == "paa":
        # PAA gets the next alternating color
        bg = BODY_COLORS[body_idx % 2]
        body_idx += 1
        widgets = [make_heading(h2_text)]
        sub_parts = re.split(r'(?=<h3[^>]*>)', body.strip())
        for sp in sub_parts:
            sp = sp.strip()
            if not sp: continue
            hm = re.match(r'<h3[^>]*>(.*?)</h3>(.*)', sp, re.DOTALL)
            if hm:
                widgets.append(make_heading(hm.group(1).strip(), "h3"))
                ans = hm.group(2).strip()
                if ans:
                    widgets.append(make_text(ans))
        elementor_sections.append(make_section(widgets, bg=bg))

    elif kind == "conclusion":
        # Conclusion: dark navy, 60px padding, white heading, #aaaacc body text
        widgets = [make_heading(h2_text, color="#ffffff"), make_text(body, dark_section=True)]
        elementor_sections.append(make_section(widgets, bg="#1a1a2e", pad_v="60"))

    elif kind == "faq":
        widgets = [make_heading(h2_text)]
        sub_parts = re.split(r'(?=<h3[^>]*>)', body.strip())
        for sp in sub_parts:
            sp = sp.strip()
            if not sp: continue
            hm = re.match(r'<h3[^>]*>(.*?)</h3>(.*)', sp, re.DOTALL)
            if hm:
                widgets.append(make_heading(hm.group(1).strip(), "h3"))
                ans = hm.group(2).strip()
                if ans:
                    widgets.append(make_text(ans))
        # FAQ: light gray (same as Executive Summary — visual bookend)
        elementor_sections.append(make_section(widgets, bg="#f9f9fb"))

print(f"\nBuilt {len(elementor_sections)} Elementor sections with colors:")
for i, s in enumerate(elementor_sections):
    bg = s["settings"]["background_color"]
    pad = s["settings"]["padding"]["top"]
    widgets = s["elements"][0]["elements"]
    h = next((w["settings"].get("title","")[:35] for w in widgets if w.get("widgetType")=="heading"), "?")
    print(f"  {i:2}: bg={bg}  pad={pad}px  [{h}]")

# ── Push ──────────────────────────────────────────────────────────────────────
elementor_data_json = json.dumps(elementor_sections)
payload = {
    "meta": {
        "_elementor_edit_mode": "builder",
        "_elementor_template_type": "wp-post",
        "_elementor_data": elementor_data_json,
    }
}

print(f"\nPushing to post 186 ({len(elementor_data_json)} chars)...")
body_bytes = json.dumps(payload).encode()
req2 = urllib.request.Request(f"{WP_BASE}/posts/186", data=body_bytes, headers=HEADERS, method="POST")
try:
    with urllib.request.urlopen(req2) as r:
        resp = json.loads(r.read())
    print(f"  HTTP 200  status={resp.get('status')}  featured_media={resp.get('featured_media')}")
except urllib.error.HTTPError as e:
    print(f"  HTTP ERROR {e.code}: {e.read()[:300]}")
    raise

# ── Verify ────────────────────────────────────────────────────────────────────
req3 = urllib.request.Request(f"{WP_BASE}/posts/186?context=edit", headers=HEADERS)
with urllib.request.urlopen(req3) as r:
    verified = json.loads(r.read())
meta_v = verified.get('meta', {})
ed = json.loads(meta_v.get('_elementor_data', '[]'))
print(f"\nVerified: {len(ed)} sections, edit_mode={meta_v.get('_elementor_edit_mode')!r}")

# Quick color audit
print("Section colors pushed:")
for i, s in enumerate(ed):
    bg = s["settings"].get("background_color", "?")
    pad = s["settings"].get("padding", {}).get("top", "?")
    h = ""
    for col in s.get("elements", []):
        for w in col.get("elements", []):
            if w.get("widgetType") == "heading":
                h = w["settings"].get("title", "")[:35]
                break
        if h: break
    print(f"  {i:2}: bg={bg}  pad={pad}px  [{h}]")

print("\nDone. Post 186 updated with correct section colors and spacing.")
