"""Compare TOC structure between post 42177 (arrows work) and 42202 (arrows missing)."""
import os, sys, requests, base64, urllib3, re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://virtina.com"
USERNAME = "anujith"
PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0"}

print("=== Post 42177 (arrows WORK in live) ===")
r177 = requests.get(f"{SITE}/wp-json/wp/v2/posts/42177?context=edit", headers=h, verify=False, timeout=20)
c177 = r177.json()["content"]["raw"]
toc177 = c177.find("Table of Contents")
li177 = c177.find("<li", toc177)
print(f"Length: {len(c177)}, SVGs: {c177.count('fill:#43627f')}")
print("Container 400 chars before first <li>:")
print(repr(c177[max(0,li177-400):li177]))
print("First <li> (600 chars):")
print(repr(c177[li177:li177+600]))

print()
print("=== Post 42202 (arrows MISSING) ===")
r202 = requests.get(f"{SITE}/wp-json/wp/v2/posts/42202?context=edit", headers=h, verify=False, timeout=20)
c202 = r202.json()["content"]["raw"]
toc202 = c202.find("Table of Contents")
li202 = c202.find("<li", toc202)
print(f"Length: {len(c202)}, SVGs: {c202.count('fill:#43627f')}")
print("Container 400 chars before first <li>:")
print(repr(c202[max(0,li202-400):li202]))
print("First <li> (600 chars):")
print(repr(c202[li202:li202+600]))

# Also check data-* attributes near TOC
print()
print("=== data-* attrs near TOC ===")
for label, content, toc_pos in [("42177", c177, toc177), ("42202", c202, toc202)]:
    segment = content[max(0, toc_pos-800):toc_pos+50]
    data_attrs = re.findall(r'data-[\w-]+=["|\'][^"\']*["\']', segment)
    classes = re.findall(r'class="[^"]*toc[^"]*"', segment, re.I)
    print(f"{label} data-attrs: {data_attrs[:8]}")
    print(f"{label} toc classes: {classes[:5]}")
    # Find 'thrv' or 'tve' element wrapping TOC
    tve_tags = re.findall(r'<[a-z-]+[^>]*(?:thrv|tve|tcb)[^>]*>', segment, re.I)
    print(f"{label} tve/tcb elements: {tve_tags[:5]}")
    print()
