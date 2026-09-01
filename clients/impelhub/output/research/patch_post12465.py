#!/usr/bin/env python3
"""
PATCH post 12465 with corrected HTML:
  - n-accordion (elementor-widget-n-accordion) replacing old accordion
  - data-elementor-id="12465" and class="elementor elementor-12465"
"""
import os, sys, re, base64
from pathlib import Path

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

USER = os.environ.get("IMPELHUB_WP_USERNAME", "")
PASS = os.environ.get("IMPELHUB_WP_APP_PASSWORD", "")

if not USER or not PASS:
    print(f"ERROR: Missing credentials")
    sys.exit(1)

WP_BASE  = "https://impelhub.com/wp-json/wp/v2"
POST_ID  = 12465
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
    "Referer": f"https://impelhub.com/wp-admin/post.php?post={POST_ID}&action=edit",
})

DRAFT_PATH = Path(r"C:\content-intel\clients\impelhub\output\drafts\reduce-churn-b2b-saas-2026-06-10.md")

def read_draft():
    text = DRAFT_PATH.read_text(encoding="utf-8")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4:].lstrip()
    return text

def fix_elementor_id(html, post_id):
    html = html.replace('data-elementor-id="0"', f'data-elementor-id="{post_id}"')
    html = html.replace('class="elementor elementor-0"', f'class="elementor elementor-{post_id}"')
    return html

def main():
    print("=" * 60)
    print(f"PATCH ImpelHub post {POST_ID}")
    print("=" * 60)

    html = read_draft()
    html = fix_elementor_id(html, POST_ID)

    placeholders = re.findall(r"PLACEHOLDER[^\"']*", html)
    if placeholders:
        print(f"[WARN] Placeholder image URLs still present: {placeholders}")
        print("       Images need manual upload in WP dashboard.")
    else:
        print("[OK] No placeholder URLs found.")

    # Check accordion type
    if "elementor-widget-n-accordion" in html:
        print("[OK] n-accordion (nested) widget confirmed.")
    elif "elementor-widget-accordion" in html:
        print("[WARN] Old accordion widget still present!")

    # Check elementor ID
    if f'data-elementor-id="{POST_ID}"' in html:
        print(f"[OK] data-elementor-id={POST_ID} confirmed.")

    print(f"\nContent length: {len(html):,} chars")

    payload = {
        "content": html,
        "status":  "draft",
    }

    print(f"\n--- PATCH /posts/{POST_ID} ---")
    try:
        r = SESS.post(
            f"{WP_BASE}/posts/{POST_ID}",
            headers={**AUTH_HDR, "Content-Type": "application/json"},
            json=payload,
            timeout=180,
            verify=False,
        )
    except Exception as e:
        print(f"  PATCH exception: {e}")
        sys.exit(1)

    if r.status_code not in (200, 201):
        print(f"  PATCH FAILED: HTTP {r.status_code}")
        print(f"  {r.text[:1000]}")
        sys.exit(1)

    d = r.json()
    print(f"  PATCH SUCCESS")
    print(f"  Post ID:    {d['id']}")
    print(f"  Status:     {d.get('status')}")
    print(f"  c.rendered: {len(d.get('content', {}).get('rendered', ''))} chars")
    print(f"  Link:       {d.get('link', '')}")

    # Save updated published HTML
    pub = Path(r"C:\content-intel\clients\impelhub\output\published\reduce-churn-b2b-saas-2026-06-10.html")
    pub.write_text(html, encoding="utf-8")
    print(f"\n  Saved: {pub}")

    print("\n" + "=" * 60)
    print("MANUAL STEPS REMAINING:")
    print("  1. Upload 3 images in WP dashboard (Media > Add New):")
    print("     - impelhub-churn-featured.jpg (1200x628) → set as Featured Image")
    print("     - impelhub-churn-body1.jpg (800x450) → replace PLACEHOLDER-analytics-dashboard")
    print("     - impelhub-churn-body2.jpg (800x450) → replace PLACEHOLDER-startup-team-planning")
    print("  2. Set Yoast SEO in WP dashboard:")
    print("     Title:   Reduce B2B SaaS Churn: Fix the Right Root Cause | ImpelHub")
    print("     Desc:    Most early-stage B2B SaaS founders fix the wrong churn problem.")
    print("              Diagnose root cause first: ICP fit, onboarding failure, or product gap.")
    print("     KW:      reduce churn b2b saas early stage")
    print("=" * 60)

if __name__ == "__main__":
    main()
