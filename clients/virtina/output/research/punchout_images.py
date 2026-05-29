#!/usr/bin/env python3
"""
Image fetch, crop-resize, upload, and infographic generation for WooCommerce punchout post.
Run: python clients/virtina/output/research/punchout_images.py
"""
import os, sys, json, time, io, base64, textwrap
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from PIL import Image
from io import BytesIO
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ---- Credentials ----
WP_USERNAME    = os.environ.get("WP_USERNAME", "")
WP_APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")

if not WP_USERNAME or not WP_APP_PASSWORD:
    print("ERROR: WP_USERNAME or WP_APP_PASSWORD not set. Load .env first.")
    sys.exit(1)

WP_MEDIA_EP = "https://virtina.com/wp-json/wp/v2/media"
auth_b64 = base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()).decode()
AUTH_HEADER = f"Basic {auth_b64}"

SESS = requests.Session()
SESS.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
SESS.verify = False

# ---- Image specs ----
IMAGES = [
    {
        "name": "featured",
        "width": 1309, "height": 500,
        "pexels_ids": [3184297, 3182812, 3183197, 1181533, 1181467, 3184338],
        "openverse_queries": ["business laptop office meeting", "professional office computer work", "team office computers business"],
        "alt": "Two B2B business professionals reviewing a WooCommerce supplier catalog and eProcurement integration setup on a laptop in a modern office",
        "filename": "woocommerce-punchout-catalog-integration-hero.jpg",
    },
    {
        "name": "body1",
        "width": 670, "height": 352,
        "pexels_ids": [1181671, 3183150, 4491461, 1181244, 7364107],
        "openverse_queries": ["procurement office computer work", "office professional computer desk", "business person laptop purchase order"],
        "alt": "Procurement officer at a desk reviewing a supplier catalog on a computer screen for enterprise B2B purchase order workflow integration",
        "filename": "woocommerce-punchout-catalog-what-is-punchout.jpg",
    },
    {
        "name": "body2",
        "width": 670, "height": 352,
        "pexels_ids": [2004161, 1181263, 1181298, 546819, 3861958],
        "openverse_queries": ["developer laptop coding integration", "software developer computer api", "developer typing laptop desk"],
        "alt": "Developer configuring a WooCommerce punchout catalog plugin with cXML endpoint settings on a laptop during integration setup",
        "filename": "woocommerce-punchout-setup-steps-developer.jpg",
    },
]

def pexels_large2x_url(photo_id):
    return f"https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"

def pexels_api_search(query, per_page=8):
    if not PEXELS_API_KEY:
        return []
    url = f"https://api.pexels.com/v1/search?query={requests.utils.quote(query)}&orientation=landscape&per_page={per_page}"
    r = SESS.get(url, headers={"Authorization": PEXELS_API_KEY}, timeout=30)
    if r.status_code == 200:
        return r.json().get("photos", [])
    return []

def openverse_search(query, per_page=8):
    url = f"https://api.openverse.org/v1/images/?q={requests.utils.quote(query)}&source=stocksnap&license_type=commercial&per_page={per_page}&aspect_ratio=wide"
    r = SESS.get(url, timeout=30)
    if r.status_code == 200:
        return r.json().get("results", [])
    return []

def download(url):
    try:
        r = SESS.get(url, timeout=60)
        if r.status_code == 200 and len(r.content) > 8000:
            return r.content
    except Exception as e:
        print(f"  download error: {e}")
    return None

def crop_resize(raw, w, h, quality=88):
    img = Image.open(BytesIO(raw)).convert("RGB")
    ow, oh = img.size
    scale = max(w / ow, h / oh)
    nw, nh = int(ow * scale), int(oh * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top  = (nh - h) // 2
    img = img.crop((left, top, left + w, top + h))
    buf = BytesIO()
    img.save(buf, "JPEG", quality=quality, optimize=True)
    out = buf.getvalue()
    if len(out) > 250 * 1024:
        buf = BytesIO()
        img.save(buf, "JPEG", quality=75, optimize=True)
        out = buf.getvalue()
        print(f"    recompressed to 75q: {len(out)//1024}KB")
    return out

def upload_wp(img_bytes, filename, alt):
    headers = {
        "Authorization": AUTH_HEADER,
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "image/jpeg",
    }
    r = SESS.post(WP_MEDIA_EP, headers=headers, data=img_bytes, timeout=120)
    if r.status_code in (200, 201):
        media = r.json()
        mid = media.get("id")
        print(f"    Uploaded: media_id={mid}")
        # Set alt text
        SESS.post(f"{WP_MEDIA_EP}/{mid}",
                  headers={**headers, "Content-Type": "application/json"},
                  json={"alt_text": alt}, timeout=30)
        return media
    else:
        print(f"    Upload failed {r.status_code}: {r.text[:200]}")
        return None

def process_image(spec):
    print(f"\n=== {spec['name']} ({spec['width']}x{spec['height']}) ===")

    raw = None
    source_desc = None

    # 1. Try Pexels API if key available
    if PEXELS_API_KEY:
        for q in spec.get("openverse_queries", [])[:2]:
            photos = pexels_api_search(q)
            for p in photos:
                if p.get("width", 0) >= spec["width"] and p.get("height", 0) >= spec["height"]:
                    url = p["src"].get("large2x") or p["src"].get("original")
                    raw = download(url)
                    if raw:
                        source_desc = f"pexels_api_id={p['id']}"
                        break
            if raw:
                break

    # 2. Try Pexels CDN direct (no key needed)
    if not raw:
        for pid in spec.get("pexels_ids", []):
            url = pexels_large2x_url(pid)
            print(f"  Trying Pexels CDN id={pid}")
            raw = download(url)
            if raw:
                source_desc = f"pexels_cdn_id={pid}"
                print(f"    Downloaded {len(raw)//1024}KB")
                break
            time.sleep(0.3)

    # 3. Fall back to Openverse
    if not raw:
        print("  Falling back to Openverse...")
        for q in spec.get("openverse_queries", []):
            results = openverse_search(q)
            for item in results:
                url = item.get("url") or item.get("thumbnail")
                if url:
                    raw = download(url)
                    if raw:
                        source_desc = f"openverse_id={item.get('id', '?')}"
                        print(f"    Openverse hit: {url[:70]}")
                        break
            if raw:
                break
            time.sleep(0.5)

    if not raw:
        print(f"  FAILED: no image found for {spec['name']}")
        return {"name": spec["name"], "status": "FAILED", "media_id": None, "src": None, "alt": spec["alt"]}

    processed = crop_resize(raw, spec["width"], spec["height"])
    print(f"  Cropped to {spec['width']}x{spec['height']}, {len(processed)//1024}KB")

    media = upload_wp(processed, spec["filename"], spec["alt"])
    if media:
        return {
            "name": spec["name"],
            "status": "OK",
            "media_id": media["id"],
            "src": media.get("source_url", ""),
            "alt": spec["alt"],
            "filename": spec["filename"],
            "source": source_desc,
        }
    else:
        return {"name": spec["name"], "status": "UPLOAD_FAILED", "media_id": None, "src": None, "alt": spec["alt"]}


# ---- Infographic generator ----
def generate_infographic():
    """Generate cXML punchout roundtrip workflow infographic at 670x352."""
    print("\n=== Generating infographic (670x352) ===")

    TEAL  = "#16afa0"
    SLATE = "#43627f"
    LIGHT = "#e8f4f3"
    DARK  = "#2d3e50"
    WHITE = "#ffffff"

    DPI = 96
    fig_w = 670 / DPI
    fig_h = 352 / DPI
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=DPI)
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 670)
    ax.set_ylim(0, 352)
    ax.axis("off")

    # Title
    ax.text(335, 330, "cXML Punchout Roundtrip Workflow",
            ha="center", va="top", fontsize=11, fontweight="bold", color=SLATE)

    # Steps
    steps = [
        ("1", "Buyer opens\nSAP Ariba / Coupa"),
        ("2", "PSR sent to\nWooCommerce"),
        ("3", "Buyer browses\ncatalog (SSO)"),
        ("4", "Cart transferred\nback (POM)"),
        ("5", "PO created in\nbuyer system"),
    ]

    n = len(steps)
    step_w = 105
    step_h = 72
    gap    = 20
    total_w = n * step_w + (n - 1) * gap
    start_x = (670 - total_w) / 2
    center_y = 190

    for i, (num, label) in enumerate(steps):
        x = start_x + i * (step_w + gap)
        y = center_y - step_h / 2

        # Box
        box = FancyBboxPatch((x, y), step_w, step_h,
                              boxstyle="round,pad=4",
                              facecolor=LIGHT, edgecolor=TEAL, linewidth=1.5)
        ax.add_patch(box)

        # Circle number
        circle = plt.Circle((x + step_w / 2, y + step_h - 16), 12,
                             color=TEAL, zorder=5)
        ax.add_patch(circle)
        ax.text(x + step_w / 2, y + step_h - 16, num,
                ha="center", va="center", fontsize=8, fontweight="bold",
                color=WHITE, zorder=6)

        # Label
        ax.text(x + step_w / 2, y + step_h / 2 - 4, label,
                ha="center", va="center", fontsize=7.5, color=DARK,
                multialignment="center")

        # Arrow (not after last step)
        if i < n - 1:
            ax_x = x + step_w + 2
            ay = center_y
            ax.annotate("", xy=(ax_x + gap - 4, ay), xytext=(ax_x, ay),
                        arrowprops=dict(arrowstyle="->", color=SLATE, lw=1.5))

    # Stats bar at bottom
    stats = [
        ("2-5 days", "avg implementation"),
        ("$299-$599/mo", "plugin cost"),
        ("5.5M+ suppliers", "on SAP Ariba"),
        ("100+ platforms", "support cXML"),
    ]
    stats_y = 75
    stat_w = 670 / len(stats)
    for i, (val, label) in enumerate(stats):
        sx = i * stat_w + stat_w / 2
        ax.text(sx, stats_y + 14, val, ha="center", va="center",
                fontsize=8.5, fontweight="bold", color=TEAL)
        ax.text(sx, stats_y - 4, label, ha="center", va="center",
                fontsize=7, color=DARK)

    # Divider line above stats
    ax.axhline(y=100, xmin=0.03, xmax=0.97, color="#dde0e6", linewidth=0.8)

    # Footer
    ax.text(335, 15, "Source: cXML.org | virtina.com | Data: 2026",
            ha="center", va="bottom", fontsize=6, color="#888888")

    plt.tight_layout(pad=0)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    buf = BytesIO()
    fig.savefig(buf, format="JPEG", dpi=DPI, bbox_inches="tight",
                facecolor=WHITE, pil_kwargs={"quality": 88, "optimize": True})
    buf.seek(0)
    raw = buf.read()
    plt.close(fig)
    print(f"  Infographic generated: {len(raw)//1024}KB")

    # Verify dimensions
    img_check = Image.open(BytesIO(raw))
    actual_w, actual_h = img_check.size
    print(f"  Actual size: {actual_w}x{actual_h}")

    # Resize to exactly 670x352 if needed
    if actual_w != 670 or actual_h != 352:
        img_check = img_check.resize((670, 352), Image.LANCZOS)
        buf2 = BytesIO()
        img_check.save(buf2, "JPEG", quality=88, optimize=True)
        raw = buf2.getvalue()
        print(f"  Resized to 670x352: {len(raw)//1024}KB")

    # Upload
    filename = "woocommerce-punchout-cxml-workflow-infographic.jpg"
    alt = ("cXML punchout roundtrip workflow diagram for WooCommerce B2B stores showing the 5-step "
           "process from SAP Ariba to purchase order creation with implementation stats")
    media = upload_wp(raw, filename, alt)

    if media:
        return {
            "name": "infographic",
            "status": "OK",
            "media_id": media["id"],
            "src": media.get("source_url", ""),
            "alt": alt,
            "filename": filename,
            "source": "matplotlib_generated",
        }
    else:
        return {"name": "infographic", "status": "UPLOAD_FAILED", "media_id": None, "src": None}


def main():
    print("=== Punchout Blog Image Pipeline ===")
    print(f"WP user: {WP_USERNAME}")
    print(f"Pexels key: {'YES' if PEXELS_API_KEY else 'NO (CDN fallback)'}")

    all_results = []

    for spec in IMAGES:
        r = process_image(spec)
        all_results.append(r)
        time.sleep(1)

    infographic_result = generate_infographic()
    all_results.append(infographic_result)

    print("\n=== SUMMARY ===")
    for r in all_results:
        print(f"  {r['name']:15s} | {r.get('status','?'):15s} | id={r.get('media_id')} | {(r.get('src') or '')[:70]}")

    out = r"C:\content-intel\clients\virtina\output\research\punchout_image_results.json"
    with open(out, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults: {out}")

    fails = [r for r in all_results if r.get("status") != "OK"]
    if fails:
        print(f"FAILURES: {[r['name'] for r in fails]}")
        sys.exit(1)
    else:
        print("All 4 images (featured + 2 body + infographic) uploaded OK.")
    return all_results

if __name__ == "__main__":
    main()
