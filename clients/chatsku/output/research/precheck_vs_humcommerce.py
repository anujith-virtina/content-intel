import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import curlshim, subprocess
import re,json,base64,urllib.request,urllib.error,html,time,sys
env={}
for l in open(r'C:\content-intel\.env',encoding='utf-8'):
    l=l.strip()
    if '=' in l and not l.startswith('#'):
        k,v=l.split('=',1); env[k]=v.strip().strip('"')
A=base64.b64encode(f"{env['CHATSKU_WP_USERNAME']}:{env['CHATSKU_WP_APP_PASSWORD']}".encode()).decode()
H={'Authorization':'Basic '+A,'User-Agent':'Mozilla/5.0'}
raw=open(r'C:\content-intel\clients\chatsku\output\drafts\chatsku-vs-humcommerce-2026-11-05.md',encoding='utf-8').read()
body=raw.split('<!-- BUILD NOTES')[0]
links=sorted(set(re.findall(r'\]\((https?://[^)]+|/[^)]+)\)',body)))
txt=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',body)
txt=re.sub(r'[#*|>`]',' ',txt)
# sentences over 20 words
long=[s for s in re.split(r'(?<=[.?!])\s+',re.sub(r'\n+',' ',txt)) if len(s.split())>20 and '|' not in s]
print('long sentences',len(long)); [print('  ',len(s.split()),s[:110]) for s in long[:12]]
# 8-gram
def W(x): return re.sub(r'[^a-z0-9 ]',' ',x.lower()).split()
mine=W(txt); g=set(tuple(mine[i:i+8]) for i in range(len(mine)-7))
for pid in [294,3956,3461,4090,4078]:
    for typ in ('posts','pages'):
        try:
            d=json.load(urllib.request.urlopen(urllib.request.Request(f'https://chatsku.com/wp-json/wp/v2/{typ}/{pid}?context=edit&_fields=id,slug,content',headers=H),timeout=60)); break
        except Exception as e: d=None
    if not d: print(pid,'fetch failed'); continue
    o=W(html.unescape(re.sub(r'<[^>]+>',' ',d['content']['raw'] or '')))
    og=set(tuple(o[i:i+8]) for i in range(len(o)-7)); c=g&og
    print(pid,d['slug'][:40],'overlap',len(c)); [print('    ',' '.join(x)) for x in list(c)[:3]]
    time.sleep(2)
for u in links:
    full=u if u.startswith('http') else 'https://chatsku.com'+u
    code=subprocess.run(['curl','-s','-o','NUL','-w','%{http_code}','-A',curlshim.UA,full],capture_output=True,text=True).stdout
    print(code,full); time.sleep(2)
