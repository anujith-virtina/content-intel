"""
Probe POST /tcb/v1/posts/html — Thrive's own content save API.
If this updates Thrive's stored version (not just post_content), arrows would show.
Also check OPTIONS to understand accepted parameters.
"""
import os, sys, requests, base64, urllib3, json, time, re
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
WP  = f"{SITE}/wp-json/wp/v2"

# Get current DB content (with SVGs and arrows already in it)
r = requests.get(f"{WP}/posts/42202?context=edit", headers=h, verify=False, timeout=30)
post_data = r.json()
content_raw = post_data["content"]["raw"]
content_rendered = post_data["content"]["rendered"]
print(f"DB raw: {len(content_raw)} chars, SVGs: {content_raw.count('fill:#43627f')}")
print(f"DB rendered: {len(content_rendered)} chars, SVGs: {content_rendered.count('fill:#43627f')}")

# Check OPTIONS on /posts/html
print("\n=== OPTIONS /tcb/v1/posts/html ===")
r_opts = requests.options(f"{TCB}/posts/html", headers=hj, verify=False, timeout=10)
print(f"Status: {r_opts.status_code}")
try:
    opts = r_opts.json()
    endpoints = opts.get("endpoints", [{}])
    for ep in endpoints:
        print(f"Methods: {ep.get('methods')}")
        args = ep.get("args", {})
        print(f"Args: {json.dumps(args, indent=2)[:600]}")
except:
    print(r_opts.text[:300])

# Try POST /posts/html with various payloads
# This endpoint is Thrive's save-content API — if it updates Thrive's stored version,
# the lightspeed cache would be invalidated
print("\n=== POST /tcb/v1/posts/html ===")

payloads = [
    # Standard Thrive Architect save format
    {"post_id": 42202, "tve_content": content_raw, "tve_save_post": 1},
    {"post_id": 42202, "html": content_raw},
    # Rendered content (fully processed HTML)
    {"post_id": 42202, "tve_content": content_rendered, "tve_save_post": 1},
    # Minimal with just the ID
    {"post_id": 42202},
    # String version
    {"post_id": "42202", "tve_content": content_raw[:500]},
]

for payload in payloads:
    keys = list(payload.keys())
    r2 = requests.post(f"{TCB}/posts/html", json=payload,
                       headers=hj, verify=False, timeout=30)
    print(f"  keys={keys} -> {r2.status_code}: {r2.text[:200]}")

# Try with form-encoded data instead of JSON
print("\n=== POST /posts/html (form-encoded) ===")
import urllib.parse
form_data = urllib.parse.urlencode({
    "post_id": 42202,
    "tve_content": content_raw[:1000],
    "tve_save_post": 1,
})
r3 = requests.post(f"{TCB}/posts/html", data=form_data,
                   headers=hf, verify=False, timeout=30)
print(f"  form-encoded -> {r3.status_code}: {r3.text[:200]}")

# Check live page to see if anything changed
print("\nChecking live page...")
time.sleep(8)
r_live = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                      headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
live = r_live.text
svg_live = live.count("fill:#43627f")
arrow_live = "➜" in live
cache = r_live.headers.get("X-nananana", "?")
print(f"Live: SVGs={svg_live}, arrow_char={arrow_live}, cache={cache}")
toc = live.find("Table of Contents")
first_li = live.find("<li", toc)
print(f"First live TOC li:\n{live[first_li:first_li+300]}")
