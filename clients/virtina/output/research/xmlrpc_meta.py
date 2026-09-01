"""Get all post meta via XMLRPC for post 42202."""
import os, xmlrpc.client, ssl, urllib3
urllib3.disable_warnings()

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    server = xmlrpc.client.ServerProxy(
        "https://virtina.com/xmlrpc.php",
        context=ctx,
        allow_none=True,
    )
    post_data = server.wp.getPost(1, USERNAME, APP_PASSWORD, 42202, ["custom_fields"])
    meta = post_data.get("custom_fields", [])
    print(f"Total meta fields: {len(meta)}")
    for m in meta:
        k = m.get("key", "")
        v = str(m.get("value", ""))
        is_thrive = any(x in k.lower() for x in ["thrv", "thrive", "tve", "tcb"])
        if is_thrive:
            print(f"\n*** THRIVE: {k} ({len(v)} chars) ***")
            print(v[:300])
        else:
            print(f"  {k} = {v[:80]}")
except Exception as e:
    print(f"Error: {e}")
