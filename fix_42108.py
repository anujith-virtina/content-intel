"""
Fix post 42108:
1. Replace all em dashes with natural punctuation
2. Generate 3 branded images (670x352), upload to WordPress, replace placehold.co URLs
"""
import json, base64, re, io, urllib.request, urllib.parse, mimetypes

# ── Credentials ────────────────────────────────────────────────────────────────
CREDS = base64.b64encode(b'anujith:Mibz 1h3E jWRi bfJs WAXZ rwrM').decode()
POST_URL = 'https://virtina.com/wp-json/wp/v2/posts/42108'
MEDIA_URL = 'https://virtina.com/wp-json/wp/v2/media'

def wp_headers(extra=None):
    h = {'Authorization': 'Basic ' + CREDS}
    if extra:
        h.update(extra)
    return h

# ── Step 1: fetch current content ──────────────────────────────────────────────
print("Fetching post 42108...")
req = urllib.request.Request(
    POST_URL + '?context=edit&_fields=content,featured_media,status',
    headers=wp_headers()
)
with urllib.request.urlopen(req) as r:
    post = json.loads(r.read())
content = post['content']['raw']
print(f"Fetched. Length: {len(content)}")
em_count_before = content.count('—')
print(f"Em dashes before: {em_count_before}")

# ── Step 2: em dash replacements ──────────────────────────────────────────────
# Ordered from most specific to most general
replacements = [
    # Conjunction patterns — keep sentence flowing with comma
    (' — but ',     ', but '),
    (' — and ',     ', and '),
    (' — or ',      ', or '),
    (' — not ',     ', not '),
    (' — never ',   ', never '),
    (' — no ',      '. No '),
    # Clarification / explanation patterns
    (' — it’s ', ': it\'s '),
    (' — it ',      ': it '),
    (' — the ',     ': the '),
    (' — they ',    ', they '),
    (' — which ',   ', which '),
    (' — this ',    ', this '),
    (' — that ',    ', that '),
    (' — when ',    ', when '),
    (' — where ',   ', where '),
    (' — so ',      ', so '),
    (' — then ',    '. Then '),
    # Arrow replacement (pricing hierarchy line uses → already, skip)
    # Fallback: any remaining em dash with spaces
    (' — ',         ', '),
    # Em dash without spaces (rare)
    ('—',           ', '),
    # HTML entity
    ('&mdash;',          ', '),
]

fixed = content
for old, new in replacements:
    fixed = fixed.replace(old, new)

em_count_after = fixed.count('—')
print(f"Em dashes after: {em_count_after}")

# ── Step 3: generate branded images with Pillow ────────────────────────────────
try:
    from PIL import Image, ImageDraw, ImageFont
    PILLOW_OK = True
except ImportError:
    PILLOW_OK = False
    print("ERROR: Pillow not available")
    exit(1)

# Image specs
IMAGES = [
    {
        'filename': 'woocommerce-erp-integration-section-1-670x352.jpg',
        'title_line1': 'ERP Integration',
        'title_line2': 'Pre-Integration Audit',
        'subtitle': 'Item master, data mapping & sync architecture',
        'alt': 'B2B operations manager reviewing WooCommerce ERP integration failure analysis and pre-integration audit checklist for manufacturers',
    },
    {
        'filename': 'woocommerce-erp-integration-section-2-670x352.jpg',
        'title_line1': 'Data Mapping',
        'title_line2': 'Workshop',
        'subtitle': 'System-of-record decisions & field mapping documentation',
        'alt': 'Development team conducting WooCommerce ERP data mapping workshop to define system-of-record rules and field ownership for B2B integration',
    },
    {
        'filename': 'woocommerce-erp-integration-section-3-670x352.jpg',
        'title_line1': 'B2B Pricing',
        'title_line2': 'Architecture',
        'subtitle': 'ERP as the pricing engine for customer-specific rates',
        'alt': 'WooCommerce B2B checkout displaying customer-specific ERP pricing tiers for wholesale distributor and manufacturer accounts with contract rates',
    },
]

W, H = 670, 352
BG_COLOR     = (224, 242, 241)   # #e0f2f1 light teal
ACCENT_COLOR = (0, 160, 226)     # #00a0e2 Virtina blue
DARK_COLOR   = (45, 62, 80)      # #2d3e50 dark slate
MID_COLOR    = (67, 98, 127)     # #43627f Virtina slate

def make_image(spec):
    img = Image.new('RGB', (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Top accent bar
    draw.rectangle([0, 0, W, 8], fill=ACCENT_COLOR)
    # Bottom accent bar
    draw.rectangle([0, H-8, W, H], fill=ACCENT_COLOR)
    # Left accent bar
    draw.rectangle([0, 0, 8, H], fill=ACCENT_COLOR)

    # Subtle inner border
    draw.rectangle([16, 16, W-16, H-16], outline=MID_COLOR, width=1)

    # Try to use a font, fall back to default
    try:
        font_large  = ImageFont.truetype("arial.ttf", 42)
        font_medium = ImageFont.truetype("arial.ttf", 30)
        font_small  = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        font_large  = ImageFont.load_default(size=42)
        font_medium = ImageFont.load_default(size=30)
        font_small  = ImageFont.load_default(size=18)

    # Title line 1
    bbox1 = draw.textbbox((0, 0), spec['title_line1'], font=font_large)
    tw1 = bbox1[2] - bbox1[0]
    draw.text(((W - tw1) // 2, 90), spec['title_line1'], font=font_large, fill=DARK_COLOR)

    # Title line 2
    bbox2 = draw.textbbox((0, 0), spec['title_line2'], font=font_medium)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W - tw2) // 2, 148), spec['title_line2'], font=font_medium, fill=MID_COLOR)

    # Divider line
    draw.rectangle([(W//2 - 60), 195, (W//2 + 60), 197], fill=ACCENT_COLOR)

    # Subtitle
    # Word-wrap subtitle to fit within W-80 px
    words = spec['subtitle'].split()
    lines = []
    current = ''
    for word in words:
        test = (current + ' ' + word).strip()
        tb = draw.textbbox((0, 0), test, font=font_small)
        if tb[2] - tb[0] > W - 80:
            lines.append(current)
            current = word
        else:
            current = test
    if current:
        lines.append(current)

    y = 212
    for line in lines:
        tb = draw.textbbox((0, 0), line, font=font_small)
        tw = tb[2] - tb[0]
        draw.text(((W - tw) // 2, y), line, font=font_small, fill=MID_COLOR)
        y += 26

    # Virtina logo text bottom right
    logo_text = 'virtina.com'
    try:
        font_logo = ImageFont.truetype("arial.ttf", 14)
    except Exception:
        font_logo = ImageFont.load_default(size=14)
    lb = draw.textbbox((0, 0), logo_text, font=font_logo)
    draw.text((W - (lb[2]-lb[0]) - 24, H - 28), logo_text, font=font_logo, fill=MID_COLOR)

    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=85)
    buf.seek(0)
    return buf.read()

# ── Upload images and collect IDs/URLs ─────────────────────────────────────────
import email.mime.multipart
import email.mime.base

def upload_image(img_bytes, filename, alt_text):
    """Upload image bytes to WP media library, set alt text, return (id, src_url)"""
    boundary = 'VirtinaUpload12345'

    # Build multipart body manually
    body = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f'Content-Type: image/jpeg\r\n\r\n'
    ).encode('utf-8') + img_bytes + f'\r\n--{boundary}--\r\n'.encode('utf-8')

    req = urllib.request.Request(
        MEDIA_URL,
        data=body,
        headers={
            'Authorization': 'Basic ' + CREDS,
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Content-Disposition': f'attachment; filename="{filename}"',
        },
        method='POST'
    )
    with urllib.request.urlopen(req) as r:
        media = json.loads(r.read())

    media_id = media['id']
    src_url  = media['source_url']
    print(f"  Uploaded: ID={media_id}, URL={src_url}")

    # Set alt text via PATCH
    patch_payload = json.dumps({'alt_text': alt_text}).encode('utf-8')
    patch_req = urllib.request.Request(
        f'https://virtina.com/wp-json/wp/v2/media/{media_id}',
        data=patch_payload,
        headers={
            'Authorization': 'Basic ' + CREDS,
            'Content-Type': 'application/json; charset=utf-8'
        },
        method='POST'  # WP REST uses POST for updates on media
    )
    with urllib.request.urlopen(patch_req) as r:
        updated = json.loads(r.read())
    print(f"  Alt text set: {updated.get('alt_text','')[:60]}...")

    return media_id, src_url

uploaded = []
for i, spec in enumerate(IMAGES, 1):
    print(f"\nGenerating image {i}: {spec['filename']}")
    img_bytes = make_image(spec)
    print(f"  Generated {len(img_bytes)} bytes")
    media_id, src_url = upload_image(img_bytes, spec['filename'], spec['alt'])
    uploaded.append({'id': media_id, 'url': src_url, 'alt': spec['alt'], 'filename': spec['filename']})

# ── Step 4: replace placehold.co URLs and fix image markup ────────────────────
# Find all placehold.co occurrences in order
placeholder_pattern = re.compile(r'src="https://placehold\.co/670x352"')
matches = list(placeholder_pattern.finditer(fixed))
print(f"\nFound {len(matches)} placehold.co occurrences to replace")

if len(matches) != len(uploaded):
    print(f"WARNING: {len(matches)} placeholders but {len(uploaded)} uploads — mismatch!")

# Replace in order
for idx, match in enumerate(reversed(matches)):
    if idx < len(uploaded):
        u = uploaded[len(uploaded) - 1 - idx]
        new_src = f'src="{u["url"]}"'
        # Also update alt text in the same img tag
        start = match.start()
        # Find the full img tag surrounding this src
        # Go back to find the opening < of the span/img
        tag_start = fixed.rfind('<span', 0, start)
        tag_end_search = fixed.find('</span>', start)
        tag_end = tag_end_search + len('</span>') if tag_end_search != -1 else start + 300
        old_chunk = fixed[tag_start:tag_end]

        # Build the new img tag with proper markup
        new_chunk = (
            f'<span style="display:block;margin:20px 0;">'
            f'<img alt="{u["alt"]}" data-id="{u["id"]}" '
            f'width="670" data-init-width="670" height="352" data-init-height="352" '
            f'title="" loading="lazy" src="{u["url"]}" '
            f'data-width="670" data-height="352" '
            f'style="aspect-ratio: auto 670 / 352;max-width:100%;"></span>'
        )
        fixed = fixed[:tag_start] + new_chunk + fixed[tag_end:]
        print(f"  Replaced placeholder {len(matches)-idx} with media ID {u['id']}")

# ── Step 5: push updated content ──────────────────────────────────────────────
print("\nPushing updated content to WordPress...")
payload = json.dumps({
    'content': fixed,
    'status': 'draft',
    'featured_media': 42109
}).encode('utf-8')

req = urllib.request.Request(
    POST_URL,
    data=payload,
    headers={
        'Authorization': 'Basic ' + CREDS,
        'Content-Type': 'application/json; charset=utf-8'
    },
    method='PUT'
)
with urllib.request.urlopen(req) as r:
    result = json.loads(r.read())

print(f"POST status: {result['status']}")
print(f"featured_media: {result['featured_media']}")
print(f"Content length: {len(result['content']['raw'])}")

# Save fixed content locally
with open('C:/content-intel/new-42108-content.html', 'w', encoding='utf-8') as f:
    f.write(fixed)

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"Em dashes before: {em_count_before}")
print(f"Em dashes after:  {em_count_after}")
print(f"\nUploaded images:")
for u in uploaded:
    print(f"  ID {u['id']}: {u['url']}")
    print(f"    alt: {u['alt'][:80]}...")
print(f"\nContent pushed: {len(result['content']['raw'])} chars, status={result['status']}")
