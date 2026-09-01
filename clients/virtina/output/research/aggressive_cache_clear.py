"""Aggressive cache clear: WP Rocket + Pressable edge + Batcache + object cache + touch post."""
import os, sys, requests, urllib3, re, time, base64
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://virtina.com"
USERNAME = "anujith"
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
REAL_PASSWORD = os.environ.get("WP_REAL_PASSWORD", "")

# Login
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
sh = {"X-WP-Nonce": rest_nonce, "Content-Type": "application/json"}

# Step 1: Touch post 42202 with a trivial update to force WP to invalidate object cache
print("\n1. Touching post 42202 to invalidate object cache...")
r_touch = session.get(f"{SITE}/wp-json/wp/v2/posts/42202?context=edit", headers=sh, timeout=15)
current_mod = r_touch.json().get("modified", "")
# Send a trivial POST that doesn't change content
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h_api = {"Authorization": f"Basic {token}", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
r_retouched = requests.post(f"{SITE}/wp-json/wp/v2/posts/42202",
    json={"ping_status": "closed"},
    headers=h_api, verify=False, timeout=15)
print(f"Touch POST: {r_retouched.status_code}")

# Step 2: WP Rocket purge (find URL)
print("\n2. Purging WP Rocket...")
r_rocket = session.get(f"{SITE}/wp-admin/options-general.php?page=wprocket", timeout=20)
toolbar_urls = re.findall(r'href=["\']([^"\']*rocket[^"\']*purge[^"\']*)["\']', r_rocket.text, re.I)
if not toolbar_urls:
    purge_urls = re.findall(r'(https?://[^"\']*admin-post\.php[^"\']*purge[^"\']*)', r_rocket.text, re.I)
    for u in purge_urls[:2]:
        u = u.replace("&#038;", "&").replace("&amp;", "&")
        r = session.get(u, allow_redirects=True, timeout=15)
        print(f"  WP Rocket purge: {r.status_code}")
# Also check admin toolbar
r_admin = session.get(f"{SITE}/wp-admin/", timeout=15)
rocket_purges = re.findall(r'href=["\']([^"\']*rocket[^"\']*purge[^"\']*)["\']', r_admin.text, re.I)
for u in rocket_purges[:2]:
    full = u if u.startswith("http") else SITE + u
    full = full.replace("&#038;", "&").replace("&amp;", "&")
    r = session.get(full, allow_redirects=True, timeout=15)
    print(f"  WP Rocket toolbar purge: {r.status_code} -> {r.url[:80]}")

# Step 3: Pressable edge cache
print("\n3. Purging Pressable edge cache...")
press_page = session.get(f"{SITE}/wp-admin/admin.php?page=pressable_cache_management", timeout=15)
press_nonce = re.search(r'"nonce"\s*:\s*"([a-f0-9]+)"', press_page.text)
if press_nonce:
    rp = session.post(f"{SITE}/wp-admin/admin-ajax.php", data={
        "action": "pressable_edge_cache_purge", "nonce": press_nonce.group(1)
    }, timeout=15)
    print(f"  Edge cache: {rp.text[:80]}")
    # Also look for object cache / batcache flush action
    print(f"  Pressable page actions: {re.findall(r'action[\"\'=]+([a-z_]+pressable[a-z_]*)', press_page.text, re.I)[:10]}")
    batcache_actions = re.findall(r'"action"\s*:\s*"([^"]*(?:cache|flush|purge)[^"]*)"', press_page.text, re.I)
    print(f"  Cache actions found: {batcache_actions}")

# Step 4: Try object cache flush via wp.ajax
print("\n4. Trying WP object cache flush...")
for action in ["pressable_batcache_purge", "pressable_flush_all", "pressable_cache_flush",
               "rocket_clean_minify", "rocket_clean_home_cache"]:
    r = session.post(f"{SITE}/wp-admin/admin-ajax.php", data={
        "action": action, "nonce": press_nonce.group(1) if press_nonce else ""
    }, timeout=10)
    if r.text not in ["-1", "0", ""]:
        print(f"  {action}: {r.text[:60]}")

# Step 5: Direct URL purge for post 42202
print("\n5. Direct URL cache purge for post 42202...")
post_url = f"{SITE}/woocommerce-b2b-customer-portal/"
for purge_variant in [
    f"{SITE}/wp-admin/admin-ajax.php",
]:
    pass

# Use admin-post.php purge if we find the nonce
nonce_m = re.search(r'_wpnonce=([a-f0-9]+)', r_admin.text)
if nonce_m:
    purge_url = f"{SITE}/wp-admin/admin-post.php?action=purge_cache&type=all&_wpnonce={nonce_m.group(1)}"
    r_clear = session.get(purge_url, allow_redirects=True, timeout=15)
    print(f"  admin-post purge: {r_clear.status_code}")

print("\nWaiting 10s...")
time.sleep(10)

# Step 6: Check live page
print("\n6. Checking live page...")
headers_list = [
    {"User-Agent": "Mozilla/5.0 (test-1)"},
    {"User-Agent": "Mozilla/5.0 (test-2)", "Cache-Control": "no-cache, no-store"},
    {"User-Agent": "Mozilla/5.0 (test-3)", "Pragma": "no-cache"},
]
for i, hdrs in enumerate(headers_list):
    r = requests.get(post_url, headers=hdrs, verify=False, timeout=30)
    cache_hdr = r.headers.get("X-nananana", r.headers.get("X-Cache", "none"))
    toc = r.text.find("Table of Contents")
    li = r.text.find("<li", toc)
    li_html = r.text[li:li+200]
    # Extract padding and color
    pad_m = re.search(r'padding:\s*([^;!"]+)[;!]', li_html)
    col_m = re.search(r'color:\s*(#[0-9a-f]{6})', li_html, re.I)
    arrow = chr(0x279C) in r.text
    svg = r.text.count("fill:#43627f")
    print(f"  Request {i+1}: cache={cache_hdr}, padding={pad_m.group(1) if pad_m else '?'}, color={col_m.group(1) if col_m else '?'}, arrow={arrow}, svg={svg}")
