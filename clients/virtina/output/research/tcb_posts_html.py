"""
Try POST /tcb/v1/posts/html with actual content to bypass Thrive Lightspeed.
Also try the correct Thrive save payload format.
"""
import os, sys, requests, base64, urllib3, json, time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}",
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
hj = {**h, "Content-Type": "application/json"}
hf = {**h, "Content-Type": "application/x-www-form-urlencoded"}
SITE = "https://virtina.com"
TCB = f"{SITE}/wp-json/tcb/v1"

# First get the current post_content (with SVGs) to use as the content
r_post = requests.get(f"{SITE}/wp-json/wp/v2/posts/42202?context=edit",
                      headers=h, verify=False, timeout=30)
current_content = r_post.json()["content"]["raw"]
print(f"Current content SVG count: {current_content.count('fill:#43627f')}")

# Probe the /posts/html endpoint options
r_opts = requests.options(f"{TCB}/posts/html", headers=h, verify=False, timeout=10)
print(f"\nOPTIONS /posts/html: {r_opts.status_code}")
try:
    opts_data = r_opts.json()
    eps = opts_data.get("endpoints", [{}])
    if eps:
        print(f"Args: {list(eps[0].get('args', {}).keys())}")
    print(json.dumps(opts_data, indent=2)[:800])
except Exception:
    print(r_opts.text[:300])

# Try various payload formats for the POST endpoint
print("\n=== POST /tcb/v1/posts/html with various payloads ===")
payloads = [
    {"post_id": 42202, "html": current_content[:200]},
    {"post_id": 42202, "tve_content": current_content[:200]},
    {"post_id": "42202", "content": current_content[:200]},
    {"ID": 42202, "html": current_content[:200]},
    {"id": 42202, "tve_content": current_content[:200]},
]
for p in payloads:
    keys = list(p.keys())
    r = requests.post(f"{TCB}/posts/html", json=p, headers=hj, verify=False, timeout=20)
    print(f"  keys={keys} -> {r.status_code}: {r.text[:150]}")

# Also try POST with the full current content
print("\n=== POST /posts/html with FULL content ===")
full_payload = {
    "post_id": 42202,
    "tve_content": current_content,
    "tve_content_more": "",
    "tve_save_post": 1,
    "post_title": "Does your WooCommerce store have a B2B customer portal, or just an account page?",
}
r_full = requests.post(f"{TCB}/posts/html", json=full_payload, headers=hj, verify=False, timeout=30)
print(f"  status: {r_full.status_code}: {r_full.text[:300]}")

# Check live page
time.sleep(3)
r_live = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                      headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
                      verify=False, timeout=30)
svg_count = r_live.text.count("fill:#43627f")
print(f"\nLive page SVG count: {svg_count}")
print(f"Cache: {r_live.headers.get('X-nananana','?')}")
