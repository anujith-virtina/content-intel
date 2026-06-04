import re
with open(r'C:\content-intel\clients\virtina\output\drafts\ecommerce-platform-seo-b2b-guide-2026-06-03.html', encoding='utf-8') as f:
    html = f.read()

tokens = []
for m in re.finditer(r'<h2[^>]+id="([^"]+)"[^>]*>([^<]+)', html):
    tokens.append(('H2', m.start(), m.group(1), m.group(2).strip()[:55]))
# alt comes before data-id in Template G
for m in re.finditer(r'alt="([^"]+)"[^>]*data-id="(\d+)"', html):
    tokens.append(('IMG', m.start(), m.group(2), m.group(1)[:65]))

tokens.sort(key=lambda x: x[1])
print("=== Document order: H2 sections and images ===")
for kind, pos, id_, text in tokens:
    prefix = "  [IMG]" if kind == "IMG" else "[H2] "
    print(f"{prefix} id={id_:<8} {text}")
