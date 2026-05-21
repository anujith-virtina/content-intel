"""Patch body images using final_html_v7.html as base (has ids 42217/42218/42219)."""
import os, re, requests, base64, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WP_URL       = "https://virtina.com/wp-json/wp/v2"
USERNAME     = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
POST_ID      = 42202

token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
wp_headers = {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

# old_id -> (new_id, new_src, alt, w, h)
REPLACEMENTS = {
    42217: (
        42222,
        "https://virtina.com/wp-content/uploads/2026/05/woocommerce-b2b-portal-body1-670x352-v4.jpg",
        "iMac desktop displaying a business analytics dashboard representing the "
        "real-time data and order management features of a WooCommerce B2B customer portal",
        670, 352,
    ),
    42218: (
        42223,
        "https://virtina.com/wp-content/uploads/2026/05/woocommerce-b2b-portal-body2-670x352-v3.jpg",
        "Business team gathered around a conference table with laptops and tablets "
        "discussing WooCommerce B2B portal implementation timeline and costs",
        670, 352,
    ),
    42219: (
        42224,
        "https://virtina.com/wp-content/uploads/2026/05/woocommerce-b2b-portal-body3-670x352-v4.jpg",
        "B2B procurement buyer using a laptop to place a repeat order on a "
        "WooCommerce self-service portal, without needing to call a sales rep",
        670, 352,
    ),
}

html_path = os.path.join(os.path.dirname(__file__), "final_html_v7.html")
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

for old_id, (new_id, src, alt, w, h) in REPLACEMENTS.items():
    new_span = (
        f'<span style="display:block;margin:20px 0;">'
        f'<img alt="{alt}" data-id="{new_id}" '
        f'width="{w}" data-init-width="{w}" '
        f'height="{h}" data-init-height="{h}" '
        f'title="" loading="lazy" src="{src}" '
        f'data-width="{w}" data-height="{h}" '
        f'style="aspect-ratio: auto {w} / {h};max-width:100%;"></span>'
    )
    pat = re.compile(rf'<span[^>]*>\s*<img[^>]*data-id="{old_id}"[^>]*>\s*</span>', re.DOTALL)
    if pat.search(content):
        content = pat.sub(new_span, content)
        print(f"Replaced data-id={old_id} -> {new_id}")
    else:
        print(f"WARNING: data-id={old_id} not found")

v8_path = os.path.join(os.path.dirname(__file__), "final_html_v8.html")
with open(v8_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Saved final_html_v8.html")

resp = requests.patch(
    f"{WP_URL}/posts/{POST_ID}",
    json={"content": content},
    headers=wp_headers, verify=False, timeout=60,
)
print(f"PATCH status: {resp.status_code}")
if resp.status_code == 200:
    rendered = resp.json()["content"]["rendered"]
    for old_id, (new_id, _, _, _, _) in REPLACEMENTS.items():
        print(f"  id={new_id} live: {str(new_id) in rendered}  old {old_id} gone: {f'data-id=\"{old_id}\"' not in rendered}")
    print(f"  Post status: {resp.json()['status']}")
    print("Done.")
else:
    print(f"Error: {resp.text[:300]}")
