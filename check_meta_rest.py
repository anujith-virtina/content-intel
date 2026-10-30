"""
Check what meta fields are accessible via REST API for post 42202.
Try to read/write tve_updated_post via /wp/v2/posts/{id}/meta or meta param.
Also check the post schema for registered meta fields.
"""
import os, sys, requests, base64, urllib3, json
urllib3.disable_warnings()
sys.stdout.reconfigure(encoding="utf-8")

USERNAME     = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h  = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0"}
hj = {**h, "Content-Type": "application/json"}
SITE = "https://virtina.com"
WP   = f"{SITE}/wp-json/wp/v2"

# 1. Check OPTIONS on /posts schema for registered meta fields
print("=== POST schema meta fields ===")
r_schema = requests.options(f"{WP}/posts", headers=hj, verify=False, timeout=20)
try:
    schema = r_schema.json()
    meta_schema = schema.get("schema", {}).get("properties", {}).get("meta", {})
    if meta_schema:
        meta_props = meta_schema.get("properties", {})
        print(f"REST-registered meta fields: {list(meta_props.keys())[:20]}")
        for k in meta_props.keys():
            if any(x in k.lower() for x in ["tve", "tcb", "thrive"]):
                print(f"  THRIVE META: {k} = {json.dumps(meta_props[k])[:200]}")
    else:
        print("No meta in schema, or schema not returned")
        print(f"Schema keys: {list(schema.get('schema', {}).get('properties', {}).keys())[:20]}")
except Exception as e:
    print(f"Schema parse error: {e}")

# 2. Try reading meta fields via GET /posts/{id} with _fields=meta
print("\n=== GET post 42202 with meta fields ===")
r_meta = requests.get(f"{WP}/posts/42202?context=edit&_fields=meta",
                       headers=h, verify=False, timeout=20)
try:
    meta_data = r_meta.json().get("meta", {})
    if meta_data:
        print(f"Accessible meta fields: {list(meta_data.keys())}")
        for k, v in meta_data.items():
            sv = str(v)
            if any(x in k.lower() for x in ["tve", "tcb", "thrive"]):
                print(f"  THRIVE: {k} = {sv[:200]}")
    else:
        print(f"meta is empty: {r_meta.json()}")
except Exception as e:
    print(f"Parse error: {e}, raw: {r_meta.text[:300]}")

# 3. Try to PATCH tve_updated_post via REST meta
print("\n=== Try PATCH with meta.tve_updated_post ===")
# Get current content.raw to use as value
r_post = requests.get(f"{WP}/posts/42202?context=edit", headers=h, verify=False, timeout=30)
content_raw = r_post.json()["content"]["raw"]
print(f"Current content.raw: {len(content_raw)} chars, 28px: {'28px' in content_raw}")

r_patch = requests.patch(f"{WP}/posts/42202",
                          json={"meta": {"tve_updated_post": content_raw}},
                          headers=hj, verify=False, timeout=30)
print(f"PATCH with meta.tve_updated_post: {r_patch.status_code}")
try:
    resp = r_patch.json()
    meta_resp = resp.get("meta", {})
    tve_val = meta_resp.get("tve_updated_post", "NOT_IN_RESPONSE")
    print(f"  tve_updated_post in response: {str(tve_val)[:100]}")
except:
    print(f"  raw: {r_patch.text[:300]}")

# 4. Try PATCH with _tve_updated_post (underscore prefix)
print("\n=== Try PATCH with meta._tve_updated_post ===")
r_patch2 = requests.patch(f"{WP}/posts/42202",
                           json={"meta": {"_tve_updated_post": content_raw}},
                           headers=hj, verify=False, timeout=30)
print(f"PATCH with meta._tve_updated_post: {r_patch2.status_code}: {r_patch2.text[:200]}")

# 5. Try Thrive's own endpoint with explicit save
print("\n=== Try POST /tcb/v1/posts/html with explicit action=save ===")
for payload in [
    {"post_id": 42202, "tve_content": content_raw, "action": "save"},
    {"post_id": 42202, "tve_content": content_raw, "save": True},
    {"post_id": 42202, "content": content_raw, "post_status": "publish"},
]:
    r_tcb = requests.post(f"{SITE}/wp-json/tcb/v1/posts/html",
                           json=payload, headers=hj, verify=False, timeout=20)
    print(f"  keys={list(payload.keys())} -> {r_tcb.status_code}: {r_tcb.text[:150]}")
