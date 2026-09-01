import os, requests, base64, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0"}

TARGET = "fill:#43627f"

# Default context (context=view) — goes through the_content() WP filters
r = requests.get("https://virtina.com/wp-json/wp/v2/posts/42202", headers=h, verify=False, timeout=30)
post = r.json()
rendered = post["content"]["rendered"]
print(f"context=view rendered SVG count: {rendered.count(TARGET)}")
print(f"Rendered length: {len(rendered)}")
toc = rendered.find("Table of Contents")
if toc >= 0:
    print(f"Rendered TOC:\n{rendered[toc:toc+400]}")

# Also check edit context rendered
r2 = requests.get("https://virtina.com/wp-json/wp/v2/posts/42202?context=edit", headers=h, verify=False, timeout=30)
post2 = r2.json()
rendered2 = post2["content"].get("rendered", "")
raw2 = post2["content"].get("raw", "")
print(f"\ncontext=edit rendered SVG count: {rendered2.count(TARGET)}")
print(f"context=edit raw SVG count: {raw2.count(TARGET)}")
