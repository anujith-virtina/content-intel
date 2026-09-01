import os, requests, base64, urllib3, json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WP_URL = "https://chatsku.com/wp-json/wp/v2"
USERNAME = os.environ.get("CHATSKU_WP_USERNAME", "")
APP_PASSWORD = os.environ.get("CHATSKU_WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {
    "Authorization": f"Basic {token}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}

# Find post by slug
r = requests.get(f"{WP_URL}/posts", params={"slug": "b2b-catalog-issues-costing-sales", "per_page": 1},
                 headers=h, verify=False, timeout=20)
posts = r.json()
if not posts:
    print("Post not found")
    exit(1)
post = posts[0]
print(f"Post ID: {post['id']}")
print(f"Title: {post['title']['rendered']}")
print(f"Status: {post['status']}")
content = post["content"]["raw"] if "raw" in post.get("content", {}) else post["content"]["rendered"]
print(f"Content length: {len(content)}")
print("\n--- FIRST 3000 chars ---")
print(content[:3000])
out = {"id": post["id"], "content": content}
with open("b2b_catalog_post.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("\nSaved b2b_catalog_post.json")
