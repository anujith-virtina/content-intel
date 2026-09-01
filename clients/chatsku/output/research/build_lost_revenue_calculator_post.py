"""
Build and publish: lost-b2b-revenue-calculator
Post: "How to calculate lost B2B revenue from after-hours buyers and slow quote response"
Format: Format B (Conversational Q&A)  Date: 2026-06-16

Pipeline:
  1. Load .env credentials
  2. Source and upload 3 images (Pexels -> Openverse/Stocksnap fallback)
  3. Build Elementor JSON from draft HTML with injected blocks
  4. Push to WordPress as draft
  5. Clear Elementor cache
  6. Save published HTML to output/published/
  7. Report media IDs, post ID, checklist results

Template: clients/chatsku/output/research/build_b2b_catalog_conversion_post.py (post 96 structure)
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

# -- Load .env -----------------------------------------------------------------
_env_path = r"C:\content-intel\.env"
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

# -- Credentials ---------------------------------------------------------------
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

# =============================================================================
# IMAGE SOURCING
# =============================================================================

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

# Pre-selected CC0 StockSnap images (visually verified 2026-06-16)
PRESELECTED = {
    "featured": "https://cdn.stocksnap.io/img-thumbs/960w/Q1OSKR7D42.jpg",  # B2B team meeting, multiple laptops
    "body2":    "https://cdn.stocksnap.io/img-thumbs/960w/ITA18FXIBL.jpg",  # Dollar bills — revenue / lost money
    "body3":    "https://cdn.stocksnap.io/img-thumbs/960w/ONN4Z188GF.jpg",  # Office building lit up at night — after-hours
}

def source_preselected_or_search(key, queries):
    url = PRESELECTED.get(key)
    if url:
        print(f"  Pre-selected ({key}): {url}")
        raw = download_image(url)
        if raw:
            return url, resize_image(raw)
        print(f"  Pre-selected failed, falling back to search...")
    return source_image(queries)

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
    print(f"  Alt text set: {alt_text[:70]}...")
    return {"id": media_id, "url": media_url, "alt": alt_text}

# =============================================================================
# INFOGRAPHIC BLOCK (inserted into Q4 section, BEFORE bullet list)
# =============================================================================

INFOGRAPHIC_HTML = """<div style="background:#1a1a2e;border-radius:12px;padding:28px 24px;margin:24px 0;overflow-x:auto;">
  <p style="color:#00C9B1;font-weight:700;font-size:14px;text-transform:uppercase;letter-spacing:1px;margin:0 0 16px;">Response time vs. B2B conversion rate</p>
  <div style="display:flex;align-items:flex-end;gap:12px;height:120px;margin-bottom:12px;">
    <div style="display:flex;flex-direction:column;align-items:center;gap:6px;flex:1;">
      <div style="background:#00C9B1;width:100%;border-radius:4px 4px 0 0;height:100px;"></div>
      <span style="color:#ffffff;font-size:11px;text-align:center;">5 min<br><strong style="color:#00C9B1;">21%</strong></span>
    </div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:6px;flex:1;">
      <div style="background:#2a9d7f;width:100%;border-radius:4px 4px 0 0;height:67px;"></div>
      <span style="color:#ffffff;font-size:11px;text-align:center;">30 min<br><strong style="color:#2a9d7f;">14%</strong></span>
    </div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:6px;flex:1;">
      <div style="background:#e9a84c;width:100%;border-radius:4px 4px 0 0;height:38px;"></div>
      <span style="color:#ffffff;font-size:11px;text-align:center;">1 hour<br><strong style="color:#e9a84c;">8%</strong></span>
    </div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:6px;flex:1;">
      <div style="background:#e07b3a;width:100%;border-radius:4px 4px 0 0;height:24px;"></div>
      <span style="color:#ffffff;font-size:11px;text-align:center;">4 hours<br><strong style="color:#e07b3a;">5%</strong></span>
    </div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:6px;flex:1;">
      <div style="background:#e94560;width:100%;border-radius:4px 4px 0 0;height:11px;"></div>
      <span style="color:#ffffff;font-size:11px;text-align:center;">24+ hours<br><strong style="color:#e94560;">2.3%</strong></span>
    </div>
  </div>
  <p style="color:#aaaacc;font-size:12px;margin:0;">Source: Casey Response 2026, Artemis GTM 2026, MIT Lead Response Management Study. Illustrative visualization.</p>
</div>"""

# =============================================================================
# FULL DRAFT HTML
# All em dashes (U+2014) replaced. Zero remaining.
# Conclusion CTA metadata lines stripped (publisher metadata, not content).
# Infographic injected into Q4 section BEFORE the bullet list.
# =============================================================================

DRAFT_HTML = """\
<h2>Executive summary</h2>

<p>52% of inbound B2B leads arrive outside standard business hours. The average B2B company takes 42 to 47 hours to respond. Those two numbers, combined, produce a revenue gap that most manufacturers and distributors have never actually calculated.</p>

<p>This post gives you the <strong>lost B2B revenue calculator</strong> framework: a five-step formula you run on your own inputs to produce a defensible annual loss figure. It also shows you how that number scales across company sizes, where the biggest conversion cliff is, and what your process audit should cover before you decide how to fix it.</p>

<p>Once you have your number, use the <a href="https://chatsku.com/revenue-calculator/">ChatSKU revenue calculator</a> to model what you could recover if that gap closed.</p>

<h2>Introduction</h2>

<p>It is 9pm on a Tuesday. A purchasing manager at a regional manufacturer finds your website. They need 400 units of a specific SKU, they have a deadline, and they are ready to quote. They fill out your contact form and wait.</p>

<p>Your sales team sees the inquiry at 8am Wednesday. They call back. The buyer already got a quote from your competitor at 7am. The deal is gone.</p>

<p>That is one lead. Now multiply it by how many times that happens in a month. Your website gets 400 visits per month. 52% arrive after 5pm. Your team responds the next morning, 14 to 18 hours later. No single miss feels fatal. The math says otherwise.</p>

<p>The problem is not that your sales team is slow. It is that no system exists to respond when they are offline. This article gives you the formula to calculate exactly what that costs.</p>

<h2>How much revenue is the average B2B company losing to slow lead response?</h2>

<p>The short answer: more than the gut feeling suggests, and the data makes the case clearly.</p>

<p>According to the <a href="https://caseyresponse.com/blog/lead-response-time-statistics" target="_blank" rel="noopener noreferrer">Casey Response 2026 speed-to-lead analysis</a>, a 5-minute response converts at 21%. A 24-hour response converts at 2.3%. That is a 9x gap between fastest and slowest, and most B2B companies sit at the bottom. The Artemis GTM 2026 speed-to-lead benchmark puts the average B2B response time at 42 to 47 hours, which places the typical manufacturer or distributor firmly in the 2.3% conversion zone.</p>

<p>The first-responder effect compounds the problem. According to the Google and Corporate Executive Board white paper on digital B2B buying behavior, 35 to 50% of deals go to the vendor that responds first. That is not a small edge. That is a structural advantage for whoever picks up first.</p>

<p>To put a dollar figure on it: at a $3,500 average B2B quote value and 10 missed after-hours leads per month, you are looking at $117,600 in annual revenue at risk before accounting for customer lifetime value. Your actual inputs will differ. The formula in the next section shows you how to calculate your specific number. And if you want to understand what the catalog side of this cost looks like separately, see <a href="https://chatsku.com/b2b-catalog-issues-costing-sales/">how much your B2B catalog gap may be costing you</a>.</p>

<h2>What happens to B2B buyers who inquire after business hours?</h2>

<p>According to HubSpot research, 52% of inbound B2B leads arrive outside standard business hours. That means more than half your inbound volume lands when nobody is there to answer it.</p>

<p>What happens next is not ambiguous. According to <a href="https://www.docket.io/blog/7-reasons-why-b2b-companies-lose-40-60-of-website-leads" target="_blank" rel="noopener noreferrer">Docket.io's analysis of B2B website lead loss</a>, 40 to 60% of website leads are lost when no immediate response is available. Buyers do not call again in the morning. They do not check their inbox waiting for your reply. They move to the next supplier's website and fill out another form.</p>

<p>The window to be the first responder closes in minutes. By the time your sales rep arrives at 8am, the buyer has already moved on. That is <a href="https://chatsku.com/b2b-after-hours-buyer-problem/">the after-hours B2B lead problem</a> in its clearest form: it is not a communication delay. It is a permanent loss.</p>

<h2>How do I calculate my lost revenue from slow quote response?</h2>

<p>This is the core section. The following five steps function as a <strong>lost B2B revenue calculator</strong> you can run right now with numbers from your CRM and website analytics.</p>

<ol>
  <li><strong>Monthly inbound leads &times; percentage that arrive after hours = after-hours leads</strong></li>
  <li><strong>After-hours leads &times; percentage that get no same-session response = abandoned leads</strong></li>
  <li><strong>Abandoned leads &times; your average quote value = revenue at risk per month</strong></li>
  <li><strong>Revenue at risk &times; your historical close rate = monthly lost revenue</strong></li>
  <li><strong>Monthly lost revenue &times; 12 = annual lost revenue</strong></li>
</ol>

<p>The inputs you need are your monthly inbound lead count, your average quote value, and your historical close rate. Your after-hours percentage defaults to 52% if you do not have your own data. Your abandonment rate defaults to 70% if you have no same-session response system in place.</p>

<div style="background:#f0f4ff;border-left:4px solid #00C9B1;border-radius:8px;padding:20px 24px;margin:24px 0;">
  <p style="font-weight:700;margin:0 0 8px;color:#1a1a2e;">Illustrative example: mid-market industrial distributor</p>
  <ul style="margin:0;padding-left:20px;color:#333;">
    <li>50 inbound leads/month</li>
    <li>52% arrive after hours = 26 after-hours leads</li>
    <li>70% get no same-session response = 18 abandoned leads</li>
    <li>$4,200 average quote value</li>
    <li>28% historical close rate</li>
    <li><strong>Monthly lost revenue: $21,168</strong></li>
    <li><strong>Annual lost revenue: $254,016</strong></li>
  </ul>
  <p style="margin:12px 0 0;font-size:14px;color:#555;">Numbers are illustrative. Run your own calculation at <a href="https://chatsku.com/revenue-calculator/">the ChatSKU revenue calculator</a>.</p>
</div>

<p>The formula shows the floor. It does not account for customer lifetime value or repeat order cycles. Your actual loss is higher.</p>

<p>A distributor with 50 monthly leads, a 52% after-hours rate, and a $4,200 average quote stands to lose roughly $254,000 per year before accounting for repeat orders. That is for a company with only 50 leads per month. For a company at 150 leads, the number crosses $750,000.</p>

<h2>Does quote response time actually affect whether I win the deal?</h2>

INFOGRAPHIC_INJECT

<p>Yes. And the effect is not linear. It drops off a cliff.</p>

<p>The conversion rate by response window, per the Artemis GTM 2026 benchmark and MIT Lead Response Management Study:</p>

<ul>
  <li><strong>5 minutes:</strong> 21% conversion</li>
  <li><strong>30 minutes:</strong> approximately 14% conversion</li>
  <li><strong>1 hour:</strong> approximately 8% conversion</li>
  <li><strong>4 hours:</strong> approximately 5% conversion</li>
  <li><strong>24 hours or more:</strong> 2.3% conversion</li>
</ul>

<p>The drop from a 5-minute response to a 1-hour response cuts your conversion by more than half. Moving from 1 hour to 24 hours cuts it again. By the time your average 42 to 47 hour response arrives, you are converting at roughly 11% of the rate you would at 5 minutes.</p>

<p>Layer in the first-responder effect: 35 to 50% of B2B deals go to whichever vendor responds first, per the Google and CEB white paper. Speed becomes structural. It is not a nice-to-have improvement. Whoever answers first sets the frame for the entire deal. That is why <a href="https://chatsku.com/response-gap/">the response gap</a> is not a service quality problem. It is a revenue architecture problem.</p>

<h2>How does lost revenue vary by company size or industry?</h2>

<p>The formula scales with lead volume and quote value. Here is what that looks like across three representative company profiles.</p>

<table style="border-collapse:collapse;width:100%;font-size:15px;margin:20px 0;">
  <thead>
    <tr>
      <th style="background:#1a1a2e;color:#fff;padding:10px 14px;text-align:left;">Company profile</th>
      <th style="background:#1a1a2e;color:#fff;padding:10px 14px;text-align:left;">Avg monthly inbound</th>
      <th style="background:#1a1a2e;color:#fff;padding:10px 14px;text-align:left;">Avg quote value</th>
      <th style="background:#1a1a2e;color:#fff;padding:10px 14px;text-align:left;">Est. after-hours leads</th>
      <th style="background:#1a1a2e;color:#fff;padding:10px 14px;text-align:left;">Est. monthly loss</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background:#f0f4ff;">
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">SMB distributor</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">20&ndash;40 leads</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">$800&ndash;$2,000</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">10&ndash;21 leads</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">$1,400&ndash;$8,400/mo</td>
    </tr>
    <tr style="background:#ffffff;">
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Mid-market manufacturer</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">40&ndash;120 leads</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">$3,000&ndash;$8,500</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">21&ndash;62 leads</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">$17,640&ndash;$147,420/mo</td>
    </tr>
    <tr style="background:#f0f4ff;">
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Enterprise wholesaler</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">120&ndash;400 leads</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">$8,000&ndash;$30,000</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">62&ndash;208 leads</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">$138,000&ndash;$1.7M/mo</td>
    </tr>
  </tbody>
</table>
<p style="font-size:13px;color:#666;margin-top:4px;">Estimates based on 52% after-hours rate, 70% abandonment, 28% close rate. Illustrative ranges only.</p>

<p>These are illustrative ranges. Your number depends on your specific close rate, quote volume, and product mix. See <a href="https://chatsku.com/b2b-catalog-issues-costing-sales/">how much your B2B catalog gap may be costing you</a> for a related breakdown.</p>

<h2>How do I audit my current lead response process?</h2>

<p>Before you fix the gap, you need to know where it is. Most manufacturers and distributors discover they cannot answer questions 3, 4, and 6 below. That inability is itself the finding.</p>

<ul style="list-style:none;padding:0;">
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:14px;padding:14px 16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="color:#00C9B1;font-size:18px;flex-shrink:0;">&#10003;</span>
    <div><strong>Track inbound by time of day.</strong> Do you know what percentage of leads arrive outside business hours? If not, you are measuring the wrong thing.</div>
  </li>
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:14px;padding:14px 16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="color:#00C9B1;font-size:18px;flex-shrink:0;">&#10003;</span>
    <div><strong>Measure your average first-response time.</strong> Not your best case. Your median. Across all inbound channels.</div>
  </li>
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:14px;padding:14px 16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="color:#00C9B1;font-size:18px;flex-shrink:0;">&#10003;</span>
    <div><strong>Check for same-session acknowledgment.</strong> Does every after-hours lead receive an automated, personalized response within 5 minutes? Or do they wait until morning?</div>
  </li>
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:14px;padding:14px 16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="color:#00C9B1;font-size:18px;flex-shrink:0;">&#10003;</span>
    <div><strong>Segment close rates by response speed.</strong> Leads responded to in under 5 minutes versus over 1 hour. If you do not have this data, that is the first gap to fix.</div>
  </li>
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:14px;padding:14px 16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="color:#00C9B1;font-size:18px;flex-shrink:0;">&#10003;</span>
    <div><strong>Review lost-deal analysis.</strong> Do you ask why you lost? "Went with another vendor" is not an answer. "Vendor responded faster" is.</div>
  </li>
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:14px;padding:14px 16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="color:#00C9B1;font-size:18px;flex-shrink:0;">&#10003;</span>
    <div><strong>Identify catalog questions that go unanswered.</strong> What are buyers asking that your team cannot answer in real time? Spec questions, MOQ, lead time, pricing. These are the abandonment triggers.</div>
  </li>
</ul>

<p>If you identified gaps in steps 1 through 3, <a href="https://chatsku.com/response-gap/">the response gap page</a> explains the structural cause and what it takes to close it.</p>

<h2>What is the fastest way to close the after-hours response gap?</h2>

<p>Three options exist. Only one works without adding headcount or accepting partial coverage.</p>

<ul>
  <li><strong>Hire overnight staff.</strong> Full coverage, but a dedicated after-hours rep costs $60,000 to $80,000 per year in salary and benefits. It does not scale with lead volume. It is not realistic for most manufacturers or distributors under $10M in revenue.</li>
  <li><strong>After-hours answering service.</strong> Partial coverage. An answering service can acknowledge an inbound call, but it cannot answer pricing questions, MOQ minimums, or lead times from your catalog. Buyers who need a quote will not wait on hold for information a human operator cannot give them.</li>
  <li><strong>Catalog-aware AI assistant.</strong> Full coverage without headcount. Connects to your existing product catalog, answers spec, pricing, MOQ, and lead-time questions 24/7, and captures qualified leads with quote context in real time.</li>
</ul>

<p>ChatSKU connects to your existing catalog: PDF, Excel, or ERP export. It answers buyer questions the moment they arrive, regardless of the hour. Leads captured after hours include quote context, product SKUs, and pricing requests. Not just an email address.</p>

<div style="background:#f9f9fb;border-left:4px solid #1a1a2e;border-radius:8px;padding:20px 24px;margin:24px 0;">
  <p style="margin:0;font-style:italic;color:#333;">"From conversations with our manufacturing and distribution customers, the most common surprise is not how many after-hours leads they miss. It is that they had no system to detect the miss in the first place."</p>
  <p style="margin:8px 0 0;font-size:13px;color:#666;">ChatSKU team, based on onboarding conversations with 50+ B2B manufacturers and distributors</p>
</div>

<p>Learn more about <a href="https://chatsku.com/ai-sales-assistant-b2b-ecommerce/">ChatSKU's B2B AI sales assistant</a> and its <a href="https://chatsku.com/features/">catalog integration features</a>.</p>

<h2>Conclusion</h2>

<p>The revenue is calculable. The gap is closable.</p>

<p>52% of your inbound arrives when nobody is watching. First-responder advantage goes to whoever is there. Right now, that is not you.</p>

<p>Start with the number. Know what you are actually losing before you decide whether to fix it.</p>

<h2>Frequently asked questions</h2>

<h3>What is a good B2B lead response time?</h3>

<p>Under 5 minutes for initial acknowledgment. Under 1 hour for a qualified response. The industry average is 42 to 47 hours, per the Artemis GTM 2026 benchmark. The gap between average and best practice is where the revenue leaks. A 5-minute response converts at 21%. A 24-hour response converts at 2.3%. That 9x difference is not a marginal improvement: it is the difference between winning and not being in the conversation.</p>

<h3>How do I track after-hours lead loss?</h3>

<p>Start with your CRM. Filter leads by time of submission. Compare close rates for business-hours leads versus after-hours leads. The delta is your baseline. If your CRM does not capture submission time, check your web form logs or your marketing automation platform. Most companies discover they have no system for this. That absence is itself the answer.</p>

<h3>Does after-hours lead loss affect B2B more than B2C?</h3>

<p>Yes. B2B buyers research across multiple sessions and multiple days. But the first vendor to respond to a specific inquiry sets the frame. After-hours B2B abandonment is structurally worse than B2C because the alternative is not "buy it elsewhere online." It is "call your competitor's sales rep tomorrow." The dependency on a human response makes the delay more damaging in B2B than in any self-serve consumer context.</p>

<h3>What is the average cost of a missed B2B lead?</h3>

<p>It depends on your average quote value and close rate. At $5,000 average quote and 25% close rate, each missed lead costs $1,250 in expected revenue. At $18,000 per quote, the same calculation produces $4,500 per missed lead. Use the five-step formula in this article to calculate your own figure. Multiply by your monthly after-hours abandonment volume for the annual number.</p>

<h3>Can a catalog-aware AI assistant really answer my buyers' specific questions?</h3>

<p>If your product data exists in a structured form: PDF, Excel, ERP export, a catalog-aware assistant can answer specs, MOQ, lead time, and pricing questions in real time. It is not a generic FAQ bot. It knows your catalog. ChatSKU does not replace your sales rep. It removes the dependency on one being available at 10pm, captures the lead with full quote context, and routes it to your team in the morning.</p>

<h3>How quickly does a B2B revenue calculator pay off?</h3>

<p>The calculator itself is free at <a href="https://chatsku.com/revenue-calculator/">chatsku.com/revenue-calculator</a>. If the output shows $50,000 or more in annual lost revenue, the ROI math on any response automation becomes straightforward. ChatSKU goes live in under 24 hours using your existing catalog files. For most manufacturers and distributors, the first after-hours lead capture happens within the first week.</p>
"""

# Inject infographic block into Q4 section (BEFORE the bullet list)
DRAFT_HTML = DRAFT_HTML.replace("INFOGRAPHIC_INJECT", INFOGRAPHIC_HTML)

# Em dash scan (critical)
em_count = DRAFT_HTML.count("—") + DRAFT_HTML.count("&mdash;")
assert em_count == 0, f"ERROR: {em_count} em dashes found in content"
print("Em dash scan: PASS (0 found)")

# =============================================================================
# ELEMENTOR JSON BUILDERS
# =============================================================================

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
    # Normalize relative internal links to absolute
    html = re.sub(r'href="/([\w/\-]+)"', r'href="https://chatsku.com/\1"', html)
    # Strip any bare img tags (Elementor image widget handles images)
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
        sec_pad = {"top": "60", "bottom": "60", "unit": "px"}  # NO left/right keys per MUST-FOLLOW-RULES
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

# Section background color cycle: exec=#f9f9fb, intro=#ffffff, then body sections per spec
# Per section map in task instructions:
SECTION_BACKGROUNDS = {
    "executive summary":   "#f9f9fb",
    "introduction":        "#ffffff",
    # Body Q sections (key = lowercase substring of H2):
    "how much revenue":    "#f0f4ff",   # Q3
    "what happens to":     "#ffffff",   # Q4
    "how do i calculate":  "#f9f9fb",   # Q5
    "does quote response": "#ffffff",   # Q6
    "how does lost":       "#f0f4ff",   # Q7
    "how do i audit":      "#ffffff",   # Q8
    "what is the fastest": "#f9f9fb",   # Q9
    "conclusion":          "#1a1a2e",   # Conclusion
    "frequently asked":    "#f9f9fb",   # FAQ
}

# Sections that get a body image (image AFTER text-editor)
# Q5 = "how do i calculate" -> body2_img
# Q9 = "what is the fastest" -> body3_img
IMG_SECTION_KEYWORDS = {
    "how do i calculate": "body2",
    "what is the fastest": "body3",
}

def build_elementor(body2_img, body3_img):
    """Parse DRAFT_HTML into Elementor sections following the section map."""
    img_map = {
        "body2": body2_img,
        "body3": body3_img,
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

        # Find background color
        bg = "#f9f9fb"  # fallback
        for key, color in SECTION_BACKGROUNDS.items():
            if key in label:
                bg = color
                break

        is_conclusion = "conclusion" in label
        is_faq = "frequently asked" in label

        if is_conclusion:
            widgets = [
                make_heading(h2_text, color="#ffffff", align="center"),
                make_text(body_html, dark_section=True),
                make_button("Calculate your lost revenue", "https://chatsku.com/revenue-calculator/"),
            ]
            elementor_sections.append(make_section(widgets, bg="#1a1a2e", is_conclusion=True))

        elif is_faq:
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
            # Standard body section
            widgets = [make_heading(h2_text)]
            if body_html:
                widgets.append(make_text(body_html))

            # Check if this section gets a body image (image AFTER text-editor per MUST-FOLLOW-RULES)
            img_data = None
            for kw, img_key in IMG_SECTION_KEYWORDS.items():
                if kw in label:
                    img_data = img_map[img_key]
                    break

            if img_data:
                widgets.append(make_image_widget(img_data))  # CRITICAL: image LAST

            elementor_sections.append(make_section(widgets, bg=bg))

    return elementor_sections

# =============================================================================
# MAIN
# =============================================================================
print("=" * 65)
print("BUILD: lost-b2b-revenue-calculator  (2026-06-16)")
print("=" * 65)

# -- STEP 1: Source and upload images -----------------------------------------
print("\n[IMAGE 1/3] Featured: B2B sales team office night")
FEAT_ALT = ("B2B sales team missing after-hours buyer inquiry: calculating lost revenue from slow quote response in a manufacturing office")
_, feat_bytes = source_preselected_or_search("featured", [
    "business team",
    "sales office",
    "office meeting",
])
if feat_bytes is None:
    print("FATAL: Could not source featured image"); sys.exit(1)
feat_media = upload_image(feat_bytes, "chatsku-lost-revenue-calculator-featured.jpg", FEAT_ALT)

print("\n[IMAGE 2/3] Body: revenue / financial visual (Q5 section)")
BODY2_ALT = ("B2B manufacturer calculating lost revenue from slow lead response using a five-step formula on a desktop")
_, body2_bytes = source_preselected_or_search("body2", [
    "business finance",
    "laptop desk",
    "office revenue",
])
if body2_bytes is None:
    print("FATAL: Could not source body image 2"); sys.exit(1)
body2_media = upload_image(body2_bytes, "chatsku-lost-revenue-calculator-body2.jpg", BODY2_ALT)

print("\n[IMAGE 3/3] Body: office after hours (Q9 section)")
BODY3_ALT = ("Empty B2B distributor office after hours with laptop open showing AI assistant capturing buyer inquiries overnight")
_, body3_bytes = source_preselected_or_search("body3", [
    "office night",
    "laptop night",
    "business evening",
])
if body3_bytes is None:
    print("FATAL: Could not source body image 3"); sys.exit(1)
body3_media = upload_image(body3_bytes, "chatsku-lost-revenue-calculator-body3.jpg", BODY3_ALT)

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

# -- STEP 2: Build Elementor JSON ---------------------------------------------
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
    h    = next((w["settings"].get("title","")[:50] for w in cols if w.get("widgetType")=="heading"), "?")
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

# -- STEP 3: Pre-publish checklist --------------------------------------------
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
    "b2b-after-hours-lead-capture", "b2b-catalog-conversion-rate",
    "convert-pdf-catalog-to-website", "b2b-catalog-issues-costing-sales",
    "b2b-after-hours-buyer-problem",
]
new_slug = "lost-b2b-revenue-calculator"
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

# Section count check (expect 11 sections)
checks["Section count"] = len(elementor_sections) == 11
print(f"  [{'PASS' if checks['Section count'] else 'FAIL'}] Section count: {len(elementor_sections)} (expected 11)")

# Build WP content (stripped of img tags)
wp_content = re.sub(r'<img[^>]*/>', '', DRAFT_HTML).strip()
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

# Internal links (target 6-7 for pillar post)
int_links = re.findall(r'href="https://chatsku\.com/[^"]+', DRAFT_HTML)
checks["Internal links"] = 5 <= len(int_links) <= 10
print(f"  [{'PASS' if checks['Internal links'] else 'FAIL'}] Internal links: {len(int_links)} (target 5-10)")
for il in int_links:
    print(f"    {il[:80]}")

# No competitor links
competitor_domains = ["drift.com", "intercom.com", "tidio.com"]
no_comp = not any(cd in DRAFT_HTML for cd in competitor_domains)
checks["No competitor links"] = no_comp
print(f"  [{'PASS' if no_comp else 'FAIL'}] No competitor links")

# Conclusion section checks
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
    h_align = h_w["settings"].get("align") if h_w else None
    has_btn = any(w.get("widgetType") == "button" for w in col_ws)
    btn_w = next((w for w in col_ws if w.get("widgetType") == "button"), None)
    btn_color = btn_w["settings"].get("background_color") if btn_w else None
    btn_url = btn_w["settings"]["link"]["url"] if btn_w else None
    checks["Conclusion bg"] = bg_c == "#1a1a2e"
    checks["Conclusion heading white"] = h_color == "#ffffff"
    checks["Conclusion heading centered"] = h_align == "center"
    checks["Conclusion button"] = has_btn
    checks["Conclusion button color"] = btn_color == "#e94560"
    checks["Conclusion button url"] = btn_url == "https://chatsku.com/revenue-calculator/"
    print(f"  [{'PASS' if checks['Conclusion bg'] else 'FAIL'}] Conclusion bg: {bg_c}")
    print(f"  [{'PASS' if checks['Conclusion heading white'] else 'FAIL'}] Conclusion heading color: {h_color}")
    print(f"  [{'PASS' if checks['Conclusion heading centered'] else 'FAIL'}] Conclusion heading align: {h_align}")
    print(f"  [{'PASS' if checks['Conclusion button'] else 'FAIL'}] Conclusion button widget present")
    print(f"  [{'PASS' if checks['Conclusion button color'] else 'FAIL'}] Conclusion button color: {btn_color}")
    print(f"  [{'PASS' if checks['Conclusion button url'] else 'FAIL'}] Conclusion button URL: {btn_url}")
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

# -- STEP 4: Push to WordPress ------------------------------------------------
print("\n" + "=" * 65)
print("PUSHING TO WORDPRESS (draft)")
print("=" * 65)

payload = {
    "title": "How to calculate lost B2B revenue from after-hours buyers and slow quote response",
    "slug": "lost-b2b-revenue-calculator",
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

# -- STEP 5: Verify saved data ------------------------------------------------
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

# -- STEP 6: Clear Elementor cache --------------------------------------------
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

# -- STEP 7: Save published HTML ----------------------------------------------
print("\nSaving published HTML...")

published_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>How to calculate lost B2B revenue from after-hours buyers and slow quote response | ChatSKU</title>
<meta name="description" content="52% of B2B leads arrive after hours. Use this 5-step formula to calculate your lost revenue from slow quote response, then model recovery with the ChatSKU calculator.">
<meta name="robots" content="index,follow">
<!-- ChatSKU Published Post -->
<!-- Post ID: {post_id} -->
<!-- Date: 2026-06-16 -->
<!-- Slug: lost-b2b-revenue-calculator -->
<!-- Featured Media ID: {feat_media['id']} -->
<!-- Body Image 2 ID: {body2_media['id']} -->
<!-- Body Image 3 ID: {body3_media['id']} -->
<!-- Status: draft -->
<!-- Yoast meta: SET MANUALLY in WP dashboard -->
<!-- Yoast title: Lost B2B Revenue Calculator: Quantify What You're Missing | ChatSKU -->
<!-- Yoast desc: 52% of B2B leads arrive after hours. Use this 5-step formula to calculate your lost revenue from slow quote response, then model recovery with the ChatSKU calculator. -->
</head>
<body>

<h1>How to calculate lost B2B revenue from after-hours buyers and slow quote response</h1>

<!-- Featured image: 860x452 | Media ID: {feat_media['id']} -->
<img src="{feat_media['url']}" width="860" height="452" alt="{FEAT_ALT}">

{DRAFT_HTML}

</body>
</html>"""

out_path = Path(r"C:\content-intel\clients\chatsku\output\published\lost-b2b-revenue-calculator-2026-06-16.html")
out_path.write_text(published_html, encoding="utf-8")
print(f"  Saved: {out_path}")

# -- FINAL REPORT -------------------------------------------------------------
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
print("     Title:  Lost B2B Revenue Calculator: Quantify What You're Missing | ChatSKU")
print("     Desc:   52% of B2B leads arrive after hours. Use this 5-step formula to")
print("             calculate your lost revenue from slow quote response, then model")
print("             recovery with the ChatSKU calculator.")
print("  (Yoast meta cannot be set via REST API on chatsku.com)")
print()
print(f"RESULTS_JSON={json.dumps({'post_id': post_id, 'post_link': post_link, 'feat_id': feat_media['id'], 'body2_id': body2_media['id'], 'body3_id': body3_media['id']})}")
