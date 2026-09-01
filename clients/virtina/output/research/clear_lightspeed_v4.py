"""
Access tve_lightspeed admin page — extract correct AJAX actions, nonces, and form data.
Then call the deoptimize action for post 42202.
"""
import os, sys, requests, urllib3, re, time, json
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
print(f"Logged in: {any('logged_in' in k for k in session.cookies.keys())}")

# Get REST nonce
nonce = session.get(f"{SITE}/wp-admin/admin-ajax.php?action=rest-nonce", timeout=10).text.strip()
print(f"REST nonce: {nonce}")

# Load the tve_lightspeed page
print("\nLoading tve_lightspeed page...")
r_ls = session.get(f"{SITE}/wp-admin/admin.php?page=tve_lightspeed", timeout=30)
html = r_ls.text
print(f"Page size: {len(html)} chars")

# Extract all nonces from the page
print("\n=== Nonces in tve_lightspeed page ===")
nonces = {}
for pattern, name in [
    (r'"nonce"\s*:\s*"([a-f0-9]+)"', "nonce"),
    (r'"_nonce"\s*:\s*"([a-f0-9]+)"', "_nonce"),
    (r'nonce["\s:=,\']+([a-f0-9]{10,})', "any_nonce"),
    (r'wp_nonce["\s:=,\']+([a-f0-9]+)', "wp_nonce"),
    (r'"_wpnonce"\s*:\s*"([a-f0-9]+)"', "_wpnonce"),
    (r'createNonceMiddleware\(["\']([a-f0-9]+)["\']', "apiFetch_nonce"),
]:
    matches = re.findall(pattern, html, re.I)
    if matches:
        nonces[name] = matches[0]
        print(f"  {name}: {matches[0]} (total {len(matches)})")

# Extract all AJAX action names from the page
print("\n=== AJAX actions in tve_lightspeed page ===")
actions = re.findall(r'"action"\s*:\s*"([a-z_]+)"', html)
actions_unique = list(dict.fromkeys(actions))
for a in actions_unique[:30]:
    print(f"  {a}")

# Extract lightspeed-specific JS data
print("\n=== Lightspeed JS data ===")
ls_data_match = re.search(r'tve_lightspeed_data\s*=\s*(\{[^;]+\})', html, re.DOTALL)
if ls_data_match:
    print(ls_data_match.group(0)[:500])

# Look for deoptimize/clear buttons or forms
print("\n=== Deoptimize/clear references ===")
for keyword in ["deoptimize", "de-optimize", "clear", "remove", "lightspeed"]:
    matches = [(m.start(), html[max(0,m.start()-50):m.start()+100])
               for m in re.finditer(keyword, html, re.I)]
    if matches:
        print(f"\n'{keyword}' found {len(matches)} times. First 3:")
        for start, ctx in matches[:3]:
            print(f"  ...{ctx.strip()[:120]}...")

# Look for the specific post 42202 in the page
print(f"\n=== Post 42202 in lightspeed page ===")
idx = html.find("42202")
if idx >= 0:
    print(html[max(0,idx-200):idx+200])

# Save the full page for inspection
with open("tve_lightspeed_page.html", "w", encoding="utf-8") as f:
    f.write(html)
print("\nFull page saved to tve_lightspeed_page.html")
