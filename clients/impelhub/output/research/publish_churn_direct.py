#!/usr/bin/env python3
"""
ImpelHub churn post publisher — direct image download + WP push
Run: python publish_churn_direct.py
Expects env vars: IMPELHUB_WP_USERNAME, IMPELHUB_WP_APP_PASSWORD
"""
import os, sys, base64, json, time, re
from pathlib import Path
from io import BytesIO

import requests
from PIL import Image

# ---- Credentials -----------------------------------------------------------
USER = os.environ.get("IMPELHUB_WP_USERNAME", "")
PASS = os.environ.get("IMPELHUB_WP_APP_PASSWORD", "")

if not USER or not PASS:
    print("ERROR: IMPELHUB_WP_USERNAME or IMPELHUB_WP_APP_PASSWORD not set.")
    sys.exit(1)

WP_BASE  = "https://impelhub.com/wp-json/wp/v2"
auth_b64 = base64.b64encode(f"{USER}:{PASS}".encode()).decode()
AUTH_HDR = {"Authorization": f"Basic {auth_b64}"}

SESS = requests.Session()
SESS.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
})

DRAFT_PATH    = Path(r"C:\content-intel\clients\impelhub\output\drafts\reduce-churn-b2b-saas-2026-06-10.md")
PUBLISHED_DIR = Path(r"C:\content-intel\clients\impelhub\output\published")
PUBLISHED_DIR.mkdir(parents=True, exist_ok=True)

# ---- Images (visually pre-selected, CC0) -----------------------------------
# Verified via thumbnail visual review 2026-06-11:
#  featured: rawpixel laptop with analytics charts — clean, professional workspace
#  body1:    wikimedia commons — professional woman working at laptop in bright office
#  body2:    wikimedia commons — business professional taking notes at meeting desk

IMAGE_SPECS = [
    {
        "key":      "featured",
        "url":      "https://images.rawpixel.com/editor_1024/cHJpdmF0ZS9zdGF0aWMvaW1hZ2Uvd2Vic2l0ZS8yMDIyLTA0L2xyL3B4NzMwNjI4LWltYWdlLWt3dnYxeGZ5LmpwZw.jpg",
        "fallback": "https://upload.wikimedia.org/wikipedia/commons/0/05/Professional_woman_working_at_desk_with_laptop_and_documents_in_bright_office_setting.jpg",
        "filename": "impelhub-churn-featured.jpg",
        "alt":      "B2B SaaS founder at laptop reviewing analytics and churn data to diagnose retention problems at an early-stage startup",
        "width":    1200,
        "height":   628,
    },
    {
        "key":      "body1",
        "url":      "https://upload.wikimedia.org/wikipedia/commons/0/05/Professional_woman_working_at_desk_with_laptop_and_documents_in_bright_office_setting.jpg",
        "fallback": "https://upload.wikimedia.org/wikipedia/commons/e/e9/Business_professional_engages_in_note-taking_during_a_meeting_at_a_modern_office_desk.jpg",
        "filename": "impelhub-churn-body1.jpg",
        "alt":      "Startup founder reviewing customer data and analytics to identify B2B SaaS churn root causes and ICP fit problems",
        "width":    800,
        "height":   450,
    },
    {
        "key":      "body2",
        "url":      "https://upload.wikimedia.org/wikipedia/commons/e/e9/Business_professional_engages_in_note-taking_during_a_meeting_at_a_modern_office_desk.jpg",
        "fallback": "https://upload.wikimedia.org/wikipedia/commons/0/05/Professional_woman_working_at_desk_with_laptop_and_documents_in_bright_office_setting.jpg",
        "filename": "impelhub-churn-body2.jpg",
        "alt":      "Small startup team planning customer success hiring and churn reduction strategy at a B2B SaaS company",
        "width":    800,
        "height":   450,
    },
]


def download_image(url):
    """Download image, return bytes or None."""
    try:
        r = SESS.get(url, timeout=60, allow_redirects=True)
        if r.status_code == 200 and len(r.content) > 8000:
            sig = r.content[:4]
            if (sig[:2] == b'\xff\xd8' or sig[:4] == b'\x89PNG'
                    or b'JFIF' in r.content[:20] or b'Exif' in r.content[:20]):
                print(f"    OK ({len(r.content):,} bytes)")
                return r.content
            # Accept anything large enough if not identifiable
            if len(r.content) > 50000:
                print(f"    OK (unknown sig, {len(r.content):,} bytes)")
                return r.content
        print(f"    FAILED: status={r.status_code}, size={len(r.content)}")
        return None
    except Exception as e:
        print(f"    Exception: {e}")
        return None


def crop_resize(img_bytes, width, height):
    """Scale-to-cover, center-crop."""
    img    = Image.open(BytesIO(img_bytes)).convert("RGB")
    ow, oh = img.size
    tr     = width / height
    ir     = ow / oh
    if ir > tr:
        nh = height
        nw = int(ow * height / oh)
    else:
        nw = width
        nh = int(oh * width / ow)
    img  = img.resize((nw, nh), Image.LANCZOS)
    l    = (nw - width)  // 2
    t    = (nh - height) // 2
    img  = img.crop((l, t, l + width, t + height))
    buf  = BytesIO()
    img.save(buf, "JPEG", quality=85, optimize=True)
    return buf.getvalue()


def upload_media(img_bytes, filename, alt_text):
    """Upload to WP media. Returns (id, url) or (None, None)."""
    hdrs = {
        **AUTH_HDR,
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type":        "image/jpeg",
    }
    try:
        r = requests.post(f"{WP_BASE}/media", headers=hdrs, data=img_bytes, timeout=120)
        if r.status_code in (200, 201):
            d   = r.json()
            mid = d["id"]
            mur = d["source_url"]
            print(f"    Uploaded: id={mid}, url={mur}")
            # Set alt text
            try:
                r2 = requests.post(
                    f"{WP_BASE}/media/{mid}",
                    headers={**AUTH_HDR, "Content-Type": "application/json"},
                    json={"alt_text": alt_text},
                    timeout=30,
                )
                if r2.status_code in (200, 201):
                    print(f"    Alt text set OK")
                else:
                    print(f"    Alt text set FAILED: {r2.status_code}")
            except Exception as e:
                print(f"    Alt text exception: {e}")
            return mid, mur
        else:
            print(f"    Upload FAILED: {r.status_code}\n    {r.text[:400]}")
            return None, None
    except Exception as e:
        print(f"    Upload exception: {e}")
        return None, None


def source_image(spec):
    """Download, resize, upload. Returns (id, url) or (None, None)."""
    print(f"\n[Image: {spec['key']}] {spec['filename']}")

    raw = None
    for attempt_url in [spec["url"], spec.get("fallback")]:
        if not attempt_url:
            continue
        print(f"  Downloading: {attempt_url[:80]}...")
        raw = download_image(attempt_url)
        if raw:
            break
        time.sleep(1)

    if not raw:
        print(f"  WARN: All download attempts failed for {spec['key']}")
        return None, None

    print(f"  Resizing to {spec['width']}x{spec['height']}...")
    try:
        resized = crop_resize(raw, spec["width"], spec["height"])
        print(f"  Resized: {len(resized):,} bytes")
    except Exception as e:
        print(f"  Resize error: {e}")
        return None, None

    print(f"  Uploading to WordPress...")
    return upload_media(resized, spec["filename"], spec["alt"])


def read_draft_html():
    """Strip YAML frontmatter from draft, return HTML."""
    text = DRAFT_PATH.read_text(encoding="utf-8")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4:].lstrip()
    return text


def main():
    print("=" * 62)
    print("ImpelHub Post Publisher: reduce-churn-b2b-saas-2026-06-10")
    print("=" * 62)

    # --- Step 1: Source and upload all images ---
    image_results = {}
    for spec in IMAGE_SPECS:
        mid, mur = source_image(spec)
        image_results[spec["key"]] = {"id": mid, "url": mur}
        time.sleep(1)

    print("\n--- Image upload summary ---")
    for k, v in image_results.items():
        status = "OK" if v["id"] else "FAILED"
        print(f"  {k:10s}: [{status}] id={v['id']}, url={v['url']}")

    # --- Step 2: Read draft and inject real image URLs ---
    html = read_draft_html()

    body1_url = image_results["body1"]["url"]
    if body1_url:
        html = html.replace(
            "https://impelhub.com/wp-content/uploads/2026/06/PLACEHOLDER-analytics-dashboard.jpg",
            body1_url
        )
        print(f"\n[inject] body1 URL: {body1_url}")
    else:
        print("\n[inject] body1 SKIPPED (upload failed)")

    body2_url = image_results["body2"]["url"]
    if body2_url:
        html = html.replace(
            "https://impelhub.com/wp-content/uploads/2026/06/PLACEHOLDER-startup-team-planning.jpg",
            body2_url
        )
        print(f"[inject] body2 URL: {body2_url}")
    else:
        print("[inject] body2 SKIPPED (upload failed)")

    # Verify no placeholder URLs remain
    if "PLACEHOLDER" in html:
        print("[WARN] Placeholder URL(s) still present in HTML. These must be replaced manually.")

    # --- Step 3: Build and POST WordPress payload ---
    featured_id = image_results["featured"]["id"] or 0

    payload = {
        "title":          "What's actually causing your B2B SaaS churn: and what to fix first",
        "content":        html,
        "status":         "draft",
        "slug":           "reduce-churn-b2b-saas-early-stage",
        "featured_media": featured_id,
        "meta": {
            "yoast_wpseo_title":    "Reduce B2B SaaS Churn: Fix the Right Root Cause | ImpelHub",
            "yoast_wpseo_metadesc": (
                "Most early-stage B2B SaaS founders fix the wrong churn problem. "
                "Diagnose root cause first: ICP fit, onboarding failure, or product gap. "
                "Then fix in sequence."
            ),
            "yoast_wpseo_focuskw":  "reduce churn b2b saas early stage",
        }
    }

    print(f"\n--- Pushing to WordPress (status: {payload['status']}) ---")
    print(f"  title:          {payload['title']}")
    print(f"  featured_media: {featured_id}")
    print(f"  content length: {len(html):,} chars")

    try:
        r = requests.post(
            f"{WP_BASE}/posts",
            headers={**AUTH_HDR, "Content-Type": "application/json"},
            json=payload,
            timeout=180,
        )
    except Exception as e:
        print(f"  POST exception: {e}")
        sys.exit(1)

    if r.status_code not in (200, 201):
        print(f"  POST FAILED: {r.status_code}")
        print(f"  Response: {r.text[:1000]}")
        sys.exit(1)

    d           = r.json()
    post_id     = d["id"]
    post_link   = d.get("link", "")
    post_status = d.get("status", "")
    fm_id       = d.get("featured_media", 0)
    rendered_l  = len(d.get("content", {}).get("rendered", ""))

    print(f"\n  POST SUCCESS")
    print(f"  Post ID:              {post_id}")
    print(f"  Status:               {post_status}")
    print(f"  Preview URL:          {post_link}")
    print(f"  featured_media:       {fm_id}")
    print(f"  content.rendered len: {rendered_l} chars")

    # --- Step 4: Verify via GET ---
    print("\n--- Verifying saved post ---")
    time.sleep(4)
    try:
        rv = requests.get(f"{WP_BASE}/posts/{post_id}", headers=AUTH_HDR, timeout=30)
        if rv.status_code == 200:
            vd = rv.json()
            v_status = vd.get("status")
            v_fm     = vd.get("featured_media", 0)
            v_clen   = len(vd.get("content", {}).get("rendered", ""))
            print(f"  GET status:         {v_status}")
            print(f"  GET featured_media: {v_fm}")
            print(f"  GET content length: {v_clen} chars")

            fails = []
            if v_status != "draft":
                fails.append(f"status is '{v_status}' not 'draft'")
            if v_fm == 0:
                fails.append("featured_media is 0")
            if v_clen == 0:
                fails.append("content.rendered is empty")
            if fails:
                print("  [WARN] Verification issues: " + "; ".join(fails))
            else:
                print("  [OK] All verification checks passed")
        else:
            print(f"  GET failed: {rv.status_code}")
    except Exception as e:
        print(f"  GET exception: {e}")

    # --- Step 5: Save published HTML ---
    pub_path = PUBLISHED_DIR / "reduce-churn-b2b-saas-2026-06-10.html"
    pub_path.write_text(html, encoding="utf-8")
    print(f"\n  Published HTML saved: {pub_path}")

    # --- Summary ---
    print("\n" + "=" * 62)
    print("PUBLISH SUMMARY")
    print("=" * 62)
    print(f"  WordPress post ID:    {post_id}")
    print(f"  Status:               {post_status}")
    print(f"  Preview URL:          {post_link}")
    print(f"  Featured media ID:    {fm_id}")
    print(f"  body1 media ID:       {image_results['body1']['id']}")
    print(f"  body2 media ID:       {image_results['body2']['id']}")
    print(f"  Published HTML:       {pub_path}")
    print()
    print("YOAST META:")
    print("  REST API may not persist Yoast fields. If blank in WP dashboard, set manually:")
    print("  Title:    Reduce B2B SaaS Churn: Fix the Right Root Cause | ImpelHub")
    print("  Desc:     Most early-stage B2B SaaS founders fix the wrong churn problem.")
    print("            Diagnose root cause first: ICP fit, onboarding failure, or product gap.")
    print("            Then fix in sequence.")
    print("  Focus KW: reduce churn b2b saas early stage")
    print("=" * 62)

    return post_id


if __name__ == "__main__":
    main()
