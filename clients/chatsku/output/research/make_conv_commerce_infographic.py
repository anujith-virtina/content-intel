"""
Infographic for: b2b-conversational-commerce (2026-06-25)
860x452, ChatSKU palette (accent #00C9B1, navy #1a1a2e).
Four verified figures from the brief/research whitelist.
Output: scratchpad JPEG (uploaded to WP by the build script).
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 860, 452
NAVY = (26, 26, 46)
ACCENT = (0, 201, 177)
CARD = (247, 248, 251)
INK = (26, 26, 46)
GREY = (120, 124, 138)
WHITE = (255, 255, 255)
RED = (233, 69, 96)

def font(path, size):
    return ImageFont.truetype(path, size)

BOLD = r"C:\Windows\Fonts\arialbd.ttf"
REG = r"C:\Windows\Fonts\arial.ttf"

f_title = font(BOLD, 26)
f_big = font(BOLD, 34)
f_label = font(BOLD, 17)
f_sub = font(REG, 14)
f_foot = font(REG, 12)

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

# Header band
d.rectangle([0, 0, W, 84], fill=NAVY)
d.text((32, 22), "What conversational commerce moves", font=f_title, fill=WHITE)
d.text((32, 54), "for a B2B distributor", font=font(REG, 16), fill=ACCENT)

# 2x2 cards
pad = 24
gap = 18
top = 100
card_w = (W - pad * 2 - gap) // 2
card_h = 138
positions = [
    (pad, top),
    (pad + card_w + gap, top),
    (pad, top + card_h + gap),
    (pad + card_w + gap, top + card_h + gap),
]

cards = [
    ("Avg lead response", "42 hrs", "->", "under 2 min", "Faster than any rep can answer"),
    ("Chat-engaged conversion", "3.1%", "->", "12.3%", "~4x lift for engaged buyers"),
    ("B2B research off-hours", "~50%", "", "of buying happens after 5pm", "Captured, not lost"),
    ("Prefer a rep-free buy", "67%", "", "of B2B buyers (Gartner, 2026)", "Self-serve is the default now"),
]

def rounded(draw, box, r, fill):
    draw.rounded_rectangle(box, radius=r, fill=fill)

for (x, y), (label, a, arrow, b, sub) in zip(positions, cards):
    rounded(d, [x, y, x + card_w, y + card_h], 14, CARD)
    d.rectangle([x, y + 14, x + 6, y + card_h - 14], fill=ACCENT)
    d.text((x + 22, y + 18), label.upper(), font=f_label, fill=GREY)
    if arrow:
        # before -> after
        d.text((x + 22, y + 50), a, font=f_big, fill=RED)
        aw = d.textlength(a, font=f_big)
        d.text((x + 22 + aw + 14, y + 58), arrow, font=font(BOLD, 24), fill=GREY)
        arw = d.textlength(arrow, font=font(BOLD, 24))
        d.text((x + 22 + aw + 14 + arw + 14, y + 50), b, font=f_big, fill=ACCENT)
        d.text((x + 22, y + 102), sub, font=f_sub, fill=GREY)
    else:
        d.text((x + 22, y + 50), a, font=font(BOLD, 40), fill=ACCENT)
        aw = d.textlength(a, font=font(BOLD, 40))
        d.text((x + 22 + aw + 12, y + 64), b, font=f_sub, fill=INK)
        d.text((x + 22, y + 102), sub, font=f_sub, fill=GREY)

# Footer
d.text((32, H - 28), "Sources: Gartner 2026; Forrester 2025; chat-engagement benchmark (Envive 2025). Figures illustrative.",
       font=f_foot, fill=GREY)

out = os.path.join(os.environ.get("OUT_DIR", os.getcwd()), "conv_commerce_infographic_860x452.jpg")
img.save(out, "JPEG", quality=88, optimize=True)
print("Saved:", out, img.size, str(os.path.getsize(out)//1024) + "KB")
