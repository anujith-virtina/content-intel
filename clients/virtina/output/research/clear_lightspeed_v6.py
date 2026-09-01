"""
Use correct {key, value} format for lightspeed/options to disable Lightspeed.
Then check SVGs are visible. Then re-enable.
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

# Get nonce from tve_lightspeed page
r_ls = session.get(f"{SITE}/wp-admin/admin.php?page=tve_lightspeed", timeout=20)
m = re.search(r'lightspeed_localize\s*=\s*\{.*?"nonce"\s*:\s*"([a-f0-9]+)"', r_ls.text, re.DOTALL)
nonce = m.group(1) if m else ""
print(f"Nonce: {nonce}")

headers = {"Content-Type": "application/json", "X-WP-Nonce": nonce}

# Step 1: Disable Lightspeed globally with correct {key, value} format
print("\n=== Disable Lightspeed (key/value format) ===")
for payload in [
    {"key": "is_enabled", "value": False},
    {"key": "is_enabled", "value": "false"},
    {"key": "is_enabled", "value": 0},
]:
    r = session.post(f"{TCB_BASE}/options", json=payload, headers=headers, timeout=20)
    print(f"  {payload} -> {r.status_code}: {r.text[:200]}")
    if r.status_code == 200:
        print("  SUCCESS! Lightspeed disabled.")
        break

    r2 = session.patch(f"{TCB_BASE}/options", json=payload, headers=headers, timeout=20)
    print(f"  PATCH {payload} -> {r2.status_code}: {r2.text[:200]}")
    if r2.status_code == 200:
        print("  SUCCESS via PATCH! Lightspeed disabled.")
        break

# Step 2: Check current state of options
print("\n=== Current options ===")
r_ls2 = session.get(f"{SITE}/wp-admin/admin.php?page=tve_lightspeed", timeout=20)
m2 = re.search(r'lightspeed_localize\s*=\s*(\{[^\n]+\})', r_ls2.text)
if m2:
    try:
        data = json.loads(m2.group(1).replace('lightspeed_localize = ', ''))
        print(f"is_enabled: {data.get('options', {}).get('is_enabled')}")
    except:
        print(m2.group(0)[:200])

# Step 3: Check live page for SVGs regardless
print("\nWaiting 12s for cache...")
time.sleep(12)
r_live = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                      headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
svgs = r_live.text.count("fill:#43627f")
cache = r_live.headers.get("X-nananana", "?")
print(f"Live: SVGs={svgs}, cache={cache}")

toc_idx = r_live.text.find("Table of Contents")
first_li = r_live.text.find("<li", toc_idx)
print(f"First TOC li: {r_live.text[first_li:first_li+250]}")

# Step 4: Also try Pressable cache purge for this specific URL
print("\n=== Pressable cache purge ===")
r_press = session.get(f"{SITE}/wp-admin/admin.php?page=pressable_cache_management", timeout=15)
press_nonce = ""
nm = re.search(r'"nonce"\s*:\s*"([a-f0-9]+)"', r_press.text)
if nm:
    press_nonce = nm.group(1)
    print(f"Pressable nonce: {press_nonce}")

# Try the edge cache purge action with various formats
for action in ["pressable_edge_cache_purge", "pressable_purge_url", "pressable_cache_purge"]:
    for data in [
        {"action": action, "nonce": press_nonce, "url": f"{SITE}/woocommerce-b2b-customer-portal/"},
        {"action": action, "_ajax_nonce": press_nonce, "url": f"{SITE}/woocommerce-b2b-customer-portal/"},
        {"action": action, "nonce": press_nonce},
    ]:
        rp = session.post(f"{SITE}/wp-admin/admin-ajax.php", data=data, timeout=10)
        if rp.status_code == 200 and rp.text != "0" and rp.text != "-1":
            print(f"  {action}: {rp.status_code} '{rp.text[:100]}'")
            break
        elif rp.text not in ["0", "-1"]:
            print(f"  {action}: {rp.status_code} '{rp.text[:60]}'")
