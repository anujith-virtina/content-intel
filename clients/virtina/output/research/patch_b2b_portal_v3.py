import os, re, requests, base64
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WP_URL = "https://virtina.com/wp-json/wp/v2"
USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
POST_ID = 42202

html_path = os.path.join(os.path.dirname(__file__), "final_html_v2.html")
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# ── FIX 1: H3 style → match agentic-ai blog pattern ─────────────────────────
# Replace: <h3 style="color:#43627f;font-size:23px;">TEXT</h3>
# With:    <h3><span style="font-weight: normal;"><span>TEXT</span></span></h3>
content = re.sub(
    r'<h3 style="color:#43627f;font-size:23px;">(.+?)</h3>',
    r'<h3><span style="font-weight: normal;"><span>\1</span></span></h3>',
    content,
    flags=re.DOTALL
)
print(f"H3 tags converted: {len(re.findall(r'<h3><span style=\"font-weight: normal;\">', content))}")

# ── FIX 2: Remove all em dashes ──────────────────────────────────────────────
em_before = content.count("—") + content.count("&mdash;") + content.count("&#8212;")

# " — " (spaced em dash) → ", "
content = content.replace(" — ", ", ")
# Remaining bare em dash → ","
content = content.replace("—", ",")
# HTML entity variants
content = content.replace("&mdash;", ",")
content = content.replace("&#8212;", ",")
content = content.replace("&#x2014;", ",")

em_after = content.count("—") + content.count("&mdash;") + content.count("&#8212;")
print(f"Em dashes removed: {em_before - em_after} (remaining: {em_after})")

# ── Save v3 ──────────────────────────────────────────────────────────────────
v3_path = os.path.join(os.path.dirname(__file__), "final_html_v3.html")
with open(v3_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Saved final_html_v3.html")

# ── PATCH post ───────────────────────────────────────────────────────────────
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
headers = {"Authorization": f"Basic {token}", "Content-Type": "application/json"}
resp = requests.patch(
    f"{WP_URL}/posts/{POST_ID}",
    json={"content": content},
    headers=headers,
    verify=False,
    timeout=60,
)
print(f"PATCH status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    rendered = data["content"]["rendered"]
    h3_new = len(re.findall(r'<h3><span style="font-weight: normal;">', rendered))
    em_live = rendered.count("—") + rendered.count("&mdash;") + rendered.count("&#8212;")
    print(f"Live H3 (new pattern): {h3_new}")
    print(f"Live em dashes: {em_live}")
    print(f"Post status: {data.get('status')}")
    print("PATCH successful.")
else:
    print(f"Error: {resp.text[:400]}")
