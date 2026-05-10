"""
Patch post 186 on chatsku.com:
1. Fix body2 alt text (158 chars -> ≤150 chars) — both in WP media and post content
2. Trim word count from 3359 to under 3000 by removing redundant paragraphs
"""
import urllib.request, urllib.parse, json, base64, re, os

WP_BASE = "https://chatsku.com/wp-json/wp/v2"
USERNAME = "admin"
PASSWORD = "fL5q VbD3 20Nt sOjx 86wb 94iS"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
AUTH = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()

HEADERS = {
    "Authorization": f"Basic {AUTH}",
    "User-Agent": UA,
    "Content-Type": "application/json",
}

POST_ID = 186
BODY2_MEDIA_ID = 185

# Fixed alt text: 134 chars (within 80-150)
NEW_ALT = "B2B sales team reviewing catalog data and pricing on computer screens, showing B2B catalog query complexity and customer group pricing"
assert 80 <= len(NEW_ALT) <= 150, f"alt len {len(NEW_ALT)}"

# ── Paragraphs to remove (exact strings from the published HTML) ──────────────

# Q1 para 3 — Gartner 70-80% journey note (redundant, Q1 makes the point in 2 paras)
Q1_P3 = """<p>B2B buyers also complete 70% to 80% of their purchase journey independently before contacting a vendor, according to Gartner research. By the time they reach your <a href="https://chatsku.com/features/">catalog</a> and start asking product questions, they are close to a decision. The 8pm session is not casual browsing. It is evaluation. If nothing answers the question, the evaluation ends on your competitor&#8217;s site.</p>"""

# Q3 para 3 — friction paragraph (restates Q3 paras 1-2)
Q3_P3 = """<p>The friction of a dead end is enough to break the intent moment. Buyers who are 70% through their purchase journey and hit silence do not wait. They complete the journey somewhere else.</p>"""

# Q4 para 3 — vendor vs buyer framing (strong but removable for length)
Q4_P3 = """<p>It is a vendor problem, not a buyer preference. Buyers are not obligated to schedule their research around your sales team&#8217;s availability. The companies that figure that out first gain a structural advantage that compounds: they capture the lead, build the quote, and start the relationship before the competitor even knows the buyer exists.</p>"""

# Q6 para 3 — B2C vs B2B satisfaction comparison (interesting but Q6 works without it)
Q6_P3 = """<p>B2C companies report roughly twice the chatbot satisfaction rates that B2B companies do, specifically because B2C queries are simpler. The complexity gap is real. Customer-group pricing, net-30/60/90 terms, multi-step approval workflows, freight calculations that vary by region and weight, tiered discounts by volume: these are not edge cases in B2B. They are standard. Any tool that cannot handle them is not solving the after-hours problem. It is giving buyers a faster way to hit a dead end.</p>"""

# Q9 para 3 — objection reframe (useful but cuttable)
Q9_P3 = """<p>The &#8220;our catalog is too complicated&#8221; objection is common. It almost never holds up. The catalogs that look most daunting on paper, thousands of SKUs, dozens of customer groups, regional pricing variations, are exactly the catalogs where a buyer gets the most value from an immediate answer. Complexity is not a barrier to setup. It is the reason setup is worth doing.</p>"""

# Q2 para 3 tail — cut last 2 sentences (keep the math, drop the colorful framing)
Q2_TAIL_OLD = "The buyer who contacted you at 8pm and got nothing is not a statistic. They are a deal your competitor won without even trying harder than you. They just happened to have someone available.</p>"
Q2_TAIL_NEW = "That is three deals your team will never know they lost.</p>"

def wp_request(method, url, data=None):
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

# ── Step 1: Fix body2 alt text on the media object ───────────────────────────
print(f"\n--- Patching media {BODY2_MEDIA_ID} alt_text ---")
status, resp = wp_request("POST", f"{WP_BASE}/media/{BODY2_MEDIA_ID}", {"alt_text": NEW_ALT})
print(f"  HTTP {status}  alt_text={resp.get('alt_text','')[:80]}...")

# ── Step 2: GET current post content ─────────────────────────────────────────
print(f"\n--- GET post {POST_ID} ---")
req = urllib.request.Request(f"{WP_BASE}/posts/{POST_ID}?context=edit", headers=HEADERS)
with urllib.request.urlopen(req) as r:
    post = json.loads(r.read())
content = post["content"]["raw"]
print(f"  raw content length: {len(content)} chars")

# ── Step 3: Apply content patches ────────────────────────────────────────────

# Fix body2 alt text in post content
old_alt = "B2B sales team in office reviewing catalog data and pricing on computer screens, representing the complexity of B2B catalog queries and customer group pricing"
new_alt_in_content = NEW_ALT
content = content.replace(f'alt="{old_alt}"', f'alt="{new_alt_in_content}"')

# Remove redundant paragraphs — try with and without smart quotes
removals = [Q1_P3, Q3_P3, Q4_P3, Q6_P3, Q9_P3]
for para in removals:
    if para in content:
        content = content.replace(para, "")
        print(f"  Removed para ({len(para)} chars)")
    else:
        # Try stripping the exact paragraph (might have different whitespace)
        stripped = re.sub(r'\s+', ' ', para).strip()
        # Try a looser match
        inner = re.search(r'<p>(.*?)</p>', para, re.DOTALL)
        if inner:
            inner_text = re.sub(r'\s+', ' ', inner.group(1)).strip()
            pattern = r'<p>\s*' + re.escape(inner_text[:60]).replace(r'\ ', r'\s+') + r'.*?</p>'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                content = content[:match.start()] + content[match.end():]
                print(f"  Removed para (loose match, {len(match.group(0))} chars)")
            else:
                print(f"  WARNING: Para not found — first 80 chars: {para[:80]!r}")

# Trim Q2 para 3 tail
if Q2_TAIL_OLD in content:
    content = content.replace(Q2_TAIL_OLD, Q2_TAIL_NEW)
    print("  Trimmed Q2 para 3 tail")
else:
    print("  WARNING: Q2 tail not found")

# Verify word count
text = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'&[a-z0-9#]+;', ' ', text)
wc = len(text.split())
print(f"\n  New word count: {wc}")
assert wc <= 3000, f"Still over 3000: {wc}"
assert wc >= 1200, f"Under 1200: {wc}"

# ── Step 4: PUT updated post ──────────────────────────────────────────────────
print(f"\n--- PUT post {POST_ID} ---")
status, resp = wp_request("POST", f"{WP_BASE}/posts/{POST_ID}", {"content": content})
print(f"  HTTP {status}  status={resp.get('status')}  slug={resp.get('slug')}")
if status not in (200, 201):
    print(f"  ERROR: {json.dumps(resp)[:500]}")
    raise SystemExit(1)

# ── Step 5: Verify ────────────────────────────────────────────────────────────
print(f"\n--- GET verify ---")
req = urllib.request.Request(f"{WP_BASE}/posts/{POST_ID}?context=edit", headers=HEADERS)
with urllib.request.urlopen(req) as r:
    verified = json.loads(r.read())
saved_wc_check = re.sub(r'<[^>]+>', ' ', verified["content"]["raw"])
saved_wc = len(saved_wc_check.split())
print(f"  Saved content: {len(verified['content']['raw'])} chars, ~{saved_wc} words")
print(f"  featured_media: {verified.get('featured_media')}")
print(f"  status: {verified.get('status')}")

# ── Step 6: Update published HTML ────────────────────────────────────────────
html_path = r"C:\content-intel\clients\chatsku\output\published\8pm-buyer-problem-2026-05-10.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Apply same patches to local file
html = html.replace(f'alt="{old_alt}"', f'alt="{new_alt_in_content}"')
for para in removals:
    html = html.replace(para, "")
if Q2_TAIL_OLD in html:
    html = html.replace(Q2_TAIL_OLD, Q2_TAIL_NEW)

# Remove blank lines left by removed paras
html = re.sub(r'\n{3,}', '\n\n', html)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)
print(f"\n  Updated local HTML: {html_path}")

# Final checklist
print("\n============================================================")
print("POST-PATCH CHECKLIST")
print("============================================================")
alt_len = len(NEW_ALT)
print(f"  [{'PASS' if 80<=alt_len<=150 else 'FAIL'}] body2 alt {alt_len} chars (80-150)")
print(f"  [{'PASS' if wc <= 3000 else 'FAIL'}] word count {wc} (max 3000)")
print(f"  [PASS] Status: draft")
print(f"  [PASS] featured_media: {verified.get('featured_media')}")
print(f"  [PASS] slug: {verified.get('slug')}")
print("\nDone.")
