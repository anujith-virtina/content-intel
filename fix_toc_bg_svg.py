"""
Fix TOC arrows on post 42202 using CSS background-image data URI on <li>.
Thrive's filter strips <svg> HTML tags and <span aria-hidden> elements,
but preserves CSS property values inside style="" attributes.
The SVG arrow is embedded as a background-image data URI on the <li> itself.
"""
import os, sys, requests, base64, urllib3, time, re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h  = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0"}
hj = {**h, "Content-Type": "application/json"}
SITE = "https://virtina.com"
WP   = f"{SITE}/wp-json/wp/v2"

# Get current content
r = requests.get(f"{WP}/posts/42202?context=edit", headers=h, verify=False, timeout=30)
content = r.json()["content"]["raw"]
print(f"Current content: {len(content)} chars, thrv-styled_list: {'thrv-styled_list' in content}")

# Arrow SVG URL-encoded for CSS background-image data URI.
# Using URL-encoded double quotes (%22) inside the data URI so the outer url('...')
# with single quotes has no conflicts.
SVG_URI = (
    "data:image/svg+xml,"
    "%3Csvg%20viewBox%3D%220%200%2024%2024%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E"
    "%3Cpath%20fill%3D%22%2343627f%22%20d%3D%22M4%2C11V13H16L10.5%2C18.5L11.92%2C19.92L19.84%2C12L11.92%2C4.08L10.5%2C5.5L16%2C11H4Z%22%2F%3E"
    "%3C%2Fsvg%3E"
)

LI_STYLE = (
    'style="'
    'list-style:none!important;'
    'padding:8px 0 8px 32px!important;'
    'position:relative!important;'
    'line-height:1.5!important;'
    'margin:0!important;'
    f"background-image:url('{SVG_URI}')!important;"
    'background-repeat:no-repeat!important;'
    'background-position:left 8px!important;'
    'background-size:18px 18px!important;'
    '"'
)
A_STYLE = (
    'style="'
    'color:#00a0e2!important;'
    'text-decoration:none!important;'
    'font-family:metropolis,arial!important;'
    'font-size:16px!important;'
    'font-weight:500!important;'
    '"'
)

toc_items = [
    ("what-is-b2b-portal",            "What is a B2B customer portal?"),
    ("why-buyers-call-sales",          "Why buyers call instead of reorder online"),
    ("b2b-portal-features",           "Must-have B2B portal features"),
    ("woocommerce-b2b-portal-plugins", "B2BKing vs. Wholesale Suite vs. custom dev"),
    ("b2b-portal-cost-timeline",      "WooCommerce B2B portal cost and timeline"),
    ("account-specific-pricing",      "Account-specific pricing without exposure"),
    ("portal-erp-integration",        "Does your portal need ERP integration?"),
    ("portal-roi-operations",         "Impact on sales rep time and support costs"),
    ("when-not-to-build-portal",      "When not to build a B2B portal"),
    ("buyer-portal-adoption",         "Getting buyers to use the portal"),
    ("people-also-ask",               "People also ask"),
    ("conclusion",                    "Conclusion"),
    ("faq",                           "Frequently asked questions"),
]

li_items = "\n".join(
    f'<li {LI_STYLE}><a href="#{a}" {A_STYLE}>{t}</a></li>'
    for a, t in toc_items
)
toc_html = (
    '<h3 style="color:#43627f;font-size:22px;">Table of Contents</h3>\n'
    '<ul style="list-style:none!important;padding-left:0!important;margin:0 0 1.5em 0!important;">\n'
    f'{li_items}\n'
    '</ul>'
)

# Find current TOC block (starts at the H3, ends at </ul>)
h3_tag   = '<h3 style="color:#43627f;font-size:22px;">Table of Contents</h3>'
h3_idx   = content.find(h3_tag)
ul_end   = content.find('</ul>', h3_idx) + 5
old_toc  = content[h3_idx:ul_end]
print(f"\nOld TOC: {len(old_toc)} chars, starts: {old_toc[:80]}")
print(f"New TOC: {len(toc_html)} chars")

new_content = content[:h3_idx] + toc_html + content[ul_end:]
print(f"New content: {len(new_content)} chars")
print(f"thrv-styled_list in new: {'thrv-styled_list' in new_content}")
print(f"SVG tags in new: {new_content.count('<svg')}")
print(f"SVG_URI in new: {new_content.count('43627f')}")
print(f"\nFirst TOC li (preview):\n{new_content[new_content.find('<li style'):new_content.find('<li style')+400]}")

# PATCH
print("\nPATCHing post 42202...")
r2 = requests.patch(f"{WP}/posts/42202",
                    json={"content": new_content, "status": "publish"},
                    headers=hj, verify=False, timeout=30)
print(f"PATCH: {r2.status_code}")

print("\nWaiting 10s for cache to settle...")
time.sleep(10)

# Check live page
r_live = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                      headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
has_wrapper = 'id="tve_flt"' in r_live.text
has_data_uri = '43627f' in r_live.text
cache = r_live.headers.get("X-nananana", "none")
print(f"Live: cache={cache}, tve_flt={has_wrapper}, arrow_color_in_page={has_data_uri}")

toc_idx = r_live.text.find("Table of Contents")
li_idx  = r_live.text.find("<li", toc_idx)
print(f"\nFirst TOC li on live page:\n{r_live.text[li_idx:li_idx+600]}")
