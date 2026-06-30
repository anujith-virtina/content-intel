"""
Infographic for: b2b-chatbot-for-woocommerce (2026-06-29)
860x452, white background, ChatSKU palette (accent #00C9B1, navy #1a1a2e, red #e94560).
Before/after after-hours conversion bar chart for the 4,200-SKU WooCommerce distributor example.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 860, 452
NAVY = (26, 26, 46); ACCENT = (0, 201, 177); RED = (233, 69, 96)
INK = (26, 26, 46); GREY = (120, 124, 138); WHITE = (255, 255, 255); LIGHT = (240, 244, 255)

BOLD = r"C:\Windows\Fonts\arialbd.ttf"; REG = r"C:\Windows\Fonts\arial.ttf"
def F(p, s): return ImageFont.truetype(p, s)

img = Image.new("RGB", (W, H), WHITE); d = ImageDraw.Draw(img)

# Header band
d.rectangle([0, 0, W, 78], fill=NAVY)
d.text((32, 18), "WooCommerce B2B store: before vs after a chatbot", font=F(BOLD, 24), fill=WHITE)
d.text((32, 50), "4,200 SKUs. 980 after-hours visitors/month. $750 AOV.", font=F(REG, 14), fill=ACCENT)

# Chart area
base_y = 358; left_x = 80; bar_w = 130
gap_top = 112
max_val = 24990
def bar_h(v): return int((v / max_val) * (base_y - gap_top))

# Before bar
bv = 11760; bh = bar_h(bv); bx = left_x
d.rectangle([bx, base_y - bh, bx + bar_w, base_y], fill=GREY)
d.text((bx - 4, base_y + 12), "BEFORE", font=F(BOLD, 14), fill=INK)
d.text((bx - 4, base_y + 33), "1.6% conversion", font=F(REG, 13), fill=GREY)
d.text((bx, base_y - bh - 30), "$11,760/mo", font=F(BOLD, 21), fill=INK)

# After bar
av = 24990; ah = bar_h(av); ax = left_x + bar_w + 80
d.rectangle([ax, base_y - ah, ax + bar_w, base_y], fill=ACCENT)
d.text((ax - 4, base_y + 12), "AFTER", font=F(BOLD, 14), fill=NAVY)
d.text((ax - 4, base_y + 33), "3.4% conversion", font=F(REG, 13), fill=ACCENT)
d.text((ax, base_y - ah - 30), "$24,990/mo", font=F(BOLD, 21), fill=ACCENT)

# Gap callout box (right side)
gx = ax + bar_w + 56
d.rounded_rectangle([gx, 140, W - 30, 330], radius=12, fill=LIGHT)
d.rectangle([gx, 156, gx + 6, 314], fill=RED)
d.text((gx + 24, 158), "AFTER-HOURS GAIN", font=F(BOLD, 14), fill=RED)
d.text((gx + 24, 188), "$13,230", font=F(BOLD, 32), fill=NAVY)
d.text((gx + 24, 230), "more every month", font=F(REG, 14), fill=GREY)
d.text((gx + 24, 262), "$158,760 / year", font=F(BOLD, 19), fill=RED)

# baseline
d.line([left_x - 10, base_y, ax + bar_w + 10, base_y], fill=(220, 222, 230), width=2)

# Footer
d.text((32, H - 26), "Illustrative worked example. Same traffic, better answers. Figures for explanation, not a guaranteed result.",
       font=F(REG, 12), fill=GREY)

out = os.path.join(os.environ.get("OUT_DIR", os.getcwd()), "woocommerce_b2b_infographic_860x452.jpg")
img.save(out, "JPEG", quality=88, optimize=True)
print("Saved:", out, img.size, str(os.path.getsize(out)//1024) + "KB")
