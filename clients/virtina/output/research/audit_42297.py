"""
Full audit of post 42297 current state.
Shows every paragraph that fails, every long sentence, and the full section order.
"""
import re

with open(r"C:\content-intel\clients\virtina\output\research\_42297_fixed.txt", encoding="utf-8") as f:
    content = f.read()

print("=" * 70)
print("PARAGRAPH AUDIT (>3 sentences OR >60 words)")
print("=" * 70)
p_tags = re.findall(r'<p[^>]*dir="ltr"[^>]*>(.*?)</p>', content, re.DOTALL)
para_fails = []
for i, p in enumerate(p_tags):
    plain = re.sub(r'<[^>]+>', '', p).strip()
    words = len(plain.split())
    sents = len([x for x in re.split(r'[.!?]+', plain) if x.strip()])
    if words > 60 or sents > 3:
        para_fails.append((i+1, sents, words, plain))

if para_fails:
    for idx, s, w, text in para_fails:
        print(f"\n  FAIL para #{idx}: {s} sentences, {w} words")
        print(f"  TEXT: {text[:200]}")
else:
    print("  ALL PASS")

print(f"\nTotal failing paragraphs: {len(para_fails)}")

print("\n" + "=" * 70)
print("SENTENCE AUDIT (>25 words, body content only)")
print("=" * 70)
all_text = re.sub(r'<[^>]+>', ' ', content)
all_text = re.sub(r'\s+', ' ', all_text)
sents_list = [s.strip() for s in re.split(r'(?<=[.!?])\s+', all_text) if len(s.strip().split()) > 5]
skip = re.compile(
    r'background|padding|border|margin|font-size|display|rgba|data-|'
    r'\$[0-9]|\d+/year|\d{1,2}-\d{1,2} weeks|Plugin install|'
    r'Cost\s+\$|Speed to deploy|ERP sync|Setup complex|Best for|Credit risk|'
    r'Day \d+:|Model [ABC]\s*\(|Your situation|Monthly volume|Recommended', re.I
)
longs = [(len(s.split()), s) for s in sents_list if len(s.split()) > 25 and not skip.search(s)]
if longs:
    for wc, s in longs:
        print(f"\n  {wc}w: {s[:200]}")
else:
    print("  ALL PASS")
print(f"\nTotal long sentences: {len(longs)}")

print("\n" + "=" * 70)
print("SECTION ORDER (H2 + H3 headings in sequence)")
print("=" * 70)
headings = re.findall(r'<(h[23])[^>]*>(.*?)</\1>', content, re.DOTALL)
for tag, text in headings:
    clean = re.sub(r'<[^>]+>', '', text).strip()
    indent = "    " if tag == "h3" else ""
    print(f"  {indent}[{tag.upper()}] {clean}")
