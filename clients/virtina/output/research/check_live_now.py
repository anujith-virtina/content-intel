"""Check current live state of post 42202 and the actual rendered TOC HTML."""
import os, sys, requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://virtina.com"

r = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                 headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
                 verify=False, timeout=30)

print(f"Status: {r.status_code}")
print(f"Cache: {r.headers.get('X-nananana', r.headers.get('X-Cache', '?'))}")
print(f"SVGs (fill:#43627f): {r.text.count('fill:#43627f')}")
print(f"Unicode arrow (➜): {r.text.count(chr(0x279C))}")
print(f"Color #00a0e2: {r.text.count('#00a0e2')}")
print(f"Color #43627f: {r.text.count('#43627f')}")

toc = r.text.find("Table of Contents")
if toc >= 0:
    li = r.text.find("<li", toc)
    print(f"\nFirst rendered TOC li (500 chars):")
    print(r.text[li:li+500])
    # Show all li items
    pos = li
    count = 0
    while pos >= 0 and count < 15:
        end = r.text.find("</li>", pos) + 5
        item = r.text[pos:end]
        # Extract just anchor text
        import re
        atxt = re.findall(r'<a[^>]*>(.*?)</a>', item, re.S)
        print(f"  li {count+1}: {atxt}")
        pos = r.text.find("<li", end)
        count += 1
else:
    print("No 'Table of Contents' found in rendered HTML")
    # Search for any toc-like content
    idx = r.text.find("toc")
    print(f"'toc' at: {idx}")
