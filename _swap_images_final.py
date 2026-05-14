"""
Final image replacement for Virtina Volusion post (ID 42177).

Selected images from Openverse (CC-BY licensed, Flickr):
- Featured : smiling businessman at laptop — upgrade _b to _k (2048px) for sharpness
- Section 1: woman at work with laptop — professional computing context
- Section 2: business people in a meeting — team planning context
- Section 3: happy businesswoman — smiling success context

Body images are 1024px source -> downscaled to 670px = crisp (no upscaling).
Featured tries multiple _k.jpg candidates (2048px) -> no upscaling needed.
"""
import requests, base64, io, re
import urllib3
urllib3.disable_warnings()
from PIL import Image

creds = base64.b64encode(b'anujith:Mibz 1h3E jWRi bfJs WAXZ rwrM').decode()
WP_H = {'Authorization': f'Basic {creds}'}
DL_H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def download(url, min_w=0, min_kb=30):
    try:
        r = requests.get(url, timeout=25, verify=False, headers=DL_H)
        if r.status_code == 200 and len(r.content) >= min_kb * 1024:
            img = Image.open(io.BytesIO(r.content)).convert('RGB')
            if img.size[0] >= min_w:
                print(f'  Got: {img.size[0]}x{img.size[1]}  {len(r.content)//1024}KB  {url.split("/")[-1]}')
                return img
    except Exception as e:
        print(f'  Error {url.split("/")[-1]}: {e}')
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
    img.save(buf, 'JPEG', quality=85, optimize=True)
    buf.seek(0)
    return buf

def wp_upload(buf, filename, alt, title):
    uh = {**WP_H,
          'Content-Disposition': f'attachment; filename="{filename}"',
          'Content-Type': 'image/jpeg'}
    r = requests.post('https://virtina.com/wp-json/wp/v2/media',
                      headers=uh, data=buf.getvalue(), verify=False, timeout=60)
    if r.status_code not in [200, 201]:
        print(f'  Upload fail {r.status_code}: {r.text[:80]}')
        return None, ''
    d = r.json()
    mid = d['id']
    src = d.get('source_url', '')
    sz  = d.get('media_details', {}).get('filesize', 0) // 1024
    requests.post(f'https://virtina.com/wp-json/wp/v2/media/{mid}',
                  headers={**WP_H, 'Content-Type': 'application/json'},
                  json={'alt_text': alt, 'title': title},
                  verify=False, timeout=20)
    print(f'  Uploaded ID={mid}  {sz}KB  {src.split("/")[-1]}')
    return mid, src

# ══════════════════════════════════════════════════════════════════════════════
# IMAGE CANDIDATES (from Openverse search results above)
# ══════════════════════════════════════════════════════════════════════════════

# Featured: smiling businessman at laptop
# Try _k.jpg (2048px) on several candidates; fall back to _b.jpg only if needed
FEATURED_CANDIDATES = [
    'https://live.staticflickr.com/65535/48063963308_ee9c1575c4_k.jpg',  # try 2048px
    'https://live.staticflickr.com/7820/47505938771_0eb243bf76_k.jpg',
    'https://live.staticflickr.com/65535/48105529121_68a79ce4f6_k.jpg',
    'https://live.staticflickr.com/4823/45739275642_5df3183d07_k.jpg',
    'https://live.staticflickr.com/65535/49107115366_cbd00d6237_k.jpg',
    # _h.jpg fallback (1600px)
    'https://live.staticflickr.com/65535/48063963308_ee9c1575c4_h.jpg',
    'https://live.staticflickr.com/7820/47505938771_0eb243bf76_h.jpg',
    'https://live.staticflickr.com/4823/45739275642_5df3183d07_h.jpg',
]

# Section 1: professional working at laptop (1024px _b — downscale to 670px)
SECTION1_CANDIDATES = [
    'https://live.staticflickr.com/3907/14408940363_2c187fa1f5_b.jpg',  # Woman at work
    'https://live.staticflickr.com/65535/48063963308_ee9c1575c4_b.jpg',  # smiling businessman
    'https://live.staticflickr.com/4823/45739275642_5df3183d07_b.jpg',   # happy businesswoman
    'https://live.staticflickr.com/65535/48105529121_68a79ce4f6_b.jpg',
]

# Section 2: business team meeting / collaboration
SECTION2_CANDIDATES = [
    'https://live.staticflickr.com/4840/30849318147_5f54060204_b.jpg',   # Business people in a meeting
    'https://live.staticflickr.com/1902/45789230251_f9b8096a2d_b.jpg',   # Two people fist bump / collaboration
    'https://live.staticflickr.com/65535/52969639648_dd36a09cf9_b.jpg',  # Engaged female in virtual meeting
    'https://live.staticflickr.com/2891/11123538363_07bb05134a_b.jpg',   # Business team
]

# Section 3: smiling happy person — success after migration
SECTION3_CANDIDATES = [
    'https://live.staticflickr.com/4896/30849316687_833aa1ce06_b.jpg',   # Cheerful woman holding AT sign
    'https://live.staticflickr.com/65535/45739275442_b936dc3980_b.jpg',  # smiling professional
    'https://live.staticflickr.com/65535/49107115366_cbd00d6237_b.jpg',  # smiling businessman
    'https://live.staticflickr.com/3725/9787766243_03f0344bab_b.jpg',    # Smile!
]

slots = [
    {
        'name': 'featured', 'tw': 1309, 'th': 500, 'min_w': 1310,
        'candidates': FEATURED_CANDIDATES,
        'filename': 'volusion-migration-featured-1309x500.jpg',
        'alt': 'Smiling business professional at laptop reviewing eCommerce dashboard after successful Volusion to WooCommerce migration',
        'title': 'Confident business professional — Volusion to WooCommerce migration',
    },
    {
        'name': 'section1', 'tw': 670, 'th': 352, 'min_w': 670,
        'candidates': SECTION1_CANDIDATES,
        'filename': 'volusion-migration-section1-670x352.jpg',
        'alt': 'Business professional focused at laptop reviewing eCommerce platform costs and billing, evaluating Volusion migration options',
        'title': 'eCommerce merchant reviewing platform costs — Volusion migration decision',
    },
    {
        'name': 'section2', 'tw': 670, 'th': 352, 'min_w': 670,
        'candidates': SECTION2_CANDIDATES,
        'filename': 'volusion-migration-section2-670x352.jpg',
        'alt': 'Business team collaborating in office meeting to plan eCommerce platform migration strategy from Volusion to WooCommerce',
        'title': 'Business team planning eCommerce platform migration to WooCommerce',
    },
    {
        'name': 'section3', 'tw': 670, 'th': 352, 'min_w': 670,
        'candidates': SECTION3_CANDIDATES,
        'filename': 'volusion-migration-section3-670x352.jpg',
        'alt': 'Happy smiling business professional reviewing eCommerce sales growth and analytics results after successful WooCommerce migration from Volusion',
        'title': 'Smiling business professional reviewing WooCommerce results after Volusion migration',
    },
]

results = {}
src_urls = {}

for slot in slots:
    print(f'\n{slot["name"].upper()} ({slot["tw"]}x{slot["th"]})')
    for url in slot['candidates']:
        img = download(url, min_w=slot['min_w'])
        if img:
            buf = crop_resize(img, slot['tw'], slot['th'])
            out_kb = len(buf.getvalue()) // 1024
            print(f'  Resized: {slot["tw"]}x{slot["th"]}  {out_kb}KB')
            mid, src = wp_upload(buf, slot['filename'], slot['alt'], slot['title'])
            if mid:
                results[slot['name']] = mid
                src_urls[slot['name']] = src
                break
    if slot['name'] not in results:
        print(f'  FAILED — no candidate worked')

print(f'\nResults ({len(results)}/4): {results}')

if len(results) < 4:
    missing = [s['name'] for s in slots if s['name'] not in results]
    print(f'Missing: {missing}. Post not patched.')
else:
    print('\nPatching post 42177...')
    r = requests.get('https://virtina.com/wp-json/wp/v2/posts/42177?context=edit',
                     headers=WP_H, verify=False, timeout=30)
    content = r.json()['content']['raw']

    old_ids = {42178: results['featured'], 42179: results['section1'],
               42180: results['section2'], 42181: results['section3']}
    for old, new in old_ids.items():
        content = content.replace(f'wp-image-{old}', f'wp-image-{new}')
        content = content.replace(f'data-image-id="{old}"', f'data-image-id="{new}"')
        content = content.replace(f'data-id="{old}"', f'data-id="{new}"')

    # Replace image src URLs using pattern match on old filenames
    old_patterns = {
        'featured': r'volusion-[a-z-]+-featured-1309x500[^"]*\.jpg',
        'section1': r'volusion-[a-z-]+-section1-670x352[^"]*\.jpg',
        'section2': r'volusion-[a-z-]+-section2-670x352[^"]*\.jpg',
        'section3': r'volusion-[a-z-]+-section3-670x352[^"]*\.jpg',
    }
    for name, pattern in old_patterns.items():
        new_src = src_urls.get(name, '')
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
    if pr.status_code == 200:
        print('\nAll 4 images replaced. Post still draft.')
        for name, mid in results.items():
            print(f'  {name}: ID={mid}  {src_urls[name].split("/")[-1]}')
