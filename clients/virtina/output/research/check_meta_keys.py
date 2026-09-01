"""Check meta keys for both posts via XMLRPC + REST to find Thrive flags."""
import os, sys, requests, base64, urllib3, xmlrpc.client
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://virtina.com"
USERNAME = "anujith"
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
REAL_PASSWORD = os.environ.get("WP_REAL_PASSWORD", "")

# XMLRPC to get all meta for post 42177 (working) and 42202 (broken)
print("=== XMLRPC meta keys ===")
transport = xmlrpc.client.Transport()
transport.https = True

class SSLTransport(xmlrpc.client.SafeTransport):
    def make_connection(self, host):
        import http.client, ssl
        conn = http.client.HTTPSConnection(host, context=ssl.create_default_context())
        conn._context.check_hostname = False
        conn._context.verify_mode = ssl.CERT_NONE
        return conn

proxy = xmlrpc.client.ServerProxy(f"{SITE}/xmlrpc.php", transport=SSLTransport(), allow_none=True)

for post_id in [42177, 42202]:
    try:
        post = proxy.wp.getPost(0, USERNAME, REAL_PASSWORD, post_id, ["custom_fields"])
        fields = post.get("custom_fields", [])
        print(f"\nPost {post_id} — {len(fields)} custom fields:")
        for f in fields:
            k = f["key"]
            v = str(f["value"])[:80]
            print(f"  {k}: {v}")
    except Exception as e:
        print(f"Post {post_id} XMLRPC error: {e}")

# Also use REST API to check meta
print("\n=== REST meta ===")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0"}
for post_id in [42177, 42202]:
    r = requests.get(f"{SITE}/wp-json/wp/v2/posts/{post_id}?context=edit", headers=h, verify=False, timeout=20)
    meta = r.json().get("meta", {})
    print(f"\nPost {post_id} REST meta keys: {list(meta.keys())[:30]}")
    for k, v in meta.items():
        if v and v not in [False, 0, "", []]:
            print(f"  {k}: {str(v)[:80]}")
