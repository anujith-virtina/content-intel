"""
1. Toggle post 42202 to draft then back to publish (triggers Thrive re-opt).
2. Check WP options for Thrive Lightspeed storage keys.
"""
import os, sys, requests, base64, urllib3, json, time
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

def check_live():
    r = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                     headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
    return r.text.count(TARGET), r.headers.get("X-nananana","?")

# Verify current content has SVGs
r_db = requests.get(f"{WP}/posts/42202?context=edit", headers=h, verify=False, timeout=30)
post = r_db.json()
content = post["content"]["raw"]
print(f"DB SVG count: {content.count(TARGET)}, status: {post['status']}")

svg_count, cache = check_live()
print(f"Live before toggle: SVG={svg_count} cache={cache}")

# Step 1: Set to draft
print("\nSetting to draft...")
r1 = requests.patch(f"{WP}/posts/42202", json={"status": "draft", "content": content},
                    headers=hj, verify=False, timeout=30)
print(f"Draft status: {r1.status_code}, post status: {r1.json().get('status')}")

time.sleep(2)

# Step 2: Set back to publish
print("Setting back to publish...")
r2 = requests.patch(f"{WP}/posts/42202", json={"status": "publish", "content": content},
                    headers=hj, verify=False, timeout=30)
print(f"Publish status: {r2.status_code}, post status: {r2.json().get('status')}")

time.sleep(4)

# Check lightspeed optimize status
r_ls = requests.get(f"{SITE}/wp-json/tcb/v1/lightspeed/analyze", headers=h, verify=False, timeout=20)
ls_data = r_ls.json()
posts = ls_data.get("post", {}).get("items", [])
for p in posts:
    if p.get("id") == 42202:
        print(f"\nLightspeed status after toggle: optimized={p.get('optimized')}")

# Check live page
time.sleep(3)
svg_count2, cache2 = check_live()
print(f"Live after toggle: SVG={svg_count2} cache={cache2}")

# Also try checking WP options for Thrive data via REST settings
print("\n=== WP options probe (try known Thrive transient keys) ===")
tcb_keys = [
    "tcb_lightspeed_post_42202",
    "tcb_lightspeed_42202",
    "tcb_ls_42202",
    "_tcb_lightspeed_version_42202",
    "thrive_lightspeed_42202",
]
for k in tcb_keys:
    r_s = requests.get(f"{WP}/settings", params={"_fields": k}, headers=h, verify=False, timeout=10)
    val = r_s.json().get(k, "NOT_FOUND")
    if val != "NOT_FOUND":
        print(f"  FOUND: {k} = {val}")
