import re

with open(r"C:\content-intel\clients\virtina\output\research\_42297_fixed.txt", encoding="utf-8") as f:
    content = f.read()

print("=== TABLE OF CONTENTS (links in order) ===")
toc_section = content[:4000]
toc_entries = re.findall(r'href="(#[^"]+)"[^>]*color:#00a0e2[^>]*>([^<]+)', toc_section)
for i, (anchor, text) in enumerate(toc_entries, 1):
    print(f"  {i:2}. {anchor}")

print()
print("=== ACTUAL SECTION ORDER (h2 id= in document) ===")
sections = re.findall(r'<h2[^>]*\bid="([^"]+)"[^>]*>(.*?)</h2>', content, re.DOTALL)
for i, (sid, text) in enumerate(sections, 1):
    clean = re.sub(r'<[^>]+>', '', text).strip()
    print(f"  {i:2}. #{sid}  ({clean[:60]})")
