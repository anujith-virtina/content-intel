"""Download, crop, resize and re-upload replacement images to WordPress."""
import urllib.request, ssl, os, json, base64
from PIL import Image
from io import BytesIO

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

OUT = r"C:\content-intel\clients\virtina\output\research\images"

WP_USER = "anujith"
WP_PASS = "Mibz 1h3E jWRi bfJs WAXZ rwrM"
WP_B64  = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
WP_HEADERS = {"Authorization": f"Basic {WP_B64}"}

REPLACEMENTS = [
    {
        "name":     "featured",
        "url":      "https://cdn.stocksnap.io/img-thumbs/960w/3ZHG0XOIT6.jpg",
        "w": 1309, "h": 500,
        "filename": "seo-platforms-featured.jpg",
        "alt":      "Ecommerce professional reviewing platform interface and SEO settings on laptop screen",
        "old_id":   42344,
    },
    {
        "name":     "body1",
        "url":      "https://cdn.stocksnap.io/img-thumbs/960w/Y01VDYAX63.jpg",
        "w": 670,  "h": 352,
        "filename": "seo-platforms-comparison-desk.jpg",
        "alt":      "Two business professionals reviewing ecommerce platform SEO data and analytics notes with laptops",
        "old_id":   42345,
    },
    {
        "name":     "body2",
        "url":      "https://cdn.stocksnap.io/img-thumbs/960w/Z1ZIMB54UM.jpg",
        "w": 670,  "h": 352,
        "filename": "seo-core-web-vitals-office-team.jpg",
        "alt":      "Business team in professional office discussing Core Web Vitals optimization strategy with laptops",
        "old_id":   42346,
    },
]

def crop_center(img, tw, th):
    sw, sh = img.size
    tr = tw / th
    sr = sw / sh
    if sr > tr:
        nw = int(sh * tr)
        l = (sw - nw) // 2
        img = img.crop((l, 0, l + nw, sh))
    else:
        nh = int(sw / tr)
        t = (sh - nh) // 2
        img = img.crop((0, t, sw, t + nh))
    return img.resize((tw, th), Image.LANCZOS)

def download(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
        return r.read()

def wp_upload(path, filename, alt):
    with open(path, "rb") as f:
        data = f.read()
    hdrs = dict(WP_HEADERS)
    hdrs["Content-Disposition"] = f'attachment; filename="{filename}"'
    hdrs["Content-Type"] = "image/jpeg"
    req = urllib.request.Request(
        "https://virtina.com/wp-json/wp/v2/media",
        data=data, headers=hdrs, method="POST"
    )
    with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
        resp = json.loads(r.read())
    # set alt text
    meta_body = json.dumps({"alt_text": alt}).encode()
    meta_hdrs = dict(WP_HEADERS)
    meta_hdrs["Content-Type"] = "application/json"
    req2 = urllib.request.Request(
        f"https://virtina.com/wp-json/wp/v2/media/{resp['id']}",
        data=meta_body, headers=meta_hdrs, method="POST"
    )
    urllib.request.urlopen(req2, timeout=30, context=ctx).close()
    return resp["id"], resp["source_url"]

results = {}
for item in REPLACEMENTS:
    print(f"\n--- {item['name']} ---")
    print(f"  Downloading from {item['url']}")
    raw = download(item["url"])
    img = Image.open(BytesIO(raw)).convert("RGB")
    img = crop_center(img, item["w"], item["h"])
    path = os.path.join(OUT, item["filename"])
    img.save(path, "JPEG", quality=82, optimize=True)
    sz = os.path.getsize(path) / 1024
    print(f"  Saved {item['filename']} ({item['w']}x{item['h']}, {sz:.0f}KB)")
    print(f"  Uploading to WordPress...")
    new_id, new_url = wp_upload(path, item["filename"], item["alt"])
    print(f"  Uploaded: ID {new_id} -> {new_url}")
    results[item["name"]] = {"old_id": item["old_id"], "new_id": new_id, "url": new_url}

print("\n=== REPLACEMENT IDs ===")
for k, v in results.items():
    print(f"  {k}: old={v['old_id']} -> new={v['new_id']}")
