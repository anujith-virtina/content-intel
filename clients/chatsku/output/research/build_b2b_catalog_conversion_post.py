"""
Build and publish: b2b-catalog-conversion-rate
Post: "Why your B2B catalog conversion rate is still stuck (and what to do about it)"
Format: Format B (Conversational Q&A)  Date: 2026-06-11

Pipeline:
  1. Load .env credentials
  2. Source and upload 3 images (Pexels -> Openverse/Stocksnap fallback)
  3. Build Elementor JSON from draft HTML with enhancements
  4. Push to WordPress as draft
  5. Clear Elementor cache
  6. Save published HTML to output/published/
  7. Report media IDs, post ID, checklist results

Template: clients/chatsku/output/research/build_elementor_post186_v3.py (post 96 structure)
Verified rules from MUST-FOLLOW-RULES.md:
  - Section padding: {top:"60", bottom:"60", unit:"px"} -- NO left/right keys
  - Column padding: {unit:"px", top:"20", right:"20", bottom:"20", left:"20", isLinked:True}
  - Heading H2: title_color="#1a1a2e", font_size=28px
  - Heading H3: header_size="h3", title_color="#1a1a2e", font_size=22px
  - Image widget AFTER text-editor widget (Elementor 4.0.3 confirmed bug)
  - Conclusion: bg=#1a1a2e, heading white centered, body #aaaacc, button #e94560
  - FAQ section: bg=#f9f9fb
  - Cloudflare: User-Agent header required on every request
"""

import json, secrets, re, urllib.request, urllib.error, urllib.parse
import base64, os, io, time, sys, ssl

from pathlib import Path

# Windows SSL bypass (cert store issue on some WP Engine hosts)
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

# ── Credentials ────────────────────────────────────────────────────────────────
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

def source_image(queries):
    """Try Pexels then Openverse for each query."""
    for query in queries:
        print(f"  Trying Pexels: '{query}'")
        urls = pexels_search(query)
        for url in urls:
            raw = download_image(url)
            if raw:
                return url, resize_image(raw)
        print(f"  Trying Openverse: '{query}'")
        urls = openverse_search(query)
        for url in urls:
            raw = download_image(url)
            if raw:
                return url, resize_image(raw)
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
# ENHANCED HTML CONTENT (draft + injected blocks)
# ═══════════════════════════════════════════════════════════════════════════════

# ── Comparison table (goes in Q7 / Algolia section) ───────────────────────────
COMPARISON_TABLE_HTML = """
<p>Here is a side-by-side breakdown of what each tool is designed to do:</p>

<table style="border-collapse:collapse;width:100%;font-size:15px;">
  <thead>
    <tr>
      <th style="background:#1a1a2e;color:#ffffff;padding:10px 14px;text-align:left;">Capability</th>
      <th style="background:#1a1a2e;color:#ffffff;padding:10px 14px;text-align:left;">AI search (e.g. Algolia)</th>
      <th style="background:#1a1a2e;color:#ffffff;padding:10px 14px;text-align:left;">Conversational commerce (ChatSKU)</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background:#f0f4ff;">
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Product discovery</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Fast, relevance-ranked, faceted</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">N/A - discovery is search's job</td>
    </tr>
    <tr style="background:#ffffff;">
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Contract pricing</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">No - indexes catalog data only</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Yes - pulls from ERP/account data</td>
    </tr>
    <tr style="background:#f0f4ff;">
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">MOQ confirmation</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">No</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Yes - account-specific</td>
    </tr>
    <tr style="background:#ffffff;">
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Compatibility check</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">No</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Yes - guided Q&amp;A</td>
    </tr>
    <tr style="background:#f0f4ff;">
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Lead time by location</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">No</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Yes - real-time inventory data</td>
    </tr>
    <tr style="background:#ffffff;">
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">RFQ generation</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">No</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Yes - natural language to RFQ</td>
    </tr>
    <tr style="background:#f0f4ff;">
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">After-hours coverage</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Partial (finds product)</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Full (answers and qualifies)</td>
    </tr>
    <tr style="background:#ffffff;">
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Integration required</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Catalog index</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">ERP + catalog</td>
    </tr>
  </tbody>
</table>
"""

# ── Infographic stats block (goes in Q6 / conversion section, BEFORE the math para) ──
STATS_BLOCK_HTML = """<div style="display:flex;gap:20px;flex-wrap:wrap;margin:24px 0;">
  <div style="flex:1;min-width:180px;background:#f0f4ff;border-radius:10px;padding:20px;text-align:center;">
    <div style="font-size:36px;font-weight:700;color:#1a1a2e;">2.4%</div>
    <div style="font-size:14px;color:#555;margin-top:6px;">Average B2B catalog<br>conversion rate</div>
  </div>
  <div style="flex:1;min-width:180px;background:#00C9B1;border-radius:10px;padding:20px;text-align:center;">
    <div style="font-size:36px;font-weight:700;color:#ffffff;">12.3%</div>
    <div style="font-size:14px;color:#ffffff;margin-top:6px;">Conversion rate for<br>chat-engaged visitors</div>
  </div>
  <div style="flex:1;min-width:180px;background:#1a1a2e;border-radius:10px;padding:20px;text-align:center;">
    <div style="font-size:36px;font-weight:700;color:#00C9B1;">4x</div>
    <div style="font-size:14px;color:#aaaacc;margin-top:6px;">Conversion lift with<br>conversational commerce</div>
  </div>
</div>"""

# ── Checklist (replaces the three bold "First/Second/Third" paragraphs in Q8) ─
CHECKLIST_HTML = """<p>Three diagnostic questions before you spend another dollar.</p>

<ul style="list-style:none;padding:0;">
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:16px;padding:16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="font-size:20px;color:#00C9B1;flex-shrink:0;">&#10003;</span>
    <div><strong>Diagnose the gap.</strong> Look at your session-to-purchase conversion rate by traffic segment. What is the rate for visitors who interact with product pages vs. visitors who bounce before the cart? If most exits happen from the product detail page or after adding to cart, you have a post-discovery conversion problem, not a search problem. That distinction tells you exactly where to invest.</div>
  </li>
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:16px;padding:16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="font-size:20px;color:#00C9B1;flex-shrink:0;">&#10003;</span>
    <div><strong>Audit your product detail pages.</strong> Do your PDPs show account-specific pricing for logged-in buyers? Do they show branch-level inventory? Do they answer MOQ questions inline? If any of those answers is "no" or "inconsistently," that's where revenue is escaping. Not from search. From the page that comes after search.</div>
  </li>
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:16px;padding:16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="font-size:20px;color:#00C9B1;flex-shrink:0;">&#10003;</span>
    <div><strong>Model the conversational layer ROI before committing.</strong> Take your monthly product page sessions, multiply by your current conversion rate to get order volume, then apply a 23% site-wide lift and a 12.3% chat-engaged conversion rate to a realistic engagement percentage. If the incremental orders at your average B2B order value outweigh the tool cost, the decision is straightforward. You can <a href="https://chatsku.com/pricing/">check ChatSKU's pricing</a> to run that math directly.</div>
  </li>
</ul>

<p>ChatSKU connects to your existing catalog sources (ERP exports, PDFs, Excel files) and deploys via one line of code. No site rebuild. No Algolia migration. It layers on top of what you already have. You can <a href="https://chatsku.com/features/">explore how ChatSKU connects to your catalog</a> to see the integration options, or <a href="https://chatsku.com/signup/">start a free trial</a> and have it running before end of day. Improving your <strong>B2B catalog conversion rate</strong> doesn't require replacing anything you've already built.</p>"""

# ── Full draft HTML: em dash scan applied, enhancements injected ───────────────
# IMPORTANT: All em dashes (--) replaced with colons, commas, or periods.
# Verified: zero U+2014 or &mdash; in the draft source.
DRAFT_HTML = """\
<h2>Executive summary</h2>

<p>B2B distribution averages a 2.4% session-to-purchase conversion rate. Industrial equipment sits at 1.8%. Even after investing in AI search and bringing zero-result rates under 5%, most distributors still see <strong>B2B catalog conversion rates</strong> at 2.1%-3.1%. The numbers barely move.</p>

<p>83% of B2B sellers now prioritize AI when selecting search tools, per Algolia's 2026 B2B report. AI search delivers a 10-15% relative lift in search-assisted conversion. A 15% lift on a 2.4% baseline is 2.76%. Still under 3%. The problem is structural, not tactical.</p>

<p>70% of abandoned carts in complex B2B catalogs happen because buyers cannot confirm specs, contract pricing, or compatibility at the moment they need to. Those are not search queries. They are conversational questions. Chat-engaged B2B visitors convert at 12.3% vs. 3.1% for non-engaged visitors. That 4x delta is what this article explains.</p>

<h2>Introduction</h2>

<p>Your Algolia implementation is working. Buyers find the right product on the first search. Your zero-result rate is under 5%. Your conversion rate is still 2.1%.</p>

<p>You're not imagining it. The search is working. The conversion isn't.</p>

<p>Here's what that looks like in practice. A buyer searches for a 3-phase motor with a specific frame size. AI search returns the right product in position one. The buyer clicks through. The product page shows list price. The buyer has a negotiated contract rate. The page says "in stock." The buyer needs to know which warehouse. The add-to-cart button is right there. The buyer still needs MOQ confirmation and net-30 terms. So the buyer emails their sales rep. The sale stalls for 48 hours. The buyer may or may not come back.</p>

<p>Algolia did its job. The failure happened in the gap between "found it" and "bought it." That gap is what this article is about.</p>

<h2>What is B2B catalog conversion rate and what's a good benchmark?</h2>

<p>Simple definition: your B2B catalog conversion rate is the percentage of product page sessions that result in a completed purchase or qualified quote. Now move past the definition. Here's where you stand relative to everyone else.</p>

<p>Per Elogic's 2026 benchmarks, B2B distribution averages 2.4%. B2B manufacturing sits at about 2.1%, per Mida's 2026 data. Industrial equipment drops as low as 1.8%, per Atwix. Top-performing B2B ecommerce operations exceed 5%. Only 8%-15% of product page visitors add anything to a cart.</p>

<p>Frame it in revenue terms. A distributor with 10,000 monthly product page sessions at 2.4% closes 240 orders. At 5%, they close 500. That 260-order gap is not a hypothetical. It's a revenue decision you're making every month. AI search buyers often expect post-implementation numbers to be higher than these baselines. They're not. A 10-15% relative lift from search optimization moves a 2.4% baseline to roughly 2.7%. Still far from top-performer territory.</p>

<h2>Why does AI search improve discovery but not conversion?</h2>

<p>Here's the part nobody tells you. Buyers were never really struggling to find products.</p>

<p>83% of B2B sellers now prioritize AI when selecting search tools. Algolia's 2026 report describes a strategic shift from "expansion to optimization": companies that adopted AI search are now trying to extract more value from it because the initial adoption didn't move the numbers they expected. That's not an indictment of AI search. It's a sign that discovery was already a solved problem for most repeat B2B buyers. They knew the part number. What they needed was a set of answers that no search results page has ever been able to provide.</p>

<p>The AI search vs. conversational commerce distinction comes down to what each tool is designed to do. AI search matches queries to relevant results. It does this extremely well. But B2B buyers ask questions that go beyond finding a product: Can I order this at my contract price? Does this ship from my preferred warehouse? Is the MOQ compatible with my project scope? What are the lead times? These are not search queries. They require access to account-specific data, real-time inventory, and business logic that lives in the ERP, not in the search index.</p>

<p>Elogic puts it plainly: for complex B2B and enterprise ecommerce, conversion rate is often constrained by architecture, not only UX. That validates what you already suspected. The problem isn't the interface. It's what the interface cannot answer.</p>

<h2>What happens between "found it" and "bought it" in B2B catalogs?</h2>

<p>The buyer found the product. So why is the cart empty?</p>

<p>69%-75% of B2B shopping carts are abandoned, per <a href="https://humcommerce.com/knowledge-center/how-ai-chatbot-improves-b2b-ecommerce-conversion-rates/" target="_blank" rel="noopener noreferrer">HumCommerce's 2026 data</a>. In complex B2B catalogs with 50,000+ SKUs and 100+ attributes per product, 70% of that abandonment happens because buyers cannot confirm specs, compatibility, or pricing at the moment of decision. The buyer already found the product. That's not the problem.</p>

<p>Here are the 12 questions a B2B buyer needs answered before they place an order:</p>

<ul>
  <li><strong>Contract pricing.</strong> What is my account-specific price for this product?</li>
  <li><strong>Minimum order quantity.</strong> What is the MOQ, and does it match my project scope?</li>
  <li><strong>Inventory location.</strong> Is this in stock at my preferred or nearest distribution center?</li>
  <li><strong>Lead time.</strong> What are the lead times if it's not locally available?</li>
  <li><strong>Compatibility.</strong> Does this work with my existing equipment or system?</li>
  <li><strong>Payment terms.</strong> What payment options apply to my account tier?</li>
  <li><strong>Order history.</strong> Has my company ordered this before, and at what quantity?</li>
  <li><strong>Volume discounts.</strong> Are there breaks above a certain quantity?</li>
  <li><strong>Return terms.</strong> What are the exchange or return conditions for this category?</li>
  <li><strong>Documentation.</strong> What SDS sheets, certs of conformance, or CAD files come with the order?</li>
  <li><strong>Substitute products.</strong> Are there alternatives if this item has a long lead time?</li>
  <li><strong>Order workflow.</strong> Does this require an RFQ, or can I place it directly?</li>
</ul>

<p>None of those are answered by a search results page. Some aren't even answered by a well-designed product detail page. Every unanswered question sends the buyer to the phone or email. And every one of those contacts is a delay, a friction point, and a chance for a faster competitor to close the deal instead. Per HumCommerce, 48% of B2B abandonment comes from unexpected costs, 22% from inventory and delivery uncertainty, and 18% from checkout complexity.</p>

<h2>Why do sophisticated buyers with AI search still abandon at checkout?</h2>

<p>You solved the obvious problems. The abandonment is still there.</p>

<p>If you're reading this, you're not dealing with a catalog data problem or a zero-result search issue. You've already fixed those. Your abandonment is happening after a successful search interaction. That means the problem is upstream of checkout, not in checkout design. Here's where the conversion is actually escaping:</p>

<ul>
  <li><strong>Contract pricing not surfaced at the product level.</strong> AI search indexes catalog data. It does not index account-specific pricing tables from the ERP. The buyer finds the right product and sees list price. That's not Algolia's fault. It's an architecture gap. The buyer needs a system that knows who they are and what their negotiated rate is.</li>
  <li><strong>Inventory specificity.</strong> "In stock" is not sufficient for a B2B buyer who needs products from a specific warehouse to meet a project deadline. Most distributors haven't built branch-level inventory surfacing at the product-display layer. The buyer doesn't know if this ships from the right location.</li>
  <li><strong>MOQ and order logic.</strong> A 24-pack minimum doesn't communicate itself on a search result. The buyer adds 12 units, gets to checkout, and hits an error or a call-to-inquire block. That's a sale that walked out.</li>
  <li><strong>Approval workflow uncertainty.</strong> Many B2B orders above a dollar threshold require internal approval. A buyer who isn't sure if an order needs a PO is less likely to complete it without confirmation first.</li>
</ul>

<p>38% of B2B searches on legacy keyword systems return zero results. AI search reduced that. But even after improving search relevance, the remaining conversion gap is driven by these post-search friction points. You solved the discovery architecture problem. The next problem is the conversation architecture problem.</p>

<h2>What is conversational commerce and how does it layer on top of existing search?</h2>

<p>Conversational commerce is not a replacement for search. Let's be precise about that from the start.</p>

<p>A conversational commerce layer sits between the buyer and the catalog, answering the questions that a search results page cannot. Unlike generic customer service chatbots, which handle ticket deflection and return FAQs, a B2B-specific conversational layer knows the buyer's account, pricing tier, order history, and the full catalog. It answers the specific questions that block B2B purchase decisions: contract pricing, MOQ, compatibility, lead time.</p>

<p>The architecture is additive. The buyer uses Algolia (or whatever they're using) to find the product. Once on the product page or at the cart, the conversational layer picks up the questions the page can't answer. The buyer doesn't leave the page. They don't call the sales rep. They get an answer and place the order. ChatSKU is built for exactly this layered architecture. It connects to existing catalog sources (PDF, Excel, ERP exports) and answers account-specific questions without requiring a site rebuild. You can <a href="https://chatsku.com/features/">explore how ChatSKU's catalog integration works</a> if you want to see what that looks like in practice.</p>

<p>1 in 4 B2B buyers now use generative AI more often than conventional search when researching suppliers, per Digital Commerce 360's October 2025 data. Two-thirds rely on AI chat tools as much as or more than Google when evaluating vendors. Buyers are training themselves to expect conversational answers. If your site still only offers a search bar, that expectation gap is widening every quarter. The term "conversational commerce B2B" has moved from early-adopter vocabulary to active buying-decision category in under 24 months.</p>

<h2>How does conversational commerce improve B2B catalog conversion rate?</h2>

STATS_BLOCK_INJECT

<p>Here are the numbers. Chat-engaged B2B visitors convert at 12.3%. Non-engaged visitors convert at 3.1%, per <a href="https://humcommerce.com/knowledge-center/how-ai-chatbot-improves-b2b-ecommerce-conversion-rates/" target="_blank" rel="noopener noreferrer">HumCommerce's 2026 data</a>. That's a 4x delta. Site-wide conversion increases by 23% with AI catalog assistant deployment. Average order value increases by 15% from contextual upsells and cross-sells surfaced during the conversation.</p>

<p>Run the math on your own catalog. Take 10,000 monthly product page sessions. At 2.4% conversion, you close 240 orders. Apply a conservative scenario: 30% of visitors engage with the conversational layer and convert at 12.3%. That's 369 orders from engaged visitors alone. Add the remaining 70% at baseline. Even before the full blended 23% site-wide lift kicks in, the delta is clear. At $2,000 average B2B order value, a 23% site-wide lift on 240 orders adds roughly $110,000 in incremental monthly revenue. That's not a feature improvement. That's a structural gap being filled.</p>

<p>The reason the lift is this large is not a minor UX tweak. It is because conversational commerce answers the 12 questions that were blocking purchase completion for the majority of interested buyers. The <strong>B2B catalog conversion rate</strong> improvement is not coming from better product discovery. Discovery was already working. It's coming from turning product page visits into answered questions and answered questions into orders. <a href="https://chatsku.com/demo/">See the conversion impact for your catalog</a> to get a sense of what the deployment looks like in a real distributor environment.</p>

<h2>Is conversational commerce an Algolia alternative or a complement?</h2>

<p>A complement. Not a replacement. Not a competitor. Let's make that concrete.</p>

<p>Algolia's strengths are real. Fast, scalable, relevance-tuned search with rich filtering, faceted navigation, and intelligent ranking. It gets the right product in front of the right buyer in milliseconds. That capability is exactly as valuable as it sounds, and nothing in this article challenges it. If you deployed Algolia, you made a good call. It does what it was built to do.</p>

<p>Where Algolia ends is also precise. Algolia was built to optimize finding, not buying. It does not surface account-specific contract pricing from an ERP. It doesn't conduct a guided compatibility conversation. It can't generate an RFQ from a natural language request. It can't confirm MOQ requirements dynamically for a specific account. These are not criticisms: they are scope boundaries. Algolia is a search engine. The "Algolia alternative B2B" framing misses the point: you don't need an alternative to Algolia. You need the layer that does the job Algolia was never designed to do.</p>

TABLE_INJECT

<p>The correct architecture: Algolia handles discovery. The conversational layer handles the buying conversation. The buyer searches, finds the product, and gets their remaining questions answered without leaving the page, without calling a sales rep, and without a 48-hour delay. You don't re-platform. You don't replace your search investment. You add the layer that closes the gap between finding and buying.</p>

<h2>How do I get started improving my B2B catalog conversion rate?</h2>

CHECKLIST_INJECT

<h2>Conclusion</h2>

<p>Your catalog is already doing its job. Now get it to close the sale.</p>

<p>AI search solved discovery. Your buyers are finding the products. The missing piece is the conversation that answers the questions only your sales rep used to answer: contract pricing, MOQ, compatibility, lead time. ChatSKU puts that conversation on your product page, 24/7, without rebuilding your site.</p>

<p>See the live demo.</p>

<h2>Frequently asked questions</h2>

<h3>What is a good B2B catalog conversion rate?</h3>
<p>For B2B distribution, 3%-5% is a strong benchmark. The industry average sits at 2.4% for distribution and as low as 1.8% for industrial equipment, per Atwix's 2026 data. Top-performing B2B ecommerce operations exceed 5%. Most distributors with large catalogs convert below these marks because buyers cannot get account-specific answers at the point of purchase.</p>

<h3>Why does B2B ecommerce have lower conversion rates than B2C?</h3>
<p>B2B purchases require confirmation on multiple variables before a buyer commits. Contract pricing, minimum order quantities, compatibility with existing equipment, lead times from specific locations, and internal approval requirements all create friction that standard product pages cannot resolve. B2C buyers make individual decisions. B2B buyers need confirmation on business-critical variables before placing an order.</p>

<h3>Does AI search improve B2B catalog conversion rates?</h3>
<p>AI search improves product discovery and reduces zero-result rates, which produces a 10-15% relative lift in search-assisted conversion. That typically moves a 2.4% baseline to approximately 2.7%. AI search does not address the post-discovery questions: contract pricing, MOQ, inventory specificity. These drive the majority of B2B cart abandonment. The discovery problem and the conversion problem require different tools.</p>

<h3>What is conversational commerce in B2B?</h3>
<p>Conversational commerce in B2B is a chat-based layer between the buyer and the catalog that answers the account-specific questions product pages cannot. Unlike generic customer service chatbots, a B2B conversational layer connects to ERP data, contract pricing, inventory, and order history. Chat-engaged B2B visitors convert at 12.3% vs. 3.1% for non-engaged visitors, a 4x difference.</p>

<h3>Is ChatSKU a replacement for Algolia?</h3>
<p>No. ChatSKU is a complement to Algolia, not a replacement. Algolia handles search and discovery: finding the right product. ChatSKU handles the buying conversation that follows discovery: answering the account-specific questions that move a buyer from "I found it" to "I ordered it." Both run in the same architecture without conflict. You keep your Algolia investment. You add the layer that closes the conversion gap.</p>

<h3>How quickly can I add a conversational layer to my existing B2B catalog?</h3>
<p>ChatSKU connects to existing catalog sources (ERP exports, PDFs, Excel files) and deploys via a single line of code. For distributors who already have AI search infrastructure in place, implementation typically takes hours. No site rebuild or search platform migration is required.</p>
"""

# Inject enhanced blocks
DRAFT_HTML = DRAFT_HTML.replace("STATS_BLOCK_INJECT", STATS_BLOCK_HTML)
DRAFT_HTML = DRAFT_HTML.replace("TABLE_INJECT", COMPARISON_TABLE_HTML)
DRAFT_HTML = DRAFT_HTML.replace("CHECKLIST_INJECT", CHECKLIST_HTML)

# ── Em dash verification ───────────────────────────────────────────────────────
em_count = DRAFT_HTML.count("—") + DRAFT_HTML.count("&mdash;")
assert em_count == 0, f"ERROR: {em_count} em dashes found in content"
print("Em dash scan: PASS (0 found)")

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
        sec_pad = {"top": "60", "bottom": "60", "unit": "px"}  # no left/right keys
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

def build_elementor(body2_img, body3_img):
    """Parse DRAFT_HTML into Elementor sections."""

    # Color cycle: exec=f9f9fb, intro=ffffff, body starts at index 2 (=f0f4ff) per post 96
    BODY_COLORS = ["#f9f9fb", "#ffffff", "#f0f4ff", "#ffffff"]
    body_color_idx = 2  # verified from post 96

    # Section map: which H2 headings get which body image
    # Q3: "What happens between" -> body2_img
    # Q6: "How does conversational commerce improve" -> body3_img
    IMG_SECTIONS = {
        "what happens between": body2_img,
        "how does conversational commerce improve": body3_img,
    }

    elementor_sections = []

    # Split on H2 boundaries
    chunks = [c.strip() for c in re.split(r'(?=<h2[^>]*>)', DRAFT_HTML.strip()) if c.strip()]

    for chunk in chunks:
        hm = re.match(r'<h2[^>]*>(.*?)</h2>(.*)', chunk, re.DOTALL)
        if not hm:
            continue
        h2_text   = hm.group(1).strip()
        body_html = hm.group(2).strip()
        label     = h2_text.lower()

        # Detect section type
        if "executive summary" in label:
            widgets = [make_heading(h2_text), make_text(body_html)]
            elementor_sections.append(make_section(widgets, bg="#f9f9fb"))

        elif label.strip() == "introduction":
            widgets = [make_heading(h2_text), make_text(body_html)]
            elementor_sections.append(make_section(widgets, bg="#ffffff"))

        elif "conclusion" in label:
            widgets = [
                make_heading(h2_text, color="#ffffff", align="center"),
                make_text(body_html, dark_section=True),
                make_button("See the live demo", "https://chatsku.com/demo/"),
            ]
            elementor_sections.append(make_section(widgets, bg="#1a1a2e", is_conclusion=True))

        elif "frequently asked questions" in label:
            widgets = [make_heading(h2_text)]
            faq_parts = re.split(r'(?=<h3[^>]*>)', body_html.strip())
            for fp in faq_parts:
                fp = fp.strip()
                if not fp:
                    continue
                fm = re.match(r'<h3[^>]*>(.*?)</h3>(.*)', fp, re.DOTALL)
                if fm:
                    widgets.append(make_heading(fm.group(1).strip(), "h3"))
                    ans = fm.group(2).strip()
                    if ans:
                        widgets.append(make_text(ans))
            elementor_sections.append(make_section(widgets, bg="#f9f9fb"))

        else:
            # Body Q sections
            bg = BODY_COLORS[body_color_idx % len(BODY_COLORS)]
            body_color_idx += 1

            widgets = [make_heading(h2_text)]

            # Text widget first (CRITICAL: image AFTER text per Elementor 4.0.3 bug)
            if body_html:
                widgets.append(make_text(body_html))

            # Determine if this section has a body image
            img_data = None
            for kw, img in IMG_SECTIONS.items():
                if kw in label:
                    img_data = img
                    break

            if img_data:
                widgets.append(make_image_widget(img_data))  # image LAST

            elementor_sections.append(make_section(widgets, bg=bg))

    return elementor_sections

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 65)
print("BUILD: b2b-catalog-conversion-rate  (2026-06-11)")
print("=" * 65)

# ── STEP 1: Source and upload images ──────────────────────────────────────────
# Pre-selected CC0 images from StockSnap (visually verified via title/context):
#   Featured:  JBW2PXDOL6 — "Team Meeting" — business team at table with laptops
#   Body 2:    Q1OSKR7D42 — "Business Team" — team working at computers, office
#   Body 3:    RRJH1KMRMW — "Business Working" — person working at laptop, professional
# Fallback: search via Pexels/Openverse if pre-selected URL fails

PRESELECTED = {
    "featured": "https://cdn.stocksnap.io/img-thumbs/960w/JBW2PXDOL6.jpg",
    "body2":    "https://cdn.stocksnap.io/img-thumbs/960w/Q1OSKR7D42.jpg",
    "body3":    "https://cdn.stocksnap.io/img-thumbs/960w/RRJH1KMRMW.jpg",
}

def source_preselected_or_search(pre_url, fallback_queries):
    print(f"  Downloading pre-selected: {pre_url}")
    raw = download_image(pre_url)
    if raw:
        return pre_url, resize_image(raw)
    print("  Pre-selected failed, trying search fallback...")
    return source_image(fallback_queries)

print("\n[IMAGE 1/3] Featured: B2B team meeting")
FEAT_ALT = ("B2B sales team reviewing catalog conversion metrics on office computers "
            "during a product strategy meeting")
_, feat_bytes = source_preselected_or_search(
    PRESELECTED["featured"],
    ["B2B sales team office meeting", "business meeting office", "sales team office"]
)
if feat_bytes is None:
    print("FATAL: Could not source featured image"); sys.exit(1)
feat_media = upload_image(feat_bytes, "chatsku-b2b-catalog-conversion-featured.jpg", FEAT_ALT)

print("\n[IMAGE 2/3] Body: business team at computers (Q3 section)")
BODY2_ALT = ("Warehouse distributor checking B2B product catalog inventory and order "
             "specifications on a computer screen")
_, body2_bytes = source_preselected_or_search(
    PRESELECTED["body2"],
    ["warehouse inventory management computer", "distributor warehouse desk", "inventory SKU computer office"]
)
if body2_bytes is None:
    print("FATAL: Could not source body image 2"); sys.exit(1)
body2_media = upload_image(body2_bytes, "chatsku-b2b-catalog-conversion-body2.jpg", BODY2_ALT)

print("\n[IMAGE 3/3] Body: professional working at laptop (Q6 section)")
BODY3_ALT = ("B2B sales representative using conversational commerce tool on laptop to "
             "assist distributor buyer with catalog order questions")
_, body3_bytes = source_preselected_or_search(
    PRESELECTED["body3"],
    ["B2B sales conversation laptop", "sales team computer screens", "business quote document desk"]
)
if body3_bytes is None:
    print("FATAL: Could not source body image 3"); sys.exit(1)
body3_media = upload_image(body3_bytes, "chatsku-b2b-catalog-conversion-body3.jpg", BODY3_ALT)

print(f"\nImages uploaded:")
print(f"  Featured: ID={feat_media['id']}  {feat_media['url']}")
print(f"  Body2:    ID={body2_media['id']}  {body2_media['url']}")
print(f"  Body3:    ID={body3_media['id']}  {body3_media['url']}")

# Validate URLs
for lbl, m in [("Featured", feat_media), ("Body2", body2_media), ("Body3", body3_media)]:
    if not m["url"].startswith("https://chatsku.com/wp-content/uploads/"):
        print(f"FATAL: {lbl} URL invalid: {m['url']}")
        sys.exit(1)
print("All image URLs: PASS (begin with https://chatsku.com/wp-content/uploads/)")

# ── STEP 2: Build Elementor JSON ──────────────────────────────────────────────
print("\n" + "=" * 65)
print("BUILDING ELEMENTOR JSON")
print("=" * 65)

elementor_sections = build_elementor(body2_media, body3_media)
elementor_json = json.dumps(elementor_sections)

print(f"\nBuilt {len(elementor_sections)} Elementor sections:")
for i, s in enumerate(elementor_sections):
    bg   = s["settings"]["background_color"]
    pad  = s["settings"]["padding"]["top"]
    cols = s["elements"][0]["elements"]
    h    = next((w["settings"].get("title","")[:45] for w in cols if w.get("widgetType")=="heading"), "?")
    types = [w.get("widgetType") for w in cols]
    # Verify image-after-text rule
    if "image" in types and "text-editor" in types:
        img_pos  = types.index("image")
        text_pos = types.index("text-editor")
        order_ok = img_pos > text_pos
        print(f"  {i:2}: bg={bg}  pad={pad}  [{h}]  {types}  img_order={'OK' if order_ok else 'FAIL!'}")
        if not order_ok:
            print("  CRITICAL ERROR: image before text-editor!")
            sys.exit(1)
    else:
        print(f"  {i:2}: bg={bg}  pad={pad}  [{h}]  {types}")

# Validate JSON
parsed_check = json.loads(elementor_json)
assert isinstance(parsed_check, list) and len(parsed_check) > 0, "Elementor JSON empty"
print(f"\nElementor JSON: {len(elementor_json):,} chars  {len(parsed_check)} sections")

# ── STEP 3: Pre-publish checklist ─────────────────────────────────────────────
print("\n" + "=" * 65)
print("PRE-PUBLISH CHECKLIST")
print("=" * 65)

checks = {}

# Em dashes
ed = DRAFT_HTML.count("—") + DRAFT_HTML.count("&mdash;")
checks["No em dashes"] = ed == 0
print(f"  [{'PASS' if checks['No em dashes'] else 'FAIL'}] Em dashes: {ed}")

# Slug uniqueness
existing_slugs = [
    "rfq-automation-manufacturers", "rfq-automation-for-product-catalogs",
    "ai-chatbot-for-manufacturers-dallas", "b2b-ecommerce-chatbot-dallas",
    "pdf-catalog-sales-liability", "rfq-form-conversion-rate",
]
new_slug = "b2b-catalog-conversion-rate"
checks["Slug unique"] = new_slug not in existing_slugs
print(f"  [{'PASS' if checks['Slug unique'] else 'FAIL'}] Slug '{new_slug}' unique")

# Featured media set
checks["Featured media"] = bool(feat_media["id"])
print(f"  [{'PASS' if checks['Featured media'] else 'FAIL'}] Featured media ID: {feat_media['id']}")

# Image URLs
url_ok = all(m["url"].startswith("https://chatsku.com/wp-content/uploads/")
             for m in [feat_media, body2_media, body3_media])
checks["Image URLs"] = url_ok
print(f"  [{'PASS' if url_ok else 'FAIL'}] All image URLs: chatsku.com/wp-content/uploads/")

# Image order (image AFTER text-editor)
order_ok = True
for s in elementor_sections:
    types = [w.get("widgetType") for w in s["elements"][0]["elements"]]
    if "image" in types and "text-editor" in types:
        if types.index("image") < types.index("text-editor"):
            order_ok = False
checks["Image widget order"] = order_ok
print(f"  [{'PASS' if order_ok else 'FAIL'}] Image widgets AFTER text-editor in every section")

# Build WP content (stripped of img tags, H1)
wp_content = re.sub(r'<h1[^>]*>.*?</h1>', '', DRAFT_HTML, flags=re.DOTALL).strip()
wp_content = re.sub(r'<img[^>]*/>', '', wp_content).strip()
wp_content = re.sub(r'<img[^>]*>', '', wp_content).strip()
no_bare_img = not bool(re.search(r'<img[^>]*>', wp_content))
checks["No bare img"] = no_bare_img
print(f"  [{'PASS' if no_bare_img else 'FAIL'}] No bare <img> tags in WP content")

# External links <= 2
ext_links = re.findall(r'href="https?://(?!chatsku\.com)[^"]+', DRAFT_HTML)
checks["External links"] = len(ext_links) <= 2
print(f"  [{'PASS' if checks['External links'] else 'FAIL'}] External links: {len(ext_links)} (max 2)")
for el in ext_links:
    print(f"    {el[:80]}")

# Internal links 3-5
int_links = re.findall(r'href="https://chatsku\.com/[^"]+', DRAFT_HTML)
checks["Internal links"] = 3 <= len(int_links) <= 5
print(f"  [{'PASS' if checks['Internal links'] else 'FAIL'}] Internal links: {len(int_links)} (target 3-5)")
for il in int_links:
    print(f"    {il[:80]}")

# No competitor links
competitor_domains = ["drift.com", "intercom.com", "tidio.com"]
no_comp = not any(cd in DRAFT_HTML for cd in competitor_domains)
checks["No competitor links"] = no_comp
print(f"  [{'PASS' if no_comp else 'FAIL'}] No competitor links")

# Conclusion: dark bg, white heading, button
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

# Elementor JSON non-empty
checks["Elementor JSON"] = len(elementor_sections) > 0
print(f"  [{'PASS' if checks['Elementor JSON'] else 'FAIL'}] Elementor JSON: {len(elementor_sections)} sections")

# Status = draft
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

payload = {
    "title": "Why your B2B catalog conversion rate is still stuck (and what to do about it)",
    "slug": "b2b-catalog-conversion-rate",
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

# ── STEP 5: Verify saved data ──────────────────────────────────────────────────
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

# ── STEP 6: Clear Elementor cache ─────────────────────────────────────────────
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

# ── STEP 7: Save published HTML ────────────────────────────────────────────────
print("\nSaving published HTML...")

# Build full-page HTML with featured image at top
published_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Why your B2B catalog conversion rate is still stuck (and what to do about it) | ChatSKU</title>
<meta name="description" content="Your AI search is working but your B2B catalog conversion rate is still stuck at 2%. Learn why discovery was never the problem and how conversational commerce fixes it.">
<meta name="robots" content="index,follow">
<!-- ChatSKU Published Post -->
<!-- Post ID: {post_id} -->
<!-- Date: 2026-06-11 -->
<!-- Slug: b2b-catalog-conversion-rate -->
<!-- Featured Media ID: {feat_media['id']} -->
<!-- Body Image 2 ID: {body2_media['id']} -->
<!-- Body Image 3 ID: {body3_media['id']} -->
<!-- Status: draft -->
<!-- Yoast meta: SET MANUALLY in WP dashboard -->
<!-- Yoast title: B2B Catalog Conversion Rate: Why AI Search Isn't Enough | ChatSKU -->
<!-- Yoast desc: Your AI search is working but your B2B catalog conversion rate is still stuck at 2%. Learn why discovery was never the problem and how conversational commerce fixes it. -->
</head>
<body>

<h1>Why your B2B catalog conversion rate is still stuck (and what to do about it)</h1>

<!-- Featured image: 860x452 | Media ID: {feat_media['id']} -->
<img src="{feat_media['url']}" width="860" height="452" alt="{FEAT_ALT}">

{DRAFT_HTML}

</body>
</html>"""

out_path = Path(r"C:\content-intel\clients\chatsku\output\published\b2b-catalog-conversion-rate-2026-06-11.html")
out_path.write_text(published_html, encoding="utf-8")
print(f"  Saved: {out_path}")

# ── STEP 8: Update published-posts-inventory.md is deferred (manual) ──────────
# (done separately after confirming post is live)

# ── FINAL REPORT ──────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("PUBLISH COMPLETE")
print("=" * 65)
print(f"  Post ID:           {post_id}")
print(f"  Post URL:          {post_link}")
print(f"  Post status:       draft")
print(f"  Featured media ID: {feat_media['id']}")
print(f"  Body image 2 ID:   {body2_media['id']}")
print(f"  Body image 3 ID:   {body3_media['id']}")
print(f"  Elementor sections:{len(elementor_sections)}")
print(f"  Published HTML:    {out_path}")
print()
print("MANUAL FOLLOW-UP REQUIRED:")
print("  1. WP Admin > Posts > Edit post")
print("  2. Yoast SEO > SEO tab > enter:")
print("     Title:  B2B Catalog Conversion Rate: Why AI Search Isn't Enough | ChatSKU")
print("     Desc:   Your AI search is working but your B2B catalog conversion rate is still")
print("             stuck at 2%. Learn why discovery was never the problem and how")
print("             conversational commerce fixes it.")
print("  (Yoast meta cannot be set via REST API on chatsku.com)")
print()
print(f"RESULTS_JSON={json.dumps({'post_id': post_id, 'post_link': post_link, 'feat_id': feat_media['id'], 'body2_id': body2_media['id'], 'body3_id': body3_media['id']})}")
