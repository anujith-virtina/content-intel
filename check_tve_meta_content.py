"""
Read tve_updated_post meta for post 42202 via XML-RPC.
If it exists, Thrive renders from it — not from post_content.
"""
import os, sys, xmlrpc.client, ssl, urllib3
urllib3.disable_warnings()
sys.stdout.reconfigure(encoding="utf-8")

USERNAME     = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
SITE = "https://virtina.com"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
server = xmlrpc.client.ServerProxy(f"{SITE}/xmlrpc.php", context=ctx, allow_none=True)

post = server.wp.getPost(1, USERNAME, APP_PASSWORD, 42202, ["custom_fields"])
fields = post.get("custom_fields", [])
print(f"Total meta fields on post 42202: {len(fields)}\n")

thrive_keys = []
for m in fields:
    k = m.get("key", "")
    v = str(m.get("value", ""))
    if any(x in k.lower() for x in ["tve", "tcb", "thrive", "thrv"]):
        thrive_keys.append(k)
        print(f"THRIVE META: {k}")
        print(f"  value length: {len(v)}")
        if "tve_updated_post" in k:
            print(f"  padding 32px: {'padding:8px 0 8px 32px' in v}")
            print(f"  padding 28px: {'padding:8px 0 8px 28px' in v}")
            print(f"  thrv-styled_list: {'thrv-styled_list' in v}")
            print(f"  &#10095;: {'&#10095;' in v}")
            print(f"  First 400 chars of content:\n  {v[:400]}")
        print()

if not thrive_keys:
    print("No Thrive meta found on post 42202 via XML-RPC.")
    print("(Private meta starting with _ may not be returned by wp.getPost)")
    print("\nAll meta keys returned:")
    for m in fields:
        print(f"  {m.get('key','')} ({len(str(m.get('value','')))} chars)")
