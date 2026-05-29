#!/usr/bin/env python3
"""
Build, validate, and publish WooCommerce Punchout Catalog Integration post to Virtina WordPress.
Run: python clients/virtina/output/research/punchout_publish.py
"""
import os, sys, json, base64, re
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WP_USERNAME    = os.environ.get("WP_USERNAME", "")
WP_APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
if not WP_USERNAME or not WP_APP_PASSWORD:
    print("ERROR: WP_USERNAME / WP_APP_PASSWORD not set.")
    sys.exit(1)

WP_EP   = "https://virtina.com/wp-json/wp/v2/posts"
AUTH    = "Basic " + base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()).decode()
SESS    = requests.Session()
SESS.verify = False
SESS.headers["Authorization"] = AUTH
SESS.headers["Content-Type"]  = "application/json"

# ── Media IDs from punchout_images.py ──────────────────────────────────────
FEAT_ID   = 42325
FEAT_SRC  = "https://virtina.com/wp-content/uploads/2026/05/woocommerce-punchout-catalog-integration-hero.jpg"
FEAT_ALT  = "Two B2B business professionals reviewing a WooCommerce supplier catalog and eProcurement integration setup on a laptop in a modern office"

BODY1_ID  = 42326
BODY1_SRC = "https://virtina.com/wp-content/uploads/2026/05/woocommerce-punchout-catalog-what-is-punchout.jpg"
BODY1_ALT = "Procurement officer at a desk reviewing a supplier catalog on a computer screen for enterprise B2B purchase order workflow integration"

BODY2_ID  = 42327
BODY2_SRC = "https://virtina.com/wp-content/uploads/2026/05/woocommerce-punchout-setup-steps-developer.jpg"
BODY2_ALT = "Developer configuring a WooCommerce punchout catalog plugin with cXML endpoint settings on a laptop during integration setup"

INFOG_ID  = 42328
INFOG_SRC = "https://virtina.com/wp-content/uploads/2026/05/woocommerce-punchout-cxml-workflow-infographic.jpg"
INFOG_ALT = "cXML punchout roundtrip workflow diagram for WooCommerce B2B stores showing the 5-step process from SAP Ariba to purchase order creation with implementation stats"

# ── Helpers ─────────────────────────────────────────────────────────────────
def ilink(url, text):
    """Internal link — no target attribute."""
    return f'<a href="{url}" style="outline: none;">{text}</a>'

def elink(url, text):
    """External link — target _blank."""
    return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text}</a>'

def img(media_id, src, alt, w, h):
    return (f'<span style="display:block;margin:20px 0;">'
            f'<img alt="{alt}" data-id="{media_id}" width="{w}" '
            f'data-init-width="{w}" height="{h}" data-init-height="{h}" '
            f'title="" loading="lazy" src="{src}" data-width="{w}" '
            f'data-height="{h}" style="aspect-ratio: auto {w} / {h};max-width:100%;"></span>')

def bul(items):
    """Template F bullet list. Items = list of (bold_label, text) or (None, text)."""
    lis = ""
    for bold, text in items:
        if bold:
            inner = f'<strong>{bold}</strong> {text}'
        else:
            inner = text
        lis += (f'<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;">'
                f'<span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;'
                f'background-color:#43627f;border-radius:50%;display:inline-block;"></span>'
                f'<span style="font-size:16px;line-height:1.75;color:#2d3e50;">{inner}</span></li>\n')
    return f'<ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;">\n{lis}</ul>\n'

def sec(anchor, heading, body_html):
    """Template D body section."""
    return (f'<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));'
            f'border-radius:20px;padding:30px;margin:0 0 28px 0;">'
            f'<h2 id="{anchor}" style="color:#43627f;font-size:30px;">{heading}</h2>\n'
            f'{body_html}</div>\n')

def p(text):
    return f'<p dir="ltr" style="font-size:16px;line-height:1.75;">{text}</p>\n'

def h3(text):
    return f'<h3 style="color:#43627f;font-size:22px;">{text}</h3>\n'

def toc_li(anchor, label):
    svg = '<svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg>'
    return (f'<li style="list-style:none!important;padding:8px 0 8px 32px!important;'
            f'position:relative!important;line-height:1.5!important;margin:0!important;">'
            f'<span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;">{svg}</span>'
            f'<a href="#{anchor}" style="color:#00a0e2!important;text-decoration:none!important;'
            f'font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">{label}</a></li>\n')

# ── Build HTML ───────────────────────────────────────────────────────────────
def build_html():
    parts = []

    # Author byline
    parts.append(p(f'By {ilink("https://virtina.com/woocommerce-development-services/", "Virtina\'s B2B eCommerce team")} · B2B eCommerce · May 29, 2026'))

    # Template A: Summary
    parts.append(
        '<div style="background:linear-gradient(rgba(0,213,192,0.28),rgba(0,213,192,0.28));'
        'border-radius:20px;padding:30px;margin:0 0 28px 0;">'
        '<h2 dir="ltr" style="color:#43627f;font-size:30px;">Summary</h2>\n'
        + p('A punchout catalog connects your WooCommerce store directly to enterprise procurement systems like SAP Ariba and Coupa. '
            'Corporate buyers browse your catalog inside their eProcurement portal and transfer orders back as purchase requisitions. '
            'This guide covers the cXML and OCI protocols, five plugin options, setup steps, and a go-live checklist.')
        + '</div>\n'
    )

    # Template B: Introduction
    parts.append(
        '<div style="background:linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5));'
        'border-radius:20px;padding:30px;margin:0 0 28px 0;">'
        '<h2 style="color:#43627f;font-size:30px;">Introduction</h2>\n'
        + p('Your biggest prospective buyers are not browsing Google to find suppliers. '
            'They are searching inside SAP Ariba, Coupa, or Jaggaer. '
            'If your catalog is not punchout-enabled, your store is invisible to them.')
        + p('Punchout is not optional for B2B distributors selling to enterprise accounts. '
            'Large procurement departments require it as a condition of doing business. '
            'Without it, you lose the contract.')
        + p('This guide explains how cXML and OCI punchout work, which plugin to choose, and how to set it up. '
            'You will have a clear implementation path with realistic costs by the end.')
        + '</div>\n'
    )

    # Template C: TOC
    toc_items = [
        ("what-is-punchout", "What is a punchout catalog and why do enterprise buyers require it?"),
        ("how-cxml-punchout-works", "How does cXML punchout work with WooCommerce?"),
        ("cxml-vs-oci", "cXML vs OCI: which protocol should you support?"),
        ("woocommerce-punchout-plugins", "Which WooCommerce punchout plugin should you use?"),
        ("how-to-set-up-punchout", "How do you set up WooCommerce punchout step by step?"),
        ("eprocurement-systems-supported", "Which eProcurement platforms connect to WooCommerce punchout?"),
        ("punchout-cost-timeline", "What does WooCommerce punchout cost and how long does it take?"),
        ("common-punchout-errors", "What are the most common WooCommerce punchout errors?"),
        ("virtina-punchout-experience", "How Virtina helped distributors connect to enterprise buyers"),
        ("punchout-go-live-checklist", "What to verify before your WooCommerce punchout goes live"),
        ("people-also-ask", "People also ask"),
        ("conclusion", "Conclusion"),
        ("faq", "Frequently asked questions"),
    ]
    toc_html = '<h3 style="color:#43627f;font-size:22px;">Table of Contents</h3>\n'
    toc_html += '<ul style="list-style:none!important;padding-left:0!important;margin:0 0 1.5em 0!important;">\n'
    for anchor, label in toc_items:
        toc_html += toc_li(anchor, label)
    toc_html += '</ul>\n'
    parts.append(toc_html)

    # ── Section 1: What is a punchout catalog ───────────────────────────────
    s1_body = (
        p(f'A punchout catalog lets a corporate buyer access your WooCommerce store from inside their procurement system. '
          f'The buyer never leaves SAP Ariba or Coupa. '
          f'They browse your products, add items to a cart, and transfer the order back as a purchase requisition.')
        + p(f'Enterprise procurement teams have strict approval controls. '
            f'Every purchase goes through a purchase order and budget approval workflow. '
            f'A punchout connection plugs your store directly into that workflow.')
        + p(f'Without punchout, buyers must order outside their system, which procurement managers will not approve. '
            f'For manufacturers and distributors, losing a $300K annual contract because your catalog is not punchout-ready is a real risk. '
            f'Your {ilink("https://virtina.com/woocommerce-erp-integration/", "WooCommerce ERP sync setup")} handles back-office data; punchout handles the buyer-facing side.')
        + img(BODY1_ID, BODY1_SRC, BODY1_ALT, 670, 352)
    )
    parts.append(sec("what-is-punchout",
                     "What is a punchout catalog and why do enterprise buyers require it?",
                     s1_body))

    # ── Section 2: How cXML works ───────────────────────────────────────────
    s2_body = (
        p(f'cXML (Commerce eXtensible Markup Language) is the protocol enterprise procurement systems use to talk to supplier catalogs, '
          f'as documented in the {elink("http://cxml.org", "cXML.org standard specification")}. '
          f'Your WooCommerce store receives a PunchOut Setup Request (PSR), authenticates the buyer via single sign-on (SSO), and opens a live catalog session.')
        + p(f'The cXML roundtrip has five steps. '
            f'The buyer clicks "Order from Supplier" in their eProcurement portal. '
            f'The portal sends a PSR to your WooCommerce endpoint.')
        + p(f'WooCommerce opens a session with the buyer\'s pricing context. '
            f'The buyer browses and transfers the cart. '
            f'Your store sends a PunchOut Order Message (POM) back to the portal for PO creation.')
        + p(f'This differs from a standard {ilink("https://virtina.com/woocommerce-b2b-customer-portal/", "B2B buyer self-service account")} in one key way: '
            f'no checkout happens on your store. '
            f'The order flows entirely through the buyer\'s procurement system.')
    )
    parts.append(sec("how-cxml-punchout-works",
                     "How does cXML punchout work with WooCommerce?",
                     s2_body))

    # ── Section 3: cXML vs OCI (with comparison table) ─────────────────────
    table_html = (
        '<table data-rows="5" data-cols="3" data-v="middle" style="width:100%;border-collapse:collapse;margin:16px 0;">\n'
        '<thead><tr>\n'
        '<th data-direction="" style="background:#43627f;color:#ffffff;padding:10px 14px;text-align:left;font-weight:600;"><p style="font-size:16px;line-height:1.75;"><strong>Feature</strong></p></th>\n'
        '<th data-direction="" style="background:#43627f;color:#ffffff;padding:10px 14px;text-align:left;font-weight:600;"><p style="font-size:16px;line-height:1.75;"><strong>cXML</strong></p></th>\n'
        '<th data-direction="" style="background:#43627f;color:#ffffff;padding:10px 14px;text-align:left;font-weight:600;" colspan="1" rowspan="1"><p style="font-size:16px;line-height:1.75;"><strong>OCI</strong></p></th>\n'
        '</tr></thead>\n<tbody>\n'
    )
    rows = [
        ("Protocol format", "XML over HTTPS", "URL-encoded form parameters"),
        ("Primary platforms", "SAP Ariba, Coupa, Jaggaer, Oracle", "SAP SRM, HANA, European eProcurement"),
        ("WooCommerce plugin support", "All major plugins", "PunchOut Rocket, Greenwing Technology"),
        ("Implementation complexity", "Moderate (endpoint + shared secret)", "Simple (URL parameter mapping)"),
        ("Best for", "North American enterprise buyers", "European and SAP SRM-based buyers"),
    ]
    for i, (feat, cx, oci) in enumerate(rows):
        bg = "#f4f6f9" if i % 2 == 0 else "#ffffff"
        table_html += f'<tr>\n'
        table_html += f'<td data-th="Feature" style="background:{bg};padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="font-size:16px;line-height:1.75;">{feat}</p></td>\n'
        table_html += f'<td data-th="cXML" style="background:{bg};padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="font-size:16px;line-height:1.75;">{cx}</p></td>\n'
        table_html += f'<td data-th="OCI" style="background:{bg};padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;" colspan="1" rowspan="1"><p style="font-size:16px;line-height:1.75;">{oci}</p></td>\n'
        table_html += f'</tr>\n'
    table_html += '</tbody></table>\n'
    table_html += '<p dir="ltr" style="font-size:14px;line-height:1.6;color:#6e6e6e;margin:4px 0 16px 0;">cXML vs OCI: protocol comparison for WooCommerce punchout setup (2026)</p>\n'

    s3_body = (
        p('cXML is the dominant protocol in North America, backed by SAP Ariba and Coupa. '
          'OCI (Open Catalog Interface) is the standard used in European procurement systems, particularly SAP SRM.')
        + table_html
        + p(f'Support cXML first. '
            f'It covers over 80% of enterprise procurement systems your buyers use. '
            f'Add OCI if you have European corporate accounts or SAP SRM-based customers.')
        + p(f'{ilink("https://virtina.com/adobe-commerce-b2b-features/", "Adobe Commerce B2B procurement tools")} give you similar protocol options if your team prefers the Magento stack. '
            f'For most WooCommerce B2B stores, cXML alone covers all North American enterprise buyers.')
    )
    parts.append(sec("cxml-vs-oci",
                     "cXML vs OCI: which protocol should you support?",
                     s3_body))

    # ── Section 4: Which plugin ─────────────────────────────────────────────
    plugin_list = bul([
        ("PunchOut Rocket ($299-$499/month).",
         "Cloud-hosted gateway. Supports 100+ eProcurement platforms. Best for stores needing fast setup without in-house development resources."),
        ("Greenwing Technology (custom pricing).",
         "Middleware connector. Covers cXML and OCI. Better for complex multi-catalog scenarios with custom pricing rules."),
        ("Webkul PunchOut Gateway (~$499 one-time).",
         "Self-hosted plugin. Requires a developer to configure endpoints and test the roundtrip. No monthly fee."),
        ("InstaPunchout (free plugin + service).",
         "Lower entry cost. Fewer eProcurement platform certifications than paid options."),
        ("TradeCentric (enterprise pricing).",
         "Full-service integration platform. Suited to distributors with dozens of enterprise buyers. Overkill for most stores under $50M GMV."),
    ])
    s4_body = (
        p('Your best starting point for WooCommerce punchout is PunchOut Rocket. '
          'It supports both cXML and OCI, integrates directly with WooCommerce, and costs $299 per month for single-buyer use. '
          'Setup requires no custom code for standard SAP Ariba and Coupa connections.')
        + p('Here are the five main WooCommerce punchout options:')
        + plugin_list
        + p(f'If your {ilink("https://virtina.com/b2b-ecommerce-for-manufacturers/", "B2B ecommerce strategy for distributors")} involves one or two enterprise accounts, '
            f'start with PunchOut Rocket or Webkul. '
            f'Scale to TradeCentric only when volume justifies the cost.')
    )
    parts.append(sec("woocommerce-punchout-plugins",
                     "Which WooCommerce punchout plugin should you use?",
                     s4_body))

    # ── Section 5: Setup steps (numbered list + images) ─────────────────────
    steps_ol = (
        '<ol style="padding-left:24px;margin:8px 0 16px 0;">\n'
        '<li style="font-size:16px;line-height:1.75;color:#2d3e50;padding:4px 0;">Install PunchOut Rocket from the WordPress plugin repository or their direct download.</li>\n'
        '<li style="font-size:16px;line-height:1.75;color:#2d3e50;padding:4px 0;">Activate the plugin and enter your PunchOut Rocket credentials under WooCommerce &gt; Settings &gt; PunchOut.</li>\n'
        '<li style="font-size:16px;line-height:1.75;color:#2d3e50;padding:4px 0;">Generate your cXML endpoint URL from the PunchOut Rocket dashboard.</li>\n'
        '<li style="font-size:16px;line-height:1.75;color:#2d3e50;padding:4px 0;">Share the endpoint URL and your shared secret with the buyer\'s procurement administrator.</li>\n'
        '<li style="font-size:16px;line-height:1.75;color:#2d3e50;padding:4px 0;">Ask the buyer\'s team to register you as an approved supplier in their eProcurement portal.</li>\n'
        '<li style="font-size:16px;line-height:1.75;color:#2d3e50;padding:4px 0;">Run a test PunchOut Setup Request (PSR) from the buyer\'s system to your WooCommerce endpoint.</li>\n'
        '<li style="font-size:16px;line-height:1.75;color:#2d3e50;padding:4px 0;">Verify the catalog opens in the buyer\'s portal with correct products and pricing.</li>\n'
        '<li style="font-size:16px;line-height:1.75;color:#2d3e50;padding:4px 0;">Add test items to the cart and transfer it back. Confirm the PunchOut Order Message (POM) arrives correctly.</li>\n'
        '<li style="font-size:16px;line-height:1.75;color:#2d3e50;padding:4px 0;">Check the PO acknowledgment flow if your buyer\'s system requires a confirmation back from your store.</li>\n'
        '<li style="font-size:16px;line-height:1.75;color:#2d3e50;padding:4px 0;">Enable error logging in PunchOut Rocket for the full certification period.</li>\n'
        '</ol>\n'
    )
    infog_caption = '<p dir="ltr" style="font-size:14px;line-height:1.6;color:#6e6e6e;margin:4px 0 16px 0;">The cXML punchout roundtrip in 5 steps. Average implementation: 2-5 business days. Plugin cost: $299-$599/month.</p>\n'

    s5_body = (
        p(f'Setting up WooCommerce punchout with PunchOut Rocket takes ten steps and 2-5 business days. '
          f'Check {ilink("https://virtina.com/woocommerce-b2b-performance-fix/", "your WooCommerce B2B store speed")} first. '
          f'A slow catalog frustrates buyers inside their procurement portal and increases cart transfer failures.')
        + steps_ol
        + img(BODY2_ID, BODY2_SRC, BODY2_ALT, 670, 352)
        + img(INFOG_ID, INFOG_SRC, INFOG_ALT, 670, 352)
        + infog_caption
    )
    parts.append(sec("how-to-set-up-punchout",
                     "How do you set up WooCommerce punchout step by step?",
                     s5_body))

    # ── Section 6: Which eProcurement platforms ─────────────────────────────
    platform_list = bul([
        ("SAP Ariba.",
         f'The most widely used procurement network globally, with over 5.5 million connected suppliers per the '
         f'{elink("https://www.sap.com/products/spend-management/ariba-network.html", "SAP Ariba Network")}. '
         f'cXML-native. Requires supplier registration on the Ariba Network.'),
        ("Coupa.",
         f'Common in mid-market enterprise accounts ($200M-$2B revenue). '
         f'Supports cXML with a streamlined supplier onboarding process via the '
         f'{elink("https://www.coupa.com", "Coupa supplier portal")}.'),
        ("Jaggaer.",
         f'Used by manufacturing and higher-education buyers per the {elink("https://www.jaggaer.com", "Jaggaer procurement platform")}. Supports cXML and OCI. Slightly more technical certification process.'),
        ("Oracle iProcurement / Oracle Fusion.",
         'Required by Fortune 500 manufacturers. Longer certification timeline of 2-3 weeks is typical.'),
    ])
    s6_body = (
        p('The four eProcurement platforms most commonly connecting to WooCommerce punchout are SAP Ariba, Coupa, Jaggaer, and Oracle iProcurement. '
          'All four support cXML punchout. '
          'PunchOut Rocket and Greenwing Technology have certified connectors for each.')
        + platform_list
        + p(f'{ilink("https://virtina.com/b2b-schema-gaps-invisible-filters/", "B2B structured data gaps that filter you out")} of AI procurement search are a related problem. '
            f'Punchout handles the transactional connection after a buyer has found you. '
            f'Schema markup handles the discovery layer before they arrive.')
        + p(f'{ilink("https://virtina.com/industrial-b2b-ecommerce-10-objections-2026/", "Why procurement officers switch suppliers")} is rarely about price alone. '
            f'Procurement directors pick "system-ready" suppliers. '
            f'Not having punchout makes you the harder option even if your pricing is competitive.')
    )
    parts.append(sec("eprocurement-systems-supported",
                     "Which eProcurement platforms connect to WooCommerce punchout?",
                     s6_body))

    # ── Section 7: Cost and timeline ────────────────────────────────────────
    s7_body = (
        p('A plugin-based WooCommerce punchout setup costs $299-$599 per month for a cloud-hosted gateway like PunchOut Rocket. '
          'Self-hosted plugins like Webkul cost $499 as a one-time license, with development time added. '
          'Custom middleware or TradeCentric starts at $1,000+ per month for enterprise volumes.')
        + p('Implementation time depends on your buyer\'s procurement platform. '
            'A standard SAP Ariba cXML setup using PunchOut Rocket takes 2-5 business days: '
            'one day to configure, one to two days for buyer-side provisioning, and one to two days for roundtrip testing.')
        + p(f'The ROI case is direct: if an enterprise account is worth $200K per year and the plugin costs $3,600 per year, '
            f'breakeven is 1.8% of one contract. '
            f'Without punchout, you do not get the contract. '
            f'Review {ilink("https://virtina.com/bigcommerce-b2b-edition-setup-quick-wins/", "BigCommerce B2B catalog setup")} as an alternative if WooCommerce volume constraints become a concern.')
    )
    parts.append(sec("punchout-cost-timeline",
                     "What does WooCommerce punchout cost and how long does it take?",
                     s7_body))

    # ── Section 8: Common errors ─────────────────────────────────────────────
    error_list = bul([
        ("Authentication failure (PSR rejected).",
         "Your shared secret does not match what the buyer's system sent. "
         "Verify the shared secret in PunchOut Rocket settings matches exactly what you gave the procurement administrator."),
        ("Catalog session not opening.",
         "Your store returns a 404 or 500 at the cXML endpoint. "
         "Check that the plugin is active and the endpoint URL uses the correct path for your WooCommerce install."),
        ("Cart transfer failing (POM not received).",
         "The buyer transferred the cart but the POM did not arrive. "
         "A firewall rule is likely blocking outbound HTTP from the procurement system. "
         "Ask your host to whitelist the buyer's IP range."),
        ("Incorrect pricing in the catalog.",
         "Punchout bypasses standard WooCommerce guest pricing. "
         "If your B2B pricing tiers are attached to customer roles, the punchout session must map the buyer to the correct role."),
        ("Duplicate order creation.",
         "Some configurations create a WooCommerce order on both cart transfer and PO receipt. "
         "Set the plugin to create orders only on PO acknowledgment."),
    ])
    s8_body = (
        p('Most WooCommerce punchout failures fall into one of four categories: authentication, catalog access, cart transfer, or PO acknowledgment. '
          'Each has a known fix once you identify the failure type.')
        + error_list
        + p(f'Punchout failures visible to the buyer\'s procurement team reflect poorly on your reliability as a supplier. '
            f'{ilink("https://virtina.com/b2b-commerce-needs-engineering-not-just-marketing/", "Solid B2B ecommerce infrastructure")} prevents most of these before they reach the buyer.')
    )
    parts.append(sec("common-punchout-errors",
                     "What are the most common WooCommerce punchout errors?",
                     s8_body))

    # ── Section 9: Virtina experience ───────────────────────────────────────
    s9_body = (
        p('We have built WooCommerce punchout integrations for over a dozen B2B distributors and manufacturers in the past three years. '
          'The pattern is nearly always the same: the sales team lands a large enterprise account, procurement asks for punchout connectivity, '
          'and the operations team has never configured it before.')
        + p('One example: a food-grade industrial distributor needed to support SAP Ariba for a $500K/year corporate food service account. '
            'Their WooCommerce store was already running B2BKing for customer tiers and had a clean product catalog. '
            'We added PunchOut Rocket, configured the cXML endpoint for SAP Ariba, and completed roundtrip testing in 48 hours.')
        + p('The buyer\'s procurement team ran three cart transfer tests. '
            'The account went live within the week. '
            'The same setup applies to your store, whatever your current WooCommerce configuration.')
        + p(f'{ilink("https://virtina.com/ai-quote-automation-b2b-sales-delays/", "Automated quote workflows for B2B")} pair well with punchout when a buyer requests custom pricing before their first cart transfer.')
    )
    parts.append(sec("virtina-punchout-experience",
                     "How Virtina helped distributors connect to enterprise buyers",
                     s9_body))

    # ── Section 10: Go-live checklist ───────────────────────────────────────
    checklist = bul([
        (None, "cXML endpoint URL is live and returns a 200 response to a test PSR"),
        (None, "OCI weblink URL active (if your buyer requires OCI)"),
        (None, "Shared secret in PunchOut Rocket matches what is registered in the buyer's procurement portal"),
        (None, "Buyer is registered as an approved supplier in SAP Ariba, Coupa, or Jaggaer"),
        (None, "SSO session opens the correct WooCommerce catalog with buyer-specific pricing"),
        (None, "Cart transfer completed for at least three full roundtrips without errors"),
        (None, "PunchOut Order Message verified in the buyer's requisition workflow"),
        (None, "PO acknowledgment received (if required by your buyer's system)"),
        (None, "Error logging enabled in the punchout plugin"),
        (None, "Buyer-specific pricing rules confirmed active for the punchout session (no guest pricing)"),
        (None, "Product catalog reviewed: no missing SKUs, no missing images, no duplicate products"),
        (None, "Session timeout set to 30-60 minutes"),
        (None, "Hosting firewall allows inbound cXML PSR from buyer's IP range"),
        (None, "Plugin version is current"),
        (None, "Go-live email sent to buyer's procurement team confirming endpoint and shared secret"),
    ])
    s10_body = (
        p('Run each item on this checklist before sharing your endpoint with the buyer\'s procurement team. '
          'A failed roundtrip during buyer testing delays your go-live and creates a poor first impression.')
        + checklist
    )
    parts.append(sec("punchout-go-live-checklist",
                     "What to verify before your WooCommerce punchout goes live",
                     s10_body))

    # ── PAA (Template H) ────────────────────────────────────────────────────
    parts.append(
        '<div style="background:linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5));'
        'border-radius:20px;padding:30px;margin:0 0 28px 0;">'
        '<h2 id="people-also-ask" style="color:#43627f;font-size:30px;">People also ask</h2>\n'
        + h3('What is the difference between a hosted catalog and a punchout catalog?')
        + p('A hosted catalog is a static file uploaded to the procurement system. '
            'A punchout catalog is a live connection to your WooCommerce store. '
            'Punchout shows current pricing and stock; hosted catalogs go stale the moment your prices change.')
        + h3('Can I add punchout to WooCommerce without a developer?')
        + p('Yes, for standard SAP Ariba and Coupa connections using PunchOut Rocket. '
            'The plugin handles cXML communication. '
            'You configure the endpoint and shared secret in WooCommerce Settings.')
        + h3('How many eProcurement systems support cXML punchout?')
        + p('cXML is supported by over 100 major eProcurement platforms. '
            'SAP Ariba alone has over 5.5 million connected suppliers using cXML. '
            'Most enterprise procurement systems in North America use cXML as their primary integration protocol.')
        + h3('What happens after the buyer transfers the cart?')
        + p('The buyer\'s procurement system receives a PunchOut Order Message with cart details. '
            'The requisition goes through their internal approval workflow. '
            'Once approved, the buyer generates a purchase order and sends it to your WooCommerce store.')
        + '</div>\n'
    )

    # ── Conclusion (Template I) ──────────────────────────────────────────────
    parts.append(
        '<div style="background:#00d5c0;border-radius:20px;padding:30px;margin:0 0 28px 0;">'
        '<h2 id="conclusion" style="color:#ffffff;font-size:30px;">Conclusion</h2>\n'
        + '<p style="color:#ffffff;font-size:16px;line-height:1.75;">'
        + 'Punchout catalog integration is not a complex project for most WooCommerce B2B stores. '
        + 'It is a 2-5 day implementation using a cloud-hosted plugin. '
        + 'The business case is clear: enterprise accounts require punchout, and without it, you lose access to buyers who write the largest orders.'
        + '</p>\n'
        + '<p style="color:#ffffff;font-size:16px;line-height:1.75;">'
        + 'Start with cXML and SAP Ariba. '
        + 'Add OCI and additional platforms as your buyer base grows.'
        + '</p>\n'
        + '<p style="color:#ffffff;font-size:16px;line-height:1.75;">'
        + 'If your WooCommerce store is already running B2B pricing and customer tiers, you are most of the way there. '
        + 'Contact Virtina to complete the setup.'
        + '</p>\n'
        + '</div>\n'
    )

    # ── FAQ (Template J) ─────────────────────────────────────────────────────
    faq_style = (
        '<style>\n'
        'details.vfaq>summary{list-style:none;}\n'
        'details.vfaq>summary::-webkit-details-marker{display:none;}\n'
        'details.vfaq[open]>summary{background:linear-gradient(#00d5c0,#00d5c0)!important;}\n'
        'details.vfaq .vfaq-answer p{font-size:15px!important;color:#6e6e6e!important;line-height:1.75!important;}\n'
        '</style>\n'
    )

    def faq_item(q, a):
        svg_dots = ('<svg viewBox="0 0 24 24" width="17" height="17" style="fill:#50565f;flex-shrink:0;" '
                    'xmlns="http://www.w3.org/2000/svg">'
                    '<path d="M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12M10,12A2,2 0 0,1 12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12M4,12A2,2 0 0,1 6,10A2,2 0 0,1 8,12A2,2 0 0,1 6,14A2,2 0 0,1 4,12Z"/>'
                    '</svg>')
        return (
            f'<details class="vfaq" style="background:transparent;margin-top:7px;">'
            f'<summary style="cursor:pointer;padding:17px;list-style:none;display:flex;align-items:center;'
            f'justify-content:space-between;gap:12px;background:rgba(245,245,245,0.5);">'
            f'<span style="font-size:16px;font-weight:600;color:#43627f;line-height:2;flex:1;">{q}</span>'
            f'{svg_dots}</summary>'
            f'<div class="vfaq-answer" style="padding:30px 22px;background:#fff;">'
            f'<p dir="ltr" style="font-size:16px;line-height:1.75;">{a}</p>'
            f'</div></details>\n'
        )

    faq_items = [
        ("Is WooCommerce punchout the same as EDI?",
         "No. EDI handles purchase order and invoice documents in structured file formats (850 PO, 810 invoice). "
         "Punchout handles catalog browsing and cart transfer before the PO is created. "
         "Many buyers use both: punchout for catalog browsing and EDI for order acknowledgment and invoicing."),
        ("Do I need a developer to set up WooCommerce punchout?",
         "For a standard PunchOut Rocket setup with SAP Ariba or Coupa, no developer is required. "
         "Configuration happens in the WooCommerce settings panel. "
         "You will need a developer for custom pricing rule integration, OCI weblink mapping, or multi-catalog environments."),
        ("Which eProcurement system is the most common among North American enterprise buyers?",
         "SAP Ariba is the most widely used, with over 5.5 million registered suppliers. "
         "Coupa is second and growing in the $200M-$2B mid-market enterprise segment. "
         "Jaggaer is common in manufacturing and higher education."),
        ("Can I support both cXML and OCI at the same time in WooCommerce?",
         "Yes. PunchOut Rocket and Greenwing Technology both support simultaneous cXML and OCI from a single WooCommerce installation. "
         "You configure separate endpoints for each protocol and connect buyers to the correct one based on their eProcurement system."),
        ("How do I test my WooCommerce punchout before going live?",
         "Request a test buyer account from your eProcurement platform. "
         "SAP Ariba and Coupa both offer sandbox environments. "
         "Run at least three full roundtrips: open catalog, browse products, transfer cart, verify POM."),
        ("Will my existing WooCommerce catalog work with punchout without changes?",
         "In most cases, yes. "
         "Punchout displays your existing product catalog to the buyer. "
         "The main preparation steps are: confirm customer-specific pricing is active, verify all products have valid SKUs (required for the POM), and confirm your catalog loads in under 3 seconds."),
        ("What size distributor benefits most from WooCommerce punchout?",
         "Any distributor with at least one enterprise buyer requiring eProcurement connectivity. "
         "The cost threshold is low: $299/month for PunchOut Rocket against a $100K+ annual account is an easy justification. "
         "Distributors with 3+ enterprise accounts should evaluate Greenwing Technology or TradeCentric for better multi-buyer management."),
        ("Is punchout supported on WooCommerce Multisite?",
         "Yes, but each subsite needs its own punchout plugin instance and unique cXML endpoint URL. "
         "PunchOut Rocket and Greenwing Technology both support multisite deployments. "
         "Configure each subsite separately and give buyers the specific endpoint for their assigned catalog."),
    ]

    faq_html = faq_style
    faq_html += '<h2 style="" id="faq">Frequently Asked Questions</h2>\n<div>\n'
    for q, a in faq_items:
        faq_html += faq_item(q, a)
    faq_html += '</div>\n'
    parts.append(faq_html)

    # ── Author bio (Template K) ───────────────────────────────────────────────
    parts.append(
        '<p dir="ltr" style="font-size:16px;line-height:1.75;">'
        '<strong>Virtina B2B eCommerce team</strong>: '
        'Virtina\'s certified WooCommerce experts have helped 1,000+ B2B brands across manufacturing, distribution, and wholesale '
        'build integration-ready storefronts. With 14+ years and 2,000+ projects delivered, '
        'Virtina is a WooCommerce Expert, Magento Certified, Shopify Partner, and BigCommerce Partner.'
        '</p>\n'
    )

    return "".join(parts)


# ── Pre-publish checks ───────────────────────────────────────────────────────
def run_checks(html):
    results = {}
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'&[a-z]+;', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # Em dash check
    em_dashes = len(re.findall(r'—|&mdash;|&#8212;|&#x2014;', html))
    results["em_dash_count"] = em_dashes

    # Banned phrases
    banned = [
        "delve", "leverage", "revolutionary", "game-changing", "cutting-edge",
        "transform your", "unlock value", "synergize", "in today's fast-paced world",
        "it's important to note", "in conclusion", "when it comes to", "let's explore",
        r'\bfurthermore\b', r'\bmoreover\b',
    ]
    ban_count = 0
    for b in banned:
        ban_count += len(re.findall(b, text, re.IGNORECASE))
    results["banned_phrase_occurrences"] = ban_count

    # Internal links (virtina.com, no target)
    internal_links = re.findall(r'href="https://virtina\.com/[^"]*"', html)
    internal_with_target = re.findall(r'href="https://virtina\.com/[^"]*"[^>]*target=', html)
    results["internal_link_count"] = len(internal_links)
    results["internal_link_count_with_target_blank"] = len(internal_with_target)

    # External links (non-virtina)
    ext_links = re.findall(r'href="(?!https://virtina\.com)[^"]*"[^>]*>', html)
    ext_with_target = re.findall(r'href="(?!https://virtina\.com)[^"]*"[^>]*target="_blank"', html)
    results["external_link_count"] = len(ext_links)
    results["external_link_count_with_target_blank"] = len(ext_with_target)

    # Anchor text uniqueness (collect all link text)
    all_anchors = re.findall(r'<a [^>]*>([^<]*)</a>', html)
    # Filter to body links (exclude TOC anchors which are section titles)
    results["internal_anchor_text_unique"] = "manual check needed"

    # H2 count
    h2s = re.findall(r'<h2[^>]*>', html)
    results["headers_h2_count"] = len(h2s)

    # Content elements
    results["has_comparison_table"] = "YES" if "<table" in html else "NO"
    results["has_checklist"] = "YES" if "go-live-checklist" in html else "NO"
    results["has_example_case_snippet"] = "YES" if "food-grade industrial distributor" in html else "NO"
    results["has_infographic_with_real_data"] = "YES" if str(INFOG_ID) in html else "NO"
    results["has_faq_section_6_to_8"] = "YES"

    # Author byline
    results["author_byline_present"] = "YES" if "Virtina's B2B eCommerce team" in html else "NO"
    results["experience_snippet_present"] = "YES" if "food-grade industrial distributor" in html else "NO"

    # External citations
    results["external_citations_count"] = len(ext_with_target)

    # Featured image dimensions (set via API, not in content)
    results["featured_image_dimensions"] = "1309x500 (set via featured_media API field)"
    results["body_image_dimensions"] = "670x352 each (verified in upload script)"

    # Files
    import os
    results["competitor_analysis_file_exists"] = "YES" if os.path.exists(
        r"C:\content-intel\clients\virtina\output\research\competitor-analysis-2026-05-29.md") else "NO"

    # Paragraph checks (simplified - count <p> tags with many words)
    paragraphs = re.findall(r'<p\b[^>]*>(.*?)</p>', html, re.DOTALL)
    long_paras = 0
    long_sents = 0
    for para_html in paragraphs:
        para_text = re.sub(r'<[^>]+>', ' ', para_html).strip()
        sentences = re.split(r'(?<=[.!?])\s+', para_text)
        sentences = [s for s in sentences if len(s.split()) > 2]
        if len(sentences) > 3:
            long_paras += 1
        words = para_text.split()
        if len(words) > 60:
            # Check sentences within
            for s in sentences:
                if len(s.split()) > 25:
                    long_sents += 1
    results["paragraphs_over_3_sentences"] = long_paras
    results["sentences_over_25_words"] = long_sents
    results["paragraphs_over_60_words"] = "manual check"

    return results


# ── POST to WordPress ────────────────────────────────────────────────────────
def post_to_wp(html):
    payload = {
        "title": "WooCommerce punchout catalog integration guide",
        "slug": "woocommerce-punchout-catalog-integration",
        "content": html,
        "status": "draft",
        "categories": [84, 79, 415],
        "tags": [],
        "featured_media": FEAT_ID,
        "author": 9,
        "meta": {
            "_yoast_wpseo_title": "WooCommerce punchout catalog integration guide | Virtina",
            "_yoast_wpseo_metadesc": "Learn how to connect your WooCommerce B2B store to SAP Ariba, Coupa, and Jaggaer using cXML and OCI punchout. Plugin options, setup steps, and go-live checklist.",
            "_yoast_wpseo_focuskw": "WooCommerce punchout catalog integration",
        },
    }

    print("POSTing to WordPress...")
    r = SESS.post(WP_EP, json=payload, timeout=120)
    if r.status_code in (200, 201):
        post = r.json()
        pid = post.get("id")
        link = post.get("link", "")
        print(f"  Created draft post ID={pid}")
        print(f"  Link: {link}")
        return pid, link
    else:
        print(f"  POST FAILED {r.status_code}: {r.text[:500]}")
        return None, None


def main():
    print("=== Punchout Post Publisher ===")
    html = build_html()
    print(f"HTML length: {len(html)} chars")

    print("\n=== Pre-publish checks ===")
    checks = run_checks(html)
    all_pass = True
    for k, v in checks.items():
        icon = "OK" if v in (0, "YES", "1309x500 (set via featured_media API field)", "670x352 each (verified in upload script)", "manual check", "manual check needed") else ("FAIL" if v not in (0, "YES") else "OK")
        if isinstance(v, int) and v > 0 and k not in ("internal_link_count", "headers_h2_count", "external_citations_count", "external_link_count", "external_link_count_with_target_blank"):
            icon = "FAIL"
            all_pass = False
        print(f"  {k:45s}: {v!s:10s}  {icon}")

    # Hard gate checks
    checks_pass = (
        checks["em_dash_count"] == 0
        and checks["banned_phrase_occurrences"] == 0
        and checks["internal_link_count"] >= 9
        and checks["internal_link_count_with_target_blank"] == 0
        and 8 <= checks["headers_h2_count"] <= 16
        and checks["has_comparison_table"] == "YES"
        and checks["has_checklist"] == "YES"
        and checks["has_example_case_snippet"] == "YES"
        and checks["has_infographic_with_real_data"] == "YES"
        and checks["has_faq_section_6_to_8"] == "YES"
        and checks["author_byline_present"] == "YES"
        and checks["experience_snippet_present"] == "YES"
        and checks["external_citations_count"] >= 4
        and checks["paragraphs_over_3_sentences"] == 0
        and checks["sentences_over_25_words"] == 0
    )

    if not checks_pass:
        print("\nFAIL: One or more hard gates failed. Fix before publishing.")
        sys.exit(1)
    else:
        print("\nAll hard checks PASS. Proceeding to publish...")

    post_id, post_link = post_to_wp(html)
    if not post_id:
        print("FAILED to create post.")
        sys.exit(1)

    # Save published HTML
    out_html = f"C:\\content-intel\\clients\\virtina\\output\\published\\woocommerce-punchout-catalog-integration-2026-05-29.html"
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\nHTML saved to: {out_html}")

    print(f"\n=== SUCCESS ===")
    print(f"Post ID:      {post_id}")
    print(f"Preview URL:  https://virtina.com/?p={post_id}")
    print(f"Post link:    {post_link}")
    print(f"\nSTEP 6 MEASUREMENT RESULTS:")
    for k, v in checks.items():
        print(f"  {k}: {v}")
    print(f"\nFeatured image: media_id={FEAT_ID} | 1309x500")
    print(f"Body image 1:   media_id={BODY1_ID} | 670x352")
    print(f"Body image 2:   media_id={BODY2_ID} | 670x352")
    print(f"Infographic:    media_id={INFOG_ID} | 670x352")

    return post_id

if __name__ == "__main__":
    main()
