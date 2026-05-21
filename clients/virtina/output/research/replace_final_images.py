"""
FINAL image replacement for post 42202 — IDs verified by visual inspection.
Uses Pexels CDN at w=1920 for max resolution, no API key needed.

Featured  1309x500  old=42216  id=3182812  diverse team smiling at laptop in office
Body1     670x352   old=42217  id=6476588   iMac with analytics dashboard (portal features section)
Body2     670x352   old=42218  id=5325076   overhead team meeting with laptops (cost/timeline)
Body3     670x352   old=42219  id=7654203   woman in blazer at laptop (buyer adoption)
"""
import os, re, io, requests, base64, urllib3
from PIL import Image

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WP_URL       = "https://virtina.com/wp-json/wp/v2"
USERNAME     = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
POST_ID      = 42202

token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
wp_headers = {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

SESS = requests.Session()
SESS.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
SESS.verify = False

# High-res Pexels CDN — no API key needed
CDN = "https://images.pexels.com/photos/{id}/pexels-photo-{id}.jpeg?auto=compress&cs=tinysrgb&w=1920&dpr=1"

SLOTS = [
    {
        "name": "featured", "pexels_id": 3182812,
        "w": 1309, "h": 500, "max_kb": 400, "old_id": 42216,
        "filename": "woocommerce-b2b-portal-featured-1309x500-v3.jpg",
        "alt": (
            "Diverse B2B ecommerce team collaborating at a laptop in a modern office, "
            "reviewing WooCommerce customer portal features together"
        ),
        "logo": True,
    },
    {
        "name": "body1", "pexels_id": 6476588,
        "w": 670, "h": 352, "max_kb": 200, "old_id": 42217,
        "filename": "woocommerce-b2b-portal-body1-670x352-v4.jpg",
        "alt": (
            "iMac desktop displaying a business analytics dashboard representing the "
            "real-time data and order management features of a WooCommerce B2B customer portal"
        ),
        "logo": False,
    },
    {
        "name": "body2", "pexels_id": 5325076,
        "w": 670, "h": 352, "max_kb": 200, "old_id": 42218,
        "filename": "woocommerce-b2b-portal-body2-670x352-v3.jpg",
        "alt": (
            "Business team gathered around a conference table with laptops and tablets "
            "discussing WooCommerce B2B portal implementation timeline and costs"
        ),
        "logo": False,
    },
    {
        "name": "body3", "pexels_id": 7654203,
        "w": 670, "h": 352, "max_kb": 200, "old_id": 42219,
        "filename": "woocommerce-b2b-portal-body3-670x352-v4.jpg",
        "alt": (
            "B2B procurement buyer using a laptop to place a repeat order on a "
            "WooCommerce self-service portal, without needing to call a sales rep"
        ),
        "logo": False,
    },
]


# ── Logo helpers ────────────────────────────────────────────────────────────

def fetch_logo():
    r = SESS.get("https://virtina.com/wp-content/uploads/2026/03/cropped-logo-2.webp", timeout=20)
    if r.status_code != 200:
        return None
    img = Image.open(io.BytesIO(r.content)).convert("RGBA")
    # White/near-white bg → transparent; dark navy text → white; teal stays
    px = list(img.getdata())
    new_px = []
    for r2, g, b, a in px:
        if r2 > 220 and g > 220 and b > 220:
            new_px.append((255, 255, 255, 0))
        elif r2 < 80 and g < 90 and b < 120:
            new_px.append((255, 255, 255, 255))
        else:
            new_px.append((r2, g, b, a))
    img.putdata(new_px)
    print(f"Logo ready: {img.size}")
    return img


def composite_logo(photo_rgb, logo_rgba, padding=28):
    pw, ph = photo_rgb.size
    lw = int(pw * 0.18)
    lh = int(lw / (logo_rgba.width / logo_rgba.height))
    logo = logo_rgba.resize((lw, lh), Image.LANCZOS)
    base = photo_rgb.convert("RGBA")
    # Semi-dark patch behind logo
    x0, y0 = pw - lw - padding - 12, ph - lh - padding - 12
    patch = base.crop((x0, y0, x0 + lw + 24, y0 + lh + 24))
    dark = Image.new("RGBA", patch.size, (0, 0, 0, 100))
    patch = Image.alpha_composite(patch, dark)
    base.paste(patch, (x0, y0))
    base.paste(logo, (pw - lw - padding, ph - lh - padding), logo)
    return base.convert("RGB")


# ── Core download + resize ───────────────────────────────────────────────────

def download(pexels_id):
    url = CDN.format(id=pexels_id)
    r = SESS.get(url, timeout=40, allow_redirects=True)
    print(f"  [{pexels_id}] {r.status_code} {len(r.content)//1024}KB")
    if r.status_code != 200 or len(r.content) < 30000:
        return None
    return Image.open(io.BytesIO(r.content)).convert("RGB")


def crop_resize(img, tw, th):
    ow, oh = img.size
    if ow / oh > tw / th:
        nh, nw = th, int(ow * th / oh)
    else:
        nw, nh = tw, int(oh * tw / ow)
    img = img.resize((nw, nh), Image.LANCZOS)
    l, t = (nw - tw) // 2, (nh - th) // 2
    return img.crop((l, t, l + tw, t + th))


def encode(img, max_kb):
    for q in [85, 80, 75]:
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=q, optimize=True)
        if buf.tell() <= max_kb * 1024:
            print(f"  Encoded {img.size} {buf.tell()//1024}KB q={q}")
            return buf.getvalue()
    return None


def upload(img_bytes, filename, alt):
    mh = {
        "Authorization": f"Basic {token}",
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "image/jpeg",
    }
    r = requests.post(f"{WP_URL}/media", data=img_bytes, headers=mh, verify=False, timeout=60)
    if r.status_code not in (200, 201):
        print(f"  Upload error {r.status_code}: {r.text[:150]}")
        return None, None
    mid, src = r.json()["id"], r.json()["source_url"]
    requests.post(f"{WP_URL}/media/{mid}", json={"alt_text": alt},
                  headers=wp_headers, verify=False, timeout=20)
    print(f"  Uploaded: id={mid}  {src}")
    return mid, src


# ── Main ────────────────────────────────────────────────────────────────────

logo = fetch_logo()
results = {}

for slot in SLOTS:
    print(f"\n{'='*55}\n{slot['name'].upper()}  pexels={slot['pexels_id']}  {slot['w']}x{slot['h']}\n{'='*55}")
    img = download(slot["pexels_id"])
    if not img:
        print("  FAILED: download")
        results[slot["name"]] = None
        continue
    print(f"  Source: {img.size}")
    img = crop_resize(img, slot["w"], slot["h"])
    if slot["logo"] and logo:
        img = composite_logo(img, logo.copy())
        print("  Logo composited")
    img_bytes = encode(img, slot["max_kb"])
    if not img_bytes:
        print("  FAILED: encode")
        results[slot["name"]] = None
        continue
    mid, src = upload(img_bytes, slot["filename"], slot["alt"])
    if not mid:
        results[slot["name"]] = None
        continue
    results[slot["name"]] = {"media_id": mid, "src_url": src, "alt": slot["alt"],
                              "old_id": slot["old_id"], "w": slot["w"], "h": slot["h"]}
    print(f"  SUCCESS -> media_id={mid}")

# ── Patch HTML + featured_media ─────────────────────────────────────────────
html_path = os.path.join(os.path.dirname(__file__), "final_html_v6.html")
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

for slot in SLOTS:
    name = slot["name"]
    r = results.get(name)
    if not r or name == "featured":
        continue
    new_span = (
        f'<span style="display:block;margin:20px 0;">'
        f'<img alt="{r["alt"]}" data-id="{r["media_id"]}" '
        f'width="{r["w"]}" data-init-width="{r["w"]}" '
        f'height="{r["h"]}" data-init-height="{r["h"]}" '
        f'title="" loading="lazy" src="{r["src_url"]}" '
        f'data-width="{r["w"]}" data-height="{r["h"]}" '
        f'style="aspect-ratio: auto {r["w"]} / {r["h"]};max-width:100%;"></span>'
    )
    pat = re.compile(rf'<span[^>]*>\s*<img[^>]*data-id="{slot["old_id"]}"[^>]*>\s*</span>', re.DOTALL)
    if pat.search(content):
        content = pat.sub(new_span, content)
        print(f"\nReplaced {name} span (data-id={slot['old_id']})")
    else:
        print(f"\nWARNING: {name} span not found (data-id={slot['old_id']})")

v8_path = os.path.join(os.path.dirname(__file__), "final_html_v8.html")
with open(v8_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Saved final_html_v8.html")

patch_payload = {"content": content}
feat = results.get("featured")
if feat:
    patch_payload["featured_media"] = feat["media_id"]

resp = requests.patch(
    f"{WP_URL}/posts/{POST_ID}", json=patch_payload,
    headers=wp_headers, verify=False, timeout=60,
)
print(f"\nPATCH status: {resp.status_code}")
if resp.status_code == 200:
    rdata = resp.json()
    rendered = rdata["content"]["rendered"]
    for slot in SLOTS:
        r = results.get(slot["name"])
        if r:
            live = str(r["media_id"]) in rendered or slot["name"] == "featured"
            gone = f'data-id="{slot["old_id"]}"' not in rendered or slot["name"] == "featured"
            print(f"  {slot['name']}: live={live} old_gone={gone}")
    if feat:
        print(f"  featured_media live: {rdata.get('featured_media') == feat['media_id']}")
    print(f"  Post status: {rdata.get('status')}")
    print("Done.")
else:
    print(f"Error: {resp.text[:300]}")
