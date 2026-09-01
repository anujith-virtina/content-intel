"""
Disable Thrive Lightspeed using the correct key: _tve_enable_lightspeed.
SVGs will render from DB. Then check live page.
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

# Get nonce from lightspeed page
r_ls = session.get(f"{SITE}/wp-admin/admin.php?page=tve_lightspeed", timeout=20)
m = re.search(r'lightspeed_localize\s*=\s*\{.*?"nonce"\s*:\s*"([a-f0-9]+)"', r_ls.text, re.DOTALL)
nonce = m.group(1) if m else ""
print(f"Nonce: {nonce}")

headers = {"Content-Type": "application/json", "X-WP-Nonce": nonce}

# Check current state
r_a = session.get(f"{TCB_BASE}/analyze", headers=headers, timeout=15)
for p in r_a.json().get("post", {}).get("items", []):
    if p.get("id") == 42202:
        print(f"Post 42202 before: optimized={p.get('optimized')}")

# DISABLE Lightspeed
print("\nDisabling Lightspeed (_tve_enable_lightspeed = 0)...")
r_off = session.post(f"{TCB_BASE}/options",
                     json={"key": "_tve_enable_lightspeed", "value": 0},
                     headers=headers, timeout=20)
print(f"Disable: {r_off.status_code} {r_off.text[:300]}")

if r_off.status_code != 200:
    # Try PATCH
    r_off = session.patch(f"{TCB_BASE}/options",
                          json={"key": "_tve_enable_lightspeed", "value": 0},
                          headers=headers, timeout=20)
    print(f"PATCH disable: {r_off.status_code} {r_off.text[:300]}")

print("\nWaiting 12s for Pressable/Batcache to cycle...")
time.sleep(12)

# Check live page for SVGs
r_live = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                      headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
svgs = r_live.text.count("fill:#43627f")
cache = r_live.headers.get("X-nananana", "?")
print(f"Live: SVGs={svgs}, cache={cache}")

toc_idx = r_live.text.find("Table of Contents")
first_li = r_live.text.find("<li", toc_idx)
print(f"First TOC li:\n{r_live.text[first_li:first_li+400]}")

if svgs > 0:
    print(f"\nSUCCESS: {svgs} SVG arrows now visible!")
    print("Lightspeed is disabled — page renders from DB. Arrows are live.")
    print("\nNOTE: Lightspeed is currently disabled site-wide.")
    print("Re-enabling it will restore the pre-cached version without arrows.")
    print("Options: (A) Leave disabled for now, (B) Re-optimize post 42202 to include arrows.")
else:
    print("\nSVGs not showing yet — Pressable edge cache may need another purge.")
    # Purge Pressable edge cache
    press_nonce_m = re.search(r'"nonce"\s*:\s*"([a-f0-9]+)"',
                              session.get(f"{SITE}/wp-admin/admin.php?page=pressable_cache_management", timeout=10).text)
    if press_nonce_m:
        rp = session.post(f"{SITE}/wp-admin/admin-ajax.php",
                          data={"action": "pressable_edge_cache_purge",
                                "nonce": press_nonce_m.group(1)},
                          timeout=10)
        print(f"Pressable purge: {rp.text[:60]}")
        time.sleep(8)
        r_live2 = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                               headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
        svgs2 = r_live2.text.count("fill:#43627f")
        print(f"After purge: SVGs={svgs2}, cache={r_live2.headers.get('X-nananana','?')}")
        toc_idx2 = r_live2.text.find("Table of Contents")
        first_li2 = r_live2.text.find("<li", toc_idx2)
        print(f"First TOC li:\n{r_live2.text[first_li2:first_li2+400]}")
