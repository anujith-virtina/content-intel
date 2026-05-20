import os, requests, base64
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WP_URL = "https://virtina.com/wp-json/wp/v2"
USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
POST_ID = 42202

token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
headers = {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

html_path = os.path.join(os.path.dirname(__file__), "final_html_v2.html")
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

payload = {"content": content}

resp = requests.patch(
    f"{WP_URL}/posts/{POST_ID}",
    json=payload,
    headers=headers,
    verify=False,
    timeout=60,
)

print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    print(f"Post ID: {data.get('id')}")
    print(f"Status: {data.get('status')}")
    print(f"Link: {data.get('link')}")
    print("PATCH successful.")
else:
    print(f"Error: {resp.text[:500]}")
