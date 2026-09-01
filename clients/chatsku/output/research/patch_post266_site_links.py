"""
Patch post 266: add 5 internal links from newly discovered chatsku.com pages/posts.

Links added:
  Intro   → /response-gap/                       (48-hour sales rep delay)
  Q1      → /b2b-catalog-issues-costing-sales/   (cost of the conversion gap)
  Q3      → /passive-catalog/                    (catalog shows products, can't close)
  Q7      → /ai-sales-assistant-b2b-ecommerce/   (what the conversational layer is)
  Q8      → /revenue-calculator                  (model the ROI math)
"""

import json, urllib.request, urllib.error, base64, os, ssl, sys, re

_ssl_ctx = ssl._create_unverified_context()

_env_path = r"C:\content-intel\.env"
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

WP_BASE  = "https://chatsku.com/wp-json/wp/v2"
UA       = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
USERNAME = os.environ.get("CHATSKU_WP_USERNAME", "")
PASSWORD = os.environ.get("CHATSKU_WP_APP_PASSWORD", "")
if not USERNAME or not PASSWORD:
    print("ERROR: credentials not set"); sys.exit(1)

AUTH    = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
HEADERS = {"Authorization": f"Basic {AUTH}", "User-Agent": UA,
           "Content-Type": "application/json"}
POST_ID = 266

REPLACEMENTS = [
    # 1. Introduction — name the 48-hour delay as the response gap
    (
        "The sale stalls for 48 hours. The buyer may or may not come back.",
        'The sale stalls for 48 hours. That window has a name: '
        '<a href="https://chatsku.com/response-gap/">the response gap</a>. '
        'The buyer may or may not come back.'
    ),
    # 2. Q1 — link to the catalog-costs-money post after the revenue math
    (
        "It's a revenue decision you're making every month. AI search buyers often expect",
        'It\'s a revenue decision you\'re making every month. For a deeper look at what that gap costs, '
        'see <a href="https://chatsku.com/b2b-catalog-issues-costing-sales/">'
        'how much your B2B catalog is costing you</a>. '
        'AI search buyers often expect'
    ),
    # 3. Q3 opening — link to passive catalog problem page
    (
        "<p>The buyer found the product. So why is the cart empty?</p>",
        '<p>The buyer found the product. So why is the cart empty? '
        'This is <a href="https://chatsku.com/passive-catalog/">the passive catalog problem</a>: '
        'the catalog shows what is available but cannot close the sale.</p>'
    ),
    # 4. Q7 — link to AI sales assistant page in architecture summary
    (
        "The conversational layer handles the buying conversation.",
        'ChatSKU\'s <a href="https://chatsku.com/ai-sales-assistant-b2b-ecommerce/">'
        'B2B AI sales assistant</a> handles the buying conversation.'
    ),
    # 5. Q8 checklist item 3 — add revenue calculator link alongside pricing link
    (
        'You can <a href="https://chatsku.com/pricing/">check ChatSKU\'s pricing</a> '
        'to run that math directly.',
        'You can <a href="https://chatsku.com/revenue-calculator">model the impact with the '
        'revenue calculator</a> or <a href="https://chatsku.com/pricing/">check ChatSKU\'s pricing</a> '
        'to run that math directly.'
    ),
]

# ── Fetch post ─────────────────────────────────────────────────────────────────
print(f"Fetching post {POST_ID}...")
req = urllib.request.Request(f"{WP_BASE}/posts/{POST_ID}?context=edit", headers=HEADERS)
with urllib.request.urlopen(req, context=_ssl_ctx, timeout=30) as r:
    post = json.loads(r.read())
print(f"  Status: {post['status']}  Title: {post['title']['raw'][:60]}")

elementor_str = post.get("meta", {}).get("_elementor_data", "")
if not elementor_str:
    print("ERROR: _elementor_data not found"); sys.exit(1)

elementor_sections = json.loads(elementor_str)
print(f"  Sections: {len(elementor_sections)}")

# ── Apply patches ──────────────────────────────────────────────────────────────
applied = []

def walk_and_patch(elements):
    for el in elements:
        if el.get("widgetType") == "text-editor":
            editor = el["settings"].get("editor", "")
            for old, new in REPLACEMENTS:
                if old in editor:
                    el["settings"]["editor"] = editor.replace(old, new, 1)
                    applied.append(old[:65])
                    print(f"  PATCHED: {old[:65]}...")
                    editor = el["settings"]["editor"]
        if el.get("elements"):
            walk_and_patch(el["elements"])

print("\nApplying site-wide link patches:")
walk_and_patch(elementor_sections)

missing = [old for old, _ in REPLACEMENTS if old[:65] not in applied]
if missing:
    print(f"\nWARNING: {len(missing)} patches not applied (string not found live):")
    for m in missing:
        print(f"  NOT FOUND: {m[:80]}")
else:
    print(f"\nAll {len(REPLACEMENTS)} patches applied.")

# ── Patch WP content field too ─────────────────────────────────────────────────
content_raw = ""
cf = post.get("content", {})
if isinstance(cf, dict):
    content_raw = cf.get("raw", "")
for old, new in REPLACEMENTS:
    content_raw = content_raw.replace(old, new)

# ── Push update ────────────────────────────────────────────────────────────────
new_elementor_str = json.dumps(elementor_sections)
payload = {
    "meta": {
        "_elementor_edit_mode": "builder",
        "_elementor_template_type": "wp-post",
        "_elementor_data": new_elementor_str,
    }
}
if content_raw:
    payload["content"] = content_raw

payload_bytes = json.dumps(payload).encode()
print(f"\nPushing update ({len(payload_bytes):,} bytes) to post {POST_ID}...")

put_req = urllib.request.Request(
    f"{WP_BASE}/posts/{POST_ID}",
    data=payload_bytes, headers=HEADERS, method="POST"
)
try:
    with urllib.request.urlopen(put_req, context=_ssl_ctx, timeout=60) as r:
        result = json.loads(r.read())
    print(f"  Updated: ID={result['id']}  Status={result['status']}")
except urllib.error.HTTPError as e:
    print(f"  HTTP {e.code}: {e.read()[:400]}"); sys.exit(1)

# ── Clear cache ────────────────────────────────────────────────────────────────
print("\nClearing Elementor cache...")
cache_req = urllib.request.Request(
    "https://chatsku.com/wp-json/elementor/v1/cache",
    headers=HEADERS, method="DELETE"
)
with urllib.request.urlopen(cache_req, context=_ssl_ctx, timeout=20) as r:
    print(f"  HTTP {r.status}")

# ── Verify all 9 blog/page links now present ───────────────────────────────────
print("\nVerifying internal links in live Elementor data:")
ed_str = new_elementor_str
all_expected = [
    "rfq-automation-for-product-catalogs",
    "b2b-ecommerce-chatbot-dallas",
    "ai-chatbot-for-manufacturers-dallas",
    "pdf-catalog-sales-liability",
    "response-gap",
    "b2b-catalog-issues-costing-sales",
    "passive-catalog",
    "ai-sales-assistant-b2b-ecommerce",
    "revenue-calculator",
]
for slug in all_expected:
    present = slug in ed_str
    print(f"  {'OK' if present else 'MISSING':6}  {slug}")

print("\nDONE.")
