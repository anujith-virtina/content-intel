import os, re, requests, base64
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WP_URL = "https://virtina.com/wp-json/wp/v2"
USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
POST_ID = 42202

html_path = os.path.join(os.path.dirname(__file__), "final_html_v3.html")
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# ── FIX: Revert wrong Elementor H3 pattern → correct Thrive Architect H3 ────
# Wrong (Elementor): <h3><span style="font-weight: normal;"><span>TEXT</span></span></h3>
# Correct (Thrive):  <h3 style="color:#43627f;font-size:22px;">TEXT</h3>
# Verified from post 42177 (Volusion migration, Thrive Architect, May 2026)

before = len(re.findall(r'<h3><span style="font-weight: normal;">', content))
content = re.sub(
    r'<h3><span style="font-weight: normal;"><span>(.+?)</span></span></h3>',
    r'<h3 style="color:#43627f;font-size:22px;">\1</h3>',
    content,
    flags=re.DOTALL
)
after = len(re.findall(r'<h3 style="color:#43627f;font-size:22px;">', content))
print(f"H3 reverted: {before} wrong -> {after} correct")

# ── Double-check: no em dashes remain ────────────────────────────────────────
em = content.count("—") + content.count("&mdash;") + content.count("&#8212;")
print(f"Em dashes remaining: {em}")

# ── Save v4 ──────────────────────────────────────────────────────────────────
v4_path = os.path.join(os.path.dirname(__file__), "final_html_v4.html")
with open(v4_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Saved final_html_v4.html")

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
    correct_h3 = len(re.findall(r'<h3 style="color:#43627f;font-size:22px;">', rendered))
    wrong_h3   = len(re.findall(r'<h3><span style="font-weight: normal;">', rendered))
    em_live    = rendered.count("—") + rendered.count("&mdash;") + rendered.count("&#8212;")
    print(f"Live correct H3 (Thrive): {correct_h3}")
    print(f"Live wrong H3 (Elementor): {wrong_h3}")
    print(f"Live em dashes: {em_live}")
    print(f"Post status: {data.get('status')}")
    print("Done.")
else:
    print(f"Error: {resp.text[:400]}")
