# -*- coding: utf-8 -*-
"""8-gram dedup: what-is-agentic-commerce vs every live + draft ChatSKU post."""
import os, re, json, base64, urllib.request, html as H
ENV=r"C:\content-intel\.env"
for ln in open(ENV,encoding="utf-8"):
    ln=ln.strip()
    if ln and "=" in ln and not ln.startswith("#"):
        k,v=ln.split("=",1); os.environ.setdefault(k.strip(),v.strip())
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
AUTH=base64.b64encode(f"{os.environ['CHATSKU_WP_USERNAME']}:{os.environ['CHATSKU_WP_APP_PASSWORD']}".encode()).decode()
HD={"Authorization":"Basic "+AUTH,"User-Agent":UA}
DRAFT=r"C:\content-intel\clients\chatsku\output\drafts\what-is-agentic-commerce-2026-09-07.md"

def toks(s):
    s=re.sub(r'<[^>]+>',' ',s)
    return [w.lower() for w in re.findall(r"[A-Za-z0-9][A-Za-z0-9'/-]*", H.unescape(s))]

def fetch():
    posts=[]; seen=set()
    for st in ("publish","draft","pending","private"):
        for pg in (1,2,3):
            u=(f"https://chatsku.com/wp-json/wp/v2/posts?per_page=100&page={pg}"
               f"&status={st}&context=edit&_fields=id,slug,content,status")
            try:
                batch=json.loads(urllib.request.urlopen(urllib.request.Request(u,headers=HD),timeout=90).read())
            except Exception as e:
                break
            if not batch: break
            for p in batch:
                if p["id"] not in seen:
                    seen.add(p["id"]); posts.append(p)
    return posts

if __name__=="__main__":
    raw=open(DRAFT,encoding="utf-8").read()
    raw=re.sub(r'^---.*?---\s*','',raw,count=1,flags=re.S)
    raw=re.split(r'\n---\s*\n+##\s*(Publishing notes|Meta|Images)',raw)[0]
    mine=toks(raw)
    mg={tuple(mine[i:i+8]) for i in range(len(mine)-7)}
    print("draft words:", len(mine), "| draft 8-grams:", len(mg))
    posts=fetch()
    print("corpus posts fetched:", len(posts),
          "(", sum(1 for p in posts if p.get('status')=='publish'), "live /",
          sum(1 for p in posts if p.get('status')!='publish'), "non-live )")
    tot=0
    for p in posts:
        if p["slug"].startswith("what-is-agentic-commerce"): continue
        ow=toks(p["content"]["raw"])
        ov=mg & {tuple(ow[i:i+8]) for i in range(len(ow)-7)}
        if ov:
            tot+=len(ov)
            print(f"  COLLISION {p['id']} {p['slug'][:50]} ({p.get('status')}): {len(ov)}")
            for g in sorted(ov)[:8]: print("       ", " ".join(g))
    print("TOTAL overlapping 8-grams:", tot)
    print("VERDICT:", "PASS" if tot==0 else "FAIL - reword collisions before push")
