# -*- coding: utf-8 -*-
"""Image sourcing + upload for the ElderCareMatters post
"Who Pays for Respite Care: A Guide to Funding Options"  (slug: who-pays-for-respite-care)

Two phases, deliberately separated because MUST-FOLLOW-RULES.md section 5 makes
visual QA mandatory. There is NO auto-picker. A human (or an agent with image-read
capability) must look at every resized candidate before phase 2 runs.

  phase 1:  python respite_images.py fetch
            -> sources >=6 candidates per slot, downloads, validates, scale-to-cover
               + center-crops to exactly 1024x536, converts to WebP, writes
               candidates/ + candidates/manifest.json (provider, license, creator,
               source page) for visual QA.

  phase 2:  python respite_images.py upload
            -> reads selection.json (written by whoever did the visual QA),
               copies the 3 chosen files into output/images/ under descriptive
               names, uploads to ECM /wp/v2/media as image/webp, sets alt_text,
               then GETs each media item and BLOCKS unless
               width==1024, height==536, mime_type=="image/webp", and the
               source_url is on https://eldercarematters.com/wp-content/uploads/.

Scope guard: this script touches /wp/v2/media ONLY. It never writes a post.

Credentials: ECM_WP_USERNAME / ECM_WP_APP_PASSWORD from C:\\content-intel\\.env.
Never another client's keys.

Rules enforced here (section 5):
  - 1024x536 WebP for all three images, featured and body alike
  - alt text 80..150 chars on every image, featured included
  - a keyword prefilter drops obviously clinical and nature/landscape results.
    It is a safety net, NOT a substitute for visual QA. Rejected on post 283684
    for clinical imagery; generic mismatched stock rejected on post 42349.
"""
import os, sys, io, ssl, json, time, base64, shutil, urllib.parse, urllib.request, urllib.error

ROOT = r"C:\content-intel"
ENV_PATH = os.path.join(ROOT, ".env")
if os.path.exists(ENV_PATH):
    for _ln in open(ENV_PATH, encoding="utf-8-sig"):
        _ln = _ln.strip()
        if _ln and not _ln.startswith("#") and "=" in _ln:
            _k, _v = _ln.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

ctx = ssl._create_unverified_context()
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
WP = "https://eldercarematters.com/wp-json/wp/v2"

BASE = os.path.join(ROOT, r"clients\eldercarematters\output")
CAND_DIR = os.path.join(BASE, r"research\respite_img_candidates")
IMG_DIR = os.path.join(BASE, "images")
MANIFEST = os.path.join(CAND_DIR, "manifest.json")
SELECTION = os.path.join(CAND_DIR, "selection.json")
STATE = os.path.join(BASE, r"research\respite_media_state.json")

W, H = 1024, 536

# ---------------------------------------------------------------- queries
# Non-clinical, non-nature. Funding + paperwork + two generations at home.
#
# QUERY LENGTH MATTERS. Probed against the live Openverse API 2026-09-09:
#   q="adult daughter elderly mother talking home" + aspect_ratio=wide
#      + orientation=landscape + license=cc0,pdm  -> 0 results
#   q="elderly mother daughter" + license=cc0,pdm -> 4 results
#   q="paperwork calculator" (no license filter)  -> 240 results
# So: keep Openverse queries to 2-3 words and do NOT send aspect_ratio or
# orientation (they are effectively an AND filter that empties the set).
# Pexels tolerates longer natural-language queries, so it gets the richer ones.
QUERIES = {
    "featured": [
        # pexels-friendly (long) first, openverse-friendly (short) after
        "adult daughter and senior mother at home",
        "older parent and adult child talking",
        "family two generations kitchen table",
        "elderly mother daughter",
        "senior father son",
        "family grandmother home",
    ],
    "body1": [
        "woman on phone call at home",
        "man making a phone call at desk",
        "person on phone taking notes",
        "phone call notebook",
        "woman smartphone home",
        "person telephone desk",
    ],
    "body2": [
        "documents calculator on a table",
        "woman with laptop and paperwork at kitchen table",
        "reviewing bills and documents at home",
        "paperwork calculator",
        "insurance policy documents",
        "signing papers desk",
    ],
}

CLINICAL = ("hospital", "wheelchair", "nurse", "nursing", "doctor", "clinic", "clinical",
            "medical", "medicine", "patient", "stethoscope", "scrub", "surgery", "surgical",
            "ward", "ambulance", "syringe", "pill", "drug", "therapy", "x-ray", "dementia care unit")
NATURE = ("flower", "floral", "landscape", "mountain", "beach", "forest", "garden", "sunset",
          "sunrise", "tree", "field", "sky", "lake", "river", "bloom", "petal", "leaf")

PREFERRED_PROVIDERS = ["flickr", "wikimedia", "rawpixel", "smithsonian", "nappy", "stocksnap"]


def _get(url, headers=None, timeout=30):
    r = urllib.request.Request(url, headers=headers or {"User-Agent": UA})
    return urllib.request.urlopen(r, timeout=timeout, context=ctx)


def clean(res_text):
    t = (res_text or "").lower()
    if any(k in t for k in CLINICAL):
        return False, "clinical keyword"
    if any(k in t for k in NATURE):
        return False, "nature keyword"
    return True, ""


# ---------------------------------------------------------------- sources
def search_pexels(q, n=6):
    key = os.environ.get("PEXELS_API_KEY")
    if not key:
        return []
    url = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode(
        {"query": q, "orientation": "landscape", "per_page": n})
    try:
        data = json.loads(_get(url, {"Authorization": key, "User-Agent": UA}).read())
    except Exception as e:
        print("   pexels err:", q, e); return []
    out = []
    for p in data.get("photos", []):
        out.append({
            "provider": "pexels", "license": "Pexels License (free, no attribution required)",
            "creator": p.get("photographer", ""), "page": p.get("url", ""),
            "title": p.get("alt", ""), "url": (p.get("src") or {}).get("large2x", ""),
        })
    return out


def search_openverse(q, n=10):
    # NOTE: source=stocksnap now returns 0 results (logged 2026). General cc0/pdm query
    # plus provider ranking plus visual QA is the working approach.
    # Do NOT add aspect_ratio/orientation: probed 2026-09-09, they zero out the
    # result set on this subject. Cropping to 1024x536 handles shape anyway.
    # license stays cc0,pdm: ECM posts carry no attribution line, so CC BY and
    # CC BY-SA are not usable, and NC is not usable on a commercial directory.
    url = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(
        {"q": q, "license": "cc0,pdm", "page_size": n})
    try:
        data = json.loads(_get(url).read())
    except Exception as e:
        print("   openverse err:", q, e); return []
    out = []
    for r in data.get("results", []):
        out.append({
            "provider": r.get("provider", "openverse"),
            "license": (r.get("license", "") + " " + (r.get("license_version") or "")).strip(),
            "creator": r.get("creator", ""), "page": r.get("foreign_landing_url", ""),
            "title": r.get("title", ""), "url": r.get("url", ""),
        })
    rank = {p: i for i, p in enumerate(PREFERRED_PROVIDERS)}
    out.sort(key=lambda x: rank.get(x["provider"], 99))
    return out


def search_unsplash(q, n=6):
    # Official API only. source.unsplash.com is DEPRECATED and returns random
    # unrelated images -- never use it.
    key = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not key:
        return []
    url = "https://api.unsplash.com/search/photos?" + urllib.parse.urlencode(
        {"query": q, "orientation": "landscape", "per_page": n})
    try:
        data = json.loads(_get(url, {"Authorization": "Client-ID " + key, "User-Agent": UA}).read())
    except Exception as e:
        print("   unsplash err:", q, e); return []
    out = []
    for p in data.get("results", []):
        out.append({
            "provider": "unsplash", "license": "Unsplash License",
            "creator": (p.get("user") or {}).get("name", ""),
            "page": (p.get("links") or {}).get("html", ""),
            "title": p.get("alt_description") or "", "url": (p.get("urls") or {}).get("regular", ""),
        })
    return out


# ---------------------------------------------------------------- image ops
def to_webp_1024x536(raw, out_path):
    """scale-to-cover + center-crop to exactly 1024x536, save WebP."""
    from PIL import Image
    im = Image.open(io.BytesIO(raw))
    ow, oh = im.size
    im = im.convert("RGB")
    scale = max(W / ow, H / oh)
    nw, nh = max(W, int(round(ow * scale))), max(H, int(round(oh * scale)))
    im = im.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - W) // 2, (nh - H) // 2
    im = im.crop((left, top, left + W, top + H))
    assert im.size == (W, H), im.size
    im.save(out_path, "WEBP", quality=82, method=6)
    return ow, oh


def fetch():
    try:
        import PIL  # noqa
    except ImportError:
        sys.exit("BLOCKING: Pillow is required.  pip install pillow")
    if not (os.environ.get("PEXELS_API_KEY") or os.environ.get("UNSPLASH_ACCESS_KEY")):
        # Probed 2026-09-09: the Openverse CC0/PDM pool for this subject is
        # 0-16 mostly irrelevant results per query, nowhere near the 6+ usable
        # candidates per slot that section 5 requires. Openverse alone will not
        # clear visual QA here.
        print("WARNING: no PEXELS_API_KEY or UNSPLASH_ACCESS_KEY in the environment.")
        print("Openverse CC0/PDM alone is too thin for this subject. Expect to fail")
        print("the 6-candidates-per-slot bar. Set PEXELS_API_KEY and re-run.")
        if os.environ.get("ALLOW_OPENVERSE_ONLY") != "1":
            sys.exit("BLOCKING: set PEXELS_API_KEY, or ALLOW_OPENVERSE_ONLY=1 to try anyway.")
    os.makedirs(CAND_DIR, exist_ok=True)
    manifest, idx = [], 0
    for slot, queries in QUERIES.items():
        print("\n==", slot)
        seen, kept = set(), 0
        for q in queries:
            if kept >= 8:
                break
            results = search_pexels(q) + search_unsplash(q) + search_openverse(q)
            for r in results:
                if kept >= 8:
                    break
                u = r.get("url")
                if not u or u in seen:
                    continue
                seen.add(u)
                ok, why = clean(r.get("title", "") + " " + q)
                if not ok:
                    print(f"   skip ({why}): {r.get('title','')[:50]}")
                    continue
                try:
                    raw = _get(u).read()
                except Exception as e:
                    print("   dl fail:", e); continue
                if len(raw) < 8000:
                    print("   too small:", len(raw)); continue
                sig_ok = raw[:2] == b"\xff\xd8" or raw[:8] == b"\x89PNG\r\n\x1a\n" or raw[:4] == b"RIFF"
                if not sig_ok:
                    print("   bad signature"); continue
                key = f"{slot}_{idx:02d}"
                path = os.path.join(CAND_DIR, key + ".webp")
                try:
                    ow, oh = to_webp_1024x536(raw, path)
                except Exception as e:
                    print("   resize fail:", e); continue
                manifest.append({"key": key, "slot": slot, "query": q, "file": path,
                                 "orig": [ow, oh], "bytes": os.path.getsize(path), **r})
                print(f"   [{key}] {r['provider']:<10} {r.get('title','')[:44]}")
                idx += 1; kept += 1
                time.sleep(1)   # be polite; Openverse/Wikimedia 429 easily
        print(f"   -> {kept} candidates for {slot}")
    json.dump(manifest, open(MANIFEST, "w", encoding="utf-8"), indent=2)
    thin = [s for s in QUERIES if sum(1 for m in manifest if m["slot"] == s) < 6]
    if thin:
        print("\nBLOCKING: fewer than 6 candidates for:", ", ".join(thin))
        print("Section 5 requires 6+ per slot before visual QA. Add a source key and re-run.")
    print("\nmanifest:", MANIFEST)
    print("NEXT: LOOK AT EVERY .webp IN", CAND_DIR)
    print("Then write selection.json:")
    print(json.dumps({s: {"candidate": f"{s}_00", "filename": f"who-pays-respite-{s}.webp",
                          "alt": "<80-150 chars, written against the image actually chosen>"}
                      for s in QUERIES}, indent=2))


# ---------------------------------------------------------------- upload
def _auth_headers():
    u, a = os.environ["ECM_WP_USERNAME"], os.environ["ECM_WP_APP_PASSWORD"]   # ECM only
    return {"Authorization": "Basic " + base64.b64encode(f"{u}:{a}".encode()).decode(),
            "User-Agent": UA}


def _req(url, data=None, headers=None, method="GET"):
    r = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    return urllib.request.urlopen(r, timeout=90, context=ctx)


def upload():
    if not os.path.exists(SELECTION):
        sys.exit(f"BLOCKING: no visual QA selection at {SELECTION}. Run fetch, LOOK at the "
                 f"candidates, then write selection.json.")
    sel = json.load(open(SELECTION, encoding="utf-8"))
    if set(sel) != {"featured", "body1", "body2"}:
        sys.exit("BLOCKING: selection.json needs exactly featured, body1, body2.")
    os.makedirs(IMG_DIR, exist_ok=True)
    H_ = _auth_headers()
    state = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}

    # --- pre-flight validation, all blocking
    from PIL import Image
    alts = []
    for slot, s in sel.items():
        src = os.path.join(CAND_DIR, s["candidate"] + ".webp")
        if not os.path.exists(src):
            sys.exit(f"BLOCKING: {slot}: candidate file missing: {src}")
        alt = (s.get("alt") or "").strip()
        if not (80 <= len(alt) <= 150):
            sys.exit(f"BLOCKING: {slot}: alt text is {len(alt)} chars, must be 80-150.")
        if "<" in alt or "placeholder" in alt.lower():
            sys.exit(f"BLOCKING: {slot}: alt text looks like a placeholder.")
        alts.append(alt)
        im = Image.open(src)
        if im.size != (W, H) or im.format != "WEBP":
            sys.exit(f"BLOCKING: {slot}: {im.size} {im.format}, must be (1024, 536) WEBP.")
    if len(set(alts)) != 3:
        sys.exit("BLOCKING: alt text must be unique across all three images.")

    for slot in ("featured", "body1", "body2"):
        s = sel[slot]
        src = os.path.join(CAND_DIR, s["candidate"] + ".webp")
        dst = os.path.join(IMG_DIR, s["filename"])
        shutil.copyfile(src, dst)
        if state.get(slot):
            print(f"{slot}: already uploaded as media {state[slot]}, skipping"); continue

        h = dict(H_)
        h["Content-Disposition"] = f'attachment; filename="{s["filename"]}"'
        h["Content-Type"] = "image/webp"
        m = json.loads(_req(f"{WP}/media", data=open(dst, "rb").read(),
                            headers=h, method="POST").read())
        mid = m["id"]
        ph = dict(H_); ph["Content-Type"] = "application/json"
        _req(f"{WP}/media/{mid}", data=json.dumps({"alt_text": s["alt"]}).encode(),
             headers=ph, method="POST").read()

        # --- post-upload verification, blocking
        v = json.loads(_req(f"{WP}/media/{mid}?context=edit", headers=H_).read())
        det = v.get("media_details", {})
        url = v.get("source_url", "")
        problems = []
        if not url.startswith("https://eldercarematters.com/wp-content/uploads/"):
            problems.append(f"bad url {url}")
        if (det.get("width"), det.get("height")) != (W, H):
            problems.append(f"dims {det.get('width')}x{det.get('height')}")
        if v.get("mime_type") != "image/webp":
            problems.append(f"mime {v.get('mime_type')}")
        if (v.get("alt_text") or "").strip() != s["alt"]:
            problems.append("alt_text did not persist")
        if problems:
            sys.exit(f"BLOCKING: media {mid} failed verification: {'; '.join(problems)}")

        state[slot] = mid
        state[slot + "_url"] = url
        state[slot + "_alt"] = s["alt"]
        state[slot + "_source"] = {k: s.get(k) for k in ("candidate", "filename")}
        json.dump(state, open(STATE, "w", encoding="utf-8"), indent=1)
        print(f"{slot}: media {mid}  {url}  {det.get('width')}x{det.get('height')} "
              f"{v.get('mime_type')}  alt {len(s['alt'])} chars")

    print("\nstate:", STATE)
    print("featured_media =", state.get("featured"))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "fetch"
    {"fetch": fetch, "upload": upload}[cmd]()
