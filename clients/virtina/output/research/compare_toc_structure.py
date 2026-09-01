"""
Compare TOC item HTML between post 42177 (arrows work) and post 42202 (arrows missing).
Find the exact structural difference that makes Thrive preserve SVGs in 42177.
"""
import os, sys, requests, base64, urllib3, re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://virtina.com"
USERNAME = "anujith"
PASSWORD = os.environ.get("WP_REAL_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0"}

# Get both posts
print("=== Post 42177 (arrows WORK in live) ===")
r177 = requests.get(f"{SITE}/wp-json/wp/v2/posts/42177?context=edit",
                    headers=h, verify=False, timeout=20)
c177 = r177.json()["content"]["raw"]
toc177 = c177.find("Table of Contents")
li177 = c177.find("<li", toc177)
print(f"post_content length: {len(c177)}")
print(f"SVGs: {c177.count('fill:#43627f')}")
print(f"\nFirst TOC li (400 chars):\n{c177[li177:li177+400]}")

print("\n\n=== Post 42202 (arrows MISSING in live) ===")
r202 = requests.get(f"{SITE}/wp-json/wp/v2/posts/42202?context=edit",
                    headers=h, verify=False, timeout=20)
c202 = r202.json()["content"]["raw"]
toc202 = c202.find("Table of Contents")
li202 = c202.find("<li", toc202)
print(f"post_content length: {len(c202)}")
print(f"SVGs: {c202.count('fill:#43627f')}")
print(f"Arrows: {c202.count(chr(0x279C))}")
print(f"\nFirst TOC li (400 chars):\n{c202[li202:li202+400]}")

# Compare 200 chars BEFORE first <li> — what wraps the TOC list?
print("\n\n=== TOC container structure ===")
print("42177 TOC container (300 chars before first li):")
print(c177[max(0,li177-300):li177])
print("\n42202 TOC container (300 chars before first li):")
print(c202[max(0,li202-300):li202])

# Find the exact TOC element wrapper in both posts
print("\n\n=== TOC element attributes ===")
for label, content, toc_idx in [("42177", c177, toc177), ("42202", c202, toc202)]:
    # Find the containing element of Table of Contents text
    toc_text_pos = content.find("Table of Contents")
    # Go back to find the nearest opening tag
    search_start = max(0, toc_text_pos - 500)
    segment = content[search_start:toc_text_pos + 20]
    # Find data-* attributes and class names around the TOC
    data_attrs = re.findall(r'data-[\w-]+="[^"]*"', segment)
    classes = re.findall(r'class="[^"]*"', segment)
    print(f"\n{label} data-attrs near TOC: {data_attrs[:5]}")
    print(f"{label} classes near TOC: {classes[:5]}")
