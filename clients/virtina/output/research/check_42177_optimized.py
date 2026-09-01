"""Check if post 42177 is in Thrive Lightspeed optimized list."""
import os, sys, requests, base64, urllib3, json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0"}
SITE = "https://virtina.com"

# Get the full lightspeed analyze list (all pages)
r = requests.get(f"{SITE}/wp-json/tcb/v1/lightspeed/analyze",
                 headers=h, verify=False, timeout=20)
data = r.json()

# Find posts of type "post"
posts = data.get("post", {}).get("items", [])
print(f"Total posts in lightspeed: {len(posts)}")
print(f"\nSearching for posts 42202 and 42177...")
for p in posts:
    if p.get("id") in [42202, 42177]:
        print(f"  ID={p['id']} optimized={p.get('optimized')} name={p.get('name','')[:60]}")

# Also check if 42177 is optimized
optimized_ids = [p["id"] for p in posts if p.get("optimized") == 1]
not_optimized_ids = [p["id"] for p in posts if p.get("optimized") == 0]
print(f"\nOptimized count: {len(optimized_ids)}")
print(f"Not optimized count: {len(not_optimized_ids)}")
print(f"42177 in optimized: {42177 in optimized_ids}")
print(f"42202 in optimized: {42202 in optimized_ids}")

# Check user ID 9 (admin user)
print("\n=== Check user ID 9 capabilities ===")
r2 = requests.get(f"{SITE}/wp-json/wp/v2/users/9", headers=h, verify=False, timeout=15)
u = r2.json()
print(f"User: {u.get('name')} role: {u.get('roles')} caps: {list(u.get('capabilities',{}).keys())[:10]}")
