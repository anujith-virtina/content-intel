"""
Wrap the warehouse image (Image 1) in a colored section div
so it appears inside a box on the live page, matching reference post 42202.
"""
import os, re, requests, urllib3
from dotenv import load_dotenv
urllib3.disable_warnings()
load_dotenv()

auth = (os.getenv("WP_USERNAME"), os.getenv("WP_APP_PASSWORD"))
orig_put = requests.put
requests.put = lambda *a, **kw: orig_put(*a, **{**kw, "verify": False})
orig_get = requests.get
requests.get = lambda *a, **kw: orig_get(*a, **{**kw, "verify": False})

resp = requests.get("https://virtina.com/wp-json/wp/v2/posts/42297?context=edit", auth=auth)
d = resp.json()
raw = d["content"]["raw"]
status = d["status"]
print(f"Fetched: {len(raw)} chars, status={status}")

# The warehouse image block to wrap
img_block_pat = re.compile(
    r'<p><span style="display: block; margin: 20px 0;">\s*<img[^>]*A-warehouse[^>]*>\s*</span></p>',
    re.DOTALL
)
m = img_block_pat.search(raw)
if not m:
    print("MISS: warehouse image block not found")
    exit(1)

old_block = m.group()
print(f"Found image block at char {m.start()}")

# Wrap it in a styled div matching Virtina section box style
new_block = (
    '<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));'
    'border-radius:20px;padding:20px;margin:0 0 28px 0;">\n'
    + old_block + '\n'
    '</div>'
)

raw = raw.replace(old_block, new_block, 1)
print("  APPLIED: Warehouse image wrapped in colored section div")

# Verify
print("\n[VERIFY]")
print(f"  'A-warehouse' in div box: {'linear-gradient' in raw[raw.find('A-warehouse')-200:raw.find('A-warehouse')]}")

resp2 = requests.put(
    "https://virtina.com/wp-json/wp/v2/posts/42297",
    auth=auth,
    json={"content": raw, "status": status}
)
print(f"\nHTTP {resp2.status_code}")
if resp2.status_code in (200, 201):
    print(f"Modified: {resp2.json().get('modified','')}")
    print("DONE — hard refresh the live page to verify")
else:
    print("ERROR:", resp2.text[:300])
