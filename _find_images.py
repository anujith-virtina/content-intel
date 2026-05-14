"""
Search Openverse for high-quality smiling professional images.
Priority: rawpixel > stocksnap > nappy sources (all CC0 / commercial-use).
Min source width: 2000px for featured, 1400px for body images.
Download, crop-resize to exact pixel targets, upload to WP, patch post.
"""
import requests, base64, io, json, time
import urllib3
from PIL import Image
urllib3.disable_warnings()

# ── WP AUTH ──────────────────────────────────────────────────────────────────
creds = base64.b64encode(b'anujith:Mibz 1h3E jWRi bfJs WAXZ rwrM').decode()
WP_H = {'Authorization': f'Basic {creds}'}

# ── OPENVERSE SEARCH ─────────────────────────────────────────────────────────
OV_BASE = 'https://api.openverse.org/v1/images/'

def search_ov(query, min_w=1400, sources='rawpixel,stocksnap,nappy', n=30):
    params = {
        'q': query,
        'license_type': 'commercial',
        'page_size': n,
    }
    if sources:
        params['source'] = sources
    try:
        r = requests.get(OV_BASE, params=params, timeout=15)
        hits = r.json().get('results', [])
    except Exception as e:
        print(f'  OV search error: {e}')
        return []
    good = [h for h in hits if (h.get('width') or 0) >= min_w]
    return good

def best_hit(results):
    """Return result with largest width."""
    if not results:
        return None
    return max(results, key=lambda h: (h.get('width') or 0))

# ── DOWNLOAD ─────────────────────────────────────────────────────────────────
def download_img(url, timeout=20):
    try:
        r = requests.get(url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200 and len(r.content) > 10000:
            img = Image.open(io.BytesIO(r.content)).convert('RGB')
            return img, r.content
    except Exception as e:
        print(f'  Download error {url[:60]}: {e}')
    return None, None

# ── CROP-RESIZE (centre crop to target aspect, then resize) ──────────────────
def crop_resize(img, target_w, target_h, quality=85):
    src_w, src_h = img.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:          # source is wider → crop sides
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, src_h))
    else:                                  # source is taller → crop top/bottom
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        img = img.crop((0, top, src_w, top + new_h))

    img = img.resize((target_w, target_h), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=quality, optimize=True)
    buf.seek(0)
    return buf

# ── WP UPLOAD ────────────────────────────────────────────────────────────────
def wp_upload(buf, filename, alt_text, title):
    upload_h = dict(WP_H)
    upload_h['Content-Disposition'] = f'attachment; filename="{filename}"'
    upload_h['Content-Type'] = 'image/jpeg'
    r = requests.post(
        'https://virtina.com/wp-json/wp/v2/media',
        headers=upload_h,
        data=buf.getvalue(),
        verify=False,
        timeout=60
    )
    if r.status_code not in [200, 201]:
        print(f'  Upload failed {r.status_code}: {r.text[:200]}')
        return None
    mid = r.json()['id']
    # Set alt text
    requests.post(
        f'https://virtina.com/wp-json/wp/v2/media/{mid}',
        headers={**WP_H, 'Content-Type': 'application/json'},
        json={'alt_text': alt_text, 'title': title},
        verify=False, timeout=20
    )
    url = r.json().get('source_url','')
    sz  = r.json().get('media_details',{}).get('filesize',0)
    print(f'  Uploaded: ID={mid}  {sz//1024}KB  {url.split("/")[-1]}')
    return mid

# ══════════════════════════════════════════════════════════════════════════════
# IMAGE SLOTS
# ══════════════════════════════════════════════════════════════════════════════
slots = [
    {
        'name'    : 'featured',
        'tw': 1309, 'th': 500,
        'min_w'   : 2000,
        'filename': 'volusion-migration-featured-1309x500.jpg',
        'alt'     : 'Smiling business professional reviewing WooCommerce eCommerce dashboard on laptop after successful Volusion migration',
        'title'   : 'Volusion to WooCommerce migration success — business professional',
        'queries' : [
            'smiling businessman laptop office',
            'happy business professional computer desk',
            'confident business man laptop smiling',
            'professional entrepreneur laptop smile',
        ],
    },
    {
        'name'    : 'section1',
        'tw': 670, 'th': 352,
        'min_w'   : 1400,
        'filename': 'volusion-migration-section1-670x352.jpg',
        'alt'     : 'Business professional reviewing eCommerce billing costs on computer screen, evaluating platform migration options for online store',
        'title'   : 'eCommerce merchant reviewing platform billing — Volusion migration',
        'queries' : [
            'business professional computer screen focused',
            'man working laptop office professional',
            'business owner reviewing computer data',
            'professional man working computer desk office',
        ],
    },
    {
        'name'    : 'section2',
        'tw': 670, 'th': 352,
        'min_w'   : 1400,
        'filename': 'volusion-migration-section2-670x352.jpg',
        'alt'     : 'Business team planning eCommerce platform migration strategy in office meeting, discussing WooCommerce transition steps on whiteboard',
        'title'   : 'Business team planning eCommerce platform migration — WooCommerce',
        'queries' : [
            'business team meeting office planning',
            'business people meeting discussion office',
            'team strategy meeting whiteboard office',
            'business colleagues discussion planning',
        ],
    },
    {
        'name'    : 'section3',
        'tw': 670, 'th': 352,
        'min_w'   : 1400,
        'filename': 'volusion-migration-section3-670x352.jpg',
        'alt'     : 'Happy smiling business owner reviewing eCommerce analytics and sales growth on laptop after successful WooCommerce migration from Volusion',
        'title'   : 'Smiling business owner reviewing WooCommerce analytics after Volusion migration',
        'queries' : [
            'smiling business owner laptop success',
            'happy entrepreneur laptop analytics',
            'smiling professional business laptop',
            'business woman man smiling laptop success',
        ],
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# FIND + PROCESS + UPLOAD
# ══════════════════════════════════════════════════════════════════════════════
results = {}

for slot in slots:
    print(f'\n── {slot["name"].upper()} ({slot["tw"]}x{slot["th"]}) ──')
    found = None

    for q in slot['queries']:
        print(f'  Searching: "{q}"')
        hits = search_ov(q, min_w=slot['min_w'])
        if hits:
            hit = best_hit(hits)
            print(f'  Found: {hit["width"]}x{hit.get("height","?")}px  {hit["url"][:70]}')
            img, raw = download_img(hit['url'])
            if img:
                print(f'  Downloaded: {img.size[0]}x{img.size[1]}px  {len(raw)//1024}KB')
                buf = crop_resize(img, slot['tw'], slot['th'])
                kb = len(buf.getvalue()) // 1024
                print(f'  Resized to: {slot["tw"]}x{slot["th"]}  {kb}KB')
                mid = wp_upload(buf, slot['filename'], slot['alt'], slot['title'])
                if mid:
                    results[slot['name']] = mid
                    found = True
                    break
        time.sleep(0.5)

    if not found:
        print(f'  FAILED: no suitable image found for {slot["name"]}')

print('\n── RESULTS ──')
print(json.dumps(results, indent=2))

# ── PATCH POST WITH NEW MEDIA IDs ────────────────────────────────────────────
if len(results) == 4:
    print('\nPatching post 42177 with new image IDs...')

    import re

    # Get current content
    r = requests.get('https://virtina.com/wp-json/wp/v2/posts/42177?context=edit',
                     headers=WP_H, verify=False, timeout=30)
    content = r.json()['content']['raw']

    # Map old media IDs to new ones
    old_new = {
        42178: results['featured'],
        42179: results['section1'],
        42180: results['section2'],
        42181: results['section3'],
    }
    for old, new in old_new.items():
        content = content.replace(f'wp-image-{old}', f'wp-image-{new}')
        content = content.replace(f'data-image-id="{old}"', f'data-image-id="{new}"')
        content = content.replace(f'data-id="{old}"', f'data-id="{new}"')

    # Replace image src URLs (keep same filenames but new upload paths may differ)
    # Actually safer to replace by media ID and let WP resolve — patch media src directly
    # Fetch new source URLs
    src_map = {}
    for name, mid in results.items():
        mr = requests.get(f'https://virtina.com/wp-json/wp/v2/media/{mid}',
                          headers=WP_H, verify=False, timeout=15)
        src_map[name] = mr.json().get('source_url', '')

    # Replace image src URLs
    old_srcs = {
        'featured': 'volusion-woocommerce-migration-featured-1309x500-2.jpg',
        'section1': 'volusion-woocommerce-migration-section1-670x352-2.jpg',
        'section2': 'volusion-woocommerce-migration-section2-670x352-2.jpg',
        'section3': 'volusion-woocommerce-migration-section3-670x352-2.jpg',
    }
    for name, old_fn in old_srcs.items():
        new_src = src_map.get(name, '')
        if new_src:
            content = re.sub(
                r'src="https://virtina\.com/wp-content/uploads/[^"]*' + re.escape(old_fn) + r'"',
                f'src="{new_src}"',
                content
            )

    payload = {
        'content': content,
        'featured_media': results['featured'],
        'status': 'draft'
    }
    pr = requests.post('https://virtina.com/wp-json/wp/v2/posts/42177',
                       headers={**WP_H, 'Content-Type': 'application/json'},
                       json=payload, verify=False, timeout=60)
    print(f'Post patch: {pr.status_code} | featured_media={pr.json().get("featured_media")}')
else:
    print(f'\nOnly {len(results)}/4 images found. Post not patched.')
    print('Missing:', [s["name"] for s in slots if s["name"] not in results])
