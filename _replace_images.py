import requests, base64, io, json, time, re
import urllib3
urllib3.disable_warnings()
from PIL import Image

creds = base64.b64encode(b'anujith:Mibz 1h3E jWRi bfJs WAXZ rwrM').decode()
WP_H = {'Authorization': f'Basic {creds}'}

def search_ov(query, min_w=1400, sources='rawpixel,stocksnap,nappy'):
    params = {'q': query, 'license_type': 'commercial', 'page_size': 30, 'source': sources}
    try:
        r = requests.get('https://api.openverse.org/v1/images/', params=params,
                         timeout=15, verify=False)
        hits = r.json().get('results', [])
        return [h for h in hits if (h.get('width') or 0) >= min_w]
    except Exception as e:
        print(f'  OV error: {e}')
        return []

def best_hit(results):
    return max(results, key=lambda h: (h.get('width') or 0)) if results else None

def download_img(url):
    try:
        r = requests.get(url, timeout=25, verify=False,
                         headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200 and len(r.content) > 20000:
            img = Image.open(io.BytesIO(r.content)).convert('RGB')
            return img, r.content
    except Exception as e:
        print(f'  DL error: {e}')
    return None, None

def crop_resize(img, tw, th, quality=85):
    sw, sh = img.size
    if sw / sh > tw / th:
        nw = int(sh * tw / th)
        left = (sw - nw) // 2
        img = img.crop((left, 0, left + nw, sh))
    else:
        nh = int(sw * th / tw)
        top = (sh - nh) // 2
        img = img.crop((0, top, sw, top + nh))
    img = img.resize((tw, th), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, 'JPEG', quality=quality, optimize=True)
    buf.seek(0)
    return buf

def wp_upload(buf, filename, alt, title):
    uh = dict(WP_H)
    uh['Content-Disposition'] = f'attachment; filename="{filename}"'
    uh['Content-Type'] = 'image/jpeg'
    r = requests.post('https://virtina.com/wp-json/wp/v2/media',
                      headers=uh, data=buf.getvalue(), verify=False, timeout=60)
    if r.status_code not in [200, 201]:
        print(f'  Upload fail {r.status_code}: {r.text[:100]}')
        return None
    mid = r.json()['id']
    src = r.json().get('source_url', '')
    sz = r.json().get('media_details', {}).get('filesize', 0)
    requests.post(f'https://virtina.com/wp-json/wp/v2/media/{mid}',
                  headers={**WP_H, 'Content-Type': 'application/json'},
                  json={'alt_text': alt, 'title': title}, verify=False, timeout=20)
    print(f'  Uploaded ID={mid}  {sz//1024}KB  {src.split("/")[-1]}')
    return mid

slots = [
    {
        'name': 'featured', 'tw': 1309, 'th': 500, 'min_w': 2000,
        'filename': 'volusion-migration-featured-1309x500.jpg',
        'alt': 'Smiling business professional reviewing WooCommerce eCommerce dashboard on laptop after successful Volusion migration',
        'title': 'Volusion to WooCommerce migration — confident business professional',
        'queries': [
            'smiling businessman laptop office',
            'happy business professional laptop',
            'business man smiling computer',
            'confident entrepreneur laptop desk',
        ],
    },
    {
        'name': 'section1', 'tw': 670, 'th': 352, 'min_w': 1400,
        'filename': 'volusion-migration-section1-670x352.jpg',
        'alt': 'Business professional reviewing eCommerce billing and platform costs on computer, evaluating Volusion migration options',
        'title': 'eCommerce merchant reviewing platform costs for Volusion migration decision',
        'queries': [
            'business professional working laptop office',
            'man working computer office desk',
            'business owner laptop focused',
            'professional man computer screen office',
        ],
    },
    {
        'name': 'section2', 'tw': 670, 'th': 352, 'min_w': 1400,
        'filename': 'volusion-migration-section2-670x352.jpg',
        'alt': 'Business team planning eCommerce platform migration strategy in office, discussing WooCommerce transition steps together',
        'title': 'Business team planning eCommerce platform migration to WooCommerce',
        'queries': [
            'business team meeting office smiling',
            'business people discussion planning office',
            'team office meeting professional',
            'business colleagues office discussion smiling',
        ],
    },
    {
        'name': 'section3', 'tw': 670, 'th': 352, 'min_w': 1400,
        'filename': 'volusion-migration-section3-670x352.jpg',
        'alt': 'Happy smiling business owner reviewing eCommerce analytics and sales growth on laptop after successful WooCommerce migration',
        'title': 'Smiling business owner reviewing WooCommerce results after Volusion migration',
        'queries': [
            'smiling business owner laptop',
            'happy entrepreneur laptop success',
            'business woman smiling laptop',
            'smiling professional laptop computer',
        ],
    },
]

results = {}

for slot in slots:
    print(f'\n{slot["name"].upper()} ({slot["tw"]}x{slot["th"]})')
    for q in slot['queries']:
        print(f'  Searching: {q}')
        hits = search_ov(q, slot['min_w'])
        hit = best_hit(hits)
        if hit:
            print(f'  Found: {hit["width"]}x{hit.get("height","?")} px  {hit["url"][:70]}')
            img, raw = download_img(hit['url'])
            if img:
                print(f'  Downloaded: {img.size[0]}x{img.size[1]}  {len(raw)//1024}KB source')
                buf = crop_resize(img, slot['tw'], slot['th'])
                print(f'  Resized to: {slot["tw"]}x{slot["th"]}  {len(buf.getvalue())//1024}KB')
                mid = wp_upload(buf, slot['filename'], slot['alt'], slot['title'])
                if mid:
                    results[slot['name']] = mid
                    break
        time.sleep(0.5)
    if slot['name'] not in results:
        print(f'  FAILED: no image found for {slot["name"]}')

print(f'\nResults: {results}')

if len(results) < 4:
    print(f'Only {len(results)}/4 images found. Missing: {[s["name"] for s in slots if s["name"] not in results]}')
else:
    print('\nPatching post 42177...')
    r = requests.get('https://virtina.com/wp-json/wp/v2/posts/42177?context=edit',
                     headers=WP_H, verify=False, timeout=30)
    content = r.json()['content']['raw']

    old_new = {
        42178: results['featured'],
        42179: results['section1'],
        42180: results['section2'],
        42181: results['section3'],
    }
    for old, new in old_new.items():
        content = content.replace(f'wp-image-{old}', f'wp-image-{new}')
        content = content.replace(f'data-image-id="{old}"', f'data-image-id="{new}"')
        content = content.replace(f'data-id="{old}"', f'data-id="{new}"')

    src_map = {}
    for name, mid in results.items():
        mr = requests.get(f'https://virtina.com/wp-json/wp/v2/media/{mid}',
                          headers=WP_H, verify=False, timeout=15)
        src_map[name] = mr.json().get('source_url', '')

    old_fns = {
        'featured': 'volusion-woocommerce-migration-featured-1309x500-2.jpg',
        'section1': 'volusion-woocommerce-migration-section1-670x352-2.jpg',
        'section2': 'volusion-woocommerce-migration-section2-670x352-2.jpg',
        'section3': 'volusion-woocommerce-migration-section3-670x352-2.jpg',
    }
    for name, old_fn in old_fns.items():
        new_src = src_map.get(name, '')
        if new_src:
            pattern = r'src="https://virtina\.com/wp-content/uploads/[^"]*' + re.escape(old_fn) + '"'
            content = re.sub(pattern, f'src="{new_src}"', content)

    pr = requests.post(
        'https://virtina.com/wp-json/wp/v2/posts/42177',
        headers={**WP_H, 'Content-Type': 'application/json'},
        json={'content': content, 'featured_media': results['featured'], 'status': 'draft'},
        verify=False, timeout=60
    )
    d = pr.json()
    print(f'Post patch: {pr.status_code} | featured_media={d.get("featured_media")}')
