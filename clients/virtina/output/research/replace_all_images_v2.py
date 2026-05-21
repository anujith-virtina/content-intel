"""
Replace all 4 images in post 42202 using Pexels CDN (no API key — public URLs)
+ Virtina logo composited on featured image.

Slots:
  featured  1309x500  old=42203  section: blog header (needs Virtina logo)
  body1     670x352   old=42214  section: portal features (person using portal/software)
  body2     670x352   old=42204  section: cost & timeline (business planning/meeting)
  body3     670x352   old=42212  section: buyer adoption (person ordering online)
"""
import os, re, io, requests, base64, urllib3
from PIL import Image, ImageFilter

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WP_URL       = "https://virtina.com/wp-json/wp/v2"
USERNAME     = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
POST_ID      = 42202

token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
wp_headers = {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

SESS = requests.Session()
SESS.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
SESS.verify = False

# ---------------------------------------------------------------------------
# Pexels CDN — no API key needed, images are CC0 free
# URL pattern: https://images.pexels.com/photos/{id}/pexels-photo-{id}.jpeg?auto=compress&cs=tinysrgb&w=1260
# ---------------------------------------------------------------------------

PEXELS_CDN = "https://images.pexels.com/photos/{id}/pexels-photo-{id}.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"

# Curated IDs per slot — office/business/professional photography, no nature/warehouse
SLOT_IDS = {
    # Featured: wide team/collaboration scene for WooCommerce B2B portal blog
    "featured": [
        3184418,   # women collaborating at laptop in bright office
        3182812,   # business people reviewing laptop in office
        1181263,   # group of business people in open office
        3183132,   # professional women working at desk
        3184292,   # business team meeting room
        3183153,   # people in modern office with computers
        1181396,   # man using laptop at table (office)
        3760067,   # professional woman at laptop, blazer
        3182813,   # woman looking at laptop screen, office
        3184319,   # people at desk with computers
    ],
    # Body1: someone actively using a software portal/ecommerce dashboard
    "body1": [
        574071,    # woman sitting in front of MacBook, professional
        1181271,   # woman working at laptop, focused
        4491461,   # woman working on laptop at wooden desk
        2381069,   # person using laptop at desk
        3153201,   # MacBook on table, clean desk
        6476254,   # professional working on laptop
        3861969,   # man working with laptop
        1181244,   # business woman with white laptop
        7364107,   # person working on computer
        1181316,   # three men sitting with laptops (portal review)
    ],
    # Body2: business planning, cost discussion, implementation meeting
    "body2": [
        5816297,   # team of professionals discussing at table with laptops
        3183150,   # man and woman looking at screen together
        3182812,   # business group in modern office
        1181316,   # three men at laptops, conference setting
        3184465,   # people in modern open-plan office
        1181388,   # woman presenting in meeting room
        3756165,   # business meeting, whiteboard, team
        1181677,   # person pointing at laptop screen (review)
        5324897,   # team around table with documents
        3184418,   # colleagues sharing laptop screen
    ],
    # Body3: B2B buyer placing online order / self-serving without calling sales
    "body3": [
        3183197,   # two women using computer and laptop
        7654203,   # professional woman on laptop, smiling
        4491461,   # woman working at laptop
        3861969,   # man at laptop, focused on screen
        6476254,   # professional at laptop
        1181271,   # woman using laptop, working
        3760067,   # professional woman laptop
        574071,    # woman at MacBook
        2381069,   # person using laptop to order/work
        1181396,   # man using MacBook
    ],
}

SLOT_META = {
    "featured": {
        "w": 1309, "h": 500, "min_src_w": 1600, "min_src_h": 500,
        "max_kb": 400, "old_id": 42203,
        "filename": "woocommerce-b2b-portal-featured-1309x500-v2.jpg",
        "alt": (
            "Business team reviewing WooCommerce B2B customer portal features "
            "on a laptop in a modern office, with Virtina logo"
        ),
        "logo": True,
    },
    "body1": {
        "w": 670, "h": 352, "min_src_w": 1200, "min_src_h": 400,
        "max_kb": 200, "old_id": 42214,
        "filename": "woocommerce-b2b-portal-body1-670x352-v3.jpg",
        "alt": (
            "B2B procurement professional logged into a WooCommerce customer portal "
            "reviewing contract pricing and order history on a laptop"
        ),
        "logo": False,
    },
    "body2": {
        "w": 670, "h": 352, "min_src_w": 1200, "min_src_h": 400,
        "max_kb": 200, "old_id": 42204,
        "filename": "woocommerce-b2b-portal-body2-670x352-v2.jpg",
        "alt": (
            "Small business team discussing WooCommerce B2B portal implementation "
            "timeline and budget at a conference table with laptops open"
        ),
        "logo": False,
    },
    "body3": {
        "w": 670, "h": 352, "min_src_w": 1200, "min_src_h": 400,
        "max_kb": 200, "old_id": 42212,
        "filename": "woocommerce-b2b-portal-body3-670x352-v3.jpg",
        "alt": (
            "B2B buyer self-serving on a WooCommerce portal, completing a repeat order "
            "without calling a sales rep, on a laptop in a professional setting"
        ),
        "logo": False,
    },
}

# ---------------------------------------------------------------------------
# Logo helpers
# ---------------------------------------------------------------------------

def fetch_virtina_logo():
    """Download Virtina logo, return as RGBA PIL image."""
    url = "https://virtina.com/wp-content/uploads/2026/03/cropped-logo-2.webp"
    r = SESS.get(url, timeout=20)
    if r.status_code != 200:
        print(f"Logo fetch failed: {r.status_code}")
        return None
    img = Image.open(io.BytesIO(r.content)).convert("RGBA")
    print(f"Logo downloaded: {img.size}")
    return img


def make_white_logo(logo_rgba):
    """
    Convert the dark navy text in the logo to white so it reads on photos.
    Teal/cyan triangle pixels are kept. White/near-white background → transparent.
    """
    data = logo_rgba.getdata()
    new_data = []
    for r, g, b, a in data:
        # Near-white background → fully transparent
        if r > 220 and g > 220 and b > 220:
            new_data.append((255, 255, 255, 0))
        # Dark navy text → white
        elif r < 80 and g < 90 and b < 120:
            new_data.append((255, 255, 255, 255))
        # Teal/cyan triangle → keep as-is
        else:
            new_data.append((r, g, b, a))
    logo_rgba.putdata(new_data)
    return logo_rgba


def composite_logo(photo_rgb, logo_rgba, padding=28):
    """
    Place white Virtina logo in bottom-right corner of photo.
    Logo width = 18% of photo width.
    """
    photo_w, photo_h = photo_rgb.size
    logo_target_w = int(photo_w * 0.18)
    logo_aspect = logo_rgba.width / logo_rgba.height
    logo_target_h = int(logo_target_w / logo_aspect)
    logo_resized = logo_rgba.resize((logo_target_w, logo_target_h), Image.LANCZOS)

    # Semi-transparent dark overlay behind logo for legibility
    overlay_pad = 14
    overlay = Image.new("RGBA", (logo_target_w + overlay_pad*2, logo_target_h + overlay_pad*2), (0, 0, 0, 0))

    photo_rgba = photo_rgb.convert("RGBA")
    x = photo_w - logo_target_w - padding - overlay_pad
    y = photo_h - logo_target_h - padding - overlay_pad

    # Darken background area slightly
    bg_patch = photo_rgba.crop((x, y, x + logo_target_w + overlay_pad*2, y + logo_target_h + overlay_pad*2))
    dark = Image.new("RGBA", bg_patch.size, (0, 0, 0, 110))
    bg_patch = Image.alpha_composite(bg_patch.convert("RGBA"), dark)
    photo_rgba.paste(bg_patch, (x, y))

    # Paste logo
    lx = photo_w - logo_target_w - padding
    ly = photo_h - logo_target_h - padding
    photo_rgba.paste(logo_resized, (lx, ly), logo_resized)
    return photo_rgba.convert("RGB")


# ---------------------------------------------------------------------------
# Core download + resize
# ---------------------------------------------------------------------------

def download_pexels(photo_id):
    url = PEXELS_CDN.format(id=photo_id)
    try:
        r = SESS.get(url, timeout=30, allow_redirects=True)
        print(f"    [{photo_id}] {r.status_code} {len(r.content)//1024}KB")
        if r.status_code != 200 or len(r.content) < 30000:
            return None, None
        img = Image.open(io.BytesIO(r.content)).convert("RGB")
        return img, url
    except Exception as e:
        print(f"    [{photo_id}] error: {e}")
        return None, None


def crop_resize(img, target_w, target_h):
    orig_w, orig_h = img.size
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
    return img.crop((left, top, left + target_w, top + target_h))


def encode_jpeg(img, max_kb):
    for q in [85, 80, 75, 70]:
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=q, optimize=True)
        if buf.tell() <= max_kb * 1024:
            print(f"    Encoded: {img.size}, {buf.tell()//1024}KB, q={q}")
            return buf.getvalue()
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
    requests.post(f"{WP_URL}/media/{mid}", json={"alt_text": alt_text},
                  headers=wp_headers, verify=False, timeout=20)
    print(f"Uploaded: media_id={mid}  {src}")
    return mid, src


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

logo = fetch_virtina_logo()
if logo:
    logo = make_white_logo(logo)
    print("Logo ready (white version)")
else:
    print("WARNING: Logo not available — featured image will have no logo overlay")

results = {}

for slot_name, meta in SLOT_META.items():
    print(f"\n{'='*60}")
    print(f"SLOT: {slot_name}  ({meta['w']}x{meta['h']})  old_id={meta['old_id']}")
    print(f"{'='*60}")

    found = False
    for photo_id in SLOT_IDS[slot_name]:
        img, url = download_pexels(photo_id)
        if img is None:
            continue
        orig_w, orig_h = img.size
        if orig_w < meta["min_src_w"] or orig_h < meta["min_src_h"]:
            print(f"    SKIP [{photo_id}] too small: {orig_w}x{orig_h}")
            continue

        # Crop-resize
        img = crop_resize(img, meta["w"], meta["h"])

        # Composite Virtina logo on featured
        if meta["logo"] and logo:
            img = composite_logo(img, logo.copy())
            print(f"    Logo composited")

        # Encode
        img_bytes = encode_jpeg(img, meta["max_kb"])
        if img_bytes is None:
            print(f"    SKIP [{photo_id}] cannot compress to {meta['max_kb']}KB")
            continue

        # Upload
        mid, src_url = upload_media(img_bytes, meta["filename"], meta["alt"])
        if not mid:
            continue

        results[slot_name] = {
            "media_id": mid, "src_url": src_url,
            "alt": meta["alt"], "old_id": meta["old_id"],
            "w": meta["w"], "h": meta["h"],
            "pexels_id": photo_id,
        }
        print(f"SUCCESS: pexels_id={photo_id} -> media_id={mid}")
        found = True
        break

    if not found:
        print(f"FAILED: no usable image found for {slot_name}")
        results[slot_name] = None

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print(f"\n{'='*60}\nSUMMARY\n{'='*60}")
all_ok = True
for name, r in results.items():
    if r:
        print(f"  {name}: pexels_id={r['pexels_id']} -> media_id={r['media_id']}")
    else:
        print(f"  {name}: FAILED")
        all_ok = False

# ---------------------------------------------------------------------------
# Patch post HTML (body images) + featured_media
# ---------------------------------------------------------------------------
html_path = os.path.join(os.path.dirname(__file__), "final_html_v6.html")
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

for slot_name, meta in SLOT_META.items():
    if slot_name == "featured":
        continue  # Featured handled via featured_media field, not inline HTML
    r = results.get(slot_name)
    if not r:
        continue
    old_id = meta["old_id"]
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
        print(f"Replaced {slot_name} span (data-id={old_id})")
    else:
        print(f"WARNING: could not locate {slot_name} span with data-id={old_id}")

v7_path = os.path.join(os.path.dirname(__file__), "final_html_v7.html")
with open(v7_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Saved final_html_v7.html")

patch_payload = {"content": content}
feat = results.get("featured")
if feat:
    patch_payload["featured_media"] = feat["media_id"]

resp = requests.patch(
    f"{WP_URL}/posts/{POST_ID}",
    json=patch_payload,
    headers=wp_headers, verify=False, timeout=60,
)
print(f"PATCH status: {resp.status_code}")
if resp.status_code == 200:
    rendered = resp.json()["content"]["rendered"]
    for slot_name, meta in SLOT_META.items():
        if slot_name == "featured":
            continue
        r = results.get(slot_name)
        if r:
            live  = str(r["media_id"]) in rendered
            gone  = f'data-id="{meta["old_id"]}"' not in rendered
            print(f"  {slot_name}: new_live={live}, old_gone={gone}")
    if feat:
        live_feat = resp.json().get("featured_media") == feat["media_id"]
        print(f"  featured: media_id_live={live_feat}")
    print(f"Post status: {resp.json()['status']}")
    print("Done.")
else:
    print(f"Error: {resp.text[:300]}")
