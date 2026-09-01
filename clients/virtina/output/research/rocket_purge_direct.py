"""Call WP Rocket purge_cache directly via admin-post.php."""
import os, sys, requests, urllib3, re, time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://virtina.com"
USERNAME = "anujith"
PASSWORD = os.environ.get("WP_REAL_PASSWORD", "")

session = requests.Session()
session.verify = False
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "Referer": f"{SITE}/wp-admin/options-general.php?page=wprocket"})

# Login
session.get(f"{SITE}/wp-login.php", timeout=15)
session.post(f"{SITE}/wp-login.php", data={
    "log": USERNAME, "pwd": PASSWORD, "wp-submit": "Log In",
    "redirect_to": f"{SITE}/wp-admin/", "testcookie": "1",
}, allow_redirects=True, timeout=20)
logged_in = any("logged_in" in k for k in session.cookies.keys())
print(f"Logged in: {logged_in}")

# Get a nonce for purge_cache action
r_rocket = session.get(f"{SITE}/wp-admin/options-general.php?page=wprocket", timeout=20)

# Find the actual purge URL with nonce embedded
purge_urls = re.findall(
    r'https://virtina\.com/wp-admin/admin-post\.php\?action=purge_cache[^"\'<\s]*',
    r_rocket.text
)
print(f"Purge URLs found: {len(purge_urls)}")
for u in purge_urls:
    clean_url = u.replace("&#038;", "&").replace("&amp;", "&")
    print(f"  {clean_url[:200]}")

# Call each purge URL directly with our session
for u in purge_urls[:3]:
    clean_url = u.replace("&#038;", "&").replace("&amp;", "&")
    r = session.get(clean_url, allow_redirects=True, timeout=20)
    print(f"\nGET purge_cache: {r.status_code} -> {r.url}")
    if r.status_code in [200, 302]:
        print(f"  Likely succeeded")

# Also try with nonce from the page
nonce_m = re.search(r'name=["\']_wpnonce["\'][^>]*value=["\']([a-f0-9]+)["\']', r_rocket.text)
if nonce_m:
    wp_nonce = nonce_m.group(1)
    print(f"\nWP nonce: {wp_nonce}")
    purge_url = f"{SITE}/wp-admin/admin-post.php?action=purge_cache&type=all&_wpnonce={wp_nonce}"
    r2 = session.get(purge_url, allow_redirects=True, timeout=20)
    print(f"GET purge with nonce: {r2.status_code} -> {r2.url}")

# Purge Pressable
press_page = session.get(f"{SITE}/wp-admin/admin.php?page=pressable_cache_management", timeout=10)
press_nonce_m = re.search(r'"nonce"\s*:\s*"([a-f0-9]+)"', press_page.text)
if press_nonce_m:
    rp = session.post(f"{SITE}/wp-admin/admin-ajax.php", data={
        "action": "pressable_edge_cache_purge", "nonce": press_nonce_m.group(1)
    }, timeout=10)
    print(f"\nPressable purge: {rp.text[:60]}")

print("\nWaiting 15s...")
time.sleep(15)

r_live = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                      headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
svgs = r_live.text.count("fill:#43627f")
cache = r_live.headers.get("X-nananana", "?")
print(f"Live: SVGs={svgs}, cache={cache}")
toc = r_live.text.find("Table of Contents")
li = r_live.text.find("<li", toc)
print(f"First TOC li:\n{r_live.text[li:li+400]}")
