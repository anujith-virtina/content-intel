"""Re-enable Lightspeed and trigger optimization for post 42202."""
import os, sys, requests, urllib3, re, time, base64
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://virtina.com"
USERNAME = "anujith"
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
REAL_PASSWORD = os.environ.get("WP_REAL_PASSWORD", "")

session = requests.Session()
session.verify = False
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
session.get(f"{SITE}/wp-login.php", timeout=15)
session.post(f"{SITE}/wp-login.php", data={
    "log": USERNAME, "pwd": REAL_PASSWORD, "wp-submit": "Log In",
    "redirect_to": f"{SITE}/wp-admin/", "testcookie": "1",
}, allow_redirects=True, timeout=20)
logged_in = any("logged_in" in k for k in session.cookies.keys())
print(f"Logged in: {logged_in}")

rest_nonce = session.get(f"{SITE}/wp-admin/admin-ajax.php?action=rest-nonce", timeout=10).text.strip()
print(f"Nonce: {rest_nonce}")
sh = {"X-WP-Nonce": rest_nonce, "Content-Type": "application/json"}

# Step 1: Re-enable Lightspeed
print("\n1. Re-enabling Lightspeed...")
r_ls = session.post(f"{SITE}/wp-json/tcb/v1/lightspeed/options",
                    json={"key": "_tve_enable_lightspeed", "value": 1},
                    headers=sh, timeout=15)
print(f"   Enable: {r_ls.status_code} '{r_ls.text[:60]}'")

# Step 2: Verify Lightspeed enabled
r_check = session.get(f"{SITE}/wp-admin/admin.php?page=tve_lightspeed", timeout=20)
ls_m = re.search(r'"is_enabled"\s*:\s*(true|false|\d+)', r_check.text)
print(f"   Lightspeed is_enabled: {ls_m.group(1) if ls_m else 'UNKNOWN'}")

# Re-get nonce from lightspeed page for fresh one
ls_nonce_m = re.search(r'"nonce"\s*:\s*"([a-f0-9]+)"', r_check.text)
if ls_nonce_m:
    rest_nonce = ls_nonce_m.group(1)
    sh = {"X-WP-Nonce": rest_nonce, "Content-Type": "application/json"}
    print(f"   Lightspeed nonce: {rest_nonce}")

# Step 3: Load the optimization URL directly - Thrive's iframe optimization trigger
optimize_url = f"{SITE}/?p=42202&force-flat=1&force-all-js=1&tcb-lightspeed-optimize=1"
print(f"\n2. Loading optimization URL for post 42202...")
print(f"   URL: {optimize_url}")
r_opt = session.get(optimize_url, allow_redirects=True, timeout=60)
print(f"   Response: {r_opt.status_code}, length: {len(r_opt.text)}")
# Check if optimization was triggered
opt_markers = ['lightspeed-optimize', 'tcb-lightspeed', 'optimized']
for marker in opt_markers:
    if marker in r_opt.text:
        idx = r_opt.text.find(marker)
        print(f"   Found '{marker}': {r_opt.text[max(0,idx-30):idx+80]}")
        break
# Check for SVG arrows in this rendered page
svg_count = r_opt.text.count('fill:#43627f')
tcb_svg = r_opt.text.count('tcb-icon')
print(f"   fill:#43627f: {svg_count}, tcb-icon: {tcb_svg}")

# Step 4: Verify optimization status
print("\n3. Checking optimization status...")
r_analyze = session.get(f"{SITE}/wp-json/tcb/v1/lightspeed/analyze", headers=sh, timeout=20)
import json
try:
    data = r_analyze.json()
    content = json.dumps(data)
    idx = content.find("42202")
    if idx >= 0:
        print(f"   42202 status: {content[max(0,idx-20):idx+150]}")
except:
    print(f"   analyze: {r_analyze.text[:200]}")

# Step 5: Purge all caches
print("\n4. Purging edge cache...")
press_page = session.get(f"{SITE}/wp-admin/admin.php?page=pressable_cache_management", timeout=15)
press_nonce = re.search(r'"nonce"\s*:\s*"([a-f0-9]+)"', press_page.text)
if press_nonce:
    rp = session.post(f"{SITE}/wp-admin/admin-ajax.php", data={
        "action": "pressable_edge_cache_purge", "nonce": press_nonce.group(1)
    }, timeout=15)
    print(f"   Edge cache: {rp.text[:60]}")

# Step 6: Also try loading page as admin to warm Batcache with fresh content
print("\n5. Hitting live page as admin (warms Batcache)...")
r_warm = session.get(f"{SITE}/woocommerce-b2b-customer-portal/", timeout=30)
cache_w = r_warm.headers.get("X-nananana", "none")
toc_w = r_warm.text.find("Table of Contents")
li_w = r_warm.text.find("<li", toc_w)
li_html = r_warm.text[li_w:li_w+400]
svg_w = r_warm.text.count("fill:#43627f") + r_warm.text.count("tcb-icon")
print(f"   Admin render: cache={cache_w}, svg/tcb-icon={svg_w}")
print(f"   First li: {li_html[:250]}")

print("\nWaiting 10s...")
time.sleep(10)

# Step 7: Final anonymous check
print("\n=== FINAL CHECK ===")
for i in range(3):
    r = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                     headers={"User-Agent": f"Mozilla/5.0 (check-{i})"}, verify=False, timeout=30)
    cache = r.headers.get("X-nananana", r.headers.get("X-Cache", "none"))
    toc_f = r.text.find("Table of Contents")
    li_f = r.text.find("<li", toc_f)
    li_html = r.text[li_f:li_f+400]
    svg = r.text.count("fill:#43627f")
    tcb = r.text.count("tcb-icon")
    print(f"[{i+1}] cache={cache}, fill:#43627f={svg}, tcb-icon={tcb}")
    if svg > 0 or tcb > 0:
        print(f"  ARROWS PRESENT! First li: {li_html[:200]}")
    time.sleep(1)
