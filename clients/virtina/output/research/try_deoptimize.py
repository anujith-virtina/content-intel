"""
Last attempt: try all Thrive REST routes + attempt deoptimize via various methods.
"""
import os, sys, requests, base64, urllib3, json
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
WP = f"{SITE}/wp-json/wp/v2"

# List all TCB routes
print("=== All /tcb/v1 routes ===")
r = requests.get(f"{SITE}/wp-json/tcb/v1", headers=h, verify=False, timeout=15)
data = r.json()
routes = data.get("routes", {})
for route, info in sorted(routes.items()):
    methods = info.get("methods", [])
    print(f"  {','.join(methods):30s} {route}")

print("\n=== Try lightspeed/deoptimize variants ===")
post_id = 42202
tests = [
    ("DELETE", f"{TCB}/lightspeed/optimize",           {"post_id": post_id}),
    ("DELETE", f"{TCB}/lightspeed/optimize/{post_id}", None),
    ("POST",   f"{TCB}/lightspeed/deoptimize",         {"post_id": post_id}),
    ("DELETE", f"{TCB}/lightspeed/{post_id}",          None),
    ("POST",   f"{TCB}/lightspeed/clear",              {"post_id": post_id}),
    ("POST",   f"{TCB}/lightspeed/reset",              {"post_id": post_id}),
    ("DELETE", f"{TCB}/posts/42202",                   None),
    ("POST",   f"{TCB}/posts/42202/lightspeed/clear",  {}),
]
for method, url, body in tests:
    try:
        if method == "DELETE":
            r2 = requests.delete(url, json=body, headers=hj, verify=False, timeout=10)
        elif method == "POST":
            r2 = requests.post(url, json=body, headers=hj, verify=False, timeout=10)
        print(f"  {method:6s} {url.replace(TCB,'')} -> {r2.status_code}: {r2.text[:120]}")
    except Exception as e:
        print(f"  {method:6s} {url.replace(TCB,'')} -> ERROR: {e}")

# Try admin-ajax lightspeed clear action
print("\n=== Try admin-ajax lightspeed actions ===")
ajax_url = f"{SITE}/wp-admin/admin-ajax.php"
ajax_actions = [
    "tcb_lightspeed_clear",
    "tcb_lightspeed_deoptimize",
    "tve_lightspeed_clear",
    "tcb_ls_clear",
    "thrive_lightspeed_clear",
    "tcb_lightspeed_clear_post",
]
for action in ajax_actions:
    r3 = requests.post(ajax_url,
                       data={"action": action, "post_id": post_id, "ID": post_id},
                       headers=h, verify=False, timeout=10)
    print(f"  {action}: {r3.status_code} {r3.text[:80]}")

# Check what post meta is registered for REST API
print("\n=== Registered REST meta for post 42202 ===")
r_schema = requests.get(f"{WP}/posts/42202?context=edit&_fields=meta",
                        headers=h, verify=False, timeout=15)
meta = r_schema.json().get("meta", {})
print(f"REST-accessible meta keys ({len(meta)}): {list(meta.keys())[:30]}")
tcb_keys = {k: v for k, v in meta.items() if any(x in k for x in ['tcb', 'tve', 'thrive', 'lightspeed'])}
print(f"Thrive-related meta: {tcb_keys}")
