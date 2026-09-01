"""Read the Thrive lightspeed.min.js to find the toggle action and key name."""
import requests, urllib3, re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://virtina.com/wp-content/plugins/thrive-visual-editor/admin/assets/js/lightspeed.min.js?ver=10.8.10.1"
r = requests.get(url, verify=False, timeout=20,
                 headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
print(f"JS file: {r.status_code}, {len(r.text)} chars")
js = r.text

# Find toggle/enable/disable logic
for keyword in ["toggle-lightspeed", "is_enabled", "toggle_lightspeed",
                "enable", "options", "key", "value", "route"]:
    idxs = [m.start() for m in re.finditer(keyword, js)]
    if idxs:
        print(f"\n'{keyword}' at {len(idxs)} locations. First context:")
        idx = idxs[0]
        print(js[max(0,idx-100):idx+200])
        print("---")

# Save full JS for inspection
with open("lightspeed.min.js", "w", encoding="utf-8") as f:
    f.write(js)
print("\nSaved to lightspeed.min.js")
