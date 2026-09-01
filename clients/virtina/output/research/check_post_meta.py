import os, requests, base64, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
WP_URL = "https://virtina.com/wp-json/wp/v2"
USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0"}

r = requests.get(f"{WP_URL}/posts/42202/meta", headers=h, verify=False, timeout=30)
print("Meta endpoint status:", r.status_code)
if r.status_code == 200:
    metas = r.json()
    print("Total meta entries:", len(metas))
    for m in metas:
        k = m.get("key", "")
        v = str(m.get("value", ""))[:100]
        mid = m.get("id", "")
        print(f"  [{mid}] {k}: {v}")
else:
    print(r.text[:300])

# Also check if there's a thrv content stored somewhere via custom query
print("\nChecking for Thrive content in raw post data...")
r2 = requests.get(f"{WP_URL}/posts/42202?context=edit", headers=h, verify=False, timeout=30)
post = r2.json()
all_keys = list(post.keys())
print("Top-level post keys:", all_keys)
