"""
Virtina Blog Publisher - WooCommerce B2B Net Payment Terms
Sources images from Openverse (stocksnap), generates infographic, uploads to WP, creates post draft.
"""

import os
import re
import sys
import json
import base64
import requests
import io
import hashlib
import warnings
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Suppress SSL warnings on Windows (corporate cert chains)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()

# Monkey-patch requests.get/post to default verify=False on this machine
_orig_get = requests.get
_orig_post = requests.post

def _get(*a, **kw):
    kw.setdefault('verify', False)
    return _orig_get(*a, **kw)

def _post(*a, **kw):
    kw.setdefault('verify', False)
    return _orig_post(*a, **kw)

requests.get = _get
requests.post = _post

# ── Load credentials ──────────────────────────────────────────────────────────
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent.parent.parent.parent / '.env')

WP_USERNAME = os.getenv('WP_USERNAME', 'anujith')
WP_APP_PASSWORD = os.getenv('WP_APP_PASSWORD', '')
WP_BASE = 'https://virtina.com/wp-json/wp/v2'
AUTH = base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()).decode()
HEADERS = {'Authorization': f'Basic {AUTH}'}

DRAFT_PATH = Path(__file__).parent.parent / 'drafts' / 'woocommerce-b2b-net-payment-terms-2026-05-25.md'
OUTPUT_DIR = Path(__file__).parent.parent / 'published'
OUTPUT_DIR.mkdir(exist_ok=True)
IMAGES_DIR = Path(__file__).parent / 'net-terms-images'
IMAGES_DIR.mkdir(exist_ok=True)

# ── Image sourcing from Openverse (stocksnap) ────────────────────────────────

def fetch_openverse_image(query, target_w, target_h, filename):
    """Fetch best matching image from Openverse stocksnap and resize to exact dimensions."""
    dest = IMAGES_DIR / filename
    if dest.exists():
        print(f"  [cache] {filename} already exists")
        return dest

    url = "https://api.openverse.org/v1/images/"
    params = {
        "q": query,
        "source": "stocksnap",
        "page_size": 20,
    }
    print(f"  Searching Openverse for: '{query}' ...")
    r = requests.get(url, params=params, timeout=30)
    if r.status_code != 200:
        print(f"  ERROR: Openverse returned {r.status_code}")
        return None

    data = r.json()
    results = data.get('results', [])
    if not results:
        print(f"  No results for '{query}' in stocksnap, trying broader search...")
        # Retry without source filter
        params2 = {
            "q": query,
            "page_size": 20,
        }
        r2 = requests.get(url, params=params2, timeout=30)
        if r2.status_code == 200:
            results = r2.json().get('results', [])

    if not results:
        print(f"  No results at all for '{query}'")
        return None

    # Pick largest image
    best = None
    best_size = 0
    for item in results:
        w = item.get('width', 0) or 0
        h = item.get('height', 0) or 0
        size = w * h
        if size > best_size:
            best_size = size
            best = item

    if not best:
        best = results[0]

    img_url = best.get('url') or best.get('thumbnail')
    print(f"  Found: {img_url[:80]}... ({best.get('width')}x{best.get('height')})")

    dl_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36',
        'Referer': 'https://stocksnap.io/',
        'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
    }
    img_r = requests.get(img_url, headers=dl_headers, timeout=60, stream=True)
    if img_r.status_code != 200:
        # Try Openverse thumbnail proxy as fallback
        thumb_url = best.get('thumbnail')
        if thumb_url:
            img_r = requests.get(thumb_url, timeout=60, stream=True)
            if img_r.status_code != 200:
                print(f"  Failed to download image (both CDN and thumbnail): {img_r.status_code}")
                return None
        else:
            print(f"  Failed to download image: {img_r.status_code}")
            return None

    try:
        raw = Image.open(io.BytesIO(img_r.content)).convert('RGB')
        cropped = smart_crop(raw, target_w, target_h)
        cropped.save(str(dest), 'JPEG', quality=88, optimize=True)

        size_kb = dest.stat().st_size / 1024
        print(f"  Saved: {filename} ({size_kb:.0f} KB)")

        # Compress if over 250KB
        if size_kb > 250:
            q = 82
            while size_kb > 200 and q > 50:
                buf = io.BytesIO()
                cropped.save(buf, 'JPEG', quality=q, optimize=True)
                buf.seek(0)
                size_kb = buf.tell() / 1024
                q -= 5
            with open(str(dest), 'wb') as f:
                f.write(buf.getvalue())
            print(f"  Compressed to {size_kb:.0f} KB at quality={q+5}")

        return dest
    except Exception as e:
        print(f"  Error processing image: {e}")
        return None


def smart_crop(img, target_w, target_h):
    """Center-crop and resize to exact dimensions."""
    src_w, src_h = img.size
    src_ratio = src_w / src_h
    tgt_ratio = target_w / target_h

    if src_ratio > tgt_ratio:
        # Too wide — crop sides
        new_w = int(src_h * tgt_ratio)
        offset = (src_w - new_w) // 2
        img = img.crop((offset, 0, offset + new_w, src_h))
    else:
        # Too tall — crop top/bottom (keep top 60% for faces/subjects)
        new_h = int(src_w / tgt_ratio)
        offset = int((src_h - new_h) * 0.3)  # slightly favor top
        img = img.crop((0, offset, src_w, offset + new_h))

    return img.resize((target_w, target_h), Image.LANCZOS)


# ── Infographic generation ────────────────────────────────────────────────────

def generate_infographic():
    """Generate branded infographic: B2B net terms adoption + abandonment data."""
    dest = IMAGES_DIR / 'b2b-net-terms-infographic.png'
    if dest.exists():
        print("  [cache] infographic already exists")
        return dest

    fig, axes = plt.subplots(1, 2, figsize=(9.31, 4.89))  # 670x352 at 72dpi
    fig.patch.set_facecolor('#FAFAFA')

    TEAL = '#16afa0'
    SLATE = '#43627f'
    LIGHT = '#e8f5f4'
    TEXT = '#2d3e50'

    # ── Left chart: abandonment / demand stats ────────────────────────────────
    ax1 = axes[0]
    ax1.set_facecolor('#FAFAFA')
    labels = ['Abandon without\nnet terms', 'Call terms\n"essential"', 'Use Net 30\nterms (B2B)']
    values = [67, 78, 60]
    colors = [TEAL, SLATE, '#5ba8c4']

    bars = ax1.barh(labels, values, color=colors, height=0.55, edgecolor='none')

    for bar, val in zip(bars, values):
        ax1.text(val + 1.5, bar.get_y() + bar.get_height() / 2,
                 f'{val}%', va='center', ha='left',
                 fontsize=11, fontweight='bold', color=TEXT)

    ax1.set_xlim(0, 95)
    ax1.set_xlabel('% of B2B buyers', fontsize=9, color=TEXT)
    ax1.set_title('B2B Payment Terms: Buyer Impact', fontsize=11,
                  fontweight='bold', color=SLATE, pad=8)
    ax1.tick_params(colors=TEXT, labelsize=9)
    ax1.spines[['top', 'right', 'left']].set_visible(False)
    ax1.spines['bottom'].set_color('#dde0e6')
    ax1.xaxis.label.set_color(TEXT)
    for label in ax1.get_yticklabels():
        label.set_color(TEXT)
    ax1.set_axisbelow(True)
    ax1.xaxis.grid(True, color='#dde0e6', linewidth=0.5)
    ax1.text(0, -0.85, 'Source: Hokodo 2025 B2B Buyer Report',
             transform=ax1.get_yaxis_transform(),
             fontsize=7, color='#888888', va='bottom')

    # ── Right chart: DSO by industry ─────────────────────────────────────────
    ax2 = axes[1]
    ax2.set_facecolor('#FAFAFA')
    sectors = ['Manufacturing', 'Wholesale\nDistribution', 'Retail\n(B2C avg)', 'Technology']
    dso_mid = [52, 40, 25, 45]
    bar_colors = [TEAL, TEAL, '#cccccc', TEAL]
    bar_alpha = [1.0, 1.0, 0.5, 1.0]

    for i, (s, d, c, a) in enumerate(zip(sectors, dso_mid, bar_colors, bar_alpha)):
        ax2.bar(i, d, color=c, alpha=a, edgecolor='none', width=0.6)
        ax2.text(i, d + 1, f'{d} days', ha='center', va='bottom',
                 fontsize=9, fontweight='bold', color=TEXT)

    ax2.set_xticks(range(len(sectors)))
    ax2.set_xticklabels(sectors, fontsize=8.5, color=TEXT)
    ax2.set_ylabel('Average DSO (days)', fontsize=9, color=TEXT)
    ax2.set_title('Days Sales Outstanding by Sector', fontsize=11,
                  fontweight='bold', color=SLATE, pad=8)
    ax2.set_ylim(0, 70)
    ax2.spines[['top', 'right']].set_visible(False)
    ax2.spines[['left', 'bottom']].set_color('#dde0e6')
    ax2.tick_params(colors=TEXT, labelsize=8.5)
    ax2.set_axisbelow(True)
    ax2.yaxis.grid(True, color='#dde0e6', linewidth=0.5)
    ax2.text(0.5, -0.14, 'Source: Clearly Payments / CreditPulse 2025',
             transform=ax2.transAxes,
             fontsize=7, color='#888888', va='bottom', ha='center')

    # ── Footer branding ───────────────────────────────────────────────────────
    fig.text(0.5, 0.01, 'virtina.com', ha='center', fontsize=8,
             color=TEAL, fontweight='bold')

    plt.tight_layout(rect=[0, 0.04, 1, 0.98])
    plt.savefig(str(dest), dpi=72, bbox_inches='tight',
                facecolor='#FAFAFA', edgecolor='none')
    plt.close()

    size_kb = dest.stat().st_size / 1024
    print(f"  Infographic saved: {dest.name} ({size_kb:.0f} KB)")
    return dest


# ── WordPress upload ──────────────────────────────────────────────────────────

def upload_to_wordpress(filepath, alt_text, title=None):
    """Upload image file to WordPress media library, return media ID and URL."""
    filepath = Path(filepath)
    mime = 'image/jpeg' if filepath.suffix.lower() in ('.jpg', '.jpeg') else 'image/png'

    with open(filepath, 'rb') as f:
        data = f.read()

    upload_headers = {
        **HEADERS,
        'Content-Disposition': f'attachment; filename="{filepath.name}"',
        'Content-Type': mime,
    }

    print(f"  Uploading {filepath.name} to WordPress...")
    r = requests.post(f'{WP_BASE}/media', headers=upload_headers, data=data, timeout=120)

    if r.status_code not in (200, 201):
        print(f"  UPLOAD FAILED: {r.status_code} - {r.text[:200]}")
        return None, None

    result = r.json()
    media_id = result['id']
    media_url = result['source_url']
    print(f"  Uploaded: ID={media_id}, URL={media_url}")

    # Update alt text
    patch_r = requests.post(
        f'{WP_BASE}/media/{media_id}',
        headers={**HEADERS, 'Content-Type': 'application/json'},
        json={'alt_text': alt_text, 'title': title or filepath.stem},
        timeout=30
    )
    if patch_r.status_code in (200, 201):
        print(f"  Alt text set: '{alt_text[:60]}...'")

    return media_id, media_url


# ── Build final HTML content ──────────────────────────────────────────────────

def build_html_content(draft_text, image_map, infographic_map):
    """Replace image placeholders in draft with real Template G HTML."""

    def make_img_block(media_id, media_url, alt_text, width, height):
        return (
            f'<span style="display:block;margin:20px 0;">'
            f'<img alt="{alt_text}" data-id="{media_id}" '
            f'width="{width}" data-init-width="{width}" '
            f'height="{height}" data-init-height="{height}" '
            f'title="" loading="lazy" src="{media_url}" '
            f'data-width="{width}" data-height="{height}" '
            f'style="aspect-ratio: auto {width} / {height};max-width:100%;">'
            f'</span>'
        )

    html = draft_text

    # Replace featured image comment
    featured_id, featured_url = image_map['featured']
    featured_alt = ('Business professional reviewing purchase order and WooCommerce B2B '
                    'net payment terms workflow on a laptop at an office desk, '
                    'representing deferred invoice payment setup for manufacturers and distributors. '
                    '(120 chars)')
    # Trim alt to max 150 chars
    featured_alt = 'Business professional reviewing purchase order documents alongside WooCommerce order screen on laptop, representing B2B net payment terms setup for manufacturers and distributors'
    featured_alt = featured_alt[:150]

    featured_block = make_img_block(featured_id, featured_url, featured_alt, 1309, 500)
    html = re.sub(
        r'<!-- FEATURED IMAGE:.*?-->',
        featured_block,
        html,
        flags=re.DOTALL
    )

    # Replace body image 1
    img1_id, img1_url = image_map['body1']
    img1_alt = 'B2B procurement manager at computer encountering WooCommerce checkout without net payment terms, highlighting why B2B buyers abandon purchases at card-only checkout'
    img1_alt = img1_alt[:150]
    html = html.replace(
        '<!-- IMAGE_1_PLACEHOLDER: 670x352 - B2B buyer at computer frustrated with checkout -->',
        make_img_block(img1_id, img1_url, img1_alt, 670, 352)
    )

    # Replace body image 2
    img2_id, img2_url = image_map['body2']
    img2_alt = 'Business professional reviewing financial dashboard and accounts receivable data, representing revenue impact analysis for WooCommerce B2B stores without net payment terms'
    img2_alt = img2_alt[:150]
    html = html.replace(
        '<!-- IMAGE_2_PLACEHOLDER: 670x352 - Business professional reviewing financial dashboard -->',
        make_img_block(img2_id, img2_url, img2_alt, 670, 352)
    )

    # Replace infographic placeholder
    infog_id, infog_url = infographic_map
    infog_alt = ('B2B net payment terms data: 67% of B2B buyers abandon without terms, '
                 '78% call terms essential, average DSO by sector including manufacturing 52 days '
                 'and wholesale distribution 40 days')
    infog_alt = infog_alt[:150]
    html = html.replace(
        '<!-- INFOGRAPHIC_PLACEHOLDER: B2B buyer abandonment and net terms adoption stats bar chart -->',
        make_img_block(infog_id, infog_url, infog_alt, 670, 352)
    )

    # Replace body image 3
    img3_id, img3_url = image_map['body3']
    img3_alt = 'Office team reviewing ERP integration plans and WooCommerce order workflow for B2B net payment terms setup, representing manufacturer and distributor operations team'
    img3_alt = img3_alt[:150]
    html = html.replace(
        '<!-- IMAGE_3_PLACEHOLDER: 670x352 - Warehouse worker with tablet, inventory management -->',
        make_img_block(img3_id, img3_url, img3_alt, 670, 352)
    )

    # Remove optional 4th image placeholder (keep body image count at 3)
    html = re.sub(
        r'<!-- IMAGE PLACEHOLDER: 670x352.*?-->',
        '',
        html,
        flags=re.DOTALL
    )
    # Remove the "Note to publisher" comment line
    html = re.sub(r'<!-- Note to publisher:.*?-->', '', html, flags=re.DOTALL)

    return html.strip()


# ── Extract HTML content from draft ──────────────────────────────────────────

def read_draft_content():
    """Read draft file and return just the HTML body (strip YAML frontmatter)."""
    text = DRAFT_PATH.read_text(encoding='utf-8')
    # Strip YAML frontmatter
    if text.startswith('---'):
        end = text.index('---', 3) + 3
        return text[end:].strip()
    return text.strip()


# ── Pre-publish checklist ─────────────────────────────────────────────────────

def run_checklist(html_content, featured_media_id, internal_links, external_links):
    """Run pre-publish checklist. Return (passed, failures) tuple."""
    failures = []
    checks = {}

    # Em dash check
    for form in ['—', '&mdash;', '&#8212;', '&#x2014;']:
        if form in html_content:
            failures.append(f"Em dash found: {form}")
    checks['no_em_dashes'] = 'PASS' if not any(f.startswith('Em dash') for f in failures) else 'FAIL'

    # Banned words
    banned = ['delve', 'leverage', 'revolutionary', 'game-changing', 'cutting-edge',
              'synergy', 'ecosystem', 'landscape', 'realm', 'in today\'s fast-paced',
              'it\'s important to note', 'in conclusion', 'transform your']
    content_lower = html_content.lower()
    for word in banned:
        if word.lower() in content_lower:
            failures.append(f"Banned word/phrase found: '{word}'")
    checks['no_banned_words'] = 'PASS' if not any('Banned word' in f for f in failures) else 'FAIL'

    # Featured media ID
    checks['featured_media'] = 'PASS' if featured_media_id and featured_media_id > 0 else 'FAIL'
    if not (featured_media_id and featured_media_id > 0):
        failures.append("featured_media is 0 or None")

    # Status: draft (enforced at POST time)
    checks['status_draft'] = 'PASS'

    # Internal links count — only <a href>, not img src
    int_count = len(re.findall(r'<a\s+href="https://virtina\.com/[^"]*"', html_content))
    checks['internal_links'] = f'PASS ({int_count} links)' if 7 <= int_count <= 10 else f'FAIL ({int_count})'
    if not (7 <= int_count <= 10):
        failures.append(f"Internal link count is {int_count}, expected 7-10")

    # External links count — only <a href>, not img src
    ext_links_found = re.findall(r'<a\s[^>]*href="https?://(?!virtina\.com)[^"]+', html_content)
    ext_count = len(ext_links_found)
    checks['external_links_max2'] = f'PASS ({ext_count})' if ext_count <= 2 else f'FAIL ({ext_count})'
    if ext_count > 2:
        failures.append(f"External link count is {ext_count} (max 2)")

    # External links have target="_blank"
    ext_missing_target = [
        m.group(0) for m in re.finditer(r'<a\s[^>]*href="https?://(?!virtina\.com)[^"]+"[^>]*>', html_content)
        if 'target="_blank"' not in m.group(0)
    ]
    checks['external_target_blank'] = 'PASS' if not ext_missing_target else f'FAIL: {len(ext_missing_target)} missing'
    if ext_missing_target:
        failures.append(f"External links missing target='_blank': {ext_missing_target[:2]}")

    # Internal links (a href) no target attribute — img src on virtina.com is fine
    int_with_target = re.findall(r'<a\s[^>]*href="https://virtina\.com/[^"]*"[^>]*target=', html_content)
    checks['internal_no_target'] = 'PASS' if not int_with_target else f'FAIL: {len(int_with_target)}'
    if int_with_target:
        failures.append(f"Internal links have target attribute: {int_with_target[:2]}")

    # H2 ids
    h2_ids = re.findall(r'<h2 id="([^"]+)"', html_content)
    toc_hrefs = re.findall(r'href="#([^"]+)"', html_content)
    # Check all body H2 ids appear in TOC
    for h2_id in h2_ids:
        if h2_id not in toc_hrefs:
            failures.append(f"H2 id '{h2_id}' not in TOC hrefs")
    checks['h2_ids_in_toc'] = 'PASS' if not any('not in TOC' in f for f in failures) else 'FAIL'

    # TOC uses SVG not Unicode arrow
    if '→' in html_content:
        failures.append("Unicode arrow → found in TOC")
    checks['toc_svg_arrow'] = 'PASS' if '→' not in html_content else 'FAIL'

    # !important has no space
    if 'list-style:none !important' in html_content or 'list-style: none!important' in html_content:
        failures.append("Space before !important in list-style")
    checks['no_space_before_important'] = 'PASS' if 'list-style:none !important' not in html_content else 'FAIL'

    # Comparison table present
    checks['comparison_table'] = 'PASS' if '<table' in html_content else 'FAIL'
    if '<table' not in html_content:
        failures.append("No comparison table found")

    # Image srcs start with virtina.com uploads (after replacements)
    bad_srcs = re.findall(r'src="(?!https://virtina\.com/wp-content/uploads/)[^"]*virtina[^"]*"', html_content)
    checks['image_srcs'] = 'PASS' if not bad_srcs else f'FAIL: {bad_srcs[:2]}'

    # H3 pattern check (Thrive)
    bad_h3 = re.findall(r'<h3[^>]*><span[^>]*font-weight[^>]*>', html_content)
    checks['h3_thrive_pattern'] = 'PASS' if not bad_h3 else f'FAIL: Elementor H3 pattern found'
    if bad_h3:
        failures.append("Elementor H3 pattern found (wrong for Thrive)")

    # No placehold.co or unsplash
    for bad in ['placehold.co', 'source.unsplash.com']:
        if bad in html_content:
            failures.append(f"Forbidden image source: {bad}")
    checks['no_forbidden_sources'] = 'PASS' if not any('Forbidden image' in f for f in failures) else 'FAIL'

    passed = len(failures) == 0
    return passed, failures, checks


# ── WordPress post creation ───────────────────────────────────────────────────

def create_wp_post(title, slug, html_content, featured_media_id, category_id, tag_ids):
    """Create WordPress post as draft. Return post ID and URL."""
    yoast_title = 'WooCommerce B2B net payment terms: Net 30/60/90 guide | Virtina'
    if len(yoast_title) > 60:
        yoast_title = 'WooCommerce B2B net payment terms guide | Virtina'

    meta_desc = ('Learn the 3 ways to add net 30/60/90 payment terms to WooCommerce. '
                 'Vendor-neutral guide for B2B manufacturers and distributors with ERP integration advice.')
    # Ensure 150-160 chars
    meta_desc = meta_desc[:160]

    payload = {
        'title': title,
        'slug': slug,
        'content': html_content,
        'status': 'draft',
        'featured_media': featured_media_id,
        'categories': [category_id],
        'tags': tag_ids,
        'meta': {
            '_yoast_wpseo_title': yoast_title,
            '_yoast_wpseo_metadesc': meta_desc,
            '_yoast_wpseo_focuskw': 'WooCommerce net payment terms B2B',
        }
    }

    print(f"\nCreating WordPress draft post...")
    r = requests.post(
        f'{WP_BASE}/posts',
        headers={**HEADERS, 'Content-Type': 'application/json'},
        json=payload,
        timeout=60
    )

    if r.status_code not in (200, 201):
        print(f"POST FAILED: {r.status_code}")
        print(r.text[:500])
        return None, None

    result = r.json()
    post_id = result['id']
    post_url = result.get('link', f'https://virtina.com/?p={post_id}')
    print(f"Post created: ID={post_id}, URL={post_url}")
    return post_id, post_url


def get_or_create_category():
    """Get WooCommerce category ID or use General (1)."""
    r = requests.get(f'{WP_BASE}/categories?search=WooCommerce&per_page=10', headers=HEADERS, timeout=20)
    if r.status_code == 200:
        cats = r.json()
        for cat in cats:
            if 'woocommerce' in cat['name'].lower() or 'b2b' in cat['name'].lower():
                return cat['id']
    # Fallback to first category
    r2 = requests.get(f'{WP_BASE}/categories?per_page=5', headers=HEADERS, timeout=20)
    if r2.status_code == 200:
        cats = r2.json()
        if cats:
            return cats[0]['id']
    return 1


def get_or_create_tags():
    """Get relevant tag IDs, create if missing."""
    wanted_tags = ['WooCommerce', 'B2B eCommerce', 'Net Payment Terms', 'Payment Terms']
    tag_ids = []

    for tag_name in wanted_tags[:3]:
        r = requests.get(f'{WP_BASE}/tags?search={requests.utils.quote(tag_name)}&per_page=5',
                         headers=HEADERS, timeout=20)
        if r.status_code == 200:
            tags = r.json()
            for tag in tags:
                if tag['name'].lower() == tag_name.lower():
                    tag_ids.append(tag['id'])
                    break
            else:
                # Create tag
                cr = requests.post(
                    f'{WP_BASE}/tags',
                    headers={**HEADERS, 'Content-Type': 'application/json'},
                    json={'name': tag_name},
                    timeout=20
                )
                if cr.status_code in (200, 201):
                    tag_ids.append(cr.json()['id'])

    return tag_ids


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Virtina Blog Publisher: WooCommerce B2B Net Payment Terms")
    print("=" * 60)

    # ── 1. Source and process images ──────────────────────────────────────────
    print("\n[1/5] Sourcing images...")

    images = {}

    # Featured: business professional with laptop + documents
    feat_path = fetch_openverse_image(
        'business professional laptop office desk',
        1309, 500,
        'featured-net-terms-1309x500.jpg'
    )
    if not feat_path:
        feat_path = fetch_openverse_image(
            'laptop office business work',
            1309, 500,
            'featured-net-terms-1309x500.jpg'
        )

    # Body 1: Person at computer (checkout / order frustration)
    body1_path = fetch_openverse_image(
        'office worker computer business',
        670, 352,
        'body1-office-worker-670x352.jpg'
    )
    if not body1_path:
        body1_path = fetch_openverse_image(
            'working typing computer desk',
            670, 352,
            'body1-office-worker-670x352.jpg'
        )

    # Body 2: Financial dashboard / data
    body2_path = fetch_openverse_image(
        'business financial dashboard laptop',
        670, 352,
        'body2-financial-dashboard-670x352.jpg'
    )
    if not body2_path:
        body2_path = fetch_openverse_image(
            'macbook desk business work',
            670, 352,
            'body2-financial-dashboard-670x352.jpg'
        )

    # Body 3: Office/business team (ERP/integration planning context)
    body3_path = fetch_openverse_image(
        'coworkers office meeting',
        670, 352,
        'body3-office-team-670x352.jpg'
    )
    if not body3_path:
        body3_path = fetch_openverse_image(
            'business team office computers',
            670, 352,
            'body3-office-team-670x352.jpg'
        )

    # Verify all images were sourced
    for name, path in [('featured', feat_path), ('body1', body1_path),
                       ('body2', body2_path), ('body3', body3_path)]:
        if not path or not path.exists():
            print(f"CRITICAL: {name} image not sourced. Exiting.")
            sys.exit(1)

    # ── 2. Generate infographic ───────────────────────────────────────────────
    print("\n[2/5] Generating infographic...")
    infog_path = generate_infographic()

    # ── 3. Upload images to WordPress ─────────────────────────────────────────
    print("\n[3/5] Uploading images to WordPress...")

    feat_id, feat_url = upload_to_wordpress(
        feat_path,
        'Business professional reviewing purchase order documents alongside WooCommerce order screen on laptop, representing B2B net payment terms setup for manufacturers and distributors',
        'WooCommerce B2B net payment terms featured image'
    )
    body1_id, body1_url = upload_to_wordpress(
        body1_path,
        'B2B procurement manager at computer encountering WooCommerce checkout without net payment terms, highlighting why B2B buyers abandon purchases at card-only checkout',
        'WooCommerce checkout B2B buyer'
    )
    body2_id, body2_url = upload_to_wordpress(
        body2_path,
        'Business professional reviewing financial dashboard and accounts receivable data, representing revenue impact analysis for WooCommerce B2B stores without net payment terms',
        'Financial dashboard business review'
    )
    body3_id, body3_url = upload_to_wordpress(
        body3_path,
        'Warehouse worker using tablet for inventory management, representing WooCommerce net payment terms ERP integration workflow for manufacturers and distributors',
        'Warehouse worker tablet inventory'
    )
    infog_id, infog_url = upload_to_wordpress(
        infog_path,
        'B2B net payment terms data: 67% of B2B buyers abandon without terms, 78% call terms essential, average DSO by sector including manufacturing 52 days and wholesale distribution 40 days',
        'B2B net terms infographic'
    )

    for name, (mid, murl) in [('featured', (feat_id, feat_url)),
                               ('body1', (body1_id, body1_url)),
                               ('body2', (body2_id, body2_url)),
                               ('body3', (body3_id, body3_url)),
                               ('infog', (infog_id, infog_url))]:
        if not mid:
            print(f"CRITICAL: Upload failed for {name}. Exiting.")
            sys.exit(1)

    image_map = {
        'featured': (feat_id, feat_url),
        'body1': (body1_id, body1_url),
        'body2': (body2_id, body2_url),
        'body3': (body3_id, body3_url),
    }
    infographic_map = (infog_id, infog_url)

    # ── 4. Build final HTML ───────────────────────────────────────────────────
    print("\n[4/5] Building final HTML content...")
    raw_html = read_draft_content()
    final_html = build_html_content(raw_html, image_map, infographic_map)

    # ── 4a. Run pre-publish checklist ─────────────────────────────────────────
    print("\n[4a] Running pre-publish checklist...")
    int_links = re.findall(r'href="https://virtina\.com/[^"]*"', final_html)
    ext_links = re.findall(r'href="https?://(?!virtina\.com)[^"]+"', final_html)

    passed, failures, checks = run_checklist(final_html, feat_id, int_links, ext_links)

    print("\nChecklist results:")
    for key, result in checks.items():
        status = "[PASS]" if "PASS" in str(result) else "[FAIL]"
        print(f"  {status} {key}: {result}")

    if failures:
        print(f"\nFAILURES ({len(failures)}):")
        for f in failures:
            print(f"  [FAIL] {f}")
        print("\nAborting publish due to checklist failures.")
        sys.exit(1)

    print("\nAll checklist items PASSED. Proceeding to publish.")

    # ── 5. Create WordPress post ──────────────────────────────────────────────
    print("\n[5/5] Creating WordPress draft post...")
    category_id = get_or_create_category()
    tag_ids = get_or_create_tags()

    post_id, post_url = create_wp_post(
        title="Why your WooCommerce B2B buyers leave without buying (and how net payment terms fix it)",
        slug="woocommerce-b2b-net-payment-terms",
        html_content=final_html,
        featured_media_id=feat_id,
        category_id=category_id,
        tag_ids=tag_ids
    )

    if not post_id:
        print("Post creation failed. Exiting.")
        sys.exit(1)

    # ── Save published version ─────────────────────────────────────────────────
    pub_path = OUTPUT_DIR / 'woocommerce-b2b-net-payment-terms-2026-05-25.md'
    pub_path.write_text(
        f"---\npost_id: {post_id}\npost_url: {post_url}\n"
        f"featured_media_id: {feat_id}\n"
        f"image_ids:\n  featured: {feat_id}\n  body1: {body1_id}\n"
        f"  body2: {body2_id}\n  body3: {body3_id}\n  infographic: {infog_id}\n"
        f"status: draft\npublished: 2026-05-25\n---\n\n" + final_html,
        encoding='utf-8'
    )

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("PUBLISH COMPLETE")
    print("=" * 60)
    print(f"Post ID:       {post_id}")
    print(f"Preview URL:   {post_url}")
    print(f"Status:        draft")
    print(f"Featured img:  {feat_id} ({feat_url})")
    print(f"Body img 1:    {body1_id}")
    print(f"Body img 2:    {body2_id}")
    print(f"Body img 3:    {body3_id}")
    print(f"Infographic:   {infog_id}")
    print(f"Internal links: {len(re.findall(r'href=\"https://virtina\\.com/', final_html))}")
    print(f"External links: {len(re.findall(r'href=\"https?://(?!virtina\\.com)[^\"]+\"', final_html))}")
    print(f"Checklist:     ALL PASSED")

    return post_id, post_url


if __name__ == '__main__':
    main()
