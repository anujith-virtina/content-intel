import urllib.request, base64, json, ssl, os
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE
UN = os.environ['CHATSKU_WP_USERNAME']
PW = os.environ['CHATSKU_WP_APP_PASSWORD']
creds = base64.b64encode(f'{UN}:{PW}'.encode()).decode()
H = {'Authorization': f'Basic {creds}', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
targets = [
    'https://chatsku.com/wp-json/wp/v2/posts/211?force=true',
    'https://chatsku.com/wp-json/wp/v2/media/208?force=true',
    'https://chatsku.com/wp-json/wp/v2/media/209?force=true',
    'https://chatsku.com/wp-json/wp/v2/media/210?force=true',
]
for url in targets:
    req = urllib.request.Request(url, headers=H, method='DELETE')
    try:
        with urllib.request.urlopen(req, timeout=15, context=SSL_CTX) as r:
            d = json.loads(r.read())
            label = url.split('/')[-1].split('?')[0]
            print(f'Deleted {label}: {d.get("deleted")}')
    except Exception as e:
        print(f'Error on {url}: {e}')
