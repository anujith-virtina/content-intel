"""
Publish: shopify-vape-ban-merchant-deplatforming (Virtina).
Resizes+uploads 1 featured (1309x500) + 3 body (670x352) images to virtina.com,
substitutes __BODY_IMG_n__ / {{MEDIA_ID_n}} tokens in the built HTML, pushes a NEW
draft with featured_media + categories, tries Yoast meta, clears nothing (no Elementor).
Env: DRY_RUN=1 to validate without pushing.
"""
import os, ssl, base64, json, re, io, sys, urllib.request, urllib.error
from pathlib import Path
for ln in open(r"C:\content-intel\.env"):
    ln=ln.strip()
    if ln and not ln.startswith("#") and "=" in ln:
        k,v=ln.split("=",1); os.environ.setdefault(k.strip(),v.strip())
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
AUTH=base64.b64encode(f"{os.environ['WP_USERNAME']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()
HJSON={"Authorization":f"Basic {AUTH}","User-Agent":UA,"Content-Type":"application/json"}
ctx=ssl._create_unverified_context()
WP="https://virtina.com/wp-json/wp/v2"

HTML_PATH=r"C:\content-intel\clients\virtina\output\published\shopify-vape-ban-merchant-deplatforming-2026-07-15.html"
TITLE="Why Vape Retailers Lost Their Shopify Stores (And What to Do Now)"
SLUG="shopify-vape-ban-merchant-deplatforming"
META_TITLE="Why Vape Retailers Lost Their Shopify Stores | Virtina"
META_DESC=("Shopify banned ENDS/vape products in June 2026 with about two weeks' notice. Learn why any "
           "SaaS platform can deplatform you, and how to move to WooCommerce.")
CATEGORIES=[79,99]  # WooCommerce, Shopify

IMG_WOO=r"C:\Users\ASUS\AppData\Local\Temp\wooimg"
IMG_VT=r"C:\Users\ASUS\AppData\Local\Temp\vtimg"
FEAT_SRC=os.path.join(IMG_WOO,"scr_2.jpg")
B1_SRC=os.path.join(IMG_VT,"b1_0.jpg")
B2_SRC=os.path.join(IMG_WOO,"feat_2.jpg")
B3_SRC=os.path.join(IMG_VT,"b3_0.jpg")
FEAT_ALT=("Ecommerce professional at a desk with a widescreen monitor and keyboard working through a "
          "Shopify to WooCommerce store migration")
B1_ALT=("Business planning document and pen on an office desk, representing compliance and payment gateway "
        "review before a Shopify to WooCommerce migration")
B2_ALT=("Ecommerce team reviewing laptops and a migration plan at an office desk after a Shopify vape "
        "product ban")
B3_ALT=("Hands typing on a laptop keyboard while configuring a high-risk payment gateway for a WooCommerce "
        "store migration")

def resize(path,w,h,q=82):
    from PIL import Image
    im=Image.open(path).convert("RGB"); sw,sh=im.size
    sc=max(w/sw,h/sh); im=im.resize((int(sw*sc),int(sh*sc)),Image.LANCZOS)
    nw,nh=im.size; l,t=(nw-w)//2,(nh-h)//2; im=im.crop((l,t,l+w,t+h))
    buf=io.BytesIO(); im.save(buf,"JPEG",quality=q,optimize=True); d=buf.getvalue()
    if len(d)>200*1024:
        buf=io.BytesIO(); im.save(buf,"JPEG",quality=70,optimize=True); d=buf.getvalue()
    from PIL import Image as I2
    assert I2.open(io.BytesIO(d)).size==(w,h)
    print(f"  resized {os.path.basename(path)} -> {w}x{h} ({len(d)//1024}KB)")
    return d
def upload(jpeg,fn,alt):
    uh={"Authorization":f"Basic {AUTH}","User-Agent":UA,"Content-Type":"image/jpeg",
        "Content-Disposition":f'attachment; filename="{fn}"'}
    with urllib.request.urlopen(urllib.request.Request(f"{WP}/media",data=jpeg,headers=uh,method="POST"),timeout=120,context=ctx) as r:
        m=json.loads(r.read())
    mid,murl=m["id"],m["source_url"]
    with urllib.request.urlopen(urllib.request.Request(f"{WP}/media/{mid}",data=json.dumps({"alt_text":alt}).encode(),headers=HJSON,method="POST"),timeout=30,context=ctx) as r:
        r.read()
    print(f"  uploaded {fn}: id={mid}")
    return mid,murl

html=Path(HTML_PATH).read_text(encoding="utf-8")

# em-dash guard on final html
for form in ["—","&mdash;","&#8212;","&#x2014;"]:
    assert form not in html, f"em dash form found: {form}"
print("em-dash guard: PASS")
ext=re.findall(r'href="https?://(?!virtina\.com)[^"]+',html)
intn=re.findall(r'href="https://virtina\.com/[^"]+',html)
print(f"links: internal={len(intn)} external={len(ext)}")
assert len(ext)<=2, "too many external"
assert 5<=len(intn)<=10, f"internal link count {len(intn)}"
assert "shopify.com" not in html and "bigcommerce.com" not in html, "competitor link!"

if os.environ.get("DRY_RUN"):
    print("DRY_RUN: skipping upload/push"); sys.exit(0)

print("Uploading images...")
feat_id,feat_url=upload(resize(FEAT_SRC,1309,500),"shopify-vape-ban-woocommerce-migration-featured.jpg",FEAT_ALT)
b1_id,b1_url=upload(resize(B1_SRC,670,352),"vape-store-compliance-review.jpg",B1_ALT)
b2_id,b2_url=upload(resize(B2_SRC,670,352),"shopify-woocommerce-migration-team.jpg",B2_ALT)
b3_id,b3_url=upload(resize(B3_SRC,670,352),"high-risk-payment-gateway-setup.jpg",B3_ALT)

html=html.replace("__BODY_IMG_1__",b1_url).replace("{{MEDIA_ID_1}}",str(b1_id))
html=html.replace("__BODY_IMG_2__",b2_url).replace("{{MEDIA_ID_2}}",str(b2_id))
html=html.replace("__BODY_IMG_3__",b3_url).replace("{{MEDIA_ID_3}}",str(b3_id))
assert "__BODY_IMG_" not in html and "{{MEDIA_ID" not in html, "unsubstituted token"
for u in (feat_url,b1_url,b2_url,b3_url):
    assert u.startswith("https://virtina.com/wp-content/uploads/"), u
Path(HTML_PATH).write_text(html,encoding="utf-8")
print("Tokens substituted, HTML saved.")

payload={"title":TITLE,"slug":SLUG,"content":html,"status":"draft",
         "featured_media":feat_id,"categories":CATEGORIES}
# try with Yoast meta first
payload_meta=dict(payload)
payload_meta["meta"]={"yoast_wpseo_title":META_TITLE,"yoast_wpseo_metadesc":META_DESC}
yoast_ok=False; post_id=None
for attempt,pl in [("with-yoast",payload_meta),("no-yoast",payload)]:
    try:
        req=urllib.request.Request(f"{WP}/posts",data=json.dumps(pl).encode("utf-8"),headers=HJSON,method="POST")
        with urllib.request.urlopen(req,timeout=120,context=ctx) as r:
            resp=json.loads(r.read())
        post_id=resp["id"]; yoast_ok=(attempt=="with-yoast")
        print(f"PUSH OK ({attempt}): post {post_id} status={resp.get('status')} link={resp.get('link')}")
        break
    except urllib.error.HTTPError as e:
        body=e.read()[:400].decode('utf-8','replace')
        print(f"  push {attempt} HTTP {e.code}: {body}")
        if attempt=="no-yoast": sys.exit(1)
if post_id is None: sys.exit(1)

# verify
with urllib.request.urlopen(urllib.request.Request(f"{WP}/posts/{post_id}?context=edit",headers=HJSON),timeout=30,context=ctx) as r:
    v=json.loads(r.read())
print(f"Verified: status={v.get('status')} featured={v.get('featured_media')} cats={v.get('categories')}")
print(f"RESULTS_JSON={json.dumps({'post_id':post_id,'featured':feat_id,'body':[b1_id,b2_id,b3_id],'yoast_via_rest':yoast_ok,'categories':CATEGORIES})}")
print("YOAST_MANUAL_NEEDED:", not yoast_ok, "| Title:",META_TITLE,"| Desc:",META_DESC)
