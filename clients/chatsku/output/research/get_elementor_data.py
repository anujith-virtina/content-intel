import os, requests, base64, urllib3, json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WP_URL = "https://chatsku.com/wp-json/wp/v2"
USERNAME = os.environ.get("CHATSKU_WP_USERNAME", "")
APP_PASSWORD = os.environ.get("CHATSKU_WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
h = {"Authorization": f"Basic {token}", "User-Agent": UA}

# Fetch with context=edit to get raw meta
r = requests.get(f"{WP_URL}/posts/216?context=edit", headers=h, verify=False, timeout=30)
post = r.json()
print(f"Status: {post.get('status')}")

meta = post.get("meta", {})
print(f"Meta keys: {list(meta.keys())}")

el_data = meta.get("_elementor_data", "")
print(f"_elementor_data length: {len(el_data)}")

if el_data:
    with open("elementor_data_216.json", "w", encoding="utf-8") as f:
        f.write(el_data)
    print("Saved elementor_data_216.json")
    # Parse and show section count
    try:
        sections = json.loads(el_data)
        print(f"Sections: {len(sections)}")
        for i, s in enumerate(sections):
            heading = ""
            for col in s.get("elements", []):
                for w in col.get("elements", []):
                    if w.get("widgetType") == "heading":
                        heading = w.get("settings", {}).get("title", "")[:60]
            print(f"  [{i}] id={s['id']} bg={s.get('settings',{}).get('background_color','')} heading={heading}")
    except Exception as e:
        print(f"Parse error: {e}")
