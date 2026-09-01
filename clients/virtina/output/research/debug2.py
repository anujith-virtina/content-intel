import re
with open(r'C:\content-intel\clients\virtina\output\drafts\ecommerce-platform-seo-b2b-guide-2026-06-03.html', encoding='utf-8') as f:
    html = f.read()

# Find the raw <p> that contains TOC-like text
paras_raw = re.findall(r'<p[^>]*>.*?</p>', html, re.DOTALL)
for p in paras_raw:
    if 'Why does your platform' in p or 'Which platforms rank' in p:
        print(repr(p[:500]))
        print()

# Also find position in html
pos = html.find('Which platforms rank best')
print(f"\nPosition of 'Which platforms rank best': {pos}")
print(repr(html[max(0,pos-300):pos+100]))
