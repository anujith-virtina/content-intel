"""
Add unicode arrow character to each TOC <a> text content.
This is pure text — Thrive Lightspeed cannot strip text nodes from <a>.
Also reduce <li> left padding since arrow is now inline.
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

# Fetch current content
r = requests.get(f"{WP}/posts/42202?context=edit", headers=h, verify=False, timeout=30)
content = r.json()["content"]["raw"]
print(f"DB: {len(content)} chars, SVGs: {content.count('fill:#43627f')}")

# Step 1: Change <a> color to #43627f (brand color) so arrow matches other blogs
# AND add → character to text content of each TOC <a>
# The TOC <a> elements have style="color: #00a0e2!important; ..."

# Pattern: find each TOC <a> opening tag + text content
# <a style="color: #00a0e2!important; ..." href="#...">Title text</a>
toc_a_pattern = re.compile(
    r'(<li[^>]*8px 0 8px 32px[^>]*>)'
    r'(?:<span[^>]*>.*?</span>)?'  # optional existing SVG span
    r'(<a\s+style=")(color:\s*#00a0e2!important;)([^"]*"[^>]*>)'
    r'([^<]+)',  # the text content
    re.DOTALL
)
matches = toc_a_pattern.findall(content)
print(f"TOC <a> items found: {len(matches)}")
if matches:
    print(f"Sample text: '{matches[0][4][:50]}'")

def transform_toc_item(m):
    li_tag   = m.group(1)
    a_open   = m.group(2)   # '<a style="'
    color    = m.group(3)   # 'color: #00a0e2!important;'
    rest_a   = m.group(4)   # rest of style + href + '>'
    text     = m.group(5)   # the anchor text

    # Change color to brand teal (#43627f) and change padding on li
    new_color = "color: #43627f!important;"

    # Change <li> left padding from 32px to 8px (arrow is now in the text)
    new_li = li_tag.replace("8px 0 8px 32px", "8px 0 8px 8px")

    # Prepend arrow to text — using bold right arrow ➜ (U+279C)
    arrow = "➜ "  # ➜ + non-breaking space

    return new_li + a_open + new_color + rest_a + arrow + text

modified = toc_a_pattern.sub(transform_toc_item, content)

# Verify
arrow_count = modified.count("➜")
color_changed = modified.count("#43627f")
print(f"Arrows added: {arrow_count}, brand color count: {color_changed}")

# Show first TOC item
toc_start = modified.find("Table of Contents")
first_li = modified.find("<li", toc_start)
first_a_close = modified.find("</a>", first_li)
print(f"\nFirst TOC item:\n{modified[first_li:first_a_close+4]}\n")

# PATCH
resp = requests.patch(f"{WP}/posts/42202", json={"content": modified},
                      headers=hj, verify=False, timeout=60)
print(f"PATCH: {resp.status_code}")

print("Waiting 12s...")
time.sleep(12)

r_live = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                      headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
live = r_live.text
arrow_live = "➜" in live or "&#x279C" in live or "279C" in live
cache = r_live.headers.get("X-nananana", "?")
print(f"Live: arrow='{chr(0x279C)}' present={arrow_live}, cache={cache}")

# Show first TOC item in live
toc_start_live = live.find("Table of Contents")
first_li_live = live.find("<li", toc_start_live)
first_a_close_live = live.find("</a>", first_li_live)
print(f"\nFirst live TOC item:\n{live[first_li_live:first_a_close_live+4]}")
