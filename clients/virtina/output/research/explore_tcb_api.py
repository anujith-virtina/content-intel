"""Explore Thrive Architect /tcb/v1 REST endpoints for post 42202."""
import os, requests, base64, urllib3, json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}",
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
     "Content-Type": "application/json"}
BASE = "https://virtina.com/wp-json/tcb/v1"

# Try /tcb/v1/posts/html with post_id param
print("=== GET /tcb/v1/posts/html ===")
r = requests.get(f"{BASE}/posts/html", params={"post_id": 42202},
                 headers=h, verify=False, timeout=20)
print(f"Status: {r.status_code}")
body = r.text[:800]
print(body)

# Try /tcb/v1/posts
print("\n=== GET /tcb/v1/posts ===")
r2 = requests.get(f"{BASE}/posts", params={"post_id": 42202},
                  headers=h, verify=False, timeout=20)
print(f"Status: {r2.status_code}")
print(r2.text[:500])

# Try POST /tcb/v1/posts/html
print("\n=== POST /tcb/v1/posts/html (options) ===")
r3 = requests.options(f"{BASE}/posts/html", headers=h, verify=False, timeout=20)
print(f"Status: {r3.status_code}")
print(r3.headers.get("Allow", "no Allow header"))
print(r3.text[:300])
