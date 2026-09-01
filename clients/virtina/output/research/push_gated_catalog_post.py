# -*- coding: utf-8 -*-
"""Upload images + create the Virtina draft:
"Your B2B catalog is invisible to AI search, and you built it that way on purpose"
slug: gated-catalog-ai-visibility

Adapted from push_virtina_shortcodes.py (post 42465). Differences:
  - Body image placeholders are {{BODY1_IMG}} / {{BODY2_IMG}} and are replaced with
    full Template G blocks built here, so the draft file stays free of media IDs.
  - Blocking checks run before any POST: em dashes (all 4 forms), banned words,
    TOC anchor/H2 id parity, external link count and attributes, image dimensions,
    alt text length, paragraph sentence count, sentence word count.
  - Crash resilience: post id and media ids are written to gated_push_state.json the
    instant they return, so a re-run UPDATEs rather than creating a duplicate.

Images are pre-QA'd. QA_DIR must hold final_featured.jpg (1309x500),
final_body1.jpg and final_body2.jpg (670x352). There is no auto-picker.

Run: set QA_DIR, then `python push_gated_catalog_post.py publish`. Default is DRY_RUN.
"""
import os, sys, json, base64, ssl, re, html as htmlmod, urllib.request

ENV_PATH = r"C:\content-intel\.env"
if os.path.exists(ENV_PATH):
    for _ln in open(ENV_PATH, encoding="utf-8"):
        _ln = _ln.strip()
        if _ln and not _ln.startswith("#") and "=" in _ln:
            _k, _v = _ln.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

ctx = ssl._create_unverified_context()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
WP = "https://virtina.com/wp-json/wp/v2"
U, A = os.environ["WP_USERNAME"], os.environ["WP_APP_PASSWORD"]   # Virtina creds, never ChatSKU/ImpelHub
AUTH = base64.b64encode(f"{U}:{A}".encode()).decode()
H = {"Authorization": "Basic " + AUTH, "User-Agent": UA}
ROOT = r"C:\content-intel"
HTML_PATH = os.path.join(ROOT, r"clients\virtina\output\drafts\gated-catalog-ai-visibility-2026-08-31.html")
STATE = os.path.join(ROOT, r"clients\virtina\output\research\gated_push_state.json")
QA_DIR = os.environ.get("QA_DIR", "")

TITLE = "Your B2B catalog is invisible to AI search, and you built it that way on purpose"
SLUG = "gated-catalog-ai-visibility"
YOAST_TITLE = "Why AI Search Can't See Your B2B Catalog | Virtina"
YOAST_DESC = ("Your B2B catalog sits behind a login, so AI search cannot read it. See which catalog "
              "layers to open, which to keep gated, and how to fix it in WooCommerce.")
FOCUS_KW = "B2B catalog AI search"
CATEGORY_ID = 79          # WooCommerce

FEATURED_ALT = ("Hand holding a payment card beside a laptop showing an online store product grid, "
                "the public face of an ecommerce catalog")
BODY1_ALT = ("Laptop on a desk showing an online store catalog page, the public view an AI retrieval bot "
             "receives from a product page")
BODY2_ALT = ("Ecommerce manager at an office desk holding a folder of pricing paperwork that stays behind "
             "the customer login")

TEMPLATE_G = ('<span style="display:block;margin:20px 0;"><img alt="{alt}" data-id="{mid}" width="670" '
              'data-init-width="670" height="352" data-init-height="352" title="" loading="lazy" '
              'src="{url}" data-width="670" data-height="352" '
              'style="aspect-ratio: auto 670 / 352;max-width:100%;"></span>')


def load_state():
    if os.path.exists(STATE):
        try: return json.load(open(STATE, encoding="utf-8"))
        except Exception: return {}
    return {}


def save_state(**kw):
    st = load_state(); st.update(kw); st.setdefault("slug", SLUG)
    json.dump(st, open(STATE, "w", encoding="utf-8"), indent=1)
    print("  [state]", kw)
    return st


def req(url, data=None, headers=None, method=None):
    r = urllib.request.Request(url, data=data, headers=headers or H, method=method)
    return urllib.request.urlopen(r, timeout=120, context=ctx)


def read_qa(slot, w, h):
    if not QA_DIR:
        raise SystemExit("BLOCKING: QA_DIR not set. This script has no auto-picker.")
    p = os.path.join(QA_DIR, f"final_{slot}.jpg")
    if not os.path.exists(p):
        raise SystemExit(f"BLOCKING: missing pre-QA'd image {p}")
    from PIL import Image
    data = open(p, "rb").read()
    size = Image.open(p).size
    if size != (w, h):
        raise SystemExit(f"BLOCKING: {p} is {size}, expected ({w}, {h})")
    if len(data) > 200_000:
        raise SystemExit(f"BLOCKING: {p} is {len(data)} bytes, over the 200 KB cap")
    print(f"  pre-QA'd {slot}: {size} {len(data)//1024} KB")
    return data


def upload(data, filename, alt, state_key):
    h = dict(H)
    h["Content-Disposition"] = f'attachment; filename="{filename}"'
    h["Content-Type"] = "image/jpeg"
    m = json.loads(req(f"{WP}/media", data=data, headers=h, method="POST").read())
    mid = m["id"]
    save_state(**{state_key: mid})
    ph = dict(H); ph["Content-Type"] = "application/json"
    req(f"{WP}/media/{mid}", data=json.dumps({"alt_text": alt}).encode(), headers=ph, method="POST").read()
    if not m["source_url"].startswith("https://virtina.com/wp-content/uploads/"):
        raise SystemExit(f"BLOCKING: unexpected upload URL {m['source_url']}")
    print(f"  uploaded media {mid}: {m['source_url']}")
    return mid, m["source_url"]


content = open(HTML_PATH, encoding="utf-8").read()

# --------------------------------------------------------------------------
# Blocking checks (MUST-FOLLOW-RULES.md section 9)
# --------------------------------------------------------------------------
print("=== BLOCKING CHECKS ===")
em = content.count("\u2014") + content.count("&mdash;") + content.count("&#8212;") + content.count("&#x2014;")
if em: raise SystemExit(f"BLOCKING: {em} em dash form(s) present")
print("  em dashes (all 4 forms): 0 OK")

BANNED = ["revolutionary", "game-changing", "best-in-class", "cutting-edge", "transform your",
          "unlock value", "synergize", "delve", "leverage", "realm", "ecosystem",
          "in today's fast-paced world", "it's important to note", "in conclusion"]
low = content.lower()
hits = [b for b in BANNED if b in low]
if re.search(r"\bnavigat(?:e|es|ed|ing)\b", low): hits.append("navigate(verb)")
if hits: raise SystemExit(f"BLOCKING: banned words {hits}")
print("  banned words: 0 OK")

ids = re.findall(r'<h2 id="([^"]+)"', content)
anchors = re.findall(r'href="#([^"]+)"', content)
if sorted(ids) != sorted(anchors):
    raise SystemExit(f"BLOCKING: TOC anchors do not match H2 ids\n  ids={sorted(ids)}\n  anchors={sorted(anchors)}")
print(f"  TOC parity: {len(ids)} H2 ids == {len(anchors)} anchors OK")

h3 = len(re.findall(r"<h3[ >]", content))
if h3 < 6: raise SystemExit(f"BLOCKING: only {h3} H3 subheadings, minimum 6")
if re.search(r"<h3><span", content): raise SystemExit("BLOCKING: Elementor H3 pattern present in a Thrive post")
print(f"  H3 subheadings: {h3} OK")

ext = [e for e in re.findall(r'href="(https?://(?!virtina\.com)[^"]+)"', content) if "w3.org" not in e]
if len(ext) > 2: raise SystemExit(f"BLOCKING: {len(ext)} external links, cap is 2: {ext}")
COMPETITORS = ["shopify.com", "bigcommerce.com", "magento.com", "wix.com", "squarespace.com"]
for e in ext:
    if any(c in e.lower() for c in COMPETITORS): raise SystemExit(f"BLOCKING: competitor link {e}")
for a in re.findall(r'<a [^>]*href="https?://(?!virtina\.com)[^"]*"[^>]*>', content):
    if "w3.org" in a: continue
    if 'target="_blank"' not in a or 'rel="noopener noreferrer"' not in a:
        raise SystemExit(f"BLOCKING: external link missing target/rel: {a}")
internal = re.findall(r'href="(https://virtina\.com/[^"]+)"', content)
if not (5 <= len(internal) <= 10):
    raise SystemExit(f"BLOCKING: {len(internal)} internal links, need 5-10")
print(f"  links: {len(internal)} internal, {len(ext)} external OK")

bad_p, long_s = [], []
for m in re.findall(r"<p(?: [^>]*)?>(.*?)</p>", content, re.S):
    txt = htmlmod.unescape(re.sub(r"<[^>]+>", "", m)).strip()
    if not txt: continue
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", txt) if s.strip()]
    if len(sents) >= 4: bad_p.append(txt[:60])
    long_s += [s[:60] for s in sents if len(s.split()) > 20]
if bad_p: raise SystemExit(f"BLOCKING: paragraphs with 4+ sentences: {bad_p}")
if long_s: raise SystemExit(f"BLOCKING: sentences over 20 words: {long_s}")
print("  paragraphs <4 sentences, sentences <=20 words OK")

wc = len(htmlmod.unescape(re.sub(r"<[^>]+>", " ", content)).split())
if not (1500 <= wc <= 2500): raise SystemExit(f"BLOCKING: word count {wc} outside 1500-2500")
print(f"  word count: {wc} OK")

if len(YOAST_TITLE) > 60 or not YOAST_TITLE.endswith("| Virtina"):
    raise SystemExit(f"BLOCKING: Yoast title invalid ({len(YOAST_TITLE)} chars)")
if not (150 <= len(YOAST_DESC) <= 160):
    raise SystemExit(f"BLOCKING: Yoast desc {len(YOAST_DESC)} chars, need 150-160")
print(f"  Yoast title {len(YOAST_TITLE)} chars, desc {len(YOAST_DESC)} chars OK")

for alt in (FEATURED_ALT, BODY1_ALT, BODY2_ALT):
    if not (80 <= len(alt) <= 150): raise SystemExit(f"BLOCKING: alt {len(alt)} chars outside 80-150: {alt}")
if len({FEATURED_ALT, BODY1_ALT, BODY2_ALT}) != 3: raise SystemExit("BLOCKING: alt texts not unique")
print("  alt text lengths OK and unique")

circles = content.count("background-color:#43627f;border-radius:50%")
if circles < 1: raise SystemExit("BLOCKING: no Template F bullet circles found")
if re.search(r'<ul(?! style="list-style:none)', content): raise SystemExit("BLOCKING: non-template <ul> present")
print(f"  Template F bullets: {circles} OK")

for bad in ("placehold.co", "source.unsplash.com"):
    if bad in content: raise SystemExit(f"BLOCKING: banned image host {bad}")

DRY = "publish" not in sys.argv
if DRY:
    print("\nDRY RUN complete. Pass 'publish' to upload and push.")
    raise SystemExit(0)

# --------------------------------------------------------------------------
print("\n=== MEDIA UPLOAD ===")
st = load_state()
if st.get("featured_media"):
    print("  featured already uploaded:", st["featured_media"])
    fm = st["featured_media"]
else:
    fm, _ = upload(read_qa("featured", 1309, 500),
                   "virtina-gated-catalog-ai-visibility-featured.jpg", FEATURED_ALT, "featured_media")
b1, b1u = upload(read_qa("body1", 670, 352),
                 "virtina-gated-catalog-ai-visibility-body1.jpg", BODY1_ALT, "body1_media")
b2, b2u = upload(read_qa("body2", 670, 352),
                 "virtina-gated-catalog-ai-visibility-body2.jpg", BODY2_ALT, "body2_media")

content = content.replace("{{BODY1_IMG}}", TEMPLATE_G.format(alt=BODY1_ALT, mid=b1, url=b1u))
content = content.replace("{{BODY2_IMG}}", TEMPLATE_G.format(alt=BODY2_ALT, mid=b2, url=b2u))
left = re.findall(r"\{\{[A-Z_0-9]+\}\}", content)
if left: raise SystemExit(f"BLOCKING: unresolved placeholders {set(left)}")
print("  placeholders resolved, 2 body image blocks inserted")

payload = {
    "title": TITLE, "slug": SLUG, "status": "draft", "content": content,
    "excerpt": YOAST_DESC, "featured_media": fm, "categories": [CATEGORY_ID],
    "meta": {"_yoast_wpseo_title": YOAST_TITLE, "_yoast_wpseo_metadesc": YOAST_DESC,
             "_yoast_wpseo_focuskw": FOCUS_KW},
}
ph = dict(H); ph["Content-Type"] = "application/json"
pid = load_state().get("post_id")
if pid:
    resp = req(f"{WP}/posts/{pid}", data=json.dumps(payload).encode(), headers=ph, method="POST")
else:
    resp = req(f"{WP}/posts", data=json.dumps(payload).encode(), headers=ph, method="POST")
post = json.loads(resp.read())
save_state(post_id=post["id"], status=post["status"], link=post.get("link"))
print(f"\nPOST {resp.status} | POST_ID {post['id']} | status {post['status']}")
print("edit:", f"https://virtina.com/wp-admin/post.php?post={post['id']}&action=edit")
print("preview:", f"https://virtina.com/?p={post['id']}&preview=true")
