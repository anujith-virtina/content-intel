"""
Build and publish ChatSKU blog post: "How to convert a PDF catalog into a searchable website"
slug: convert-pdf-catalog-to-website
Format B — Conversational Q&A

Structure (matching post 96 / build_elementor_post186_v3.py template):
  Section padding: top/bottom 60px, NO left/right keys (conclusion: top:20 bottom:30)
  Column inner padding: {top:20, right:20, bottom:20, left:20, isLinked:true, unit:px}
  Body color cycle starting at #f0f4ff (index 2 of BODY_COLORS list)
  Conclusion: #1a1a2e

Section mapping:
  0. Executive summary   — #f9f9fb
  1. Why can't buyers... — #f0f4ff  (body_color_idx=2)
  2. What options...     — #ffffff  (body_color_idx=3, img: body1 AFTER text)
  3. Won't a flipbook... — #f9f9fb  (body_color_idx=0)
  4. Do I need to clean  — #ffffff  (body_color_idx=1, img: body2 AFTER text)
  5. What does buyer see — #f0f4ff  (body_color_idx=2)
  6. How long does it... — #ffffff  (body_color_idx=3)
  7. FAQ                 — #f9f9fb
  8. Conclusion          — #1a1a2e

Pre-publish checks embedded: em-dash scan, img ordering, link behavior,
external link count, conclusion widget count.
"""

import json
import secrets
import re
import urllib.request
import urllib.error
import urllib.parse
import base64
import os
import sys
import io
import time
import ssl

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

# ── Credentials ──────────────────────────────────────────────────────────────
WP_BASE = "https://chatsku.com/wp-json/wp/v2"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)
UN = os.environ.get("CHATSKU_WP_USERNAME", "")
PW = os.environ.get("CHATSKU_WP_APP_PASSWORD", "")
if not UN or not PW:
    sys.exit("ERROR: CHATSKU_WP_USERNAME or CHATSKU_WP_APP_PASSWORD not set in environment.")

creds = base64.b64encode(f"{UN}:{PW}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {creds}",
    "User-Agent": UA,
    "Content-Type": "application/json",
}

PEXELS_KEY = os.environ.get("PEXELS_API_KEY", "")

# ── Image specs ───────────────────────────────────────────────────────────────
TARGET_W, TARGET_H = 860, 452
JPEG_QUALITY = 82
MAX_BYTES = 200 * 1024  # 200 KB

IMAGES_NEEDED = [
    {
        "key": "featured",
        "filename": "chatsku-pdf-catalog-featured.jpg",
        "alt": "Business professional reviewing a B2B product catalog at their desk, representing manufacturers converting PDF catalogs to searchable websites",
        "title": "B2B manufacturer reviewing product catalog",
        "pexels_queries": [
            "business team product catalog desk",
            "manufacturer office catalog review",
            "business professional documents desk office",
        ],
        "openverse_queries": [
            "business catalog office desk",
            "manufacturer office documents",
        ],
    },
    {
        "key": "body1",
        "filename": "chatsku-pdf-catalog-body1.jpg",
        "alt": "B2B buyer searching for products on a laptop, representing the experience of searching an AI catalog assistant instead of scrolling a PDF",
        "title": "B2B buyer searching products on laptop",
        "pexels_queries": [
            "person laptop office search",
            "B2B buyer computer screen office",
            "business person typing laptop",
        ],
        "openverse_queries": [
            "office laptop search computer",
            "business person laptop desk",
        ],
    },
    {
        "key": "body2",
        "filename": "chatsku-pdf-catalog-body2.jpg",
        "alt": "Business team discussing a product quote in an office, representing the B2B RFQ process enabled by an AI catalog assistant",
        "title": "Business team discussing B2B product quote",
        "pexels_queries": [
            "business quote meeting office",
            "sales team office meeting",
            "business meeting discussion office",
        ],
        "openverse_queries": [
            "business meeting office team",
            "sales team meeting office",
        ],
    },
]


# ── Image sourcing helpers ────────────────────────────────────────────────────

def pexels_search(query, key):
    """Search Pexels and return URL of first landscape result, or None."""
    if not key:
        return None
    url = (
        f"https://api.pexels.com/v1/search"
        f"?query={urllib.parse.quote(query)}&orientation=landscape&per_page=5"
    )
    req = urllib.request.Request(url, headers={"Authorization": key, "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20, context=SSL_CTX) as r:
            data = json.loads(r.read())
        photos = data.get("photos", [])
        if photos:
            return photos[0]["src"]["large2x"]
    except Exception as e:
        print(f"    Pexels error ({query!r}): {e}")
    return None


def openverse_search(query):
    """Search Openverse (CC0/PDM, stocksnap source) and return first image URL."""
    encoded = urllib.parse.quote(query)
    url = (
        f"https://api.openverse.org/v1/images/"
        f"?q={encoded}&license=cc0,pdm&page_size=10"
        f"&aspect_ratio=wide&source=stocksnap"
    )
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20, context=SSL_CTX) as r:
            data = json.loads(r.read())
        results = data.get("results", [])
        if results:
            return results[0]["url"]
        # Try without source filter if stocksnap returned nothing
        url2 = (
            f"https://api.openverse.org/v1/images/"
            f"?q={encoded}&license=cc0,pdm&page_size=10&aspect_ratio=wide"
        )
        req2 = urllib.request.Request(url2, headers={"User-Agent": UA})
        with urllib.request.urlopen(req2, timeout=20, context=SSL_CTX) as r2:
            data2 = json.loads(r2.read())
        results2 = data2.get("results", [])
        if results2:
            return results2[0]["url"]
    except Exception as e:
        print(f"    Openverse error ({query!r}): {e}")
    return None


def fetch_image_bytes(src_url):
    """Download image bytes, validate >8000 bytes and JPEG/PNG signature."""
    req = urllib.request.Request(src_url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60, context=SSL_CTX) as r:
        data = r.read()
    if len(data) < 8000:
        raise ValueError(f"Download too small: {len(data)} bytes from {src_url}")
    sig = data[:4]
    if sig[:2] == b'\xff\xd8':
        fmt = "JPEG"
    elif sig[:4] == b'\x89PNG':
        fmt = "PNG"
    else:
        raise ValueError(f"Not a JPEG or PNG: header={sig.hex()} from {src_url}")
    print(f"    Downloaded {len(data):,} bytes ({fmt}) from {src_url[:80]}")
    return data


def resize_crop(raw_bytes, w, h):
    """Scale-to-cover + center-crop to (w, h). Returns BytesIO JPEG at quality 82."""
    try:
        from PIL import Image
    except ImportError:
        sys.exit("ERROR: Pillow not installed. Run: pip install Pillow")
    buf_in = io.BytesIO(raw_bytes)
    img = Image.open(buf_in).convert("RGB")
    src_w, src_h = img.size
    scale = max(w / src_w, h / src_h)
    new_w = int(src_w * scale)
    new_h = int(src_h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - w) // 2
    top = (new_h - h) // 2
    img = img.crop((left, top, left + w, top + h))
    buf_out = io.BytesIO()
    img.save(buf_out, format="JPEG", quality=JPEG_QUALITY, optimize=True)
    size = buf_out.tell()
    if size > MAX_BYTES:
        print(f"    Image {size:,} bytes > {MAX_BYTES:,}; re-saving at q=75")
        buf_out = io.BytesIO()
        img.save(buf_out, format="JPEG", quality=75, optimize=True)
    buf_out.seek(0)
    return buf_out


def upload_image(buf, filename, alt, title):
    """Upload image to WordPress media library and set alt/title. Returns (id, url)."""
    upload_headers = {
        "Authorization": f"Basic {creds}",
        "User-Agent": UA,
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "image/jpeg",
    }
    req = urllib.request.Request(
        f"{WP_BASE}/media",
        data=buf.getvalue(),
        headers=upload_headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=90, context=SSL_CTX) as r:
            d = json.loads(r.read())
    except urllib.error.HTTPError as e:
        err = e.read()[:300].decode("utf-8", errors="replace")
        print(f"    Upload FAIL {e.code}: {err}")
        return None, ""
    mid = d["id"]
    src = d.get("source_url", "")
    # Set alt text and title via POST to media/{id}
    meta_payload = json.dumps({"alt_text": alt, "title": title}).encode()
    meta_req = urllib.request.Request(
        f"{WP_BASE}/media/{mid}",
        data=meta_payload,
        headers={**HEADERS},
        method="POST",
    )
    try:
        urllib.request.urlopen(meta_req, timeout=20)
    except Exception as e:
        print(f"    Alt/title set warning: {e}")
    print(f"    Uploaded ID={mid}  {src.split('/')[-1]}")
    return mid, src


def source_and_upload(spec):
    """Try Pexels then Openverse for spec, resize, upload. Returns (id, url)."""
    print(f"\n  Sourcing image: {spec['key']}")
    src_url = None

    # Try Pexels first
    if PEXELS_KEY:
        for q in spec["pexels_queries"]:
            print(f"    Pexels query: {q!r}")
            src_url = pexels_search(q, PEXELS_KEY)
            if src_url:
                print(f"    Pexels hit: {src_url[:80]}")
                break
    else:
        print("    No PEXELS_API_KEY — skipping Pexels")

    # Fall back to Openverse
    if not src_url:
        for q in spec["openverse_queries"]:
            print(f"    Openverse query: {q!r}")
            time.sleep(1)  # avoid 429
            src_url = openverse_search(q)
            if src_url:
                print(f"    Openverse hit: {src_url[:80]}")
                break

    if not src_url:
        sys.exit(f"ERROR: Could not source image for key={spec['key']!r}. All APIs exhausted.")

    raw = fetch_image_bytes(src_url)
    buf = resize_crop(raw, TARGET_W, TARGET_H)
    final_size = len(buf.getvalue())
    print(f"    Resized to {TARGET_W}x{TARGET_H}, {final_size:,} bytes")
    mid, url = upload_image(buf, spec["filename"], spec["alt"], spec["title"])
    if not mid:
        sys.exit(f"ERROR: Upload failed for {spec['key']}")
    return mid, url


# ── Elementor builder helpers ─────────────────────────────────────────────────


def gid():
    """Random 7-char hex widget ID (matches post186 template pattern)."""
    return secrets.token_hex(4)[:7]


def make_button(text, url):
    return {
        "id": gid(),
        "elType": "widget",
        "widgetType": "button",
        "elements": [],
        "settings": {
            "text": text,
            "link": {"url": url, "is_external": "true"},
            "align": "center",
            "background_color": "#e94560",
            "button_text_color": "#ffffff",
            "border_radius": {"size": 6, "unit": "px"},
            "_margin": {
                "unit": "px",
                "top": "20",
                "right": "0",
                "bottom": "0",
                "left": "0",
                "isLinked": False,
            },
        },
    }


def make_section(widgets, bg, is_conclusion=False):
    """Build Elementor section matching post 96 structure exactly."""
    if is_conclusion:
        section_padding = {"top": "20", "bottom": "30", "unit": "px", "right": "0", "left": "0"}
    else:
        section_padding = {"top": "60", "bottom": "60", "unit": "px"}

    column_padding = {
        "unit": "px",
        "top": "20",
        "right": "20",
        "bottom": "20",
        "left": "20",
        "isLinked": True,
    }

    return {
        "id": gid(),
        "elType": "section",
        "isInner": False,
        "settings": {
            "background_background": "classic",
            "background_color": bg,
            "padding": section_padding,
        },
        "elements": [
            {
                "id": gid(),
                "elType": "column",
                "isInner": False,
                "settings": {
                    "_column_size": 100,
                    "width": "100",
                    "padding": column_padding,
                },
                "elements": widgets,
            }
        ],
    }


def make_heading(title, level="h2", color="#1a1a2e", align="left"):
    size = 28 if level == "h2" else 22
    s = {
        "title": title,
        "align": align,
        "title_color": color,
        "typography_font_size": {"size": size, "unit": "px"},
    }
    if level != "h2":
        s["header_size"] = level
    return {
        "id": gid(),
        "elType": "widget",
        "widgetType": "heading",
        "elements": [],
        "settings": s,
    }


def make_text(html, dark_section=False):
    # Fix relative hrefs to absolute chatsku.com URLs
    html = re.sub(r'href="/([\w/\-]+)"', r'href="https://chatsku.com/\1"', html)
    # Strip any figure/img tags (images handled via explicit image widgets)
    html = re.sub(r"<figure[^>]*>.*?</figure>", "", html, flags=re.DOTALL).strip()
    html = re.sub(r"<img[^>]*/?>", "", html).strip()
    # Replace em dashes (safety net — should already be clean from content below)
    html = html.replace("—", ",").replace("&mdash;", ",")
    if dark_section:
        html = re.sub(
            r"<p([ >])",
            r'<p style="color:#aaaacc;text-align:center;font-size:18px;max-width:720px;margin:0 auto;"\1',
            html,
        )
    return {
        "id": gid(),
        "elType": "widget",
        "widgetType": "text-editor",
        "elements": [],
        "settings": {"editor": html},
    }


def make_image_widget(mid, url, alt):
    return {
        "id": gid(),
        "elType": "widget",
        "widgetType": "image",
        "elements": [],
        "settings": {
            "image": {
                "id": mid,
                "url": url,
                "alt": alt,
                "source": "library",
                "size": "",
            },
            "align": "center",
            "width": {"size": 100, "unit": "%"},
            "border_radius": {
                "top": "10",
                "right": "10",
                "bottom": "10",
                "left": "10",
                "unit": "px",
            },
        },
    }


# ── Content ───────────────────────────────────────────────────────────────────
# All em dashes replaced with commas/periods. External links have target/rel.
# Internal chatsku.com links have no target attribute.

EXEC_SUMMARY_HTML = """\
<p>There are four realistic ways to make a B2B catalog searchable: rebuild it as a product website, implement a PIM system, host it on a flipbook platform, or add an AI catalog assistant layer over your existing PDF. Each path solves a different version of the problem at a different cost and timeline.</p>
<p>For most manufacturers and distributors in the ICP A range, 50 to 500 SKUs, no dedicated development team, buyers who research after hours, the AI catalog assistant is the right first move. It works with your existing PDF. It deploys in under a day. And it gives buyers a way to ask questions and start a quote without a rep involved.</p>
<p>The other three paths have their place. But they require months and significant budget before your first buyer gets a better experience. If you are losing deals to faster competitors right now, you cannot afford to wait for a rebuild to ship.</p>"""

SECTION_WHY_HTML = """\
<p>PDF search and web search are structurally different. A PDF is a document. A website is a database. Those two things handle queries, typos, synonyms, and filters in completely different ways.</p>
<p>If your catalog was scanned from a physical document, it is stored as an image. There is no text for a search engine to read. A buyer who types "3/8 zinc bolt" gets zero results. Not because the product is not there, but because the file is a picture of the product, not a record of it. Text-based PDFs fare better, but they still return crude results: every page where the phrase appears, with no ranking, no filtering, and no ability to handle synonyms or partial part numbers.</p>
<p>Web-based product search handles the queries buyers actually type. "Galvanized fastener" returns zinc-plated results. "3/8 hex bolt qty 500" finds the matching SKU and the relevant tiered price break. "Fastenar" still works. Document search does none of this.</p>
<p>There is also a second problem that often gets tangled with the first: Google indexing. A well-structured text PDF can show up in Google search results. But an indexed PDF is not a product page. It has no structured markup, no filter navigation, no conversion path. Being findable via Google and being usable when a buyer arrives are two separate problems. This article keeps them separate because the fix for each is different.</p>"""

SECTION_OPTIONS_HTML = """\
<p>There are four realistic paths. They differ by cost, timeline, and how much of your current setup you have to throw away.</p>
<p><strong>Option 1: Rebuild as a product website.</strong> A purpose-built catalog website backed by a product database. The most capable option long-term. Cost runs $15,000 to $150,000 depending on scope. Mid-market builds with ERP or CRM integration often land between $50,000 and $100,000 in year-one total spend. Timeline: 12 to 16 weeks for standard builds. Complex catalog structures with deep integrations can stretch to 6 to 15 months. This is the right answer eventually. It is the wrong answer if you need results this quarter.</p>
<p><strong>Option 2: Implement a PIM system.</strong> A Product Information Management platform centralizes your product data and pushes it to multiple destinations: your website, marketplaces, distributor portals, and printed catalogs. Best for manufacturers publishing to many channels simultaneously. Year-one cost: $25,000 to $90,000 including license and implementation. Timeline: 3 to 6 months for mid-market, 9 to 12 months for enterprise. This solves an internal data management problem. If your core problem is that buyers cannot find products on your site at 9pm, a PIM does not fix that directly.</p>
<p><strong>Option 3: Hosted flipbook platform.</strong> Upload your PDF and the platform converts it to a web-hosted document with page-flip navigation and basic text search. Fast to set up. Affordable. But it is a presentation upgrade, not a buyer-engagement upgrade. The next section covers why this matters.</p>
<p><strong>Option 4: AI catalog assistant layer over your existing PDF.</strong> An <a href="https://chatsku.com/pdf-catalog-chatbot/">AI catalog assistant</a> ingests your existing PDF, plus Excel files, ERP exports, or CSVs if you have them, and deploys on your current site as a conversational interface. No rebuild. No data migration project. Buyers type a question in plain English and get a direct answer from your catalog. Cost: a SaaS subscription, far less than a rebuild. Setup: hours to one day.</p>"""

SECTION_FLIPBOOK_HTML = """\
<p>A flipbook fixes the presentation problem. It does not fix the buyer-engagement problem. Those are different things.</p>
<p>Flipbooks do some things well. The catalog looks polished. Page-flip navigation is intuitive. You can share a link instead of attaching a file. Basic keyword search within the document works. For a prospect who already knows what they want and just needs to confirm a part number, a flipbook is a reasonable step up from a static PDF.</p>
<p>But here is what a flipbook cannot do: it cannot show live pricing or inventory status. It cannot surface customer-specific pricing for account holders. It cannot accept a quote request from a product listing. And when a buyer lands on your flipbook at 11pm, there is no way for them to ask a question and get an answer. The catalog is still passive. The buyer still has to wait.</p>
<p>There is also a traffic problem that often goes unmentioned. When a buyer finds your flipbook through Google, the traffic lands on the hosted flipbook platform's domain, not on yours. You receive no organic search benefit. Any SEO value that could accrue from buyers engaging with your catalog goes to the platform, not to your site.</p>
<p>For ICP A manufacturers, the real test is this: if a buyer arrives and cannot find the right spec, can they ask a question and get an answer right now? A flipbook cannot pass that test. An AI catalog assistant can.</p>"""

SECTION_CLEAN_DATA_HTML = """\
<p>Better data means better answers. But messy data does not mean you cannot start.</p>
<p>Most manufacturers with 50 to 500 SKUs know their catalog has inconsistencies. Outdated prices in one version. Different spec formats across product lines. Missing attributes for newer items. This is normal. It does not disqualify you from moving forward.</p>
<p>What matters most for an AI catalog assistant is that your catalog is text-readable. Not scanned, not image-based, just actual text that a system can read. Product names, SKUs, and specs need to be present in the document, even if imperfectly formatted. The assistant handles synonym matching and typo tolerance on the buyer's side. It does not require perfect data. It requires readable data.</p>
<p>If pricing or inventory is frequently outdated in your PDF, the right move is connecting the assistant to a live data source, an ERP export or a regularly updated CSV feed, rather than waiting until the PDF is perfect. According to Logistics IT (2025), <a href="https://www.logisticsit.com/" target="_blank" rel="noopener noreferrer">85% of B2B buyers report product findability frustrations that lead to abandoned purchases</a>. Every week you wait for clean data is another week of deals leaving through the side door.</p>"""

SECTION_BUYER_SEES_HTML = """\
<p>Your buyer types a question in plain English. The assistant finds the answer, shows the relevant SKUs, and offers to start a quote request. No rep involved.</p>
<p>Walk through the scenario. A buyer types: "do you have 3/8 inch zinc-plated hex bolts in quantities of 500?" The assistant returns the matching SKUs, notes the available stock, and surfaces the tiered pricing for a 500-unit order. If the buyer wants to move forward, they can <a href="https://chatsku.com/rfq-automation-manufacturers/">initiate an RFQ directly from the conversation</a>. No form submission, no waiting for a callback, no rep needed at 9pm.</p>
<p>Typo and synonym tolerance matter here. A buyer searching for "galvanized fastener" finds zinc-plated results. A buyer who types "fastenar" still gets a result. This is the structural difference between document search and what an <a href="https://chatsku.com/pdf-catalog-chatbot/">AI catalog assistant</a> does: it reads intent, not just characters.</p>
<p>According to 6sense, 81% of B2B buyers already have a preferred vendor in mind before they make first contact. The buyer searching your catalog at 9pm is not browsing. They are evaluating. If your catalog answers their question clearly and quickly, you stay on the shortlist. If it does not, they move to the next tab.</p>
<p>Gartner (2025) puts it plainly: 75% of B2B buyers prefer a rep-free buying experience. The AI catalog assistant is the rep-free path for complex B2B queries. It does not replace your sales team. It handles the early research and qualification so your reps talk to buyers who are already ready.</p>"""

SECTION_TIMELINE_HTML = """\
<p>It depends entirely on which path you choose. The range runs from one day to fifteen months.</p>
<ul>
  <li><strong>Rebuild from scratch.</strong> 12 to 16 weeks minimum. Complex builds with ERP integration: 6 to 15 months.</li>
  <li><strong>PIM system.</strong> 3 to 6 months mid-market. 9 to 12 months enterprise.</li>
  <li><strong>Hosted flipbook.</strong> Minutes to a few hours. Fast, but limited. See the section above on what flipbooks cannot do.</li>
  <li><strong>AI catalog assistant.</strong> Hours to one day. Your existing PDF is the starting point. The assistant deploys via a one-line script tag on your current site.</li>
</ul>
<p>The AI catalog assistant path does not require a rebuild, a data migration project, or IT involvement. You do not wait for a development sprint to finish. You do not onboard a new platform and train a team on it. The existing PDF becomes the source material, and the assistant is live while your competitors are still scoping a rebuild.</p>
<p>For a clearer picture of what setup actually looks like, <a href="https://chatsku.com/demo/">see the live demo</a>. No gate, no discovery call required.</p>"""

FAQ_QA = [
    (
        "Does a PDF catalog hurt my Google rankings?",
        "<p>Not automatically. Google has indexed text-based PDFs since 2001, so a well-structured PDF can appear in search results. The issue is what happens when a buyer finds it. A PDF page has no product structured markup, no filter navigation, no mobile-optimized layout, and no conversion path from a search result to a quote request. Getting indexed is not the same as ranking well for product-level queries, and ranking well is not the same as converting the visitor into a buyer. If organic traffic and product-level SEO matter to you, indexed HTML product pages will always outperform PDFs on those metrics.</p>",
    ),
    (
        "How much does it cost to make a catalog searchable?",
        "<p>It depends on the approach. A full rebuild runs $15,000 to $150,000 and takes 12 to 16 weeks at minimum. A PIM implementation adds $25,000 to $90,000 in year-one costs and takes 3 to 12 months. A hosted flipbook platform runs between $15 and $200 per month but does not solve the buyer-engagement problem. An AI catalog assistant runs on a SaaS subscription, significantly less than a rebuild, with no implementation project and no IT overhead.</p>",
    ),
    (
        "Can I keep my existing PDF and still make it searchable?",
        "<p>Yes. An AI catalog assistant ingests your existing PDF as the starting point. You do not need to rebuild your website, migrate your data to a new system, or wait until your catalog is perfectly formatted. The assistant reads your catalog as-is, handles typos and synonyms from the buyer's end, and deploys on your current site via a single script tag. If your catalog data improves over time, the assistant gets better with it.</p>",
    ),
    (
        "Is a digital catalog the same as a searchable catalog?",
        "<p>No. A digital catalog is typically a web-hosted version of your PDF: a flipbook, a shared link, or an embedded document viewer. It looks better than a static file, but it is still a document. A searchable catalog is backed by structured product data: SKUs, attributes, specs, and pricing that a search system can filter and return based on a buyer's specific query. The two are often confused because &#8220;digital&#8221; implies modern, and modern implies searchable. They are not the same thing.</p>",
    ),
    (
        "What happens if my catalog data is messy or outdated?",
        "<p>Start anyway. Messy data slows an AI assistant down but does not stop it. The assistant answers accurately where data is present and flags gaps where it is not, rather than guessing. As you improve the underlying catalog, better specs, current pricing, added attributes, the assistant's answers improve automatically. Waiting for a perfect catalog before deploying is the same as waiting for a perfect sales rep before opening for business. The buyers are not waiting.</p>",
    ),
    (
        "How is this different from a PIM system?",
        "<p>A PIM system centralizes your product data so you can push it to multiple channels: your website, marketplaces, printed catalogs, and distributor portals. It is the right tool if you publish product data across many destinations and need a single source of truth. An AI catalog assistant is the right tool if your core problem is that buyers cannot find or ask about products on your existing site. A PIM is an internal data management project. An AI catalog assistant is a buyer-facing engagement layer. They solve different problems, and for most manufacturers with 50 to 500 SKUs, the buyer-engagement problem is more urgent and faster to fix.</p>",
    ),
]

CONCLUSION_P1 = "<p>Your catalog is ready. Your buyers are not waiting.</p>"
CONCLUSION_P2 = "<p>ChatSKU turns your existing PDF catalog into a 24/7 AI catalog assistant that answers buyer questions, builds quotes, and captures leads, without rebuilding your website. Setup takes hours, not months. Your catalog should be working while you sleep.</p>"

# WP plain-HTML fallback content (no bare img tags)
WP_CONTENT = """\
<p>A buyer lands on your site at 8pm. They need 500 units of zinc-plated fasteners. They find a link to your catalog. It opens as a 47-page PDF. They scroll for three minutes, can't find the right spec, and close the tab. By morning they've placed the order with your competitor.</p>
<p>Your catalog is not broken. It is just not searchable. Those are two different problems with four different fixes. This article walks through each option honestly, costs, timelines, and what actually fits a manufacturer with 50 to 500 SKUs and no IT team.</p>

<h2>Executive summary</h2>
""" + EXEC_SUMMARY_HTML + """

<h2>Why can't buyers just search my PDF the way they search a website?</h2>
""" + SECTION_WHY_HTML + """

<h2>What options do I actually have to make my catalog searchable?</h2>
""" + SECTION_OPTIONS_HTML + """

<h2>Won't a flipbook or digital catalog platform solve this?</h2>
""" + SECTION_FLIPBOOK_HTML + """

<h2>Do I need to clean up my product data before doing anything?</h2>
""" + SECTION_CLEAN_DATA_HTML + """

<h2>What does my buyer actually see when they search my catalog through an AI assistant?</h2>
""" + SECTION_BUYER_SEES_HTML + """

<h2>How long does this actually take to set up?</h2>
""" + SECTION_TIMELINE_HTML + """

<h2>Frequently asked questions</h2>
<h3>Does a PDF catalog hurt my Google rankings?</h3>
""" + FAQ_QA[0][1] + """
<h3>How much does it cost to make a catalog searchable?</h3>
""" + FAQ_QA[1][1] + """
<h3>Can I keep my existing PDF and still make it searchable?</h3>
""" + FAQ_QA[2][1] + """
<h3>Is a digital catalog the same as a searchable catalog?</h3>
""" + FAQ_QA[3][1] + """
<h3>What happens if my catalog data is messy or outdated?</h3>
""" + FAQ_QA[4][1] + """
<h3>How is this different from a PIM system?</h3>
""" + FAQ_QA[5][1] + """

<h2>Conclusion</h2>
""" + CONCLUSION_P1 + """
""" + CONCLUSION_P2


# ── Pre-publish checks ────────────────────────────────────────────────────────

def run_preflight_checks(elementor_sections, wp_content, featured_media_id):
    """Run all pre-publish checklist items. Aborts on failure."""
    print("\n--- Pre-publish checklist ---")
    failures = []

    # 1. Em dash scan across all content strings
    em_dash = "—"
    all_text = wp_content
    for s in elementor_sections:
        all_text += json.dumps(s)
    if em_dash in all_text or "&mdash;" in all_text:
        failures.append("Em dash (—) or &mdash; found in content. Replace before publishing.")
    else:
        print("  [PASS] No em dashes")

    # 2. featured_media is real ID, not 0
    if not featured_media_id or featured_media_id == 0:
        failures.append("featured_media is 0 or unset.")
    else:
        print(f"  [PASS] featured_media = {featured_media_id}")

    # 3. WP content has no bare <img> tags
    if re.search(r"<img\s", wp_content):
        failures.append("Bare <img> tag found in WP content field. Strip before pushing.")
    else:
        print("  [PASS] No bare <img> tags in WP content")

    # 4. External link count <= 2
    ext_links = re.findall(r'href="https?://(?!chatsku\.com)[^"]*"', wp_content)
    if len(ext_links) > 2:
        failures.append(f"External link count = {len(ext_links)} (max 2): {ext_links}")
    else:
        print(f"  [PASS] External links: {len(ext_links)} ({ext_links})")

    # 5. External links have target/rel
    for link in re.finditer(r'<a\s[^>]*href="https?://(?!chatsku\.com)[^"]*"[^>]*>', wp_content):
        tag = link.group(0)
        if 'target="_blank"' not in tag or "noopener" not in tag:
            failures.append(f"External link missing target/rel: {tag[:120]}")
    if not any("missing target" in f for f in failures):
        print("  [PASS] All external links have target=_blank rel=noopener noreferrer")

    # 6. Internal chatsku links have no target attribute
    for link in re.finditer(r'<a\s[^>]*href="https://chatsku\.com[^"]*"[^>]*>', wp_content):
        tag = link.group(0)
        if "target=" in tag:
            failures.append(f"Internal link has target attribute (should be same tab): {tag[:120]}")
    if not any("target attribute" in f for f in failures):
        print("  [PASS] Internal links open in same tab (no target attr)")

    # 7. Image widgets come AFTER text-editor in every section
    for i, sec in enumerate(elementor_sections):
        for col in sec.get("elements", []):
            widgets = col.get("elements", [])
            last_text_idx = -1
            first_img_idx = -1
            for j, w in enumerate(widgets):
                wt = w.get("widgetType", "")
                if wt == "text-editor":
                    last_text_idx = j
                elif wt == "image":
                    if first_img_idx == -1:
                        first_img_idx = j
            if first_img_idx != -1 and last_text_idx != -1:
                if first_img_idx < last_text_idx:
                    failures.append(
                        f"Section {i}: image widget (idx {first_img_idx}) appears BEFORE text-editor (idx {last_text_idx}). Must be after."
                    )
    if not any("appears BEFORE" in f for f in failures):
        print("  [PASS] Image widgets positioned after text-editor in all sections")

    # 8. Conclusion section has exactly 3 widgets: heading + text-editor + button
    conclusion_sections = [
        s for s in elementor_sections
        if s["settings"].get("background_color") == "#1a1a2e"
    ]
    if not conclusion_sections:
        failures.append("No conclusion section found (bg=#1a1a2e missing).")
    else:
        conc = conclusion_sections[0]
        for col in conc.get("elements", []):
            widgets = col.get("elements", [])
            types = [w.get("widgetType") for w in widgets]
            if types != ["heading", "text-editor", "button"]:
                failures.append(f"Conclusion widgets = {types}, expected [heading, text-editor, button]")
            else:
                print("  [PASS] Conclusion has 3 widgets: heading + text-editor + button")
            # heading must be centered and white
            if widgets[0].get("settings", {}).get("title_color") != "#ffffff":
                failures.append("Conclusion heading color is not #ffffff")
            if widgets[0].get("settings", {}).get("align") != "center":
                failures.append("Conclusion heading is not centered")
            # button must be #e94560
            btn_bg = widgets[2].get("settings", {}).get("background_color", "")
            if btn_bg != "#e94560":
                failures.append(f"Conclusion button background = {btn_bg!r}, expected #e94560")
            else:
                print("  [PASS] Conclusion button color #e94560")

    # 9. Status will be draft (confirmed in payload)
    print("  [PASS] Status: draft")

    # 10. Section count sanity (9 sections expected)
    print(f"  [INFO] Elementor section count: {len(elementor_sections)}")

    if failures:
        print("\nPRE-PUBLISH FAILURES:")
        for f in failures:
            print(f"  FAIL: {f}")
        sys.exit("Aborting — fix checklist failures before publishing.")
    else:
        print("\n  All pre-publish checks passed.")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("ChatSKU blog build: convert-pdf-catalog-to-website")
    print("=" * 60)

    # Step 1: Source and upload images
    print("\n[1/5] Sourcing and uploading images...")
    images = {}
    for spec in IMAGES_NEEDED:
        mid, url = source_and_upload(spec)
        images[spec["key"]] = {"id": mid, "url": url, "alt": spec["alt"]}
        time.sleep(0.5)

    featured_id = images["featured"]["id"]
    body1_id = images["body1"]["id"]
    body2_id = images["body2"]["id"]

    print(f"\n  Featured:  ID={featured_id}  {images['featured']['url'].split('/')[-1]}")
    print(f"  Body img1: ID={body1_id}  {images['body1']['url'].split('/')[-1]}")
    print(f"  Body img2: ID={body2_id}  {images['body2']['url'].split('/')[-1]}")

    # Verify all image URLs start with chatsku.com
    for key, img in images.items():
        if not img["url"].startswith("https://chatsku.com/wp-content/uploads/"):
            sys.exit(f"ERROR: {key} URL does not start with chatsku.com/wp-content/uploads/: {img['url']}")
    print("  [PASS] All image URLs start with https://chatsku.com/wp-content/uploads/")

    # Step 2: Build Elementor JSON
    print("\n[2/5] Building Elementor JSON...")

    BODY_COLORS = ["#f9f9fb", "#ffffff", "#f0f4ff", "#ffffff"]
    body_color_idx = 2  # first body section starts at #f0f4ff (index 2), matching post 96

    elementor_sections = []

    # Section 0: Executive Summary — #f9f9fb
    elementor_sections.append(make_section(
        [make_heading("Executive summary"), make_text(EXEC_SUMMARY_HTML)],
        bg="#f9f9fb",
    ))

    # Section 1: Why can't buyers... — #f0f4ff (body_color_idx=2)
    bg = BODY_COLORS[body_color_idx % len(BODY_COLORS)]
    body_color_idx += 1
    elementor_sections.append(make_section(
        [
            make_heading("Why can't buyers just search my PDF the way they search a website?"),
            make_text(SECTION_WHY_HTML),
        ],
        bg=bg,
    ))

    # Section 2: What options... — #ffffff (idx=3) + body image 1 AFTER text
    bg = BODY_COLORS[body_color_idx % len(BODY_COLORS)]
    body_color_idx += 1
    elementor_sections.append(make_section(
        [
            make_heading("What options do I actually have to make my catalog searchable?"),
            make_text(SECTION_OPTIONS_HTML),
            make_image_widget(body1_id, images["body1"]["url"], images["body1"]["alt"]),
        ],
        bg=bg,
    ))

    # Section 3: Won't a flipbook... — #f9f9fb (idx=0)
    bg = BODY_COLORS[body_color_idx % len(BODY_COLORS)]
    body_color_idx += 1
    elementor_sections.append(make_section(
        [
            make_heading("Won't a flipbook or digital catalog platform solve this?"),
            make_text(SECTION_FLIPBOOK_HTML),
        ],
        bg=bg,
    ))

    # Section 4: Do I need to clean up... — #ffffff (idx=1) + body image 2 AFTER text
    bg = BODY_COLORS[body_color_idx % len(BODY_COLORS)]
    body_color_idx += 1
    elementor_sections.append(make_section(
        [
            make_heading("Do I need to clean up my product data before doing anything?"),
            make_text(SECTION_CLEAN_DATA_HTML),
            make_image_widget(body2_id, images["body2"]["url"], images["body2"]["alt"]),
        ],
        bg=bg,
    ))

    # Section 5: What does my buyer see... — #f0f4ff (idx=2)
    bg = BODY_COLORS[body_color_idx % len(BODY_COLORS)]
    body_color_idx += 1
    elementor_sections.append(make_section(
        [
            make_heading("What does my buyer actually see when they search my catalog through an AI assistant?"),
            make_text(SECTION_BUYER_SEES_HTML),
        ],
        bg=bg,
    ))

    # Section 6: How long does it take... — #ffffff (idx=3)
    bg = BODY_COLORS[body_color_idx % len(BODY_COLORS)]
    body_color_idx += 1
    elementor_sections.append(make_section(
        [
            make_heading("How long does this actually take to set up?"),
            make_text(SECTION_TIMELINE_HTML),
        ],
        bg=bg,
    ))

    # Section 7: FAQ — #f9f9fb
    faq_widgets = [make_heading("Frequently asked questions")]
    for question, answer_html in FAQ_QA:
        faq_widgets.append(make_heading(question, level="h3"))
        faq_widgets.append(make_text(answer_html))
    elementor_sections.append(make_section(faq_widgets, bg="#f9f9fb"))

    # Section 8: Conclusion — #1a1a2e
    conclusion_html = CONCLUSION_P1 + "\n" + CONCLUSION_P2
    elementor_sections.append(make_section(
        [
            make_heading("Conclusion", color="#ffffff", align="center"),
            make_text(conclusion_html, dark_section=True),
            make_button("See the live demo", "https://chatsku.com/demo/"),
        ],
        bg="#1a1a2e",
        is_conclusion=True,
    ))

    print(f"  Built {len(elementor_sections)} sections")
    for i, s in enumerate(elementor_sections):
        bg = s["settings"]["background_color"]
        col = s["elements"][0]
        widgets = col["elements"]
        w_types = [w.get("widgetType", "?") for w in widgets]
        h_title = next(
            (w["settings"].get("title", "")[:45] for w in widgets if w.get("widgetType") == "heading"),
            "?",
        )
        print(f"  {i:2}: bg={bg}  widgets={w_types}  [{h_title}]")

    # Step 3: Pre-publish checks
    print("\n[3/5] Running pre-publish checks...")
    run_preflight_checks(elementor_sections, WP_CONTENT, featured_id)

    # Step 4: Push post to WordPress
    print("\n[4/5] Pushing post to WordPress...")
    elementor_data_json = json.dumps(elementor_sections)
    print(f"  Elementor JSON: {len(elementor_data_json):,} chars")

    post_payload = {
        "title": "How to convert a PDF catalog into a searchable website (without rebuilding it)",
        "slug": "convert-pdf-catalog-to-website",
        "status": "draft",
        "featured_media": featured_id,
        "content": WP_CONTENT,
        "meta": {
            "_elementor_edit_mode": "builder",
            "_elementor_template_type": "wp-post",
            "_elementor_data": elementor_data_json,
        },
    }

    payload_bytes = json.dumps(post_payload).encode("utf-8")
    req = urllib.request.Request(
        f"{WP_BASE}/posts",
        data=payload_bytes,
        headers=HEADERS,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120, context=SSL_CTX) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        err_body = e.read()[:600].decode("utf-8", errors="replace")
        sys.exit(f"HTTP ERROR {e.code}: {err_body}")

    post_id = resp.get("id")
    post_status = resp.get("status")
    post_link = resp.get("link", "")
    featured_media_returned = resp.get("featured_media")
    print(f"  Post created: ID={post_id}  status={post_status}")
    print(f"  Link: {post_link}")
    print(f"  featured_media: {featured_media_returned}")

    # Step 5: Clear Elementor cache
    print("\n[5/5] Clearing Elementor cache...")
    try:
        cache_req = urllib.request.Request(
            "https://chatsku.com/wp-json/elementor/v1/cache",
            headers=HEADERS,
            method="DELETE",
        )
        urllib.request.urlopen(cache_req, timeout=15, context=SSL_CTX)
        print("  Cache cleared successfully")
    except Exception as e:
        print(f"  Cache clear (non-fatal): {e}")

    # Post-push verification
    print("\nVerifying saved post...")
    verify_req = urllib.request.Request(
        f"{WP_BASE}/posts/{post_id}?context=edit",
        headers=HEADERS,
    )
    with urllib.request.urlopen(verify_req, timeout=30, context=SSL_CTX) as r:
        verified = json.loads(r.read())

    meta_v = verified.get("meta", {})
    ed_raw = meta_v.get("_elementor_data", "[]")
    ed = json.loads(ed_raw) if ed_raw else []
    print(f"  Sections saved: {len(ed)} (expected {len(elementor_sections)})")
    print(f"  edit_mode: {meta_v.get('_elementor_edit_mode')!r}")
    print(f"  template_type: {meta_v.get('_elementor_template_type')!r}")
    print(f"  featured_media: {verified.get('featured_media')}")
    print(f"  status: {verified.get('status')}")

    # Section color audit
    print("\nSection color/padding audit (verified from server):")
    for i, s in enumerate(ed):
        bg_v = s["settings"].get("background_color", "?")
        pad_top = s["settings"].get("padding", {}).get("top", "?")
        col_pad_top = ""
        widget_types = []
        h_title = ""
        for col in s.get("elements", []):
            col_pad_top = col.get("settings", {}).get("padding", {}).get("top", "?")
            for w in col.get("elements", []):
                widget_types.append(w.get("widgetType", "?"))
                if w.get("widgetType") == "heading" and not h_title:
                    h_title = w["settings"].get("title", "")[:40]
        print(
            f"  {i:2}: bg={bg_v}  sec_pad={pad_top}px  col_pad={col_pad_top}px  "
            f"widgets={widget_types}  [{h_title}]"
        )

    # Summary report
    print("\n" + "=" * 60)
    print("PUBLISH SUMMARY")
    print("=" * 60)
    print(f"  Post ID:           {post_id}")
    print(f"  Status:            {verified.get('status')}")
    print(f"  Draft preview URL: {post_link}")
    print(f"  Featured image ID: {featured_id}  ({images['featured']['url'].split('/')[-1]})")
    print(f"  Body image 1 ID:   {body1_id}  ({images['body1']['url'].split('/')[-1]})")
    print(f"  Body image 2 ID:   {body2_id}  ({images['body2']['url'].split('/')[-1]})")
    print(f"  Elementor sections: {len(ed)}")
    content_wc = len(WP_CONTENT.split())
    print(f"  WP content word count (approx): {content_wc}")
    print("")
    print("  MANUAL STEP REQUIRED:")
    print("  Yoast meta CANNOT be set via REST API on chatsku.com.")
    print("  Go to WP Admin -> Posts -> Edit -> Yoast SEO panel -> SEO tab:")
    print("    Title:       Convert a PDF catalog to a searchable website | ChatSKU")
    print("    Description: Your PDF catalog is costing you B2B deals. Learn the four real options")
    print("                 to make it searchable -- with honest costs, timelines, and what actually")
    print("                 works for manufacturers.")
    print("    Focus KW:    convert PDF catalog to website")
    print("=" * 60)
    print("Done.")

    # Return values for record
    return {
        "post_id": post_id,
        "post_link": post_link,
        "featured_image_id": featured_id,
        "featured_image_url": images["featured"]["url"],
        "body_image_1_id": body1_id,
        "body_image_1_url": images["body1"]["url"],
        "body_image_2_id": body2_id,
        "body_image_2_url": images["body2"]["url"],
        "elementor_sections": len(ed),
        "status": verified.get("status"),
    }


if __name__ == "__main__":
    result = main()
