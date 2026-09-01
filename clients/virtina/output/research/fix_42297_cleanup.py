"""
Two removals:
1. Inline featured image at top of content (already shown by WP theme as featured image)
2. Author bio paragraph at the bottom
"""
import os, re, requests, urllib3
from dotenv import load_dotenv

urllib3.disable_warnings()
load_dotenv()

WP_BASE = "https://virtina.com"
WP_USER = os.getenv("WP_USERNAME")
WP_PASS = os.getenv("WP_APP_PASSWORD")
POST_ID = 42297

orig_put = requests.put
requests.put = lambda *a, **kw: orig_put(*a, **{**kw, "verify": False})

with open(r"C:\content-intel\clients\virtina\output\research\_42297_fixed.txt", encoding="utf-8") as f:
    content = f.read()
print(f"Loaded {len(content)} chars")

applied = 0

# FIX 1 — Remove inline featured image at top of content
# Pattern: <span style="display:block;..."><img ... featured-net-terms ... ></span>
img_pat = re.compile(
    r'<span style="display:block;[^"]*"><img[^>]*featured-net-terms[^>]*></span>\n*',
    re.DOTALL
)
new_content, n = img_pat.subn('', content, count=1)
if n:
    content = new_content
    print("  APPLIED: Inline featured image removed from top of content")
    applied += 1
else:
    print("  MISS: Inline featured image pattern not found")

# FIX 2 — Remove author bio paragraph
author_bio = '<p dir="ltr" style="font-size:16px;line-height:1.75;"><strong>The Virtina Team</strong> builds B2B ecommerce systems for manufacturers, distributors, and wholesalers on WooCommerce and Magento.</p>'
if author_bio in content:
    content = content.replace(author_bio, '', 1)
    print("  APPLIED: Author bio paragraph removed")
    applied += 1
else:
    print("  MISS: Author bio not found exactly — trying regex")
    bio_pat = re.compile(r'<p[^>]*><strong>The Virtina Team</strong>.*?</p>\n?', re.DOTALL)
    new_content, n = bio_pat.subn('', content, count=1)
    if n:
        content = new_content
        print("  APPLIED: Author bio removed (regex)")
        applied += 1
    else:
        print("  MISS: Author bio regex also failed")

print(f"\n{applied} fixes applied")

# Verify: check content starts with Summary div now
print("\n[TOP OF CONTENT CHECK]")
first_200 = content.strip()[:200]
print(f"  Starts with: {first_200[:100]}")
if content.strip().startswith('<div') and 'Summary' in content[:500]:
    print("  PASS: Content starts cleanly with Summary div")
else:
    print("  WARN: Check content start")

print("\n[AUTHOR BIO CHECK]")
print(f"  'Virtina Team' still present: {'Virtina Team' in content}")

print("\n[EM DASH]")
em = [i+1 for i, l in enumerate(content.split('\n')) if chr(0x2014) in l]
print(f"  {em if em else 'none'}")

with open(r"C:\content-intel\clients\virtina\output\research\_42297_fixed.txt", "w", encoding="utf-8") as f:
    f.write(content)
print(f"\nSaved ({len(content)} chars)")

print(f"PUTting to post {POST_ID}...")
resp = requests.put(
    f"{WP_BASE}/wp-json/wp/v2/posts/{POST_ID}",
    auth=(WP_USER, WP_PASS),
    json={"content": content, "status": "draft"}
)
print(f"HTTP {resp.status_code}")
if resp.status_code in (200, 201):
    print(f"Modified: {resp.json().get('modified', '')}")
    print("DONE")
else:
    print("ERROR:", resp.text[:400])
