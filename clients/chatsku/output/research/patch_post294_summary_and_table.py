"""
Patch post 294 (best-b2b-catalog-chatbots-2026):
  1. Add Executive summary + Introduction H2 headings (were missing -- flagged by user)
  2. Add inline-styled comparison table (was unstyled plain HTML -- flagged by user)

Reuses already-uploaded media IDs (290 featured, 291 body1, 292 body2, 293 infographic).
Rebuilds Elementor JSON from the updated draft and PUTs to the existing post (no new post).
"""

import json, secrets, re, urllib.request, urllib.error
import base64, os, sys, ssl
from pathlib import Path

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
AUTH = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
HEADERS = {"Authorization": f"Basic {AUTH}", "User-Agent": UA, "Content-Type": "application/json"}

POST_ID = 294
MEDIA = {
    "featured": {"id": 290, "url": "https://chatsku.com/wp-content/uploads/2026/06/chatsku-best-b2b-catalog-chatbots-featured.jpg",
                 "alt": "B2B sales manager presenting catalog chatbot vendor options to a small team during a software evaluation meeting"},
    "body1":    {"id": 291, "url": "https://chatsku.com/wp-content/uploads/2026/06/chatsku-best-b2b-catalog-chatbots-body1.jpg",
                 "alt": "Distributor employee reviewing B2B catalog pricing data on a laptop dashboard with a calculator, checking customer-specific rates"},
    "body2":    {"id": 292, "url": "https://chatsku.com/wp-content/uploads/2026/06/chatsku-best-b2b-catalog-chatbots-body2.jpg",
                 "alt": "B2B sales team reviewing chatbot vendor options together on laptops around an office table"},
    "infographic": {"id": 293, "url": "https://chatsku.com/wp-content/uploads/2026/06/chatsku-best-b2b-catalog-chatbots-infographic.jpg",
                 "alt": "Infographic comparing deployment speed and annual cost for seven B2B catalog chatbot vendors including ChatSKU, Algolia, Coveo, and Tidio"},
}

DRAFT_PATH = Path(r"C:\content-intel\clients\chatsku\output\drafts\best-b2b-catalog-chatbots-2026-2026-06-17.md")
_raw = DRAFT_PATH.read_text(encoding="utf-8")
_parts = _raw.split("---", 2)
DRAFT_HTML = _parts[2].strip() if len(_parts) >= 3 else _raw.strip()

em_count = DRAFT_HTML.count("—") + DRAFT_HTML.count("&mdash;")
assert em_count == 0, f"ERROR: {em_count} em dashes found"
print(f"Em dash scan: PASS (0 found)")

def gid():
    return secrets.token_hex(4)

def make_heading(title, level="h2", color="#1a1a2e", align="left"):
    size = 28 if level == "h2" else 22
    s = {"title": title, "align": align, "title_color": color,
         "typography_font_size": {"size": size, "unit": "px"}}
    if level != "h2":
        s["header_size"] = level
    return {"id": gid(), "elType": "widget", "widgetType": "heading", "elements": [], "settings": s}

def make_text(html, dark_section=False):
    html = re.sub(r'href="/([\w/\-]+)"', r'href="https://chatsku.com/\1"', html)
    html = re.sub(r'<img[^>]*>', '', html).strip()
    if dark_section:
        html = re.sub(r'<p([ >])', r'<p style="color:#aaaacc;text-align:center;font-size:18px;max-width:720px;margin:0 auto;"\1', html)
    return {"id": gid(), "elType": "widget", "widgetType": "text-editor", "elements": [], "settings": {"editor": html}}

def make_image_widget(img_data):
    return {"id": gid(), "elType": "widget", "widgetType": "image", "elements": [],
            "settings": {"image": {"id": img_data["id"], "url": img_data["url"], "alt": img_data["alt"], "source": "library", "size": ""},
                          "align": "center", "width": {"size": 100, "unit": "%"},
                          "border_radius": {"top": "10", "right": "10", "bottom": "10", "left": "10", "unit": "px"}}}

def make_button(text, url):
    return {"id": gid(), "elType": "widget", "widgetType": "button", "elements": [],
            "settings": {"text": text, "link": {"url": url, "is_external": "true"}, "align": "center",
                          "background_color": "#e94560", "button_text_color": "#ffffff",
                          "border_radius": {"size": 6, "unit": "px"},
                          "_margin": {"unit": "px", "top": "20", "right": "0", "bottom": "0", "left": "0", "isLinked": False}}}

def make_section(widgets, bg, is_conclusion=False):
    sec_pad = {"top": "20", "bottom": "30", "unit": "px", "right": "0", "left": "0"} if is_conclusion else {"top": "60", "bottom": "60", "unit": "px"}
    col_pad = {"unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20", "isLinked": True}
    return {"id": gid(), "elType": "section", "isInner": False,
            "settings": {"background_background": "classic", "background_color": bg, "padding": sec_pad},
            "elements": [{"id": gid(), "elType": "column", "isInner": False,
                          "settings": {"_column_size": 100, "width": "100", "padding": col_pad},
                          "elements": widgets}]}

def parse_h3_blocks(body_html):
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

def build_elementor():
    BODY_COLORS = ["#f0f4ff", "#ffffff", "#f9f9fb", "#ffffff"]
    body_color_idx = 0
    sections = []
    html = re.sub(r'<h1[^>]*>.*?</h1>', '', DRAFT_HTML, count=1, flags=re.DOTALL).strip()
    chunks = [c.strip() for c in re.split(r'(?=<h2[^>]*>)', html) if c.strip()]

    for chunk in chunks:
        hm = re.match(r'<h2[^>]*>(.*?)</h2>(.*)', chunk, re.DOTALL)
        if not hm:
            continue
        h2_text, body_html = hm.group(1).strip(), hm.group(2).strip()
        label = h2_text.lower()

        if "executive summary" in label:
            sections.append(make_section([make_heading(h2_text), make_text(body_html)], bg="#f9f9fb"))
            continue
        if label.strip() == "introduction":
            sections.append(make_section([make_heading(h2_text), make_text(body_html)], bg="#ffffff"))
            continue
        if "conclusion" in label:
            widgets = [make_heading(h2_text, color="#ffffff", align="center"),
                       make_text(body_html, dark_section=True),
                       make_button("Start your free trial", "https://chatsku.com/signup/")]
            sections.append(make_section(widgets, bg="#1a1a2e", is_conclusion=True))
            continue
        if "frequently asked questions" in label:
            widgets = [make_heading(h2_text)]
            lead, blocks = parse_h3_blocks(body_html)
            if lead: widgets.append(make_text(lead))
            for h3_text, h3_body in blocks:
                widgets.append(make_heading(h3_text, "h3"))
                if h3_body: widgets.append(make_text(h3_body))
            sections.append(make_section(widgets, bg="#f9f9fb"))
            continue
        if "people also ask" in label:
            widgets = [make_heading(h2_text)]
            lead, blocks = parse_h3_blocks(body_html)
            if lead: widgets.append(make_text(lead))
            for h3_text, h3_body in blocks:
                widgets.append(make_heading(h3_text, "h3"))
                if h3_body: widgets.append(make_text(h3_body))
            bg = BODY_COLORS[body_color_idx % len(BODY_COLORS)]; body_color_idx += 1
            sections.append(make_section(widgets, bg=bg))
            continue
        if label.strip() == "best b2b catalog chatbots in 2026":
            widgets = [make_heading(h2_text)]
            lead, blocks = parse_h3_blocks(body_html)
            if lead: widgets.append(make_text(lead))
            for h3_text, h3_body in blocks:
                widgets.append(make_heading(h3_text, "h3"))
                if h3_body: widgets.append(make_text(h3_body))
            widgets.append(make_image_widget(MEDIA["body2"]))
            bg = BODY_COLORS[body_color_idx % len(BODY_COLORS)]; body_color_idx += 1
            sections.append(make_section(widgets, bg=bg))
            continue

        widgets = [make_heading(h2_text)]
        if body_html: widgets.append(make_text(body_html))
        if "what makes a b2b catalog chatbot different" in label:
            widgets.append(make_image_widget(MEDIA["body1"]))
        elif "how do these b2b catalog chatbots compare" in label:
            widgets.append(make_image_widget(MEDIA["infographic"]))
        bg = BODY_COLORS[body_color_idx % len(BODY_COLORS)]; body_color_idx += 1
        sections.append(make_section(widgets, bg=bg))

    return sections

sections = build_elementor()
elementor_json = json.dumps(sections)
print(f"Built {len(sections)} sections, {len(elementor_json):,} chars")

for i, s in enumerate(sections):
    types = [w.get("widgetType") for w in s["elements"][0]["elements"]]
    h = next((w["settings"].get("title","")[:40] for w in s["elements"][0]["elements"] if w.get("widgetType")=="heading"), "(no heading)")
    if "image" in types and "text-editor" in types:
        ok = max(i for i,t in enumerate(types) if t=="image") > max(i for i,t in enumerate(types) if t=="text-editor")
        if not ok:
            print(f"FATAL: image before text-editor in section {i} [{h}]"); sys.exit(1)
    print(f"  {i:2}: bg={s['settings']['background_color']}  [{h}]  widgets={len(types)}")

wp_content = re.sub(r'<h1[^>]*>.*?</h1>', '', DRAFT_HTML, flags=re.DOTALL).strip()
wp_content = re.sub(r'<img[^>]*>', '', wp_content).strip()
assert not re.search(r'<img[^>]*>', wp_content), "bare img tags remain"

payload = {
    "content": wp_content,
    "meta": {
        "_elementor_edit_mode": "builder",
        "_elementor_template_type": "wp-post",
        "_elementor_data": elementor_json
    }
}
payload_bytes = json.dumps(payload).encode("utf-8")
print(f"Payload: {len(payload_bytes):,} bytes")

req = urllib.request.Request(f"{WP_BASE}/posts/{POST_ID}", data=payload_bytes, headers=HEADERS, method="POST")
try:
    with urllib.request.urlopen(req, timeout=120, context=_ssl_ctx) as r:
        resp = json.loads(r.read())
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read()[:600]}"); sys.exit(1)

print(f"PATCH SUCCESS: post {resp['id']} status={resp.get('status')} link={resp.get('link')}")

cache_req = urllib.request.Request("https://chatsku.com/wp-json/elementor/v1/cache",
                                    headers={"Authorization": f"Basic {AUTH}", "User-Agent": UA}, method="DELETE")
try:
    with urllib.request.urlopen(cache_req, timeout=20, context=_ssl_ctx) as r:
        print(f"Cache clear: HTTP {r.status}")
except urllib.error.HTTPError as e:
    print(f"Cache clear HTTP {e.code}: {e.read()[:200]}")

req_v = urllib.request.Request(f"{WP_BASE}/posts/{POST_ID}?context=edit", headers=HEADERS)
with urllib.request.urlopen(req_v, timeout=30, context=_ssl_ctx) as r:
    verified = json.loads(r.read())
saved_ed = json.loads(verified["meta"]["_elementor_data"])
print(f"Verified: {len(saved_ed)} sections saved, status={verified.get('status')}")
headings = [w["settings"]["title"] for s in saved_ed for w in s["elements"][0]["elements"] if w.get("widgetType")=="heading"]
print("Headings now present:", headings[:4])
