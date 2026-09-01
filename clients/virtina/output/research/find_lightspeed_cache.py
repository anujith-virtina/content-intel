"""Find Thrive Lightspeed cache location and try to manipulate it."""
import os, sys, requests, base64, urllib3, json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}",
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
hj = {**h, "Content-Type": "application/json"}
SITE = "https://virtina.com"

# Check user role
r_me = requests.get(f"{SITE}/wp-json/wp/v2/users/me?context=edit", headers=h, verify=False, timeout=15)
me = r_me.json()
print(f"User: {me.get('name')} roles: {me.get('roles')} slug: {me.get('slug')}")

# Try Thrive Product Manager endpoints
print("\n=== Thrive Product Manager API ===")
for ep in ["", "/deactivate/1"]:
    r = requests.get(f"{SITE}/wp-json/thrive-product-manager/v1{ep}",
                     headers=h, verify=False, timeout=15)
    print(f"  GET {ep}: {r.status_code} {r.text[:150]}")

# Try to find lightspeed file cache via various slug/ID patterns
print("\n=== Probing for Lightspeed cache files ===")
slug = "woocommerce-b2b-customer-portal"
patterns = [
    f"/wp-content/uploads/tcb-lightspeed/{slug}.html",
    f"/wp-content/uploads/tcb-lightspeed/{slug}/index.html",
    f"/wp-content/uploads/tcb-lightspeed/posts/{slug}.html",
    f"/wp-content/uploads/tcb_lightspeed/{slug}.html",
    f"/wp-content/uploads/thrive-lightspeed/{slug}.html",
    f"/wp-content/cache/thrive/{slug}.html",
    f"/wp-content/cache/tcb/{slug}.html",
    f"/wp-content/uploads/tcb-lightspeed/",  # directory listing
    f"/wp-content/uploads/tcb-lightspeed/posts/",
]
for path in patterns:
    r = requests.get(f"{SITE}{path}", headers={"User-Agent": "Mozilla/5.0"},
                     verify=False, timeout=10, allow_redirects=False)
    print(f"  {r.status_code} {path.split('uploads/')[-1] if 'uploads' in path else path}")

# Try wp-cron with no_init_cookies
print("\n=== WP Cron probe ===")
r_cron = requests.get(f"{SITE}/wp-cron.php?doing_wp_cron=1",
                      headers={"User-Agent": "WordPress/6.0"}, verify=False, timeout=20)
print(f"wp-cron.php status: {r_cron.status_code} len={len(r_cron.text)}")

# Try lightspeed options with key "enabled"
print("\n=== Try disable/re-enable lightspeed globally ===")
for key in ["enabled", "active", "lightspeed_enabled", "tcb_lightspeed"]:
    r2 = requests.post(f"{SITE}/wp-json/tcb/v1/lightspeed/options",
                       json={"key": key, "value": 0},
                       headers=hj, verify=False, timeout=10)
    print(f"  key={key} disable: {r2.status_code} {r2.text[:100]}")
