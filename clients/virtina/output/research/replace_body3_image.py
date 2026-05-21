import os, re, requests, base64, io
import urllib3
from PIL import Image

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WP_URL       = "https://virtina.com/wp-json/wp/v2"
USERNAME     = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
POST_ID      = 42202

TARGET_W, TARGET_H = 670, 352
JPEG_Q  = 82
MAX_BYTES = 200 * 1024

token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
wp_headers = {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

ALT_TEXT = (
    "B2B buyer reviewing contract pricing and order history inside a "
    "WooCommerce self-service customer portal on a laptop in a professional office"
)

# Openverse sources that serve from their own CDNs (not stocksnap)
SOURCES = ["rawpixel", "flickr", "nappy", "wordpress"]

QUERIES = [
    "business person laptop office",
    "professional computer desk work",
    "laptop screen office business",
    "person computer office work",
    "business laptop screen",
]

SKIP_TAGS = {"nature", "flower", "tree", "mountain", "water", "ocean",
             "forest", "animal", "cat", "dog", "food", "baby", "wedding"}

def search_openverse(query, source, per_page=10):
    try:
        r = requests.get(
            "https://api.openverse.org/v1/images/",
            params={"q": query, "source": source, "license_type": "commercial",
                    "per_page": per_page, "mature": "false"},
            timeout=20, verify=False
        )
        if r.status_code != 200:
            return []
        return r.json().get("results", [])
    except Exception as e:
        print(f"    Openverse/{source} error: {e}")
        return []

def is_relevant(item):
    tags = {t.get("name","").lower() for t in item.get("tags", [])}
    title = (item.get("title") or "").lower()
    if tags & SKIP_TAGS:
        return False
    bad_words = {"nature", "flower", "landscape", "animal", "food", "wedding"}
    if any(w in title for w in bad_words):
        return False
    return True

def process_image(url):
    try:
        r = requests.get(url, timeout=30, verify=False, allow_redirects=True,
                         headers={"User-Agent": "Mozilla/5.0 (compatible; ContentBot/1.0)"})
        print(f"    {r.status_code} ({len(r.content)//1024}KB) <- {url[:70]}")
        if r.status_code != 200 or len(r.content) < 15000:
            return None
        img = Image.open(io.BytesIO(r.content)).convert("RGB")
        orig_w, orig_h = img.size
        print(f"    Source size: {orig_w}x{orig_h}")
        if orig_w < 1200 or orig_h < 400:
            print(f"    SKIP — too small")
            return None
        # Crop-resize
        tgt_ratio = TARGET_W / TARGET_H
        src_ratio = orig_w / orig_h
        if src_ratio > tgt_ratio:
            new_h = TARGET_H
            new_w = int(orig_w * (TARGET_H / orig_h))
        else:
            new_w = TARGET_W
            new_h = int(orig_h * (TARGET_W / orig_w))
        img = img.resize((new_w, new_h), Image.LANCZOS)
        left = (new_w - TARGET_W) // 2
        top  = (new_h - TARGET_H) // 2
        img = img.crop((left, top, left + TARGET_W, top + TARGET_H))
        for q in [JPEG_Q, 75, 70]:
            buf = io.BytesIO()
            img.save(buf, "JPEG", quality=q, optimize=True)
            if buf.tell() <= MAX_BYTES:
                print(f"    Output: {TARGET_W}x{TARGET_H}, {buf.tell()//1024}KB, q={q}")
                return buf.getvalue()
        return None
    except Exception as e:
        print(f"    Exception: {e}")
        return None

def upload_media(img_bytes, filename):
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
    requests.post(f"{WP_URL}/media/{mid}", json={"alt_text": ALT_TEXT},
                  headers=wp_headers, verify=False, timeout=20)
    print(f"Uploaded: media_id={mid}  {src}")
    return mid, src

# ── Search across multiple sources ────────────────────────────────────────────
img_bytes = None
chosen_url = None

for query in QUERIES:
    for source in SOURCES:
        print(f"\n[{source}] '{query}'")
        items = search_openverse(query, source, per_page=10)
        if not items:
            print("  No results.")
            continue
        print(f"  {len(items)} results")
        for item in items:
            if not is_relevant(item):
                continue
            url  = item.get("url", "")
            meta_w = item.get("width", 0)
            if not url:
                continue
            # Build list of URLs to try (highest-res first)
            urls_to_try = []
            if "editor_1024" in url:
                urls_to_try.append(url.replace("editor_1024", "editor_2048"))
                urls_to_try.append(url.replace("editor_1024", "editor_original"))
            urls_to_try.append(url)
            print(f"  w={meta_w} {url[:65]}")
            result = None
            for try_url in urls_to_try:
                result = process_image(try_url)
                if result:
                    url = try_url
                    break
            if result:
                img_bytes = result
                chosen_url = url
                break
        if img_bytes:
            break
    if img_bytes:
        break

if not img_bytes:
    print("\nAll sources exhausted — no suitable HD image found.")
    exit(1)

print(f"\nSelected: {chosen_url}")
media_id, src_url = upload_media(img_bytes, "woocommerce-b2b-portal-body3-670x352-v2.jpg")
if not media_id:
    print("Upload failed.")
    exit(1)

# ── Build new Template G span ─────────────────────────────────────────────────
new_span = (
    f'<span style="display:block;margin:20px 0;">'
    f'<img alt="{ALT_TEXT}" '
    f'data-id="{media_id}" '
    f'width="{TARGET_W}" data-init-width="{TARGET_W}" '
    f'height="{TARGET_H}" data-init-height="{TARGET_H}" '
    f'title="" loading="lazy" '
    f'src="{src_url}" '
    f'data-width="{TARGET_W}" data-height="{TARGET_H}" '
    f'style="aspect-ratio: auto {TARGET_W} / {TARGET_H};max-width:100%;">'
    f'</span>'
)

html_path = os.path.join(os.path.dirname(__file__), "final_html_v4.html")
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

old_pat = re.compile(r'<span[^>]*>\s*<img[^>]*data-id="42205"[^>]*>\s*</span>', re.DOTALL)
if old_pat.search(content):
    content = old_pat.sub(new_span, content)
    print("Replaced body3 span (by data-id=42205)")
else:
    old_src = re.compile(r'<span[^>]*>\s*<img[^>]*body3[^"]*"[^>]*>\s*</span>', re.DOTALL)
    if old_src.search(content):
        content = old_src.sub(new_span, content)
        print("Replaced body3 span (by src filename)")
    else:
        print("WARNING: could not find old body3 span — appending manually")

v5_path = os.path.join(os.path.dirname(__file__), "final_html_v5.html")
with open(v5_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Saved final_html_v5.html")

resp = requests.patch(
    f"{WP_URL}/posts/{POST_ID}",
    json={"content": content},
    headers=wp_headers,
    verify=False,
    timeout=60,
)
print(f"PATCH status: {resp.status_code}")
if resp.status_code == 200:
    rendered = resp.json()["content"]["rendered"]
    print(f"New media ID live: {str(media_id) in rendered}")
    print(f"Old ID 42205 gone: {'data-id=\"42205\"' not in rendered}")
    print(f"Post status: {resp.json()['status']}")
    print("Done.")
else:
    print(f"Error: {resp.text[:300]}")
