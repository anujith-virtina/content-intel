"""
Build + publish: product-information-management-software (ChatSKU).
Format E (contrarian). Parses draft (mixed ### SECTION: + <h2>), builds Elementor,
Article+FAQPage+BreadcrumbList schema (NO HowTo), 1 featured + 2 body images (860x452).
BLOCKING: live HTTP-200 check on every internal link before push (per user 404 rule).
Env: DRY_RUN=1, REUSE_MEDIA="f,b1,b2", UPDATE_POST_ID, FORCE_STATUS.
"""
import json, secrets, re, urllib.request, urllib.error, base64, os, io, sys, ssl
from pathlib import Path
from collections import OrderedDict
_ssl=ssl._create_unverified_context()
for ln in open(r"C:\content-intel\.env"):
    ln=ln.strip()
    if ln and not ln.startswith("#") and "=" in ln:
        k,v=ln.split("=",1); os.environ.setdefault(k.strip(),v.strip())
WP="https://chatsku.com/wp-json/wp/v2"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
USER=os.environ.get("CHATSKU_WP_USERNAME",""); PW=os.environ.get("CHATSKU_WP_APP_PASSWORD","")
if not USER or not PW: print("ERROR: creds"); sys.exit(1)
AUTH=base64.b64encode(f"{USER}:{PW}".encode()).decode()
HEADERS={"Authorization":f"Basic {AUTH}","User-Agent":UA,"Content-Type":"application/json"}

DRAFT=r"C:\content-intel\clients\chatsku\output\drafts\product-information-management-software-2026-07-16.md"
TITLE="Product information management software organizes your data. It still can't answer your buyer."
SLUG="product-information-management-software"
DATE="2026-07-16"
META_TITLE="Product Information Management Software | ChatSKU"
META_DESC=("Product information management software keeps your product data clean and synced across channels. "
           "See why buyers still bounce, and what closes that gap fast.")

IMG=r"C:\Users\ASUS\AppData\Local\Temp\pimimg"
FEAT_SRC=os.path.join(IMG,"feat_3.jpg"); B1_SRC=os.path.join(IMG,"b1_5.jpg"); B2_SRC=os.path.join(IMG,"feat_1.jpg")
FEAT_ALT=("B2B buyer working at a laptop at a desk, the kind of visitor who asks a product question and needs "
          "a fast answer")
B1_ALT=("Person reviewing synced product and analytics data on a screen, representing clean, centralized PIM "
        "software data")
B2_ALT=("Laptop and tablet on a desk showing organized product data, the kind of catalog data a live assistant "
        "answers buyers from")

# ---- parse draft: normalize ### SECTION: -> <h2>, strip CTA placeholder ----
raw=Path(DRAFT).read_text(encoding="utf-8")
raw=re.sub(r'^---\n.*?\n---\n','',raw,count=1,flags=re.S)
raw=re.sub(r'<!--.*?-->','',raw,flags=re.S)
raw=re.sub(r'\[CTA BUTTON:.*?\]','',raw)
raw=raw.replace('</content>','')
raw=re.sub(r'^### SECTION: (.+)$',r'<h2>\1</h2>',raw,flags=re.M)
parts=re.split(r'<h2>(.*?)</h2>',raw,flags=re.S)
sections=OrderedDict()
for i in range(1,len(parts),2):
    title=parts[i].strip()
    body=parts[i+1].strip().replace('href="/','href="https://chatsku.com/')
    sections[title]=body
EXPECTED=["Executive summary","Introduction","What is product information management software?",
    "What does PIM software actually get right?","Why does clean PIM data still leave buyers stuck?",
    "What closes the gap between clean data and an answered buyer?","People also ask","Conclusion",
    "Frequently asked questions"]
missing=[h for h in EXPECTED if h not in sections]
if missing: print("FATAL missing:",missing); print("GOT:",list(sections)); sys.exit(1)
print(f"Parsed {len(sections)} sections.")

ALL_TEXT="\n".join(sections.values())
em=ALL_TEXT.count("—")+ALL_TEXT.count("&mdash;")
print(f"Em dash: {'PASS' if em==0 else 'FAIL'} ({em})")
if em: sys.exit(1)
BANNED=["just a chatbot","ai-powered","revolutionary","game-changing","cutting-edge","delve","leverage",
        "seamless","transform your","world-class","unlock value","synergize"]
bh=[b for b in BANNED if b in ALL_TEXT.lower()]
print(f"Banned: {'PASS' if not bh else 'FAIL '+str(bh)}")
if bh: sys.exit(1)

# ---- LIVE 200 internal link check (BLOCKING) ----
int_urls=sorted(set(re.findall(r'href="(https://chatsku\.com/[^"]+)"',ALL_TEXT)))
print("\nLIVE LINK CHECK (blocking):")
bad=[]
for u in int_urls:
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA}),timeout=40,context=_ssl)
        redir = r.geturl().rstrip('/')!=u.rstrip('/')
        status="OK" if (r.status==200 and not redir) else (f"REDIRECT->{r.geturl()}" if redir else f"code {r.status}")
        print(f"  [{r.status}] {u}  {status}")
        if r.status!=200 or redir: bad.append((u,status))
    except Exception as e:
        print(f"  [ERR] {u}  {e}"); bad.append((u,str(e)))
if bad:
    print("LINK CHECK FAILED (fix before publish):",bad); sys.exit(1)
print("All internal links resolve 200, no redirects.")

# ---- elementor builders ----
def gid(): return secrets.token_hex(4)
def make_heading(t,level="h2",color="#1a1a2e",align="left"):
    size=28 if level=="h2" else 22
    s={"title":t,"align":align,"title_color":color,"typography_typography":"custom","typography_font_size":{"size":size,"unit":"px"}}
    if level!="h2": s["header_size"]=level
    return {"id":gid(),"elType":"widget","widgetType":"heading","elements":[],"settings":s}
def make_text(html,dark=False):
    if dark: html=re.sub(r'<p([ >])',r'<p style="color:#aaaacc;text-align:center;font-size:18px;max-width:720px;margin:0 auto;"\1',html)
    return {"id":gid(),"elType":"widget","widgetType":"text-editor","elements":[],"settings":{"editor":html}}
def make_image_widget(img):
    return {"id":gid(),"elType":"widget","widgetType":"image","elements":[],
            "settings":{"image":{"id":img["id"],"url":img["url"],"alt":img["alt"],"source":"library","size":""},
                        "align":"center","width":{"size":100,"unit":"%"},
                        "border_radius":{"top":"10","right":"10","bottom":"10","left":"10","unit":"px"}}}
def make_button(t,url):
    return {"id":gid(),"elType":"widget","widgetType":"button","elements":[],
            "settings":{"text":t,"link":{"url":url,"is_external":"","nofollow":""},"align":"center",
                        "background_color":"#e94560","button_text_color":"#ffffff","border_radius":{"size":6,"unit":"px"},
                        "_margin":{"unit":"px","top":"20","right":"0","bottom":"0","left":"0","isLinked":False}}}
def make_html_widget(html): return {"id":gid(),"elType":"widget","widgetType":"html","elements":[],"settings":{"html":html}}
def make_section(widgets,bg,concl=False):
    pad={"top":"20","bottom":"30","unit":"px","right":"0","left":"0"} if concl else {"top":"60","bottom":"60","unit":"px"}
    return {"id":gid(),"elType":"section","isInner":False,
            "settings":{"background_background":"classic","background_color":bg,"padding":pad},
            "elements":[{"id":gid(),"elType":"column","isInner":False,
                         "settings":{"_column_size":100,"width":"100","padding":{"unit":"px","top":"20","right":"20","bottom":"20","left":"20","isLinked":True}},
                         "elements":widgets}]}
def strip_inline(s): return re.sub(r'<[^>]+>','',s)
def make_accordion(html):
    pairs=re.findall(r'<h3>(.*?)</h3>\s*(<p>.*?</p>)',html,flags=re.S)
    tabs=[{"tab_title":strip_inline(q).strip(),"tab_content":re.sub(r'^\s*<p>(.*)</p>\s*$',r'\1',a.strip(),flags=re.S).strip(),"_id":secrets.token_hex(4)[:7]} for q,a in pairs]
    return {"id":gid(),"elType":"widget","widgetType":"accordion","elements":[],"settings":{"tabs":tabs,"title_html_tag":"h3"}},len(tabs)
def split_widgets(html):
    out=[]
    for part in re.split(r'(<h3>.*?</h3>)',html,flags=re.S):
        p=part.strip()
        if not p: continue
        m=re.match(r'<h3>(.*?)</h3>$',p,flags=re.S)
        out.append(make_heading(m.group(1).strip(),"h3") if m else make_text(p))
    return out
def strip_tags(s): return re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',s)).strip()

def build_schema(feat_url):
    article={"@context":"https://schema.org","@type":"Article","headline":TITLE,"description":META_DESC,
             "image":feat_url,"datePublished":DATE,"dateModified":DATE,
             "author":{"@type":"Organization","name":"ChatSKU","url":"https://chatsku.com"},
             "publisher":{"@type":"Organization","name":"ChatSKU","logo":{"@type":"ImageObject","url":"https://chatsku.com/wp-content/uploads/2024/logo.png"}},
             "mainEntityOfPage":{"@type":"WebPage","@id":f"https://chatsku.com/{SLUG}/"}}
    faqs=[(strip_tags(q),strip_tags(a)) for q,a in re.findall(r'<h3>(.*?)</h3>\s*<p>(.*?)</p>',sections["Frequently asked questions"],flags=re.S)]
    faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":"https://chatsku.com/"},
        {"@type":"ListItem","position":2,"name":"Blog","item":"https://chatsku.com/blog/"},
        {"@type":"ListItem","position":3,"name":TITLE,"item":f"https://chatsku.com/{SLUG}/"}]}
    blocks,types=[],[]
    for nm,obj in [("Article",article),("FAQPage",faqpage),("BreadcrumbList",bc)]:
        s=json.dumps(obj,ensure_ascii=False); json.loads(s)
        blocks.append(f'<script type="application/ld+json">\n{s}\n</script>'); types.append(obj["@type"])
        print(f"  JSON-LD {nm}: valid")
    return "\n".join(blocks),types,len(faqs)

def resize(path,w=860,h=452,q=84):
    from PIL import Image
    im=Image.open(path).convert("RGB"); sw,sh=im.size
    sc=max(w/sw,h/sh); im=im.resize((int(sw*sc),int(sh*sc)),Image.LANCZOS)
    nw,nh=im.size; l,t=(nw-w)//2,(nh-h)//2; im=im.crop((l,t,l+w,t+h))
    buf=io.BytesIO(); im.save(buf,"JPEG",quality=q,optimize=True); d=buf.getvalue()
    if len(d)>200*1024:
        buf=io.BytesIO(); im.save(buf,"JPEG",quality=72,optimize=True); d=buf.getvalue()
    from PIL import Image as I2; assert I2.open(io.BytesIO(d)).size==(w,h)
    print(f"  resized {os.path.basename(path)} -> {w}x{h} ({len(d)//1024}KB)"); return d
def upload(jpeg,fn,alt):
    uh={"Authorization":f"Basic {AUTH}","User-Agent":UA,"Content-Type":"image/jpeg","Content-Disposition":f'attachment; filename="{fn}"'}
    with urllib.request.urlopen(urllib.request.Request(f"{WP}/media",data=jpeg,headers=uh,method="POST"),timeout=90,context=_ssl) as r:
        m=json.loads(r.read())
    with urllib.request.urlopen(urllib.request.Request(f"{WP}/media/{m['id']}",data=json.dumps({"alt_text":alt}).encode(),headers=HEADERS,method="POST"),timeout=30,context=_ssl) as r: r.read()
    print(f"  uploaded {fn}: id={m['id']}"); return {"id":m["id"],"url":m["source_url"],"alt":alt}
def fetch_media(mid,alt):
    with urllib.request.urlopen(urllib.request.Request(f"{WP}/media/{mid}",headers=HEADERS),timeout=30,context=_ssl) as r: m=json.loads(r.read())
    return {"id":int(mid),"url":m["source_url"],"alt":alt}

DRY=os.environ.get("DRY_RUN"); REUSE=os.environ.get("REUSE_MEDIA")
if DRY:
    feat={"id":9001,"url":"https://chatsku.com/wp-content/uploads/2026/07/f.jpg","alt":FEAT_ALT}
    b1={"id":9002,"url":"https://chatsku.com/wp-content/uploads/2026/07/b1.jpg","alt":B1_ALT}
    b2={"id":9003,"url":"https://chatsku.com/wp-content/uploads/2026/07/b2.jpg","alt":B2_ALT}
    print("DRY images")
elif REUSE:
    f,x,y=[z.strip() for z in REUSE.split(",")]; feat,b1,b2=fetch_media(f,FEAT_ALT),fetch_media(x,B1_ALT),fetch_media(y,B2_ALT)
    print(f"Reusing media {f},{x},{y}")
else:
    print("Uploading images...")
    feat=upload(resize(FEAT_SRC),"chatsku-pim-software-buyer-laptop.jpg",FEAT_ALT)
    b1=upload(resize(B1_SRC),"chatsku-pim-clean-product-data.jpg",B1_ALT)
    b2=upload(resize(B2_SRC),"chatsku-catalog-data-live-answer.jpg",B2_ALT)
imgs=[feat,b1,b2]
for lbl,m in zip(["feat","b1","b2"],imgs):
    if not m["url"].startswith("https://chatsku.com/wp-content/uploads/"): print("FATAL url",lbl,m["url"]); sys.exit(1)
print(f"Images: feat={feat['id']} b1={b1['id']} b2={b2['id']}")

BODY_CYCLE=["#f0f4ff","#ffffff","#f9f9fb","#ffffff"]
IMG_AFTER={"What does PIM software actually get right?":b1,"What closes the gap between clean data and an answered buyer?":b2}
elementor=[]; bi=0
for head,html in sections.items():
    if head=="Executive summary": bg="#f9f9fb"
    elif head=="Introduction": bg="#ffffff"
    elif head=="Conclusion":
        elementor.append(make_section([make_heading("Conclusion",color="#ffffff",align="center"),
            make_text(html,dark=True),make_button("See the live demo","https://chatsku.com/demo/")],bg="#1a1a2e",concl=True)); continue
    elif head=="Frequently asked questions":
        acc,n=make_accordion(html); elementor.append(make_section([make_heading(head,"h2"),acc],bg="#f9f9fb")); print(f"FAQ accordion {n} tabs"); continue
    else: bg=BODY_CYCLE[bi%len(BODY_CYCLE)]; bi+=1
    w=[make_heading(head,"h2")]+split_widgets(html)
    if head in IMG_AFTER: w.append(make_image_widget(IMG_AFTER[head]))
    elementor.append(make_section(w,bg=bg))

schema_html,schema_types,n_faq=build_schema(feat["url"])
ss=make_section([make_html_widget(schema_html)],bg="#ffffff"); ss["settings"]["padding"]={"top":"0","bottom":"0","unit":"px"}
elementor.append(ss)
elementor_json=json.dumps(elementor)

def sec_to_content(s):
    out=[]
    for w in s["elements"][0]["elements"]:
        wt=w.get("widgetType")
        if wt=="heading": lv=w["settings"].get("header_size","h2"); out.append(f"<{lv}>{w['settings']['title']}</{lv}>")
        elif wt=="text-editor": out.append(w["settings"]["editor"])
        elif wt=="button": out.append(f'<p><a href="{w["settings"]["link"]["url"]}">{w["settings"]["text"]}</a></p>')
        elif wt=="accordion":
            for t in w["settings"]["tabs"]: out.append(f'<h3>{t["tab_title"]}</h3>\n<p>{t["tab_content"]}</p>')
        elif wt=="html": out.append(w["settings"]["html"])
    return "\n".join(out)
wp_content=re.sub(r'<img[^>]*>','',"\n\n".join(sec_to_content(s) for s in elementor))

# ---- checklist ----
print("\nCHECKLIST")
c={}
c["Em dash 0"]=em==0; c["No banned"]=not bh
c["Slug ok"]=SLUG=="product-information-management-software"
c["Featured media"]=bool(feat["id"])
c["Img urls"]=all(m["url"].startswith("https://chatsku.com/wp-content/uploads/") for m in imgs)
alts=[m["alt"] for m in imgs]; c["Alt 80-150 uniq"]=all(80<=len(a)<=150 for a in alts) and len(set(alts))==3
extl=re.findall(r'href="https?://(?!chatsku\.com)[^"]+',ALL_TEXT); c["External<=2"]=len(extl)<=2
intl=re.findall(r'href="https://chatsku\.com/[^"]+',ALL_TEXT); c["Internal>=4"]=len(intl)>=4
BLOG=["passive-catalog-costing-you-sales","what-is-the-response-gap","what-is-a-b2b-catalog-chatbot"]
c["Blog links>=2"]=sum(1 for b in BLOG if f"chatsku.com/{b}/" in ALL_TEXT)>=2
c["No competitor"]=not any(x in ALL_TEXT.lower() for x in ["akeneo","salsify","pimcore","inriver","plytix","drift.com","tidio","intercom.com"])
conc=next(s for s in elementor if s["settings"]["background_color"]=="#1a1a2e"); cw=conc["elements"][0]["elements"]
hw=next((w for w in cw if w["widgetType"]=="heading"),None); bw=next((w for w in cw if w["widgetType"]=="button"),None)
c["Concl white center"]=bool(hw) and hw["settings"]["title_color"]=="#ffffff" and hw["settings"]["align"]=="center"
c["Concl btn demo"]=bool(bw) and bw["settings"]["link"]["url"]=="https://chatsku.com/demo/"
c["Exec first"]=elementor[0]["elements"][0]["elements"][0]["settings"]["title"]=="Executive summary"
c["Schema 3"]=set(schema_types)=={"Article","FAQPage","BreadcrumbList"}
c["FAQ 6-8"]=6<=n_faq<=8
c["No bare img"]="<img" not in wp_content
c["Img after text"]=all(not ("image" in (t:=[w.get("widgetType") for w in s["elements"][0]["elements"]]) and "text-editor" in t and t.index("image")<t.index("text-editor")) for s in elementor)
ot=[ (s["elements"][0]["elements"][0]["settings"].get("title","")) for s in elementor]
c["Concl before FAQ"]="Conclusion" in ot and "Frequently asked questions" in ot and ot.index("Conclusion")<ot.index("Frequently asked questions")
acc=[w for s in elementor for w in s["elements"][0]["elements"] if w.get("widgetType")=="accordion"]; c["FAQ accordion"]=len(acc)==1
c["kw in title"]="product information management software" in TITLE.lower()
plain=re.sub(r'<[^>]+>',' ',ALL_TEXT); wc=len(plain.split()); c["Words 1200-2200"]=1200<=wc<=2200
c["Meta title<=60"]=len(META_TITLE)<=60 and META_TITLE.endswith("| ChatSKU")
c["Meta desc 150-160"]=150<=len(META_DESC)<=160
for k,v in c.items(): print(f"  [{'PASS' if v else 'FAIL'}] {k}")
print(f"  ext={len(extl)} int={len(intl)} words={wc} faq={n_faq} metaTitle={len(META_TITLE)} metaDesc={len(META_DESC)}")
if not all(c.values()): print("FAILED:",[k for k,v in c.items() if not v]); sys.exit(1)
print("ALL CHECKS PASS")
if DRY: print("DRY stop"); sys.exit(0)

print("\nPUSHING (draft)")
UPD=os.environ.get("UPDATE_POST_ID","")
payload={"title":TITLE,"slug":SLUG,"content":wp_content,"featured_media":feat["id"],
         "meta":{"_elementor_edit_mode":"builder","_elementor_template_type":"wp-post","_elementor_data":elementor_json}}
if UPD:
    fs=os.environ.get("FORCE_STATUS","")
    if fs: payload["status"]=fs
    else:
        with urllib.request.urlopen(urllib.request.Request(f"{WP}/posts/{UPD}?context=edit",headers=HEADERS),timeout=20,context=_ssl) as r: print("live status:",json.loads(r.read()).get("status"))
    url=f"{WP}/posts/{UPD}"
else: payload["status"]="draft"; url=f"{WP}/posts"
try:
    with urllib.request.urlopen(urllib.request.Request(url,data=json.dumps(payload).encode(),headers=HEADERS,method="POST"),timeout=120,context=_ssl) as r: resp=json.loads(r.read())
except urllib.error.HTTPError as e: print("HTTP",e.code,e.read()[:500]); sys.exit(1)
pid=resp["id"]; print(f"Post {pid} status={resp.get('status')} link={resp.get('link')}")
with urllib.request.urlopen(urllib.request.Request(f"{WP}/posts/{pid}?context=edit",headers=HEADERS),timeout=30,context=_ssl) as r: v=json.loads(r.read())
print(f"Verified sections={len(json.loads(v.get('meta',{}).get('_elementor_data','[]')))} featured={v.get('featured_media')} status={v.get('status')}")
try:
    with urllib.request.urlopen(urllib.request.Request("https://chatsku.com/wp-json/elementor/v1/cache",headers={"Authorization":f"Basic {AUTH}","User-Agent":UA},method="DELETE"),timeout=20,context=_ssl) as r: print("cache clear",r.status)
except Exception as e: print("cache",e)
def sec_pub(s):
    out=[]
    for w in s["elements"][0]["elements"]:
        wt=w.get("widgetType")
        if wt=="heading": lv=w["settings"].get("header_size","h2"); out.append(f"<{lv}>{w['settings']['title']}</{lv}>")
        elif wt=="text-editor": out.append(w["settings"]["editor"])
        elif wt=="image": im=w["settings"]["image"]; out.append(f'<img src="{im["url"]}" alt="{im["alt"]}" width="860" height="452">')
        elif wt=="button": out.append(f'<p><a href="{w["settings"]["link"]["url"]}">{w["settings"]["text"]}</a></p>')
        elif wt=="accordion":
            for t in w["settings"]["tabs"]: out.append(f'<h3>{t["tab_title"]}</h3>\n<p>{t["tab_content"]}</p>')
        elif wt=="html": out.append(w["settings"]["html"])
    return "\n".join(out)
pub=(f'<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{META_TITLE}</title>'
     f'<meta name="description" content="{META_DESC}">\n<!-- Post {pid} | {SLUG} | Format E | {DATE} -->\n'
     f'<!-- Feat {feat["id"]} B1 {b1["id"]} B2 {b2["id"]} | Yoast manual: {META_TITLE} / {META_DESC} -->\n</head><body>\n'
     f'<h1>{TITLE}</h1>\n<img src="{feat["url"]}" width="860" height="452" alt="{FEAT_ALT}">\n'
     +"\n\n".join(sec_pub(s) for s in elementor)+"\n</body></html>")
Path(r"C:\content-intel\clients\chatsku\output\published\product-information-management-software-2026-07-16.html").write_text(pub,encoding="utf-8")
print(f"RESULTS_JSON={json.dumps({'post_id':pid,'feat':feat['id'],'b1':b1['id'],'b2':b2['id'],'words':wc,'internal':len(intl),'external':len(extl),'faqs':n_faq})}")
print("MANUAL YOAST -> Title:",META_TITLE,"| Desc:",META_DESC)
