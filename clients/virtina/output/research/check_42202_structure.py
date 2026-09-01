"""Show the exact HTML structure around images in reference post 42202."""
import os, re, requests, urllib3
from dotenv import load_dotenv
urllib3.disable_warnings()
load_dotenv()

auth = (os.getenv("WP_USERNAME"), os.getenv("WP_APP_PASSWORD"))

r = requests.get(
    "https://virtina.com/wp-json/wp/v2/posts/42202?context=edit",
    auth=auth, verify=False
)
raw = r.json()["content"]["raw"]
print(f"Post 42202 raw: {len(raw)} chars\n")

# Find every image and show 400 chars before + 100 after
imgs = list(re.finditer(r'<img[^>]+>', raw, re.DOTALL))
print(f"Total images: {len(imgs)}\n")

for i, m in enumerate(imgs, 1):
    tag = m.group()
    pos = m.start()
    src = re.search(r'src="([^"]+)"', tag)
    w   = re.search(r'width="([^"]+)"', tag)
    h   = re.search(r'height="([^"]+)"', tag)
    fname = src.group(1).split('/')[-1][:60] if src else '?'

    before = raw[max(0, pos-500):pos]
    after  = raw[m.end():m.end()+200]

    # find last div opening before this image
    div_opens = list(re.finditer(r'<div[^>]*>', before))
    last_div = div_opens[-1].group()[:120] if div_opens else 'none'

    print(f"--- Image {i}: {fname} [{w.group(1) if w else '?'}x{h.group(1) if h else '?'}] ---")
    print(f"  Last <div> before img: {last_div}")
    print(f"  400 chars before:")
    print(f"  {before[-400:].replace(chr(10),' ')}")
    print(f"  100 chars after:")
    print(f"  {after[:100].replace(chr(10),' ')}")
    print()
