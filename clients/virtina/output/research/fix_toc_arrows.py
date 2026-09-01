"""Re-insert SVG arrow spans into TOC list items for Virtina post 42202."""
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

# Fetch current content
r = requests.get(f"{WP_URL}/posts/{POST_ID}?context=edit", headers=h, verify=False, timeout=30)
post = r.json()
print(f"Status: {post.get('status')}, content length: {len(post['content'].get('raw',''))}")
content = post["content"]["raw"]

SVG_SPAN = (
    '<span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;">'
    '<svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/>'
    '</svg></span>'
)

# Match TOC <li> items that have padding:8px 0 8px 32px but no SVG yet
# Insert SVG span between the <li ...> tag and the <a href=...>
before = content.count("fill:#43627f")
print(f"SVG arrows currently in content: {before}")

# Pattern: <li with 32px padding> immediately followed by <a (no span in between)
pattern = re.compile(
    r'(<li[^>]*?padding:\s*8px 0 8px 32px[^>]*?>)(<a\s)',
    re.DOTALL
)
fixed = pattern.sub(rf'\1{SVG_SPAN}\2', content)

after = fixed.count("fill:#43627f")
print(f"SVG arrows after fix: {after}")
changes = after - before
print(f"Changes made: {changes}")

if changes == 0:
    print("Nothing to fix — already correct or pattern mismatch.")
    raise SystemExit(0)

# PATCH
resp = requests.patch(
    f"{WP_URL}/posts/{POST_ID}",
    json={"content": fixed},
    headers=h, verify=False, timeout=60,
)
print(f"PATCH status: {resp.status_code}")
if resp.status_code == 200:
    rendered = resp.json()["content"]["rendered"]
    count = rendered.count("fill:#43627f")
    print(f"SVG arrows confirmed in rendered output: {count}")
    print("Done.")
else:
    print(f"Error: {resp.text[:400]}")
