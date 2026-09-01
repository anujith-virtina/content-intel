"""
Logged in — now get the correct WP REST nonce and call Thrive deoptimize.
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

# Login
session.get(f"{SITE}/wp-login.php", timeout=15)
r_login = session.post(f"{SITE}/wp-login.php", data={
    "log": USERNAME, "pwd": PASSWORD, "wp-submit": "Log In",
    "redirect_to": f"{SITE}/wp-admin/", "testcookie": "1",
}, allow_redirects=True, timeout=20)
logged_in = any("logged_in" in k.lower() for k in session.cookies.keys())
print(f"Logged in: {logged_in}")
if not logged_in:
    sys.exit("Login failed")

# Get correct REST nonce — wpApiSettings.nonce in admin page
r_admin = session.get(f"{SITE}/wp-admin/", timeout=15)

# Look for wpApiSettings nonce
nonce = None
for pattern in [
    r'"nonce"\s*:\s*"([a-f0-9]+)"',
    r'wpApiSettings[^}]*"nonce"\s*:\s*"([a-f0-9]+)"',
    r'wp\.apiFetch\.createNonceMiddleware\(\s*"([a-f0-9]+)"',
    r'X-WP-Nonce["\s:,]+([a-f0-9]{10})',
    r'"_wpnonce"\s*:\s*"([a-f0-9]+)"',
    r'rest_nonce["\s:,]+([a-f0-9]+)',
]:
    m = re.search(pattern, r_admin.text)
    if m:
        nonce = m.group(1)
        print(f"Nonce ({pattern[:30]}): {nonce}")
        break

# Also try admin-ajax rest-nonce with the session
r_nonce2 = session.get(f"{SITE}/wp-admin/admin-ajax.php?action=rest-nonce", timeout=10)
print(f"ajax rest-nonce: {r_nonce2.status_code} '{r_nonce2.text[:30]}'")
if r_nonce2.status_code == 200 and r_nonce2.text.strip():
    nonce = r_nonce2.text.strip()
    print(f"Using ajax nonce: {nonce}")

# Try heartbeat API to get nonce
r_hb = session.post(f"{SITE}/wp-admin/admin-ajax.php",
                    data={"action": "heartbeat", "has_focus": "true"},
                    timeout=15)
print(f"heartbeat: {r_hb.status_code} {r_hb.text[:100]}")

# Try getting REST nonce from user endpoint
r_wp = session.get(f"{SITE}/wp-json/", timeout=10)
print(f"wp-json root: {r_wp.status_code}")

print(f"\nUsing nonce: {nonce}")
headers = {"Content-Type": "application/json", "X-WP-Nonce": nonce or ""}

# Test: GET analyze with session + nonce
r_a = session.get(f"{TCB}/lightspeed/analyze", headers=headers, timeout=15)
print(f"Analyze: {r_a.status_code} {r_a.text[:200]}")

# Test: POST optimize with session + nonce
r_opt = session.post(f"{TCB}/lightspeed/optimize",
                     json={"to_optimize": [42202]},
                     headers=headers, timeout=30)
print(f"Optimize: {r_opt.status_code} {r_opt.text[:300]}")

# Try Thrive dashboard page to find TCB nonce
print("\nLooking for TCB-specific nonce in Thrive dashboard...")
r_tcb = session.get(f"{SITE}/wp-admin/admin.php?page=thrive_dashboard", timeout=15)
print(f"Thrive dashboard: {r_tcb.status_code}")

tcb_nonce = None
for pattern in [
    r'tcb[_\-]nonce["\s:=,\']+([a-f0-9]+)',
    r'lightspeed[_\-]nonce["\s:=,\']+([a-f0-9]+)',
    r'"nonce"\s*:\s*"([a-f0-9]+)"',
    r'tve_dash_front[^}]*"nonce"\s*:\s*"([a-f0-9]+)"',
]:
    m2 = re.search(pattern, r_tcb.text, re.I)
    if m2:
        tcb_nonce = m2.group(1)
        print(f"TCB nonce ({pattern[:40]}): {tcb_nonce}")
        break

if tcb_nonce and tcb_nonce != nonce:
    headers2 = {"Content-Type": "application/json", "X-WP-Nonce": tcb_nonce}
    r_opt2 = session.post(f"{TCB}/lightspeed/optimize",
                          json={"to_optimize": [42202]},
                          headers=headers2, timeout=30)
    print(f"Optimize with TCB nonce: {r_opt2.status_code} {r_opt2.text[:300]}")
