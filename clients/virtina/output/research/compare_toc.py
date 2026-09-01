import os, requests, base64, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
WP_URL = "https://virtina.com/wp-json/wp/v2"
USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0"}

for pid, label in [(42177, "volusion"), (42202, "b2b-portal")]:
    r = requests.get(f"{WP_URL}/posts/{pid}?context=edit", headers=h, verify=False, timeout=30)
    post = r.json()
    raw = post["content"].get("raw", "")
    print(f"\n=== {label} (post {pid}) ===")
    print(f"Status: {post.get('status')}, raw length: {len(raw)}")
    print(f"SVG count in raw: {raw.count('fill:#43627f')}")
    idx = raw.find("Table of Contents")
    if idx >= 0:
        print("TOC snippet:")
        print(raw[idx:idx+500])
    else:
        print("No TOC found")
