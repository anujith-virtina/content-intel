# -*- coding: utf-8 -*-
"""Build Virtina carousel slides from ChatGPT scenes: full-bleed scene, dark bottom gradient,
yellow headline, white body, footer strip with www.virtina.com and the logo, page counter,
numbered badge on point slides. Also writes the LinkedIn document PDF.

usage: python social/build_chatgpt_slides.py <pack.json> <scene1> <scene2> ... (one scene PNG per slide, in order)
Output: clients/virtina/output/social/slides/<pack name>/chatgpt/slide-0N.jpg + <slug>-chatgpt.pdf + contact-sheet.jpg
"""
import os, sys, json
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
FONTS = os.path.join(HERE, 'fonts')
W = 1080
WHITE = (255, 255, 255)
BRANDS = {
    'virtina': {'accent': (255, 230, 0), 'badge': (21, 101, 230), 'badge_outline': WHITE, 'footer': (8, 18, 80),
                'site': 'www.virtina.com', 'logo': 'virtina-logo.webp', 'recolor_logo': True},
    'chatsku': {'accent': (245, 193, 46), 'badge': (13, 37, 80), 'badge_outline': (78, 221, 204), 'footer': None,
                'site': 'www.chatsku.com', 'logo': 'chatsku-logo.png', 'recolor_logo': False},
}


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def wrap(d, text, fnt, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(d, text, name, sizes, maxw, maxlines):
    for s in sizes:
        f = font(name, s)
        lines = wrap(d, text, f, maxw)
        if len(lines) <= maxlines:
            return f, lines
    raise SystemExit('text does not fit: %r' % text)


def white_logo(width, brand):
    logo = Image.open(os.path.join(HERE, 'brand', brand['logo'])).convert('RGBA')
    if brand['footer'] is None:
        brand['footer'] = logo.getpixel((3, 3))[:3]   # logo carries its own navy
    else:
        logo = logo.crop(logo.getbbox())
    logo = logo.resize((width, round(logo.height * width / logo.width)), Image.LANCZOS)
    if not brand['recolor_logo']:
        return logo
    px = logo.load()
    for y in range(logo.height):
        for x in range(logo.width):
            r, g, b, a = px[x, y]
            if a and r < 110 and g < 120 and b < 140 and not (b > g + 25 and g > r + 40):  # dark navy text -> white
                px[x, y] = (255, 255, 255, a)
    return logo


def build(pack_path, scenes):
    pack = json.load(open(pack_path, encoding='utf-8'))
    slides = pack['slides']
    assert len(scenes) == len(slides), 'need %d scenes, got %d' % (len(slides), len(scenes))
    name = os.path.splitext(os.path.basename(pack_path))[0]
    out = os.path.join(PROJ, 'clients', pack['client'], 'output', 'social', 'slides', name, 'chatgpt')
    os.makedirs(out, exist_ok=True)
    brand = BRANDS[pack['client']]
    YELLOW = brand['accent']
    logo = white_logo(250 if pack['client'] == 'virtina' else 232, brand)
    paths = []
    n = len(slides)
    for i, (s, sc) in enumerate(zip(slides, scenes), 1):
        art = Image.open(sc).convert('RGB')
        side = min(art.size)
        art = art.crop(((art.width - side) // 2, (art.height - side) // 2, (art.width + side) // 2, (art.height + side) // 2)).resize((W, W), Image.LANCZOS)
        img = art.convert('RGBA')
        # bottom gradient for text
        grad = Image.new('RGBA', (W, W), (0, 0, 0, 0))
        gp = grad.load()
        top = 470
        for y in range(top, W):
            t = (y - top) / (W - top)
            a = int(min(1, t * 1.25) ** 1.2 * 235)
            for x in range(W):
                gp[x, y] = (6, 14, 64, a)
        img.alpha_composite(grad)
        d = ImageDraw.Draw(img)
        # footer strip
        d.rectangle([0, 984, W, W], fill=tuple(brand['footer']) + (255,))
        d.text((44, 1032), brand['site'], font=font('Poppins-Medium.ttf', 28), fill=WHITE, anchor='lm')
        img.alpha_composite(logo, (W - 44 - logo.width, 1032 - logo.height // 2))
        # counter
        d.text((W - 36, 34), '%d / %d' % (i, n), font=font('Poppins-Medium.ttf', 26), fill=WHITE, anchor='ra')
        mx = 64
        if s['type'] == 'poster':
            f1, l1 = fit(d, s['headline_top'], 'Poppins-ExtraBold.ttf', range(54, 40, -2), W - 2 * mx, 2)
            f2, l2 = fit(d, s['headline_main'], 'Poppins-ExtraBold.ttf', range(78, 50, -2), W - 2 * mx, 2)
            f3, l3 = fit(d, s['sub'], 'Poppins-Medium.ttf', range(34, 26, -1), W - 2 * mx, 2)
            blocks = [(l, f1, WHITE) for l in l1] + [(l, f2, YELLOW) for l in l2] + [(l, f3, WHITE) for l in l3]
        else:
            f1, l1 = fit(d, s['headline'], 'Poppins-ExtraBold.ttf', range(58, 40, -2), W - 2 * mx, 2)
            f2, l2 = fit(d, s['body'], 'Poppins-Medium.ttf', range(32, 24, -1), W - 2 * mx, 4)
            blocks = [(l, f1, YELLOW) for l in l1] + [(l, f2, WHITE) for l in l2]
        heights = [int(f.size * 1.22) for _, f, _ in blocks]
        y = 960 - sum(heights) - 14
        for (line, f, col), h in zip(blocks, heights):
            d.text((mx + 2, y + 2), line, font=f, fill=(4, 10, 50), anchor='la')
            d.text((mx, y), line, font=f, fill=col, anchor='la')
            y += h
        if s['type'] == 'point':
            k = i - 1
            cx, cy, r = 78, 78, 38
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=brand['badge'], outline=brand['badge_outline'], width=3)
            d.text((cx, cy), str(k), font=font('Poppins-ExtraBold.ttf', 40), fill=WHITE, anchor='mm')
        p = os.path.join(out, 'slide-%02d.jpg' % i)
        img.convert('RGB').save(p, quality=92)
        paths.append(p)
    ims = [Image.open(p).convert('RGB') for p in paths]
    pdf = os.path.join(out, '%s-chatgpt.pdf' % pack['slug'])
    ims[0].save(pdf, save_all=True, append_images=ims[1:], resolution=100)
    cols = 3
    sheet = Image.new('RGB', (cols * 360, ((n + cols - 1) // cols) * 360), 'white')
    for k, im in enumerate(ims):
        t = im.resize((360, 360)); sheet.paste(t, ((k % cols) * 360, (k // cols) * 360))
    sheet.save(os.path.join(out, 'contact-sheet.jpg'), quality=90)
    print(out)
    return paths


if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2:])
