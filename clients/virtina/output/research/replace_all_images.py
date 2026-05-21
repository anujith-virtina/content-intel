"""
Replace ALL images in post 42202 with watermark-free HD images.
Sources: nappy, wordpress (Openverse CC-licensed — no rawpixel, no stocksnap, no flickr).

Image slots:
  featured  : 1309x500  currently 42203
  body1     : 670x352   currently 42214  (section: portal features)
  body2     : 670x352   currently 42204  (section: cost & timeline)
  body3     : 670x352   currently 42212  (section: buyer adoption)
"""
import os, re, requests, base64, io
import urllib3
from PIL import Image

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WP_URL       = "https://virtina.com/wp-json/wp/v2"
USERNAME     = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
POST_ID      = 42202

token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
wp_headers = {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

# Watermark-free Openverse sources only
SOURCES = ["nappy", "wordpress", "wikimedia"]

SKIP_TAGS = {
    "nature", "flower", "tree", "mountain", "water", "ocean", "forest",
    "animal", "cat", "dog", "food", "baby", "wedding", "warehouse",
    "factory", "industrial", "construction", "medical", "hospital",
    "travel", "vacation", "beach"
}
BAD_WORDS = {
    "nature", "flower", "landscape", "animal", "food", "wedding",
    "warehouse", "factory", "worker", "vest", "industrial", "outdoor",
    "medical", "doctor", "beach", "travel"
}

# Each slot: target size, alt text, queries, filename, old_media_id
SLOTS = [
    {
        "name": "featured",
        "w": 1309, "h": 500,
        "alt": (
            "B2B ecommerce manager comparing WooCommerce customer portal "
            "capabilities against a standard account page on a laptop in a modern office"
        ),
        "queries": [
            "professional woman laptop office",
            "business person computer desk",
            "professional man laptop office desk",
            "woman computer office work",
            "business laptop screen professional",
        ],
        "filename": "woocommerce-b2b-portal-featured-1309x500-v2.jpg",
        "old_id": 42203,
        "min_src_w": 1600, "min_src_h": 500,
    },
    {
        "name": "body1",
        "w": 670, "h": 352,
        "alt": (
            "Business buyer logged into a WooCommerce B2B customer portal "
            "viewing contract pricing, order history, and real-time inventory on a desktop"
        ),
        "queries": [
            "woman laptop office screen",
            "professional computer screen work",
            "business person laptop desk",
            "man laptop computer screen office",
            "office professional computer",
        ],
        "filename": "woocommerce-b2b-portal-body1-670x352-v3.jpg",
        "old_id": 42214,
        "min_src_w": 1200, "min_src_h": 400,
    },
    {
        "name": "body2",
        "w": 670, "h": 352,
        "alt": (
            "Small business team discussing WooCommerce B2B portal build timeline "
            "and implementation cost at a conference table with laptops open"
        ),
        "queries": [
            "business team meeting laptop",
            "office team discussion table",
            "professional meeting discussion",
            "business woman man meeting office",
            "team office discussion laptop",
        ],
        "filename": "woocommerce-b2b-portal-body2-670x352-v2.jpg",
        "old_id": 42204,
        "min_src_w": 1200, "min_src_h": 400,
    },
    {
        "name": "body3",
        "w": 670, "h": 352,
        "alt": (
            "B2B buyer self-serving on a WooCommerce customer portal, "
            "placing a repeat order and reviewing contract pricing without calling a sales rep"
        ),
        "queries": [
            "woman online shopping laptop",
            "business person online order computer",
            "professional woman computer shopping",
            "man laptop online business purchase",
            "person computer screen order",
        ],
        "filename": "woocommerce-b2b-portal-body3-670x352-v3.jpg",
        "old_id": 42212,
        "min_src_w": 1200, "min_src_h": 400,
    },
]


def search_openverse(query, source, per_page=20):
    try:
        r = requests.get(
            "https://api.openverse.org/v1/images/",
            params={"q": query, "source": source, "license_type": "commercial",
                    "per_page": per_page, "mature": "false"},
            timeout=20, verify=False
        )
        if r.status_code != 200:
            print(f"    Openverse {r.status_code}")
            return []
        return r.json().get("results", [])
    except Exception as e:
        print(f"    Openverse error: {e}")
        return []


def is_relevant(item):
    tags = {t.get("name", "").lower() for t in item.get("tags", [])}
    title = (item.get("title") or "").lower()
    if tags & SKIP_TAGS:
        return False
    if any(w in title for w in BAD_WORDS):
        return False
    return True


def download_and_process(url, target_w, target_h, min_src_w, min_src_h):
    try:
        r = requests.get(
            url, timeout=30, verify=False, allow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (compatible; ContentBot/1.0)"}
        )
        print(f"    {r.status_code} {len(r.content)//1024}KB <- {url[:70]}")
        if r.status_code != 200 or len(r.content) < 20000:
            return None
        img = Image.open(io.BytesIO(r.content)).convert("RGB")
        orig_w, orig_h = img.size
        print(f"    Source: {orig_w}x{orig_h}")
        if orig_w < min_src_w or orig_h < min_src_h:
            print(f"    SKIP - too small (need {min_src_w}x{min_src_h})")
            return None
        tgt_ratio = target_w / target_h
        src_ratio = orig_w / orig_h
        if src_ratio > tgt_ratio:
            new_h = target_h
            new_w = int(orig_w * (target_h / orig_h))
        else:
            new_w = target_w
            new_h = int(orig_h * (target_w / orig_w))
        img = img.resize((new_w, new_h), Image.LANCZOS)
        left = (new_w - target_w) // 2
        top  = (new_h - target_h) // 2
        img = img.crop((left, top, left + target_w, top + target_h))
        max_bytes = 350 * 1024 if target_w > 900 else 200 * 1024
        for q in [85, 80, 75]:
            buf = io.BytesIO()
            img.save(buf, "JPEG", quality=q, optimize=True)
            if buf.tell() <= max_bytes:
                print(f"    Out: {target_w}x{target_h}, {buf.tell()//1024}KB, q={q}")
                return buf.getvalue()
        return None
    except Exception as e:
        print(f"    Exception: {e}")
        return None


def upload_media(img_bytes, filename, alt_text):
    mh = {
        "Authorization": f"Basic {token}",
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "image/jpeg",
    }
    r = requests.post(f"{WP_URL}/media", data=img_bytes, headers=mh, verify=False, timeout=60)
    if r.status_code not in (200, 201):
        print(f"Upload error {r.status_code}: {r.text[:200]}")
        return None, None
    mid = r.json()["id"]
    src = r.json()["source_url"]
    requests.post(
        f"{WP_URL}/media/{mid}",
        json={"alt_text": alt_text},
        headers=wp_headers, verify=False, timeout=20
    )
    print(f"Uploaded: media_id={mid}  {src}")
    return mid, src


def find_image(slot):
    """Search all sources and queries until we find a usable image for this slot."""
    for query in slot["queries"]:
        for source in SOURCES:
            print(f"\n  [{source}] '{query}'")
            items = search_openverse(query, source, per_page=20)
            if not items:
                print("    No results")
                continue
            print(f"    {len(items)} results")
            for item in items:
                if not is_relevant(item):
                    continue
                url = item.get("url", "")
                if not url:
                    continue
                result = download_and_process(
                    url, slot["w"], slot["h"],
                    slot["min_src_w"], slot["min_src_h"]
                )
                if result:
                    return result, url
    return None, None


# Process each slot
results = {}

for slot in SLOTS:
    print(f"\n{'='*60}")
    print(f"SLOT: {slot['name']} ({slot['w']}x{slot['h']})")
    print(f"{'='*60}")
    img_bytes, chosen_url = find_image(slot)
    if not img_bytes:
        print(f"FAILED to find image for {slot['name']}")
        results[slot["name"]] = None
        continue
    print(f"\nChosen: {chosen_url}")
    media_id, src_url = upload_media(img_bytes, slot["filename"], slot["alt"])
    if not media_id:
        print(f"Upload failed for {slot['name']}")
        results[slot["name"]] = None
        continue
    results[slot["name"]] = {
        "media_id": media_id,
        "src_url": src_url,
        "alt": slot["alt"],
        "old_id": slot["old_id"],
        "w": slot["w"],
        "h": slot["h"],
    }
    print(f"SUCCESS {slot['name']}: media_id={media_id}")

print(f"\n\n{'='*60}")
print("SUMMARY")
print(f"{'='*60}")
for name, r in results.items():
    if r:
        print(f"{name}: old={[s['old_id'] for s in SLOTS if s['name']==name][0]} -> new={r['media_id']}")
    else:
        print(f"{name}: FAILED")

# Check all slots succeeded
failed = [name for name, r in results.items() if r is None]
if failed:
    print(f"\nFailed slots: {failed}")
    print("Patching with whatever succeeded...")

# Load current HTML
html_path = os.path.join(os.path.dirname(__file__), "final_html_v6.html")
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace body images in HTML content
for slot in SLOTS:
    name = slot["name"]
    r = results.get(name)
    if not r or name == "featured":
        continue
    old_id = slot["old_id"]
    new_span = (
        f'<span style="display:block;margin:20px 0;">'
        f'<img alt="{r["alt"]}" '
        f'data-id="{r["media_id"]}" '
        f'width="{r["w"]}" data-init-width="{r["w"]}" '
        f'height="{r["h"]}" data-init-height="{r["h"]}" '
        f'title="" loading="lazy" '
        f'src="{r["src_url"]}" '
        f'data-width="{r["w"]}" data-height="{r["h"]}" '
        f'style="aspect-ratio: auto {r["w"]} / {r["h"]};max-width:100%;">'
        f'</span>'
    )
    pat = re.compile(rf'<span[^>]*>\s*<img[^>]*data-id="{old_id}"[^>]*>\s*</span>', re.DOTALL)
    if pat.search(content):
        content = pat.sub(new_span, content)
        print(f"Replaced {name} span (by data-id={old_id})")
    else:
        print(f"WARNING: could not find {name} span with data-id={old_id}")

v7_path = os.path.join(os.path.dirname(__file__), "final_html_v7.html")
with open(v7_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Saved final_html_v7.html")

# Build PATCH payload — content + featured media if available
patch_payload = {"content": content}
feat = results.get("featured")
if feat:
    patch_payload["featured_media"] = feat["media_id"]

resp = requests.patch(
    f"{WP_URL}/posts/{POST_ID}",
    json=patch_payload,
    headers=wp_headers,
    verify=False,
    timeout=60,
)
print(f"PATCH status: {resp.status_code}")
if resp.status_code == 200:
    rendered = resp.json()["content"]["rendered"]
    for slot in SLOTS:
        r = results.get(slot["name"])
        if r:
            live = str(r["media_id"]) in rendered
            gone = f'data-id="{slot["old_id"]}"' not in rendered
            print(f"  {slot['name']}: new_id_live={live}, old_id_gone={gone}")
    print(f"Post status: {resp.json()['status']}")
    print("Done.")
else:
    print(f"Error: {resp.text[:300]}")
