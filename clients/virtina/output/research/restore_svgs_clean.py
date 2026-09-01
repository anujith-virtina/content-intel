"""
Restore SVG spans to post 42202 DB content (clean — remove bg-image, add SVG spans).
Once Thrive Lightspeed is deoptimized for this post, these SVGs will render correctly
(same as post 42177 which is not Lightspeed-optimized and shows SVGs fine).
"""
import os, sys, requests, base64, urllib3, re, time
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

# The SVG arrow span — same format as post 42177
SVG_SPAN = (
    '<span aria-hidden="true" style="position:absolute!important;left:0!important;'
    'top:8px!important;display:inline-block!important;width:18px!important;height:18px!important;">'
    '<svg viewBox="0 0 24 24" width="18" height="18" '
    'style="fill:#43627f!important;" '
    'xmlns="http://www.w3.org/2000/svg">'
    '<path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/>'
    '</svg></span>'
)

# Fetch current content
r = requests.get(f"{WP}/posts/42202?context=edit", headers=h, verify=False, timeout=30)
content = r.json()["content"]["raw"]
print(f"Current DB: {len(content)} chars")
print(f"SVG spans: {content.count('fill:#43627f')}")
print(f"background-image entries: {content.count('background-image')}")

# Step 1: Remove any background-image additions from previous attempts
# Pattern: background-image:url(...) added to <li> style attributes
bg_pattern = re.compile(
    r'background-image:[^;]+;background-repeat:[^;]+;background-position:[^;]+;background-size:[^;]+;',
    re.DOTALL
)
clean = bg_pattern.sub('', content)
print(f"After removing bg-image: {len(clean)} chars, bg-image remaining: {clean.count('background-image')}")

# Step 2: Also remove any existing SVG spans (to avoid doubles)
clean = re.sub(
    r'<span[^>]*aria-hidden[^>]*>.*?</span>(?=<a)',
    '',
    clean,
    flags=re.DOTALL
)
print(f"After removing existing SVG spans: {len(clean)} chars, SVG spans: {clean.count('fill:#43627f')}")

# Step 3: Add SVG span before each TOC <a>
# Pattern: <li style="...padding: 8px 0 8px 32px..."><a style=
toc_pattern = re.compile(
    r'(<li[^>]*?padding[^>]*?8px 0 8px 32px[^>]*?>)'
    r'(<a\s)',
    re.DOTALL
)
matches = toc_pattern.findall(clean)
print(f"TOC <li><a> pairs found: {len(matches)}")

fixed = toc_pattern.sub(lambda m: m.group(1) + SVG_SPAN + m.group(2), clean)
svg_count = fixed.count('fill:#43627f')
print(f"SVG spans added: {svg_count}")

# Verify first TOC item
toc_start = fixed.find("Table of Contents")
first_li = fixed.find("<li", toc_start)
print(f"\nFirst TOC <li> preview (350 chars):\n{fixed[first_li:first_li+350]}\n")

# PATCH
print("PATCHing post 42202 with SVG spans...")
resp = requests.patch(f"{WP}/posts/42202", json={"content": fixed},
                      headers=hj, verify=False, timeout=60)
print(f"PATCH status: {resp.status_code}")

if resp.status_code == 200:
    # Verify stored in DB
    r2 = requests.get(f"{WP}/posts/42202?context=edit", headers=h, verify=False, timeout=30)
    stored = r2.json()["content"]["raw"]
    print(f"DB verified: SVG spans = {stored.count('fill:#43627f')}, bg-image = {stored.count('background-image')}")
    print("\nDB content is ready with SVG arrows.")
    print("Next step: Deoptimize post 42202 in Thrive Dashboard (see instructions below).")
else:
    print(f"ERROR: {resp.text[:300]}")
