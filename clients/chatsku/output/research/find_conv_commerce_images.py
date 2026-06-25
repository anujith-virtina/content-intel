"""Find candidate images via Openverse (source=stocksnap), short queries.
Downloads top candidates to scratchpad for visual QA. No API key needed."""
import json, urllib.request, urllib.parse, os, ssl
ctx = ssl._create_unverified_context()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
OUT = os.environ.get("OUT_DIR", os.getcwd())

QUERIES = {
    "featured": ["business meeting laptop desk", "office laptop buyer desk"],
    "body": ["warehouse office computer", "distribution office team computer"],
}

def search(q):
    url = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode({
        "q": q, "source": "stocksnap", "license_type": "all", "page_size": 6,
        "aspect_ratio": "wide", "orientation": "landscape",
    })
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
            return json.loads(r.read()).get("results", [])
    except Exception as e:
        print("  search err", q, e); return []

def dl(url, path):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
            data = r.read()
        if len(data) < 8000 or not (data[:2] == b'\xff\xd8' or data[:8] == b'\x89PNG\r\n\x1a\n'):
            return False
        with open(path, "wb") as f:
            f.write(data)
        return True
    except Exception as e:
        print("  dl err", e); return False

idx = 0
manifest = []
for slot, qs in QUERIES.items():
    seen = set()
    for q in qs:
        for res in search(q):
            u = res.get("url") or res.get("thumbnail")
            if not u or u in seen:
                continue
            seen.add(u)
            p = os.path.join(OUT, f"cand_{slot}_{idx}.jpg")
            if dl(u, p):
                manifest.append({"slot": slot, "i": idx, "url": u, "path": p,
                                 "title": res.get("title", ""), "src": res.get("source", "")})
                print(f"[{slot}] {idx}: {res.get('title','')[:50]}  {u[:70]}")
                idx += 1
            if sum(1 for m in manifest if m['slot'] == slot) >= 4:
                break
        if sum(1 for m in manifest if m['slot'] == slot) >= 4:
            break

with open(os.path.join(OUT, "img_manifest.json"), "w") as f:
    json.dump(manifest, f, indent=2)
print("\nManifest:", len([m for m in manifest if m['slot']=='featured']), "featured,",
      len([m for m in manifest if m['slot']=='body']), "body")
