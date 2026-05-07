"""
Fix post 42108 completely:
A) Real Unsplash photos for featured (1309x500) + 3 body (670x352)
B) Bullet lists rewritten from 42074 exact template
C) PUT all fixes, save list-template.html
"""
import json, base64, urllib.request, urllib.error, io, re, sys

from PIL import Image

CREDS    = base64.b64encode(b'anujith:Mibz 1h3E jWRi bfJs WAXZ rwrM').decode()
POST_URL = 'https://virtina.com/wp-json/wp/v2/posts/42108'
MEDIA_URL = 'https://virtina.com/wp-json/wp/v2/media'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'

# ── helpers ────────────────────────────────────────────────────────────────────
def wp_get(url):
    req = urllib.request.Request(url, headers={'Authorization': 'Basic ' + CREDS})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def wp_json_post(url, body_dict, method='POST'):
    data = json.dumps(body_dict).encode('utf-8')
    req = urllib.request.Request(url, data=data, method=method, headers={
        'Authorization': 'Basic ' + CREDS,
        'Content-Type': 'application/json; charset=utf-8'
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

def fetch_photo(url):
    """Download from URL following all redirects, return bytes."""
    opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with opener.open(req, timeout=30) as r:
        data = r.read()
    if len(data) < 5000:
        raise ValueError(f"Response too small ({len(data)} bytes) — probably not an image")
    return data

def resize_exact(img_bytes, w, h):
    """Scale-then-center-crop to exact (w, h). Return JPEG bytes under 200KB."""
    img = Image.open(io.BytesIO(img_bytes))
    if img.mode != 'RGB':
        img = img.convert('RGB')
    sw, sh = img.size
    scale = max(w / sw, h / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
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

def upload_image(img_bytes, filename, alt_text):
    """Upload bytes to WP media, set alt, return (id, url)."""
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
    print(f"    Uploaded ID={mid}  {murl}")
    wp_json_post(f'https://virtina.com/wp-json/wp/v2/media/{mid}', {'alt_text': alt_text})
    print(f"    Alt -> {alt_text[:70]}...")
    return mid, murl

# ── STEP 0: fetch both posts ───────────────────────────────────────────────────
print("\n=== FETCHING POSTS ===")
p74  = wp_get('https://virtina.com/wp-json/wp/v2/posts/42074?context=edit&_fields=content')
p108 = wp_get(f'{POST_URL}?context=edit&_fields=content,featured_media,status')
c74  = p74['content']['raw']
content = p108['content']['raw']
print(f"42074: {len(c74)} chars")
print(f"42108: {len(content)} chars  featured_media={p108['featured_media']}")

# ── STEP 1: extract bullet template from 42074 ────────────────────────────────
print("\n=== EXTRACTING BULLET TEMPLATE FROM 42074 ===")
# Body bullet <ul> in 42074 uses list-style:none;padding-left:4px
ul_re = re.compile(r'<ul style="list-style:none;padding-left:4px[^>]*>.*?</ul>', re.DOTALL)
ul_m  = ul_re.search(c74)
if ul_m:
    ul_sample  = ul_m.group()
    ul_open    = re.match(r'<ul[^>]+>', ul_sample).group()
    li_m       = re.search(r'<li[^>]+>.*?</li>', ul_sample, re.DOTALL)
    li_tag     = re.match(r'<li([^>]*)>', li_m.group()).group()    # e.g. <li style="...">
    li_style   = re.search(r'style="([^"]+)"', li_tag).group(1) if li_tag else \
                 'display:flex;align-items:flex-start;gap:8px;padding:4px 0;'
    svg_m      = re.search(r'<svg[^>]*>.*?</svg>', li_m.group(), re.DOTALL)
    ICON_HTML  = svg_m.group() if svg_m else \
                 '<svg viewBox="0 0 512 512" width="10" height="10" style="fill:#43627f;flex-shrink:0;margin-top:5px;" xmlns="http://www.w3.org/2000/svg"><path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512z"/></svg>'
    span_m     = re.search(r'<span style="([^"]*)">', li_m.group())
    SPAN_STYLE = span_m.group(1) if span_m else 'font-size:16px;line-height:1.75;'
    UL_OPEN    = ul_open
    LI_STYLE   = li_style
    print(f"  UL open : {UL_OPEN}")
    print(f"  LI style: {LI_STYLE}")
    print(f"  Icon    : {ICON_HTML[:80]}...")
    print(f"  Span    : {SPAN_STYLE}")
else:
    print("  WARNING: body <ul> not found in 42074, using known-good fallback")
    UL_OPEN    = 'ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;"'
    LI_STYLE   = 'display:flex;align-items:flex-start;gap:8px;padding:4px 0;'
    ICON_HTML  = '<svg viewBox="0 0 512 512" width="10" height="10" style="fill:#43627f;flex-shrink:0;margin-top:5px;" xmlns="http://www.w3.org/2000/svg"><path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512z"/></svg>'
    SPAN_STYLE = 'font-size:16px;line-height:1.75;'

# Save list-template.html
tmpl_items = '\n'.join(
    f'<li style="{LI_STYLE}">{ICON_HTML}<span style="{SPAN_STYLE}">{{{{LIST_ITEM_{i}}}}}</span></li>'
    for i in range(1, 4)
)
TEMPLATE_HTML = f'<{UL_OPEN}>\n{tmpl_items}\n</ul>'
with open('C:/content-intel/clients/virtina/list-template.html', 'w', encoding='utf-8') as f:
    f.write(TEMPLATE_HTML)
print("  Saved -> clients/virtina/list-template.html")

def build_ul(item_html_list):
    lis = '\n'.join(
        f'<li style="{LI_STYLE}">{ICON_HTML}<span style="{SPAN_STYLE}">{t}</span></li>'
        for t in item_html_list
    )
    return f'<{UL_OPEN}>\n{lis}\n</ul>'

# ── STEP 2: rewrite bullet lists in 42108 ─────────────────────────────────────
print("\n=== REWRITING BULLET LISTS ===")
# Match non-TOC <ul> blocks (TOC uses list-style:none!important without spaces before !)
body_ul_re = re.compile(r'<ul style="list-style:none;[^>]*>.*?</ul>', re.DOTALL)
list_count = 0
for m in list(body_ul_re.finditer(content)):
    ul_html = m.group()
    # Extract each LI's inner HTML (strip icon SVG, keep text span content)
    items = []
    for li_m in re.finditer(r'<li[^>]*>(.*?)</li>', ul_html, re.DOTALL):
        inner = li_m.group(1)
        inner = re.sub(r'<svg[^>]*>.*?</svg>', '', inner, flags=re.DOTALL).strip()
        sp = re.search(r'<span[^>]*>(.*?)</span>', inner, re.DOTALL)
        items.append(sp.group(1).strip() if sp else inner)
    if not items:
        continue
    content = content.replace(ul_html, build_ul(items), 1)
    list_count += 1
    print(f"  List {list_count}: {len(items)} items")
print(f"  Total rewritten: {list_count}")

# ── STEP 3: download and upload photos ────────────────────────────────────────
print("\n=== DOWNLOADING & UPLOADING PHOTOS ===")
SPECS = [
    dict(kind='featured', w=1309, h=500,
         kw_list=[
             'warehouse,manager,laptop,business',
             'business,office,manager,laptop',
             'office,professional,laptop,work',
         ],
         filename='woocommerce-erp-integration-featured-1309x500.jpg',
         alt='Warehouse operations manager reviewing WooCommerce orders on laptop while coordinating ERP inventory data for B2B distribution'),
    dict(kind='body1', w=670, h=352,
         kw_list=[
             'business,analyst,data,dashboard',
             'data,analyst,computer,office',
             'office,computer,work,professional',
         ],
         filename='woocommerce-erp-integration-sku-data-670x352.jpg',
         alt='Data analyst examining product master records and SKU mapping spreadsheet for WooCommerce ERP integration project'),
    dict(kind='body2', w=670, h=352,
         kw_list=[
             'developer,team,meeting,screens',
             'team,office,meeting,computer',
             'collaboration,office,technology,work',
         ],
         filename='woocommerce-erp-integration-pricing-670x352.jpg',
         alt='Development team mapping B2B customer-specific pricing rules between ERP and WooCommerce for manufacturer integration'),
    dict(kind='body3', w=670, h=352,
         kw_list=[
             'warehouse,worker,scanner,inventory',
             'warehouse,logistics,worker,storage',
             'warehouse,industrial,equipment,work',
         ],
         filename='woocommerce-erp-integration-operations-670x352.jpg',
         alt='Warehouse worker scanning inventory with handheld device while ERP synchronizes stock levels with WooCommerce B2B store'),
]

photos = {}
for spec in SPECS:
    print(f"\n  [{spec['kind']}] {spec['w']}x{spec['h']}")
    raw = None
    tried = []
    for kw in spec['kw_list']:
        url = f"https://source.unsplash.com/{spec['w']}x{spec['h']}/?{kw}"
        tried.append(url)
        try:
            raw = fetch_photo(url)
            print(f"    Got {len(raw)} bytes via Unsplash keywords: {kw}")
            break
        except Exception as e:
            print(f"    Unsplash failed ({kw}): {e}")
    if raw is None:
        # Last resort: random featured photo at exact size
        url = f"https://source.unsplash.com/featured/{spec['w']}x{spec['h']}/"
        tried.append(url)
        try:
            raw = fetch_photo(url)
            print(f"    Got {len(raw)} bytes via Unsplash random featured")
        except Exception as e:
            print(f"    Unsplash random also failed: {e}")
    if raw is None:
        # picsum.photos — real photos, free, no auth
        url = f"https://picsum.photos/{spec['w']}/{spec['h']}"
        tried.append(url)
        try:
            raw = fetch_photo(url)
            print(f"    Got {len(raw)} bytes via picsum.photos (fallback)")
        except Exception as e:
            print(f"    picsum also failed: {e}")
    if raw is None:
        print(f"    ERROR: All photo sources failed for {spec['kind']}")
        print(f"    Tried: {tried}")
        sys.exit(1)

    final = resize_exact(raw, spec['w'], spec['h'])
    print(f"    Resized -> {spec['w']}x{spec['h']}  {len(final)} bytes")
    mid, murl = upload_image(final, spec['filename'], spec['alt'])
    photos[spec['kind']] = dict(id=mid, url=murl, alt=spec['alt'])

# ── STEP 4: replace body image spans ──────────────────────────────────────────
print("\n=== REPLACING BODY IMAGE SPANS ===")
span_re = re.compile(r'<span style="display:block;margin:20px 0;">.*?</span>', re.DOTALL)
spans   = list(span_re.finditer(content))
print(f"  Found {len(spans)} body image span(s)")

if len(spans) < 3:
    print(f"  ERROR: expected 3 spans, found {len(spans)}")
    sys.exit(1)

# Replace in reverse order to preserve offsets
for i, kind in reversed(list(enumerate(['body1', 'body2', 'body3']))):
    p    = photos[kind]
    new  = (
        f'<span style="display:block;margin:20px 0;">'
        f'<img alt="{p["alt"]}" data-id="{p["id"]}" '
        f'width="670" data-init-width="670" height="352" data-init-height="352" '
        f'title="" loading="lazy" src="{p["url"]}" '
        f'data-width="670" data-height="352" '
        f'style="aspect-ratio: auto 670 / 352;max-width:100%;"></span>'
    )
    m = spans[i]
    content = content[:m.start()] + new + content[m.end():]
    print(f"  Replaced span {i+1} -> ID={p['id']}  {p['url']}")

# ── STEP 5: PUT post ──────────────────────────────────────────────────────────
print("\n=== PUSHING POST 42108 ===")
feat_id = photos['featured']['id']
payload = json.dumps({
    'content': content,
    'status': 'draft',
    'featured_media': feat_id
}).encode('utf-8')
req = urllib.request.Request(POST_URL, data=payload, method='PUT', headers={
    'Authorization': 'Basic ' + CREDS,
    'Content-Type': 'application/json; charset=utf-8'
})
with urllib.request.urlopen(req, timeout=60) as r:
    result = json.loads(r.read())
print(f"  status={result['status']}  featured_media={result['featured_media']}  len={len(result['content']['raw'])}")

# Save locally
with open('C:/content-intel/new-42108-content.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("  Saved -> new-42108-content.html")

# ── FINAL SUMMARY ─────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("COMPLETE")
print("="*60)
print(f"Featured : ID={photos['featured']['id']}  {photos['featured']['url']}")
for n, k in enumerate(['body1','body2','body3'], 1):
    print(f"Body {n}   : ID={photos[k]['id']}  {photos[k]['url']}")
print(f"Lists rewritten : {list_count}")
print(f"Post featured_media: {result['featured_media']}")
print(f"Post content len   : {len(result['content']['raw'])}")
