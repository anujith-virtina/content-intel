import os, requests, base64, re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

token = base64.b64encode(f"{os.environ['WP_USERNAME']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()
headers = {"Authorization": f"Basic {token}"}
r = requests.get("https://virtina.com/wp-json/wp/v2/posts/42202?_fields=content,status", headers=headers, verify=False)
data = r.json()
c = data["content"]["rendered"]

print("=== TABLE STYLES ===")
print("table width:100%       :", "width:100%;border-collapse" in c)
print("th slate header        :", "background:#43627f;color:#ffffff;padding:10px" in c)
print("td bg #f4f6f9          :", "background:#f4f6f9;padding:10px 14px;border-bottom" in c)
print("td bg #ffffff          :", "background:#ffffff;padding:10px 14px;border-bottom" in c)

print("\n=== H3 TAGS ===")
h3_tags = re.findall(r'<h3[^>]*>([^<]+)</h3>', c)
print(f"H3 count: {len(h3_tags)}")
for h in h3_tags:
    print(f"  - {h}")

print("\n=== FAQ ===")
faq_count = c.count('class="vfaq"')
print(f"FAQ accordion items: {faq_count}")
print("FAQ section present:", 'id="faq"' in c)

print("\n=== TOC faq entry ===")
print('TOC #faq link:', 'href="#faq"' in c)

print("\n=== PARAGRAPH COUNT ===")
paras = re.findall(r'<p[^>]*>(.+?)</p>', c, re.DOTALL)
print(f"Total paragraphs: {len(paras)}")
long_paras = [p for p in paras if len(re.sub(r'<[^>]+>', '', p)) > 250]
print(f"Paragraphs >250 chars (stripped): {len(long_paras)}")
if long_paras:
    for lp in long_paras[:3]:
        clean = re.sub(r'<[^>]+>', '', lp).strip()
        print(f"  [{len(clean)} chars] {clean[:120]}...")

print("\n=== STATUS ===")
print(f"Post status: {data['status']}")
print("DONE.")
