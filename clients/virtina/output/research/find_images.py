"""Search Openverse for section-specific images and preview candidates."""
import urllib.request, ssl, json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def search(q, n=8):
    url = f"https://api.openverse.org/v1/images/?source=stocksnap&q={urllib.parse.quote(q)}&page_size={n}&license_type=commercial"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
        data = json.loads(r.read())
    return [(x['id'], x['url'], x['width'], x['height']) for x in data['results']]

import urllib.parse

searches = {
    "featured_seo_analytics":   "laptop screen website analytics",
    "body1_platform_comparison": "ecommerce website laptop screen",
    "body2_performance_data":    "macbook desk business work",
}

for label, query in searches.items():
    print(f"\n=== {label} (query: '{query}') ===")
    for id_, url, w, h in search(query):
        ratio = round(w/h, 2)
        print(f"  {id_[:8]}  {w}x{h} ({ratio})  {url}")
