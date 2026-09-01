"""
Move warehouse image (Image 1) from white space between sections
into the 'why WooCommerce loses B2B orders' section box.
Also check and fix body2/body3 image placement.
Works on the PUBLISHED post_content (62329 chars).
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
print(f"Fetched: {len(raw)} chars, status={status}\n")

# Find the warehouse image block (the full <p><span>...<img>...</span></p>)
img_block_pat = re.compile(
    r'<p><span style="display: block; margin: 20px 0;">\s*'
    r'<img[^>]*A-warehouse[^>]*>\s*</span></p>',
    re.DOTALL
)
m_img = img_block_pat.search(raw)
if not m_img:
    print("MISS: warehouse image block not found")
    exit(1)

img_block = m_img.group()
img_pos   = m_img.start()
print(f"Found warehouse image block at char {img_pos}")
print(f"Context before: ...{raw[max(0,img_pos-100):img_pos][-80:]}")
print(f"Context after:  {raw[m_img.end():m_img.end()+100][:80]}...")

# The image is currently between the why-woocommerce section and next h2.
# Find the closing </div> of the why-woocommerce section that immediately precedes the image.
# The section div opened before the image — find the last </div> before the image
closing_div_pat = re.compile(r'</div>')
# Find all </div> occurrences before img_pos
closing_divs = list(closing_div_pat.finditer(raw[:img_pos]))
if not closing_divs:
    print("MISS: no closing </div> found before image")
    exit(1)

# The last </div> before the image is where the section closed
last_close = closing_divs[-1]
print(f"\nLast </div> before image at char {last_close.start()}: ...{raw[last_close.start()-30:last_close.end()+30]}...")

# Strategy: remove image block from current position,
# and insert it BEFORE the last </div> (i.e., inside the section)
# Remove image from current position
raw_no_img = raw[:m_img.start()] + raw[m_img.end():]

# Re-find the </div> position in the adjusted content
# (it's now at the same relative position since we removed content AFTER it)
new_close_pos = last_close.start()

# Insert image block before that </div>
raw_fixed = (
    raw_no_img[:new_close_pos]
    + '\n' + img_block + '\n'
    + raw_no_img[new_close_pos:]
)

print(f"\nFixed content: {len(raw_fixed)} chars")

# Verify placement
m_check = re.search(r'A-warehouse', raw_fixed)
if m_check:
    ctx = raw_fixed[max(0,m_check.start()-150):m_check.start()+100]
    print(f"\nImage new context: ...{ctx}...")

# Check all images now inside section boxes
print("\n[ALL IMAGE PLACEMENT CHECK]")
imgs_check = list(re.finditer(r'<img[^>]+wp-content/uploads[^>]+>', raw_fixed, re.DOTALL))
section_divs = list(re.finditer(
    r'<div[^>]*style="[^"]*(?:linear-gradient|background:#00d5c0)[^"]*"[^>]*>',
    raw_fixed
))
for i, m in enumerate(imgs_check, 1):
    pos = m.start()
    src = re.search(r'src="([^"]+)"', m.group())
    fname = src.group(1).split('/')[-1][:45] if src else '?'
    divs_before = [d for d in section_divs if d.start() < pos]
    if divs_before:
        last_div = divs_before[-1]
        chunk = raw_fixed[last_div.end():pos]
        opens  = len(re.findall(r'<div\b', chunk))
        closes = len(re.findall(r'</div>', chunk))
        inside = closes <= opens
    else:
        inside = False
    print(f"  Img {i}: {fname} — {'INSIDE box ✓' if inside else 'OUTSIDE box ✗'}")

resp2 = requests.put(
    "https://virtina.com/wp-json/wp/v2/posts/42297",
    auth=auth,
    json={"content": raw_fixed, "status": status}
)
print(f"\nHTTP {resp2.status_code}")
if resp2.status_code in (200, 201):
    print(f"Modified: {resp2.json().get('modified','')}")
    print("DONE")
else:
    print("ERROR:", resp2.text[:300])
