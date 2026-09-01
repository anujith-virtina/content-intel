"""Check published post slug vs our draft, and show full Image 1 HTML context."""
import os, re, requests, urllib3
from dotenv import load_dotenv

urllib3.disable_warnings()
load_dotenv()

auth = (os.getenv("WP_USERNAME"), os.getenv("WP_APP_PASSWORD"))

# 1. Find post by slug to confirm ID
resp = requests.get(
    "https://virtina.com/wp-json/wp/v2/posts?slug=woocommerce-b2b-net-payment-terms&context=edit",
    auth=auth, verify=False
)
posts = resp.json()
if posts:
    p = posts[0]
    print(f"Published post: ID={p['id']} status={p['status']}")
    raw = p.get("content", {}).get("raw", "")
    print(f"Raw chars: {len(raw)}")
else:
    print("No post found by slug")
    exit()

# 2. Show full Image 1 tag + surrounding 200 chars
m = re.search(r'<img[^>]*A-warehouse[^>]*>', raw, re.IGNORECASE)
if m:
    start = m.start()
    print("\n--- Image 1 full tag ---")
    print(m.group())
    print("\n--- 200 chars before ---")
    print(raw[max(0, start-200):start])
    print("\n--- 200 chars after ---")
    print(raw[m.end():m.end()+200])
else:
    print("A-warehouse image not found by slug search")
    # find all imgs
    for i, mg in enumerate(re.finditer(r'<img[^>]+>', raw, re.DOTALL), 1):
        src = re.search(r'src="([^"]+)"', mg.group())
        w = re.search(r'width="([^"]+)"', mg.group())
        h = re.search(r'height="([^"]+)"', mg.group())
        print(f"  Img {i}: {src.group(1)[-50:] if src else '?'} {w.group(1) if w else '?'}x{h.group(1) if h else '?'}")
