# -*- coding: utf-8 -*-
"""Push "Balancing a Full-Time Job and Caregiving: What Working Caregivers Should Know"
to ElderCareMatters as a draft.

Cloned from push_hospital_discharge.py. EVERY constant below was reset for this post.

Topic uniqueness was settled before drafting: a full live corpus sweep (~900 posts,
84 pages) found no post covering FMLA, employer conversations, or workplace
flexibility for working caregivers. Closest post is 272201 (caregiver burnout,
personal-coping only). See uniqueness-audit-2026-10-08.md.

YMYL notes: FMLA facts are stable federal law, cited to DOL.gov. State paid-leave
programs are named (CA/NJ/NY/WA/CO/MA) but never with a dollar figure or percentage.
No Medicare/Medicaid/tax/medical claims anywhere.

Adds a media-upload step the prior ECM push scripts didn't need (images had been
pushed separately before). Pattern follows the Virtina/ChatSKU upload_media approach,
adapted for WebP and ECM's plain-HTML (no page builder) publishing.

Run:
    python push_working_caregiver.py                 # QA + link check + push
    python push_working_caregiver.py --skip-links     # links verified moments ago
    python push_working_caregiver.py --dry-run        # QA + links only, no push
"""
import os, sys, json, re, html, base64, time, urllib.request, urllib.error, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(ROOT, '..', '..', '..', '..'))
DRAFT = os.path.join(PROJ, 'clients', 'eldercarematters', 'output', 'drafts',
                     'working-caregiver-job-balance-2026-10-08.html')
STATE = os.path.join(ROOT, 'working_caregiver_push_state.json')

TITLE = "Balancing a Full-Time Job and Caregiving: What Working Caregivers Should Know"
SLUG = "working-caregiver-job-balance"
# Resolved live from the categories endpoint on 2026-10-08. Never guess these.
#   309 Caregiving | 1759 Elder Care
CATS = [309, 1759]
YOAST_TITLE = "FMLA and Caregiving: What Working Caregivers Need to Know"   # 57 chars
YOAST_DESC = ("FMLA protects your job while you care for a parent, but it does not replace lost "
              "wages. See how professional care and paid leave programs can help too.")  # 151 chars

QA_DIR = os.environ.get("QA_DIR", "")
ALTS = {
 "featured": "A person writes notes on paper next to an open laptop and phone at a home desk, managing caregiving tasks.",
 "body1": "An adult daughter embraces her senior mother at home, both smiling warmly together.",
 "body2": "An overhead view of hands writing in a planner next to an open laptop and phone on a desk.",
}
for k, v in ALTS.items():
    assert 80 <= len(v) <= 150, "alt %s is %d chars, must be 80-150" % (k, len(v))

env = {}
for line in open(os.path.join(PROJ, '.env'), encoding='utf-8'):
    line = line.strip()
    if '=' in line and not line.startswith('#'):
        k, v = line.split('=', 1)
        env[k] = v.strip().strip('"')
AUTH = base64.b64encode(f"{env['ECM_WP_USERNAME']}:{env['ECM_WP_APP_PASSWORD']}".encode()).decode()
BASE = "https://eldercarematters.com/wp-json/wp/v2/"


def api(path, method="GET", payload=None, tries=5):
    """Wordfence rate-limits this host. Retry 429/403/503 with exponential backoff.
    Backoff does NOT clear a content block, only a rate limit."""
    data = json.dumps(payload).encode() if payload is not None else None
    delay = 10
    for n in range(1, tries + 1):
        r = urllib.request.Request(BASE + path, data=data, method=method, headers={
            'Authorization': 'Basic ' + AUTH, 'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(r, timeout=90) as f:
                return json.loads(f.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (429, 403, 503) and n < tries:
                print(f"    {e.code} from Wordfence, backing off {delay}s (attempt {n}/{tries})")
                time.sleep(delay)
                delay *= 2
                continue
            raise


def state():
    return json.load(open(STATE)) if os.path.exists(STATE) else {}


def save(d):
    json.dump(d, open(STATE, 'w'), indent=1)


# ---------- 0. MEDIA UPLOAD (images pre-cropped to 1024x536 WebP and visually QA'd) ----------
def upload_media(slot):
    path = os.path.join(QA_DIR, "final_%s.webp" % slot)
    if not os.path.exists(path):
        print("ABORT: missing pre-QA'd image %s" % path); sys.exit(1)
    data = open(path, 'rb').read()
    r = urllib.request.Request(
        BASE + "media", data=data, method="POST",
        headers={'Authorization': 'Basic ' + AUTH,
                 'Content-Disposition': 'attachment; filename="ecm-%s-%s.webp"' % (SLUG, slot),
                 'Content-Type': 'image/webp', 'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(r, timeout=180) as f:
        m = json.loads(f.read().decode())
    api("media/%d" % m['id'], "POST", {"alt_text": ALTS[slot]})
    print("    %-9s media %d  %s" % (slot, m['id'], m['source_url']))
    return m['id'], m['source_url']


st0 = state()
if not QA_DIR:
    print("ABORT: set QA_DIR to the folder holding final_featured/body1/body2.webp")
    sys.exit(1)
print("[0] media upload")
MEDIA = st0.get('media') or {}
if not MEDIA:
    for slot in ("featured", "body1", "body2"):
        mid, url = upload_media(slot)
        MEDIA[slot] = {"id": mid, "url": url}
        st0['media'] = MEDIA; save(st0)
        time.sleep(2)
else:
    print("    reusing media from state: %s" % {k: v['id'] for k, v in MEDIA.items()})
for m in MEDIA.values():
    if not m["url"].startswith("https://eldercarematters.com/wp-content/uploads/"):
        print("ABORT: media src not on eldercarematters uploads:", m["url"])
        sys.exit(1)

# ---------- 1. BLOCKING QA ----------
print("[1] QA gate")
q = subprocess.run([sys.executable, os.path.join(PROJ, 'qa_ecm_draft.py'), DRAFT],
                   capture_output=True, text=True, encoding='utf-8', errors='replace')
print(q.stdout[-3000:] if q.stdout else "(no output)")
if q.returncode != 0:
    print("ABORT: QA failed. Fix the draft before pushing.")
    sys.exit(1)

content = open(DRAFT, encoding='utf-8').read()
# The featured image lives ONLY in featured_media (the theme renders it as the
# hero above the title). Gold-standard post 283258 confirms this: featured_media
# is set, but 0 of its inline <img> tags duplicate it in post_content. Inserting
# it a second time into the body put the same image above the Introduction H2,
# which is what the user flagged. So: strip the FEATURED marker outright, only
# insert body1/body2 into content.
content = re.sub(r'<!-- FEATURED IMAGE:.*?-->\s*', '', content, flags=re.S)
for slot in ("body1", "body2"):
    marker = "<!-- BODY IMAGE %s: " % ("1" if slot == "body1" else "2")
    pattern = re.compile(re.escape(marker) + r'.*?-->', re.S)
    if pattern.search(content):
        content = pattern.sub(
            '<img src="%s" alt="%s" width="1024" height="536" loading="lazy">' % (
                MEDIA[slot]['url'], ALTS[slot]),
            content, count=1)
        print("    inserted %s image" % slot)
if '<!-- FEATURED IMAGE' in content or '<!-- BODY IMAGE' in content:
    print("ABORT: an image placeholder comment survived insertion."); sys.exit(1)

# Strip remaining HTML comments before pushing. Wordfence 403s any POST body
# carrying literal REST paths, and publisher-note comments routinely contain them.
_before = len(content)
content = re.sub(r'<!--.*?-->', '', content, flags=re.S).strip()
content = re.sub('\n{3,}', '\n\n', content)
print(f"    stripped remaining HTML comments: {_before} -> {len(content)} chars")
if re.search(r'/wp/v2/|context=edit', content):
    print("ABORT: a literal REST path survived in post_content. Wordfence will 403 this.")
    sys.exit(1)

# ---------- 2. LIVE LINK VERIFICATION ----------
print("[2] verifying every link resolves and lands where the anchor claims")
if "--skip-links" in sys.argv:
    print("    SKIPPED by flag (links verified moments earlier)")
    links = []
else:
    links = re.findall(r'<a\s[^>]*href=["\'](https?://[^"\']+)["\']', content)
bad = []
for u in sorted(set(links)):
    try:
        rq = urllib.request.Request(u, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(rq, timeout=45) as f:
            final, code = f.geturl(), f.status
            t = re.search(r'<title[^>]*>(.*?)</title>', f.read().decode('utf-8', 'replace'),
                          re.S | re.I)
        title = html.unescape(re.sub(r'\s+', ' ', t.group(1))).strip() if t else '?'
        home = final.rstrip('/') == "https://eldercarematters.com"
        moved = final.rstrip('/') != u.rstrip('/')
        flag = "DEAD->home" if home else ("REDIRECT" if moved else "ok")
        if home:
            bad.append((u, "resolves 200 then redirects to the homepage"))
        print(f"    {flag:11} {code} {u}\n                -> {title[:70]}")
    except Exception as e:
        bad.append((u, str(e)))
        print(f"    ERROR       {u} :: {e}")
    time.sleep(6)
if bad:
    print("ABORT: link failures:")
    for u, r in bad:
        print("   ", u, r)
    sys.exit(1)

if "--dry-run" in sys.argv:
    print("\nDRY RUN complete. QA and links pass. Nothing pushed.")
    sys.exit(0)

if links:
    print("[2b] cooling down 20s before the push so Wordfence does not 403 it")
    time.sleep(20)

# ---------- 3. CREATE OR UPDATE ----------
st = state()
pid = st.get('post_id')
payload = {"title": TITLE, "slug": SLUG, "content": content, "status": "draft",
           "categories": CATS, "featured_media": MEDIA["featured"]["id"],
           "meta": {"_yoast_wpseo_title": YOAST_TITLE, "_yoast_wpseo_metadesc": YOAST_DESC}}
if pid:
    print(f"[3] updating existing post {pid}")
    live = api(f"posts/{pid}?context=edit&_fields=id,status,featured_media")
    if live['status'] != 'draft':
        print(f"    live status is '{live['status']}', not draft. Preserving it.")
        payload.pop('status')
    post = api(f"posts/{pid}", 'POST', payload)
else:
    print("[3] creating new draft")
    post = api("posts", 'POST', payload)
pid = post['id']
st.update({'post_id': pid, 'status': post['status'], 'slug': post['slug'],
           'link': post['link']})
save(st)
print(f"    post {pid}  status={post['status']}  {post['link']}")
print(f"    EDIT: https://eldercarematters.com/wp-admin/post.php?post={pid}&action=edit")

# ---------- 4. VERIFY YOAST ----------
print("[4] verifying Yoast (known NOT REST-writable on this install)")
chk = api(f"posts/{pid}?context=edit&_fields=id,meta,featured_media")
m = chk.get('meta', {}) or {}
tp = m.get('_yoast_wpseo_title') == YOAST_TITLE
dp = m.get('_yoast_wpseo_metadesc') == YOAST_DESC
st['yoast_title_persisted'] = bool(tp)
st['yoast_desc_persisted'] = bool(dp)
save(st)
print(f"    title persisted={tp}  desc persisted={dp}")
print(f"    featured_media live: {chk.get('featured_media')}")
if not (tp and dp):
    print("    -> MANUAL DASHBOARD ENTRY REQUIRED (Posts > Edit > Yoast SEO panel):")
    print(f"       SEO title        ({len(YOAST_TITLE)} chars): {YOAST_TITLE}")
    print(f"       Meta description ({len(YOAST_DESC)} chars): {YOAST_DESC}")

print("\nDONE. Post is a DRAFT.")
