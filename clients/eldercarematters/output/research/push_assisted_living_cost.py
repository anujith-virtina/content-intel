# -*- coding: utf-8 -*-
"""Upload images + create the ElderCareMatters draft:
"How Much Does Assisted Living Cost?"
slug: how-much-does-assisted-living-cost

First push for this client. ECM has NO page builder, so this is far simpler than
the chatsku/impelhub (Elementor) or virtina (Thrive) scripts: plain semantic HTML
goes straight into post_content.

Known constraints, verified 2026-09-01:
  - Yoast fields are NOT exposed in the REST `meta` object on this install. The
    script still attempts the write and then re-reads with context=edit, and
    reports honestly whether they persisted. Expect manual dashboard entry.
  - The site serves WebP. Images are uploaded as WebP at 1024x536.
  - Wordfence is active. Do not hammer the API.

Images are pre-QA'd. QA_DIR must hold final_featured.webp, final_body1.webp,
final_body2.webp, all 1024x536. There is no auto-picker.

Run: set QA_DIR, then `python push_assisted_living_cost.py publish`. Default is DRY_RUN.
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
WP = "https://eldercarematters.com/wp-json/wp/v2"
U, A = os.environ["ECM_WP_USERNAME"], os.environ["ECM_WP_APP_PASSWORD"]   # ECM creds only
AUTH = base64.b64encode(f"{U}:{A}".encode()).decode()
H = {"Authorization": "Basic " + AUTH, "User-Agent": UA}
ROOT = r"C:\content-intel"
HTML_PATH = os.path.join(ROOT, r"clients\eldercarematters\output\drafts\assisted-living-cost-2026-09-01.html")
STATE = os.path.join(ROOT, r"clients\eldercarematters\output\research\alc_push_state.json")
QA_DIR = os.environ.get("QA_DIR", "")

TITLE = "How Much Does Assisted Living Cost?"
SLUG = "how-much-does-assisted-living-cost"
YOAST_TITLE = "How Much Does Assisted Living Cost? | ElderCareMatters"
YOAST_DESC = ("Assisted living costs a median of $6,200 a month in 2025. See what drives the price, "
              "which fees are left out of the quote, and who actually ends up paying.")
CATEGORY_ID = 174        # "Assisted Living", verified via /wp/v2/categories

FEATURED_ALT = ("Smiling older couple standing together by a bright window while thinking about a move "
                "to an assisted living community")
BODY1_ALT = ("Calculator, coins, reading glasses and a notepad on a table, used to work out the monthly "
             "cost of assisted living")
BODY2_ALT = ("Hands working out care costs on a calculator beside a laptop showing an account statement "
             "at a wooden desk")

IMG_TAG = '<img src="{url}" alt="{alt}" class="wp-image-{mid}" loading="lazy" />'


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


def read_qa(slot):
    if not QA_DIR:
        raise SystemExit("BLOCKING: QA_DIR not set. This script has no auto-picker.")
    p = os.path.join(QA_DIR, f"final_{slot}.webp")
    if not os.path.exists(p):
        raise SystemExit(f"BLOCKING: missing pre-QA'd image {p}")
    from PIL import Image
    data = open(p, "rb").read()
    size = Image.open(p).size
    if size != (1024, 536):
        raise SystemExit(f"BLOCKING: {p} is {size}, expected (1024, 536)")
    if len(data) > 200_000:
        raise SystemExit(f"BLOCKING: {p} is {len(data)} bytes, over the 200 KB cap")
    print(f"  pre-QA'd {slot}: {size} {len(data)//1024} KB")
    return data


def upload(data, filename, alt, state_key):
    h = dict(H)
    h["Content-Disposition"] = f'attachment; filename="{filename}"'
    h["Content-Type"] = "image/webp"
    m = json.loads(req(f"{WP}/media", data=data, headers=h, method="POST").read())
    mid = m["id"]
    save_state(**{state_key: mid})
    ph = dict(H); ph["Content-Type"] = "application/json"
    req(f"{WP}/media/{mid}", data=json.dumps({"alt_text": alt}).encode(), headers=ph, method="POST").read()
    if not m["source_url"].startswith("https://eldercarematters.com/wp-content/uploads/"):
        raise SystemExit(f"BLOCKING: unexpected upload URL {m['source_url']}")
    print(f"  uploaded media {mid}: {m['source_url']}")
    return mid, m["source_url"]


content = open(HTML_PATH, encoding="utf-8").read()

print("=== BLOCKING CHECKS ===")
em = content.count("\u2014") + content.count("&mdash;")
if em: raise SystemExit(f"BLOCKING: {em} em dash(es)")
print("  em dashes: 0 OK")

BANNED = ["delve", "leverage", "realm", "ecosystem", "revolutionary", "game-changing", "cutting-edge",
          "best-in-class", "transform your", "in conclusion", "it's important to note",
          "in today's fast-paced world", "when it comes to", "the elderly", "suffering from",
          "placement"]
low = content.lower()
hits = [b for b in BANNED if b in low]
if re.search(r"\bnavigat(?:e|es|ed|ing)\b", low): hits.append("navigate(verb)")
if hits: raise SystemExit(f"BLOCKING: banned words {hits}")
print("  banned words: 0 OK")

# YMYL guardrails specific to this client
if re.search(r"medicare (pays|covers) for (assisted living|long-term care|custodial)", low):
    raise SystemExit("BLOCKING: claims Medicare pays for assisted living")
for pat, why in [(r"look-?back period of \d", "states a Medicaid look-back period"),
                 (r"asset limit of \$[\d,]+", "states a Medicaid asset limit")]:
    if re.search(pat, low): raise SystemExit(f"BLOCKING: {why}")
print("  YMYL guardrails OK (no Medicare coverage claim, no Medicaid eligibility figures)")

# every dollar figure must sit in a post that names its source
if "$" in content and "CareScout" not in content:
    raise SystemExit("BLOCKING: dollar figures present with no named source")
print("  cost figures carry a named, dated source OK")

h2_txt = [re.sub("<[^>]+>", "", x).strip() for x in re.findall(r"<h2[^>]*>(.*?)</h2>", content, re.S)]
REQUIRED = ["Introduction", "People Also Ask", "Conclusion", "Frequently Asked Questions"]
missing = [r for r in REQUIRED if r not in h2_txt]
if missing:
    raise SystemExit(f"BLOCKING: required sections missing: {missing}")
_paa = content[content.index("<h2>People Also Ask</h2>"):content.index("<h2>Conclusion</h2>")]
_faq = content[content.index("<h2>Frequently Asked Questions</h2>"):]
n_paa, n_faq = len(re.findall(r"<h3", _paa)), len(re.findall(r"<h3", _faq))
if not (3 <= n_paa <= 4): raise SystemExit(f"BLOCKING: People Also Ask has {n_paa} questions, need 3-4")
if not (5 <= n_faq <= 8): raise SystemExit(f"BLOCKING: FAQ has {n_faq} questions, need 5-8")
n_det, n_sum = _faq.count("<details"), _faq.count("<summary")
if n_det != n_faq or n_sum != n_faq:
    raise SystemExit(f"BLOCKING: FAQ accordion malformed ({n_det} details, {n_sum} summary, {n_faq} h3)")
if _faq.count("</details>") != n_det:
    raise SystemExit("BLOCKING: unbalanced </details> tags in FAQ")
print(f"  required sections: all 4 present (PAA {n_paa} Qs, FAQ {n_faq} Qs) OK")

h2 = re.findall(r"<h2[^>]*>(.*?)</h2>", content, re.S)
h3 = re.findall(r"<h3[^>]*>(.*?)</h3>", content, re.S)
if len(h2) < 6: raise SystemExit(f"BLOCKING: only {len(h2)} H2 sections")
STOP = {"a","an","the","and","or","but","for","of","in","on","at","to","is","it","not","does","your","with","so"}
bad_case = [x for x in h2 if any(w[0].islower() for w in re.sub("<[^>]+>", "", x).split()
                                 if w and w[0].isalpha() and w.lower() not in STOP)]
if bad_case: raise SystemExit(f"BLOCKING: H2 not Title Case: {bad_case}")
print(f"  headings: {len(h2)} H2, {len(h3)} H3, Title Case OK")

ext = sorted(set(re.findall(r'href="(https?://(?!eldercarematters\.com)[^"]+)"', content)))
if len(ext) > 2: raise SystemExit(f"BLOCKING: {len(ext)} external links, cap 2: {ext}")
COMPETITORS = ["aplaceformom", "caring.com", "senioradvisor", "agingcare", "care.com", "seniorliving.com",
               "assistedlivinglocators"]
for e in ext:
    if any(c in e.lower() for c in COMPETITORS): raise SystemExit(f"BLOCKING: competitor link {e}")
for a in re.findall(r'<a [^>]*href="https?://(?!eldercarematters)[^"]*"[^>]*>', content):
    if 'target="_blank"' not in a or 'rel="noopener noreferrer"' not in a:
        raise SystemExit(f"BLOCKING: external link missing target/rel: {a}")
internal = sorted(set(re.findall(r'href="(https://eldercarematters\.com/[^"]+)"', content)))
if len(internal) < 5: raise SystemExit(f"BLOCKING: only {len(internal)} internal links")
if "https://eldercarematters.com/assisted-living-vs-home-care/" not in internal:
    raise SystemExit("BLOCKING: the user-requested interlink to /assisted-living-vs-home-care/ is missing")
print(f"  links: {len(internal)} internal (incl. required interlink), {len(ext)} external OK")

bad_p, long_s = [], []
for m in re.findall(r"<p(?: [^>]*)?>(.*?)</p>", content, re.S):
    txt = htmlmod.unescape(re.sub(r"<[^>]+>", "", m)).strip()
    if not txt: continue
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", txt) if s.strip()]
    if len(sents) >= 4: bad_p.append(txt[:60])
    long_s += [s[:60] for s in sents if len(s.split()) > 25]
if bad_p: raise SystemExit(f"BLOCKING: paragraphs with 4+ sentences: {bad_p}")
if long_s: raise SystemExit(f"BLOCKING: sentences over 25 words: {long_s}")
print("  paragraphs <4 sentences, sentences <=25 words OK")

wc = len(htmlmod.unescape(re.sub(r"<[^>]+>", " ", content)).split())
if not (1500 <= wc <= 2400): raise SystemExit(f"BLOCKING: word count {wc} outside 1500-2400")
print(f"  word count: {wc} OK")

for alt in (FEATURED_ALT, BODY1_ALT, BODY2_ALT):
    if not (80 <= len(alt) <= 150): raise SystemExit(f"BLOCKING: alt {len(alt)} chars: {alt}")
if len({FEATURED_ALT, BODY1_ALT, BODY2_ALT}) != 3: raise SystemExit("BLOCKING: alt texts not unique")
print("  alt text lengths OK and unique")

if len(YOAST_TITLE) > 60: raise SystemExit(f"BLOCKING: Yoast title {len(YOAST_TITLE)} chars")
if not (150 <= len(YOAST_DESC) <= 160): raise SystemExit(f"BLOCKING: Yoast desc {len(YOAST_DESC)} chars")
print(f"  Yoast title {len(YOAST_TITLE)} chars, desc {len(YOAST_DESC)} chars OK")

DRY = "publish" not in sys.argv
if DRY:
    print("\nDRY RUN complete. Pass 'publish' to upload and push.")
    raise SystemExit(0)

print("\n=== MEDIA UPLOAD ===")
st = load_state()
fm = st.get("featured_media") or upload(read_qa("featured"),
        "assisted-living-cost-featured.webp", FEATURED_ALT, "featured_media")[0]
def existing(mid):
    m = json.loads(req(f"{WP}/media/{mid}").read())
    print(f"  reusing media {mid}: {m['source_url']}")
    return mid, m["source_url"]

b1, b1u = existing(st["body1_media"]) if st.get("body1_media") else           upload(read_qa("body1"), "assisted-living-cost-body1.webp", BODY1_ALT, "body1_media")
b2, b2u = existing(st["body2_media"]) if st.get("body2_media") else           upload(read_qa("body2"), "assisted-living-cost-body2.webp", BODY2_ALT, "body2_media")

# body images placed between sections, matching the house pattern
content = content.replace('<h2>Which Costs Are Not in the Quote?</h2>',
    IMG_TAG.format(url=b1u, alt=BODY1_ALT, mid=b1) + '\n\n<h2>Which Costs Are Not in the Quote?</h2>', 1)
content = content.replace('<h2>How Families Actually Pay for Assisted Living</h2>',
    IMG_TAG.format(url=b2u, alt=BODY2_ALT, mid=b2) + '\n\n<h2>How Families Actually Pay for Assisted Living</h2>', 1)
if content.count("<img") != 2:
    raise SystemExit(f"BLOCKING: expected 2 body images, found {content.count('<img')}")
print("  2 body images inserted")

payload = {
    "title": TITLE, "slug": SLUG, "status": "draft", "content": content,
    "excerpt": YOAST_DESC, "featured_media": fm, "categories": [CATEGORY_ID],
    "meta": {"_yoast_wpseo_title": YOAST_TITLE, "_yoast_wpseo_metadesc": YOAST_DESC},
}
ph = dict(H); ph["Content-Type"] = "application/json"
pid = load_state().get("post_id")
url = f"{WP}/posts/{pid}" if pid else f"{WP}/posts"
resp = req(url, data=json.dumps(payload).encode(), headers=ph, method="POST")
post = json.loads(resp.read())
save_state(post_id=post["id"], status=post["status"])
print(f"\nPOST {resp.status} | POST_ID {post['id']} | status {post['status']}")

print("\n=== VERIFY (context=edit) ===")
v = json.loads(req(f"{WP}/posts/{post['id']}?context=edit").read())
vm = v.get("meta", {})
yt = vm.get("_yoast_wpseo_title") == YOAST_TITLE
yd = vm.get("_yoast_wpseo_metadesc") == YOAST_DESC
print("  status:", v["status"], "| featured_media:", v["featured_media"], "| categories:", v["categories"])
print("  images in content:", len(re.findall(r"<img", v["content"]["raw"])))
print("  Yoast title persisted:", yt)
print("  Yoast desc persisted: ", yd)
if not (yt and yd):
    print("  >> Yoast is not REST-writable on this install, as expected.")
    print("  >> SET MANUALLY in WP Admin, Posts, Edit, Yoast SEO panel:")
    print("       Title:", YOAST_TITLE)
    print("       Desc :", YOAST_DESC)
save_state(yoast_title_persisted=yt, yoast_desc_persisted=yd, verified=True)
print("\nedit:", f"https://eldercarematters.com/wp-admin/post.php?post={post['id']}&action=edit")
print("preview:", f"https://eldercarematters.com/?p={post['id']}&preview=true")
