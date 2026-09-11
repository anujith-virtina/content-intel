"""
Rebuild ImpelHub post 12478 as REAL Elementor data.

The first push wrote Elementor-shaped HTML but left `_elementor_data` empty, so
none of the per-widget typography applied and the post rendered with theme
defaults instead of matching previous blogs.

This script parses the existing semantic structure and emits `_elementor_data`
whose widget settings are copied EXACTLY from reference post 12433:

  container        content_width full, padding 0, margin-top 35px
  H2 heading       #0d0b1e, 26px, weight 700, line-height 1.35em
  H3 heading       #0d0b1e, 20px, weight 700, line-height 1.4em
  text-editor      16px, line-height 1.8em
  image            align center
  nested-accordion title #FD9ED0 hover/active, 20px, weight 400, lh 1.33em,
                   padding 20/0/20/0, space-between 0,
                   header border-bottom 1px #D5D8DC, icons #FD9ED0
"""
import re, io, json, base64, urllib.request, urllib.error, hashlib, sys
from bs4 import BeautifulSoup

POST_ID = 12478
REF_ID = 12433
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")


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


# ---- element id generator (Elementor uses 8-char hex-ish ids) ----
_n = [0]


def eid(seed):
    _n[0] += 1
    return hashlib.md5(f"{seed}-{_n[0]}".encode()).hexdigest()[:8]


CONTAINER_SETTINGS = {
    "content_width": "full",
    # exactly as reference 12433 stores it - no isLinked key on padding
    "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0"},
    "margin": {"unit": "px", "top": "35", "right": "0", "bottom": "0", "left": "0",
               "isLinked": False},
}

H2_SETTINGS = {
    "title_color": "#0d0b1e",
    "typography_typography": "custom",
    "typography_font_size": {"unit": "px", "size": 26},
    "typography_font_weight": "700",
    "typography_line_height": {"unit": "em", "size": 1.35},
}

H3_SETTINGS = {
    "title_color": "#0d0b1e",
    "typography_typography": "custom",
    "typography_font_size": {"unit": "px", "size": 20},
    "typography_font_weight": "700",
    "typography_line_height": {"unit": "em", "size": 1.4},
}

TEXT_SETTINGS = {
    "typography_typography": "custom",
    "typography_font_size": {"unit": "px", "size": 16},
    "typography_line_height": {"unit": "em", "size": 1.8},
}

ACCORDION_SETTINGS = {
    "title_hover_color": "#FD9ED0",
    "title_active_color": "#FD9ED0",
    "title_typography_typography": "custom",
    "title_typography_font_size": {"unit": "px", "size": 20, "sizes": []},
    "title_typography_font_weight": "400",
    "title_typography_line_height": {"unit": "em", "size": 1.33, "sizes": []},
    "icon_color": "#FD9ED0",
    "icon_hover_color": "#FD9ED0",
    "icon_active_color": "#FD9ED0",
    "padding": {"unit": "px", "top": "20", "right": "0", "bottom": "20", "left": "0",
                "isLinked": False},
    "title_space_between": {"unit": "px", "size": 0, "sizes": []},
    "header_border_border": "solid",
    "header_border_width": {"unit": "px", "top": "0", "right": "0", "bottom": "1",
                            "left": "0", "isLinked": False},
    "header_border_color": "#D5D8DC",
}


def widget(wtype, settings, extra=None):
    w = {"id": eid(wtype), "elType": "widget", "widgetType": wtype,
         "settings": dict(settings)}
    if extra:
        w["settings"].update(extra)
    return w


def container(children, settings=None):
    return {"id": eid("con"), "elType": "container",
            "settings": dict(settings or CONTAINER_SETTINGS),
            "elements": children, "isInner": False}


def heading_widget(text, level, anchor=None):
    s = H2_SETTINGS if level == "h2" else H3_SETTINGS
    extra = {"title": text, "header_size": level}
    if anchor:
        extra["_element_id"] = anchor
    return widget("heading", s, extra)


def text_widget(html):
    return widget("text-editor", TEXT_SETTINGS, {"editor": html})


def build():
    src = io.open("/tmp/c12478.html", encoding="utf-8").read()
    soup = BeautifulSoup(src, "html.parser")

    elements = []
    faq_items = []

    # Walk the existing Elementor-shaped containers in document order.
    for con in soup.select('[data-element_type="container"]'):
        # skip nested containers (accordion item panes) - handled with the accordion
        if con.find_parent(attrs={"data-element_type": "container"}):
            continue

        kids = []
        for w in con.select('[data-element_type="widget"]'):
            wt = w.get("data-widget_type", "")

            if wt.startswith("heading"):
                h = w.find(["h1", "h2", "h3", "h4"])
                if not h:
                    continue
                lvl = h.name
                anchor = w.get("id") or None
                kids.append(heading_widget(h.get_text(strip=True), lvl, anchor))

            elif wt.startswith("text-editor"):
                inner = w.decode_contents().strip()
                if inner:
                    kids.append(text_widget(inner))

            elif "accordion" in wt:
                # Rebuild the nested accordion in place, inside this container,
                # so the FAQ heading and accordion stay together as in 12433.
                items, panes = [], []
                for det in w.select("details.e-n-accordion-item"):
                    q_el = det.select_one(".e-n-accordion-item-title-text")
                    if not q_el:
                        continue
                    q = q_el.get_text(strip=True)
                    te = det.select_one('[data-widget_type^="text-editor"]')
                    body = te.decode_contents().strip() if te else ""
                    iid = eid("acc")
                    items.append({"item_title": q, "element_id": iid,
                                  "item_title_id": iid, "_id": iid})
                    panes.append({"id": eid("accpane"), "elType": "container",
                                  "settings": {"content_width": "full"},
                                  "elements": [text_widget(body)], "isInner": True})
                    faq_items.append((q, body))
                acc = widget("nested-accordion", ACCORDION_SETTINGS, {"items": items})
                acc["elements"] = panes
                kids.append(acc)

        if kids:
            elements.append(container(kids))

    return elements, faq_items


def main():
    elements, faq = build()
    data = json.dumps(elements, ensure_ascii=False, separators=(",", ":"))

    # ---- guards before any write ----
    for d in ["\u2014", "&mdash;", "&#8212;", "&#x2014;"]:
        assert data.count(d) == 0, f"em dash {d!r} leaked into _elementor_data"
    assert "<!--" not in data, "HTML comment leaked into _elementor_data"
    assert "NEWID" not in data, "NEWID placeholder leaked into _elementor_data"
    json.loads(data)  # must parse

    n_h2 = sum(1 for e in elements for w in e["elements"]
               if w.get("widgetType") == "heading" and w["settings"].get("header_size") == "h2")
    n_h3 = sum(1 for e in elements for w in e["elements"]
               if w.get("widgetType") == "heading" and w["settings"].get("header_size") == "h3")
    print(f"containers: {len(elements)}  h2: {n_h2}  h3: {n_h3}  faq items: {len(faq)}")
    print(f"_elementor_data bytes: {len(data)}")

    if "--dry" in sys.argv:
        io.open("/tmp/ed12478.json", "w", encoding="utf-8").write(
            json.dumps(elements, indent=1))
        print("dry run - wrote /tmp/ed12478.json, nothing pushed")
        return

    r = api(f"posts/{POST_ID}", {
        "meta": {
            "_elementor_edit_mode": "builder",
            "_elementor_template_type": "wp-post",
            "_elementor_data": data,
            "_elementor_version": "3.24.0",
        }}, method="POST")
    print("push status:", r.get("status"), "| id:", r.get("id"))

    # ---- verify ----
    v = api(f"posts/{POST_ID}?context=edit")
    saved = v.get("meta", {}).get("_elementor_data") or ""
    print("saved _elementor_data bytes:", len(saved))
    print("IDENTICAL to sent:", saved == data)
    print("edit_mode:", v["meta"].get("_elementor_edit_mode"),
          "| template_type:", v["meta"].get("_elementor_template_type"))
    if saved:
        parsed = json.loads(saved)
        print("parses as list:", isinstance(parsed, list), "| containers:", len(parsed))


if __name__ == "__main__":
    main()
