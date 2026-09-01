#!/usr/bin/env python3
"""
Full publish pipeline for Virtina WooCommerce B2B Customer Portal post.
1. Fetch images from Openverse/Pexels
2. Crop-resize to exact dimensions
3. Upload to WordPress media library
4. Build final HTML
5. Push to WordPress as draft

Run: python publish_b2b_portal.py
Requires: pip install requests pillow
"""

import os
import sys
import json
import time
import requests
import base64
from io import BytesIO

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("WARNING: Pillow not installed. Image resizing will not work.")
    print("Run: pip install pillow")

# ---- Credentials (loaded from environment) ----
WP_USERNAME = os.environ.get("WP_USERNAME", "")
WP_APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")

if not WP_USERNAME or not WP_APP_PASSWORD:
    print("ERROR: WP_USERNAME or WP_APP_PASSWORD not set.")
    print("Load from .env first: Get-Content .env | % { $e = $_ -split '=',2; [System.Environment]::SetEnvironmentVariable($e[0],$e[1],'Process') }")
    sys.exit(1)

auth_b64 = base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()).decode()
WP_AUTH_HEADER = f"Basic {auth_b64}"
WP_MEDIA_ENDPOINT = "https://virtina.com/wp-json/wp/v2/media"
WP_POSTS_ENDPOINT = "https://virtina.com/wp-json/wp/v2/posts"

# ---- Image specs ----
IMAGES = [
    {
        "name": "featured",
        "width": 1309, "height": 500,
        "pexels_query": "business professional laptop dashboard office",
        "openverse_queries": ["office laptop business", "business desk laptop work", "professional office worker laptop"],
        "alt": "Business professional reviewing a B2B customer portal dashboard on a laptop in a modern office workspace",
        "filename": "woocommerce-b2b-portal-featured.jpg",
    },
    {
        "name": "body1",
        "width": 670, "height": 352,
        "pexels_query": "warehouse worker inventory shelves",
        "openverse_queries": ["warehouse worker shelves", "warehouse inventory storage", "warehouse worker boxes"],
        "alt": "Warehouse worker in high-visibility vest checking inventory shelves representing B2B order and stock management",
        "filename": "woocommerce-b2b-portal-body1.jpg",
    },
    {
        "name": "body2",
        "width": 670, "height": 352,
        "pexels_query": "business team meeting laptop table",
        "openverse_queries": ["team meeting laptop", "business meeting table", "office meeting discussion"],
        "alt": "Small business team reviewing WooCommerce portal implementation plans at a meeting table with laptop and documents",
        "filename": "woocommerce-b2b-portal-body2.jpg",
    },
    {
        "name": "body3",
        "width": 670, "height": 352,
        "pexels_query": "business person phone laptop office desk",
        "openverse_queries": ["business phone office", "office phone call laptop", "business desk phone work"],
        "alt": "Account manager at a desk on a phone call while reviewing customer account data on a laptop representing B2B portal onboarding support",
        "filename": "woocommerce-b2b-portal-body3.jpg",
    },
]


def fetch_pexels_photos(query: str, per_page: int = 10) -> list:
    if not PEXELS_API_KEY:
        return []
    url = f"https://api.pexels.com/v1/search"
    params = {"query": query, "orientation": "landscape", "per_page": per_page}
    headers = {"Authorization": PEXELS_API_KEY}
    try:
        r = requests.get(url, params=params, headers=headers, timeout=20)
        if r.status_code == 200:
            return r.json().get("photos", [])
        print(f"  Pexels {r.status_code}: {r.text[:100]}")
    except Exception as e:
        print(f"  Pexels error: {e}")
    return []


def fetch_openverse_images(query: str, per_page: int = 10) -> list:
    url = "https://api.openverse.org/v1/images/"
    params = {
        "q": query,
        "source": "stocksnap",
        "license_type": "commercial",
        "per_page": per_page,
        "aspect_ratio": "wide",
    }
    try:
        r = requests.get(url, params=params, timeout=20)
        if r.status_code == 200:
            return r.json().get("results", [])
        print(f"  Openverse {r.status_code}: {r.text[:100]}")
        # Try without source filter
        params2 = {"q": query, "license": "cc0,pdm", "per_page": per_page, "aspect_ratio": "wide"}
        r2 = requests.get(url, params=params2, timeout=20)
        if r2.status_code == 200:
            return r2.json().get("results", [])
    except Exception as e:
        print(f"  Openverse error: {e}")
    return []


def download_image(url: str) -> bytes | None:
    try:
        r = requests.get(url, timeout=60, stream=True)
        if r.status_code == 200:
            data = r.content
            if len(data) < 5000:
                print(f"  Too small ({len(data)} bytes), skipping")
                return None
            if data[:3] == b'\xff\xd8\xff' or data[:4] == b'\x89PNG':
                return data
            print(f"  Not JPEG/PNG, header={data[:4].hex()}")
        else:
            print(f"  Download {r.status_code}: {url[:60]}")
    except Exception as e:
        print(f"  Download error: {e}")
    return None


def crop_resize_jpeg(img_bytes: bytes, w: int, h: int, quality: int = 82) -> bytes:
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    ow, oh = img.size
    scale = max(w / ow, h / oh)
    nw, nh = int(ow * scale), int(oh * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top = (nh - h) // 2
    img = img.crop((left, top, left + w, top + h))
    buf = BytesIO()
    img.save(buf, "JPEG", quality=quality, optimize=True)
    result = buf.getvalue()
    if len(result) > 200 * 1024:
        buf = BytesIO()
        img.save(buf, "JPEG", quality=72, optimize=True)
        result = buf.getvalue()
    return result


def upload_wp_media(img_bytes: bytes, filename: str, alt_text: str) -> dict | None:
    headers = {
        "Authorization": WP_AUTH_HEADER,
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "image/jpeg",
    }
    print(f"  Uploading {filename} ({len(img_bytes)//1024}KB)...")
    try:
        r = requests.post(WP_MEDIA_ENDPOINT, headers=headers, data=img_bytes, timeout=120)
        if r.status_code in (200, 201):
            media = r.json()
            mid = media.get("id")
            print(f"  Uploaded OK: media ID={mid}")
            # Set alt_text
            patch = requests.post(
                f"{WP_MEDIA_ENDPOINT}/{mid}",
                headers={"Authorization": WP_AUTH_HEADER, "Content-Type": "application/json"},
                json={"alt_text": alt_text},
                timeout=30,
            )
            if patch.status_code in (200, 201):
                print(f"  Alt text set OK")
            else:
                print(f"  Alt text FAILED {patch.status_code}")
            return media
        else:
            print(f"  Upload FAILED {r.status_code}: {r.text[:300]}")
    except Exception as e:
        print(f"  Upload exception: {e}")
    return None


def source_and_upload(spec: dict) -> dict:
    print(f"\n--- {spec['name']} ({spec['width']}x{spec['height']}) ---")
    selected_url = None
    photo_source_id = None
    source_name = None

    # Try Pexels first
    if PEXELS_API_KEY:
        all_pexels_queries = [spec["pexels_query"]] + spec.get("openverse_queries", [])[:1]
        for q in all_pexels_queries:
            print(f"  Pexels query: '{q}'")
            photos = fetch_pexels_photos(q, 10)
            for p in photos:
                if p.get("width", 0) >= spec["width"] and p.get("height", 0) >= spec["height"]:
                    img_url = p["src"].get("large2x") or p["src"].get("original")
                    if img_url:
                        selected_url = img_url
                        photo_source_id = str(p.get("id", ""))
                        source_name = "pexels"
                        print(f"  Selected Pexels photo {photo_source_id}")
                        break
            if selected_url:
                break
            time.sleep(0.5)

    # Try Openverse if no Pexels result
    if not selected_url:
        all_ov_queries = spec.get("openverse_queries", [spec["pexels_query"]])
        for q in all_ov_queries:
            print(f"  Openverse query: '{q}'")
            results = fetch_openverse_images(q, 10)
            for item in results:
                img_url = item.get("url") or item.get("thumbnail")
                if img_url and not img_url.endswith(".gif"):
                    selected_url = img_url
                    photo_source_id = str(item.get("id", "openverse"))
                    source_name = "openverse"
                    print(f"  Selected Openverse: {img_url[:70]}")
                    break
            if selected_url:
                break
            time.sleep(1)

    if not selected_url:
        print(f"  IMAGE SEARCH FAILED for {spec['name']}")
        return {"name": spec["name"], "status": "FAILED", "media_id": None, "src": None,
                "alt": spec["alt"], "pexels_id": None, "source": None}

    # Download
    print(f"  Downloading...")
    img_bytes = download_image(selected_url)
    if not img_bytes:
        # Try one more fallback
        fallback_q = spec.get("openverse_queries", [""])[0]
        print(f"  Download failed, trying fallback openverse query: '{fallback_q}'")
        results = fetch_openverse_images(fallback_q, 5)
        for item in results:
            fb_url = item.get("url")
            if fb_url and fb_url != selected_url:
                img_bytes = download_image(fb_url)
                if img_bytes:
                    photo_source_id = str(item.get("id", "openverse_fallback"))
                    break
        if not img_bytes:
            print(f"  IMAGE FAILED: could not download")
            return {"name": spec["name"], "status": "DOWNLOAD_FAILED", "media_id": None,
                    "src": None, "alt": spec["alt"], "pexels_id": photo_source_id, "source": source_name}

    print(f"  Downloaded {len(img_bytes)//1024}KB")

    # Crop/resize
    if not PIL_AVAILABLE:
        print("  ERROR: Pillow not available, cannot resize image")
        return {"name": spec["name"], "status": "NO_PIL", "media_id": None,
                "src": None, "alt": spec["alt"], "pexels_id": photo_source_id, "source": source_name}

    processed = crop_resize_jpeg(img_bytes, spec["width"], spec["height"])
    print(f"  Resized to {spec['width']}x{spec['height']}: {len(processed)//1024}KB")

    # Upload (with one retry)
    media = upload_wp_media(processed, spec["filename"], spec["alt"])
    if not media:
        time.sleep(3)
        print("  Retrying upload...")
        media = upload_wp_media(processed, spec["filename"], spec["alt"])

    if media:
        src_url = media.get("source_url", "")
        return {"name": spec["name"], "status": "OK", "media_id": media.get("id"),
                "src": src_url, "alt": spec["alt"], "pexels_id": photo_source_id, "source": source_name}
    else:
        return {"name": spec["name"], "status": "UPLOAD_FAILED", "media_id": None,
                "src": None, "alt": spec["alt"], "pexels_id": photo_source_id, "source": source_name}


def build_html(img_results: dict) -> str:
    """Build the complete post HTML with actual image URLs substituted."""

    def img_tag(name: str) -> str:
        r = img_results.get(name, {})
        mid = r.get("media_id") or 0
        src = r.get("src") or "PLACEHOLDER_UPLOAD_REQUIRED"
        alt = r.get("alt", "")
        if name == "featured":
            # Featured image is set via featured_media, not inline
            return ""
        w, h = (670, 352)
        return f'<span style="display:block;margin:20px 0;"><img alt="{alt}" data-id="{mid}" width="{w}" data-init-width="{w}" height="{h}" data-init-height="{h}" title="" loading="lazy" src="{src}" data-width="{w}" data-height="{h}" style="aspect-ratio: auto {w} / {h};max-width:100%;"></span>'

    html = """<div style="background:linear-gradient(rgba(0,213,192,0.28),rgba(0,213,192,0.28));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 dir="ltr" style="color:#43627f;font-size:30px;">Summary</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Your WooCommerce "My Account" page is not a B2B customer portal. It was built for retail consumers, and it shows: your buyers can't see their contract pricing, can't reorder in bulk from their history, and can't check live inventory without calling someone. This Q&amp;A article answers the ten questions B2B decision-makers ask before commissioning a portal build: what a portal is, which WooCommerce plugins deliver it (B2BKing vs. Wholesale Suite vs. custom development), what it realistically costs and how long it takes, and when the investment simply doesn't make sense. The adoption question, how to get buyers to actually use the portal once it's live, is covered last, because it's the one question no competitor article bothers to answer.</p>
</div>

<div style="background:linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 style="color:#43627f;font-size:30px;">Introduction</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Your sales rep picks up the phone. Again. A buyer needs to know if SKU #4471 is in stock, what their net-30 price is, and whether last month's order shipped. Three questions your website should answer without a phone call, but doesn't. This isn't a buyer behavior problem. It's a self-service infrastructure gap, and it's costing you more than you think: each manual order costs $30-60 to handle versus $1-3 through a portal.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">If you're running WooCommerce and selling B2B, you have a choice to make. The questions below walk through it clearly: what a real B2B portal includes, which plugin path gets you there, and what the math looks like on the other side.</p>
</div>

<h3>Table of Contents</h3>
<ul style="list-style:none!important;padding-left:0!important;margin:0 0 1.5em 0!important;">
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#what-is-b2b-portal" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">What is a B2B customer portal?</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#why-buyers-call-sales" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">Why buyers call instead of reorder online</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#b2b-portal-features" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">Must-have B2B portal features on WooCommerce</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#woocommerce-b2b-portal-plugins" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">B2BKing vs. Wholesale Suite vs. custom dev</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#b2b-portal-cost-timeline" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">WooCommerce B2B portal cost and timeline</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#account-specific-pricing" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">Account-specific pricing without exposure</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#portal-erp-integration" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">Does your portal need ERP integration?</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#portal-roi-operations" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">Impact on sales rep time and support costs</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#when-not-to-build-portal" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">When not to build a B2B portal</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#buyer-portal-adoption" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">Getting buyers to use the portal</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#people-also-ask" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">People also ask</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#conclusion" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">Conclusion</a></li>
</ul>

<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="what-is-b2b-portal" style="color:#43627f;font-size:30px;">What exactly is a B2B customer portal, and is it different from my WooCommerce account page?</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">A B2B customer portal is a private, account-specific dashboard where your buyers can check order status, download invoices, view their contract pricing, and reorder without calling anyone. It is very different from the standard WooCommerce "My Account" page, which was built for individual consumers, not company accounts.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">The default WooCommerce account page gives buyers an order history, basic account settings, and a simple login. That's adequate for a retail customer buying once or twice a year. It is not adequate for a distribution account placing 40 orders per year across multiple buyers, with negotiated pricing and net-30 terms.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">What separates a B2B portal from an account page comes down to five things: a company account hierarchy where multiple users log in under one corporate account with different permission levels, contract-specific pricing visible only after authenticated login, reorder tools that let buyers replicate a past order in bulk, invoice management with payment terms visible in the dashboard, and a quote request workflow that doesn't require an email or phone call. If your buyers are logging in and seeing the same account page your retail customers see, you don't have a B2B portal.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">This distinction matters for buyers who need to do business efficiently. It also matters for you: <a href="https://virtina.com/b2b-ecommerce-marketplace-on-woocommerce/" style="outline: none;">WooCommerce's B2B capabilities</a> go well beyond the defaults, but only if you build for them deliberately.</p>
</div>

<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="why-buyers-call-sales" style="color:#43627f;font-size:30px;">Why are my B2B buyers calling the sales team instead of reordering online?</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Your buyers are calling because your online store does not show them their contract pricing, does not let them reorder from their order history, and does not tell them whether the SKU they need is in stock. Until those three things are true, calling a sales rep is faster than using your website.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">This is not a buyer attitude problem. Per Gartner (2025), 75% of B2B buyers prefer to complete purchases without involving a sales rep. That preference is real. But a preference for self-service doesn't fix a self-service experience that actively fails them. If your portal shows retail pricing to an authenticated account holder, they'll call to get their real price every time.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">The three gaps that drive phone calls: pricing is wrong or missing for authenticated accounts; there's no reorder path from order history (or reorder requires rebuilding the cart manually); and inventory visibility is either absent or cached so far out of date that buyers can't trust it. These are feature gaps, not buyer habits. Don't blame your customers for calling. Fix what's missing. The features that close these gaps are exactly what a B2B portal provides, which is covered in the next section.</p>
</div>

<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="b2b-portal-features" style="color:#43627f;font-size:30px;">What does a WooCommerce B2B customer portal actually include, what are the must-have features?</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">A production-ready WooCommerce B2B portal needs seven core features: company account hierarchy, contract-specific pricing display, reorder from order history, real-time inventory visibility, invoice download with payment terms, a quote request workflow, and shipment tracking. WooCommerce provides none of these out of the box.</p>
<ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;">
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Company account hierarchy.</strong> Multiple users log in under one corporate account. A procurement manager gets full order access; a warehouse buyer gets catalog-only access. Role-based permissions prevent junior users from seeing sensitive pricing or payment data.</span></li>
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Contract-specific pricing.</strong> Each authenticated account sees only their negotiated rates, not public prices. The pricing update happens at login and is invisible to any other account or guest visitor.</span></li>
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Reorder from order history.</strong> One-click reorder of a previous order, including quantities and SKUs. Buyers who place the same order monthly should never rebuild their cart from scratch. When this feature is enabled, repeat orders increase significantly: one-click reorder drove a 33% lift in repeat purchases within six months (per WizCommerce research).</span></li>
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Real-time inventory visibility.</strong> Live stock levels at login, not a cached snapshot from this morning. A buyer who orders 500 units and sees "in stock" needs that data to be accurate when they submit the order.</span></li>
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Invoice and payment terms access.</strong> PDF invoice download, net-30/60 terms visible in the account dashboard. This eliminates the most common accounts-payable support request: "Can you resend the invoice for PO #7741?"</span></li>
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Quote request workflow.</strong> The buyer submits a quote request inside the portal. Your team responds in the same interface, without phone tag or email chains. <a href="https://virtina.com/ai-quote-automation-b2b-sales-delays/" style="outline: none;">Quote request workflow automation</a> can accelerate response time significantly for high-volume distributors.</span></li>
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Shipment tracking.</strong> Order status and carrier tracking number accessible from the account dashboard. Buyers stop calling your logistics team to ask where their pallet is.</span></li>
</ul>
BODY_IMAGE_1_PLACEHOLDER
<p dir="ltr" style="font-size:16px;line-height:1.75;">WooCommerce handles none of these natively. They all require plugins or custom development. The next question covers which plugin path gets you there fastest.</p>
</div>

<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="woocommerce-b2b-portal-plugins" style="color:#43627f;font-size:30px;">Which WooCommerce plugins actually build this, B2BKing, Wholesale Suite, or custom development?</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">B2BKing and Wholesale Suite are the two dominant plugin paths for building a WooCommerce B2B portal. The right choice depends on whether you need an all-in-one solution or a modular stack. Custom development is the path only when both plugins reach their limits. Before selecting either, check how well they support your existing <a href="https://virtina.com/woocommerce-erp-integration/" style="outline: none;">WooCommerce ERP connectors</a> because ERP compatibility is often the deciding factor.</p>

<table data-rows="10" data-cols="5" data-v="middle">
<thead>
<tr>
<th style="" data-direction=""><p><strong>Feature</strong></p></th>
<th style="" data-direction=""><p><strong>WooCommerce (default)</strong></p></th>
<th style="" data-direction=""><p><strong>B2BKing</strong></p></th>
<th style="" data-direction=""><p><strong>Wholesale Suite</strong></p></th>
<th style="" data-direction="" colspan="1" rowspan="1"><p><strong>Custom development</strong></p></th>
</tr>
</thead>
<tbody>
<tr>
<td data-th="Feature" style=""><p>Company account hierarchy</p></td>
<td data-th="WooCommerce (default)" style=""><p>No</p></td>
<td data-th="B2BKing" style=""><p>Yes</p></td>
<td data-th="Wholesale Suite" style=""><p>Partial (with add-ons)</p></td>
<td data-th="Custom development" style="" colspan="1" rowspan="1"><p>Yes</p></td>
</tr>
<tr>
<td data-th="Feature" style=""><p>Role-based / contract pricing</p></td>
<td data-th="WooCommerce (default)" style=""><p>No</p></td>
<td data-th="B2BKing" style=""><p>Yes</p></td>
<td data-th="Wholesale Suite" style=""><p>Yes</p></td>
<td data-th="Custom development" style="" colspan="1" rowspan="1"><p>Yes</p></td>
</tr>
<tr>
<td data-th="Feature" style=""><p>Bulk / quick order form</p></td>
<td data-th="WooCommerce (default)" style=""><p>No</p></td>
<td data-th="B2BKing" style=""><p>Yes</p></td>
<td data-th="Wholesale Suite" style=""><p>Yes</p></td>
<td data-th="Custom development" style="" colspan="1" rowspan="1"><p>Yes</p></td>
</tr>
<tr>
<td data-th="Feature" style=""><p>Reorder from order history</p></td>
<td data-th="WooCommerce (default)" style=""><p>Basic (no bulk reorder)</p></td>
<td data-th="B2BKing" style=""><p>Yes</p></td>
<td data-th="Wholesale Suite" style=""><p>Yes</p></td>
<td data-th="Custom development" style="" colspan="1" rowspan="1"><p>Yes</p></td>
</tr>
<tr>
<td data-th="Feature" style=""><p>Invoice download</p></td>
<td data-th="WooCommerce (default)" style=""><p>No</p></td>
<td data-th="B2BKing" style=""><p>Yes</p></td>
<td data-th="Wholesale Suite" style=""><p>No (requires add-on)</p></td>
<td data-th="Custom development" style="" colspan="1" rowspan="1"><p>Yes</p></td>
</tr>
<tr>
<td data-th="Feature" style=""><p>Quote request workflow</p></td>
<td data-th="WooCommerce (default)" style=""><p>No</p></td>
<td data-th="B2BKing" style=""><p>Yes</p></td>
<td data-th="Wholesale Suite" style=""><p>No</p></td>
<td data-th="Custom development" style="" colspan="1" rowspan="1"><p>Yes</p></td>
</tr>
<tr>
<td data-th="Feature" style=""><p>B2B registration with approval</p></td>
<td data-th="WooCommerce (default)" style=""><p>No</p></td>
<td data-th="B2BKing" style=""><p>Yes</p></td>
<td data-th="Wholesale Suite" style=""><p>Yes (via Lead Capture plugin)</p></td>
<td data-th="Custom development" style="" colspan="1" rowspan="1"><p>Yes</p></td>
</tr>
<tr>
<td data-th="Feature" style=""><p>Real-time ERP sync support</p></td>
<td data-th="WooCommerce (default)" style=""><p>No</p></td>
<td data-th="B2BKing" style=""><p>Via third-party connector</p></td>
<td data-th="Wholesale Suite" style=""><p>Via third-party connector</p></td>
<td data-th="Custom development" style="" colspan="1" rowspan="1"><p>Yes (custom)</p></td>
</tr>
<tr>
<td data-th="Feature" style=""><p>Annual cost (plugin only)</p></td>
<td data-th="WooCommerce (default)" style=""><p>Free</p></td>
<td data-th="B2BKing" style=""><p>$149-$349/yr</p></td>
<td data-th="Wholesale Suite" style=""><p>$300-$600/yr (stack)</p></td>
<td data-th="Custom development" style="" colspan="1" rowspan="1"><p>Project-based</p></td>
</tr>
</tbody>
</table>
<p dir="ltr" style="font-size:14px;line-height:1.6;color:#6e6e6e;margin:4px 0 16px 0;">Feature comparison as of 2026. Plugin capabilities subject to vendor updates.</p>

<p dir="ltr" style="font-size:16px;line-height:1.75;"><strong>B2BKing</strong> packs 137+ features into a single plugin: subaccounts, tiered pricing, bulk order forms, a CRM hub, role-based catalogs, and B2B registration with approval workflow. It's active on 10,000+ WooCommerce stores. Annual cost runs $149-$349 depending on tier. The case for B2BKing is simple: one plugin handles the full portal with minimal configuration overhead. If you want to ship a working portal without coordinating multiple plugin vendors, B2BKing is the faster path.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;"><strong>Wholesale Suite</strong> is a four-plugin stack: Wholesale Prices, Wholesale Order Form, Wholesale Lead Capture, and Wholesale Payments. Buying the full stack costs $300-$600 per year. It's more modular, buy only what you need, but the configuration spans multiple plugins and requires a developer who's comfortable coordinating across all four. Teams that want granular control over each layer, and have a developer on staff to manage it, often prefer this path.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;"><strong>Custom development</strong> is the right path when neither plugin handles your specific account hierarchy, your ERP field mapping, or your catalog rule complexity. That said, custom adds significant cost and timeline (see the next section). An <a href="https://virtina.com/woocommerce-developer-for-ecommerce-success/" style="outline: none;">experienced WooCommerce developer</a> can extend either plugin path with custom code rather than rebuilding from scratch. Virtina builds on both B2BKing and Wholesale Suite and applies custom development where the situation calls for it.</p>
</div>

<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="b2b-portal-cost-timeline" style="color:#43627f;font-size:30px;">How long does it take to build a WooCommerce B2B customer portal, and what does it cost?</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">A plugin-based WooCommerce B2B portal typically takes 4-12 weeks to implement and costs $15,000-$40,000. A custom-built portal runs 3-6 months and $40,000-$80,000. The range depends almost entirely on whether your ERP needs to sync in real time.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">On the plugin path with B2BKing or Wholesale Suite: the low end ($15K-$20K, 4-6 weeks) is a clean install with straightforward pricing rules and no ERP dependency. The high end ($30K-$40K, 8-12 weeks) means custom account hierarchy design, multiple buyer role configurations, and moderate ERP integration. On the custom development path: $40K-$80K and 3-6 months, used when plugin architecture genuinely can't support the required catalog logic or account structure.</p>
BODY_IMAGE_2_PLACEHOLDER
<p dir="ltr" style="font-size:16px;line-height:1.75;">For context, WooCommerce B2B implementation costs $46K-$135K over three years, versus $240K-$540K for enterprise alternatives. Even the high end of a custom WooCommerce portal is a fraction of what Magento Commerce or a comparable enterprise platform would cost over the same period.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">What drives cost up: real-time ERP sync adds 4-8 weeks to any project scope. Custom account hierarchy that goes beyond what plugins support natively adds design and development time. Buyer-specific catalog rules at the SKU level, thousands of separate pricing rules, create database load that requires performance work. These are working ranges based on Virtina's implementation experience. A scoping call determines your actual cost.</p>
</div>

<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="account-specific-pricing" style="color:#43627f;font-size:30px;">Can a WooCommerce portal show each buyer their own pricing and catalog without exposing prices to other accounts?</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Yes. Both B2BKing and Wholesale Suite support role-based pricing that displays contract prices only when the correct buyer account is authenticated. Hidden catalog mode prevents unauthenticated visitors or wrong-account logins from seeing any pricing at all.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Here's how it works in practice: each buyer account is assigned a price ruleset tied to their role or tier. When that buyer logs in, their prices update to contract rates automatically. A different buyer in a different tier sees their own rates. Guest visitors and non-portal buyers see either no prices or a "log in to see pricing" message. This is the configuration distributors with negotiated rates require: three customers buying the same SKU at three different price points, none of them visible to the others.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">The pricing isolation works well, but the data setup isn't automatic on installation. Mapping each account to the correct price tier is a configuration task that requires care. Mistakes here mean buyers see the wrong rates at login, which damages trust immediately. One related consideration: large price-rule sets can affect <a href="https://virtina.com/woocommerce-b2b-performance-fix/" style="outline: none;">portal page load speed</a> under high concurrency if not configured with proper database indexing. It's the most common question Virtina hears from distributors evaluating a portal project, and the answer is yes, it works, but the configuration has to be done correctly.</p>
</div>

<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="portal-erp-integration" style="color:#43627f;font-size:30px;">Does my WooCommerce B2B portal need to connect to my ERP, and how hard is that?</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">If your pricing or inventory changes more than once a week, yes. Without ERP sync, your portal shows stale data, and buyers will stop trusting it within the first month.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Here's the core problem without ERP sync: portal inventory diverges from actual warehouse stock as soon as an order ships, a return is processed, or a pricing contract is updated. A buyer who finds stale data once will revert to calling. The portal then undermines itself. The phone calls don't stop; they just shift from routine reorders to data-verification calls, which are harder and longer.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">What ERP sync does: it pushes real-time stock levels and contract pricing from your ERP into WooCommerce so the portal always reflects current data, then pulls confirmed orders back into the ERP so fulfillment runs in one system. To <a href="https://virtina.com/woocommerce-erp-integration/" style="outline: none;">connect WooCommerce to your ERP</a>, you'll use documented connectors for NetSuite, SAP Business One, Epicor, and Infor. <a href="https://virtina.com/guide-on-woocommerce-rest-api/" style="outline: none;">WooCommerce REST API connections</a> handle the data exchange in most middleware implementations. Timeline: ERP integration adds 4-8 weeks to any portal project scope.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">The exception: if your pricing is static and your inventory turns slowly, a scheduled daily batch sync may be sufficient. Daily sync avoids the complexity of real-time middleware and keeps costs lower. If prices change monthly and you rarely stock out, a batch sync works. If prices change daily or inventory runs close to zero on fast-moving SKUs, real-time sync is not optional.</p>
</div>

<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="portal-roi-operations" style="color:#43627f;font-size:30px;">What does a B2B portal actually do to my sales rep workload and customer service costs?</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">The math is straightforward: a portal-processed order costs $1-3 to handle versus $30-60 for a phone or email order. When buyers can reorder, track shipments, and download invoices themselves, your support ticket volume drops 30-50%.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">On the sales rep side: Forrester research shows that 26% of a sales rep's time goes to administrative tasks, including order entry, order status calls, and invoice resend requests. A portal eliminates the majority of that administrative load. Those are not calls your reps should be taking. That time shifts to account expansion, new relationship development, and consultative selling, which actually generate revenue.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">The impact on the buyer side is measurable too. Portal customers buy 25% more SKUs than non-portal customers, per Adelco case data from Commercetools. One-click reorder drove a 33% increase in repeat purchases within six months in documented buyer portal deployments. Both outcomes reflect a simpler buying experience: when it's easy to reorder, buyers reorder more. When catalog browsing requires no friction, buyers discover more SKUs.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Frame this as operational leverage, not headcount reduction. Your sales reps don't disappear after a portal launch. They stop being expensive order clerks, which is what they were when the only alternative was a phone call.</p>
</div>

<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="when-not-to-build-portal" style="color:#43627f;font-size:30px;">When does a WooCommerce B2B portal NOT make sense, are there situations where we shouldn't build one?</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">A portal does not pay off when your buyers order fewer than four times per year, when your catalog has under 50 SKUs, or when your sales process is inherently consultative. In those cases, the investment in portal infrastructure will not recover its cost.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Three specific situations where a portal is the wrong call, based on Virtina's implementation experience:</p>
<ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;">
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Low order frequency.</strong> If your average buyer places fewer than four orders per year, the self-service efficiency gain is too small to justify $15K-$80K. The math requires volume. Infrequent buyers don't generate enough repetitive order tasks for a portal to earn back the build cost.</span></li>
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Small catalog.</strong> If you carry fewer than 50 SKUs, the browsing and reorder complexity a portal solves doesn't exist. A simple contact form and a PDF price list serve these buyers better, at a fraction of the cost.</span></li>
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Consultative buying processes.</strong> Capital equipment, custom manufacturing, and engineered-to-order products require a sales conversation regardless of what any portal provides. A portal won't replace that conversation. It will add friction between the buyer and the rep who needs to understand the spec.</span></li>
</ul>
<p dir="ltr" style="font-size:16px;line-height:1.75;">This is the "when not to build" guidance that most portal vendors skip. For context on when <a href="https://virtina.com/b2b-ecommerce-for-manufacturers/" style="outline: none;">B2B ecommerce for manufacturers</a> does make sense at scale, the fit criteria look different: high order frequency, deep catalogs, multi-buyer accounts, and standardized products that don't require a custom quote on every order. If those conditions don't describe your business, start smaller before committing to a full portal build.</p>
</div>

<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="buyer-portal-adoption" style="color:#43627f;font-size:30px;">How do I get my B2B buyers to actually use the portal instead of calling their account rep?</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Buyer adoption is the most underdiscussed problem in B2B portal implementation. You can build a technically perfect portal and still have buyers defaulting to phone calls six months later. Adoption is a change management problem, not a feature problem.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">None of the competitor articles on WooCommerce B2B portals address this. It is, in Virtina's experience, the most common post-launch problem. Four tactics that actually move the needle:</p>
<ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;">
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Show buyers their contract pricing is online before go-live.</strong> Many B2B buyers don't know their negotiated rates are in the portal. Put it in the onboarding email: "Log in now to see your account pricing." That single line removes the biggest reason buyers pick up the phone first.</span></li>
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Demonstrate one-click reorder in the onboarding sequence.</strong> This is the biggest friction reducer in the portal. Walk buyers through it with a 60-second video or a guided first-login walkthrough tied to their actual order history, not a generic demo.</span></li>
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Keep a human fallback for the first 90 days.</strong> Don't cut off account rep access at portal launch. Let buyers self-serve and still call. Over 90 days, self-service becomes the default for routine orders because it's genuinely faster, not because you removed the alternative.</span></li>
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Track portal activity by account.</strong> Know which buyer accounts are not logging in by month two. Have your rep follow up with those specific accounts. Personalized outreach from a known rep outperforms any generic "don't forget your portal" email campaign.</span></li>
</ul>
BODY_IMAGE_3_PLACEHOLDER
<p dir="ltr" style="font-size:16px;line-height:1.75;">Adoption is the difference between a portal that pays off and one that sits unused. The technology is the easy part. The change management is where most portal projects succeed or fail, and it starts on day one of your launch sequence, not six months later when the numbers disappoint.</p>
</div>

<div style="background:linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="people-also-ask" style="color:#43627f;font-size:30px;">People also ask</h2>
<h3 style="color:#43627f;font-size:23px;">How much does a WooCommerce B2B portal cost?</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">A plugin-based WooCommerce B2B portal costs $15,000-$40,000 to implement, including configuration, design customization, testing, and QA. A custom-built portal runs $40,000-$80,000 and takes 3-6 months. The cost driver in both cases is ERP integration: adding real-time sync pushes the timeline out by 4-8 weeks and raises the total cost accordingly.</p>
<h3 style="color:#43627f;font-size:23px;">What is the difference between B2BKing and Wholesale Suite?</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">B2BKing is a single plugin with 137+ features, priced at $149-$349 per year. Wholesale Suite is a four-plugin stack costing $300-$600 per year for the full set. B2BKing is faster to configure and includes features like invoice download and quote workflow that Wholesale Suite requires add-ons for. Wholesale Suite gives more granular control over individual components and suits teams with a developer who wants to manage each layer separately.</p>
<h3 style="color:#43627f;font-size:23px;">Do I need a B2B portal if I already have a WooCommerce store?</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">It depends on your order frequency and catalog size. If your buyers place four or more orders per year, your catalog has more than 50 SKUs, and your buyers hold negotiated pricing or net payment terms, the case for a portal is strong. If your buyers order occasionally and your catalog is small, a standard WooCommerce account page may be adequate for now.</p>
<h3 style="color:#43627f;font-size:23px;">How long does buyer portal adoption take?</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Most B2B portal deployments see meaningful self-service adoption within 60-90 days when onboarding is done actively. Passive launch, where you send one announcement email and expect buyers to adapt, typically results in low adoption for 6+ months. The 90-day window with a human fallback, account-level activity tracking, and direct rep follow-up for non-adopters is the approach that consistently closes the gap.</p>
</div>

<div style="background:#00d5c0;border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="conclusion" style="color:#ffffff;font-size:30px;">Conclusion</h2>
<p style="color:#ffffff;font-size:16px;line-height:1.75;">The gap between a WooCommerce account page and a real B2B customer portal is exactly where buyer frustration lives. Your buyers aren't calling because they prefer it. They're calling because your store hasn't given them a better option yet. A portal sized correctly to your order frequency, catalog depth, and ERP situation pays back in reduced support costs, lower order-handling overhead, and higher repeat purchase rates. The ROI math works when the fit criteria are met.</p>
<p style="color:#ffffff;font-size:16px;line-height:1.75;">Virtina helps B2B manufacturers and distributors build WooCommerce portals that buyers actually use: the right plugin path, the right ERP integration approach, and the onboarding structure that drives adoption from day one. If you want to understand where your current WooCommerce setup falls short and what a portal build would actually require, contact Virtina for a scoping conversation.</p>
</div>"""

    # Substitute image placeholders
    b1 = img_tag("body1")
    b2 = img_tag("body2")
    b3 = img_tag("body3")
    html = html.replace("BODY_IMAGE_1_PLACEHOLDER", b1)
    html = html.replace("BODY_IMAGE_2_PLACEHOLDER", b2)
    html = html.replace("BODY_IMAGE_3_PLACEHOLDER", b3)

    return html


def get_categories():
    """Fetch WP categories and find WooCommerce (79) and B2B eCommerce (84)."""
    # Use known IDs from cms.md
    return [79, 84]  # WooCommerce, B2B eCommerce


def push_to_wp(html_content: str, featured_media_id: int) -> dict | None:
    payload = {
        "title": "Does your WooCommerce store have a B2B customer portal, or just an account page?",
        "slug": "woocommerce-b2b-customer-portal",
        "status": "draft",
        "content": html_content,
        "featured_media": featured_media_id,
        "categories": [79, 84],
        "author": 9,
        "meta": {
            "_yoast_wpseo_title": "WooCommerce B2B Customer Portal Guide | Virtina",
            "_yoast_wpseo_metadesc": "Learn what a WooCommerce B2B customer portal includes, which plugins build it, what it costs, and how to get your buyers to stop calling and start self-serving.",
            "_yoast_wpseo_focuskw": "B2B customer portal WooCommerce",
        },
    }
    headers = {
        "Authorization": WP_AUTH_HEADER,
        "Content-Type": "application/json",
    }
    print(f"\nPushing post to WordPress ({WP_POSTS_ENDPOINT})...")
    try:
        r = requests.post(WP_POSTS_ENDPOINT, headers=headers, json=payload, timeout=120)
        if r.status_code in (200, 201):
            post = r.json()
            print(f"Post created! ID={post.get('id')}, link={post.get('link')}")
            return post
        else:
            print(f"POST failed {r.status_code}: {r.text[:500]}")
            # Retry
            time.sleep(5)
            r2 = requests.post(WP_POSTS_ENDPOINT, headers=headers, json=payload, timeout=120)
            if r2.status_code in (200, 201):
                post = r2.json()
                print(f"Retry OK! ID={post.get('id')}")
                return post
            print(f"Retry also failed: {r2.status_code}: {r2.text[:300]}")
    except Exception as e:
        print(f"Push exception: {e}")
    return None


def main():
    if not PIL_AVAILABLE:
        print("FATAL: Pillow not installed. Run: pip install pillow")
        sys.exit(1)

    print("=== VIRTINA PUBLISH PIPELINE: WooCommerce B2B Customer Portal ===\n")

    # Step 1: Source and upload all images
    img_results = {}
    for spec in IMAGES:
        result = source_and_upload(spec)
        img_results[result["name"]] = result
        time.sleep(1)

    # Step 2: Summarize image results
    print("\n=== IMAGE RESULTS ===")
    for name, r in img_results.items():
        print(f"  {name}: {r['status']} | media_id={r['media_id']} | pexels_id={r['pexels_id']} | source={r['source']}")
        if r["src"]:
            print(f"    src={r['src'][:80]}")

    # Validate body images
    failures = [n for n, r in img_results.items() if r["status"] != "OK"]
    if failures:
        print(f"\nWARNING: These images failed: {failures}")
        print("Continuing with placeholders for failed images...")

    # Verify all body image srcs start with virtina.com
    for name in ["body1", "body2", "body3"]:
        src = img_results.get(name, {}).get("src") or ""
        if src and not src.startswith("https://virtina.com/wp-content/uploads/"):
            print(f"WARNING: {name} src does not begin with virtina.com: {src}")

    # Step 3: Build HTML
    print("\n=== BUILDING HTML ===")
    html_content = build_html(img_results)
    print(f"HTML built: {len(html_content)} chars")

    # Step 4: Push to WordPress
    featured_id = img_results.get("featured", {}).get("media_id") or 0
    if featured_id == 0:
        print("WARNING: Featured image has media_id=0. Post will be pushed but featured_media will be 0.")

    post = push_to_wp(html_content, featured_id)

    # Step 5: Save results
    output = {
        "post": post,
        "images": img_results,
        "html_length": len(html_content),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    results_path = r"C:\content-intel\clients\virtina\output\research\publish_results.json"
    with open(results_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nResults saved: {results_path}")

    # Save HTML to file too
    html_path = r"C:\content-intel\clients\virtina\output\research\final_html.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML saved: {html_path}")

    print("\n=== DONE ===")
    if post:
        print(f"Post ID: {post.get('id')}")
        print(f"Preview URL: {post.get('link')} (add ?preview=true to preview)")
    else:
        print("Post push FAILED. Check results file and push manually.")


if __name__ == "__main__":
    main()
