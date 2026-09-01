"""
Fix TOC order to match actual document section order.
Current TOC tail: ...before-you-go-live, common-mistakes, people-also-ask, conclusion, key-takeaways, faq
Correct TOC tail: ...before-you-go-live, key-takeaways, common-mistakes, people-also-ask, faq, conclusion
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

# Extract TOC <ul> block so we can rebuild it
toc_ul_pat = re.compile(
    r'(<ul style="list-style:none!important[^>]*>)(.*?)(</ul>)',
    re.DOTALL
)
m = toc_ul_pat.search(content)
if not m:
    print("MISS: TOC <ul> not found")
    exit(1)

ul_open  = m.group(1)
ul_inner = m.group(2)
ul_close = m.group(3)

# Extract each <li> and its anchor
li_pat = re.compile(r'(<li[^>]*>.*?href="(#[^"]+)".*?</li>)', re.DOTALL)
entries = li_pat.findall(ul_inner)  # list of (full_li_html, anchor)

print("Current TOC order:")
for i, (_, anchor) in enumerate(entries, 1):
    print(f"  {i:2}. {anchor}")

# Desired order matching actual document section order
desired_order = [
    "#why-woocommerce-loses-b2b-orders",
    "#what-are-net-payment-terms",
    "#how-much-revenue-are-you-losing",
    "#three-ways-to-add-net-terms",
    "#which-model-fits-manufacturers",
    "#real-world-scenarios",
    "#restrict-net-terms-approved-accounts",
    "#connect-to-erp-invoicing",
    "#what-happens-when-buyer-pays-late",
    "#before-you-go-live",
    "#key-takeaways",
    "#common-mistakes",
    "#people-also-ask",
    "#faq",
    "#conclusion",
]

# Build lookup: anchor -> li html
li_map = {anchor: li_html for li_html, anchor in entries}

# Warn if any anchor in desired_order is missing
for anchor in desired_order:
    if anchor not in li_map:
        print(f"  WARN: {anchor} not found in current TOC entries")

# Rebuild ul_inner in correct order
new_inner = "\n".join(li_map[a] for a in desired_order if a in li_map)
new_toc_ul = ul_open + "\n" + new_inner + "\n" + ul_close

content = content[:m.start()] + new_toc_ul + content[m.end():]

print("\nNew TOC order:")
for i, anchor in enumerate(desired_order, 1):
    print(f"  {i:2}. {anchor}")

# Verify
print("\n[VERIFY: TOC anchors match document sections]")
doc_sections = re.findall(r'<h2[^>]*\bid="([^"]+)"', content)
toc_anchors  = [a for _, a in li_pat.findall(new_inner)]

ok = True
for i, (toc_a, doc_a) in enumerate(zip(toc_anchors, ["#"+s for s in doc_sections]), 1):
    status = "OK" if toc_a == doc_a else "MISMATCH"
    if status == "MISMATCH":
        ok = False
    print(f"  {i:2}. TOC:{toc_a:45} DOC:{doc_a}")
if ok:
    print("  ALL MATCH")

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
