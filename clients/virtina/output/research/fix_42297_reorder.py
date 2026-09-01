"""
Reorder fix for post 42297:
1. Remove Quick Answer block (was incorrectly inserted before Summary)
2. Move Conclusion div from before FAQ to after Key Takeaways table
Final order: Summary -> [body] -> FAQ -> Key Takeaways -> Conclusion -> Author bio
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

applied = 0

# FIX 1 — Remove Quick Answer block
# It starts with the teal gradient div containing h2 "Quick answer"
qa_pat = re.compile(
    r'<div style="background:linear-gradient\(rgba\(0,213,192,0\.28\).*?Quick answer</h2>.*?</div>\n?',
    re.DOTALL
)
new_content, n = qa_pat.subn('', content, count=1)
if n:
    content = new_content
    print("  APPLIED: Quick Answer block removed")
    applied += 1
else:
    print("  MISS: Quick Answer block not found")

# FIX 2 — Extract Conclusion div (currently sitting before FAQ)
conc_pat = re.compile(
    r'(<div style="background:#00d5c0[^"]*"[^>]*><h2 id="conclusion".*?</div>)\n*(?=<h2 id="faq")',
    re.DOTALL
)
m = conc_pat.search(content)
if m:
    conclusion_div = m.group(1)
    # Remove conclusion from current position
    content = content[:m.start()] + '\n' + content[m.end():]
    print("  APPLIED: Conclusion extracted from before FAQ")

    # Insert conclusion after </table> of Key Takeaways, just before author bio
    bio_pat = re.compile(r'<p[^>]*><strong>The Virtina Team</strong>')
    bio_m = bio_pat.search(content)
    if bio_m:
        insert_pos = bio_m.start()
        content = content[:insert_pos] + conclusion_div + '\n' + content[insert_pos:]
        print("  APPLIED: Conclusion inserted before author bio (after Key Takeaways)")
        applied += 1
    else:
        print("  MISS: Author bio anchor not found")
else:
    print("  MISS: Conclusion+FAQ boundary pattern not found")

print(f"\n{applied} fixes applied")

# ── ORDER VERIFICATION ─────────────────────────────────────────────────────────
print("\n[ORDER CHECK]")
pos = {
    "summary":       content.find('>Summary<'),
    "faq":           content.find('id="faq"'),
    "key-takeaways": content.find('id="key-takeaways"'),
    "conclusion":    content.find('id="conclusion"'),
    "author-bio":    content.find('<strong>The Virtina Team</strong>'),
    "quick-answer":  content.find('Quick answer'),
}
for k, v in pos.items():
    print(f"  {k}: {v}")

if pos["quick-answer"] == -1:
    print("  PASS: Quick Answer block gone")
else:
    print("  FAIL: Quick Answer still present")

if (pos["faq"] > 0 and
        pos["key-takeaways"] > pos["faq"] and
        pos["conclusion"] > pos["key-takeaways"] and
        pos["author-bio"] > pos["conclusion"]):
    print("  PASS: FAQ -> Key Takeaways -> Conclusion -> Author bio")
else:
    print("  FAIL: Order is wrong — check positions above")

# ── EM DASH CHECK ──────────────────────────────────────────────────────────────
em = [i+1 for i, line in enumerate(content.split('\n')) if '—' in line or '&mdash;' in line]
print(f"\nem dashes: {em if em else 'none'}")

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
