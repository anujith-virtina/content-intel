#!/usr/bin/env python3
"""
ImpelHub blog publisher: reduce-churn-b2b-saas-2026-06-10
Step-by-step:
  1. Source 3 images (Pexels -> Openverse fallback)
  2. Crop/resize with Pillow
  3. Upload to impelhub.com media library
  4. Inject real image URLs into draft HTML
  5. POST to WordPress REST API as draft
  6. Verify saved post
  7. Save final HTML to published/
  8. Print result summary

Run:
  python C:\content-intel\clients\impelhub\output\research\publish_churn_post.py
"""
import os, sys, re, base64, json, time
from pathlib import Path

import requests
from PIL import Image
from io import BytesIO

# ---- Credentials from env ------------------------------------------------
IMPELHUB_USER = os.environ.get("IMPELHUB_WP_USERNAME", "")
IMPELHUB_PASS = os.environ.get("IMPELHUB_WP_APP_PASSWORD", "")
PEXELS_KEY    = os.environ.get("PEXELS_API_KEY", "")

if not IMPELHUB_USER or not IMPELHUB_PASS:
    print("ERROR: IMPELHUB_WP_USERNAME or IMPELHUB_WP_APP_PASSWORD not set.")
    sys.exit(1)

WP_BASE   = "https://impelhub.com/wp-json/wp/v2"
auth_str  = base64.b64encode(f"{IMPELHUB_USER}:{IMPELHUB_PASS}".encode()).decode()
AUTH_HDR  = {"Authorization": f"Basic {auth_str}"}

SESS = requests.Session()
SESS.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36"
})

DRAFT_PATH     = Path(r"C:\content-intel\clients\impelhub\output\drafts\reduce-churn-b2b-saas-2026-06-10.md")
PUBLISHED_DIR  = Path(r"C:\content-intel\clients\impelhub\output\published")
PUBLISHED_DIR.mkdir(parents=True, exist_ok=True)

# ---- Image spec ------------------------------------------------------------
IMAGES = [
    {
        "key":      "featured",
        "query":    "founder laptop strategy decision",
        "filename": "impelhub-churn-featured.jpg",
        "alt":      "B2B SaaS founder at laptop working through churn diagnosis and retention strategy for early-stage startup",
        "width":    1200,
        "height":   628,
    },
    {
        "key":      "body1",
        "query":    "business analytics dashboard startup",
        "filename": "impelhub-churn-body1.jpg",
        "alt":      "Startup founder reviewing business analytics dashboard to identify root cause of B2B SaaS churn trends",
        "width":    800,
        "height":   450,
    },
    {
        "key":      "body2",
        "query":    "startup team planning meeting",
        "filename": "impelhub-churn-body2.jpg",
        "alt":      "Small startup team in planning meeting deciding on customer success hiring and churn reduction priorities",
        "width":    800,
        "height":   450,
    },
]

# ---- Image sourcing --------------------------------------------------------

def search_pexels(query, per_page=8):
    """Return list of photo dicts from Pexels. Returns [] if key absent."""
    if not PEXELS_KEY:
        print(f"  [Pexels] No API key — skipping Pexels for '{query}'")
        return []
    url = "https://api.pexels.com/v1/search"
    params = {"query": query, "orientation": "landscape", "per_page": per_page}
    try:
        r = requests.get(url, headers={"Authorization": PEXELS_KEY}, params=params, timeout=30)
        if r.status_code == 200:
            photos = r.json().get("photos", [])
            print(f"  [Pexels] '{query}' -> {len(photos)} results")
            return photos
        else:
            print(f"  [Pexels] HTTP {r.status_code} for '{query}'")
            return []
    except Exception as e:
        print(f"  [Pexels] Error: {e}")
        return []


def search_openverse(query, per_page=8):
    """Return list of image dicts from Openverse CC0/PDM."""
    url = "https://api.openverse.org/v1/images/"
    params = {
        "q":           query,
        "license":     "cc0,pdm",
        "page_size":   per_page,
        "aspect_ratio": "wide",
    }
    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code == 200:
            results = r.json().get("results", [])
            print(f"  [Openverse] '{query}' -> {len(results)} results")
            return results
        else:
            print(f"  [Openverse] HTTP {r.status_code} for '{query}'")
            return []
    except Exception as e:
        print(f"  [Openverse] Error: {e}")
        return []


def download_image(url):
    """Download image bytes. Returns bytes or None."""
    try:
        r = SESS.get(url, timeout=60)
        if r.status_code == 200 and len(r.content) > 8000:
            # Validate JPEG or PNG signature
            sig = r.content[:4]
            if sig[:2] == b'\xff\xd8' or sig[:4] == b'\x89PNG':
                return r.content
            # Some Pexels URLs return JPEG without proper sig check needing looser test
            if b'JFIF' in r.content[:20] or b'Exif' in r.content[:20]:
                return r.content
        print(f"  [download] Failed or too small: status={r.status_code}, size={len(r.content)}")
        return None
    except Exception as e:
        print(f"  [download] Error for {url}: {e}")
        return None


def crop_resize(img_bytes, width, height):
    """Scale-to-cover then center-crop to exact dimensions."""
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    orig_w, orig_h = img.size
    target_ratio  = width / height
    orig_ratio    = orig_w / orig_h

    if orig_ratio > target_ratio:
        # Wider than needed: scale by height
        new_h = height
        new_w = int(orig_w * (height / orig_h))
    else:
        # Taller than needed: scale by width
        new_w = width
        new_h = int(orig_h * (width / orig_w))

    img = img.resize((new_w, new_h), Image.LANCZOS)
    left   = (new_w - width)  // 2
    top    = (new_h - height) // 2
    img    = img.crop((left, top, left + width, top + height))

    buf = BytesIO()
    img.save(buf, format="JPEG", quality=85, optimize=True)
    return buf.getvalue()


def upload_to_wp(img_bytes, filename, alt_text):
    """Upload image to WP media library. Returns (media_id, src_url) or (None, None)."""
    headers = {
        "Authorization":       f"Basic {auth_str}",
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type":        "image/jpeg",
    }
    try:
        r = requests.post(f"{WP_BASE}/media", headers=headers, data=img_bytes, timeout=120)
        if r.status_code in (200, 201):
            data     = r.json()
            media_id = data["id"]
            src_url  = data["source_url"]
            print(f"  [upload] OK: id={media_id}, url={src_url}")

            # Set alt text
            try:
                r2 = requests.post(
                    f"{WP_BASE}/media/{media_id}",
                    headers={**AUTH_HDR, "Content-Type": "application/json"},
                    json={"alt_text": alt_text},
                    timeout=30
                )
                if r2.status_code in (200, 201):
                    print(f"  [alt-text] Set OK for media {media_id}")
                else:
                    print(f"  [alt-text] Failed HTTP {r2.status_code}: {r2.text[:200]}")
            except Exception as e:
                print(f"  [alt-text] Error: {e}")

            return media_id, src_url
        else:
            print(f"  [upload] FAILED HTTP {r.status_code}: {r.text[:400]}")
            return None, None
    except Exception as e:
        print(f"  [upload] Exception: {e}")
        return None, None


# ---- Pre-selected image URLs (visually verified 2026-06-11) ----------------
# These were chosen after visual QA of thumbnails from Openverse.
# Featured: MacBook laptop desk scene (workspace/strategy context), CC0
# Body1:    Laptop screen with analytics charts (dashboard/metrics context), CC0
# Body2:    Small team at table with laptop (meeting/planning context), CC0

PRE_SELECTED_URLS = {
    "featured": "https://cdn.stocksnap.io/img-thumbs/960w/DWLWL9USBG.jpg",
    "body1":    "https://images.rawpixel.com/editor_1024/cHJpdmF0ZS9zdGF0aWMvaW1hZ2Uvd2Vic2l0ZS8yMDIyLTA0L2xyL3B4NzMwNjI4LWltYWdlLWt3dnYxeGZ5LmpwZw.jpg",
    "body2":    "https://cdn.stocksnap.io/img-thumbs/960w/JBW2PXDOL6.jpg",
}


def source_and_upload(img_spec):
    """Source image, crop, upload. Returns (media_id, src_url) or (None, None)."""
    key      = img_spec["key"]
    filename = img_spec["filename"]
    alt      = img_spec["alt"]
    width    = img_spec["width"]
    height   = img_spec["height"]

    print(f"\n--- Sourcing image: {filename} ---")

    # Use pre-selected visually-verified URL
    candidate_url = PRE_SELECTED_URLS.get(key)
    img_bytes = None

    if candidate_url:
        print(f"  [pre-selected] Using: {candidate_url}")
        img_bytes = download_image(candidate_url)
        if img_bytes:
            print(f"  [download] OK ({len(img_bytes):,} bytes)")

    # Fallback: Pexels
    if not img_bytes and PEXELS_KEY:
        print(f"  [Pexels] Trying fallback for '{img_spec['query']}'...")
        photos = search_pexels(img_spec["query"], per_page=5)
        for i, photo in enumerate(photos[:3]):
            url = photo.get("src", {}).get("large2x") or photo.get("src", {}).get("large")
            if not url:
                continue
            raw = download_image(url)
            if raw:
                img_bytes = raw
                print(f"  [Pexels] Downloaded ({len(raw):,} bytes)")
                break
            time.sleep(0.5)

    # Fallback: Openverse
    if not img_bytes:
        print(f"  [Openverse] Trying fallback for '{img_spec['query']}'...")
        ov_results = search_openverse(img_spec["query"], per_page=8)
        for i, result in enumerate(ov_results[:5]):
            url = result.get("url")
            if not url:
                continue
            raw = download_image(url)
            if raw:
                img_bytes = raw
                print(f"  [Openverse] Downloaded ({len(raw):,} bytes)")
                break
            time.sleep(1)

    if not img_bytes:
        print(f"  [WARN] Could not source image for '{key}'. Skipping.")
        return None, None

    # Crop/resize
    try:
        img_bytes = crop_resize(img_bytes, width, height)
        print(f"  [resize] Cropped to {width}x{height} ({len(img_bytes):,} bytes)")
    except Exception as e:
        print(f"  [resize] Error: {e}")
        return None, None

    # Upload
    return upload_to_wp(img_bytes, filename, alt)


# ---- Read draft HTML -------------------------------------------------------

def read_draft_html():
    """Read draft .md file, strip frontmatter, return HTML string."""
    text = DRAFT_PATH.read_text(encoding="utf-8")
    # Strip YAML frontmatter
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4:].lstrip()
    return text


# ---- Main ------------------------------------------------------------------

def main():
    print("=" * 60)
    print("ImpelHub Post Publisher: reduce-churn-b2b-saas")
    print("=" * 60)

    # Step 1: Source and upload images
    results = {}
    for spec in IMAGES:
        media_id, src_url = source_and_upload(spec)
        results[spec["key"]] = {"media_id": media_id, "src_url": src_url}
        time.sleep(1)

    print("\n--- Image upload summary ---")
    for key, val in results.items():
        print(f"  {key}: id={val['media_id']}, url={val['src_url']}")

    # Step 2: Read draft HTML and inject real image URLs
    html = read_draft_html()

    # Replace body1 placeholder
    body1_url = results["body1"]["src_url"]
    if body1_url:
        html = html.replace(
            "https://impelhub.com/wp-content/uploads/2026/06/PLACEHOLDER-analytics-dashboard.jpg",
            body1_url
        )
        print(f"\n[inject] body1 image URL replaced: {body1_url}")
    else:
        print("\n[inject] body1 upload failed — placeholder remains (will be flagged)")

    # Replace body2 placeholder
    body2_url = results["body2"]["src_url"]
    if body2_url:
        html = html.replace(
            "https://impelhub.com/wp-content/uploads/2026/06/PLACEHOLDER-startup-team-planning.jpg",
            body2_url
        )
        print(f"[inject] body2 image URL replaced: {body2_url}")
    else:
        print("[inject] body2 upload failed — placeholder remains (will be flagged)")

    # Step 3: Build WordPress post payload
    featured_id = results["featured"]["media_id"] or 0

    post_title = "What’s actually causing your B2B SaaS churn: and what to fix first"

    payload = {
        "title":          post_title,
        "content":        html,
        "status":         "draft",
        "featured_media": featured_id,
        "slug":           "reduce-churn-b2b-saas-early-stage",
        "meta": {
            "yoast_wpseo_title":    "Reduce B2B SaaS Churn: Fix the Right Root Cause | ImpelHub",
            "yoast_wpseo_metadesc": "Most early-stage B2B SaaS founders fix the wrong churn problem. Diagnose root cause first: ICP fit, onboarding failure, or product gap. Then fix in sequence.",
            "yoast_wpseo_focuskw":  "reduce churn b2b saas early stage",
        }
    }

    print("\n--- Pushing to WordPress ---")
    print(f"  Status:         {payload['status']}")
    print(f"  Title:          {payload['title']}")
    print(f"  featured_media: {featured_id}")

    try:
        r = requests.post(
            f"{WP_BASE}/posts",
            headers={**AUTH_HDR, "Content-Type": "application/json"},
            json=payload,
            timeout=120
        )
    except Exception as e:
        print(f"  [WP POST] Exception: {e}")
        sys.exit(1)

    if r.status_code not in (200, 201):
        print(f"  [WP POST] FAILED HTTP {r.status_code}")
        print(f"  Response: {r.text[:800]}")
        sys.exit(1)

    post_data   = r.json()
    post_id     = post_data["id"]
    post_link   = post_data.get("link", "")
    post_status = post_data.get("status", "")
    rendered    = post_data.get("content", {}).get("rendered", "")

    print(f"\n  [WP POST] SUCCESS")
    print(f"  Post ID:    {post_id}")
    print(f"  Status:     {post_status}")
    print(f"  Preview:    {post_link}")
    print(f"  featured_media: {post_data.get('featured_media', 0)}")
    print(f"  content.rendered length: {len(rendered)} chars")

    # Step 4: Verify by GETting the post back
    print("\n--- Verifying saved post ---")
    time.sleep(3)
    try:
        rv = requests.get(
            f"{WP_BASE}/posts/{post_id}",
            headers=AUTH_HDR,
            timeout=30
        )
        if rv.status_code == 200:
            vd = rv.json()
            print(f"  GET status:         {vd.get('status')}")
            print(f"  GET featured_media: {vd.get('featured_media', 0)}")
            content_len = len(vd.get("content", {}).get("rendered", ""))
            print(f"  GET content length: {content_len} chars")

            # Confirm status is draft
            if vd.get("status") != "draft":
                print("  [WARN] Status is not draft!")
            if vd.get("featured_media", 0) == 0:
                print("  [WARN] featured_media is 0")
            if content_len == 0:
                print("  [WARN] content.rendered is empty!")
        else:
            print(f"  [GET verify] HTTP {rv.status_code}")
    except Exception as e:
        print(f"  [GET verify] Exception: {e}")

    # Step 5: Check for placeholder URLs still in saved content
    if body1_url is None and "PLACEHOLDER-analytics-dashboard" in rendered:
        print("  [WARN] body1 placeholder still in saved content. Replace manually.")
    if body2_url is None and "PLACEHOLDER-startup-team-planning" in rendered:
        print("  [WARN] body2 placeholder still in saved content. Replace manually.")

    # Step 6: Save published HTML
    published_html_path = PUBLISHED_DIR / "reduce-churn-b2b-saas-2026-06-10.html"
    published_html_path.write_text(html, encoding="utf-8")
    print(f"\n  [save] Published HTML saved to: {published_html_path}")

    # Step 7: Print results
    print("\n" + "=" * 60)
    print("PUBLISH SUMMARY")
    print("=" * 60)
    print(f"  WordPress post ID:    {post_id}")
    print(f"  Status:               {post_status}")
    print(f"  Preview URL:          {post_link}")
    print(f"  Featured media ID:    {featured_id}")
    print(f"  body1 media ID:       {results['body1']['media_id']}")
    print(f"  body2 media ID:       {results['body2']['media_id']}")
    print(f"  Published HTML path:  {published_html_path}")
    print()
    print("YOAST META NOTE:")
    print("  Yoast meta fields may not write via REST API (known WP limitation).")
    print("  If not reflected in the post, set manually in WP dashboard:")
    print("    Title:    Reduce B2B SaaS Churn: Fix the Right Root Cause | ImpelHub")
    print("    Desc:     Most early-stage B2B SaaS founders fix the wrong churn problem.")
    print("              Diagnose root cause first: ICP fit, onboarding failure, or product gap.")
    print("              Then fix in sequence.")
    print("    Focus KW: reduce churn b2b saas early stage")
    print("=" * 60)

    # Return post_id for further use
    return post_id


if __name__ == "__main__":
    main()
