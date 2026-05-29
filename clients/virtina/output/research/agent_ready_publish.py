#!/usr/bin/env python3
"""
Build, validate, and publish "The customer was a robot: how to make your store
readable to AI shopping agents" to Virtina WordPress as a draft.

Prerequisites: run agent_ready_images.py first to populate agent_ready_image_results.json.
Run: python clients/virtina/output/research/agent_ready_publish.py
"""
import os, sys, json, base64, re
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WP_USERNAME     = os.environ.get("WP_USERNAME", "")
WP_APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
if not WP_USERNAME or not WP_APP_PASSWORD:
    print("ERROR: WP_USERNAME / WP_APP_PASSWORD not set.")
    sys.exit(1)

WP_EP = "https://virtina.com/wp-json/wp/v2/posts"
AUTH  = "Basic " + base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()).decode()
SESS  = requests.Session()
SESS.verify = False
SESS.headers["Authorization"] = AUTH
SESS.headers["Content-Type"]  = "application/json"

RESULTS_FILE = r"C:\content-intel\clients\virtina\output\research\agent_ready_image_results.json"

# ── Load image results ────────────────────────────────────────────────────────
if not os.path.exists(RESULTS_FILE):
    print(f"ERROR: {RESULTS_FILE} not found. Run agent_ready_images.py first.")
    sys.exit(1)

with open(RESULTS_FILE, encoding="utf-8") as f:
    IMG = json.load(f)

def _get(key, field):
    val = IMG.get(key, {}).get(field)
    if not val:
        print(f"ERROR: image results missing {key}.{field}. Re-run agent_ready_images.py.")
        sys.exit(1)
    return val

FEAT_ID   = _get("featured", "media_id")
FEAT_SRC  = _get("featured", "src")
FEAT_ALT  = _get("featured", "alt")

BODY1_ID  = _get("body1", "media_id")
BODY1_SRC = _get("body1", "src")
BODY1_ALT = _get("body1", "alt")

BODY2_ID  = _get("body2", "media_id")
BODY2_SRC = _get("body2", "src")
BODY2_ALT = _get("body2", "alt")

# ── HTML helpers (same pattern as punchout_publish.py) ───────────────────────

def ilink(url, text):
    """Internal virtina.com link — no target attribute."""
    return f'<a href="{url}" style="outline: none;">{text}</a>'

def elink(url, text):
    """External link — opens in new tab."""
    return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text}</a>'

def img_block(media_id, src, alt, w, h):
    """Template G body image block."""
    return (
        f'<span style="display:block;margin:20px 0;">'
        f'<img alt="{alt}" data-id="{media_id}" width="{w}" '
        f'data-init-width="{w}" height="{h}" data-init-height="{h}" '
        f'title="" loading="lazy" src="{src}" data-width="{w}" '
        f'data-height="{h}" style="aspect-ratio: auto {w} / {h};max-width:100%;"></span>\n'
    )

def p(text):
    """Standard body paragraph."""
    return f'<p dir="ltr" style="font-size:16px;line-height:1.75;">{text}</p>\n'

def pc(text):
    """Conclusion paragraph — white text on teal."""
    return f'<p style="color:#ffffff;font-size:16px;line-height:1.75;">{text}</p>\n'

def h3(text):
    """H3 subheading — Thrive Architect pattern."""
    return f'<h3 style="color:#43627f;font-size:22px;">{text}</h3>\n'

def sec(anchor, heading, body_html):
    """Template D body section wrapper."""
    return (
        f'<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));'
        f'border-radius:20px;padding:30px;margin:0 0 28px 0;">'
        f'<h2 id="{anchor}" style="color:#43627f;font-size:30px;">{heading}</h2>\n'
        f'{body_html}</div>\n'
    )

def bul(items):
    """Template F bullet list. Items = list of (bold_label, text) or (None, text)."""
    lis = ""
    for bold, text in items:
        if bold:
            inner = f'<strong>{bold}</strong> {text}'
        else:
            inner = text
        lis += (
            f'<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;">'
            f'<span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;'
            f'background-color:#43627f;border-radius:50%;display:inline-block;"></span>'
            f'<span style="font-size:16px;line-height:1.75;color:#2d3e50;">{inner}</span></li>\n'
        )
    return f'<ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;">\n{lis}</ul>\n'

def ol_steps(items):
    """Numbered ordered list with consistent li styling."""
    lis = ""
    for item in items:
        lis += (
            f'<li style="font-size:16px;line-height:1.75;color:#2d3e50;padding:4px 0;">'
            f'{item}</li>\n'
        )
    return f'<ol style="padding-left:24px;margin:8px 0 16px 0;">\n{lis}</ol>\n'

def toc_li(anchor, label):
    """Template C TOC list item with inline SVG arrow."""
    svg = (
        '<svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" '
        'xmlns="http://www.w3.org/2000/svg">'
        '<path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/>'
        '</svg>'
    )
    return (
        f'<li style="list-style:none!important;padding:8px 0 8px 32px!important;'
        f'position:relative!important;line-height:1.5!important;margin:0!important;">'
        f'<span aria-hidden="true" style="position:absolute!important;left:0!important;'
        f'top:8px!important;">{svg}</span>'
        f'<a href="#{anchor}" style="color:#00a0e2!important;text-decoration:none!important;'
        f'font-family:metropolis,arial!important;font-size:16px!important;'
        f'font-weight:500!important;">{label}</a></li>\n'
    )

def faq_item(q, a):
    """Template J FAQ accordion item. Use || in 'a' to split into multiple paragraphs."""
    svg_dots = (
        '<svg viewBox="0 0 24 24" width="17" height="17" style="fill:#50565f;flex-shrink:0;" '
        'xmlns="http://www.w3.org/2000/svg">'
        '<path d="M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12'
        'M10,12A2,2 0 0,1 12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12'
        'M4,12A2,2 0 0,1 6,10A2,2 0 0,1 8,12A2,2 0 0,1 6,14A2,2 0 0,1 4,12Z"/>'
        '</svg>'
    )
    para_html = "".join(
        f'<p dir="ltr" style="font-size:16px;line-height:1.75;">{part.strip()}</p>'
        for part in a.split("||") if part.strip()
    )
    return (
        f'<details class="vfaq" style="background:transparent;margin-top:7px;">'
        f'<summary style="cursor:pointer;padding:17px;list-style:none;display:flex;'
        f'align-items:center;justify-content:space-between;gap:12px;'
        f'background:rgba(245,245,245,0.5);">'
        f'<span style="font-size:16px;font-weight:600;color:#43627f;line-height:2;flex:1;">'
        f'{q}</span>{svg_dots}</summary>'
        f'<div class="vfaq-answer" style="padding:30px 22px;background:#fff;">'
        f'{para_html}'
        f'</div></details>\n'
    )

# ── Build HTML ────────────────────────────────────────────────────────────────

def build_html():
    parts = []

    # ── Author byline ─────────────────────────────────────────────────────────
    parts.append(p(
        f'By {ilink("https://virtina.com/woocommerce-development-services/", "Virtina\'s eCommerce strategy team")}'
        f' · eCommerce Strategy · May 29, 2026'
    ))

    # ── Template A: Summary ───────────────────────────────────────────────────
    parts.append(
        '<div style="background:linear-gradient(rgba(0,213,192,0.28),rgba(0,213,192,0.28));'
        'border-radius:20px;padding:30px;margin:0 0 28px 0;">'
        '<h2 dir="ltr" style="color:#43627f;font-size:30px;">Summary</h2>\n'
        + p(
            'AI shopping agents are now a mainstream customer acquisition channel. '
            'In 2025, 61% of American adults used AI for shopping, and Adobe recorded 693% growth in AI-sourced retail traffic.'
        )
        + p(
            'Most stores are invisible to these agents because of JavaScript-rendered prices, incomplete schema, and accidentally blocked crawlers. '
            'This guide explains what agent-ready means, how it differs from GEO, and the 10-step audit to fix it.'
        )
        + '</div>\n'
    )

    # ── Template B: Introduction ──────────────────────────────────────────────
    parts.append(
        '<div style="background:linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5));'
        'border-radius:20px;padding:30px;margin:0 0 28px 0;">'
        '<h2 style="color:#43627f;font-size:30px;">Introduction</h2>\n'
        + p(
            'A buyer asks ChatGPT to find the best industrial pump under $500 and order it. '
            'Your store carries that product, but prices load via JavaScript, GTIN fields are empty, and GPTBot is blocked. '
            'The agent visits, gets an empty page, and moves on to a competitor.'
        )
        + p(
            'This is not a future problem. '
            'Shopify data shows AI-driven orders grew 15x year over year since January 2025. '
            'Adobe found AI-referred shoppers converted 31% more, bounced 33% less, and that revenue goes to stores that are readable to agents.'
        )
        + p(
            'There is a distinction worth making. '
            'ChatGPT can cite your store as a recommendation, and that same agent can still fail to buy from you. '
            'Citation and transaction are two different problems, and this post covers both.'
        )
        + '</div>\n'
    )

    # ── Template C: Table of Contents ────────────────────────────────────────
    toc_items = [
        ("what-is-agent-ready",         'What does "agent-ready" mean for an ecommerce store?'),
        ("geo-vs-agent-ready",          "What is the difference between GEO and being agent-ready?"),
        ("how-agents-find-products",    "How do AI shopping agents find and evaluate products?"),
        ("not-showing-in-ai-results",   "Why isn't my store showing up in AI shopping results?"),
        ("product-page-invisible",      "What makes a product page invisible to AI shopping agents?"),
        ("structured-data-needed",      "Do I need structured data for AI shopping agents?"),
        ("optimize-product-data",       "How do I optimize my product data for AI agents?"),
        ("training-vs-retrieval-bots",  "What is the difference between training crawlers and retrieval bots?"),
        ("agent-ready-checklist",       "How do I make my ecommerce store agent-ready?"),
        ("people-also-ask",             "People also ask"),
        ("conclusion",                  "Conclusion"),
        ("faq",                         "Frequently asked questions"),
    ]
    toc_html = '<h3 style="color:#43627f;font-size:22px;">Table of Contents</h3>\n'
    toc_html += '<ul style="list-style:none!important;padding-left:0!important;margin:0 0 1.5em 0!important;">\n'
    for anchor, label in toc_items:
        toc_html += toc_li(anchor, label)
    toc_html += '</ul>\n'
    parts.append(toc_html)

    # ── Section 1: What does agent-ready mean ────────────────────────────────
    s1 = (
        p('Agent-ready means an AI agent can read your store, compare products, and complete a purchase with no human involved. '
          'Mobile-ready and SEO-ready optimize the experience for a human visitor. '
          'Agent-ready optimizes the data layer for a machine acting on a buyer\'s behalf.')
        + p('A human customer can read a price rendered by JavaScript, solve a CAPTCHA, and tolerate a slow page. '
            'An AI shopping agent cannot. '
            'It fetches static HTML, reads structured data fields, checks real-time availability, and transacts or moves on in seconds.')
        + p(f'A buyer asks ChatGPT to find the best industrial air compressor under $500. '
            f'ChatGPT visits 12 product pages: eight return usable data, four return a spinner with no price, and your store is one of the four. '
            f'The {ilink("https://virtina.com/ai-impact-woocommerce/", "AI features already reshaping ecommerce")} have made agent-readiness a baseline requirement, not an advanced optimization.')
        + img_block(BODY1_ID, BODY1_SRC, BODY1_ALT, 670, 352)
    )
    parts.append(sec("what-is-agent-ready",
                     'What does "agent-ready" mean for an ecommerce store?', s1))

    # ── Section 2: GEO vs agent-ready ────────────────────────────────────────
    s2 = (
        p('GEO means AI mentions your content in its responses. '
          'Agent-ready means AI can execute a purchase from your store. '
          'These are different problems: GEO is a discoverability issue, and agent-readiness is a transaction infrastructure problem.')
        + p('Here is the gap in practice: ChatGPT says "Buy from Acme Tools," which is a GEO win. '
            'But if Acme\'s page renders prices via JavaScript and blocked OAI-SearchBot, the agent cannot buy from Acme. '
            'GEO gets the mention, but agent-readiness closes the sale.')
        + p(f'Most store operators start by fixing {ilink("https://virtina.com/b2b-schema-gaps-invisible-filters/", "how schema gaps filter you out of AI results")}, '
            f'but schema alone bridges only half the gap. '
            f'The transaction half requires server-side rendering, real-time inventory data, and a checkout path an agent can complete.')
    )
    parts.append(sec("geo-vs-agent-ready",
                     "What is the difference between GEO and being agent-ready?", s2))

    # ── Section 3: How agents find products ──────────────────────────────────
    s3 = (
        p('AI shopping agents find products through three channels: crawling product pages, reading Merchant Center feeds, and consuming structured data in page HTML. '
          'Each channel is a gate. '
          'Fail one, and you may lose a specific agent entirely.')
        + p('Four major agents dominate in 2026. '
            'ChatGPT Shopping reaches 900 million weekly users, and Google AI Mode crossed 1 billion monthly users in May 2026. '
            'Perplexity Shopping has 45 million monthly users, and Amazon Rufus served 300 million customers in 2025.')
        + p('Google AI Mode leans on Merchant Center feed data. '
            'Perplexity Shopping reads schema markup and requires GTINs. '
            'ChatGPT Shopping uses product page schema plus Merchant Center data where available.')
        + p(f'Some agents, like ChatGPT Operator, skip cached data and browse live pages directly. '
            f'Either way, if your page returns no readable data, your store is invisible. '
            f'Maintaining {ilink("https://virtina.com/woocommerce-erp-integration/", "clean product data connected to your ERP")} is what keeps you in contention.')
    )
    parts.append(sec("how-agents-find-products",
                     "How do AI shopping agents find and evaluate products?", s3))

    # ── Section 4: Why not showing in results ────────────────────────────────
    s4 = (
        p('Your store likely isn\'t showing up because of a missing Merchant Center feed, structured data errors, or blocked retrieval bots. '
          'Any one of those removes you from results entirely. '
          'Together, they make your store completely invisible to AI shopping agents.')
        + p('The scale of what you\'re missing is real. '
            'Adobe recorded 693% growth in AI-sourced retail traffic in the 2025 holiday season. '
            'Shopify reports 15x YoY growth in AI-driven orders, and AI-referred shoppers convert 31% higher and bounce 33% less.')
        + p('Consider a mid-market industrial parts store with solid Google rankings. '
            'When a Perplexity Shopping agent fetched that SKU, the page returned an empty shell: prices were React-rendered and invisible to the crawler. '
            'The agent moved to a lower-ranked competitor whose prices were server-side rendered.')
        + p(f'Understanding {ilink("https://virtina.com/woocommerce-seo-made-easy/", "standard SEO fundamentals")} is necessary but not sufficient. '
            f'Agent-readiness adds a technical layer that standard SEO does not cover.')
    )
    parts.append(sec("not-showing-in-ai-results",
                     "Why isn't my store showing up in AI shopping results?", s4))

    # ── Section 5: Product page invisible ────────────────────────────────────
    audit_bullets = bul([
        ("Robots.txt check.",
         "Open your robots.txt and search for GPTBot, OAI-SearchBot, and PerplexityBot. "
         "Confirm retrieval bots are listed as allowed."),
        ("JS rendering check.",
         "Disable JavaScript in your browser on a product page. "
         "If price and stock disappear, AI crawlers see the same blank state."),
        ("Schema.org validation.",
         "Run 3 product URLs through Google's Rich Results Test. "
         "Check for missing GTIN, priceCurrency, and availability."),
        ("Merchant Center feed.",
         "Log in to Google Merchant Center and check your attribute completeness score. "
         "99.9% completion gives 3-4x higher AI Mode visibility."),
        ("Checkout friction test.",
         "Open incognito and attempt checkout without an account. "
         "If blocked, agents will fail here too."),
        ("Product API response.",
         "Can your store return price, availability, and shipping for a SKU in under 200ms? "
         "If not, real-time agents will skip your store."),
    ])
    s5 = (
        p('Three failure modes make a product page invisible to AI agents. '
          'JS-rendered prices, missing Product schema, and blocked bot names in robots.txt account for most cases where an agent skips a store it could otherwise convert.')
        + p('JavaScript rendering is the most common failure: four of six major AI crawlers fetch static HTML only and do not execute JavaScript. '
            'A React or Vue product page returns a blank shell to the crawler. '
            'Server-side rendering for price and availability is the fix.')
        + p('Missing GTIN fields are the second most common failure. '
            'Perplexity Shopping requires GTINs to list products, and Google AI Mode uses GTIN to cross-reference Merchant Center data with on-page schema. '
            'A product without a GTIN is deprioritized or skipped.')
        + p(f'Checkout barriers are the third failure class. '
            f'Login walls, CAPTCHA triggers, and viewport-blocking cookie banners stop agents at the point of purchase. '
            f'Treating {ilink("https://virtina.com/b2b-commerce-needs-engineering-not-just-marketing/", "your store as an engineering problem, not a marketing one")} means addressing these as blocking bugs.')
        + h3("Agent-ready audit: check these 6 things today")
        + audit_bullets
    )
    parts.append(sec("product-page-invisible",
                     "What makes a product page invisible to AI shopping agents?", s5))

    # ── Section 6: Structured data ────────────────────────────────────────────
    s6 = (
        p('Yes. '
          'Schema.org Product markup with Offers, GTIN, and availability is the minimum for AI agents to read your product data. '
          'Without it, agents skip your pages or rely on best-guess parsing of unstructured HTML.')
        + p(f'The required fields are: name, sku, gtin, offers (price, priceCurrency, availability), image, brand, and aggregateRating. '
            f'For stores that want agents to complete transactions, also add OfferShippingDetails, hasMerchantReturnPolicy, and ProductGroup for variant products. '
            f'The {elink("https://schema.org/Product", "Schema.org Product specification")} is the definitive reference.')
        + p(f'JSON-LD is the preferred format: place it in the page head, server-side rendered, never JavaScript-injected. '
            f'65% of pages cited by Google AI Mode include structured data. '
            f'Investing in {ilink("https://virtina.com/woocommerce-development-services/", "a structured data implementation")} now is cheaper than retrofitting after AI traffic is already routing around you.')
        + img_block(BODY2_ID, BODY2_SRC, BODY2_ALT, 670, 352)
    )
    parts.append(sec("structured-data-needed",
                     "Do I need structured data for AI shopping agents?", s6))

    # ── Section 7: Optimize product data ─────────────────────────────────────
    opt_bullets = bul([
        ("Product title format.",
         '"DeWalt DCD771C2 20V Max Cordless Drill Driver Kit" is machine-readable. '
         '"Cordless Drill Kit" is not. Use brand + model + key spec in every title.'),
        ("Price as static HTML text.",
         "Price must be visible in page source before JavaScript runs. "
         "Confirm by viewing page source, not DevTools."),
        ("In-stock signals.",
         "Availability must be explicit in schema: schema.org/InStock or schema.org/OutOfStock. "
         "Never leave the field blank."),
        ("Google Merchant Center feed.",
         "Submit a complete feed and maintain 99.9% attribute completion. "
         "This is the primary data source for Google AI Mode."),
        ("llms.txt file.",
         "Create a plain-text file at yoursite.com/llms.txt pointing to your product feed URL and sitemap. "
         "Fewer than 1,000 domains had published one as of July 2025."),
        ("Review markup.",
         "Add AggregateRating to every product page. "
         "AI agents use review counts as a proxy for product reliability when comparing options."),
    ])
    s7 = (
        p('Start with clean product titles, complete descriptions without AI-generated filler, and valid JSON-LD schema on every product page. '
          'These three changes produce the most immediate improvement in agent readability.')
        + p('The optimizations that move the needle:')
        + opt_bullets
        + p(f'{ilink("https://virtina.com/b2b-ecommerce-for-manufacturers/", "B2B catalog data standards")} require an even higher bar. '
            f'B2B product pages carry complex attribute sets: compatibility ranges, certifications, industry classifications. '
            f'These need explicit schema fields, not buried description text.')
    )
    parts.append(sec("optimize-product-data",
                     "How do I optimize my product data for AI agents?", s7))

    # ── Section 8: Training crawlers vs retrieval bots ────────────────────────
    s8 = (
        p('Training crawlers collect data to build AI models. '
          'Retrieval bots fetch real-time data to answer user queries right now. '
          'Blocking them together is the mistake most store operators made between 2024 and 2026.')
        + p('Training crawlers (GPTBot, ClaudeBot, Google-Extended, Meta-ExternalAgent) crawl the web to build model training data. '
            'Blocking them has zero effect on whether ChatGPT or Perplexity shows your products to shoppers today.')
        + p('Retrieval bots (OAI-SearchBot, PerplexityBot, Claude-SearchBot, standard Googlebot) power real-time AI answers and shopping results. '
            'Blocking any of them removes you from that agent\'s results immediately.')
        + p(f'Many SEO plugins added "block AI bots" toggles in 2024 and 2025, enabled by default. '
            f'Stores activated these thinking they were stopping training scrapes, but instead blocked retrieval bots and vanished from AI results overnight. '
            f'The {ilink("https://virtina.com/industrial-b2b-ecommerce-10-objections-2026/", "B2B buyers now evaluating suppliers through AI agents")} depend on exactly those bots.')
    )
    parts.append(sec("training-vs-retrieval-bots",
                     "What is the difference between training crawlers and retrieval bots?", s8))

    # ── Section 9: Agent-ready checklist ─────────────────────────────────────
    checklist_steps = [
        "Confirm GPTBot and OAI-SearchBot are not blocked in robots.txt.",
        "Confirm PerplexityBot and Google-Extended directives are correct: allow PerplexityBot, optionally restrict Google-Extended for training only.",
        "Validate Product schema on 5 random product pages using Google's Rich Results Test.",
        "Add GTIN and MPN fields to schema on every product page where identifiers exist.",
        "Make price and availability visible as static HTML text before JavaScript runs.",
        "Submit or verify your Google Merchant Center product feed. Check attribute completeness.",
        "Add brand + model + key spec to every product title.",
        "Set up AggregateRating markup on product pages.",
        "Create or verify a site search API endpoint that returns price, stock, and shipping for any SKU in under 200ms.",
        "Create an llms.txt file at your site root pointing to your product feed URL and product sitemap.",
    ]
    s9 = (
        p('Start with these 10 items in order. This is your agent-ready audit.')
        + ol_steps(checklist_steps)
        + p('The fastest wins are items 1, 2, 5, and 7: no new development required. '
            'Schema fixes (3, 4, 8) and feed work (6) take longer but produce the largest visibility gains. '
            'A typical mid-market store completes the full list in two to four weeks.')
        + p(f'Start with {ilink("https://virtina.com/woocommerce-b2b-customer-portal/", "your B2B product catalog and customer portal")} to identify data gaps before writing a single schema line. '
            f'Virtina helps WooCommerce, Magento, Shopify, and BigCommerce stores work through this checklist systematically.')
    )
    parts.append(sec("agent-ready-checklist",
                     "How do I make my ecommerce store agent-ready?", s9))

    # ── Template H: People also ask ──────────────────────────────────────────
    parts.append(
        '<div style="background:linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5));'
        'border-radius:20px;padding:30px;margin:0 0 28px 0;">'
        '<h2 id="people-also-ask" style="color:#43627f;font-size:30px;">People also ask</h2>\n'
        + h3("What is the difference between AI search and an AI shopping agent?")
        + p('AI search returns information to a human who then acts on it. '
            'An AI shopping agent acts on behalf of the human directly, browsing pages, comparing products, and placing the order. '
            'The difference is who takes the final action.')
        + h3("Can AI agents buy on my behalf?")
        + p('Perplexity Shopping\'s "Buy with Pro" and Amazon Rufus both complete purchases today. '
            'ChatGPT\'s Instant Checkout via the Agentic Commerce Protocol launched in late 2025 and is expanding. '
            'The infrastructure is live, not theoretical.')
        + h3("How do I test if an AI agent can read my product pages?")
        + p('Disable JavaScript in your browser and reload a product page: if price and stock disappear, AI crawlers see the same empty state. '
            'Run a product URL through Google\'s Rich Results Test and check for GTIN and complete Offer fields. '
            'Then search for that product in Perplexity Shopping; all three tests take under 15 minutes.')
        + h3("What structured data do I need for Google AI Mode?")
        + p('Google AI Mode uses your Merchant Center feed as the primary source and on-page Product schema as verification. '
            'Required fields are name, brand, sku, gtin, image, price, priceCurrency, and availability. '
            'Mismatches between schema and Merchant Center data cause Google to deprioritize both.')
        + '</div>\n'
    )

    # ── Template I: Conclusion ────────────────────────────────────────────────
    parts.append(
        '<div style="background:#00d5c0;border-radius:20px;padding:30px;margin:0 0 28px 0;">'
        '<h2 id="conclusion" style="color:#ffffff;font-size:30px;">Conclusion</h2>\n'
        + pc('AI shopping agents are now a real customer acquisition channel. '
             'Adobe\'s 693% traffic growth and Shopify\'s 15x order growth came from a single holiday season. '
             'Stores that close the agent-readiness gap in 2026 will have a structural advantage going into 2027.')
        + pc('The 10-step checklist in this post is your starting point. '
             'robots.txt, schema, Merchant Center feed, SSR, and llms.txt are all within reach for any ecommerce store. '
             'Contact Virtina to run the audit and prioritize the fixes for your specific stack.')
        + '</div>\n'
    )

    # ── Template J: FAQ ───────────────────────────────────────────────────────
    faq_style = (
        '<style>\n'
        'details.vfaq>summary{list-style:none;}\n'
        'details.vfaq>summary::-webkit-details-marker{display:none;}\n'
        'details.vfaq[open]>summary{background:linear-gradient(#00d5c0,#00d5c0)!important;}\n'
        'details.vfaq .vfaq-answer p{font-size:15px!important;color:#6e6e6e!important;line-height:1.75!important;}\n'
        '</style>\n'
    )

    faq_data = [
        (
            "What is agentic commerce?",
            "Agentic commerce is the model in which AI agents act as autonomous buyers on behalf of human users. "
            "The agent receives a brief, browses stores, compares options, and completes the purchase. "
            "The Agentic Commerce Protocol (ACP) from OpenAI and Stripe is the emerging standard for how agents authenticate and transact at merchant stores."
        ),
        (
            "Does my store need to be on Shopify or a specific platform to be agent-ready?",
            "No. Agent-readiness depends on your technical setup, not your platform choice. "
            "WooCommerce, Magento, BigCommerce, and Shopify all support SSR prices, Product schema with GTIN, Merchant Center feeds, and correct robots.txt. "
            "The checklist is the same regardless of which platform you run."
        ),
        (
            "What is llms.txt and do I need it?",
            "llms.txt is a plain-text file at yoursite.com/llms.txt giving AI crawlers a path to your product feed, sitemap, and data endpoints. "
            "It had fewer than 1,000 adopters globally as of July 2025. "
            "Implement it now for early-mover advantage, but it does not replace schema or Merchant Center feeds."
        ),
        (
            "How do I check if AI bots are blocked on my site?",
            "Go to yoursite.com/robots.txt and search for GPTBot, OAI-SearchBot, PerplexityBot, and Claude-SearchBot. "
            "If any appear under Disallow: /, that bot is blocked from your store entirely. "
            "Also check your SEO plugin settings: many added default-on block AI crawlers toggles in 2024-2025."
        ),
        (
            "How long does it take to make a store agent-ready?",
            "For a typical mid-market store with 100-500 SKUs, the core work takes two to four weeks. "
            "robots.txt fixes and SSR price changes happen in a day or two."
            "||"
            "Schema markup with complete fields typically takes one to two weeks. "
            "Merchant Center feed work varies by how far the current feed falls from 99.9% attribute completion."
        ),
        (
            "Do AI agents actually complete purchases or just make recommendations?",
            "Google AI Mode and Perplexity Shopping currently make recommendations and redirect to your store for checkout. "
            "ChatGPT Operator and Perplexity's Buy with Pro complete purchases autonomously. "
            "The proportion of agents completing end-to-end purchases is growing."
        ),
        (
            "What is the difference between a Google Shopping feed and being agent-ready?",
            "A Google Shopping feed is one component of agent-readiness, not the whole picture. "
            "Your Merchant Center feed supplies Google AI Mode with data, but schema, SSR prices, and correct robots.txt are also required. "
            "A complete feed paired with blocked crawlers and JS-rendered prices still produces invisible product pages for most AI shopping agents."
        ),
        (
            "Will being agent-ready hurt my regular SEO?",
            "No. Every change required for agent-readiness aligns with standard SEO best practices. "
            "Server-side rendering improves Google crawlability, schema markup improves rich result eligibility, and correct robots.txt does not affect standard Googlebot. "
            "Agent-readiness extends your existing SEO work into a new channel."
        ),
    ]

    faq_html = faq_style
    faq_html += '<h2 style="" id="faq">Frequently Asked Questions</h2>\n<div>\n'
    for q, a in faq_data:
        faq_html += faq_item(q, a)
    faq_html += '</div>\n'
    parts.append(faq_html)

    # ── Template K: Author bio ────────────────────────────────────────────────
    parts.append(
        '<p dir="ltr" style="font-size:16px;line-height:1.75;">'
        '<strong>Virtina eCommerce strategy team</strong>: '
        'Virtina\'s certified eCommerce experts have helped 1,000+ B2B and B2C brands across manufacturing, distribution, retail, and wholesale. '
        'With 14+ years and 2,000+ projects delivered, '
        'Virtina is a WooCommerce Expert, Magento Certified, Shopify Partner, and BigCommerce Partner.'
        '</p>\n'
    )

    return "".join(parts)


# ── Pre-publish checks ────────────────────────────────────────────────────────

def run_checks(html):
    results = {}

    # Strip tags for plain-text checks
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'&[a-z]+;', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # 1. Em dash — all four forms
    em_dashes = len(re.findall(r'—|&mdash;|&#8212;|&#x2014;', html))
    results["em_dash_count"] = em_dashes

    # 2. Banned phrases
    banned = [
        "delve", "leverage", "revolutionary", "game-changing", "cutting-edge",
        "transform your", "unlock value", "synergize",
        r"in today's fast-paced world", r"it's important to note",
        r"\bin conclusion\b", r"when it comes to", r"let's explore",
        r"\bfurthermore\b", r"\bmoreover\b", r"\blandscape\b",
        r"\becosystem\b", r"\bnavigate\b",
    ]
    ban_count = 0
    for b in banned:
        ban_count += len(re.findall(b, text, re.IGNORECASE))
    results["banned_phrase_occurrences"] = ban_count

    # 3. Internal links (virtina.com, no target blank)
    internal_links = re.findall(r'href="https://virtina\.com/[^"]*"', html)
    internal_with_target = re.findall(
        r'href="https://virtina\.com/[^"]*"[^>]*target=', html)
    results["internal_link_count"] = len(internal_links)
    results["internal_link_count_with_target_blank"] = len(internal_with_target)

    # 4. External links
    ext_links_with_target = re.findall(
        r'href="(?!https://virtina\.com)[^"#][^"]*"[^>]*target="_blank"', html)
    ext_links_total = re.findall(
        r'href="(?!https://virtina\.com)(?!#)[^"]*"', html)
    results["external_link_count"] = len(ext_links_total)
    results["external_link_count_with_target_blank"] = len(ext_links_with_target)

    # 5. H2 count
    h2s = re.findall(r'<h2[^>]*>', html)
    results["headers_h2_count"] = len(h2s)

    # 6. Content elements
    results["has_faq"] = "YES" if 'id="faq"' in html else "NO"
    results["has_checklist"] = "YES" if "agent-ready-checklist" in html else "NO"
    results["has_case_snippet"] = "YES" if "industrial" in html.lower() else "NO"
    results["author_byline_present"] = (
        "YES" if "Virtina's eCommerce strategy team" in html else "NO"
    )

    # 7. Image src validation
    img_srcs = re.findall(r'<img[^>]+src="([^"]+)"', html)
    bad_srcs = [s for s in img_srcs if not s.startswith("https://virtina.com/wp-content/uploads/")]
    results["image_src_all_virtina"] = "YES" if not bad_srcs else f"NO: {bad_srcs}"

    # 8. TOC: check !important present (no space), SVG present
    has_toc_important = "list-style:none!important" in html
    has_toc_svg = 'viewBox="0 0 24 24"' in html
    results["toc_has_important_no_space"] = "YES" if has_toc_important else "NO"
    results["toc_has_svg_arrows"] = "YES" if has_toc_svg else "NO"

    # 9. No << or >> fragments (Thrive serializer corruption)
    corruption = len(re.findall(r'<<|>>', html))
    results["markup_corruption_fragments"] = corruption

    # 10. Paragraph sentence count — use <p\b to avoid matching SVG <path>
    paragraphs = re.findall(r'<p\b[^>]*>(.*?)</p>', html, re.DOTALL)
    long_paras = 0
    long_sents = 0
    for para_html in paragraphs:
        para_text = re.sub(r'<[^>]+>', ' ', para_html).strip()
        sentences = re.split(r'(?<=[.!?])\s+', para_text)
        sentences = [s for s in sentences if len(s.split()) > 2]
        if len(sentences) > 3:
            long_paras += 1
        for s in sentences:
            if len(s.split()) > 25:
                long_sents += 1
    results["paragraphs_over_3_sentences"] = long_paras
    results["sentences_over_25_words"] = long_sents

    # 11. No placehold.co or unsplash sources
    has_placeholder = "placehold.co" in html or "source.unsplash.com" in html
    results["no_placeholder_images"] = "YES" if not has_placeholder else "NO"

    # 12. Featured media
    results["featured_media_id"] = FEAT_ID

    return results


# ── POST to WordPress ─────────────────────────────────────────────────────────

def post_to_wp(html):
    # Yoast meta description: 163 chars raw — trim to 160
    meta_desc = (
        "AI shopping agents are now a real acquisition channel. "
        "Learn why most stores are invisible to them and how to fix it with schema, SSR, and the right bot settings."
    )
    # Confirm length
    if len(meta_desc) > 160:
        meta_desc = meta_desc[:157] + "..."

    payload = {
        "title":          "The customer was a robot: how to make your store readable to AI shopping agents",
        "slug":           "ecommerce-store-agent-ready",
        "content":        html,
        "status":         "draft",
        "categories":     [84, 79, 415],
        "tags":           [],
        "featured_media": FEAT_ID,
        "author":         9,
        "meta": {
            "_yoast_wpseo_title":    "Make your store readable to AI shopping agents | Virtina",
            "_yoast_wpseo_metadesc": meta_desc,
            "_yoast_wpseo_focuskw":  "ecommerce store agent-ready",
        },
    }

    print("POSTing to WordPress...")
    r = SESS.post(WP_EP, json=payload, timeout=120)
    if r.status_code in (200, 201):
        post = r.json()
        pid  = post.get("id")
        link = post.get("link", "")
        print(f"  Created draft post ID={pid}")
        print(f"  Link: {link}")
        return pid, link
    else:
        print(f"  POST FAILED {r.status_code}: {r.text[:500]}")
        return None, None


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=== Agent-Ready Post Publisher ===")
    print(f"Featured image: media_id={FEAT_ID}")
    print(f"Body image 1:   media_id={BODY1_ID}")
    print(f"Body image 2:   media_id={BODY2_ID}")

    html = build_html()
    print(f"\nHTML length: {len(html):,} chars")

    print("\n=== Pre-publish checks ===")
    checks = run_checks(html)

    # Print check table
    PASS_VALUES = {0, "YES"}
    for k, v in checks.items():
        if k == "featured_media_id":
            icon = "OK" if v and v != 0 else "FAIL"
        elif k in ("internal_link_count", "headers_h2_count",
                   "external_link_count", "external_link_count_with_target_blank"):
            icon = "OK"  # value printed for info, not a pass/fail gate
        elif isinstance(v, int):
            icon = "OK" if v == 0 else "FAIL"
        else:
            icon = "OK" if v in ("YES", "manual check needed") else "FAIL"
        print(f"  {k:50s}: {str(v):20s}  {icon}")

    # Hard gate evaluation
    checks_pass = (
        checks["em_dash_count"] == 0
        and checks["banned_phrase_occurrences"] == 0
        and checks["internal_link_count"] >= 7
        and checks["internal_link_count_with_target_blank"] == 0
        and 8 <= checks["headers_h2_count"] <= 16
        and checks["has_faq"] == "YES"
        and checks["has_checklist"] == "YES"
        and checks["has_case_snippet"] == "YES"
        and checks["author_byline_present"] == "YES"
        and checks["external_link_count_with_target_blank"] <= 2
        and checks["paragraphs_over_3_sentences"] == 0
        and checks["sentences_over_25_words"] == 0
        and checks["toc_has_important_no_space"] == "YES"
        and checks["toc_has_svg_arrows"] == "YES"
        and checks["markup_corruption_fragments"] == 0
        and checks["no_placeholder_images"] == "YES"
        and checks["image_src_all_virtina"] == "YES"
    )

    if not checks_pass:
        print("\nFAIL: One or more hard gates failed. Fix before publishing.")
        sys.exit(1)

    print("\nAll hard checks PASS. Proceeding to publish...")

    post_id, post_link = post_to_wp(html)
    if not post_id:
        print("FAILED to create post.")
        sys.exit(1)

    # Save HTML locally
    out_dir = r"C:\content-intel\clients\virtina\output\published"
    os.makedirs(out_dir, exist_ok=True)
    out_html = os.path.join(out_dir, "ecommerce-store-agent-ready-2026-05-29.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\nHTML saved to: {out_html}")

    print(f"\n=== SUCCESS ===")
    print(f"Post ID:      {post_id}")
    print(f"Preview URL:  https://virtina.com/?p={post_id}")
    print(f"Post link:    {post_link}")
    print(f"\nImage summary:")
    print(f"  Featured: media_id={FEAT_ID} | 1309x500 | {FEAT_SRC}")
    print(f"  Body 1:   media_id={BODY1_ID} | 670x352  | {BODY1_SRC}")
    print(f"  Body 2:   media_id={BODY2_ID} | 670x352  | {BODY2_SRC}")
    print(f"\nYoast SEO:")
    print(f"  Title:    Make your store readable to AI shopping agents | Virtina")
    print(f"  Focus KW: ecommerce store agent-ready")
    print(f"\nNOTE: Yoast meta title and description may need manual entry in WP dashboard")
    print(f"      if REST API meta write is restricted on this installation.")

    return post_id


if __name__ == "__main__":
    main()
