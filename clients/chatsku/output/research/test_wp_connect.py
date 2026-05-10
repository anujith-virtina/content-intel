"""Test WP connectivity and Openverse image download."""
import base64, requests, sys

WP_USER = "admin"
WP_PASS = "fL5q VbD3 20Nt sOjx 86wb 94iS"
WP_BASE = "https://chatsku.com/wp-json/wp/v2"
BROWSER_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
AUTH = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
HEADERS = {"User-Agent": BROWSER_UA, "Authorization": f"Basic {AUTH}"}

print("=== Test 1: WP API auth ===")
r = requests.get(f"{WP_BASE}/users/me", headers=HEADERS, timeout=15)
print(f"HTTP {r.status_code}: {r.text[:200]}")

print("\n=== Test 2: Openverse image download ===")
img_url = "https://cdn.stocksnap.io/img-thumbs/960w/XGXORJWZIX.jpg"
r2 = requests.get(img_url, headers={"User-Agent": BROWSER_UA, "Referer": "https://openverse.org/"}, timeout=20)
print(f"HTTP {r2.status_code}, size={len(r2.content)} bytes")

print("\n=== Test 3: Openverse API ===")
r3 = requests.get(
    "https://api.openverse.org/v1/images/",
    params={"q": "office desk laptop", "source": "stocksnap", "page_size": 3},
    headers={"User-Agent": BROWSER_UA},
    timeout=15
)
print(f"HTTP {r3.status_code}")
if r3.status_code == 200:
    data = r3.json()
    print(f"Results: {len(data.get('results', []))}")
    for item in data.get('results', []):
        print(f"  {item.get('title')} -- {item.get('url')}")
