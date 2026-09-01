"""Check if arrows appear in TOC section of live page."""
import requests, urllib3, re, sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

r = requests.get("https://virtina.com/woocommerce-b2b-customer-portal/",
                 headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)

print(f"Cache: {r.headers.get('X-nananana', 'none')}")
print(f"Page length: {len(r.text)}")
print(f"tcb-icon count: {r.text.count('tcb-icon')}")
print(f"fill:#43627f: {r.text.count('fill:#43627f')}")
print(f"thrv-styled-list-item: {r.text.count('thrv-styled-list-item')}")

# Find Table of Contents section and show 2000 chars
toc = r.text.find("Table of Contents")
if toc >= 0:
    print(f"\n=== TOC section (2000 chars) ===")
    # Show from h3 backwards to find its start
    h3_start = r.text.rfind("<h3", 0, toc)
    toc_end = r.text.find("</ul>", toc)
    print(r.text[h3_start:toc_end+5])
else:
    print("No TOC found")

# Also show where tcb-icon first appears
idx = r.text.find("tcb-icon")
if idx >= 0:
    print(f"\nFirst tcb-icon context (200 chars before, 100 after):")
    print(r.text[max(0,idx-200):idx+100])

# Check the first 3 TOC items
print("\n=== First 3 TOC list items ===")
toc = r.text.find("Table of Contents")
pos = r.text.find("<li", toc)
for i in range(3):
    end = r.text.find("</li>", pos) + 5
    print(f"LI {i+1}:")
    print(r.text[pos:end])
    print()
    pos = r.text.find("<li", end)
    if pos < 0:
        break
