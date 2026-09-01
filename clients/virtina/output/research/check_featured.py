import requests, base64, os, urllib3
urllib3.disable_warnings()
token = base64.b64encode(f"{os.environ['WP_USERNAME']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()
h = {"Authorization": f"Basic {token}"}

for post_id in [42177, 42108, 42074]:
    r = requests.get(f"https://virtina.com/wp-json/wp/v2/posts/{post_id}", headers=h, verify=False, timeout=20)
    d = r.json()
    fmid = d.get("featured_media")
    print(f"\nPost {post_id} featured_media: {fmid}")
    if fmid:
        r2 = requests.get(f"https://virtina.com/wp-json/wp/v2/media/{fmid}", headers=h, verify=False, timeout=20)
        m = r2.json()
        print(f"  URL: {m.get('source_url')}")
        details = m.get("media_details", {})
        print(f"  Size: {details.get('width')}x{details.get('height')}")
        print(f"  Alt: {m.get('alt_text','')[:100]}")
