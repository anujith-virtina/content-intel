"""
Fix TOC arrows on post 42202 using a unicode character in a positioned <span>.
wp_kses_post strips SVG tags (empty span removed) and strips url() from CSS.
A <span> containing a text node (unicode arrow ❯) should survive the filter.
No aria-hidden attribute (not in kses allowed attrs for span).
"""
import os, sys, requests, base64, urllib3, time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h  = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0"}
hj = {**h, "Content-Type": "application/json"}
SITE = "https://virtina.com"
WP   = f"{SITE}/wp-json/wp/v2"

r = requests.get(f"{WP}/posts/42202?context=edit", headers=h, verify=False, timeout=30)
content = r.json()["content"]["raw"]
print(f"Current content: {len(content)} chars")

# Arrow span: unicode ❯ (U+276F), absolutely positioned at left edge of the li.
# No aria-hidden, no SVG — just a text node inside <span style="...">.
ARROW_SPAN = (
    '<span style="'
    'color:#43627f!important;'
    'position:absolute!important;'
    'left:0!important;'
    'top:50%!important;'
    'transform:translateY(-50%)!important;'
    'font-size:18px!important;'
    'line-height:1!important;'
    'font-style:normal!important;'
    'font-weight:700!important;'
    '">❯</span>'
)
LI_STYLE = (
    'style="'
    'list-style:none!important;'
    'padding:8px 0 8px 28px!important;'
    'position:relative!important;'
    'line-height:1.5!important;'
    'margin:0!important;'
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
    f'<li {LI_STYLE}>{ARROW_SPAN}<a href="#{a}" {A_STYLE}>{t}</a></li>'
    for a, t in toc_items
)
toc_html = (
    '<h3 style="color:#43627f;font-size:22px;">Table of Contents</h3>\n'
    '<ul style="list-style:none!important;padding-left:0!important;margin:0 0 1.5em 0!important;">\n'
    f'{li_items}\n'
    '</ul>'
)

h3_tag = '<h3 style="color:#43627f;font-size:22px;">Table of Contents</h3>'
h3_idx = content.find(h3_tag)
ul_end = content.find('</ul>', h3_idx) + 5
old_toc = content[h3_idx:ul_end]
print(f"Old TOC: {len(old_toc)} chars")
print(f"New TOC: {len(toc_html)} chars")

new_content = content[:h3_idx] + toc_html + content[ul_end:]
print(f"New content: {len(new_content)} chars")
print(f"❯ count in new: {new_content.count('❯')}")
print(f"\nFirst TOC li:\n{new_content[new_content.find('<li style'):new_content.find('<li style')+300]}")

print("\nPATCHing post 42202...")
r2 = requests.patch(f"{WP}/posts/42202",
                    json={"content": new_content, "status": "publish"},
                    headers=hj, verify=False, timeout=30)
print(f"PATCH: {r2.status_code}")

print("Waiting 10s...")
time.sleep(10)

r_live = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                      headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
cache       = r_live.headers.get("X-nananana", "none")
has_tve     = 'id="tve_flt"' in r_live.text
arrow_count = r_live.text.count("❯")
print(f"Live: cache={cache}, tve_flt={has_tve}, ❯ count={arrow_count}")

toc_idx = r_live.text.find("Table of Contents")
li_idx  = r_live.text.find("<li", toc_idx)
print(f"\nFirst TOC li on live page:\n{r_live.text[li_idx:li_idx+600]}")
