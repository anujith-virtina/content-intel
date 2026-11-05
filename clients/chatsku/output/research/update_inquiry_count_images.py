# Swap the images on live post 4015 in place (no new post). Imports the build module for its sections.
import sys, os, json, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_inquiry_count_post as b

PID = 4015
live = json.load(urllib.request.urlopen(urllib.request.Request(f"{b.WP}/posts/{PID}?context=edit", headers=b.H), timeout=60))
assert live["status"] == "publish", live["status"]
media = {slot: b.upload_image(slot, path, alt) for slot, (path, alt, _) in b.IMAGES.items()}
print("new media:", {k: v["id"] for k, v in media.items()})
elementor = json.dumps(b.resolve(b.sections, media), ensure_ascii=False)
res = b.post_json(f"{b.WP}/posts/{PID}", {"featured_media": media["featured"]["id"],
                                           "meta": {"_elementor_data": elementor}})
print("updated", res["id"], res["status"], res["featured_media"])
st = json.load(open(b.STATE_PATH, encoding="utf-8"))
st["media"] = media
json.dump(st, open(b.STATE_PATH, "w", encoding="utf-8"), indent=2)
try:
    urllib.request.urlopen(urllib.request.Request("https://chatsku.com/wp-json/elementor/v1/cache", headers=b.H, method="DELETE"), timeout=60)
    print("cache cleared")
except Exception as e:
    print("cache error", e)
