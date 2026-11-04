---
title: "Brief: Best B2B store platforms for a catalog chatbot (Shopify, BigCommerce, WooCommerce and Magento)"
client: chatsku
date: 2026-11-04
topic: Best B2B Store Platforms for a Catalog Chatbot
audience: Owners, sales and ecommerce managers at B2B manufacturers, distributors and wholesalers choosing or running an online store platform
stage: brief
slug: best-b2b-platforms-for-catalog-chatbot
---

# Brief: best B2B platforms for a catalog chatbot

Inputs: `output/research/best-b2b-platforms-catalog-chatbot-2026-11-04.md` (A to F, conflicts list), `output/research/content-map-chatsku-blog2-source-2026-11-04.md` (user's brief, overrides generic defaults), MUST-FOLLOW-RULES.md, style files. Scheduled Thu 2026-11-19, full length.

## 1. Thesis and angle

**Thesis (one sentence):** There is no single best B2B store platform for a catalog assistant, because what matters is what the platform hands to the chat (structured product fields, customer-specific price rules, API and change events, and a path for the quote), so judge Shopify, BigCommerce, WooCommerce and Magento on those four things, fix the foundation first, then let the catalog talk.

**Unique angle:** compare the platforms by what a catalog assistant needs FROM the platform, not by what ChatSKU does on each one. No ChatSKU post does this (research D). Competing SERP pages rank platforms on features, pricing and "best for" labels. None ties chat quality to platform data.

**The honest limit (say it in the Executive Summary and in section 1):** a catalog assistant works best on clean, structured product data. If specs, prices or stock are not in the store in a readable form, the assistant cannot answer from them. So the order is: foundation first, answer layer second.

**Position:** a decision guide, not a ranking. Say plainly, early and again in the PAA and Conclusion: no platform wins. The right one depends on catalog shape, pricing rules, team and budget. The word "best" appears only in the H1, Yoast title and keyword; the copy never crowns a winner and never says "the best platform is".

**Why this take, why now, why ChatSKU:** buyers are comparing platforms and assistants at the same time; ChatSKU reads the store's own data, so the platform's data model is the real constraint; ChatSKU owns "customer group / tiered pricing complexity" and "catalog-to-chat without site rebuilds" (brand.md).

**Brand-fit guard (brand.md "Themes to avoid" = generic platform comparisons):** every section must tie back to catalog, price and quote workflows. No general "which platform is cheaper or faster to launch" content. No consumer-store content.

**Audience:** owners and sales/ecommerce managers, industry-fluent, 5 to 10 minutes. They know their catalog, not the API terms. Define each term once in plain words: API, webhook, metafield, price list, shared catalog.

## 2. Format choice

**Chosen: Format B (conversational Q&A), with section 6 ("How do you choose?") written as a short decision playbook.**

- **Reason:** the user's outline is six reader questions, each answerable in its first sentence. That is Format B's native shape (question H2s, direct answer first, 2 to 4 short paragraphs). The close is a decision, which the final section handles without turning the whole post into Format D.
- **Recent formats found (briefs and drafts, newest first):** inquiry-tracking-seven-day-count D (11-02); part-number-cross-reference E (10-30); trade-show-booth-catalog-assistant D (10-27); bigcommerce-chatbot-quoting D (10-22); woocommerce-b2b-chatbot-buyers-guide E (10-06); sales-kpis-comp-ramp A (10-05); minimum-order-quantity-b2b B (09-30); b2b-shipping-costs B (09-22); will-ai-replace-reps D (09-21).
- **Overused and skipped:** Format D (used by 3 of the last 10 live posts: inquiry-tracking, trade-show, bigcommerce-quoting; 3010 also D). Format E is at 2, so also avoided, and it does not fit a neutral guide. Format A is at 1 and is a weaker fit than B.
- **OPEN ITEM for the orchestrator:** formats of Blog 1, ai-sales-agent-vs-chatbot-vs-sales-rep, who-b2b-catalog-assistant-is-built-for and chatgpt-vs-catalog-chatbot could not be confirmed from files. If B turns out to be at 3 of the last 10, fall back to Format A with the same question H2s. The outline does not change either way.

**Required structure (MUST-FOLLOW sections 2 and 4), in this order:**
H1, Executive Summary, Introduction, the 6 user H2s in the user's order, People Also Ask, Conclusion (with CTA button), Frequently asked questions (AFTER the conclusion). All headings sentence case. TOC: include a simple anchor list (post is over 2,000 words).

**H1 (sentence case):** Best B2B store platforms for a catalog chatbot: Shopify, BigCommerce, WooCommerce and Magento

## 3. Uniqueness and fences

**Overlapping ChatSKU posts (research D):**

| Post | What it owns | This post's fence |
|---|---|---|
| 685 /b2b-chatbot-for-woocommerce/ | WooCommerce how-to, plugin layer | Link only. No setup steps. |
| 1455 /woocommerce-b2b-chatbot-integration/ | Woo REST API reads, plugin data architecture | Link only. Do not list what ChatSKU reads from the Woo API beyond one sentence. |
| 3305 /woocommerce-b2b-chatbot-buyers-guide/ | Six in-demo tests, vendor evaluation; one H3 on "different chatbot for WooCommerce vs Shopify or Magento" | Do not give vendor-evaluation tests. Do not link (rules file marks draft; research found it live; skip it). |
| 1056 /magento-b2b-chatbot-integration/ | What Magento B2B data ChatSKU reads, readiness | Link only as fallback. Do not re-teach. |
| 3066 /magento-b2b-extensions/ | Magento native vs add-on edition map, Open Source vs Adobe Commerce B2B | Hand off with one link. Do not say whether Open Source includes B2B. |
| 3767 /bigcommerce-chatbot-quoting/ | BigCommerce quote start point; price per customer group | Link once. Do not explain quote intake. |
| 3039 tiered pricing post (long slug) | Tiered pricing as a concept, platform-agnostic | Do not define tiered pricing. This post only asks how each platform stores and exposes it. |
| 2684 /erp-export-ai-agent-ready/ | ERP export field QA (UOM, GTIN, tiers) | Do not teach field QA. |
| 353 / 294 | Definition of catalog chatbot; vendor roundup | Do not define the category at length; do not compare vendors. |
| 2044 /one-line-of-code/ | "Does it matter which platform your site runs on?" | Do not argue one-line install again beyond one clause. |
| **Blog 1 /is-your-b2b-catalog-ready-for-ai-chatbot/** (live Nov 3) | TAKEN: specs in fields vs PDFs, store speed and mobile, "what if the store itself needs work?", catalog hygiene checks; FAQ "Does it work with my store platform?" lists the four platforms in one line | Must NOT re-teach hygiene, field cleanup, speed or mobile checks. Section 1 and section 4 link out. Use different FAQ wording. |

**What this post owns:** the four-need lens applied across the four platforms; precedence of price rules (which price wins) as a platform fact the chat must follow; the platform-by-platform data facts in the table; the decision method.

**Do not link to any draft.** Verify every ChatSKU URL returns 200 right before build (the rules file is stale on several: see section 11).

**8-word phrases and ideas to avoid repeating (paraphrase; run the 8-gram check against the full corpus before publish):**
- ChatSKU's own platform-page lines: "Reads companies, catalogs, and price lists for logged-in B2B buyers"; "Respects Magento customer groups, shared catalogs, and tier pricing rules"; "indexes every Magento product, every variant, every customer-group price"; "Paste one line into your BigCommerce theme"; "That is the whole install"; "Nothing to install in Magento itself"; "Most Magento and Adobe Commerce merchants are live the same day"; "Send us your catalog. PDF, Excel, whatever you have."
- Template B sample sentence from the user's doc: "A chat can only answer as well as the store and product data behind it". Adapt it, do not copy.
- Approved phrase "Fix the foundation first, then let the catalog talk" is allowed once. If the 8-gram check hits Blog 1, vary it.
- Blog 1 headings: "Are your specs in fields or hidden in PDFs?", "What if the store itself needs work?".
- Ideas to avoid: "one line of code, live in under a day, no rebuild" as a repeated claim (one clause at most); "the 8pm buyer" retold (open with the 9 PM buyer once, new details); tiered pricing definition; MOQ; RFQ form vs chat.

## 4. Section-by-section outline (target 2,100 to 2,600 words; plan total about 2,500)

Style for all sections: direct answer first in 1 sentence, short sentences (20 words or fewer), paragraphs of 2 to 3 sentences, prose for depth, bullets only where list-shaped (the four needs in section 1, the table, the choosing questions in section 6).

### Executive Summary (about 150 words)
Line first: "Updated November 2026" (matches house style).
Opening sentence: "No single B2B store platform is best for a catalog chatbot, because the right one depends on your catalog shape, pricing rules, team and budget."
Content: the four needs; Shopify, BigCommerce, WooCommerce and Magento each cover them differently; assistant works best on clean, structured product data, so fix the foundation first; this is a decision guide, not a ranking.

### Introduction (about 170 words)
Open with the buyer scene (user's 9 PM buyer, platform side): 9 PM, a buyer types an exact part number into your store search. The store returns near matches. The specs sit inside one long description. The price she sees is list price, though her account has a contract price. She closes the tab. State the point: the weak link was not the chat, it was what the store could hand over. Say what the article does: compares four platforms on four needs; says plainly there is no winner. One link: "B2B catalog chatbot guide" (/what-is-a-b2b-catalog-chatbot/). End with the early Virtina link inside one sentence: a broader look at the four platforms outside the catalog question sits in an "ecommerce platforms comparison" (https://virtina.com/ecommerce-platforms-comparison/). Do not name Virtina here, no 14 years/2,500+.

### H2 1: What does a catalog chatbot need from a store platform? (about 240 words)
Direct answer first: "It needs four things from the store: product specs in fields, the right price for each buyer, a way to read the catalog and hear about changes, and a place to send the quote."
Four bullets (`<li><strong>Label.</strong> text`) with one plain sentence each:
1. Specs in fields (not in one description blob).
2. Customer-specific price rules (the price this company sees).
3. API access and webhooks (webhook defined in one clause: a message the store sends when a product changes).
4. A quote handoff (where the request lands: email, CRM, draft order, or a native quote object).
Then the honest limit in two or three sentences: the assistant can only be as good as the data it reads, so it works best on clean, structured product data; fix the foundation first, then let the catalog talk. Hand off the hygiene checks with one link: "catalog readiness checklist" (/is-your-b2b-catalog-ready-for-ai-chatbot/). Do not list the checks.

### H2 2: How do Shopify, BigCommerce, WooCommerce and Magento compare? (about 400 words including table)
Direct answer first: "All four can feed a catalog assistant, but they hand over price rules, fields and events in different ways."
Then the table (exact spec below), a one-line "how to read this" before it, and a source line after it: "Facts from each platform's own documentation, checked 4 November 2026. Plans and features change, so confirm on the platform's current docs." (Platform names in prose; sources named, not linked.)
After the table, 3 short paragraphs of reading (no ranking): (a) one fact-based difference in where price rules live (company catalogs vs price lists vs shared catalogs vs extensions); (b) WooCommerce's B2B pricing is a choice of extension, so the chat must read whichever one you run; (c) where the table says "check current docs", say that plainly and that those are questions to put to your platform or developer.

**Comparison table: exact rows and columns (columns: Need | Shopify | BigCommerce | WooCommerce | Magento (Adobe Commerce B2B)). Use ONLY these facts:**

| Need | Shopify | BigCommerce | WooCommerce | Magento / Adobe Commerce |
|---|---|---|---|---|
| Customer-specific prices | Each B2B customer is a company. Catalogs set pricing per company. | Price lists, assignable to a customer group. | Comes from extensions, so it depends on the one you run. | Shared catalogs with custom pricing. Needs Adobe Commerce B2B. |
| Quantity breaks | Quantity rules and volume pricing exist. Check which plan has what. | Bulk pricing at product level. A variant with its own price record skips it in the cart. | Quantity tiers come from extensions. | Tier prices by website, customer group or shared catalog. Fixed price or percent off. |
| Specs as fields | Product metafields. The storefront reads them only if exposed. | Check BigCommerce's current docs. | Attributes and meta_data fields in the REST API. | Check Adobe's current docs. |
| API and change events | Storefront API with buyer context. Webhooks for near-real-time events. | Webhooks with light payloads. The receiver then calls back for detail. | REST API v3, a public Store API, and native webhooks for product add, edit and delete. | Check Adobe's current docs for REST and webhooks. |
| Built-in B2B objects | Companies, company locations, catalogs. | Check BigCommerce's current docs for what is built in and what depends on plan. | Added by extensions. | Company accounts, hierarchies, shared catalogs, quick order, negotiable quotes, requisition lists, purchase order approvals. |

Table notes: cells reading "check ... docs" are deliberate, not placeholders. Do not fill them from memory. No plan names, no prices, no caps in the table. Keep the Shopify "Check which plan has what" clause. Do not add rows. Do not put the Shopify three-catalog cap in the table (it goes in section 3).

### H2 3: Which platform suits a B2B catalog with tiered pricing? (about 300 words)
Direct answer first: "The one whose price rules match how you actually quote, and whose rules the chat can read the way a logged-in buyer sees them." No winner.
Content (do not define tiered pricing; link "tiered B2B pricing" to the 3039 canonical long-slug URL once):
- The key insight: a price rule has a precedence, and the chat must follow the platform's precedence rather than calculate its own. Verified examples: on Magento/Adobe Commerce, custom shared-catalog pricing overrides customer-group pricing; on BigCommerce, a variant with its own price record ignores product-level bulk pricing in the cart. If the assistant ignores the order, it quotes a price the cart will not honor.
- Shopify: catalogs per company; Basic, Grow and Advanced are limited to 3 active catalog assignments, Plus has no limit and can assign catalogs directly to company locations (per Shopify's help page). Say this matters only if you run many distinct company price sets.
- Buyer context: Shopify's Storefront API takes the buyer's company location, so a chat can ask for prices as that buyer.
- WooCommerce: pricing comes from the extension you pick, for example B2B & Wholesale Suite lists group prices and quantity tiers. Word as "tiered and customer-group pricing comes from extensions in the documented route". Do NOT say core lacks tier pricing.
- Magento: hand off with "Magento B2B extensions" link (3066) for native vs add-on. Do not discuss Open Source vs Adobe Commerce B2B.
- Close with a test the reader can run in 10 minutes: ask for one company's price on one part at one quantity, in the store, and see if the answer comes from a rule you can name.
Body image 1 sits at the end of this section.

### H2 4: What if you are on Volusion or an older platform? (about 260 words, includes Template B)
Direct answer first: "You can still start with a catalog assistant on Volusion, because the product data leaves the store as a file." Safe facts: Volusion's status page showed all systems operational on 4 November 2026 and no end-of-life notice was found; do not say Volusion is dying or shutting down. Volusion has a CSV product export and an XML API (documented; do not claim "no modern API"). Older stores differ, so check the export options on the store you run. ChatSKU's site says it can start from a PDF, Excel or store catalog file (vendor claim, label it "ChatSKU can").
The reader decision: the question for an older store is whether the platform can hold your price rules and spec fields as the catalog grows. Do not repeat Blog 1's "store needs work" advice (speed, mobile, spec cleanup).
Then the **Template B block, 80 to 140 words**, in this order: why the store and data come first; what Virtina is (short description); what it does at this layer; the 14 years and 2,500+ projects (ONCE in the whole post); one link; suggestion of the free Store + Catalog Review. Model (adapt, do not copy, 8-gram safe):
"The store sits under the chat, so the store comes first. If the platform cannot hold your price rules or your specs as fields, an assistant has little to read. Virtina is an eCommerce web design and development company with more than 14 years of experience and 2,500+ projects. It builds, redesigns and moves stores, including moving Volusion stores to Shopify, WooCommerce, Magento or BigCommerce, and its engineers lead the work. Its [migration services](https://virtina.com/volusion-migration-services/) are one route if a move makes sense. If you are not sure where your store stands, a free Store + Catalog Review is a simple first step."
Rules: suggestion only; no promises, timelines, prices, guarantees, results, client names, testimonials, ISO claims, password caveat. Service wording limited to what the migration page confirms (migrates Volusion stores to Shopify, WooCommerce, Magento, BigCommerce). Do not call Virtina a ChatSKU service or ChatSKU a Virtina plugin. Anchor exactly "migration services". Body image 2 sits in this section.

### H2 5: How does ChatSKU connect to each platform? (about 280 words)
Direct answer first: "ChatSKU reads each store through that platform's own catalog access and takes a single script on the site."  Then four H3s (real headings, not bold paragraphs), 45 to 65 words each, each saying only what chatsku.com confirms (research A5 to A8), in new words:
- **H3 Shopify:** authorizes through API authentication; reads products, variants, inventory through the Storefront API; reads companies, catalogs and price lists for logged-in B2B buyers; sends quote requests to your team, CRM or draft orders; embed script in the theme or Hydrogen app. Link "Shopify B2B page". Do not mention metafields, plan requirements.
- **H3 BigCommerce:** reads through the Storefront API and the B2B Edition API; company accounts, price lists, inventory; one script tag; works on Stencil, headless and Catalyst; quotes arrive with product, quantity, company account and price list. Link "BigCommerce B2B page" and "BigCommerce quote requests" (/bigcommerce-chatbot-quoting/). DO NOT repeat: "Magento customer groups" on that page, or "no theme to modify". Name "B2B Edition" in plain text only if needed (brand.md competitor-feature rule), never link it.
- **H3 WooCommerce:** works on top of WooCommerce and your B2B plugins; reads SKUs, variants, custom attributes, stock and plugin pricing rules; data comes through the product CSV export, a direct connection or REST sync. Per-plugin reading is not confirmed for every plugin, so say "check the plugin you run". No platform page exists; link the "WooCommerce setup guide" (/b2b-chatbot-for-woocommerce/) and "WooCommerce integration guide" (/woocommerce-b2b-chatbot-integration/).
- **H3 Magento and Adobe Commerce:** reads the catalog through the standard Magento REST API; Open Source and Adobe Commerce, including Cloud; respects customer groups, shared catalogs and tier pricing; for Adobe Commerce, company accounts and negotiable quotes. Link "Magento B2B page".
Closing lines (no link): most teams go live the same day (ONLY this setup wording; no "4 hours", no "1 to 3 days"). Customer groups, tiered pricing and store integration come with paid plans, not the free trial; do not imply otherwise and do not use /chatsku-pricing/ or /pricing/.

### H2 6: How do you choose? (about 250 words)
Direct answer first: "Choose by four things, in this order: your catalog shape, your pricing rules, your team, and your budget."  No winner. One short paragraph per factor plus a closing step list (list-shaped):
1. Catalog shape: many variants and attributes vs a flat list; whether specs can live in fields on that platform.
2. Pricing rules: company-specific prices, quantity breaks, which one wins when they clash (back-reference to section 3).
3. Team: who maintains the store; how much an extension or developer is needed (WooCommerce extensions, Magento B2B module); no claims about ease or difficulty beyond what the table says.
4. Budget: word as "plan limits, paid extensions and developer time", with no figures.
Then a 4-step playbook, one line each: write down your three hardest price cases; ask your platform or developer the four "check the docs" questions from the table; test one company's price on one part; then pick the platform, or fix the foundation before adding the answer layer. Link "ERP export check" is NOT needed here. Reaffirm: fix the foundation first, then let the catalog talk. Mention "Virtina builds the store. ChatSKU answers the buyer." ONLY if it reads naturally and without adding a Virtina name beyond section 4; safer to omit.

### People Also Ask (about 130 words, 4 H3 questions, 1 to 2 sentences each)
See section 8.

### Conclusion (about 100 words, centered, white heading on navy; no inline CTA links)
Restate: no single best platform; judge on the four needs; foundation first. Then one sentence: a free Store + Catalog Review is a simple first step if you want a second pair of eyes on the store and catalog (worded as a suggestion, no Virtina description, no 14 years, no link). CTA button: "See the live demo" to https://chatsku.com/demo/ (one-sentence lead-in in the text).

### Frequently asked questions (about 250 words, AFTER the conclusion)
See section 8. Plain-text brand names, NO links.

## 5. Fact bank for the creator (with source URLs; cite by naming the source in prose, no outbound links)

**Shopify (VERIFIED)**
- B2B available on Basic, Grow, Advanced and Plus (not Starter or Retail). Each B2B customer is a company. Catalogs customise pricing, currency, products, payment and shipping per customer. https://help.shopify.com/en/manual/b2b
- Catalogs: include or exclude products, percentage adjustment or fixed prices; Basic, Grow, Advanced limited to 3 active catalog assignments; Plus unlimited, assignable to company locations; quantity rules and volume pricing exist (plan split not stated). https://help.shopify.com/en/manual/b2b/catalogs
- Admin GraphQL API holds Company, CompanyLocation, CompanyContact, Catalog objects. https://shopify.dev/docs/apps/build/b2b (OMIT the "dev stores, Plus Partners and affiliates" access limit; ambiguous.)
- Storefront API: `@inContext` takes a `buyer` argument (customer access token plus company location ID); metafields readable only with token auth. https://shopify.dev/docs/api/storefront
- Metafields: key-value pairs on any resource including products; Storefront exposure needs the definition set to PUBLIC_READ. https://shopify.dev/docs/apps/build/custom-data/metafields
- Webhooks: near-real-time event delivery; `products/create` named. https://shopify.dev/docs/apps/build/webhooks

**BigCommerce (VERIFIED items only)**
- Webhooks documented, light payloads (id and type), callback needs a follow-up GET, subscription through the v3 hooks endpoint. https://docs.bigcommerce.com/docs/integrations/webhooks
- Price lists assignable to a customer group (Control Panel or Customer Groups API); a variant with a price record ignores product-level bulk pricing in the cart; bulk upsert up to 1,000 price records per call (OMIT the 1,000; not needed). https://docs.bigcommerce.com/docs/store-operations/pricing/price-lists
- NOT CONFIRMED, never state: plan gating, plan renames, B2B Edition native vs paid, custom fields. Wording when needed: "price lists depend on plan, check BigCommerce's current docs".

**WooCommerce (VERIFIED)**
- REST API v3 products include `attributes` (id, name, position, visible, variation, options) and `meta_data` (id, key, value). https://developer.woocommerce.com/docs/apis/rest-api/v3/products/
- Store API: public, unauthenticated reads of products, attributes, categories, brands, reviews; namespace wc/store/v1. https://developer.woocommerce.com/docs/apis/store-api/
- Native webhooks: product add, edit, delete topics; auto-disable after more than five consecutive failures. https://woocommerce.com/document/webhooks/
- Tiered and wholesale pricing offered as paid extensions: B2B & Wholesale Suite (group prices, quantity tiers, CSV import) https://woocommerce.com/products/b2b-wholesale-suite/ ; Dynamic Pricing https://woocommerce.com/document/woocommerce-dynamic-pricing/. Safe wording: "in the documented route, tiered and customer-group pricing comes from extensions, so the chat must read whichever one you run."
- NOT CONFIRMED: 2026 status of WooCommerce; "core has no tier pricing" as a stated fact.

**Adobe Commerce / Magento (VERIFIED)**
- B2B features: company accounts, company hierarchy, shared catalogs, quick order, negotiable quotes, requisition lists, purchase order approvals; B2B is described as an extension installed in an Adobe Commerce store. https://experienceleague.adobe.com/en/docs/commerce-admin/b2b/introduction
- Shared catalogs: one public catalog plus unlimited custom catalogs for assigned company associates; custom shared-catalog pricing overrides customer-group pricing. https://experienceleague.adobe.com/en/docs/commerce-admin/b2b/shared-catalogs/catalog-shared
- Tier pricing: quantity discounts; scope website, customer group or shared catalog (shared catalog needs B2B); fixed price or percent off. https://experienceleague.adobe.com/en/docs/commerce-admin/catalog/products/pricing/product-price-tier
- Optional and low value: Adobe Commerce 2.4.9 reached general availability on 12 May 2026. https://experienceleague.adobe.com/en/docs/commerce-operations/release/planning/lifecycle-policy . Recommend OMIT (does not cover Open Source; adds no decision value).
- NOT CONFIRMED, never state: Adobe REST and webhook specifics (use "check Adobe's current docs"; ChatSKU's own page says it reads via the Magento REST API, cite that only in section 5), product attribute details, any Open Source patch floor, whether Open Source includes B2B.

**Volusion (VERIFIED)**
- Status page showed "All Systems Operational" on 2026-11-04; October 2026 maintenance and a PHP vulnerability mitigation noted; no end-of-life notice. https://status.volusion.com/ (do not cite the CVE ids).
- CSV product export (Inventory > Import/Export > Standard Export) and an XML API exist. https://help.volusion.com/s/allaboutimportexport (confirmed via search snippet; state only "CSV export and an XML API exist").
- OMIT: store counts, decline figures, "100 products at a time", any claim of "no modern API", any claim Volusion is shutting down.

**ChatSKU (vendor claims from chatsku.com, label as "ChatSKU can/does")**: research A5 to A8 as summarised in section 4, H2 5. Setup "same day" only.

**Virtina:** https://virtina.com/volusion-migration-services/ migrates Volusion stores to Shopify, WooCommerce, Magento, BigCommerce and others; https://virtina.com/ecommerce-platforms-comparison/ is a full four-platform comparison. Use no timelines, guarantees, ISO, testimonials or password caveat from them.

## 6. Link plan (10 internal in text, plus CTA button, plus 2 Virtina links; zero other external)

| # | Section | URL | Anchor |
|---|---|---|---|
| 1 | Introduction | https://chatsku.com/what-is-a-b2b-catalog-chatbot/ | B2B catalog chatbot guide |
| V1 | Introduction (last paragraph) | https://virtina.com/ecommerce-platforms-comparison/ | ecommerce platforms comparison |
| 2 | H2 1 | https://chatsku.com/is-your-b2b-catalog-ready-for-ai-chatbot/ | catalog readiness checklist |
| 3 | H2 3 | https://chatsku.com/one-catalog-a-thousand-prices-making-tiered-b2b-pricing-work-online/ | tiered B2B pricing |
| 4 | H2 3 | https://chatsku.com/magento-b2b-extensions/ | Magento B2B extensions |
| V2 | H2 4 (Template B) | https://virtina.com/volusion-migration-services/ | migration services |
| 5 | H2 5 Shopify | https://chatsku.com/shopify-b2b-chatbot/ | Shopify B2B page |
| 6 | H2 5 BigCommerce | https://chatsku.com/bigcommerce-b2b-chatbot/ | BigCommerce B2B page |
| 7 | H2 5 BigCommerce | https://chatsku.com/bigcommerce-chatbot-quoting/ | BigCommerce quote requests |
| 8 | H2 5 WooCommerce | https://chatsku.com/b2b-chatbot-for-woocommerce/ | WooCommerce setup guide |
| 9 | H2 5 WooCommerce | https://chatsku.com/woocommerce-b2b-chatbot-integration/ | WooCommerce integration guide |
| 10 | H2 5 Magento | https://chatsku.com/magento-b2b-chatbot/ | Magento B2B page |
| CTA | Conclusion button | https://chatsku.com/demo/ | See the live demo |

- 3 pages (Shopify, BigCommerce, Magento) plus /demo/; 6 blog posts. Meets "3+ pages, 2+ posts".
- The Virtina links are external, so they use `target="_blank" rel="noopener noreferrer"`. They are the only external links (2 of the 2 allowed). Zero official-doc links; platform facts are in prose with the source named.
- V1 and V2 are far apart (Introduction vs H2 4, separated by about 1,000 words and three sections).
- No links in FAQ answers or PAA is optional (keep PAA link-free too for safety).
- No competitor links. No /pricing/ and no /chatsku-pricing/. No /rfq-automation-for-product-catalogs/. No links to any draft. Re-verify all URLs return 200 immediately before build. If /magento-b2b-extensions/ is not live, swap to /magento-b2b-chatbot-integration/ with anchor "Magento setup guide". If /bigcommerce-chatbot-quoting/ is not live, drop link 7 (9 internal remains valid).
- Anchors must truthfully name the destination; no "click here".

## 7. Stats and claims discipline

**There are no numbers in this post except verified ones and clearly labeled illustrative examples.** Allowed numbers: "3 active catalog assignments" (Shopify help page); the Virtina "14 years" and "2,500+ projects" ONCE; dates. Anything else is out.

**Do NOT make these claims:**
- Market share, "X% of B2B sites run Y", store counts, platform growth or decline, Volusion store counts.
- The unsourced "$15T / 90% by 2028" figure (the linked post /ai-ready-b2b-catalog-autonomous-buying/ carries it; do not link or quote).
- Baymard 48% (real figures are 40% and 12% and are B2C); any conversion lift, response time or revenue figure for ChatSKU.
- Prices, plan names, caps or plan prices for any platform or extension; BigCommerce plan gating or plan renames; "Shopify needs apps for B2B" (out of date per official docs); "Magento/BigCommerce have stronger native B2B" generalisations from agency blogs; "WooCommerce core has no tier pricing"; "older platforms have no modern API"; "Volusion is dying/closing".
- Setup times other than "same day"; "4 hours"; "1 to 3 days"; "live in under an hour".
- Virtina timelines, guarantees, ISO, testimonials, results or client names; ChatSKU customer names or results; "replaces your sales team".
- Free trial including customer groups, tiered pricing or store integration.
- Any feature or integration not on chatsku.com; ChatSKU capturing phone or email.
- Any ranking, "winner", "top pick", "#1".

**Banned phrases and words (in addition to voice.md):** em dashes (U+2014 and `&mdash;`), "AI-powered", "solutions" as filler, "chatbot" alone for ChatSKU (use "AI catalog assistant"; "catalog chatbot" only as the generic category in the title/keyword/H2), "just a chatbot", delve, leverage, navigate (verb), realm, landscape, ecosystem, robust, seamless, powerful, game-changing, cutting-edge, best-in-class, world-class, revolutionary, "in today's fast-paced world", "it's important to note", "in conclusion", "Schedule a demo to learn more", "we will" outcome promises about Virtina or ChatSKU, "our guide", "check out our", "learn more".

## 8. People Also Ask and FAQ

**People Also Ask (H3 questions, 1 to 2 sentences each, no links):**
1. **Which B2B platform is best for a catalog chatbot?** Seed: There is no single best one. The right platform depends on your catalog shape, pricing rules, team and budget, and on what the platform lets an assistant read.
2. **Do you need to switch platforms to add a catalog chatbot?** Seed: Usually not. The assistant reads the store you have. A move only makes sense if the platform cannot hold your price rules or product fields.
3. **Can a catalog chatbot show customer-specific prices?** Seed: Yes, when the platform exposes those prices for the logged-in buyer. That is why price rules are one of the four needs.
4. **Does Shopify have built-in B2B features?** Seed: Shopify's help pages describe B2B companies and catalogs on Basic, Grow, Advanced and Plus. Check Shopify's current docs for which feature sits on which plan.

**Frequently asked questions (follow-ups only; answers 35 to 50 words; plain-text brand names; NO links):**
1. **How long does it take to connect ChatSKU to a store?** Seed: Most teams go live the same day.
2. **Does the free trial include customer groups and tiered pricing?** Seed: No. Customer groups, tiered pricing and store integration come with paid plans, not the free trial.
3. **Do I have to migrate my store to use ChatSKU?** Seed: No. ChatSKU reads the store you have through the platform or from catalog files. A move is worth weighing only if the platform cannot hold your price rules or specs.
4. **Is WooCommerce enough for B2B pricing?** Seed: In the documented route, tiered and customer-group pricing comes from extensions. The assistant has to read whichever extension you run, so confirm that one.
5. **Can ChatSKU work with a custom or older store?** Seed: ChatSKU can start from a PDF, Excel or store catalog file, and an older store such as Volusion can export a product file. Confirm the details in the live demo.
6. **Does ChatSKU see the same prices my logged-in buyers see?** Seed: For Shopify, BigCommerce and Magento, ChatSKU says it reads company or customer-group prices for logged-in buyers. For WooCommerce it depends on the pricing plugin you run.
(Do NOT reuse Blog 1's FAQ wording "Does it work with my store platform?". No replace-reps answer needed.)

## 9. Images (3: featured plus 2 body)

Standard: CLAUDE.md image quality standard wins where it conflicts with MUST-FOLLOW section 3. Display 860 x 452. Export at **1720 x 904** (2x), JPEG quality 90 or higher, 4:4:4 subsampling, no upscaling of a smaller source, no quality reduction to hit a size target (the 200 KB cap in MUST-FOLLOW section 3 is superseded; resize instead). View each at 100% before upload; soft or artifacted images are rejected. Realistic documentary-style photos of a real person in the exact situation. No concept art, neon, glow or metaphor scenes. No readable fake software UI or brand logos on screens. Do not reuse scenes from recent posts (night-laptop buyer, warehouse counter, trade-show booth, rep on phone, shipping dock); check the media library before choosing.

| Slot | Under | Exact scene | Alt text (80 to 150 chars) |
|---|---|---|---|
| Featured | Header (above Executive Summary) | A wholesale store owner at a desk comparing two ecommerce admin dashboards side by side on a monitor, notebook with a handwritten comparison grid beside the keyboard | Wholesale store owner comparing two ecommerce platform dashboards side by side to choose a B2B catalog chatbot platform |
| Body 1 | H2 3, end of section | A distributor reviewing a printed price-tier table with several customer price columns next to an open laptop, pen in hand | Distributor reviewing a printed price-tier table beside a laptop to plan tiered B2B pricing on an online store |
| Body 2 | H2 4, end of section | A developer and a store owner side by side at a monitor reviewing an older store's product list and an exported spreadsheet | Developer and store owner reviewing an older Volusion store product export on a monitor to plan a platform move |

Alt text lengths run about 115 to 120 characters; recount in the build. Each alt must describe the image actually chosen (visual QA). Image widget goes AFTER the text-editor widget in its section. Strip bare `<img>` from the WP content field.

## 10. SEO

- **H1:** Best B2B store platforms for a catalog chatbot: Shopify, BigCommerce, WooCommerce and Magento
- **Yoast title:** Best B2B Platforms for a Catalog Chatbot | ChatSKU (51 characters; ends "| ChatSKU")
- **Meta description (about 153 characters, recount before push; must land 150 to 160):** Shopify, BigCommerce, WooCommerce or Magento? Compare what each B2B store platform gives a catalog chatbot: price rules, product fields, APIs and quotes.
  (Adapted from the user's line, which is replaced because it promises "what to do if you are on an older one" in under the limit; if the user wants theirs, trim to fit 160.)
- **Focus keyword:** B2B platforms for catalog chatbot (secondary: best B2B ecommerce platform for chatbot, Shopify BigCommerce WooCommerce Magento B2B comparison). Use the exact focus keyword in the Executive Summary opening, one H2 context, the Yoast title and the meta description.
- **Slug:** `best-b2b-platforms-for-catalog-chatbot` (user's slug; checked, no match among existing slugs).
- Push Yoast through `meta` and verify with a `context=edit` GET. Status draft. Clear the Elementor cache.

## 11. Checklist and voice rules for the creator

**Voice:** ChatSKU is an "AI catalog assistant". "Catalog chatbot" only as the generic category where the title/keyword/H2 needs it. No em dashes. No hype. No "AI-powered" filler. Sentence-case headings. Short sentences (20 words or fewer), paragraphs of 2 to 3 sentences. Second person. Open with the buyer scene. Prose for depth; bullets only for the four needs, the table, and the closing steps. Neutral, honest tone: this is a guide, not an advert, and ChatSKU is not the hero.

**Checklist:**
- [ ] 6 outline questions appear as H2s in the user's order, exact wording above, sentence case
- [ ] Executive Summary, Introduction, PAA, Conclusion with CTA button, FAQ AFTER Conclusion
- [ ] Opens with the 9 PM buyer scene; names no real customers
- [ ] Says plainly there is no single best platform (Exec Summary, section 6, PAA 1, Conclusion)
- [ ] Table has only the listed facts; no plan names, caps, prices
- [ ] Every "NOT CONFIRMED" item is worded safely or omitted
- [ ] Foundation first, then answer layer; the hygiene advice stays in Blog 1 (link only)
- [ ] Virtina: Template B 80 to 140 words in H2 4; 14 years and 2,500+ projects exactly once; "migration services" anchor; one earlier link, anchor "ecommerce platforms comparison"; the closing Store + Catalog Review sentence is the only other mention; suggestions only
- [ ] 3 platform pages + 6 posts linked, anchors 2 to 5 words, all verified 200; no drafts; no competitor links; no /pricing/ or /chatsku-pricing/
- [ ] Zero external links except the 2 Virtina links; both with `target="_blank" rel="noopener noreferrer"`
- [ ] No links in FAQ answers
- [ ] No claims from the section 7 list; no numbers beyond the allowed
- [ ] "Same day" is the only setup wording; free trial exclusions respected
- [ ] 8-gram check against the whole corpus passes (esp. 3767, 1056, 1455, 3066, 3305, Blog 1, ChatSKU platform pages)
- [ ] Word count 2,100 to 2,600; readability at or above the ChatSKU corpus (aim Flesch 70+)
- [ ] 3 images at 1720 x 904, q90+, 4:4:4, alt 80 to 150 chars, scenes as specified
- [ ] Yoast title 51 chars ends "| ChatSKU"; description 150 to 160 chars
- [ ] Conclusion: centered white heading on navy, body #aaaacc 18px, button #e94560 to /demo/

**Flags for the orchestrator:** (1) MUST-FOLLOW rules are stale on /chatsku-pricing/ (live), on /magento-b2b-extensions/ and /woocommerce-b2b-chatbot-buyers-guide/ (rules say draft; research found live), and on the 200 KB image cap (superseded by the quality floor). (2) The BigCommerce solutions page has copy errors (Magento customer groups; "no theme to modify") that the client should fix. (3) brand.md lists Adobe Commerce and BigCommerce B2B Edition as "competitors (do not cite or link)"; the post names them in plain text as platform facts only, never linked. (4) brand.md says Virtina has "2,000+ clients"; the user's brief says 2,500+ projects; use the user's. (5) Format B count needs confirmation (section 2). (6) The user's meta description was adapted for the 150 to 160 range.
