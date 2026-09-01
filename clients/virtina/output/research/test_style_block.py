"""
Test: inject a <style> block at the top of post content with ::before pseudo-element
for TOC arrows. Add class to each TOC <li> and define ::before in the <style> block.
Thrive strips HTML elements inside <li>/<a>, but a top-level <style> block might survive.
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
MARKER = "VSTYLE99TEST"

# The SVG arrow as a URL-encoded data URI
SVG_URI = (
    "url(\"data:image/svg+xml,%3Csvg viewBox='0 0 24 24' width='18' height='18' "
    "xmlns='http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg'%3E"
    "%3Cpath fill='%2343627f' d='M4%2C11V13H16L10.5%2C18.5L11.92%2C19.92L19.84%2C12L11.92%2C4.08L10.5%2C5.5L16%2C11H4Z'%2F%3E"
    "%3C%2Fsvg%3E\")"
)

STYLE_BLOCK = f"""<style id="{MARKER}">
.vtoc-li {{
  background-image: {SVG_URI} !important;
  background-repeat: no-repeat !important;
  background-position: 0 8px !important;
  background-size: 18px 18px !important;
}}
.vtoc-li::before {{
  content: '' !important;
}}
</style>"""

# Fetch current content
r = requests.get(f"{WP}/posts/42202?context=edit", headers=h, verify=False, timeout=30)
content = r.json()["content"]["raw"]
print(f"DB content: {len(content)} chars")
print(f"style blocks present: {content.count('<style')}")

# Step 1: Add class 'vtoc-li' to each TOC <li>
toc_li_pattern = re.compile(
    r'<li\s+style="[^"]*padding[^"]*8px 0 8px 32px[^"]*"',
    re.DOTALL
)
matches = toc_li_pattern.findall(content)
print(f"TOC <li> items to add class to: {len(matches)}")

def add_class_to_li(m):
    tag = m.group(0)
    # Add class="vtoc-li" to the li tag
    return tag.replace('<li ', '<li class="vtoc-li" ', 1)

modified = toc_li_pattern.sub(add_class_to_li, content)
vtoc_count = modified.count('class="vtoc-li"')
print(f"vtoc-li class added: {vtoc_count} items")

# Step 2: Prepend <style> block to content
modified_with_style = STYLE_BLOCK + "\n" + modified
print(f"Style block added: {MARKER in modified_with_style}")

# PATCH
r_p = requests.patch(f"{WP}/posts/42202", json={"content": modified_with_style},
                     headers=hj, verify=False, timeout=60)
print(f"PATCH status: {r_p.status_code}")

# Check what WP stored — does it preserve <style> block?
r_check = requests.get(f"{WP}/posts/42202?context=edit", headers=h, verify=False, timeout=30)
stored = r_check.json()["content"]["raw"]
style_in_db = MARKER in stored
vtoc_in_db = 'class="vtoc-li"' in stored
print(f"In DB after PATCH: style_block={style_in_db}, vtoc-class={vtoc_in_db}")

if not style_in_db:
    print("WARNING: WordPress stripped <style> block — wp_kses is filtering it.")
    print("Cannot use <style> block approach with current user permissions.")
else:
    print("GOOD: <style> block survived WordPress wp_kses — checking live page...")
    print("Waiting 12s for Batcache...")
    time.sleep(12)

    r_live = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                          headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=30)
    style_live = MARKER in r_live.text
    vtoc_live = 'vtoc-li' in r_live.text
    bg_live = "background-image" in r_live.text
    cache = r_live.headers.get("X-nananana", "?")
    print(f"Live: style_block={style_live}, vtoc-class={vtoc_live}, background-image={bg_live}, cache={cache}")

    if style_live and vtoc_live:
        print("SUCCESS: Both <style> block and class survived Thrive Lightspeed!")
        if bg_live:
            print("background-image in live — ARROWS SHOULD BE VISIBLE!")
        else:
            print("WARNING: background-image in <style> block still stripped. Try ::before content approach.")
    else:
        if not style_live:
            print("FAIL: Thrive stripped the <style> block too.")
        if not vtoc_live:
            print("FAIL: Thrive stripped the vtoc-li class from <li>.")

# Restore (no style block, no class changes — restore original DB content)
print("\nRestoring original content (no style block, no vtoc-li class)...")
r_restore = requests.patch(f"{WP}/posts/42202", json={"content": content},
                           headers=hj, verify=False, timeout=60)
print(f"Restore status: {r_restore.status_code}")
