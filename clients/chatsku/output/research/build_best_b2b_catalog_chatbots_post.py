"""
Build and publish: best-b2b-catalog-chatbots-2026
Post: "Best B2B catalog chatbots in 2026"
Format: Format C (Listicle with opinions)  Date: 2026-06-17

Pipeline:
  1. Load .env credentials
  2. Source and upload 3 photo images (Pexels -> Openverse/Stocksnap fallback)
  3. Generate 1 infographic (PIL raster, 670x452) with real research data
  4. Build Elementor JSON from draft HTML (handles H3 sub-blocks: tool profiles, PAA, FAQ)
  5. Push to WordPress as draft
  6. Clear Elementor cache
  7. Save published HTML to output/published/
  8. Run full pre-publish checklist, report results

Template: clients/chatsku/output/research/build_b2b_catalog_conversion_post.py
Draft source: clients/chatsku/output/drafts/best-b2b-catalog-chatbots-2026-2026-06-17.md
Brief source: clients/chatsku/output/briefs/best-b2b-catalog-chatbots-2026-2026-06-17.md
"""

import json, secrets, re, urllib.request, urllib.error, urllib.parse
import base64, os, io, time, sys, ssl

from pathlib import Path

_ssl_ctx = ssl._create_unverified_context()

# ── Load .env ──────────────────────────────────────────────────────────────────
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
PEXELS_KEY = os.environ.get("PEXELS_API_KEY", "")

if not USERNAME or not PASSWORD:
    print("ERROR: CHATSKU_WP_USERNAME or CHATSKU_WP_APP_PASSWORD not set in .env")
    sys.exit(1)

AUTH = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {AUTH}",
    "User-Agent": UA,
    "Content-Type": "application/json"
}

print(f"Credentials: WP user={USERNAME!r}")
print(f"Pexels key: {'set' if PEXELS_KEY else 'not set (will use Openverse fallback)'}")

# ═══════════════════════════════════════════════════════════════════════════════
# IMAGE SOURCING
# ═══════════════════════════════════════════════════════════════════════════════

def pexels_search(query, per_page=5):
    if not PEXELS_KEY:
        return []
    url = (f"https://api.pexels.com/v1/search"
           f"?query={urllib.parse.quote(query)}&orientation=landscape&per_page={per_page}")
    req = urllib.request.Request(url, headers={"Authorization": PEXELS_KEY, "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15, context=_ssl_ctx) as r:
            data = json.loads(r.read())
        photos = data.get("photos", [])
        print(f"  Pexels '{query}': {len(photos)} results")
        return [p["src"]["large2x"] for p in photos]
    except Exception as e:
        print(f"  Pexels error: {e}")
        return []

def openverse_search(query, per_page=10):
    url = (f"https://api.openverse.org/v1/images/"
           f"?q={urllib.parse.quote(query)}&license=cc0,pdm&page_size={per_page}&source=stocksnap")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15, context=_ssl_ctx) as r:
            data = json.loads(r.read())
        results = data.get("results", [])
        print(f"  Openverse '{query}': {len(results)} results")
        return [r["url"] for r in results if r.get("url")]
    except Exception as e:
        print(f"  Openverse error: {e}")
        return []

def download_image(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25, context=_ssl_ctx) as r:
            data = r.read()
        if len(data) < 8000:
            print(f"  Too small ({len(data)} bytes): {url[:60]}")
            return None
        if data[:2] == b'\xff\xd8' or data[:8] == b'\x89PNG\r\n\x1a\n':
            print(f"  Downloaded {len(data)//1024}KB: {url[:70]}...")
            return data
        print(f"  Invalid signature: {url[:60]}")
        return None
    except Exception as e:
        print(f"  Download error: {e}")
        return None

def resize_image(data, width=860, height=452, quality=82):
    try:
        from PIL import Image
    except ImportError:
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "Pillow", "-q"], check=True)
        from PIL import Image

    img = Image.open(io.BytesIO(data)).convert("RGB")
    src_w, src_h = img.size
    scale = max(width / src_w, height / src_h)
    new_w, new_h = int(src_w * scale), int(src_h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - width) // 2
    top  = (new_h - height) // 2
    img = img.crop((left, top, left + width, top + height))

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    result = buf.getvalue()
    if len(result) > 200 * 1024:
        buf2 = io.BytesIO()
        img.save(buf2, format="JPEG", quality=70, optimize=True)
        result = buf2.getvalue()
        print(f"  Re-encoded at q70: {len(result)//1024}KB")
    print(f"  Resized to {width}x{height}: {len(result)//1024}KB")
    return result

def source_image(queries, width=860, height=452):
    for query in queries:
        print(f"  Trying Pexels: '{query}'")
        urls = pexels_search(query)
        for url in urls:
            raw = download_image(url)
            if raw:
                return url, resize_image(raw, width, height)
        print(f"  Trying Openverse: '{query}'")
        urls = openverse_search(query)
        for url in urls:
            raw = download_image(url)
            if raw:
                return url, resize_image(raw, width, height)
        time.sleep(0.8)
    return None, None

def upload_image(jpeg_bytes, filename, alt_text):
    upload_headers = {
        "Authorization": f"Basic {AUTH}",
        "User-Agent": UA,
        "Content-Type": "image/jpeg",
        "Content-Disposition": f'attachment; filename="{filename}"',
    }
    req = urllib.request.Request(
        f"{WP_BASE}/media", data=jpeg_bytes, headers=upload_headers, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=60, context=_ssl_ctx) as r:
            media = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  Upload HTTP {e.code}: {e.read()[:400]}")
        raise
    media_id  = media["id"]
    media_url = media["source_url"]
    print(f"  Uploaded: ID={media_id}  URL={media_url}")

    alt_payload = json.dumps({"alt_text": alt_text}).encode()
    req2 = urllib.request.Request(
        f"{WP_BASE}/media/{media_id}", data=alt_payload, headers=HEADERS, method="POST"
    )
    with urllib.request.urlopen(req2, timeout=20, context=_ssl_ctx) as r:
        r.read()
    print(f"  Alt text: {alt_text[:70]}...")
    return {"id": media_id, "url": media_url, "alt": alt_text}

# ═══════════════════════════════════════════════════════════════════════════════
# INFOGRAPHIC GENERATION (raster, 670x452, real data from research)
# ═══════════════════════════════════════════════════════════════════════════════

def generate_infographic():
    from PIL import Image, ImageDraw, ImageFont

    W, H = 670, 452
    BG = (249, 249, 251)
    NAVY = (26, 26, 46)
    TEAL = (0, 201, 177)
    GRAY = (110, 110, 120)
    LIGHT_GRID = (220, 222, 230)

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    def font(size, bold=False):
        candidates = [
            r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
            r"C:\Windows\Fonts\arial.ttf",
        ]
        for c in candidates:
            if os.path.exists(c):
                try:
                    return ImageFont.truetype(c, size)
                except Exception:
                    pass
        return ImageFont.load_default()

    f_title = font(18, bold=True)
    f_axis = font(12, bold=True)
    f_label = font(12)
    f_sub = font(11)

    # Title
    d.text((20, 14), "Speed vs. cost: 7 B2B catalog chatbots compared (2026)", fill=NAVY, font=f_title)
    d.text((20, 38), "Deployment time vs. typical annual cost band, from published and estimated figures", fill=GRAY, font=f_sub)

    # Plot area
    px0, py0, px1, py1 = 110, 80, 645, 400
    d.rectangle([px0, py0, px1, py1], outline=LIGHT_GRID, width=1)

    x_labels = ["Same-day", "Days", "Weeks", "~4 months avg."]
    y_labels = ["Enterprise\n$30K-$500K+/yr", "Custom /\nnot disclosed", "Free to\nlow-cost"]

    n_x, n_y = len(x_labels), len(y_labels)
    col_w = (px1 - px0) / n_x
    row_h = (py1 - py0) / n_y

    for i in range(1, n_x):
        x = px0 + i * col_w
        d.line([(x, py0), (x, py1)], fill=LIGHT_GRID, width=1)
    for i in range(1, n_y):
        y = py0 + i * row_h
        d.line([(px0, y), (px1, y)], fill=LIGHT_GRID, width=1)

    for i, lbl in enumerate(x_labels):
        cx = px0 + i * col_w + col_w / 2
        d.text((cx - 28, py1 + 10), lbl, fill=NAVY, font=f_axis)

    for i, lbl in enumerate(y_labels):
        cy = py0 + i * row_h + row_h / 2
        for j, line in enumerate(lbl.split("\n")):
            d.text((10, cy - 12 + j * 13), line, fill=NAVY, font=f_axis)

    d.text((px0, py1 + 32), "Deployment time", fill=GRAY, font=f_sub)
    d.text((10, py0 - 16), "Annual cost", fill=GRAY, font=f_sub)

    # Points: (label, x_idx 0-3, y_idx 0-2 (0=enterprise top,1=custom mid,2=low bottom), color, dx, dy jitter, note)
    points = [
        ("ChatSKU",   0, 1, TEAL,      0, -14, "live ~1 day"),
        ("Tidio",     0, 2, (150,150,160), 0, 14, "+ hidden AI fee"),
        ("HumCommerce", 2, 1, (90,90,140), -10, -14, "Magento only"),
        ("Zoovu",     2, 1, (90,90,140), 10, 14, "custom quote"),
        ("Algolia",   2, 2, (90,90,140), 0, -14, "free to $50K+/yr"),
        ("Coveo",     3, 0, (90,90,140), 0, -14, "$30K-$500K+/yr"),
        ("Bloomreach", 2, 0, (90,90,140), 30, 14, "$35K-$100K+/yr"),
    ]

    for name, xi, yi, color, dx, dy, note in points:
        cx = px0 + xi * col_w + col_w / 2 + dx
        cy = py0 + yi * row_h + row_h / 2 + dy
        r = 7 if name == "ChatSKU" else 5
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color, outline=NAVY)
        label = name + (" (#1)" if name == "ChatSKU" else "")
        d.text((cx + r + 5, cy - 16), label, fill=NAVY, font=f_label)
        d.text((cx + r + 5, cy - 2), note, fill=GRAY, font=f_sub)

    d.text((20, H - 18), "Source: vendor pricing pages, G2 review data, third-party pricing trackers (2026)", fill=GRAY, font=f_sub)

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=88, optimize=True)
    data = buf.getvalue()
    print(f"  Infographic generated: 670x452, {len(data)//1024}KB")
    return data

# ═══════════════════════════════════════════════════════════════════════════════
# DRAFT HTML (loaded from the approved draft file, frontmatter stripped)
# ═══════════════════════════════════════════════════════════════════════════════

DRAFT_PATH = Path(r"C:\content-intel\clients\chatsku\output\drafts\best-b2b-catalog-chatbots-2026-2026-06-17.md")
_raw = DRAFT_PATH.read_text(encoding="utf-8")
# Strip YAML frontmatter
_parts = _raw.split("---", 2)
DRAFT_HTML = _parts[2].strip() if len(_parts) >= 3 else _raw.strip()

# ── Em dash verification ───────────────────────────────────────────────────────
em_count = DRAFT_HTML.count("—") + DRAFT_HTML.count("&mdash;")
assert em_count == 0, f"ERROR: {em_count} em dashes found in content"
print("Em dash scan: PASS (0 found)")

BANNED_WORDS = [
    "delve", "leverage", "navigate", "realm", "landscape", "ecosystem",
    "robust", "seamless", "cutting-edge", "game-changing", "revolutionary",
    "moreover", "furthermore", "harness", "unlock", "supercharge",
    "transform your", "in today's fast-paced world", "it's important to note",
    "let's explore", "when it comes to", "just a chatbot",
]
lower_html = DRAFT_HTML.lower()
banned_hits = {w: lower_html.count(w) for w in BANNED_WORDS if w.lower() in lower_html}
# "Elevate" is Algolia's actual tier name, not the banned verb "elevate" -- exclude separately
if "elevate" in lower_html:
    elevate_as_word = re.findall(r'\belevate\b(?!"? (?:contracts|enterprise|tier))', lower_html)
print(f"Banned word scan: {banned_hits if banned_hits else 'PASS (0 found)'}")

# ═══════════════════════════════════════════════════════════════════════════════
# ELEMENTOR JSON BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

def gid():
    return secrets.token_hex(4)

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
    html = re.sub(r'<img[^>]*/>', '', html).strip()
    html = re.sub(r'<img[^>]*></img>', '', html, flags=re.DOTALL).strip()
    html = re.sub(r'<img[^>]*>', '', html).strip()
    if dark_section:
        html = re.sub(
            r'<p([ >])',
            r'<p style="color:#aaaacc;text-align:center;font-size:18px;max-width:720px;margin:0 auto;"\1',
            html
        )
    return {"id": gid(), "elType": "widget", "widgetType": "text-editor",
            "elements": [], "settings": {"editor": html}}

def make_image_widget(img_data):
    return {
        "id": gid(), "elType": "widget", "widgetType": "image", "elements": [],
        "settings": {
            "image": {
                "id": img_data["id"],
                "url": img_data["url"],
                "alt": img_data["alt"],
                "source": "library",
                "size": ""
            },
            "align": "center",
            "width": {"size": 100, "unit": "%"},
            "border_radius": {"top": "10", "right": "10", "bottom": "10", "left": "10", "unit": "px"}
        }
    }

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
    if is_conclusion:
        sec_pad = {"top": "20", "bottom": "30", "unit": "px", "right": "0", "left": "0"}
    else:
        sec_pad = {"top": "60", "bottom": "60", "unit": "px"}
    col_pad = {"unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20", "isLinked": True}
    return {
        "id": gid(),
        "elType": "section",
        "isInner": False,
        "settings": {
            "background_background": "classic",
            "background_color": bg,
            "padding": sec_pad
        },
        "elements": [{
            "id": gid(),
            "elType": "column",
            "isInner": False,
            "settings": {"_column_size": 100, "width": "100", "padding": col_pad},
            "elements": widgets
        }]
    }

def parse_h3_blocks(body_html):
    """Split a chunk on H3 boundaries -> list of (lead_text, [(h3_text, h3_body), ...])."""
    parts = re.split(r'(?=<h3[^>]*>)', body_html.strip())
    lead = ""
    blocks = []
    if parts and not re.match(r'^\s*<h3', parts[0]):
        lead = parts.pop(0).strip()
    for p in parts:
        p = p.strip()
        if not p:
            continue
        m = re.match(r'<h3[^>]*>(.*?)</h3>(.*)', p, re.DOTALL)
        if m:
            blocks.append((m.group(1).strip(), m.group(2).strip()))
    return lead, blocks

def build_elementor(body1_img, body2_img, infographic_img):
    BODY_COLORS = ["#f0f4ff", "#ffffff", "#f9f9fb", "#ffffff"]
    body_color_idx = 0

    elementor_sections = []

    # Strip H1 (used only for reference -- WP post title carries it)
    html = re.sub(r'<h1[^>]*>.*?</h1>', '', DRAFT_HTML, count=1, flags=re.DOTALL).strip()

    chunks = [c.strip() for c in re.split(r'(?=<h2[^>]*>)', html) if c.strip()]

    # First chunk before any H2 = intro (no heading widget, per Format C "no H2 hook")
    if chunks and not re.match(r'^\s*<h2', chunks[0]):
        intro_html = chunks.pop(0).strip()
        elementor_sections.append(make_section([make_text(intro_html)], bg="#ffffff"))

    for chunk in chunks:
        hm = re.match(r'<h2[^>]*>(.*?)</h2>(.*)', chunk, re.DOTALL)
        if not hm:
            continue
        h2_text   = hm.group(1).strip()
        body_html = hm.group(2).strip()
        label     = h2_text.lower()

        if "conclusion" in label:
            widgets = [
                make_heading(h2_text, color="#ffffff", align="center"),
                make_text(body_html, dark_section=True),
                make_button("Start your free trial", "https://chatsku.com/signup/"),
            ]
            elementor_sections.append(make_section(widgets, bg="#1a1a2e", is_conclusion=True))
            continue

        if "frequently asked questions" in label:
            widgets = [make_heading(h2_text)]
            lead, blocks = parse_h3_blocks(body_html)
            if lead:
                widgets.append(make_text(lead))
            for h3_text, h3_body in blocks:
                widgets.append(make_heading(h3_text, "h3"))
                if h3_body:
                    widgets.append(make_text(h3_body))
            elementor_sections.append(make_section(widgets, bg="#f9f9fb"))
            continue

        if "people also ask" in label:
            widgets = [make_heading(h2_text)]
            lead, blocks = parse_h3_blocks(body_html)
            if lead:
                widgets.append(make_text(lead))
            for h3_text, h3_body in blocks:
                widgets.append(make_heading(h3_text, "h3"))
                if h3_body:
                    widgets.append(make_text(h3_body))
            bg = BODY_COLORS[body_color_idx % len(BODY_COLORS)]
            body_color_idx += 1
            elementor_sections.append(make_section(widgets, bg=bg))
            continue

        if "best b2b catalog chatbots in 2026" == label.strip():
            widgets = [make_heading(h2_text)]
            lead, blocks = parse_h3_blocks(body_html)
            if lead:
                widgets.append(make_text(lead))
            for h3_text, h3_body in blocks:
                widgets.append(make_heading(h3_text, "h3"))
                if h3_body:
                    widgets.append(make_text(h3_body))
            widgets.append(make_image_widget(body2_img))  # image LAST in column
            bg = BODY_COLORS[body_color_idx % len(BODY_COLORS)]
            body_color_idx += 1
            elementor_sections.append(make_section(widgets, bg=bg))
            continue

        # Generic body H2 sections
        widgets = [make_heading(h2_text)]
        if body_html:
            widgets.append(make_text(body_html))

        if "what makes a b2b catalog chatbot different" in label:
            widgets.append(make_image_widget(body1_img))
        elif "how do these b2b catalog chatbots compare" in label:
            widgets.append(make_image_widget(infographic_img))

        bg = BODY_COLORS[body_color_idx % len(BODY_COLORS)]
        body_color_idx += 1
        elementor_sections.append(make_section(widgets, bg=bg))

    return elementor_sections

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 65)
print("BUILD: best-b2b-catalog-chatbots-2026  (2026-06-17)")
print("=" * 65)

# ── STEP 1: Source and upload photo images ───────────────────────────────────
PRESELECTED = {
    # Visually verified (full-res preview) before selection -- see QA notes below.
    # "Business Team" -- man presenting tech options to a small group, laptop + tablet, modern office.
    "featured": "https://cdn.stocksnap.io/img-thumbs/960w/W6PNBNYHM6.jpg",
    # "Accounting Finance" -- calculator + laptop showing a data dashboard, literal pricing/data scene.
    "body1": "https://cdn.stocksnap.io/img-thumbs/960w/JONMP7TPGK.jpg",
    # "Business Team" -- group at a table with laptops, distinct from featured image, no reuse.
    "body2": "https://cdn.stocksnap.io/img-thumbs/960w/V8NHXQVQ70.jpg",
}

def source_preselected_or_search(pre_url, fallback_queries, width=860, height=452):
    print(f"  Downloading pre-selected: {pre_url}")
    raw = download_image(pre_url)
    if raw:
        return pre_url, resize_image(raw, width, height)
    print("  Pre-selected failed, trying search fallback...")
    return source_image(fallback_queries, width, height)

print("\n[IMAGE 1/4] Featured: B2B sales tech evaluation scene")
FEAT_ALT = ("B2B sales manager presenting catalog chatbot vendor options to a small team "
            "during a software evaluation meeting")
_, feat_bytes = source_preselected_or_search(
    PRESELECTED["featured"], ["business team", "office laptop", "team meeting"]
)
if feat_bytes is None:
    print("FATAL: Could not source featured image"); sys.exit(1)
feat_media = upload_image(feat_bytes, "chatsku-best-b2b-catalog-chatbots-featured.jpg", FEAT_ALT)

print("\n[IMAGE 2/4] Body: product catalog / SKU pricing data scene")
BODY1_ALT = ("Distributor employee reviewing B2B catalog pricing data on a laptop dashboard "
             "with a calculator, checking customer-specific rates")
_, body1_bytes = source_preselected_or_search(
    PRESELECTED["body1"], ["spreadsheet computer", "office computer", "business working"]
)
if body1_bytes is None:
    print("FATAL: Could not source body image 1"); sys.exit(1)
body1_media = upload_image(body1_bytes, "chatsku-best-b2b-catalog-chatbots-body1.jpg", BODY1_ALT)

print("\n[IMAGE 3/4] Body: sales team comparing chatbot options scene")
BODY2_ALT = ("B2B sales team reviewing chatbot vendor options together on laptops "
             "around an office table")
_, body2_bytes = source_preselected_or_search(
    PRESELECTED["body2"], ["business team", "team computer", "office desk"]
)
if body2_bytes is None:
    print("FATAL: Could not source body image 2"); sys.exit(1)
body2_media = upload_image(body2_bytes, "chatsku-best-b2b-catalog-chatbots-body2.jpg", BODY2_ALT)

print("\n[IMAGE 4/4] Infographic: deployment speed vs. annual cost, 7 tools")
infographic_bytes = generate_infographic()
INFO_ALT = ("Infographic comparing deployment speed and annual cost for seven B2B catalog "
            "chatbot vendors including ChatSKU, Algolia, Coveo, and Tidio")
infographic_media = upload_image(infographic_bytes, "chatsku-best-b2b-catalog-chatbots-infographic.jpg", INFO_ALT)

print(f"\nImages uploaded:")
print(f"  Featured:    ID={feat_media['id']}  {feat_media['url']}")
print(f"  Body1:       ID={body1_media['id']}  {body1_media['url']}")
print(f"  Body2:       ID={body2_media['id']}  {body2_media['url']}")
print(f"  Infographic: ID={infographic_media['id']}  {infographic_media['url']}")

for lbl, m in [("Featured", feat_media), ("Body1", body1_media), ("Body2", body2_media), ("Infographic", infographic_media)]:
    if not m["url"].startswith("https://chatsku.com/wp-content/uploads/"):
        print(f"FATAL: {lbl} URL invalid: {m['url']}")
        sys.exit(1)
print("All image URLs: PASS (begin with https://chatsku.com/wp-content/uploads/)")

# ── STEP 2: Build Elementor JSON ──────────────────────────────────────────────
print("\n" + "=" * 65)
print("BUILDING ELEMENTOR JSON")
print("=" * 65)

elementor_sections = build_elementor(body1_media, body2_media, infographic_media)
elementor_json = json.dumps(elementor_sections)

print(f"\nBuilt {len(elementor_sections)} Elementor sections:")
for i, s in enumerate(elementor_sections):
    bg   = s["settings"]["background_color"]
    pad  = s["settings"]["padding"]["top"]
    cols = s["elements"][0]["elements"]
    h    = next((w["settings"].get("title","")[:45] for w in cols if w.get("widgetType")=="heading"), "(no heading)")
    types = [w.get("widgetType") for w in cols]
    if "image" in types and "text-editor" in types:
        img_pos  = max(idx for idx, t in enumerate(types) if t == "image")
        text_pos = max(idx for idx, t in enumerate(types) if t == "text-editor")
        order_ok = img_pos > text_pos
        print(f"  {i:2}: bg={bg}  pad={pad}  [{h}]  n_widgets={len(types)}  img_order={'OK' if order_ok else 'FAIL!'}")
        if not order_ok:
            print("  CRITICAL ERROR: image before text-editor!")
            sys.exit(1)
    else:
        print(f"  {i:2}: bg={bg}  pad={pad}  [{h}]  n_widgets={len(types)}")

parsed_check = json.loads(elementor_json)
assert isinstance(parsed_check, list) and len(parsed_check) > 0, "Elementor JSON empty"
print(f"\nElementor JSON: {len(elementor_json):,} chars  {len(parsed_check)} sections")

# ── STEP 3: Pre-publish checklist ─────────────────────────────────────────────
print("\n" + "=" * 65)
print("PRE-PUBLISH CHECKLIST")
print("=" * 65)

checks = {}

ed = DRAFT_HTML.count("—") + DRAFT_HTML.count("&mdash;")
checks["No em dashes"] = ed == 0
print(f"  [{'PASS' if checks['No em dashes'] else 'FAIL'}] Em dashes: {ed}")

existing_slugs = [
    "rfq-automation-manufacturers", "rfq-automation-for-product-catalogs",
    "ai-chatbot-for-manufacturers-dallas", "b2b-ecommerce-chatbot-dallas",
    "pdf-catalog-sales-liability", "rfq-form-conversion-rate",
    "convert-pdf-catalog-to-website", "b2b-catalog-issues-costing-sales",
    "b2b-after-hours-buyer-problem", "b2b-catalog-conversion-rate",
    "lost-b2b-revenue-calculator", "b2b-catalog-revenue-leakage",
    "b2b-after-hours-lead-capture",
]
new_slug = "best-b2b-catalog-chatbots-2026"
checks["Slug unique"] = new_slug not in existing_slugs
print(f"  [{'PASS' if checks['Slug unique'] else 'FAIL'}] Slug '{new_slug}' unique")

checks["Featured media"] = bool(feat_media["id"])
print(f"  [{'PASS' if checks['Featured media'] else 'FAIL'}] Featured media ID: {feat_media['id']}")

url_ok = all(m["url"].startswith("https://chatsku.com/wp-content/uploads/")
             for m in [feat_media, body1_media, body2_media, infographic_media])
checks["Image URLs"] = url_ok
print(f"  [{'PASS' if url_ok else 'FAIL'}] All image URLs: chatsku.com/wp-content/uploads/")

order_ok = True
for s in elementor_sections:
    types = [w.get("widgetType") for w in s["elements"][0]["elements"]]
    if "image" in types and "text-editor" in types:
        if max(i for i, t in enumerate(types) if t == "image") < max(i for i, t in enumerate(types) if t == "text-editor"):
            order_ok = False
checks["Image widget order"] = order_ok
print(f"  [{'PASS' if order_ok else 'FAIL'}] Image widgets AFTER text-editor in every section")

wp_content = re.sub(r'<h1[^>]*>.*?</h1>', '', DRAFT_HTML, flags=re.DOTALL).strip()
wp_content = re.sub(r'<img[^>]*/>', '', wp_content).strip()
wp_content = re.sub(r'<img[^>]*>', '', wp_content).strip()
no_bare_img = not bool(re.search(r'<img[^>]*>', wp_content))
checks["No bare img"] = no_bare_img
print(f"  [{'PASS' if no_bare_img else 'FAIL'}] No bare <img> tags in WP content")

ext_links = re.findall(r'href="https?://(?!chatsku\.com)[^"]+', DRAFT_HTML)
checks["External links"] = len(ext_links) <= 2
print(f"  [{'PASS' if checks['External links'] else 'FAIL'}] External links: {len(ext_links)} (max 2)")
for el in ext_links:
    print(f"    {el[:80]}")

int_links = re.findall(r'href="https://chatsku\.com/[^"]+', DRAFT_HTML)
checks["Internal links"] = 8 <= len(int_links) <= 10
print(f"  [{'PASS' if checks['Internal links'] else 'FAIL'}] Internal links: {len(int_links)} (target 8-10)")
for il in int_links:
    print(f"    {il[:80]}")

competitor_domains = ["drift.com", "intercom.com", "tidio.com", "algolia.com", "coveo.com",
                       "bloomreach.com", "zoovu.com", "humcommerce.com"]
no_comp = not any(cd in DRAFT_HTML for cd in competitor_domains)
checks["No competitor links"] = no_comp
print(f"  [{'PASS' if no_comp else 'FAIL'}] No competitor links")

checks["No banned words"] = len(banned_hits) == 0
print(f"  [{'PASS' if checks['No banned words'] else 'FAIL'}] Banned AI-tell words: {banned_hits if banned_hits else 0}")

conc_sec = None
for s in elementor_sections:
    col_ws = s["elements"][0]["elements"]
    for w in col_ws:
        if w.get("widgetType") == "heading" and "conclusion" in w["settings"].get("title","").lower():
            conc_sec = s; break
    if conc_sec: break

if conc_sec:
    bg_c = conc_sec["settings"].get("background_color")
    col_ws = conc_sec["elements"][0]["elements"]
    h_w = next((w for w in col_ws if w.get("widgetType") == "heading"), None)
    h_color = h_w["settings"].get("title_color") if h_w else None
    has_btn = any(w.get("widgetType") == "button" for w in col_ws)
    checks["Conclusion bg"] = bg_c == "#1a1a2e"
    checks["Conclusion heading"] = h_color == "#ffffff"
    checks["Conclusion button"] = has_btn
    print(f"  [{'PASS' if checks['Conclusion bg'] else 'FAIL'}] Conclusion bg: {bg_c}")
    print(f"  [{'PASS' if checks['Conclusion heading'] else 'FAIL'}] Conclusion heading color: {h_color}")
    print(f"  [{'PASS' if checks['Conclusion button'] else 'FAIL'}] Conclusion button widget present")
else:
    checks["Conclusion"] = False
    print("  [FAIL] Conclusion section not found")

checks["Elementor JSON"] = len(elementor_sections) > 0
print(f"  [{'PASS' if checks['Elementor JSON'] else 'FAIL'}] Elementor JSON: {len(elementor_sections)} sections")

checks["Status draft"] = True
print("  [PASS] Status: draft")

all_pass = all(checks.values())
if not all_pass:
    failed = [k for k, v in checks.items() if not v]
    print(f"\nCHECKLIST FAILED: {failed}")
    print("Fix all failures before pushing.")
    sys.exit(1)
print("\nPRE-PUBLISH CHECKLIST: ALL PASS")

# ── STEP 4: Push to WordPress ──────────────────────────────────────────────────
print("\n" + "=" * 65)
print("PUSHING TO WORDPRESS (draft)")
print("=" * 65)

POST_TITLE = "Best B2B catalog chatbots in 2026"
payload = {
    "title": POST_TITLE,
    "slug": new_slug,
    "status": "draft",
    "content": wp_content,
    "featured_media": feat_media["id"],
    "meta": {
        "_elementor_edit_mode": "builder",
        "_elementor_template_type": "wp-post",
        "_elementor_data": elementor_json
    }
}

payload_bytes = json.dumps(payload).encode("utf-8")
print(f"Payload: {len(payload_bytes):,} bytes")

req_push = urllib.request.Request(
    f"{WP_BASE}/posts", data=payload_bytes, headers=HEADERS, method="POST"
)
try:
    with urllib.request.urlopen(req_push, timeout=120, context=_ssl_ctx) as r:
        resp = json.loads(r.read())
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read()[:600]}")
    sys.exit(1)

post_id   = resp["id"]
post_link = resp.get("link", "")
print(f"\nPUSH SUCCESS:")
print(f"  Post ID:  {post_id}")
print(f"  Status:   {resp.get('status')}")
print(f"  Link:     {post_link}")

print("\nVerifying saved data...")
req_v = urllib.request.Request(f"{WP_BASE}/posts/{post_id}?context=edit", headers=HEADERS)
with urllib.request.urlopen(req_v, timeout=30, context=_ssl_ctx) as r:
    verified = json.loads(r.read())
meta_v = verified.get("meta", {})
saved_ed = json.loads(meta_v.get("_elementor_data", "[]"))
print(f"  Sections saved:  {len(saved_ed)}")
print(f"  edit_mode:       {meta_v.get('_elementor_edit_mode')!r}")
print(f"  featured_media:  {verified.get('featured_media')}")
print(f"  status:          {verified.get('status')}")

print("\nClearing Elementor cache...")
cache_req = urllib.request.Request(
    "https://chatsku.com/wp-json/elementor/v1/cache",
    headers={"Authorization": f"Basic {AUTH}", "User-Agent": UA},
    method="DELETE"
)
try:
    with urllib.request.urlopen(cache_req, timeout=20, context=_ssl_ctx) as r:
        print(f"  Cache clear: HTTP {r.status}")
except urllib.error.HTTPError as e:
    print(f"  Cache clear HTTP {e.code}: {e.read()[:200]}")
except Exception as e:
    print(f"  Cache clear: {e}")

print("\nSaving published HTML...")
published_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{POST_TITLE} | ChatSKU</title>
<meta name="description" content="ChatSKU, Algolia, Coveo, Bloomreach, Zoovu, HumCommerce, and Tidio compared for B2B catalogs, RFQs, and tiered pricing. See which catalog chatbot actually fits your distributor.">
<meta name="robots" content="index,follow">
<!-- ChatSKU Published Post -->
<!-- Post ID: {post_id} -->
<!-- Date: 2026-06-17 -->
<!-- Slug: {new_slug} -->
<!-- Featured Media ID: {feat_media['id']} -->
<!-- Body Image 1 ID: {body1_media['id']} -->
<!-- Body Image 2 ID: {body2_media['id']} -->
<!-- Infographic Media ID: {infographic_media['id']} -->
<!-- Status: draft -->
<!-- Yoast meta: SET MANUALLY in WP dashboard -->
<!-- Yoast title: Best B2B Catalog Chatbots in 2026: 7 Tools Compared | ChatSKU -->
<!-- Yoast desc: ChatSKU, Algolia, Coveo, Bloomreach, Zoovu, HumCommerce, and Tidio compared for B2B catalogs, RFQs, and tiered pricing. See which one actually fits your distributor. -->
</head>
<body>

<h1>{POST_TITLE}</h1>

<!-- Featured image: 860x452 | Media ID: {feat_media['id']} -->
<img src="{feat_media['url']}" width="860" height="452" alt="{FEAT_ALT}">

{DRAFT_HTML}

</body>
</html>"""

out_path = Path(r"C:\content-intel\clients\chatsku\output\published\best-b2b-catalog-chatbots-2026-2026-06-17.html")
out_path.write_text(published_html, encoding="utf-8")
print(f"  Saved: {out_path}")

print("\n" + "=" * 65)
print("PUBLISH COMPLETE")
print("=" * 65)
print(f"  Post ID:           {post_id}")
print(f"  Post URL:          {post_link}")
print(f"  Post status:       draft")
print(f"  Featured media ID: {feat_media['id']}")
print(f"  Body1 media ID:    {body1_media['id']}")
print(f"  Body2 media ID:    {body2_media['id']}")
print(f"  Infographic ID:    {infographic_media['id']}")
print(f"  Elementor sections:{len(elementor_sections)}")
print(f"  Internal links:    {len(int_links)}")
print(f"  External links:    {len(ext_links)}")
print(f"  Published HTML:    {out_path}")
print()
print("MANUAL FOLLOW-UP REQUIRED:")
print("  1. WP Admin > Posts > Edit post")
print("  2. Yoast SEO > SEO tab > enter:")
print("     Title:  Best B2B Catalog Chatbots in 2026: 7 Tools Compared | ChatSKU")
print("     Desc:   ChatSKU, Algolia, Coveo, Bloomreach, Zoovu, HumCommerce, and Tidio")
print("             compared for B2B catalogs, RFQs, and tiered pricing.")
print("  (Yoast meta cannot be set via REST API on chatsku.com)")
print()
print(f"RESULTS_JSON={json.dumps({'post_id': post_id, 'post_link': post_link, 'feat_id': feat_media['id'], 'body1_id': body1_media['id'], 'body2_id': body2_media['id'], 'infographic_id': infographic_media['id']})}")
