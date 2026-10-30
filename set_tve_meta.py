"""
Set tve_updated_post meta for post 42202 via XML-RPC wp.editPost.
If this meta is set, Thrive renders from it directly (bypassing the_content filter stripping).
"""
import os, sys, xmlrpc.client, ssl, urllib3, requests, base64, time
urllib3.disable_warnings()
sys.stdout.reconfigure(encoding="utf-8")

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0"}
SITE = "https://virtina.com"
WP = f"{SITE}/wp-json/wp/v2"

# Get current content (has Thrive-class TOC with SVGs)
r = requests.get(f"{WP}/posts/42202?context=edit", headers=h, verify=False, timeout=30)
post_data = r.json()
content_raw = post_data["content"]["raw"]
print(f"Current content: {len(content_raw)} chars")
print(f"thrv-styled_list: {'thrv-styled_list' in content_raw}")
print(f"SVGs: {content_raw.count('<svg')}")

# Try XML-RPC wp.editPost with tve_updated_post custom field
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
server = xmlrpc.client.ServerProxy(f"{SITE}/xmlrpc.php", context=ctx, allow_none=True)

# Method 1: Try setting tve_updated_post via custom_fields in wp.editPost
print("\n=== Method 1: wp.editPost with tve_updated_post ===")
try:
    result = server.wp.editPost(1, USERNAME, APP_PASSWORD, 42202, {
        "custom_fields": [
            {"key": "tve_updated_post", "value": content_raw}
        ]
    })
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")

# Method 2: Try setting _tve_updated_post (with underscore prefix)
print("\n=== Method 2: wp.editPost with _tve_updated_post ===")
try:
    result2 = server.wp.editPost(1, USERNAME, APP_PASSWORD, 42202, {
        "custom_fields": [
            {"key": "_tve_updated_post", "value": content_raw}
        ]
    })
    print(f"Result: {result2}")
except Exception as e:
    print(f"Error: {e}")

# Method 3: Try setting tve_globals (Thrive globals meta)
print("\n=== Method 3: wp.editPost with tve_globals ===")
try:
    result3 = server.wp.editPost(1, USERNAME, APP_PASSWORD, 42202, {
        "custom_fields": [
            {"key": "tve_globals", "value": '{"fonts":[]}'}
        ]
    })
    print(f"Result: {result3}")
except Exception as e:
    print(f"Error: {e}")

# Check if meta was actually set
print("\n=== Verifying meta via XML-RPC ===")
try:
    post_after = server.wp.getPost(1, USERNAME, APP_PASSWORD, 42202, ["custom_fields"])
    meta = post_after.get("custom_fields", [])
    print(f"Total meta fields now: {len(meta)}")
    for m in meta:
        k = m.get("key", "")
        v = str(m.get("value", ""))
        if any(x in k.lower() for x in ["tve", "tcb", "thrive", "thrv"]):
            print(f"  *** THRIVE: {k} = {v[:200]}")
        else:
            print(f"  {k}: {len(v)} chars")
except Exception as e:
    print(f"Meta check error: {e}")

# Check live page after a delay
print("\nWaiting 8s...")
time.sleep(8)
r_live = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                      headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
svg_count = r_live.text.count("fill:#43627f")
tcb_count = r_live.text.count("tcb-icon")
cache = r_live.headers.get("X-nananana", "none")
toc_idx = r_live.text.find("Table of Contents")
li_idx = r_live.text.find("<li", toc_idx)
print(f"Live: cache={cache}, SVG={svg_count}, tcb-icon={tcb_count}")
print(f"First TOC li:\n{r_live.text[li_idx:li_idx+400]}")
