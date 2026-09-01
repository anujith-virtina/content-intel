"""
Test: put SVG directly INSIDE the <a> tag (as first child, not a sibling).
Thrive strips siblings of <a>. Does it also strip children of <a>?
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
MARKER = "ANCHOR_CHILD_TEST88"

# Fetch current content
r = requests.get(f"{WP}/posts/42202?context=edit", headers=h, verify=False, timeout=30)
content = r.json()["content"]["raw"]
print(f"DB content: {len(content)} chars")

# Find first TOC <a> tag and insert a plain span INSIDE it as first child
# Pattern: <a style="color: #00a0e2... find first one after Table of Contents
toc_idx = content.find("Table of Contents")
first_a_start = content.find("<a style=", toc_idx)
# Find the end of the opening <a> tag
a_tag_end = content.find(">", first_a_start) + 1
print(f"First TOC <a> tag ends at position {a_tag_end}")
print(f"Context: ...{content[first_a_start:a_tag_end+50]}...")

# Insert a plain span with our marker as first child of <a>
marker_span = f'<span id="{MARKER}" style="display:none;">{MARKER}</span>'
content_test = content[:a_tag_end] + marker_span + content[a_tag_end:]
print(f"Marker inserted: {MARKER in content_test}")

# PATCH
r_p = requests.patch(f"{WP}/posts/42202", json={"content": content_test},
                     headers=hj, verify=False, timeout=60)
print(f"PATCH status: {r_p.status_code}")

print("Waiting 12s for Batcache...")
time.sleep(12)

# Check live
r_live = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                      headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
found = MARKER in r_live.text
cache = r_live.headers.get("X-nananana", "?")
print(f"\nLive: marker_inside_anchor={found}, cache={cache}")

if found:
    print("SUCCESS: Child of <a> survives Thrive! Can embed SVG inside anchor.")
    # Show context
    idx = r_live.text.find(MARKER)
    print(f"Context: ...{r_live.text[idx-100:idx+100]}...")
else:
    print("FAIL: Children of <a> also stripped by Thrive.")

# Restore the original content (without test marker)
print("\nRestoring content (removing test marker)...")
r_restore = requests.patch(f"{WP}/posts/42202", json={"content": content},
                           headers=hj, verify=False, timeout=60)
print(f"Restore status: {r_restore.status_code}")
