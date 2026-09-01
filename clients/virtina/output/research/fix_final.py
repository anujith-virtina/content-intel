"""Copy EXACT TOC structure from working post to 42202, then clear caches."""
import os, sys, requests, urllib3, re, time, base64, json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://virtina.com"
USERNAME = "anujith"
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
REAL_PASSWORD = os.environ.get("WP_REAL_PASSWORD", "")

token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h_api = {"Authorization": f"Basic {token}", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

# Step 1: Get the LIVE HTML of the working post
print("=== Fetching working TOC from humans-and-ai-in-marketing ===")
r_ref = requests.get(f"{SITE}/humans-and-ai-in-marketing/",
                     headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=20)
toc_ref = r_ref.text.find("Table of Contents")
if toc_ref < 0:
    print("No TOC found on reference page - checking raw source")
    print(r_ref.text[r_ref.text.find("<ul"):r_ref.text.find("<ul")+200])
else:
    li_ref = r_ref.text.find("<li", toc_ref)
    print("Reference page LIVE TOC first li:")
    print(r_ref.text[li_ref:li_ref+500])
    print(f"SVGs in ref page: {r_ref.text.count('fill:#43627f')}")

# Step 2: Get the DB post_content of the reference post (humans-and-ai-in-marketing)
# First find its post ID from the REST API
r_search = requests.get(f"{SITE}/wp-json/wp/v2/posts?slug=humans-and-ai-in-marketing&context=edit",
                        headers=h_api, verify=False, timeout=15)
ref_posts = r_search.json()
if ref_posts:
    ref_post = ref_posts[0]
    ref_id = ref_post['id']
    ref_content = ref_post['content']['raw']
    ref_toc = ref_content.find("Table of Contents")
    ref_li = ref_content.find("<li", ref_toc)
    print(f"\nRef post ID: {ref_id}")
    print(f"Ref DB first li (400 chars):")
    print(repr(ref_content[ref_li:ref_li+400]))
    print(f"Ref DB SVGs: {ref_content.count('fill:#43627f')}")

    # Extract the SVG span from the ref post
    svg_match = re.search(r'<span[^>]*aria-hidden[^>]*>.*?</span>', ref_content[ref_li:ref_li+400], re.S)
    if svg_match:
        svg_span = svg_match.group(0)
        print(f"\nExtracted SVG span: {svg_span}")
    else:
        # Build the SVG span from post 42177 which we know works
        svg_span = '<span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span>'
        print(f"\nUsing post 42177 SVG span")
else:
    print("Could not find ref post")
    svg_span = '<span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span>'

# Step 3: Get current post 42202 content
print("\n=== Current post 42202 DB content ===")
r202 = requests.get(f"{SITE}/wp-json/wp/v2/posts/42202?context=edit", headers=h_api, verify=False, timeout=15)
c202 = r202.json()["content"]["raw"]
toc202 = c202.find("Table of Contents")
li202 = c202.find("<li", toc202)
print(f"Length: {len(c202)}, SVGs: {c202.count('fill:#43627f')}")
print(f"Current first li: {repr(c202[li202:li202+300])}")

# Step 4: Fix the TOC - restore SVG spans and fix styling to match post 42177 exactly
print("\n=== Rebuilding TOC items ===")
# The current <li> structure (from apply_unicode_arrows.py changes):
# <li style="list-style: none!important; padding: 8px 0 8px 8px!important; position: relative!important; ...">
# <a style="color: #43627f!important; ...">➜ text</a></li>
#
# Target structure (matching post 42177 exactly):
# <li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;">
# <span aria-hidden="true" style="..."><svg .../></span>
# <a style="color:#00a0e2!important;..." href="...">text</a></li>

new_content = c202

# Fix: restore padding to 32px and color to #00a0e2, remove unicode arrow, add SVG span
def fix_li(m):
    li_html = m.group(0)
    # Fix padding: 8px 0 8px 8px -> 8px 0 8px 32px (with or without spaces)
    li_html = re.sub(r'padding:\s*8px 0 8px 8px', 'padding:8px 0 8px 32px', li_html)
    # Fix color: #43627f -> #00a0e2
    li_html = re.sub(r'color:\s*#43627f', 'color:#00a0e2', li_html)
    # Remove spaces after colons in <li> style (match post 42177 format)
    # Remove unicode arrow from anchor text
    li_html = li_html.replace('➜\xa0', '').replace('➜ ', '').replace('➜', '')
    # Add SVG span after <li ...>  (before the <a> tag)
    li_html = re.sub(r'(<li[^>]*>)\s*(<a)', r'\1' + svg_span + r'\2', li_html)
    return li_html

# Apply to all <li>...</li> items in the TOC section
toc_start = new_content.find("Table of Contents")
toc_end = new_content.find("</ul>", toc_start) + 5
toc_section = new_content[toc_start:toc_end]
fixed_section = re.sub(r'<li[^>]*>.*?</li>', fix_li, toc_section, flags=re.S)
new_content = new_content[:toc_start] + fixed_section + new_content[toc_end:]

# Also fix the <h3> to have proper style matching post 42177
new_content = new_content.replace(
    '<h3>Table of Contents</h3>',
    '<h3 style="color:#43627f;font-size:22px;">Table of Contents</h3>'
)

print(f"New content: {len(new_content)} chars, SVGs: {new_content.count('fill:#43627f')}")
toc_new = new_content.find("Table of Contents")
li_new = new_content.find("<li", toc_new)
print(f"New first li: {repr(new_content[li_new:li_new+500])}")

# Step 5: Push to DB
print("\n=== Pushing to DB ===")
r_push = requests.post(f"{SITE}/wp-json/wp/v2/posts/42202",
    json={"content": new_content, "status": "publish"},
    headers=h_api, verify=False, timeout=30)
print(f"Push: {r_push.status_code}")
if r_push.status_code == 200:
    pushed = r_push.json()["content"]["raw"]
    toc_p = pushed.find("Table of Contents")
    li_p = pushed.find("<li", toc_p)
    print(f"Pushed SVGs: {pushed.count('fill:#43627f')}")
    print(f"Pushed first li: {repr(pushed[li_p:li_p+300])}")
else:
    print(f"Error: {r_push.text[:200]}")
    sys.exit(1)

# Step 6: Save via admin to trigger all cache hooks (including Batcache invalidation)
print("\n=== Admin save to trigger Batcache invalidation ===")
session = requests.Session()
session.verify = False
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
session.get(f"{SITE}/wp-login.php", timeout=15)
session.post(f"{SITE}/wp-login.php", data={
    "log": USERNAME, "pwd": REAL_PASSWORD, "wp-submit": "Log In",
    "redirect_to": f"{SITE}/wp-admin/", "testcookie": "1",
}, allow_redirects=True, timeout=20)
logged_in = any("logged_in" in k for k in session.cookies.keys())
print(f"Logged in: {logged_in}")

# Get the post edit page to extract the full form state + current content
r_edit = session.get(f"{SITE}/wp-admin/post.php?post=42202&action=edit", timeout=20)
wp_nonce_m = re.search(r'name="_wpnonce"[^>]*value="([^"]+)"', r_edit.text)

if wp_nonce_m:
    wp_nonce = wp_nonce_m.group(1)
    # Extract existing form fields we need to preserve
    post_title_m = re.search(r'id="title"[^>]*value="([^"]*)"', r_edit.text)
    post_title = post_title_m.group(1) if post_title_m else "Does your WooCommerce store have a B2B customer portal, or just an account page?"

    form_data = {
        "_wpnonce": wp_nonce,
        "action": "editpost",
        "post_type": "post",
        "post_ID": "42202",
        "originalaction": "editpost",
        "post_author": "1",
        "post_status": "publish",
        "comment_status": "open",
        "ping_status": "closed",
        "save": "Update",
        "post_title": post_title,
        # Include the updated post_content
        "post_content": new_content,
    }
    r_admin_save = session.post(f"{SITE}/wp-admin/post.php",
                                data=form_data, allow_redirects=True, timeout=30)
    print(f"Admin save: {r_admin_save.status_code} -> {r_admin_save.url}")

# Also purge Pressable edge cache
press_page = session.get(f"{SITE}/wp-admin/admin.php?page=pressable_cache_management", timeout=15)
press_nonce = re.search(r'"nonce"\s*:\s*"([a-f0-9]+)"', press_page.text)
if press_nonce:
    rp = session.post(f"{SITE}/wp-admin/admin-ajax.php", data={
        "action": "pressable_edge_cache_purge", "nonce": press_nonce.group(1)
    }, timeout=15)
    print(f"Edge cache purge: {rp.text[:60]}")

# Also try to hit the live page AS ADMIN to force Batcache to regenerate
print("\nHitting live page as admin to warm Batcache with new content...")
r_warm = session.get(f"{SITE}/woocommerce-b2b-customer-portal/", timeout=20)
toc_w = r_warm.text.find("Table of Contents")
li_w = r_warm.text.find("<li", toc_w)
print(f"Admin render: {r_warm.headers.get('X-nananana', 'none')}")
print(f"Admin render first li: {r_warm.text[li_w:li_w+300]}")

print("\nWaiting 8s...")
time.sleep(8)

# Step 7: Final check
print("\n=== FINAL LIVE CHECK ===")
for i in range(3):
    r = requests.get(f"{SITE}/woocommerce-b2b-customer-portal/",
                     headers={"User-Agent": f"Mozilla/5.0 (final-check-{i})"}, verify=False, timeout=30)
    cache = r.headers.get("X-nananana", r.headers.get("X-Cache", "none"))
    toc_f = r.text.find("Table of Contents")
    li_f = r.text.find("<li", toc_f)
    li_html = r.text[li_f:li_f+400]
    svg_count = r.text.count("fill:#43627f")
    arrow_count = r.text.count(chr(0x279C))
    pad_m = re.search(r'padding:\s*([^;!"]+)[;!]', li_html)
    print(f"[{i+1}] cache={cache}, svg={svg_count}, arrows={arrow_count}, padding={pad_m.group(1) if pad_m else '?'}")
    if svg_count > 0:
        print(f"  SUCCESS! First li: {li_html[:200]}")
    time.sleep(1)
