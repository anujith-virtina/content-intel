"""
Replace ChatSKU post 215 images with genuinely content-relevant photos.

Visual story for each slot:
  Featured  — Person at laptop/desk with documents or catalog materials visible.
              Represents the PDF-catalog problem: paper meets digital.
              Target: business professional + documents/laptop, professional setting.

  Body 1    — Someone viewing or browsing a digital product list / ecommerce interface
              on a computer screen. Represents the "options to make catalog searchable."
              Target: screen showing products, or person using laptop to search items.

  Body 2    — Organized data, spreadsheets, or product information on a screen.
              Represents the "clean up your data" section.
              Target: spreadsheet/data visible on screen, or organized product files.

Source strategy:
  1. Wikimedia Commons search API — filter by filename relevance, pick large landscape
  2. Download, inspect dimensions, crop-resize to 860x452
  3. Upload to chatsku.com, set alt text + title
  4. Patch post 215 with new image IDs and update featured_media
"""

import json, ssl, urllib.request, urllib.parse, urllib.error
import base64, os, io, re, sys
from PIL import Image

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

UN = os.environ.get('CHATSKU_WP_USERNAME', '')
PW = os.environ.get('CHATSKU_WP_APP_PASSWORD', '')
if not UN or not PW:
    sys.exit('Missing CHATSKU credentials')

creds = base64.b64encode(f'{UN}:{PW}'.encode()).decode()
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
WP_H = {
    'Authorization': f'Basic {creds}',
    'User-Agent': UA,
    'Content-Type': 'application/json',
}
DL_H = {'User-Agent': UA}

TW, TH = 860, 452

def wm_search(query, min_w=1200):
    """Search Wikimedia Commons, return list of (title, url) sorted by image width desc."""
    enc = urllib.parse.quote(query)
    api = (f'https://commons.wikimedia.org/w/api.php'
           f'?action=query&generator=search&gsrnamespace=6&gsrsearch={enc}'
           f'&gsrlimit=20&prop=imageinfo&iiprop=url|size|mime|canonicaltitle'
           f'&iiurlwidth=800&format=json')
    req = urllib.request.Request(api, headers=DL_H)
    try:
        with urllib.request.urlopen(req, timeout=20, context=SSL_CTX) as r:
            data = json.loads(r.read())
    except Exception as e:
        print(f'  Wikimedia search error: {e}')
        return []
    pages = data.get('query', {}).get('pages', {})
    results = []
    for p in pages.values():
        ii = p.get('imageinfo', [{}])[0]
        mime = ii.get('mime', '')
        if 'jpeg' not in mime and 'jpg' not in mime.lower():
            continue
        w = ii.get('width', 0)
        h = ii.get('height', 0)
        if w < min_w:
            continue
        # Prefer landscape
        if h > w:
            continue
        url = ii.get('url', '')
        title = p.get('title', '')
        results.append((title, url, w, h))
    # Sort by width descending
    results.sort(key=lambda x: -x[2])
    return results

def score_relevance(title, keywords):
    """Score how many keywords appear in the title (case-insensitive)."""
    t = title.lower()
    return sum(1 for kw in keywords if kw in t)

def pick_best(candidates, keywords, label):
    """Pick the highest-scoring candidate or fall back to first large result."""
    scored = [(score_relevance(t, keywords), t, url, w, h) for t, url, w, h in candidates]
    scored.sort(key=lambda x: -x[0])
    print(f'  Top candidates for {label}:')
    for score, t, url, w, h in scored[:5]:
        print(f'    score={score} {w}x{h}  {t}')
    if not scored:
        return None, None
    best = scored[0]
    return best[2], best[1]  # url, title

def download(url, min_kb=50):
    req = urllib.request.Request(url, headers=DL_H)
    try:
        with urllib.request.urlopen(req, timeout=60, context=SSL_CTX) as r:
            data = r.read()
    except Exception as e:
        print(f'  Download failed: {e}')
        return None
    if len(data) < min_kb * 1024:
        print(f'  Too small: {len(data)//1024}KB')
        return None
    try:
        img = Image.open(io.BytesIO(data)).convert('RGB')
        print(f'  Downloaded: {img.size[0]}x{img.size[1]}  {len(data)//1024}KB')
        return img
    except Exception as e:
        print(f'  Image open failed: {e}')
        return None

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
    img.save(buf, 'JPEG', quality=82, optimize=True)
    buf.seek(0)
    return buf

def wp_upload(buf, filename, alt, title_txt):
    h = {**WP_H,
         'Content-Disposition': f'attachment; filename="{filename}"',
         'Content-Type': 'image/jpeg'}
    del h['Content-Type']
    h['Content-Type'] = 'image/jpeg'
    req = urllib.request.Request(
        'https://chatsku.com/wp-json/wp/v2/media',
        data=buf.getvalue(),
        headers={
            'Authorization': WP_H['Authorization'],
            'User-Agent': UA,
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Content-Type': 'image/jpeg',
        },
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=90, context=SSL_CTX) as r:
            d = json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:200]
        print(f'  Upload failed {e.code}: {body}')
        return None, ''
    mid = d['id']
    src = d.get('source_url', '')
    print(f'  Uploaded ID={mid}  {src.split("/")[-1]}')
    # Set alt + title
    patch_data = json.dumps({'alt_text': alt, 'title': title_txt}).encode()
    patch_req = urllib.request.Request(
        f'https://chatsku.com/wp-json/wp/v2/media/{mid}',
        data=patch_data,
        headers={
            'Authorization': WP_H['Authorization'],
            'User-Agent': UA,
            'Content-Type': 'application/json',
        },
        method='POST'
    )
    try:
        with urllib.request.urlopen(patch_req, timeout=20, context=SSL_CTX) as r:
            r.read()
        print(f'  Alt text set OK')
    except Exception as e:
        print(f'  Alt text warning: {e}')
    return mid, src


# ── IMAGE SLOTS ───────────────────────────────────────────────────────────────

slots = [
    {
        'label': 'featured',
        'filename': 'chatsku-pdf-catalog-featured-v2.jpg',
        'alt': ('Business professional at laptop reviewing product catalog documents, '
                'representing B2B manufacturers who need to convert PDF catalogs into '
                'searchable digital experiences for their buyers'),
        'title': 'Business professional reviewing product catalog at laptop',
        # Visual story: person at desk, laptop + documents/catalog visible
        # Searches ordered most-specific to fallback
        'searches': [
            ('business professional laptop catalog documents desk', ['catalog', 'document', 'laptop', 'professional', 'business']),
            ('business person reviewing documents desk office', ['document', 'review', 'desk', 'business', 'office']),
            ('manufacturer office laptop product review', ['product', 'office', 'laptop', 'manufacturer']),
            ('business laptop paperwork desk', ['laptop', 'desk', 'business', 'paper']),
        ],
    },
    {
        'label': 'body1',
        'filename': 'chatsku-pdf-catalog-body1-v2.jpg',
        'alt': ('B2B buyer browsing a digital product catalog on a laptop screen, '
                'representing the searchable catalog experience that replaces scrolling '
                'through a static PDF to find product specifications'),
        'title': 'B2B buyer browsing digital product catalog on laptop',
        # Visual story: screen showing products or ecommerce/catalog interface, person searching
        'searches': [
            ('ecommerce online shopping laptop screen products', ['ecommerce', 'online', 'shopping', 'product', 'screen']),
            ('person laptop computer screen browsing online', ['laptop', 'screen', 'browsing', 'online', 'computer']),
            ('business buyer laptop product search online', ['laptop', 'search', 'product', 'online', 'buyer']),
            ('office worker computer typing search', ['computer', 'typing', 'office', 'worker', 'search']),
        ],
    },
    {
        'label': 'body2',
        'filename': 'chatsku-pdf-catalog-body2-v2.jpg',
        'alt': ('Organized spreadsheet or product data on a computer screen, '
                'representing the process of cleaning up and structuring product catalog '
                'data before making it searchable for B2B buyers'),
        'title': 'Product data spreadsheet on computer screen representing catalog data cleanup',
        # Visual story: spreadsheet or organized product data visible on screen
        'searches': [
            ('spreadsheet data computer screen office', ['spreadsheet', 'data', 'computer', 'screen']),
            ('business data analysis laptop office', ['data', 'analysis', 'laptop', 'business']),
            ('office computer database product list', ['database', 'product', 'office', 'computer']),
            ('person organizing files computer office', ['file', 'organize', 'computer', 'office']),
        ],
    },
]

results = {}

for slot in slots:
    print(f'\n{"="*60}')
    print(f'SLOT: {slot["label"]}')
    print(f'Visual story: {slot["alt"][:80]}...')

    img = None
    chosen_url = None
    chosen_title = ''

    for query, keywords in slot['searches']:
        print(f'\n  Wikimedia search: "{query}"')
        candidates = wm_search(query, min_w=1000)
        if not candidates:
            print('  No results, trying next query')
            continue

        url, title = pick_best(candidates, keywords, slot['label'])
        if not url:
            continue

        print(f'  Chosen: {title}')
        print(f'  URL: {url}')
        img = download(url)
        if img:
            chosen_url = url
            chosen_title = title
            break

    if not img:
        print(f'  FAILED: No usable image found for {slot["label"]}')
        continue

    buf = crop_resize(img, TW, TH)
    print(f'  Resized to {TW}x{TH}  {len(buf.getvalue())//1024}KB')

    mid, src = wp_upload(buf, slot['filename'], slot['alt'], slot['title'])
    if mid:
        results[slot['label']] = {'id': mid, 'src': src, 'wm_title': chosen_title}


print(f'\n{"="*60}')
print(f'Uploaded: {list(results.keys())}')

if len(results) < 3:
    print('Not all images uploaded — aborting post patch')
    sys.exit(1)

# ── FETCH CURRENT ELEMENTOR DATA ─────────────────────────────────────────────
print('\nFetching post 215 for patch...')
fetch_req = urllib.request.Request(
    'https://chatsku.com/wp-json/wp/v2/posts/215?context=edit',
    headers=WP_H,
)
with urllib.request.urlopen(fetch_req, timeout=30, context=SSL_CTX) as r:
    post = json.loads(r.read())

meta = post.get('meta', {})
el_data_str = meta.get('_elementor_data', '[]')
el_data = json.loads(el_data_str)

OLD_FEATURED = 212
OLD_BODY1 = 213
OLD_BODY2 = 214

NEW_FEATURED = results['featured']['id']
NEW_BODY1 = results['body1']['id']
NEW_BODY2 = results['body2']['id']
NEW_FEATURED_SRC = results['featured']['src']
NEW_BODY1_SRC = results['body1']['src']
NEW_BODY2_SRC = results['body2']['src']

print(f'Replacing: featured {OLD_FEATURED}→{NEW_FEATURED}, body1 {OLD_BODY1}→{NEW_BODY1}, body2 {OLD_BODY2}→{NEW_BODY2}')

# Update image IDs and URLs in Elementor JSON
el_str = json.dumps(el_data)
el_str = (el_str
    .replace(f'"id":{OLD_FEATURED}', f'"id":{NEW_FEATURED}')
    .replace(f'"id":{OLD_BODY1}', f'"id":{NEW_BODY1}')
    .replace(f'"id":{OLD_BODY2}', f'"id":{NEW_BODY2}')
)

# Replace src URLs
def get_old_src(mid):
    req = urllib.request.Request(
        f'https://chatsku.com/wp-json/wp/v2/media/{mid}',
        headers=WP_H
    )
    try:
        with urllib.request.urlopen(req, timeout=15, context=SSL_CTX) as r:
            return json.loads(r.read()).get('source_url', '')
    except:
        return ''

print('Fetching old src URLs...')
for old_id, new_src in [(OLD_FEATURED, NEW_FEATURED_SRC), (OLD_BODY1, NEW_BODY1_SRC), (OLD_BODY2, NEW_BODY2_SRC)]:
    old_src = get_old_src(old_id)
    if old_src:
        old_fname = old_src.split('/')[-1]
        new_fname = new_src.split('/')[-1]
        el_str = el_str.replace(old_src, new_src)
        print(f'  Replaced src {old_fname} → {new_fname}')

el_data_new = json.loads(el_str)

# Update WP content field too
wp_content = post.get('content', {}).get('raw', '')
wp_content = wp_content.replace(str(OLD_FEATURED), str(NEW_FEATURED)).replace(str(OLD_BODY1), str(NEW_BODY1)).replace(str(OLD_BODY2), str(NEW_BODY2))

# Patch the post
patch_body = json.dumps({
    'featured_media': NEW_FEATURED,
    'content': wp_content,
    'meta': {
        '_elementor_edit_mode': 'builder',
        '_elementor_template_type': 'wp-post',
        '_elementor_data': json.dumps(el_data_new),
    },
    'status': 'draft',
}).encode()

patch_req = urllib.request.Request(
    'https://chatsku.com/wp-json/wp/v2/posts/215',
    data=patch_body,
    headers=WP_H,
    method='POST',
)
with urllib.request.urlopen(patch_req, timeout=60, context=SSL_CTX) as r:
    patched = json.loads(r.read())

print(f'\nPost patch: {patched.get("status")} | featured_media={patched.get("featured_media")}')

# Clear cache
cache_req = urllib.request.Request(
    'https://chatsku.com/wp-json/elementor/v1/cache',
    headers=WP_H,
    method='DELETE'
)
try:
    with urllib.request.urlopen(cache_req, timeout=15, context=SSL_CTX) as r:
        r.read()
    print('Cache cleared')
except Exception as e:
    print(f'Cache clear: {e}')

# Delete old images
print('\nDeleting old images 212, 213, 214...')
for old_id in [OLD_FEATURED, OLD_BODY1, OLD_BODY2]:
    del_req = urllib.request.Request(
        f'https://chatsku.com/wp-json/wp/v2/media/{old_id}?force=true',
        headers=WP_H,
        method='DELETE'
    )
    try:
        with urllib.request.urlopen(del_req, timeout=15, context=SSL_CTX) as r:
            d = json.loads(r.read())
        print(f'  Deleted {old_id}: {d.get("deleted")}')
    except Exception as e:
        print(f'  Delete {old_id}: {e}')

print(f'''
DONE — New image IDs:
  featured : {NEW_FEATURED}  {results["featured"]["src"].split("/")[-1]}
  body1    : {NEW_BODY1}  {results["body1"]["src"].split("/")[-1]}
  body2    : {NEW_BODY2}  {results["body2"]["src"].split("/")[-1]}
''')
