# -*- coding: utf-8 -*-
"""Push "Hospital Discharge Planning: What to Do When a Parent Is Being Sent Home"
to ElderCareMatters as a draft.

Cloned from push_agency_vs_private.py (post for 2026-09-16). EVERY constant below was
reset for this post: draft path, state file, title, slug, categories, Yoast strings.
Do not assume an inherited value is correct.

Topic uniqueness was settled by the orchestrator before drafting: a title-regex sweep of
all 890 published posts plus an H2/H3 fetch of the 11 most recent. Only adjacent post is
212662 /medicare-observation-trap/, which this post links rather than repeats.

NOTE: all dollar figures are deliberately absent. cms.gov and medicare.gov are Akamai
edge-blocked from this environment (Chrome gets "Access Denied" too), so 2026 Part A
figures could not be traced to a primary source. Rules s3 says cut what cannot be
primary-sourced, so the post describes the coverage structure instead.

Run:
    python push_hospital_discharge.py                 # QA + link check + push
    python push_hospital_discharge.py --skip-links    # links verified moments ago
    python push_hospital_discharge.py --dry-run       # QA + links only, no push

Idempotent: reuses the post id in the state file, so a re-run updates, never duplicates.
"""
import os, sys, json, re, html, base64, time, urllib.request, urllib.error, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(ROOT, '..', '..', '..', '..'))
DRAFT = os.path.join(PROJ, 'clients', 'eldercarematters', 'output', 'drafts',
                     'hospital-discharge-planning-2026-09-25.html')
STATE = os.path.join(ROOT, 'hospital_discharge_push_state.json')

TITLE = "Hospital Discharge Planning: What to Do When a Parent Is Being Sent Home"
SLUG = "hospital-discharge-planning"
# Resolved live from the categories endpoint on 2026-09-25. Never guess these.
#   1374 Elder Care Planning | 309 Caregiving | 186 Medicare
CATS = [1374, 309, 186]
# Primary keyword "hospital discharge planning" leads both fields. Set from the brief.
YOAST_TITLE = "Hospital Discharge Planning: What to Do When Sent Home"
YOAST_DESC = ("Hospital discharge planning starts the moment a doctor says your parent is ready to "
              "leave. Know your rights, the right questions, and what Medicare covers.")

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
    Backoff does NOT clear a content block, only a rate limit. If a POST 403s
    repeatedly, bisect the body instead of retrying (rules s7)."""
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


# ---------- 1. BLOCKING QA ----------
print("[1] QA gate")
q = subprocess.run([sys.executable, os.path.join(PROJ, 'qa_ecm_draft.py'), DRAFT],
                   capture_output=True, text=True, encoding='utf-8', errors='replace')
print(q.stdout[-3000:] if q.stdout else "(no output)")
if q.returncode != 0:
    print("ABORT: QA failed. Fix the draft before pushing.")
    sys.exit(1)

content = open(DRAFT, encoding='utf-8').read()
# Strip HTML comments before pushing. Wordfence 403s any POST body carrying literal
# REST paths, and publisher-note comments routinely contain them (rules s7).
_before = len(content)
content = re.sub(r'<!--.*?-->', '', content, flags=re.S).strip()
content = re.sub('\n{3,}', '\n\n', content)
print(f"    stripped HTML comments: {_before} -> {len(content)} chars")
if re.search(r'/wp/v2/|context=edit', content):
    print("ABORT: a literal REST path survived in post_content. Wordfence will 403 this.")
    sys.exit(1)

# ---------- 2. LIVE LINK VERIFICATION ----------
# Status code alone is NOT enough on this site: several URLs answer 200 and then
# silently redirect to the homepage. Compare the FINAL url, and read the page
# title so the anchor cannot claim a kind of page the destination is not (rules s1).
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
    time.sleep(6)          # Wordfence rate-limits bursts (rules s1)
if bad:
    print("ABORT: link failures:")
    for u, r in bad:
        print("   ", u, r)
    sys.exit(1)

if "--dry-run" in sys.argv:
    print("\nDRY RUN complete. QA and links pass. Nothing pushed.")
    sys.exit(0)

# Link checking leaves the host throttled. Give Wordfence room before the POST.
if links:
    print("[2b] cooling down 20s before the push so Wordfence does not 403 it")
    time.sleep(20)

# ---------- 3. CREATE OR UPDATE ----------
st = state()
pid = st.get('post_id')
media = st.get('featured_media')
payload = {"title": TITLE, "slug": SLUG, "content": content, "status": "draft",
           "categories": CATS,
           "meta": {"_yoast_wpseo_title": YOAST_TITLE, "_yoast_wpseo_metadesc": YOAST_DESC}}
if media:
    payload["featured_media"] = media
if pid:
    print(f"[3] updating existing post {pid}")
    # Never blind-overwrite a client's manual publish or their image edits.
    live = api(f"posts/{pid}?context=edit&_fields=id,status,featured_media")
    if live['status'] != 'draft':
        print(f"    live status is '{live['status']}', not draft. Preserving it.")
        payload.pop('status')
    if live.get('featured_media') and not media:
        print(f"    preserving existing featured_media {live['featured_media']}")
        payload.pop('featured_media', None)
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
# Yoast is NOT REST-writable on this install. Attempt it, verify, then report the
# exact strings for manual entry. Never claim it is set without checking (rules s7).
print("[4] verifying Yoast (known NOT REST-writable on this install)")
chk = api(f"posts/{pid}?context=edit&_fields=id,meta")
m = chk.get('meta', {}) or {}
tp = m.get('_yoast_wpseo_title') == YOAST_TITLE
dp = m.get('_yoast_wpseo_metadesc') == YOAST_DESC
st['yoast_title_persisted'] = bool(tp)
st['yoast_desc_persisted'] = bool(dp)
save(st)
print(f"    title persisted={tp}  desc persisted={dp}")
if not (tp and dp):
    print("    -> MANUAL DASHBOARD ENTRY REQUIRED (Posts > Edit > Yoast SEO panel):")
    print(f"       SEO title        ({len(YOAST_TITLE)} chars): {YOAST_TITLE}")
    print(f"       Meta description ({len(YOAST_DESC)} chars): {YOAST_DESC}")

print("\nDONE. Post is a DRAFT.")
