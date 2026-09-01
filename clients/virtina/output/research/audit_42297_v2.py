"""
Full audit — checks ALL <p> tags, not just dir=ltr ones.
Also fetches live rendered content from WordPress to check what's actually visible.
"""
import re, os, requests, urllib3
from dotenv import load_dotenv

urllib3.disable_warnings()
load_dotenv()

WP_BASE = "https://virtina.com"
WP_USER = os.getenv("WP_USERNAME")
WP_PASS = os.getenv("WP_APP_PASSWORD")

with open(r"C:\content-intel\clients\virtina\output\research\_42297_fixed.txt", encoding="utf-8") as f:
    content = f.read()

print("=" * 70)
print("ALL <p> PARAGRAPH AUDIT (any style, >3 sentences OR >60 words)")
print("=" * 70)

# Match ALL <p> tags
p_tags = re.findall(r'<p\b[^>]*>(.*?)</p>', content, re.DOTALL)
fails = []
for i, p in enumerate(p_tags):
    plain = re.sub(r'<[^>]+>', '', p).strip()
    if len(plain.split()) < 4:
        continue  # skip table cell labels, empty, tiny
    words = len(plain.split())
    sents = len([x for x in re.split(r'[.!?]+', plain) if x.strip()])
    if words > 60 or sents > 3:
        fails.append((i+1, sents, words, plain))

if fails:
    for idx, s, w, text in fails:
        print(f"\n  FAIL para #{idx}: {s}s / {w}w")
        print(f"  {text[:250]}")
else:
    print("  ALL PASS — every <p> is <=3 sentences and <=60 words")

print(f"\nFailing count: {len(fails)}")

print("\n" + "=" * 70)
print("LIVE RENDERED CONTENT CHECK (what WordPress actually shows)")
print("=" * 70)

resp = requests.get(
    f"{WP_BASE}/wp-json/wp/v2/posts/42297",
    auth=(WP_USER, WP_PASS),
    verify=False
)
rendered = resp.json().get("content", {}).get("rendered", "")
raw_stored = resp.json().get("content", {}).get("raw", "")

print(f"  REST API post_content raw: {len(raw_stored)} chars")
print(f"  REST API rendered: {len(rendered)} chars")
print(f"  Our local file: {len(content)} chars")

if abs(len(raw_stored) - len(content)) < 500:
    print("  MATCH: WordPress post_content matches our file")
else:
    print(f"  MISMATCH: {abs(len(raw_stored)-len(content))} char difference — Thrive may be rendering stale cache")

# Check rendered for long paragraphs
print("\n  Checking rendered HTML for long paragraphs...")
r_tags = re.findall(r'<p\b[^>]*>(.*?)</p>', rendered, re.DOTALL)
r_fails = []
for i, p in enumerate(r_tags):
    plain = re.sub(r'<[^>]+>', '', p).strip()
    if len(plain.split()) < 4:
        continue
    words = len(plain.split())
    sents = len([x for x in re.split(r'[.!?]+', plain) if x.strip()])
    if words > 60 or sents > 3:
        r_fails.append((i+1, sents, words, plain))

if r_fails:
    print(f"  {len(r_fails)} failing paragraphs in RENDERED content:")
    for idx, s, w, text in r_fails[:10]:
        print(f"\n    FAIL #{idx}: {s}s / {w}w")
        print(f"    {text[:250]}")
else:
    print("  ALL PASS in rendered content")
