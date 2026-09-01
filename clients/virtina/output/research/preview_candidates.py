"""Download candidate images at low res for preview."""
import urllib.request, ssl, os
from PIL import Image
from io import BytesIO

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

CANDIDATES = {
    "feat_A": "https://cdn.stocksnap.io/img-thumbs/960w/0E0M5W9O3V.jpg",
    "feat_B": "https://cdn.stocksnap.io/img-thumbs/960w/3ZHG0XOIT6.jpg",
    "feat_C": "https://cdn.stocksnap.io/img-thumbs/960w/4O4FZUVSIU.jpg",
    "b1_A":   "https://cdn.stocksnap.io/img-thumbs/960w/JBW2PXDOL6.jpg",
    "b1_B":   "https://cdn.stocksnap.io/img-thumbs/960w/69TMH4ITIE.jpg",
    "b1_C":   "https://cdn.stocksnap.io/img-thumbs/960w/DWLWL9USBG.jpg",
    "b2_A":   "https://cdn.stocksnap.io/img-thumbs/960w/Z1ZIMB54UM.jpg",
    "b2_B":   "https://cdn.stocksnap.io/img-thumbs/960w/Y01VDYAX63.jpg",
}

OUT = r"C:\content-intel\clients\virtina\output\research\preview"
os.makedirs(OUT, exist_ok=True)

for name, url in CANDIDATES.items():
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
        img = Image.open(BytesIO(r.read())).convert("RGB")
    # save small preview
    img.thumbnail((400, 300))
    out = os.path.join(OUT, f"{name}.jpg")
    img.save(out, "JPEG", quality=70)
    print(f"Saved {name}: {img.size}")
