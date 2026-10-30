# -*- coding: utf-8 -*-
"""Image sourcing + upload for ECM post 283763,
"Getting Around Safely: Transportation Options for Seniors Who No Longer Drive".

Two phases, deliberately separated because MUST-FOLLOW-RULES section 5 makes visual
QA mandatory. There is NO auto-picker: every resized candidate must be looked at
before phase 2 runs.

  fetch   -> sources 8+ candidates per slot from Openverse (cc0/pdm only, because
             ECM posts carry no attribution line so CC BY is unusable), downloads,
             validates, scale-to-cover + center-crops to exactly 1024x536, converts
             to WebP, writes candidates/ + candidates/manifest.json.

  upload  -> reads selection.json (written after the visual QA), uploads the three
             chosen files as image/webp, sets alt_text, then re-GETs each media item
             and BLOCKS unless width==1024, height==536, mime is image/webp and the
             source_url is on the ECM uploads path.

Scope guard: this script touches the media endpoint only. It never writes a post.
Credentials: ECM_WP_USERNAME / ECM_WP_APP_PASSWORD. Never another client's.
"""
import os, io, sys, json, time, base64, urllib.parse, urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
try:
    import requests
    from PIL import Image
except ImportError:
    print("BLOCKING: pip install requests Pillow")
    raise SystemExit(1)

ROOT = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(ROOT, '..', '..', '..', '..'))
IMGDIR = os.path.join(PROJ, 'clients', 'eldercarematters', 'output', 'images')
CAND = os.path.join(ROOT, 'transport_candidates')
SEL = os.path.join(ROOT, 'transport_selection.json')
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

env = {}
for line in open(os.path.join(PROJ, '.env'), encoding='utf-8'):
    line = line.strip()
    if '=' in line and not line.startswith('#'):
        k, v = line.split('=', 1)
        env[k] = v.strip().strip('"')

# Short, stock-photo-shaped queries. Long academic phrases return nothing on Openverse.
QUERIES = {
    "featured": ["senior bus", "bus stop", "public transport passengers", "bus interior seats",
                 "older woman bus", "city bus door", "passengers bus window"],
    "body1":    ["car passenger", "man opening car door", "getting into car", "car door open",
                 "woman car seat", "taxi passenger", "car front seat person"],
    "body2":    ["family kitchen table", "notebook calendar table", "two people talking table",
                 "planning notes table", "older couple table", "writing list table",
                 "phone notebook desk"],
}

# Rules s5 bans clinical imagery outright: assisted living is not a nursing home and a
# medicalised photo misrepresents it and frightens the reader. Nature/flowers also banned.
VETO = ["flower", "floral", "plant", "botanic", "bird", "animal", "dog", "cat", "landscape",
        "mountain", "forest", "beach", "sunset", "garden", "insect", "butterfly", "fish",
        "tree", "leaf", "petal", "painting", "engraving", "illustration", "drawing",
        "sculpture", "map", "manuscript", "print by", "lithograph", "watercolo", "etching",
        "portrait of a", "19th century", "18th century", "antique", "vintage poster",
        "wheelchair", "hospital", "nurse", "doctor", "clinic", "stethoscope", "patient",
        "medical", "ambulance", "surgery", "wheel chair"]
# Photo providers first. Museum and library scans are historical prints, not photography.
RANK = {"pexels": 120, "flickr": 90, "rawpixel": 80, "stocksnap": 100, "nappy": 85, "pixabay": 70,
        "wikimedia": 25, "smithsonian": 5, "met": 5, "nypl": 5, "clevelandmuseum": 5,
        "statensmuseum": 5, "brooklynmuseum": 5, "sciencemuseum": 5, "thorvaldsensmuseum": 5}


def veto(title):
    t = (title or "").lower()
    return any(w in t for w in VETO)


PEXELS_KEY = env.get("PEXELS_API_KEY", "")


def search_pexels(q, n=12):
    """Preferred source when a key exists: real editorial lifestyle photography,
    no attribution required, and no anonymous rate limit. Openverse is the keyless
    fallback and Commons is not a usable substitute for this subject (verified by
    visual QA 2026-09-16: empty foreign bus interiors and 1940s archival scans)."""
    if not PEXELS_KEY:
        return []
    try:
        r = requests.get("https://api.pexels.com/v1/search",
                         params={"query": q, "orientation": "landscape", "per_page": n},
                         headers={"Authorization": PEXELS_KEY, "User-Agent": UA}, timeout=30)
        if r.status_code != 200:
            print(f"    pexels {r.status_code} on {q!r}")
            return []
        return [{"url": p["src"]["large2x"], "provider": "pexels",
                 "title": (p.get("alt") or "")[:90],
                 "license": "Pexels License (free, no attribution required)",
                 "creator": (p.get("photographer") or "")[:60],
                 "page": p.get("url", "")}
                for p in r.json().get("photos", [])]
    except Exception as e:
        print(f"    pexels error on {q!r}: {type(e).__name__}")
        return []


def search(q, n=24, tries=6):
    """The anonymous Openverse tier intermittently answers a Cloudflare 429 challenge
    (content-type text/html) and then recovers a few seconds later. Returning [] on
    the first non-200 silently emptied every slot, so retry the status code too, not
    just exceptions."""
    for i in range(tries):
        try:
            r = requests.get("https://api.openverse.org/v1/images/",
                             params={"q": q, "license": "cc0,pdm", "page_size": n},
                             headers={"User-Agent": UA}, timeout=35)
            if r.status_code != 200:
                print(f"    openverse {r.status_code} on {q!r}, retry {i+1}/{tries}")
                time.sleep(12 * (i + 1))
                continue
            out = []
            for x in r.json().get("results", []):
                if not x.get("url") or veto(x.get("title")):
                    continue
                out.append({"url": x["url"], "provider": (x.get("provider") or "").lower(),
                            "title": (x.get("title") or "")[:90],
                            "license": x.get("license", ""),
                            "creator": (x.get("creator") or "")[:60],
                            "page": x.get("foreign_landing_url", "")})
            return out
        except Exception:
            time.sleep(12 * (i + 1))
    return []


def to_webp(raw, out_path):
    """scale-to-cover + center-crop to exactly 1024x536, LANCZOS, WebP q82."""
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    TW, TH = 1024, 536
    sw, sh = im.size
    if sw < TW or sh < 420:                      # too small to crop without softening
        return None
    scale = max(TW / sw, TH / sh)
    im = im.resize((max(TW, int(sw * scale + 0.5)), max(TH, int(sh * scale + 0.5))),
                   Image.LANCZOS)
    w, h = im.size
    im = im.crop(((w - TW) // 2, (h - TH) // 2, (w - TW) // 2 + TW, (h - TH) // 2 + TH))
    im.save(out_path, "WEBP", quality=82, method=6)
    return os.path.getsize(out_path)


def fetch():
    os.makedirs(CAND, exist_ok=True)
    manifest, seen = [], set()
    for slot, queries in QUERIES.items():
        got = 0
        for q in queries:
            if got >= 10:
                break
            pool = search_pexels(q) or search(q)
            for c in sorted(pool, key=lambda x: -RANK.get(x["provider"], 30)):
                if got >= 10 or c["url"] in seen:
                    continue
                seen.add(c["url"])
                try:
                    raw = requests.get(c["url"], headers={"User-Agent": UA}, timeout=35).content
                except Exception:
                    continue
                if len(raw) < 12000:
                    continue
                name = f"{slot}_{got:02d}.webp"
                try:
                    size = to_webp(raw, os.path.join(CAND, name))
                except Exception:
                    continue
                if not size:
                    continue
                c.update({"slot": slot, "file": name, "bytes": size, "query": q})
                manifest.append(c)
                got += 1
                print(f"  {slot} [{got:2d}] {c['provider']:12s} {size//1024:4d}KB  {c['title'][:60]}")
            time.sleep(8)          # pace to stay under the anonymous rate limit
        print(f"-- {slot}: {got} candidates")
    json.dump(manifest, open(os.path.join(CAND, "manifest.json"), "w", encoding="utf-8"), indent=1)
    thin = {s for s in QUERIES} - {m["slot"] for m in manifest}
    print(f"\n{len(manifest)} candidates -> {CAND}")
    if thin:
        print("EMPTY SLOTS:", thin)
    print("Now LOOK at every candidate, then write selection.json:")
    print('  [{"slot":"featured","file":"featured_03.webp","alt":"...","name":"..."} , ...]')


def _h():
    a = base64.b64encode(f"{env['ECM_WP_USERNAME']}:{env['ECM_WP_APP_PASSWORD']}".encode()).decode()
    return {"Authorization": "Basic " + a, "User-Agent": UA}


def upload():
    if not os.path.exists(SEL):
        print(f"BLOCKING: {SEL} missing. Do the visual QA first (rules s5).")
        raise SystemExit(1)
    sel = json.load(open(SEL, encoding="utf-8"))
    os.makedirs(IMGDIR, exist_ok=True)
    out = []
    for s in sel:
        alt = s["alt"]
        if not (80 <= len(alt) <= 150):
            print(f"BLOCKING: alt for {s['slot']} is {len(alt)} chars, need 80-150.")
            raise SystemExit(1)
        src = os.path.join(CAND, s["file"])
        dst = os.path.join(IMGDIR, s["name"])
        data = open(src, "rb").read()
        w, h = Image.open(io.BytesIO(data)).size
        if (w, h) != (1024, 536):
            print(f"BLOCKING: {s['file']} is {w}x{h}, expected 1024x536.")
            raise SystemExit(1)
        open(dst, "wb").write(data)
        r = requests.post("https://eldercarematters.com/wp-json/wp/v2/media",
                          headers={**_h(), "Content-Type": "image/webp",
                                   "Content-Disposition": f'attachment; filename="{s["name"]}"'},
                          data=data, timeout=180)
        if r.status_code not in (200, 201):
            print("BLOCKING: media upload failed", r.status_code, r.text[:300])
            raise SystemExit(1)
        mid = r.json()["id"]
        print(f"  uploaded {s['slot']} -> media {mid}")
        time.sleep(4)
        requests.post(f"https://eldercarematters.com/wp-json/wp/v2/media/{mid}",
                      headers={**_h(), "Content-Type": "application/json"},
                      data=json.dumps({"alt_text": alt}).encode(), timeout=90)
        time.sleep(4)
        v = requests.get(f"https://eldercarematters.com/wp-json/wp/v2/media/{mid}",
                         headers=_h(), timeout=90).json()
        det = v.get("media_details", {})
        ok = (det.get("width") == 1024 and det.get("height") == 536
              and v.get("mime_type") == "image/webp"
              and v.get("source_url", "").startswith("https://eldercarematters.com/wp-content/uploads/"))
        print(f"    verify {det.get('width')}x{det.get('height')} {v.get('mime_type')} alt={len(v.get('alt_text') or '')} -> {'OK' if ok else 'FAIL'}")
        if not ok:
            print("BLOCKING: uploaded media failed verification.")
            raise SystemExit(1)
        out.append({"slot": s["slot"], "media": mid, "url": v["source_url"], "alt": alt})
        time.sleep(4)
    json.dump(out, open(os.path.join(IMGDIR, "transport-283763.json"), "w", encoding="utf-8"), indent=1)
    print("\n" + json.dumps(out, indent=1))


if __name__ == "__main__":
    {"fetch": fetch, "upload": upload}[sys.argv[1] if len(sys.argv) > 1 else "fetch"]()
