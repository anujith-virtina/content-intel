"""Clear WP Rocket cache and verify SVGs appear on live page."""
import os, sys, requests, urllib3, re, time
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

# Get nonce
rest_nonce = session.get(f"{SITE}/wp-admin/admin-ajax.php?action=rest-nonce", timeout=10).text.strip()
print(f"Nonce: {rest_nonce}")

ajax_url = f"{SITE}/wp-admin/admin-ajax.php"

# Find WP Rocket-specific nonce from WP Rocket admin page
r_rocket = session.get(f"{SITE}/wp-admin/options-general.php?page=wprocket", timeout=15)
print(f"WP Rocket page: {r_rocket.status_code}")
rocket_nonce = rest_nonce
if r_rocket.status_code == 200:
    for pattern in [r'rocket_nonce["\s:=,\']+([a-f0-9]+)',
                    r'"nonce"\s*:\s*"([a-f0-9]+)"',
                    r'_wpnonce["\s:=,\']+([a-f0-9]+)']:
        m = re.search(pattern, r_rocket.text, re.I)
        if m:
            rocket_nonce = m.group(1)
            print(f"Rocket nonce: {rocket_nonce}")
            break

# Try every known WP Rocket cache clear action
print("\nClearing WP Rocket cache...")
cleared = False
for action, nonce in [
    ("rocket_clear_cache", rocket_nonce),
    ("rocket_clear_cache", rest_nonce),
    ("rocket_purge_cache", rocket_nonce),
    ("rocket_clean_domain", rocket_nonce),
    ("rocket_clean_home", rocket_nonce),
]:
    r = session.post(ajax_url, data={
        "action": action, "nonce": nonce, "_ajax_nonce": nonce,
    }, timeout=15)
    print(f"  {action}: {r.status_code} '{r.text[:100]}'")
    if r.status_code == 200 and r.text not in ["0", "-1", ""]:
        cleared = True
        break

# Also try WP Rocket REST endpoint
for ep in [f"{SITE}/wp-json/wp-rocket/v1/clear-cache",
           f"{SITE}/wp-json/wp-rocket/v1/clean"]:
    r = session.delete(ep, headers={"X-WP-Nonce": rest_nonce}, timeout=10)
    print(f"  DELETE {ep.split('/')[-1]}: {r.status_code} {r.text[:80]}")
    r2 = session.post(ep, headers={"Content-Type": "application/json",
                                   "X-WP-Nonce": rest_nonce}, timeout=10)
    print(f"  POST {ep.split('/')[-1]}: {r2.status_code} {r2.text[:80]}")

# Also purge Pressable again
press_page = session.get(f"{SITE}/wp-admin/admin.php?page=pressable_cache_management", timeout=10)
press_nonce_m = re.search(r'"nonce"\s*:\s*"([a-f0-9]+)"', press_page.text)
if press_nonce_m:
    rp = session.post(ajax_url, data={
        "action": "pressable_edge_cache_purge",
        "nonce": press_nonce_m.group(1)
    }, timeout=10)
    print(f"\nPressable purge: {rp.text[:60]}")

print("\nWaiting 15s for caches to clear...")
time.sleep(15)

r_live = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                      headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
svgs = r_live.text.count("fill:#43627f")
cache = r_live.headers.get("X-nananana", "?")
print(f"\nLive: SVGs={svgs}, cache={cache}")

toc = r_live.text.find("Table of Contents")
li = r_live.text.find("<li", toc)
print(f"First TOC li:\n{r_live.text[li:li+400]}")

if svgs > 0:
    print(f"\nSUCCESS: {svgs} SVG arrows now live!")
else:
    print("\nChecking DB content state...")
    import base64
    token = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
    h = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0"}
    db = requests.get(f"{SITE}/wp-json/wp/v2/posts/42202?context=edit",
                      headers=h, verify=False, timeout=15).json()
    raw = db["content"]["raw"]
    print(f"DB SVGs: {raw.count('fill:#43627f')}")
    print(f"DB arrows: {raw.count(chr(0x279C))}")
    print(f"DB color 43627f: {raw.count('#43627f')}")
