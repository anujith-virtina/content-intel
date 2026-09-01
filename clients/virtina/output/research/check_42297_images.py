"""Fetch post 42297 rendered content and extract all image tags with context."""
import os, re, requests, urllib3
from dotenv import load_dotenv

urllib3.disable_warnings()
load_dotenv()

resp = requests.get(
    "https://virtina.com/wp-json/wp/v2/posts/42297?context=edit",
    auth=(os.getenv("WP_USERNAME"), os.getenv("WP_APP_PASSWORD")),
    verify=False
)
d = resp.json()
raw = d.get("content", {}).get("raw", "")
print(f"raw chars: {len(raw)}\n")

# Find every <img> tag and show 120 chars of surrounding context
imgs = list(re.finditer(r'<img[^>]+>', raw, re.DOTALL))
print(f"Total images found: {len(imgs)}\n")

for i, m in enumerate(imgs, 1):
    tag = m.group()
    start = m.start()

    # Extract key attrs
    src   = (re.search(r'\bsrc="([^"]+)"', tag) or re.search(r"\bsrc='([^']+)'", tag))
    alt   = re.search(r'\balt="([^"]*)"', tag)
    w     = re.search(r'\bwidth="([^"]+)"', tag)
    h     = re.search(r'\bheight="([^"]+)"', tag)
    style = re.search(r'\bstyle="([^"]+)"', tag)

    # 80 chars before the tag for context
    before = raw[max(0, start-120):start]
    # What wraps this image — look for parent div style
    parent_div = re.search(r'<div[^>]*style="([^"]*)"[^>]*>\s*(?:<[^>]+>\s*)*$', before)

    print(f"--- Image {i} ---")
    print(f"  src   : {src.group(1)[-60:] if src else 'N/A'}")
    print(f"  alt   : {(alt.group(1)[:80] if alt else 'N/A')}")
    print(f"  size  : {w.group(1) if w else '?'} x {h.group(1) if h else '?'}")
    print(f"  style : {style.group(1)[:80] if style else 'none'}")
    if parent_div:
        print(f"  parent: {parent_div.group(1)[:80]}")
    print()
