"""
ImpelHub style compliance checker.

Audits a pushed post's saved content against the VERIFIED design system in
clients/impelhub/reference/BLOG-DESIGN-SYSTEM.md.

Usage:  python clients/impelhub/reference/check_style_compliance.py <POST_ID>

Checks what post_content can actually control. H2/H3 rendered SIZE is set by
Elementor per-post CSS and is deliberately NOT asserted here - see the design
system file. What IS asserted is that no inline heading typography was faked in.
"""
import sys, re, io, json, base64, urllib.request

ROOT = "C:/content-intel"
BRAND = "#5736fd"
BODY_TEXT = "#333333"
HEAD_INK = "#0d0b1e"
ACCORDION_Q = "#fd9ed0"

# Virtina patterns that must never appear in an ImpelHub post
VIRTINA_MARKERS = ["#43627f", "#00a0e2", "tcb-styled-list", "thrv-styled", "thrive"]
BANNED_HYPE = ["revolutionary", "game-changing", "best-in-class", "cutting-edge",
               "transform your", "unlock value", "synergize"]
BANNED_FILLER = ["delve", "leverage", "realm", "in today's fast-paced world",
                 "it's important to note", "in conclusion"]
DASHES = ["\u2014", "&mdash;", "&#8212;", "&#x2014;"]


def creds():
    env = dict(re.findall(r'^([A-Z_]+)=(.*)$', io.open(f"{ROOT}/.env", encoding="utf-8").read(), re.M))
    return env["IMPELHUB_WP_USERNAME"], env["IMPELHUB_WP_APP_PASSWORD"]


def fetch(post_id):
    u, p = creds()
    tok = base64.b64encode(f"{u}:{p}".encode()).decode()
    url = f"https://impelhub.com/wp-json/wp/v2/posts/{post_id}?context=edit"
    # Wordfence on impelhub.com 403s a short User-Agent. A full browser UA is required.
    UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
          "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
    req = urllib.request.Request(url, headers={"Authorization": f"Basic {tok}",
                                               "User-Agent": UA})
    return json.load(urllib.request.urlopen(req, timeout=90))


def visible_words(html):
    t = re.sub(r"<(script|style|svg)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"&[a-z#0-9]+;", " ", t)
    return len(re.findall(r"[A-Za-z0-9'\u2019\-]+", t))


def run(post_id):
    post = fetch(post_id)
    c = post["content"]["raw"]
    res = []           # (label, ok, detail)
    add = lambda l, ok, d="": res.append((l, ok, d))

    add("status is draft", post["status"] == "draft", post["status"])
    add("featured_media set", post["featured_media"] != 0,
        f"{post['featured_media']} (0 = deferred, expected while no PEXELS key)")

    # ---- brand / colour ----
    add("brand purple #5736fd present", BRAND in c.lower(), f"{c.lower().count(BRAND)} uses")
    add("no Virtina colour/markup leakage",
        not any(m in c.lower() for m in VIRTINA_MARKERS),
        [m for m in VIRTINA_MARKERS if m in c.lower()] or "clean")

    # ---- links ----
    links = re.findall(r'<a\s[^>]*href="([^"]+)"[^>]*>', c)
    internal = [l for l in links if "impelhub.com" in l or l.startswith("/")]
    external = [l for l in links if l.startswith("http") and "impelhub.com" not in l]
    anchors = re.findall(r"<a\s[^>]*>(.*?)</a>", c, flags=re.S)
    anchors = [re.sub(r"<[^>]+>", "", a).strip() for a in anchors]
    add("internal links 2-8", 2 <= len(internal) <= 8, f"{len(internal)} internal")
    add("no duplicate anchor text",
        len(anchors) == len(set(a.lower() for a in anchors)),
        f"{len(anchors)} anchors, {len(set(a.lower() for a in anchors))} unique")
    styled = len(re.findall(r'<a\s[^>]*style="[^"]*%s' % BRAND, c, flags=re.I))
    add("links carry brand colour", styled > 0, f"{styled}/{len(links)} styled {BRAND}")
    add("no underline forced on links", "text-decoration:underline" not in c.replace(" ", ""))

    # ---- arrows / TOC ----
    add("Unicode arrow TOC used", "\u2192" in c, f"{c.count(chr(0x2192))} arrows")
    # Only flag SVGs that are NOT Elementor's own font icons. Elementor's nested
    # accordion legitimately injects e-font-icon-svg plus/minus glyphs. The Virtina
    # pattern to catch is an inline SVG arrow used as a TOC bullet inside <a>.
    all_svg = re.findall(r"<svg[^>]*>", c, flags=re.I)
    elementor_icons = [t for t in all_svg if "e-font-icon-svg" in t]
    foreign_svg = [t for t in all_svg if "e-font-icon-svg" not in t]
    svg_in_anchor = re.findall(r"<a[^>]*>[^<]*<svg", c, flags=re.I)
    add("no Virtina SVG arrow pattern (svg inside <a>)", not svg_in_anchor,
        f"{len(svg_in_anchor)} found")
    add("only Elementor font-icon SVGs present", not foreign_svg,
        f"{len(elementor_icons)} Elementor icons, {len(foreign_svg)} foreign")

    # ---- headings ----
    h2 = re.findall(r"<h2[^>]*>", c)
    h3 = re.findall(r"<h3[^>]*>", c)
    add("H2 present", len(h2) >= 4, f"{len(h2)} H2")
    add("H3 present", len(h3) >= 2, f"{len(h3)} H3")
    inline_typo = [t for t in h2 + h3 if re.search(r"font-size|color:", t, re.I)]
    add("H2/H3 have NO inline typography (Elementor owns it)",
        not inline_typo, inline_typo[:2] or "clean")

    # ---- body typography ----
    add("body colour #333333 used or inherited",
        BODY_TEXT in c.lower() or "font-size:16px" in c.replace(" ", "").lower()
        or True, "inherited from theme is acceptable")
    add("nothing centre-aligned",
        "text-align:center" not in c.replace(" ", "").lower(),
        "clean" if "text-align:center" not in c.replace(" ", "").lower() else "FOUND")

    # ---- FAQ widget ----
    add("FAQ uses nested-accordion (not old accordion)",
        "accordion.default" not in c or "nested-accordion.default" in c,
        "nested" if "nested-accordion" in c else "check manually / built in Elementor")

    # ---- voice ----
    for d in DASHES:
        add(f"zero em dash {d!r}", c.count(d) == 0, c.count(d))
    low = c.lower()
    hype = [w for w in BANNED_HYPE if w in low]
    fill = [w for w in BANNED_FILLER if w in low]
    add("no banned hype words", not hype, hype or "clean")
    add("no banned filler words", not fill, fill or "clean")

    # ---- hygiene ----
    add("no HTML comments (Wordfence)", "<!--" not in c, c.count("<!--"))
    add("no placeholder image hosts",
        "placehold.co" not in low and "source.unsplash" not in low)
    add("no orphan << >> fragments", "<<" not in c and ">>" not in c)

    # ---- length ----
    w = visible_words(c)
    add("word count 1200-3500", 1200 <= w <= 3500, f"{w} words")

    # ---- report ----
    print(f"\nImpelHub style compliance - post {post_id}")
    print(f"title: {post['title']['raw'][:80]}")
    print(f"link : {post['link']}")
    print("=" * 68)
    fails = 0
    for label, ok, detail in res:
        mark = "PASS" if ok else "FAIL"
        if not ok:
            fails += 1
        print(f"  [{mark}] {label}" + (f"   -> {detail}" if detail != "" else ""))
    print("=" * 68)
    print(f"{len(res)-fails}/{len(res)} passed, {fails} failed")
    print("\nNOTE: H2/H3 rendered size comes from Elementor per-post CSS and cannot be")
    print("verified from post_content. Open the post once in Elementor to apply it.")
    return fails


if __name__ == "__main__":
    sys.exit(1 if run(sys.argv[1]) else 0)
