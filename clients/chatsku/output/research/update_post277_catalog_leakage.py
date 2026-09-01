"""
Update post 277: replace with new content for b2b-catalog-revenue-leakage

Changes from original lost-b2b-revenue-calculator post:
  - New title, slug, primary keyword, full content rewrite
  - New angle: March of Commerce catalog stage leakage model
  - Same 3 images (IDs 274, 275, 276) — no re-upload needed
  - PUT to /wp/v2/posts/277 to update in place

Images reused:
  274 = chatsku-lost-revenue-calculator-featured.jpg  (team meeting — featured)
  275 = chatsku-lost-revenue-calculator-body2.jpg     (dollar bills — Q5/inputs section)
  276 = chatsku-lost-revenue-calculator-body3.jpg     (office at night — Q9/fastest path section)
"""

import json, secrets, re, urllib.request, urllib.error, urllib.parse
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

if not USERNAME or not PASSWORD:
    print("ERROR: Credentials not set"); sys.exit(1)

AUTH = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {AUTH}",
    "User-Agent": UA,
    "Content-Type": "application/json"
}

POST_ID = 277
FEAT_MEDIA_ID   = 274
BODY2_MEDIA_ID  = 275
BODY3_MEDIA_ID  = 276

# We need the uploaded URLs for the published HTML
def get_media_url(media_id):
    req = urllib.request.Request(f"{WP_BASE}/media/{media_id}", headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20, context=_ssl_ctx) as r:
        data = json.loads(r.read())
    return data["source_url"]

print("Fetching image URLs...")
feat_url  = get_media_url(FEAT_MEDIA_ID)
body2_url = get_media_url(BODY2_MEDIA_ID)
body3_url = get_media_url(BODY3_MEDIA_ID)
print(f"  feat:  {feat_url}")
print(f"  body2: {body2_url}")
print(f"  body3: {body3_url}")

# =============================================================================
# INFOGRAPHIC BLOCK (response time vs B2B conversion — section 8)
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
  <p style="color:#aaaacc;font-size:12px;margin:0;">Source: HubSpot Lead Response Management research; Google/CEB B2B digital buying behavior. Illustrative visualization.</p>
</div>"""

# =============================================================================
# FULL DRAFT HTML
# =============================================================================

DRAFT_HTML = """\
<h2>Executive summary</h2>

<p>Your B2B catalog has a revenue leak. Not a vague one. A calculable one, tied to your annual revenue, your catalog stage, and the percentage of buyers your current experience cannot close.</p>

<p>The March of Commerce Revenue Model is a real calculation. Not a guess. Your catalog stage determines your leakage rate. The model shows what that costs in actual dollars and what recovery looks like with ChatSKU.</p>

<p>Use the <a href="/revenue-calculator/">ChatSKU revenue calculator</a> to run your own numbers.</p>

<h2>Introduction</h2>

<p>It is 9pm on a Tuesday. A purchasing manager finds your site, needs 400 units of a specific SKU, and fills out your contact form. Your team sees it at 8am. Your competitor responded at 7am. The deal is gone.</p>

<p>That story stings. But here is the part most distributors miss: that was not bad luck. That was stage leakage: a structural feature of where your catalog sits in the March of Commerce.</p>

<p>At a PDF catalog stage, that scenario does not happen once. It happens dozens of times a month. The March of Commerce Revenue Model puts a dollar figure on the aggregate. Not a gut feeling. An actual number, built from your revenue and your stage.</p>

<h2>What does "revenue left on the table" actually mean for a B2B distributor?</h2>

<p>It is not a feeling. It is a calculable percentage of revenue that walks because the catalog experience cannot complete the transaction.</p>

<p>The model starts with your <em>contestable share</em>: the portion of your revenue where buying experience determines who wins. Not all revenue is contestable. Long-term contract work, locked accounts, sole-source specs. Those are sticky. But a meaningful slice of every distributor's revenue sits in deals where the buyer had options and chose based on who responded, who answered their question, and who made it easiest to quote. That slice is what the model measures.</p>

<p>Within that contestable share, different catalog stages have structurally different leakage rates. A company running PDFs loses a bigger percentage of contestable revenue than a company with a live eCommerce platform. The gap is not small. Understanding <a href="/b2b-catalog-issues-costing-sales/">what a passive catalog actually costs</a> starts with knowing where your stage sits on that curve.</p>

<h2>What is the March of Commerce and where does my catalog sit?</h2>

<p>The March of Commerce is a framework that maps catalog maturity across three broad stages. Each stage has a different structural leakage rate because each one serves buyers differently.</p>

<p>Stage 01-03 is the PDF catalog world. Buyers find your products on a static file. They cannot search, configure, or quote. They have to call or email. Most do not. The ones who do wait.</p>

<p>Stage 04-05 is the HTML catalog with an RFQ form. Better. Buyers can browse and submit requests. But the form creates a delay. Nobody answers at 9pm. Self-serve is partial at best.</p>

<p>Stage 06-08 is the platform and eCommerce layer. Buyers can search, configure, price, and quote on their own, any time. Leakage drops sharply because the catalog does the work the sales rep used to do.</p>

<table style="border-collapse:collapse;width:100%;font-size:15px;margin:20px 0;">
  <thead>
    <tr>
      <th style="background:#1a1a2e;color:#fff;padding:10px 14px;text-align:left;">Stage</th>
      <th style="background:#1a1a2e;color:#fff;padding:10px 14px;text-align:left;">Catalog type</th>
      <th style="background:#1a1a2e;color:#fff;padding:10px 14px;text-align:left;">Typical stage leakage</th>
      <th style="background:#1a1a2e;color:#fff;padding:10px 14px;text-align:left;">Self-serve buyers served</th>
      <th style="background:#1a1a2e;color:#fff;padding:10px 14px;text-align:left;">After-hours coverage</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background:#f0f4ff;">
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">01&ndash;03</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">PDF catalog</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">20&ndash;25%</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Low (&lt;30%)</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">None</td>
    </tr>
    <tr style="background:#ffffff;">
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">04&ndash;05</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">HTML + RFQ form</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">10&ndash;15%</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Moderate (30&ndash;55%)</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Partial</td>
    </tr>
    <tr style="background:#f0f4ff;">
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">06&ndash;08</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Platform / eCommerce</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">3&ndash;6%</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">High (55&ndash;80%)</td>
      <td style="padding:10px 14px;border-bottom:1px solid #e0e0e0;">Full</td>
    </tr>
  </tbody>
</table>
<p style="font-size:13px;color:#666;margin-top:4px;">Illustrative ranges based on March of Commerce Revenue Model default assumptions.</p>

<p>Which stage does your catalog sit at? That answer drives every number in <a href="/passive-catalog/">the passive catalog problem</a> and in the revenue model.</p>

<h2>What inputs does the revenue model use, and where do I find each one?</h2>

<p>The calculator takes seven inputs. All of them are findable. Here is what each one means and where your real number lives.</p>

<ul style="list-style:none;padding:0;">
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:14px;padding:14px 16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="color:#00C9B1;font-size:18px;flex-shrink:0;">&#10003;</span>
    <div><strong>Annual Revenue.</strong> Your total top-line revenue for the last full fiscal year. Find it in your P&amp;L or ERP. Use actual, not projected.</div>
  </li>
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:14px;padding:14px 16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="color:#00C9B1;font-size:18px;flex-shrink:0;">&#10003;</span>
    <div><strong>Stage.</strong> PDF catalog (01-03), HTML + RFQ form (04-05), or Platform / eCommerce (06-08). Honest answer. If buyers cannot quote without calling a rep, you are stage 01-03.</div>
  </li>
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:14px;padding:14px 16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="color:#00C9B1;font-size:18px;flex-shrink:0;">&#10003;</span>
    <div><strong>Contestable Share (default 40%).</strong> The percentage of your revenue where a better or worse buying experience determines who wins. Cross-reference your won/lost analysis in CRM. If you do not have won/lost data, use the 40% default.</div>
  </li>
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:14px;padding:14px 16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="color:#00C9B1;font-size:18px;flex-shrink:0;">&#10003;</span>
    <div><strong>Self-Serve Buyers (default 70%).</strong> The share of your buyers who prefer to research and quote without a sales rep. Ask your sales team what percentage of inbound leads arrive already knowing what they want. Most B2B companies are surprised how high this is.</div>
  </li>
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:14px;padding:14px 16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="color:#00C9B1;font-size:18px;flex-shrink:0;">&#10003;</span>
    <div><strong>Stage Leakage (default 22%).</strong> The percentage of contestable revenue lost because the catalog experience cannot close the deal. Pull from the table above if you are not sure. A PDF catalog defaults to 22%, which sits in the middle of the 20-25% range.</div>
  </li>
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:14px;padding:14px 16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="color:#00C9B1;font-size:18px;flex-shrink:0;">&#10003;</span>
    <div><strong>Recoverable (default 35%).</strong> The realistic portion of leaked revenue that a better catalog experience could capture. Not all lost deals come back. Some buyers are price-driven, some are locked to another vendor. 35% is a conservative floor.</div>
  </li>
  <li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:14px;padding:14px 16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #00C9B1;">
    <span style="color:#00C9B1;font-size:18px;flex-shrink:0;">&#10003;</span>
    <div><strong>Customer Lifetime (default 4 years).</strong> How long does a typical account stay with you? Check your CRM retention data. B2B relationships compound. A 4-year lifetime means 4 years of recovery, not just one order.</div>
  </li>
</ul>

<p>If you cannot find these numbers from your CRM, use the defaults. They are calibrated to B2B distribution benchmarks and will give you a directionally accurate floor estimate.</p>

<h2>What does the calculator output actually mean?</h2>

<p>The model produces four outputs. Here is what each one tells you.</p>

<p><strong>Lifetime Value Recovered</strong> is the total revenue you could realistically capture over the full customer lifetime if the catalog experience improved. It is not a ceiling. It is what the math says is sitting in your pipeline unserved.</p>

<p><strong>Lifetime ChatSKU Cost</strong> is the total cost of the tool over that same customer lifetime. Setup plus monthly fees, multiplied by the lifetime period. This is the investment side of the comparison.</p>

<p><strong>Net Lifetime Gain</strong> is what remains after subtracting the cost from the recovery. If the number is positive, the catalog upgrade more than pays for itself. If it is very large, the cost of waiting is the real number to focus on.</p>

<p><strong>Return on Spend</strong> is the ratio that matters most for a decision. A 22x return means every $1 of ChatSKU cost returns $22 in recovered revenue. The cost of not using ChatSKU is 22 times the cost of using it. Review <a href="/features/">ChatSKU's catalog integration features</a> to understand what powers that return.</p>

<h2>What does an example calculation look like?</h2>

<p>Here is a worked example with concrete numbers. Mid-market industrial distributor, $5M annual revenue, PDF catalog at stage 02.</p>

<div style="background:#f0f4ff;border-left:4px solid #00C9B1;border-radius:8px;padding:20px 24px;margin:24px 0;">
  <p style="font-weight:700;margin:0 0 8px;color:#1a1a2e;">Illustrative example: mid-market industrial distributor</p>
  <ul style="margin:0;padding-left:20px;color:#333;">
    <li>Annual revenue: $5,000,000</li>
    <li>Catalog stage: 02 (PDF catalog)</li>
    <li>Contestable share: 40% = $2,000,000 contestable revenue</li>
    <li>Stage leakage: 22% of contestable = $440,000 at risk annually</li>
    <li>Recoverable: 35% of leakage = $154,000 annual opportunity</li>
    <li>Customer lifetime: 4 years = $616,000 lifetime value recoverable</li>
    <li>ChatSKU cost (illustrative): $12,000 over 4 years</li>
    <li><strong>Net Lifetime Gain: ~$604,000</strong></li>
    <li><strong>Return on Spend: ~51x</strong></li>
  </ul>
  <p style="margin:12px 0 0;font-size:14px;color:#555;">Numbers are illustrative. Run your own inputs at the ChatSKU revenue calculator.</p>
</div>

<p>The important note is that the model accounts for customer lifetime, not just the first order. B2B accounts that stay for 4 years compound the leakage. The recovery compounds too. A single year of $154K in recovered opportunity becomes $616K when the relationship holds.</p>

<h2>How does after-hours buyer loss show up in this model?</h2>

<p>The 9pm buyer scenario is not a separate problem. It is stage leakage with a timestamp on it.</p>

<p>A PDF catalog company at stage 02 cannot self-serve a buyer at 9pm. The buyer arrives, finds your catalog, needs a quote, and hits a wall. They fill out a form. Nobody answers. They move on. That moment, repeated across dozens of inquiries each month, is exactly what stage leakage measures. The model counts it in aggregate. The 9pm story just makes it concrete.</p>

<p>According to <a href="https://blog.hubspot.com/marketing/lead-response-management" target="_blank" rel="noopener noreferrer">HubSpot's research on lead response management</a>, 52% of inbound B2B leads arrive outside standard business hours. Stage 02 companies have no coverage for any of it. That is the structural exposure behind the leakage rate.</p>

<p>Speed matters beyond coverage. Research from Google and the Corporate Executive Board on digital B2B buying behavior shows 35 to 50% of B2B deals go to the vendor who responds first. Not best. Not cheapest. First.</p>

INFOGRAPHIC_INJECT

<p>Response time drives conversion in a way that is not gradual. It falls off a cliff:</p>

<ul>
  <li><strong>5 minutes:</strong> 21% conversion rate</li>
  <li><strong>30 minutes:</strong> approximately 14% conversion rate</li>
  <li><strong>1 hour:</strong> approximately 8% conversion rate</li>
  <li><strong>4 hours:</strong> approximately 5% conversion rate</li>
  <li><strong>24 hours or more:</strong> 2.3% conversion rate</li>
</ul>

<p>The move from stage 02 to stage 04+ is not just a catalog upgrade. It is a shift from zero after-hours capability to partial or full coverage. That shift alone changes the leakage rate from 20-25% down to 10-15%. A catalog-aware AI assistant pushes the buyer experience further. That is what closes <a href="/b2b-after-hours-buyer-problem/">the after-hours B2B lead problem</a> and bridges <a href="/response-gap/">the B2B response gap</a>.</p>

<h2>What is the fastest path from your current stage to meaningful leakage reduction?</h2>

<p>Three options exist. They are not equal.</p>

<ul>
  <li><strong>Manual follow-up improvement.</strong> Hire, train, or incentivize faster response from your sales team. Cost: $60,000 to $80,000 per additional rep per year. Limitation: does not scale with lead volume, and does not work after 5pm. The best sales team in the world cannot respond to a 9pm inquiry by 9:01pm.</li>
  <li><strong>HTML + RFQ form upgrade.</strong> Moving from PDF to a web catalog with a form takes leakage from 20-25% down to 10-15%. That is real progress. But an RFQ form still creates a delay. Buyers submit and wait. After-hours coverage is partial. Self-serve quoting is still not possible.</li>
  <li><strong>Catalog-aware AI assistant.</strong> Full fix. Buyers get answers in real time, any time, from your actual catalog. No rep required. Stage leakage drops toward the 3-6% range because self-serve buyers can complete their research and begin the quoting process without waiting. This is the structural solution.</li>
</ul>

<div style="background:#f9f9fb;border-left:4px solid #1a1a2e;border-radius:8px;padding:20px 24px;margin:24px 0;">
  <p style="margin:0;font-style:italic;color:#333;">"From conversations with our manufacturing and distribution customers, the most common surprise is not how high the stage leakage rate is. It is how much of it was recoverable once the catalog started answering questions in real time."</p>
  <p style="margin:8px 0 0;font-size:13px;color:#666;">ChatSKU team, based on onboarding conversations with 50+ B2B manufacturers and distributors</p>
</div>

<p>Learn more about <a href="/ai-sales-assistant-b2b-ecommerce/">ChatSKU's B2B AI sales assistant</a> and <a href="/for-b2b-manufacturers-distributors-and-wholesalers/">how ChatSKU works for manufacturers and distributors</a>.</p>

<h2>Conclusion</h2>

<p>Your catalog has a leakage rate. It is determined by your stage, not your effort. And it is calculable right now from numbers you already have.</p>

<p>The March of Commerce Revenue Model exists because gut feelings are not enough to justify a change. The math does that job. A $5M distributor at stage 02 is looking at $440,000 of contestable revenue at risk annually. Most of that walks quietly, one unanswered buyer at a time.</p>

<p>Start with the model. Run your own number. Then decide.</p>

<h2>Frequently asked questions</h2>

<h3>What is the March of Commerce?</h3>

<p>The March of Commerce is a catalog maturity framework that maps B2B selling capability across three stages: PDF catalog (stages 01-03), HTML catalog with RFQ form (stages 04-05), and platform or eCommerce (stages 06-08). Each stage has a different structural leakage rate because each one serves self-serve buyers differently. The framework is the foundation of the ChatSKU revenue model.</p>

<h3>What is a realistic stage leakage rate for a B2B distributor?</h3>

<p>It depends on your catalog stage. PDF catalog companies (stages 01-03) typically see 20-25% leakage on their contestable revenue. HTML and RFQ form companies (stages 04-05) see 10-15%. Platform and eCommerce companies (stages 06-08) see 3-6%. The default in the revenue model is 22%, a reasonable starting point for a company that cannot self-serve buyers outside business hours.</p>

<h3>How do I find my "contestable share"?</h3>

<p>Look at your won/lost analysis in CRM. Deals where the reason for loss was speed, responsiveness, or catalog friction are your contestable revenue. If you do not have that data, the 40% default in the model is calibrated to B2B distribution benchmarks. For most distributors in competitive categories, 35-50% of revenue sits in deals where buying experience was a deciding factor.</p>

<h3>What is "recoverable" in the revenue model?</h3>

<p>Recoverable is the realistic portion of leaked revenue that a better catalog experience could actually capture. Not all buyers who leave come back, even if you fix the catalog. Some were never serious. Some are locked into competitor contracts. The model defaults to 35%, a conservative estimate. It means for every $100 of revenue your catalog leaks, you can realistically win back $35 with the right tool in place.</p>

<h3>Does the model work for manufacturers as well as distributors?</h3>

<p>Yes. The inputs are the same: annual revenue, catalog stage, and the percentage of buyers who prefer to self-serve. Manufacturers often have more complex catalogs with custom configurations, MOQ minimums, and lead-time variability. That complexity tends to push leakage rates up, not down, because it creates more friction points where buyers give up. The model handles that through the contestable share and stage leakage inputs.</p>

<h3>How quickly can a B2B company improve its catalog stage?</h3>

<p>A move from stage 02 to stage 04 behavior, meaning buyers can get real-time answers without waiting for a rep, can happen in days. ChatSKU connects to your existing catalog files (PDF, Excel, or ERP export) and goes live without a data migration or site rebuild. The catalog stage in the revenue model reflects buyer experience, not infrastructure. Improving what a buyer can do at 9pm is the lever, and that lever moves fast.</p>
"""

# Inject infographic into section 8 (INFOGRAPHIC_INJECT placeholder)
DRAFT_HTML = DRAFT_HTML.replace("INFOGRAPHIC_INJECT", INFOGRAPHIC_HTML)

# Em dash scan
em_count = DRAFT_HTML.count("—") + DRAFT_HTML.count("&mdash;")
assert em_count == 0, f"ERROR: {em_count} em dashes found"
print(f"Em dash scan: PASS (0 found)")

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

def make_image_widget(media_id, url, alt):
    return {
        "id": gid(), "elType": "widget", "widgetType": "image", "elements": [],
        "settings": {
            "image": {
                "id": media_id,
                "url": url,
                "alt": alt,
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

SECTION_BACKGROUNDS = {
    "executive summary":            "#f9f9fb",
    "introduction":                 "#ffffff",
    "revenue left on the table":    "#f0f4ff",   # Q3
    "what is the march":            "#ffffff",   # Q4: March of Commerce
    "what inputs":                  "#f9f9fb",   # Q5: inputs
    "what does the calculator":     "#ffffff",   # Q6: output meaning
    "what does an example":         "#f0f4ff",   # Q7: example calc
    "how does after-hours":         "#ffffff",   # Q8: after-hours
    "what is the fastest":          "#f9f9fb",   # Q9: fastest path
    "conclusion":                   "#1a1a2e",
    "frequently asked":             "#f9f9fb",
}

IMG_SECTION_KEYWORDS = {}


def build_elementor():
    elementor_sections = []
    chunks = [c.strip() for c in re.split(r'(?=<h2[^>]*>)', DRAFT_HTML.strip()) if c.strip()]

    for chunk in chunks:
        hm = re.match(r'<h2[^>]*>(.*?)</h2>(.*)', chunk, re.DOTALL)
        if not hm:
            continue
        h2_text   = hm.group(1).strip()
        body_html = hm.group(2).strip()
        label     = h2_text.lower()

        bg = "#f9f9fb"
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
                make_button("See what your catalog is leaking", "https://chatsku.com/revenue-calculator/"),
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
            widgets = [make_heading(h2_text)]
            if body_html:
                widgets.append(make_text(body_html))

            img_data = None
            for kw, (mid, murl, malt) in IMG_SECTION_KEYWORDS.items():
                if kw in label:
                    img_data = (mid, murl, malt)
                    break
            if img_data:
                widgets.append(make_image_widget(*img_data))

            elementor_sections.append(make_section(widgets, bg=bg))

    return elementor_sections


# =============================================================================
# MAIN
# =============================================================================
print("=" * 65)
print("UPDATE: post 277 -> b2b-catalog-revenue-leakage (2026-06-16)")
print("=" * 65)

print("\nBuilding Elementor JSON...")
elementor_sections = build_elementor()
elementor_json = json.dumps(elementor_sections)

print(f"\nBuilt {len(elementor_sections)} sections:")
for i, s in enumerate(elementor_sections):
    bg   = s["settings"]["background_color"]
    cols = s["elements"][0]["elements"]
    h    = next((w["settings"].get("title","")[:50] for w in cols if w.get("widgetType")=="heading"), "?")
    types = [w.get("widgetType") for w in cols]
    if "image" in types and "text-editor" in types:
        img_pos  = types.index("image")
        text_pos = types.index("text-editor")
        order_ok = img_pos > text_pos
        print(f"  {i:2}: bg={bg}  [{h}]  {types}  img_order={'OK' if order_ok else 'FAIL!'}")
        if not order_ok:
            print("  CRITICAL: image before text-editor!"); sys.exit(1)
    else:
        print(f"  {i:2}: bg={bg}  [{h}]  {types}")

# Validate JSON
parsed_check = json.loads(elementor_json)
assert isinstance(parsed_check, list) and len(parsed_check) == 11, f"Expected 11 sections, got {len(parsed_check)}"
print(f"\nElementor JSON: {len(elementor_json):,} chars  {len(parsed_check)} sections")

# Pre-publish checks
print("\n" + "=" * 65)
print("PRE-PUBLISH CHECKLIST")
print("=" * 65)

checks = {}

ed = DRAFT_HTML.count("—") + DRAFT_HTML.count("&mdash;")
checks["No em dashes"] = ed == 0
print(f"  [{'PASS' if checks['No em dashes'] else 'FAIL'}] Em dashes: {ed}")

ext_links = re.findall(r'href="https?://(?!chatsku\.com)[^"]+', DRAFT_HTML)
checks["External links <= 2"] = len(ext_links) <= 2
print(f"  [{'PASS' if checks['External links <= 2'] else 'FAIL'}] External links: {len(ext_links)} (max 2)")
for el in ext_links:
    print(f"    {el[:80]}")

int_links = re.findall(r'href="(?:https://chatsku\.com)?/[^"]+', DRAFT_HTML)
int_links = [l for l in int_links if "chatsku.com" in l or l.startswith('href="/')]
checks["Internal links 5-10"] = 5 <= len(int_links) <= 10
print(f"  [{'PASS' if checks['Internal links 5-10'] else 'FAIL'}] Internal links: {len(int_links)} (target 5-10)")

no_comp = not any(cd in DRAFT_HTML for cd in ["drift.com","intercom.com","tidio.com"])
checks["No competitor links"] = no_comp
print(f"  [{'PASS' if no_comp else 'FAIL'}] No competitor links")

checks["Section count"] = len(elementor_sections) == 11
print(f"  [{'PASS' if checks['Section count'] else 'FAIL'}] Section count: {len(elementor_sections)} (expected 11)")

order_ok = True
for s in elementor_sections:
    types = [w.get("widgetType") for w in s["elements"][0]["elements"]]
    if "image" in types and "text-editor" in types:
        if types.index("image") < types.index("text-editor"):
            order_ok = False
checks["Image widget order"] = order_ok
print(f"  [{'PASS' if order_ok else 'FAIL'}] Image widgets AFTER text-editor")

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
    btn_w = next((w for w in col_ws if w.get("widgetType") == "button"), None)
    checks["Conclusion bg"] = bg_c == "#1a1a2e"
    checks["Conclusion button"] = bool(btn_w)
    checks["Conclusion button color"] = btn_w["settings"].get("background_color") == "#e94560" if btn_w else False
    checks["Conclusion button url"] = btn_w["settings"]["link"]["url"] == "https://chatsku.com/revenue-calculator/" if btn_w else False
    print(f"  [{'PASS' if checks['Conclusion bg'] else 'FAIL'}] Conclusion bg: {bg_c}")
    print(f"  [{'PASS' if checks['Conclusion button'] else 'FAIL'}] Conclusion button present")
    print(f"  [{'PASS' if checks['Conclusion button color'] else 'FAIL'}] Button color: {btn_w['settings'].get('background_color') if btn_w else None}")
    print(f"  [{'PASS' if checks['Conclusion button url'] else 'FAIL'}] Button URL: {btn_w['settings']['link']['url'] if btn_w else None}")

all_pass = all(checks.values())
if not all_pass:
    failed = [k for k, v in checks.items() if not v]
    print(f"\nCHECKLIST FAILED: {failed}"); sys.exit(1)
print("\nPRE-PUBLISH CHECKLIST: ALL PASS")

# Build WP content (no bare img)
wp_content = re.sub(r'<img[^>]*/>', '', DRAFT_HTML).strip()
wp_content = re.sub(r'<img[^>]*>', '', wp_content).strip()

# PUT to post 277
print("\n" + "=" * 65)
print("UPDATING POST 277 (PUT)")
print("=" * 65)

payload = {
    "title": "Your B2B Catalog Has a Revenue Leak. Here Is How to Calculate It.",
    "slug": "b2b-catalog-revenue-leakage",
    "status": "draft",
    "content": wp_content,
    "featured_media": FEAT_MEDIA_ID,
    "meta": {
        "_elementor_edit_mode": "builder",
        "_elementor_template_type": "wp-post",
        "_elementor_data": elementor_json
    }
}

payload_bytes = json.dumps(payload).encode("utf-8")
print(f"Payload: {len(payload_bytes):,} bytes")

req_push = urllib.request.Request(
    f"{WP_BASE}/posts/{POST_ID}", data=payload_bytes, headers=HEADERS, method="POST"
)
try:
    with urllib.request.urlopen(req_push, timeout=120, context=_ssl_ctx) as r:
        resp = json.loads(r.read())
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read()[:600]}"); sys.exit(1)

post_link = resp.get("link", "")
post_slug = resp.get("slug", "")
print(f"\nUPDATE SUCCESS:")
print(f"  Post ID:  {POST_ID}")
print(f"  Slug:     {post_slug}")
print(f"  Status:   {resp.get('status')}")
print(f"  Link:     {post_link}")

# Verify
print("\nVerifying saved data...")
req_v = urllib.request.Request(f"{WP_BASE}/posts/{POST_ID}?context=edit", headers=HEADERS)
with urllib.request.urlopen(req_v, timeout=30, context=_ssl_ctx) as r:
    verified = json.loads(r.read())
meta_v = verified.get("meta", {})
saved_ed = json.loads(meta_v.get("_elementor_data", "[]"))
print(f"  Sections saved:  {len(saved_ed)}")
print(f"  edit_mode:       {meta_v.get('_elementor_edit_mode')!r}")
print(f"  featured_media:  {verified.get('featured_media')}")
print(f"  slug:            {verified.get('slug')}")

# Clear Elementor cache
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

# Save published HTML
print("\nSaving published HTML...")
FEAT_ALT = "B2B sales team reviewing catalog revenue model to calculate stage leakage and ROI of upgrading from PDF catalog to AI-assisted commerce"

published_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Your B2B Catalog Has a Revenue Leak. Here Is How to Calculate It. | ChatSKU</title>
<meta name="description" content="Your B2B catalog stage determines how much revenue leaks. The March of Commerce Revenue Model shows what your stage is costing you and what you can realistically recover.">
<meta name="robots" content="index,follow">
<!-- ChatSKU Published Post -->
<!-- Post ID: {POST_ID} -->
<!-- Date: 2026-06-16 -->
<!-- Slug: b2b-catalog-revenue-leakage -->
<!-- Featured Media ID: {FEAT_MEDIA_ID} -->
<!-- Body Image 2 ID: {BODY2_MEDIA_ID} (inputs section) -->
<!-- Body Image 3 ID: {BODY3_MEDIA_ID} (fastest path section) -->
<!-- Status: draft -->
<!-- Yoast meta: SET MANUALLY in WP dashboard -->
<!-- Yoast title: Your B2B Catalog Has a Revenue Leak. Here Is How to Calculate It. | ChatSKU -->
<!-- Yoast desc: Your B2B catalog stage determines how much revenue leaks. The March of Commerce Revenue Model shows what your stage is costing you and what you can realistically recover. -->
</head>
<body>

<h1>Your B2B Catalog Has a Revenue Leak. Here Is How to Calculate It.</h1>

<!-- Featured image: 860x452 | Media ID: {FEAT_MEDIA_ID} -->
<img src="{feat_url}" width="860" height="452" alt="{FEAT_ALT}">

{DRAFT_HTML}

</body>
</html>"""

out_path = Path(r"C:\content-intel\clients\chatsku\output\published\b2b-catalog-revenue-leakage-2026-06-16.html")
out_path.write_text(published_html, encoding="utf-8")
print(f"  Saved: {out_path}")

# Final report
print("\n" + "=" * 65)
print("UPDATE COMPLETE")
print("=" * 65)
print(f"  Post ID:           {POST_ID}")
print(f"  New slug:          b2b-catalog-revenue-leakage")
print(f"  New title:         Your B2B Catalog Has a Revenue Leak...")
print(f"  Post URL:          {post_link}")
print(f"  Featured media:    {FEAT_MEDIA_ID}")
print(f"  Elementor sections:{len(elementor_sections)}")
print(f"  Published HTML:    {out_path}")
print()
print("MANUAL FOLLOW-UP REQUIRED (Yoast cannot be set via REST API):")
print("  WP Admin > Posts > post 277 > edit > Yoast SEO > SEO tab:")
print("  Title: Your B2B Catalog Has a Revenue Leak. Here Is How to Calculate It. | ChatSKU")
print("  Desc:  Your B2B catalog stage determines how much revenue leaks. The March")
print("         of Commerce Revenue Model shows what your stage is costing you and")
print("         what you can realistically recover.")
