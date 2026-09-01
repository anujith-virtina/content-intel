"""
Use the nonce from lightspeed_localize to call:
1. lightspeed/options to disable globally -> SVGs render from DB -> visible
2. Check live page for SVGs
3. Re-enable Lightspeed (with SVGs now in DB)
Also try Pressable cache clear.
"""
import os, sys, requests, urllib3, re, time, json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://virtina.com"
USERNAME = "anujith"
PASSWORD = os.environ.get("WP_REAL_PASSWORD", "")
TCB_BASE = f"{SITE}/wp-json/tcb/v1/lightspeed"

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
if not logged_in:
    sys.exit("Login failed")

# Get the nonce from the tve_lightspeed page (same one Thrive JS uses)
r_ls = session.get(f"{SITE}/wp-admin/admin.php?page=tve_lightspeed", timeout=20)
m = re.search(r'lightspeed_localize\s*=\s*\{.*?"nonce"\s*:\s*"([a-f0-9]+)"', r_ls.text, re.DOTALL)
nonce = m.group(1) if m else ""
print(f"Lightspeed nonce: {nonce}")

# Also extract current options
opts_m = re.search(r'lightspeed_localize\s*=\s*(\{[^\n]+\})', r_ls.text)
if opts_m:
    print(f"lightspeed_localize: {opts_m.group(0)[:300]}")

headers = {"Content-Type": "application/json", "X-WP-Nonce": nonce}

# Step 1: Check analyze with this nonce
r_a = session.get(f"{TCB_BASE}/analyze", headers=headers, timeout=15)
print(f"\nAnalyze: {r_a.status_code}")
if r_a.status_code == 200:
    for p in r_a.json().get("post", {}).get("items", []):
        if p.get("id") == 42202:
            print(f"Post 42202: optimized={p.get('optimized')}")

# Step 2: Try POST optimize with this nonce
print("\n=== Try optimize ===")
r_opt = session.post(f"{TCB_BASE}/optimize",
                     json={"to_optimize": [42202]},
                     headers=headers, timeout=20)
print(f"POST optimize: {r_opt.status_code} {r_opt.text[:200]}")

# Step 3: Try options with this nonce — disable Lightspeed globally
print("\n=== Try options — disable Lightspeed ===")
r_off = session.post(f"{TCB_BASE}/options",
                     json={"is_enabled": False},
                     headers=headers, timeout=20)
print(f"Disable: {r_off.status_code} {r_off.text[:200]}")

r_off2 = session.patch(f"{TCB_BASE}/options",
                       json={"is_enabled": False},
                       headers=headers, timeout=20)
print(f"PATCH disable: {r_off2.status_code} {r_off2.text[:200]}")

# If disable worked, check if SVGs are now live
if r_off.status_code == 200 or r_off2.status_code == 200:
    print("\nLightspeed disabled! Waiting 10s and checking live page...")
    time.sleep(10)
    r_live = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                          headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
    svgs = r_live.text.count("fill:#43627f")
    print(f"Live SVGs: {svgs}, cache: {r_live.headers.get('X-nananana','?')}")
    if svgs > 0:
        print("SUCCESS! SVGs visible. Re-enabling Lightspeed...")
        re_on = session.post(f"{TCB_BASE}/options",
                             json={"is_enabled": True},
                             headers=headers, timeout=20)
        print(f"Re-enable: {re_on.status_code}")

# Step 4: Try Pressable cache purge
print("\n=== Try Pressable cache management ===")
r_press = session.get(f"{SITE}/wp-admin/admin.php?page=pressable_cache_management", timeout=15)
print(f"Pressable CM page: {r_press.status_code} ({len(r_press.text)} chars)")
if r_press.status_code == 200:
    # Find form/nonce for cache purge
    nonce_p = re.search(r'nonce["\s:=,\']+([a-f0-9]+)', r_press.text)
    action_p = re.search(r'action["\s:=,\']+([a-z_]+purge[a-z_]*)', r_press.text, re.I)
    print(f"Purge nonce: {nonce_p.group(1) if nonce_p else 'not found'}")
    print(f"Purge action: {action_p.group(1) if action_p else 'not found'}")
    # Try common Pressable purge endpoint
    for purge_action in ["pressable_purge_cache", "pressable_clear_cache", "flush_cache"]:
        rp = session.post(f"{SITE}/wp-admin/admin-ajax.php",
                         data={"action": purge_action, "nonce": nonce,
                               "url": f"{SITE}/woocommerce-b2b-customer-portal/"},
                         timeout=10)
        print(f"  {purge_action}: {rp.status_code} '{rp.text[:60]}'")
