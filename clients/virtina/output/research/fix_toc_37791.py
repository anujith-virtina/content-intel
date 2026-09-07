# -*- coding: utf-8 -*-
"""Rebuild post 37791's Table of Contents to match the refreshed structure.

The refresh reordered, cut and added sections but left the TOC untouched, so it
still listed Apple, Shopify and DoorDash, whose sections no longer exist, and
omitted Temu, Coupang, Ozon and every new section. Every <li> is cloned from the
page's own existing item so the icon markup and data-css tokens stay intact.

DRY RUN by default. Pass 'publish' to write.
"""
import os, sys, re, io, json, base64, hashlib, urllib.request

ROOT = r"C:\content-intel"
SRC = os.path.join(ROOT, r"clients\virtina\output\drafts\best-ecommerce-websites-FINAL-37791-2026-09-07.html")
POST_ID = 37791
DRY = "publish" not in sys.argv

# (anchor id, label) in the order the page now reads
TOC = [
    ("methodology",   "How this ranking is measured"),
    ("top-10",        "Top 10 online shopping sites in the world"),
    ("amazon",        "1. Amazon"),
    ("temu",          "2. Temu"),
    ("aliexpress",    "3. AliExpress"),
    ("walmart",       "4. Walmart"),
    ("ebay",          "5. eBay"),
    ("etsy",          "6. Etsy"),
    ("rakuten",       "7. Rakuten"),
    ("shein",         "8. Shein"),
    ("coupang",       "9. Coupang"),
    ("ozon",          "10. Ozon"),
    ("app-traffic",   "Why the biggest sellers are missing from this list"),
    ("financials",    "The same companies by disclosed revenue instead"),
    ("regional",      "Regional and category leaders worth knowing"),
    ("what-it-means", "What this means for your store"),
    ("paa",           "People also ask"),
    ("conclusion",    "Conclusion"),
    ("faq",           "Frequently asked questions"),
]

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


def main():
    s = io.open(SRC, encoding="utf-8").read()

    items = re.findall(r'<li class="thrv-styled-list-item.*?</li>', s, re.S)
    if len(items) < 5:
        raise SystemExit(f"BLOCKING: expected the TOC list, found {len(items)} items")
    template = items[0]
    first_at = s.find(items[0])
    last_at = s.find(items[-1]) + len(items[-1])
    print(f"existing TOC: {len(items)} items, spans {first_at}..{last_at}")

    def build(anchor, label):
        li = re.sub(r'<a href="#[^"]*"([^>]*)>.*?</a>',
                    lambda m: f'<a href="#{anchor}"{m.group(1)}>{label} </a>',
                    template, count=1, flags=re.S)
        return li

    new_list = "".join(build(a, l) for a, l in TOC)
    out = s[:first_at] + new_list + s[last_at:]

    # guards
    if len(re.findall(r'<div\b', out)) != len(re.findall(r'</div\s*>', out)):
        raise SystemExit("BLOCKING: div imbalance after TOC rebuild")
    src_css = set(re.findall(r'data-css="([^"]+)"', s))
    if set(re.findall(r'data-css="([^"]+)"', out)) - src_css:
        raise SystemExit("BLOCKING: invented data-css token")
    for dead in ("#apple", "#shopify", "#doorDash", "#overstock"):
        if f'href="{dead}"' in out:
            raise SystemExit(f"BLOCKING: TOC still links removed section {dead}")
    for a, _ in TOC:
        if f'id="{a}"' not in out:
            raise SystemExit(f"BLOCKING: TOC links #{a} but no such section id")
    print(f"  rebuilt TOC: {len(TOC)} items, all anchors resolve to real sections")
    print(f"  {len(s)} -> {len(out)} chars")

    io.open(SRC, "w", encoding="utf-8").write(out)
    print("  finished file updated")

    if DRY:
        print("\nDRY RUN. Nothing pushed.")
        return

    H = headers()
    tcb = urllib.request.urlopen(urllib.request.Request(
        f"https://virtina.com/wp-json/tcb/v1/posts/{POST_ID}/content",
        data=json.dumps({"tve_content": out}).encode("utf-8"),
        headers=H, method="POST"), timeout=300)
    print("THRIVE push:", tcb.status)
    urllib.request.urlopen(urllib.request.Request(
        f"https://virtina.com/wp-json/wp/v2/posts/{POST_ID}",
        data=json.dumps({"content": out}).encode("utf-8"),
        headers=H, method="POST"), timeout=300)

    back = json.load(urllib.request.urlopen(urllib.request.Request(
        f"https://virtina.com/wp-json/wp/v2/posts/{POST_ID}?context=edit",
        headers=H), timeout=300))
    live = back["meta"]["tve_updated_post"]
    print("  sha match:", hashlib.sha256(live.encode()).hexdigest() ==
          hashlib.sha256(out.encode()).hexdigest())
    print("  status   :", back["status"])


if __name__ == "__main__":
    main()
