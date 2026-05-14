"""
Finish Virtina post 42177 image replacement.
Sections 1-3 already uploaded: IDs 42187, 42188, 42189.
Featured: use Wikimedia Commons 6016x4016 landscape image (CC BY-SA).
Then patch post 42177 replacing all old IDs and src URLs.
"""
import requests, base64, io, re
import urllib3
urllib3.disable_warnings()
from PIL import Image

creds = base64.b64encode(b'anujith:Mibz 1h3E jWRi bfJs WAXZ rwrM').decode()
WP_H = {'Authorization': f'Basic {creds}'}
DL_H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def download(url, min_kb=500):
    r = requests.get(url, timeout=120, verify=False, headers=DL_H)
    if r.status_code == 200 and len(r.content) >= min_kb * 1024:
        img = Image.open(io.BytesIO(r.content)).convert('RGB')
        print(f'  Downloaded: {img.size[0]}x{img.size[1]}  {len(r.content)//1024}KB')
        return img
    print(f'  Download failed: {r.status_code}  {len(r.content)//1024}KB')
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
                      headers=uh, data=buf.getvalue(), verify=False, timeout=90)
    if r.status_code not in [200, 201]:
        print(f'  Upload fail {r.status_code}: {r.text[:100]}')
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

# ── FEATURED IMAGE ────────────────────────────────────────────────────────────
print('FEATURED (1309x500) - Wikimedia Commons landscape business professional')

WIKIMEDIA_URL = 'https://upload.wikimedia.org/wikipedia/commons/e/e9/Business_professional_engages_in_note-taking_during_a_meeting_at_a_modern_office_desk.jpg'

img = download(WIKIMEDIA_URL)
assert img, 'Featured image download failed'

buf = crop_resize(img, 1309, 500)
print(f'  Resized: 1309x500  {len(buf.getvalue())//1024}KB')

feat_id, feat_src = wp_upload(
    buf,
    'volusion-migration-featured-1309x500.jpg',
    'Business professional reviewing eCommerce options at a modern office desk, evaluating Volusion to WooCommerce migration strategy',
    'Business professional at office desk — Volusion to WooCommerce migration',
)
assert feat_id, 'Featured upload failed'

# ── SECTIONS ALREADY UPLOADED ─────────────────────────────────────────────────
section_ids = {
    'section1': 42187,
    'section2': 42188,
    'section3': 42189,
}

# Fetch their src URLs
src_map = {'featured': feat_src}
for name, mid in section_ids.items():
    mr = requests.get(f'https://virtina.com/wp-json/wp/v2/media/{mid}',
                      headers=WP_H, verify=False, timeout=15)
    src_map[name] = mr.json().get('source_url', '')
    print(f'  {name}: ID={mid}  {src_map[name].split("/")[-1]}')

# ── PATCH POST 42177 ──────────────────────────────────────────────────────────
print('\nFetching post 42177 content...')
r = requests.get('https://virtina.com/wp-json/wp/v2/posts/42177?context=edit',
                 headers=WP_H, verify=False, timeout=30)
content = r.json()['content']['raw']

# Replace old media IDs
old_new = {
    42178: feat_id,
    42179: section_ids['section1'],
    42180: section_ids['section2'],
    42181: section_ids['section3'],
}
for old, new in old_new.items():
    content = content.replace(f'wp-image-{old}', f'wp-image-{new}')
    content = content.replace(f'data-image-id="{old}"', f'data-image-id="{new}"')
    content = content.replace(f'data-id="{old}"', f'data-id="{new}"')

# Replace src URLs — pattern matches any versioned filename with old slot names
old_patterns = {
    'featured': r'volusion-(?:woocommerce-)?migration-featured-1309x500[^"]*\.jpg',
    'section1': r'volusion-(?:woocommerce-)?migration-section1-670x352[^"]*\.jpg',
    'section2': r'volusion-(?:woocommerce-)?migration-section2-670x352[^"]*\.jpg',
    'section3': r'volusion-(?:woocommerce-)?migration-section3-670x352[^"]*\.jpg',
}
for name, pattern in old_patterns.items():
    new_src = src_map.get(name, '')
    if new_src:
        before = content
        content = re.sub(
            r'src="https://virtina\.com/wp-content/uploads/[^"]*' + pattern + '"',
            f'src="{new_src}"',
            content
        )
        changed = content != before
        print(f'  src replace [{name}]: {"replaced" if changed else "pattern not matched"}')

# Push patch
pr = requests.post(
    'https://virtina.com/wp-json/wp/v2/posts/42177',
    headers={**WP_H, 'Content-Type': 'application/json'},
    json={'content': content, 'featured_media': feat_id, 'status': 'draft'},
    verify=False, timeout=60
)
d = pr.json()
print(f'\nPost patch: {pr.status_code} | featured_media={d.get("featured_media")}')

if pr.status_code == 200:
    print('\nAll 4 images replaced successfully:')
    print(f'  featured : ID={feat_id}  {feat_src.split("/")[-1]}')
    for name, mid in section_ids.items():
        print(f'  {name}: ID={mid}  {src_map[name].split("/")[-1]}')
    print('\nPost remains draft. Yoast fields must be set manually in WP dashboard.')
