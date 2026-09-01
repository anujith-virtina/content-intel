"""8-gram verbatim-overlap audit: new draft vs all live/draft ChatSKU posts (MUST-FOLLOW §1D)."""
import json, re, os, ssl, base64, urllib.request
from pathlib import Path

ctx = ssl._create_unverified_context()
env = r"C:\content-intel\.env"
if os.path.exists(env):
    for ln in open(env, encoding="utf-8"):
        ln = ln.strip()
        if ln and not ln.startswith("#") and "=" in ln:
            k, v = ln.split("=", 1); os.environ.setdefault(k.strip(), v.strip())
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
AUTH = base64.b64encode(f"{os.environ['CHATSKU_WP_USERNAME']}:{os.environ['CHATSKU_WP_APP_PASSWORD']}".encode()).decode()
H = {"Authorization": f"Basic {AUTH}", "User-Agent": UA}

def norm(t):
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'&[a-z]+;', ' ', t)
    t = re.sub(r'[^a-z0-9 ]', ' ', t.lower())
    return re.sub(r'\s+', ' ', t).strip()

def grams(t, n=8):
    w = t.split()
    return set(tuple(w[i:i+n]) for i in range(len(w)-n+1))

draft = Path(r"C:\content-intel\clients\chatsku\output\drafts\rfq-form-best-practices-2026-07-17.md").read_text(encoding="utf-8")
draft = re.sub(r'^---.*?---\s*', '', draft, count=1, flags=re.S)
draft = re.sub(r'<!--.*?-->', '', draft, flags=re.S)
dg = grams(norm(draft))
print(f"Draft 8-grams: {len(dg)}")

posts = []
for st in ("publish", "draft"):
    page = 1
    while True:
        url = f"https://chatsku.com/wp-json/wp/v2/posts?status={st}&per_page=50&page={page}&context=edit&_fields=id,slug,content"
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=40, context=ctx)
            batch = json.loads(r.read())
        except Exception as e:
            print(f"  ({st} p{page} stop: {e})"); break
        if not batch: break
        posts += [(p["id"], p.get("slug", "?"), p.get("content", {}).get("raw") or p.get("content", {}).get("rendered", "")) for p in batch]
        page += 1

print(f"Fetched {len(posts)} posts\n")
worst = 0
for pid, slug, content in posts:
    if pid == 1684:
        continue
    ov = dg & grams(norm(content))
    if ov:
        worst = max(worst, len(ov))
        print(f"  OVERLAP {len(ov):3}  post {pid} ({slug})")
        for g in list(ov)[:4]:
            print("      ", " ".join(g))
if worst == 0:
    print("RESULT: 0 verbatim 8-gram overlap with any post. CLEAN (§1D pass).")
else:
    print(f"RESULT: max overlap {worst} 8-grams — review above.")
