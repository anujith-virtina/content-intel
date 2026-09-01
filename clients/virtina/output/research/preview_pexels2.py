"""Preview more body1 candidates — need professional using business software on laptop."""
import requests, io, os, urllib3
from PIL import Image
urllib3.disable_warnings()

SESS = requests.Session()
SESS.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
SESS.verify = False

CDN = "https://images.pexels.com/photos/{id}/pexels-photo-{id}.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"

CANDIDATES = [
    ("body1", 3585088,  "man working on laptop clean"),
    ("body1", 4145340,  "businesswoman laptop desk"),
    ("body1", 4974030,  "person at laptop desk"),
    ("body1", 5716021,  "woman at laptop focused"),
    ("body1", 3775538,  "woman with laptop office"),
    ("body1", 7654209,  "businesswoman laptop clean"),
    ("body1", 3757949,  "professional laptop side view"),
    ("body1", 4491447,  "business person laptop"),
    ("body1", 3975535,  "woman at desk with laptop"),
    ("body1", 1181403,  "woman at laptop professional"),
    ("body1", 6476254,  "professional working laptop"),
    ("body1", 3760067,  "woman laptop blazer - CHECK"),
    ("body1", 6476588,  "businesswoman laptop"),
    ("body1", 4479971,  "person laptop desk professional"),
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
        fname = f"b1cand_{pid}_{w}x{h}.jpg"
        img.save(os.path.join(out_dir, fname), "JPEG", quality=85)
        print(f"OK  {pid} {w}x{h} [{note}] -> {fname}")
    except Exception as e:
        print(f"ERR {pid}: {e}")
