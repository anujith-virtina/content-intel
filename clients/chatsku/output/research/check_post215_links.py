import os, re, requests, urllib3
from dotenv import load_dotenv

urllib3.disable_warnings()
load_dotenv()

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
resp = requests.get(
    "https://chatsku.com/wp-json/wp/v2/posts/215?context=edit",
    auth=(os.getenv("CHATSKU_WP_USERNAME"), os.getenv("CHATSKU_WP_APP_PASSWORD")),
    verify=False,
    headers=UA
)
print("HTTP", resp.status_code)
d = resp.json()
print("status:", d.get("status"))
print("title:", d.get("title", {}).get("rendered", ""))
raw = d.get("content", {}).get("raw", "")
print(f"raw chars: {len(raw)}")

# Save raw for inspection
with open(r"C:\content-intel\clients\chatsku\output\research\_post215_raw.txt", "w", encoding="utf-8") as f:
    f.write(raw)
print("Saved raw content")

# Check all links
links = re.findall(r'href=["\']([^"\']+)["\']', raw)
print("\nAll links in content:")
for l in sorted(set(links)):
    print(f"  {l}")

target = "pdf-catalog-chatbot"
print()
if target in raw:
    print("TARGET LINK ALREADY PRESENT — do not add again")
    # Show context
    idx = raw.find(target)
    print(f"Context: ...{raw[max(0,idx-100):idx+100]}...")
else:
    print("TARGET LINK NOT FOUND — need to add interlink")
