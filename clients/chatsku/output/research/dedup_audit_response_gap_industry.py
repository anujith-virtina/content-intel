# -*- coding: utf-8 -*-
"""8-gram dedup: response-gap-by-industry vs every live + draft ChatSKU post."""
import os, re, json, base64, urllib.request, html as H
ENV=r"C:\content-intel\.env"
for ln in open(ENV,encoding="utf-8"):
    ln=ln.strip()
    if ln and "=" in ln and not ln.startswith("#"):
        k,v=ln.split("=",1); os.environ.setdefault(k.strip(),v.strip())
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
AUTH=base64.b64encode(f"{os.environ['CHATSKU_WP_USERNAME']}:{os.environ['CHATSKU_WP_APP_PASSWORD']}".encode()).decode()
HD={"Authorization":"Basic "+AUTH,"User-Agent":UA}
DRAFT=r"C:\content-intel\clients\chatsku\output\drafts\response-gap-by-industry-2026-09-02.md"

def toks(s):
    s=re.sub(r'<[^>]+>',' ',s)
    return [w.lower() for w in re.findall(r"[A-Za-z0-9][A-Za-z0-9'/-]*", H.unescape(s))]

raw=open(DRAFT,encoding="utf-8").read()
raw=re.sub(r'^---.*?---\s*','',raw,count=1,flags=re.S)
raw=re.split(r'\n---\s*\n+##\s*Publishing notes',raw)[0]
mine=toks(raw)
mg={tuple(mine[i:i+8]) for i in range(len(mine)-7)}
print("draft 8-grams:", len(mg))

posts=[]
for st in ("publish","draft"):
    for pg in (1,2):
        u=f"https://chatsku.com/wp-json/wp/v2/posts?per_page=100&page={pg}&status={st}&context=edit&_fields=id,slug,content"
        try:
            posts += json.loads(urllib.request.urlopen(urllib.request.Request(u,headers=HD),timeout=90).read())
        except Exception:
            break
print("posts fetched:", len(posts))
tot=0
for p in posts:
    ow=toks(p["content"]["raw"])
    ov=mg & {tuple(ow[i:i+8]) for i in range(len(ow)-7)}
    if ov:
        tot+=len(ov)
        print(f"  {p['id']} {p['slug'][:45]}: {len(ov)}")
        for g in list(ov)[:6]: print("      ", " ".join(g))
print("TOTAL overlapping 8-grams:", tot)
