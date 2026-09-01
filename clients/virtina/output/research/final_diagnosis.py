"""
Definitive diagnosis:
1. Check all WP settings for Thrive keys
2. Add a plain span (no SVG) before first TOC anchor to test if spans survive
3. If span survives, use CSS background-image SVG instead of inline SVG
"""
import os, sys, requests, base64, urllib3, json, time, re
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
MARKER = "TCBTEST99"

# Read all WP settings
print("=== WP Settings ===")
r_s = requests.get(f"{WP}/settings", headers=h, verify=False, timeout=15)
settings = r_s.json() if isinstance(r_s.json(), dict) else {}
thrive_s = {k: v for k, v in settings.items() if any(x in k.lower() for x in ["tcb", "thrive", "tve", "lightspeed"])}
print(f"Thrive settings: {thrive_s if thrive_s else 'none found'}")
print(f"All setting keys: {list(settings.keys())}")

# Fetch current raw content
r_post = requests.get(f"{WP}/posts/42202?context=edit", headers=h, verify=False, timeout=30)
content = r_post.json()["content"]["raw"]
print(f"\nCurrent SVG count: {content.count(TARGET)}")

# Insert a PLAIN SPAN (no SVG) as marker into the first TOC li
# This tests if any span survives Thrive's processing
content_test = content.replace(
    '</span><a style="color: #00a0e2!important;',
    f'</span><span id="{MARKER}"></span><a style="color: #00a0e2!important;',
    1  # only first occurrence
)
if MARKER not in content_test:
    # Try alternate insertion (the first TOC item might have different structure)
    toc_idx = content.find("Table of Contents")
    first_a = content.find("<a style=", toc_idx)
    content_test = content[:first_a] + f'<span id="{MARKER}"></span>' + content[first_a:]

print(f"Test marker inserted: {MARKER in content_test}")

# PATCH with the test content
print(f"\nPatching with test marker...")
r_p = requests.patch(f"{WP}/posts/42202", json={"content": content_test},
                     headers=hj, verify=False, timeout=60)
print(f"PATCH status: {r_p.status_code}")

time.sleep(5)

# Check live page for the marker
r_live = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                      headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
marker_found = MARKER in r_live.text
svg_found = r_live.text.count(TARGET)
print(f"Live: marker present={marker_found}, SVG count={svg_found}, cache={r_live.headers.get('X-nananana','?')}")

if marker_found:
    print("SUCCESS: Plain span survives! SVG was the issue. Can use CSS background-image approach.")
else:
    print("FAIL: Plain span also stripped. Thrive is removing all spans before anchors.")

# Restore the original content (with SVGs, without test marker)
print("\nRestoring content with SVGs (removing test marker)...")
r_restore = requests.patch(f"{WP}/posts/42202", json={"content": content},
                           headers=hj, verify=False, timeout=60)
print(f"Restore PATCH: {r_restore.status_code}")
