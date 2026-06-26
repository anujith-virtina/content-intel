"""
Infographic for: what-is-a-passive-catalog (2026-06-26)
860x452, white background, ChatSKU palette (accent #00C9B1, navy #1a1a2e, red #e94560).
Bar chart: passive vs active catalog monthly revenue (worked-example, illustrative).
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
d.text((32, 20), "Passive vs active catalog: monthly revenue", font=F(BOLD, 25), fill=WHITE)
d.text((32, 50), "Same 8,000-SKU distributor. 1,200 after-hours visitors/month.", font=F(REG, 14), fill=ACCENT)

# Chart area
base_y = 358; left_x = 80; bar_w = 130
gap_top = 112
max_val = 32640
def bar_h(v): return int((v / max_val) * (base_y - gap_top))

# Passive bar
pv = 14280; ph = bar_h(pv); px = left_x
d.rectangle([px, base_y - ph, px + bar_w, base_y], fill=GREY)
d.text((px, base_y + 12), "PASSIVE CATALOG", font=F(BOLD, 14), fill=INK)
d.text((px, base_y + 33), "1.4% conversion", font=F(REG, 13), fill=GREY)
d.text((px + 4, base_y - ph - 30), "$14,280", font=F(BOLD, 23), fill=INK)

# Active bar
av = 32640; ah = bar_h(av); ax = left_x + bar_w + 80
d.rectangle([ax, base_y - ah, ax + bar_w, base_y], fill=ACCENT)
d.text((ax, base_y + 12), "ACTIVE CATALOG", font=F(BOLD, 14), fill=NAVY)
d.text((ax, base_y + 33), "3.2% conversion", font=F(REG, 13), fill=ACCENT)
d.text((ax + 4, base_y - ah - 30), "$32,640", font=F(BOLD, 23), fill=ACCENT)

# Gap callout box (right side)
gx = ax + bar_w + 56
d.rounded_rectangle([gx, 148, W - 30, 322], radius=12, fill=LIGHT)
d.rectangle([gx, 162, gx + 6, 308], fill=RED)
d.text((gx + 24, 166), "THE GAP", font=F(BOLD, 14), fill=RED)
d.text((gx + 24, 194), "$18,360", font=F(BOLD, 32), fill=NAVY)
d.text((gx + 24, 236), "lost every month", font=F(REG, 14), fill=GREY)
d.text((gx + 24, 266), "$220,320 / year", font=F(BOLD, 19), fill=RED)

# baseline
d.line([left_x - 10, base_y, ax + bar_w + 10, base_y], fill=(220, 222, 230), width=2)

# Footer
d.text((32, H - 26), "Illustrative worked example. AOV ~$850. Figures for explanation, not a guaranteed result.",
       font=F(REG, 12), fill=GREY)

out = os.path.join(os.environ.get("OUT_DIR", os.getcwd()), "passive_catalog_infographic_860x452.jpg")
img.save(out, "JPEG", quality=88, optimize=True)
print("Saved:", out, img.size, str(os.path.getsize(out)//1024) + "KB")
