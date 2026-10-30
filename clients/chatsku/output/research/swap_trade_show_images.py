"""Swap the three images on draft post 3846 for AI-generated crops and drop the stock credit lines.

Usage:
  python swap_trade_show_images.py           # dry run: uploads nothing, prints what would change
  python swap_trade_show_images.py apply     # uploads 3 images, updates post 3846 in place, clears Elementor cache

Only touches: featured_media, the three image widgets, and the three credit paragraphs.
Never touches title, status, Yoast fields, categories, or any other widget. Never re-pushes the whole post.
"""
import base64, io, json, os, re, secrets, sys, urllib.request
from PIL import Image

ENV_PATH = r"C:\content-intel\.env"
SCRATCH = r"C:\Users\ASUS\AppData\Local\Temp\claude\C--content-intel\9cb78ece-d8e6-4474-956c-1b343c768e5b\scratchpad\cs_trade"
STATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trade_show_booth_images_v2_state.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0.0.0 Safari/537.36")
WP = "https://chatsku.com/wp-json/wp/v2"
POST_ID = 3846
SLUG = "trade-show-booth-catalog-assistant"

# old media id -> (new file, new alt text). Old ids stay in the library; nothing is deleted.
OLD_TO_NEW = {
    3843: ("featured.jpg",
           "A trade fair exhibition hall where two buyers and a sales rep review a product part at a booth, the floor where buyer questions begin."),
    3844: ("body2.jpg",
           "A product page open on a tablet beside stacked spec sheets in a warehouse office, the product detail a buyer checks before asking for a quote."),
    3845: ("body1.jpg",
           "A manager at a desk at dusk reviewing a printed catalog beside a laptop with a product spreadsheet and handwritten notes."),
}
FEATURED_OLD = 3843
CREDIT_PREFIXES = ("Featured photo:", "Booth photo:", "Laptop photo:")


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
    """Remove whole <p> blocks that begin with a stock credit prefix. Returns (new_html, removed_count)."""
    removed = 0
    def repl(m):
        nonlocal removed
        text = re.sub(r"<[^>]+>", "", m.group(0)).strip()
        if text.startswith(CREDIT_PREFIXES):
            removed += 1
            return ""
        return m.group(0)
    new = re.sub(r"<p[^>]*>.*?</p>", repl, html, flags=re.S)
    return new, removed


def walk_images(node, found):
    if isinstance(node, dict):
        if node.get("widgetType") == "image":
            found.append(node)
        for v in node.values():
            walk_images(v, found)
    elif isinstance(node, list):
        for x in node:
            walk_images(x, found)


def walk_texts(node, out):
    if isinstance(node, dict):
        if node.get("widgetType") == "text-editor":
            out.append(node["settings"])
        for v in node.values():
            walk_texts(v, out)
    elif isinstance(node, list):
        for x in node:
            walk_texts(x, out)


def main():
    apply = len(sys.argv) > 1 and sys.argv[1].lower() == "apply"
    if apply and os.path.exists(STATE_PATH):
        sys.exit("BLOCKING: v2 state file exists; images were already swapped. Check live state.")

    live = get_json(f"{WP}/posts/{POST_ID}?context=edit")
    # Post was published by the user after the draft push (modified stamp unchanged since 2026-10-27 10:52).
    assert live["status"] in ("draft", "publish"), f"unexpected status {live['status']}"
    assert live["modified"] == "2026-10-27T10:52:05", f"post changed since last check: {live['modified']}"
    print("live status:", live["status"], "| featured:", live["featured_media"])

    data = json.loads(live["meta"]["_elementor_data"])
    imgs = []
    walk_images(data, imgs)
    print("image widgets found:", len(imgs))
    for w in imgs:
        print("  old id", w["settings"]["image"]["id"], "->", w["settings"]["image"]["url"][-40:])
    old_ids = sorted(w["settings"]["image"]["id"] for w in imgs)
    # Featured image lives in featured_media, so the Elementor widgets are the two body images only.
    assert old_ids == [3844, 3845], f"unexpected image ids {old_ids}"
    assert live["featured_media"] == FEATURED_OLD

    texts = []
    walk_texts(data, texts)
    hits = 0
    for s in texts:
        new_editor, n = strip_credit_paragraphs(s.get("editor", ""))
        hits += n
    new_content, n_content = strip_credit_paragraphs(live["content"]["raw"])
    print("credit paragraphs in elementor:", hits, "| in post content:", n_content)
    assert hits >= 3 and n_content >= 3, "expected the three credit paragraphs in both places"

    if not apply:
        print("DRY RUN ok. Run 'apply' to upload and update post 3846.")
        return

    new_media = {}
    for old, (fname, alt) in OLD_TO_NEW.items():
        slot = {3843: "featured", 3844: "body1", 3845: "body2"}[old]
        new_media[old] = upload(os.path.join(SCRATCH, fname), alt, slot)
        print("uploaded", slot, "->", new_media[old]["id"])

    for w in imgs:
        old = w["settings"]["image"]["id"]
        nm = new_media[old]
        w["settings"]["image"] = {"id": nm["id"], "url": nm["url"], "alt": nm["alt"], "source": "library", "size": ""}

    for s in texts:
        s["editor"], _ = strip_credit_paragraphs(s.get("editor", ""))

    content, _ = strip_credit_paragraphs(live["content"]["raw"])
    payload = {
        "content": content,
        "featured_media": new_media[FEATURED_OLD]["id"],
        "meta": {"_elementor_data": json.dumps(data, ensure_ascii=False)},
    }
    req = urllib.request.Request(f"{WP}/posts/{POST_ID}", data=json.dumps(payload).encode(), method="POST",
                                 headers={**H, "Content-Type": "application/json"})
    upd = json.load(urllib.request.urlopen(req, timeout=120))
    print("updated post", upd["id"], "status", upd["status"])

    try:
        req = urllib.request.Request(f"https://chatsku.com/wp-json/elementor/v1/cache", method="DELETE", headers=H)
        urllib.request.urlopen(req, timeout=60)
        print("elementor cache cleared")
    except Exception as e:
        print("elementor cache clear failed:", e)

    chk = get_json(f"{WP}/posts/{POST_ID}?context=edit")
    left = []
    walk_images(json.loads(chk["meta"]["_elementor_data"]), left)
    print("verify: status", chk["status"], "| featured", chk["featured_media"],
          "| widget ids", sorted(w["settings"]["image"]["id"] for w in left),
          "| yoast title", chk["meta"].get("_yoast_wpseo_title"))
    json.dump({"post_id": POST_ID, "featured": new_media[FEATURED_OLD],
               "body1": new_media[3844], "body2": new_media[3845],
               "replaced_old_media": {str(k): v for k, v in OLD_TO_NEW.items()}},
              open(STATE_PATH, "w", encoding="utf-8"), indent=2)


if __name__ == "__main__":
    main()
