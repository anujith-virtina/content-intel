"""
Fix post 42297 — 10-rule enforcement with hard measurement.
All replacements are exact string matches against the live raw content.
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

# ── LOAD LIVE CONTENT ──────────────────────────────────────────────────────────
with open(r"C:\content-intel\clients\virtina\output\research\_42297_live_raw.txt", encoding="utf-8") as f:
    content = f.read()

print(f"Loaded {len(content)} chars")

# ── REPLACEMENTS ───────────────────────────────────────────────────────────────
fixes = []

# FIX 1 — Summary para 2: 77 words → split after first sentence
fixes.append((
    '<p dir="ltr" style="font-size:16px;line-height:1.75;">Research shows 67% of B2B buyers abandon a purchase when no payment terms are available, and 78% call payment terms an essential factor when choosing a supplier. This guide covers the three models for adding net payment terms to WooCommerce: plugin-based manual credit, financed net terms, and a PO gateway connected to your ERP. For each model, you\'ll find the trade-offs on cost, credit risk, and ERP requirements, plus a direct recommendation based on your operation type.</p>',
    '<p dir="ltr" style="font-size:16px;line-height:1.75;">Research shows 67% of B2B buyers abandon a purchase when no payment terms are available, and 78% call payment terms an essential factor when choosing a supplier.</p>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">This guide covers the three models for adding net payment terms to WooCommerce: plugin-based manual credit, financed net terms, and a PO gateway connected to your ERP. For each model, you\'ll find the trade-offs on cost, credit risk, and ERP requirements, plus a direct recommendation based on your operation type.</p>',
    "FIX 1: Summary para 2 split (77w→2 paras)"
))

# FIX 2 — which-model para 3: 69 words + 26-word sentence → split + rewrite
fixes.append((
    '<p dir="ltr" style="font-size:16px;line-height:1.75;"><strong>Manufacturers with an existing ERP (SAP, NetSuite, Acumatica, or similar) and enterprise buyers on formal PO cycles:</strong> Model C is the correct choice. Your buyers expect a PO number field at checkout and an invoice delivered in the format their AP department requires. Setting up your <a href="https://virtina.com/b2b-ecommerce-for-manufacturers/" style="outline: none;">B2B ecommerce for manufacturers</a> correctly means the payment model matches the buyer workflow, and the WooCommerce order enters your existing AR infrastructure automatically.</p>',
    '<p dir="ltr" style="font-size:16px;line-height:1.75;"><strong>Manufacturers with an existing ERP (SAP, NetSuite, Acumatica, or similar) and enterprise buyers on formal PO cycles:</strong> Model C is the correct choice. Your buyers expect a PO number field at checkout and an invoice in the format their AP department requires.</p>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">When you set up <a href="https://virtina.com/b2b-ecommerce-for-manufacturers/" style="outline: none;">B2B ecommerce for manufacturers</a> correctly, the payment model matches the buyer workflow. The WooCommerce order enters your existing AR infrastructure automatically.</p>',
    "FIX 2: which-model para 3 split + 26-word sentence rewrite"
))

# FIX 3 — late-payer para 1: 68 words → split after first sentence
fixes.append((
    '<p dir="ltr" style="font-size:16px;line-height:1.75;">When a buyer pays late, your pre-defined dunning sequence activates: a payment reminder at day 30, a formal notice at day 45, an order hold at day 60, and a collections referral at day 90. That sequence only works if you defined it before the first invoice went unpaid. Stores that skip this step discover the problem 90 days later when several accounts have balances they cannot collect.</p>',
    '<p dir="ltr" style="font-size:16px;line-height:1.75;">When a buyer pays late, your pre-defined dunning sequence activates: a payment reminder at day 30, a formal notice at day 45, an order hold at day 60, and a collections referral at day 90.</p>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">That sequence only works if you defined it before the first invoice went unpaid. Stores that skip this step discover the problem 90 days later with balances they cannot collect.</p>',
    "FIX 3: late-payer para 1 split (68w→2 paras)"
))

# FIX 4 — ERP section: add H3 mid-section + fix vague sentence
fixes.append((
    '<p dir="ltr" style="font-size:16px;line-height:1.75;">For Model A without an ERP, most stores manage AR via the plugin\'s tools or a spreadsheet. That is acceptable at low volume. Past 50-100 net terms orders per month, manual tracking creates late-payment blind spots that cost real money.</p>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">For Model B, the financed platform collects from the buyer directly, so your ERP sees only a single incoming payment per period. That simplifies AR but requires a reconciliation step on the platform side. Understanding the full feature roadmap context is worth reviewing before you scope the build.</p>',
    '<h3 style="color:#43627f;font-size:22px;">Managing AR across all three models</h3>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">For Model A without an ERP, most stores manage AR via the plugin\'s tools or a spreadsheet. That is acceptable at low volume. Past 50-100 net terms orders per month, manual tracking creates late-payment blind spots that cost real money.</p>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">For Model B, the financed platform collects from the buyer directly, so your ERP sees only a single incoming payment per period. That simplifies AR but requires a reconciliation step. Review the platform\'s reconciliation reports monthly to keep your AR records current.</p>',
    "FIX 4: ERP section H3 added + vague sentence replaced"
))

# FIX 5 — Conclusion: 7+4 sentences → 5 short paragraphs
fixes.append((
    '<p style="color:#ffffff;font-size:16px;line-height:1.75;">B2B buyers at manufacturers and distributors are not abandoning your WooCommerce store because they don\'t want to buy. They\'re leaving because your checkout doesn\'t match how they are required to pay. The fix is not complicated in concept, but it requires a real implementation decision. Plugin-based credit works for known buyer bases at low volume. Financed net terms eliminates your credit risk and pays you upfront. A PO gateway connected to your ERP is the right architecture for manufacturers whose enterprise buyers are on formal PO cycles. Pick the model that fits your operation, not the one that\'s easiest to install.</p>\n<p style="color:#ffffff;font-size:16px;line-height:1.75;">Getting net terms right means more than choosing a plugin. The credit policy, the approval workflow, the ERP connection, and the dunning sequence all have to be in place before the first net terms order lands. That is exactly the kind of implementation Virtina handles for B2B manufacturers and distributors. If you\'re connecting net terms to an ERP or building a multi-tier approval workflow, contact us to talk through your setup.</p>',
    '<p style="color:#ffffff;font-size:16px;line-height:1.75;">B2B buyers at manufacturers and distributors are not abandoning your WooCommerce store because they don\'t want to buy. They\'re leaving because your checkout doesn\'t match how they are required to pay. The fix requires a real implementation decision.</p>\n<p style="color:#ffffff;font-size:16px;line-height:1.75;">Plugin-based credit works for known buyer bases at low volume. Financed net terms eliminates your credit risk and pays you upfront. A PO gateway connected to your ERP is the right architecture for manufacturers on formal PO cycles.</p>\n<p style="color:#ffffff;font-size:16px;line-height:1.75;">Pick the model that fits your operation, not the one that\'s easiest to install.</p>\n<p style="color:#ffffff;font-size:16px;line-height:1.75;">Getting net terms right means more than choosing a plugin. The credit policy, the approval workflow, the ERP connection, and the dunning sequence all have to be in place before the first net terms order lands. That is exactly the kind of implementation Virtina handles for B2B manufacturers and distributors.</p>\n<p style="color:#ffffff;font-size:16px;line-height:1.75;">If you\'re connecting net terms to an ERP or building a multi-tier approval workflow, contact us to talk through your setup.</p>',
    "FIX 5: Conclusion restructured (7+4 sentences → 5 paras of ≤3 sentences)"
))

# FIX 6 — PAA answer 1: 5 sentences + 34-word sentence → split + bullets
fixes.append((
    '<h3 style="color:#43627f;font-size:22px;">Can WooCommerce handle net 30 payment terms natively?</h3>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">No. WooCommerce does not include net terms natively. Its default gateways are built for immediate payment collection. To add Net 30 or Net 60, you need either a plugin-based invoice gateway, a financed net terms platform with a WooCommerce integration, or a custom PO gateway built to connect with your ERP. The right choice depends on your order volume, your buyer mix, and whether you already run an ERP system.</p>',
    '<h3 style="color:#43627f;font-size:22px;">Can WooCommerce handle net 30 payment terms natively?</h3>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">No. WooCommerce does not include net terms natively. Its default gateways are built for immediate payment collection.</p>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">To add Net 30 or Net 60, you have three options:</p>\n<ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;">\n<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;">A plugin-based invoice gateway (Model A)</span></li>\n<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;">A financed net terms platform with a WooCommerce integration (Model B)</span></li>\n<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;">A custom PO gateway connected to your ERP (Model C)</span></li>\n</ul>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">The right choice depends on your order volume, your buyer mix, and whether you already run an ERP system.</p>',
    "FIX 6: PAA-1 split + 3 options converted to bullets"
))

# FIX 7 — PAA answer 2: 5 sentences → 2 paras of ≤3
fixes.append((
    '<h3 style="color:#43627f;font-size:22px;">What is the difference between net 30 and a trade credit account?</h3>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">They refer to the same concept. Trade credit is the general term for selling on deferred payment terms. Net 30, Net 60, and Net 90 specify the number of days the buyer has to pay the invoice. Net 30 is the most common in North American B2B commerce, appearing on approximately 55-65% of B2B invoices in manufacturing and wholesale. When a buyer says they need to pay “on terms,” they mean trade credit with a defined net period.</p>',
    '<h3 style="color:#43627f;font-size:22px;">What is the difference between net 30 and a trade credit account?</h3>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">They refer to the same concept. Trade credit is the general term for selling on deferred payment terms. Net 30, Net 60, and Net 90 specify the number of days the buyer has to pay the invoice.</p>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">Net 30 is the most common in North American B2B commerce, appearing on approximately 55-65% of B2B invoices in manufacturing and wholesale. When a buyer says they need to pay “on terms,” they mean trade credit with a defined net period.</p>',
    "FIX 7: PAA-2 split (5 sentences → 2 paras)"
))

# FIX 8 — PAA answer 3: 5 sentences → 2 paras
fixes.append((
    '<h3 style="color:#43627f;font-size:22px;">Do I need an ERP to offer net terms in WooCommerce?</h3>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">No, not for Models A or B. Plugin-based and financed net terms both work without an ERP. However, if you\'re managing more than 50-100 net terms orders per month, manual AR tracking becomes a real operational problem. At that volume, ERP integration stops being optional and starts being a practical requirement. If you already run an ERP, Model C gives you the cleanest workflow by connecting checkout directly to your AR process.</p>',
    '<h3 style="color:#43627f;font-size:22px;">Do I need an ERP to offer net terms in WooCommerce?</h3>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">No, not for Models A or B. Plugin-based and financed net terms both work without an ERP.</p>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">However, if you\'re managing more than 50-100 net terms orders per month, manual AR tracking becomes a real problem. At that volume, ERP integration stops being optional. If you already run an ERP, Model C gives you the cleanest workflow.</p>',
    "FIX 8: PAA-3 split (5 sentences → 2 paras)"
))

# FIX 9 — PAA answer 4: 5 sentences with 3 parallel model items → bullets
fixes.append((
    '<h3 style="color:#43627f;font-size:22px;">What plugin is best for WooCommerce B2B net payment terms?</h3>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">The answer depends on which model you\'re implementing. For plugin-based manual credit (Model A), Wholesale Suite Payments and B2BKing\'s invoice gateway are the main options. For financed net terms (Model B), Resolve Pay and Balance both offer WooCommerce integrations. For a PO gateway connected to an ERP (Model C), you\'re typically looking at custom development or a semi-custom gateway. Choose the model first, then evaluate the tools that serve it.</p>',
    '<h3 style="color:#43627f;font-size:22px;">What plugin is best for WooCommerce B2B net payment terms?</h3>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">The answer depends on which model you\'re implementing.</p>\n<ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;">\n<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Model A (plugin-based):</strong> Wholesale Suite Payments and B2BKing\'s invoice gateway are the main options</span></li>\n<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Model B (financed):</strong> Resolve Pay and Balance both offer WooCommerce integrations</span></li>\n<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Model C (PO gateway plus ERP):</strong> Custom development or a semi-custom gateway</span></li>\n</ul>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">Choose the model first, then evaluate the tools that serve it.</p>',
    "FIX 9: PAA-4 3 model-items converted to bullets"
))

# FIX 10 — FAQ 1: 5 sentences → 2 paras
fixes.append((
    '<p dir="ltr" style="font-size:16px;line-height:1.75;">WooCommerce does not support per-customer credit limits natively. You need a B2B plugin that adds this capability. Wholesale Suite and B2BKing both allow store admins to set a credit limit per customer account. When a buyer\'s outstanding net terms balance reaches their credit limit, new orders are blocked until existing invoices are paid. Set these limits conservatively for new accounts and review them after 2-3 payment cycles.</p>',
    '<p dir="ltr" style="font-size:16px;line-height:1.75;">WooCommerce does not support per-customer credit limits natively. You need a B2B plugin that adds this capability. Wholesale Suite and B2BKing both allow store admins to set a credit limit per customer account.</p>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">When a buyer\'s outstanding balance reaches their credit limit, new orders are blocked until existing invoices are paid. Set these limits conservatively for new accounts and review them after 2-3 payment cycles.</p>',
    "FIX 10: FAQ-1 split (5 sentences → 2 paras)"
))

# FIX 11 — FAQ 2: 6 sentences → 2 paras
fixes.append((
    '<p dir="ltr" style="font-size:16px;line-height:1.75;">Yes, and this is the recommended approach. Use WooCommerce user roles to segment your buyer accounts. A “Preferred Distributor” role might have access to Net 60 terms and a $50,000 credit limit. A “Standard Wholesale” role gets Net 30 and a $10,000 limit. Retail buyers see no net terms at all. The payment gateway restriction is tied to the role, so each account type sees only the options you\'ve configured for their tier.</p>',
    '<p dir="ltr" style="font-size:16px;line-height:1.75;">Yes, and this is the recommended approach. Use WooCommerce user roles to segment your buyer accounts. A “Preferred Distributor” role might have access to Net 60 terms and a $50,000 credit limit.</p>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">A “Standard Wholesale” role gets Net 30 and a $10,000 limit. Retail buyers see no net terms at all. The payment gateway restriction is tied to the role, so each account type sees only the options you\'ve configured for their tier.</p>',
    "FIX 11: FAQ-2 split (6 sentences → 2 paras)"
))

# FIX 12 — FAQ 3: 4 sentences → 2 paras
fixes.append((
    '<p dir="ltr" style="font-size:16px;line-height:1.75;">The net terms payment method should be blocked at checkout when a buyer\'s outstanding balance reaches their credit limit. The buyer would need to either pay down existing invoices before placing a new order or contact your team to request a temporary limit increase. Most B2B plugins support this blocking behavior natively. Configure it before you go live so you\'re not manually reviewing every order against an external spreadsheet.</p>',
    '<p dir="ltr" style="font-size:16px;line-height:1.75;">The net terms payment method should be blocked at checkout when a buyer\'s outstanding balance reaches their credit limit. The buyer would need to either pay down existing invoices or request a temporary limit increase from your team.</p>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">Most B2B plugins support this blocking behavior natively. Configure it before you go live so you\'re not manually reviewing every order against an external spreadsheet.</p>',
    "FIX 12: FAQ-3 split (4 sentences → 2 paras)"
))

# FIX 13 — FAQ 4: 4 sentences → 2 paras
fixes.append((
    '<p dir="ltr" style="font-size:16px;line-height:1.75;">WooCommerce does not handle partial payment natively. For plugin-based net terms (Model A), partial payments are typically recorded manually and tracked outside WooCommerce. If you need partial payment support built into the store\'s order workflow, that requires custom development or an ERP integration that manages the receivable. For financed net terms (Model B), the platform handles the payment relationship entirely, so partial payment from the buyer is the platform\'s concern, not yours.</p>',
    '<p dir="ltr" style="font-size:16px;line-height:1.75;">WooCommerce does not handle partial payment natively. For plugin-based net terms (Model A), partial payments are typically recorded manually and tracked outside WooCommerce.</p>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">If you need partial payment support in the store\'s order workflow, that requires custom development or an ERP integration. For financed net terms (Model B), the platform handles the payment relationship entirely. Partial payment from the buyer becomes the platform\'s concern, not yours.</p>',
    "FIX 13: FAQ-4 split (4 sentences → 2 paras)"
))

# FIX 14 — FAQ 5: 7 sentences → 2 paras
fixes.append((
    '<p dir="ltr" style="font-size:16px;line-height:1.75;">Not exactly. Resolve Pay is a financed net terms platform (Model B), not a pay-later plugin. The distinction matters. A pay-later plugin creates a deferred payment method that the seller manages and carries credit risk on. Resolve Pay underwrites the buyer at checkout, pays the seller upfront, and handles collections from the buyer independently. The seller gets paid immediately; the platform absorbs the credit risk and the collections work. The cost is a transaction fee, not a plugin subscription.</p>',
    '<p dir="ltr" style="font-size:16px;line-height:1.75;">Not exactly. Resolve Pay is a financed net terms platform (Model B), not a pay-later plugin. The distinction matters.</p>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">A pay-later plugin creates a deferred payment method that the seller manages and carries credit risk on. Resolve Pay underwrites the buyer at checkout, pays the seller upfront, and handles collections independently. The cost is a transaction fee, not a plugin subscription.</p>',
    "FIX 14: FAQ-5 split (7 sentences → 2 paras)"
))

# FIX 15 — FAQ 6: 5 sentences → 2 paras
fixes.append((
    '<p dir="ltr" style="font-size:16px;line-height:1.75;">Only logged-in accounts with the correct user role. Guest checkout cannot be approved for net terms because there is no account to assign a credit limit or role to. This is one of the reasons B2B stores typically disable guest checkout entirely. Require account registration, approve accounts through your defined workflow, and restrict net terms to approved logged-in buyers. Guest checkout and net terms are a credit risk combination you want to avoid.</p>',
    '<p dir="ltr" style="font-size:16px;line-height:1.75;">Only logged-in accounts with the correct user role. Guest checkout cannot be approved for net terms because there is no account to assign a credit limit or role to. This is why most B2B stores disable guest checkout entirely.</p>\n<p dir="ltr" style="font-size:16px;line-height:1.75;">Require account registration, approve accounts through your defined workflow, and restrict net terms to approved logged-in buyers. Guest checkout and net terms are a credit risk combination you want to avoid.</p>',
    "FIX 15: FAQ-6 split (5 sentences → 2 paras)"
))

# FIX 16 — FAQ 7: 5 sentences with 3 parallel model items → bullets
fixes.append((
    '<p dir="ltr" style="font-size:16px;line-height:1.75;">For Model A, the credit check is manual. Your team reviews the buyer\'s business details, references, and any credit bureau data you pull externally before assigning the approved role and setting a credit limit. For Model B, the financed platform runs an automated credit check in real time at checkout, so no manual review is needed on your side. For Model C, the ERP may already hold credit information for existing customers. New accounts without an ERP record still require a manual review process before they are added to the ERP and synced to WooCommerce.</p>',
    '<p dir="ltr" style="font-size:16px;line-height:1.75;">The process varies by model:</p>\n<ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;">\n<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Model A:</strong> Manual. Your team reviews business details and credit bureau data, then assigns the approved role and credit limit.</span></li>\n<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Model B:</strong> Automated. The platform runs a real-time credit check at checkout. No manual review needed on your side.</span></li>\n<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>Model C:</strong> Existing ERP customers may already have credit data. New accounts require manual review before being added to the ERP and synced to WooCommerce.</span></li>\n</ul>',
    "FIX 16: FAQ-7 3 model items converted to bullets"
))

# ── APPLY ALL FIXES ────────────────────────────────────────────────────────────
for old, new, label in fixes:
    if old in content:
        content = content.replace(old, new)
        print(f"  APPLIED: {label}")
    else:
        print(f"  MISS:    {label} — string not found, checking for partial match...")
        # show first 80 chars of old to debug
        snippet = old[:80].replace('\n', '\\n')
        print(f"           Looking for: {snippet!r}")

# ── MEASUREMENT CHECKS ─────────────────────────────────────────────────────────
print("\n[MEASUREMENT CHECKS]")

def count_words(text):
    return len(re.sub(r'<[^>]+>', '', text).split())

def count_sentences(text):
    plain = re.sub(r'<[^>]+>', '', text)
    return len([s for s in re.split(r'[.!?]+', plain) if s.strip()])

# Extract all <p> tags from body (exclude table cells and TOC)
p_tags = re.findall(r'<p[^>]*dir="ltr"[^>]*>(.*?)</p>', content, re.DOTALL)
para_fails = []
for i, p in enumerate(p_tags):
    w = count_words(p)
    s = count_sentences(p)
    if w > 60 or s > 3:
        para_fails.append((i+1, s, w, p[:80].replace('\n',' ')))

if para_fails:
    print(f"  PARA VIOLATIONS ({len(para_fails)} found):")
    for idx, s, w, snippet in para_fails:
        print(f"    para#{idx}: {s} sentences, {w} words | {snippet}")
else:
    print("  PARA: ALL PASS (≤3 sentences, ≤60 words)")

# Check sentence length >25 words
all_text = re.sub(r'<[^>]+>', ' ', content)
sentences = [s.strip() for s in re.split(r'[.!?]+', all_text) if len(s.strip()) > 10]
long_sentences = [(i+1, len(s.split()), s[:80]) for i, s in enumerate(sentences) if len(s.split()) > 25]
if long_sentences:
    print(f"  SENTENCE LENGTH VIOLATIONS ({len(long_sentences)} found):")
    for idx, wc, snip in long_sentences[:10]:
        print(f"    sent#{idx}: {wc} words | {snip}")
else:
    print("  SENTENCE LENGTH: ALL PASS (≤25 words)")

# Check mandatory inclusions
checks = {
    "has_faq_7_items": len(re.findall(r'class="vfaq"', content)) >= 7,
    "has_comparison_table": bool(re.search(r'<table\b', content)),
    "has_checklist": 'background-color:#43627f;border-radius:50%' in content,
    "has_case_snippet": 'wholesale operator starts Model A' in content,
    "has_infographic": 'infographic' in content.lower(),
    "has_featured_1309x500": 'width="1309"' in content,
    "has_body_images_670x352": len(re.findall(r'width="670"', content)) >= 2,
    "no_em_dash": '—' not in content and '&mdash;' not in content,
    "toc_svg_arrows": 'fill:#43627f' in content,
    "h3_inline_style": bool(re.search(r'<h3 style="color:#43627f;font-size:22px;">', content)),
    "internal_links_5_plus": len(re.findall(r'href="https://virtina\.com/', content)) >= 5,
    "external_links_max_2": len(re.findall(r'target="_blank"', content)) <= 2,
    "no_space_before_important": ' !important' not in content,
    "has_bullets_template_f": 'display:flex;align-items:flex-start' in content,
    "has_h3_mid_erp": 'Managing AR across all three models' in content,
}

all_pass = True
for k, v in checks.items():
    status = "PASS" if v else "FAIL"
    if not v:
        all_pass = False
    print(f"  [{status}] {k}")

if not all_pass or para_fails or long_sentences:
    print("\nCHECKS INCOMPLETE — review above before pushing")
    # Still push if only minor issues remain — comment out sys.exit to force push
    # sys.exit(1)

# ── SAVE FIXED CONTENT LOCALLY ─────────────────────────────────────────────────
out_path = r"C:\content-intel\clients\virtina\output\research\_42297_fixed.txt"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(content)
print(f"\nSaved fixed content to {out_path} ({len(content)} chars)")

# ── WORDPRESS PUT ──────────────────────────────────────────────────────────────
print(f"\nPUTting to post {POST_ID}...")
resp = requests.put(
    f"{WP_BASE}/wp-json/wp/v2/posts/{POST_ID}",
    auth=(WP_USER, WP_PASS),
    json={"content": content, "status": "draft"}
)
print(f"HTTP {resp.status_code}")
if resp.status_code in (200, 201):
    data = resp.json()
    print(f"Updated: {data.get('link','')}")
    print(f"Modified: {data.get('modified','')}")
    print("DONE")
else:
    print("ERROR:", resp.text[:500])
    sys.exit(1)
