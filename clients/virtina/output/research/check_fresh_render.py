"""
Request live page AS LOGGED-IN ADMIN — WP Rocket skips cache for admins.
This shows the true PHP render without any cache layer.
Also verify DB content and Lightspeed state.
"""
import os, sys, requests, urllib3, re, time, base64
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

# Check DB content
token = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
h_api = {"Authorization": f"Basic {token}",
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
r_db = requests.get(f"{SITE}/wp-json/wp/v2/posts/42202?context=edit",
                    headers=h_api, verify=False, timeout=15)
if r_db.status_code == 200:
    raw = r_db.json()["content"]["raw"]
    print(f"\nDB content: {len(raw)} chars")
    print(f"DB SVGs (fill:#43627f): {raw.count('fill:#43627f')}")
    print(f"DB unicode arrows (➜): {raw.count(chr(0x279C))}")
    print(f"DB color #43627f: {raw.count('#43627f')}")
    # Show first TOC item in DB
    toc = raw.find("Table of Contents")
    li = raw.find("<li", toc)
    print(f"First DB TOC li: {raw[li:li+300]}")
else:
    print(f"DB check failed: {r_db.status_code}")

# Check Lightspeed status
r_ls = session.get(f"{SITE}/wp-admin/admin.php?page=tve_lightspeed", timeout=20)
ls_m = re.search(r'"is_enabled"\s*:\s*(true|false|\d+)', r_ls.text)
print(f"\nLightspeed is_enabled: {ls_m.group(1) if ls_m else 'UNKNOWN'}")

# Request live page WITH session (WP Rocket bypasses cache for logged-in admins)
print("\n=== Fresh render via logged-in session ===")
r_fresh = session.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                      allow_redirects=True, timeout=30)
svgs_fresh = r_fresh.text.count("fill:#43627f")
arrows_fresh = chr(0x279C) in r_fresh.text
color_43 = "#43627f" in r_fresh.text
cache_hdr = r_fresh.headers.get("X-nananana", r_fresh.headers.get("X-Cache", "?"))
print(f"Admin-session render: SVGs={svgs_fresh}, arrow_char={arrows_fresh}, #43627f={color_43}")
print(f"Cache header: {cache_hdr}")
toc_f = r_fresh.text.find("Table of Contents")
li_f = r_fresh.text.find("<li", toc_f)
print(f"First TOC li:\n{r_fresh.text[li_f:li_f+400]}")

# Anonymous request for comparison
print("\n=== Anonymous request (cached) ===")
r_anon = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                      headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
svgs_anon = r_anon.text.count("fill:#43627f")
arrows_anon = chr(0x279C) in r_anon.text
cache_hdr2 = r_anon.headers.get("X-nananana", r_anon.headers.get("X-Cache", "?"))
print(f"Anonymous: SVGs={svgs_anon}, arrow_char={arrows_anon}, cache={cache_hdr2}")
toc_a = r_anon.text.find("Table of Contents")
li_a = r_anon.text.find("<li", toc_a)
print(f"First TOC li:\n{r_anon.text[li_a:li_a+350]}")
