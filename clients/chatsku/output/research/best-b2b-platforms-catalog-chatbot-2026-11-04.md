---
title: Research notes, Best B2B Store Platforms for a Catalog Chatbot
client: chatsku
date: 2026-11-04
topic: Best B2B Store Platforms for a Catalog Chatbot: Shopify, BigCommerce, WooCommerce and Magento
audience: B2B manufacturers, distributors and wholesalers choosing or running an online store platform
stage: research
slug: best-b2b-platforms-for-catalog-chatbot
---

Rules applied: no em dashes, quotes under 15 words, no stats or market share used (none verified at source), competitor chatbot vendors not named. Fetch method: WebFetch (page text is summarised by a small model, so treat quotes as "as returned" and re-check exact wording before publishing any quote).

## A. What ChatSKU itself states (all vendor claims, from chatsku.com)

### A1. Platform pages that exist
- Shopify: https://chatsku.com/shopify-b2b-chatbot/ (200). Title: "Shopify B2B Chatbot for Manufacturers and Distributors - ChatSKU"
- BigCommerce: https://chatsku.com/bigcommerce-b2b-chatbot/ (200). 
- Magento: https://chatsku.com/magento-b2b-chatbot/ (200). Title: "Magento B2B Chatbot Extension for Magento 2 & Adobe Commerce | ChatSKU"
- WooCommerce: NO standalone platform page in the site nav (home nav lists only Magento, BigCommerce, Shopify). https://chatsku.com/woocommerce-b2b-chatbot/ returns a page titled "WooCommerce B2B Chatbot Buyer's Checklist | ChatSKU" (same as post 3305). It is probably a redirect to /woocommerce-b2b-chatbot-buyers-guide/ [unverified]. Safe WooCommerce links are the three blog posts: /b2b-chatbot-for-woocommerce/, /woocommerce-b2b-chatbot-integration/, /woocommerce-b2b-chatbot-buyers-guide/. The brief's phrase "platform pages for ... WooCommerce" is therefore only half true: WooCommerce has posts, not a solutions page.
- RFQ page: /rfq-automation-for-product-catalogs/ is in the nav but MUST-FOLLOW-RULES says it serves homepage content. Do not link. Use /rfq-automation-manufacturers/.
- Pricing page: https://chatsku.com/chatsku-pricing/ (200, live). MUST-FOLLOW-RULES still says /pricing/ is dead and "no standalone pricing page". That rule is STALE for /chatsku-pricing/ (it is in the home nav and footer). Flag to orchestrator; rules file needs updating before anyone links it.

### A2. Home page https://chatsku.com/
- Install: "1 Line of Code to Deploy"; "If you can paste text, you can deploy ChatSKU" (paraphrase of: one line, works on any website).
- Setup time: "< 1 Day Average Setup Time"; "Most teams go live the same day they sign up."; "We set it up. You review it. Takes a day."
- Ingest: "Send us your catalog. PDF, Excel, whatever you have."; also "your existing PDF, Excel, or store catalog". Customers via CSV import (name, email, phone).
- Sync: "Connect your CRM, eCommerce platform, or ERP" with automatic sync. No systems named on this page.
- Customer groups: "Organize buyers into custom groups." Sample groups on the page are illustrative UI (do not reuse the sample percentages as claims).
- Tiered pricing: "Set group-specific pricing and discounts per product." Listed as "first-class".

### A3. /demo/ https://chatsku.com/demo/
- "~4 hours Average setup time"; "1 line Of code to embed"; "One line of code, one day."
- Does NOT mention ingestion formats, customer groups or tiered pricing.

### A4. /features/ https://chatsku.com/features/
- "One line of code, one day."; "Most teams go live in under 4 hours."
- Ingestion, customer groups, tiered pricing, RFQ detail: NOT CONFIRMED on this page (links out only).

### A5. Magento page https://chatsku.com/magento-b2b-chatbot/
- Connection: reads "your Magento catalog through the standard Magento REST API." "Nothing to install in Magento itself."
- Editions: Magento Open Source and Adobe Commerce, on-premises and Adobe Commerce Cloud.
- Ingest: "indexes every Magento product, every variant, every customer-group price." Syncs catalog, customer groups, tier pricing, inventory, in real time, no nightly jobs.
- B2B: "Respects Magento customer groups, shared catalogs, and tier pricing rules." For Adobe Commerce: company accounts, shared catalogs, customer-group pricing, negotiable quotes.
- Install: single script tag in theme footer or CMS block; no Composer, no core files.
- Setup: "Most Magento and Adobe Commerce merchants are live the same day." FAQ: config and code install "under an hour" for a typical B2B store. Team training "under 30 minutes".

### A6. Shopify page https://chatsku.com/shopify-b2b-chatbot/
- Connection: "Authorize ChatSKU with your Shopify store through API authentication." Reads products, variants, inventory "through the Storefront API."
- B2B: "Reads companies, catalogs, and price lists for logged-in B2B buyers." Also "volume tiers". Supports Shopify Plus B2B, Online Store 2.0, legacy Liquid themes, Hydrogen.
- Quotes: "Pushes complete quote requests to your team, your CRM, or draft orders." Fields stated: product, quantity, company account, catalog.
- Install: embed script in theme or Hydrogen app, "That is the whole install." No app install or theme rewrite.
- Setup: "Most merchants launch the same day." Training under 30 minutes.
- NOT CONFIRMED on page: metafields, customer-group configuration, which Shopify plan is required.

### A7. BigCommerce page https://chatsku.com/bigcommerce-b2b-chatbot/
- Connection: reads catalog "through the BigCommerce Storefront API and B2B Edition API." Mirrors catalog, company accounts, price lists, inventory, "in real time."
- Install: one script tag, "Paste one line into your BigCommerce theme." Works on Stencil, headless, Catalyst.
- Setup: same day; config and code "under an hour"; catalog sync minutes to hours by size; training under 30 minutes.
- Quotes arrive "with product, quantity, company account, and price list applied"; pushed into B2B Edition (workflow detail not stated).
- INTERNAL CONTRADICTIONS ON THIS PAGE: (1) a block says "Magento customer groups" on a BigCommerce page (looks like a copy error); (2) "No theme to modify" vs "Paste one line into your BigCommerce theme." Do not repeat either claim. Recommend the client fix the page.
- Tiered pricing: not described in detail on page.

### A8. WooCommerce (blog posts, not a platform page)
- Post 685 https://chatsku.com/b2b-chatbot-for-woocommerce/: works "on top of WooCommerce and your B2B plugins." Reads SKUs, variants, custom attributes, stock and plugin pricing rules. Data via WooCommerce product CSV export, direct connection, or REST sync; also CSV/PDF upload. One script tag in theme or via plugin.
- Buyer's guide (3305) says ChatSKU "connects to the core WooCommerce API plus whichever plugin layer is active." B2BKing and Wholesale Suite: "confirmed through documented REST access." WholesaleX and Addify: no dedicated API, read through underlying product data, "unconfirmed by either vendor." So per-plugin tier reading is NOT CONFIRMED for every plugin.

### A9. Pricing page https://chatsku.com/chatsku-pricing/ (new fact, high relevance)
- Three models: Free Trial, Subscription, Performance Based.
- The Free Trial is stated to LACK "customer groups and tiered pricing" and "ERP/eCommerce/PIM integration" (as returned). The paid plans include them. This matters: any claim that ChatSKU reads customer-specific prices or syncs a store must be framed as paid-plan capability, not trial capability. Do not state prices in the post unless the user approves (page shows a setup fee and monthly figure; cite only if cleared).
- Setup: trial setups "typically same-day"; professional implementations "1-3 business days depending on catalog size and complexity."

### A10. CONTRADICTIONS on setup time (record verbatim, pick one safe phrasing)
| Page | Wording |
|---|---|
| Home | "< 1 Day Average Setup Time"; "Takes a day" |
| /demo/ and /features/ | "~4 hours" / "under 4 hours" |
| Platform pages (Magento, BigCommerce, Shopify) | "same day"; config "under an hour" |
| Pricing FAQ | trial "same-day"; professional "1-3 business days" |
| Woo post 685 and buyer's guide | "under a day" / "under 4 hours" (the guide itself notes the mismatch) |
Safe phrasing for the post: "most teams go live the same day" (consistent with home, Magento, BigCommerce, Shopify and pricing trial). Avoid "4 hours" and "1 to 3 days" in the same post.

## B. Platform facts verified at the source

### Shopify
- B2B plan availability: "Shopify B2B is available on the Basic, Grow, Advanced, and Shopify Plus plans" (not Starter or Retail). Source: https://help.shopify.com/en/manual/b2b . Per-plan feature split sits on a separate page I could not read, so exact features per plan = NOT CONFIRMED.
- Native: each B2B customer is set up as a company; catalogs customise pricing, currency, products, payment and shipping methods per customer. Source: same page.
- Catalogs: include/exclude products, percentage adjustments or fixed prices; Basic/Grow/Advanced limited to 3 active catalog assignments; Plus has no limit and can assign catalogs directly to company locations. Quantity rules and volume pricing exist; plan split not stated. Source: https://help.shopify.com/en/manual/b2b/catalogs
- API: Admin GraphQL API holds Company, CompanyLocation, CompanyContact, Catalog objects. Access to B2B resources limited to dev stores, Plus Partners and affiliates per that page. Source: https://shopify.dev/docs/apps/build/b2b . Price list and webhooks not covered on that page.
- Storefront API B2B: `@inContext` directive takes a `buyer` argument (customer access token plus company location ID); products available; metafields readable only with token auth. Source: https://shopify.dev/docs/api/storefront
- Custom fields: metafields are key-value pairs on any resource incl. products; Storefront API exposure needs the definition set to PUBLIC_READ (app-owned default hides them). Source: https://shopify.dev/docs/apps/build/custom-data/metafields
- Webhooks: near-real-time event delivery; `products/create` named; `products/update` implied. Source: https://shopify.dev/docs/apps/build/webhooks
- Not verified: Shopify Plus vs lower-plan price-list behaviour; "quotes" native status (the B2B overview does not mention quotes).

### BigCommerce
- Webhooks documented, light payloads (id and type), callbacks need a follow-up GET; subscription via v3 hooks endpoint. Product event names not on that page. Source: https://docs.bigcommerce.com/docs/integrations/webhooks
- Price lists: assignable to a customer group via Control Panel or Customer Groups API (discount rule type `price_list`); a variant with a price record ignores product-level bulk pricing in the cart; bulk upsert up to 1,000 price records per call. Source: https://docs.bigcommerce.com/docs/store-operations/pricing/price-lists
- Plan gating (customer groups on Growth+, price lists on the top tier, BigCommerce renamed plans June 1 2026: Standard to Core, Plus to Growth, Pro to Scale, Enterprise to Performance): came from search-result snippets of support.bigcommerce.com and bigcommerce.com pages. I could NOT open them (support article returned only a CSS error shell; pricing page 403). Mark as [unverified]; leave plan-tier names and prices out of the post, or say "price lists depend on plan, check BigCommerce".
- B2B Edition: companies linked to customer groups; shared account entities. Official B2B Edition overview page returned 404 on the path tried, so native-vs-paid status of B2B Edition = NOT CONFIRMED here. ChatSKU's own page treats B2B Edition as the data source. brand.md lists "BigCommerce B2B Edition" as a competitor-feature to not cite or link; mention by plain name only if needed.
- Custom fields and product API: docs path 404'd. Product custom fields on BigCommerce = NOT CONFIRMED by me.

### WooCommerce
- REST API v3 products resource includes `attributes` (id, name, position, visible, variation, options) and `meta_data` (id, key, value). Source: https://developer.woocommerce.com/docs/apis/rest-api/v3/products/
- Store API: public, unauthenticated reads of products, attributes, categories, brands, reviews; namespace wc/store/v1, v1 only version. Source: https://developer.woocommerce.com/docs/apis/store-api/
- Webhooks: native, product add/edit/delete topics selectable in admin; auto-disable after more than five consecutive failures. Source: https://woocommerce.com/document/webhooks/
- Tiered B2B pricing: I found NO official core document that states core lacks it. What is verified: every tiered or wholesale pricing offering found is a separate paid extension on woocommerce.com (e.g. B2B & Wholesale Suite by WebWizards, which lists group prices, quantity tiers, CSV import: https://woocommerce.com/products/b2b-wholesale-suite/; also B2B for WooCommerce, Wholesale Pricing by Addify, and the official Dynamic Pricing extension: https://woocommerce.com/document/woocommerce-dynamic-pricing/). Safe wording: "tiered and customer-group pricing comes from extensions, so the chat must read whichever one you run." Do not assert "core has no tier pricing" as a documented fact; present it as "in core, the documented route is extensions" [partly inferred].
- Status 2026: nothing verified beyond REST v3 and Store API v1 being current. Do not make status claims.

### Adobe Commerce / Magento
- B2B features (Adobe Commerce B2B): company accounts, company hierarchy, shared catalogs, quick order, negotiable quotes, requisition lists, purchase order approvals. B2B described as an extension installed in an Adobe Commerce store. Source: https://experienceleague.adobe.com/en/docs/commerce-admin/b2b/introduction . Whether Open Source includes B2B: NOT stated there; the page says shared catalogs and negotiable quotes need stores "configured to support company accounts." Post 3066 on ChatSKU answers the Open Source question already.
- Shared catalogs: one public catalog plus unlimited custom catalogs visible only to assigned company associates; custom shared-catalog pricing overrides customer-group pricing. Source: https://experienceleague.adobe.com/en/docs/commerce-admin/b2b/shared-catalogs/catalog-shared
- Tier pricing: quantity discounts; scope can be website, customer group, or shared catalog (shared catalogs need B2B); fixed price or percent off base Price. Source: https://experienceleague.adobe.com/en/docs/commerce-admin/catalog/products/pricing/product-price-tier
- Structured fields: Magento product attributes exist; I did not fetch the attributes doc, so cite only via ChatSKU's own claims or leave out. NOT CONFIRMED here.
- REST API and webhooks: ChatSKU states REST API reads; Adobe's own REST/webhook docs not fetched = NOT CONFIRMED by me.
- Status 2026: Adobe lifecycle policy table lists Adobe Commerce 2.4.9 (GA May 12, 2026, standard support to May 31, 2029) and 2.4.8 (GA April 8, 2025, to May 31, 2028). Page covers Adobe Commerce only, not Open Source. Source: https://experienceleague.adobe.com/en/docs/commerce-operations/release/planning/lifecycle-policy . A search result also showed Open Source 2.4.8 release notes exist at experienceleague.adobe.com (not fetched). Open Source patch-floor wording differed between two Adobe bulletins in search snippets; do not state any version floor.

## C. Volusion and older platforms

Verified (primary):
- Volusion status page https://status.volusion.com/ on 2026-11-04: "All Systems Operational"; latest entries are Oct 2026 maintenance and a PHP vulnerability mitigation (CVE-2026-109618/109619), no signs of exploited stores per Volusion. So Volusion is operating, not shut down. No end-of-life or mandatory migration notice found anywhere in primary sources.
- Product export: Volusion help center says Inventory > Import/Export > Standard Export lets you export Products to CSV with chosen columns (https://help.volusion.com/s/allaboutimportexport and related help.volusion.com pages, via search; exact file not opened). Volusion API section exports products as XML, 100 products at a time (via search snippet; not opened). Virtual columns are read-only. Treat as "CSV and XML export exist" and leave the rest out.
- Store-count numbers (StoreLeads etc.) appeared in search but are third-party and unverified. DO NOT use any Volusion store counts or decline figures.
- Migration pressure is commercial: agency and competitor posts say leave; none are official. Do not claim Volusion is dying.

Why older platforms are hard for a chat to read: I have no primary source that says so for Volusion specifically. What can be said safely: (1) product data comes out as CSV or XML export, which a chat can ingest as a file, same as any CSV; (2) whether specs live in structured columns or inside a description blob depends on the store, so check yours. The claim "no modern API" is NOT CONFIRMED (Volusion has a documented XML API). Frame the older-platform section around the catalog data and speed, not around API absence. ChatSKU's own site says it ingests "PDF, Excel, or store catalog," so an older store's export can still be ingested; that is a vendor claim from the home page.

Virtina pages (WebFetch, 2026-11-04):
- https://virtina.com/volusion-migration-services/ : loaded, real page, no error. Title: "Volusion Migration Services | Move Your Store Safely | Virtina". H1: "Don't Get Stuck! Escape Volusion's Limitations and Elevate Your eCommerce Empire". Says it migrates from Volusion to Shopify, WooCommerce, Magento, BigCommerce and others, covering products, customer data, purchase history. Its own limitation: customer passwords cannot move because they are encrypted. Contains timeline ranges, a "guarantee" wording, "ISO 9001:2015" logo alt text and unnamed testimonials. Use NONE of these claims in the ChatSKU post (rules: no timelines, results, guarantees). Cite only: Virtina migrates Volusion stores, link anchor "migration services".
- https://virtina.com/ecommerce-platforms-comparison/ : loaded, real full article. Title: "WooCommerce Vs. Magento Vs. BigCommerce Vs. Shopify (2026) | Virtina". H1: "WooCommerce Vs. Magento Vs. BigCommerce Vs. Shopify: A Comprehensive Comparison Guide (Updated 2026)". Wording: builds and supports stores on those four platforms; "more than 2,500 eCommerce projects, including platform migrations."
- Both pages should be linked from ChatSKU once each, far apart, per the brief. Rules in Template B: mention 14 years and 2,500+ once. The comparison page confirms 2,500; "14 years" comes from the user's brief only.
- Note: the comparison page is a Virtina B2C/B2B generic comparison; ChatSKU brand.md says avoid "generic ecommerce platform comparisons not tied to B2B catalog/quote workflows". The ChatSKU post must stay tied to catalog/quote needs.

## D. Uniqueness (body-level, from corpus headings 2026-11-02 plus live /blog/ of 2026-11-04)

Live blog newest first (checked 2026-11-04): is-your-b2b-catalog-ready-for-ai-chatbot (Nov 3), inquiry-tracking-seven-day-count, ai-sales-agent-vs-chatbot-vs-sales-rep, part-number-cross-reference, trade-show-booth-catalog-assistant, who-b2b-catalog-assistant-is-built-for, bigcommerce-chatbot-quoting, chatgpt-vs-catalog-chatbot, woocommerce-b2b-chatbot-buyers-guide, minimum-order-quantity-b2b. Blog 1 is already live (the brief said Nov 10 scheduled; it was published Nov 3). Blog is 5 pages; I read page 1 only.

Existing posts that touch platforms or "what a chat needs from the platform":
| Post | Slug / URL | Overlapping headings |
|---|---|---|
| 3305 | /woocommerce-b2b-chatbot-buyers-guide/ | h2 "Does the vendor's demo ever touch your actual pricing plugin?"; h3 "Do I need a different chatbot for WooCommerce than for Shopify or Magento?" (one-question answer that already compares platforms in passing) |
| 685 | /b2b-chatbot-for-woocommerce/ | "What about WooCommerce B2B plugins?"; "Is your WooCommerce store ready for a B2B chatbot?" |
| 1455 | /woocommerce-b2b-chatbot-integration/ | "What does ChatSKU read from the core WooCommerce REST API?"; "What does 'integrating with WooCommerce B2B' actually connect to?" |
| 1056 | /magento-b2b-chatbot-integration/ | "What Magento B2B data does ChatSKU read?"; "Does ChatSKU replace Adobe Commerce B2B features?"; "Is your Magento B2B store ready for ChatSKU?" |
| 3066 | /magento-b2b-extensions/ | "Customer-group and tier-pricing extensions"; "Is customer-group pricing part of the paid B2B module?"; "Can Magento Open Source support company accounts and shared catalogs?" (Magento native-vs-add-on is TAKEN) |
| 3767 | /bigcommerce-chatbot-quoting/ | "What does an AI catalog assistant need before it can quote?"; "Can a chatbot show the right price for each customer group?" (BigCommerce quote start point TAKEN) |
| 3039 | /one-catalog-a-thousand-prices-making-tiered-b2b-pricing-work-online/ | "Customer-specific price lists"; "Tiered and volume pricing"; "ERP e-commerce integration" (tier pricing as a concept TAKEN, platform-agnostic) |
| 2044 | /one-line-of-code/ | h2 "Does it matter which platform your site runs on?" |
| 2684 | /erp-export-ai-agent-ready/ | ERP-export field-level checks (tier pricing, UOM, GTIN) TAKEN |
| Blog 1 | /is-your-b2b-catalog-ready-for-ai-chatbot/ | h2s "Check 2: Are your specs in fields or hidden in PDFs?", "Check 4: Does the store load fast and work on a phone?", "What if the store itself needs work?"; FAQ "Does it work with my store platform?" names the four platforms in one line only |
| 353 / 294 | /what-is-a-b2b-catalog-chatbot/, /best-b2b-catalog-chatbots-2026/ | evaluation criteria and vendor comparison (not platform comparison) |
| 2974 | era-07 deep dive | "What can a fully built B2B eCommerce platform still not answer?" (tool-page framing) |

TAKEN angles: single-platform integration how-tos (Woo x3, Magento x2, BigCommerce quoting); Magento native vs extension map; WooCommerce plugin-layer evaluation; tiered pricing as a concept; vendor roundup; field-readiness of the catalog (Blog 1).
Risk: Blog 1's "specs in fields vs PDFs" and "What if the store itself needs work?" overlap the proposed section 1 and the Volusion section. Section 1 of Blog 2 must be about platform capabilities (customer-specific price rules, API/webhook access, structured product fields), NOT catalog hygiene; the Volusion section must not repeat Blog 1's "store needs work" advice.
OPEN angle (CONFIRMED by evidence): no ChatSKU post compares Shopify, BigCommerce, WooCommerce and Magento side by side, and none frames the comparison around what a catalog assistant needs FROM the platform (structured fields, customer-specific price rules, API/webhook access, quote handoff). Only 3305's single H3 touches cross-platform, and Blog 1 mentions the four in one FAQ line. Note brand.md "Themes to avoid" says generic platform comparisons not tied to B2B catalog/quote workflows: the angle must stay tied to catalog and quote workflows to be on brand.
Caveat: only the first blog page and the Nov 2 corpus were checked; 10 of 46 draft files and several posts (3461, 3848, 3956) have empty heading entries in the corpus, so I could not body-check them for platform content. Run an 8-gram check at draft time against the full corpus (MUST-FOLLOW rule 1D), especially vs 3767, 1056, 1455, 3066, 3305, where platform wording is reused.

## E. Verified live internal links (WebFetch returned page content, 2026-11-04)
Anchors 2 to 5 words naming the destination topic.
1. https://chatsku.com/shopify-b2b-chatbot/ , title "Shopify B2B Chatbot for Manufacturers and Distributors - ChatSKU" , anchor "Shopify B2B page"
2. https://chatsku.com/bigcommerce-b2b-chatbot/ , BigCommerce platform page , anchor "BigCommerce B2B page"
3. https://chatsku.com/magento-b2b-chatbot/ , "Magento B2B Chatbot Extension for Magento 2 & Adobe Commerce | ChatSKU" , anchor "Magento B2B page"
4. https://chatsku.com/b2b-chatbot-for-woocommerce/ , "How to Add a B2B Chatbot to WooCommerce Store | ChatSKU" , anchor "WooCommerce setup guide"
5. https://chatsku.com/woocommerce-b2b-chatbot-integration/ , "ChatSKU WooCommerce B2B Integration Guide | ChatSKU" , anchor "WooCommerce integration guide"
6. https://chatsku.com/woocommerce-b2b-chatbot-buyers-guide/ , "WooCommerce B2B Chatbot Buyer's Checklist | ChatSKU" , anchor "WooCommerce buyer's checklist"
7. https://chatsku.com/magento-b2b-extensions/ , "Magento B2B Extensions: What You Need | ChatSKU" , anchor "Magento B2B extensions" (published; live 200, rules file still says draft: stale)
8. https://chatsku.com/magento-b2b-chatbot-integration/ , "Magento 2 AI Chatbot: Setup Guide for B2B Stores | ChatSKU" , anchor "Magento setup guide"
9. https://chatsku.com/bigcommerce-chatbot-quoting/ , "BigCommerce B2B Quote Requests: Form, Chat or AI | ChatSKU" , anchor "BigCommerce quote requests"
10. https://chatsku.com/one-catalog-a-thousand-prices-making-tiered-b2b-pricing-work-online/ (canonical long slug; short slug redirects) , "Tiered B2B Pricing: One Catalog, Many Price Lists | ChatSKU" , anchor "tiered B2B pricing"
11. https://chatsku.com/erp-export-ai-agent-ready/ , "Is Your ERP Export AI-Ready? 10-Min Check | ChatSKU" , anchor "ERP export check"
12. https://chatsku.com/what-is-a-b2b-catalog-chatbot/ , "What is a B2B Catalog Chatbot? Complete 2026 Guide | ChatSKU" , anchor "B2B catalog chatbot guide"
13. https://chatsku.com/one-line-of-code/ , "One Line of Code, Explained | ChatSKU" , anchor "one line of code"
14. https://chatsku.com/is-your-b2b-catalog-ready-for-ai-chatbot/ , Blog 1 (live per /blog/ index; page opened) , anchor "catalog readiness checklist"
15. https://chatsku.com/best-b2b-catalog-chatbots-2026/ , "Best B2B Catalog Chatbots 2026: 7 Compared (RFQ, Pricing)" , anchor "catalog chatbot comparison" (note: that post names competitors, link is allowed but low priority)
16. https://chatsku.com/ai-product-search-for-b2b/ , "AI Product Search for B2B Catalogs, No Replatform - ChatSKU" , anchor "AI product search"
17. https://chatsku.com/maturity-calculator/ , "Maturity Calculator - ChatSKU" (H1 "Catalog Maturity Index") , anchor "catalog maturity calculator"
18. https://chatsku.com/roi-calculator/ , "ROI Calculator - ChatSKU" , anchor "ROI calculator"
19. https://chatsku.com/demo/ and https://chatsku.com/features/ and https://chatsku.com/chatsku-pricing/ (all opened, 200). Pricing link: rules file says no pricing page; reality differs; get user OK before using.
Not re-fetched this session (listed in home nav so exist): /signup/, /faq/, /for-b2b-manufacturers-distributors-and-wholesalers/.
Link count caution: rules cap external links at 2; the two Virtina links are external (virtina.com), so no other external link is allowed.

## F. Competitive scan (search-result level only; I did not open the pages)
- "best B2B ecommerce platform": top results are roundups from software-review sites, agencies and vendor blogs. Common set: Adobe Commerce, BigCommerce, Shopify Plus, NetSuite SuiteCommerce, plus enterprise names. Coverage is features, pricing, "best for" labels. Several carry old dates (2022 to 2025) or affiliate disclosures. Gap: nothing is framed by what a conversational catalog layer needs from the platform.
- "B2B ecommerce platform comparison Shopify BigCommerce WooCommerce Magento": results are agency and extension-vendor comparisons, many dated 2021 to 2024. Common claim: BigCommerce and Magento have stronger native B2B, Shopify and WooCommerce lean on apps. That claim is agency-sourced; the official docs above confirm Adobe Commerce B2B natives (shared catalogs, company accounts, tier prices) and Shopify B2B (companies, catalogs) natively on several plans, so the "Shopify needs apps" generalisation is out of date for basic company/catalog pricing. Do not repeat it. Market-share and monthly-price numbers appear in these pages and are unverified; skipped.
- "B2B ecommerce chatbot platform": results are partner-agency listing pages and general chatbot guides focused on order status, cart recovery, support. They discuss integrations loosely ("connect to your CRM and ERP"). Gap: none ties chat quality to platform features such as company-specific price lists, product field structure or API access. Competitor chatbot vendors are excluded from this file by instruction; the banned names (Drift, Intercom, Tidio, LiveChat, Zendesk) were excluded and not researched.
- Structure norms across top pages: feature table, "best for" verdicts, pros and cons. Gap for ChatSKU: a decision lens based on data the chat will read.

## Recommended angle and structure notes
Thesis: pick the platform on what the store hands to the chat, not on the chat. Four checks per platform: where customer-specific prices live and how they are read, whether product specs are structured fields, whether there is a product API with change events (webhooks), and what B2B is native vs add-on. Fits Format D (decision playbook) or B. User's outline sections 1 to 7 fit this.

## Factual conflicts and gaps to resolve before drafting
1. Setup time: 4 hours vs under a day vs 1 to 3 business days (see A10). Use "same day".
2. /pricing/ dead per rules vs /chatsku-pricing/ live. Free trial excludes customer groups, tiered pricing and store integration per pricing page; do not imply trial includes them.
3. BigCommerce page has copy errors (Magento groups; "no theme to modify"). Do not echo.
4. No WooCommerce solutions page; only blog posts. Outline section 5 ("existing ChatSKU platform pages") must link posts for WooCommerce.
5. Blog 1 already live, which the brief treated as upcoming.
6. NOT CONFIRMED by me from official docs: BigCommerce plan gating and B2B Edition native/paid status; BigCommerce and Magento product custom fields; Magento REST and webhook docs; Shopify per-plan B2B feature split and price lists; WooCommerce core lacking tier pricing as a stated fact; WooCommerce 2026 status; any Volusion "no modern API" claim.
7. Numbers: none used. Pricing figures, plan prices, market shares, store counts, and the Virtina timelines were all deliberately left out.

## Sources
- https://help.shopify.com/en/manual/b2b
- https://help.shopify.com/en/manual/b2b/catalogs
- https://shopify.dev/docs/apps/build/b2b
- https://shopify.dev/docs/api/storefront
- https://shopify.dev/docs/apps/build/custom-data/metafields
- https://shopify.dev/docs/apps/build/webhooks
- https://docs.bigcommerce.com/docs/store-operations/pricing/price-lists
- https://docs.bigcommerce.com/docs/integrations/webhooks
- https://developer.woocommerce.com/docs/apis/rest-api/v3/products/
- https://developer.woocommerce.com/docs/apis/store-api/
- https://woocommerce.com/document/webhooks/
- https://woocommerce.com/products/b2b-wholesale-suite/
- https://woocommerce.com/document/woocommerce-dynamic-pricing/
- https://experienceleague.adobe.com/en/docs/commerce-admin/b2b/introduction
- https://experienceleague.adobe.com/en/docs/commerce-admin/b2b/shared-catalogs/catalog-shared
- https://experienceleague.adobe.com/en/docs/commerce-admin/catalog/products/pricing/product-price-tier
- https://experienceleague.adobe.com/en/docs/commerce-operations/release/planning/lifecycle-policy
- https://status.volusion.com/
- https://help.volusion.com/s/allaboutimportexport (via search snippet)
- https://virtina.com/volusion-migration-services/
- https://virtina.com/ecommerce-platforms-comparison/
- ChatSKU pages listed in A and E.
