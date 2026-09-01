#!/usr/bin/env python3
"""
Image fetch, crop-resize, and upload script for Virtina WooCommerce B2B Customer Portal post.
Run from PowerShell: python clients/virtina/output/research/image_fetch_upload.py
"""

import os
import sys
import json
import time
import struct
import zlib
import requests
from PIL import Image
from io import BytesIO
import base64

# ---- Credentials ----
WP_USERNAME = os.environ.get("WP_USERNAME", "")
WP_APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")

if not WP_USERNAME or not WP_APP_PASSWORD:
    print("ERROR: WP_USERNAME or WP_APP_PASSWORD not set in environment.")
    sys.exit(1)

WP_MEDIA_ENDPOINT = "https://virtina.com/wp-json/wp/v2/media"

auth_string = f"{WP_USERNAME}:{WP_APP_PASSWORD}"
auth_b64 = base64.b64encode(auth_string.encode()).decode()
WP_AUTH_HEADER = f"Basic {auth_b64}"

# ---- Image specs ----
IMAGES = [
    {
        "name": "featured",
        "width": 1309,
        "height": 500,
        "pexels_query": "business professional laptop dashboard office",
        "alt": "Business professional reviewing a B2B customer portal dashboard on a laptop in a modern office workspace",
        "filename": "woocommerce-b2b-portal-1.jpg",
        "fallback_queries": [
            "business professional laptop office desk",
            "office worker laptop computer desk",
        ],
    },
    {
        "name": "body1",
        "width": 670,
        "height": 352,
        "pexels_query": "warehouse worker inventory shelves",
        "alt": "Warehouse worker in high-visibility vest checking inventory shelves representing B2B order and stock management",
        "filename": "woocommerce-b2b-portal-2.jpg",
        "fallback_queries": [
            "warehouse worker shelves boxes",
            "warehouse inventory storage aisle",
        ],
    },
    {
        "name": "body2",
        "width": 670,
        "height": 352,
        "pexels_query": "business team meeting laptop table",
        "alt": "Small business team reviewing WooCommerce portal implementation plans at a meeting table with laptop and documents",
        "filename": "woocommerce-b2b-portal-3.jpg",
        "fallback_queries": [
            "team meeting table laptop",
            "office meeting discussion documents",
        ],
    },
    {
        "name": "body3",
        "width": 670,
        "height": 352,
        "pexels_query": "business person phone laptop office desk",
        "alt": "Account manager at a desk on a phone call while reviewing customer account data on a laptop representing B2B portal onboarding support",
        "filename": "woocommerce-b2b-portal-4.jpg",
        "fallback_queries": [
            "business person phone headset office",
            "office worker phone call laptop",
        ],
    },
]

# ---- Subject relevance rejects ----
REJECT_KEYWORDS_IN_DESCRIPTION = [
    "flower", "flowers", "nature", "forest", "mountain", "landscape",
    "ocean", "sea", "river", "lake", "animal", "pet", "cat", "dog",
    "building exterior", "city skyline", "abstract",
]

def is_valid_image_bytes(data: bytes) -> bool:
    if len(data) < 8000:
        print(f"  REJECT: file too small ({len(data)} bytes)")
        return False
    # JPEG starts with FF D8 FF
    if data[:3] == b'\xff\xd8\xff':
        return True
    # PNG starts with 89 50 4E 47
    if data[:4] == b'\x89PNG':
        return True
    print(f"  REJECT: not a valid JPEG or PNG (starts with {data[:4].hex()})")
    return False


def fetch_pexels(query: str, per_page: int = 10):
    """Fetch photos from Pexels API. Returns list of photo dicts or empty list."""
    if not PEXELS_API_KEY:
        print("  WARNING: PEXELS_API_KEY not set, skipping Pexels.")
        return []
    url = f"https://api.pexels.com/v1/search?query={requests.utils.quote(query)}&orientation=landscape&per_page={per_page}"
    headers = {"Authorization": PEXELS_API_KEY}
    try:
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code == 200:
            data = r.json()
            return data.get("photos", [])
        else:
            print(f"  Pexels API error {r.status_code}: {r.text[:200]}")
            return []
    except Exception as e:
        print(f"  Pexels request error: {e}")
        return []


def fetch_openverse(query: str, per_page: int = 10):
    """Fallback: Openverse CC0 images."""
    url = f"https://api.openverse.org/v1/images/?q={requests.utils.quote(query)}&source=stocksnap&license_type=commercial&per_page={per_page}&aspect_ratio=wide"
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            data = r.json()
            return data.get("results", [])
        else:
            print(f"  Openverse API error {r.status_code}: {r.text[:200]}")
            return []
    except Exception as e:
        print(f"  Openverse request error: {e}")
        return []


def download_image(url: str, timeout: int = 30) -> bytes | None:
    try:
        r = requests.get(url, timeout=timeout, stream=True)
        if r.status_code == 200:
            data = r.content
            if is_valid_image_bytes(data):
                return data
        else:
            print(f"  Download error {r.status_code} from {url}")
    except Exception as e:
        print(f"  Download exception: {e}")
    return None


def crop_resize(img_bytes: bytes, target_w: int, target_h: int, quality: int = 82) -> bytes:
    """Scale-to-cover + center-crop to exact target dimensions. Returns JPEG bytes."""
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    orig_w, orig_h = img.size

    scale = max(target_w / orig_w, target_h / orig_h)
    new_w = int(orig_w * scale)
    new_h = int(orig_h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)

    # Center crop
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    img = img.crop((left, top, left + target_w, top + target_h))

    buf = BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    out_bytes = buf.getvalue()

    # If > 200KB, retry at lower quality
    if len(out_bytes) > 200 * 1024:
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=75, optimize=True)
        out_bytes = buf.getvalue()
        print(f"  Compressed to quality=75: {len(out_bytes)//1024}KB")

    return out_bytes


def upload_to_wp(img_bytes: bytes, filename: str, alt_text: str) -> dict | None:
    """Upload image to WordPress media library. Returns media object dict or None."""
    headers = {
        "Authorization": WP_AUTH_HEADER,
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "image/jpeg",
    }
    print(f"  Uploading {filename} ({len(img_bytes)//1024}KB) to WordPress...")
    try:
        r = requests.post(WP_MEDIA_ENDPOINT, headers=headers, data=img_bytes, timeout=120)
        if r.status_code in (200, 201):
            media = r.json()
            media_id = media.get("id")
            print(f"  Upload OK: media ID = {media_id}")
            # Set alt text via PATCH
            patch_headers = {
                "Authorization": WP_AUTH_HEADER,
                "Content-Type": "application/json",
            }
            patch_data = {"alt_text": alt_text}
            pr = requests.post(
                f"{WP_MEDIA_ENDPOINT}/{media_id}",
                headers=patch_headers,
                json=patch_data,
                timeout=30,
            )
            if pr.status_code in (200, 201):
                print(f"  Alt text set OK.")
            else:
                print(f"  Alt text set FAILED {pr.status_code}: {pr.text[:200]}")
            return media
        else:
            print(f"  Upload FAILED {r.status_code}: {r.text[:300]}")
            return None
    except Exception as e:
        print(f"  Upload exception: {e}")
        return None


def process_image(spec: dict) -> dict:
    """Full pipeline for one image: search -> download -> crop/resize -> upload."""
    print(f"\n=== Processing {spec['name']} ({spec['width']}x{spec['height']}) ===")
    print(f"  Query: {spec['pexels_query']}")

    all_queries = [spec["pexels_query"]] + spec["fallback_queries"]
    selected_url = None
    selected_photo_id = None
    source = None

    for attempt, query in enumerate(all_queries):
        print(f"  Attempt {attempt+1}: query='{query}'")
        photos = fetch_pexels(query, per_page=10)
        if photos:
            # Pick the first landscape photo that is large enough
            for p in photos:
                w = p.get("width", 0)
                h = p.get("height", 0)
                if w >= spec["width"] and h >= spec["height"]:
                    selected_url = p["src"].get("large2x") or p["src"].get("original") or p["src"].get("large")
                    selected_photo_id = p.get("id")
                    source = "pexels"
                    print(f"  Selected Pexels photo ID {selected_photo_id}: {p.get('width')}x{p.get('height')}")
                    break
            if selected_url:
                break
        time.sleep(0.5)

    if not selected_url:
        # Try Openverse
        print("  Pexels exhausted. Trying Openverse...")
        for attempt, query in enumerate(all_queries[:2]):
            results = fetch_openverse(query, per_page=10)
            if results:
                for r in results:
                    url = r.get("url") or r.get("thumbnail")
                    if url and (r.get("width", 0) >= spec["width"] or r.get("width", 0) == 0):
                        selected_url = url
                        selected_photo_id = r.get("id", "openverse")
                        source = "openverse"
                        print(f"  Selected Openverse: {url[:80]}")
                        break
            if selected_url:
                break
            time.sleep(1)

    if not selected_url:
        print(f"  IMAGE SEARCH FAILED for {spec['name']} after all attempts.")
        return {
            "name": spec["name"],
            "status": "FAILED",
            "media_id": None,
            "src": None,
            "alt": spec["alt"],
            "filename": spec["filename"],
            "pexels_id": None,
            "source": None,
        }

    # Download
    print(f"  Downloading from: {selected_url[:80]}...")
    img_bytes = download_image(selected_url)
    if not img_bytes:
        print(f"  IMAGE SEARCH FAILED: download error for {spec['name']}")
        return {
            "name": spec["name"],
            "status": "FAILED",
            "media_id": None,
            "src": None,
            "alt": spec["alt"],
            "filename": spec["filename"],
            "pexels_id": selected_photo_id,
            "source": source,
        }

    print(f"  Downloaded {len(img_bytes)//1024}KB")

    # Crop/resize
    processed = crop_resize(img_bytes, spec["width"], spec["height"])
    print(f"  Resized to {spec['width']}x{spec['height']}, {len(processed)//1024}KB")

    # Upload
    media = upload_to_wp(processed, spec["filename"], spec["alt"])
    if not media:
        # Retry once
        print("  Retrying upload...")
        time.sleep(3)
        media = upload_to_wp(processed, spec["filename"], spec["alt"])

    if media:
        src_url = media.get("source_url", "")
        return {
            "name": spec["name"],
            "status": "OK",
            "media_id": media.get("id"),
            "src": src_url,
            "alt": spec["alt"],
            "filename": spec["filename"],
            "pexels_id": selected_photo_id,
            "source": source,
        }
    else:
        print(f"  Upload failed for {spec['name']}.")
        return {
            "name": spec["name"],
            "status": "UPLOAD_FAILED",
            "media_id": None,
            "src": None,
            "alt": spec["alt"],
            "filename": spec["filename"],
            "pexels_id": selected_photo_id,
            "source": source,
        }


def main():
    print("=== Virtina Image Fetch + Upload Pipeline ===")
    print(f"WordPress user: {WP_USERNAME}")
    print(f"Pexels key set: {'YES' if PEXELS_API_KEY else 'NO'}")

    results = []
    for spec in IMAGES:
        result = process_image(spec)
        results.append(result)
        time.sleep(1)

    print("\n=== RESULTS SUMMARY ===")
    for r in results:
        status = r["status"]
        mid = r["media_id"]
        src = (r["src"] or "")[:80]
        pexels_id = r["pexels_id"]
        print(f"  {r['name']:10s} | {status:15s} | ID={mid} | pexels={pexels_id} | src={src}")

    # Save results to JSON
    out_path = r"C:\content-intel\clients\virtina\output\research\image_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {out_path}")

    # Check for failures
    failures = [r for r in results if r["status"] != "OK"]
    if failures:
        print(f"\nWARNING: {len(failures)} image(s) failed:")
        for r in failures:
            print(f"  - {r['name']}: {r['status']}")
    else:
        print("\nAll 4 images processed successfully.")

    return results


if __name__ == "__main__":
    main()
