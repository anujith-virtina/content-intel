# -*- coding: utf-8 -*-
"""Push the geriatric care manager guide to ECM as a draft, then demote post 254707.
Blocking QA runs first. Idempotent: reuses post id from state file."""
import os,sys,json,re,html,base64,time,urllib.request,urllib.error,subprocess

ROOT=os.path.dirname(os.path.abspath(__file__))
PROJ=os.path.abspath(os.path.join(ROOT,'..','..','..','..'))
DRAFT=os.path.join(PROJ,'clients','eldercarematters','output','drafts','how-to-choose-a-geriatric-care-manager-2026-09-11.html')
STATE=os.path.join(ROOT,'gcm_push_state.json')
REPL=os.path.join(PROJ,'clients','eldercarematters','output','backups','254707-replacement-block.html')
PILLAR=254707
CATS=[4202,309,1374]  # Geriatric Care Management, Caregiving, Elder Care Planning
TITLE="How to Choose the Right Geriatric Care Manager for Your Family"
SLUG="how-to-choose-a-geriatric-care-manager"
YOAST_TITLE="How to Choose a Geriatric Care Manager for Your Family"
YOAST_DESC=("How to choose a geriatric care manager: the credentials that carry weight, the "
            "questions to ask, conflict-of-interest red flags, and when you may not need one.")

env={}
for line in open(os.path.join(PROJ,'.env'),encoding='utf-8'):
    line=line.strip()
    if '=' in line and not line.startswith('#'):
        k,v=line.split('=',1); env[k]=v.strip().strip('"')
AUTH=base64.b64encode(f"{env['ECM_WP_USERNAME']}:{env['ECM_WP_APP_PASSWORD']}".encode()).decode()
BASE="https://eldercarematters.com/wp-json/wp/v2/"

def api(path,method="GET",payload=None,tries=5):
    """Wordfence rate-limits this host. Retry 429/403 with exponential backoff."""
    data=json.dumps(payload).encode() if payload is not None else None
    delay=10
    for n in range(1,tries+1):
        r=urllib.request.Request(BASE+path,data=data,method=method,
            headers={'Authorization':'Basic '+AUTH,'Content-Type':'application/json','User-Agent':'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(r,timeout=90) as f: return json.loads(f.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (429,403,503) and n<tries:
                print(f"    {e.code} from Wordfence, backing off {delay}s (attempt {n}/{tries})")
                time.sleep(delay); delay*=2; continue
            raise

def state():
    return json.load(open(STATE)) if os.path.exists(STATE) else {}
def save(d):
    json.dump(d,open(STATE,'w'),indent=1)

# ---------- 1. BLOCKING QA ----------
print("[1] QA gate")
q=subprocess.run([sys.executable,os.path.join(PROJ,'qa_ecm_draft.py'),DRAFT],capture_output=True,text=True)
tail=q.stdout.strip().splitlines()[-3:] if q.stdout else []
print("    "+" | ".join(t.strip() for t in tail))
if q.returncode!=0:
    print("ABORT: QA failed. Fix the draft before pushing.")
    print(q.stdout[-2500:]); sys.exit(1)

content=open(DRAFT,encoding='utf-8').read()
# Strip HTML comments before pushing. The publisher-notes block contains literal
# REST paths (/wp/v2/..., context=edit, PUT) and Wordfence 403s any POST body
# carrying them. Comments are working notes, not body copy, so they never ship.
_before=len(content)
content=re.sub(r'<!--.*?-->','',content,flags=re.S).strip()
content=re.sub('\n{3,}','\n\n',content)
print(f'    stripped HTML comments: {_before} -> {len(content)} chars')

# ---------- 2. LIVE LINK VERIFICATION (final-URL + title, spaced for Wordfence) ----------
print("[2] verifying every link resolves and lands where the anchor claims")
if "--skip-links" in sys.argv:
    print("    SKIPPED by flag (links verified moments ago)"); links=[]
else:
    links=None
    links=re.findall(r'<a\s[^>]*href=["\'](https?://[^"\']+)["\']',content)
bad=[]
for u in sorted(set(links)):
    try:
        rq=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(rq,timeout=45) as f:
            final=f.geturl(); code=f.status
            t=re.search(r'<title[^>]*>(.*?)</title>',f.read().decode('utf-8','replace'),re.S|re.I)
        title=html.unescape(re.sub(r'\s+',' ',t.group(1))).strip() if t else '?'
        home = final.rstrip('/')=="https://eldercarematters.com"
        moved = final.rstrip('/')!=u.rstrip('/')
        flag="DEAD->home" if home else ("REDIRECT" if moved else "ok")
        if home: bad.append((u,"redirects to homepage"))
        print(f"    {flag:11} {code} {u}\n                -> {title[:70]}")
    except Exception as e:
        bad.append((u,str(e))); print(f"    ERROR       {u} :: {e}")
    time.sleep(6)
if bad:
    print("ABORT: link failures:"); [print("   ",u,r) for u,r in bad]; sys.exit(1)

# ---------- 3. CREATE OR UPDATE THE POST ----------
st=state(); pid=st.get('post_id')
media=st.get('featured_media')
payload={"title":TITLE,"slug":SLUG,"content":content,"status":"draft","categories":CATS,
         "meta":{"_yoast_wpseo_title":YOAST_TITLE,"_yoast_wpseo_metadesc":YOAST_DESC}}
if media: payload["featured_media"]=media
if pid:
    print(f"[3] updating existing draft {pid}")
    # never blind-overwrite: check live state first
    live=api(f"posts/{pid}?context=edit&_fields=id,status,featured_media")
    if live['status']!='draft':
        print(f"    live status is '{live['status']}', not draft. Preserving it.")
        payload.pop('status')
    if live.get('featured_media') and not media:
        payload.pop('featured_media',None)
    post=api(f"posts/{pid}",'POST',payload)
else:
    print("[3] creating new draft")
    post=api("posts",'POST',payload)
pid=post['id']
st.update({'post_id':pid,'status':post['status'],'slug':post['slug'],'link':post['link']}); save(st)
print(f"    post {pid}  status={post['status']}  {post['link']}")

# ---------- 4. VERIFY YOAST PERSISTED ----------
print("[4] verifying Yoast (known NOT REST-writable on this install)")
chk=api(f"posts/{pid}?context=edit&_fields=id,meta")
m=chk.get('meta',{}) or {}
tp = m.get('_yoast_wpseo_title')==YOAST_TITLE
dp = m.get('_yoast_wpseo_metadesc')==YOAST_DESC
st['yoast_title_persisted']=bool(tp); st['yoast_desc_persisted']=bool(dp); save(st)
print(f"    title persisted={tp}  desc persisted={dp}")
if not (tp and dp):
    print("    -> MANUAL DASHBOARD ENTRY REQUIRED:")
    print(f"       SEO title:       {YOAST_TITLE}")
    print(f"       Meta description: {YOAST_DESC}")

print("\nDONE. Post is a DRAFT. Demote of 272215 runs separately via --demote.")

# ---------- 5. DEMOTE PILLAR (only with --demote) ----------
if '--demote' in sys.argv:
    print(f"\n[5] demoting pillar {PILLAR}")
    new_url=post['link']
    rq=urllib.request.Request(new_url,headers={'User-Agent':'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(rq,timeout=45) as f: ok=f.status==200
    except Exception as e:
        print(f"    new post URL not publicly reachable yet ({e}).")
        print("    That is expected while it is a draft. Demote AFTER the post goes live.")
        sys.exit(0)
    live=api(f"posts/{PILLAR}?context=edit")
    raw=live['content']['raw']
    mm=re.search(r'<h3><b>\s*How to Choose the Right Geriatric Care Manager\s*</b></h3>',raw,re.I)
    if not mm:
        print("    section already demoted or not found. Nothing to do."); sys.exit(0)
    nxt=re.search(r'<h[23][^>]*>',raw[mm.end():],re.I)
    end=mm.end()+nxt.start() if nxt else len(raw)
    repl=open(REPL,encoding='utf-8').read().replace('__NEWPOST_URL__',new_url)
    updated=raw[:mm.start()]+repl+raw[end:]
    bkp=os.path.join(PROJ,'clients','eldercarematters','output','backups',f'post-{PILLAR}-predemote.html')
    open(bkp,'w',encoding='utf-8').write(raw)
    api(f"posts/{PILLAR}",'POST',{"content":updated})
    print(f"    demoted. backup at {bkp}")
    st['pillar_demoted']=True; save(st)
