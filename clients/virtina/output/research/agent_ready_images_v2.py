#!/usr/bin/env python3
"""
Replace agent-ready post images with contextually relevant versions:
  - featured:  Better stock photo (ecommerce + technology, not a meeting)
  - body1:     Custom infographic — "What AI Agents vs Humans See on Your Product Page"
  - body2:     Custom infographic — "Schema.org Product: Required Fields for AI Agents"

Updates agent_ready_image_results.json with new media IDs.
Run: python clients/virtina/output/research/agent_ready_images_v2.py
"""
import os, sys, json, base64, time, io
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from PIL import Image
from io import BytesIO
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

WP_USERNAME     = os.environ.get("WP_USERNAME", "")
WP_APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
if not WP_USERNAME or not WP_APP_PASSWORD:
    print("ERROR: WP_USERNAME / WP_APP_PASSWORD not set.")
    sys.exit(1)

WP_MEDIA_EP = "https://virtina.com/wp-json/wp/v2/media"
WP_POSTS_EP = "https://virtina.com/wp-json/wp/v2/posts"
auth_b64 = base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()).decode()
AUTH_HEADER = f"Basic {auth_b64}"

SESS = requests.Session()
SESS.verify = False
SESS.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

RESULTS_FILE = r"C:\content-intel\clients\virtina\output\research\agent_ready_image_results.json"
POST_ID = 42333

# ── Colors (Virtina brand) ────────────────────────────────────────────────────
TEAL    = "#00d5c0"
SLATE   = "#43627f"
DARK    = "#2d3e50"
LIGHT   = "#e8f4f8"
WHITE   = "#ffffff"
RED     = "#e05555"
GREEN   = "#27ae60"
ORANGE  = "#e67e22"

# ── Helpers ───────────────────────────────────────────────────────────────────

def pexels_url(photo_id):
    return (f"https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}"
            f".jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260")

def download(url):
    try:
        r = SESS.get(url, timeout=60)
        if r.status_code == 200 and len(r.content) > 8000:
            return r.content
    except Exception as e:
        print(f"  download error: {e}")
    return None

def crop_resize(raw, w, h, quality=82):
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
        img.save(buf, "JPEG", quality=72, optimize=True)
        out = buf.getvalue()
        print(f"    recompressed to 72q: {len(out)//1024}KB")
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
        SESS.post(f"{WP_MEDIA_EP}/{mid}",
                  headers={**headers, "Content-Type": "application/json"},
                  json={"alt_text": alt}, timeout=30)
        return media
    else:
        print(f"    Upload failed {r.status_code}: {r.text[:200]}")
        return None

def fig_to_jpeg(fig, w, h, quality=82):
    """Render matplotlib figure to exact w×h JPEG bytes at quality 82."""
    buf = BytesIO()
    fig.savefig(buf, format="PNG", dpi=96, bbox_inches="tight", facecolor=WHITE)
    buf.seek(0)
    img = Image.open(buf).convert("RGB")
    if img.size != (w, h):
        img = img.resize((w, h), Image.LANCZOS)
    out = BytesIO()
    img.save(out, "JPEG", quality=quality, optimize=True)
    return out.getvalue()


# ── Featured image: better Pexels photo ──────────────────────────────────────
# These IDs show ecommerce/tech product-browsing scenes, not generic meetings.
# Trying in order until one downloads successfully.
FEATURED_PEXELS_IDS = [
    5632371,   # person reviewing analytics dashboard on laptop
    4974914,   # online shopping on mobile/laptop — tech commerce
    3184338,   # laptop with graphs/charts in modern workspace
    5632391,   # data analytics screen close-up
    1181354,   # focused professional at desk with laptop screen visible
    3861969,   # developer reviewing code on monitor (tech-focused)
    5716027,   # shopping cart + tech concept
    4050285,   # person at laptop with product/store visible
    3823488,   # ecommerce product listing on screen
    2422293,   # laptop showing website/dashboard
]

FEATURED_ALT = (
    "Ecommerce store owner reviewing product data and AI shopping agent readiness "
    "on a laptop, checking structured data and bot accessibility settings"
)

def get_featured():
    print("\n=== Featured image: searching for ecommerce+tech stock photo ===")
    for pid in FEATURED_PEXELS_IDS:
        url = pexels_url(pid)
        print(f"  Trying Pexels id={pid}")
        raw = download(url)
        if raw:
            print(f"    Got {len(raw)//1024}KB")
            processed = crop_resize(raw, 1309, 500, quality=82)
            print(f"    Cropped to 1309x500, {len(processed)//1024}KB")
            filename = "ecommerce-store-agent-ready-hero-v2.jpg"
            media = upload_wp(processed, filename, FEATURED_ALT)
            if media:
                return {
                    "key": "featured",
                    "media_id": media["id"],
                    "src": media.get("source_url", ""),
                    "alt": FEATURED_ALT,
                    "filename": filename,
                    "dimensions": "1309x500",
                    "pexels_id": pid,
                    "file_size_kb": round(len(processed) / 1024, 1),
                }
        time.sleep(0.4)
    print("  FAILED: no featured image downloaded")
    return None


# ── Body 1 infographic: Human vs AI Agent reading a product page ──────────────
def build_body1_infographic():
    """
    Side-by-side: what a human shopper vs an AI agent sees on the same product page.
    Two columns with icons/checkmarks showing what each can read.
    670 × 352 px
    """
    print("\n=== Body 1 infographic: Human vs AI Agent (670x352) ===")

    DPI = 96
    W, H = 670, 352
    fig, ax = plt.subplots(figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    # Title
    ax.text(W / 2, H - 14, "What Your Product Page Shows — Depends Who's Looking",
            ha="center", va="top", fontsize=9.5, fontweight="bold", color=SLATE)

    # Divider line under title
    ax.axhline(y=H - 30, xmin=0.03, xmax=0.97, color="#dde0e6", linewidth=0.8)

    col_w = W / 2
    col_centers = [col_w / 2, col_w + col_w / 2]
    row_top = H - 42

    # Column headers
    for i, (label, color, emoji_sym) in enumerate([
        ("Human Shopper", GREEN, "👤"),
        ("AI Shopping Agent", RED, "🤖"),
    ]):
        cx = col_centers[i]
        # Header box
        box = FancyBboxPatch((cx - 95, row_top - 22), 190, 24,
                              boxstyle="round,pad=3",
                              facecolor=color, edgecolor="none")
        ax.add_patch(box)
        ax.text(cx, row_top - 10, label,
                ha="center", va="center", fontsize=9, fontweight="bold", color=WHITE)

    # Data rows
    items = [
        ("JS-rendered prices",     True,  False),
        ("Product images",         True,  True),
        ("Static HTML text",       True,  True),
        ("JSON-LD schema fields",  False, True),
        ("Real-time availability", False, True),
        ("GTIN / SKU in schema",   False, True),
        ("Blocked bot in robots.txt", True, False),
        ("Page load > 3 s",        True,  "slow"),
    ]

    row_h = 24
    start_y = row_top - 34

    for j, (label, human_ok, agent_ok) in enumerate(items):
        y = start_y - j * row_h
        bg = "#f7f9fb" if j % 2 == 0 else WHITE

        # Row background
        rect = plt.Rectangle((2, y - row_h + 6), W - 4, row_h,
                               facecolor=bg, edgecolor="none")
        ax.add_patch(rect)

        # Label (center)
        ax.text(W / 2, y - row_h / 2 + 6, label,
                ha="center", va="center", fontsize=8, color=DARK)

        # Human column check
        h_sym = "✓" if human_ok is True else ("~" if human_ok == "slow" else "✗")
        h_col = GREEN if human_ok is True else (ORANGE if human_ok == "slow" else RED)
        ax.text(col_centers[0], y - row_h / 2 + 6, h_sym,
                ha="center", va="center", fontsize=11, color=h_col, fontweight="bold")

        # Agent column check
        a_sym = "✓" if agent_ok is True else ("~" if agent_ok == "slow" else "✗")
        a_col = GREEN if agent_ok is True else (ORANGE if agent_ok == "slow" else RED)
        ax.text(col_centers[1], y - row_h / 2 + 6, a_sym,
                ha="center", va="center", fontsize=11, color=a_col, fontweight="bold")

    # Vertical divider
    ax.axvline(x=W / 2, ymin=0.04, ymax=0.86, color="#dde0e6", linewidth=1)

    # Legend
    for sym, col, label in [("✓", GREEN, "visible / passes"), ("✗", RED, "invisible / fails"), ("~", ORANGE, "partial")]:
        pass  # skip legend to save space

    # Footer
    ax.text(W / 2, 8, "Source: virtina.com | Data: 2026",
            ha="center", va="bottom", fontsize=6, color="#aaaaaa")

    raw = fig_to_jpeg(fig, W, H, quality=82)
    plt.close(fig)
    print(f"  Generated: {len(raw)//1024}KB")

    filename = "ecommerce-ai-agent-vs-human-product-page.jpg"
    alt = (
        "Side-by-side comparison showing what a human shopper vs an AI shopping agent "
        "can read on an ecommerce product page, highlighting JS-rendered prices, schema fields, and GTIN"
    )
    media = upload_wp(raw, filename, alt)
    if media:
        return {
            "key": "body1",
            "media_id": media["id"],
            "src": media.get("source_url", ""),
            "alt": alt,
            "filename": filename,
            "dimensions": "670x352",
            "pexels_id": None,
            "file_size_kb": round(len(raw) / 1024, 1),
        }
    return None


# ── Body 2 infographic: Schema.org Product required fields ────────────────────
def build_body2_infographic():
    """
    Schema.org Product: required fields for AI shopping agent visibility.
    Grouped into 3 categories with field names and AI agent outcome.
    670 × 352 px
    """
    print("\n=== Body 2 infographic: Schema.org Product fields (670x352) ===")

    DPI = 96
    W, H = 670, 352
    fig, ax = plt.subplots(figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    # Title
    ax.text(W / 2, H - 14, "Schema.org Product: Required Fields for AI Shopping Agent Visibility",
            ha="center", va="top", fontsize=9.5, fontweight="bold", color=SLATE)
    ax.axhline(y=H - 30, xmin=0.03, xmax=0.97, color="#dde0e6", linewidth=0.8)

    # 3 groups
    groups = [
        {
            "title": "Identity",
            "color": SLATE,
            "fields": [
                ("name",    "Product title with brand + model"),
                ("sku",     "Your internal product identifier"),
                ("gtin",    "Required by Perplexity Shopping"),
                ("brand",   "Manufacturer name"),
            ],
        },
        {
            "title": "Pricing & Stock",
            "color": TEAL,
            "fields": [
                ("price",          "Static HTML — not JS-rendered"),
                ("priceCurrency",  "ISO 4217 code, e.g. USD"),
                ("availability",   "schema.org/InStock or OutOfStock"),
                ("OfferShipping\nDetails", "Estimated delivery info"),
            ],
        },
        {
            "title": "Trust Signals",
            "color": "#e67e22",
            "fields": [
                ("image",           "High-res product photo URL"),
                ("aggregateRating", "Review count + avg score"),
                ("returnPolicy",    "hasMerchantReturnPolicy"),
                ("ProductGroup",    "For variant products"),
            ],
        },
    ]

    col_w = W / 3
    row_top = H - 44
    field_h = 22

    for gi, grp in enumerate(groups):
        cx = gi * col_w + col_w / 2
        # Group header
        box = FancyBboxPatch((gi * col_w + 4, row_top - 20), col_w - 8, 22,
                              boxstyle="round,pad=3",
                              facecolor=grp["color"], edgecolor="none")
        ax.add_patch(box)
        ax.text(cx, row_top - 9, grp["title"],
                ha="center", va="center", fontsize=9, fontweight="bold", color=WHITE)

        for fi, (fname, fdesc) in enumerate(grp["fields"]):
            fy = row_top - 34 - fi * field_h
            # Alternating row bg
            bg = "#f0f8ff" if fi % 2 == 0 else WHITE
            rect = plt.Rectangle((gi * col_w + 4, fy - field_h + 6), col_w - 8, field_h,
                                   facecolor=bg, edgecolor="none")
            ax.add_patch(rect)

            # Field name (bold, colored)
            ax.text(gi * col_w + 10, fy - field_h / 2 + 6 + 3,
                    fname,
                    ha="left", va="center",
                    fontsize=7.5, fontweight="bold", color=grp["color"],
                    fontfamily="monospace")
            # Field description
            ax.text(gi * col_w + 10, fy - field_h / 2 + 6 - 5,
                    fdesc,
                    ha="left", va="center",
                    fontsize=6.5, color="#555555")

        # Vertical divider (after first two columns)
        if gi < 2:
            ax.axvline(x=(gi + 1) * col_w, ymin=0.06, ymax=0.86,
                       color="#dde0e6", linewidth=0.8)

    # Footer note
    ax.text(W / 2, 10, "JSON-LD format, server-side rendered in <head>  |  virtina.com  |  schema.org/Product",
            ha="center", va="bottom", fontsize=6, color="#aaaaaa")

    raw = fig_to_jpeg(fig, W, H, quality=82)
    plt.close(fig)
    print(f"  Generated: {len(raw)//1024}KB")

    filename = "ecommerce-schema-product-fields-ai-agents.jpg"
    alt = (
        "Schema.org Product required fields for AI shopping agent visibility, "
        "grouped into Identity (name, sku, gtin, brand), Pricing and Stock (price, availability, shipping), "
        "and Trust Signals (image, aggregateRating, returnPolicy)"
    )
    media = upload_wp(raw, filename, alt)
    if media:
        return {
            "key": "body2",
            "media_id": media["id"],
            "src": media.get("source_url", ""),
            "alt": alt,
            "filename": filename,
            "dimensions": "670x352",
            "pexels_id": None,
            "file_size_kb": round(len(raw) / 1024, 1),
        }
    return None


# ── Update WordPress post ─────────────────────────────────────────────────────
def update_wp_post(post_id, new_img):
    """Replace image references in the post content and update featured_media."""
    print(f"\n=== Updating WP post {post_id} ===")

    # Load current post
    r = SESS.get(f"{WP_POSTS_EP}/{post_id}",
                 headers={"Authorization": AUTH_HEADER},
                 timeout=30)
    if r.status_code != 200:
        print(f"  ERROR fetching post: {r.status_code}")
        return False

    post = r.json()
    content = post.get("content", {}).get("raw", "") or post.get("content", {}).get("rendered", "")

    if not content:
        print("  WARNING: could not get raw content — will only update featured_media and meta")

    old = json.load(open(RESULTS_FILE, encoding="utf-8"))

    updated_content = content
    replacements = 0
    for key in ("featured", "body1", "body2"):
        old_src = old[key]["src"]
        new_src = new_img[key]["src"]
        old_id  = str(old[key]["media_id"])
        new_id  = str(new_img[key]["media_id"])
        old_alt = old[key]["alt"]
        new_alt = new_img[key]["alt"]

        if old_src in updated_content:
            updated_content = updated_content.replace(old_src, new_src)
            replacements += 1
            print(f"  Replaced src for {key}")
        if old_id in updated_content:
            updated_content = updated_content.replace(f'data-id="{old_id}"', f'data-id="{new_id}"')
            replacements += 1

    payload = {
        "featured_media": new_img["featured"]["media_id"],
    }
    if updated_content and replacements > 0:
        payload["content"] = updated_content

    r2 = SESS.post(f"{WP_POSTS_EP}/{post_id}",
                   headers={"Authorization": AUTH_HEADER, "Content-Type": "application/json"},
                   json=payload, timeout=60)
    if r2.status_code in (200, 201):
        print(f"  Post {post_id} updated OK (featured_media={new_img['featured']['media_id']})")
        return True
    else:
        print(f"  Post update failed {r2.status_code}: {r2.text[:300]}")
        return False


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=== Agent-Ready Image Replacement (v2) ===")
    print(f"WP user: {WP_USERNAME}")

    results = {}

    # 1. Featured
    feat = get_featured()
    if not feat:
        print("FATAL: featured image failed"); sys.exit(1)
    results["featured"] = feat
    time.sleep(1)

    # 2. Body1 infographic
    b1 = build_body1_infographic()
    if not b1:
        print("FATAL: body1 infographic failed"); sys.exit(1)
    results["body1"] = b1
    time.sleep(1)

    # 3. Body2 infographic
    b2 = build_body2_infographic()
    if not b2:
        print("FATAL: body2 infographic failed"); sys.exit(1)
    results["body2"] = b2
    time.sleep(1)

    # 4. Update WP post content
    update_wp_post(POST_ID, results)

    # 5. Save new results
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved: {RESULTS_FILE}")

    print("\n=== SUMMARY ===")
    for key, r in results.items():
        print(f"  {key:10s} | media_id={r['media_id']} | {r['dimensions']} | {r['file_size_kb']}KB | {(r['src'] or '')[:70]}")

    print("\nDone. Check WP draft preview to verify images match section context.")


if __name__ == "__main__":
    main()
