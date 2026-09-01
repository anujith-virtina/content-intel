"""Diagnose exactly what's in the live page vs raw DB for post 42202."""
import os, requests, base64, urllib3, re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
api_h = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0"}
pg_h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

POST_ID = 42202

# Raw DB content
r = requests.get(f"https://virtina.com/wp-json/wp/v2/posts/{POST_ID}?context=edit",
                 headers=api_h, verify=False, timeout=30)
raw = r.json()["content"]["raw"]
print(f"Raw DB length: {len(raw)}")
print(f"Raw SVG count: {raw.count('fill:#43627f')}")
print(f"Raw <span with absolute> count: {raw.count('position:absolute')}")

# Show exactly what's around TOC items in the raw content
toc_start = raw.find("Table of Contents")
if toc_start >= 0:
    toc_block = raw[toc_start:toc_start+800]
    print(f"\nRaw TOC block:\n{toc_block}\n")

# Live page
r2 = requests.get("https://virtina.com/woocommerce-b2b-customer-portal/",
                  headers=pg_h, verify=False, timeout=30)
live = r2.text
print(f"\nLive page length: {len(live)}")
print(f"Live SVG count: {live.count('fill:#43627f')}")
print(f"Live 'position:absolute' count: {live.count('position:absolute')}")

# Search for the span/svg in live page (maybe slightly different format)
live_toc = live.find("Table of Contents")
if live_toc >= 0:
    print(f"\nLive TOC block (800 chars):\n{live[live_toc:live_toc+800]}\n")

# Search for the SVG path specifically
svg_path = "M4,11V13H16L10.5"
print(f"\nSVG path in raw: {raw.count(svg_path)}")
print(f"SVG path in live: {live.count(svg_path)}")

# Look for any svg tag in live
svg_tags = re.findall(r'<svg[^>]*>', live)
print(f"\nAll <svg> tags in live page: {len(svg_tags)}")
for t in svg_tags[:5]:
    print(f"  {t[:100]}")
