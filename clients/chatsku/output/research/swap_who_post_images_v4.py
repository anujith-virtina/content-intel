"""Swap the three images on post 3798 (who-b2b-catalog-assistant-is-built-for) for AI-generated crops.

Usage:
  python swap_who_post_images.py          # dry run: uploads nothing, prints what would change
  python swap_who_post_images.py apply    # uploads 3 images, updates post 3798 in place, clears Elementor cache

Only touches: featured_media, the two body image widgets, and any stock credit paragraphs.
Never touches title, status, Yoast fields, categories, or any other widget. Never re-pushes the whole post.
"""
import base64, io, json, os, re, sys, urllib.request
from PIL import Image

ENV_PATH = r"C:\content-intel\.env"
SCRATCH = r"C:\Users\ASUS\AppData\Local\Temp\claude\C--content-intel\9cb78ece-d8e6-4474-956c-1b343c768e5b\scratchpad\cs_who3"
STATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "who_post_images_v4_state.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0.0.0 Safari/537.36")
WP = "https://chatsku.com/wp-json/wp/v2"
POST_ID = 3798
SLUG = "who-b2b-catalog-assistant-is-built-for"
EXPECTED_MODIFIED = None  # checked below against the v2 swap instead
FEATURED_OLD = 3888

# old body image id -> (new file, new alt text, slot name)
BODY_OLD_TO_NEW = {
    3889: ("data.jpg",
           "Flat-lay of the files a product catalog is built from: a printed PDF price list, an Excel workbook, CSV printouts and an ERP report with barcode labels.",
           "body1"),
    3890: ("buyer.jpg",
           "A buyer's desk at night with a laptop comparison table, a phone product page and a handwritten checklist of questions to ask.",
           "body2"),
}
FEATURED_FILE = ("featured.jpg",
                 "A quote request form, a tablet product page and a printed catalog laid out on a desk, the steps from buyer question to quote.",
                 "featured")
CREDIT_PREFIXES = ("Featured photo:", "Photo:", "Booth photo:", "Laptop photo:", "Warehouse photo:", "Image:")


def load_env():
    env = {}
    for line in open(ENV_PATH, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


ENV = load_env()
AUTH = base64.b64encode(f"{ENV['CHATSKU_WP_USERNAME']}:{ENV['CHATSKU_WP_APP_PASSWORD']}".encode()).decode()
H = {"Authorization": f"Basic {AUTH}", "User-Agent": UA}


def get_json(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=60))


def upload(path, alt, slot):
    im = Image.open(path).convert("RGB")
    assert im.size == (860, 452), f"{path} is {im.size}"
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=82, optimize=True)
    data = buf.getvalue()
    assert len(data) <= 200 * 1024, f"{slot} too big: {len(data)}"
    req = urllib.request.Request(f"{WP}/media", data=data, method="POST",
                                 headers={**H, "Content-Type": "image/jpeg",
                                          "Content-Disposition": f'attachment; filename="{SLUG}-{slot}-ai.jpg"'})
    mid = json.load(urllib.request.urlopen(req, timeout=60))
    req2 = urllib.request.Request(f"{WP}/media/{mid['id']}", method="POST",
                                  data=json.dumps({"alt_text": alt, "title": f"{SLUG} {slot} ai"}).encode(),
                                  headers={**H, "Content-Type": "application/json"})
    mid = json.load(urllib.request.urlopen(req2, timeout=60))
    return {"id": mid["id"], "url": mid["source_url"], "alt": alt}


def strip_credit_paragraphs(html):
    removed = []
    def repl(m):
        text = re.sub(r"<[^>]+>", "", m.group(0)).strip()
        if text.startswith(CREDIT_PREFIXES):
            removed.append(text[:80])
            return ""
        return m.group(0)
    new = re.sub(r"<p[^>]*>.*?</p>", repl, html, flags=re.S)
    return new, removed


def walk(node, pred, out):
    if isinstance(node, dict):
        if pred(node):
            out.append(node)
        for v in node.values():
            walk(v, pred, out)
    elif isinstance(node, list):
        for x in node:
            walk(x, pred, out)


def main():
    apply = len(sys.argv) > 1 and sys.argv[1].lower() == "apply"
    if apply and os.path.exists(STATE_PATH):
        sys.exit("BLOCKING: state file exists; images already swapped on this post.")

    live = get_json(f"{WP}/posts/{POST_ID}?context=edit")
    assert live["status"] in ("draft", "publish"), f"unexpected status {live['status']}"
    assert live["featured_media"] == FEATURED_OLD, f"featured is {live['featured_media']}"
    print("live status:", live["status"], "| featured:", live["featured_media"], "|", live["link"])

    data = json.loads(live["meta"]["_elementor_data"])
    imgs = []
    walk(data, lambda n: n.get("widgetType") == "image", imgs)
    old_ids = sorted(w["settings"]["image"]["id"] for w in imgs)
    print("image widgets:", old_ids)
    assert old_ids == sorted(BODY_OLD_TO_NEW), f"unexpected body image ids {old_ids}"

    texts = []
    walk(data, lambda n: n.get("widgetType") == "text-editor", texts)
    credits_el = []
    for s in texts:
        _, r = strip_credit_paragraphs(s["settings"].get("editor", ""))
        credits_el += r
    _, credits_content = strip_credit_paragraphs(live["content"]["raw"])
    print("credit paragraphs in elementor:", credits_el)
    print("credit paragraphs in content:", credits_content)

    if not apply:
        print("DRY RUN ok. Run 'apply' to upload and update post 3798.")
        return

    feat = upload(os.path.join(SCRATCH, FEATURED_FILE[0]), FEATURED_FILE[1], FEATURED_FILE[2])
    print("uploaded featured ->", feat["id"])
    new_body = {}
    for old, (fname, alt, slot) in BODY_OLD_TO_NEW.items():
        new_body[old] = upload(os.path.join(SCRATCH, fname), alt, slot)
        print("uploaded", slot, "->", new_body[old]["id"])

    for w in imgs:
        old = w["settings"]["image"]["id"]
        nm = new_body[old]
        w["settings"]["image"] = {"id": nm["id"], "url": nm["url"], "alt": nm["alt"], "source": "library", "size": ""}
    for s in texts:
        s["settings"]["editor"], _ = strip_credit_paragraphs(s["settings"].get("editor", ""))

    content, _ = strip_credit_paragraphs(live["content"]["raw"])
    payload = {
        "content": content,
        "featured_media": feat["id"],
        "meta": {"_elementor_data": json.dumps(data, ensure_ascii=False)},
    }
    req = urllib.request.Request(f"{WP}/posts/{POST_ID}", data=json.dumps(payload).encode(), method="POST",
                                 headers={**H, "Content-Type": "application/json"})
    upd = json.load(urllib.request.urlopen(req, timeout=120))
    print("updated post", upd["id"], "status", upd["status"])

    try:
        req = urllib.request.Request("https://chatsku.com/wp-json/elementor/v1/cache", method="DELETE", headers=H)
        urllib.request.urlopen(req, timeout=60)
        print("elementor cache cleared")
    except Exception as e:
        print("elementor cache clear failed:", e)

    chk = get_json(f"{WP}/posts/{POST_ID}?context=edit")
    left = []
    walk(json.loads(chk["meta"]["_elementor_data"]), lambda n: n.get("widgetType") == "image", left)
    print("verify: status", chk["status"], "| featured", chk["featured_media"],
          "| widget ids", sorted(w["settings"]["image"]["id"] for w in left),
          "| yoast title", chk["meta"].get("_yoast_wpseo_title"))
    json.dump({"post_id": POST_ID, "featured": feat, "body": {str(k): v for k, v in new_body.items()},
               "replaced_old_media": {"featured": FEATURED_OLD, "body": sorted(BODY_OLD_TO_NEW)}},
              open(STATE_PATH, "w", encoding="utf-8"), indent=2)


if __name__ == "__main__":
    main()
