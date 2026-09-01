"""Explore and clear Thrive Lightspeed cache for post 42202."""
import os, requests, base64, urllib3, json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}",
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
     "Content-Type": "application/json"}
BASE = "https://virtina.com/wp-json/tcb/v1"

# Check current lightspeed options
print("=== GET /tcb/v1/lightspeed/options ===")
r = requests.get(f"{BASE}/lightspeed/options", headers=h, verify=False, timeout=20)
print(f"Status: {r.status_code}")
print(r.text[:800])

# Check what analyze returns
print("\n=== GET /tcb/v1/lightspeed/analyze ===")
r2 = requests.get(f"{BASE}/lightspeed/analyze", headers=h, verify=False, timeout=20)
print(f"Status: {r2.status_code}")
print(r2.text[:800])

# Try to trigger optimize/clear for post 42202
print("\n=== POST /tcb/v1/lightspeed/optimize ===")
r3 = requests.post(f"{BASE}/lightspeed/optimize",
                   json={"post_id": 42202, "clear": True},
                   headers=h, verify=False, timeout=30)
print(f"Status: {r3.status_code}")
print(r3.text[:500])

# Also check OPTIONS for each endpoint to understand allowed methods
for ep in ["/lightspeed/analyze", "/lightspeed/options", "/lightspeed/optimize"]:
    r_opt = requests.options(f"{BASE}{ep}", headers=h, verify=False, timeout=10)
    print(f"\nOPTIONS {ep}: {r_opt.headers.get('Allow', 'no Allow')} | {r_opt.text[:100]}")
