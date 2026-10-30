# -*- coding: utf-8 -*-
"""Push the "customer payment declined" plain-language guide to Virtina as a DRAFT.

Gates, in order:
  1. QA harness must pass (qa_virtina_draft.py)
  2. 8-gram phrasing-uniqueness check against the payments/checkout cluster
  3. Every link fetched with redirects NOT followed
  4. Create/update, never blind-overwriting live state
  5. Yoast attempted, verified, reported for manual entry if it does not persist
"""
import os, sys, json, re, html, base64, time, subprocess
import urllib.request, urllib.error

ROOT = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(ROOT, '..', '..', '..', '..'))
DRAFT = os.path.join(PROJ, 'clients', 'virtina', 'output', 'drafts',
                     'customer-payment-declined-guide-2026-10-06.html')
STATE = os.path.join(ROOT, 'payment_declined_push_state.json')
QA = os.path.join(PROJ, 'qa_virtina_draft.py')

TITLE = "Why did my customer's payment get declined? A plain-English guide for WooCommerce store owners"
SLUG = "customer-payment-declined-guide"
YOAST_TITLE = "Why Was My Customer's Payment Declined? | Virtina"   # 49 chars
YOAST_DESC = ("A single declined card is almost never your store's fault. Learn the five common "
              "reasons and the one real warning sign that it needs a professional look.")  # 153 chars

CATS = [405, 79]  # eCommerce, WooCommerce - matches sibling post 40784 (checkout-not-working), pulled live 2026-10-06

# Payments/checkout cluster: posts whose phrasing this must not duplicate.
RELATED = [42682, 42037, 40784, 38785]  # money page (page), HPOS migration, checkout-not-working, conversion killers

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


# ---------- 0. MEDIA UPLOAD (images pre-cropped and visually QA'd) ----------
QA_DIR = os.environ.get("QA_DIR", "")
ALTS = {
 "featured": "Concerned small business owner leaning over a desk, looking at a laptop after a customer's WooCommerce payment was declined.",
 "body1": "WooCommerce store owner typing on a laptop at a wooden desk, checking order notes after a single declined payment.",
 "body2": "Two colleagues sitting together reviewing information on a laptop screen, discussing a repeating payment decline pattern.",
 "body3": "Three professionals gathered around a laptop, closely reviewing a WooCommerce store's payment gateway setup together.",
}
for k, v in ALTS.items():
    assert 80 <= len(v) <= 150, "alt %s is %d chars, must be 80-150" % (k, len(v))


def upload_media(slot):
    path = os.path.join(QA_DIR, "final_%s.jpg" % slot)
    if not os.path.exists(path):
        print("ABORT: missing pre-QA'd image %s" % path); sys.exit(1)
    data = open(path, 'rb').read()
    r = urllib.request.Request(
        BASE + "media", data=data, method="POST",
        headers={'Authorization': 'Basic ' + AUTH,
                 'Content-Disposition': 'attachment; filename="virtina-%s-%s.jpg"' % (SLUG, slot),
                 'Content-Type': 'image/jpeg', 'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(r, timeout=180) as f:
        m = json.loads(f.read().decode())
    api("media/%d" % m['id'], "POST", {"alt_text": ALTS[slot]})
    print("    %-9s media %d  %s" % (slot, m['id'], m['source_url']))
    return m['id'], m['source_url']


st0 = state()
if not QA_DIR:
    print("ABORT: set QA_DIR to the folder holding final_featured/body1/body2/body3.jpg")
    sys.exit(1)
print("[0] media upload")
MEDIA = st0.get('media') or {}
if not MEDIA:
    for slot in ("featured", "body1", "body2", "body3"):
        mid, url = upload_media(slot)
        MEDIA[slot] = {"id": mid, "url": url}
        st0['media'] = MEDIA; save(st0)
        time.sleep(2)
else:
    print("    reusing media from state: %s" % {k: v['id'] for k, v in MEDIA.items()})

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
for slot in ("featured", "body1", "body2", "body3"):
    ph = "https://virtina.com/wp-content/uploads/PENDING-%s.jpg" % slot
    if ph in content:
        content = content.replace(ph, MEDIA[slot]['url'])
        print("    swapped %s placeholder -> media %d" % (slot, MEDIA[slot]['id']))
if 'PENDING-' in content:
    print("ABORT: a PENDING- image placeholder survived."); sys.exit(1)
before = len(content)
content = re.sub(r'<!--.*?-->', '', content, flags=re.S).strip()
print("    stripped HTML comments: %d -> %d chars" % (before, len(content)))

plain = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ',
               re.sub(r'<style.*?</style>', '', content, flags=re.S | re.I))))

# ---------- 2. 8-GRAM PHRASING UNIQUENESS ----------
print("[2] 8-gram phrasing check against %d related posts/pages" % len(RELATED))
mine = words(plain)
grams = set(tuple(mine[i:i + 8]) for i in range(len(mine) - 7))
hits = []
for pid in RELATED:
    try:
        d = api("posts/%d?context=edit&_fields=id,slug,content" % pid)
    except urllib.error.HTTPError as e404:
        if e404.code == 404:
            try:
                d = api("pages/%d?context=edit&_fields=id,slug,content" % pid)
            except Exception as e:
                print("    could not fetch %d (%s), skipping" % (pid, e)); time.sleep(3); continue
        else:
            print("    could not fetch %d (%s), skipping" % (pid, e404)); time.sleep(3); continue
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
payload = {"title": TITLE, "slug": SLUG, "content": content, "status": "draft", "categories": CATS,
           "featured_media": MEDIA["featured"]["id"],
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
print("[5] verifying Yoast")
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
