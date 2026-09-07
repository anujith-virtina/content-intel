# -*- coding: utf-8 -*-
"""Upload images + create the ElderCareMatters draft:
"Adult Day Care 101: A Guide for Busy Family Caregivers"
slug: adult-day-care-for-elderly

Second push for this client. Adapted from push_assisted_living_cost.py.

New blocking checks added this run (MUST-FOLLOW-RULES.md section 9):
  - DEAD_LINKS: ECM has no adult day care directory page. Several plausible slugs
    return HTTP 200 but silently redirect to the homepage, so a naive status check
    passes them. Those URLs are now blocked outright.
  - "the Elderly" is caught by the existing "the elderly" banned-substring check,
    which means the official PACE program name cannot be spelled out. PACE is
    defined functionally instead. Nothing to enforce, but noted so a future run
    does not "fix" it by writing the banned string.

Known constraints, verified 2026-09-01 and re-verified 2026-09-03:
  - Yoast fields are NOT exposed in the REST `meta` object on this install.
  - The site serves WebP. Images are uploaded as WebP at 1024x536.
  - Wordfence rate-limits hard. A 17-URL burst got HTTP 429 on 15 of them.

Images are pre-QA'd. QA_DIR must hold final_featured.webp, final_body1.webp,
final_body2.webp, all 1024x536. There is no auto-picker.

Run: set QA_DIR, then `python push_adult_day_care.py publish`. Default is DRY_RUN.
"""
import os, sys, json, base64, ssl, re, time, html as htmlmod, urllib.request, urllib.error

ENV_PATH = r"C:\content-intel\.env"
if os.path.exists(ENV_PATH):
    for _ln in open(ENV_PATH, encoding="utf-8-sig"):
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
HTML_PATH = os.path.join(ROOT, r"clients\eldercarematters\output\drafts\adult-day-care-vs-nursing-home-2026-09-07.html")
STATE = os.path.join(ROOT, r"clients\eldercarematters\output\research\advnh_push_state.json")
QA_DIR = os.environ.get("QA_DIR", "")

TITLE = "Adult Day Care vs Nursing Home: Which Is Right for Your Loved One"
SLUG = "adult-day-care-vs-nursing-home"
YOAST_TITLE = "Adult Day Care vs Nursing Home: How to Decide"
YOAST_DESC = ("Compare adult day care and nursing homes on hours, cost, and who pays, with 2025 "
              "median figures and the signs a day program is no longer enough.")
CATEGORY_ID = 954        # "Nursing Homes", verified via /wp/v2/categories 2026-09-07 (8 posts).
# Note: posts 283684/283698 were manually recategorised after push (live cats [309,1759] /
# [174]), so treat categories as the user's to change and never blind-overwrite on update.

FEATURED_ONLY = os.environ.get("FEATURED_ONLY") == "1"

# Alt text written against the image actually selected, per rules section 5.
FEATURED_ALT = ("An older mother and her adult daughter lean their heads together and smile "
                "in a close black and white portrait taken at home")
BODY1_ALT = None   # not used: see FEATURED_ONLY note at the top of this file
BODY2_ALT = None

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
          "placement", "facility", "facilities"]
low = content.lower()
# "Skilled nursing facility" is the correct Medicare term for a nursing home and is
# approved for this post (table header + the Medicare explanation). Strip only that
# exact phrase before scanning, so "facility" used as a synonym for "community"
# anywhere else still blocks. Count the allowance so it cannot creep.
SNF_ALLOWED = 3
_snf = len(re.findall(r"skilled nursing facilit(?:y|ies)", low))
if _snf > SNF_ALLOWED:
    raise SystemExit(f"BLOCKING: 'skilled nursing facility' used {_snf} times, cap {SNF_ALLOWED}")
low_scan = re.sub(r"skilled nursing facilit(?:y|ies)", " ", low)
print(f"  'skilled nursing facility' allowed {_snf}/{SNF_ALLOWED} time(s)")
hits = [b for b in BANNED if b in low_scan]
if re.search(r"\bnavigat(?:e|es|ed|ing)\b", low): hits.append("navigate(verb)")
if hits: raise SystemExit(f"BLOCKING: banned words {hits}")
print("  banned words: 0 OK")

# YMYL guardrails specific to this client
if re.search(r"medicare (pays|covers) for (assisted living|long-term care|custodial|adult day)", low):
    raise SystemExit("BLOCKING: claims Medicare pays for a non-covered service")
for pat, why in [(r"look-?back period of \d", "states a Medicaid look-back period"),
                 (r"asset limit of \$[\d,]+", "states a Medicaid asset limit"),
                 (r"income (cap|limit) of \$[\d,]+", "states a Medicaid income limit")]:
    if re.search(pat, low): raise SystemExit(f"BLOCKING: {why}")
if "elder law attorney" not in low:
    raise SystemExit("BLOCKING: Medicaid discussed with no route to an elder law attorney")
print("  YMYL guardrails OK (no coverage claim, no eligibility figures, routed to counsel)")

# every dollar figure must sit in a post that names its source and the year
if "$" in content and not ("CareScout" in content and "2025" in content):
    raise SystemExit("BLOCKING: dollar figures present with no named, dated source")
if re.search(r"\baverage\b", low) and "median" not in low:
    raise SystemExit("BLOCKING: survey figures called averages")
print("  cost figures carry a named, dated source, called medians OK")

h2_txt = [re.sub("<[^>]+>", "", x).strip() for x in re.findall(r"<h2[^>]*>(.*?)</h2>", content, re.S)]
REQUIRED = ["Introduction", "People Also Ask", "Conclusion", "Frequently Asked Questions"]
missing = [r for r in REQUIRED if r not in h2_txt]
if missing:
    raise SystemExit(f"BLOCKING: required sections missing: {missing}")
if h2_txt.index("People Also Ask") > h2_txt.index("Conclusion"):
    raise SystemExit("BLOCKING: People Also Ask must come before Conclusion")
if h2_txt.index("Conclusion") > h2_txt.index("Frequently Asked Questions"):
    raise SystemExit("BLOCKING: Conclusion must come before Frequently Asked Questions")
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
if "<details" in _paa:
    raise SystemExit("BLOCKING: People Also Ask must stay flat, not an accordion")
print(f"  required sections: all 4 present and in order (PAA {n_paa} Qs, FAQ {n_faq} Qs) OK")

h2 = re.findall(r"<h2[^>]*>(.*?)</h2>", content, re.S)
h3 = re.findall(r"<h3[^>]*>(.*?)</h3>", content, re.S)
if len(h2) < 6: raise SystemExit(f"BLOCKING: only {len(h2)} H2 sections")
STOP = {"a","an","the","and","or","but","for","of","in","on","at","to","is","it","not","does","your",
        "with","so","only","own","from"}
bad_case = [x for x in h2 if any(w[0].islower() for w in re.sub("<[^>]+>", "", x).split()
                                 if w and w[0].isalpha() and w.lower() not in STOP)]
if bad_case: raise SystemExit(f"BLOCKING: H2 not Title Case: {bad_case}")
print(f"  headings: {len(h2)} H2, {len(h3)} H3, Title Case OK")

# --- links -------------------------------------------------------------------
ext = sorted(set(re.findall(r'href="(https?://(?!eldercarematters\.com)[^"]+)"', content)))
if len(ext) > 2: raise SystemExit(f"BLOCKING: {len(ext)} external links, cap 2: {ext}")
COMPETITORS = ["aplaceformom", "caring.com", "senioradvisor", "agingcare", "care.com", "seniorliving.com",
               "assistedlivinglocators"]
for e in ext:
    if any(c in e.lower() for c in COMPETITORS): raise SystemExit(f"BLOCKING: competitor link {e}")
for a in re.findall(r'<a [^>]*href="https?://(?!eldercarematters)[^"]*"[^>]*>', content):
    if 'target="_blank"' not in a or 'rel="noopener noreferrer"' not in a:
        raise SystemExit(f"BLOCKING: external link missing target/rel: {a}")

# NEW 2026-09-03: these ECM URLs return 200 but silently redirect to the homepage.
# A naive status check passes them. They are not real pages. Never link them.
DEAD_LINKS = ["/adult-day-care/", "/adult-day-care-services-for-seniors/", "/adult-day-care-centers/",
              "/adult-day-services/", "/home-health-care/", "/senior-centers/", "/veterans-benefits/",
              "/geriatric-care-managers/",
              "/skilled-nursing/"]   # verified 2026-09-07: 200 then redirects to the homepage

# Resolves cleanly, so no status or final-URL check can catch it, but it is an
# article titled "Protecting Your Rights and Holding Nursing Homes Accountable",
# not a directory. Anchoring it as a directory tells the reader a lie.
NOT_A_DIRECTORY = {
    "/nursing-homes/": "an article about residents' rights and abuse, not a directory page",
}
DIRECTORY_ANCHOR_WORDS = ("find", "directory", "browse", "search", "near you", "listings")
internal = sorted(set(re.findall(r'href="(https://eldercarematters\.com/[^"]+)"', content)))
for i in internal:
    path = i.replace("https://eldercarematters.com", "")
    if path in DEAD_LINKS:
        raise SystemExit(f"BLOCKING: {i} redirects to the homepage, it is not a real page")

# --- live verification (blocking) --------------------------------------------
# A static blocklist cannot catch a URL that rots later, and this site answers 200
# and THEN redirects to the homepage, so the final URL is what matters, not the
# status code. Wordfence 429s on bursts, so space the requests out.
_ctx = ssl.create_default_context()
_ctx.check_hostname = False
_ctx.verify_mode = ssl.CERT_NONE
_all_links = internal + [e for e in ext]
print(f"  live-checking {len(_all_links)} link(s), spaced to avoid Wordfence 429...")
for _u in _all_links:
    for _attempt in range(3):
        try:
            _r = urllib.request.urlopen(
                urllib.request.Request(_u, headers={"User-Agent": UA}), timeout=60, context=_ctx)
            _final = _r.geturl()
            _body = _r.read(80000).decode("utf-8", "ignore")
            _code = _r.status
            break
        except urllib.error.HTTPError as _e:
            if _e.code == 429:
                time.sleep(20)
                continue
            raise SystemExit(f"BLOCKING: {_u} returned HTTP {_e.code}")
        except Exception as _e:
            raise SystemExit(f"BLOCKING: {_u} failed to resolve: {_e}")
    else:
        raise SystemExit(f"BLOCKING: {_u} rate-limited on every attempt, cannot verify")
    if _final.rstrip("/") == "https://eldercarematters.com" and _u.rstrip("/") != "https://eldercarematters.com":
        raise SystemExit(f"BLOCKING: {_u} redirects to the homepage, it is not a real page")
    if _u.startswith("https://eldercarematters.com") and _final.rstrip("/") != _u.rstrip("/"):
        raise SystemExit(f"BLOCKING: {_u} redirected to {_final}, use the canonical URL")
    _title = re.search(r"<title[^>]*>(.*?)</title>", _body, re.S | re.I)
    _title = re.sub(r"\s+", " ", re.sub("<[^>]+>", "", _title.group(1))).strip() if _title else ""
    _path = _u.replace("https://eldercarematters.com", "")
    if _path in NOT_A_DIRECTORY:
        _anchors = re.findall(r'href="' + re.escape(_u) + r'"[^>]*>(.*?)</a>', content, re.S | re.I)
        for _a in _anchors:
            _atext = re.sub("<[^>]+>", "", _a).strip().lower()
            if any(w in _atext for w in DIRECTORY_ANCHOR_WORDS):
                raise SystemExit(
                    f"BLOCKING: {_u} is {NOT_A_DIRECTORY[_path]}; "
                    f"anchor {_atext!r} presents it as a directory")
    print(f"    {_code}  {_path or _u}  |  {_title[:58]}")
    time.sleep(6)
print("  all links verified live by final URL and page title OK")

if not (5 <= len(internal) <= 8):
    raise SystemExit(f"BLOCKING: {len(internal)} internal links, need 5-8")
DIRECTORY = [i for i in internal if i.rstrip("/").split("/")[-1] in
             ("assisted-living", "memory-care", "home-care-providers", "nursing-homes",
              "elder-law-attorneys")]
if len(DIRECTORY) < 3:
    raise SystemExit(f"BLOCKING: only {len(DIRECTORY)} directory category links, house pattern needs 3+")
print(f"  links: {len(internal)} internal ({len(DIRECTORY)} directory), {len(ext)} external OK")

# --- voice -------------------------------------------------------------------
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

if content.count("<table") < 1: raise SystemExit("BLOCKING: no comparison table")
if content.count("<ol") < 1: raise SystemExit("BLOCKING: no numbered question list")
print(f"  structure: {content.count('<table')} table(s), {content.count('<ol')} numbered list(s) OK")

_ALTS = [a for a in (FEATURED_ALT, BODY1_ALT, BODY2_ALT) if a]
for alt in _ALTS:
    if not (80 <= len(alt) <= 150): raise SystemExit(f"BLOCKING: alt {len(alt)} chars: {alt}")
if len(set(_ALTS)) != len(_ALTS): raise SystemExit("BLOCKING: alt texts not unique")
CLINICAL = ["wheelchair", "hospital", "stethoscope", "white coat", "clinic", "nurse ", "patient"]
_ALTS = [a for a in (FEATURED_ALT, BODY1_ALT, BODY2_ALT) if a]
for alt in _ALTS:
    bad = [c for c in CLINICAL if c in alt.lower()]
    if bad: raise SystemExit(f"BLOCKING: clinical imagery in alt text {bad}: {alt}")
print("  alt text: lengths OK, unique, non-clinical")

if len(YOAST_TITLE) > 60: raise SystemExit(f"BLOCKING: Yoast title {len(YOAST_TITLE)} chars")
if not (120 <= len(YOAST_DESC) <= 160): raise SystemExit(f"BLOCKING: Yoast desc {len(YOAST_DESC)} chars")
print(f"  Yoast title {len(YOAST_TITLE)} chars, desc {len(YOAST_DESC)} chars OK")

DRY = "publish" not in sys.argv
if DRY:
    print("\nDRY RUN complete. Pass 'publish' to upload and push.")
    raise SystemExit(0)

print("\n=== MEDIA UPLOAD ===")
st = load_state()


def existing(mid):
    m = json.loads(req(f"{WP}/media/{mid}").read())
    print(f"  reusing media {mid}: {m['source_url']}")
    return mid, m["source_url"]


fm = st["featured_media"] if st.get("featured_media") else upload(
    read_qa("featured"), "adc-vs-nursing-home-featured.webp", FEATURED_ALT, "featured_media")[0]
if FEATURED_ONLY:
    print("  ** DEVIATION: FEATURED_ONLY=1. ECM rules section 5 require featured + 2 body")
    print("  ** images. Shipping with the featured image only, by explicit user decision")
    print("  ** on 2026-09-07. Body images to be added in a follow-up update.")
    b1 = b1u = b2 = b2u = None
else:
    b1, b1u = existing(st["body1_media"]) if st.get("body1_media") else \
        upload(read_qa("body1"), "adc-vs-nursing-home-body1.webp", BODY1_ALT, "body1_media")
    b2, b2u = existing(st["body2_media"]) if st.get("body2_media") else \
        upload(read_qa("body2"), "adc-vs-nursing-home-body2.webp", BODY2_ALT, "body2_media")

# body images placed between sections, matching the house pattern
# Placed against what the images actually show, not against section order.
# Anchors for this post's own sections. Only used when body images are shipped.
ANCHOR1 = "<h2>Signs Adult Day Care Is No Longer Enough</h2>"
ANCHOR2 = "<h2>Questions to Ask Before You Decide</h2>"
for anchor in ([] if FEATURED_ONLY else (ANCHOR1, ANCHOR2)):
    if anchor not in content:
        raise SystemExit(f"BLOCKING: image anchor not found: {anchor}")
if not FEATURED_ONLY:
    content = content.replace(ANCHOR1, IMG_TAG.format(url=b1u, alt=BODY1_ALT, mid=b1) + "\n\n" + ANCHOR1, 1)
    content = content.replace(ANCHOR2, IMG_TAG.format(url=b2u, alt=BODY2_ALT, mid=b2) + "\n\n" + ANCHOR2, 1)
_want_body = 0 if FEATURED_ONLY else 2
if content.count("<img") != _want_body:
    raise SystemExit(f"BLOCKING: expected {_want_body} body images, found {content.count('<img')}")
print(f"  body images inserted: {0 if FEATURED_ONLY else 2}")

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
