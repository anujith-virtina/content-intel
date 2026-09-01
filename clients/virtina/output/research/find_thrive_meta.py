"""
Get ALL post meta for post 42202 via XMLRPC.
Find Thrive Architect content storage meta key.
"""
import os, sys, urllib3, xmlrpc.client, ssl
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://virtina.com"
USERNAME = "anujith"
PASSWORD = os.environ.get("WP_REAL_PASSWORD", "")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
transport = xmlrpc.client.SafeTransport(context=ctx)
client = xmlrpc.client.ServerProxy(f"{SITE}/xmlrpc.php", transport=transport)

print("Getting post 42202 via XMLRPC...")
try:
    post = client.wp.getPost(1, USERNAME, PASSWORD, 42202,
                              ["post_title", "post_content", "custom_fields"])
    content = post.get("post_content", "")
    print(f"post_content: {len(content)} chars, SVGs: {content.count('fill:#43627f')}, arrows: {content.count(chr(0x279C))}, #43627f: {content.count('#43627f')}")
    toc_idx = content.find("Table of Contents")
    if toc_idx >= 0:
        li = content.find("<li", toc_idx)
        print(f"First TOC li:\n{content[li:li+300]}")
    fields = post.get("custom_fields", [])
    print(f"\nAll {len(fields)} custom fields:")
    for f in fields:
        key = f.get("key", "")
        val = str(f.get("value", ""))
        marker = " *** THRIVE" if any(x in key.lower() for x in ["tve", "tcb", "thrive", "lightspeed"]) else ""
        print(f"  {key}: {val[:100]}{marker}")
except Exception as e:
    print(f"Error: {e}")
