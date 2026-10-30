"""Check what images 212, 213, 214 actually are on ChatSKU."""
import urllib.request, base64, json, ssl, os

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

UN = os.environ['CHATSKU_WP_USERNAME']
PW = os.environ['CHATSKU_WP_APP_PASSWORD']
creds = base64.b64encode(f'{UN}:{PW}'.encode()).decode()
H = {
    'Authorization': f'Basic {creds}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

for mid in [212, 213, 214]:
    req = urllib.request.Request(f'https://chatsku.com/wp-json/wp/v2/media/{mid}', headers=H)
    with urllib.request.urlopen(req, timeout=15, context=SSL_CTX) as r:
        d = json.loads(r.read())
    print(f'ID={mid}  src={d.get("source_url","").split("/")[-1]}')
    print(f'       title={d.get("title",{}).get("rendered","")}')
    print(f'       alt={d.get("alt_text","")}')
