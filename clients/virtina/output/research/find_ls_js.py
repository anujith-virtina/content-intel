import re
html = open("tve_lightspeed_page.html", encoding="utf-8").read()
# Find lightspeed JS files
matches = re.findall(r"src=[\"'](https://virtina\.com[^\"']*lightspeed[^\"']*\.js[^\"']*)[\"']", html, re.I)
for m in matches:
    print("LIGHTSPEED JS:", m)
# Also find toggle-lightspeed references in scripts
scripts = re.findall(r"<script[^>]*>(.*?)</script>", html, re.DOTALL)
for i, s in enumerate(scripts):
    if "toggle-lightspeed" in s or "is_enabled" in s or "toggle_lightspeed" in s:
        print(f"\nScript {i} with toggle-lightspeed:")
        print(s[:1000])
