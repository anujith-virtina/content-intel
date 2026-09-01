"""
Fix TOC arrows using CSS background-image on the <li> element itself.
No extra <span> or <svg> element — Thrive strips those.
The arrow becomes a background-image on the <li>, which Thrive preserves.
"""
import os, sys, re, requests, base64, urllib3, time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}",
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
hj = {**h, "Content-Type": "application/json"}
SITE = "https://virtina.com"
WP = f"{SITE}/wp-json/wp/v2"
TARGET = "fill:#43627f"

# SVG as a URL-encoded data URI (no HTML element, pure CSS)
# Arrow path: M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z
SVG_DATA_URI = (
    "url(\"data:image/svg+xml,%3Csvg viewBox='0 0 24 24' width='18' height='18' "
    "xmlns='http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg'%3E"
    "%3Cpath fill='%2343627f' d='M4%2C11V13H16L10.5%2C18.5L11.92%2C19.92L19.84%2C12L11.92%2C4.08L10.5%2C5.5L16%2C11H4Z'%2F%3E"
    "%3C%2Fsvg%3E\")"
)

# Fetch current raw content
r = requests.get(f"{WP}/posts/42202?context=edit", headers=h, verify=False, timeout=30)
content = r.json()["content"]["raw"]
print(f"Current content: {len(content)} chars, SVG spans: {content.count(TARGET)}")

# Step 1: Remove any existing SVG spans from TOC (the ones Thrive strips)
# Pattern: <span aria-hidden...><svg...></svg></span> before <a in TOC list items
clean = re.sub(
    r'<span[^>]*aria-hidden[^>]*>.*?</span>(?=<a)',
    '',
    content,
    flags=re.DOTALL
)
remaining_spans = clean.count('aria-hidden')
print(f"After removing SVG spans: {len(clean)} chars, remaining aria-hidden: {remaining_spans}")

# Step 2: Replace <li style="...padding: 8px 0 8px 32px..."> with version
# that has background-image + background-position + background-size + background-repeat
# The <li> already has position:relative, so background-image will overlay correctly

# Pattern: <li style="..."> items in the TOC (those with padding: 8px 0 8px 32px)
# We need to INSERT the background-image into the existing style attribute

def add_bg_image_to_li(m):
    """Add background-image to an existing <li> style that has the TOC pattern."""
    tag = m.group(0)
    # Insert background properties at the end of the style value (before the closing quote)
    bg_addition = (
        f"background-image:{SVG_DATA_URI}!important;"
        "background-repeat:no-repeat!important;"
        "background-position:0 8px!important;"
        "background-size:18px 18px!important;"
    )
    # Find the style attribute closing and insert before it
    tag_with_bg = re.sub(
        r'(style="[^"]*)"',
        rf'\1{bg_addition}"',
        tag,
        count=1
    )
    return tag_with_bg

toc_li_pattern = re.compile(
    r'<li\s+style="[^"]*padding[^"]*8px 0 8px 32px[^"]*"[^>]*>',
    re.DOTALL
)
matches = toc_li_pattern.findall(clean)
print(f"TOC <li> items found: {len(matches)}")

fixed = toc_li_pattern.sub(add_bg_image_to_li, clean)

# Verify
bg_image_count = fixed.count("background-image")
print(f"background-image occurrences: {bg_image_count}")

# Show what the first TOC item looks like now
toc_start = fixed.find("Table of Contents")
first_li_start = fixed.find("<li", toc_start)
print(f"\nFirst TOC <li> preview (200 chars):\n{fixed[first_li_start:first_li_start+200]}")

# PATCH
print("\nPatching post with background-image approach...")
resp = requests.patch(f"{WP}/posts/42202", json={"content": fixed},
                      headers=hj, verify=False, timeout=60)
print(f"PATCH status: {resp.status_code}")
if resp.status_code != 200:
    print(f"Error: {resp.text[:300]}")
    raise SystemExit(1)

# Wait for Batcache to refresh
print("Waiting 10s for Batcache to cycle...")
time.sleep(10)

# Check live page
r_live = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                      headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
                      verify=False, timeout=30)
live = r_live.text
bg_in_live = "background-image" in live
svg_data_in_live = "43627f" in live  # partial match
cache = r_live.headers.get("X-nananana", "?")
print(f"\nLive check: background-image present={bg_in_live}, #43627f present={svg_data_in_live}")
print(f"Cache: {cache}")

# Show first TOC li from live page
toc_live = live.find("Table of Contents")
first_li_live = live.find("<li", toc_live)
if first_li_live >= 0:
    print(f"\nFirst TOC <li> in live (300 chars):\n{live[first_li_live:first_li_live+300]}")
