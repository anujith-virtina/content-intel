import re
with open(r'C:\content-intel\clients\virtina\output\drafts\ecommerce-platform-seo-b2b-guide-2026-06-03.html', encoding='utf-8') as f:
    html = f.read()
html_no_table = re.sub(r'<table.*?</table>', '', html, flags=re.DOTALL)
html_no_list = re.sub(r'<ul style="list-style:none;padding-left:4px.*?</ul>', '', html_no_table, flags=re.DOTALL)
paras = re.findall(r'<p[^>]*>(.*?)</p>', html_no_list, re.DOTALL)
p_clean = [re.sub(r'<[^>]+>', '', p).strip() for p in paras if len(re.sub(r'<[^>]+>', '', p).strip().split()) > 10]

def sent_count(t):
    return len([s for s in re.split(r'(?<=[.!?])\s+(?=[A-Z])', t) if len(s.split()) > 4])

over3 = [p for p in p_clean if sent_count(p) > 3]
print('=== PARAGRAPHS OVER 3 SENTENCES ===')
for p in over3:
    print(f'  [{sent_count(p)} sents, {len(p.split())} words]: {repr(p[:300])}')
    print()

over60 = [p for p in p_clean if len(p.split()) > 60]
print('=== PARAGRAPHS OVER 60 WORDS ===')
for p in over60:
    print(f'  [{len(p.split())} words]: {repr(p[:300])}')
    print()
