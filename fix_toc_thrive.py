"""
Use POST /tcb/v1/posts/html to set the proper Thrive-formatted TOC for post 42202.
The data-css IDs are shared across all Thrive posts on virtina.com (same design system).
"""
import os, sys, requests, base64, urllib3, json, time, re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
hj = {**h, "Content-Type": "application/json"}
SITE = "https://virtina.com"
WP = f"{SITE}/wp-json/wp/v2"
TCB = f"{SITE}/wp-json/tcb/v1"

# First, check OPTIONS on /posts/html to understand accepted args
print("=== OPTIONS /tcb/v1/posts/html ===")
r_opts = requests.options(f"{TCB}/posts/html", headers=hj, verify=False, timeout=10)
print(f"Status: {r_opts.status_code}")
try:
    opts = r_opts.json()
    for ep in opts.get("endpoints", []):
        print(f"Methods: {ep.get('methods')}")
        args = ep.get("args", {})
        if args:
            print(f"Args: {json.dumps(args, indent=2)[:1000]}")
        else:
            print("Args: (empty)")
except Exception as e:
    print(f"Parse error: {e}, raw: {r_opts.text[:200]}")

# Get current raw content from post 42202
print("\n=== Fetching current post 42202 content ===")
r_post = requests.get(f"{WP}/posts/42202?context=edit", headers=h, verify=False, timeout=30)
post_data = r_post.json()
content_raw = post_data["content"]["raw"]
print(f"Current content: {len(content_raw)} chars, SVGs: {content_raw.count('fill:#43627f')}")

# Build Thrive TOC HTML (using same data-css IDs as reference post 42074)
# These data-css IDs are part of the shared Thrive design system on virtina.com
SVG = '<svg class="tcb-icon" viewBox="0 0 24 24" data-id="icon-arrow-right-solid" data-name=""><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"></path></svg>'
ICON_DIV = f'<div class="tcb-styled-list-icon"><div class="thrv_wrapper thrv_icon tve_no_drag tcb-no-delete tcb-no-clone tcb-no-save tcb-icon-inherit-style tcb-local-vars-root tcb-icon-display" data-css="tve-u-19a78073f6e" style="">{SVG}</div></div>'
ICON_DIV_NEXT = f'<div class="tcb-styled-list-icon"><div class="thrv_wrapper thrv_icon tve_no_drag tcb-no-delete tcb-no-clone tcb-no-save tcb-icon-inherit-style" data-css="tve-u-19ce2eec24a">{SVG}</div></div>'

def make_li(anchor, text, is_first=False):
    icon = ICON_DIV if is_first else ICON_DIV_NEXT
    span = f'<span class="thrv-advanced-inline-text tve_editable tcb-styled-list-icon-text tcb-no-delete tcb-no-save" data-css="tve-u-19a78073fba" style=""><a href="#{anchor}" class="tve-jump-scroll" style="outline: none;">{text}</a></span>'
    if is_first:
        return f'<li class="thrv-styled-list-item" data-css="tve-u-19a78073f6d" style="">{icon}{span}</li>'
    else:
        return f'<li class="thrv-styled-list-item" data-css="tve-u-19a78073f6d">{icon}{span}</li>'

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

li_items = "\n".join(make_li(a, t, i == 0) for i, (a, t) in enumerate(toc_items))
thrive_toc = (
    '<h3 style="color:#43627f;font-size:22px;">Table of Contents</h3>'
    f'\n<div class="thrv_wrapper thrv-styled_list" data-icon-code="icon-arrow-right-solid" data-css="tve-u-19a78073f6c" style="">'
    f'\n<ul class="tcb-styled-list">'
    f'\n{li_items}'
    f'\n</ul>'
    f'\n</div>'
)
print(f"\nThrive TOC HTML built: {len(thrive_toc)} chars")
print(f"First li preview: {thrive_toc[thrive_toc.find('<li'):thrive_toc.find('<li')+200]}")

# Replace the current Template C TOC with the Thrive-class TOC in content
old_toc_start = content_raw.find('<h3 style="color:#43627f;font-size:22px;">Table of Contents</h3>')
old_toc_ul_end = content_raw.find('</ul>', old_toc_start) + 5
old_toc_block = content_raw[old_toc_start:old_toc_ul_end]
print(f"\nOld TOC block: {len(old_toc_block)} chars, starts with: {old_toc_block[:60]}")

new_content = content_raw.replace(old_toc_block, thrive_toc)
print(f"New content: {len(new_content)} chars")
print(f"thrv-styled_list in new: {'thrv-styled_list' in new_content}")

# Try posting to /tcb/v1/posts/html
print("\n=== POST /tcb/v1/posts/html ===")
payloads = [
    {"post_id": 42202, "tve_content": new_content},
    {"post_id": 42202, "tve_content": new_content, "tve_save_post": 1},
    {"post_id": 42202, "html": new_content},
    {"post_id": 42202, "content": new_content},
    {"post_id": "42202", "tve_content": new_content},
]
for payload in payloads:
    keys = list(payload.keys())
    r = requests.post(f"{TCB}/posts/html", json=payload, headers=hj, verify=False, timeout=30)
    print(f"  keys={keys} -> {r.status_code}: {r.text[:200]}")
    if r.status_code == 200:
        print("  SUCCESS! Breaking.")
        break

# Also update post_content via REST API
print("\n=== Also PATCH post_content with Thrive HTML ===")
r_patch = requests.patch(f"{WP}/posts/42202",
                          json={"content": new_content, "status": "publish"},
                          headers=hj, verify=False, timeout=30)
print(f"PATCH status: {r_patch.status_code}")

# Check live page after a delay
print("\nWaiting 8s for cache to settle...")
time.sleep(8)
r_live = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                      headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
toc_idx = r_live.text.find("Table of Contents")
li_idx = r_live.text.find("<li", toc_idx)
svg_count = r_live.text.count("fill:#43627f")
tcb_icon_count = r_live.text.count("tcb-icon")
print(f"Live: SVG count={svg_count}, tcb-icon={tcb_icon_count}")
print(f"First TOC li (400 chars):\n{r_live.text[li_idx:li_idx+400]}")
