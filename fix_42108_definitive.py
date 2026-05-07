"""
Definitive fix for post 42108. Addresses all 4 issues:
1. TOC rebuilt from 42074 exact structure (SVG arrow, no-space !important, #43627f fill)
2. Body bullets: CSS circles #43627f (dark slate), NO explicit font-size, explicit dark text
3. New topical images via Openverse/Wikimedia
4. PUT, verify all checks, refuse to exit with errors
"""
import sys, io, json, re, time, base64, urllib.request, urllib.parse
from PIL import Image

CREDS    = base64.b64encode(b'anujith:Mibz 1h3E jWRi bfJs WAXZ rwrM').decode()
POST_URL = 'https://virtina.com/wp-json/wp/v2/posts/42108'
MEDIA_URL = 'https://virtina.com/wp-json/wp/v2/media'
UA_IMG   = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
UA_API   = 'Mozilla/5.0 (compatible; ContentIntelBot/1.0)'

# ── exact values from 42074 diagnosis ────────────────────────────────────────
# SVG arrow path from 42074 TOC (right-pointing arrow icon, fill:#43627f = dark slate)
SVG_ARROW = ('<svg viewBox="0 0 24 24" width="18" height="18" '
             'style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg">'
             '<path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/>'
             '</svg>')
# Body bullet circle color from 42074 SVG fill (dark slate, NOT teal)
CIRCLE_COLOR = '#43627f'
# Body text color (explicit, overrides any teal parent)
TEXT_COLOR = '#2d3e50'

def wp_get(url):
    req = urllib.request.Request(url, headers={'Authorization': 'Basic ' + CREDS})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def wp_put(url, body):
    data = json.dumps(body).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='PUT', headers={
        'Authorization': 'Basic ' + CREDS,
        'Content-Type': 'application/json; charset=utf-8'
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

def wp_post(url, body):
    data = json.dumps(body).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST', headers={
        'Authorization': 'Basic ' + CREDS,
        'Content-Type': 'application/json; charset=utf-8'
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

# ── image helpers ─────────────────────────────────────────────────────────────
def resize_exact(raw, w, h):
    img = Image.open(io.BytesIO(raw))
    if img.mode not in ('RGB',):
        img = img.convert('RGB')
    sw, sh = img.size
    scale = max(w / sw, h / sh)
    nw, nh = max(1, int(sw * scale + 0.5)), max(1, int(sh * scale + 0.5))
    img = img.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - w) // 2, (nh - h) // 2
    img = img.crop((left, top, left + w, top + h))
    for q in [82, 75, 65]:
        buf = io.BytesIO()
        img.save(buf, 'JPEG', quality=q, optimize=True)
        if buf.tell() <= 200 * 1024:
            return buf.getvalue()
    return buf.getvalue()

def download(url, timeout=30):
    req = urllib.request.Request(url, headers={'User-Agent': UA_IMG})
    opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
    with opener.open(req, timeout=timeout) as r:
        data = r.read()
    if len(data) < 8000:
        raise ValueError(f'Too small ({len(data)}b)')
    sig = data[:4]
    if not (sig[:2] == b'\xff\xd8' or sig[:4] == b'\x89PNG'):
        raise ValueError(f'Bad sig: {sig.hex()}')
    return data

def upload_image(img_bytes, filename, alt_text):
    boundary = 'VirtinaBoundaryFix42108'
    body = (f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{filename}"\r\nContent-Type: image/jpeg\r\n\r\n'
            ).encode() + img_bytes + f'\r\n--{boundary}--\r\n'.encode()
    req = urllib.request.Request(MEDIA_URL, data=body, method='POST', headers={
        'Authorization': 'Basic ' + CREDS,
        'Content-Type': f'multipart/form-data; boundary={boundary}',
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        m = json.loads(r.read())
    mid, murl = m['id'], m['source_url']
    print(f'    Uploaded ID={mid}')
    wp_post(f'https://virtina.com/wp-json/wp/v2/media/{mid}', {'alt_text': alt_text})
    return mid, murl

SKIP = ['diagram','map','logo','icon','chart','flag','screenshot','svg','plan',
        'drawing','sketch','monument','church','cathedral','painting','portrait',
        'engraving','stamp','coin','animal','tree','flower','nature','forest',
        'mountain','river','lake','ocean','beach','sky','cloud']

def openverse_search(q, limit=10):
    enc = urllib.parse.quote(q)
    url = f'https://api.openverse.org/v1/images/?q={enc}&license=cc0,pdm&page_size={limit}&aspect_ratio=wide'
    req = urllib.request.Request(url, headers={'User-Agent': UA_API})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read()).get('results', [])
    except:
        return []

def wiki_search(q, limit=10):
    enc = urllib.parse.quote(q + ' filetype:bitmap')
    url = f'https://commons.wikimedia.org/w/api.php?action=query&format=json&list=search&srsearch={enc}&srnamespace=6&srlimit={limit}'
    req = urllib.request.Request(url, headers={'User-Agent': UA_API})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read()).get('query', {}).get('search', [])
    except:
        return []

def wiki_url(title):
    t = urllib.parse.quote(title)
    url = f'https://commons.wikimedia.org/w/api.php?action=query&format=json&titles={t}&prop=imageinfo&iiprop=url|mime&iiurlwidth=1920'
    req = urllib.request.Request(url, headers={'User-Agent': UA_API})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read())
        for p in data.get('query', {}).get('pages', {}).values():
            ii = p.get('imageinfo', [{}])
            if ii:
                return ii[0].get('thumburl') or ii[0].get('url'), ii[0].get('mime','')
    except:
        pass
    return None, ''

def get_image(openverse_queries, wiki_queries):
    for q in openverse_queries:
        print(f'    Openverse: {q}')
        results = openverse_search(q, 10)
        time.sleep(0.4)
        for r in results:
            title = (r.get('title') or '').lower()
            if any(w in title for w in SKIP):
                continue
            url = r.get('url', '')
            if not url:
                continue
            # Normalise Flickr URLs
            if 'staticflickr.com' in url:
                for suffix in ['_b.jpg', '_c.jpg', '_z.jpg']:
                    candidate = re.sub(r'_[a-z]\.jpg$', suffix, url)
                    try:
                        raw = download(candidate, 25)
                        print(f'    Got {len(raw)}b: {r.get("title","")[:55]}')
                        return raw
                    except:
                        pass
            if url.lower().endswith(('.jpg','.jpeg','.png')):
                try:
                    raw = download(url, 25)
                    print(f'    Got {len(raw)}b: {r.get("title","")[:55]}')
                    return raw
                except:
                    pass
    for q in wiki_queries:
        print(f'    Wikimedia: {q}')
        hits = wiki_search(q, 10)
        time.sleep(1.0)
        for h in hits:
            title = h['title']
            if any(w in title.lower() for w in SKIP):
                continue
            img_url, mime = wiki_url(title)
            time.sleep(0.5)
            if not img_url:
                continue
            if not (img_url.lower().endswith(('.jpg','.jpeg','.png')) or 'jpeg' in mime.lower()):
                continue
            try:
                raw = download(img_url, 25)
                print(f'    Got {len(raw)}b: {title[:55]}')
                return raw
            except:
                pass
    return None

# ── PART A: Source & upload images ────────────────────────────────────────────
print('\n=== SOURCING IMAGES ===')

SPECS = [
    dict(kind='featured', w=1309, h=500,
         filename='woocommerce-erp-integration-featured-1309x500.jpg',
         alt='Warehouse distribution center operations manager at laptop reviewing WooCommerce B2B order data while coordinating ERP inventory sync for manufacturer clients',
         ov=['warehouse operations manager laptop computer',
             'distribution center manager office laptop',
             'logistics operations office computer professional'],
         wiki=['warehouse distribution center interior',
               'logistics operations manager office',
               'industrial warehouse interior workers']),
    dict(kind='body1', w=670, h=352,
         filename='woocommerce-erp-integration-itemmaster-670x352.jpg',
         alt='Business analyst at desk reviewing product master data spreadsheet for WooCommerce ERP SKU mapping and item code synchronization project',
         ov=['office professional desk computer data analysis',
             'business data spreadsheet office desk professional',
             'analyst computer office work desk'],
         wiki=['office worker computer desk professional',
               'data analyst office computer',
               'business professional office laptop work']),
    dict(kind='body2', w=670, h=352,
         filename='woocommerce-erp-integration-pricing-670x352.jpg',
         alt='Software development team at computer workstations reviewing B2B pricing integration between ERP system and WooCommerce for wholesale manufacturer accounts',
         ov=['software developers computers office workstations',
             'technology team office computers monitors work',
             'web developers office open workspace computers'],
         wiki=['software developers office computers',
               'technology office workers computers',
               'open office workers computers desks']),
    dict(kind='body3', w=670, h=352,
         filename='woocommerce-erp-integration-warehouse-670x352.jpg',
         alt='Warehouse employee scanning product barcode with handheld device while ERP system updates real-time inventory levels synced to WooCommerce B2B storefront',
         ov=['warehouse worker barcode scanner inventory',
             'warehouse employee scanning products shelf',
             'distribution center worker inventory management'],
         wiki=['warehouse worker inventory barcode',
               'warehouse employee scanning products',
               'distribution center inventory worker']),
]

photos = {}
for spec in SPECS:
    print(f'\n[{spec["kind"]}] {spec["w"]}x{spec["h"]}')
    raw = get_image(spec['ov'], spec['wiki'])
    if raw is None:
        print(f'ERROR: No image for {spec["kind"]}')
        sys.exit(1)
    final = resize_exact(raw, spec['w'], spec['h'])
    print(f'    Resized: {len(final)}b')
    mid, murl = upload_image(final, spec['filename'], spec['alt'])
    photos[spec['kind']] = {'id': mid, 'url': murl, 'alt': spec['alt']}
    time.sleep(1.0)

# ── PART B: Fetch post & rebuild content ──────────────────────────────────────
print('\n=== FETCHING POST 42108 ===')
post = wp_get(POST_URL + '?context=edit&_fields=content,featured_media,status')
content = post['content']['raw']
print(f'len={len(content)} featured_media={post["featured_media"]}')

# ── PART C: Rebuild TOC from 42074 exact structure ────────────────────────────
print('\n=== REBUILDING TOC ===')

# Extract current TOC anchor links (titles/hrefs) from broken TOC
ul_re = re.compile(r'<ul[^>]*>.*?</ul>', re.DOTALL)
toc_m = ul_re.search(content)
if not toc_m:
    print('ERROR: TOC not found')
    sys.exit(1)

toc_links = []
for li_m in re.finditer(r'<li[^>]*>(.*?)</li>', toc_m.group(), re.DOTALL):
    inner = li_m.group(1)
    # Strip any SVG or span icons
    inner = re.sub(r'<svg[^>]*>.*?</svg>', '', inner, flags=re.DOTALL)
    inner = re.sub(r'<span[^>]*></span>', '', inner)
    a_m = re.search(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', inner, re.DOTALL)
    if a_m:
        href = a_m.group(1)
        text = re.sub(r'<[^>]+>', '', a_m.group(2)).strip()
        toc_links.append((href, text))
        print(f'  TOC: {href} -> {text}')

# Build correct TOC matching 42074 structure EXACTLY:
# - list-style:none!important (NO spaces before !important)
# - SVG arrow icon (fill:#43627f)
# - link color: color:#00a0e2!important

ARROW_SPAN = (f'<span aria-hidden="true" style="position:absolute!important;'
              f'left:0!important;top:8px!important;">{SVG_ARROW}</span>')
LI_TOC_STYLE = ('list-style:none!important;padding:8px 0 8px 32px!important;'
                'position:relative!important;line-height:1.5!important;margin:0!important;')
LINK_STYLE   = ('color:#00a0e2!important;text-decoration:none!important;'
                'font-family:metropolis,arial!important;font-size:16px!important;'
                'font-weight:500!important;')

toc_lis = []
for href, text in toc_links:
    li = (f'<li style="{LI_TOC_STYLE}">'
          f'{ARROW_SPAN}'
          f'<a href="{href}" style="{LINK_STYLE}">{text}</a>'
          f'</li>')
    toc_lis.append(li)

correct_toc = ('<ul style="list-style:none!important;padding-left:0!important;'
               'margin:0 0 1.5em 0!important;">\n'
               + '\n'.join(toc_lis)
               + '\n</ul>')

# Replace the TOC in content
content = content[:toc_m.start()] + correct_toc + content[toc_m.end():]
print(f'TOC rebuilt with {len(toc_links)} items')

# ── PART D: Rebuild body bullet lists ─────────────────────────────────────────
print('\n=== REBUILDING BODY BULLET LISTS ===')

# Match ONLY body bullet lists — exclude any <ul> whose style has !important
# Safe pattern: the style attr must NOT contain '!important'
body_ul_re = re.compile(
    r'<ul\s+style="(?![^"]*!important)[^"]*"[^>]*>.*?</ul>',
    re.DOTALL
)

# CSS circle bullet template with 42074-matched values:
# - color: #43627f (dark slate, matching 42074 SVG fill — NOT bright teal)
# - font-size: NOT SET (inherit from parent, same as 42074 body LI)
# - text color: explicit #2d3e50 (dark, overrides any teal parent)
UL_OPEN   = '<ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;">'
LI_STYLE  = 'display:flex;align-items:flex-start;gap:10px;padding:6px 0;'
CIRCLE_SPAN = ('<span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;'
               f'background-color:{CIRCLE_COLOR};border-radius:50%;'
               'display:inline-block;"></span>')
TEXT_SPAN   = f'<span style="font-size:inherit;line-height:1.7;color:{TEXT_COLOR};">'

def build_ul(items):
    lis = []
    for text in items:
        li = f'<li style="{LI_STYLE}">{CIRCLE_SPAN}{TEXT_SPAN}{text}</span></li>'
        lis.append(li)
    return UL_OPEN + '\n' + '\n'.join(lis) + '\n</ul>'

def extract_items(ul_html):
    items = []
    for li_m in re.finditer(r'<li[^>]*>(.*?)</li>', ul_html, re.DOTALL):
        inner = li_m.group(1)
        # Strip SVG, empty spans (old circle spans)
        inner = re.sub(r'<svg[^>]*>.*?</svg>', '', inner, flags=re.DOTALL)
        # Strip CSS circle empty spans
        inner = re.sub(r'<span[^>]*></span>', '', inner)
        # If wrapped in a text span, unwrap it (but preserve inline <strong>)
        sp_m = re.search(r'<span[^>]*>(.*?)</span>', inner, re.DOTALL)
        if sp_m and sp_m.group(1).strip():
            text = sp_m.group(1).strip()
        else:
            # Strip outer span wrappers but keep inline tags
            text = re.sub(r'</?span[^>]*>', '', inner).strip()
        if text:
            items.append(text)
    return items

# Find and replace all body bullet lists (reverse order to preserve offsets)
matches = list(body_ul_re.finditer(content))
print(f'Body bullet lists found: {len(matches)}')
for m in reversed(matches):
    items = extract_items(m.group())
    if not items:
        continue
    new_ul = build_ul(items)
    content = content[:m.start()] + new_ul + content[m.end():]
    print(f'  Rebuilt list with {len(items)} items')

# ── PART E: Replace body images ───────────────────────────────────────────────
print('\n=== REPLACING BODY IMAGES ===')
span_re = re.compile(r'<span style="display:block;margin:20px 0;">.*?</span>', re.DOTALL)
spans   = list(span_re.finditer(content))
print(f'Found {len(spans)} body image spans')

for i, kind in reversed(list(enumerate(['body1', 'body2', 'body3']))):
    if i >= len(spans):
        continue
    p = photos[kind]
    new_span = (f'<span style="display:block;margin:20px 0;">'
                f'<img alt="{p["alt"]}" data-id="{p["id"]}" '
                f'width="670" data-init-width="670" height="352" data-init-height="352" '
                f'title="" loading="lazy" src="{p["url"]}" '
                f'data-width="670" data-height="352" '
                f'style="aspect-ratio: auto 670 / 352;max-width:100%;"></span>')
    s = spans[i]
    content = content[:s.start()] + new_span + content[s.end():]
    print(f'  Replaced span {i+1} -> ID={p["id"]}')

# ── PART F: PUT post ──────────────────────────────────────────────────────────
print('\n=== PUSHING POST 42108 ===')
result = wp_put(POST_URL, {
    'content': content,
    'status': 'draft',
    'featured_media': photos['featured']['id']
})
saved = result['content']['raw']
print(f'status={result["status"]} featured_media={result["featured_media"]} len={len(saved)}')

# ── PART G: Verify ────────────────────────────────────────────────────────────
print('\n=== VERIFICATION ===')
errors = []

# 1. featured_media
fm = result['featured_media']
ok = fm and fm != 0
print(f'1. featured_media={fm}', 'OK' if ok else 'FAIL')
if not ok: errors.append(f'featured_media={fm}')

# 2. Body image URLs (all must be virtina.com uploads)
img_urls = re.findall(r'src="(https://virtina\.com/wp-content/uploads/[^"]+)"', saved)
print(f'2. Body images ({len(img_urls)}):')
for u in img_urls: print(f'   {u}')
if len(img_urls) < 3: errors.append(f'Only {len(img_urls)} body images')
for u in img_urls:
    if 'picsum' in u or 'unsplash' in u or 'placehold' in u:
        errors.append(f'External image URL: {u}')

# 3. TOC structure
toc_saved = ul_re.search(saved)
if toc_saved:
    toc_s = toc_saved.group()
    has_svg  = 'viewBox="0 0 24 24"' in toc_s
    has_imp  = 'list-style:none!important' in toc_s  # no spaces
    no_circ  = 'border-radius:50%' not in toc_s
    has_links = 'href="#' in toc_s
    print(f'3. TOC: svg_arrow={has_svg} no-space-important={has_imp} no-circles={no_circ} links={has_links}')
    if not has_svg:  errors.append('TOC missing SVG arrow')
    if not has_imp:  errors.append('TOC !important format wrong')
    if not no_circ:  errors.append('TOC has CSS circles (wrong)')
else:
    errors.append('TOC not found')

# 4. Body bullet circle color (#43627f)
body_circles = set(re.findall(r'background-color:([^;]+);border-radius:50%', saved))
print(f'4. Body bullet circle colors: {body_circles}')
if body_circles != {CIRCLE_COLOR}: errors.append(f'Circle color {body_circles} (expected {CIRCLE_COLOR})')

# 5. Body bullet has NO explicit font-size
body_li_explicit_fs = re.findall(r'<li style="display:flex[^"]*font-size[^"]*"', saved)
print(f'5. Body LI explicit font-size: {len(body_li_explicit_fs)} (should be 0)')
if body_li_explicit_fs: errors.append('Body LI has explicit font-size override')

# 6. Text color is explicit dark
text_spans = re.findall(r'<span style="[^"]*color:([^;"]+)[^"]*"', saved)
# Find text spans specifically (the ones inside our bullets)
bullet_text_colors = set(re.findall(
    r'font-size:inherit;line-height:1\.7;color:([^;"]+)', saved))
print(f'6. Bullet text colors: {bullet_text_colors}')
if bullet_text_colors and bullet_text_colors != {TEXT_COLOR}:
    errors.append(f'Bullet text color {bullet_text_colors}')

# 7. No orphan << >>
dbl = len(re.findall(r'<<', saved)) + len(re.findall(r'>>', saved))
print(f'7. Orphan << >>: {dbl}')
if dbl: errors.append(f'{dbl} orphan << >>')

# 8. Show TOC first item and body list first item as proof
print('\n--- TOC first LI (proof):')
toc_li = re.search(r'<li[^>]*>.*?</li>', toc_saved.group(), re.DOTALL)
if toc_li: print(toc_li.group()[:300])

print('\n--- Body bullet first LI (proof):')
body_ul_saved = list(body_ul_re.finditer(saved))
if body_ul_saved:
    bl = body_ul_saved[0].group()
    bli = re.search(r'<li[^>]*>.*?</li>', bl, re.DOTALL)
    if bli: print(bli.group()[:300])

if errors:
    print('\n!!! ERRORS !!!')
    for e in errors: print(f'  - {e}')
    sys.exit(1)
else:
    print('\nALL CHECKS PASSED')

# Save local
with open('new-42108-content.html', 'w', encoding='utf-8') as f:
    f.write(saved)

print('\n' + '='*60)
print('COMPLETE')
print(f'Featured  : ID={photos["featured"]["id"]}  {photos["featured"]["url"]}')
for n, k in enumerate(["body1","body2","body3"], 1):
    print(f'Body {n}     : ID={photos[k]["id"]}  {photos[k]["url"]}')
print(f'Circle    : {CIRCLE_COLOR} (dark slate, matches 42074 SVG fill)')
print(f'Text color: {TEXT_COLOR} (explicit dark, no teal inheritance)')
print(f'Font-size : inherited (no override, same as 42074)')
