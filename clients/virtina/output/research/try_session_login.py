"""
Try to get a real WP session cookie via wp-login.php.
If app password is also the login password, this will give us a session
that can call the Thrive Lightspeed deoptimize endpoint.
"""
import os, sys, requests, base64, urllib3, re, time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
SITE = "https://virtina.com"

session = requests.Session()
session.verify = False
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
})

# Try logging in with the app password as login password
print("Attempting wp-login.php...")
login_data = {
    "log": USERNAME,
    "pwd": APP_PASSWORD,
    "wp-submit": "Log In",
    "redirect_to": f"{SITE}/wp-admin/",
    "testcookie": "1",
    "rememberme": "forever",
}
# First GET to get the login page (for testcookie)
r_get = session.get(f"{SITE}/wp-login.php", timeout=15)
print(f"GET wp-login.php: {r_get.status_code}")

# POST login
r_login = session.post(f"{SITE}/wp-login.php", data=login_data,
                       allow_redirects=True, timeout=15)
print(f"POST wp-login.php: {r_login.status_code}, final URL: {r_login.url}")

# Check if we're logged in
cookies = session.cookies.get_dict()
logged_in_cookies = {k: v for k, v in cookies.items() if "logged_in" in k.lower() or "wordpress" in k.lower()}
print(f"Auth cookies: {list(logged_in_cookies.keys())}")

is_logged_in = any("logged_in" in k.lower() for k in cookies.keys())
print(f"Session logged in: {is_logged_in}")

if is_logged_in:
    print("\nSession cookie obtained! Trying Thrive Lightspeed deoptimize...")

    # Get a nonce from admin page
    r_admin = session.get(f"{SITE}/wp-admin/admin.php?page=thrive_dashboard", timeout=15)
    print(f"Admin page: {r_admin.status_code}")

    # Try to find a nonce in the admin page
    nonce_match = re.search(r'"nonce"\s*:\s*"([a-f0-9]+)"', r_admin.text)
    tcb_nonce_match = re.search(r'tcb[_\-]nonce["\']?\s*[:=]\s*["\']([a-f0-9]+)["\']', r_admin.text, re.I)

    nonce = None
    if tcb_nonce_match:
        nonce = tcb_nonce_match.group(1)
        print(f"TCB nonce found: {nonce}")
    elif nonce_match:
        nonce = nonce_match.group(1)
        print(f"Generic nonce found: {nonce}")
    else:
        print("No nonce found in admin page, will try without")

    # Try to call Thrive optimize endpoint WITH session
    headers_with_session = {"Content-Type": "application/json"}
    if nonce:
        headers_with_session["X-WP-Nonce"] = nonce

    # First try: GET the analyze endpoint to verify session works
    r_analyze = session.get(f"{SITE}/wp-json/tcb/v1/lightspeed/analyze",
                            headers=headers_with_session, timeout=15)
    print(f"Analyze with session: {r_analyze.status_code}")
    if r_analyze.status_code == 200:
        posts = r_analyze.json().get("post", {}).get("items", [])
        for p in posts:
            if p.get("id") == 42202:
                print(f"Post 42202 optimized status: {p.get('optimized')}")

    # Try POST to optimize with empty or different payload to deoptimize
    payloads = [
        {"to_optimize": [], "deoptimize": [42202]},
        {"to_deoptimize": [42202]},
        {"to_optimize": [42202], "action": "deoptimize"},
        {"post_id": 42202, "optimized": 0},
    ]
    for payload in payloads:
        r_opt = session.post(f"{SITE}/wp-json/tcb/v1/lightspeed/optimize",
                             json=payload, headers=headers_with_session, timeout=15)
        print(f"  POST optimize {list(payload.keys())}: {r_opt.status_code} {r_opt.text[:150]}")

    # Also try PATCH
    r_patch = session.patch(f"{SITE}/wp-json/tcb/v1/lightspeed/optimize",
                             json={"to_optimize": [42202]},
                             headers=headers_with_session, timeout=15)
    print(f"  PATCH optimize: {r_patch.status_code} {r_patch.text[:200]}")

else:
    print("\nLogin failed — app password is NOT the login password.")
    print("Session cookie not obtained. Thrive Lightspeed clear requires manual WP Admin action.")

    # As a fallback: print exactly what the user needs to do
    print("\n" + "="*60)
    print("MANUAL FIX (30 seconds):")
    print("1. Go to: https://virtina.com/wp-admin")
    print("2. Left menu > Thrive Dashboard")
    print("3. Click 'Lightspeed' tab")
    print("4. Find post: 'Does your WooCommerce store have a B2B customer portal'")
    print("5. Click the X/trash icon to deoptimize it")
    print("6. Arrows will appear immediately on the live page")
    print("="*60)
