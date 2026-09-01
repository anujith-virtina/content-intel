"""Check user capabilities and find Thrive lightspeed cached file location."""
import os, sys, requests, base64, urllib3, json, time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}",
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
hj = {**h, "Content-Type": "application/json"}

SITE = "https://virtina.com"

# Check user capabilities via REST
print("=== User capabilities ===")
r = requests.get(f"{SITE}/wp-json/wp/v2/users/me", headers=h, verify=False, timeout=20)
me = r.json()
print(f"User: {me.get('name')} (ID: {me.get('id')})")
caps = me.get("capabilities", {})
print(f"manage_options: {caps.get('manage_options', 'NOT FOUND')}")
print(f"administrator: {caps.get('administrator', 'NOT FOUND')}")
print(f"edit_posts: {caps.get('edit_posts', 'NOT FOUND')}")
print(f"All caps: {list(caps.keys())[:20]}")

# Check WP settings endpoint (requires manage_options)
print("\n=== WP settings (requires manage_options) ===")
r2 = requests.get(f"{SITE}/wp-json/wp/v2/settings", headers=h, verify=False, timeout=20)
print(f"Status: {r2.status_code}")
if r2.status_code == 200:
    settings = r2.json()
    thrive_settings = {k: v for k, v in settings.items() if "thrive" in k.lower() or "tcb" in k.lower() or "lightspeed" in k.lower()}
    print(f"Thrive-related settings: {thrive_settings}")
    print(f"All setting keys: {list(settings.keys())}")

# Look for Thrive lightspeed cached files via direct URL patterns
print("\n=== Checking for Thrive Lightspeed cached file URLs ===")
candidate_urls = [
    f"{SITE}/wp-content/uploads/tcb-lightspeed/42202.html",
    f"{SITE}/wp-content/cache/tcb-lightspeed/42202.html",
    f"{SITE}/wp-content/uploads/tcb_lightspeed/42202.html",
    f"{SITE}/wp-content/uploads/tcb-lightspeed/post-42202.html",
    f"{SITE}/wp-content/uploads/tcb-lightspeed/woocommerce-b2b-customer-portal.html",
]
for url in candidate_urls:
    r3 = requests.head(url, headers=h, verify=False, timeout=10)
    print(f"  {url.split('/')[-1]} -> {r3.status_code}")

# Try the lightspeed analyze with to_analyze param
print("\n=== Lightspeed analyze with specific post ===")
r4 = requests.get(f"{SITE}/wp-json/tcb/v1/lightspeed/analyze",
                  params={"to_analyze[]": 42202},
                  headers=h, verify=False, timeout=20)
print(f"Status: {r4.status_code}")
data = r4.json()
print(json.dumps(data, indent=2)[:1000])
