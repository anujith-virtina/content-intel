"""Deep dive on Thrive APIs and try all known ways to clear lightspeed."""
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
TCB = f"{SITE}/wp-json/tcb/v1"

# Get all TCB routes
print("=== All /tcb/v1 routes ===")
r = requests.get(f"{SITE}/wp-json/tcb/v1", headers=h, verify=False, timeout=15)
data = r.json()
routes = data.get("routes", {})
for route, info in routes.items():
    methods = info.get("methods", [])
    print(f"  {','.join(methods):20s} {route}")

# Try getting a REST nonce via admin-ajax with basic auth
print("\n=== Try REST nonce via admin-ajax ===")
r_n = requests.get(f"{SITE}/wp-admin/admin-ajax.php?action=rest-nonce",
                   headers=h, verify=False, timeout=15)
print(f"  rest-nonce: {r_n.status_code} {r_n.text[:60]}")

# Try tcb specific AJAX nonces
for action in ["tcb_get_nonce", "tcb_lightspeed_nonce", "tve_get_nonce"]:
    r_na = requests.post(f"{SITE}/wp-admin/admin-ajax.php",
                         data={"action": action},
                         headers=h, verify=False, timeout=10)
    print(f"  {action}: {r_na.status_code} {r_na.text[:60]}")

# Try lightspeed/optimize with extra headers
print("\n=== Try optimize with X-WP-Nonce and Referer ===")
extra_headers = {**hj,
                 "X-WP-Nonce": "fake_nonce_test",
                 "Referer": f"{SITE}/wp-admin/admin.php?page=thrive_dashboard",
                 "X-Requested-With": "XMLHttpRequest"}
r_opt = requests.post(f"{TCB}/lightspeed/optimize",
                      json={"to_optimize": [42202]},
                      headers=extra_headers, verify=False, timeout=20)
print(f"  status: {r_opt.status_code} {r_opt.text[:200]}")

# Try DELETE on lightspeed optimize to clear/deoptimize
print("\n=== Try DELETE /lightspeed/optimize ===")
r_del = requests.delete(f"{TCB}/lightspeed/optimize",
                        json={"post_id": 42202},
                        headers=hj, verify=False, timeout=20)
print(f"  DELETE status: {r_del.status_code} {r_del.text[:200]}")

# Try modifying post meta directly to mark cache as stale
print("\n=== Try PATCH post with _tcb meta fields ===")
for meta_key in ["_tcb_lightspeed_version", "_tve_lightspeed_optimized",
                 "tcb_lightspeed_hash", "_tcb_cached_content"]:
    rm = requests.patch(f"{SITE}/wp-json/wp/v2/posts/42202",
                        json={"meta": {meta_key: "0"}},
                        headers=hj, verify=False, timeout=15)
    print(f"  {meta_key}: {rm.status_code} {rm.text[:80]}")
