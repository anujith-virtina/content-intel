#!/usr/bin/env python3
"""
Image pipeline for the "ecommerce-store-agent-ready" Virtina blog post.
Downloads from Pexels CDN, crop-resizes with Pillow, uploads to WP media library.
Run: python clients/virtina/output/research/agent_ready_images.py
"""
import os, sys, json, base64, io, time
import requests
import urllib3
from PIL import Image

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WP_USERNAME     = os.environ.get("WP_USERNAME", "")
WP_APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
if not WP_USERNAME or not WP_APP_PASSWORD:
    print("ERROR: WP_USERNAME / WP_APP_PASSWORD not set.")
    sys.exit(1)

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")

WP_MEDIA_EP = "https://virtina.com/wp-json/wp/v2/media"
AUTH        = "Basic " + base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()).decode()

SESS = requests.Session()
SESS.verify = False
SESS.headers["Authorization"] = AUTH

RESULTS_FILE = r"C:\content-intel\clients\virtina\output\research\agent_ready_image_results.json"

# ── Image specifications ─────────────────────────────────────────────────────
IMAGES = [
    {
        "key":       "featured",
        "filename":  "ecommerce-store-agent-ready-hero.jpg",
        "width":     1309,
        "height":    500,
        "alt":       "Ecommerce professional reviewing AI shopping agent readiness and product data on dual monitors in a modern office setting",
        "pexels_ids": [3184297, 3182812, 3183197, 1181533, 3184338, 1181467],
        "description": "featured hero 1309x500",
    },
    {
        "key":       "body1",
        "filename":  "ecommerce-agent-ready-product-schema-review.jpg",
        "width":     670,
        "height":    352,
        "alt":       "Developer reviewing structured data and product schema JSON-LD implementation on a laptop screen for AI shopping agent compatibility",
        "pexels_ids": [2004161, 546819, 1181263, 1181298, 3861958],
        "description": "body1 670x352",
    },
    {
        "key":       "body2",
        "filename":  "ecommerce-agent-ready-product-data-optimization.jpg",
        "width":     670,
        "height":    352,
        "alt":       "Ecommerce manager reviewing product catalog data and AI shopping performance analytics on a monitor to optimize store visibility",
        "pexels_ids": [1181671, 3183150, 4491461, 1181244, 7364107],
        "description": "body2 670x352",
    },
]

# ── Helpers ──────────────────────────────────────────────────────────────────

def fetch_pexels_photo(photo_id: int) -> bytes | None:
    """Fetch a Pexels photo by ID using the Pexels API. Returns raw bytes or None."""
    if not PEXELS_API_KEY:
        print("    PEXELS_API_KEY not set — falling back to direct CDN fetch")
        return fetch_pexels_cdn(photo_id)
    try:
        headers = {"Authorization": PEXELS_API_KEY}
        r = requests.get(
            f"https://api.pexels.com/v1/photos/{photo_id}",
            headers=headers, timeout=20, verify=False
        )
        if r.status_code != 200:
            print(f"    Pexels API {r.status_code} for id={photo_id}")
            return None
        data = r.json()
        src_url = data.get("src", {}).get("large2x") or data.get("src", {}).get("original")
        if not src_url:
            print(f"    No src.large2x for id={photo_id}")
            return None
        print(f"    Downloading: {src_url}")
        img_r = requests.get(src_url, timeout=30, verify=False)
        if img_r.status_code == 200 and len(img_r.content) > 8000:
            return img_r.content
        print(f"    Download failed or too small: {img_r.status_code} {len(img_r.content)} bytes")
        return None
    except Exception as e:
        print(f"    Pexels API error for id={photo_id}: {e}")
        return None


def fetch_pexels_cdn(photo_id: int) -> bytes | None:
    """Direct CDN fetch as fallback when no API key."""
    url = f"https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.jpeg?auto=compress&cs=tinysrgb&w=1920"
    try:
        r = requests.get(url, timeout=30, verify=False,
                         headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200 and len(r.content) > 8000:
            # Validate JPEG signature
            if r.content[:3] == b'\xff\xd8\xff':
                return r.content
            print(f"    Not a valid JPEG for id={photo_id}")
        else:
            print(f"    CDN fetch failed: {r.status_code}, {len(r.content)} bytes")
    except Exception as e:
        print(f"    CDN fetch error: {e}")
    return None


def crop_resize(raw_bytes: bytes, target_w: int, target_h: int, quality: int = 82) -> bytes:
    """Scale-to-cover + center-crop to exact dimensions. JPEG quality 82."""
    img = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
    src_w, src_h = img.size

    # Scale to cover: find the scale that makes both dimensions >= target
    scale = max(target_w / src_w, target_h / src_h)
    new_w = int(src_w * scale)
    new_h = int(src_h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)

    # Center crop
    left = (new_w - target_w) // 2
    top  = (new_h - target_h) // 2
    img  = img.crop((left, top, left + target_w, top + target_h))

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    return buf.getvalue()


def validate_image(raw_bytes: bytes) -> bool:
    """Check minimum size and valid JPEG/PNG signature."""
    if len(raw_bytes) < 8000:
        return False
    if raw_bytes[:3] == b'\xff\xd8\xff':  # JPEG
        return True
    if raw_bytes[:8] == b'\x89PNG\r\n\x1a\n':  # PNG
        return True
    return False


def upload_to_wp(jpeg_bytes: bytes, filename: str, alt_text: str) -> dict | None:
    """Upload image bytes to WP media library. Returns media object dict or None."""
    upload_sess = requests.Session()
    upload_sess.verify = False
    upload_sess.headers["Authorization"] = AUTH
    upload_sess.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    upload_sess.headers["Content-Type"] = "image/jpeg"

    print(f"    Uploading {filename} ({len(jpeg_bytes):,} bytes) ...")
    r = upload_sess.post(WP_MEDIA_EP, data=jpeg_bytes, timeout=120)
    if r.status_code not in (200, 201):
        print(f"    Upload FAILED {r.status_code}: {r.text[:300]}")
        return None

    media = r.json()
    media_id  = media.get("id")
    media_src = media.get("source_url", "")
    print(f"    Uploaded: id={media_id}, src={media_src}")

    # Set alt_text
    alt_sess = requests.Session()
    alt_sess.verify = False
    alt_sess.headers["Authorization"] = AUTH
    alt_sess.headers["Content-Type"] = "application/json"
    ar = alt_sess.post(
        f"{WP_MEDIA_EP}/{media_id}",
        json={"alt_text": alt_text},
        timeout=30
    )
    if ar.status_code in (200, 201):
        print(f"    Alt text set OK")
    else:
        print(f"    Alt text set FAILED {ar.status_code}: {ar.text[:200]}")

    return {"id": media_id, "src": media_src, "alt": alt_text}


def process_image(spec: dict) -> dict:
    """Download, resize, and upload a single image. Returns result dict."""
    key      = spec["key"]
    filename = spec["filename"]
    alt      = spec["alt"]
    w, h     = spec["width"], spec["height"]
    ids      = spec["pexels_ids"]

    print(f"\n[{key}] {spec['description']}")
    print(f"  Target: {w}x{h} | filename: {filename}")

    raw = None
    used_id = None
    for pid in ids:
        print(f"  Trying Pexels id={pid} ...")
        raw = fetch_pexels_photo(pid)
        if raw and validate_image(raw):
            used_id = pid
            print(f"  Fetched OK ({len(raw):,} bytes)")
            break
        time.sleep(0.5)

    if not raw:
        print(f"  FAIL: Could not fetch a valid image for {key}. Tried IDs: {ids}")
        return {"key": key, "error": "no valid image fetched", "pexels_ids_tried": ids}

    # Crop-resize
    print(f"  Resizing to {w}x{h} (quality=82) ...")
    jpeg = crop_resize(raw, w, h, quality=82)
    print(f"  Resized size: {len(jpeg):,} bytes")
    if len(jpeg) > 200_000:
        # Re-compress at lower quality to meet <200KB rule
        for q in [75, 70, 65]:
            jpeg = crop_resize(raw, w, h, quality=q)
            if len(jpeg) <= 200_000:
                print(f"  Re-compressed to {len(jpeg):,} bytes at quality={q}")
                break
    if len(jpeg) > 200_000:
        print(f"  WARNING: Image still >{200_000} bytes after compression ({len(jpeg):,})")

    # Upload
    media = upload_to_wp(jpeg, filename, alt)
    if not media:
        return {"key": key, "error": "upload failed", "pexels_id_used": used_id}

    return {
        "key":          key,
        "media_id":     media["id"],
        "src":          media["src"],
        "alt":          media["alt"],
        "filename":     filename,
        "dimensions":   f"{w}x{h}",
        "pexels_id":    used_id,
        "file_size_kb": round(len(jpeg) / 1024, 1),
    }


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    print("=== Agent-Ready Post — Image Pipeline ===")
    print(f"WP_USERNAME: {WP_USERNAME[:3]}***")
    print(f"PEXELS_API_KEY: {'set' if PEXELS_API_KEY else 'NOT SET (will use CDN fallback)'}")

    results = {}
    errors  = []

    for spec in IMAGES:
        result = process_image(spec)
        key = spec["key"]
        results[key] = result
        if "error" in result:
            errors.append(key)

    # Save results
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {RESULTS_FILE}")

    # Summary
    print("\n=== Summary ===")
    for key, res in results.items():
        if "error" in res:
            print(f"  {key:10s}: FAIL — {res['error']}")
        else:
            print(f"  {key:10s}: OK — media_id={res['media_id']}, {res['dimensions']}, "
                  f"{res['file_size_kb']} KB")
            src = res.get("src", "")
            if not src.startswith("https://virtina.com/wp-content/uploads/"):
                print(f"  WARNING: {key} src does not begin with virtina.com/wp-content/uploads/")

    if errors:
        print(f"\nFAIL: {len(errors)} image(s) failed: {errors}")
        print("Fix before running publisher script.")
        sys.exit(1)
    else:
        print(f"\nAll {len(IMAGES)} images uploaded successfully.")
        print(f"Run agent_ready_publish.py next.")


if __name__ == "__main__":
    main()
