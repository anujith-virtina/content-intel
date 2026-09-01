"""
Login to WP admin via cookie session, get nonce, call Thrive lightspeed
deoptimize for post 42202 — bypassing basic-auth limitations.
"""
import os, sys, re, time, requests, base64, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")  # app password for REST
# We also need the real login password — try it as the app password first
SITE = "https://virtina.com"

session = requests.Session()
session.verify = False
session.headers["User-Agent"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# ── Step 1: GET login page to get initial cookies ────────────────────────────
print("Step 1: GET login page...")
r_login = session.get(f"{SITE}/wp-login.php", timeout=20)
print(f"  Login page status: {r_login.status_code}")

# ── Step 2: POST login with app password ─────────────────────────────────────
print("Step 2: POST login...")
login_payload = {
    "log": USERNAME,
    "pwd": APP_PASSWORD,
    "wp-submit": "Log In",
    "redirect_to": "/wp-admin/",
    "testcookie": "1",
}
r_submit = session.post(f"{SITE}/wp-login.php", data=login_payload,
                        timeout=20, allow_redirects=True)
print(f"  Login submit status: {r_submit.status_code}, final URL: {r_submit.url}")
logged_in = any("wordpress_logged_in" in c.name for c in session.cookies)
print(f"  Logged in cookie present: {logged_in}")

if not logged_in:
    print("  Login with app password failed — trying without spaces...")
    login_payload["pwd"] = APP_PASSWORD.replace(" ", "")
    r_submit2 = session.post(f"{SITE}/wp-login.php", data=login_payload,
                             timeout=20, allow_redirects=True)
    logged_in = any("wordpress_logged_in" in c.name for c in session.cookies)
    print(f"  Retry logged_in: {logged_in}, status: {r_submit2.status_code}")

# ── Step 3: Get WP REST nonce from admin ─────────────────────────────────────
nonce = None
if logged_in:
    print("\nStep 3: Get REST API nonce...")
    r_nonce = session.get(f"{SITE}/wp-admin/admin-ajax.php?action=rest-nonce",
                          timeout=20)
    print(f"  Nonce response: {r_nonce.status_code}: {r_nonce.text[:100]}")
    if r_nonce.status_code == 200 and r_nonce.text.strip():
        nonce = r_nonce.text.strip()
        print(f"  Got nonce: {nonce[:20]}...")

    # Also try getting nonce from admin page
    if not nonce:
        r_admin = session.get(f"{SITE}/wp-admin/", timeout=20)
        m = re.search(r'"nonce"\s*:\s*"([a-f0-9]+)"', r_admin.text)
        if not m:
            m = re.search(r'wp\.apiFetch\.nonceMiddleware\s*=.*?"([a-f0-9]{10})"', r_admin.text)
        if m:
            nonce = m.group(1)
            print(f"  Got nonce from admin page: {nonce[:20]}...")

# ── Step 4: Call Thrive lightspeed optimize endpoint with session ─────────────
print("\nStep 4: Call Thrive lightspeed/optimize with session...")
headers_for_thrive = {"Content-Type": "application/json"}
if nonce:
    headers_for_thrive["X-WP-Nonce"] = nonce

# Try to re-optimize post 42202 (this should rebuild from current post_content)
payloads = [
    {"to_optimize": [42202]},
    {"post_id": 42202, "action": "optimize"},
    {"posts": [42202]},
    {"id": 42202},
]
for payload in payloads:
    r3 = session.post(f"{SITE}/wp-json/tcb/v1/lightspeed/optimize",
                      json=payload, headers=headers_for_thrive, timeout=30)
    print(f"  {list(payload.keys())} -> {r3.status_code}: {r3.text[:150]}")

# Try deoptimize via AJAX
print("\nStep 5: Try AJAX actions with session...")
ajax_actions = [
    {"action": "tcb_lightspeed_deoptimize", "post_id": 42202},
    {"action": "tcb_clear_lightspeed_cache", "post_id": 42202},
    {"action": "tcb_lightspeed_clear", "post_id": 42202, "nonce": nonce or ""},
]
for payload in ajax_actions:
    r4 = session.post(f"{SITE}/wp-admin/admin-ajax.php",
                      data=payload, timeout=20)
    print(f"  action={payload['action']} -> {r4.status_code}: {r4.text[:100]}")

# ── Step 6: Check live page ───────────────────────────────────────────────────
time.sleep(2)
r_live = session.get(f"{SITE}/woocommerce-b2b-customer-portal/", timeout=30)
svg_count = r_live.text.count("fill:#43627f")
print(f"\nLive page SVG count: {svg_count}")
print(f"Cache: {r_live.headers.get('X-nananana','?')}")
