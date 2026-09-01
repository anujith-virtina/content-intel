import json, re, os, ssl, base64, urllib.request
from pathlib import Path
ctx = ssl._create_unverified_context()
for ln in open(r"C:\content-intel\.env", encoding="utf-8"):
    ln = ln.strip()
    if ln and not ln.startswith("#") and "=" in ln:
        k, v = ln.split("=", 1); os.environ.setdefault(k.strip(), v.strip())
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
AUTH = base64.b64encode((os.environ["CHATSKU_WP_USERNAME"] + ":" + os.environ["CHATSKU_WP_APP_PASSWORD"]).encode()).decode()
H = {"Authorization": "Basic " + AUTH, "User-Agent": UA}
def norm(t):
    t = re.sub(r"<[^>]+>", " ", t); t = re.sub(r"&[a-z]+;", " ", t)
    t = re.sub(r"[^a-z0-9 ]", " ", t.lower()); return re.sub(r"\s+", " ", t).strip()
def grams(t, n=8):
    w = t.split(); return set(tuple(w[i:i+n]) for i in range(len(w)-n+1))
d = Path(r"C:\content-intel\clients\chatsku\output\drafts\b2b-commerce-evolution-11-stages-BUILD.md").read_text(encoding="utf-8")
d = re.sub(r"^---.*?---\s*", "", d, count=1, flags=re.S)
dg = grams(norm(d)); print("Draft 8-grams:", len(dg))
posts = []
for st in ("publish", "draft"):
    p = 1
    while True:
        u = f"https://chatsku.com/wp-json/wp/v2/posts?status={st}&per_page=50&page={p}&context=edit&_fields=id,slug,content"
        try:
            b = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=40, context=ctx).read())
        except Exception:
            break
        if not b:
            break
        posts += [(x["id"], x.get("slug", "?"), x.get("content", {}).get("raw") or x.get("content", {}).get("rendered", "")) for x in b]
        p += 1
print("Fetched", len(posts), "posts")
worst = 0
for pid, slug, c in posts:
    if pid == 1820:
        continue
    ov = dg & grams(norm(c))
    if ov:
        worst = max(worst, len(ov)); print(f"  OVERLAP {len(ov)} post {pid} ({slug})")
        for g in list(ov)[:5]:
            print("     ", " ".join(g))
print("RESULT: CLEAN, 0 overlap" if worst == 0 else f"RESULT: max overlap {worst}")
