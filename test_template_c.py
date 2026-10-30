"""
Test: replace Thrive-class TOC with Template C (no thrv_ classes).
Then check if the Thrive tve_flt wrapper appears on the live page.
If wrapper disappears with Template C, the Thrive detection is content-based.
"""
import os, sys, requests, base64, urllib3, time, re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0"}
hj = {**h, "Content-Type": "application/json"}
SITE = "https://virtina.com"
WP = f"{SITE}/wp-json/wp/v2"

# Get current content (has Thrive-class TOC)
r = requests.get(f"{WP}/posts/42202?context=edit", headers=h, verify=False, timeout=30)
content = r.json()["content"]["raw"]
print(f"Current content: {len(content)} chars, thrv-styled_list: {'thrv-styled_list' in content}")

# Build Template C TOC
SVG = '<svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg>'
SPAN = f'<span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;">{SVG}</span>'
LI_STYLE = 'style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"'
A_STYLE = 'style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;"'

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
    f'<li {LI_STYLE}>{SPAN}<a href="#{a}" {A_STYLE}>{t}</a></li>'
    for a, t in toc_items
)
template_c_toc = (
    '<h3 style="color:#43627f;font-size:22px;">Table of Contents</h3>\n'
    f'<ul style="list-style:none!important;padding-left:0!important;margin:0 0 1.5em 0!important;">\n'
    f'{li_items}\n</ul>'
)

# Find and replace the current TOC
old_h3 = '<h3 style="color:#43627f;font-size:22px;">Table of Contents</h3>'
h3_idx = content.find(old_h3)
ul_end = content.find('</ul>', h3_idx) + 5
old_block = content[h3_idx:ul_end]
new_content = content.replace(old_block, template_c_toc)

print(f"\nNew content: {len(new_content)} chars")
print(f"thrv-styled_list in new: {'thrv-styled_list' in new_content}")
print(f"SVGs in new: {new_content.count('<svg')}")
print(f"First TOC li: {new_content[new_content.find('<li style'):new_content.find('<li style')+200]}")

# Also check: does post content have any other thrv_ markers?
other_thrv = re.findall(r'class="[^"]*thrv[^"]*"', new_content)
print(f"\nOther thrv_ classes after TOC replacement: {len(other_thrv)}")
for c in other_thrv[:5]:
    print(f"  {c}")

# PATCH
print("\nPATCHing...")
r2 = requests.patch(f"{WP}/posts/42202", json={"content": new_content, "status": "publish"},
                    headers=hj, verify=False, timeout=30)
print(f"PATCH: {r2.status_code}")

print("\nWaiting 8s...")
time.sleep(8)

# Check live page for tve_flt wrapper
r_live = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                      headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
has_wrapper = 'id="tve_flt"' in r_live.text
has_svg = 'fill:#43627f' in r_live.text
cache = r_live.headers.get("X-nananana", "none")
print(f"Live: cache={cache}, tve_flt_wrapper={has_wrapper}, SVGs={r_live.text.count('fill:#43627f')}")

toc_idx = r_live.text.find("Table of Contents")
li_idx = r_live.text.find("<li", toc_idx)
print(f"\nFirst TOC li:\n{r_live.text[li_idx:li_idx+400]}")
