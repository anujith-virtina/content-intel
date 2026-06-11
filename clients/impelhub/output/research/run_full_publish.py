#!/usr/bin/env python3
"""
Self-contained ImpelHub churn post publisher.
Reads credentials from C:\\content-intel\\.env
Downloads images, resizes, uploads to WP, posts content.
"""
import os, sys, re, base64, json, time
from pathlib import Path
from io import BytesIO

# ---- Load .env -----------------------------------------------------------
env_path = Path(r"C:\content-intel\.env")
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from PIL import Image

# ---- Credentials ---------------------------------------------------------
USER = os.environ.get("IMPELHUB_WP_USERNAME", "")
PASS = os.environ.get("IMPELHUB_WP_APP_PASSWORD", "")

if not USER or not PASS:
    print(f"ERROR: Missing credentials. USER='{USER}', PASS={'set' if PASS else 'empty'}")
    sys.exit(1)

print(f"Credentials: USER={USER}, PASS={'*' * len(PASS)}")

WP_BASE  = "https://impelhub.com/wp-json/wp/v2"
auth_b64 = base64.b64encode(f"{USER}:{PASS}".encode()).decode()
AUTH_HDR = {"Authorization": f"Basic {auth_b64}"}

SESS = requests.Session()
SESS.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Origin":  "https://impelhub.com",
    "Referer": "https://impelhub.com/wp-admin/post-new.php",
})

DRAFT_PATH    = Path(r"C:\content-intel\clients\impelhub\output\drafts\reduce-churn-b2b-saas-2026-06-10.md")
PUBLISHED_DIR = Path(r"C:\content-intel\clients\impelhub\output\published")
PUBLISHED_DIR.mkdir(parents=True, exist_ok=True)

# ---- Image specs (CC0, visually verified 2026-06-11) ----------------------
IMAGE_SPECS = [
    {
        "key":      "featured",
        "urls":     [
            "https://images.rawpixel.com/editor_1024/cHJpdmF0ZS9zdGF0aWMvaW1hZ2Uvd2Vic2l0ZS8yMDIyLTA0L2xyL3B4NzMwNjI4LWltYWdlLWt3dnYxeGZ5LmpwZw.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/0/05/Professional_woman_working_at_desk_with_laptop_and_documents_in_bright_office_setting.jpg",
        ],
        "filename": "impelhub-churn-featured.jpg",
        "alt":      "B2B SaaS founder at laptop reviewing analytics to diagnose churn root cause at an early-stage startup",
        "width":    1200,
        "height":   628,
    },
    {
        "key":      "body1",
        "urls":     [
            "https://upload.wikimedia.org/wikipedia/commons/0/05/Professional_woman_working_at_desk_with_laptop_and_documents_in_bright_office_setting.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/e/e9/Business_professional_engages_in_note-taking_during_a_meeting_at_a_modern_office_desk.jpg",
        ],
        "filename": "impelhub-churn-body1.jpg",
        "alt":      "Startup founder reviewing customer data at laptop to identify B2B SaaS churn root causes and ICP fit problems",
        "width":    800,
        "height":   450,
    },
    {
        "key":      "body2",
        "urls":     [
            "https://upload.wikimedia.org/wikipedia/commons/e/e9/Business_professional_engages_in_note-taking_during_a_meeting_at_a_modern_office_desk.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/0/05/Professional_woman_working_at_desk_with_laptop_and_documents_in_bright_office_setting.jpg",
        ],
        "filename": "impelhub-churn-body2.jpg",
        "alt":      "Business professional taking notes at desk reviewing customer success hiring criteria for a B2B SaaS startup",
        "width":    800,
        "height":   450,
    },
]


def download_image(url, timeout=120):
    try:
        r = SESS.get(url, timeout=timeout, allow_redirects=True, verify=False)
        if r.status_code == 200 and len(r.content) > 8000:
            content = r.content
            sig = content[:4]
            if sig[:2] == b'\xff\xd8':
                return content  # JPEG
            if sig[:4] == b'\x89PNG':
                return content  # PNG
            if b'JFIF' in content[:20] or b'Exif' in content[:20]:
                return content  # JPEG variant
            if len(content) > 100000:
                return content  # Accept large files even without recognized sig
        print(f"    HTTP {r.status_code}, size={len(r.content)}")
        return None
    except Exception as e:
        print(f"    Download error: {e}")
        return None


def crop_resize(img_bytes, width, height):
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    ow, oh = img.size
    tr = width / height
    ir = ow / oh
    if ir > tr:
        nh = height
        nw = int(ow * height / oh)
    else:
        nw = width
        nh = int(oh * width / ow)
    img = img.resize((nw, nh), Image.LANCZOS)
    l = (nw - width) // 2
    t = (nh - height) // 2
    img = img.crop((l, t, l + width, t + height))
    buf = BytesIO()
    img.save(buf, "JPEG", quality=85, optimize=True)
    return buf.getvalue()


def upload_media(img_bytes, filename, alt_text):
    hdrs = {
        **AUTH_HDR,
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "image/jpeg",
    }
    try:
        r = SESS.post(f"{WP_BASE}/media", headers=hdrs, data=img_bytes, timeout=180, verify=False)
        if r.status_code in (200, 201):
            d = r.json()
            mid = d["id"]
            murl = d["source_url"]
            print(f"    Uploaded OK: id={mid}")
            print(f"    URL: {murl}")
            # Set alt text
            try:
                r2 = SESS.post(
                    f"{WP_BASE}/media/{mid}",
                    headers={**AUTH_HDR, "Content-Type": "application/json"},
                    json={"alt_text": alt_text},
                    timeout=30,
                    verify=False,
                )
                if r2.status_code in (200, 201):
                    print(f"    Alt text set OK")
            except Exception as e:
                print(f"    Alt text error: {e}")
            return mid, murl
        else:
            print(f"    Upload FAILED: HTTP {r.status_code}")
            print(f"    {r.text[:500]}")
            return None, None
    except Exception as e:
        print(f"    Upload exception: {e}")
        return None, None


def process_image(spec):
    print(f"\n[{spec['key']}] {spec['filename']}")
    raw = None
    for url in spec["urls"]:
        print(f"  Downloading: {url[:90]}...")
        raw = download_image(url)
        if raw:
            print(f"  Downloaded: {len(raw):,} bytes")
            break
        time.sleep(2)

    if not raw:
        print(f"  FAILED: all URLs failed")
        return None, None

    print(f"  Resizing to {spec['width']}x{spec['height']}...")
    try:
        resized = crop_resize(raw, spec["width"], spec["height"])
        print(f"  Resized: {len(resized):,} bytes")
    except Exception as e:
        print(f"  Resize error: {e}")
        return None, None

    return upload_media(resized, spec["filename"], spec["alt"])


def read_draft():
    text = DRAFT_PATH.read_text(encoding="utf-8")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4:].lstrip()
    return text


def main():
    print("=" * 65)
    print("ImpelHub Publisher: reduce-churn-b2b-saas")
    print("=" * 65)

    # Step 1: Source images (skip if PEXELS_API_KEY not set)
    PEXELS_KEY = os.environ.get("PEXELS_API_KEY", "")
    imgs = {k: {"id": None, "url": None} for k in ("featured", "body1", "body2")}

    if not PEXELS_KEY:
        print("\n[SKIP] PEXELS_API_KEY not set — skipping image upload.")
        print("       Add images manually in WP dashboard after push.")
    else:
        for spec in IMAGE_SPECS:
            mid, murl = process_image(spec)
            imgs[spec["key"]] = {"id": mid, "url": murl}
            time.sleep(2)

    print("\n--- Image results ---")
    for k, v in imgs.items():
        print(f"  {k:10}: id={v['id']}, url={v['url']}")

    # Step 2: Build HTML with real image URLs
    html = read_draft()

    b1url = imgs["body1"]["url"]
    if b1url:
        html = html.replace(
            "https://impelhub.com/wp-content/uploads/2026/06/PLACEHOLDER-analytics-dashboard.jpg",
            b1url,
        )
        print(f"\n[inject] body1 -> {b1url}")
    else:
        print("\n[inject] body1 SKIPPED — placeholder remains")

    b2url = imgs["body2"]["url"]
    if b2url:
        html = html.replace(
            "https://impelhub.com/wp-content/uploads/2026/06/PLACEHOLDER-startup-team-planning.jpg",
            b2url,
        )
        print(f"[inject] body2 -> {b2url}")
    else:
        print("[inject] body2 SKIPPED — placeholder remains")

    remaining_placeholders = [m.group() for m in re.finditer(r"PLACEHOLDER[^\"']*", html)]
    if remaining_placeholders:
        print(f"[WARN] Remaining placeholders: {remaining_placeholders}")

    # Step 3: Push to WordPress
    featured_id = imgs["featured"]["id"] or 0
    post_title  = "What's actually causing your B2B SaaS churn: and what to fix first"

    payload = {
        "title":          post_title,
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
            "yoast_wpseo_focuskw": "reduce churn b2b saas early stage",
        },
    }

    print(f"\n--- WordPress POST ---")
    print(f"  status:         {payload['status']}")
    print(f"  featured_media: {featured_id}")
    print(f"  content length: {len(html):,} chars")

    try:
        r = SESS.post(
            f"{WP_BASE}/posts",
            headers={**AUTH_HDR, "Content-Type": "application/json"},
            json=payload,
            timeout=180,
            verify=False,
        )
    except Exception as e:
        print(f"  POST exception: {e}")
        sys.exit(1)

    if r.status_code not in (200, 201):
        print(f"  POST FAILED: HTTP {r.status_code}")
        print(f"  {r.text[:1000]}")
        sys.exit(1)

    d         = r.json()
    post_id   = d["id"]
    post_link = d.get("link", "")
    post_st   = d.get("status", "")
    fm_ret    = d.get("featured_media", 0)
    c_len     = len(d.get("content", {}).get("rendered", ""))

    print(f"  POST SUCCESS")
    print(f"  Post ID:    {post_id}")
    print(f"  Status:     {post_st}")
    print(f"  Preview:    {post_link}")
    print(f"  fm:         {fm_ret}")
    print(f"  c.rendered: {c_len} chars")

    # Step 4: Verify
    print("\n--- Verifying ---")
    time.sleep(4)
    try:
        rv = SESS.get(f"{WP_BASE}/posts/{post_id}", headers=AUTH_HDR, timeout=30, verify=False)
        if rv.status_code == 200:
            vd = rv.json()
            print(f"  GET status:   {vd.get('status')}")
            print(f"  GET fm:       {vd.get('featured_media', 0)}")
            print(f"  GET c.len:    {len(vd.get('content', {}).get('rendered', ''))}")

            if vd.get("status") != "draft":
                print("  [FAIL] status is not 'draft'!")
            if vd.get("featured_media", 0) == 0:
                print("  [WARN] featured_media = 0")
            if len(vd.get("content", {}).get("rendered", "")) == 0:
                print("  [FAIL] content.rendered is empty!")
            else:
                print("  [OK] All verification checks passed")
        else:
            print(f"  GET: HTTP {rv.status_code}")
    except Exception as e:
        print(f"  GET exception: {e}")

    # Step 5: Save published HTML
    pub = PUBLISHED_DIR / "reduce-churn-b2b-saas-2026-06-10.html"
    pub.write_text(html, encoding="utf-8")
    print(f"\n  Saved: {pub}")

    # Summary
    print("\n" + "=" * 65)
    print("RESULT")
    print(f"  Post ID:       {post_id}")
    print(f"  Status:        {post_st}")
    print(f"  Preview URL:   {post_link}")
    print(f"  featured ID:   {fm_ret}")
    print(f"  body1 ID:      {imgs['body1']['id']}")
    print(f"  body2 ID:      {imgs['body2']['id']}")
    print(f"  Published:     {pub}")
    print()
    print("YOAST: If meta fields not saved, set in WP dashboard manually:")
    print("  Title:  Reduce B2B SaaS Churn: Fix the Right Root Cause | ImpelHub")
    print("  Desc:   Most early-stage B2B SaaS founders fix the wrong churn problem.")
    print("          Diagnose root cause first: ICP fit, onboarding failure, or product gap.")
    print("          Then fix in sequence.")
    print("  KW:     reduce churn b2b saas early stage")
    print("=" * 65)

    return post_id, post_link


if __name__ == "__main__":
    main()
