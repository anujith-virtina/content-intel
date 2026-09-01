"""
1. Verify Lightspeed disabled state
2. Clear WP Rocket cache
3. Purge Pressable edge cache
4. Check live page
"""
import os, sys, requests, urllib3, re, time, json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://virtina.com"
USERNAME = "anujith"
PASSWORD = os.environ.get("WP_REAL_PASSWORD", "")

session = requests.Session()
session.verify = False
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

# Login
session.get(f"{SITE}/wp-login.php", timeout=15)
session.post(f"{SITE}/wp-login.php", data={
    "log": USERNAME, "pwd": PASSWORD, "wp-submit": "Log In",
    "redirect_to": f"{SITE}/wp-admin/", "testcookie": "1",
}, allow_redirects=True, timeout=20)
logged_in = any("logged_in" in k for k in session.cookies.keys())
print(f"Logged in: {logged_in}")

# Get nonces
r_ls_page = session.get(f"{SITE}/wp-admin/admin.php?page=tve_lightspeed", timeout=20)
ls_nonce_m = re.search(r'lightspeed_localize\s*=\s*\{.*?"nonce"\s*:\s*"([a-f0-9]+)"', r_ls_page.text, re.DOTALL)
ls_nonce = ls_nonce_m.group(1) if ls_nonce_m else ""
ls_enabled_m = re.search(r'"is_enabled"\s*:\s*(true|false|\d+)', r_ls_page.text)
print(f"Lightspeed nonce: {ls_nonce}")
print(f"Lightspeed is_enabled: {ls_enabled_m.group(1) if ls_enabled_m else 'UNKNOWN'}")

# Check analyze
r_analyze = session.get(f"{SITE}/wp-json/tcb/v1/lightspeed/analyze",
                        headers={"X-WP-Nonce": ls_nonce}, timeout=15)
print(f"Analyze status: {r_analyze.status_code}")

# WP Rocket cache clear
print("\n=== WP Rocket cache clear ===")
# WP Rocket REST API nonce
r_admin = session.get(f"{SITE}/wp-admin/", timeout=15)
rest_nonce_m = session.get(f"{SITE}/wp-admin/admin-ajax.php?action=rest-nonce", timeout=10)
rest_nonce = rest_nonce_m.text.strip()
print(f"REST nonce: {rest_nonce}")

# Try WP Rocket REST API
rocket_endpoints = [
    f"{SITE}/wp-json/wp-rocket/v1/clear-cache",
    f"{SITE}/wp-json/wp-rocket/v1/preload",
]
rocket_headers = {"Content-Type": "application/json", "X-WP-Nonce": rest_nonce}
for ep in rocket_endpoints:
    r = session.post(ep, json={}, headers=rocket_headers, timeout=15)
    print(f"  {ep.split('/')[-1]}: {r.status_code} {r.text[:100]}")

    r_get = session.get(ep, headers=rocket_headers, timeout=15)
    print(f"  GET {ep.split('/')[-1]}: {r_get.status_code} {r_get.text[:100]}")

# Try admin-ajax rocket actions
ajax_url = f"{SITE}/wp-admin/admin-ajax.php"
for action in ["rocket_clear_cache", "rocket_purge_cache",
               "rocket_clean_post", "rocket_clear_all"]:
    r = session.post(ajax_url, data={
        "action": action, "nonce": rest_nonce, "_ajax_nonce": rest_nonce,
        "post_id": 42202, "url": f"{SITE}/woocommerce-b2b-customer-portal/"
    }, timeout=10)
    print(f"  {action}: {r.status_code} '{r.text[:80]}'")

# Find WP Rocket nonce from admin page
r_rocket_admin = session.get(f"{SITE}/wp-admin/options-general.php?page=wprocket", timeout=15)
print(f"\nWP Rocket admin page: {r_rocket_admin.status_code}")
if r_rocket_admin.status_code == 200:
    rocket_nonce_m = re.search(r'rocket_nonce["\s:=,\']+([a-f0-9]+)', r_rocket_admin.text, re.I)
    if rocket_nonce_m:
        rocket_nonce = rocket_nonce_m.group(1)
        print(f"Rocket nonce: {rocket_nonce}")
        # Try again with rocket-specific nonce
        r_purge = session.post(ajax_url, data={
            "action": "rocket_clear_cache",
            "nonce": rocket_nonce,
            "_ajax_nonce": rocket_nonce,
        }, timeout=10)
        print(f"rocket_clear_cache with rocket_nonce: {r_purge.status_code} '{r_purge.text[:80]}'")

# Purge Pressable too
press_page = session.get(f"{SITE}/wp-admin/admin.php?page=pressable_cache_management", timeout=10)
press_nonce_m = re.search(r'"nonce"\s*:\s*"([a-f0-9]+)"', press_page.text)
if press_nonce_m:
    rp = session.post(ajax_url, data={
        "action": "pressable_edge_cache_purge",
        "nonce": press_nonce_m.group(1)
    }, timeout=10)
    print(f"\nPressable purge: {rp.text[:60]}")

print("\nWaiting 15s...")
time.sleep(15)

r_live = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                      headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
svgs = r_live.text.count("fill:#43627f")
cache = r_live.headers.get("X-nananana", "?")
print(f"Live: SVGs={svgs}, cache={cache}")
toc = r_live.text.find("Table of Contents")
li = r_live.text.find("<li", toc)
print(f"First TOC li: {r_live.text[li:li+350]}")
