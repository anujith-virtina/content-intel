"""Preview candidate Pexels images before uploading."""
import requests, io, os, urllib3
from PIL import Image
urllib3.disable_warnings()

SESS = requests.Session()
SESS.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
SESS.verify = False

CDN = "https://images.pexels.com/photos/{id}/pexels-photo-{id}.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"

# Candidates to preview: (slot, pexels_id, note)
CANDIDATES = [
    # Featured — need wide professional B2B/office team scene
    ("featured", 3182812,  "business group modern office"),
    ("featured", 1181263,  "group business people open office"),
    ("featured", 3184292,  "business team meeting room"),
    ("featured", 3183153,  "people modern office computers"),
    ("featured", 3184319,  "people desk computers office"),
    ("featured", 3182781,  "women smiling laptop screen"),
    ("featured", 3184465,  "people modern open plan office"),
    # Body1 — section: portal features, someone using a business software/portal
    ("body1", 1181271,  "woman working at laptop focused"),
    ("body1", 3760067,  "professional woman laptop blazer"),
    ("body1", 4491461,  "woman at desk with laptop"),
    ("body1", 2381069,  "person using laptop at desk"),
    ("body1", 1181244,  "business woman white laptop"),
    ("body1", 7364107,  "person working on computer"),
    # Body2 — cost/timeline, business planning meeting
    ("body2", 3183150,  "man and woman reviewing screen"),
    ("body2", 1181316,  "three men laptops conference"),
    ("body2", 3184465,  "modern office team people"),
    ("body2", 5325076,  "team meeting office laptops"),
    ("body2", 1181388,  "woman presenting meeting room"),
    # Body3 — buyer adoption, person placing online order on laptop
    ("body3", 3183197,  "two women computer laptop"),
    ("body3", 7654203,  "professional woman laptop smiling"),
    ("body3", 3861969,  "man at laptop focused"),
    ("body3", 1181271,  "woman using laptop working"),
    ("body3", 4491461,  "woman working laptop desk"),
]

out_dir = os.path.join(os.path.dirname(__file__), "preview_images")
os.makedirs(out_dir, exist_ok=True)

for slot, pid, note in CANDIDATES:
    url = CDN.format(id=pid)
    try:
        r = SESS.get(url, timeout=20, allow_redirects=True)
        if r.status_code != 200 or len(r.content) < 20000:
            print(f"SKIP {pid} ({r.status_code} {len(r.content)//1024}KB)")
            continue
        img = Image.open(io.BytesIO(r.content))
        w, h = img.size
        fname = f"{slot}_{pid}_{w}x{h}.jpg"
        img.save(os.path.join(out_dir, fname), "JPEG", quality=85)
        print(f"OK  {slot} {pid} {w}x{h} [{note}] -> {fname}")
    except Exception as e:
        print(f"ERR {pid}: {e}")

print(f"\nPreviews saved to: {out_dir}")
