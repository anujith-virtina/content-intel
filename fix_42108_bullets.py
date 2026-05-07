"""
Fix post 42108: replace corrupted <<ul...>> bullet lists with simple CSS-circle markup.
Images are NOT touched (Pexels API key required separately).
"""
import json, base64, urllib.request, re, sys

CREDS    = base64.b64encode(b'anujith:Mibz 1h3E jWRi bfJs WAXZ rwrM').decode()
POST_URL = 'https://virtina.com/wp-json/wp/v2/posts/42108'

# ── fetch current content ─────────────────────────────────────────────────────
print("Fetching post 42108...")
req = urllib.request.Request(
    POST_URL + '?context=edit&_fields=content,featured_media,status',
    headers={'Authorization': 'Basic ' + CREDS}
)
with urllib.request.urlopen(req, timeout=30) as r:
    post = json.loads(r.read())
content = post['content']['raw']
featured_media = post['featured_media']
print(f"Length: {len(content)}  featured_media={featured_media}")

# ── build new bullet list HTML ────────────────────────────────────────────────
UL_OPEN  = '<ul style="list-style:none; padding-left:0; margin:0 0 1.5em 0;">'
LI_OPEN  = '<li style="position:relative; padding:8px 0 8px 28px; line-height:1.6; margin:0;">'
CIRCLE   = ('<span style="position:absolute; left:0; top:14px; width:10px; height:10px; '
            'background-color:#16afa0; border-radius:50%; display:inline-block;"></span>')

def build_ul(item_texts):
    items = '\n'.join(f'{LI_OPEN}{CIRCLE}{t}</li>' for t in item_texts)
    return f'{UL_OPEN}\n{items}\n</ul>'

def extract_li_text(li_inner_html):
    """Strip SVG icons and outer span wrappers, preserve inline <strong> etc."""
    # Remove SVG icons
    text = re.sub(r'<svg[^>]*>.*?</svg>', '', li_inner_html, flags=re.DOTALL)
    # If there's a wrapping span (the old text span), unwrap it
    sp = re.search(r'<span[^>]*>(.*?)</span>', text, re.DOTALL)
    if sp:
        text = sp.group(1)
    return text.strip()

# ── find and replace all body bullet lists ───────────────────────────────────
# Matches both <<ul...>> (corrupted) and <ul...> (normal) body lists
# TOC lists use !important — excluded by requiring no ! in the style
body_ul_re = re.compile(
    r'<{1,2}ul\s+style="list-style:none;(?!!)[^"]*">{1,2}.*?</ul>',
    re.DOTALL
)

fixed = content
replacements = 0
for m in list(body_ul_re.finditer(fixed)):
    ul_html = m.group()
    print(f"\nList at pos={m.start()}, length={len(ul_html)}")

    # Check for double-bracket corruption
    if ul_html.startswith('<<'):
        print("  Corrupted: <<ul...>> pattern detected")

    # Extract li text (full inner HTML minus SVG and outer span)
    items = []
    for li_m in re.finditer(r'<li[^>]*>(.*?)</li>', ul_html, re.DOTALL):
        text = extract_li_text(li_m.group(1))
        if text:
            items.append(text)
            print(f"  LI: {text[:100]}")

    if not items:
        print("  SKIP: no li items found")
        continue

    new_ul = build_ul(items)
    fixed = fixed[:m.start()] + new_ul + fixed[m.end():]
    # After replacement, positions shift — restart search on updated content
    # We re-find from scratch each time by rebuilding the iterator
    replacements += 1
    print(f"  -> Replaced with CSS-circle list ({len(items)} items)")
    # Restart: re-run findall on updated fixed content
    break

# Re-run until no more corrupted/old-style lists remain
while True:
    m = body_ul_re.search(fixed)
    if not m:
        break
    ul_html = m.group()
    print(f"\nList at pos={m.start()}")
    items = []
    for li_m in re.finditer(r'<li[^>]*>(.*?)</li>', ul_html, re.DOTALL):
        text = extract_li_text(li_m.group(1))
        if text:
            items.append(text)
    if not items:
        break
    new_ul = build_ul(items)
    fixed = fixed[:m.start()] + new_ul + fixed[m.end():]
    replacements += 1
    print(f"  -> Replaced ({len(items)} items)")

print(f"\nTotal lists replaced: {replacements}")

# ── verify no orphan << >> remain ─────────────────────────────────────────────
orphan_dbl = len(re.findall(r'<<', fixed)) + len(re.findall(r'>>', fixed))
print(f"Remaining << or >> patterns: {orphan_dbl}")
if orphan_dbl:
    # Last-pass strip any remaining double brackets around ul tags
    fixed = re.sub(r'<<(ul\s)', r'<\1', fixed)
    fixed = re.sub(r'(<ul[^>]+>)>', r'\1', fixed)
    orphan_dbl2 = len(re.findall(r'<<', fixed)) + len(re.findall(r'>>', fixed))
    print(f"After cleanup pass: {orphan_dbl2}")

# ── sanity check: count new-style lists ──────────────────────────────────────
new_ul_count = len(re.findall(r'<ul style="list-style:none; padding-left:0;', fixed))
css_circle_count = len(re.findall(r'background-color:#16afa0; border-radius:50%', fixed))
print(f"New-style lists: {new_ul_count}  CSS circles: {css_circle_count}")

# ── PUT post ──────────────────────────────────────────────────────────────────
print("\nPushing to WordPress...")
payload = json.dumps({
    'content': fixed,
    'status': 'draft',
    'featured_media': featured_media
}).encode('utf-8')

req = urllib.request.Request(POST_URL, data=payload, method='PUT', headers={
    'Authorization': 'Basic ' + CREDS,
    'Content-Type': 'application/json; charset=utf-8'
})
with urllib.request.urlopen(req, timeout=60) as r:
    result = json.loads(r.read())

saved_content = result['content']['raw']
print(f"status={result['status']}  featured_media={result['featured_media']}  len={len(saved_content)}")

# ── verify saved content ──────────────────────────────────────────────────────
print("\n=== VERIFICATION ON SAVED CONTENT ===")

# Check for orphan << >>
dbl_lt = re.findall(r'<<', saved_content)
dbl_gt = re.findall(r'>>', saved_content)
print(f"Orphan << count: {len(dbl_lt)}  >> count: {len(dbl_gt)}")

# Check old-style SVG lists gone
old_ul = len(re.findall(r'list-style:none;padding-left:4px', saved_content))
print(f"Old SVG-style lists remaining: {old_ul}")

# Check new CSS-circle lists present
new_ul = len(re.findall(r'background-color:#16afa0; border-radius:50%', saved_content))
print(f"New CSS-circle bullets present: {new_ul}")

# Check image URLs still intact
img_urls = re.findall(r'src="(https://virtina\.com/wp-content/uploads/[^"]+)"', saved_content)
print(f"Image URLs ({len(img_urls)}):")
for url in img_urls:
    print(f"  {url}")

# Show first new-style list as proof
first_new_ul = re.search(r'<ul style="list-style:none; padding-left:0[^"]*".*?</ul>', saved_content, re.DOTALL)
if first_new_ul:
    print("\nFirst CSS-circle list (proof):")
    print(first_new_ul.group()[:600])

# ── save local copy ───────────────────────────────────────────────────────────
with open('C:/content-intel/new-42108-content.html', 'w', encoding='utf-8') as f:
    f.write(saved_content)
print("\nSaved -> new-42108-content.html")
print("\nDONE. Bullets fixed. Images still need Pexels API key.")
