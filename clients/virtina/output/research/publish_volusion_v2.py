"""
Volusion→WooCommerce post v2 — replaces images (HD, section-relevant) and updates post content.
- Uses Openverse source=stocksnap for HD CC0 images
- Deletes old media 42173-42176, uploads fresh images
- PUTs updated content to post 42177
"""
import os, re, base64, json, requests
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

load_dotenv(r"C:\content-intel\.env")
WP_USERNAME = os.environ["WP_USERNAME"]
WP_APP_PASSWORD = os.environ["WP_APP_PASSWORD"]
WP_BASE = "https://virtina.com/wp-json/wp/v2"
auth_str = base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()).decode()
HEADERS = {"Authorization": f"Basic {auth_str}", "Content-Type": "application/json"}

POST_ID = 42177
OLD_MEDIA_IDS = [42173, 42174, 42175, 42176]

# Each image: query must match the section's story, not just a generic keyword
IMAGE_SPECS = [
    {
        "slot": "featured",
        "query": "laptop desk business work",      # professional, ecommerce context
        "target_w": 1309, "target_h": 500,
        "filename": "volusion-woocommerce-migration-featured-1309x500.jpg",
        "alt": "Business owner reviewing eCommerce platform options on laptop, planning Volusion to WooCommerce migration strategy for their growing online store",
    },
    {
        "slot": "section1",
        # Section: billing surprise, hitting walls — person stressed/frustrated at computer
        "query": "stressed working computer office",
        "target_w": 670, "target_h": 352,
        "filename": "volusion-woocommerce-migration-section1-670x352.jpg",
        "alt": "Online store owner frustrated at computer screen after discovering unexpected eCommerce platform billing charges and automatic plan upgrades",
    },
    {
        "slot": "section2",
        # Section: planning a migration, working through steps/checklist
        "query": "business planning whiteboard office team",
        "target_w": 670, "target_h": 352,
        "filename": "volusion-woocommerce-migration-section2-670x352.jpg",
        "alt": "eCommerce team planning platform migration steps on whiteboard, mapping out product data transfer and 301 redirect strategy",
    },
    {
        "slot": "section3",
        # Section: what you gain — growth, analytics, success, open possibilities
        "query": "business analytics dashboard laptop success",
        "target_w": 670, "target_h": 352,
        "filename": "volusion-woocommerce-migration-section3-670x352.jpg",
        "alt": "eCommerce store owner reviewing improved sales analytics dashboard on laptop after successful migration from Volusion to WooCommerce",
    },
]


def search_openverse(query: str, source: str = "stocksnap", per_page: int = 20) -> list:
    """Search Openverse for CC0 images. Returns list of result dicts sorted by resolution."""
    url = "https://api.openverse.org/v1/images/"
    params = {
        "q": query,
        "source": source,
        "license_type": "commercial",
        "mature": "false",
        "page_size": per_page,
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    results = r.json().get("results", [])
    # Sort by resolution (width * height) descending — biggest first
    results.sort(key=lambda x: (x.get("width") or 0) * (x.get("height") or 0), reverse=True)
    return results


def download_image(url: str, openverse_id: str = None) -> bytes:
    """Download image. Falls back to Openverse thumbnail CDN if direct URL fails."""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ContentBot/1.0)",
        "Referer": "https://openverse.org/",
    }
    try:
        r = requests.get(url, headers=headers, timeout=60)
        r.raise_for_status()
        return r.content
    except Exception:
        if openverse_id:
            # Openverse serves its own thumbnail — always works
            thumb_url = f"https://api.openverse.org/v1/images/{openverse_id}/thumb/"
            r = requests.get(thumb_url, timeout=60)
            r.raise_for_status()
            return r.content
        raise


def crop_resize(img_bytes: bytes, target_w: int, target_h: int, quality: int = 82) -> bytes:
    """Scale to fill, then center-crop to exact target dimensions."""
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    new_w = int(src_w * scale)
    new_h = int(src_h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    img = img.crop((left, top, left + target_w, top + target_h))
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    return buf.getvalue()


def upload_to_wp(img_bytes: bytes, filename: str, alt_text: str, title: str) -> dict:
    headers = {
        "Authorization": f"Basic {auth_str}",
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "image/jpeg",
    }
    r = requests.post(f"{WP_BASE}/media", headers=headers, data=img_bytes, timeout=60)
    if r.status_code not in (200, 201):
        raise RuntimeError(f"Media upload failed {r.status_code}: {r.text[:300]}")
    media = r.json()
    media_id = media["id"]
    # Set alt text and title
    requests.post(
        f"{WP_BASE}/media/{media_id}",
        headers=HEADERS,
        json={"alt_text": alt_text, "title": title},
        timeout=30,
    )
    return media


def delete_media(media_id: int) -> bool:
    r = requests.delete(
        f"{WP_BASE}/media/{media_id}",
        headers=HEADERS,
        params={"force": True},
        timeout=30,
    )
    return r.status_code in (200, 204)


def get_best_image(spec: dict) -> tuple[bytes, str]:
    """Search for image and return (raw_bytes, source_url) for the best HD result."""
    print(f"\n[{spec['slot']}] Searching: '{spec['query']}' (stocksnap)")
    results = search_openverse(spec["query"])

    if not results:
        # Fallback to broader stocksnap search
        fallback_q = spec["query"].split()[:2]
        print(f"  No results, fallback: '{' '.join(fallback_q)}'")
        results = search_openverse(" ".join(fallback_q))

    if not results:
        raise RuntimeError(f"No images found for slot {spec['slot']}")

    # Pick first result with width >= 1200 and a real image URL
    chosen = None
    for r in results:
        w = r.get("width") or 0
        url = r.get("url") or ""
        if w >= 1200 and url.startswith("http"):
            chosen = r
            break

    if not chosen:
        # Relax width requirement
        for r in results:
            url = r.get("url") or ""
            if url.startswith("http"):
                chosen = r
                break

    if not chosen:
        raise RuntimeError(f"No usable image found for slot {spec['slot']}")

    print(f"  Selected: {chosen.get('id')} | {chosen.get('width')}x{chosen.get('height')} | {chosen.get('title','')[:60]}")
    img_url = chosen["url"]
    ov_id = chosen.get("id")
    raw = download_image(img_url, openverse_id=ov_id)
    print(f"  Downloaded {len(raw):,} bytes from {img_url[:80]}")
    return raw, img_url


def build_post_content(media_ids: dict, draft_path: str) -> str:
    """Read draft markdown, strip frontmatter, replace image placeholders with real <img> tags."""
    with open(draft_path, encoding="utf-8") as f:
        raw = f.read()

    # Strip YAML frontmatter
    if raw.startswith("---"):
        end = raw.index("---", 3)
        raw = raw[end + 3:].strip()

    # Replace featured image comment (remove it — featured image set via featured_media field)
    raw = re.sub(r"<!-- FEATURED IMAGE:.*?-->", "", raw)

    # Replace body image placeholders
    slot_map = {
        "BODY IMAGE 1": ("section1", media_ids["section1"]),
        "BODY IMAGE 2": ("section2", media_ids["section2"]),
        "BODY IMAGE 3": ("section3", media_ids["section3"]),
    }
    for placeholder, (slot, media_id) in slot_map.items():
        spec = next(s for s in IMAGE_SPECS if s["slot"] == slot)
        wp_url = media_ids[f"{slot}_url"]
        alt = spec["alt"]
        filename = spec["filename"]
        img_html = (
            f'<span data-image-caption="" data-image-display="block" data-image-id="{media_id}" '
            f'data-image-size="full" data-init-width="{spec["target_w"]}" data-init-height="{spec["target_h"]}" '
            f'class="tve_image_frame" style="width:{spec["target_w"]}px;">'
            f'<img class="tve_image wp-image-{media_id}" '
            f'alt="{alt}" '
            f'width="{spec["target_w"]}" height="{spec["target_h"]}" '
            f'src="{wp_url}" '
            f'data-id="{media_id}" '
            f'style="width:{spec["target_w"]}px;"/></span>'
        )
        pattern = rf"<!-- {placeholder}:.*?-->"
        raw = re.sub(pattern, img_html, raw, flags=re.DOTALL)

    return raw.strip()


def main():
    print("=" * 60)
    print("Volusion to WooCommerce post v2: image replacement + content update")
    print("=" * 60)

    # 1. Get new images
    media_ids = {}
    for spec in IMAGE_SPECS:
        raw, src_url = get_best_image(spec)
        resized = crop_resize(raw, spec["target_w"], spec["target_h"])
        size_kb = len(resized) / 1024
        print(f"  Resized to {spec['target_w']}x{spec['target_h']}, {size_kb:.1f} KB")
        if size_kb > 200:
            # Re-compress at lower quality
            resized = crop_resize(raw, spec["target_w"], spec["target_h"], quality=70)
            print(f"  Re-compressed: {len(resized)/1024:.1f} KB")

        title = spec["filename"].replace("-", " ").replace(".jpg", "")
        media = upload_to_wp(resized, spec["filename"], spec["alt"], title)
        media_ids[spec["slot"]] = media["id"]
        media_ids[f"{spec['slot']}_url"] = media.get("source_url", "")
        print(f"  Uploaded -> media ID {media['id']}, URL: {media.get('source_url','')[:80]}")

    print(f"\nNew media IDs: {media_ids}")

    # 2. Build post content
    draft_path = r"C:\content-intel\clients\virtina\output\drafts\volusion-woocommerce-migration-2026-05-11.md"
    content = build_post_content(media_ids, draft_path)
    print(f"\nContent length: {len(content):,} chars")

    # 3. Update post 42177
    payload = {
        "content": content,
        "featured_media": media_ids["featured"],
        "status": "draft",
    }
    print(f"\nUpdating post {POST_ID}...")
    r = requests.put(f"{WP_BASE}/posts/{POST_ID}", headers=HEADERS, json=payload, timeout=60)
    if r.status_code not in (200, 201):
        raise RuntimeError(f"Post update failed {r.status_code}: {r.text[:400]}")

    post = r.json()
    print(f"Post updated OK. Status: {post['status']}, content length: {len(post['content']['rendered'])} chars")

    # 4. Verify
    checks = {
        "title OK": "volusion" in post["title"]["rendered"].lower(),
        "content length OK": len(post["content"]["rendered"]) > 10000,
        f"featured_media {media_ids['featured']}": post.get("featured_media") == media_ids["featured"],
        "status draft": post["status"] == "draft",
    }
    print("\nVerification:")
    for k, v in checks.items():
        print(f"  {k}: {v}")

    # 5. Delete old media
    print(f"\nDeleting old media {OLD_MEDIA_IDS}...")
    for mid in OLD_MEDIA_IDS:
        ok = delete_media(mid)
        print(f"  Deleted {mid}: {ok}")

    # 6. Save results
    results = {
        "post_id": POST_ID,
        "edit_url": f"https://virtina.com/wp-admin/post.php?post={POST_ID}&action=edit",
        "media_ids": media_ids,
        "checks": checks,
    }
    out_path = r"C:\content-intel\clients\virtina\output\research\volusion_post_v2_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")
    print("\nDone. Next step: Launch Thrive Architect at the edit URL above.")


if __name__ == "__main__":
    main()
