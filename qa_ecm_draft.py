# -*- coding: utf-8 -*-
"""ECM pre-publish QA. Enforces MUST-FOLLOW-RULES sections 1-6, 8."""
import re,sys,html,os
BANNED_SUBSTR=["the elderly","suffering from dementia","placement","facilit"]
BLOCKED=["$2,563","2563","no income test"]
COMPETITORS=["aplaceformom","caring.com","senioradvisor","agingcare","care.com","seniorliving.com","assistedlivinglocators"]
DEAD=["/adult-day-care/","/skilled-nursing/","/home-health-care/","/senior-centers/","/veterans-benefits/",
      "/adult-day-care-services-for-seniors/","/adult-day-care-centers/","/adult-day-services/"]
NOLINK=["cms.gov","medicare.gov"]
ACL_OK="eldercare.acl.gov"
DIRS=["/assisted-living/","/home-care-providers/","/memory-care/","/elder-law-attorneys/","/care-management/"]
p=sys.argv[1]
h=open(p,encoding='utf-8').read()
fails=[];warns=[];oks=[]
def F(m):fails.append(m)
def W(m):warns.append(m)
def O(m):oks.append(m)

body=re.sub(r'<style.*?</style>','',h,flags=re.S|re.I)
body=re.sub(r'<!--.*?-->','',body,flags=re.S)
txt=html.unescape(re.sub(r'<[^>]+>',' ',body))
txt=re.sub(r'\s+',' ',txt)
wc=len(txt.split())
(O if 1500<=wc<=2400 else F)(f"word count {wc} (need 1500-2400)")

h2=[html.unescape(re.sub('<[^>]+>','',m)).strip() for m in re.findall(r'<h2[^>]*>(.*?)</h2>',body,re.S|re.I)]
h3=[html.unescape(re.sub('<[^>]+>','',m)).strip() for m in re.findall(r'<h3[^>]*>(.*?)</h3>',body,re.S|re.I)]
for req in ["Introduction","People Also Ask","Conclusion","Frequently Asked Questions"]:
    (O if req in h2 else F)(f"required H2 '{req}'")
if all(x in h2 for x in ["Introduction","People Also Ask","Conclusion","Frequently Asked Questions"]):
    idx=[h2.index(x) for x in ["Introduction","People Also Ask","Conclusion","Frequently Asked Questions"]]
    (O if idx==sorted(idx) else F)(f"required H2 order {idx}")

# accordion
d_o=len(re.findall(r'<details',body,re.I));d_s=len(re.findall(r'<summary',body,re.I));d_c=len(re.findall(r'</details>',body,re.I))
(O if d_o==d_s==d_c and d_o>=5 else F)(f"details/summary/close = {d_o}/{d_s}/{d_c} (need equal, 5-8)")
(O if d_o<=8 else F)(f"FAQ count {d_o} <= 8")
insum=re.findall(r'<summary[^>]*>(.*?)</summary>',body,re.S|re.I)
(O if insum and all('<h3' in s.lower() for s in insum) else F)("every <summary> contains an <h3>")
# PAA flat
paa=body[body.find('People Also Ask'):body.find('Conclusion')] if 'People Also Ask' in body else ''
(O if '<details' not in paa.lower() else F)("People Also Ask is flat (no accordion)")

# em dash
ems=h.count('—')+h.count('&mdash;')+h.count('&#8212;')
(O if ems==0 else F)(f"em dashes = {ems}")

low=txt.lower()
for b in BANNED_SUBSTR:
    n=len(re.findall(r''+b+r'',low)) if b=='placement' else low.count(b)
    (O if n==0 else F)(f"banned '{b}' x{n}")
for b in BLOCKED:
    (O if b.lower() not in low else F)(f"blocked claim '{b}'")
for c in COMPETITORS:
    (O if c not in h.lower() else F)(f"competitor '{c}'")

# sentences / paragraphs
pbody=re.sub(r'<(h[234]|summary)[^>]*>.*?</\1>',' ',body,flags=re.S|re.I)
paras=re.findall(r'<p[^>]*>(.*?)</p>',pbody,re.S|re.I)
badp=0;longs=[]
for pr in paras:
    t=html.unescape(re.sub('<[^>]+>','',pr)).strip()
    s=[x for x in re.split(r'(?<=[.!?])\s+',t) if x.strip()]
    s=[x for x in s if len(x.split())>=4]  # ignore 'No.' style direct answers
    if len(s)>=4: badp+=1
    for x in s:
        if len(x.split())>25: longs.append(x[:70])
(O if badp==0 else F)(f"paragraphs with 4+ sentences = {badp}")
(O if not longs else W)(f"sentences over 25 words = {len(longs)}"+("; e.g. "+longs[0] if longs else ""))

# title case-ish on H2
bad_tc=[x for x in h2 if re.match(r'^[a-z]',x)]
(O if not bad_tc else F)(f"H2 not Title Case: {bad_tc}")

# links
links=re.findall(r'<a\s[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',body,re.S|re.I)
internal=[(u,html.unescape(re.sub('<[^>]+>','',a)).strip()) for u,a in links if 'eldercarematters.com' in u or u.startswith('/')]
external=[(u,html.unescape(re.sub('<[^>]+>','',a)).strip()) for u,a in links if 'eldercarematters.com' not in u and not u.startswith('/') and u.startswith('http')]
(O if 5<=len(internal)<=8 else F)(f"internal links = {len(internal)} (need 5-8)")
(O if len(external)<=2 else F)(f"external links = {len(external)} (max 2)")
dhit=[u for u,_ in internal if any(x in u for x in DEAD)]
(O if not dhit else F)(f"DEAD links used: {dhit}")
nl=[u for u,_ in links if any(x in u for x in NOLINK)]
nl+=[u for u,_ in links if 'acl.gov' in u and ACL_OK not in u]
(O if not nl else F)(f"forbidden domains linked: {nl}")
dircount=sum(1 for u,_ in internal if any(x in u for x in DIRS))
(O if dircount>=3 else F)(f"directory-category links = {dircount} (need >=3)")
blogct=sum(1 for u,_ in internal if 'eldercarematters.com' in u and not any(x in u for x in DIRS))
(O if blogct>=2 else F)("earlier-blog-post links = "+str(blogct)+" (need >=2)")
for u,a in external:
    tag=[m for m in re.findall(r'<a\s[^>]*>',body,re.I) if u in m]
    ok=all('target="_blank"' in t and 'noopener' in t for t in tag) if tag else False
    (O if ok else F)(f"external target/rel on {u[:45]}")
allhref=re.findall(r'href="([^"]*)"',body,re.I)
placeholder=[u for u in allhref if (not u.startswith("https://")) or ("TODO" in u.upper())]
(O if not placeholder else F)("placeholder/relative hrefs: "+str(placeholder))
badanchor=[(u,a) for u,a in internal if not (2<=len(a.split())<=5)]
(O if not badanchor else W)(f"anchors outside 2-5 words: {badanchor}")

# style block !important discipline
st=" ".join(re.findall(r'<style.*?</style>',h,flags=re.S|re.I))
decls=re.findall(r'(font-size|font-weight|line-height|color)\s*:\s*[^;}]+[;}]',st)
noimp=[d for d in re.findall(r'(?:font-size|line-height)\s*:\s*[^;}]+[;}]',st) if '!important' not in d]
(O if not noimp else F)(f"typography without !important: {len(noimp)} -> {noimp[:3]}")
(O if '.single-post .entry-content' in st else F)("style block scopes .single-post .entry-content")

# images
(O if '<img' not in body.lower() else W)("no raw <img> in draft (publisher inserts)")

print(f"\n{'='*66}\nECM QA  {os.path.basename(p)}\n{'='*66}")
for m in oks: print("  PASS  "+m)
for m in warns: print("  WARN  "+m)
for m in fails: print("  FAIL  "+m)
print(f"\nH2s ({len(h2)}): "+" | ".join(h2))
print(f"\nInternal links:")
for u,a in internal: print(f"   {a!r:38} -> {u}")
print(f"External links:")
for u,a in external: print(f"   {a!r:38} -> {u}")
print(f"\n{'='*66}\n{len(fails)} FAIL, {len(warns)} WARN, {len(oks)} PASS\n{'='*66}")
sys.exit(1 if fails else 0)
