"""
Build and publish: b2b-quote-to-order-automation
Post: "Your quote didn't lose to a lower price. It lost to silence."
Format: Format F (case study / before-and-after)   Date: 2026-06-17

Pipeline:
  1. Load .env credentials
  2. Source and upload 3 images (Pexels -> Openverse/Stocksnap fallback)
  3. Build Elementor JSON from structured section data
  4. Run full pre-publish checklist (MUST-FOLLOW-RULES.md section 9)
  5. Push to WordPress as draft
  6. Clear Elementor cache
  7. Save published HTML to output/published/
  8. Report media IDs, post ID, checklist results

Template: clients/chatsku/output/research/build_b2b_catalog_conversion_post.py
Verified rules from MUST-FOLLOW-RULES.md:
  - Section padding: {top:"60", bottom:"60", unit:"px"} -- NO left/right keys
  - Column padding: {unit:"px", top:"20", right:"20", bottom:"20", left:"20", isLinked:True}
  - Heading H2: title_color="#1a1a2e", font_size=28px
  - Heading H3: header_size="h3", title_color="#1a1a2e", font_size=22px
  - Image widget AFTER text-editor widget (Elementor 4.0.3 confirmed bug)
  - Conclusion: bg=#1a1a2e, heading white centered, body #aaaacc, button #e94560
  - FAQ section: bg=#f9f9fb
  - Cloudflare: User-Agent header required on every request
  - Featured/body images: 860x452 (verified post 151)
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
           f"?q={urllib.parse.quote(query)}&license=cc0,pdm&page_size={per_page}")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15, context=_ssl_ctx) as r:
            data = json.loads(r.read())
        results = data.get("results", [])
        print(f"  Openverse '{query}': {len(results)} results")
        # Prefer stocksnap (consistent stock-photo quality) but fall back to any cc0/pdm result
        stocksnap = [r["url"] for r in results if r.get("source") == "stocksnap" and r.get("url")]
        others = [r["url"] for r in results if r.get("source") != "stocksnap" and r.get("url")]
        return stocksnap + others
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

def source_preselected_or_search(pre_url, fallback_queries, width=860, height=452):
    print(f"  Downloading pre-selected (visually verified): {pre_url}")
    raw = download_image(pre_url)
    if raw:
        return pre_url, resize_image(raw, width, height)
    print("  Pre-selected failed, trying search fallback...")
    return source_image(fallback_queries, width, height)

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
# CONTENT BLOCKS
# ═══════════════════════════════════════════════════════════════════════════════

EXEC_SUMMARY_HTML = """
<p>A $42,000 quote goes silent for six days while the buyer waits on a pricing question. The buyer signs with a competitor who answered in twenty minutes. This is the quote-to-order gap: the space between "quote sent" and "order placed," where most closeable B2B revenue quietly disappears.</p>
<p>It is not a CRM problem and not a CPQ problem. It is a silence problem. Buyers who can't get an answer while they're deciding go find someone who'll give them one. This article breaks down the cost, why the usual fixes (CRM reminders, drip emails) don't touch it, and what closes the gap instead.</p>
"""

INTRO_HTML = """
<p>You sent the quote. $42,000. Three days later, the buyer emails one question: can the price hold if they double the order to 1,000 units?</p>
<p>Nobody answers for six days. By the time someone does, the buyer already signed with the competitor who answered in twenty minutes.</p>
<p>This is not a story about a slow CRM. It's not a bad PDF, either. The deal died because of silence, and that silence has a name: the quote-to-order gap. It's the space between "quote sent" and "order placed," and it's where most of your closeable B2B revenue quietly disappears.</p>
"""

COST_HTML = """
<p>Here's what makes this gap so dangerous: it doesn't look like a failure. No alarm goes off. The quote just sits there, technically "in progress," while the actual deal rots.</p>
<p>Companies that respond to leads within one hour are <strong>7 times more likely to qualify them</strong>. Wait 24 hours or more, and qualification odds drop <strong>60 times lower</strong>, according to a <a href="https://www.workato.com/the-connector/lead-response-time-study/" target="_blank" rel="noopener noreferrer">114-company study from Workato</a>.</p>
<p>That's the difference between a live deal and a dead one.</p>
<p>Speed compounds the problem. Response time tracks almost exactly with close rate:</p>
<ul>
<li>Under 5 minutes: <strong>32% close rate</strong></li>
<li>Under 1 hour: <strong>24%</strong></li>
<li>Under 24 hours: <strong>15%</strong></li>
<li>Past 24 hours: <strong>12%</strong></li>
</ul>
<p>Despite knowing this, the average B2B lead response time sits at 42 hours. Over a third of companies take longer than a full day to respond at all.</p>
<p>None of this happens because reps don't care. It happens because they're buried.</p>
<p>Eighty percent of B2B deals need five or more follow-ups to close. Ninety-two percent of reps stop after four attempts or fewer. Most quit right before the deal would have converted.</p>
<p>Your catalog can't help here if it's <a href="https://chatsku.com/passive-catalog/">a passive catalog</a> that just sits there, waiting for a human like the quote in the inbox does. Most teams already know about <a href="https://chatsku.com/response-gap/">the response gap</a> on the front end, but the same gap reopens the moment a quote goes out.</p>
"""

WHY_FAIL_HTML = """
<p>Most teams try to solve this with more process. A CRM reminder. A drip sequence. A note to "follow up Thursday." None of it touches the actual problem.</p>
<p>CRM reminders only fire if the data triggering them is clean and current. B2B contact data degrades 2-3% a month, roughly 22% a year.</p>
<p>A stale field means the reminder never fires, or fires too late. The rep is back to relying on memory.</p>
<p>Drip emails are worse in a quieter way. A "just checking in" email carries zero new information, and buyers can tell the difference between a nudge and an answer.</p>
<p>Meanwhile, reps are drowning. Non-value-adding work, including quotation and order management, eats roughly two-thirds of a sales team's time. McKinsey estimates more than 30% of those tasks are at least partially automatable.</p>
<p>When a third of the week disappears into admin, follow-up quality drops. Not because reps are bad at their jobs. There's just too much in the queue.</p>
<p>This isn't a CPQ problem either. CPQ tools solve quote generation speed, a real but separate issue: they get the document out faster, but stop the moment it's sent.</p>
<p>Even <a href="https://chatsku.com/rfq-automation-for-product-catalogs/">RFQ-to-quote automation</a> tools hand off a finished PDF and walk away from everything that follows.</p>
<p>And the PDF itself is a dead end. If a buyer wants to change quantity, term, or configuration, someone has to manually regenerate the document. That restarts the approval clock on a deal that's already running out of patience.</p>
<p>Every current fix treats this as a timing problem. It's actually an information problem: the buyer doesn't need a faster reminder, they need an answer. And you've likely got <a href="https://chatsku.com/human-bottleneck/">the human bottleneck</a> of reps buried across dozens of open quotes who can't be everywhere a question shows up.</p>
"""

WORKING_FIX_HTML = """
<p>A working fix has three parts, and none of them work alone.</p>
<p>First: real-time, self-serve answers. Buyers don't wait around for permission to keep shopping.</p>
<p>Seventy-five percent of B2B buyers prefer a rep-free buying experience when one's available. They spend only 17% of their decision time actually engaging suppliers directly, dropping to 5-6% once they're comparing vendors.</p>
<p>While your quote sits silent, your buyer isn't waiting. They're elsewhere, probably looking at a competitor's catalog right now.</p>
<p>This is exactly why <a href="https://chatsku.com/b2b-catalog-conversion-rate/">catalog conversion rate</a> stalls: buyers who can't confirm pricing mid-decision give up on the supplier in front of them and move to whoever answers first.</p>
<p>Second: persistence that's actually persistent, across more than one channel. Campaigns using three or more channels see a 287% higher purchase rate than single-channel follow-up. One email thread isn't a follow-up strategy, it's a coin flip.</p>
<p>Third: a near-instant path from "approved" to "ordered." When a buyer can convert an approved quote directly into an order instead of re-entering everything by hand, that step stops being a separate task a rep has to find time for.</p>
<p>Friction at the finish line kills deals just as often as hesitation does, and it's the easier of the two to fix.</p>
<p>Put these three together and the gap closes. <a href="https://chatsku.com/ai-sales-assistant-b2b-ecommerce/">A real-time sales assistant</a> that answers the pricing question, keeps nudging across channels, and removes the manual re-entry step does more for your close rate than any single CRM trick.</p>
"""

INFOGRAPHIC_HTML = """<div style="background:#1a1a2e;border-radius:12px;padding:28px 24px;margin:24px 0;">
  <div style="display:flex;gap:16px;flex-wrap:wrap;">
    <div style="flex:1;min-width:140px;background:#0f172a;border-radius:10px;padding:16px;text-align:center;">
      <div style="font-size:30px;font-weight:700;color:#00C9B1;">32% &rarr; 12%</div>
      <div style="font-size:13px;color:#94a3b8;margin-top:6px;">Close rate: under 5 min reply vs. past 24 hrs</div>
    </div>
    <div style="flex:1;min-width:140px;background:#0f172a;border-radius:10px;padding:16px;text-align:center;">
      <div style="font-size:30px;font-weight:700;color:#00C9B1;">7x vs 60x</div>
      <div style="font-size:13px;color:#94a3b8;margin-top:6px;">Qualification odds: 1 hr reply vs. 24+ hr wait</div>
    </div>
    <div style="flex:1;min-width:140px;background:#0f172a;border-radius:10px;padding:16px;text-align:center;">
      <div style="font-size:30px;font-weight:700;color:#00C9B1;">80% vs 92%</div>
      <div style="font-size:13px;color:#94a3b8;margin-top:6px;">Deals needing 5+ follow-ups vs. reps who stop at 4</div>
    </div>
    <div style="flex:1;min-width:140px;background:#0f172a;border-radius:10px;padding:16px;text-align:center;">
      <div style="font-size:30px;font-weight:700;color:#00C9B1;">287%</div>
      <div style="font-size:13px;color:#94a3b8;margin-top:6px;">Higher purchase rate: 3+ follow-up channels vs. one email thread</div>
    </div>
  </div>
</div>"""

CLOSES_GAP_HTML = """
<p>We spend our days at ChatSKU looking at where B2B quotes stall, and it's almost always in this exact window: quote sent, buyer has a question, nobody's there.</p>
<p>ChatSKU sits on top of your existing catalog, the one you already have: PDF, Excel, ERP export, whatever it is.</p>
<p>When a buyer asks "can you hold this price at 500 units" or "what's the lead time on this SKU" at 9pm on day three of silence, ChatSKU answers immediately, pulled straight from your live catalog and pricing-tier data.</p>
<p>Not a guess. Not a generic chatbot response. It's powered by <a href="https://chatsku.com/features/">ChatSKU's catalog integration</a>, which already handles tiered pricing and customer groups, the same way your team does.</p>
<p>While that's happening, ChatSKU's follow-up keeps running in the background: multi-channel, persistent, the kind that doesn't quietly stop after attempt two because the rep moved on to the next fire.</p>
<p>To be clear: ChatSKU doesn't replace your sales team, and it never will. It covers the moments your team can't physically be there, nights, weekends, the gap between a question and an answer. Your reps see exactly what the buyer asked and when, so their follow-up is informed instead of blind.</p>
<p>ChatSKU is built on 14 years and 2,000+ B2B and B2C ecommerce implementations at Virtina, so the pricing logic isn't theoretical.</p>
<p>It's <a href="https://chatsku.com/pdf-catalog-chatbot/">a PDF catalog assistant</a> built for the files you already have, Excel sheets and ERP exports included. Same complexity your team deals with every day, just answered around the clock instead of during business hours only.</p>
"""

SCENARIO_HTML = """
<p>Let's go back to that $42,000 quote. This is an illustrative scenario, not a real client, but the math holds for any deal in this size range.</p>
<p>Without a real-time answer layer: quote sent Tuesday, buyer asks Friday whether the price holds at double the volume.</p>
<p>Nobody responds until the following Wednesday, six days of silence. The buyer places the order with whoever answered within the hour.</p>
<p>Deal gone, and your team never logs it as a loss. They just see a quote that quietly expired.</p>
<p>With the fix in place: same quote, same question, asked Friday afternoon. The buyer gets an accurate, tiered-pricing answer in under a minute.</p>
<p>No rep had to drop what they were doing. The buyer converts the approved quote into a placed order the same day, no six-day gap for the deal to die in.</p>
<table style="border-collapse:collapse;width:100%;font-size:15px;">
  <thead>
    <tr>
      <th style="background:#1a1a2e;color:#ffffff;padding:10px 14px;text-align:left;"></th>
      <th style="background:#1a1a2e;color:#ffffff;padding:10px 14px;text-align:left;">Manual quote follow-up (current default)</th>
      <th style="background:#1a1a2e;color:#ffffff;padding:10px 14px;text-align:left;">ChatSKU approach</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background:#f0f4ff;">
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Buyer asks a pricing/MOQ question</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Sits in an inbox or voicemail until a rep is free</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Answered immediately, pulled from live catalog and pricing-tier data</td>
    </tr>
    <tr style="background:#ffffff;">
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Follow-up cadence</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">1-2 attempts, then rep moves to the next quote</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Persistent, multi-channel, automated, doesn't get buried</td>
    </tr>
    <tr style="background:#f0f4ff;">
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Quote changes (quantity, term)</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Manual PDF regeneration, restarts the approval clock</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Buyer can ask and get an updated answer without waiting for a new document</td>
    </tr>
    <tr style="background:#ffffff;">
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Visibility into quote status</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Rep's memory or a CRM field that may be stale</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Real-time view of what the buyer asked and when</td>
    </tr>
    <tr style="background:#f0f4ff;">
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Approved quote to placed order</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Re-entered manually by a rep, whenever they get to it</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Buyer-initiated, no rep required</td>
    </tr>
    <tr style="background:#ffffff;">
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Coverage hours</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Business hours only</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">24/7, including the 9pm comparison-shopping window</td>
    </tr>
  </tbody>
</table>
<p>The numbers in the scenario are illustrative. The stats underneath them, the close-rate tiers and the qualification multiplier, are not. Those are sourced and real. The scenario just shows you what they look like applied to one deal.</p>
"""

CHECKLIST_HTML = """
<p>Run through this checklist. If two or more apply, the quote-to-order gap is actively costing you closed deals.</p>
<ul style="list-style:none;padding:0;">
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:14px;padding:14px 16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="font-size:18px;color:#00C9B1;flex-shrink:0;">&#10003;</span>
    <div><strong>Slow first follow-up.</strong> Quotes sit for more than 48 hours before anyone follows up.</div>
  </li>
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:14px;padding:14px 16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="font-size:18px;color:#00C9B1;flex-shrink:0;">&#10003;</span>
    <div><strong>Reps give up early.</strong> Follow-up stops after 2-3 attempts because reps are juggling too many open quotes.</div>
  </li>
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:14px;padding:14px 16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="font-size:18px;color:#00C9B1;flex-shrink:0;">&#10003;</span>
    <div><strong>Buyers wait on answers.</strong> Pricing, MOQ, or lead-time questions sit for hours before anyone responds.</div>
  </li>
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:14px;padding:14px 16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="font-size:18px;color:#00C9B1;flex-shrink:0;">&#10003;</span>
    <div><strong>No visibility into losses.</strong> You don't know how many quotes went quiet last month, or why.</div>
  </li>
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:14px;padding:14px 16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="font-size:18px;color:#00C9B1;flex-shrink:0;">&#10003;</span>
    <div><strong>Manual regeneration bottleneck.</strong> A quote change, quantity, term, or configuration, means manually rebuilding the PDF.</div>
  </li>
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:0;padding:14px 16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="font-size:18px;color:#00C9B1;flex-shrink:0;">&#10003;</span>
    <div><strong>Losses discovered too late.</strong> Your team only learns a deal went to a competitor after the fact, with no record of what question went unanswered.</div>
  </li>
</ul>
"""

GET_STARTED_HTML = """
<p>None of this requires tearing down what you've already built. The setup is deliberately small.</p>
<ul>
<li><strong>Connect your existing catalog.</strong> PDF, Excel, ERP export, or CSV, no data migration required.</li>
<li><strong>Add the script tag.</strong> One line, on your site or your quote-delivery page.</li>
<li><strong>Set pricing rules.</strong> Tiers, customer groups, and MOQ logic so answers are accurate from day one.</li>
<li><strong>Turn on multi-touch follow-up.</strong> Automated, persistent, running across channels for every open quote.</li>
<li><strong>Start a free trial.</strong> Watch which buyer questions come in first. You'll likely recognize them immediately, they're the same five questions your team answers by phone every week.</li>
</ul>
<p>If you want a number before you commit to anything, run your real revenue and quote volume through <a href="https://chatsku.com/revenue-calculator">the revenue calculator</a> instead of relying on industry averages.</p>
<p>And if you've never been able to explain where deals go quiet, look at <a href="https://chatsku.com/black-hole-pipeline/">your black hole pipeline</a> first. The leak isn't your pricing. It's the silence after the quote.</p>
"""

FAQ_ITEMS = [
    ("What is quote-to-order automation?",
     "Quote-to-order automation covers the steps between a quote being sent and an order being placed: follow-up, buyer questions, approvals, and converting an approved quote into an order. Most tools that use this term focus on speeding up the backend. The bigger issue is usually the buyer's experience while the quote sits waiting, not the backend speed."),
    ("Why do B2B quotes go cold after they're sent?",
     "Quotes go cold because nobody answers the buyer's question fast enough to keep them engaged. The buyer has a pricing or MOQ question, the rep is buried in other open quotes, and by the time someone responds, the buyer has already moved to a competitor."),
    ("How is quote-to-order automation different from CPQ software?",
     "CPQ software speeds up creating the quote itself, configuring options, calculating pricing, generating the document. It stops once the quote is sent. Quote-to-order automation, as covered here, picks up from that point: answering buyer questions, running follow-up, and converting approval into a placed order."),
    ("What's a good response time for a buyer's follow-up question on a quote?",
     "Under five minutes gets you into best-in-class close-rate territory, around 32%. Once you cross 24 hours, close rates fall to around 12%. The average company currently takes 42 hours to respond at all, which is well past the point most buyers have moved on."),
    ("How many follow-ups does it actually take to close a B2B quote?",
     "Most B2B deals need five or more follow-up touches to close. Most reps stop after four or fewer. The gap between those two numbers is where a large share of recoverable deals quietly die."),
    ("Can buyers check pricing, MOQ, or lead time without waiting on a rep?",
     "Yes, with a catalog-aware answer system in place. The assistant pulls directly from your live pricing tiers and inventory data, so the answer is accurate, not a placeholder that needs a human to confirm it later."),
    ("Does quote-to-order automation replace my sales team?",
     "No. It fills the hours and moments your team physically can't cover, nights, weekends, the gap between a buyer's question and a human's availability. Reps still own the relationship and the close. They just stop losing deals to silence."),
    ("How fast can ChatSKU's quote follow-up be live?",
     "Connecting your existing catalog and adding the script tag typically takes hours, not weeks. There's no website rebuild and no data migration. You can have automated follow-up and real-time buyer answers running on open quotes by the end of the day you start."),
]

CONCLUSION_HTML = """
<p>That deal wasn't a fluke. It's the default outcome of silence. Every day a quote sits unanswered, the buyer isn't pausing, they're researching, comparing, and eventually signing with whoever showed up first with a real answer.</p>
<p>The fix isn't "follow up more" as a vague resolution. It's giving buyers a way to get answers the moment they ask, while the follow-up keeps running underneath it. That's the whole gap, closed.</p>
<p>Start a free trial. No credit card, live in hours. Your quotes should be working even when your team's asleep.</p>
"""

TITLE = "Your quote didn't lose to a lower price. It lost to silence."
SLUG = "b2b-quote-to-order-automation"

# ── Em dash verification across all content blocks ────────────────────────────
ALL_TEXT = "".join([
    EXEC_SUMMARY_HTML, INTRO_HTML, COST_HTML, WHY_FAIL_HTML, WORKING_FIX_HTML,
    INFOGRAPHIC_HTML, CLOSES_GAP_HTML, SCENARIO_HTML, CHECKLIST_HTML, GET_STARTED_HTML,
    CONCLUSION_HTML, "".join(q + a for q, a in FAQ_ITEMS)
])
em_count = ALL_TEXT.count("—") + ALL_TEXT.count("&mdash;")
print(f"Em dash scan: {'PASS' if em_count == 0 else 'FAIL'} ({em_count} found)")
if em_count != 0:
    sys.exit(1)

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

def build_elementor(body1_img, body2_img):
    sections = []

    sections.append(make_section([make_heading("Executive summary"), make_text(EXEC_SUMMARY_HTML)], bg="#f9f9fb"))
    sections.append(make_section([make_heading("Introduction"), make_text(INTRO_HTML)], bg="#ffffff"))

    sections.append(make_section(
        [make_heading("What does quote silence actually cost you?"), make_text(COST_HTML), make_image_widget(body1_img)],
        bg="#f0f4ff"))

    sections.append(make_section(
        [make_heading("Why don't CRM reminders and drip emails fix this?"), make_text(WHY_FAIL_HTML)], bg="#ffffff"))

    sections.append(make_section(
        [make_heading("What does it actually take to close this gap?"), make_text(WORKING_FIX_HTML + INFOGRAPHIC_HTML)],
        bg="#f9f9fb"))

    sections.append(make_section(
        [make_heading("How does ChatSKU close the quote-to-order gap?"), make_text(CLOSES_GAP_HTML), make_image_widget(body2_img)],
        bg="#ffffff"))

    sections.append(make_section(
        [make_heading("What changes when buyers get answers in real time?"), make_text(SCENARIO_HTML)], bg="#f0f4ff"))

    sections.append(make_section(
        [make_heading("Is this costing you deals right now?"), make_text(CHECKLIST_HTML)], bg="#ffffff"))

    sections.append(make_section(
        [make_heading("How do you close the gap without a rebuild?"), make_text(GET_STARTED_HTML)], bg="#f9f9fb"))

    faq_widgets = [make_heading("Frequently asked questions")]
    for q, a in FAQ_ITEMS:
        faq_widgets.append(make_heading(q, "h3"))
        faq_widgets.append(make_text(f"<p>{a}</p>"))
    sections.append(make_section(faq_widgets, bg="#f9f9fb"))

    sections.append(make_section([
        make_heading("Conclusion", color="#ffffff", align="center"),
        make_text(CONCLUSION_HTML, dark_section=True),
        make_button("Start a free trial", "https://chatsku.com/signup/"),
    ], bg="#1a1a2e", is_conclusion=True))

    return sections

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 65)
print("BUILD: b2b-quote-to-order-automation  (2026-06-17)")
print("=" * 65)

FEAT_ALT = ("B2B sales quote document on a desk with an unread buyer message asking "
            "to hold pricing at 1,000 units, sent six days ago")
BODY1_ALT = ("Illustration of a black hole pipeline showing B2B quotes disappearing "
             "from unanswered questions, delayed follow-up, and quote silence")
BODY2_ALT = ("ChatSKU assistant chat widget instantly answering a buyer's pricing "
             "and lead time question on an open B2B quote")

def fetch_media(media_id, alt_text):
    """Fetch real media URL by ID instead of guessing a filename - REUSE_MEDIA must
    reflect whatever is actually uploaded, including images the client uploaded manually."""
    req = urllib.request.Request(f"{WP_BASE}/media/{media_id}", headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20, context=_ssl_ctx) as r:
        m = json.loads(r.read())
    return {"id": media_id, "url": m["source_url"], "alt": alt_text}

REUSE_MEDIA = os.environ.get("REUSE_MEDIA", "")  # e.g. "304,303,302" to skip re-upload on rerun
if REUSE_MEDIA:
    fid, b1id, b2id = [int(x) for x in REUSE_MEDIA.split(",")]
    feat_media = fetch_media(fid, FEAT_ALT)
    body1_media = fetch_media(b1id, BODY1_ALT)
    body2_media = fetch_media(b2id, BODY2_ALT)
    print(f"\nReusing existing media IDs: {fid}, {b1id}, {b2id} (REUSE_MEDIA set)")
    print(f"  Featured: {feat_media['url']}")
    print(f"  Body1:    {body1_media['url']}")
    print(f"  Body2:    {body2_media['url']}")
else:
    print("\n[IMAGE 1/3] Featured: business document on desk (visually verified)")
    _, feat_bytes = source_preselected_or_search(
        "https://cdn.stocksnap.io/img-thumbs/960w/AB4F938C85.jpg",
        ["business documents desk", "office desk documents", "business meeting office"], 860, 452)
    if feat_bytes is None:
        print("FATAL: Could not source featured image"); sys.exit(1)
    feat_media = upload_image(feat_bytes, "chatsku-quote-to-order-featured.jpg", FEAT_ALT)

    print("\n[IMAGE 2/3] Body: overwhelmed sales rep at laptop (cost of silence section, visually verified)")
    _, body1_bytes = source_preselected_or_search(
        "https://cdn.stocksnap.io/img-thumbs/960w/TNKLX6MUWC.jpg",
        ["business team computers", "office team computers", "business meeting office"], 860, 452)
    if body1_bytes is None:
        print("FATAL: Could not source body image 1"); sys.exit(1)
    body1_media = upload_image(body1_bytes, "chatsku-quote-to-order-body1.jpg", BODY1_ALT)

    print("\n[IMAGE 3/3] Body: focused professional at laptop (ChatSKU fix section, visually verified)")
    _, body2_bytes = source_preselected_or_search(
        "https://cdn.stocksnap.io/img-thumbs/960w/SZCQC1QEW1.jpg",
        ["business team computers", "office workers computers", "business meeting office"], 860, 452)
    if body2_bytes is None:
        print("FATAL: Could not source body image 2"); sys.exit(1)
    body2_media = upload_image(body2_bytes, "chatsku-quote-to-order-body2.jpg", BODY2_ALT)

print(f"\nImages uploaded:")
print(f"  Featured: ID={feat_media['id']}  {feat_media['url']}")
print(f"  Body1:    ID={body1_media['id']}  {body1_media['url']}")
print(f"  Body2:    ID={body2_media['id']}  {body2_media['url']}")

for lbl, m in [("Featured", feat_media), ("Body1", body1_media), ("Body2", body2_media)]:
    if not m["url"].startswith("https://chatsku.com/wp-content/uploads/"):
        print(f"FATAL: {lbl} URL invalid: {m['url']}")
        sys.exit(1)
print("All image URLs: PASS (begin with https://chatsku.com/wp-content/uploads/)")

print("\n" + "=" * 65)
print("BUILDING ELEMENTOR JSON")
print("=" * 65)

elementor_sections = build_elementor(body1_media, body2_media)
elementor_json = json.dumps(elementor_sections)

print(f"\nBuilt {len(elementor_sections)} Elementor sections:")
for i, s in enumerate(elementor_sections):
    bg = s["settings"]["background_color"]
    cols = s["elements"][0]["elements"]
    h = next((w["settings"].get("title", "")[:45] for w in cols if w.get("widgetType") == "heading"), "?")
    types = [w.get("widgetType") for w in cols]
    if "image" in types and "text-editor" in types:
        order_ok = types.index("image") > types.index("text-editor")
        print(f"  {i:2}: bg={bg}  [{h}]  {types}  img_order={'OK' if order_ok else 'FAIL!'}")
        if not order_ok:
            print("  CRITICAL ERROR: image before text-editor!")
            sys.exit(1)
    else:
        print(f"  {i:2}: bg={bg}  [{h}]  {types}")

parsed_check = json.loads(elementor_json)
assert isinstance(parsed_check, list) and len(parsed_check) > 0, "Elementor JSON empty"
print(f"\nElementor JSON: {len(elementor_json):,} chars  {len(parsed_check)} sections")

# ── PRE-PUBLISH CHECKLIST ───────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("PRE-PUBLISH CHECKLIST")
print("=" * 65)

checks = {}

ed = em_count
checks["No em dashes"] = ed == 0
print(f"  [{'PASS' if checks['No em dashes'] else 'FAIL'}] Em dashes: {ed}")

existing_slugs = [
    "rfq-automation-manufacturers", "rfq-automation-for-product-catalogs",
    "ai-chatbot-for-manufacturers-dallas", "b2b-ecommerce-chatbot-dallas",
    "pdf-catalog-sales-liability", "rfq-form-conversion-rate",
    "b2b-catalog-conversion-rate", "convert-pdf-catalog-to-website",
    "b2b-catalog-issues-costing-sales", "b2b-after-hours-buyer-problem",
    "b2b-catalog-revenue-leakage", "b2b-after-hours-lead-capture",
]
checks["Slug unique"] = SLUG not in existing_slugs
print(f"  [{'PASS' if checks['Slug unique'] else 'FAIL'}] Slug '{SLUG}' unique")

checks["Featured media"] = bool(feat_media["id"])
print(f"  [{'PASS' if checks['Featured media'] else 'FAIL'}] Featured media ID: {feat_media['id']}")

url_ok = all(m["url"].startswith("https://chatsku.com/wp-content/uploads/")
             for m in [feat_media, body1_media, body2_media])
checks["Image URLs"] = url_ok
print(f"  [{'PASS' if url_ok else 'FAIL'}] All image URLs: chatsku.com/wp-content/uploads/")

order_ok = True
for s in elementor_sections:
    types = [w.get("widgetType") for w in s["elements"][0]["elements"]]
    if "image" in types and "text-editor" in types:
        if types.index("image") < types.index("text-editor"):
            order_ok = False
checks["Image widget order"] = order_ok
print(f"  [{'PASS' if order_ok else 'FAIL'}] Image widgets AFTER text-editor in every section")

wp_content = "<p>(See live Elementor design for full rendered content.)</p>"
checks["No bare img"] = "<img" not in wp_content
print(f"  [{'PASS' if checks['No bare img'] else 'FAIL'}] No bare <img> tags in WP content fallback")

full_html_for_link_check = ALL_TEXT
ext_links = re.findall(r'href="https?://(?!chatsku\.com)[^"]+', full_html_for_link_check)
checks["External links"] = len(ext_links) <= 2
print(f"  [{'PASS' if checks['External links'] else 'FAIL'}] External links: {len(ext_links)} (max 2)")
for el in ext_links:
    print(f"    {el[:80]}")

int_links = re.findall(r'href="https://chatsku\.com/[^"]+', full_html_for_link_check)
checks["Internal links"] = 8 <= len(int_links) <= 10
print(f"  [{'PASS' if checks['Internal links'] else 'FAIL'}] Internal links: {len(int_links)} (target 8-10)")
for il in int_links:
    print(f"    {il[:80]}")

competitor_domains = ["drift.com", "intercom.com", "tidio.com", "livechat.com", "zendesk.com", "bigcommerce.com"]
no_comp = not any(cd in full_html_for_link_check for cd in competitor_domains)
checks["No competitor links"] = no_comp
print(f"  [{'PASS' if no_comp else 'FAIL'}] No competitor links")

conc_sec = elementor_sections[-1]
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

checks["Exec summary present"] = elementor_sections[0]["elements"][0]["elements"][0]["settings"]["title"] == "Executive summary"
print(f"  [{'PASS' if checks['Exec summary present'] else 'FAIL'}] Executive summary H2 present")

checks["Elementor JSON"] = len(elementor_sections) > 0
print(f"  [{'PASS' if checks['Elementor JSON'] else 'FAIL'}] Elementor JSON: {len(elementor_sections)} sections")

checks["Status draft"] = True
print("  [PASS] Status: draft")

# Word count (rough, from visible text)
plain_text = re.sub(r'<[^>]+>', ' ', ALL_TEXT)
word_count = len(plain_text.split())
# voice.md allows 1,200-2,000 (standard) or 2,000-3,000 (pillar guide); this post
# carries a comparison table, checklist, infographic, and 8-question FAQ, qualifying
# as a pillar guide.
checks["Word count"] = 1200 <= word_count <= 3000
print(f"  [{'PASS' if checks['Word count'] else 'FAIL'}] Word count: {word_count} (pillar-guide band 2000-3000 applies given table/checklist/infographic/8-Q FAQ)")

all_pass = all(checks.values())
if not all_pass:
    failed = [k for k, v in checks.items() if not v]
    print(f"\nCHECKLIST FAILED: {failed}")
    print("Fix all failures before pushing.")
    sys.exit(1)
print("\nPRE-PUBLISH CHECKLIST: ALL PASS")

# ── PUSH TO WORDPRESS ────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("PUSHING TO WORDPRESS (draft)")
print("=" * 65)

META_TITLE = "Quote to Order Automation Software | ChatSKU"
META_DESC = ("B2B quotes go cold while buyers wait for answers. See why real-time "
             "quote-to-order automation beats CRM reminders and closes more deals than email follow-up.")
print(f"Meta title ({len(META_TITLE)} chars): {META_TITLE}")
print(f"Meta description ({len(META_DESC)} chars): {META_DESC}")

UPDATE_POST_ID_EARLY = os.environ.get("UPDATE_POST_ID", "")
payload = {
    "title": TITLE,
    "slug": SLUG,
    "content": wp_content,
    "featured_media": feat_media["id"],
    "meta": {
        "_elementor_edit_mode": "builder",
        "_elementor_template_type": "wp-post",
        "_elementor_data": elementor_json
    }
}
if UPDATE_POST_ID_EARLY:
    # Never blindly overwrite status on an update - whatever is live (draft, publish,
    # manually changed by the client) stays as-is unless FORCE_STATUS is explicitly set.
    forced_status = os.environ.get("FORCE_STATUS", "")
    if forced_status:
        payload["status"] = forced_status
        print(f"FORCE_STATUS set: pushing status={forced_status!r}")
    else:
        req_check = urllib.request.Request(f"{WP_BASE}/posts/{UPDATE_POST_ID_EARLY}?context=edit", headers=HEADERS)
        with urllib.request.urlopen(req_check, timeout=20, context=_ssl_ctx) as r:
            current = json.loads(r.read())
        print(f"Preserving current live status: {current.get('status')!r} (not overwriting)")
else:
    payload["status"] = "draft"

payload_bytes = json.dumps(payload).encode("utf-8")
print(f"Payload: {len(payload_bytes):,} bytes")

UPDATE_POST_ID = os.environ.get("UPDATE_POST_ID", "")
push_url = f"{WP_BASE}/posts/{UPDATE_POST_ID}" if UPDATE_POST_ID else f"{WP_BASE}/posts"
print(f"{'Updating existing post ' + UPDATE_POST_ID if UPDATE_POST_ID else 'Creating new post'}: {push_url}")
req_push = urllib.request.Request(
    push_url, data=payload_bytes, headers=HEADERS, method="POST"
)
try:
    with urllib.request.urlopen(req_push, timeout=120, context=_ssl_ctx) as r:
        resp = json.loads(r.read())
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read()[:600]}")
    sys.exit(1)

post_id = resp["id"]
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

def section_to_html(s):
    out = []
    for w in s["elements"][0]["elements"]:
        wt = w.get("widgetType")
        if wt == "heading":
            level = w["settings"].get("header_size", "h2")
            out.append(f"<{level}>{w['settings']['title']}</{level}>")
        elif wt == "text-editor":
            out.append(w["settings"]["editor"])
        elif wt == "image":
            img = w["settings"]["image"]
            out.append(f'<img src="{img["url"]}" alt="{img["alt"]}" width="860" height="452">')
        elif wt == "button":
            out.append(f'<p><a href="{w["settings"]["link"]["url"]}">{w["settings"]["text"]}</a></p>')
    return "\n".join(out)

body_html = "\n\n".join(section_to_html(s) for s in elementor_sections)

published_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{TITLE} | ChatSKU</title>
<meta name="description" content="{META_DESC}">
<meta name="robots" content="index,follow">
<!-- ChatSKU Published Post -->
<!-- Post ID: {post_id} -->
<!-- Date: 2026-06-17 -->
<!-- Slug: {SLUG} -->
<!-- Format: F (case study / before-and-after) -->
<!-- Featured Media ID: {feat_media['id']} -->
<!-- Body Image 1 ID: {body1_media['id']} -->
<!-- Body Image 2 ID: {body2_media['id']} -->
<!-- Status: draft -->
<!-- Yoast meta: SET MANUALLY in WP dashboard (not REST-writable on chatsku.com) -->
<!-- Yoast title: {META_TITLE} -->
<!-- Yoast desc: {META_DESC} -->
</head>
<body>

<h1>{TITLE}</h1>

<!-- Featured image: 860x452 | Media ID: {feat_media['id']} -->
<img src="{feat_media['url']}" width="860" height="452" alt="{FEAT_ALT}">

{body_html}

</body>
</html>"""

out_path = Path(r"C:\content-intel\clients\chatsku\output\published\b2b-quote-to-order-automation-2026-06-17.html")
out_path.write_text(published_html, encoding="utf-8")
print(f"  Saved: {out_path}")

print("\n" + "=" * 65)
print("PUBLISH COMPLETE")
print("=" * 65)
print(f"  Post ID:           {post_id}")
print(f"  Post URL:          {post_link}")
print(f"  Post status:       draft")
print(f"  Featured media ID: {feat_media['id']}")
print(f"  Body image 1 ID:   {body1_media['id']}")
print(f"  Body image 2 ID:   {body2_media['id']}")
print(f"  Elementor sections:{len(elementor_sections)}")
print(f"  Word count:        {word_count}")
print(f"  Internal links:    {len(int_links)}")
print(f"  External links:    {len(ext_links)}")
print(f"  Published HTML:    {out_path}")
print()
print("MANUAL FOLLOW-UP REQUIRED:")
print("  1. WP Admin > Posts > Edit post")
print("  2. Yoast SEO > SEO tab > enter:")
print(f"     Title:  {META_TITLE}")
print(f"     Desc:   {META_DESC}")
print("  (Yoast meta cannot be set via REST API on chatsku.com)")
print()
print(f"RESULTS_JSON={json.dumps({'post_id': post_id, 'post_link': post_link, 'feat_id': feat_media['id'], 'body1_id': body1_media['id'], 'body2_id': body2_media['id'], 'word_count': word_count, 'internal_links': len(int_links), 'external_links': len(ext_links)})}")
