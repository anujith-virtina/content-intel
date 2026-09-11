"""
Fix post 12478 to match the LIVE ImpelHub blog design, as seen on post 12433.

Four divergences found by actually looking at the rendered reference post
instead of only reading computed style numbers:

1. H2 headings were missing `_css_classes: "blog-title-h2"`. That class is what
   draws the signature purple bar under every H2:
       .blog-title-h2 h2::before { position:absolute; bottom:0; left:0;
                                   width:76px; height:3px; background:#5736fd; }
   Without the class there is no bar, which is a large part of why the post
   looked wrong.

2. Anchors were written as `_element_id`. The reference uses `css_id`.
   Wrong key means the TOC links do not resolve.

3. The TOC was built as an H3 plus arrow paragraphs. The live design is a single
   text-editor holding a lavender box with a numbered <ol>.

4. Unicode arrows. Reference post 12433 contains ZERO of them and uses <ol>,
   never <ul>. `MUST-FOLLOW-RULES.md` is wrong on this point.
"""
import re, io, json, base64, urllib.request, hashlib

POST_ID = 12478
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
ARROW = "\u2192"

TOC_BOX_OPEN = ('<div style="background:#FBE9FF;border-radius:8px;padding:18px 24px;">'
                '<div style="font-weight:700;color:#0d0b1e;font-size:18px;'
                'margin-bottom:8px;">Table of Contents</div>'
                '<ol style="margin:0;padding-left:20px;color:#0d0b1e;'
                'font-size:16px;line-height:1.8;">')
TOC_BOX_CLOSE = "</ol></div>"


def creds():
    env = dict(re.findall(r'^([A-Z_]+)=(.*)$',
                          io.open("C:/content-intel/.env", encoding="utf-8").read(), re.M))
    return env["IMPELHUB_WP_USERNAME"], env["IMPELHUB_WP_APP_PASSWORD"]


def api(path, data=None, method="GET"):
    u, p = creds()
    tok = base64.b64encode(f"{u}:{p}".encode()).decode()
    body = json.dumps(data, ensure_ascii=False).encode("utf-8") if data else None
    req = urllib.request.Request(
        f"https://impelhub.com/wp-json/wp/v2/{path}", data=body, method=method,
        headers={"Authorization": f"Basic {tok}", "User-Agent": UA,
                 "Content-Type": "application/json; charset=utf-8"})
    return json.load(urllib.request.urlopen(req, timeout=120))


def strip_arrows(html):
    """Remove the arrow span prefix, leaving clean paragraphs like the reference."""
    html = re.sub(r'<span style="color:#5736fd;">\s*' + ARROW + r'\s*</span>\s*', "", html)
    return html.replace(ARROW, "").replace("  ", " ")


def main():
    tree = json.loads(api(f"posts/{POST_ID}?context=edit")["meta"]["_elementor_data"])

    toc_links = []          # (anchor, title) harvested from the old TOC
    stats = {"h2_class": 0, "css_id": 0, "arrows_removed": 0, "toc_rebuilt": 0}

    # ---- pass 1: fix headings, harvest TOC targets ----
    def fix(node):
        s = node.get("settings", {})
        if node.get("widgetType") == "heading":
            if s.get("header_size") == "h2":
                s["_css_classes"] = "blog-title-h2"
                stats["h2_class"] += 1
            if "_element_id" in s:                     # wrong key -> css_id
                s["css_id"] = s.pop("_element_id")
                stats["css_id"] += 1
        for c in node.get("elements", []) or []:
            fix(c)
    for n in tree:
        fix(n)

    # ---- pass 2: locate and rebuild the TOC, strip arrows everywhere ----
    def find_toc(container):
        """Return index of the TOC heading widget inside a container, or None."""
        for i, w in enumerate(container.get("elements", []) or []):
            if (w.get("widgetType") == "heading"
                    and "table of contents" in str(w["settings"].get("title", "")).lower()):
                return i
        return None

    for con in tree:
        i = find_toc(con)
        if i is None:
            continue
        kids = con["elements"]
        # the text-editor right after the heading holds the arrow links
        body = kids[i + 1] if i + 1 < len(kids) else None
        if body and body.get("widgetType") == "text-editor":
            for m in re.finditer(r'<a href="(#[^"]+)"[^>]*>(.*?)</a>',
                                 body["settings"]["editor"], flags=re.S):
                toc_links.append((m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip()))
            items = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in toc_links)
            body["settings"]["editor"] = TOC_BOX_OPEN + items + TOC_BOX_CLOSE
            del kids[i]                                 # drop the standalone H3
            stats["toc_rebuilt"] = len(toc_links)
        break

    def de_arrow(node):
        s = node.get("settings", {})
        e = s.get("editor")
        if e and ARROW in e:
            stats["arrows_removed"] += e.count(ARROW)
            s["editor"] = strip_arrows(e)
        for c in node.get("elements", []) or []:
            de_arrow(c)
    for n in tree:
        de_arrow(n)

    data = json.dumps(tree, ensure_ascii=False, separators=(",", ":"))

    # ---- guards ----
    assert ARROW not in data, "arrows still present"
    for d in ["\u2014", "&mdash;", "&#8212;", "&#x2014;"]:
        assert data.count(d) == 0, f"em dash {d!r} present"
    assert "<!--" not in data and "NEWID" not in data
    json.loads(data)

    print("fixes:", stats)

    api(f"posts/{POST_ID}", {"meta": {
        "_elementor_edit_mode": "builder",
        "_elementor_template_type": "wp-post",
        "_elementor_data": data}}, method="POST")

    # ---- verify ----
    saved = api(f"posts/{POST_ID}?context=edit")["meta"]["_elementor_data"]
    print("saved identical:", saved == data)
    t = json.loads(saved)
    n_cls = json.dumps(t).count("blog-title-h2")
    n_cssid = json.dumps(t).count('"css_id"')
    print(f"blog-title-h2 on {n_cls} headings | css_id anchors: {n_cssid}"
          f" | arrows: {json.dumps(t, ensure_ascii=False).count(ARROW)}"
          f" | TOC box: {'FBE9FF' in json.dumps(t)}")


if __name__ == "__main__":
    main()
