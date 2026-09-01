# LinkedIn card for the agentic commerce glossary post.
# 1200x627 (LinkedIn's preferred landscape ratio).
# Palette from clients/chatsku/brand-primary.txt.
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 627
BG      = "#0f172a"   # page background dark
ACCENT  = "#00C9B1"   # primary brand accent
ACCENT2 = "#4eddcc"   # lighter teal
TEXT    = "#f8fafc"   # text primary on dark
MUTED   = "#94a3b8"   # text muted
RED     = "#e94560"   # CTA red, used for the struck-through claim

F = "C:/Windows/Fonts/"
def font(name, size):
    return ImageFont.truetype(F + name, size)

f_kicker = font("segoeuib.ttf", 22)
f_huge   = font("seguibl.ttf", 118)
f_huge2  = font("seguibl.ttf", 118)
f_label  = font("seguisb.ttf", 24)
f_unit   = font("segoeui.ttf", 26)
f_body   = font("seguisb.ttf", 30)
f_src    = font("segoeui.ttf", 20)
f_mark   = font("seguibl.ttf", 28)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# top accent bar
d.rectangle([0, 0, W, 7], fill=ACCENT)

def spaced(draw, xy, text, fnt, fill, tracking=4, anchor_center=False):
    """Draw text with manual letter-spacing. Returns total width."""
    total = sum(draw.textlength(c, font=fnt) + tracking for c in text) - tracking
    x, y = xy
    if anchor_center:
        x -= total / 2
    for c in text:
        draw.text((x, y), c, font=fnt, fill=fill)
        x += draw.textlength(c, font=fnt) + tracking
    return total

# kicker
spaced(d, (70, 62), "AGENTIC COMMERCE REALITY CHECK", f_kicker, ACCENT, tracking=3)

# ---- two-column stat contrast ----
LEFT_CX, RIGHT_CX = 340, 880
LABEL_Y, NUM_Y, UNIT_Y = 150, 195, 335

def col(cx, label, number, unit, num_fill, strike=False):
    d.text((cx, LABEL_Y), label, font=f_label, fill=MUTED, anchor="ma")
    d.text((cx, NUM_Y), number, font=f_huge, fill=num_fill, anchor="ma")
    if strike:
        w = d.textlength(number, font=f_huge)
        bbox = d.textbbox((cx, NUM_Y), number, font=f_huge, anchor="ma")
        ymid = (bbox[1] + bbox[3]) / 2 + 6
        d.line([cx - w/2 - 12, ymid, cx + w/2 + 12, ymid], fill=RED, width=7)
    d.text((cx, UNIT_Y), unit, font=f_unit, fill=MUTED, anchor="ma")

col(LEFT_CX,  "PROMOTED AT LAUNCH",  "1M+", "merchants, Sept 2025", TEXT, strike=True)
col(RIGHT_CX, "ACTUALLY LIVE",       "~30", "merchants, Feb 2026",  ACCENT)

# vertical divider
d.line([(W//2 + 20), 150, (W//2 + 20), 370], fill="#1e293b", width=3)

# ---- bottom statement ----
d.line([70, 432, W-70, 432], fill="#1e293b", width=2)
d.text((70, 462), "OpenAI ended in-chat checkout on March 24, 2026.", font=f_body, fill=TEXT)
d.text((70, 503), "It converted at about a third the rate of sending the buyer to the merchant's own site.",
       font=f_src, fill=MUTED)
d.text((70, 545), "Source: Forrester", font=f_src, fill=MUTED)

# wordmark
mark = "ChatSKU"
mw = d.textlength(mark, font=f_mark)
d.text((W - 70 - mw, 540), mark, font=f_mark, fill=ACCENT)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "linkedin_card.png")
img.save(out, "PNG", optimize=True)
print("saved", out, img.size, os.path.getsize(out)//1024, "KB")
