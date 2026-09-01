import urllib.request, ssl, json, urllib.parse

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def search(q, n=8):
    url = f"https://api.openverse.org/v1/images/?source=stocksnap&q={urllib.parse.quote(q)}&page_size={n}&license_type=commercial"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
        data = json.loads(r.read())
    return [(x['id'], x['url'], x['width'], x['height']) for x in data['results']]

searches = {
    "featured":  "working typing computer desk",
    "body1":     "office computer work business",
    "body2":     "coworkers office computer work",
}

for label, query in searches.items():
    print(f"\n=== {label} ('{query}') ===")
    for id_, url, w, h in search(query):
        print(f"  {id_[:8]}  {w}x{h}  {url}")
