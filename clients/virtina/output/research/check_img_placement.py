"""Check if each image is inside or outside a section div box."""
import os, re, requests, urllib3
from dotenv import load_dotenv

urllib3.disable_warnings()
load_dotenv()

resp = requests.get(
    "https://virtina.com/wp-json/wp/v2/posts/42297?context=edit",
    auth=(os.getenv("WP_USERNAME"), os.getenv("WP_APP_PASSWORD")),
    verify=False
)
raw = resp.json()["content"]["raw"]

imgs = list(re.finditer(r'<img[^>]+>', raw, re.DOTALL))

for i, m in enumerate(imgs, 1):
    tag = m.group()
    pos = m.start()

    src = re.search(r'src="([^"]+)"', tag)
    w   = re.search(r'width="([^"]+)"', tag)
    h   = re.search(r'height="([^"]+)"', tag)

    # Look backward for the most recent opening <div style="..."> and count unclosed divs
    before = raw[:pos]
    # Find last section div (background gradient)
    open_section_divs = [x for x in re.finditer(
        r'<div style="background:[^"]*(?:linear-gradient|#00d5c0)[^"]*"', before
    )]
    # Count closing </div> tags after the last section div open
    last_open = open_section_divs[-1] if open_section_divs else None

    if last_open:
        between = raw[last_open.end():pos]
        opens  = len(re.findall(r'<div\b', between))
        closes = len(re.findall(r'</div>', between))
        inside = closes <= opens  # more opens than closes = still inside the div
    else:
        inside = False

    # Also show 80 chars before the image's parent <span> or <p>
    snippet_before = raw[max(0, pos-150):pos].strip()[-100:]
    snippet_after  = raw[m.end():m.end()+80].strip()[:80]

    fname = src.group(1).split('/')[-1] if src else '?'
    print(f"Image {i}: {fname}")
    print(f"  Size   : {w.group(1) if w else '?'} x {h.group(1) if h else '?'}")
    print(f"  Inside section box: {inside}")
    print(f"  Before : ...{snippet_before}")
    print(f"  After  : {snippet_after}...")
    print()
