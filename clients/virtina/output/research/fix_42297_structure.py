"""
Structural revision of post 42297 to match LLM-optimized blog format.
Additions:
  1. Quick Answer block (before Summary)
  2. "Best for" + key bullets inside each Model A/B/C subsection
  3. Real-World Scenarios section (3 concrete scenarios)
  4. Common Mistakes section (4 mistakes)
  5. Key Takeaways table (after FAQ, before author bio)
  6. TOC updated with real-world-scenarios + common-mistakes anchors
"""
import os, sys, re, requests, urllib3
from dotenv import load_dotenv

urllib3.disable_warnings()
load_dotenv()

WP_BASE = "https://virtina.com"
WP_USER = os.getenv("WP_USERNAME")
WP_PASS = os.getenv("WP_APP_PASSWORD")
POST_ID = 42297

orig_put = requests.put
requests.put = lambda *a, **kw: orig_put(*a, **{**kw, "verify": False})
orig_get = requests.get
requests.get = lambda *a, **kw: orig_get(*a, **{**kw, "verify": False})

with open(r"C:\content-intel\clients\virtina\output\research\_42297_fixed.txt", encoding="utf-8") as f:
    content = f.read()
print(f"Loaded {len(content)} chars")

# ── SHARED TEMPLATES ───────────────────────────────────────────────────────────
def toc_li(anchor, text):
    return (
        '<li style="list-style:none!important;padding:8px 0 8px 32px!important;'
        'position:relative!important;line-height:1.5!important;margin:0!important;">'
        '<span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;">'
        '<svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg">'
        '<path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span>'
        f'<a href="#{anchor}" style="color:#00a0e2!important;text-decoration:none!important;'
        f'font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">{text}</a></li>'
    )

def bullet_li(text):
    return (
        '<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;">'
        '<span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;'
        'border-radius:50%;display:inline-block;"></span>'
        f'<span style="font-size:16px;line-height:1.75;color:#2d3e50;">{text}</span></li>'
    )

def bullet_ul(items):
    lis = "\n".join(bullet_li(i) for i in items)
    return f'<ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;">\n{lis}\n</ul>'

def p(text, color="#2d3e50"):
    style = f'font-size:16px;line-height:1.75;{"color:"+color+";" if color != "#2d3e50" else ""}'
    return f'<p dir="ltr" style="{style}">{text}</p>'

def h3(text):
    return f'<h3 style="color:#43627f;font-size:22px;">{text}</h3>'

def section_div(content_inner):
    return (
        '<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));'
        'border-radius:20px;padding:30px;margin:0 0 28px 0;">'
        f'{content_inner}</div>'
    )

applied = 0

# ═══════════════════════════════════════════════════════════════════════════════
# 1. QUICK ANSWER BLOCK — insert before Summary div
# ═══════════════════════════════════════════════════════════════════════════════
QUICK_ANSWER = (
    '<div style="background:linear-gradient(rgba(0,213,192,0.28),rgba(0,213,192,0.28));'
    'border-radius:20px;padding:30px;margin:0 0 28px 0;">'
    '<h2 style="color:#43627f;font-size:30px;">Quick answer</h2>\n'
    + p('WooCommerce does not include net payment terms natively. '
        'You need one of three implementation models to add them.')
    + '\n'
    + bullet_ul([
        '<strong>Model A: Plugin-based</strong> — best for small wholesalers with a known buyer base and fewer than 50 net terms orders per month',
        '<strong>Model B: Financed net terms</strong> — best for high-volume stores that need zero credit risk and same-day payment',
        '<strong>Model C: PO gateway plus ERP</strong> — best for manufacturers whose enterprise buyers operate on formal purchase order cycles',
    ])
    + '\n'
    + p('Your choice depends on monthly order volume, whether you run an ERP, and how much credit risk your cash flow can carry.')
    + '\n</div>\n\n'
)

SUMMARY_ANCHOR = '<div style="background:linear-gradient(rgba(0,213,192,0.28),rgba(0,213,192,0.28));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 dir="ltr" style="color:#43627f;font-size:30px;">Summary</h2>'

if SUMMARY_ANCHOR in content:
    content = content.replace(SUMMARY_ANCHOR, QUICK_ANSWER + SUMMARY_ANCHOR, 1)
    print("  APPLIED: Quick Answer block inserted before Summary")
    applied += 1
else:
    print("  MISS:    Quick Answer — Summary anchor not found")

# ═══════════════════════════════════════════════════════════════════════════════
# 2a. "BEST FOR" BULLETS — Model A
# ═══════════════════════════════════════════════════════════════════════════════
MODEL_A_BULLETS = (
    '\n\n'
    + '<p dir="ltr" style="font-size:16px;line-height:1.75;"><strong>Best for:</strong></p>\n'
    + bullet_ul([
        'Small wholesalers with a known, repeat buyer base',
        'Stores under 50 net terms orders per month',
        'Operations with no ERP that want a fast, low-cost start',
    ])
    + '\n<p dir="ltr" style="font-size:16px;line-height:1.75;"><strong>Trade-offs:</strong></p>\n'
    + bullet_ul([
        'Seller carries all credit risk',
        'No automated credit underwriting',
        'Manual AR tracking breaks down above 50 orders per month',
    ])
)

MODEL_A_ANCHOR = 'There is no automated credit underwriting, and the seller carries all credit risk.</p>\n\n<h3 style="color:#43627f;font-size:22px;">Model B: Financed net terms</h3>'

if MODEL_A_ANCHOR in content:
    content = content.replace(
        MODEL_A_ANCHOR,
        'There is no automated credit underwriting, and the seller carries all credit risk.</p>'
        + MODEL_A_BULLETS
        + '\n\n<h3 style="color:#43627f;font-size:22px;">Model B: Financed net terms</h3>',
        1
    )
    print("  APPLIED: Model A Best-for + Trade-offs bullets")
    applied += 1
else:
    print("  MISS:    Model A bullets anchor")

# ═══════════════════════════════════════════════════════════════════════════════
# 2b. "BEST FOR" BULLETS — Model B
# ═══════════════════════════════════════════════════════════════════════════════
MODEL_B_BULLETS = (
    '\n\n'
    + '<p dir="ltr" style="font-size:16px;line-height:1.75;"><strong>Best for:</strong></p>\n'
    + bullet_ul([
        'High-volume distributors where cash flow is a constraint',
        'Stores acquiring new buyers with no payment history',
        'Operations that want zero credit risk and same-day payment',
    ])
    + '\n<p dir="ltr" style="font-size:16px;line-height:1.75;"><strong>Trade-offs:</strong></p>\n'
    + bullet_ul([
        '1-3% transaction fee on every net terms order',
        'Platform handles the buyer relationship on the payment side',
        'Reconciliation step required on the platform side',
    ])
)

MODEL_B_ANCHOR = 'The cost is 1-3% per transaction, and platforms like Resolve Pay and Balance offer WooCommerce integrations for this model.</p>\n\n<h3 style="color:#43627f;font-size:22px;">Model C: PO gateway plus ERP integration</h3>'

if MODEL_B_ANCHOR in content:
    content = content.replace(
        MODEL_B_ANCHOR,
        'The cost is 1-3% per transaction, and platforms like Resolve Pay and Balance offer WooCommerce integrations for this model.</p>'
        + MODEL_B_BULLETS
        + '\n\n<h3 style="color:#43627f;font-size:22px;">Model C: PO gateway plus ERP integration</h3>',
        1
    )
    print("  APPLIED: Model B Best-for + Trade-offs bullets")
    applied += 1
else:
    print("  MISS:    Model B bullets anchor")

# ═══════════════════════════════════════════════════════════════════════════════
# 2c. "BEST FOR" BULLETS — Model C
# ═══════════════════════════════════════════════════════════════════════════════
MODEL_C_BULLETS = (
    '\n\n'
    + '<p dir="ltr" style="font-size:16px;line-height:1.75;"><strong>Best for:</strong></p>\n'
    + bullet_ul([
        'Manufacturers with an existing ERP (SAP, NetSuite, Acumatica)',
        'Enterprise buyers who require a PO number field at checkout',
        'Operations that need WooCommerce orders to enter their AR workflow automatically',
    ])
    + '\n<p dir="ltr" style="font-size:16px;line-height:1.75;"><strong>Trade-offs:</strong></p>\n'
    + bullet_ul([
        'Highest setup complexity and longest time to deploy (4-12 weeks)',
        'ERP connector development required',
        'Seller still carries credit risk',
    ])
)

MODEL_C_ANCHOR = "If you're running Model C, your net terms setup is only as good as your <a href=\"https://virtina.com/woocommerce-erp-integration/\" style=\"outline: none;\">WooCommerce ERP integration</a>.</p>\n\n<p dir=\"ltr\" style=\"font-size:16px;line-height:1.75;\">The table below"

if MODEL_C_ANCHOR in content:
    content = content.replace(
        MODEL_C_ANCHOR,
        "If you're running Model C, your net terms setup is only as good as your <a href=\"https://virtina.com/woocommerce-erp-integration/\" style=\"outline: none;\">WooCommerce ERP integration</a>.</p>"
        + MODEL_C_BULLETS
        + '\n\n<p dir="ltr" style="font-size:16px;line-height:1.75;">The table below',
        1
    )
    print("  APPLIED: Model C Best-for + Trade-offs bullets")
    applied += 1
else:
    print("  MISS:    Model C bullets anchor")

# ═══════════════════════════════════════════════════════════════════════════════
# 3. REAL-WORLD SCENARIOS — insert after which-model div, before body3 image
# ═══════════════════════════════════════════════════════════════════════════════
SCENARIOS_SECTION = (
    '\n\n'
    + '<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));'
    'border-radius:20px;padding:30px;margin:0 0 28px 0;">'
    '<h2 id="real-world-scenarios" style="color:#43627f;font-size:30px;">Real-world scenarios: which model fits?</h2>\n'
    + p('Three operation types, three clear answers. Match your situation to the scenario below.')
    + '\n\n'
    + h3('Scenario 1: Small wholesale distributor, 20-40 B2B orders per month')
    + '\n'
    + p('<strong>Recommended model: Model A (plugin-based).</strong>')
    + '\n'
    + bullet_ul([
        'Order volume is low enough for manual credit approval',
        'Buyer base is known, so credit risk is predictable',
        'No ERP in place, so a plugin is the fastest and lowest-cost path',
        'Setup takes days, not weeks',
    ])
    + '\n\n'
    + h3('Scenario 2: High-volume distributor, 100+ net terms orders per month')
    + '\n'
    + p('<strong>Recommended model: Model B (financed net terms).</strong>')
    + '\n'
    + bullet_ul([
        'Manual credit tracking breaks down at this volume',
        'Cash flow cannot absorb risk across 100+ open invoices',
        'New buyer acquisition means approving accounts without payment history',
        'Platform pays you upfront, eliminating credit risk entirely',
    ])
    + '\n\n'
    + h3('Scenario 3: Manufacturer with SAP or NetSuite, enterprise buyers on formal PO cycles')
    + '\n'
    + p('<strong>Recommended model: Model C (PO gateway plus ERP integration).</strong>')
    + '\n'
    + bullet_ul([
        'Enterprise buyers require a PO number field at checkout',
        'AP departments need an invoice in a specific format',
        'WooCommerce orders must enter the ERP AR workflow automatically',
        'ERP already holds the customer credit record',
    ])
    + '\n</div>'
)

# Insert after closing </div> of which-model-fits-manufacturers, before body3 image span
SCENARIOS_ANCHOR = '</div>\n\n<span style="display:block;margin:20px 0;"><img alt="Office team reviewing ERP integration plans'

if SCENARIOS_ANCHOR in content:
    content = content.replace(
        SCENARIOS_ANCHOR,
        '</div>'
        + SCENARIOS_SECTION
        + '\n\n<span style="display:block;margin:20px 0;"><img alt="Office team reviewing ERP integration plans',
        1
    )
    print("  APPLIED: Real-World Scenarios section inserted")
    applied += 1
else:
    print("  MISS:    Scenarios anchor not found")

# ═══════════════════════════════════════════════════════════════════════════════
# 4. COMMON MISTAKES — insert before PAA div
# ═══════════════════════════════════════════════════════════════════════════════
MISTAKES_SECTION = (
    '<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));'
    'border-radius:20px;padding:30px;margin:0 0 28px 0;">'
    '<h2 id="common-mistakes" style="color:#43627f;font-size:30px;">Common mistakes when setting up net terms</h2>\n'
    + p('Most implementation problems are predictable. These four mistakes appear in almost every first deployment.')
    + '\n\n'
    + h3('1. Opening net terms to all buyers without approval')
    + '\n'
    + p('Net terms must be gated to approved accounts. '
        'Unrestricted access exposes you to credit risk from buyers with no payment history.')
    + '\n\n'
    + h3('2. Setting no per-account credit limits')
    + '\n'
    + p('Without a credit limit per account, a single buyer can accumulate more open balance than your cash flow can absorb. '
        'Set conservative limits before the first order, not after the first overdue invoice.')
    + '\n\n'
    + h3('3. Skipping dunning sequence configuration')
    + '\n'
    + p('Most stores go live with net terms and skip dunning setup. '
        'The first overdue invoice reveals the gap, usually 45 days after it was preventable. '
        'Configure your escalation sequence before the first order ships.')
    + '\n\n'
    + h3('4. Going live before completing an end-to-end test')
    + '\n'
    + p('Complete one full test order as an approved buyer-role account before launch. '
        'Confirm the net terms option appears, the PO field works, the invoice sends, and the ERP syncs if applicable.')
    + '\n</div>\n\n'
)

PAA_ANCHOR = '<div style="background:linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="people-also-ask"'

if PAA_ANCHOR in content:
    content = content.replace(PAA_ANCHOR, MISTAKES_SECTION + PAA_ANCHOR, 1)
    print("  APPLIED: Common Mistakes section inserted before PAA")
    applied += 1
else:
    print("  MISS:    Common Mistakes — PAA anchor not found")

# ═══════════════════════════════════════════════════════════════════════════════
# 5. KEY TAKEAWAYS TABLE — insert after last FAQ div, before author bio
# ═══════════════════════════════════════════════════════════════════════════════
KEY_TAKEAWAYS = (
    '\n\n'
    '<h2 id="key-takeaways" style="color:#43627f;font-size:30px;">Key takeaways</h2>\n'
    '<table data-rows="6" data-cols="3" data-v="middle" style="width:100%;border-collapse:collapse;margin:16px 0;">\n'
    '<thead>\n<tr>\n'
    '<th data-direction="" style="background:#43627f;color:#ffffff;padding:10px 14px;text-align:left;font-weight:600;"><p style="font-size:16px;line-height:1.75;"><strong>Your situation</strong></p></th>\n'
    '<th data-direction="" style="background:#43627f;color:#ffffff;padding:10px 14px;text-align:left;font-weight:600;"><p style="font-size:16px;line-height:1.75;"><strong>Monthly volume</strong></p></th>\n'
    '<th data-direction="" style="background:#43627f;color:#ffffff;padding:10px 14px;text-align:left;font-weight:600;"><p style="font-size:16px;line-height:1.75;"><strong>Recommended model</strong></p></th>\n'
    '</tr>\n</thead>\n<tbody>\n'
    '<tr>\n'
    '<td data-th="Your situation" style="background:#f4f6f9;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="font-size:16px;line-height:1.75;">Small wholesaler, known buyer base, no ERP</p></td>\n'
    '<td data-th="Monthly volume" style="background:#f4f6f9;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="font-size:16px;line-height:1.75;">Under 50 orders</p></td>\n'
    '<td data-th="Recommended model" style="background:#f4f6f9;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="font-size:16px;line-height:1.75;">Model A: Plugin-based</p></td>\n'
    '</tr>\n'
    '<tr>\n'
    '<td data-th="Your situation" style="background:#ffffff;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="font-size:16px;line-height:1.75;">High-volume store, cash flow priority</p></td>\n'
    '<td data-th="Monthly volume" style="background:#ffffff;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="font-size:16px;line-height:1.75;">100+ orders</p></td>\n'
    '<td data-th="Recommended model" style="background:#ffffff;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="font-size:16px;line-height:1.75;">Model B: Financed net terms</p></td>\n'
    '</tr>\n'
    '<tr>\n'
    '<td data-th="Your situation" style="background:#f4f6f9;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="font-size:16px;line-height:1.75;">Manufacturer with ERP, enterprise PO buyers</p></td>\n'
    '<td data-th="Monthly volume" style="background:#f4f6f9;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="font-size:16px;line-height:1.75;">Any</p></td>\n'
    '<td data-th="Recommended model" style="background:#f4f6f9;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="font-size:16px;line-height:1.75;">Model C: PO gateway plus ERP</p></td>\n'
    '</tr>\n'
    '<tr>\n'
    '<td data-th="Your situation" style="background:#ffffff;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="font-size:16px;line-height:1.75;">New B2B buyers, no payment history</p></td>\n'
    '<td data-th="Monthly volume" style="background:#ffffff;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="font-size:16px;line-height:1.75;">Any</p></td>\n'
    '<td data-th="Recommended model" style="background:#ffffff;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="font-size:16px;line-height:1.75;">Model B (new buyers) + Model A (returning accounts)</p></td>\n'
    '</tr>\n'
    '<tr>\n'
    '<td data-th="Your situation" style="background:#f4f6f9;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="font-size:16px;line-height:1.75;">Store growing from 50 to 100+ orders</p></td>\n'
    '<td data-th="Monthly volume" style="background:#f4f6f9;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="font-size:16px;line-height:1.75;">50-100 orders</p></td>\n'
    '<td data-th="Recommended model" style="background:#f4f6f9;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="font-size:16px;line-height:1.75;">Migrate from Model A to Model B</p></td>\n'
    '</tr>\n'
    '</tbody>\n</table>\n'
)

AUTHOR_BIO_ANCHOR = '<p dir="ltr" style="font-size:16px;line-height:1.75;"><strong>The Virtina Team'

if AUTHOR_BIO_ANCHOR in content:
    content = content.replace(AUTHOR_BIO_ANCHOR, KEY_TAKEAWAYS + AUTHOR_BIO_ANCHOR, 1)
    print("  APPLIED: Key Takeaways table inserted before author bio")
    applied += 1
else:
    print("  MISS:    Key Takeaways — author bio anchor not found")

# ═══════════════════════════════════════════════════════════════════════════════
# 6. TOC — add new section entries
# ═══════════════════════════════════════════════════════════════════════════════

# Add real-world-scenarios after which-model-fits-manufacturers TOC entry
TOC_WHICH_MODEL = toc_li("which-model-fits-manufacturers", "Which net terms model fits a manufacturer or distributor?")
TOC_SCENARIOS = toc_li("real-world-scenarios", "Real-world scenarios: which model fits?")

if TOC_WHICH_MODEL in content:
    content = content.replace(
        TOC_WHICH_MODEL,
        TOC_WHICH_MODEL + '\n' + TOC_SCENARIOS,
        1
    )
    print("  APPLIED: TOC entry for real-world-scenarios added")
    applied += 1
else:
    print("  MISS:    TOC which-model entry not found")

# Add common-mistakes before people-also-ask TOC entry
TOC_BEFORE_YOU_GO_LIVE = toc_li("before-you-go-live", "What should you have before going live with net terms?")
TOC_MISTAKES = toc_li("common-mistakes", "Common mistakes when setting up net terms")

if TOC_BEFORE_YOU_GO_LIVE in content:
    content = content.replace(
        TOC_BEFORE_YOU_GO_LIVE,
        TOC_BEFORE_YOU_GO_LIVE + '\n' + TOC_MISTAKES,
        1
    )
    print("  APPLIED: TOC entry for common-mistakes added")
    applied += 1
else:
    print("  MISS:    TOC before-you-go-live entry not found")

# Add key-takeaways entry at end of TOC (before the faq entry)
TOC_FAQ = toc_li("faq", "Frequently asked questions")
TOC_KEY_TAKEAWAYS = toc_li("key-takeaways", "Key takeaways")

if TOC_FAQ in content:
    content = content.replace(
        TOC_FAQ,
        TOC_KEY_TAKEAWAYS + '\n' + TOC_FAQ,
        1
    )
    print("  APPLIED: TOC entry for key-takeaways added")
    applied += 1
else:
    print("  MISS:    TOC faq entry not found")

print(f"\n{applied}/9 structural additions applied")

# ── FINAL CHECK ────────────────────────────────────────────────────────────────
print("\n[STRUCTURAL CHECK]")
structural = {
    "Quick Answer block": 'id="quick-answer"' in content or 'Quick answer' in content,
    "Model A Best-for bullets": 'Best for:</strong></p>' in content,
    "Real-World Scenarios H2": 'id="real-world-scenarios"' in content,
    "Scenario 1 (Model A rec)": 'Scenario 1' in content,
    "Scenario 2 (Model B rec)": 'Scenario 2' in content,
    "Scenario 3 (Model C rec)": 'Scenario 3' in content,
    "Common Mistakes H2": 'id="common-mistakes"' in content,
    "Key Takeaways table": 'id="key-takeaways"' in content,
    "TOC real-world-scenarios": 'real-world-scenarios' in content,
    "TOC common-mistakes": 'common-mistakes' in content,
    "TOC key-takeaways": 'key-takeaways' in content,
    "FAQ 7+ items": len(re.findall(r'class="vfaq"', content)) >= 7,
    "Comparison table": bool(re.search(r'<table\b', content)),
    "Infographic": 'infographic' in content.lower(),
    "No em dash": '—' not in content,
}
all_pass = True
for k, v in structural.items():
    s = "PASS" if v else "FAIL"
    if not v:
        all_pass = False
    print(f"  [{s}] {k}")

# ── SAVE + PUT ─────────────────────────────────────────────────────────────────
with open(r"C:\content-intel\clients\virtina\output\research\_42297_fixed.txt", "w", encoding="utf-8") as f:
    f.write(content)
print(f"\nSaved ({len(content)} chars)")

print(f"PUTting to post {POST_ID}...")
resp = requests.put(
    f"{WP_BASE}/wp-json/wp/v2/posts/{POST_ID}",
    auth=(WP_USER, WP_PASS),
    json={"content": content, "status": "draft"}
)
print(f"HTTP {resp.status_code}")
if resp.status_code in (200, 201):
    print(f"Modified: {resp.json().get('modified','')}")
    print("DONE")
else:
    print("ERROR:", resp.text[:400])
    sys.exit(1)
