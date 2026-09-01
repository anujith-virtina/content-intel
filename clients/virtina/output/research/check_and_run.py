#!/usr/bin/env python3
"""
Check prerequisites and run the Virtina publish pipeline.
"""
import os
import sys
import json
import time
import requests
import base64

# Load .env
env_path = r"C:\content-intel\.env"
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()
    print("Loaded .env")

WP_USERNAME = os.environ.get("WP_USERNAME", "")
WP_APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")

print(f"WP_USERNAME: {WP_USERNAME}")
print(f"WP_APP_PASSWORD set: {'YES' if WP_APP_PASSWORD else 'NO'}")
print(f"PEXELS_API_KEY set: {'YES' if PEXELS_API_KEY else 'NO'}")

# Test PIL
try:
    from PIL import Image
    print("Pillow: AVAILABLE")
    PIL_AVAILABLE = True
except ImportError:
    print("Pillow: NOT AVAILABLE")
    PIL_AVAILABLE = False

# Test WP auth
if WP_USERNAME and WP_APP_PASSWORD:
    auth_b64 = base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()).decode()
    headers = {"Authorization": f"Basic {auth_b64}"}
    try:
        r = requests.get("https://virtina.com/wp-json/wp/v2/users/me", headers=headers, timeout=15)
        print(f"WP auth test: {r.status_code} - {r.json().get('name', r.text[:50]) if r.status_code == 200 else r.text[:100]}")
    except Exception as e:
        print(f"WP auth test error: {e}")

# Test Openverse
try:
    r = requests.get("https://api.openverse.org/v1/images/?q=office+laptop&per_page=3&license=cc0", timeout=15)
    print(f"Openverse test: {r.status_code} - {len(r.json().get('results',[])) if r.status_code==200 else r.text[:100]} results")
except Exception as e:
    print(f"Openverse test error: {e}")

print("\nCheck complete.")
print(f"PIL available: {PIL_AVAILABLE}")
print("Ready to proceed." if PIL_AVAILABLE and WP_USERNAME and WP_APP_PASSWORD else "NOT ready - fix issues above.")
