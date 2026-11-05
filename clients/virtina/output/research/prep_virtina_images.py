"""Prepare Virtina blog images: bodies 1340x704 (correct crop for any source ratio, never pads), featured with the logo pill.
Usage: python prep_virtina_images.py <folder> [body1-raw.png body2-raw.png body3-raw.png featured-raw.png names]"""
import sys, os
from PIL import Image, ImageDraw, ImageFilter
ROOT = r'C:\content-intel'
folder = sys.argv[1]
src = {'body1': 'body1-raw.png', 'body2': sys.argv[2] if len(sys.argv) > 2 else 'body2-raw.png', 'body3': 'body3-raw.png', 'featured': 'featured-raw.png'}
for slot in ('body1', 'body2', 'body3'):
    im = Image.open(os.path.join(folder, src[slot])).convert('RGB'); w, h = im.size
    ratio = 1340 / 704
    if w / h > ratio:  # too wide: trim sides
        nw = round(h * ratio); l = (w - nw) // 2; im = im.crop((l, 0, l + nw, h))
    else:              # too tall: trim top and bottom
        nh = round(w / ratio); t = (h - nh) // 2; im = im.crop((0, t, w, t + nh))
    assert im.size[0] >= 1340 or True
    im.resize((1340, 704), Image.LANCZOS).save(os.path.join(folder, 'final_%s.jpg' % slot), quality=93, subsampling=0)
im = Image.open(os.path.join(folder, src['featured'])).convert('RGB'); w, h = im.size
th = round(w / 2.617)
if th <= h:
    t = (h - th) // 2; im = im.crop((0, t, w, t + th))
w, h = im.size
logo = Image.open(os.path.join(ROOT, 'social', 'brand', 'virtina-logo.webp')).convert('RGBA')
pw = round(w * 0.1375); ph = round(w * 83 / 2000); lw = round(pw * 0.85); lh = round(logo.height * lw / logo.width)
if lh > ph * 0.8:
    lh = round(ph * 0.8); lw = round(logo.width * lh / logo.height)
logo = logo.resize((lw, lh), Image.LANCZOS)
x = w - round(w * 0.016) - pw; y = h - round(h * 0.036) - ph
sh = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x, y + 3, x + pw, y + ph + 3), radius=ph // 2, fill=(0, 0, 0, 70)); sh = sh.filter(ImageFilter.GaussianBlur(4))
ov = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(ov).rounded_rectangle((x, y, x + pw, y + ph), radius=ph // 2, fill=(255, 255, 255, 237))
base = im.convert('RGBA'); base.alpha_composite(sh); base.alpha_composite(ov); base.alpha_composite(logo, (x + (pw - lw) // 2, y + (ph - lh) // 2))
base.convert('RGB').save(os.path.join(folder, 'final_featured.jpg'), quality=93, subsampling=0)
print('done', folder)
