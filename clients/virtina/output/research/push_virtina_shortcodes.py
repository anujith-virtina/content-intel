# Upload images + create the Virtina WooCommerce shortcodes draft.
# Images were hand-QA'd visually before selection (feedback_image_visual_qa).
import os, sys, json, base64, ssl, re, urllib.request

ctx = ssl._create_unverified_context()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
WP = "https://virtina.com/wp-json/wp/v2"
U, A = os.environ["WP_USERNAME"], os.environ["WP_APP_PASSWORD"]
AUTH = base64.b64encode(f"{U}:{A}".encode()).decode()
H = {"Authorization": "Basic " + AUTH, "User-Agent": UA}
S = os.path.dirname(os.path.abspath(__file__))
ROOT = r"C:\content-intel"
HTML = os.path.join(ROOT, r"clients\virtina\output\published\woocommerce-shortcodes-2026-08-10.html")

TITLE = "Are WooCommerce shortcodes deprecated? No, and here's what's actually happening in 2026"
SLUG = "woocommerce-shortcodes"
YOAST_TITLE = "Are WooCommerce Shortcodes Deprecated in 2026? | Virtina"
YOAST_DESC = ("WooCommerce shortcodes aren't deprecated in 2026. Get the full attribute reference, "
              "honest shortcode vs block guidance, and fixes for all 8 failure modes.")

IMAGES = [
    ("featured", "vfinal_featured.jpg", "virtina-woocommerce-shortcodes-featured.jpg",
     "Store developer reviewing WooCommerce shortcode setup on a laptop in an office boardroom before editing a product page"),
    ("1", "vfinal_body1.jpg", "virtina-woocommerce-shortcodes-body1.jpg",
     "Developer typing a WooCommerce products shortcode with limit, columns and category attributes into the WordPress code editor"),
    ("2", "vfinal_body2.jpg", "virtina-woocommerce-shortcodes-body2.jpg",
     "Two coworkers reviewing a WooCommerce shortcode versus block checkout comparison on a laptop during an office planning meeting"),
    ("3", "vfinal_body3.jpg", "virtina-woocommerce-shortcodes-body3.jpg",
     "Developer debugging a WooCommerce shortcode error on a desktop monitor at an office workstation"),
]

def req(url, data=None, headers=None, method=None):
    r = urllib.request.Request(url, data=data, headers=headers or H, method=method)
    return urllib.request.urlopen(r, timeout=90, context=ctx)

def upload(path, filename, alt):
    with open(path, "rb") as f:
        body = f.read()
    h = dict(H)
    h["Content-Disposition"] = f'attachment; filename="{filename}"'
    h["Content-Type"] = "image/jpeg"
    m = json.loads(req(f"{WP}/media", data=body, headers=h, method="POST").read())
    mid = m["id"]
    ph = dict(H); ph["Content-Type"] = "application/json"
    req(f"{WP}/media/{mid}", data=json.dumps({"alt_text": alt}).encode(), headers=ph, method="POST").read()
    return mid, m["source_url"]

DRY = "publish" not in sys.argv
html = open(HTML, encoding="utf-8").read()

# ---- blocking pre-flight: no placeholder may survive into the pushed content ----
print("Uploading images..." if not DRY else "DRY RUN (no upload)")
media = {}
if not DRY:
    for key, local, fname, alt in IMAGES:
        p = os.path.join(S, local)
        mid, url = upload(p, fname, alt)
        media[key] = (mid, url)
        print(f"  {key}: media {mid}  {url}")
        if not url.startswith("https://virtina.com/wp-content/uploads/"):
            raise SystemExit(f"BLOCKING: unexpected upload URL {url}")

    for n in ("1", "2", "3"):
        mid, url = media[n]
        html = html.replace("{{MEDIA_ID_%s}}" % n, str(mid)).replace("{{IMAGE_URL_%s}}" % n, url)

    left = re.findall(r"\{\{[A-Z_0-9]+\}\}", html)
    if left:
        raise SystemExit(f"BLOCKING: unresolved placeholders remain: {set(left)}")
    if "placehold.co" in html or "source.unsplash.com" in html:
        raise SystemExit("BLOCKING: banned image host in content")

if DRY:
    print("placeholders present:", sorted(set(re.findall(r"\{\{[A-Z_0-9]+\}\}", html))))
    print("content chars:", len(html))
    raise SystemExit(0)

payload = {
    "title": TITLE, "slug": SLUG, "status": "draft", "content": html,
    "excerpt": YOAST_DESC, "featured_media": media["featured"][0], "categories": [79],
    "meta": {"_yoast_wpseo_title": YOAST_TITLE, "_yoast_wpseo_metadesc": YOAST_DESC,
             "_yoast_wpseo_focuskw": "woocommerce shortcodes deprecated"},
}
ph = dict(H); ph["Content-Type"] = "application/json"
resp = req(f"{WP}/posts", data=json.dumps(payload).encode(), headers=ph, method="POST")
post = json.loads(resp.read())
print(f"\nPOST {resp.status} | POST_ID {post['id']} | status {post['status']}")
print("edit:", f"https://virtina.com/wp-admin/post.php?post={post['id']}&action=edit")
json.dump({"post_id": post["id"], "media": media}, open(os.path.join(S, "virtina_push_result.json"), "w"), indent=1)
