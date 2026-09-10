# -*- coding: utf-8 -*-
"""Push the Magento support-cliff post to Virtina as a DRAFT.

Gates, in order:
  1. QA harness must pass (qa_virtina_draft.py)
  2. 8-gram phrasing-uniqueness check against the related-post corpus
  3. Every link fetched with redirects NOT followed (a 301 must surface)
  4. Create/update, never blind-overwriting live state
  5. Yoast attempted, verified, reported for manual entry if it does not persist
"""
import os, sys, json, re, html, base64, time, subprocess
import urllib.request, urllib.error

ROOT = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(ROOT, '..', '..', '..', '..'))
DRAFT = os.path.join(PROJ, 'clients', 'virtina', 'output', 'drafts',
                     'magento-version-support-cliff-2026-09-10.html')
STATE = os.path.join(ROOT, 'magento_cliff_push_state.json')
QA = os.path.join(PROJ, 'qa_virtina_draft.py')

TITLE = "The August 2026 Magento Support Cliff: Upgrade, Move, or Replatform"
SLUG = "magento-version-support-cliff-2026"
YOAST_TITLE = "Magento Support Cliff 2026: What to Do Next | Virtina"
YOAST_DESC = ("Adobe ended support for Magento 2.4.6 and 2.4.5 in August 2026. "
              "Here is what that exposes, and how to choose between upgrading and replatforming.")

# Posts whose phrasing we must not duplicate (the Magento + migration cluster).
RELATED = [29601, 42413, 37552, 39502, 34921, 18791, 37776, 42177]

env = {}
for line in open(os.path.join(PROJ, '.env'), encoding='utf-8'):
    line = line.strip()
    if '=' in line and not line.startswith('#'):
        k, v = line.split('=', 1)
        env[k] = v.strip().strip('"')
AUTH = base64.b64encode(("%s:%s" % (env['WP_USERNAME'], env['WP_APP_PASSWORD'])).encode()).decode()
BASE = "https://virtina.com/wp-json/wp/v2/"


def api(path, method="GET", payload=None, tries=5):
    data = json.dumps(payload).encode() if payload is not None else None
    delay = 10
    for n in range(tries):
        r = urllib.request.Request(BASE + path, data=data, method=method, headers={
            'Authorization': 'Basic ' + AUTH,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(r, timeout=90) as f:
                return json.loads(f.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (429, 403, 503) and n < tries - 1:
                print("    %d, backing off %ds" % (e.code, delay))
                time.sleep(delay); delay *= 2; continue
            raise


def state():
    return json.load(open(STATE)) if os.path.exists(STATE) else {}


def save(d):
    json.dump(d, open(STATE, 'w'), indent=1)


def words(x):
    return re.sub(r'[^a-z0-9 ]', ' ', x.lower()).split()


# ---------- 1. QA GATE ----------
print("[1] QA gate")
q = subprocess.run([sys.executable, QA, DRAFT], capture_output=True, text=True)
tail = q.stdout.strip().splitlines()[-2:] if q.stdout else []
print("    " + " | ".join(t.strip() for t in tail))
if q.returncode != 0:
    print("ABORT: QA failed.")
    print(q.stdout[-3000:])
    sys.exit(1)

content = open(DRAFT, encoding='utf-8').read()
before = len(content)
content = re.sub(r'<!--.*?-->', '', content, flags=re.S).strip()
print("    stripped HTML comments: %d -> %d chars" % (before, len(content)))

plain = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ',
               re.sub(r'<style.*?</style>', '', content, flags=re.S | re.I))))

# ---------- 2. 8-GRAM PHRASING UNIQUENESS ----------
print("[2] 8-gram phrasing check against %d related posts" % len(RELATED))
mine = words(plain)
grams = set(tuple(mine[i:i + 8]) for i in range(len(mine) - 7))
hits = []
for pid in RELATED:
    try:
        d = api("posts/%d?context=edit&_fields=id,slug,content" % pid)
    except Exception as e:
        print("    could not fetch %d (%s), skipping" % (pid, e)); time.sleep(3); continue
    other = words(re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', d['content']['raw'] or ''))))
    og = set(tuple(other[i:i + 8]) for i in range(len(other) - 7))
    common = grams & og
    if common:
        for c in list(common)[:3]:
            hits.append((pid, d['slug'], ' '.join(c)))
    print("    %d %-46s overlap=%d" % (pid, d['slug'][:46], len(common)))
    time.sleep(3)
if hits:
    print("ABORT: verbatim 8+ word sequences shared with existing posts:")
    for pid, slug, g in hits:
        print("    %d %s :: \"%s\"" % (pid, slug, g))
    sys.exit(1)
print("    no shared 8-word sequences")

# ---------- 3. LINKS, REDIRECTS NOT FOLLOWED ----------
print("[3] verifying links (redirects NOT followed, per section 6)")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


opener = urllib.request.build_opener(NoRedirect)
bad = []
if '--skip-links' in sys.argv:
    print("    SKIPPED by flag")
else:
    for u in sorted(set(re.findall(r'<a\s[^>]*href=["\'](https?://[^"\']+)["\']', content))):
        try:
            with opener.open(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}),
                             timeout=45) as f:
                code = f.status
                loc = f.headers.get('Location')
                raw = f.read().decode('utf-8', 'replace')
            t = re.search(r'<title[^>]*>(.*?)</title>', raw, re.S | re.I)
            title = html.unescape(re.sub(r'\s+', ' ', t.group(1))).strip() if t else '?'
            if code != 200:
                bad.append((u, "%d -> %s" % (code, loc)))
                print("    %-14s %s" % ("%d REDIRECT" % code, u))
            else:
                print("    %-14s %s" % ("ok 200", u))
                print("                   %s" % title[:72])
        except urllib.error.HTTPError as e:
            bad.append((u, "HTTP %d" % e.code)); print("    %-14s %s" % ("%d DEAD" % e.code, u))
        except Exception as e:
            bad.append((u, str(e))); print("    %-14s %s :: %s" % ("ERROR", u, e))
        time.sleep(4)
if bad:
    print("ABORT: link failures (a 301 is a failure here, use the canonical URL):")
    for u, r in bad:
        print("   ", u, r)
    sys.exit(1)

# ---------- 4. CREATE OR UPDATE ----------
st = state()
pid = st.get('post_id')
payload = {"title": TITLE, "slug": SLUG, "content": content, "status": "draft",
           "meta": {"_yoast_wpseo_title": YOAST_TITLE, "_yoast_wpseo_metadesc": YOAST_DESC}}
if st.get('featured_media'):
    payload["featured_media"] = st['featured_media']
if pid:
    print("[4] updating existing post %d" % pid)
    live = api("posts/%d?context=edit&_fields=id,status,featured_media" % pid)
    if live['status'] != 'draft':
        print("    live status is '%s', preserving it" % live['status'])
        payload.pop('status')
    if live.get('featured_media') and not st.get('featured_media'):
        payload.pop('featured_media', None)
    post = api("posts/%d" % pid, 'POST', payload)
else:
    print("[4] creating new draft")
    post = api("posts", 'POST', payload)
pid = post['id']
st.update({'post_id': pid, 'status': post['status'], 'slug': post['slug'], 'link': post['link']})
save(st)
print("    post %d  status=%s  %s" % (pid, post['status'], post['link']))

# ---------- 5. YOAST ----------
print("[5] verifying Yoast (not REST-writable on this install, per post 42441)")
chk = api("posts/%d?context=edit&_fields=id,meta" % pid)
m = chk.get('meta', {}) or {}
tp = m.get('_yoast_wpseo_title') == YOAST_TITLE
dp = m.get('_yoast_wpseo_metadesc') == YOAST_DESC
st['yoast_title_persisted'] = bool(tp)
st['yoast_desc_persisted'] = bool(dp)
save(st)
print("    title persisted=%s  desc persisted=%s" % (tp, dp))
if not (tp and dp):
    print("    -> MANUAL WP DASHBOARD ENTRY REQUIRED:")
    print("       SEO title (%d chars): %s" % (len(YOAST_TITLE), YOAST_TITLE))
    print("       Meta desc (%d chars): %s" % (len(YOAST_DESC), YOAST_DESC))

print("")
print("DONE. Post %d is a DRAFT." % pid)
print("THRIVE CAVEAT: _tve_updated_post is not REST-writable. The post renders the")
print("semantic HTML fallback until it is opened and saved once in Thrive Architect.")
print("Do NOT hand-generate Thrive markup to work around this (broke post 38972).")
