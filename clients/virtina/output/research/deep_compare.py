"""Deep compare post 42177 vs 42202 - find Thrive shortcodes and full structure."""
import os, sys, requests, base64, urllib3, re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://virtina.com"
USERNAME = "anujith"
PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0"}

r177 = requests.get(f"{SITE}/wp-json/wp/v2/posts/42177?context=edit", headers=h, verify=False, timeout=20)
c177 = r177.json()["content"]["raw"]
r202 = requests.get(f"{SITE}/wp-json/wp/v2/posts/42202?context=edit", headers=h, verify=False, timeout=20)
c202 = r202.json()["content"]["raw"]

for label, content in [("42177", c177), ("42202", c202)]:
    print(f"\n{'='*60}")
    print(f"POST {label} — {len(content)} chars")
    print(f"{'='*60}")
    print(f"First 800 chars:")
    print(repr(content[:800]))
    print(f"\nLast 400 chars:")
    print(repr(content[-400:]))

    # Find all Thrive shortcodes
    shortcodes = re.findall(r'\[[a-z_]{3,}[^\]]*\]', content, re.I)
    tve_sc = [s for s in shortcodes if any(x in s.lower() for x in ['tve', 'tcb', 'thrive', 'thrv'])]
    print(f"\nThrive shortcodes ({len(tve_sc)}): {tve_sc[:10]}")
    print(f"All shortcodes ({len(shortcodes)}): {shortcodes[:10]}")

    # Find all <div with data-* attributes
    divs_with_data = re.findall(r'<div[^>]+data-[^>]+>', content, re.I)
    print(f"\ndivs with data-*: {len(divs_with_data)}")
    for d in divs_with_data[:3]:
        print(f"  {d[:120]}")

    # Count SVG-related content
    print(f"\nSVG count: {content.count('<svg')}")
    print(f"fill:#43627f: {content.count('fill:#43627f')}")

    # Find any content that looks like Thrive template marker
    for marker in ['tve_content_before_more', '_tve_template', 'tcb-content', 'thrv-']:
        cnt = content.count(marker)
        if cnt:
            print(f"Marker '{marker}': {cnt}")

    # Find the TOC area and show full surrounding context
    toc = content.find("Table of Contents")
    if toc > 0:
        print(f"\nTOC context (600 chars before, 200 after):")
        print(repr(content[max(0,toc-600):toc+200]))
