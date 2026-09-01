"""
Build and publish: rfq-form-best-practices
Post: "RFQ form best practices: 15 proven ways to generate more qualified quote requests"
Format: Format C (listicle with opinions)   Date: 2026-07-17

Parses the APPROVED draft HTML directly (fidelity > hand-transcription):
  clients/chatsku/output/drafts/rfq-form-best-practices-2026-07-17.md

Pipeline:
  1. Load .env credentials (CHATSKU_* only)
  2. Resize + upload 3 visually-QA'd local images (860x452) OR reuse via REUSE_MEDIA
  3. Parse draft -> Elementor sections (1 per H2), heading/text/image widgets
     - Mistakes table restyled inline (navy header, alt rows, mobile scroll)
     - FAQ rendered as native Elementor accordion (accordion.default) AFTER conclusion
     - Conclusion = heading(white,center) + styled body (keeps 1 contextual 251 link) + button
     - Body image widget LAST in its section (Elementor 4.0.3 order bug)
  4. Full pre-publish checklist
  5. Push draft, verify, clear Elementor cache, save published HTML

Image provenance (Openverse license=cc0, StockSnap origin, visually QA'd 2026-07-20):
  Featured feat_3.jpg  - two people reviewing a marked-up document w/ laptops
  Body1    feat_0.jpg  - team collaborating over documents + laptop
  Body2    body2_1.jpg - professional using a tablet in a modern office
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
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

WP_BASE = "https://chatsku.com/wp-json/wp/v2"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
USERNAME = os.environ.get("CHATSKU_WP_USERNAME", "")
PASSWORD = os.environ.get("CHATSKU_WP_APP_PASSWORD", "")
if not USERNAME or not PASSWORD:
    print("ERROR: CHATSKU_WP_USERNAME / CHATSKU_WP_APP_PASSWORD not set"); sys.exit(1)

AUTH = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
HEADERS = {"Authorization": f"Basic {AUTH}", "User-Agent": UA, "Content-Type": "application/json"}

DRAFT = r"C:\content-intel\clients\chatsku\output\drafts\rfq-form-best-practices-2026-07-17.md"
SCRATCH = r"C:\Users\ASUS\AppData\Local\Temp\claude\C--content-intel\d7aa1939-3bb2-49aa-ba16-e70373c2caf2\scratchpad"

TITLE = "RFQ form best practices: 15 proven ways to generate more qualified quote requests"
SLUG = "rfq-form-best-practices"
META_TITLE = "RFQ Form Best Practices: 15 Ways to Convert Buyers | ChatSKU"
META_DESC = ("15 evidence-backed RFQ form best practices for B2B sellers, covering field count, "
             "mobile UX, inline validation, trust signals, file uploads, and A/B testing.")

FEAT_ALT = ("Two B2B sales staff reviewing a submitted RFQ form and spec document on laptops, "
            "checking quote request details in an office")
BODY1_ALT = ("Distributor sales team reviewing quote request paperwork together at an office "
             "desk with a laptop during RFQ lead follow-up")
BODY2_ALT = ("B2B buyer completing a multi-step RFQ form on a tablet in a modern office, an "
             "example of clean quote request form UX")

DRY_RUN = bool(os.environ.get("DRY_RUN", ""))

# ── IMAGE HELPERS ─────────────────────────────────────────────────────────────
def resize_file(path, width=860, height=452, quality=82):
    from PIL import Image
    img = Image.open(path).convert("RGB")
    sw, sh = img.size
    scale = max(width / sw, height / sh)
    nw, nh = int(sw * scale), int(sh * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - width) // 2, (nh - height) // 2
    img = img.crop((left, top, left + width, top + height))
    buf = io.BytesIO(); img.save(buf, format="JPEG", quality=quality, optimize=True)
    data = buf.getvalue()
    if len(data) > 200 * 1024:
        buf = io.BytesIO(); img.save(buf, format="JPEG", quality=70, optimize=True); data = buf.getvalue()
    print(f"  Resized {os.path.basename(path)} -> {width}x{height}, {len(data)//1024}KB")
    return data

def upload_image(jpeg, filename, alt):
    h = {"Authorization": f"Basic {AUTH}", "User-Agent": UA, "Content-Type": "image/jpeg",
         "Content-Disposition": f'attachment; filename="{filename}"'}
    req = urllib.request.Request(f"{WP_BASE}/media", data=jpeg, headers=h, method="POST")
    with urllib.request.urlopen(req, timeout=60, context=_ssl_ctx) as r:
        m = json.loads(r.read())
    urllib.request.urlopen(urllib.request.Request(
        f"{WP_BASE}/media/{m['id']}", data=json.dumps({"alt_text": alt}).encode(),
        headers=HEADERS, method="POST"), timeout=20, context=_ssl_ctx).read()
    print(f"  Uploaded {filename}: ID={m['id']}  {m['source_url']}")
    return {"id": m["id"], "url": m["source_url"], "alt": alt}

def fetch_media(mid, alt):
    with urllib.request.urlopen(urllib.request.Request(f"{WP_BASE}/media/{mid}", headers=HEADERS),
                                timeout=20, context=_ssl_ctx) as r:
        m = json.loads(r.read())
    return {"id": int(mid), "url": m["source_url"], "alt": alt}

# ── DRAFT PARSER ──────────────────────────────────────────────────────────────
def load_draft():
    raw = Path(DRAFT).read_text(encoding="utf-8")
    # strip YAML frontmatter (first two --- delimited block)
    raw = re.sub(r'^---.*?---\s*', '', raw, count=1, flags=re.S)
    # strip HTML comment (SEO block)
    raw = re.sub(r'<!--.*?-->', '', raw, flags=re.S)
    # strip image placeholder markers
    raw = re.sub(r'\[FEATURED IMAGE.*?\]', '', raw, flags=re.S)
    raw = re.sub(r'\[BODY IMAGE.*?\]', '', raw, flags=re.S)
    return raw

def parse_sections(html):
    """Return list of (heading_text, [ (tag, inner_or_full) ... ]) in document order.
    Blocks after the H1 are grouped under the preceding H2."""
    sections = []
    cur = None
    for m in re.finditer(r'<(h1|h2|h3|p|ul|table)\b[^>]*>.*?</\1>', html, re.S):
        tag = m.group(1); full = m.group(0)
        inner = re.sub(r'^<[^>]+>|</[^>]+>$', '', full, flags=re.S).strip() if tag in ("h1", "h2", "h3") else full
        if tag == "h1":
            continue
        if tag == "h2":
            cur = (inner.strip(), [])
            sections.append(cur)
        else:
            if cur is None:
                continue
            cur[1].append((tag, full))
    return sections

# ── TABLE RESTYLE ─────────────────────────────────────────────────────────────
def style_table(t):
    t = t.replace('<table>',
                  '<table style="border-collapse:collapse;width:100%;font-size:15px;min-width:640px;">')
    t = t.replace('<th>',
                  '<th style="background:#1a1a2e;color:#ffffff;padding:11px 14px;text-align:left;font-weight:600;">')
    t = t.replace('<td>',
                  '<td style="padding:11px 14px;border-bottom:1px solid #e2e2ea;vertical-align:top;">')
    idx = [0]
    def rowrepl(m):
        row = m.group(0)
        if '<td' in row:
            bg = '#f0f4ff' if idx[0] % 2 == 0 else '#ffffff'
            idx[0] += 1
            return row.replace('<tr>', f'<tr style="background:{bg};">', 1)
        return row
    t = re.sub(r'<tr>.*?</tr>', rowrepl, t, flags=re.S)
    return '<div style="overflow-x:auto;">' + t + '</div>'

# ── ELEMENTOR BUILDERS ────────────────────────────────────────────────────────
def gid(): return secrets.token_hex(4)

def w_heading(title, level="h2", color="#1a1a2e", align="left"):
    size = 28 if level == "h2" else 22
    s = {"title": title, "align": align, "title_color": color,
         "typography_typography": "custom", "typography_font_size": {"size": size, "unit": "px"}}
    if level != "h2":
        s["header_size"] = level
    return {"id": gid(), "elType": "widget", "widgetType": "heading", "elements": [], "settings": s}

def w_text(html, dark=False):
    if dark:
        html = re.sub(r'<p([ >])',
                      r'<p style="color:#aaaacc;text-align:center;font-size:18px;max-width:720px;margin:0 auto 14px;"\1',
                      html)
    return {"id": gid(), "elType": "widget", "widgetType": "text-editor", "elements": [],
            "settings": {"editor": html}}

def w_image(img):
    return {"id": gid(), "elType": "widget", "widgetType": "image", "elements": [],
            "settings": {"image": {"id": img["id"], "url": img["url"], "alt": img["alt"],
                                   "source": "library", "size": ""},
                         "align": "center", "width": {"size": 100, "unit": "%"},
                         "border_radius": {"top": "10", "right": "10", "bottom": "10", "left": "10", "unit": "px"}}}

def w_button(text, url):
    return {"id": gid(), "elType": "widget", "widgetType": "button", "elements": [],
            "settings": {"text": text, "link": {"url": url, "is_external": "", "nofollow": ""},
                         "align": "center", "background_color": "#e94560",
                         "button_text_color": "#ffffff", "border_radius": {"size": 6, "unit": "px"},
                         "_margin": {"unit": "px", "top": "22", "right": "0", "bottom": "0", "left": "0", "isLinked": False}}}

def w_accordion(items):
    tabs = [{"_id": gid(), "tab_title": q, "tab_content": f"<p>{a}</p>"} for q, a in items]
    return {"id": gid(), "elType": "widget", "widgetType": "accordion", "elements": [],
            "settings": {"tabs": tabs, "title_html_tag": "h3", "icon_active": {"value": "fas fa-minus", "library": "fa-solid"},
                         "icon": {"value": "fas fa-plus", "library": "fa-solid"}}}

def w_html(html):
    return {"id": gid(), "elType": "widget", "widgetType": "html", "elements": [],
            "settings": {"html": html}}

def section(widgets, bg, conclusion=False):
    sec_pad = {"top": "20", "bottom": "30", "unit": "px"} if conclusion else {"top": "60", "bottom": "60", "unit": "px"}
    col_pad = {"unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20", "isLinked": True}
    return {"id": gid(), "elType": "section", "isInner": False,
            "settings": {"background_background": "classic", "background_color": bg, "padding": sec_pad},
            "elements": [{"id": gid(), "elType": "column", "isInner": False,
                          "settings": {"_column_size": 100, "width": "100", "padding": col_pad},
                          "elements": widgets}]}

BG = {
    "executive summary": "#f9f9fb",
    "introduction": "#ffffff",
    "what is an rfq form?": "#f0f4ff",
    "why rfq forms matter in b2b lead generation": "#ffffff",
    "why most rfq forms fail": "#f9f9fb",
    "15 rfq form best practices": "#ffffff",
    "common rfq form mistakes": "#f0f4ff",
    "rfq form design examples": "#ffffff",
    "rfq form optimization checklist": "#f9f9fb",
    "people also ask": "#ffffff",
    "conclusion": "#f0f4ff",
    "frequently asked questions": "#f9f9fb",
    "ready to capture the quote requests your form is losing?": "#1a1a2e",
}

CONCLUSION_BODY = (
    "<p>Every practice on this list raises the ceiling on how well a static RFQ form can perform. "
    "Field staging, mobile input types, validation timing, page speed, testing discipline, all of it "
    "compounds into a form that converts noticeably better than the one you're running today.</p>"
    "<p>But even a form that checks every box here assumes one thing: the buyer already knows the exact "
    "part number, spec, or grade to type into the field. For a catalog with a few hundred SKUs, that's "
    "usually true. For a catalog with a few thousand, tiered pricing, and buyers mid-research who can "
    "describe what they need but not name it, that assumption is the ceiling no amount of form polish "
    "removes. We covered exactly that floor problem in our piece on "
    "<a href=\"https://chatsku.com/rfq-form-conversion-rate/\">RFQ conversion benchmarks</a> and what "
    "drives them upstream of the form itself. A catalog-native conversational path lets a buyer describe "
    "what they need in plain language and builds the structured RFQ behind the scenes, no part number "
    "required upfront.</p>"
    "<p>Start with the 15 practices above. Then see what a catalog-native quote path looks like on your "
    "own product data.</p>"
)

def build(sections_data, feat, body1, body2):
    out = []
    faq_items = []
    for heading, blocks in sections_data:
        key = heading.lower()
        bg = BG.get(key, "#ffffff")

        # Final dark CTA box (matches every live ChatSKU post: heading + styled body + button, AFTER the FAQ)
        if key == "ready to capture the quote requests your form is losing?":
            body = "\n".join(full for tag, full in blocks if tag in ("p", "ul"))
            out.append(section([
                w_heading(heading, color="#ffffff", align="center"),
                w_text(body, dark=True),
                w_button("Book a live demo", "https://chatsku.com/demo/"),
            ], bg="#1a1a2e", conclusion=True))
            continue

        if key == "frequently asked questions":
            for tag, full in blocks:
                if tag == "h3":
                    q = re.sub(r'^<[^>]+>|</[^>]+>$', '', full).strip()
                    faq_items.append([q, None])
                elif tag == "p" and faq_items and faq_items[-1][1] is None:
                    a = re.sub(r'^<p[^>]*>|</p>$', '', full, flags=re.S).strip()
                    faq_items[-1][1] = a
            faq_items = [(q, a) for q, a in faq_items if a]
            # No schema HTML widget: an Elementor HTML widget renders <script> JSON-LD as
            # visible raw text on the page. Prior ChatSKU posts leave Article/FAQ schema to Yoast.
            widgets = [w_heading("Frequently asked questions"), w_accordion(faq_items)]
            out.append(section(widgets, bg=bg))
            continue

        widgets = [w_heading(heading)]
        buf = []
        def flush():
            if buf:
                widgets.append(w_text("\n".join(buf)))
                buf.clear()
        for tag, full in blocks:
            if tag == "h3":
                flush()
                h3text = re.sub(r'^<[^>]+>|</[^>]+>$', '', full).strip()
                widgets.append(w_heading(h3text, level="h3"))
            elif tag == "table":
                flush()
                widgets.append(w_text(style_table(full)))
            else:  # p, ul
                buf.append(full)
        flush()
        if key == "15 rfq form best practices":
            widgets.append(w_image(body1))
        elif key == "rfq form design examples":
            widgets.append(w_image(body2))
        out.append(section(widgets, bg=bg))
    return out, faq_items

def build_schema(faq_items):
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q,
                           "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_items]}
    article = {"@context": "https://schema.org", "@type": "Article",
               "headline": TITLE, "description": META_DESC,
               "author": {"@type": "Organization", "name": "ChatSKU"},
               "publisher": {"@type": "Organization", "name": "ChatSKU"},
               "mainEntityOfPage": f"https://chatsku.com/{SLUG}/"}
    crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList",
             "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://chatsku.com/"},
                 {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://chatsku.com/blog/"},
                 {"@type": "ListItem", "position": 3, "name": TITLE, "item": f"https://chatsku.com/{SLUG}/"}]}
    return ("<script type=\"application/ld+json\">" + json.dumps(article) + "</script>"
            "<script type=\"application/ld+json\">" + json.dumps(faq) + "</script>"
            "<script type=\"application/ld+json\">" + json.dumps(crumb) + "</script>")

# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 66)
print("BUILD: rfq-form-best-practices  (Format C, 2026-07-17)")
print("=" * 66)

html = load_draft()
sections_data = parse_sections(html)
print(f"Parsed {len(sections_data)} H2 sections:")
for h, b in sections_data:
    print(f"  - {h[:50]:50} ({len(b)} blocks)")

# em dash guard
all_text = html
em = all_text.count("—") + all_text.count("&mdash;")
print(f"\nEm dash scan: {'PASS' if em == 0 else 'FAIL'} ({em})")
if em: sys.exit(1)

# ── IMAGES ────────────────────────────────────────────────────────────────────
print("\n--- IMAGES ---")
REUSE = os.environ.get("REUSE_MEDIA", "")
if REUSE:
    fid, b1, b2 = [int(x) for x in REUSE.split(",")]
    feat, body1, body2 = fetch_media(fid, FEAT_ALT), fetch_media(b1, BODY1_ALT), fetch_media(b2, BODY2_ALT)
    print(f"Reusing media {fid},{b1},{b2}")
elif DRY_RUN:
    feat = {"id": 9001, "url": "https://chatsku.com/wp-content/uploads/dry-feat.jpg", "alt": FEAT_ALT}
    body1 = {"id": 9002, "url": "https://chatsku.com/wp-content/uploads/dry-b1.jpg", "alt": BODY1_ALT}
    body2 = {"id": 9003, "url": "https://chatsku.com/wp-content/uploads/dry-b2.jpg", "alt": BODY2_ALT}
    print("DRY_RUN: using placeholder media")
else:
    feat = upload_image(resize_file(os.path.join(SCRATCH, "feat_3.jpg")),
                        "chatsku-rfq-form-best-practices-featured.jpg", FEAT_ALT)
    body1 = upload_image(resize_file(os.path.join(SCRATCH, "feat_0.jpg")),
                         "chatsku-rfq-form-best-practices-team-review.jpg", BODY1_ALT)
    body2 = upload_image(resize_file(os.path.join(SCRATCH, "body2_1.jpg")),
                         "chatsku-rfq-form-best-practices-tablet-form.jpg", BODY2_ALT)

for lbl, m in [("Featured", feat), ("Body1", body1), ("Body2", body2)]:
    if not DRY_RUN and not m["url"].startswith("https://chatsku.com/wp-content/uploads/"):
        print(f"FATAL: {lbl} URL invalid: {m['url']}"); sys.exit(1)

# ── BUILD JSON ────────────────────────────────────────────────────────────────
elementor, faq_items = build(sections_data, feat, body1, body2)
elementor_json = json.dumps(elementor)
print(f"\nBuilt {len(elementor)} Elementor sections. FAQ items: {len(faq_items)}")
for i, s in enumerate(elementor):
    cols = s["elements"][0]["elements"]
    types = [w.get("widgetType") for w in cols]
    h = next((w["settings"].get("title", "")[:42] for w in cols if w.get("widgetType") == "heading"), "?")
    order = ""
    if "image" in types and "text-editor" in types:
        order = "  img_order=" + ("OK" if types.index("image") > max(j for j, t in enumerate(types) if t == "text-editor") else "FAIL")
        if "FAIL" in order:
            print(f"  {i:2} bg={s['settings']['background_color']} [{h}] {types}{order}")
            print("  CRITICAL: image before text-editor"); sys.exit(1)
    print(f"  {i:2} bg={s['settings']['background_color']} [{h}] {types}{order}")

# ── CHECKLIST ─────────────────────────────────────────────────────────────────
print("\n--- PRE-PUBLISH CHECKLIST ---")
checks = {}
checks["No em dashes"] = em == 0
ext = re.findall(r'href="https?://(?!chatsku\.com)[^"]+', html)
checks["External <=2"] = len(ext) <= 2
intl = re.findall(r'href="https://chatsku\.com/[^"]+', html)
checks["Internal 5-10"] = 5 <= len(intl) <= 10
comp = ["drift.com", "intercom.com", "tidio.com", "zendesk.com", "bigcommerce.com", "livechat.com"]
checks["No competitor links"] = not any(c in html for c in comp)
checks["Exec summary first"] = sections_data[0][0].lower() == "executive summary"

def find_sec(title_lower):
    for s in elementor:
        cols = s["elements"][0]["elements"]
        if cols and cols[0].get("widgetType") == "heading" and cols[0]["settings"].get("title", "").lower() == title_lower:
            return s
    return None

conc = find_sec("conclusion")
checks["Conclusion heading present"] = bool(conc)
checks["Conclusion is light"] = bool(conc) and conc["settings"]["background_color"] != "#1a1a2e"
checks["Conclusion no button"] = bool(conc) and not any(w.get("widgetType") == "button" for w in conc["elements"][0]["elements"])

cta = find_sec("ready to capture the quote requests your form is losing?")
ctaw = cta["elements"][0]["elements"] if cta else []
checks["CTA dark"] = bool(cta) and cta["settings"]["background_color"] == "#1a1a2e"
checks["CTA white heading"] = bool(ctaw) and ctaw[0]["settings"].get("title_color") == "#ffffff"
checks["CTA button"] = any(w.get("widgetType") == "button" for w in ctaw)
checks["CTA is last section"] = bool(elementor) and elementor[-1] is cta
checks["FAQ accordion"] = any(w.get("widgetType") == "accordion"
                              for s in elementor for w in s["elements"][0]["elements"])
checks["FAQ count 8"] = len(faq_items) == 8
wp_content = "<p>See the full formatted guide in the Elementor layout.</p>"
checks["No bare img in content"] = "<img" not in wp_content
plain = re.sub(r'<[^>]+>', ' ', html)
wc = len(plain.split())
# wc here is FULL rendered count (prose ~3620 + table + checklist + 8-Q FAQ); band widened accordingly
checks["Word count (rendered)"] = 2900 <= wc <= 4400
checks["Meta title <=60"] = len(META_TITLE) <= 60
checks["Meta desc 150-160"] = 150 <= len(META_DESC) <= 160

for k, v in checks.items():
    print(f"  [{'PASS' if v else 'FAIL'}] {k}")
print(f"  external={len(ext)} internal={len(intl)} words={wc} meta_title={len(META_TITLE)} meta_desc={len(META_DESC)}")
for e in ext: print(f"    EXT {e[:75]}")

if not all(checks.values()):
    print("\nCHECKLIST FAILED:", [k for k, v in checks.items() if not v]); sys.exit(1)
print("\nCHECKLIST: ALL PASS")

if DRY_RUN:
    print("\nDRY_RUN complete — no push.")
    print(f"RESULTS_JSON={json.dumps({'sections': len(elementor), 'faq': len(faq_items), 'words': wc, 'internal': len(intl), 'external': len(ext)})}")
    sys.exit(0)

# ── PUSH ──────────────────────────────────────────────────────────────────────
print("\n--- PUSH (draft) ---")
UPDATE = os.environ.get("UPDATE_POST_ID", "")
payload = {"title": TITLE, "slug": SLUG, "content": wp_content, "featured_media": feat["id"],
           "meta": {"_elementor_edit_mode": "builder", "_elementor_template_type": "wp-post",
                    "_elementor_data": elementor_json}}
if UPDATE:
    forced = os.environ.get("FORCE_STATUS", "")
    if forced:
        payload["status"] = forced
    else:
        with urllib.request.urlopen(urllib.request.Request(
                f"{WP_BASE}/posts/{UPDATE}?context=edit", headers=HEADERS), timeout=20, context=_ssl_ctx) as r:
            cur = json.loads(r.read())
        print(f"Preserving live status: {cur.get('status')!r}")
else:
    payload["status"] = "draft"

url = f"{WP_BASE}/posts/{UPDATE}" if UPDATE else f"{WP_BASE}/posts"
try:
    with urllib.request.urlopen(urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"), headers=HEADERS, method="POST"),
            timeout=120, context=_ssl_ctx) as r:
        resp = json.loads(r.read())
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read()[:600]}"); sys.exit(1)

post_id = resp["id"]
print(f"PUSH OK  id={post_id}  status={resp.get('status')}  link={resp.get('link')}")

with urllib.request.urlopen(urllib.request.Request(
        f"{WP_BASE}/posts/{post_id}?context=edit", headers=HEADERS), timeout=30, context=_ssl_ctx) as r:
    ver = json.loads(r.read())
saved = json.loads(ver.get("meta", {}).get("_elementor_data", "[]"))
print(f"Verified: sections={len(saved)} featured_media={ver.get('featured_media')} status={ver.get('status')}")

print("Clearing Elementor cache...")
try:
    with urllib.request.urlopen(urllib.request.Request(
            "https://chatsku.com/wp-json/elementor/v1/cache",
            headers={"Authorization": f"Basic {AUTH}", "User-Agent": UA}, method="DELETE"),
            timeout=20, context=_ssl_ctx) as r:
        print(f"  cache: HTTP {r.status}")
except Exception as e:
    print(f"  cache clear: {e}")

# save published html snapshot
def sec_html(s):
    o = []
    for w in s["elements"][0]["elements"]:
        wt = w.get("widgetType")
        if wt == "heading":
            lv = w["settings"].get("header_size", "h2"); o.append(f"<{lv}>{w['settings']['title']}</{lv}>")
        elif wt == "text-editor":
            o.append(w["settings"]["editor"])
        elif wt == "image":
            im = w["settings"]["image"]; o.append(f'<img src="{im["url"]}" alt="{im["alt"]}" width="860" height="452">')
        elif wt == "accordion":
            for t in w["settings"]["tabs"]:
                o.append(f"<h3>{t['tab_title']}</h3>\n{t['tab_content']}")
        elif wt == "button":
            o.append(f'<p><a href="{w["settings"]["link"]["url"]}">{w["settings"]["text"]}</a></p>')
    return "\n".join(o)

pub = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>{META_TITLE}</title><meta name="description" content="{META_DESC}">
<!-- Post ID: {post_id} | Slug: {SLUG} | Format C | Status: draft -->
<!-- Featured {feat['id']} | Body1 {body1['id']} | Body2 {body2['id']} -->
<!-- Yoast (set manually): Title="{META_TITLE}" Desc="{META_DESC}" -->
</head><body>
<h1>{TITLE}</h1>
<img src="{feat['url']}" width="860" height="452" alt="{FEAT_ALT}">
{chr(10).join(sec_html(s) for s in elementor)}
</body></html>"""
outp = Path(r"C:\content-intel\clients\chatsku\output\published\rfq-form-best-practices-2026-07-17.html")
outp.write_text(pub, encoding="utf-8")
print(f"Saved: {outp}")

print("\n" + "=" * 66)
print("PUBLISH COMPLETE")
print(f"  Post ID:  {post_id}   status: {resp.get('status')}")
print(f"  Media:    feat={feat['id']} body1={body1['id']} body2={body2['id']}")
print(f"  Sections: {len(elementor)}  FAQ: {len(faq_items)}  Words: {wc}")
print(f"  Yoast title ({len(META_TITLE)}): {META_TITLE}")
print(f"  Yoast desc  ({len(META_DESC)}): {META_DESC}")
print(f"RESULTS_JSON={json.dumps({'post_id': post_id, 'link': resp.get('link'), 'feat': feat['id'], 'body1': body1['id'], 'body2': body2['id'], 'sections': len(elementor), 'faq': len(faq_items), 'words': wc, 'internal': len(intl), 'external': len(ext)})}")
