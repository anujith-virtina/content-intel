# -*- coding: utf-8 -*-
"""Rebuild post 37791's body in Virtina's real blog design system.

The article currently uses Thrive content-box widgets. The house style, per the
reference post 42491 (https://virtina.com/gated-catalog-ai-visibility/), is plain
inline-styled boxes inside a single Thrive WP-shortcode wrapper. See
clients/virtina/reference/BLOG-DESIGN-SYSTEM.md.

This keeps every word, heading, list, table, image and link, and only changes the
container each section sits in.

DRY RUN by default. Pass 'publish' to write.
"""
import os, sys, re, io, json, base64, urllib.request, html as _html

ROOT = r"C:\content-intel"
CUR = os.path.join(ROOT, r"clients\virtina\output\research\_37791_current.html")
OUT = os.path.join(ROOT, r"clients\virtina\output\research\_37791_restyled.html")
POST_ID = 37791
DRY = "publish" not in sys.argv

# design tokens, lifted verbatim from post 42491
GEO = "border-radius: 20px; padding: 30px; margin: 0 0 28px 0;"
BG_SUMMARY = "linear-gradient(rgba(0,213,192,0.28),rgba(0,213,192,0.28))"
BG_BODY = "linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13))"
BG_NEUTRAL = "linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5))"
BG_CONCLUSION = "#00d5c0"
H2 = 'style="color: #43627f; font-size: 30px;"'
H2_WHITE = 'style="color: #ffffff; font-size: 30px;"'
H3 = 'style="color: #43627f; font-size: 22px;"'
P = 'dir="ltr" style="font-size: 16px; line-height: 1.75;"'
P_WHITE = 'style="color: #ffffff; font-size: 16px; line-height: 1.75;"'

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def headers():
    e = {}
    for ln in io.open(os.path.join(ROOT, ".env"), encoding="utf-8"):
        ln = ln.strip()
        if ln and "=" in ln and not ln.startswith("#"):
            k, v = ln.split("=", 1)
            e[k.strip()] = v.strip()
    tok = base64.b64encode(f"{e['WP_USERNAME']}:{e['WP_APP_PASSWORD']}".encode()).decode()
    return {"User-Agent": UA, "Content-Type": "application/json",
            "Authorization": "Basic " + tok}


def slugify(t):
    s = re.sub(r'[^a-z0-9\s-]', '', t.lower()).strip()
    return re.sub(r'\s+', '-', s)[:48] or "section"


def clean(fragment):
    """Keep the content, drop every Thrive wrapper and token."""
    f = fragment
    f = re.sub(r'(?is)<div[^>]*class="[^"]*tve-content-box-background[^"]*"[^>]*>.*?</div>', '', f)
    f = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', '', f)
    f = re.sub(r'(?is)</?div[^>]*>', '', f)          # all Thrive divs go
    f = re.sub(r'(?is)</?span[^>]*>', '', f)          # spans carried Thrive styling
    f = re.sub(r'\sdata-css="[^"]*"', '', f)
    f = re.sub(r'\sdata-[a-z-]+="[^"]*"', '', f)
    f = re.sub(r'\sclass="[^"]*"', '', f)
    # normalise the tags we keep
    f = re.sub(r'<p[^>]*>', f'<p {P}>', f)
    f = re.sub(r'<h3[^>]*>', f'<h3 {H3}>', f)
    f = re.sub(r'<h4[^>]*>', f'<h4 {H3}>', f)
    f = re.sub(r'<a ', '<a style="color: #00a0e2; outline: none;" ', f)
    f = re.sub(r'\s+', ' ', f)
    f = re.sub(r'<p [^>]*>\s*</p>', '', f)
    return f.strip()


def build():
    src = io.open(CUR, encoding="utf-8").read()
    # split on top-level H2s
    marks = [(m.start(), m.end(),
              re.sub(r'\s+', ' ', _html.unescape(re.sub('<[^>]+>', '', m.group(1)))).strip())
             for m in re.finditer(r'<h2[^>]*>(.*?)</h2>', src, re.S | re.I)]
    if not marks:
        raise SystemExit("BLOCKING: no H2s found")
    sections = []
    for i, (a, b, title) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(src)
        body = clean(src[b:end])
        sections.append((title, body))
    print(f"  sections parsed: {len(sections)}")

    out = []
    body_i = 0
    for title, body in sections:
        low = title.lower()
        anchor = slugify(title)
        if low.startswith("summary"):
            bg, h, p = BG_SUMMARY, H2, None
        elif low.startswith("conclusion"):
            bg, h, p = BG_CONCLUSION, H2_WHITE, P_WHITE
        else:
            bg = BG_BODY if body_i % 2 == 0 else BG_NEUTRAL
            h, p = H2, None
            body_i += 1
        if p:                                    # conclusion: white text
            body = re.sub(r'<p [^>]*>', f'<p {p}>', body)
            body = re.sub(r'<h3 [^>]*>', '<h3 style="color:#ffffff; font-size: 22px;">', body)
        out.append(f'<div style="background: {bg}; {GEO}">'
                   f'<h2 id="{anchor}" {h}>{_html.escape(title, quote=False)}</h2>'
                   f'{body}</div>')
    article = "".join(out)

    # wrap exactly the way post 42491 does
    wrapped = ('<div class="thrv_wrapper tve_wp_shortcode">'
               '<div class="tve_shortcode_raw" style="display: none">___TVE_SHORTCODE_RAW__'
               + _html.escape(article, quote=True) +
               '</div>' + article + '</div>')

    # guards
    def words(x):
        return len(re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', _html.unescape(x))).split())
    w_before, w_after = words(src), words(article)
    print(f"  words: {w_before} -> {w_after} (content must not be lost)")
    if w_after < w_before * 0.85:
        raise SystemExit(f"BLOCKING: lost {w_before - w_after} words, refusing")
    if 'thrv_contentbox_shortcode' in article:
        raise SystemExit("BLOCKING: a Thrive content box survived into the new body")
    if 'data-css' in article:
        raise SystemExit("BLOCKING: a Thrive token survived into the new body")
    boxes = len(re.findall(r'border-radius: 20px; padding: 30px', article))
    print(f"  design boxes built: {boxes}")
    print(f"  images kept: {len(re.findall(r'<img', article))} | "
          f"tables kept: {len(re.findall(r'<table', article))} | "
          f"links kept: {len(re.findall(r'<a ', article))}")
    io.open(OUT, "w", encoding="utf-8").write(wrapped)
    return wrapped


def main():
    wrapped = build()
    if DRY:
        print("\nDRY RUN. Nothing pushed. Preview:", OUT)
        return
    H = headers()
    r = urllib.request.urlopen(urllib.request.Request(
        f"https://virtina.com/wp-json/tcb/v1/posts/{POST_ID}/content",
        data=json.dumps({"tve_content": wrapped}).encode("utf-8"),
        headers=H, method="POST"), timeout=300)
    print("THRIVE push:", r.status)
    urllib.request.urlopen(urllib.request.Request(
        f"https://virtina.com/wp-json/wp/v2/posts/{POST_ID}",
        data=json.dumps({"content": wrapped}).encode("utf-8"),
        headers=H, method="POST"), timeout=300)
    back = json.load(urllib.request.urlopen(urllib.request.Request(
        f"https://virtina.com/wp-json/wp/v2/posts/{POST_ID}?context=edit",
        headers=H), timeout=300))
    live = back["meta"]["tve_updated_post"]
    print("  stored length:", len(live), "| expected:", len(wrapped))
    print("  design boxes stored:", len(re.findall(r'border-radius: 20px; padding: 30px', live)))
    print("  status:", back["status"])


if __name__ == "__main__":
    main()
