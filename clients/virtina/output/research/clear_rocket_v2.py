"""Find exact WP Rocket clear cache URL/nonce from admin page and execute it."""
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

# Load WP Rocket admin page — find the exact clear cache button URL
r_rocket = session.get(f"{SITE}/wp-admin/options-general.php?page=wprocket", timeout=20)
html = r_rocket.text
print(f"WP Rocket page: {r_rocket.status_code} ({len(html)} chars)")

# Find clear cache links/buttons
print("\n=== Clear cache URLs in WP Rocket page ===")
clear_urls = re.findall(r'href=["\']([^"\']*(?:purge|clear|flush|cache)[^"\']*)["\']', html, re.I)
for u in clear_urls[:15]:
    print(f"  {u[:120]}")

# Find nonces associated with clear actions
print("\n=== Nonces ===")
for pattern in [
    r'rocket[_-]clear[_-]cache[_-]nonce["\s:=,\']+([a-f0-9]+)',
    r'wpr[_-]nonce["\s:=,\']+([a-f0-9]+)',
    r'"rocket_nonce"\s*:\s*"([a-f0-9]+)"',
    r'data-nonce=["\']([a-f0-9]+)["\']',
    r'name=["\']_wpnonce["\'][^>]*value=["\']([a-f0-9]+)["\']',
    r'value=["\']([a-f0-9]+)["\'][^>]*name=["\']_wpnonce["\']',
]:
    m = re.search(pattern, html, re.I)
    if m:
        print(f"  {pattern[:50]}: {m.group(1)}")

# Find admin-bar clear cache link (WP Rocket adds one)
admin_bar_m = re.search(r'(https?://[^"\']*(?:purge|clear)[^"\']*nonce[^"\']*)', html, re.I)
if admin_bar_m:
    print(f"\nAdmin bar clear URL: {admin_bar_m.group(1)[:200]}")

# Try the admin bar clear cache URL directly
# WP Rocket usually adds: ?rocket=clear-cache&_wpnonce=NONCE to admin pages
rocket_clear_m = re.search(r'\?[^"\']*rocket[^"\']*clear[^"\']*nonce=([a-f0-9]+)', html, re.I)
if rocket_clear_m:
    print(f"Rocket clear nonce from URL: {rocket_clear_m.group(1)}")

# Also check the wp-admin toolbar
r_admin = session.get(f"{SITE}/wp-admin/", timeout=15)
toolbar_clear = re.findall(r'href=["\']([^"\']*rocket[^"\']*purge[^"\']*)["\']', r_admin.text, re.I)
for u in toolbar_clear[:5]:
    print(f"\nToolbar clear URL: {u[:150]}")
    # Try calling it directly
    full_url = u if u.startswith("http") else SITE + u
    r_clear = session.get(full_url, allow_redirects=True, timeout=15)
    print(f"  Response: {r_clear.status_code} -> {r_clear.url}")

# Also try WP Rocket's direct admin-post.php action
r_export_nonce = re.search(r'_wpnonce=([a-f0-9]+)', html)
if r_export_nonce:
    wp_nonce = r_export_nonce.group(1)
    print(f"\nWP nonce from page: {wp_nonce}")

    # Try via admin-post.php
    for action in ["rocket_purge_cache", "rocket_clear_cache"]:
        r = session.post(f"{SITE}/wp-admin/admin-post.php", data={
            "action": action, "_wpnonce": wp_nonce,
        }, allow_redirects=True, timeout=15)
        print(f"  admin-post {action}: {r.status_code} {r.url}")

# Purge Pressable
press_page = session.get(f"{SITE}/wp-admin/admin.php?page=pressable_cache_management", timeout=10)
press_nonce_m = re.search(r'"nonce"\s*:\s*"([a-f0-9]+)"', press_page.text)
if press_nonce_m:
    rp = session.post(f"{SITE}/wp-admin/admin-ajax.php", data={
        "action": "pressable_edge_cache_purge", "nonce": press_nonce_m.group(1)
    }, timeout=10)
    print(f"\nPressable purge: {rp.text[:50]}")

print("\nWaiting 15s...")
time.sleep(15)

r_live = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                      headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
svgs = r_live.text.count("fill:#43627f")
print(f"Live SVGs: {svgs}, cache: {r_live.headers.get('X-nananana','?')}")
toc = r_live.text.find("Table of Contents")
li = r_live.text.find("<li", toc)
print(f"First TOC li: {r_live.text[li:li+300]}")
