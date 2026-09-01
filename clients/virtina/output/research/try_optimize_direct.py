"""
Direct attempt at Thrive lightspeed optimize endpoint — capture exact error.
"""
import os, sys, requests, base64, urllib3
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

print("=== Current user capabilities ===")
r_me = requests.get(f"{SITE}/wp-json/wp/v2/users/me?context=edit",
                    headers=h, verify=False, timeout=15)
me = r_me.json()
print(f"User: {me.get('name')} (ID {me.get('id')})")
print(f"Roles: {me.get('roles')}")
caps = me.get("capabilities", {})
admin_cap = caps.get("administrator", caps.get("manage_options", "not found"))
print(f"administrator cap: {admin_cap}")
print(f"All caps (first 10): {dict(list(caps.items())[:10])}")

print("\n=== Try POST /lightspeed/optimize ===")
# Try deoptimize — remove post from optimized list
for payload in [
    {"to_optimize": [42202]},
    {"to_optimize": [], "to_deoptimize": [42202]},
    {"post_id": 42202, "action": "deoptimize"},
]:
    r = requests.post(f"{TCB}/lightspeed/optimize",
                      json=payload, headers=hj, verify=False, timeout=20)
    print(f"  POST {payload} -> {r.status_code}: {r.text[:300]}")

print("\n=== Try PATCH /lightspeed/optimize ===")
r2 = requests.patch(f"{TCB}/lightspeed/optimize",
                    json={"to_optimize": [42202]},
                    headers=hj, verify=False, timeout=20)
print(f"  PATCH -> {r2.status_code}: {r2.text[:300]}")

print("\n=== Try PUT /lightspeed/optimize ===")
r3 = requests.put(f"{TCB}/lightspeed/optimize",
                  json={"to_optimize": [42202]},
                  headers=hj, verify=False, timeout=20)
print(f"  PUT -> {r3.status_code}: {r3.text[:300]}")

print("\n=== Check analyze — is post already deoptimized? ===")
r4 = requests.get(f"{TCB}/lightspeed/analyze", headers=h, verify=False, timeout=15)
data = r4.json()
posts = data.get("post", {}).get("items", [])
for p in posts:
    if p.get("id") == 42202:
        print(f"Post 42202: optimized={p.get('optimized')}, full={p}")
        break
