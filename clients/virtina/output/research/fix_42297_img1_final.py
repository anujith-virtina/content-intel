"""
Final fix for warehouse image:
1. Correct size to 670x352
2. Add max-width:100% so it never overflows its container
3. Keep the div box wrapper already in place
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
raw = resp.json()["content"]["raw"]
status = resp.json()["status"]
print(f"Fetched: {len(raw)} chars, status={status}")

# Fix the image tag: 860x452 with no style → 670x352 with max-width:100%
old_img = '<img src="https://virtina.com/wp-content/uploads/2026/05/A-warehouse.jpg" alt="Warehouse employee reviewing and signing a purchase order beside a desktop computer displaying an online checkout/order management screen in a large warehouse setting with shelves and inventory in the background." width="860" height="452">'

new_img = '<img src="https://virtina.com/wp-content/uploads/2026/05/A-warehouse.jpg" alt="Warehouse employee reviewing and signing a purchase order beside a desktop computer displaying an online checkout/order management screen in a large warehouse setting with shelves and inventory in the background." width="670" height="352" style="aspect-ratio: auto 670 / 352; max-width:100%; display:block;">'

if old_img in raw:
    raw = raw.replace(old_img, new_img, 1)
    print("  APPLIED: warehouse image 860x452 -> 670x352 + max-width:100%")
else:
    # Regex fallback
    pat = re.compile(r'(<img[^>]*A-warehouse[^>]*)width="860"([^>]*)height="452"([^>]*)>', re.DOTALL)
    def fix(m):
        tag = m.group(0)
        tag = re.sub(r'width="\d+"', 'width="670"', tag)
        tag = re.sub(r'height="\d+"', 'height="352"', tag)
        if 'style=' not in tag:
            tag = tag.rstrip('>')
            tag += ' style="aspect-ratio: auto 670 / 352; max-width:100%; display:block;">'
        return tag
    raw, n = pat.subn(fix, raw, count=1)
    if n:
        print(f"  APPLIED: warehouse image fixed (regex)")
    else:
        print("  MISS: image not found — check manually")
        exit(1)

# Confirm div box is still wrapping it
idx = raw.find('A-warehouse')
context = raw[max(0, idx-250):idx+50]
in_box = 'linear-gradient' in context
print(f"  Still inside div box: {in_box}")

# Final check all body images
print("\n[ALL IMAGES]")
for i, m in enumerate(re.finditer(r'<img[^>]*wp-content/uploads[^>]+>', raw, re.DOTALL), 1):
    tag = m.group()
    src = re.search(r'src="([^"]+)"', tag)
    w   = re.search(r'width="([^"]+)"', tag)
    h   = re.search(r'height="([^"]+)"', tag)
    sty = 'max-width' in tag
    fname = src.group(1).split('/')[-1][:45] if src else '?'
    print(f"  {i}. {fname} | {w.group(1) if w else '?'}x{h.group(1) if h else '?'} | max-width: {'OK' if sty else 'MISSING'}")

resp2 = requests.put(
    "https://virtina.com/wp-json/wp/v2/posts/42297",
    auth=auth,
    json={"content": raw, "status": status}
)
print(f"\nHTTP {resp2.status_code}")
if resp2.status_code in (200, 201):
    print(f"Modified: {resp2.json().get('modified','')}")
    print("DONE")
else:
    print("ERROR:", resp2.text[:300])
