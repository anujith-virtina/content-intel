"""Flush Pressable Batcache and WordPress object cache, then verify live page."""
import os, sys, requests, urllib3, re, time, base64, json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://virtina.com"
USERNAME = "anujith"
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
REAL_PASSWORD = os.environ.get("WP_REAL_PASSWORD", "")
POST_URL = f"{SITE}/woocommerce-b2b-customer-portal/"

session = requests.Session()
session.verify = False
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
session.get(f"{SITE}/wp-login.php", timeout=15)
session.post(f"{SITE}/wp-login.php", data={
    "log": USERNAME, "pwd": REAL_PASSWORD, "wp-submit": "Log In",
    "redirect_to": f"{SITE}/wp-admin/", "testcookie": "1",
}, allow_redirects=True, timeout=20)
logged_in = any("logged_in" in k for k in session.cookies.keys())
print(f"Logged in: {logged_in}")

rest_nonce = session.get(f"{SITE}/wp-admin/admin-ajax.php?action=rest-nonce", timeout=10).text.strip()
print(f"REST nonce: {rest_nonce}")

# Get full Pressable cache management page HTML
print("\n=== Pressable cache management page ===")
r_press = session.get(f"{SITE}/wp-admin/admin.php?page=pressable_cache_management", timeout=20)
print(f"Status: {r_press.status_code}, length: {len(r_press.text)}")

# Find ALL AJAX actions on this page
all_actions = re.findall(r'"action"\s*:\s*"([^"]+)"', r_press.text)
print(f"All AJAX actions: {list(set(all_actions))}")

# Find all nonces
all_nonces = re.findall(r'"nonce"\s*:\s*"([a-f0-9]{10})"', r_press.text)
print(f"All nonces: {list(set(all_nonces))[:5]}")

# Find JavaScript functions related to cache clearing
js_funcs = re.findall(r'function\s+\w*[Cc]ache\w*\s*\(', r_press.text)
print(f"Cache functions: {js_funcs[:10]}")

# Find all href/data-action attributes
data_actions = re.findall(r'data-action=["\']([^"\']+)["\']', r_press.text)
print(f"data-action: {data_actions[:10]}")

# Show relevant sections of the page
for pattern in ['batcache', 'object', 'flush', 'purge', 'memcache', 'redis']:
    matches = [(m.start(), r_press.text[max(0,m.start()-50):m.start()+100]) for m in re.finditer(pattern, r_press.text, re.I)]
    if matches:
        print(f"\n'{pattern}' context: {matches[0][1][:150]}")

# Try all cache-related AJAX actions
print("\n=== Trying all cache actions ===")
nonces = list(set(all_nonces))
for action in list(set(all_actions)) + [
    "pressable_batcache_flush", "pressable_object_cache_flush", "pressable_flush_batcache",
    "pressable_cache_clear_all", "pressable_clear_all_caches", "pressable_full_cache_purge",
    "rocket_clean_domain", "batcache_clear"
]:
    for nonce in (nonces[:2] if nonces else [rest_nonce]):
        r = session.post(f"{SITE}/wp-admin/admin-ajax.php", data={
            "action": action, "nonce": nonce, "_ajax_nonce": nonce
        }, timeout=10)
        if r.text not in ["-1", "0", "", "false", "null"]:
            print(f"  ACTION {action}: {r.text[:80]}")

# Try saving the post from WP admin (triggers full cache clear)
print("\n=== Saving post 42202 from WP admin (triggers all cache hooks) ===")
edit_url = f"{SITE}/wp-admin/post.php?post=42202&action=edit"
r_edit = session.get(edit_url, timeout=20)
if r_edit.status_code == 200:
    # Find _wpnonce, post_ID, hidden fields
    wp_nonce_m = re.search(r'name="_wpnonce"[^>]*value="([^"]+)"', r_edit.text)
    if wp_nonce_m:
        wp_nonce = wp_nonce_m.group(1)
        print(f"  Found WP nonce: {wp_nonce}")
        # Submit post update via classic editor form
        form_data = {
            "_wpnonce": wp_nonce,
            "action": "editpost",
            "post_type": "post",
            "post_ID": "42202",
            "save": "Update",
            "post_status": "publish",
            "ping_status": "closed",
            "comment_status": "open",
        }
        r_save = session.post(f"{SITE}/wp-admin/post.php", data=form_data,
                              allow_redirects=True, timeout=30)
        print(f"  Admin save: {r_save.status_code} -> {r_save.url}")
    else:
        print(f"  No WP nonce found")
        # Check redirect or error
        print(f"  Edit page status: {r_edit.status_code}, first 200: {r_edit.text[:200]}")
else:
    print(f"  Edit page failed: {r_edit.status_code}")

# Final check
print("\nWaiting 5s for caches to settle...")
time.sleep(5)
print("\n=== Final live check ===")
for i in range(3):
    r = requests.get(POST_URL, headers={"User-Agent": f"Mozilla/5.0 (check-{i})"}, verify=False, timeout=30)
    cache = r.headers.get("X-nananana", r.headers.get("X-Cache", "none"))
    toc = r.text.find("Table of Contents")
    li = r.text.find("<li", toc)
    li_html = r.text[li:li+300]
    pad_m = re.search(r'padding:\s*([^;!"]+)[;!]', li_html)
    col_m = re.search(r'color:\s*(#[0-9a-f]{6})', li_html, re.I)
    arrow = chr(0x279C) in r.text
    svg = r.text.count("fill:#43627f")
    print(f"  [{i+1}] cache={cache}, padding={pad_m.group(1) if pad_m else '?'}, color={col_m.group(1) if col_m else '?'}, arrow={arrow}, svg={svg}")
    time.sleep(1)
