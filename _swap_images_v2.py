"""
Replace all 4 Virtina post 42177 images with eCommerce-specific, contextually relevant photos.

Visual story:
  Featured  — Online store on MacBook screen (3500x1969 CC0, Wikimedia/Unsplash)
              Immediately signals eCommerce to any reader
  Section 1 — Business professional at laptop in bright office (4016x6016, Wikimedia)
              "Why hitting a wall" — merchant at their screen, professional context
  Section 2 — Business meeting (existing 42188, keep)
              "When to migrate" — team making a decision together
  Section 3 — CRO eCommerce concept: laptop + graphs + shopping cart (4000x2667 CC BY 2.0)
              "Migration / what you gain" — platform metrics, conversion optimization

Old IDs being replaced:
  featured 42190 → new
  section1 42192 → new
  section2 42188 → keep (no upload)
  section3 42193 → new
"""
import requests, base64, io, re, urllib3
urllib3.disable_warnings()
from PIL import Image

creds = base64.b64encode(b'anujith:Mibz 1h3E jWRi bfJs WAXZ rwrM').decode()
WP_H = {'Authorization': f'Basic {creds}'}
DL_H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def download(url, min_kb=500):
    print(f'  Downloading {url.split("/")[-1][:60]}...')
    r = requests.get(url, timeout=180, verify=False, headers=DL_H)
    if r.status_code == 200 and len(r.content) >= min_kb * 1024:
        img = Image.open(io.BytesIO(r.content)).convert('RGB')
        print(f'  Source: {img.size[0]}x{img.size[1]}  {len(r.content)//1024}KB')
        return img
    print(f'  FAIL {r.status_code} {len(r.content)//1024}KB')
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
    img.save(buf, 'JPEG', quality=88, optimize=True)
    buf.seek(0)
    return buf

def wp_upload(buf, filename, alt, title):
    uh = {**WP_H, 'Content-Disposition': f'attachment; filename="{filename}"',
          'Content-Type': 'image/jpeg'}
    r = requests.post('https://virtina.com/wp-json/wp/v2/media',
                      headers=uh, data=buf.getvalue(), verify=False, timeout=90)
    if r.status_code not in [200, 201]:
        print(f'  Upload FAIL {r.status_code}: {r.text[:80]}')
        return None, ''
    d = r.json()
    mid, src = d['id'], d.get('source_url', '')
    sz = d.get('media_details', {}).get('filesize', 0) // 1024
    requests.post(f'https://virtina.com/wp-json/wp/v2/media/{mid}',
                  headers={**WP_H, 'Content-Type': 'application/json'},
                  json={'alt_text': alt, 'title': title}, verify=False, timeout=20)
    print(f'  Uploaded ID={mid}  {sz}KB  {src.split("/")[-1]}')
    return mid, src

# ── SLOT DEFINITIONS ──────────────────────────────────────────────────────────
slots = [
    {
        'name': 'featured', 'tw': 1309, 'th': 500,
        'url': 'https://upload.wikimedia.org/wikipedia/commons/0/05/Online_store_on_a_screen_%28Unsplash%29.jpg',
        'filename': 'volusion-online-store-featured-1309x500.jpg',
        'alt': ('Laptop screen displaying an eCommerce online store interface, '
                'representing the kind of store Volusion merchants run before '
                'deciding to migrate to WooCommerce'),
        'title': 'Online store on laptop screen — Volusion to WooCommerce migration context',
    },
    {
        'name': 'section1', 'tw': 670, 'th': 352,
        'url': 'https://upload.wikimedia.org/wikipedia/commons/7/70/Business_professional_working_on_laptop_in_a_bright_office_space.jpg',
        'filename': 'volusion-merchant-laptop-section1-670x352.jpg',
        'alt': ('Business professional working at laptop in a bright modern office, '
                'representing a Volusion merchant reviewing their eCommerce store '
                'performance and unexpected platform billing charges'),
        'title': 'Business professional at laptop — Volusion merchant reviewing eCommerce platform costs',
    },
    {
        'name': 'section3', 'tw': 670, 'th': 352,
        'url': 'https://upload.wikimedia.org/wikipedia/commons/e/e8/CRO-_Ecommerce_Conversion_Rate_Optimisation_Concept.jpg',
        'filename': 'volusion-ecommerce-metrics-section3-670x352.jpg',
        'alt': ('Laptop screen showing eCommerce conversion rate optimisation metrics, '
                'graphs, and shopping cart icon representing the performance gains '
                'WooCommerce merchants see after migrating from Volusion'),
        'title': 'eCommerce metrics and conversion graphs — WooCommerce performance after Volusion migration',
    },
]

results = {}
src_urls = {}

for slot in slots:
    print(f'\n{slot["name"].upper()} ({slot["tw"]}x{slot["th"]})')
    img = download(slot['url'])
    if not img:
        print(f'  SKIP — download failed')
        continue
    buf = crop_resize(img, slot['tw'], slot['th'])
    print(f'  Resized: {slot["tw"]}x{slot["th"]}  {len(buf.getvalue())//1024}KB')
    mid, src = wp_upload(buf, slot['filename'], slot['alt'], slot['title'])
    if mid:
        results[slot['name']] = mid
        src_urls[slot['name']] = src

print(f'\nUploaded: {list(results.keys())}')

# Section 2 keeps existing image
results['section2']   = 42188
mr = requests.get('https://virtina.com/wp-json/wp/v2/media/42188',
                  headers=WP_H, verify=False, timeout=15)
src_urls['section2'] = mr.json().get('source_url', '')
print(f'  section2: kept ID=42188  {src_urls["section2"].split("/")[-1]}')

# ── PATCH POST 42177 ──────────────────────────────────────────────────────────
if 'featured' not in results or 'section1' not in results or 'section3' not in results:
    print('\nMissing uploads — abort patch')
else:
    print('\nFetching post 42177...')
    r = requests.get('https://virtina.com/wp-json/wp/v2/posts/42177?context=edit',
                     headers=WP_H, verify=False, timeout=30)
    content = r.json()['content']['raw']

    # Replace old media IDs in content
    old_new = {
        42190: results['featured'],
        42192: results['section1'],
        42188: results['section2'],   # same → no-op
        42193: results['section3'],
    }
    for old, new in old_new.items():
        content = content.replace(f'wp-image-{old}', f'wp-image-{new}')
        content = content.replace(f'data-image-id="{old}"', f'data-image-id="{new}"')
        content = content.replace(f'data-id="{old}"', f'data-id="{new}"')

    # Replace src URLs — pattern covers any filename with the slot dimensions
    old_patterns = {
        'featured': r'volusion-[a-z-]+-featured-1309x500[^"]*\.jpg',
        'section1': r'volusion-[a-z-]+-[a-z-]*section1-670x352[^"]*\.jpg',
        'section2': r'volusion-[a-z-]+-[a-z-]*section2-670x352[^"]*\.jpg',
        'section3': r'volusion-[a-z-]+-[a-z-]*section3-670x352[^"]*\.jpg',
    }
    for name, pattern in old_patterns.items():
        new_src = src_urls.get(name, '')
        if new_src:
            before = content
            content = re.sub(
                r'src="https://virtina\.com/wp-content/uploads/[^"]*' + pattern + '"',
                f'src="{new_src}"',
                content
            )
            print(f'  src [{name}]: {"replaced" if content != before else "not matched — ID replace covered it"}')

    pr = requests.post(
        'https://virtina.com/wp-json/wp/v2/posts/42177',
        headers={**WP_H, 'Content-Type': 'application/json'},
        json={'content': content, 'featured_media': results['featured'], 'status': 'draft'},
        verify=False, timeout=60,
    )
    d = pr.json()
    print(f'\nPost patch: {pr.status_code} | featured_media={d.get("featured_media")}')

    if pr.status_code == 200:
        print('\nAll images updated:')
        print(f'  featured : ID={results["featured"]}  {src_urls["featured"].split("/")[-1]}')
        print(f'  section1 : ID={results["section1"]}  {src_urls["section1"].split("/")[-1]}')
        print(f'  section2 : ID={results["section2"]}  kept')
        print(f'  section3 : ID={results["section3"]}  {src_urls["section3"].split("/")[-1]}')
