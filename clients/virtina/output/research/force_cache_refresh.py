"""Force Batcache to re-populate by touching the post, then fetching the live URL."""
import os, requests, base64, urllib3, time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
api_h = {"Authorization": f"Basic {token}",
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
         "Content-Type": "application/json"}
pg_h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Cache-Control": "no-cache", "Pragma": "no-cache"}

TARGET = "fill:#43627f"

# Verify current DB content has SVGs
r_db = requests.get("https://virtina.com/wp-json/wp/v2/posts/42202?context=edit",
                    headers=api_h, verify=False, timeout=30)
raw = r_db.json()["content"]["raw"]
print(f"DB raw SVG count: {raw.count(TARGET)} (length: {len(raw)})")
if raw.count(TARGET) == 0:
    print("ERROR: DB content has no SVGs — need to re-patch first")
    raise SystemExit(1)

# Touch the post to invalidate Batcache (PATCH with same content)
print("Touching post to invalidate Batcache...")
resp = requests.patch(
    "https://virtina.com/wp-json/wp/v2/posts/42202",
    json={"content": raw},  # same content, just triggers cache invalidation
    headers=api_h, verify=False, timeout=60,
)
print(f"PATCH status: {resp.status_code}")

# Wait 2 seconds for cache to propagate
print("Waiting 3 seconds...")
time.sleep(3)

# Now fetch the live page — this should trigger Batcache-Set from fresh content
print("Fetching live page to prime Batcache...")
r_live = requests.get(
    "https://virtina.com/woocommerce-b2b-customer-portal/",
    headers=pg_h, verify=False, timeout=30,
)
live_svg = r_live.text.count(TARGET)
cache_header = r_live.headers.get("X-nananana", "unknown")
lm = r_live.headers.get("Last-Modified", "unknown")
print(f"Live page SVG count: {live_svg}")
print(f"Cache: {cache_header}, Last-Modified: {lm}")

if live_svg > 0:
    print("SUCCESS: SVG arrows are now live!")
else:
    print("STILL MISSING — fetching once more after brief delay...")
    time.sleep(5)
    r_live2 = requests.get(
        "https://virtina.com/woocommerce-b2b-customer-portal/",
        headers=pg_h, verify=False, timeout=30,
    )
    svg2 = r_live2.text.count(TARGET)
    cache2 = r_live2.headers.get("X-nananana", "unknown")
    print(f"Second fetch SVG count: {svg2}, Cache: {cache2}")
