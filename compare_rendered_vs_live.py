"""
Compare content.rendered (REST API with_content filters applied)
vs live page HTML for post 42202.
Also compares content.raw padding to see if it matches live.
"""
import os, sys, requests, base64, urllib3
urllib3.disable_warnings()
sys.stdout.reconfigure(encoding="utf-8")

USERNAME     = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h  = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0"}
SITE = "https://virtina.com"
WP   = f"{SITE}/wp-json/wp/v2"

# Fetch post with both raw and rendered content
r = requests.get(f"{WP}/posts/42202?context=edit", headers=h, verify=False, timeout=30)
post = r.json()
raw      = post["content"]["raw"]
rendered = post["content"]["rendered"]

print(f"=== content.raw ===")
print(f"  Length: {len(raw)}")
print(f"  padding 28px: {'8px 0 8px 28px' in raw}")
print(f"  padding 32px: {'8px 0 8px 32px' in raw}")
print(f"  &#10095;: {raw.count('&#10095;')}")
print(f"  <b> arrows: {raw.count('&#10095;')}")
h3_idx = raw.find('<h3 style="color:#43627f;font-size:22px;">Table of Contents</h3>')
ul_end = raw.find('</ul>', h3_idx) + 5
raw_toc = raw[h3_idx:ul_end]
li_idx = raw_toc.find('<li ')
print(f"\n  First TOC li (raw):\n  {raw_toc[li_idx:li_idx+300]}")

print(f"\n=== content.rendered (REST API filter output) ===")
print(f"  Length: {len(rendered)}")
print(f"  padding 28px: {'8px 0 8px 28px' in rendered}")
print(f"  padding 32px: {'8px 0 8px 32px' in rendered}")
print(f"  &#10095;: {rendered.count('&#10095;')}")
print(f"  ❯: {rendered.count('❯')}")
toc_r = rendered.find("Table of Contents")
li_r  = rendered.find("<li", toc_r)
print(f"\n  First TOC li (rendered):\n  {rendered[li_r:li_r+400]}")

print(f"\n=== Live page ===")
r_live = requests.get(
    f"{SITE}/woocommerce-b2b-customer-portal/",
    headers={"User-Agent": "Mozilla/5.0 (compatible; compare-check/1.0)"},
    verify=False, timeout=30
)
live = r_live.text
cache = r_live.headers.get("X-nananana", "none")
print(f"  Cache: {cache}, Length: {len(live)}")
print(f"  padding 28px: {'8px 0 8px 28px' in live}")
print(f"  padding 32px: {'8px 0 8px 32px' in live}")
print(f"  &#10095;: {live.count('&#10095;')}")
print(f"  ❯: {live.count('❯')}")
toc_l = live.find("Table of Contents")
li_l  = live.find("<li", toc_l)
print(f"\n  First TOC li (live):\n  {live[li_l:li_l+400]}")

# Check if Thrive renders from tve_updated_post by looking for Thrive markers
print(f"\n=== Thrive rendering markers ===")
print(f"  tve_flt wrapper in live: {'id=\"tve_flt\"' in live}")
print(f"  tve_shortcode_rendered in live: {'tve_shortcode_rendered' in live}")
print(f"  thrv-styled_list in live: {'thrv-styled_list' in live}")
print(f"  tcb-styled-list in live: {'tcb-styled-list' in live}")

# Try fetching with logged-in user context to see if different
print(f"\n=== Auth'd page fetch (bypass some caches) ===")
r_auth = requests.get(
    f"{SITE}/woocommerce-b2b-customer-portal/",
    headers={**h, "Cache-Control": "no-cache", "Pragma": "no-cache"},
    verify=False, timeout=30
)
live_auth = r_auth.text
cache_auth = r_auth.headers.get("X-nananana", "none")
print(f"  Cache: {cache_auth}, Length: {len(live_auth)}")
print(f"  padding 28px: {'8px 0 8px 28px' in live_auth}")
print(f"  padding 32px: {'8px 0 8px 32px' in live_auth}")
toc_a = live_auth.find("Table of Contents")
li_a  = live_auth.find("<li", toc_a)
print(f"\n  First TOC li (auth'd):\n  {live_auth[li_a:li_a+400]}")
