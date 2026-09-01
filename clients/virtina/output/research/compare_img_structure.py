"""Compare image placement structure between reference post 42202 and new post 42297."""
import os, re, requests, urllib3
from dotenv import load_dotenv

urllib3.disable_warnings()
load_dotenv()

auth = (os.getenv("WP_USERNAME"), os.getenv("WP_APP_PASSWORD"))

def get_raw(post_id):
    r = requests.get(
        f"https://virtina.com/wp-json/wp/v2/posts/{post_id}?context=edit",
        auth=auth, verify=False
    )
    return r.json()["content"]["raw"]

ref  = get_raw(42202)  # woocommerce-b2b-customer-portal (reference)
new  = get_raw(42297)  # woocommerce-b2b-net-payment-terms (new)

def show_img_context(raw, label):
    print(f"\n{'='*60}")
    print(f"POST: {label}")
    print('='*60)
    imgs = list(re.finditer(r'<img[^>]+>', raw, re.DOTALL))
    for i, m in enumerate(imgs, 1):
        tag   = m.group()
        pos   = m.start()
        src   = re.search(r'src="([^"]+)"', tag)
        w     = re.search(r'width="([^"]+)"', tag)
        h     = re.search(r'height="([^"]+)"', tag)
        fname = src.group(1).split('/')[-1] if src else '?'

        # 300 chars before image — show the wrapper chain
        before = raw[max(0,pos-300):pos]
        # Find last opening div with background style
        last_div = None
        for dm in re.finditer(r'<div[^>]*style="[^"]*background[^"]*"[^>]*>', before):
            last_div = dm
        # Count div opens/closes between that div and image
        if last_div:
            chunk = raw[last_div.end():pos]
            opens  = len(re.findall(r'<div\b', chunk))
            closes = len(re.findall(r'</div>', chunk))
            inside = closes <= opens
            div_style = re.search(r'background:[^;]+', last_div.group())
            div_bg = div_style.group()[:40] if div_style else '?'
        else:
            inside = False
            div_bg = 'no section div above'

        # immediate parent tag of image
        parent_span = raw[max(0,pos-80):pos]

        print(f"\n  Img {i}: {fname}")
        print(f"    Size   : {w.group(1) if w else '?'} x {h.group(1) if h else '?'}")
        print(f"    Inside section box: {'YES ✓' if inside else 'NO ✗'}")
        print(f"    Nearest section bg : {div_bg}")
        print(f"    Immediate parent   : ...{parent_span[-60:]}")

show_img_context(ref, "42202 — woocommerce-b2b-customer-portal (REFERENCE)")
show_img_context(new, "42297 — woocommerce-b2b-net-payment-terms (NEW)")
