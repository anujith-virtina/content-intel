"""
Replace all 4 Virtina volusion post images with high-quality smiling professional photos.
Uses Openverse (all sources). Min-width thresholds set per slot:
  featured  -> 1310px (target 1309x500)
  body      ->  700px (target 670x352, downscaling = no blur)
Flickr _b.jpg (1024px) is upgraded to _k.jpg (2048px) where available.
"""
import requests, base64, io, re, time
import urllib3
urllib3.disable_warnings()
from PIL import Image

creds = base64.b64encode(b'anujith:Mibz 1h3E jWRi bfJs WAXZ rwrM').decode()
WP_H = {'Authorization': f'Basic {creds}'}

# ── OPENVERSE ─────────────────────────────────────────────────────────────────
def search_ov(query, min_w=700):
    try:
        r = requests.get(
            'https://api.openverse.org/v1/images/',
            params={'q': query, 'license_type': 'commercial', 'page_size': 30},
            timeout=12, verify=False
        )
        if r.status_code != 200:
            return []
        hits = r.json().get('results', [])
        return [h for h in hits if (h.get('width') or 0) >= min_w]
    except Exception as e:
        print(f'    OV err: {e}')
        return []

def upgrade_flickr_url(url):
    """Try to get the 2048px version of a Flickr image."""
    for old, new in [('_b.jpg', '_k.jpg'), ('_b.jpg', '_h.jpg')]:
        if url.endswith(old):
            return url[:-len(old)] + new
    return url

def best_hit(hits, prefer_min_w):
    """Return widest image; prefer ones already >= prefer_min_w."""
    if not hits:
        return None
    above = [h for h in hits if (h.get('width') or 0) >= prefer_min_w]
    pool = above if above else hits
    return max(pool, key=lambda h: h.get('width') or 0)

# ── DOWNLOAD ──────────────────────────────────────────────────────────────────
def download(url, min_bytes=30000):
    for attempt_url in ([upgrade_flickr_url(url), url] if url != upgrade_flickr_url(url) else [url]):
        try:
            r = requests.get(attempt_url, timeout=25, verify=False,
                             headers={'User-Agent': 'Mozilla/5.0'})
            if r.status_code == 200 and len(r.content) >= min_bytes:
                img = Image.open(io.BytesIO(r.content)).convert('RGB')
                print(f'    Source: {img.size[0]}x{img.size[1]}  {len(r.content)//1024}KB  ({attempt_url.split("/")[-1]})')
                return img
        except Exception as e:
            print(f'    DL err {attempt_url[-30:]}: {e}')
    return None

# ── CROP-RESIZE ───────────────────────────────────────────────────────────────
def crop_resize(img, tw, th):
    sw, sh = img.size
    if sw / sh > tw / th:
        nw = int(sh * tw / th)
        img = img.crop(((sw - nw) // 2, 0, (sw - nw) // 2 + nw, sh))
    else:
        nh = int(sw * th / tw)
        img = img.crop((0, (sh - nh) // 2, sw, (sh - nh) // 2 + nh))
    img = img.resize((tw, th), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, 'JPEG', quality=85, optimize=True)
    buf.seek(0)
    return buf

# ── WP UPLOAD ─────────────────────────────────────────────────────────────────
def wp_upload(buf, filename, alt, title):
    uh = {**WP_H, 'Content-Disposition': f'attachment; filename="{filename}"',
          'Content-Type': 'image/jpeg'}
    r = requests.post('https://virtina.com/wp-json/wp/v2/media',
                      headers=uh, data=buf.getvalue(), verify=False, timeout=60)
    if r.status_code not in [200, 201]:
        print(f'    Upload FAIL {r.status_code}: {r.text[:80]}')
        return None
    d = r.json()
    mid = d['id']
    src = d.get('source_url', '')
    sz  = d.get('media_details', {}).get('filesize', 0)
    # set alt
    requests.post(f'https://virtina.com/wp-json/wp/v2/media/{mid}',
                  headers={**WP_H, 'Content-Type': 'application/json'},
                  json={'alt_text': alt, 'title': title}, verify=False, timeout=20)
    print(f'    Uploaded ID={mid}  {sz//1024}KB  {src.split("/")[-1]}')
    return mid

# ══════════════════════════════════════════════════════════════════════════════
# SLOTS
# ══════════════════════════════════════════════════════════════════════════════
slots = [
    {
        'name': 'featured', 'tw': 1309, 'th': 500, 'min_w': 1310,
        'filename': 'volusion-migration-featured-1309x500.jpg',
        'alt': 'Smiling business professional at laptop reviewing eCommerce platform options after deciding to migrate from Volusion to WooCommerce',
        'title': 'Confident business professional — Volusion to WooCommerce migration',
        'queries': [
            'smiling businessman laptop',
            'happy business man computer',
            'professional man laptop smiling office',
            'business person laptop happy',
            'entrepreneur laptop smile office',
        ],
    },
    {
        'name': 'section1', 'tw': 670, 'th': 352, 'min_w': 700,
        'filename': 'volusion-migration-section1-670x352.jpg',
        'alt': 'Business professional reviewing eCommerce billing and platform pricing on computer screen, considering Volusion migration decision',
        'title': 'Business professional reviewing eCommerce platform costs — Volusion migration',
        'queries': [
            'business professional laptop office',
            'man working laptop computer desk',
            'businessman computer focused office',
            'professional working laptop',
            'man laptop office desk work',
        ],
    },
    {
        'name': 'section2', 'tw': 670, 'th': 352, 'min_w': 700,
        'filename': 'volusion-migration-section2-670x352.jpg',
        'alt': 'Business team in office meeting discussing eCommerce platform migration strategy and planning WooCommerce transition steps',
        'title': 'Business team planning eCommerce platform migration to WooCommerce',
        'queries': [
            'business team office meeting smiling',
            'business people office discussion',
            'team meeting office professional',
            'colleagues office planning smiling',
            'business team discussion office',
        ],
    },
    {
        'name': 'section3', 'tw': 670, 'th': 352, 'min_w': 700,
        'filename': 'volusion-migration-section3-670x352.jpg',
        'alt': 'Happy smiling business owner at laptop reviewing eCommerce sales growth and analytics after successful WooCommerce migration from Volusion',
        'title': 'Smiling business owner reviewing WooCommerce growth results after Volusion migration',
        'queries': [
            'smiling business owner laptop',
            'happy entrepreneur laptop',
            'smiling woman business laptop',
            'happy business person computer',
            'person smiling laptop office',
        ],
    },
]

results = {}

for slot in slots:
    name = slot['name']
    print(f'\n{name.upper()} ({slot["tw"]}x{slot["th"]}, min_src={slot["min_w"]}px)')
    for q in slot['queries']:
        print(f'  Query: "{q}"')
        hits = search_ov(q, slot['min_w'])
        if not hits:
            print(f'    No hits >= {slot["min_w"]}px')
            time.sleep(0.8)
            continue
        hit = best_hit(hits, slot['min_w'])
        print(f'    Best: {hit["width"]}x{hit.get("height","?")}px')
        img = download(hit['url'])
        if img and img.size[0] >= slot['tw']:
            buf = crop_resize(img, slot['tw'], slot['th'])
            out_kb = len(buf.getvalue()) // 1024
            print(f'    Resized: {slot["tw"]}x{slot["th"]}  {out_kb}KB')
            mid = wp_upload(buf, slot['filename'], slot['alt'], slot['title'])
            if mid:
                results[name] = mid
                break
        time.sleep(0.8)

print(f'\nResults ({len(results)}/4): {results}')

if len(results) < 4:
    missing = [s['name'] for s in slots if s['name'] not in results]
    print(f'Missing: {missing}')
    print('Post not patched.')
else:
    # ── PATCH POST ──────────────────────────────────────────────────────────
    print('\nPatching post 42177...')
    r = requests.get('https://virtina.com/wp-json/wp/v2/posts/42177?context=edit',
                     headers=WP_H, verify=False, timeout=30)
    content = r.json()['content']['raw']

    old_ids = {'featured': 42178, 'section1': 42179, 'section2': 42180, 'section3': 42181}
    for name, old in old_ids.items():
        new = results[name]
        content = content.replace(f'wp-image-{old}', f'wp-image-{new}')
        content = content.replace(f'data-image-id="{old}"', f'data-image-id="{new}"')
        content = content.replace(f'data-id="{old}"', f'data-id="{new}"')

    # Replace src URLs
    src_map = {}
    for name, mid in results.items():
        mr = requests.get(f'https://virtina.com/wp-json/wp/v2/media/{mid}',
                          headers=WP_H, verify=False, timeout=15)
        src_map[name] = mr.json().get('source_url', '')

    old_fns = {
        'featured': r'volusion-woocommerce-migration-featured-1309x500-\d+\.jpg',
        'section1': r'volusion-woocommerce-migration-section1-670x352-\d+\.jpg',
        'section2': r'volusion-woocommerce-migration-section2-670x352-\d+\.jpg',
        'section3': r'volusion-woocommerce-migration-section3-670x352-\d+\.jpg',
    }
    for name, pattern in old_fns.items():
        new_src = src_map.get(name, '')
        if new_src:
            content = re.sub(
                r'src="https://virtina\.com/wp-content/uploads/[^"]*' + pattern + '"',
                f'src="{new_src}"',
                content
            )

    pr = requests.post(
        'https://virtina.com/wp-json/wp/v2/posts/42177',
        headers={**WP_H, 'Content-Type': 'application/json'},
        json={'content': content, 'featured_media': results['featured'], 'status': 'draft'},
        verify=False, timeout=60
    )
    d = pr.json()
    print(f'Post patch: {pr.status_code} | featured_media={d.get("featured_media")}')
    print('Done.')
