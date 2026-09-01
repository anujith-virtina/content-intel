"""
Patch post 266 (b2b-catalog-conversion-rate):
Add 4 internal blog post links to existing Elementor content.

Links being added:
  Q3  → /rfq-automation-for-product-catalogs/  (Order workflow bullet)
  Q4  → /b2b-ecommerce-chatbot-dallas/          (end of last paragraph)
  Q5  → /ai-chatbot-for-manufacturers-dallas/   (end of paragraph 2)
  Q5  → /pdf-catalog-sales-liability/           (PDF mention in paragraph 3)

Does NOT re-upload images or rebuild from scratch.
Fetches live _elementor_data, patches text-editor widgets, PUTs update.
"""

import json, urllib.request, urllib.error, base64, os, ssl, sys

_ssl_ctx = ssl._create_unverified_context()

# ── Credentials ────────────────────────────────────────────────────────────────
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

AUTH = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
HEADERS = {"Authorization": f"Basic {AUTH}", "User-Agent": UA,
           "Content-Type": "application/json"}

POST_ID = 266

# ── 4 targeted replacements ────────────────────────────────────────────────────
REPLACEMENTS = [
    # 1. Q3 — Order workflow bullet: add RFQ automation link
    (
        "<li><strong>Order workflow.</strong> Does this require an RFQ, or can I place it directly?</li>",
        '<li><strong>Order workflow.</strong> Does this require an RFQ, or can I place it directly? '
        'For teams with high quote volume, <a href="https://chatsku.com/rfq-automation-for-product-catalogs/">'
        'RFQ automation</a> handles this step end-to-end.</li>'
    ),
    # 2. Q4 — last paragraph: add after-hours lead loss link
    (
        "The next problem is the conversation architecture problem.</p>",
        'The next problem is the conversation architecture problem. '
        'The same gap <a href="https://chatsku.com/b2b-ecommerce-chatbot-dallas/">'
        'costs distributors leads after hours</a> too.</p>'
    ),
    # 3. Q5 — paragraph 2: add AI chatbot eval link at end
    (
        "It answers the specific questions that block B2B purchase decisions: "
        "contract pricing, MOQ, compatibility, lead time.</p>",
        'It answers the specific questions that block B2B purchase decisions: '
        'contract pricing, MOQ, compatibility, lead time. '
        'If you\'re evaluating options, <a href="https://chatsku.com/ai-chatbot-for-manufacturers-dallas/">'
        'here are the questions to ask before you commit</a>.</p>'
    ),
    # 4. Q5 — paragraph 3: PDF catalog link
    (
        "It connects to existing catalog sources (PDF, Excel, ERP exports) and answers "
        "account-specific questions without requiring a site rebuild.",
        'It connects to existing catalog sources '
        '(<a href="https://chatsku.com/pdf-catalog-sales-liability/">PDF catalogs</a>, '
        'Excel, ERP exports) and answers account-specific questions without requiring a site rebuild.'
    ),
]

# ── Fetch current post ─────────────────────────────────────────────────────────
print(f"Fetching post {POST_ID}...")
req = urllib.request.Request(f"{WP_BASE}/posts/{POST_ID}?context=edit", headers=HEADERS)
with urllib.request.urlopen(req, context=_ssl_ctx, timeout=30) as r:
    post = json.loads(r.read())

print(f"  Status: {post['status']}  Title: {post['title']['raw'][:60]}")

# ── Parse Elementor data ───────────────────────────────────────────────────────
raw_meta = post.get("meta", {})
elementor_str = raw_meta.get("_elementor_data", "")
if not elementor_str:
    print("ERROR: _elementor_data not found in meta — cannot patch"); sys.exit(1)

try:
    elementor_sections = json.loads(elementor_str)
except Exception as e:
    print(f"ERROR parsing _elementor_data: {e}"); sys.exit(1)

print(f"  Parsed {len(elementor_sections)} Elementor sections")

# ── Walk widgets and apply replacements ────────────────────────────────────────
applied = []

def walk_and_patch(elements):
    for el in elements:
        if el.get("widgetType") == "text-editor":
            editor = el["settings"].get("editor", "")
            for old, new in REPLACEMENTS:
                if old in editor:
                    el["settings"]["editor"] = editor.replace(old, new, 1)
                    applied.append(old[:70])
                    print(f"  PATCHED: ...{old[:70]}...")
                    editor = el["settings"]["editor"]
        if el.get("elements"):
            walk_and_patch(el["elements"])

print("\nApplying blog link patches to text-editor widgets:")
walk_and_patch(elementor_sections)

if len(applied) != len(REPLACEMENTS):
    print(f"\nWARNING: Expected {len(REPLACEMENTS)} patches, applied {len(applied)}")
    missing = [old[:70] for old, _ in REPLACEMENTS if old[:70] not in applied]
    for m in missing:
        print(f"  NOT FOUND: {m}...")
    print("  (String may have changed; check the live post and apply manually if needed)")
else:
    print(f"\nAll {len(applied)} patches applied successfully.")

# ── Also patch WP content field ───────────────────────────────────────────────
content_raw = ""
content_field = post.get("content", {})
if isinstance(content_field, dict):
    content_raw = content_field.get("raw", "")
for old, new in REPLACEMENTS:
    content_raw = content_raw.replace(old, new)

# ── Build payload ──────────────────────────────────────────────────────────────
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
print(f"\nPayload size: {len(payload_bytes):,} bytes")

# ── PUT to post 266 ────────────────────────────────────────────────────────────
print(f"Pushing update to post {POST_ID}...")
put_req = urllib.request.Request(
    f"{WP_BASE}/posts/{POST_ID}",
    data=payload_bytes,
    headers=HEADERS,
    method="POST"
)
try:
    with urllib.request.urlopen(put_req, context=_ssl_ctx, timeout=60) as r:
        result = json.loads(r.read())
    print(f"  Updated: ID={result['id']}  Status={result['status']}  Link={result.get('link','')}")
except urllib.error.HTTPError as e:
    body = e.read()[:400]
    print(f"  HTTP {e.code}: {body}")
    sys.exit(1)

# ── Clear Elementor cache ──────────────────────────────────────────────────────
print("\nClearing Elementor cache...")
cache_req = urllib.request.Request(
    "https://chatsku.com/wp-json/elementor/v1/cache",
    headers=HEADERS,
    method="DELETE"
)
with urllib.request.urlopen(cache_req, context=_ssl_ctx, timeout=20) as r:
    print(f"  Cache clear: HTTP {r.status}")

# ── Report link counts ─────────────────────────────────────────────────────────
import re
full_html = new_elementor_str
internal_links = re.findall(r'href="https://chatsku\.com/[^"]*"', full_html)
external_links = re.findall(r'href="https://(?!chatsku\.com)[^"]*"', full_html)

print(f"\nLink count in updated Elementor data:")
print(f"  Internal (chatsku.com): {len(internal_links)}")
for lnk in sorted(set(internal_links)):
    print(f"    {lnk}")
print(f"  External (non-chatsku): {len(external_links)}")
for lnk in sorted(set(external_links)):
    print(f"    {lnk}")

print("\nDONE. Post 266 updated with 4 blog post internal links.")
print("Manual follow-up: Yoast title/desc still needs manual WP dashboard entry.")
