"""
Push woocommerce-erp-integration post to WordPress as draft.
Reads credentials from C:\content-intel\.env
"""
import base64
import json
import urllib.request
import urllib.error
import re

# --- Load credentials ---
env_path = r"C:\content-intel\.env"
creds = {}
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            creds[k.strip()] = v.strip()

WP_USERNAME = creds["WP_USERNAME"]
WP_APP_PASSWORD = creds["WP_APP_PASSWORD"]

# --- Build auth header ---
token = base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode("utf-8")).decode("utf-8")
auth_header = f"Basic {token}"

# --- Read the published file and extract post_content (strip frontmatter) ---
published_path = r"C:\content-intel\clients\virtina\output\published\woocommerce-erp-integration-2026-05-07.md"
with open(published_path, "r", encoding="utf-8") as f:
    raw = f.read()

# Strip YAML frontmatter (between first two --- lines)
# Find second --- after the first
parts = raw.split("---", 2)
# parts[0] = "" (before first ---), parts[1] = frontmatter, parts[2] = content
post_content = parts[2].strip() if len(parts) >= 3 else raw.strip()

# --- Build payload ---
payload = {
    "title": "How to connect WooCommerce to your ERP: a practical guide for B2B manufacturers and distributors",
    "slug": "woocommerce-erp-integration",
    "status": "draft",
    "content": post_content,
    "featured_media": 0,
    "categories": [79, 84],
    "author": 9,
    "meta": {
        "_yoast_wpseo_title": "WooCommerce ERP integration for B2B manufacturers | Virtina",
        "_yoast_wpseo_metadesc": "Learn how to connect WooCommerce to your ERP. A guide for B2B manufacturers and distributors covering data mapping, sync strategy, and connector selection.",
        "_yoast_wpseo_focuskw": "WooCommerce ERP integration"
    }
}

payload_json = json.dumps(payload, ensure_ascii=False).encode("utf-8")

# --- Make POST request ---
endpoint = "https://virtina.com/wp-json/wp/v2/posts"
req = urllib.request.Request(
    endpoint,
    data=payload_json,
    method="POST",
    headers={
        "Authorization": auth_header,
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "VirtinaPublisher/1.0"
    }
)

print(f"Posting to: {endpoint}")
print(f"Username: {WP_USERNAME}")
print(f"Payload size: {len(payload_json)} bytes")
print(f"SEO title length: {len(payload['meta']['_yoast_wpseo_title'])} chars")
print(f"Meta desc length: {len(payload['meta']['_yoast_wpseo_metadesc'])} chars")

try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        status_code = resp.status
        response_body = resp.read().decode("utf-8")
        response_json = json.loads(response_body)
        post_id = response_json.get("id")
        post_link = response_json.get("link", "")
        edit_link = response_json.get("guid", {}).get("raw", "") if isinstance(response_json.get("guid"), dict) else ""
        print(f"\nSUCCESS: HTTP {status_code}")
        print(f"Post ID: {post_id}")
        print(f"Post link: {post_link}")
        print(f"Edit URL: https://virtina.com/wp-admin/post.php?post={post_id}&action=edit")
        # Save response for reference
        out_path = r"C:\content-intel\clients\virtina\output\research\push_erp_response.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(response_json, f, indent=2, ensure_ascii=False)
        print(f"Full response saved to: {out_path}")
except urllib.error.HTTPError as e:
    error_body = e.read().decode("utf-8")
    print(f"\nFAILED: HTTP {e.code} {e.reason}")
    print(f"Error body: {error_body[:2000]}")
    out_path = r"C:\content-intel\clients\virtina\output\research\push_erp_error.json"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(error_body)
    print(f"Full error saved to: {out_path}")
except Exception as ex:
    print(f"\nFAILED with exception: {type(ex).__name__}: {ex}")
