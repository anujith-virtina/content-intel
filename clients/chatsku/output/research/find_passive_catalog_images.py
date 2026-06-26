"""Find candidate images via Openverse (source=stocksnap) for the passive-catalog post.
featured+passive: buyer at laptop/desk (evening/struggle). active: modern B2B sales/chat scene."""
import json, urllib.request, urllib.parse, os, ssl
ctx = ssl._create_unverified_context()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
OUT = os.environ.get("OUT_DIR", os.getcwd())
QUERIES = {
    "passive": ["man laptop desk night", "frustrated laptop office", "person laptop documents desk", "working late laptop"],
    "active": ["smartphone business person office", "modern office laptop smiling", "businessman phone laptop desk", "office worker computer headset"],
}
def search(q):
    url = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode({
        "q": q, "source": "stocksnap", "page_size": 6, "aspect_ratio": "wide", "orientation": "landscape"})
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=25, context=ctx) as r:
            return json.loads(r.read()).get("results", [])
    except Exception as e:
        print("  err", q, e); return []
def dl(url, path):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=25, context=ctx) as r:
            data = r.read()
        if len(data) < 8000 or not (data[:2] == b'\xff\xd8' or data[:8] == b'\x89PNG\r\n\x1a\n'): return False
        open(path, "wb").write(data); return True
    except Exception: return False
idx = 0; manifest = []
for slot, qs in QUERIES.items():
    seen = set()
    for q in qs:
        for res in search(q):
            u = res.get("url") or res.get("thumbnail")
            if not u or u in seen: continue
            seen.add(u)
            p = os.path.join(OUT, f"pc_{slot}_{idx}.jpg")
            if dl(u, p):
                manifest.append({"slot": slot, "i": idx, "url": u, "title": res.get("title", "")})
                print(f"[{slot}] {idx}: {res.get('title','')[:45]}  {u[:66]}"); idx += 1
            if sum(1 for m in manifest if m['slot'] == slot) >= 5: break
        if sum(1 for m in manifest if m['slot'] == slot) >= 5: break
json.dump(manifest, open(os.path.join(OUT, "pc_manifest.json"), "w"), indent=2)
print("\n", sum(1 for m in manifest if m['slot']=='passive'), "passive,", sum(1 for m in manifest if m['slot']=='active'), "active")
