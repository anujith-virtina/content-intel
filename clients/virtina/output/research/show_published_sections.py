"""Show all H2 sections and div boxes in published post to understand full structure."""
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
print(f"Published raw: {len(raw)} chars\n")

# Show all H2 sections in order
print("=== ALL H2 SECTIONS ===")
for m in re.finditer(r'<h2[^>]*>(.*?)</h2>', raw, re.DOTALL):
    pos  = m.start()
    text = re.sub(r'<[^>]+>', '', m.group(1)).strip()[:60]
    print(f"  char {pos:5}: {text}")

print("\n=== ALL COLORED SECTION DIVs ===")
for m in re.finditer(r'<div[^>]*style="[^"]*(?:linear-gradient|background:#)[^"]*"[^>]*>', raw):
    pos = m.start()
    bg  = re.search(r'background:[^;"]+', m.group())
    print(f"  char {pos:5}: {bg.group()[:60] if bg else '?'}")

print("\n=== ALL IMAGES ===")
for i, m in enumerate(re.finditer(r'<img[^>]+>', raw, re.DOTALL), 1):
    pos = m.start()
    src = re.search(r'src="([^"]+)"', m.group())
    w   = re.search(r'width="([^"]+)"', m.group())
    print(f"  char {pos:5}: {src.group(1).split('/')[-1][:50] if src else '?'} [{w.group(1) if w else '?'}px]")
