"""Debug: compare live page vs stored content for both posts."""
import os, re, requests, base64, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WP_URL = "https://virtina.com/wp-json/wp/v2"
USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
api_h = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0"}
page_h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# Check post 42202 - 50 chars around the first TOC <li> in the live page
r_live = requests.get("https://virtina.com/woocommerce-b2b-customer-portal/",
                      headers=page_h, verify=False, timeout=30)
live_html = r_live.text
print("=== LIVE PAGE 42202 ===")
print(f"SVG count: {live_html.count('fill:#43627f')}")
toc_idx = live_html.find("Table of Contents")
if toc_idx >= 0:
    print("Live TOC snippet (400 chars):")
    print(live_html[toc_idx:toc_idx+400])

# Check raw DB content for 42202
r_api = requests.get(f"{WP_URL}/posts/42202?context=edit", headers=api_h, verify=False, timeout=30)
raw_42202 = r_api.json()["content"]["raw"]
print(f"\nDB raw SVG count: {raw_42202.count('fill:#43627f')}")

# Live page for 42177
r_live177 = requests.get("https://virtina.com/?p=42177", headers=page_h, verify=False, timeout=30)
live_html177 = r_live177.text
print("\n=== LIVE PAGE 42177 ===")
print(f"SVG count: {live_html177.count('fill:#43627f')}")
toc_idx177 = live_html177.find("Table of Contents")
if toc_idx177 >= 0:
    print("Live TOC snippet (400 chars):")
    print(live_html177[toc_idx177:toc_idx177+400])

# Check raw DB content for 42177
r_api177 = requests.get(f"{WP_URL}/posts/42177?context=edit", headers=api_h, verify=False, timeout=30)
raw_42177 = r_api177.json()["content"]["raw"]
print(f"\nDB raw SVG count: {raw_42177.count('fill:#43627f')}")
toc_idx_r = raw_42177.find("Table of Contents")
if toc_idx_r >= 0:
    print("Raw TOC snippet:")
    print(raw_42177[toc_idx_r:toc_idx_r+300])
