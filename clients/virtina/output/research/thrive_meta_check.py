"""Check Thrive meta via XMLRPC and explore /tcb/v1 POST endpoint."""
import os, requests, base64, urllib3, json, xmlrpc.client
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
api_h = {"Authorization": f"Basic {token}",
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
         "Content-Type": "application/json"}

# --- Try XMLRPC to get all post meta (including private) ---
print("=== XMLRPC: get post meta for 42202 ===")
try:
    transport = xmlrpc.client.Transport()
    server = xmlrpc.client.ServerProxy(
        "https://virtina.com/xmlrpc.php",
        transport=transport,
        use_datetime=True,
        allow_none=True,
    )
    # wp.getPost returns all meta including private
    post_data = server.wp.getPost(1, USERNAME, APP_PASSWORD, 42202,
                                   ["post_meta"])
    meta = post_data.get("custom_fields", [])
    print(f"Total meta fields: {len(meta)}")
    for m in meta:
        k = m.get("key", "")
        v = str(m.get("value", ""))
        if "thrv" in k.lower() or "thrive" in k.lower() or "tve" in k.lower() or "tcb" in k.lower():
            print(f"  THRIVE: {k} = {v[:200]}")
        elif len(v) < 100:
            print(f"  {k} = {v}")
        else:
            print(f"  {k} = [{len(v)} chars]")
except Exception as e:
    print(f"XMLRPC error: {e}")

# --- Try POST to /tcb/v1/posts/html with minimal payload ---
print("\n=== POST /tcb/v1/posts/html (probe) ===")
r = requests.post(
    "https://virtina.com/wp-json/tcb/v1/posts/html",
    json={"post_id": 42202},
    headers=api_h, verify=False, timeout=20,
)
print(f"Status: {r.status_code}")
print(r.text[:500])
