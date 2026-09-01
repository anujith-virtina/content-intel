# -*- coding: utf-8 -*-
"""Append People Also Ask + Conclusion + FAQ to existing ChatSKU post 1855.
Post 1855 is a PLAIN-HTML post (no Elementor data), so we append matching
plain HTML into the `content` field only. Preserves status/media/meta.
Dry-run by default; pass 'publish' to PUT.
"""
import os, sys, json, re, requests

U = os.environ["CHATSKU_WP_USERNAME"]
A = os.environ["CHATSKU_WP_APP_PASSWORD"]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
H = {"User-Agent": UA}
POST = 1855
SCRATCH = r"C:\Users\ASUS\AppData\Local\Temp\claude\C--content-intel\a2138730-61a8-4dd4-8f74-ba5ab9d92c6f\scratchpad"

# --- always re-fetch live content (never rely on cached copy for the write) ---
r = requests.get(f"https://chatsku.com/wp-json/wp/v2/posts/{POST}?context=edit", headers=H, auth=(U, A), timeout=60)
r.raise_for_status()
j = r.json()
content = j["content"]["raw"]
print("live content len:", len(content), "| status:", j["status"])

# guard: do not duplicate if sections already exist
low = content.lower()
for marker in ["people also ask", "frequently asked questions", ">conclusion<", "<h2>conclusion"]:
    if marker in low:
        print(f"WARNING: marker '{marker}' already present. Aborting to avoid duplication.")
        raise SystemExit(1)

# ---------- new sections (plain HTML, matches existing bare <h2>/<h3>/<p> style) ----------
PAA = [
    ("What is the response gap in B2B sales?",
     'The response gap is the delay between a buyer\'s request and your reply. In B2B it often runs 24 to 72 hours. By then, most buyers have already leaned toward the vendor who answered first. Here is a closer look at <a href="https://chatsku.com/what-is-the-response-gap/">the response gap</a>.'),
    ("How fast should you respond to a B2B quote request?",
     "Aim for under one hour on standard catalog items. A reply within 5 minutes makes you far more likely to win the deal. Wait 24 hours and your win rate flatlines."),
    ("Can you quote faster without hiring more salespeople?",
     'Yes. Most standard quotes follow set pricing and spec rules, so they can run on their own around the clock. Your team then spends its time only on the complex deals. That is the job of a <a href="https://chatsku.com/ai-sales-assistant-b2b-ecommerce/">B2B AI sales assistant</a>.'),
    ("What makes quoting so slow in manufacturing and distribution?",
     'The usual culprit is the "specialist bridge." A rep waits on an engineer for specs, then waits again for the right customer price. Move that knowledge into an AI layer and the wait disappears.'),
]

CONCL = [
    "The response gap is not a service problem. It is a revenue problem, and you can start fixing it this week.",
    "Every hour of silence gives your buyer a reason to choose someone else. Close the gap and you protect margin, win more RFQs, and grow sales without adding headcount.",
    "You do not need a rebuild to begin. ChatSKU turns your existing catalog into a round-the-clock quoting engine in about a day.",
]

FAQ = [
    ("How quickly can ChatSKU return a quote?",
     "In minutes, even at 2 AM. It reads your catalog, applies the buyer's pricing tier, checks stock, and sends a formal quote without waiting on a rep."),
    ("Does ChatSKU work with my existing catalog and pricing?",
     'Yes. It ingests PDFs, spreadsheets, and ERP exports, then applies customer-specific and tiered pricing on its own. See how it handles a <a href="https://chatsku.com/pdf-catalog-chatbot/">PDF catalog</a>.'),
    ("Will I need to rebuild my website?",
     "No. ChatSKU adds to your current site with a single line of code, and setup is usually under a day."),
    ("Which businesses is this built for?",
     'B2B manufacturers, distributors, and wholesalers with large or technical catalogs and customer-specific pricing. Here is the <a href="https://chatsku.com/for-b2b-manufacturers-distributors-and-wholesalers/">fit for manufacturers and distributors</a>.'),
    ("Is a faster quote really worth the change?",
     "Yes. Faster quotes lift win rates and repeat business, and they cut costly quoting errors. Each deal ends up worth more over time."),
    ('How is this different from a standard "request a quote" form?',
     "A form only collects a request and waits for a human. ChatSKU answers, prices, and quotes in the moment, so the buyer never leaves to shop elsewhere."),
]

def build_paa():
    out = "\n<hr>\n<h2>People also ask</h2>\n"
    for q, a in PAA:
        out += f"<h3>{q}</h3>\n<p>{a}</p>\n"
    return out

def build_concl():
    out = "\n<hr>\n<h2>Conclusion</h2>\n"
    for p in CONCL:
        out += f"<p>{p}</p>\n"
    out += ('<p style="text-align:center;margin-top:24px;">'
            '<a href="https://chatsku.com/demo/" style="display:inline-block;background:#e94560;'
            'color:#ffffff;padding:14px 30px;border-radius:6px;text-decoration:none;font-weight:600;">'
            'Book a ChatSKU demo</a></p>\n')
    return out

def build_faq():
    out = "\n<hr>\n<h2>Frequently asked questions</h2>\n"
    for q, a in FAQ:
        out += ('<details style="border:1px solid #e5e5ef;border-radius:8px;padding:12px 16px;margin:10px 0;">'
                f'<summary style="cursor:pointer;font-weight:600;color:#1a1a2e;">{q}</summary>'
                f'<p style="margin-top:10px;">{a}</p></details>\n')
    return out

new_html = build_paa() + build_concl() + build_faq()

# FAQPage JSON-LD (strip tags from answers for schema text)
def plain(t): return re.sub(r"<[^>]+>", "", t)
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in FAQ]}
faq_script = '<script type="application/ld+json">' + json.dumps(faq_ld) + "</script>"

# ---------- insert before last </div>, append FAQ schema after existing script ----------
idx = content.rindex("</div>")
new_content = content[:idx] + new_html + content[idx:] + "\n" + faq_script

# ---------- QA on the ADDITIONS only ----------
add_text = plain(new_html)
problems = []
if "—" in new_html or "&mdash;" in new_html:
    problems.append("em dash present")
banned = ["revolutionary","game-changing","cutting-edge","best-in-class","transform your",
          "delve","leverage","navigate","just a chatbot","ai-powered","in today's fast-paced world"]
for b in banned:
    if b in add_text.lower():
        problems.append(f"banned word: {b}")
# links in additions must be internal chatsku with no target
for m in re.finditer(r'<a href="([^"]+)"([^>]*)>', new_html):
    href, attrs = m.group(1), m.group(2)
    if "chatsku.com" not in href:
        problems.append(f"non-chatsku link: {href}")
    if "target=" in attrs:
        problems.append(f"internal link has target: {href}")
print("ADD QA problems:", problems or "NONE")
print("additions: PAA q=%d, FAQ q=%d, links=%d" % (len(PAA), len(FAQ), new_html.count("<a href")))
open(os.path.join(SCRATCH, "post1855_new_content.html"), "w", encoding="utf-8").write(new_content)
print("new total content len:", len(new_content))

if problems:
    print("ABORT: fix QA problems first."); raise SystemExit(1)
if "publish" not in sys.argv:
    print("DRY RUN. pass 'publish' to PUT."); raise SystemExit(0)

# ---------- PUT: content only (preserve status/media/meta) ----------
pr = requests.post(f"https://chatsku.com/wp-json/wp/v2/posts/{POST}",
                   headers=H, auth=(U, A), json={"content": new_content}, timeout=120)
print("PUT status:", pr.status_code)
if pr.status_code not in (200, 201):
    print(pr.text[:1500]); raise SystemExit(1)
res = pr.json()
print("updated id:", res["id"], "| status:", res["status"], "| link:", res.get("link"))
