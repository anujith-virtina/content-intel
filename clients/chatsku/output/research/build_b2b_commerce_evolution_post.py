"""
Build and publish: b2b-commerce-evolution
Post: "The 11 stages of B2B commerce evolution: where does your company actually stand?"
Format: Format C (listicle / thought-leadership)   Date: 2026-07-23

Parses the build-ready HTML draft directly:
  clients/chatsku/output/drafts/b2b-commerce-evolution-11-stages-BUILD.md

User-specified structure (no Exec summary / no FAQ): hook -> 11 stages -> gap ->
ChatCommerce -> data-first objection -> agentic commerce -> dark CTA box.
Images (Openverse cc0, visually QA'd 2026-07-23, NOT reused from post 1684):
  Featured evfeat_1.jpg  - multi-device business/tech meeting
  Body     evbody_2.jpg  - clean digital workspace (after the ChatCommerce section)
"""
import json, secrets, re, urllib.request, urllib.error, urllib.parse
import base64, os, io, sys, ssl
from pathlib import Path

_ssl_ctx = ssl._create_unverified_context()
_env_path = r"C:\content-intel\.env"
if os.path.exists(_env_path):
    with open(_env_path, encoding="utf-8") as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1); os.environ.setdefault(_k.strip(), _v.strip())

WP_BASE = "https://chatsku.com/wp-json/wp/v2"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
USERNAME = os.environ.get("CHATSKU_WP_USERNAME", ""); PASSWORD = os.environ.get("CHATSKU_WP_APP_PASSWORD", "")
if not USERNAME or not PASSWORD:
    print("ERROR: CHATSKU creds missing"); sys.exit(1)
AUTH = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
HEADERS = {"Authorization": f"Basic {AUTH}", "User-Agent": UA, "Content-Type": "application/json"}

DRAFT = r"C:\content-intel\clients\chatsku\output\drafts\b2b-commerce-evolution-11-stages-BUILD.md"
SCRATCH = r"C:\Users\ASUS\AppData\Local\Temp\claude\C--content-intel\d7aa1939-3bb2-49aa-ba16-e70373c2caf2\scratchpad"

TITLE = "The 11 stages of B2B commerce evolution: where does your company actually stand?"
SLUG = "b2b-commerce-evolution"
META_TITLE = "The 11 Stages of B2B Commerce Evolution | ChatSKU"
META_DESC = ("B2B commerce evolution spans 11 stages, from paper catalogs to agentic commerce. "
             "See which stage your company is stuck at and how to close the gap fast.")
FEAT_ALT = ("B2B distribution team reviewing digital commerce systems on multiple laptops, assessing "
            "where their company sits on the B2B commerce evolution timeline")
BODY_ALT = ("Clean digital workspace with a laptop on a desk, representing a modern AI-enabled B2B "
            "commerce platform that answers buyer questions from real catalog data")

CTA_KEY = "ready to move your catalog past stage 4?"
BODY_IMG_AFTER = "what chatcommerce looks like in practice"
DRY_RUN = bool(os.environ.get("DRY_RUN", ""))

# ── IMAGES ────────────────────────────────────────────────────────────────────
def resize_file(path, width=860, height=452, quality=82):
    from PIL import Image
    img = Image.open(path).convert("RGB"); sw, sh = img.size
    scale = max(width / sw, height / sh); nw, nh = int(sw * scale), int(sh * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    l, t = (nw - width) // 2, (nh - height) // 2; img = img.crop((l, t, l + width, t + height))
    buf = io.BytesIO(); img.save(buf, format="JPEG", quality=quality, optimize=True); data = buf.getvalue()
    if len(data) > 200 * 1024:
        buf = io.BytesIO(); img.save(buf, format="JPEG", quality=70, optimize=True); data = buf.getvalue()
    print(f"  Resized {os.path.basename(path)} -> {width}x{height}, {len(data)//1024}KB"); return data

def upload_image(jpeg, filename, alt):
    h = {"Authorization": f"Basic {AUTH}", "User-Agent": UA, "Content-Type": "image/jpeg",
         "Content-Disposition": f'attachment; filename="{filename}"'}
    with urllib.request.urlopen(urllib.request.Request(f"{WP_BASE}/media", data=jpeg, headers=h, method="POST"),
                                timeout=60, context=_ssl_ctx) as r:
        m = json.loads(r.read())
    urllib.request.urlopen(urllib.request.Request(f"{WP_BASE}/media/{m['id']}", data=json.dumps({"alt_text": alt}).encode(),
                           headers=HEADERS, method="POST"), timeout=20, context=_ssl_ctx).read()
    print(f"  Uploaded {filename}: ID={m['id']}  {m['source_url']}")
    return {"id": m["id"], "url": m["source_url"], "alt": alt}

def fetch_media(mid, alt):
    with urllib.request.urlopen(urllib.request.Request(f"{WP_BASE}/media/{mid}", headers=HEADERS),
                                timeout=20, context=_ssl_ctx) as r:
        m = json.loads(r.read())
    return {"id": int(mid), "url": m["source_url"], "alt": alt}

# ── PARSER ────────────────────────────────────────────────────────────────────
def load_draft():
    raw = Path(DRAFT).read_text(encoding="utf-8")
    raw = re.sub(r'^---.*?---\s*', '', raw, count=1, flags=re.S)
    return raw

def parse_sections(html):
    sections = []; cur = None
    for m in re.finditer(r'<(h1|h2|h3|p|ul|ol|table)\b[^>]*>.*?</\1>', html, re.S):
        tag = m.group(1); full = m.group(0)
        if tag == "h1":
            continue
        if tag == "h2":
            cur = (re.sub(r'^<[^>]+>|</[^>]+>$', '', full, flags=re.S).strip(), []); sections.append(cur)
        elif cur is not None:
            cur[1].append((tag, full))
    return sections

# ── ELEMENTOR ─────────────────────────────────────────────────────────────────
def gid(): return secrets.token_hex(4)

def w_heading(title, level="h2", color="#1a1a2e", align="left"):
    size = 28 if level == "h2" else 22
    s = {"title": title, "align": align, "title_color": color,
         "typography_typography": "custom", "typography_font_size": {"size": size, "unit": "px"}}
    if level != "h2": s["header_size"] = level
    return {"id": gid(), "elType": "widget", "widgetType": "heading", "elements": [], "settings": s}

def w_text(html, dark=False):
    if dark:
        html = re.sub(r'<p([ >])', r'<p style="color:#aaaacc;text-align:center;font-size:18px;max-width:720px;margin:0 auto 14px;"\1', html)
    return {"id": gid(), "elType": "widget", "widgetType": "text-editor", "elements": [], "settings": {"editor": html}}

def w_image(img):
    return {"id": gid(), "elType": "widget", "widgetType": "image", "elements": [],
            "settings": {"image": {"id": img["id"], "url": img["url"], "alt": img["alt"], "source": "library", "size": ""},
                         "align": "center", "width": {"size": 100, "unit": "%"},
                         "border_radius": {"top": "10", "right": "10", "bottom": "10", "left": "10", "unit": "px"}}}

def w_button(text, url):
    return {"id": gid(), "elType": "widget", "widgetType": "button", "elements": [],
            "settings": {"text": text, "link": {"url": url, "is_external": "", "nofollow": ""}, "align": "center",
                         "background_color": "#e94560", "button_text_color": "#ffffff", "border_radius": {"size": 6, "unit": "px"},
                         "_margin": {"unit": "px", "top": "22", "right": "0", "bottom": "0", "left": "0", "isLinked": False}}}

def section(widgets, bg, conclusion=False):
    sec_pad = {"top": "20", "bottom": "30", "unit": "px"} if conclusion else {"top": "60", "bottom": "60", "unit": "px"}
    col_pad = {"unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20", "isLinked": True}
    return {"id": gid(), "elType": "section", "isInner": False,
            "settings": {"background_background": "classic", "background_color": bg, "padding": sec_pad},
            "elements": [{"id": gid(), "elType": "column", "isInner": False,
                          "settings": {"_column_size": 100, "width": "100", "padding": col_pad}, "elements": widgets}]}

BG = {
    "which stage is your catalog actually stuck at?": "#f9f9fb",
    "the 11 stages of b2b commerce evolution": "#ffffff",
    "the gap between where you sit and what buyers expect": "#f0f4ff",
    "what chatcommerce looks like in practice": "#ffffff",
    "but we need to fix our data first": "#f9f9fb",
    "agentic commerce is the next frontier, so start moving now": "#ffffff",
    CTA_KEY: "#1a1a2e",
}

def build(sections_data, feat, body):
    out = []
    for heading, blocks in sections_data:
        key = heading.lower(); bg = BG.get(key, "#ffffff")
        if key == CTA_KEY:
            btext = "\n".join(full for tag, full in blocks if tag in ("p", "ul", "ol"))
            out.append(section([w_heading(heading, color="#ffffff", align="center"),
                                w_text(btext, dark=True), w_button("Book a live demo", "https://chatsku.com/demo/")],
                               bg="#1a1a2e", conclusion=True))
            continue
        widgets = [w_heading(heading)]; buf = []
        def flush():
            if buf: widgets.append(w_text("\n".join(buf))); buf.clear()
        for tag, full in blocks:
            if tag == "h3":
                flush(); widgets.append(w_heading(re.sub(r'^<[^>]+>|</[^>]+>$', '', full).strip(), level="h3"))
            else:
                buf.append(full)
        flush()
        if key == BODY_IMG_AFTER:
            widgets.append(w_image(body))
        out.append(section(widgets, bg=bg))
    return out

# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 66); print("BUILD: b2b-commerce-evolution (Format C, 2026-07-23)"); print("=" * 66)
html = load_draft()
sections_data = parse_sections(html)
print(f"Parsed {len(sections_data)} H2 sections:")
for h, b in sections_data: print(f"  - {h[:52]:52} ({len(b)} blocks)")

em = html.count("—") + html.count("&mdash;")
print(f"\nEm dash scan: {'PASS' if em == 0 else 'FAIL'} ({em})")
if em: sys.exit(1)

print("\n--- IMAGES ---")
REUSE = os.environ.get("REUSE_MEDIA", "")
if REUSE:
    fid, bid = [int(x) for x in REUSE.split(",")]
    feat, body = fetch_media(fid, FEAT_ALT), fetch_media(bid, BODY_ALT); print(f"Reusing media {fid},{bid}")
elif DRY_RUN:
    feat = {"id": 9001, "url": "https://chatsku.com/wp-content/uploads/dry-f.jpg", "alt": FEAT_ALT}
    body = {"id": 9002, "url": "https://chatsku.com/wp-content/uploads/dry-b.jpg", "alt": BODY_ALT}
    print("DRY_RUN placeholder media")
else:
    feat = upload_image(resize_file(os.path.join(SCRATCH, "evfeat_1.jpg")), "chatsku-b2b-commerce-evolution-featured.jpg", FEAT_ALT)
    body = upload_image(resize_file(os.path.join(SCRATCH, "evbody_2.jpg")), "chatsku-b2b-commerce-evolution-chatcommerce.jpg", BODY_ALT)
for lbl, m in [("Featured", feat), ("Body", body)]:
    if not DRY_RUN and not m["url"].startswith("https://chatsku.com/wp-content/uploads/"):
        print(f"FATAL: {lbl} URL invalid"); sys.exit(1)

elementor = build(sections_data, feat, body)
elementor_json = json.dumps(elementor)
print(f"\nBuilt {len(elementor)} sections:")
for i, s in enumerate(elementor):
    cols = s["elements"][0]["elements"]; types = [w.get("widgetType") for w in cols]
    h = next((w["settings"].get("title", "")[:40] for w in cols if w.get("widgetType") == "heading"), "?")
    order = ""
    if "image" in types and "text-editor" in types:
        order = "  img_order=" + ("OK" if types.index("image") > max(j for j, t in enumerate(types) if t == "text-editor") else "FAIL")
        if "FAIL" in order: print(f"  {i} [{h}] {types}{order}"); print("CRITICAL: image before text"); sys.exit(1)
    print(f"  {i:2} bg={s['settings']['background_color']} [{h}] {types}{order}")

print("\n--- CHECKLIST ---")
checks = {}
checks["No em dashes"] = em == 0
ext = re.findall(r'href="https?://(?!chatsku\.com)[^"]+', html); checks["External <=2"] = len(ext) <= 2
intl = re.findall(r'href="https://chatsku\.com/[^"]+', html); checks["Internal 3-9"] = 3 <= len(intl) <= 9
comp = ["drift.com", "intercom.com", "tidio.com", "zendesk.com", "bigcommerce.com", "livechat.com"]
checks["No competitor links"] = not any(c in html for c in comp)

def find_sec(tl):
    for s in elementor:
        cols = s["elements"][0]["elements"]
        if cols and cols[0].get("widgetType") == "heading" and cols[0]["settings"].get("title", "").lower() == tl:
            return s
    return None
cta = find_sec(CTA_KEY); ctaw = cta["elements"][0]["elements"] if cta else []
checks["CTA dark"] = bool(cta) and cta["settings"]["background_color"] == "#1a1a2e"
checks["CTA white heading"] = bool(ctaw) and ctaw[0]["settings"].get("title_color") == "#ffffff"
checks["CTA button"] = any(w.get("widgetType") == "button" for w in ctaw)
checks["CTA is last"] = bool(elementor) and elementor[-1] is cta
checks["Featured img set"] = bool(feat["id"])
wp_content = "<p>See the full formatted guide in the Elementor layout.</p>"
checks["No bare img"] = "<img" not in wp_content
wc = len(re.sub(r'<[^>]+>', ' ', html).split()); checks["Word count 800-1400"] = 800 <= wc <= 1400
checks["Meta title <=60"] = len(META_TITLE) <= 60
checks["Meta desc 150-160"] = 150 <= len(META_DESC) <= 160
for k, v in checks.items(): print(f"  [{'PASS' if v else 'FAIL'}] {k}")
print(f"  external={len(ext)} internal={len(intl)} words={wc} meta_title={len(META_TITLE)} meta_desc={len(META_DESC)}")
for il in intl: print(f"    INT {il[8:70]}")
if not all(checks.values()):
    print("FAILED:", [k for k, v in checks.items() if not v]); sys.exit(1)
print("\nCHECKLIST: ALL PASS")

if DRY_RUN:
    print("DRY_RUN done."); print(f"RESULTS_JSON={json.dumps({'sections': len(elementor), 'words': wc, 'internal': len(intl)})}"); sys.exit(0)

print("\n--- PUSH (draft) ---")
UPDATE = os.environ.get("UPDATE_POST_ID", "")
payload = {"title": TITLE, "slug": SLUG, "content": wp_content, "featured_media": feat["id"],
           "meta": {"_elementor_edit_mode": "builder", "_elementor_template_type": "wp-post", "_elementor_data": elementor_json}}
if UPDATE:
    forced = os.environ.get("FORCE_STATUS", "")
    if forced: payload["status"] = forced
    else:
        with urllib.request.urlopen(urllib.request.Request(f"{WP_BASE}/posts/{UPDATE}?context=edit", headers=HEADERS), timeout=20, context=_ssl_ctx) as r:
            cur = json.loads(r.read())
        print(f"Preserving live status: {cur.get('status')!r}")
else:
    payload["status"] = "draft"
url = f"{WP_BASE}/posts/{UPDATE}" if UPDATE else f"{WP_BASE}/posts"
try:
    with urllib.request.urlopen(urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=HEADERS, method="POST"), timeout=120, context=_ssl_ctx) as r:
        resp = json.loads(r.read())
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read()[:600]}"); sys.exit(1)
post_id = resp["id"]; print(f"PUSH OK  id={post_id}  status={resp.get('status')}  link={resp.get('link')}")
with urllib.request.urlopen(urllib.request.Request(f"{WP_BASE}/posts/{post_id}?context=edit", headers=HEADERS), timeout=30, context=_ssl_ctx) as r:
    ver = json.loads(r.read())
print(f"Verified: sections={len(json.loads(ver.get('meta', {}).get('_elementor_data', '[]')))} featured_media={ver.get('featured_media')} status={ver.get('status')}")
print("Clearing Elementor cache...")
try:
    with urllib.request.urlopen(urllib.request.Request("https://chatsku.com/wp-json/elementor/v1/cache", headers={"Authorization": f"Basic {AUTH}", "User-Agent": UA}, method="DELETE"), timeout=20, context=_ssl_ctx) as r:
        print(f"  cache: HTTP {r.status}")
except Exception as e:
    print(f"  cache: {e}")
print("\n" + "=" * 66); print("PUBLISH COMPLETE")
print(f"  Post ID: {post_id}  status: {resp.get('status')}")
print(f"  Media: feat={feat['id']} body={body['id']}  Sections: {len(elementor)}  Words: {wc}")
print(f"  Yoast title ({len(META_TITLE)}): {META_TITLE}")
print(f"  Yoast desc  ({len(META_DESC)}): {META_DESC}")
print(f"RESULTS_JSON={json.dumps({'post_id': post_id, 'link': resp.get('link'), 'feat': feat['id'], 'body': body['id'], 'sections': len(elementor), 'words': wc, 'internal': len(intl)})}")
