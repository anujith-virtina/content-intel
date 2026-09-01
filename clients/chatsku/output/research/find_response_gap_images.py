"""Find candidate images via Openverse (source=stocksnap) for the response-gap post.
featured: buyer alone at laptop at night, no reply (after-hours silence).
body1: sales team looking at backlog of unanswered inquiries on screens (daytime, RFQ delay).
body2: warehouse/distributor desk, laptop with live chat/assistant answering (response gap closed)."""
import json, urllib.request, urllib.parse, os, ssl
ctx = ssl._create_unverified_context()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
OUT = os.environ.get("OUT_DIR", os.getcwd())
QUERIES = {
    "feat": ["laptop desk night working late", "person laptop dark office night", "man laptop desk night", "office empty after hours"],
    "body1": ["sales team computer screens", "office team meeting computer screens", "business team reviewing documents office", "B2B sales conversation meeting"],
    "body2": ["distributor warehouse desk computer", "warehouse office laptop desk", "man laptop desk warehouse", "business quote document desk"],
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
            p = os.path.join(OUT, f"rg_{slot}_{idx}.jpg")
            if dl(u, p):
                manifest.append({"slot": slot, "i": idx, "url": u, "title": res.get("title", "")})
                print(f"[{slot}] {idx}: {res.get('title','')[:45]}  {u[:66]}"); idx += 1
            if sum(1 for m in manifest if m['slot'] == slot) >= 5: break
        if sum(1 for m in manifest if m['slot'] == slot) >= 5: break
json.dump(manifest, open(os.path.join(OUT, "rg_manifest.json"), "w"), indent=2)
for slot in QUERIES:
    print(slot, sum(1 for m in manifest if m['slot'] == slot))
