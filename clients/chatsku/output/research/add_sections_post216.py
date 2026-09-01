"""Add Executive Summary, Introduction, and FAQ sections to ChatSKU post 216."""
import os, json, random, requests, base64, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WP_URL = "https://chatsku.com/wp-json/wp/v2"
USERNAME = os.environ.get("CHATSKU_WP_USERNAME", "")
APP_PASSWORD = os.environ.get("CHATSKU_WP_APP_PASSWORD", "")
token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
h = {"Authorization": f"Basic {token}", "User-Agent": UA, "Content-Type": "application/json"}

POST_ID = 216

def eid():
    return "".join(random.choices("0123456789abcdef", k=8))

# Load current Elementor data
data_path = os.path.join(os.path.dirname(__file__), "elementor_data_216.json")
with open(data_path, "r", encoding="utf-8") as f:
    sections = json.load(f)

assert sections[0]["id"] == "32b22297", f"Unexpected section[0] id: {sections[0]['id']}"
assert sections[-1]["id"] == "4abea811", f"Unexpected last section id: {sections[-1]['id']}"
print(f"Loaded {len(sections)} sections. First: {sections[0]['id']}, Last: {sections[-1]['id']}")

# Save original intro text (will move to Introduction section)
original_intro_html = sections[0]["elements"][0]["elements"][0]["settings"]["editor"]

# ── EXECUTIVE SUMMARY ────────────────────────────────────────────────────────
exec_summary_html = (
    "<p>B2B companies have invested heavily in digitizing their product catalogs. "
    "PDFs, web pages, downloadable spec sheets. The catalog exists. Buyers can technically access it. "
    "But having a catalog online and enabling buying through it are two different things, "
    "and the gap between them is where revenue quietly disappears.</p>"
    "<p>This post identifies ten specific catalog problems that cost manufacturers, distributors, "
    "and wholesalers sales every day. Problems that require nothing more than friction to trigger: "
    "a search that returns nothing, a spec that contradicts itself, a form that sits in an inbox "
    "for 48 hours, a question asked at 9pm with no one available to answer it.</p>"
    "<p>ChatSKU was built to close exactly this gap, by turning the catalog you already have into "
    "a live, conversational buying experience that deploys in a single line of code.</p>"
)

exec_heading_widget = {
    "id": eid(),
    "elType": "widget",
    "settings": {
        "title": "Executive summary",
        "align": "left",
        "title_color": "#1a1a2e",
        "typography_font_size": {"size": 26, "unit": "px"},
    },
    "elements": [],
    "widgetType": "heading",
}

exec_text_widget = {
    "id": eid(),
    "elType": "widget",
    "settings": {"editor": exec_summary_html},
    "elements": [],
    "widgetType": "text-editor",
}

# Replace section[0] column widgets with heading + exec summary text
sections[0]["elements"][0]["elements"] = [exec_heading_widget, exec_text_widget]

# ── INTRODUCTION ──────────────────────────────────────────────────────────────
intro_section = {
    "id": eid(),
    "elType": "section",
    "settings": {
        "background_background": "classic",
        "background_color": "#ffffff",
        "padding": {"top": "60", "bottom": "60", "unit": "px"},
    },
    "elements": [
        {
            "id": eid(),
            "elType": "column",
            "settings": {
                "_column_size": 100,
                "width": "100",
                "padding": {"top": "20", "bottom": "20", "left": "20", "right": "20", "unit": "px"},
            },
            "elements": [
                {
                    "id": eid(),
                    "elType": "widget",
                    "settings": {
                        "title": "Introduction",
                        "align": "left",
                        "title_color": "#1a1a2e",
                        "typography_font_size": {"size": 26, "unit": "px"},
                    },
                    "elements": [],
                    "widgetType": "heading",
                },
                {
                    "id": eid(),
                    "elType": "widget",
                    "settings": {"editor": original_intro_html},
                    "elements": [],
                    "widgetType": "text-editor",
                },
            ],
            "isInner": False,
        }
    ],
    "isInner": False,
}

# Insert Introduction at index 1 (right after exec summary)
sections.insert(1, intro_section)

# ── FAQ ───────────────────────────────────────────────────────────────────────
faq_items = [
    (
        "What is ChatSKU and how does it work?",
        "ChatSKU is a catalog intelligence platform that converts your existing product catalog "
        "into a conversational buying interface. Buyers interact with it through a chat widget "
        "embedded on your website. They can search in plain language, ask compatibility questions, "
        "get spec clarifications, and submit quote requests, all without calling your sales team. "
        "The platform works with PDFs, CSVs, and existing product pages, with no database build or "
        "ERP integration required.",
    ),
    (
        "Do I need to rebuild my website or integrate with my ERP to deploy ChatSKU?",
        "No. ChatSKU deploys in a single line of embed code and works with the catalog you already "
        "have. There is no ERP integration, no database build, and no site rebuild required. Your "
        "existing product data, regardless of format, becomes the foundation.",
    ),
    (
        "What catalog formats does ChatSKU support?",
        "ChatSKU ingests PDFs, CSVs, product spreadsheets, and existing web-based product pages. "
        "For companies whose primary catalog is a PDF, this is particularly significant: a static "
        "document becomes an interactive buying experience without any manual re-keying of product data.",
    ),
    (
        "How does ChatSKU handle buyers who search using informal or industry-specific terminology?",
        "ChatSKU matches buyer intent against your product data, not just exact keywords. A buyer "
        "searching \"pump for chemical transfer\" will find the relevant product even if your catalog "
        "labels it \"centrifugal impeller unit, chemical grade.\" The system handles synonyms, "
        "abbreviations, legacy part numbers, and plain-language descriptions automatically.",
    ),
    (
        "Can ChatSKU replace our existing RFQ form?",
        "ChatSKU captures quote requests through the chat conversation itself. A buyer can find a "
        "product, confirm the spec, and submit a quote request in a single interaction, with full "
        "product context already attached. This replaces the blank RFQ form workflow that typically "
        "introduces 48-hour delays between buyer intent and vendor response.",
    ),
    (
        "How long does a typical ChatSKU deployment take?",
        "Most deployments are measured in days, not months. Unlike a full ecommerce implementation "
        "that can take 12 to 18 months and cost hundreds of thousands of dollars, ChatSKU requires "
        "only your existing catalog and a single embed code. There is no infrastructure build and "
        "no dedicated dev team required.",
    ),
    (
        "Is ChatSKU available to buyers outside standard business hours?",
        "Yes. ChatSKU operates around the clock. Buyers can search products, ask technical questions, "
        "and submit quote requests at any time without a human in the loop. This matters particularly "
        "for companies whose buyers operate across multiple time zones or make procurement decisions "
        "outside regular business hours.",
    ),
    (
        "What types of companies is ChatSKU designed for?",
        "ChatSKU is primarily built for B2B manufacturers, distributors, and wholesalers that have "
        "an existing product catalog and need to convert it into a buying experience. It is especially "
        "effective for companies managing large SKU counts, complex technical specifications, or buyer "
        "bases that expect self-service options without waiting for a sales rep.",
    ),
]

faq_html_parts = []
for question, answer in faq_items:
    faq_html_parts.append(
        f'<p><strong>{question}</strong></p><p>{answer}</p>'
    )
faq_html = "\n".join(faq_html_parts)

faq_section = {
    "id": eid(),
    "elType": "section",
    "settings": {
        "background_background": "classic",
        "background_color": "#f9f9fb",
        "padding": {"top": "60", "bottom": "60", "unit": "px"},
    },
    "elements": [
        {
            "id": eid(),
            "elType": "column",
            "settings": {
                "_column_size": 100,
                "width": "100",
                "padding": {"top": "20", "bottom": "20", "left": "20", "right": "20", "unit": "px"},
            },
            "elements": [
                {
                    "id": eid(),
                    "elType": "widget",
                    "settings": {
                        "title": "Frequently asked questions",
                        "align": "left",
                        "title_color": "#1a1a2e",
                        "typography_font_size": {"size": 26, "unit": "px"},
                    },
                    "elements": [],
                    "widgetType": "heading",
                },
                {
                    "id": eid(),
                    "elType": "widget",
                    "settings": {"editor": faq_html},
                    "elements": [],
                    "widgetType": "text-editor",
                },
            ],
            "isInner": False,
        }
    ],
    "isInner": False,
}

# Append FAQ at the very end
sections.append(faq_section)

print(f"New section count: {len(sections)}")
for i, s in enumerate(sections):
    heading = ""
    for col in s.get("elements", []):
        for w in col.get("elements", []):
            if w.get("widgetType") == "heading":
                heading = w.get("settings", {}).get("title", "")[:55]
                break
    print(f"  [{i}] bg={s.get('settings',{}).get('background_color','')} heading={heading}")

# Save modified data locally
out_path = os.path.join(os.path.dirname(__file__), "elementor_data_216_v2.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(sections, f, ensure_ascii=False)
print(f"\nSaved elementor_data_216_v2.json")

# ── PATCH WordPress ───────────────────────────────────────────────────────────
el_data_str = json.dumps(sections, ensure_ascii=False)
payload = {
    "meta": {
        "_elementor_data": el_data_str,
        "_elementor_edit_mode": "builder",
        "_elementor_template_type": "wp-post",
        "_elementor_version": "4.0.3",
    },
    "status": "publish",
}

print("\nPATCHing post 216...")
r = requests.patch(
    f"{WP_URL}/posts/{POST_ID}?context=edit",
    json=payload,
    headers=h,
    verify=False,
    timeout=120,
)
print(f"PATCH status: {r.status_code}")
if r.status_code == 200:
    post = r.json()
    print(f"  Post status: {post.get('status')}")
    meta = post.get("meta", {})
    saved_el = meta.get("_elementor_data", "")
    print(f"  _elementor_data length saved: {len(saved_el)}")
    try:
        saved_sections = json.loads(saved_el)
        print(f"  Sections in saved data: {len(saved_sections)}")
        for i, s in enumerate(saved_sections):
            heading = ""
            for col in s.get("elements", []):
                for w in col.get("elements", []):
                    if w.get("widgetType") == "heading":
                        heading = w.get("settings", {}).get("title", "")[:55]
                        break
            print(f"    [{i}] bg={s.get('settings',{}).get('background_color','')} heading={heading}")
    except Exception as e:
        print(f"  Parse error: {e}")
else:
    print(f"Error: {r.text[:600]}")
    raise SystemExit(1)

# ── Clear Elementor cache ─────────────────────────────────────────────────────
print("\nClearing Elementor cache...")
try:
    cr = requests.delete(
        "https://chatsku.com/wp-json/elementor/v1/cache",
        headers=h, verify=False, timeout=20,
    )
    print(f"Cache clear: {cr.status_code}")
except Exception as e:
    print(f"Cache clear error (non-fatal): {e}")

print("\nDone. Visit: https://chatsku.com/b2b-catalog-issues-costing-sales/")
