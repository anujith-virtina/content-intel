"""
Try admin-ajax lightspeed actions with real session + nonce.
Also check who the Thrive admin user is and try Thrive-specific admin pages.
"""
import os, sys, requests, urllib3, re, time, json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://virtina.com"
USERNAME = "anujith"
PASSWORD = os.environ.get("WP_REAL_PASSWORD", "")
TCB = f"{SITE}/wp-json/tcb/v1"

session = requests.Session()
session.verify = False
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

# Login
session.get(f"{SITE}/wp-login.php", timeout=15)
session.post(f"{SITE}/wp-login.php", data={
    "log": USERNAME, "pwd": PASSWORD, "wp-submit": "Log In",
    "redirect_to": f"{SITE}/wp-admin/", "testcookie": "1",
}, allow_redirects=True, timeout=20)
logged_in = any("logged_in" in k.lower() for k in session.cookies.keys())
print(f"Logged in: {logged_in}")

# Get REST nonce
r_nonce = session.get(f"{SITE}/wp-admin/admin-ajax.php?action=rest-nonce", timeout=10)
nonce = r_nonce.text.strip()
print(f"REST nonce: {nonce}")

ajax_url = f"{SITE}/wp-admin/admin-ajax.php"

# Try all lightspeed AJAX actions with nonce
print("\n=== Admin-ajax lightspeed actions with session + nonce ===")
for action in ["tcb_lightspeed_clear", "tcb_lightspeed_deoptimize",
               "tcb_lightspeed_clear_post", "tve_lightspeed_clear",
               "tcb_lightspeed_remove", "tcb_ls_deoptimize"]:
    r = session.post(ajax_url, data={
        "action": action,
        "post_id": 42202,
        "_ajax_nonce": nonce,
        "nonce": nonce,
    }, timeout=10)
    print(f"  {action}: {r.status_code} '{r.text[:80]}'")

# Check who the Thrive admin is
print("\n=== List all admin users ===")
import base64
token = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}",
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
r_users = requests.get(f"{SITE}/wp-json/wp/v2/users?roles=administrator&per_page=20",
                       headers=h, verify=False, timeout=15)
if r_users.status_code == 200:
    for u in r_users.json():
        print(f"  ID={u.get('id')} login={u.get('slug')} name={u.get('name')}")

# Try accessing Thrive admin pages
print("\n=== Thrive admin pages ===")
for page in ["thrive_dashboard", "tve_dash_section", "tcb_lightspeed",
             "thrive-lightspeed", "tve_lightspeed"]:
    r_p = session.get(f"{SITE}/wp-admin/admin.php?page={page}", timeout=10)
    print(f"  page={page}: {r_p.status_code} ({len(r_p.text)} chars)")

# Try Thrive TCB admin-ajax for settings
print("\n=== Try TCB settings/options ajax ===")
for action in ["tcb_get_post_settings", "tve_save_post_lightspeed",
               "tcb_admin_ajax", "tcb_save_post_lightspeed"]:
    r_a = session.post(ajax_url, data={
        "action": action, "post_id": 42202, "nonce": nonce, "_ajax_nonce": nonce,
    }, timeout=10)
    print(f"  {action}: {r_a.status_code} '{r_a.text[:80]}'")

# Check the TCB optimize endpoint permission specifically
print("\n=== Try lightspeed/optimize with session (no extra nonce header) ===")
r_opt_plain = session.post(f"{TCB}/lightspeed/optimize",
                           json={"to_optimize": [42202]},
                           headers={"Content-Type": "application/json"},
                           timeout=20)
print(f"  Without X-WP-Nonce: {r_opt_plain.status_code} {r_opt_plain.text[:200]}")

r_opt_nonce = session.post(f"{TCB}/lightspeed/optimize",
                           json={"to_optimize": [42202]},
                           headers={"Content-Type": "application/json",
                                    "X-WP-Nonce": nonce},
                           timeout=20)
print(f"  With X-WP-Nonce: {r_opt_nonce.status_code} {r_opt_nonce.text[:200]}")
