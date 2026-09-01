"""
Patch 3 — final 3 sentence violations:
1. Model C description: 31w sentence
2. Late-payer dunning list: 35w sentence → convert to bullets (Rule 6 also applies)
3. Conclusion sentence: 26w
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

# FIX A — Model C para 1, sentence 3: 31 words
# "The WooCommerce order then pushes into your ERP, which generates a formatted invoice,
#  delivers it to the buyer's AP department, and handles aging and collections through
#  your existing accounts receivable workflow."
old_a = ('The WooCommerce order then pushes into your ERP, which generates a formatted invoice, '
         'delivers it to the buyer’s AP department, and handles aging and collections through '
         'your existing accounts receivable workflow.')
new_a = ('The WooCommerce order pushes into your ERP, triggering invoice generation. '
         'Your ERP delivers the invoice to the buyer’s AP department and handles aging and collections.')

if old_a in content:
    content = content.replace(old_a, new_a, 1)
    print("  APPLIED: Model C sentence split (31w→2x≤18w)")
    applied += 1
else:
    # try without smart apostrophe
    old_a2 = old_a.replace('’', "'")
    if old_a2 in content:
        content = content.replace(old_a2, new_a.replace('’', "'"), 1)
        print("  APPLIED: Model C sentence split (straight apostrophe)")
        applied += 1
    else:
        print("  MISS:    Model C sentence — trying regex")
        pat = re.compile(
            r'The WooCommerce order then pushes into your ERP, which generates a formatted invoice, '
            r'delivers it to the buyer.s AP department, and handles aging and collections through '
            r'your existing accounts receivable workflow\.'
        )
        new_content, n = pat.subn(
            'The WooCommerce order pushes into your ERP, triggering invoice generation. '
            'Your ERP delivers the invoice to the buyer’s AP department and handles aging and collections.',
            content
        )
        if n:
            content = new_content
            print(f"  APPLIED: Model C sentence split (regex, {n} match)")
            applied += 1
        else:
            print("  MISS:    Model C sentence regex also failed")

# FIX B — Late-payer dunning sentence: 35 words (Rule 6: 4 parallel items → bullets)
# "When a buyer pays late, your pre-defined dunning sequence activates: a payment reminder
#  at day 30, a formal notice at day 45, an order hold at day 60, and a collections
#  referral at day 90."
old_b = ('When a buyer pays late, your pre-defined dunning sequence activates: '
         'a payment reminder at day 30, a formal notice at day 45, '
         'an order hold at day 60, and a collections referral at day 90.')
new_b = ('When a buyer pays late, your dunning sequence activates automatically.\n</p>\n'
         '<ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;">\n'
         '<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;">'
         '<span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span>'
         '<span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Day 30:</strong> Payment reminder sent to the buyer</span></li>\n'
         '<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;">'
         '<span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span>'
         '<span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Day 45:</strong> Formal overdue notice issued</span></li>\n'
         '<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;">'
         '<span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span>'
         '<span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Day 60:</strong> New orders placed on hold</span></li>\n'
         '<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;">'
         '<span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span>'
         '<span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Day 90:</strong> Account referred to collections</span></li>\n'
         '</ul>\n'
         '<p dir="ltr" style="font-size:16px;line-height:1.75;">That sequence')

if old_b in content:
    # The old_b starts inside a <p> tag; "That sequence" continues the paragraph
    # Original: <p>When a buyer pays late...day 90.</p>\n<p>That sequence only works...
    # We split it: close the <p> after "activates automatically", add bullets, open new <p> before "That sequence"
    # But "That sequence..." is ALREADY in a separate paragraph (from patch 1 fix 3)
    # So old_b is just the first sentence of its own <p>
    # After replacement: <p dir="ltr" ...>When a buyer...automatically.\n</p>\n<ul>...</ul>\n<p...>That sequence
    # BUT: the original closing </p> still exists after "day 90."
    # So the structure becomes:
    # <p>...automatically.\n</p>\n<ul>...</ul>\n<p...>That sequence</p>   <- original </p> closes the new <p>
    # Wait no -- old_b ends at "day 90." and new_b replaces that with "...automatically.\n</p>\n<ul>...</ul>\n<p...>That sequence"
    # The original paragraph had: <p>When...day 90.</p>  (period then close p)
    # new_b replaces "When...day 90." with the new content
    # Result: <p>[new content ending with "That sequence"]</p>  <- this is WRONG
    # The </p> from old file closes the new <p> for "That sequence" — actually that's correct!
    # Let me trace:
    # BEFORE: <p dir="ltr"...>When a buyer pays late...day 90.</p>\n<p...>That sequence...collect.</p>
    # old_b matches: "When a buyer pays late...day 90."
    # new_b: "When a buyer pays late...automatically.\n</p>\n<ul>...</ul>\n<p dir="ltr"...>That sequence"
    # AFTER: <p dir="ltr"...>When a buyer pays late...automatically.\n</p>\n<ul>...</ul>\n<p dir="ltr"...>That sequence</p>\n<p...>That sequence...collect.</p>
    # PROBLEM: "That sequence" appears TWICE — once from new_b and once from the existing second paragraph!
    # I need to NOT include "That sequence" in new_b

    # Fix: new_b should NOT include "That sequence" at the end
    new_b_fixed = ('When a buyer pays late, your dunning sequence activates automatically.\n</p>\n'
                   '<ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;">\n'
                   '<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;">'
                   '<span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span>'
                   '<span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Day 30:</strong> Payment reminder sent to the buyer</span></li>\n'
                   '<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;">'
                   '<span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span>'
                   '<span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Day 45:</strong> Formal overdue notice issued</span></li>\n'
                   '<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;">'
                   '<span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span>'
                   '<span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Day 60:</strong> New orders placed on hold</span></li>\n'
                   '<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;">'
                   '<span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span>'
                   '<span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Day 90:</strong> Account referred to collections</span></li>\n'
                   '</ul>\n'
                   '<p dir="ltr" style="font-size:16px;line-height:1.75;">Configure this sequence before the first net terms order ships')
    # old_b = the first sentence in its own paragraph. After replace, the original </p> closes the new <p>
    # But wait: original structure after patch1 fix3 is:
    #   <p>When a buyer pays late...day 90.</p>
    #   <p>That sequence only works...</p>
    # old_b = "When a buyer pays late...day 90." (the CONTENT of the first p, not including <p> tags)
    # After replace: <p>When a buyer pays late...automatically.\n</p>\n<ul>...</ul>\n<p...>Configure this sequence before...</p>
    # <- the original </p> from first paragraph closes the inserted <p>
    # Then the second paragraph <p>That sequence only works...</p> remains unchanged
    # PROBLEM: new_b_fixed ends with "Configure this sequence before the first net terms order ships"
    # but the original second paragraph starts with "That sequence only works if..."
    # So the final structure would be:
    # <p>...automatically.</p><ul>...</ul><p>Configure this sequence before the first net terms order ships</p>
    # <p>That sequence only works if you defined it before the first invoice went unpaid...</p>
    # The second paragraph becomes redundant/contradictory. I need to ALSO remove or merge the second paragraph.

    # Better approach: replace both paragraphs together
    old_both = ('When a buyer pays late, your pre-defined dunning sequence activates: '
                'a payment reminder at day 30, a formal notice at day 45, '
                'an order hold at day 60, and a collections referral at day 90.'
                '</p>\n'
                '<p dir="ltr" style="font-size:16px;line-height:1.75;">'
                'That sequence only works if you defined it before the first invoice went unpaid. '
                'Stores that skip this step discover the problem 90 days later with balances they cannot collect.')

    new_both = ('When a buyer pays late, your dunning sequence activates automatically. '
                'Configure this sequence before your first net terms order ships.\n</p>\n'
                '<ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;">\n'
                '<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;">'
                '<span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span>'
                '<span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Day 30:</strong> Payment reminder sent to the buyer</span></li>\n'
                '<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;">'
                '<span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span>'
                '<span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Day 45:</strong> Formal overdue notice issued</span></li>\n'
                '<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;">'
                '<span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span>'
                '<span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Day 60:</strong> New orders placed on hold</span></li>\n'
                '<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;">'
                '<span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span>'
                '<span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Day 90:</strong> Account referred to collections</span></li>\n'
                '</ul>\n'
                '<p dir="ltr" style="font-size:16px;line-height:1.75;">'
                'Stores that skip this setup discover the problem 90 days later with balances they cannot collect.')

    if old_both in content:
        content = content.replace(old_both, new_both, 1)
        print("  APPLIED: Late-payer dunning → bullets (both paras replaced)")
        applied += 1
    else:
        print("  MISS:    Late-payer dunning old_both not found")
        content = content.replace(old_b, 'When a buyer pays late, your dunning sequence activates. It runs: reminder at day 30, notice at day 45, order hold at day 60, and referral to collections at day 90.', 1)
        print("  FALLBACK: Sentence condensed to ≤25w")
        applied += 1
else:
    print("  MISS:    Late-payer dunning old_b not found")

# FIX C — Conclusion sentence: 26 words
old_c = ('The credit policy, the approval workflow, the ERP connection, and the dunning sequence '
         'all have to be in place before the first net terms order lands.')
new_c = ('The credit policy, approval workflow, ERP connection, and dunning sequence '
         'must all be in place before the first net terms order lands.')

if old_c in content:
    content = content.replace(old_c, new_c, 1)
    print("  APPLIED: Conclusion sentence shortened (26w→22w)")
    applied += 1
else:
    print("  MISS:    Conclusion sentence not found")

print(f"\n{applied} fixes applied")

# ── FINAL CHECKS ───────────────────────────────────────────────────────────────
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

print("\n[SENTENCE CHECK >25w — real body only]")
all_text = re.sub(r'<[^>]+>', ' ', content)
sents_list = [s.strip() for s in re.split(r'(?<=[.!?])\s+', all_text) if len(s.strip().split()) > 5]
longs = [(len(s.split()), s[:90]) for s in sents_list
         if len(s.split()) > 25
         and not re.search(r'background|padding|border|margin|font-size|display|rgba|border-radius|data-', s, re.I)
         and not re.search(r'\$[0-9]|\d+/year|\d+-\d+ weeks|Plugin install', s)]
if longs:
    for wc, snip in longs[:6]:
        print(f"  {wc}w | {snip}")
else:
    print("  ALL PASS")

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
