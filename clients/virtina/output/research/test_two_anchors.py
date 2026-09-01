"""
Test: use TWO <a> elements in each TOC <li> — one positioned arrow <a> + the text <a>.
Thrive strips <span> siblings but <a> is the whitelisted TOC element type.
Maybe two <a> elements both survive where a <span> does not.
"""
import os, sys, requests, base64, urllib3, re, time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}",
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
hj = {**h, "Content-Type": "application/json"}
SITE = "https://virtina.com"
WP = f"{SITE}/wp-json/wp/v2"
MARKER = "ARWANCH77"

# Fetch current content
r = requests.get(f"{WP}/posts/42202?context=edit", headers=h, verify=False, timeout=30)
content = r.json()["content"]["raw"]
print(f"DB: {len(content)} chars")

# Find first TOC <li> and its <a> tag — insert a sibling <a> styled as arrow BEFORE it
# Structure we want:
# <li style="...existing style...">
#   <a style="color:#43627f!important;position:absolute!important;left:0!important;top:8px!important;
#             font-size:18px!important;text-decoration:none!important;" href="#anchor">&#x279C;</a>
#   <a style="...existing style..." href="#anchor">Section Title</a>
# </li>
#
# Unicode arrows to try: → (→) ❯ (❯) ➤ (➤) ➜ (➜)
# Using a circle arrow: ➤ U+27A4

ARROW_CHAR = "&#x279C;"  # ➜ curved right arrow, close to the SVG arrow shape

toc_idx = content.find("Table of Contents")
print(f"TOC found at position: {toc_idx}")

# Pattern to find: <li style="...8px 0 8px 32px..."><a style="...#00a0e2..." href="#...">
toc_li_a_pattern = re.compile(
    r'(<li\s+style="[^"]*8px 0 8px 32px[^"]*"[^>]*>)'  # the <li> tag
    r'(<a\s+style="[^"]*#00a0e2[^"]*"\s+href="(#[^"]+)"[^>]*>)',  # the <a> opening
    re.DOTALL
)
matches = toc_li_a_pattern.findall(content)
print(f"TOC <li><a> pairs found: {len(matches)}")
if matches:
    print(f"First match href: {matches[0][2]}")

def insert_arrow_anchor(m):
    li_tag = m.group(1)
    a_tag = m.group(2)
    href = m.group(3)
    arrow_a = (
        f'<a style="color:#43627f!important;position:absolute!important;'
        f'left:0!important;top:4px!important;font-size:20px!important;'
        f'text-decoration:none!important;line-height:1!important;" href="{href}">'
        f'{ARROW_CHAR}</a>'
    )
    return li_tag + arrow_a + a_tag

# Only test on FIRST item first (diagnostic)
first_match = toc_li_a_pattern.search(content)
if first_match:
    test_content = content[:first_match.start(2)] + \
                   f'<a id="{MARKER}" style="color:#43627f!important;position:absolute!important;left:0!important;top:4px!important;font-size:20px!important;text-decoration:none!important;" href="{first_match.group(3)}">{ARROW_CHAR}</a>' + \
                   content[first_match.start(2):]
    print(f"Test: marker inserted = {MARKER in test_content}")

    r_p = requests.patch(f"{WP}/posts/42202", json={"content": test_content},
                         headers=hj, verify=False, timeout=60)
    print(f"PATCH: {r_p.status_code}")

    print("Waiting 12s for Batcache...")
    time.sleep(12)

    r_live = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                          headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
    found = MARKER in r_live.text
    cache = r_live.headers.get("X-nananana", "?")
    print(f"Live: arrow_anchor_found={found}, cache={cache}")

    if found:
        print("SUCCESS: Second <a> element survived Thrive! Applying to all TOC items...")
        idx = r_live.text.find(MARKER)
        print(f"Context: {r_live.text[idx-50:idx+150]}")
    else:
        print("FAIL: Thrive also strips sibling <a> elements.")
        # Show what the first TOC li looks like in live
        toc_start = r_live.text.find("Table of Contents")
        first_li = r_live.text.find("<li", toc_start)
        print(f"First live <li>: {r_live.text[first_li:first_li+300]}")

# Restore
print("\nRestoring original content...")
r_restore = requests.patch(f"{WP}/posts/42202", json={"content": content},
                           headers=hj, verify=False, timeout=60)
print(f"Restore: {r_restore.status_code}")
