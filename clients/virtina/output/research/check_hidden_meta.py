"""Find hidden _tve_* meta keys and meta_box for both posts."""
import os, sys, requests, base64, urllib3, json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://virtina.com"
USERNAME = "anujith"
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
REAL_PASSWORD = os.environ.get("WP_REAL_PASSWORD", "")

token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0"}

# Check meta_box field for both posts
for post_id in [42177, 42202]:
    r = requests.get(f"{SITE}/wp-json/wp/v2/posts/{post_id}?context=edit", headers=h, verify=False, timeout=20)
    data = r.json()
    print(f"\n=== Post {post_id} meta_box ===")
    print(json.dumps(data.get("meta_box", {}), indent=2)[:1000])
    print(f"\n=== Post {post_id} meta ===")
    print(json.dumps(data.get("meta", {}), indent=2)[:500])

# Try session-based approach to get protected meta
session = requests.Session()
session.verify = False
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
session.get(f"{SITE}/wp-login.php", timeout=15)
session.post(f"{SITE}/wp-login.php", data={
    "log": USERNAME, "pwd": REAL_PASSWORD, "wp-submit": "Log In",
    "redirect_to": f"{SITE}/wp-admin/", "testcookie": "1",
}, allow_redirects=True, timeout=20)
rest_nonce = session.get(f"{SITE}/wp-admin/admin-ajax.php?action=rest-nonce", timeout=10).text.strip()
sh = {"X-WP-Nonce": rest_nonce, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

print("\n=== Session-auth meta check ===")
for post_id in [42177, 42202]:
    r = session.get(f"{SITE}/wp-json/wp/v2/posts/{post_id}?context=edit", headers=sh, timeout=20)
    data = r.json()
    meta = data.get("meta", {})
    print(f"\nPost {post_id} session meta: {list(meta.keys())}")
    for k, v in meta.items():
        if v:
            print(f"  {k}: {str(v)[:80]}")

# Try to access Thrive-specific meta via TCB endpoints
print("\n=== TCB lightspeed analyze (post 42202) ===")
r = session.get(f"{SITE}/wp-json/tcb/v1/lightspeed/analyze", headers=sh, timeout=20)
print(f"Status: {r.status_code}")
try:
    analyze_data = r.json()
    # Look for post 42202 in the data
    content = json.dumps(analyze_data)
    idx = content.find("42202")
    if idx >= 0:
        print(f"42202 found: {content[max(0,idx-50):idx+200]}")
    else:
        # Show structure
        if isinstance(analyze_data, dict):
            for key, val in analyze_data.items():
                if isinstance(val, dict) and 'items' in val:
                    print(f"Group '{key}': {len(val.get('items', []))} items")
                    for item in val.get('items', [])[:3]:
                        print(f"  {item}")
        print(f"First 500: {content[:500]}")
except:
    print(r.text[:300])

# Try to get Thrive custom CSS endpoint
print("\n=== Thrive custom CSS endpoint ===")
r = session.get(f"{SITE}/wp-json/tcb/v1/post_css", headers=sh, timeout=20)
print(f"GET /tcb/v1/post_css: {r.status_code} {r.text[:200]}")
r2 = session.get(f"{SITE}/wp-json/tcb/v1/css", headers=sh, timeout=20)
print(f"GET /tcb/v1/css: {r2.status_code} {r2.text[:200]}")
