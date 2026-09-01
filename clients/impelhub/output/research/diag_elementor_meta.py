#!/usr/bin/env python3
"""
Diagnostic: check if _elementor_data and _elementor_edit_mode are
writable via the WordPress REST API for ImpelHub.
"""
import os, sys, base64, json
from pathlib import Path

env_path = Path(r"C:\content-intel\.env")
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

import requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

USER = os.environ.get("IMPELHUB_WP_USERNAME", "")
PASS = os.environ.get("IMPELHUB_WP_APP_PASSWORD", "")
WP_BASE = "https://impelhub.com/wp-json/wp/v2"
POST_ID = 12465

auth_b64 = base64.b64encode(f"{USER}:{PASS}".encode()).decode()
AUTH_HDR = {"Authorization": f"Basic {auth_b64}"}

SESS = requests.Session()
SESS.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Origin":  "https://impelhub.com",
    "Referer": f"https://impelhub.com/wp-admin/post.php?post={POST_ID}&action=edit",
})

print("=" * 60)
print("Step 1: GET post 12465 meta fields (auth required)")
print("=" * 60)
r = SESS.get(
    f"{WP_BASE}/posts/{POST_ID}?context=edit&_fields=id,status,meta",
    headers=AUTH_HDR, timeout=30, verify=False
)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    d = r.json()
    print(f"Post ID: {d.get('id')}")
    meta = d.get("meta", {})
    print(f"Meta keys visible: {list(meta.keys())}")
    if "_elementor_edit_mode" in meta:
        print(f"  _elementor_edit_mode = {repr(meta['_elementor_edit_mode'])}")
    if "_elementor_data" in meta:
        ed = meta.get("_elementor_data", "")
        print(f"  _elementor_data length = {len(ed)}")
        print(f"  _elementor_data[:200] = {ed[:200]}")
else:
    print(r.text[:500])

print()
print("=" * 60)
print("Step 2: GET reference post 12433 meta fields")
print("=" * 60)
r2 = SESS.get(
    f"{WP_BASE}/posts/12433?context=edit&_fields=id,status,meta",
    headers=AUTH_HDR, timeout=30, verify=False
)
print(f"Status: {r2.status_code}")
if r2.status_code == 200:
    d2 = r2.json()
    meta2 = d2.get("meta", {})
    print(f"Meta keys: {list(meta2.keys())}")
    if "_elementor_data" in meta2:
        ed2 = meta2["_elementor_data"]
        print(f"  _elementor_data length: {len(ed2)}")
        print(f"  First 500 chars: {ed2[:500]}")
        # Save full data
        out = Path(r"C:\content-intel\clients\impelhub\output\research\post12433_elementor_data.json")
        out.write_text(ed2, encoding="utf-8")
        print(f"  Full JSON saved to: {out}")
    if "_elementor_edit_mode" in meta2:
        print(f"  _elementor_edit_mode = {repr(meta2['_elementor_edit_mode'])}")
else:
    print(r2.text[:500])

print()
print("=" * 60)
print("Step 3: Try writing _elementor_edit_mode via PATCH")
print("=" * 60)
r3 = SESS.post(
    f"{WP_BASE}/posts/{POST_ID}",
    headers={**AUTH_HDR, "Content-Type": "application/json"},
    json={"meta": {"_elementor_edit_mode": "builder"}},
    timeout=30, verify=False
)
print(f"PATCH status: {r3.status_code}")
if r3.status_code in (200, 201):
    d3 = r3.json()
    meta3 = d3.get("meta", {})
    em = meta3.get("_elementor_edit_mode", "NOT_PRESENT")
    print(f"  _elementor_edit_mode after PATCH = {repr(em)}")
    print("  SUCCESS - meta is writable via REST API")
else:
    print(f"  FAILED: {r3.text[:500]}")
