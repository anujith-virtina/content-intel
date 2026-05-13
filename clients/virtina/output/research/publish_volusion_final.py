"""
Final publisher script for Volusion to WooCommerce migration post.
Uses pre-selected Openverse image IDs. Resizes, uploads to WP, builds HTML, pushes post.
"""

import sys
import json
import base64
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO

# ── Credentials ───────────────────────────────────────────────────────────────
env_path = Path(r"C:\content-intel\.env")
env_vars = {}
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env_vars[k.strip()] = v.strip()

WP_USERNAME = env_vars["WP_USERNAME"]
WP_APP_PASSWORD = env_vars["WP_APP_PASSWORD"]

WP_BASE = "https://virtina.com/wp-json/wp/v2"
auth_str = base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()).decode()
WP_HEADERS = {
    "Authorization": f"Basic {auth_str}",
    "Content-Type": "application/json",
}

WORK_DIR = Path(r"C:\content-intel\clients\virtina\output\research")

# ── Selected image IDs (Openverse StockSnap, CC0) ────────────────────────────
IMAGES = [
    {
        "key": "featured",
        "openverse_id": "7f0cd475-ee7f-48c5-add5-7c688f3820ca",
        "width": 1309,
        "height": 500,
        "filename": "volusion-woocommerce-migration-featured-1309x500.jpg",
        "alt": "Volusion merchant reviewing WooCommerce migration plan on laptop, preparing to switch eCommerce platforms for their growing online store",
        "title": "Volusion to WooCommerce migration planning",
    },
    {
        "key": "section1",
        "openverse_id": "3a5371c2-949c-492d-9a8e-caf5ce4dfc21",
        "width": 670,
        "height": 352,
        "filename": "volusion-woocommerce-migration-section1-670x352.jpg",
        "alt": "Online store owner frustrated by unexpected Volusion plan upgrade fees and platform billing changes affecting their eCommerce business",
        "title": "Frustrated store owner on Volusion billing",
    },
    {
        "key": "section2",
        "openverse_id": "8f40cddf-7969-4a8b-967e-b9bebfbac3af",
        "width": 670,
        "height": 352,
        "filename": "volusion-woocommerce-migration-section2-670x352.jpg",
        "alt": "eCommerce developer planning Volusion to WooCommerce migration steps including 301 redirects and product data import mapping",
        "title": "Migration planning and checklist",
    },
    {
        "key": "section3",
        "openverse_id": "fe9c0e44-93d6-49b2-b7e5-dfb02871104f",
        "width": 670,
        "height": 352,
        "filename": "volusion-woocommerce-migration-section3-670x352.jpg",
        "alt": "Small business owner reviewing improved WooCommerce store analytics after successful migration from Volusion eCommerce platform",
        "title": "WooCommerce store success after migration",
    },
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def fetch_openverse_thumb(openverse_id):
    """Fetch image via Openverse thumbnail proxy."""
    url = f"https://api.openverse.org/v1/images/{openverse_id}/thumb/"
    print(f"  Fetching: {url}")
    r = requests.get(url, headers={"User-Agent": "VirtinaContentPublisher/1.0"}, timeout=30)
    r.raise_for_status()
    return r.content


def crop_resize(img_bytes, target_w, target_h, quality=82):
    """Scale-to-cover then center-crop. JPEG quality 82."""
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    new_w = int(src_w * scale)
    new_h = int(src_h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    img = img.crop((left, top, left + target_w, top + target_h))
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    return buf.getvalue()


def upload_to_wp(img_bytes, filename, alt_text, title):
    """Upload image bytes to WP media library. Returns (media_id, source_url)."""
    upload_headers = {
        "Authorization": f"Basic {auth_str}",
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "image/jpeg",
    }
    r = requests.post(f"{WP_BASE}/media", headers=upload_headers, data=img_bytes, timeout=60)
    if not r.ok:
        print(f"  Upload error {r.status_code}: {r.text[:200]}")
        r.raise_for_status()
    media = r.json()
    media_id = media["id"]
    media_url = media["source_url"]
    print(f"  Uploaded media ID={media_id}, URL={media_url}")
    # Set alt text and title
    upd = requests.post(
        f"{WP_BASE}/media/{media_id}",
        headers=WP_HEADERS,
        json={"alt_text": alt_text, "title": title},
        timeout=30,
    )
    upd.raise_for_status()
    return media_id, media_url


# ── Image pipeline ────────────────────────────────────────────────────────────
print("=== Downloading and processing images ===")
media_ids = {}
media_urls = {}

for spec in IMAGES:
    print(f"\n[{spec['key']}] {spec['width']}x{spec['height']}")
    raw = fetch_openverse_thumb(spec["openverse_id"])
    print(f"  Downloaded {len(raw)//1024}KB")
    resized = crop_resize(raw, spec["width"], spec["height"])
    size_kb = len(resized) / 1024
    print(f"  Resized to {spec['width']}x{spec['height']}, {size_kb:.1f}KB")
    if size_kb > 200:
        resized = crop_resize(raw, spec["width"], spec["height"], quality=70)
        print(f"  Re-encoded at q70: {len(resized)//1024}KB")
    local_path = WORK_DIR / spec["filename"]
    with open(local_path, "wb") as f:
        f.write(resized)
    print(f"  Saved: {local_path}")
    mid, murl = upload_to_wp(resized, spec["filename"], spec["alt"], spec["title"])
    media_ids[spec["key"]] = mid
    media_urls[spec["key"]] = murl

print("\n=== Media IDs ===")
for k in ["featured", "section1", "section2", "section3"]:
    print(f"  {k}: {media_ids[k]} -> {media_urls[k]}")

# ── Build post HTML ───────────────────────────────────────────────────────────
def img_tag(media_id, media_url, alt_text):
    return (
        f'<span style="display:block;margin:20px 0;">'
        f'<img alt="{alt_text}" data-id="{media_id}" '
        f'width="670" data-init-width="670" height="352" data-init-height="352" '
        f'title="" loading="lazy" src="{media_url}" '
        f'data-width="670" data-height="352" '
        f'style="aspect-ratio: auto 670 / 352;max-width:100%;">'
        f'</span>'
    )

s1 = img_tag(
    media_ids["section1"], media_urls["section1"],
    "Online store owner frustrated by unexpected Volusion plan upgrade fees and platform billing changes affecting their eCommerce business",
)
s2 = img_tag(
    media_ids["section2"], media_urls["section2"],
    "eCommerce developer planning Volusion to WooCommerce migration steps including 301 redirects and product data import mapping",
)
s3 = img_tag(
    media_ids["section3"], media_urls["section3"],
    "Small business owner reviewing improved WooCommerce store analytics after successful migration from Volusion eCommerce platform",
)

FAQ_STYLE = """<style>
details.vfaq>summary{list-style:none;}
details.vfaq>summary::-webkit-details-marker{display:none;}
details.vfaq[open]>summary{background:linear-gradient(#00d5c0,#00d5c0)!important;}
details.vfaq .vfaq-answer p{font-size:15px!important;color:#6e6e6e!important;line-height:1.75!important;}
</style>"""

content = f"""<div style="background:linear-gradient(rgba(0,213,192,0.28),rgba(0,213,192,0.28));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 dir="ltr" style="color:#43627f;font-size:30px;">Summary</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">You opened a billing notification one morning and your Volusion plan had upgraded itself overnight. No email. No warning. The price jumped from $35 to $79 a month because your store crossed an annual sales cap you didn't know existed. That moment, more than any feature comparison, is why Volusion merchants eventually leave. This article walks through what's actually happening on Volusion, what the migration to WooCommerce genuinely involves, and what you get on the other side, including the parts that are harder than the marketing makes them sound.</p>
</div>

<div style="background:linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 style="color:#43627f;font-size:30px;">Introduction</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">The billing surprise is not a bug. Volusion's Personal plan caps annual sales at $50,000. The Professional plan caps at $100,000. The Business plan at $500,000. Cross any of those thresholds and the account upgrades automatically. Merchants have reported charges jumping 600% in a matter of weeks without any notification. Some have had revenue held during disputes. The pricing structure is not designed to grow with you. It is designed to extract more from you as you grow.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">If you're reading this, you probably already know something is off. You've hit a wall, or several. Maybe it's the billing. Maybe it's an integration that should exist and doesn't. Maybe it's the gnawing question that started in 2020 when Volusion filed for Chapter 11 bankruptcy protection: should my business be built on this? The decision to migrate is not a crisis. It's a recognition. This piece is written for the moment after that recognition, when you want someone to be straight with you about what moving to WooCommerce actually takes.</p>
</div>

<h3>Table of Contents</h3>
<ul style="list-style:none!important;padding-left:0!important;margin:0 0 1.5em 0!important;">
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#walls" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">The walls you keep hitting on Volusion</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#decision" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">When the frustration becomes a decision</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#migration" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">What the migration actually looks like</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#what-you-gain" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">What WooCommerce gives you that Volusion cannot</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#people-also-ask" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">People also ask</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#conclusion" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">Conclusion</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#faq" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">Frequently asked questions</a></li>
</ul>

<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="walls" style="color:#43627f;font-size:30px;">The walls you keep hitting on Volusion</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">The sales cap structure is the one that gets merchants first, but it's rarely the only problem. You're paying a monthly fee on the assumption that it's your monthly fee. Then you cross $50,000 in annual sales and Volusion upgrades you to the Professional plan at $79 a month, with no warning email. Cross $100,000 and you're looking at the Business tier at $299. On top of plan fees, bandwidth overages run $7 per gigabyte, billed separately. The plan price was never the real price. Merchants who found out the hard way have described charges that "just kept skyrocketing" and billing jumps that hit without any prior notification or consent. To understand <a href="https://virtina.com/platforms/woocommerce-development-services/" style="outline: none;">what WooCommerce offers as a platform</a> compared to Volusion, you first need to see the full picture of what Volusion is costing you.</p>

{s1}

<p dir="ltr" style="font-size:16px;line-height:1.75;">The integration ceiling is a different kind of frustration. Volusion's app marketplace holds roughly 80 apps. One developer reviewing the platform on Capterra described the API as something no agency wants to build on, because the proprietary structure makes custom work prohibitively difficult. When you need a tool that Volusion doesn't natively support and you can't get a developer to build it, you're stuck. That's not a minor inconvenience for a growing store. It's a ceiling.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">The SEO picture is also harder than it looks from inside the platform. Volusion has no native blogging capability, which cuts off content-driven organic acquisition entirely. URL canonicalization issues create confusion for crawlers. Schema markup support is limited. These are structural constraints that affect rankings in ways that can be difficult to diagnose until you've left and seen what's possible on a platform with full schema control. For any store relying on organic search for acquisition, this isn't a cosmetic problem.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">For B2B merchants, Volusion has no native tiered pricing, no customer roles, and no quote workflows. Wholesale operations that need customer-specific pricing or a simple quote request process have no path forward inside Volusion's product. The <a href="https://virtina.com/b2b-ecommerce-development/" style="outline: none;">WooCommerce B2B development</a> story is a separate conversation, but the contrast with Volusion starts here. These aren't feature gaps that might close in a future update. They are architectural limitations of a platform that filed for Chapter 11 bankruptcy in June 2020 and has operated under restructured ownership since. <a href="https://storeleads.app/reports/volusion" target="_blank" rel="noopener noreferrer">StoreLeads' 2026 tracking data</a> puts Volusion at 3,526 active stores, down from 13,889 in Q1 2020. That is a 75% contraction in six years, with the platform losing 40 stores for every 2 it gains in recent tracking windows.</p>
</div>

<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="decision" style="color:#43627f;font-size:30px;">When the frustration becomes a decision</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">The decision to migrate rarely arrives as a sudden realization. It accumulates. One support ticket goes unanswered. One integration turns out not to exist. One billing surprise hits at a bad time. Then one day a competitor who migrated to WooCommerce six months ago is outranking you, running automations you can't replicate, and selling wholesale at customer-specific prices you can't offer. That's when it tips.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">For many merchants, the 2020 bankruptcy was a quiet turning point. Volusion entered Chapter 11 protection in June 2020. The company continued operating and eventually emerged from bankruptcy, but the question it raised doesn't fully go away: do you want your business to depend on this platform? Some merchants left immediately. Others stayed and are still running fine. But "I stayed because leaving seemed hard" is a different calculation than "I stayed because the platform is working for me." If you're reading this, you probably know which category you're in.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">The 2019 data breach is a second data point in the same direction. Credit card data from 239,000 customers across 6,589 Volusion stores was <a href="https://steva.co/volusion-review/" target="_blank" rel="noopener noreferrer">compromised in a single breach, with estimated damages of $133.89 million</a>. The breach was not disclosed publicly for months. As a merchant, you were liable for your customers' experience on your store, but the vulnerability was not in your control. Full data ownership, where your database lives on your host and no third party controls access, is one of the things WooCommerce gives you. On Volusion, your data lives on Volusion's servers.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">The decision to migrate is not a verdict on the years you spent on Volusion. The platform was workable for a generation of small eCommerce stores. The question now is whether it's the right fit for where your business is going. If you've already mapped out what that looks like, understanding your <a href="https://virtina.com/ecommerce-replatform/" style="outline: none;">eCommerce replatforming options</a> will save you from the most common missteps before you touch a single file.</p>
</div>

<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="migration" style="color:#43627f;font-size:30px;">What the migration actually looks like</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">This is the section most migration guides skip past. Here's what actually happens, including the parts that are harder than you'd expect.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">It starts with an export. Go to Admin, then Data Management, then Export. Products, customers, orders. Volusion produces CSV files. The data is there. The problem is that the field names differ between Volusion and WooCommerce, variant structures don't map one-to-one, and any custom fields you've built in Volusion have no automatic equivalent. Plan 1-3 days for this phase, and document every live URL on your Volusion store. That URL list becomes your redirect map. If you don't create it now, you'll be rebuilding it from memory later, which is worse.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">WooCommerce is self-hosted. That means you're now choosing and managing your own server. A managed WordPress host like WP Engine, Kinsta, or Cloudways takes most of the infrastructure burden off you, but the choice matters. Don't treat this as a commodity decision. WooCommerce performance lives and dies on the hosting environment. Get this wrong and you'll spend months debugging slowness that is actually a server configuration problem.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Migrate the data in a test run first. Tools like LitExtension and Cart2Cart run automated product and customer transfers starting around $69 for basic catalogs. Run the test on a subset of your products. Check variant mapping. Check prices. Check that customer records carry over. Fix what's off before you run the full migration. Products create the most friction in this phase. Customer records and order history typically move more cleanly.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Here is what does not migrate and requires manual rebuild:</p>
<ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;">
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Store design.</strong> Zero carries over. Your Volusion theme does not translate to WordPress. Treat this as a redesign from scratch. If your old theme was constraining you, this is the moment to fix it.</span></li>
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Payment gateways.</strong> Stripe, PayPal, Square, and most major processors have official WooCommerce extensions. But you're setting them up from new API keys. If you were using Volusion Payments, you'll also need to re-establish merchant processing.</span></li>
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Tax rules and shipping zones.</strong> Both must be rebuilt inside WooCommerce. Volusion and WooCommerce handle these configurations differently enough that there is no shortcut.</span></li>
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>SEO plugin and meta fields.</strong> WooCommerce has no native meta field management. Install Yoast or RankMath before anything goes live. Your SEO data migrates as raw fields but requires an SEO plugin to render correctly.</span></li>
</ul>
<p dir="ltr" style="font-size:16px;line-height:1.75;">The 301 redirect mapping is the highest-risk step in the migration, and it's the one most commonly deprioritized. Volusion URLs follow one structure. WooCommerce URLs follow a different one. Every URL that existed on your Volusion store and changes in the move is treated by Google as a brand new page unless it has a redirect pointing to the equivalent WooCommerce URL. Missing redirects don't just mean a temporary traffic dip. They mean you're starting from zero on pages that took years to rank. Map every page before DNS cutover. Implement the redirects before anything goes live. Check Google Search Console for crawl errors 4-6 weeks post-launch. Understanding <a href="https://virtina.com/woocommerce-hpos-migration/" style="outline: none;">WooCommerce order storage migration</a> is also worth attention during this phase, particularly for stores with large order histories.</p>

{s2}

<p dir="ltr" style="font-size:16px;line-height:1.75;">The honest part: WooCommerce is not simpler than Volusion. It's more powerful and more flexible, but those things come with more responsibility. Plugin selection has no guardrails. The 60,000-plugin library means choosing wrong is easy, and <a href="https://virtina.com/woocommerce-issues-killing-conversions/" style="outline: none;">WooCommerce plugin conflicts</a> are a real operational headache. You are now responsible for hosting management, plugin updates, security patching, and performance tuning. None of those were your job on Volusion. For most stores, a <a href="https://virtina.com/woocommerce-developer-for-ecommerce-success/" style="outline: none;">WooCommerce developer</a> is not optional for the redirect implementation, theme build, and integration configuration phases. For small stores with simple catalogs and no custom integrations, the data transfer piece is doable with automated tools. Everything else benefits from professional judgment.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Timeline: small-to-mid stores typically take 1-3 weeks. Larger stores with complex catalogs, custom integrations, or significant SEO footprints should budget 4-8 weeks. The data transfer is the fastest part. Design, redirects, and integration rebuilds take most of the time.</p>
</div>

<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="what-you-gain" style="color:#43627f;font-size:30px;">What WooCommerce gives you that Volusion cannot</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">After accepting the complexity costs of self-hosting and plugin management, here is what you actually get. No sales caps. No automatic plan upgrades because you hit a revenue threshold. No bandwidth overage fees at $7 a gigabyte. Your monthly cost is your hosting plan, plus the extensions you choose to run. That's it. The pricing model doesn't work against you as your store grows.</p>

{s3}

<p dir="ltr" style="font-size:16px;line-height:1.75;">The 60,000-plugin library means the integration you needed and couldn't find in Volusion's ~80-app marketplace almost certainly exists. Klaviyo, Mailchimp, QuickBooks, Xero, NetSuite, ShipStation, Stripe, Authorize.net: all have official WooCommerce extensions. The API is open. Developers will build on it. Agencies know it. That changes what's possible for your store's custom requirements. A look at the full range of <a href="https://virtina.com/ecommerce-integration/" style="outline: none;">eCommerce integration capabilities</a> on WooCommerce shows how wide the gap has grown.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Data ownership changes the risk picture. Your database lives on your server. No third party can lock your account, freeze your funds, or shut down your store. For merchants who built contingency plans around what happened to Volusion in 2020, this is a material difference in business continuity, not a philosophical one.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;"><a href="https://virtina.com/woocommerce-seo-made-easy/" style="outline: none;">WooCommerce's SEO capabilities</a> are a step change from what Volusion offers. Clean URL structures. Native blogging via WordPress. Full schema markup through Yoast or RankMath. Page-level meta management. Correct canonicalization. WordPress powers 43% of all websites for a reason: the SEO tooling is mature, well-supported, and built to serve content-driven acquisition strategies. For stores that have been limited by Volusion's SEO ceiling, this is often the most tangible post-migration win.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">For B2B merchants, the contrast is sharpest here. <a href="https://virtina.com/b2b-ecommerce/" style="outline: none;">B2B eCommerce on WooCommerce</a> includes tiered pricing by customer role, wholesale registration workflows, quote request tools, customer-specific catalog visibility, and ERP integration patterns. Plugins like B2BKing, WholesaleX, and Wholesale Suite handle the wholesale layer. None of these exist natively in Volusion. For a distributor or manufacturer trying to run a wholesale channel alongside a retail catalog, Volusion's flat product model is not a minor inconvenience. It's a structural dead end.</p>
</div>

<div style="background:linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="people-also-ask" style="color:#43627f;font-size:30px;">People also ask</h2>
<h3 style="color:#43627f;font-size:23px;">Is Volusion still in business?</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Yes. Volusion filed for Chapter 11 bankruptcy in June 2020 and continued operating under restructured ownership. It emerged from bankruptcy protection and is still active. However, the platform has contracted sharply: from roughly 13,889 active stores at its 2020 peak to 3,526 as of May 2026, a 75% decline over six years. The platform continues to process orders and support merchants, but investment in new features has been limited and third-party agency support has declined significantly.</p>
<h3 style="color:#43627f;font-size:23px;">How long does a Volusion to WooCommerce migration take?</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">For a small to mid-size store with a straightforward catalog and no complex integrations, the migration typically takes 1-3 weeks. Larger stores with custom features, extensive SKU catalogs, or significant SEO footprints should budget 4-8 weeks. The data transfer itself is the faster part. Design rebuild, redirect mapping, and integration reconfiguration take the most time, and rushing any of those three phases creates problems that are much slower to fix after launch.</p>
<h3 style="color:#43627f;font-size:23px;">Will I lose my SEO rankings if I migrate from Volusion to WooCommerce?</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Not if the 301 redirects are implemented correctly before DNS cutover. Every Volusion URL that changes in the migration needs a redirect pointing to its WooCommerce equivalent. If redirects are missing, Google treats the new URLs as new pages and traffic drops. With a complete redirect map in place, most stores recover to pre-migration ranking levels within a few months post-launch. Many see improvement over baseline because WooCommerce's URL structure and schema capabilities are stronger than Volusion's.</p>
<h3 style="color:#43627f;font-size:23px;">How much does migrating from Volusion to WooCommerce cost?</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Automated data transfer tools start around $69 for basic migrations. That covers the data only, not design, redirects, or configuration. A full migration with a new WooCommerce theme, redirect mapping, plugin selection, payment gateway setup, and testing requires developer time. The total cost scales with store size, catalog complexity, and the amount of custom work the WooCommerce build needs. For stores coming off the Volusion Professional or Business plan, the ongoing savings from eliminating plan fees and bandwidth overages often offset the migration investment within the first year.</p>
</div>

<div style="background:#00d5c0;border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="conclusion" style="color:#ffffff;font-size:30px;">Conclusion</h2>
<p style="color:#ffffff;font-size:16px;line-height:1.75;">This isn't about WooCommerce being a perfect platform. It isn't. You'll manage your own hosting, make your own plugin choices, and carry more operational responsibility than you did on Volusion. Those are real costs. The question is whether you're trading a managed simplicity that has stopped working for you, for a complexity you can actually control. If your store is at $30,000 in annual sales with no integration ambitions and no B2B requirements, Volusion may still work. But if you've hit the sales caps, if you've run into the integration dead ends, if you've watched a competitor on WooCommerce pull ahead on SEO and customization, then the migration is a project with a defined scope and a defined end date. It's not a catastrophe.</p>
<p style="color:#ffffff;font-size:16px;line-height:1.75;">The merchant is the one who decides. But if you're planning a migration and want a team that has done this before, Virtina's WooCommerce migration team has run this project hundreds of times, on both sides of the Volusion equation. The conversation is worth having before you build the plan.</p>
</div>

{FAQ_STYLE}
<h2 id="faq" style="color:#43627f;font-size:30px;">Frequently asked questions</h2>
<div>
<details class="vfaq" style="background:transparent;margin-top:7px;"><summary style="cursor:pointer;padding:17px;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;background:rgba(245,245,245,0.5);"><span style="font-size:16px;font-weight:600;color:#43627f;line-height:2;flex:1;">Can I keep my Volusion store live while I build the WooCommerce store?</span><svg viewBox="0 0 24 24" width="17" height="17" style="fill:#50565f;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg"><path d="M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12M8,12A2,2 0 0,1 10,10A2,2 0 0,1 12,12A2,2 0 0,1 10,14A2,2 0 0,1 8,12M0,12A2,2 0 0,1 2,10A2,2 0 0,1 4,12A2,2 0 0,1 2,14A2,2 0 0,1 0,12Z"/></svg></summary><div class="vfaq-answer" style="padding:30px 22px;background:#fff;"><p dir="ltr" style="font-size:16px;line-height:1.75;">Yes. Build and test the WooCommerce store on a staging URL or temporary domain while your Volusion store stays live and continues processing orders. Only cut over DNS when the WooCommerce store is fully tested, redirect-mapped, and approved. The DNS propagation window is typically a few hours, which is your only real downtime. Keep your Volusion account active for at least 30 days post-launch so you can reference order history and handle customer service issues that reference Volusion order numbers.</p></div></details>
<details class="vfaq" style="background:transparent;margin-top:7px;"><summary style="cursor:pointer;padding:17px;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;background:rgba(245,245,245,0.5);"><span style="font-size:16px;font-weight:600;color:#43627f;line-height:2;flex:1;">What happens to my customer passwords during migration?</span><svg viewBox="0 0 24 24" width="17" height="17" style="fill:#50565f;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg"><path d="M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12M8,12A2,2 0 0,1 10,10A2,2 0 0,1 12,12A2,2 0 0,1 10,14A2,2 0 0,1 8,12M0,12A2,2 0 0,1 2,10A2,2 0 0,1 4,12A2,2 0 0,1 2,14A2,2 0 0,1 0,12Z"/></svg></summary><div class="vfaq-answer" style="padding:30px 22px;background:#fff;"><p dir="ltr" style="font-size:16px;line-height:1.75;">Volusion stores passwords in a proprietary hashed format that cannot be converted to WooCommerce's format. Customer accounts migrate with names, addresses, and order history intact. Passwords do not. After migration, customers receive a password reset prompt on first login. This is expected behavior and not a sign that something went wrong. Tell your customers in advance, ideally via email before the cutover, so the password reset doesn't become a flood of support tickets.</p></div></details>
<details class="vfaq" style="background:transparent;margin-top:7px;"><summary style="cursor:pointer;padding:17px;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;background:rgba(245,245,245,0.5);"><span style="font-size:16px;font-weight:600;color:#43627f;line-height:2;flex:1;">Do I need a developer to migrate from Volusion to WooCommerce?</span><svg viewBox="0 0 24 24" width="17" height="17" style="fill:#50565f;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg"><path d="M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12M8,12A2,2 0 0,1 10,10A2,2 0 0,1 12,12A2,2 0 0,1 10,14A2,2 0 0,1 8,12M0,12A2,2 0 0,1 2,10A2,2 0 0,1 4,12A2,2 0 0,1 2,14A2,2 0 0,1 0,12Z"/></svg></summary><div class="vfaq-answer" style="padding:30px 22px;background:#fff;"><p dir="ltr" style="font-size:16px;line-height:1.75;">For a simple store with a basic catalog and no <a href="https://virtina.com/woocommerce-customizations/" style="outline: none;">custom WooCommerce development</a> requirements, you can handle the data transfer with an automated tool like LitExtension without developer involvement. But theme rebuild, 301 redirect implementation, SEO plugin configuration, and any custom functionality require technical judgment. For any store with a meaningful SEO footprint, B2B pricing requirements, or integrations that need to carry over, a WooCommerce developer is not optional. Getting the redirect map wrong, or launching without SEO configuration in place, creates problems that take longer to fix than the original migration did.</p></div></details>
<details class="vfaq" style="background:transparent;margin-top:7px;"><summary style="cursor:pointer;padding:17px;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;background:rgba(245,245,245,0.5);"><span style="font-size:16px;font-weight:600;color:#43627f;line-height:2;flex:1;">What happens to my Volusion payment processing after migration?</span><svg viewBox="0 0 24 24" width="17" height="17" style="fill:#50565f;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg"><path d="M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12M8,12A2,2 0 0,1 10,10A2,2 0 0,1 12,12A2,2 0 0,1 10,14A2,2 0 0,1 8,12M0,12A2,2 0 0,1 2,10A2,2 0 0,1 4,12A2,2 0 0,1 2,14A2,2 0 0,1 0,12Z"/></svg></summary><div class="vfaq-answer" style="padding:30px 22px;background:#fff;"><p dir="ltr" style="font-size:16px;line-height:1.75;">Volusion's own payment gateway charges maintenance fees ranging from 1.25% (Personal plan) to 0.35% (Business plan) on top of standard processing fees. On WooCommerce you choose your own gateway. Stripe, PayPal, Square, and Authorize.net all have official WooCommerce extensions. Setup requires new API key configuration but is not technically complex. If you were on Volusion Payments, you'll also need to re-establish merchant processing with an independent gateway before go-live. Factor this into your testing checklist before DNS cutover.</p></div></details>
<details class="vfaq" style="background:transparent;margin-top:7px;"><summary style="cursor:pointer;padding:17px;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;background:rgba(245,245,245,0.5);"><span style="font-size:16px;font-weight:600;color:#43627f;line-height:2;flex:1;">What data can I actually export from Volusion before I leave?</span><svg viewBox="0 0 24 24" width="17" height="17" style="fill:#50565f;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg"><path d="M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12M8,12A2,2 0 0,1 10,10A2,2 0 0,1 12,12A2,2 0 0,1 10,14A2,2 0 0,1 8,12M0,12A2,2 0 0,1 2,10A2,2 0 0,1 0,12Z"/></svg></summary><div class="vfaq-answer" style="padding:30px 22px;background:#fff;"><p dir="ltr" style="font-size:16px;line-height:1.75;">Via Admin, then Data Management, then Export, you can pull products (titles, descriptions, prices, images), customer accounts, order history, and category structure in CSV format. Store settings, custom fields that have no WooCommerce equivalent, and theme or design assets do not transfer. Screenshot or export all active SEO meta titles and descriptions before you leave. Volusion stores these in product and category fields, and you'll need them to restore your meta data inside WooCommerce's SEO plugin once the migration is complete.</p></div></details>
</div>"""

print(f"\n=== Post content built: {len(content)} chars ===")

# ── WordPress payload ─────────────────────────────────────────────────────────
payload = {
    "title": "From Volusion to WooCommerce: the migration story every frustrated store owner needs to read",
    "slug": "volusion-to-woocommerce-migration",
    "status": "draft",
    "content": content,
    "featured_media": media_ids["featured"],
    "categories": [79, 415],
    "author": 9,
    "meta": {
        "_yoast_wpseo_title": "From Volusion to WooCommerce: the migration story | Virtina",
        "_yoast_wpseo_metadesc": "Frustrated with Volusion billing surprises and integration dead ends? The honest Volusion to WooCommerce migration story: what it takes and what you gain.",
        "_yoast_wpseo_focuskw": "Volusion to WooCommerce migration",
    },
}

print("\n=== Pushing post to WordPress ===")
r = requests.post(f"{WP_BASE}/posts", headers=WP_HEADERS, json=payload, timeout=90)
if not r.ok:
    print(f"POST error {r.status_code}: {r.text[:500]}")
    sys.exit(1)
post = r.json()
post_id = post["id"]
post_edit_url = f"https://virtina.com/wp-admin/post.php?post={post_id}&action=edit"
print(f"  Post ID: {post_id}")
print(f"  Edit URL: {post_edit_url}")
print(f"  Status: {post.get('status')}")

# ── Verify ────────────────────────────────────────────────────────────────────
print("\n=== Verification ===")
vr = requests.get(f"{WP_BASE}/posts/{post_id}?context=edit", headers=WP_HEADERS, timeout=30)
vr.raise_for_status()
vpost = vr.json()
title_ok = "Volusion" in vpost.get("title", {}).get("rendered", "")
content_raw = vpost.get("content", {}).get("raw", "")
content_ok = len(content_raw) > 5000
fm_ok = vpost.get("featured_media") == media_ids["featured"]
status_ok = vpost.get("status") == "draft"

print(f"  title OK: {title_ok}")
print(f"  content length: {len(content_raw)} chars — OK: {content_ok}")
print(f"  featured_media {vpost.get('featured_media')} == {media_ids['featured']}: {fm_ok}")
print(f"  status draft: {status_ok}")

# ── Save results ──────────────────────────────────────────────────────────────
results = {
    "post_id": post_id,
    "post_edit_url": post_edit_url,
    "media_ids": media_ids,
    "media_urls": media_urls,
    "checks": {
        "title_ok": title_ok,
        "content_ok": content_ok,
        "featured_media_ok": fm_ok,
        "status_ok": status_ok,
    },
    "content": content,
}
out_path = WORK_DIR / "volusion_post_final_results.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"\nResults saved: {out_path}")
print(f"\n=== DONE ===")
print(f"Post ID: {post_id}")
print(f"Edit: {post_edit_url}")
print("Media IDs:")
for k in ["featured", "section1", "section2", "section3"]:
    print(f"  {k}: {media_ids[k]}")
