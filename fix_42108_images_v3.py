"""
Fix post 42108 images only.
Uses Openverse filtered to source=stocksnap — modern professional CC0 stock photos.
Short queries match actual stocksnap photo titles (not academic descriptions).
"""
import sys, io, json, re, time, base64, urllib.request, urllib.parse
from PIL import Image

CREDS    = base64.b64encode(b'anujith:Mibz 1h3E jWRi bfJs WAXZ rwrM').decode()
POST_URL = 'https://virtina.com/wp-json/wp/v2/posts/42108'
MEDIA_URL = 'https://virtina.com/wp-json/wp/v2/media'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# ── fetch post ──────────────────────────────────────────────────────────────
req = urllib.request.Request(
    POST_URL + '?context=edit&_fields=content,featured_media',
    headers={'Authorization': 'Basic ' + CREDS}
)
with urllib.request.urlopen(req, timeout=30) as r:
    post = json.loads(r.read())
content = post['content']['raw']
print(f'Fetched post: {len(content)} chars')

# ── image helpers ────────────────────────────────────────────────────────────
def resize_exact(raw, w, h):
    img = Image.open(io.BytesIO(raw))
    if img.mode != 'RGB':
        img = img.convert('RGB')
    sw, sh = img.size
    scale = max(w / sw, h / sh)
    nw, nh = max(1, int(sw*scale+.5)), max(1, int(sh*scale+.5))
    img = img.resize((nw, nh), Image.LANCZOS)
    left, top = (nw-w)//2, (nh-h)//2
    img = img.crop((left, top, left+w, top+h))
    for q in [82, 75, 65]:
        buf = io.BytesIO()
        img.save(buf, 'JPEG', quality=q, optimize=True)
        if buf.tell() <= 200*1024:
            return buf.getvalue()
    return buf.getvalue()

def download(url, timeout=30):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    if len(data) < 8000:
        raise ValueError(f'Too small: {len(data)}b')
    if data[:2] not in (b'\xff\xd8',) and data[:4] != b'\x89PNG':
        raise ValueError(f'Bad signature: {data[:4].hex()}')
    return data

def upload_image(img_bytes, filename, alt):
    boundary = 'VirtinaBnd42108v3'
    body = (f'--{boundary}\r\nContent-Disposition: form-data; name="file"; '
            f'filename="{filename}"\r\nContent-Type: image/jpeg\r\n\r\n'
            ).encode() + img_bytes + f'\r\n--{boundary}--\r\n'.encode()
    req = urllib.request.Request(MEDIA_URL, data=body, method='POST', headers={
        'Authorization': 'Basic ' + CREDS,
        'Content-Type': f'multipart/form-data; boundary={boundary}',
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        m = json.loads(r.read())
    mid, murl = m['id'], m['source_url']
    # Set alt text
    data = json.dumps({'alt_text': alt}).encode('utf-8')
    req2 = urllib.request.Request(
        f'https://virtina.com/wp-json/wp/v2/media/{mid}',
        data=data, method='POST',
        headers={'Authorization': 'Basic ' + CREDS,
                 'Content-Type': 'application/json; charset=utf-8'}
    )
    urllib.request.urlopen(req2, timeout=30).close()
    print(f'  Uploaded ID={mid}  {murl.split("/")[-1]}')
    return mid, murl

# ── search: Openverse stocksnap-source only ──────────────────────────────────
def stocksnap_search(queries, seen_codes=None, limit=20):
    """
    Short, stocksnap-style queries get modern professional photos.
    Returns raw image bytes of first suitable result.
    """
    if seen_codes is None:
        seen_codes = set()

    for q in queries:
        enc = urllib.parse.quote(q)
        url = (f'https://api.openverse.org/v1/images/?'
               f'q={enc}&license=cc0,pdm&page_size={limit}'
               f'&aspect_ratio=wide&source=stocksnap')
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                results = json.loads(r.read()).get('results', [])
        except Exception as e:
            print(f'  Openverse err [{q}]: {e}')
            time.sleep(0.5)
            continue

        print(f'  [{q}] -> {len(results)} results')

        for item in results:
            img_url = item.get('url', '')
            if not img_url:
                continue
            # Extract stocksnap code from URL to deduplicate across image slots
            m = re.search(r'/img-thumbs/\d+w/([A-Z0-9]+)\.jpg', img_url)
            code = m.group(1) if m else img_url
            if code in seen_codes:
                continue
            title = (item.get('title') or '').lower()
            # Skip anything that sounds off-topic or low-quality
            if any(w in title for w in [
                'building','depot','museum','historic','vintage','retro',
                'outdoor','nature','landscape','flower','animal','logo',
                'icon','chart','diagram','map','aerial','exterior',
                'church','monument','nasa','station','fema','disaster',
            ]):
                continue
            try:
                raw = download(img_url, 25)
                print(f'  OK {len(raw)}b: "{item.get("title","")[:50]}"')
                seen_codes.add(code)
                return raw
            except Exception as e:
                print(f'  Skip {code}: {e}')
        time.sleep(0.4)

    return None

# ── image specs — each slot has unique queries so photos don't repeat ─────────
# Keep a shared set of used codes to guarantee uniqueness across all 4 images
used_codes = set()

SPECS = [
    dict(
        kind='featured', w=1309, h=500,
        filename='woocommerce-erp-integration-featured-1309x500.jpg',
        alt='Business professional reviewing WooCommerce ERP integration dashboard on laptop in modern office, managing B2B wholesale order synchronization across manufacturer systems',
        queries=[
            'laptop office business professional',
            'woman laptop office work',
            'man laptop business desk',
            'office worker laptop desk',
        ],
    ),
    dict(
        kind='body1', w=670, h=352,
        filename='woocommerce-erp-integration-itemmaster-670x352.jpg',
        alt='Office professional working at desktop computer reviewing product data spreadsheet for WooCommerce item master synchronization and SKU catalog management across ERP systems',
        queries=[
            'macbook desk business work',
            'working typing computer desk',
            'business working computer office',
            'person computer desk office work',
        ],
    ),
    dict(
        kind='body2', w=670, h=352,
        filename='woocommerce-erp-integration-pricing-670x352.jpg',
        alt='Development team collaborating at computer workstations in open-plan office, configuring B2B pricing rules and wholesale tier integration between WooCommerce and ERP platform',
        queries=[
            'office team meeting computers',
            'team meeting business office',
            'coworkers office computer work',
            'office people working together',
        ],
    ),
    dict(
        kind='body3', w=670, h=352,
        filename='woocommerce-erp-integration-warehouse-670x352.jpg',
        alt='Operations manager at computer workstation monitoring ecommerce order fulfilment workflow with real-time ERP inventory data synced to WooCommerce B2B wholesale storefront',
        queries=[
            'office work business desk',
            'professional office computer desk',
            'business office desk laptop',
            'startup office computer work',
        ],
    ),
]

photos = {}
print('\n=== SOURCING IMAGES (stocksnap via Openverse) ===')
for spec in SPECS:
    print(f'\n[{spec["kind"]}] {spec["w"]}x{spec["h"]}')
    raw = stocksnap_search(spec['queries'], used_codes)
    if raw is None:
        print(f'ERROR: no suitable image found for {spec["kind"]}')
        sys.exit(1)
    final = resize_exact(raw, spec['w'], spec['h'])
    print(f'  Resized to {spec["w"]}x{spec["h"]}: {len(final)}b')
    mid, murl = upload_image(final, spec['filename'], spec['alt'])
    photos[spec['kind']] = {'id': mid, 'url': murl, 'alt': spec['alt']}
    time.sleep(1.0)

# ── replace image spans in post content ──────────────────────────────────────
print('\n=== REPLACING IMAGE SPANS ===')
span_re = re.compile(r'<span style="display:block;margin:20px 0;">.*?</span>', re.DOTALL)
spans = list(span_re.finditer(content))
print(f'Found {len(spans)} body image spans')

for i, kind in reversed(list(enumerate(['body1', 'body2', 'body3']))):
    if i >= len(spans):
        print(f'  WARNING: no span at index {i}')
        continue
    p = photos[kind]
    new_span = (
        f'<span style="display:block;margin:20px 0;">'
        f'<img alt="{p["alt"]}" data-id="{p["id"]}" '
        f'width="670" data-init-width="670" height="352" data-init-height="352" '
        f'title="" loading="lazy" src="{p["url"]}" '
        f'data-width="670" data-height="352" '
        f'style="aspect-ratio: auto 670 / 352;max-width:100%;"></span>'
    )
    s = spans[i]
    content = content[:s.start()] + new_span + content[s.end():]
    print(f'  Span {i+1} replaced -> ID={p["id"]}')

# ── push post ─────────────────────────────────────────────────────────────────
print('\n=== PUSHING POST 42108 ===')
payload = json.dumps({
    'content': content,
    'status': 'draft',
    'featured_media': photos['featured']['id'],
}).encode('utf-8')
req = urllib.request.Request(POST_URL, data=payload, method='PUT', headers={
    'Authorization': 'Basic ' + CREDS,
    'Content-Type': 'application/json; charset=utf-8',
})
with urllib.request.urlopen(req, timeout=60) as r:
    result = json.loads(r.read())
saved = result['content']['raw']
print(f'status={result["status"]} feat={result["featured_media"]} len={len(saved)}')

# ── verify ────────────────────────────────────────────────────────────────────
print('\n=== VERIFICATION ===')
errors = []

img_urls = re.findall(r'src="(https://virtina\.com/wp-content/uploads/[^"]+)"', saved)
print(f'Body images: {len(img_urls)}')
for u in img_urls:
    print(f'  {u.split("/")[-1]}')
if len(img_urls) < 3:
    errors.append(f'Only {len(img_urls)} body images')

fm = result['featured_media']
print(f'featured_media={fm}', 'OK' if fm else 'FAIL')
if not fm:
    errors.append('featured_media=0')

ext = re.findall(r'href="(https?://(?!virtina\.com)[^"]+)"', saved)
print(f'External links: {len(ext)}')

dbl = len(re.findall(r'<<', saved)) + len(re.findall(r'>>', saved))
print(f'Orphan <<>>: {dbl}')
if dbl:
    errors.append(f'{dbl} orphan <<>>')

toc_m = re.search(r'<ul[^>]*>.*?</ul>', saved, re.DOTALL)
if toc_m:
    t = toc_m.group()
    print(f'TOC: svg={("viewBox" in t)} important={"!important" in t} no-circ={"border-radius:50%" not in t}')

with open('new-42108-content.html', 'w', encoding='utf-8') as f:
    f.write(saved)
print('Saved -> new-42108-content.html')

if errors:
    print('\nERRORS:', errors)
    sys.exit(1)

print('\n' + '='*60)
print('ALL CHECKS PASSED')
print(f'Featured : {photos["featured"]["id"]}  {photos["featured"]["url"].split("/")[-1]}')
for n, k in enumerate(['body1','body2','body3'], 1):
    print(f'Body {n}   : {photos[k]["id"]}  {photos[k]["url"].split("/")[-1]}')
