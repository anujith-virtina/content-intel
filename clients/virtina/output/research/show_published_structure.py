"""Show published content structure: first 12000 chars around Image 1."""
import os, re, requests, urllib3
from dotenv import load_dotenv
urllib3.disable_warnings()
load_dotenv()

resp = requests.get(
    "https://virtina.com/wp-json/wp/v2/posts/42297?context=edit",
    auth=(os.getenv("WP_USERNAME"), os.getenv("WP_APP_PASSWORD")),
    verify=False
)
raw = resp.json()["content"]["raw"]

# Show the 2000 chars around Image 1
idx = raw.find("A-warehouse")
print("=== 1500 chars BEFORE warehouse image ===")
print(raw[max(0, idx-1500):idx])
print("\n=== warehouse image + 500 chars AFTER ===")
end = raw.find("</span></p>", idx) + len("</span></p>")
print(raw[idx-50:end+500])
