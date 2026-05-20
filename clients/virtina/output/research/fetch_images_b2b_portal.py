#!/usr/bin/env python3
"""
Fetch 4 images for the WooCommerce B2B Customer Portal post using Openverse search API.
Crop-resize and upload to Virtina WordPress media library.
Then PATCH the existing post 42202 with image IDs.
"""
import sys
import json
import base64
import requests
import time
from pathlib import Path
from io import BytesIO

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow not installed. Run: pip install pillow")
    sys.exit(1)

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ── Credentials ────────────────────────────────────────────────────────────────
env_path = Path(r"C:\content-intel\.env")
env_vars = {}
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env_vars[k.strip()] = v.strip()

WP_USERNAME = env_vars["WP_USERNAME"]
WP_APP_PASSWORD = env_vars["WP_APP_PASSWORD"]
WP_BASE = "https://virtina.com/wp-json/wp/v2"
auth_str = base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()).decode()
WP_HEADERS = {"Authorization": f"Basic {auth_str}", "Content-Type": "application/json"}
POST_ID = 42202

WORK_DIR = Path(r"C:\content-intel\clients\virtina\output\research")

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ContentBot/1.0)"}

# ── Image specs with search queries ──────────────────────────────────────────
IMAGES = [
    {
        "key": "featured",
        "queries": ["business professional laptop office", "person working laptop desk", "office worker computer"],
        "width": 1309, "height": 500,
        "filename": "woocommerce-b2b-portal-featured-1309x500.jpg",
        "alt": "Business professional reviewing a B2B customer portal dashboard on a laptop in a modern office workspace",
        "concept": "business professional at desk with laptop showing dashboard"
    },
    {
        "key": "body1",
        "queries": ["warehouse worker inventory shelves", "warehouse storage boxes", "fulfillment worker storage"],
        "width": 670, "height": 352,
        "filename": "woocommerce-b2b-portal-body1-670x352.jpg",
        "alt": "Warehouse worker in high-visibility vest checking inventory shelves representing B2B order and stock management",
        "concept": "warehouse worker checking inventory shelves"
    },
    {
        "key": "body2",
        "queries": ["business team meeting laptop", "office team meeting table", "coworkers reviewing documents laptop"],
        "width": 670, "height": 352,
        "filename": "woocommerce-b2b-portal-body2-670x352.jpg",
        "alt": "Small business team reviewing WooCommerce portal implementation plans at a meeting table with laptop and documents",
        "concept": "2-3 people at table reviewing documents or laptop"
    },
    {
        "key": "body3",
        "queries": ["business person phone office laptop", "office worker phone desk", "man phone laptop office"],
        "width": 670, "height": 352,
        "filename": "woocommerce-b2b-portal-body3-670x352.jpg",
        "alt": "Account manager at a desk on a phone call while reviewing customer account data on a laptop representing B2B portal onboarding support",
        "concept": "person at desk on phone while looking at laptop"
    },
]

def search_openverse(query: str, per_page: int = 10):
    """Search Openverse for CC0 images matching query."""
    url = "https://api.openverse.org/v1/images/"
    params = {
        "q": query,
        "license_type": "commercial",
        "source": "stocksnap",
        "per_page": per_page,
        "page_size": per_page,
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=30, verify=False)
        if r.status_code == 200:
            data = r.json()
            results = data.get("results", [])
            print(f"    Openverse '{query}': {len(results)} results")
            return results
        else:
            print(f"    Openverse error {r.status_code}: {r.text[:100]}")
    except Exception as e:
        print(f"    Openverse exception: {e}")
    return []

def download_image(url: str) -> bytes | None:
    """Download image bytes from URL."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=60, verify=False)
        if r.status_code == 200 and len(r.content) > 5000:
            # Verify it's an actual image
            content_type = r.headers.get("content-type", "")
            if "image" in content_type or r.content[:3] == b'\xff\xd8\xff' or r.content[:8] == b'\x89PNG\r\n\x1a\n':
                print(f"    Downloaded: {len(r.content)//1024}KB")
                return r.content
            else:
                print(f"    Not an image: {content_type}, first bytes: {r.content[:4].hex()}")
        else:
            print(f"    Download failed: {r.status_code}, {len(r.content)} bytes")
    except Exception as e:
        print(f"    Download error: {e}")
    return None

def find_best_image(spec: dict) -> bytes | None:
    """Try queries in order until we find a good downloadable image."""
    for query in spec["queries"]:
        print(f"  Searching: '{query}'")
        results = search_openverse(query, per_page=10)
        for result in results:
            url = result.get("url") or result.get("thumbnail")
            if not url:
                continue
            # Skip obvious mismatches
            tags = [t.get("name", "").lower() for t in result.get("tags", [])]
            title = result.get("title", "").lower()
            # Filter out nature/abstract
            skip_keywords = ["flower", "tree", "nature", "mountain", "ocean", "animal", "cat", "dog", "bird", "forest", "landscape", "abstract", "sky", "river"]
            if any(kw in title or kw in " ".join(tags) for kw in skip_keywords):
                continue
            print(f"    Trying: {title[:50]} | {url[:60]}")
            img = download_image(url)
            if img:
                return img
    return None

def crop_resize(img_bytes: bytes, w: int, h: int) -> bytes:
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    ow, oh = img.size
    print(f"  Original: {ow}x{oh}")
    scale = max(w / ow, h / oh)
    nw, nh = int(ow * scale + 1), int(oh * scale + 1)
    img = img.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - w) // 2, (nh - h) // 2
    img = img.crop((left, top, left + w, top + h))
    buf = BytesIO()
    quality = 82
    img.save(buf, "JPEG", quality=quality, optimize=True)
    result = buf.getvalue()
    if len(result) > 200 * 1024:
        buf = BytesIO()
        img.save(buf, "JPEG", quality=72, optimize=True)
        result = buf.getvalue()
        print(f"  Re-compressed to q=72: {len(result)//1024}KB")
    print(f"  Final: {w}x{h}, {len(result)//1024}KB")
    return result

def upload_media(img_bytes: bytes, filename: str, alt_text: str) -> dict | None:
    headers = {
        "Authorization": f"Basic {auth_str}",
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "image/jpeg",
    }
    print(f"  Uploading {filename} ({len(img_bytes)//1024}KB)...")
    for attempt in range(2):
        try:
            r = requests.post(f"{WP_BASE}/media", headers=headers, data=img_bytes, timeout=120, verify=False)
            if r.status_code in (200, 201):
                media = r.json()
                mid = media.get("id")
                src = media.get("source_url", "")
                print(f"  Upload OK: ID={mid}, src={src[:70]}")
                # Set alt text
                patch = requests.post(
                    f"{WP_BASE}/media/{mid}",
                    headers=WP_HEADERS,
                    json={"alt_text": alt_text},
                    timeout=20, verify=False,
                )
                if patch.status_code in (200, 201):
                    print(f"  Alt text set OK")
                return media
            else:
                print(f"  Upload failed {r.status_code}: {r.text[:200]}")
        except Exception as e:
            print(f"  Upload error: {e}")
        if attempt == 0:
            time.sleep(3)
    return None

def main():
    print("=== Virtina Image Fetch + Post Update ===")
    print(f"Target post: {POST_ID}\n")

    results = {}

    for spec in IMAGES:
        print(f"\n[{spec['key']}] {spec['width']}x{spec['height']}")
        print(f"  Concept: {spec['concept']}")

        img_bytes = find_best_image(spec)
        if not img_bytes:
            print(f"  IMAGE FETCH FAILED after all queries — marking as FAILED")
            results[spec["key"]] = {"status": "FETCH_FAILED", "media_id": None, "src_url": None, "alt": spec["alt"]}
            continue

        processed = crop_resize(img_bytes, spec["width"], spec["height"])

        # Save locally for inspection
        local_path = WORK_DIR / spec["filename"]
        with open(local_path, "wb") as f:
            f.write(processed)
        print(f"  Saved locally: {local_path}")

        media = upload_media(processed, spec["filename"], spec["alt"])
        if media:
            src = media.get("source_url", "")
            if not src.startswith("https://virtina.com/wp-content/uploads/"):
                print(f"  WARNING: src doesn't start with virtina.com/wp-content/uploads/: {src}")
            results[spec["key"]] = {
                "status": "OK",
                "media_id": media.get("id"),
                "src_url": src,
                "alt": spec["alt"],
            }
        else:
            results[spec["key"]] = {"status": "UPLOAD_FAILED", "media_id": None, "src_url": None, "alt": spec["alt"]}

        time.sleep(1)

    print("\n=== IMAGE RESULTS ===")
    for k, r in results.items():
        print(f"  {k}: status={r['status']}, media_id={r['media_id']}")
        if r.get("src_url"):
            print(f"    src={r['src_url'][:80]}")

    # PATCH the existing post with featured_media
    featured_id = results.get("featured", {}).get("media_id") or 0
    body1_id = results.get("body1", {}).get("media_id") or 0
    body2_id = results.get("body2", {}).get("media_id") or 0
    body3_id = results.get("body3", {}).get("media_id") or 0

    # Build updated content with actual image tags
    html_path = WORK_DIR / "final_html.html"
    if html_path.exists():
        with open(html_path, encoding="utf-8") as f:
            html = f.read()

        def img_tag(mid, src, alt, w, h):
            return (f'<span style="display:block;margin:20px 0;">'
                    f'<img alt="{alt}" data-id="{mid}" width="{w}" height="{h}" '
                    f'loading="lazy" src="{src}" '
                    f'style="max-width:100%;height:auto;display:block;border-radius:8px;"></span>')

        # The HTML already has {b1}, {b2}, {b3} placeholders replaced in build_html
        # But the placeholders are the img_tag spans from the original script
        # They will have src="" if images failed. Let's check and patch.
        print(f"\nFeatured media ID to set: {featured_id}")
        print(f"Body image IDs: body1={body1_id}, body2={body2_id}, body3={body3_id}")

        # For body images: if they have real src URLs, the HTML already contains them
        # We just need to PATCH the post with featured_media
        if featured_id > 0:
            patch_payload = {"featured_media": featured_id}
            pr = requests.post(
                f"{WP_BASE}/posts/{POST_ID}",
                headers=WP_HEADERS,
                json=patch_payload,
                timeout=30, verify=False,
            )
            if pr.status_code in (200, 201):
                print(f"  Post {POST_ID} featured_media set to {featured_id}: OK")
            else:
                print(f"  PATCH failed {pr.status_code}: {pr.text[:200]}")
        else:
            print("  featured_media is 0 — skipping PATCH")

    # If body images succeeded, we need to rebuild HTML content and re-push
    body_ok = all(results.get(k, {}).get("status") == "OK" for k in ["body1", "body2", "body3"])
    if body_ok:
        print("\nAll body images OK. Updating post content with real image URLs...")
        # Read the original build_html output and replace empty src spans
        # The HTML was built with empty srcs for failed images, so we need to rebuild
        # Read the original script's build_html and inject real image srcs
        b1_r = results["body1"]
        b2_r = results["body2"]
        b3_r = results["body3"]

        def real_img_tag(r, w, h):
            mid = r.get("media_id") or 0
            src = r.get("src_url") or ""
            alt = r.get("alt", "")
            return (f'<span style="display:block;margin:20px 0;">'
                    f'<img alt="{alt}" data-id="{mid}" width="{w}" height="{h}" '
                    f'loading="lazy" src="{src}" '
                    f'style="max-width:100%;height:auto;display:block;border-radius:8px;"></span>')

        b1_html = real_img_tag(b1_r, 670, 352)
        b2_html = real_img_tag(b2_r, 670, 352)
        b3_html = real_img_tag(b3_r, 670, 352)

        # Replace the original empty-src spans in the existing HTML
        # The original spans have src="" — replace with real ones
        old_b1 = '<span style="display:block;margin:20px 0;"><img alt="' + b1_r["alt"] + '"'
        old_b2 = '<span style="display:block;margin:20px 0;"><img alt="' + b2_r["alt"] + '"'
        old_b3 = '<span style="display:block;margin:20px 0;"><img alt="' + b3_r["alt"] + '"'

        import re
        # Replace each body image span entirely with the new one
        for old_prefix, new_html in [(old_b1, b1_html), (old_b2, b2_html), (old_b3, b3_html)]:
            pattern = re.escape(old_prefix) + r'[^<]*?</span>'
            if re.search(pattern, html):
                html = re.sub(pattern, new_html, html, count=1)
                print(f"  Replaced image span for: {old_prefix[:50]}")
            else:
                print(f"  Could not find span to replace for: {old_prefix[:50]}")
                # Try a simpler approach: find by data-id="0" src="" for that alt text
                old_simple = f'data-id="0"'
                print(f"  Current HTML sample around image: {html[html.find(old_prefix[:30]):html.find(old_prefix[:30])+200] if old_prefix[:30] in html else 'not found'}")

        # Save updated HTML
        updated_html_path = WORK_DIR / "final_html_updated.html"
        with open(updated_html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  Updated HTML saved: {updated_html_path}")

        # PATCH the post content
        patch_payload = {
            "content": html,
            "featured_media": featured_id,
        }
        pr = requests.post(
            f"{WP_BASE}/posts/{POST_ID}",
            headers=WP_HEADERS,
            json=patch_payload,
            timeout=60, verify=False,
        )
        if pr.status_code in (200, 201):
            pdata = pr.json()
            print(f"\nPost content updated: ID={pdata.get('id')}, status={pdata.get('status')}")
        else:
            print(f"  Content PATCH failed {pr.status_code}: {pr.text[:300]}")
    else:
        failed = [k for k in ["body1", "body2", "body3"] if results.get(k, {}).get("status") != "OK"]
        print(f"\nSome body images failed: {failed}")
        print("Post content NOT updated — images need manual upload.")

    # Save results
    out = {"post_id": POST_ID, "images": results, "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    with open(WORK_DIR / "image_results.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nResults saved: {WORK_DIR / 'image_results.json'}")

    # Final summary
    print("\n=== FINAL SUMMARY ===")
    print(f"Post ID: {POST_ID}")
    print(f"Preview: https://virtina.com/?p={POST_ID}")
    print(f"Featured media ID: {featured_id}")
    for k in ["body1", "body2", "body3"]:
        r = results.get(k, {})
        print(f"  {k}: ID={r.get('media_id')}, status={r.get('status')}")

if __name__ == "__main__":
    main()
