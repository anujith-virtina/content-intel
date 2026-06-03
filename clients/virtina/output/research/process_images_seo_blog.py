"""
Image processor for Virtina SEO platforms blog.
Downloads, crops, resizes to exact pixel targets, saves as JPEG quality 82.
Generates infographic with matplotlib.
"""
import os
import sys
import urllib.request
import urllib.error
import ssl
from io import BytesIO

_ssl_ctx = ssl.create_default_context()
_ssl_ctx.check_hostname = False
_ssl_ctx.verify_mode = ssl.CERT_NONE

try:
    from PIL import Image
except ImportError:
    print("Installing Pillow...")
    os.system("pip install Pillow -q")
    from PIL import Image

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
except ImportError:
    print("Installing matplotlib...")
    os.system("pip install matplotlib -q")
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np

OUT_DIR = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(OUT_DIR, exist_ok=True)

# ── image sources ──────────────────────────────────────────────────────────
IMAGES = [
    {
        "name": "featured",
        "url": "https://cdn.stocksnap.io/img-thumbs/960w/HQLFQ0FSK0.jpg",
        "width": 1309,
        "height": 500,
        "filename": "seo-platforms-featured.jpg",
        "alt": "Business professional reviewing ecommerce SEO analytics and platform performance data on laptop dashboard",
    },
    {
        "name": "body1",
        "url": "https://cdn.stocksnap.io/img-thumbs/960w/DKO3B7QNG7.jpg",
        "width": 670,
        "height": 352,
        "filename": "seo-platforms-comparison-desk.jpg",
        "alt": "Business professional at desk comparing ecommerce platform options for SEO performance and B2B requirements",
    },
    {
        "name": "body2",
        "url": "https://cdn.stocksnap.io/img-thumbs/960w/VQXYE2ZEHC.jpg",
        "width": 670,
        "height": 352,
        "filename": "seo-core-web-vitals-office-team.jpg",
        "alt": "Office team analyzing Core Web Vitals and ecommerce platform performance metrics on computer screens",
    },
    {
        "name": "body3",
        "url": "https://cdn.stocksnap.io/img-thumbs/960w/3PLFDQQZ5M.jpg",
        "width": 670,
        "height": 352,
        "filename": "seo-platform-migration-team.jpg",
        "alt": "Business team planning ecommerce platform migration strategy at whiteboard to preserve SEO equity",
    },
]

def crop_center(img, target_w, target_h):
    """Center-crop image to target aspect ratio, then resize."""
    src_w, src_h = img.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        # wider than target — crop sides
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, src_h))
    else:
        # taller than target — crop top/bottom
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        img = img.crop((0, top, src_w, top + new_h))

    return img.resize((target_w, target_h), Image.LANCZOS)

def download_and_process(item):
    print(f"  Downloading {item['name']}: {item['url']}")
    try:
        req = urllib.request.Request(item['url'], headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30, context=_ssl_ctx) as resp:
            data = resp.read()
    except Exception as e:
        print(f"  ERROR downloading {item['name']}: {e}")
        return None

    img = Image.open(BytesIO(data)).convert("RGB")
    img = crop_center(img, item['width'], item['height'])
    out_path = os.path.join(OUT_DIR, item['filename'])
    img.save(out_path, "JPEG", quality=82, optimize=True)
    size_kb = os.path.getsize(out_path) / 1024
    print(f"  Saved {item['filename']} ({item['width']}x{item['height']}, {size_kb:.0f}KB)")
    return out_path

# ── infographic ────────────────────────────────────────────────────────────
def make_infographic():
    """
    Grouped bar chart: ecommerce platform SEO benchmarks 2026.
    Shows out-of-box CWV pass rate and fully-optimized LCP (inverted scale).
    Colors: Virtina teal #16afa0 and slate #43627f.
    """
    platforms = ['Shopify', 'WooCommerce', 'BigCommerce', 'Adobe\nCommerce']
    cwv_pass = [68, 78, 52, 62]          # % out-of-box CWV pass rate
    lcp_opt = [1.65, 1.1, 2.0, 1.4]     # fully optimized LCP (seconds)

    teal = '#16afa0'
    slate = '#43627f'
    bg_teal_light = '#e8f8f7'

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.37), facecolor='white')
    fig.patch.set_facecolor('white')

    x = np.arange(len(platforms))
    bar_w = 0.5

    # Chart 1 — CWV pass rate
    bars1 = ax1.bar(x, cwv_pass, width=bar_w, color=teal, edgecolor='white', linewidth=1.5)
    ax1.set_xticks(x)
    ax1.set_xticklabels(platforms, fontsize=11, color=slate)
    ax1.set_ylim(0, 100)
    ax1.set_ylabel('Pass rate (%)', fontsize=10, color=slate)
    ax1.set_title('Core Web Vitals pass rate\n(out-of-box, 2026)', fontsize=12, color=slate, fontweight='bold', pad=10)
    ax1.set_facecolor('white')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.tick_params(colors=slate)
    for bar, val in zip(bars1, cwv_pass):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
                 f'{val}%', ha='center', va='bottom', fontsize=11, color=slate, fontweight='bold')

    # Chart 2 — Optimized LCP (lower = better)
    bars2 = ax2.bar(x, lcp_opt, width=bar_w, color=slate, edgecolor='white', linewidth=1.5)
    ax2.set_xticks(x)
    ax2.set_xticklabels(platforms, fontsize=11, color=slate)
    ax2.set_ylim(0, 3.0)
    ax2.set_ylabel('LCP (seconds, lower = better)', fontsize=10, color=slate)
    ax2.set_title('Fully optimized LCP\n(seconds, 2026 benchmarks)', fontsize=12, color=slate, fontweight='bold', pad=10)
    ax2.set_facecolor('white')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.tick_params(colors=slate)
    for bar, val in zip(bars2, lcp_opt):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.04,
                 f'{val}s', ha='center', va='bottom', fontsize=11, color=slate, fontweight='bold')

    # Add "Good" threshold line on LCP chart
    ax2.axhline(y=2.5, color=teal, linestyle='--', linewidth=1.2, alpha=0.7)
    ax2.text(len(platforms) - 0.45, 2.55, 'Google "Needs Improvement" (2.5s)', fontsize=8, color=teal, va='bottom')

    fig.suptitle('Ecommerce Platform SEO Benchmarks 2026', fontsize=14, color=slate,
                 fontweight='bold', y=1.02)

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, 'seo-platform-benchmarks-infographic.jpg')
    # Save at high res first, then resize to exact 670x352
    fig.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white', format='jpeg',
                pil_kwargs={'quality': 88, 'optimize': True})
    plt.close(fig)
    # Resize to exactly 670×352 (body image standard)
    img = Image.open(out_path).convert("RGB")
    img = crop_center(img, 670, 352)
    img.save(out_path, "JPEG", quality=88, optimize=True)
    size_kb = os.path.getsize(out_path) / 1024
    print(f"  Saved infographic: seo-platform-benchmarks-infographic.jpg ({size_kb:.0f}KB) — 670x352")
    return out_path

# ── main ───────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("=== Processing images ===")
    results = {}
    for item in IMAGES:
        path = download_and_process(item)
        results[item['name']] = {'path': path, 'alt': item['alt']}

    print("\n=== Generating infographic ===")
    infographic_path = make_infographic()
    results['infographic'] = {
        'path': infographic_path,
        'alt': 'Bar chart comparing ecommerce platform Core Web Vitals pass rates and optimized LCP scores: WooCommerce leads with 78% CWV pass rate and 1.1s LCP',
    }

    print("\n=== Summary ===")
    for k, v in results.items():
        if v['path']:
            sz = os.path.getsize(v['path']) / 1024
            print(f"  {k}: {v['path']} ({sz:.0f}KB)")
        else:
            print(f"  {k}: FAILED")
    print("\nDone.")
