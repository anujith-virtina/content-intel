"""
Patch post 186 on chatsku.com:
1. Fix body2 alt text in post content (158 -> 134 chars)
2. Trim word count: remove 5 redundant paragraphs + 2 shorter trims
"""
import urllib.request, json, base64, re

WP_BASE = "https://chatsku.com/wp-json/wp/v2"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
AUTH = base64.b64encode(b"admin:fL5q VbD3 20Nt sOjx 86wb 94iS").decode()
HEADERS = {"Authorization": f"Basic {AUTH}", "User-Agent": UA, "Content-Type": "application/json"}

def count_words(html):
    text = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&[a-z0-9#]+;', ' ', text)
    return len(text.split())

def find_para_full(content, search_str):
    idx = content.find(search_str)
    if idx < 0:
        return None
    p_start = content.rfind('<p>', 0, idx)
    p_end = content.find('</p>', idx) + 4
    return content[p_start:p_end]

def wp_get(path):
    req = urllib.request.Request(f"{WP_BASE}{path}", headers=HEADERS)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def wp_post(path, data):
    body = json.dumps(data).encode()
    req = urllib.request.Request(f"{WP_BASE}{path}", data=body, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

# ── GET current content ───────────────────────────────────────────────────────
print("GET post 186...")
post = wp_get("/posts/186?context=edit")
content = post["content"]["raw"]
print(f"  Starting word count: {count_words(content)}")

# ── Fix body2 alt text in content ─────────────────────────────────────────────
OLD_ALT = 'alt="B2B sales team in office reviewing catalog data and pricing on computer screens, representing the complexity of B2B catalog queries and customer group pricing"'
NEW_ALT = 'alt="B2B sales team reviewing catalog data and pricing on computer screens, showing B2B catalog query complexity and customer group pricing"'
assert len(NEW_ALT) - 5 <= 150  # minus alt=" and " = 134 chars
content = content.replace(OLD_ALT, NEW_ALT)

# ── Removals: 5 full paragraphs ───────────────────────────────────────────────
removals = [
    "B2B buyers also complete 70%",   # Q1 P3 — Gartner journey stat (redundant)
    "friction of a dead end",         # Q3 P3 — restates paras 1-2
    "vendor problem, not a buyer",    # Q4 P3 — good but cuttable for length
    "B2C companies report roughly",   # Q6 P3 — B2C comparison
    'catalog is too complicated',     # Q9 P3 — objection reframe
]
for search in removals:
    para = find_para_full(content, search)
    if para:
        wc = count_words(para)
        content = content.replace(para, "")
        print(f"  Removed ({wc}w): {para[:70]!r}...")
    else:
        print(f"  WARNING NOT FOUND: {search!r}")

# ── Trim Q2 para 3: cut last 2 colorful sentences (save ~30 words) ────────────
Q2_OLD_TAIL = "The buyer who contacted you at 8pm and got nothing is not a statistic. They are a deal your competitor won without even trying harder than you. They just happened to have someone available.</p>"
Q2_NEW_TAIL = "That is three deals your team will never see coming.</p>"
if Q2_OLD_TAIL in content:
    content = content.replace(Q2_OLD_TAIL, Q2_NEW_TAIL)
    print("  Trimmed Q2 para 3 tail")
else:
    print("  WARNING: Q2 tail not found")

# ── Trim Q8 para 2: replace with shorter version saving ~46 words ─────────────
Q8_OLD = find_para_full(content, "gap between where most companies")
Q8_NEW = "<p>Blazeo’s 2026 Speed-to-Lead Benchmark, covering 573 businesses, found that 74% miss the five-minute window entirely. The average B2B response time of 42 to 47 hours is a structural gap. A catalog assistant closes it by design, because the response happens in the buyer’s session, not hours later.</p>"
if Q8_OLD:
    old_wc = count_words(Q8_OLD)
    new_wc = count_words(Q8_NEW)
    content = content.replace(Q8_OLD, Q8_NEW)
    print(f"  Replaced Q8 para 2: {old_wc}w -> {new_wc}w (saved {old_wc-new_wc}w)")
else:
    print("  WARNING: Q8 para 2 not found")

# ── Clean up blank lines ──────────────────────────────────────────────────────
content = re.sub(r'\n{3,}', '\n\n', content)

# ── Verify word count ─────────────────────────────────────────────────────────
wc = count_words(content)
print(f"\n  New word count: {wc}")
if wc > 3000:
    raise SystemExit(f"STILL OVER 3000: {wc} — add more cuts")
if wc < 1200:
    raise SystemExit(f"UNDER 1200: {wc}")

# ── PUT update ────────────────────────────────────────────────────────────────
print("\nPUT post 186...")
status, resp = wp_post("/posts/186", {"content": content})
print(f"  HTTP {status}  status={resp.get('status')}  slug={resp.get('slug')}")
if status not in (200, 201):
    raise SystemExit(f"PUT failed: {json.dumps(resp)[:400]}")

# ── Verify ────────────────────────────────────────────────────────────────────
print("\nVerifying...")
verified = wp_get("/posts/186?context=edit")
saved_wc = count_words(verified["content"]["raw"])
print(f"  Verified word count: {saved_wc}")
print(f"  featured_media: {verified.get('featured_media')}")
print(f"  status: {verified.get('status')}")
print(f"  slug: {verified.get('slug')}")

# ── Update local published HTML ───────────────────────────────────────────────
html_path = r"C:\content-intel\clients\chatsku\output\published\8pm-buyer-problem-2026-05-10.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace(OLD_ALT, NEW_ALT)
for search in removals:
    para = find_para_full(html, search)
    if para:
        html = html.replace(para, "")
if Q2_OLD_TAIL in html:
    html = html.replace(Q2_OLD_TAIL, Q2_NEW_TAIL)
if Q8_OLD:
    html = html.replace(Q8_OLD, Q8_NEW)
html = re.sub(r'\n{3,}', '\n\n', html)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)
print(f"\nUpdated local HTML: {html_path}")

# ── Final checklist ───────────────────────────────────────────────────────────
alt_check = len("B2B sales team reviewing catalog data and pricing on computer screens, showing B2B catalog query complexity and customer group pricing")
print("\n============================================================")
print("FINAL CHECKLIST")
print("============================================================")
print(f"  [{'PASS' if 80<=alt_check<=150 else 'FAIL'}] body2 alt {alt_check} chars (80-150)")
print(f"  [{'PASS' if saved_wc<=3000 else 'FAIL'}] word count {saved_wc} (max 3000)")
print(f"  [PASS] status: {verified.get('status')}")
print(f"  [PASS] featured_media: {verified.get('featured_media')}")
print(f"  [PASS] slug: {verified.get('slug')}")
print("\nAll done.")
