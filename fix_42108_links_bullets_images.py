"""
Fix post 42108:
1. External links: keep max 2 non-competitor links, strip the rest to plain text
2. Bullet text: match body <p> exactly (font-size:16px;line-height:1.75)
3. Images: office/laptop/business photos (NOT buildings, warehouses, FEMA scenes)
"""
import sys, io, json, re, time, base64, urllib.request, urllib.parse
from PIL import Image

CREDS    = base64.b64encode(b'anujith:Mibz 1h3E jWRi bfJs WAXZ rwrM').decode()
POST_URL = 'https://virtina.com/wp-json/wp/v2/posts/42108'
MEDIA_URL = 'https://virtina.com/wp-json/wp/v2/media'
UA_IMG = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
UA_API = 'Mozilla/5.0 (compatible; ContentIntelBot/1.0)'

# ── fetch post ─────────────────────────────────────────────────────────────────
req = urllib.request.Request(
    POST_URL + '?context=edit&_fields=content,featured_media',
    headers={'Authorization': 'Basic ' + CREDS}
)
with urllib.request.urlopen(req, timeout=30) as r:
    post = json.loads(r.read())
content = post['content']['raw']
feat    = post['featured_media']
print(f'Fetched: len={len(content)} feat={feat}')

# ═══════════════════════════════════════════════════════════════
# FIX 1 — External links: strip down to max 2 non-competitor links
# ═══════════════════════════════════════════════════════════════
print('\n=== FIX 1: EXTERNAL LINKS ===')

BANNED_DOMAINS = ['shopify.com']  # competitors — all links to these stripped

ext_re = re.compile(r'<a\s+[^>]*href="(https?://(?!virtina\.com)[^"]+)"[^>]*>(.*?)</a>', re.DOTALL)
all_ext = list(ext_re.finditer(content))
print(f'Found {len(all_ext)} external links')

kept = 0
fixed_content = content
# Process in reverse to preserve offsets
for m in reversed(all_ext):
    url  = m.group(1)
    text = m.group(2)
    domain = re.search(r'https?://(?:www\.)?([^/]+)', url)
    domain = domain.group(1) if domain else ''

    # Always strip banned domains (Shopify etc)
    is_banned = any(b in domain for b in BANNED_DOMAINS)
    # Strip if we've already kept 2 links, or if it's banned
    if is_banned or kept >= 2:
        # Replace with plain text (strip the anchor)
        plain = re.sub(r'<[^>]+>', '', text).strip()
        fixed_content = fixed_content[:m.start()] + plain + fixed_content[m.end():]
        print(f'  STRIPPED: {domain} -> "{plain[:60]}"')
    else:
        kept += 1
        print(f'  KEPT ({kept}): {domain} -> {url[:70]}')

print(f'External links remaining: {kept}')
content = fixed_content

# Verify
remaining = re.findall(r'href="(https?://(?!virtina\.com)[^"]+)"', content)
print(f'Verification: {len(remaining)} external hrefs remaining')
for u in remaining:
    print(f'  {u[:80]}')

# ═══════════════════════════════════════════════════════════════
# FIX 2 — Bullet text: match body paragraph style exactly
# ═══════════════════════════════════════════════════════════════
print('\n=== FIX 2: BULLET TEXT STYLE ===')

# Body <p> uses: font-size:16px;line-height:1.75 (confirmed from post content)
# Current bullet text span: font-size:inherit;line-height:1.7;color:#2d3e50
# Fix: set font-size:16px;line-height:1.75 to match exactly

OLD_SPAN_STYLE = 'font-size:inherit;line-height:1.7;color:#2d3e50;'
NEW_SPAN_STYLE = 'font-size:16px;line-height:1.75;color:#2d3e50;'

count = content.count(OLD_SPAN_STYLE)
content = content.replace(OLD_SPAN_STYLE, NEW_SPAN_STYLE)
print(f'Updated {count} bullet text spans: line-height 1.7->1.75, font-size inherit->16px')

# Verify
check = len(re.findall(re.escape(NEW_SPAN_STYLE), content))
print(f'New style present: {check} times')

# ═══════════════════════════════════════════════════════════════
# FIX 3 — New images: office/laptop/business context
# ═══════════════════════════════════════════════════════════════
print('\n=== FIX 3: SOURCING TOPICAL IMAGES ===')

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
    for q in [82,75,65]:
        buf = io.BytesIO()
        img.save(buf,'JPEG',quality=q,optimize=True)
        if buf.tell() <= 200*1024: return buf.getvalue()
    return buf.getvalue()

def download(url, timeout=30):
    opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
    req = urllib.request.Request(url, headers={'User-Agent': UA_IMG})
    with opener.open(req, timeout=timeout) as r:
        data = r.read()
    if len(data) < 8000: raise ValueError(f'Too small: {len(data)}b')
    if data[:2] not in (b'\xff\xd8',) and data[:4] != b'\x89PNG':
        raise ValueError(f'Bad sig: {data[:4].hex()}')
    return data

def upload_image(img_bytes, filename, alt):
    boundary = 'VirtinaBnd42108Fix'
    body = (f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{filename}"\r\nContent-Type: image/jpeg\r\n\r\n'
            ).encode() + img_bytes + f'\r\n--{boundary}--\r\n'.encode()
    req = urllib.request.Request(MEDIA_URL, data=body, method='POST', headers={
        'Authorization': 'Basic ' + CREDS,
        'Content-Type': f'multipart/form-data; boundary={boundary}',
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        m = json.loads(r.read())
    mid, murl = m['id'], m['source_url']
    data = json.dumps({'alt_text': alt}).encode('utf-8')
    req2 = urllib.request.Request(f'https://virtina.com/wp-json/wp/v2/media/{mid}',
                                   data=data, method='POST', headers={
        'Authorization':'Basic '+CREDS, 'Content-Type':'application/json; charset=utf-8'})
    urllib.request.urlopen(req2, timeout=30).close()
    print(f'    Uploaded ID={mid}  {murl[:80]}')
    return mid, murl

# Skip titles containing these — we want PEOPLE IN OFFICES, not buildings/nature/disasters
SKIP = ['building','depot','station','freight','fema','disaster','flood','hurricane',
        'fire','monument','church','cathedral','nature','forest','mountain','river',
        'lake','beach','flower','animal','flag','map','logo','icon','chart','diagram',
        'drawing','sketch','portrait','painting','engraving','stamp','coin','aerial',
        'satellite','exterior','facade','architecture','bridge','road','highway',
        'sunset','sunrise','landscape','wilderness','park','garden','tree','plant']

def openverse_search(q, limit=15):
    enc = urllib.parse.quote(q)
    url = f'https://api.openverse.org/v1/images/?q={enc}&license=cc0,pdm&page_size={limit}&aspect_ratio=wide'
    req = urllib.request.Request(url, headers={'User-Agent': UA_API})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read()).get('results', [])
    except Exception as e:
        print(f'    Openverse err: {e}')
        return []

def wiki_search(q, limit=12):
    enc = urllib.parse.quote(q + ' filetype:bitmap')
    url = f'https://commons.wikimedia.org/w/api.php?action=query&format=json&list=search&srsearch={enc}&srnamespace=6&srlimit={limit}'
    req = urllib.request.Request(url, headers={'User-Agent': UA_API})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read()).get('query',{}).get('search',[])
    except Exception as e:
        print(f'    Wikimedia err: {e}')
        return []

def wiki_url(title):
    t = urllib.parse.quote(title)
    url = f'https://commons.wikimedia.org/w/api.php?action=query&format=json&titles={t}&prop=imageinfo&iiprop=url|mime&iiurlwidth=1920'
    req = urllib.request.Request(url, headers={'User-Agent': UA_API})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read())
        for p in data.get('query',{}).get('pages',{}).values():
            ii = p.get('imageinfo',[{}])
            if ii: return ii[0].get('thumburl') or ii[0].get('url'), ii[0].get('mime','')
    except:
        pass
    return None, ''

def get_image(ov_queries, wiki_queries, label):
    for q in ov_queries:
        print(f'    Openverse [{label}]: {q}')
        results = openverse_search(q, 15)
        time.sleep(0.5)
        for r in results:
            title = (r.get('title') or '').lower()
            if any(w in title for w in SKIP):
                continue
            url = r.get('url','')
            if not url: continue
            # Handle Flickr
            if 'staticflickr.com' in url:
                for sfx in ['_b.jpg','_c.jpg','_z.jpg']:
                    cand = re.sub(r'_[a-z]\.jpg$', sfx, url)
                    try:
                        raw = download(cand, 25)
                        print(f'    OK {len(raw)}b: {r.get("title","")[:55]}')
                        return raw
                    except: pass
            if url.lower().endswith(('.jpg','.jpeg','.png')):
                try:
                    raw = download(url, 25)
                    print(f'    OK {len(raw)}b: {r.get("title","")[:55]}')
                    return raw
                except: pass
    for q in wiki_queries:
        print(f'    Wikimedia [{label}]: {q}')
        hits = wiki_search(q, 12)
        time.sleep(1.2)
        for h in hits:
            t = h['title']
            if any(w in t.lower() for w in SKIP): continue
            img_url, mime = wiki_url(t)
            time.sleep(0.6)
            if not img_url: continue
            if not (img_url.lower().endswith(('.jpg','.jpeg','.png')) or 'jpeg' in mime.lower()): continue
            try:
                raw = download(img_url, 25)
                print(f'    OK {len(raw)}b: {t[:55]}')
                return raw
            except: pass
    return None

# Image specs — all queries focus on PEOPLE + COMPUTERS + OFFICE
SPECS = [
    dict(
        kind='featured', w=1309, h=500,
        filename='woocommerce-erp-integration-featured-1309x500.jpg',
        alt='Operations manager reviewing WooCommerce B2B order dashboard on laptop screen while coordinating ERP data synchronization for manufacturer distribution network',
        ov=['person laptop computer office desk working professional',
            'professional office desk laptop computer work',
            'business man woman laptop office work desk'],
        wiki=['office worker laptop computer professional',
              'business person computer office desk',
              'professional working laptop office'],
    ),
    dict(
        kind='body1', w=670, h=352,
        filename='woocommerce-erp-integration-itemmaster-670x352.jpg',
        alt='Data analyst at computer reviewing product catalog spreadsheet for WooCommerce ERP item master synchronization and SKU mapping across B2B manufacturer systems',
        ov=['office worker computer spreadsheet data analysis professional',
            'woman man computer office desk spreadsheet work',
            'analyst office computer data professional desk work'],
        wiki=['office worker computer spreadsheet',
              'data analysis office professional computer',
              'person office computer work professional'],
    ),
    dict(
        kind='body2', w=670, h=352,
        filename='woocommerce-erp-integration-pricing-670x352.jpg',
        alt='Software development team working at computer workstations reviewing B2B pricing architecture integration between ERP platform and WooCommerce wholesale storefront',
        ov=['developers office computers multiple screens programming',
            'software team office computers monitors work',
            'programmers computers office open workspace'],
        wiki=['software developers office computers screens',
              'programmers office computer work',
              'developers working computers office'],
    ),
    dict(
        kind='body3', w=670, h=352,
        filename='woocommerce-erp-integration-warehouse-670x352.jpg',
        alt='Ecommerce operations team at computers managing B2B order fulfillment with ERP inventory data synchronized to WooCommerce storefront for wholesale manufacturer clients',
        ov=['office team computers ecommerce operations work',
            'business team office computers work professional',
            'office workers computers technology professional'],
        wiki=['office workers computers technology',
              'business team office computers',
              'professional office team computer work'],
    ),
]

photos = {}
for spec in SPECS:
    print(f'\n[{spec["kind"]}] {spec["w"]}x{spec["h"]}')
    raw = get_image(spec['ov'], spec['wiki'], spec['kind'])
    if raw is None:
        print(f'ERROR: no image for {spec["kind"]}')
        sys.exit(1)
    final = resize_exact(raw, spec['w'], spec['h'])
    print(f'    Resized: {len(final)}b')
    mid, murl = upload_image(final, spec['filename'], spec['alt'])
    photos[spec['kind']] = {'id': mid, 'url': murl, 'alt': spec['alt']}
    time.sleep(1.0)

# ═══════════════════════════════════════════════════════════════
# Replace body image spans
# ═══════════════════════════════════════════════════════════════
print('\n=== REPLACING IMAGE SPANS ===')
span_re = re.compile(r'<span style="display:block;margin:20px 0;">.*?</span>', re.DOTALL)
spans = list(span_re.finditer(content))
print(f'Found {len(spans)} image spans')

for i, kind in reversed(list(enumerate(['body1','body2','body3']))):
    if i >= len(spans): continue
    p = photos[kind]
    new = (f'<span style="display:block;margin:20px 0;">'
           f'<img alt="{p["alt"]}" data-id="{p["id"]}" '
           f'width="670" data-init-width="670" height="352" data-init-height="352" '
           f'title="" loading="lazy" src="{p["url"]}" '
           f'data-width="670" data-height="352" '
           f'style="aspect-ratio: auto 670 / 352;max-width:100%;"></span>')
    s = spans[i]
    content = content[:s.start()] + new + content[s.end():]
    print(f'  Span {i+1} -> ID={p["id"]}')

# ═══════════════════════════════════════════════════════════════
# PUT post
# ═══════════════════════════════════════════════════════════════
print('\n=== PUSHING POST 42108 ===')
payload = json.dumps({
    'content': content,
    'status': 'draft',
    'featured_media': photos['featured']['id']
}).encode('utf-8')
req = urllib.request.Request(POST_URL, data=payload, method='PUT', headers={
    'Authorization': 'Basic ' + CREDS,
    'Content-Type': 'application/json; charset=utf-8'
})
with urllib.request.urlopen(req, timeout=60) as r:
    result = json.loads(r.read())
saved = result['content']['raw']
print(f'status={result["status"]} feat={result["featured_media"]} len={len(saved)}')

# ═══════════════════════════════════════════════════════════════
# Verify
# ═══════════════════════════════════════════════════════════════
print('\n=== VERIFICATION ===')
errors = []

ext_remaining = re.findall(r'href="(https?://(?!virtina\.com)[^"]+)"', saved)
print(f'1. External links: {len(ext_remaining)} (max 2)')
for u in ext_remaining: print(f'   {u[:80]}')
if len(ext_remaining) > 2: errors.append(f'{len(ext_remaining)} external links (max 2)')

bullet_spans = re.findall(r'font-size:16px;line-height:1\.75;color:#2d3e50', saved)
print(f'2. Bullet text spans (font-size:16px;line-height:1.75): {len(bullet_spans)}')

img_urls = re.findall(r'src="(https://virtina\.com/wp-content/uploads/[^"]+)"', saved)
print(f'3. Body images ({len(img_urls)}):')
for u in img_urls: print(f'   {u}')
if len(img_urls) < 3: errors.append(f'Only {len(img_urls)} body images')

fm = result['featured_media']
print(f'4. featured_media={fm}', 'OK' if fm else 'FAIL')
if not fm: errors.append('featured_media=0')

dbl = len(re.findall(r'<<', saved)) + len(re.findall(r'>>', saved))
print(f'5. Orphan << >>: {dbl}')
if dbl: errors.append(f'{dbl} orphan << >>')

toc = re.search(r'<ul[^>]*>.*?</ul>', saved, re.DOTALL)
print(f'6. TOC svg_arrow={"viewBox" in toc.group()} no-circ={"border-radius:50%" not in toc.group()} important={"!important" in toc.group()}')

with open('new-42108-content.html','w',encoding='utf-8') as f: f.write(saved)
print('Saved -> new-42108-content.html')

if errors:
    print('\nERRORS:', errors)
    sys.exit(1)

print('\n' + '='*60)
print('ALL CHECKS PASSED')
print(f'External links : {len(ext_remaining)} (max 2)')
print(f'Bullet style   : font-size:16px; line-height:1.75 (matches body <p>)')
print(f'Featured ID    : {photos["featured"]["id"]}')
for n, k in enumerate(["body1","body2","body3"], 1):
    print(f'Body {n} ID      : {photos[k]["id"]}  {photos[k]["url"][:70]}')
