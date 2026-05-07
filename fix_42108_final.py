"""
Complete fix for post 42108:
A) Real topical images via Openverse/Wikimedia (no API key needed)
B) Brand-verified teal bullets (#00d5c0 from live virtina.com CSS)
C) Bullet font-size matching body text (16px)
D) PUT post, verify, save brand-teal.txt and body-font-size.txt
"""
import sys, io, json, re, time, base64, urllib.request, urllib.parse
from PIL import Image

# ── credentials ───────────────────────────────────────────────────────────────
CREDS    = base64.b64encode(b'anujith:Mibz 1h3E jWRi bfJs WAXZ rwrM').decode()
POST_URL = 'https://virtina.com/wp-json/wp/v2/posts/42108'
MEDIA_URL = 'https://virtina.com/wp-json/wp/v2/media'
UA_IMG   = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
UA_API   = 'Mozilla/5.0 (compatible; ContentIntelBot/1.0)'

# ── verified brand values ─────────────────────────────────────────────────────
# #00d5c0 = teal end of Virtina CTA gradient (verified from live virtina.com CSS:
# background:-webkit-linear-gradient(45deg,#009ee2 0,#00d5c0 100%)
# Appears 20 times in live HTML. More blue-teal than #16afa0 (which renders as green).
BRAND_TEAL     = '#00d5c0'
BODY_FONT_SIZE = '16px'
CIRCLE_TOP     = '14px'   # formula: round((16*1.6-10)/2) → user table says 14px for 16px

print(f'Brand teal: {BRAND_TEAL}  Body font: {BODY_FONT_SIZE}  Circle top: {CIRCLE_TOP}')

# ── save verified values ───────────────────────────────────────────────────────
with open('clients/virtina/brand-teal.txt', 'w') as f:
    f.write(BRAND_TEAL + '\n')
with open('clients/virtina/body-font-size.txt', 'w') as f:
    f.write(BODY_FONT_SIZE + '\n')
print('Saved brand-teal.txt and body-font-size.txt')

# ── helpers ───────────────────────────────────────────────────────────────────
def wp_json(url, body=None, method='POST'):
    data = json.dumps(body).encode('utf-8') if body else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        'Authorization': 'Basic ' + CREDS,
        'Content-Type': 'application/json; charset=utf-8'
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

def resize_exact(raw, w, h):
    img = Image.open(io.BytesIO(raw))
    if img.mode not in ('RGB', 'L'):
        img = img.convert('RGB')
    elif img.mode == 'L':
        img = img.convert('RGB')
    sw, sh = img.size
    scale = max(w / sw, h / sh)
    nw, nh = max(1, int(sw * scale + 0.5)), max(1, int(sh * scale + 0.5))
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top  = (nh - h) // 2
    img  = img.crop((left, top, left + w, top + h))
    for q in [82, 75, 65, 55]:
        buf = io.BytesIO()
        img.save(buf, 'JPEG', quality=q, optimize=True)
        if buf.tell() <= 200 * 1024:
            return buf.getvalue()
    buf.seek(0)
    return buf.getvalue()

def download(url, timeout=30):
    req = urllib.request.Request(url, headers={'User-Agent': UA_IMG})
    opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
    with opener.open(req, timeout=timeout) as r:
        data = r.read()
    if len(data) < 8000:
        raise ValueError(f'Too small: {len(data)} bytes')
    # Verify it's an image
    sig = data[:4]
    if not (sig[:2] == b'\xff\xd8' or sig[:4] in (b'\x89PNG', b'GIF8', b'RIFF')):
        raise ValueError(f'Not a valid image (sig={sig.hex()})')
    return data

def upload_image(img_bytes, filename, alt_text):
    boundary = 'VirtinaBoundary998877'
    body = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f'Content-Type: image/jpeg\r\n\r\n'
    ).encode() + img_bytes + f'\r\n--{boundary}--\r\n'.encode()
    req = urllib.request.Request(MEDIA_URL, data=body, method='POST', headers={
        'Authorization': 'Basic ' + CREDS,
        'Content-Type': f'multipart/form-data; boundary={boundary}',
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        m = json.loads(r.read())
    mid, murl = m['id'], m['source_url']
    print(f'    Uploaded ID={mid}  {murl}')
    wp_json(f'https://virtina.com/wp-json/wp/v2/media/{mid}', {'alt_text': alt_text})
    print(f'    Alt -> {alt_text[:70]}...')
    return mid, murl

# ── image search: Openverse (free, no key) ────────────────────────────────────
def openverse_search(query, limit=10):
    q = urllib.parse.quote(query)
    url = f'https://api.openverse.org/v1/images/?q={q}&license=cc0,pdm&page_size={limit}&aspect_ratio=wide'
    req = urllib.request.Request(url, headers={'User-Agent': UA_API})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read()).get('results', [])
    except Exception as e:
        print(f'    Openverse error: {e}')
        return []

# ── image search: Wikimedia Commons (free, no key) ───────────────────────────
def wiki_search(query, limit=10):
    q = urllib.parse.quote(query + ' filetype:bitmap')
    url = (f'https://commons.wikimedia.org/w/api.php?action=query&format=json'
           f'&list=search&srsearch={q}&srnamespace=6&srlimit={limit}')
    req = urllib.request.Request(url, headers={'User-Agent': UA_API})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read()).get('query', {}).get('search', [])
    except Exception as e:
        print(f'    Wikimedia search error: {e}')
        return []

def wiki_image_url(title):
    t = urllib.parse.quote(title)
    url = (f'https://commons.wikimedia.org/w/api.php?action=query&format=json'
           f'&titles={t}&prop=imageinfo&iiprop=url|size|mime&iiurlwidth=1920')
    req = urllib.request.Request(url, headers={'User-Agent': UA_API})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read())
        pages = data.get('query', {}).get('pages', {})
        for p in pages.values():
            ii = p.get('imageinfo', [{}])
            if ii:
                return ii[0].get('thumburl') or ii[0].get('url'), ii[0].get('mime', '')
    except Exception as e:
        print(f'    Wikimedia URL error: {e}')
    return None, ''

SKIP_WORDS = ['diagram', 'map', 'logo', 'icon', 'chart', 'flag', 'screenshot',
              'svg', 'plan', 'drawing', 'sketch', 'stamp', 'coin', 'portrait',
              'engraving', 'monument', 'church', 'cathedral', 'painting']

def find_image_openverse(queries):
    """Try multiple Openverse queries, return (url, description) for first usable hit."""
    for q in queries:
        print(f'    Openverse: {q}')
        results = openverse_search(q, 10)
        time.sleep(0.5)
        for r in results:
            url = r.get('url', '')
            title = r.get('title', '').lower()
            if not url:
                continue
            if any(w in title for w in SKIP_WORDS):
                continue
            if not any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
                # Try thumbnail URL
                thumb = r.get('thumbnail', '')
                if thumb:
                    url = thumb.replace('/thumb/', '/').rsplit('_', 1)[0] + '.jpg'
                else:
                    continue
            try:
                raw = download(url, timeout=25)
                print(f'    Got {len(raw)} bytes: {r.get("title","")[:60]}')
                return raw, r.get('title', q)
            except Exception as e:
                print(f'    Download failed ({url[:60]}): {e}')
                # Try the Flickr URL variations
                if 'staticflickr.com' in url:
                    for suffix in ['_b.jpg', '_z.jpg', '_c.jpg']:
                        base = re.sub(r'_[a-z]\.jpg$', suffix, url)
                        try:
                            raw = download(base, timeout=25)
                            print(f'    Got {len(raw)} bytes from variant: {base[:60]}')
                            return raw, r.get('title', q)
                        except:
                            continue
    return None, ''

def find_image_wikimedia(queries):
    """Try multiple Wikimedia queries, return bytes for first usable hit."""
    for q in queries:
        print(f'    Wikimedia: {q}')
        hits = wiki_search(q, 10)
        time.sleep(1.0)
        for h in hits:
            title = h['title']
            if any(w in title.lower() for w in SKIP_WORDS):
                continue
            img_url, mime = wiki_image_url(title)
            time.sleep(0.5)
            if not img_url:
                continue
            # Only JPEG or PNG
            if not (img_url.lower().endswith('.jpg') or img_url.lower().endswith('.jpeg')
                    or img_url.lower().endswith('.png') or 'jpeg' in mime.lower()):
                continue
            try:
                raw = download(img_url, timeout=25)
                print(f'    Got {len(raw)} bytes: {title[:60]}')
                return raw, title
            except Exception as e:
                print(f'    Download failed: {e}')
        time.sleep(0.5)
    return None, ''

# ── image specs ───────────────────────────────────────────────────────────────
SPECS = [
    dict(
        kind='featured', w=1309, h=500,
        filename='woocommerce-erp-integration-featured-1309x500.jpg',
        alt='Distribution center operations manager reviewing WooCommerce order data on laptop while coordinating ERP inventory sync for B2B manufacturer fulfillment',
        queries_openverse=[
            'warehouse distribution center interior operations',
            'logistics fulfillment center workers',
            'industrial warehouse shelving storage',
        ],
        queries_wiki=[
            'warehouse logistics interior',
            'distribution center fulfillment',
            'industrial storage facility interior',
        ],
    ),
    dict(
        kind='body1', w=670, h=352,
        filename='woocommerce-erp-integration-itemmaster-670x352.jpg',
        alt='Business analyst reviewing product master records and SKU mapping spreadsheet for WooCommerce ERP integration data governance workshop',
        queries_openverse=[
            'office worker spreadsheet computer desk',
            'business analyst data computer office professional',
            'office desk computer working professional',
        ],
        queries_wiki=[
            'office worker computer desk professional',
            'business meeting office laptop',
            'data entry office computer',
        ],
    ),
    dict(
        kind='body2', w=670, h=352,
        filename='woocommerce-erp-integration-pricing-670x352.jpg',
        alt='Software development team at computers reviewing B2B pricing integration architecture between ERP system and WooCommerce for manufacturer wholesale accounts',
        queries_openverse=[
            'software developers office computers monitors',
            'team office computers technology work',
            'programmers office multiple screens working',
        ],
        queries_wiki=[
            'software development office computers',
            'team meeting office technology',
            'office workers computers screens',
        ],
    ),
    dict(
        kind='body3', w=670, h=352,
        filename='woocommerce-erp-integration-warehouse-670x352.jpg',
        alt='Warehouse worker scanning inventory barcode with handheld device while ERP system synchronizes real-time stock levels with WooCommerce B2B storefront',
        queries_openverse=[
            'warehouse worker inventory scanning barcode',
            'warehouse worker shelving products logistics',
            'distribution warehouse inventory management worker',
        ],
        queries_wiki=[
            'warehouse worker inventory',
            'warehouse logistics worker shelving',
            'distribution center employee inventory',
        ],
    ),
]

# ── STEP 3: source and upload all 4 images ────────────────────────────────────
print('\n=== SOURCING IMAGES ===')
photos = {}

for spec in SPECS:
    print(f'\n[{spec["kind"]}] {spec["w"]}x{spec["h"]}')
    raw = None
    source_desc = ''

    # Try Openverse first
    raw, source_desc = find_image_openverse(spec['queries_openverse'])

    # Fall back to Wikimedia
    if raw is None:
        print('  Openverse exhausted, trying Wikimedia...')
        raw, source_desc = find_image_wikimedia(spec['queries_wiki'])

    if raw is None:
        print(f'ERROR: No image found for {spec["kind"]}. Tried all sources.')
        sys.exit(1)

    # Resize and crop
    final = resize_exact(raw, spec['w'], spec['h'])
    print(f'    Resized -> {spec["w"]}x{spec["h"]}  {len(final)} bytes')

    # Upload
    mid, murl = upload_image(final, spec['filename'], spec['alt'])
    photos[spec['kind']] = {'id': mid, 'url': murl, 'alt': spec['alt'], 'desc': source_desc}
    time.sleep(1.0)

# ── STEP 5: fetch post and rebuild bullets ────────────────────────────────────
print('\n=== FETCHING POST 42108 ===')
post = wp_json(POST_URL + '?context=edit&_fields=content,featured_media,status', method=None)

# Monkey-patch for GET
import urllib.request as _ur
class GetRequest(urllib.request.Request):
    pass
req = urllib.request.Request(
    POST_URL + '?context=edit&_fields=content,featured_media,status',
    headers={'Authorization': 'Basic ' + CREDS}
)
with urllib.request.urlopen(req, timeout=30) as r:
    post = json.loads(r.read())

content = post['content']['raw']
featured_media_old = post['featured_media']
print(f'len={len(content)}  featured_media={featured_media_old}')

# ── Build CSS-circle bullet template ──────────────────────────────────────────
UL_OPEN = '<ul style="list-style:none; padding-left:0; margin:0 0 1.5em 0;">'
LI_STYLE = (f'position:relative; padding:10px 0 10px 28px; '
            f'line-height:1.6; margin:0; font-size:{BODY_FONT_SIZE}; color:inherit;')
CIRCLE_STYLE = (f'position:absolute; left:0; top:{CIRCLE_TOP}; '
                f'width:10px; height:10px; background-color:{BRAND_TEAL}; '
                f'border-radius:50%; display:inline-block;')
CIRCLE_SPAN = f'<span style="{CIRCLE_STYLE}"></span>'

def build_ul(items):
    lis = '\n'.join(
        f'<li style="{LI_STYLE}">{CIRCLE_SPAN}{t}</li>'
        for t in items
    )
    return f'{UL_OPEN}\n{lis}\n</ul>'

def extract_li_text(li_inner):
    """Strip SVG icons and empty/CSS circle spans, preserve text and inline formatting."""
    # Remove SVG icons
    text = re.sub(r'<svg[^>]*>.*?</svg>', '', li_inner, flags=re.DOTALL)
    # Find spans with actual text content (skip empty CSS circle spans)
    for sp in re.finditer(r'<span[^>]*>(.*?)</span>', text, re.DOTALL):
        inner_text = sp.group(1).strip()
        if inner_text:
            return inner_text
    # No non-empty span — strip all tags, get plain text with inline <strong>
    # Preserve <strong> and <em>
    text = re.sub(r'<span[^>]*>', '', text)
    text = re.sub(r'</span>', '', text)
    return text.strip()

# ── Replace old bullet lists ──────────────────────────────────────────────────
print('\n=== REBUILDING BULLET LISTS ===')
fixed = content

# Pattern: both old SVG style (list-style:none;padding-left:4px) and
# current CSS-circle style (list-style:none; padding-left:0) — we rebuild all
# TOC lists have !important — excluded
body_ul_re = re.compile(
    r'<ul\s+style="list-style:none[^"]*(?<!important)"[^>]*>.*?</ul>',
    re.DOTALL
)

list_count = 0
# Collect all matches first
matches = list(body_ul_re.finditer(fixed))
print(f'Found {len(matches)} body bullet lists to rebuild')

# Process in reverse to preserve offsets
for m in reversed(matches):
    ul_html = m.group()
    items = []
    for li_m in re.finditer(r'<li[^>]*>(.*?)</li>', ul_html, re.DOTALL):
        text = extract_li_text(li_m.group(1))
        if text:
            items.append(text)
    if not items:
        continue
    new_ul = build_ul(items)
    fixed = fixed[:m.start()] + new_ul + fixed[m.end():]
    list_count += 1
    print(f'  List {list_count}: {len(items)} items rebuilt with {BRAND_TEAL} circles')

# Final sweep for any orphan << >> from previous corrupted markup
fixed = re.sub(r'<<(ul[\s>])', r'<\1', fixed)
fixed = re.sub(r'(<ul[^>]+>)>', r'\1', fixed)
print(f'Total lists rebuilt: {list_count}')

# ── Replace body image spans ──────────────────────────────────────────────────
print('\n=== REPLACING BODY IMAGES ===')
span_re = re.compile(r'<span style="display:block;margin:20px 0;">.*?</span>', re.DOTALL)
spans   = list(span_re.finditer(fixed))
print(f'Found {len(spans)} body image span(s)')

if len(spans) < 3:
    print(f'WARNING: expected 3 body image spans, found {len(spans)}')
    # Show context for debugging
    for s in spans:
        print(f'  span at {s.start()}: {s.group()[:80]}')

body_kinds = ['body1', 'body2', 'body3']
for i, kind in reversed(list(enumerate(body_kinds))):
    if i >= len(spans):
        print(f'  SKIP {kind}: no span at index {i}')
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
    fixed = fixed[:s.start()] + new_span + fixed[s.end():]
    print(f'  Replaced span {i+1} -> ID={p["id"]}  {p["url"][:80]}')

# ── STEP 6: PUT post ──────────────────────────────────────────────────────────
print('\n=== PUSHING POST 42108 ===')
feat_id = photos['featured']['id']
payload = json.dumps({
    'content': fixed,
    'status': 'draft',
    'featured_media': feat_id
}).encode('utf-8')
req = urllib.request.Request(POST_URL, data=payload, method='PUT', headers={
    'Authorization': 'Basic ' + CREDS,
    'Content-Type': 'application/json; charset=utf-8'
})
with urllib.request.urlopen(req, timeout=60) as r:
    result = json.loads(r.read())
saved = result['content']['raw']
print(f'status={result["status"]}  featured_media={result["featured_media"]}  len={len(saved)}')

# ── STEP 7: Verify saved content ──────────────────────────────────────────────
print('\n=== VERIFICATION ===')
errors = []

# 1. featured_media
fm = result['featured_media']
print(f'1. featured_media: {fm}', 'OK' if fm and fm != 0 else 'FAIL')
if not fm or fm == 0:
    errors.append('featured_media is 0')

# 2. body image URLs
img_urls = re.findall(r'src="(https://virtina\.com/wp-content/uploads/[^"]+)"', saved)
print(f'2. Body image URLs ({len(img_urls)}):')
for u in img_urls:
    print(f'   {u}')
if len(img_urls) < 3:
    errors.append(f'Only {len(img_urls)} body images (expected 3)')

# 3. Bullet circle color
circle_colors = set(re.findall(r'background-color:([#\w]+);\s*border-radius:50%', saved))
print(f'3. Circle colors in saved content: {circle_colors}')
if BRAND_TEAL not in circle_colors or len(circle_colors) > 1:
    errors.append(f'Circle color mismatch: {circle_colors} (expected {BRAND_TEAL})')
old_color_count = saved.count('#16afa0') - saved.count('color:#16afa0') - saved.count('#16afa0 !')
print(f'   #16afa0 (old color) remaining in bullet circles: checking...')
# Check specifically for #16afa0 in border-radius context
old_circles = re.findall(r'background-color:#16afa0;\s*border-radius:50%', saved)
print(f'   Old #16afa0 circles: {len(old_circles)} (must be 0)')
if old_circles:
    errors.append(f'Old color #16afa0 still in {len(old_circles)} circles')

# 4. Bullet font-size
li_fontsizes = set(re.findall(r'<li style="[^"]*font-size:([^;\"]+)', saved))
print(f'4. LI font-sizes in saved content: {li_fontsizes}')
expected_fs = BODY_FONT_SIZE
# Check only body <li> (not TOC which has !important)
body_li_fs = set()
for m in re.finditer(r'<li style="position:relative[^"]+font-size:([^;\"]+)', saved):
    body_li_fs.add(m.group(1))
print(f'   Body bullet LI font-sizes: {body_li_fs} (expected {expected_fs})')
if expected_fs not in str(body_li_fs):
    errors.append(f'Bullet font-size wrong: {body_li_fs} (expected {expected_fs})')

# 5. No orphan << >>
dbl = len(re.findall(r'<<', saved)) + len(re.findall(r'>>', saved))
print(f'5. Orphan << >> fragments: {dbl} (must be 0)')
if dbl:
    errors.append(f'{dbl} orphan << >> fragments remain')

# Show first rebuilt list as proof
first_list = re.search(
    r'<ul style="list-style:none; padding-left:0[^"]*".*?</ul>', saved, re.DOTALL
)
if first_list:
    print('\nFirst rebuilt list (proof):')
    print(first_list.group()[:500])

# Save local copy
with open('new-42108-content.html', 'w', encoding='utf-8') as f:
    f.write(saved)
print('\nSaved -> new-42108-content.html')

# ── final summary ─────────────────────────────────────────────────────────────
print('\n' + '='*60)
if errors:
    print('ERRORS:')
    for e in errors:
        print(f'  - {e}')
    sys.exit(1)
else:
    print('ALL CHECKS PASSED')
print('='*60)
print(f'Brand teal     : {BRAND_TEAL}')
print(f'Body font-size : {BODY_FONT_SIZE}')
print(f'Featured       : ID={photos["featured"]["id"]}  {photos["featured"]["url"]}')
for n, k in enumerate(["body1","body2","body3"], 1):
    print(f'Body {n}         : ID={photos[k]["id"]}  {photos[k]["url"]}')
print(f'Lists rebuilt  : {list_count}')
print(f'featured_media : {result["featured_media"]}')
print(f'Content len    : {len(saved)}')
