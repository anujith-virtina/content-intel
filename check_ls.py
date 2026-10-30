"""Check Thrive Lightspeed status for post 42202 and try optimize endpoint."""
import os, requests, base64, urllib3, json
urllib3.disable_warnings()

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0"}
hj = {**h, "Content-Type": "application/json"}
SITE = "https://virtina.com"

# Check lightspeed analyze
print("=== Lightspeed analyze ===")
r = requests.get(f"{SITE}/wp-json/tcb/v1/lightspeed/analyze", headers=h, verify=False, timeout=20)
data = r.json()
posts = data.get("post", {}).get("items", [])
print(f"Total posts in Lightspeed: {len(posts)}")

target = None
for p in posts:
    if p.get("id") == 42202:
        target = p
        print(f"Post 42202: {json.dumps(p, indent=2)}")
        break

if not target:
    print("Post 42202 NOT in Lightspeed index — not optimized")

if posts:
    print(f"\nSample item (first): {json.dumps(posts[0], indent=2)[:400]}")

print(f"\nAll analyze keys: {list(data.keys())}")

# Try the optimize endpoint with the post_id to re-optimize or clear
print("\n=== Try POST /lightspeed/optimize with post_id=42202 ===")
for payload in [
    {"post_id": 42202},
    {"post_id": 42202, "action": "clear"},
    {"post_id": 42202, "action": "deoptimize"},
    {"post_id": [42202], "regenerate": True},
]:
    r2 = requests.post(f"{SITE}/wp-json/tcb/v1/lightspeed/optimize",
                       json=payload, headers=hj, verify=False, timeout=20)
    print(f"  {list(payload.keys())} -> {r2.status_code}: {r2.text[:200]}")

# Try OPTIONS on the optimize endpoint to see accepted params
print("\n=== OPTIONS /lightspeed/optimize ===")
r3 = requests.options(f"{SITE}/wp-json/tcb/v1/lightspeed/optimize", headers=hj, verify=False, timeout=10)
try:
    opts = r3.json()
    for ep in opts.get("endpoints", []):
        print(f"Methods: {ep.get('methods')}")
        print(f"Args: {json.dumps(ep.get('args', {}), indent=2)[:1000]}")
except:
    print(r3.text[:300])
