"""Fetch live rendered HTML of both posts and compare image wrapper structure."""
import re, requests, urllib3
urllib3.disable_warnings()

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def get_img_blocks(url, label):
    r = requests.get(url, headers=UA, verify=False, timeout=20)
    html = r.text
    print(f"\n{'='*60}")
    print(f"{label}")
    print(f"{'='*60}")

    imgs = list(re.finditer(r'<img[^>]+>', html, re.DOTALL))
    # Filter to body images only (skip logo/nav/social)
    body_imgs = [m for m in imgs if
                 re.search(r'width="(?:670|860|1309)"', m.group()) or
                 re.search(r'wp-content/uploads', m.group())]

    for i, m in enumerate(body_imgs, 1):
        tag = m.group()
        pos = m.start()
        src = re.search(r'src="([^"]+)"', tag)
        w   = re.search(r'width="([^"]+)"', tag)
        h   = re.search(r'height="([^"]+)"', tag)
        fname = src.group(1).split('/')[-1][:50] if src else '?'

        # 400 chars before image — look for parent container divs
        before = html[max(0, pos-400):pos]
        # Check if inside a thrv_wrapper or section div
        in_thrv = 'thrv_wrapper' in before or 'tve_image' in before
        in_section_div = bool(re.search(r'background.*(?:linear-gradient|rgba)', before[-300:]))

        # Find the immediate wrapping tags
        parent_chain = re.findall(r'<(div|span|p|figure|section)[^>]*>', before[-200:])
        parent_chain = parent_chain[-3:] if parent_chain else []

        # Check max-width on img
        has_maxwidth = 'max-width' in tag

        print(f"\n  Img {i}: {fname}")
        print(f"    Size          : {w.group(1) if w else '?'} x {h.group(1) if h else '?'}")
        print(f"    has max-width : {has_maxwidth}")
        print(f"    in thrv_wrapper: {in_thrv}")
        print(f"    in section div : {in_section_div}")
        print(f"    parent tags   : {parent_chain}")
        print(f"    before[-120:] : ...{before[-120:].replace(chr(10),' ')}")

get_img_blocks("https://virtina.com/woocommerce-b2b-customer-portal/", "42202 REFERENCE")
get_img_blocks("https://virtina.com/woocommerce-b2b-net-payment-terms/", "42297 NEW")
