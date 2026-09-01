"""Probe Thrive Lightspeed API to find valid keys and storage location."""
import os, sys, requests, base64, urllib3, json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h = {"Authorization": f"Basic {token}",
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
     "Content-Type": "application/json"}
BASE = "https://virtina.com/wp-json/tcb/v1"

# Get full OPTIONS to see the key enum
print("=== Full OPTIONS /lightspeed/options ===")
r = requests.options(f"{BASE}/lightspeed/options", headers=h, verify=False, timeout=10)
data = r.json()
print(json.dumps(data, indent=2)[:2000])

# Get full OPTIONS /lightspeed/analyze to see its args
print("\n=== Full OPTIONS /lightspeed/analyze ===")
r2 = requests.options(f"{BASE}/lightspeed/analyze", headers=h, verify=False, timeout=10)
data2 = r2.json()
print(json.dumps(data2, indent=2)[:2000])

# Try the WP admin ajax to clear Thrive cache (bypass REST)
print("\n=== WP Admin AJAX - try tcb clear cache ===")
ajax_h = {"Authorization": f"Basic {token}",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
          "Content-Type": "application/x-www-form-urlencoded"}
ajax_payloads = [
    "action=tcb_clear_lightspeed&post_id=42202",
    "action=thrv_clear_cache&post_id=42202",
    "action=tcb_lightspeed_deoptimize&post_id=42202",
]
for payload in ajax_payloads:
    r3 = requests.post("https://virtina.com/wp-admin/admin-ajax.php",
                       data=payload, headers=ajax_h, verify=False, timeout=20)
    print(f"  {payload[:40]} -> {r3.status_code}: {r3.text[:100]}")
