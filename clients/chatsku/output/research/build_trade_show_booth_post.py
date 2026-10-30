"""Build + push ChatSKU post: trade show booth follow-up with a catalog assistant (draft status).

Usage:
  python build_trade_show_booth_post.py            # dry run: builds Elementor JSON, prints checks
  python build_trade_show_booth_post.py publish    # uploads 3 images, creates the WP draft, sets Yoast, clears Elementor cache

Source: clients/chatsku/output/drafts/trade-show-booth-catalog-assistant-2026-10-27.md
Pattern: cloned from build_who_b2b_catalog_post.py (section per H2, heading/text/image widgets,
image AFTER text-editor, conclusion = heading + styled text + button, FAQ accordion after conclusion).
Create-only: refuses to run if its state file already exists, so the post cannot be created twice.
"""
import base64, io, json, os, re, secrets, sys, urllib.request
from PIL import Image

DRAFT = r"C:\content-intel\clients\chatsku\output\drafts\trade-show-booth-catalog-assistant-2026-10-27.md"
SCRATCH = r"C:\Users\ASUS\AppData\Local\Temp\claude\C--content-intel\9cb78ece-d8e6-4474-956c-1b343c768e5b\scratchpad\cs_img5"
ENV_PATH = r"C:\content-intel\.env"
STATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trade_show_booth_push_state.json")

WP = "https://chatsku.com/wp-json/wp/v2"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0.0.0 Safari/537.36")
SLUG = "trade-show-booth-catalog-assistant"
TITLE = "Your trade show booth closes at 5 pm. Your catalog can keep working."
YOAST_TITLE = "Trade Show Follow-Up With a Catalog Assistant | ChatSKU"
YOAST_DESC = ("Your booth closes at 5 pm, but buyers keep asking questions. See which trade show "
              "questions a catalog assistant can answer, and which ones need a person.")
CATEGORIES = [22, 24]   # B2B Commerce / Catalog Optimization. NEVER 25 (DFW Local).
DEMO_URL = "https://chatsku.com/demo/"

# Image slots: (file, alt text, placed after the body section whose title matches, or None = featured)
IMAGES = {
    "featured": (os.path.join(SCRATCH, "w12.jpg"),
                 "A trade fair exhibition hall with rows of booths and visitors walking the aisles, the floor where buyer questions begin.",
                 None),
    "body1": (os.path.join(SCRATCH, "w04.jpg"),
              "Visitors talk with staff at a trade show booth with product displays on a blue table, the in-person questions a catalog assistant can take later.",
              "Which booth questions can a catalog assistant answer on its own?"),
    "body2": (os.path.join(SCRATCH, "w22.jpg"),
              "A business professional takes notes at a laptop during a meeting, the careful research buyers do before they request a quote.",
              "How do you prepare the catalog before the show?"),
}
CAPTIONS = {
    "body1": "Photo: USDA exhibit at the 2026 World Pork Expo, Wikimedia Commons, public domain.",
    "body2": "Photo: Business professional engages in note-taking during a meeting, Wikimedia Commons, CC BY 2.0.",
}


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


def gid():
    return secrets.token_hex(4)


# ---------------------------------------------------------------- markdown -> html
def inline(s):
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)",
               lambda m: f'<a href="{m.group(2)}" target="_blank" rel="noopener noreferrer">{m.group(1)}</a>'
               if m.group(2).startswith("https://chatsku.com") is False else
               f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    s = re.sub(r"\[([^\]]+)\]\((/[^)]+)\)", r'<a href="https://chatsku.com\2">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s


def blocks(md):
    """Turn a markdown chunk into ('h3', text) | ('html', html) blocks, in order."""
    out, para, lst, lst_tag = [], [], [], None

    def flush():
        nonlocal para, lst, lst_tag
        if para:
            out.append(("html", "<p>" + inline(" ".join(para)) + "</p>"))
            para = []
        if lst:
            out.append(("html", f"<{lst_tag}>" + "".join(f"<li>{inline(i)}</li>" for i in lst) + f"</{lst_tag}>"))
            lst, lst_tag = [], None

    for line in md.splitlines():
        t = line.strip()
        if not t:
            flush(); continue
        m3 = re.match(r"###\s+(.*)", t)
        if m3:
            flush(); out.append(("h3", m3.group(1).strip())); continue
        mu = re.match(r"-\s+(.*)", t)
        mo = re.match(r"\d+\.\s+(.*)", t)
        if mu or mo:
            tag = "ul" if mu else "ol"
            if lst and lst_tag != tag:
                flush()
            if para:
                flush()
            lst_tag = tag
            lst.append((mu or mo).group(1))
            continue
        if lst:
            flush()
        para.append(t)
    flush()
    return out


def plain(html):
    return re.sub(r"<[^>]+>", "", html)


# ---------------------------------------------------------------- source parse
raw = open(DRAFT, encoding="utf-8").read()
body_md = re.sub(r"^---.*?---\s*", "", raw, count=1, flags=re.S)
body_md = body_md.split("<!-- BUILD NOTES")[0]                       # build notes never ship
body_md = re.sub(r"\n-{3,}\s*$", "", body_md.rstrip())               # trailing horizontal rule
body_md = re.sub(r"^#\s+.*\n", "", body_md, count=1, flags=re.M)     # H1 is the WP title

parts = [p for p in re.split(r"(?m)^## ", body_md) if p.strip()]
parsed = []
for p in parts:
    title, _, rest = p.partition("\n")
    title = title.strip()
    label = title.lower()
    if label == "executive summary": kind = "exec"
    elif label.startswith("introduction"): kind = "intro"
    elif label == "people also ask": kind = "paa"
    elif label.startswith("conclusion"): kind = "concl"
    elif label == "frequently asked questions": kind = "faq"
    else: kind = "body"
    parsed.append((kind, title, rest))

kinds = [k for k, _, _ in parsed]
for req in ("exec", "intro", "paa", "concl", "faq"):
    if kinds.count(req) != 1:
        sys.exit(f"BLOCKING: expected exactly one '{req}' section, got {kinds}")
if kinds.index("faq") < kinds.index("concl"):
    sys.exit("BLOCKING: FAQ must come after Conclusion")

# Conclusion: the rules forbid inline CTA links in the body text; the CTA is the button widget.
CONCL_TEXT = "Run the demo with your own catalog file to see which booth questions it can answer."
CONCL_BUTTON = ("See the live demo", DEMO_URL)


def concl_paras(bl):
    """Draft conclusion paragraphs minus any link paragraph (CTA is the button widget)."""
    paras = [h for t, h in bl if t == "html" and "<a " not in h]
    return paras + [f"<p>{CONCL_TEXT}</p>"]


# ---------------------------------------------------------------- elementor widgets
def w_heading(text, level="h2", color="#1a1a2e", align="left"):
    s = {"title": text, "align": align, "title_color": color,
         "typography_typography": "custom",
         "typography_font_size": {"size": 28 if level == "h2" else 22, "unit": "px"}}
    if level != "h2":
        s["header_size"] = level
    return {"id": gid(), "elType": "widget", "widgetType": "heading", "elements": [], "settings": s}


def w_text(html, dark=False):
    if dark:
        html = re.sub(r"<p>", '<p style="color:#aaaacc;text-align:center;font-size:18px;'
                              'max-width:720px;margin:0 auto 14px auto;">', html)
    return {"id": gid(), "elType": "widget", "widgetType": "text-editor", "elements": [],
            "settings": {"editor": html}}


def w_image(m):
    return {"id": gid(), "elType": "widget", "widgetType": "image", "elements": [],
            "settings": {"image": {"id": m["id"], "url": m["url"], "alt": m["alt"], "source": "library", "size": ""},
                         "align": "center", "width": {"size": 100, "unit": "%"},
                         "border_radius": {"top": "10", "right": "10", "bottom": "10", "left": "10", "unit": "px"}}}


def w_button(text, url):
    return {"id": gid(), "elType": "widget", "widgetType": "button", "elements": [],
            "settings": {"text": text, "link": {"url": url, "is_external": "", "nofollow": ""},
                         "align": "center", "background_color": "#e94560", "button_text_color": "#ffffff",
                         "border_radius": {"size": 6, "unit": "px"},
                         "_margin": {"unit": "px", "top": "20", "right": "0", "bottom": "0", "left": "0", "isLinked": False}}}


def w_accordion(pairs):
    tabs = [{"_id": gid(), "tab_title": q, "tab_content": a} for q, a in pairs]
    return {"id": gid(), "elType": "widget", "widgetType": "accordion", "elements": [], "settings": {"tabs": tabs}}


def section(widgets, bg, conclusion=False):
    pad = ({"top": "20", "bottom": "30", "unit": "px"} if conclusion
           else {"top": "60", "bottom": "60", "unit": "px"})
    return {"id": gid(), "elType": "section", "isInner": False,
            "settings": {"background_background": "classic", "background_color": bg, "padding": pad},
            "elements": [{"id": gid(), "elType": "column", "isInner": False,
                          "settings": {"_column_size": 100, "width": "100",
                                       "padding": {"unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20", "isLinked": True}},
                          "elements": widgets}]}


BODY_COLORS = ["#f0f4ff", "#ffffff", "#f9f9fb", "#ffffff"]
faq_pairs = []
sections = []
body_i = 0
for kind, title, md in parsed:
    bl = blocks(md)
    if kind == "exec":
        w = [w_heading(title)] + [w_text(h) for t, h in bl if t == "html"]
        sections.append(section(w, "#f9f9fb"))
    elif kind == "intro":
        w = [w_heading(title)] + [w_text(h) for t, h in bl if t == "html"]
        sections.append(section(w, "#ffffff"))
    elif kind == "body":
        w = [w_heading(title)]
        for t, v in bl:
            w.append(w_heading(v, "h3") if t == "h3" else w_text(v))
        for slot, (_, _, after) in IMAGES.items():
            if after == title:
                w.append(("IMG", slot))     # image widget appended after text, resolved below
        sections.append(section(w, BODY_COLORS[body_i % 4]))
        body_i += 1
    elif kind == "paa":
        w = [w_heading(title)]
        for t, v in bl:
            w.append(w_heading(v, "h3") if t == "h3" else w_text(v))
        sections.append(section(w, BODY_COLORS[body_i % 4]))
        body_i += 1
    elif kind == "concl":
        w = [w_heading(title, color="#ffffff", align="center"), w_text("".join(concl_paras(bl)), dark=True),
             w_button(*CONCL_BUTTON)]
        sections.append(section(w, "#1a1a2e", conclusion=True))
    elif kind == "faq":
        pairs, q, ans = [], None, []
        for t, v in bl:
            if t == "h3":
                if q: pairs.append((q, "".join(ans)))
                q, ans = v, []
            else:
                ans.append(v)
        if q: pairs.append((q, "".join(ans)))
        faq_pairs = pairs
        sections.append(section([w_heading(title), w_accordion(pairs)], "#f9f9fb"))

# every image slot must have been placed exactly once
placed = [w[1] for sec in sections for w in sec["elements"][0]["elements"] if isinstance(w, tuple)]
assert sorted(placed) == sorted(k for k in IMAGES if IMAGES[k][2] is not None), f"image placement {placed}"


def resolve(sections_, media):
    out = []
    for sec in sections_:
        col = sec["elements"][0]
        col["elements"] = [w_image(media[x[1]]) if isinstance(x, tuple) else x for x in col["elements"]]
        out.append(sec)
    return out


# WP content field: plain semantic HTML, no <img>, no Elementor markup.
content_parts = []
for kind, title, md in parsed:
    if kind == "concl":
        content_parts.append(f"<h2>{title}</h2>" + "".join(concl_paras(blocks(md))))
        continue
    content_parts.append(f"<h2>{title}</h2>")
    for t, v in blocks(md):
        content_parts.append(f"<h3>{v}</h3>" if t == "h3" else v)
CONTENT_HTML = "".join(content_parts)
assert "<img" not in CONTENT_HTML and "\u2014" not in CONTENT_HTML and "&mdash;" not in CONTENT_HTML
concl_html = CONTENT_HTML.split("<h2>Conclusion")[1].split("<h2>")[0]
assert not re.search(r'<a href="https://chatsku\.com', concl_html), "conclusion must have no inline links"


def upload_image(slot, path, alt):
    """Scale-to-cover + center crop to 860x452, JPEG q82, upload, set alt and caption."""
    im = Image.open(path).convert("RGB")
    s = max(860 / im.width, 452 / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - 860) // 2, (im.height - 452) // 2
    im = im.crop((l, t, l + 860, t + 452))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=82, optimize=True)
    data = buf.getvalue()
    assert len(data) <= 200 * 1024, f"{slot} too big: {len(data)}"
    req = urllib.request.Request(f"{WP}/media", data=data, method="POST",
                                 headers={**H, "Content-Type": "image/jpeg",
                                          "Content-Disposition": f'attachment; filename="{SLUG}-{slot}.jpg"'})
    mid = json.load(urllib.request.urlopen(req, timeout=60))
    req2 = urllib.request.Request(f"{WP}/media/{mid['id']}", method="POST",
                                  data=json.dumps({"alt_text": alt, "title": f"{SLUG} {slot}", "caption": CAPTIONS.get(slot, "")}).encode(),
                                  headers={**H, "Content-Type": "application/json"})
    mid = json.load(urllib.request.urlopen(req2, timeout=60))
    return {"id": mid["id"], "url": mid["source_url"], "alt": alt}


def post_json(url, payload, method="POST"):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), method=method,
                                 headers={**H, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=90))


def main():
    publish = len(sys.argv) > 1 and sys.argv[1].lower() == "publish"
    for slot, (path, alt, _) in IMAGES.items():
        assert 80 <= len(alt) <= 150, f"{slot} alt length {len(alt)}"
        assert os.path.exists(path), path
    assert 150 <= len(YOAST_DESC) <= 160, f"meta desc length {len(YOAST_DESC)}"
    assert len(YOAST_TITLE) <= 60, f"meta title length {len(YOAST_TITLE)}"

    if not publish:
        print("DRY RUN ok")
        print(f"sections: {kinds}")
        print(f"meta title {len(YOAST_TITLE)} chars, meta desc {len(YOAST_DESC)} chars")
        print(f"content html chars: {len(CONTENT_HTML)}; words ~{len(plain(CONTENT_HTML).split())}")
        print("Run with 'publish' to upload images and create the WordPress draft.")
        return

    if os.path.exists(STATE_PATH):
        sys.exit("BLOCKING: state file exists, post was already created. Check live state before re-running.")
    media = {slot: upload_image(slot, path, alt) for slot, (path, alt, _) in IMAGES.items()}
    print("media:", {k: v["id"] for k, v in media.items()})
    final_sections = resolve(sections, media)
    elementor = json.dumps(final_sections, ensure_ascii=False)
    payload = {
        "title": TITLE, "slug": SLUG, "status": "draft", "content": CONTENT_HTML,
        "categories": CATEGORIES, "featured_media": media["featured"]["id"],
        "meta": {"_elementor_edit_mode": "builder", "_elementor_template_type": "wp-post",
                 "_elementor_data": elementor,
                 "_yoast_wpseo_title": YOAST_TITLE, "_yoast_wpseo_metadesc": YOAST_DESC},
    }
    post = post_json(f"{WP}/posts", payload)
    pid = post["id"]
    print("created draft post", pid, post["link"])
    json.dump({"post_id": pid, "link": post["link"], "media": media},
              open(STATE_PATH, "w", encoding="utf-8"), indent=2)
    chk = json.load(urllib.request.urlopen(urllib.request.Request(
        f"{WP}/posts/{pid}?context=edit", headers=H), timeout=60))
    print("status:", chk["status"], "| featured:", chk["featured_media"],
          "| yoast title:", chk["meta"].get("_yoast_wpseo_title"),
          "| yoast desc set:", bool(chk["meta"].get("_yoast_wpseo_metadesc")),
          "| elementor data chars:", len(chk["meta"].get("_elementor_data") or ""))
    req = urllib.request.Request("https://chatsku.com/wp-json/elementor/v1/cache", headers=H, method="DELETE")
    try:
        urllib.request.urlopen(req, timeout=60); print("elementor cache cleared")
    except Exception as e:
        print("cache clear error:", e)


if __name__ == "__main__":
    main()
