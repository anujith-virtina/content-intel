"""
Fetch live HTML of both posts.
For each body image, show what div/section wrapper contains it on the RENDERED page.
"""
import re, requests, urllib3
urllib3.disable_warnings()

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def analyse(url, label):
    html = requests.get(url, headers=UA, verify=False, timeout=20).text
    print(f"\n{'='*65}")
    print(f"{label}")
    print(f"{'='*65}")

    # Find all section-style divs (background colored boxes)
    section_divs = list(re.finditer(
        r'<div[^>]*style="[^"]*(?:linear-gradient|background:#00d5c0)[^"]*"[^>]*>',
        html
    ))
    print(f"  Colored section boxes found: {len(section_divs)}")

    # Find body images (wp-content uploads, skip logo/avatar/sidebar)
    imgs = list(re.finditer(
        r'<img[^>]*wp-content/uploads/202[0-9][^>]*(?:width="(?:670|860|1309)")[^>]*>',
        html, re.DOTALL
    ))
    print(f"  Body images found: {len(imgs)}\n")

    for i, m in enumerate(imgs, 1):
        tag = m.group()
        pos = m.start()
        src = re.search(r'(?:src|data-lazy-src)="([^"]+)"', tag)
        w   = re.search(r'width="([^"]+)"', tag)
        h   = re.search(r'height="([^"]+)"', tag)
        fname = src.group(1).split('/')[-1][:55] if src else '?'

        # Find the nearest section div before this image
        divs_before = [d for d in section_divs if d.start() < pos]
        if divs_before:
            last_div = divs_before[-1]
            chunk = html[last_div.end():pos]
            opens  = len(re.findall(r'<div\b', chunk))
            closes = len(re.findall(r'</div>', chunk))
            inside = closes <= opens
            bg = re.search(r'background:[^;}"]+', last_div.group())
            bg_val = bg.group()[:50] if bg else '?'
        else:
            inside = False
            bg_val = 'no section box above'

        # Show 200 chars of context before the <figure>/<p>/<span> wrapping the image
        ctx_start = max(0, pos - 250)
        ctx = html[ctx_start:pos].replace('\n', ' ').strip()[-200:]

        print(f"  Img {i}: {fname}")
        print(f"    {w.group(1) if w else '?'} x {h.group(1) if h else '?'}")
        print(f"    Inside section box : {'YES ✓' if inside else 'NO — floating in white space'}")
        print(f"    Section bg         : {bg_val}")
        print(f"    Context before     : ...{ctx}")
        print()

analyse("https://virtina.com/woocommerce-b2b-customer-portal/",    "42202 REFERENCE — customer portal")
analyse("https://virtina.com/woocommerce-b2b-net-payment-terms/",  "42297 NEW — net payment terms")
