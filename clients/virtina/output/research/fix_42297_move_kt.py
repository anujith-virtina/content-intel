"""
Move Key Takeaways table from after FAQ to after Real-world Scenarios
(before Common Mistakes). Also update TOC entry order.
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

# ── STEP 1: Extract the Key Takeaways block ────────────────────────────────────
# It starts at <h2 id="key-takeaways"> and ends before the conclusion div
kt_pat = re.compile(
    r'(\n*<h2 id="key-takeaways".*?</table>\n?)',
    re.DOTALL
)
m = kt_pat.search(content)
if not m:
    print("MISS: Key Takeaways block not found")
    exit(1)

kt_block = m.group(1)
print(f"  Extracted Key Takeaways block ({len(kt_block)} chars)")

# Remove from current position
content = content[:m.start()] + content[m.end():]
print("  Removed from after FAQ")

# ── STEP 2: Insert after Real-world Scenarios section ─────────────────────────
# Anchor: the common-mistakes div opening tag
common_mistakes_anchor = '<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="common-mistakes"'

if common_mistakes_anchor in content:
    content = content.replace(
        common_mistakes_anchor,
        '\n' + kt_block.strip() + '\n\n' + common_mistakes_anchor,
        1
    )
    print("  Inserted Key Takeaways before Common Mistakes section")
    applied += 1
else:
    print("  MISS: Common Mistakes anchor not found")
    exit(1)

# ── STEP 3: Fix TOC order ──────────────────────────────────────────────────────
# Current TOC has: real-world-scenarios, common-mistakes, key-takeaways
# New order should be: real-world-scenarios, key-takeaways, common-mistakes
toc_kt = re.search(
    r'(<li[^>]*>.*?href="#key-takeaways".*?</li>)',
    content, re.DOTALL
)
toc_cm = re.search(
    r'(<li[^>]*>.*?href="#common-mistakes".*?</li>)',
    content, re.DOTALL
)

if toc_kt and toc_cm:
    kt_li = toc_kt.group(1)
    cm_li = toc_cm.group(1)
    # Only swap if common-mistakes comes BEFORE key-takeaways in TOC
    if toc_cm.start() < toc_kt.start():
        # Remove key-takeaways li from its current position
        content_no_kt_toc = content[:toc_kt.start()] + content[toc_kt.end():]
        # Re-find common-mistakes in the adjusted content
        toc_cm2 = re.search(
            r'(<li[^>]*>.*?href="#common-mistakes".*?</li>)',
            content_no_kt_toc, re.DOTALL
        )
        if toc_cm2:
            # Insert key-takeaways li BEFORE common-mistakes li
            content = (content_no_kt_toc[:toc_cm2.start()]
                       + kt_li + '\n'
                       + content_no_kt_toc[toc_cm2.start():])
            print("  TOC order fixed: real-world-scenarios -> key-takeaways -> common-mistakes")
            applied += 1
        else:
            print("  MISS: common-mistakes TOC entry not found after adjustment")
    else:
        print("  TOC order already correct")
        applied += 1
else:
    print(f"  MISS: TOC entries not found (kt={bool(toc_kt)}, cm={bool(toc_cm)})")

print(f"\n{applied} fixes applied")

# ── VERIFY ─────────────────────────────────────────────────────────────────────
print("\n[ORDER CHECK]")
positions = {
    "real-world-scenarios": content.find('id="real-world-scenarios"'),
    "key-takeaways":        content.find('id="key-takeaways"'),
    "common-mistakes":      content.find('id="common-mistakes"'),
    "faq":                  content.find('id="faq"'),
    "conclusion":           content.find('id="conclusion"'),
}
for k, v in positions.items():
    print(f"  {k}: char {v}")

rw = positions["real-world-scenarios"]
kt = positions["key-takeaways"]
cm = positions["common-mistakes"]
fq = positions["faq"]
cn = positions["conclusion"]

if rw < kt < cm < fq < cn:
    print("  PASS: Real-world -> Key Takeaways -> Common Mistakes -> FAQ -> Conclusion")
else:
    print("  FAIL: Order wrong")

print("\n[EM DASH]")
em = [i+1 for i, l in enumerate(content.split('\n')) if chr(0x2014) in l]
print(f"  {em if em else 'none'}")

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
    print(f"Modified: {resp.json().get('modified', '')}")
    print("DONE")
else:
    print("ERROR:", resp.text[:400])
