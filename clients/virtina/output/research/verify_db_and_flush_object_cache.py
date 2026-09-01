"""Verify DB content and flush object cache via admin toolbar URL."""
import os, sys, requests, urllib3, re, time, base64, json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://virtina.com"
USERNAME = "anujith"
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
REAL_PASSWORD = os.environ.get("WP_REAL_PASSWORD", "")

# Check DB via REST API
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0"}
r_db = requests.get(f"{SITE}/wp-json/wp/v2/posts/42202?context=edit", headers=h, verify=False, timeout=15)
raw = r_db.json()["content"]["raw"]
toc = raw.find("Table of Contents")
li = raw.find("<li", toc)
print(f"DB content: {len(raw)} chars")
print(f"DB first <li> (300 chars):")
print(raw[li:li+300])
print(f"DB SVGs: {raw.count('fill:#43627f')}")
print(f"DB arrows: {raw.count(chr(0x279C))}")
print(f"DB #43627f count: {raw.count('#43627f')}")

# Session login
session = requests.Session()
session.verify = False
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
session.get(f"{SITE}/wp-login.php", timeout=15)
session.post(f"{SITE}/wp-login.php", data={
    "log": USERNAME, "pwd": REAL_PASSWORD, "wp-submit": "Log In",
    "redirect_to": f"{SITE}/wp-admin/", "testcookie": "1",
}, allow_redirects=True, timeout=20)

# Find and click "Flush Object Cache" from the admin toolbar
print("\n=== Finding Flush Object Cache action ===")
r_admin = session.get(f"{SITE}/wp-admin/", timeout=15)
# Look for flush object cache URL
flush_urls = re.findall(r'href=["\']([^"\']*(?:flush|purge|object)[^"\']*)["\']', r_admin.text, re.I)
for u in flush_urls[:10]:
    print(f"  {u[:120]}")

# Look in the PCM toolbar items
pcm_items = re.findall(r'id=["\']wp-admin-bar-[^"\']*["\'][^>]*>[^<]*<div[^>]*>[^<]*(?:Flush|Object|Cache|Purge)[^<]*</div', r_admin.text, re.I)
for item in pcm_items[:5]:
    print(f"  PCM item: {item[:150]}")

# More aggressive: look for any action with flush/object in it
all_hrefs = re.findall(r'href=["\']([^"\']+)["\']', r_admin.text)
cache_hrefs = [h for h in all_hrefs if any(x in h.lower() for x in ['flush', 'object-cache', 'objectcache', 'batcache', 'purge'])]
print(f"\nCache-related hrefs: {cache_hrefs[:10]}")

# Also check the admin page directly for the Pressable Cache Management
r_pcm = session.get(f"{SITE}/wp-admin/admin.php?page=pressable_cache_management", timeout=20)
# Find the "Flush Object Cache" button action URL
flush_hrefs = re.findall(r'href=["\']([^"\']*(?:flush|object)[^"\']*)["\']', r_pcm.text, re.I)
print(f"\nPCM flush hrefs: {flush_hrefs[:10]}")
# Look for the admin bar URL with "flush-object-cache"
admin_bar_flush = re.findall(r'href=["\']([^"\']*flush-object-cache[^"\']*)["\']', r_pcm.text, re.I)
if not admin_bar_flush:
    admin_bar_flush = re.findall(r'(?:href|url)=["\']([^"\']*(?:object.cache|batcache)[^"\']*)["\']', r_pcm.text, re.I)
print(f"\nFlush object cache href: {admin_bar_flush[:5]}")

# Try the flush-object-cache URL directly (some plugins use this)
for try_url in [
    f"{SITE}/wp-admin/?flush-object-cache=1",
    f"{SITE}/wp-admin/admin.php?flush-object-cache=1",
    f"{SITE}/wp-admin/?do=flush-object-cache",
]:
    r = session.get(try_url, allow_redirects=True, timeout=10)
    print(f"GET {try_url.split('?')[1]}: {r.status_code}")

# Also look in the admin toolbar HTML for the wp-admin-bar items
pcm_bar = re.findall(r'id=["\']wp-admin-bar-[^"\']*pcm[^"\']*["\'].*?</li>', r_admin.text, re.S | re.I)
for item in pcm_bar[:5]:
    print(f"\nPCM bar item: {item[:200]}")

# Check current live render - is it fresh or cached?
print("\n=== Live page state (admin session) ===")
r_live_admin = session.get(f"{SITE}/woocommerce-b2b-customer-portal/", timeout=20)
cache = r_live_admin.headers.get("X-nananana", "none")
toc_l = r_live_admin.text.find("Table of Contents")
li_l = r_live_admin.text.find("<li", toc_l)
li_html = r_live_admin.text[li_l:li_l+300]
pad_m = re.search(r'padding:\s*([^;!"]+)[;!]', li_html)
col_m = re.search(r'color:\s*(#[0-9a-f]{6})', li_html, re.I)
print(f"Admin session live render: cache={cache}")
print(f"  padding={pad_m.group(1) if pad_m else '?'}, color={col_m.group(1) if col_m else '?'}")
print(f"  arrows: {r_live_admin.text.count(chr(0x279C))}, svgs: {r_live_admin.text.count('fill:#43627f')}")
