"""
Patch 2 for post 42297:
- Fix PAA-2 and FAQ-2 (smart quotes caused miss in patch 1)
- Fix sentence length violations >25 words in real body content
"""
import os, sys, re, requests, urllib3
from dotenv import load_dotenv

urllib3.disable_warnings()
load_dotenv()

WP_BASE = "https://virtina.com"
WP_USER = os.getenv("WP_USERNAME")
WP_PASS = os.getenv("WP_APP_PASSWORD")
POST_ID = 42297

orig_put = requests.put
requests.put = lambda *a, **kw: orig_put(*a, **{**kw, "verify": False})
orig_get = requests.get
requests.get = lambda *a, **kw: orig_get(*a, **{**kw, "verify": False})

with open(r"C:\content-intel\clients\virtina\output\research\_42297_fixed.txt", encoding="utf-8") as f:
    content = f.read()
print(f"Loaded {len(content)} chars")

applied = 0

# ── PAA-2: regex match to avoid smart-quote mismatch ──────────────────────────
# Target: single <p> with "They refer to the same concept... net period.</p>"
# Split after 3rd sentence (after "pay the invoice.")
pat_paa2 = re.compile(
    r'(<p[^>]*>)(They refer to the same concept\. Trade credit is the general term for selling on deferred payment terms\. Net 30, Net 60, and Net 90 specify the number of days the buyer has to pay the invoice\. )(Net 30 is the most common.*?net period\.)(</p>)',
    re.DOTALL
)
def replace_paa2(m):
    open_tag, part1, part2, close_tag = m.group(1), m.group(2), m.group(3), m.group(4)
    return (f'{open_tag}{part1.rstrip()}</p>\n'
            f'<p dir="ltr" style="font-size:16px;line-height:1.75;">{part2.strip()}{close_tag}')

new_content, n = pat_paa2.subn(replace_paa2, content)
if n:
    content = new_content
    print(f"  APPLIED: PAA-2 split (regex, {n} match)")
    applied += 1
else:
    print("  MISS:    PAA-2 — regex did not match")

# ── FAQ-2: regex match ─────────────────────────────────────────────────────────
# Target: single <p> starting "Yes, and this is the recommended approach..."
# Split after 3rd sentence (after "$50,000 credit limit.")
pat_faq2 = re.compile(
    r'(<p[^>]*>)(Yes, and this is the recommended approach\. Use WooCommerce user roles to segment your buyer accounts\. .{10,80}?\$50,000 credit limit\.)(.*?)(</p>)',
    re.DOTALL
)
def replace_faq2(m):
    open_tag, part1, part2, close_tag = m.group(1), m.group(2), m.group(3), m.group(4)
    return (f'{open_tag}{part1.rstrip()}</p>\n'
            f'<p dir="ltr" style="font-size:16px;line-height:1.75;">{part2.strip()}{close_tag}')

new_content, n = pat_faq2.subn(replace_faq2, content)
if n:
    content = new_content
    print(f"  APPLIED: FAQ-2 split (regex, {n} match)")
    applied += 1
else:
    print("  MISS:    FAQ-2 — regex did not match")

# ── SENTENCE LENGTH FIXES (exact string, no smart quotes) ─────────────────────
sentence_fixes = [
    # Summary sentence 1: 27 words → split
    (
        'Research shows 67% of B2B buyers abandon a purchase when no payment terms are available, and 78% call payment terms an essential factor when choosing a supplier.',
        'Research shows 67% of B2B buyers abandon when no payment terms are available at checkout. Separately, 78% call payment terms an essential factor when choosing a supplier.',
        "S1: Summary sentence 1 (27w→2x≤20w)"
    ),
    # Summary sentence 2: 27 words → shorten
    (
        'This guide covers the three models for adding net payment terms to WooCommerce: plugin-based manual credit, financed net terms, and a PO gateway connected to your ERP.',
        'This guide covers the three models for adding net terms to WooCommerce: plugin-based manual credit, financed net terms, and a PO gateway with ERP integration.',
        "S2: Summary sentence 2 (27w→25w)"
    ),
    # Introduction sentence: 26 words → shorten
    (
        'It breaks immediately when a procurement manager arrives with a $25,000 order that must route through an AP approval process before a single dollar can move.',
        'It breaks the moment a procurement manager needs a $25,000 order approved through AP before any payment moves.',
        "S3: Introduction sentence (26w→19w)"
    ),
    # Introduction sentence: 32 words → split
    (
        "You'll get a plain explanation of how net terms work, what the three implementation models are, which one fits your operation, and what you need before the first net terms order lands.",
        "You'll get a plain explanation of how net terms work and which of the three models fits your operation. You'll also see what to have in place before the first net terms order lands.",
        "S4: Introduction sentence (32w→2x≤20w)"
    ),
    # which-model para 1: 31 words → shorten
    (
        'Model fit depends on three variables: how many net terms orders you expect per month, whether you already run an ERP, and how much credit risk your cash flow can absorb.',
        'Model fit comes down to three variables: monthly order volume, whether you run an ERP, and how much credit risk your cash flow can absorb.',
        "S5: which-model para 1 (31w→23w)"
    ),
    # which-model para 4: 28 words → shorten
    (
        'A common and effective approach is to offer Model A for known, credit-approved accounts and Model B for new buyers who have not yet established a payment history.',
        'A common approach is to run Model A for known, credit-approved accounts and Model B for new buyers without a payment history.',
        "S6: which-model para 4 (28w→22w)"
    ),
]

for old, new, label in sentence_fixes:
    if old in content:
        content = content.replace(old, new, 1)
        print(f"  APPLIED: {label}")
        applied += 1
    else:
        print(f"  MISS:    {label}")

print(f"\n{applied} fixes applied")

# ── PARA VERIFICATION ──────────────────────────────────────────────────────────
print("\n[PARA CHECK]")
p_tags = re.findall(r'<p[^>]*dir="ltr"[^>]*>(.*?)</p>', content, re.DOTALL)
fails = []
for i, p in enumerate(p_tags):
    plain = re.sub(r'<[^>]+>', '', p)
    words = len(plain.split())
    sents = len([x for x in re.split(r'[.!?]+', plain) if x.strip()])
    if words > 60 or sents > 3:
        fails.append((i+1, sents, words, plain[:70].replace('\n', ' ')))
if fails:
    for idx, s, w, snip in fails:
        print(f"  FAIL para#{idx}: {s}s {w}w | {snip}")
else:
    print("  ALL PASS")

# ── SENTENCE VERIFICATION ──────────────────────────────────────────────────────
print("\n[SENTENCE CHECK >25w]")
all_text = re.sub(r'<[^>]+>', ' ', content)
sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', all_text) if len(s.strip().split()) > 5]
longs = [(i+1, len(s.split()), s[:80]) for i, s in enumerate(sents)
         if len(s.split()) > 25
         and not re.search(r'background|padding|border|margin|font-size|display|rgba|border-radius', s, re.I)]
if longs:
    for idx, wc, snip in longs[:8]:
        print(f"  {wc}w | {snip}")
else:
    print("  ALL PASS (real body sentences ≤25w)")

# ── SAVE + PUT ─────────────────────────────────────────────────────────────────
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
    print(f"Modified: {resp.json().get('modified','')}")
    print("DONE")
else:
    print("ERROR:", resp.text[:400])
    sys.exit(1)
