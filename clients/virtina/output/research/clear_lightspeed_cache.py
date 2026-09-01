"""
Log in via wp-login.php with real password, get session cookie,
call Thrive Lightspeed deoptimize for post 42202.
"""
import os, sys, requests, base64, urllib3, re, time, json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://virtina.com"
USERNAME = "anujith"
PASSWORD = os.environ.get("WP_REAL_PASSWORD", "")
TCB = f"{SITE}/wp-json/tcb/v1"

session = requests.Session()
session.verify = False
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

# Step 1: GET login page (sets testcookie)
print("Step 1: GET wp-login.php...")
r_get = session.get(f"{SITE}/wp-login.php", timeout=15)
print(f"  Status: {r_get.status_code}")

# Step 2: POST login
print("Step 2: POST wp-login.php...")
login_data = {
    "log": USERNAME,
    "pwd": PASSWORD,
    "wp-submit": "Log In",
    "redirect_to": f"{SITE}/wp-admin/",
    "testcookie": "1",
    "rememberme": "forever",
}
r_login = session.post(f"{SITE}/wp-login.php", data=login_data,
                       allow_redirects=True, timeout=20)
print(f"  Status: {r_login.status_code}, URL: {r_login.url}")

cookies = session.cookies.get_dict()
logged_in = any("logged_in" in k.lower() for k in cookies.keys())
print(f"  Logged in: {logged_in}")
print(f"  Cookies: {[k for k in cookies.keys()]}")

if not logged_in:
    print("Login FAILED — wrong password or login blocked.")
    sys.exit(1)

print("\nStep 3: Get REST nonce from admin...")
r_admin = session.get(f"{SITE}/wp-admin/", timeout=15)
nonce_match = re.search(r'"nonce":"([a-f0-9]+)"', r_admin.text)
wp_api_nonce = None
if nonce_match:
    wp_api_nonce = nonce_match.group(1)
    print(f"  Nonce found: {wp_api_nonce}")
else:
    # Try admin-ajax nonce endpoint
    r_nonce = session.get(f"{SITE}/wp-admin/admin-ajax.php?action=rest-nonce", timeout=10)
    if r_nonce.status_code == 200 and len(r_nonce.text) < 20:
        wp_api_nonce = r_nonce.text.strip()
        print(f"  Nonce via ajax: {wp_api_nonce}")
    else:
        print(f"  No nonce found, proceeding with session cookie only")

headers = {"Content-Type": "application/json"}
if wp_api_nonce:
    headers["X-WP-Nonce"] = wp_api_nonce

# Step 4: Verify analyze shows post 42202 as optimized
print("\nStep 4: Check current lightspeed status...")
r_analyze = session.get(f"{TCB}/lightspeed/analyze", headers=headers, timeout=15)
print(f"  Analyze status: {r_analyze.status_code}")
if r_analyze.status_code == 200:
    posts = r_analyze.json().get("post", {}).get("items", [])
    for p in posts:
        if p.get("id") == 42202:
            print(f"  Post 42202: optimized={p.get('optimized')}")

# Step 5: Call lightspeed optimize to trigger re-optimization
# This should re-read the DB content (with SVGs) and rebuild the cache
print("\nStep 5: Trigger re-optimization for post 42202...")
r_opt = session.post(f"{TCB}/lightspeed/optimize",
                     json={"to_optimize": [42202]},
                     headers=headers, timeout=30)
print(f"  Optimize status: {r_opt.status_code}: {r_opt.text[:300]}")

# Step 6: Wait and check live page
print("\nStep 6: Waiting 15s for cache refresh...")
time.sleep(15)

r_live = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                      headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
svg_count = r_live.text.count("fill:#43627f")
cache = r_live.headers.get("X-nananana", "?")
print(f"  Live: SVGs={svg_count}, cache={cache}")

toc_idx = r_live.text.find("Table of Contents")
first_li = r_live.text.find("<li", toc_idx)
print(f"\nFirst live TOC <li>:\n{r_live.text[first_li:first_li+300]}")

if svg_count > 0:
    print(f"\nSUCCESS: {svg_count} SVG arrows now visible in live page!")
else:
    print("\nSVGs still not showing — will try deoptimize approach next.")
