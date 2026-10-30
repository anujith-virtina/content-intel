# -*- coding: utf-8 -*-
"""Wikimedia Commons fallback harvester for ECM post 283763.

Why this exists: the anonymous Openverse tier hard-throttled to 401/429 mid-run and
its quota does not reset quickly, and there is no PEXELS_API_KEY in .env. Commons is
the only remaining keyless source.

MUST-FOLLOW-RULES section 5 warns Commons is "not a substitute" for lifestyle
photography, which is true for family/caregiver subjects. Transit infrastructure is
the one subject where it plausibly holds up, so this harvests candidates and leaves
the judgement to the visual QA rather than assuming either way.

Licence filter is strict: CC0 and public domain ONLY. ECM posts carry no attribution
line, so CC BY and CC BY-SA are unusable no matter how good the photo is.

fetch only. Upload reuses transport_images.py, which already verifies dimensions,
mime type and the uploads path.
"""
import os, io, sys, json, time, requests
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.join(ROOT, "transport_candidates")
API = "https://commons.wikimedia.org/w/api.php"
UA = "ContentIntelBot/1.0 (ElderCareMatters editorial; contact GK@impelhub.com)"

QUERIES = {
    "featured": ["bus stop passengers waiting", "public bus interior seats", "senior citizen bus",
                 "transit bus boarding passenger", "bus passengers seated", "community shuttle bus"],
    "body1":    ["taxi passenger door", "car passenger seat person", "person entering car",
                 "volunteer driver car", "car door open street", "sedan passenger door open"],
    "body2":    ["people talking at table", "family at kitchen table", "notebook writing table",
                 "two people conversation table", "older people talking", "planning notes desk"],
}
# ECM bans clinical imagery outright, and wheelchairs specifically.
VETO = ["wheelchair", "wheel chair", "hospital", "ambulance", "nurse", "doctor", "clinic",
        "patient", "medical", "stretcher", "painting", "engraving", "drawing", "map",
        "diagram", "logo", "sign ", "timetable", "schematic", "poster", "coat of arms",
        "flower", "plant", "tree", "landscape", "monument", "statue"]
OK_LIC = ("cc0", "public domain", "pd-", "pdm")


def usable_licence(lic):
    l = (lic or "").strip().lower()
    return any(l.startswith(x) or x in l for x in OK_LIC) and "by" not in l.replace("by-", "")


def search(q, n=20):
    try:
        r = requests.get(API, headers={"User-Agent": UA}, timeout=45, params={
            "action": "query", "generator": "search", "gsrsearch": f"filetype:bitmap {q}",
            "gsrnamespace": "6", "gsrlimit": n, "prop": "imageinfo",
            "iiprop": "url|size|extmetadata", "iiurlwidth": "1600", "format": "json"})
        if r.status_code != 200:
            print(f"    commons HTTP {r.status_code} on {q!r}")
            return []
    except Exception as e:
        print(f"    commons error on {q!r}: {type(e).__name__}")
        return []
    out = []
    for p in ((r.json().get("query") or {}).get("pages", {})).values():
        ii = (p.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata", {})
        lic = em.get("LicenseShortName", {}).get("value") or ""
        title = (p.get("title") or "")[5:]
        if not usable_licence(lic):
            continue
        if any(v in title.lower() for v in VETO):
            continue
        if ii.get("width", 0) < 1100 or ii.get("height", 0) < 450:
            continue
        url = ii.get("thumburl") or ii.get("url")
        if not url:
            continue
        out.append({"url": url, "provider": "wikimedia", "license": lic,
                    "title": title[:90], "page": ii.get("descriptionurl", "")})
    return out


def to_webp(raw, path):
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    TW, TH = 1024, 536
    sw, sh = im.size
    if sw < TW or sh < 420:
        return None
    sc = max(TW / sw, TH / sh)
    im = im.resize((max(TW, int(sw * sc + .5)), max(TH, int(sh * sc + .5))), Image.LANCZOS)
    w, h = im.size
    im = im.crop(((w - TW) // 2, (h - TH) // 2, (w - TW) // 2 + TW, (h - TH) // 2 + TH))
    im.save(path, "WEBP", quality=82, method=6)
    return os.path.getsize(path)


def main():
    os.makedirs(CAND, exist_ok=True)
    manifest, seen = [], set()
    for slot, qs in QUERIES.items():
        got = 0
        for q in qs:
            if got >= 8:
                break
            for c in search(q):
                if got >= 8 or c["url"] in seen:
                    continue
                seen.add(c["url"])
                try:
                    raw = requests.get(c["url"], headers={"User-Agent": UA}, timeout=45).content
                except Exception:
                    continue
                if len(raw) < 12000:
                    continue
                name = f"wm_{slot}_{got:02d}.webp"
                try:
                    size = to_webp(raw, os.path.join(CAND, name))
                except Exception:
                    continue
                if not size:
                    continue
                c.update({"slot": slot, "file": name, "bytes": size, "query": q})
                manifest.append(c)
                got += 1
                print(f"  {slot} [{got}] {c['license'][:14]:16s} {size//1024:4d}KB {c['title'][:55]}")
            time.sleep(1)
        print(f"-- {slot}: {got}")
    json.dump(manifest, open(os.path.join(CAND, "manifest_wm.json"), "w", encoding="utf-8"), indent=1)
    print(f"\n{len(manifest)} candidates -> {CAND}")


if __name__ == "__main__":
    main()
