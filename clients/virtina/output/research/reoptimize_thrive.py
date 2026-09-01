"""Clear and re-trigger Thrive Lightspeed optimization for post 42202."""
import os, sys, requests, base64, urllib3, time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}",
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
     "Content-Type": "application/json"}
BASE = "https://virtina.com/wp-json/tcb/v1"

# The args are: key (string, required) + value (int, required)
# Try known Thrive Lightspeed keys to disable optimization for post 42202
print("=== PATCH /tcb/v1/lightspeed/options (key/value pairs) ===")
key_value_pairs = [
    {"key": "post_42202_optimized", "value": 0},
    {"key": "disable_post_42202", "value": 1},
    {"key": "42202", "value": 0},
    {"key": "post_id", "value": 42202},
]
for payload in key_value_pairs:
    r = requests.patch(f"{BASE}/lightspeed/options",
                       json=payload, headers=h, verify=False, timeout=20)
    print(f"  key={payload['key']} value={payload['value']} -> {r.status_code}: {r.text[:100]}")

# Try POST /lightspeed/optimize with correct key/value format
print("\n=== POST /tcb/v1/lightspeed/optimize ===")
for payload in [
    {"key": "post_42202", "value": 1},
    {"key": "post_id", "value": 42202},
]:
    r2 = requests.post(f"{BASE}/lightspeed/optimize",
                       json=payload, headers=h, verify=False, timeout=30)
    print(f"  {payload} -> {r2.status_code}: {r2.text[:150]}")

# Check analyze to see if optimized status changed
print("\n=== Check analyze status after ===")
r3 = requests.get(f"{BASE}/lightspeed/analyze", headers=h, verify=False, timeout=20)
import json
data = r3.json()
posts = data.get("post", {}).get("items", [])
for p in posts:
    if p.get("id") == 42202:
        print(f"Post 42202 optimized status: {p.get('optimized')}")

# Check live page
time.sleep(3)
pg_h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
r_live = requests.get("https://virtina.com/woocommerce-b2b-customer-portal/",
                      headers=pg_h, verify=False, timeout=30)
svg_count = r_live.text.count("fill:#43627f")
print(f"\nLive page SVG count: {svg_count}")
print(f"Cache: {r_live.headers.get('X-nananana','?')}")
