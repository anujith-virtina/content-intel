"""Fix TOC arrows - patch and immediately re-read to verify persistence."""
import os, re, requests, base64, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WP_URL = "https://virtina.com/wp-json/wp/v2"
USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}",
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
     "Content-Type": "application/json"}

POST_ID = 42202

SVG_SPAN = (
    '<span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;">'
    '<svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/>'
    '</svg></span>'
)

# Fetch current content
r = requests.get(f"{WP_URL}/posts/{POST_ID}?context=edit", headers=h, verify=False, timeout=30)
post = r.json()
content = post["content"]["raw"]
print(f"Fetched raw content length: {len(content)}")
print(f"SVG count before: {content.count('fill:#43627f')}")

# Show exact TOC li structure for diagnosis
toc_idx = content.find("Table of Contents")
if toc_idx >= 0:
    snippet = content[toc_idx:toc_idx+300]
    print(f"\nTOC snippet:\n{snippet}\n")

# Insert SVG spans
pattern = re.compile(
    r'(<li[^>]*?padding[^>]*?32px[^>]*?>)(<a)',
    re.DOTALL
)
fixed = pattern.sub(r'\g<1>' + SVG_SPAN + r'\g<2>', content)
print(f"SVG count after regex: {fixed.count('fill:#43627f')}")

if fixed == content:
    print("WARNING: No changes made — regex did not match")
    raise SystemExit(1)

# Show what the patched TOC looks like
toc_idx2 = fixed.find("Table of Contents")
if toc_idx2 >= 0:
    print(f"\nPatched TOC snippet:\n{fixed[toc_idx2:toc_idx2+400]}\n")

# PATCH
print("Sending PATCH...")
resp = requests.patch(
    f"{WP_URL}/posts/{POST_ID}",
    json={"content": fixed},
    headers=h, verify=False, timeout=60,
)
print(f"PATCH status: {resp.status_code}")
if resp.status_code != 200:
    print(f"Error: {resp.text[:400]}")
    raise SystemExit(1)

patch_response_rendered = resp.json()["content"]["rendered"]
print(f"Rendered in PATCH response - SVG count: {patch_response_rendered.count('fill:#43627f')}")

# Immediately re-read raw content
import time
time.sleep(2)
r2 = requests.get(f"{WP_URL}/posts/{POST_ID}?context=edit", headers=h, verify=False, timeout=30)
post2 = r2.json()
raw2 = post2["content"]["raw"]
print(f"\nRe-read raw content length: {len(raw2)}")
print(f"SVG count in re-read raw: {raw2.count('fill:#43627f')}")

toc3 = raw2.find("Table of Contents")
if toc3 >= 0:
    print(f"Re-read TOC snippet:\n{raw2[toc3:toc3+400]}")
