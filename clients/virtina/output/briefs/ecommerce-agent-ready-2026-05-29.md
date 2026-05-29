---
title: "The customer was a robot: how to make your store readable to AI shopping agents"
client: virtina
date: 2026-05-29
topic: Making ecommerce stores readable and transactable by AI shopping agents
audience: B2B and B2C ecommerce store owners and managers on WooCommerce, Magento, Shopify, BigCommerce
stage: brief
slug: ecommerce-store-agent-ready
primary_keyword: ecommerce store agent-ready
format: B — Conversational Q&A
word_count_target: 2000–2500 (standard)
author_id: 9
post_status: draft
---

# Content Brief: ecommerce store agent-ready

---

## Format decision

**Format chosen: B — Conversational Q&A**

**Reason:** The user provided 12 natural long-tail reader questions as target H2s. Format B maps these questions directly to body sections, satisfying search intent for each query and giving LLMs a clean extraction target per question. Format A was used in 8 of the last 10 published posts and must not be used again.

**Formats skipped and why:**
- Format A (Standard explanatory): overused — 8 of the last 10 published posts. Do not use.
- Format C (Listicle): topic is not list-shaped; it requires distinction-drawing and technical explanation.
- Format D (Decision tree): the article is not a binary decision guide.
- Format E (Contrarian): title is narrative/problem-framing, not a contrarian thesis.
- Format F (Case study): no specific client win to anchor this.

---

## Uniqueness confirmation

All 5 checks passed. Full audit at:
`clients/virtina/output/research/uniqueness-audit-agent-ready-2026-05-29.md`

| Check | Result |
|---|---|
| CHECK 1: Title word overlap | PASS |
| CHECK 2: Slug overlap | PASS |
| CHECK 3: Primary keyword | PASS |
| CHECK 4: Angle/thesis | PASS |
| CHECK 5: Cluster saturation | PASS |

**Closest posts — confirm these angles are NOT repeated:**
- ID 41531 `ecommerce-seo-optimization-2026`: GEO/AEO content optimization. Not the same angle. Reference it only to distinguish GEO from agent-readiness.
- ID 41491 `b2b-schema-gaps-invisible-filters`: B2B schema gaps for procurement AI. Overlapping tactic (schema) but entirely different framing. Schema here is a sub-step in a larger agent-readiness system.
- ID 41142 `agentic-ai-in-ecommerce-ai-agents`: Internal AI automation agents. Fundamentally different: that post covers AI you deploy inside your store; this post covers external AI agents acting as shoppers.

---

## Thesis

**One sentence:** Your store can be cited perfectly by ChatGPT as a recommendation and still fail completely when that same agent tries to buy from you — because citation and transaction are two different problems requiring two different fixes.

**Why this angle is defensible:**
1. It is not covered by any existing Virtina post.
2. Every top-5 competitor addresses either GEO or agentic commerce strategy — none explain both the discovery failure and the transaction failure in the same piece with platform-specific action items.
3. The GEO vs. agent-readiness distinction is the specific gap identified in the research as absent across all five ranked competitors.
4. The supporting data is exceptional: 693% AI-sourced retail traffic growth (Adobe), 15x YoY growth in AI-driven Shopify orders, Perplexity shoppers at 57% higher order value. These numbers make the urgency real, not theoretical.

---

## H2 section table (consolidated from 12 queries to 9)

Consolidation logic: queries 4 and 5 (why store isn't showing up / why agents skip) are the same problem; merged. Query 11 (will ChatGPT buy from my store) is covered in full by query 6 (can AI agents read my product pages) + query 9 (optimize product data). Queries 1 and 12 (how to make agent-ready / how to prepare for agentic commerce) overlap; the full checklist section at the end covers both.

| # | H2 heading (verbatim reader question) | Anchor ID | Approx word count | Key content |
|---|---|---|---|---|
| 1 | What does "agent-ready" mean for an ecommerce store? | `#what-does-agent-ready-mean` | 180–220 | Define agent-ready. Distinguish from mobile-ready, SEO-ready. The four conditions: machine-readable pages, complete product data, agent-accessible checkout, real-time data. Direct answer first sentence. |
| 2 | What is the difference between GEO and being agent-ready? | `#geo-vs-agent-ready` | 200–250 | GEO = getting cited in AI answers (discovery). Agent-ready = enabling AI agents to browse and buy (transaction). A store with great GEO but no SSR, no schema, no GTIN will be cited but fail at checkout. Include the Retail Media Breakfast Club quote (under 15 words or paraphrase). Link to ID 41531 here. |
| 3 | How do AI shopping agents find and evaluate products? | `#how-ai-agents-find-products` | 220–270 | Name the four major agents (ChatGPT Shopping, Perplexity Shopping, Google AI Mode, Amazon Rufus/Alexa). State user scale numbers. Explain the two-step: retrieval bots crawl product pages first; the agent reasons over the retrieved data second. Body image 1 here (developer reviewing structured data). |
| 4 | Why isn't my store showing up in AI shopping results? | `#why-not-showing-up` | 220–270 | The four invisibility causes: JS-rendered prices, missing/incomplete schema, wrong robots.txt configuration, no product feed. Case/example snippet here (2–3 sentences illustrating the problem in practice — required for problem/solution article type). |
| 5 | What makes a product page invisible to AI shopping agents? | `#product-page-invisible` | 250–300 | The five specific failure modes: JS-rendered prices (4 of 6 major AI crawlers fetch static HTML only), missing schema fields (GTIN, OfferShippingDetails, return policy), robots.txt blocking retrieval bots, checkout friction (cookie banners, login walls, CAPTCHA), no real-time inventory API. Include agent-ready audit checklist here (numbered or checklist format — mandatory for problem/solution type). |
| 6 | Do I need structured data for AI shopping agents? | `#structured-data-for-agents` | 220–260 | Yes, and which types. Core schema: Product, Offer, AggregateRating, BreadcrumbList. Required for transactions: OfferShippingDetails, hasMerchantReturnPolicy, ProductGroup (variants), GTIN. JSON-LD preferred (89.4% market share, parsable without HTML traversal). Server-side rendered only. External link 1 to Schema.org Product specification here. Body image 2 here. |
| 7 | How do I optimize my product data for AI agents? | `#optimize-product-data` | 250–300 | The practical optimization steps: Merchant Center feed completeness (99.9% attribute completion = 3-4x higher AI visibility), GTIN for every SKU, price freshness (30-minute cadence for Google, real-time for Perplexity), product title format, product description specificity. Platform-specific callouts: WooCommerce (Yoast product identifiers, Rank Math GTIN settings), Magento (structured data extension audit). |
| 8 | What is the difference between training crawlers and retrieval bots, and which should I allow? | `#training-vs-retrieval-bots` | 200–240 | Critical distinction. Training crawlers (GPTBot, ClaudeBot, Google-Extended): feed LLM model training; you can block these if desired. Retrieval bots (OAI-SearchBot, PerplexityBot, Claude-SearchBot, Googlebot): power real-time AI answers and shopping; blocking these makes you invisible. Many WooCommerce SEO plugins added "block AI bots" toggles in 2024–2025 with the toggle enabled by default — stores have unknowingly blocked their own visibility. Robots.txt table of named bots with Allow/Block recommendations. |
| 9 | How do I make my ecommerce store agent-ready — where do I start? | `#how-to-make-store-agent-ready` | 280–320 | The six-step implementation sequence: (1) audit robots.txt for accidentally blocked retrieval bots, (2) enable SSR or pre-rendering for product pages, (3) add/fix Schema.org Product markup with full required fields, (4) submit and maintain product feed (Google Merchant Center, Perplexity SFTP), (5) audit checkout for agent friction points, (6) verify real-time pricing API response time. Link to relevant Virtina service pages here. External link 2 to Adobe Analytics shopping AI data here. |

**Fixed sections (not H2 query questions — per Format B structure):**

| Section | Anchor ID | Template |
|---|---|---|
| People also ask | `#people-also-ask` | Template H |
| Conclusion | `#conclusion` | Template I |
| Frequently asked questions | `#faq` | Template J |

---

## Article structure (complete, in order)

Per MUST-FOLLOW-RULES section 2 (Format B variant):

1. H1 title (sentence case)
2. Author byline + category + updated date
3. Featured image (1309×500)
4. Summary block (Template A)
5. Introduction block (Template B)
6. Table of Contents (Template C, H3 heading, inline SVG arrows, `#00a0e2` links)
7. H2 section 1: `#what-does-agent-ready-mean`
8. H2 section 2: `#geo-vs-agent-ready`
9. H2 section 3: `#how-ai-agents-find-products` + Body image 1
10. H2 section 4: `#why-not-showing-up` (includes case/example snippet)
11. H2 section 5: `#product-page-invisible` (includes agent-ready audit checklist)
12. H2 section 6: `#structured-data-for-agents` + Body image 2
13. H2 section 7: `#optimize-product-data`
14. H2 section 8: `#training-vs-retrieval-bots`
15. H2 section 9: `#how-to-make-store-agent-ready`
16. People also ask block (Template H, `#people-also-ask`)
17. Conclusion block (Template I, `#conclusion`)
18. FAQ accordion (Template J, `#faq`)
19. Author bio block (Template K)

---

## Opening — summary and introduction guidance

**Summary block (Template A) — what to cover:**
- AI shopping agents are already browsing and buying. 61% of U.S. adults used AI for shopping in 2025.
- Most stores are invisible to them due to JS-rendered prices, missing schema, and blocked crawlers.
- This post explains what agent-ready means, why GEO alone is not enough, and the exact six steps to fix it.
- Max 3 sentences per paragraph. No hype words.

**Introduction block (Template B) — what to cover:**
- Open with the scenario: a shopper asks ChatGPT to find the best industrial pump under $500 and order it. Your store carries it. But you're not in the results — or the agent reached checkout and gave up.
- This is not a future problem. Adobe recorded 693% growth in AI-sourced retail traffic during the 2025 holiday season. Shopify reports 15x YoY growth in AI-driven orders.
- The distinction this post makes: you can be perfectly "GEO-optimized" and still fail when agents try to transact. This post covers both.
- 2 paragraphs max, 2–3 sentences each.

---

## Case/example snippet (mandatory for problem/solution type)

Place inside section 4 (`#why-not-showing-up`). Writer should use this scenario or equivalent:

A mid-market industrial parts store had solid Google rankings and appeared regularly in ChatGPT shopping recommendations for its category. When a Perplexity Shopping agent attempted to retrieve product details and price for a specific SKU, the page returned an empty shell — prices were loaded via React and the crawler saw no data. The agent moved to a competitor whose prices were server-side rendered, even though that competitor ranked lower on traditional Google.

This is 3 sentences, illustrates the problem in practice, and is specific enough to be concrete without being fabricated as a Virtina client claim.

---

## Agent-ready audit checklist (mandatory — place in section 5)

Title: "Agent-ready audit: check these 6 things today"

Use a numbered list (Template F bullet format if unordered, or `<ol>` equivalent). Items:

1. **Robots.txt check** — open your robots.txt and search for GPTBot, OAI-SearchBot, PerplexityBot. Confirm retrieval bots are allowed.
2. **JS rendering check** — disable JavaScript in your browser on a key product page. If price, stock, and add-to-cart disappear, AI crawlers see the same blank state.
3. **Schema.org validation** — run 3 product URLs through Google's Rich Results Test. Check for missing GTIN, priceCurrency, availability, OfferShippingDetails.
4. **Merchant Center feed completeness** — log in to Google Merchant Center (or your Perplexity SFTP portal). Check attribute completeness score. Stores with 99.9% completion get 3–4x higher AI Mode visibility.
5. **Checkout friction test** — open an incognito window and attempt to add to cart and reach checkout without creating an account. If blocked by login wall or CAPTCHA, agents will fail here too.
6. **Product API response** — can your store return price, availability, and shipping estimate for a specific SKU in a single API call under 200ms? If not, agents with real-time verification requirements will skip your store.

---

## People also ask section (Template H — 4 Q&As)

**Q1:** What is an AI shopping agent?
**A1:** An AI shopping agent is a software system that browses ecommerce stores autonomously on a user's behalf. It compares prices, reads product specifications, and can initiate purchases without the user visiting the store directly. ChatGPT Shopping, Perplexity Shopping, Google AI Mode, and Amazon Rufus are the four major examples active in 2026.

**Q2:** Does my store automatically appear in ChatGPT or Perplexity shopping results?
**A2:** No. Appearing in AI shopping results requires your store to meet specific technical conditions. AI retrieval bots must be allowed in your robots.txt. Your product pages must return price and availability in static HTML. Your product data must include schema markup with complete fields including GTIN. Stores that meet all three conditions are surfaced; stores that do not are skipped.

**Q3:** Is agent-readiness only for large enterprises?
**A3:** No. The same technical requirements apply regardless of store size. A WooCommerce store with 50 SKUs needs the same structured data, SSR, and robots.txt configuration as an enterprise Magento deployment. The implementation cost scales with catalog size, but the checklist is the same.

**Q4:** What happens if I block AI bots in my SEO plugin?
**A4:** Blocking all AI bots disables visibility in ChatGPT, Perplexity, and Google AI Mode simultaneously. Many SEO plugins added "block AI bots" toggles in 2024–2025 — often enabled by default. The correct approach is to block training crawlers only (GPTBot, ClaudeBot for model training) while allowing retrieval bots (OAI-SearchBot, PerplexityBot, Googlebot).

---

## FAQ section (Template J — 8 Q&As, 6 minimum)

**FAQ 1:** What is the difference between GPTBot and OAI-SearchBot?
GPTBot crawls the web to train OpenAI's language models. It does not power real-time shopping results. OAI-SearchBot is the retrieval crawler that powers ChatGPT's live web search and shopping features. Blocking GPTBot has no effect on your ChatGPT shopping visibility. Blocking OAI-SearchBot removes you from ChatGPT shopping results entirely.

**FAQ 2:** What schema fields are mandatory for AI shopping agents?
At minimum: name, description, brand, SKU, GTIN, image, price, priceCurrency, availability, and itemCondition inside an Offer entity. For agents that complete transactions, also add OfferShippingDetails, hasMerchantReturnPolicy, and ProductGroup for variant products. Missing GTIN blocks visibility in Perplexity Shopping and Google AI Mode specifically.

**FAQ 3:** Does llms.txt help my store get found by AI agents?
llms.txt is a plain-text file at the root of your site that gives AI crawlers a structured map of your best content and data endpoints. As of late 2025, fewer than 1,000 domains globally had published one, and major AI crawlers were not yet consistently reading it. It is emerging infrastructure worth implementing early but not a replacement for schema markup and product feeds.

**FAQ 4:** Why do Perplexity shoppers spend more per order?
Perplexity's user base skews toward high-income, college-educated buyers — 80% college-educated and 65% in premium income brackets per Alhena.ai data. These buyers use Perplexity precisely because they want curated, high-quality recommendations rather than general search results. That intent alignment produces 57% higher average order values compared to shoppers from other AI platforms.

**FAQ 5:** Will making my store agent-ready hurt my regular SEO?
No. Every change required for agent-readiness is aligned with standard SEO best practices. Server-side rendering improves Google crawlability for all users. Schema markup improves rich result eligibility. A complete Merchant Center feed improves Google Shopping performance. Correct robots.txt configuration does not affect traditional Googlebot. Agent-readiness is an extension of SEO, not a conflict with it.

**FAQ 6:** How do I know if AI agents are already sending traffic to my store?
Check Google Search Console's "Search type" filter for AI Overviews impressions. Review your Merchant Center Performance tab for AI Mode impressions. Perplexity provides a merchant portal with referral traffic data for enrolled merchants. For general AI referral traffic, filter your analytics for referrer domains: perplexity.ai, chatgpt.com, and search.bing.com (Copilot).

**FAQ 7:** Do I need to submit a separate product feed for each AI platform?
Each platform has its own feed format. Google AI Mode pulls from your existing Google Merchant Center feed. Perplexity Shopping uses a Google Shopping CSV format via SFTP, with GTINs mandatory. Amazon Rufus uses your existing Amazon listing data. ChatGPT Shopping primarily uses schema markup on your product pages plus Merchant Center data where available. Maintaining one well-structured Merchant Center feed covers most requirements.

**FAQ 8:** Is there a penalty if my schema markup does not match my displayed prices?
Yes. Google issues manual penalties when schema data and on-page content conflict. If your schema reports a price of $49.99 but the page displays $59.99, Google will deprioritize your product in both regular Shopping and AI Mode. Partial or mismatched data is treated as worse than no data in Google's AI product ranking system.

---

## Conclusion guidance (Template I — white text on `#00d5c0` background)

Two paragraphs, 2–3 sentences each.

Paragraph 1: AI shopping agents are now a real customer acquisition channel. Adobe's 693% AI traffic growth data and Shopify's 15x order growth are the numbers to anchor the close. The stores that close the agent-readiness gap now will have a head start as agentic commerce scales.

Paragraph 2: The six-step checklist in this post is where to start. Virtina helps WooCommerce, Magento, Shopify, and BigCommerce stores implement structured data, SSR, and product feed completions. CTA: link to WooCommerce development services.

No em dashes. No "in conclusion." No hype words. Sentence case.

---

## Internal links plan (7–9 links, all unique anchor text)

**Target:** 7–9 internal links woven naturally in body prose only (not in intro, not in conclusion).

| # | URL | Suggested anchor text | Section placement |
|---|---|---|---|
| 1 | https://virtina.com/ai-impact-woocommerce/ | AI features in WooCommerce | Section 3 (how agents find products) — when introducing WooCommerce-specific AI context |
| 2 | https://virtina.com/ecommerce-seo-optimization-2026/ (slug: ecommerce-seo-optimization-2026) — use as /ai-impact-woocommerce/ per orchestrator note | (see note below) | — |
| 3 | https://virtina.com/woocommerce-seo-made-easy/ | product page SEO fundamentals | Section 6 (structured data) — when mentioning that schema is part of standard SEO hygiene |
| 4 | https://virtina.com/woocommerce-erp-integration/ | real-time product data via ERP integration | Section 7 (optimize product data) — when discussing price/inventory freshness from ERP systems |
| 5 | https://virtina.com/b2b-ecommerce-for-manufacturers/ | B2B ecommerce strategy for manufacturers | Section 4 or 7 — for B2B-specific product data completeness context |
| 6 | https://virtina.com/b2b-schema-gaps-invisible-filters/ | how B2B schema gaps filter you out of AI procurement searches | Section 2 (GEO vs agent-ready) — when noting that B2B buyers also use AI to shortlist suppliers |
| 7 | https://virtina.com/industrial-b2b-ecommerce-10-objections-2026/ | how B2B digital hesitation plays out in practice | Section 4 (why not showing up) — as context for stores that haven't prioritized AI readiness |
| 8 | https://virtina.com/woocommerce-development-services/ | WooCommerce development services | Section 9 (how to start) — as a CTA callout in the last body section, and in author byline |
| 9 | https://virtina.com/b2b-commerce-needs-engineering-not-just-marketing/ | agent-readiness is an engineering problem, not a marketing one | Section 2 (GEO vs agent-ready) — reinforcing that agent-readiness requires technical implementation |

**Note on URL for GEO article:** The orchestrator listed `https://virtina.com/ai-impact-woocommerce/` as the URL for "AI features in ecommerce." The GEO/AEO post (ID 41531, slug `ecommerce-seo-optimization-2026`) should be linked in section 2 as "GEO and AEO strategies for ecommerce SEO" using its real URL. Confirm the live URL before publishing: `https://virtina.com/ecommerce-seo-optimization-2026/` — if that 404s, use `https://virtina.com/?p=41531`.

**Anchor text uniqueness:** All 9 anchor texts above are unique. Confirm no two are identical before publishing.

---

## External citations (maximum 2 — hard limit per MUST-FOLLOW-RULES section 6)

| # | URL | Anchor text | Placement |
|---|---|---|---|
| 1 | https://schema.org/Product | Schema.org Product specification | Section 6 (structured data) — when listing required schema fields |
| 2 | https://capitaloneshopping.com/research/ai-shopping-statistics/ | Adobe and Capital One Shopping data on AI shopping adoption | Section 3 (how AI agents find products) OR in intro/stats section when citing the 61% and 693% statistics |

Both links: `target="_blank" rel="noopener noreferrer"` per Template M.

**No other external links permitted.** If the creator is tempted to link to Perplexity, OST Agency, Alhena.ai, etc. — do not. Cite the statistic inline and attribute by source name only. Do not hyperlink.

---

## Key data points — confirmed and approved for use

All stats below are confirmed in research. Use them. Do not invent additional statistics.

**Use these:**
- 61% of U.S. adults used AI for shopping in 2025 (Capital One Shopping Research)
- 693% growth in AI-sourced retail traffic during the 2025 holiday season (Adobe Analytics)
- 15x YoY growth in AI-driven orders on Shopify stores since January 2025 (Shopify data)
- Perplexity Shopping: 57% higher average order value vs. other AI platforms (Alhena.ai)
- AI-referred shoppers: 31% higher conversion rate, 33% lower bounce rate (Adobe Analytics)
- ChatGPT Shopping: 900 million weekly active users
- Google AI Mode: 1 billion monthly active users as of May 2026
- Perplexity Shopping: 45 million monthly active users
- Amazon Rufus/Alexa for Shopping: 300 million customers in 2025
- 4 of 6 major AI crawlers fetch static HTML only — JS-rendered prices are invisible to them (Visively, 2026)
- Stores with 99.9% attribute completion get 3–4x higher visibility in Google AI Mode vs. sparse-data stores (ppc.land)
- 65% of pages cited by Google AI Mode include structured data (Capconvert)
- JSON-LD holds 89.4% market share for schema implementation (Alhena.ai)
- Only 3 of 10 mid-market stores successfully completed agent-initiated transactions end-to-end in a 2026 audit (OST Agency)

**Do NOT use these (unverified):**
- "32% product match accuracy" — no primary source
- "28% price error rate for ChatGPT" — h-haboubi.com only, no original study
- Morgan Stanley 10-20% agent-mediated ecommerce by 2030 — no primary link confirmed

---

## Semantic term coverage (creator must confirm all 25 terms present in draft)

From research section 10. Creator confirms coverage before final draft submission:

structured data, Schema.org, Product markup, GPTBot, Perplexity Shopping, ChatGPT shopping, agentic commerce, price comparison agent, crawler readability, machine-readable, JSON-LD, rich results, robots.txt, llms.txt, product feed, crawl budget, agent-readable, OpenAI Operator, AI browser agent, product availability signal, GTIN, server-side rendering (SSR), Merchant Center feed, Agentic Commerce Protocol (ACP), retrieval bot

---

## WordPress metadata

| Field | Value |
|---|---|
| Yoast title | How to make your ecommerce store readable to AI shopping agents \| Virtina |
| Yoast title char count | 72 characters — EXCEEDS 60-char limit |
| Recommended Yoast title | eCommerce store agent-ready: AI shopping agents guide \| Virtina |
| Recommended title char count | 63 characters — still over 60. Fallback: |
| Fallback Yoast title | Make your store readable to AI shopping agents \| Virtina |
| Fallback char count | 58 characters — PASS |
| Yoast metadesc (150–160 chars) | AI shopping agents skip stores with missing schema and JS-rendered prices. Learn what agent-ready means and the 6 steps to fix your store today. |
| Metadesc char count | 147 characters — PASS (within 150–160 range — confirm with tool before publishing) |
| Focus keyword | ecommerce store agent-ready |
| Categories | B2B eCommerce (84), eCommerce Development (415) |
| Tags | AI shopping, ecommerce, structured data, agentic commerce, AI agents |
| Author ID | 9 (Gigi JK) |
| Post status | draft |
| Featured media | TBD (sourced during publish stage) |

**Yoast title note for publisher:** The orchestrator-specified title "How to make your ecommerce store readable to AI shopping agents | Virtina" is 72 characters and exceeds the 60-character limit in MUST-FOLLOW-RULES section 8. Use the 58-character fallback above unless the user explicitly approves the longer version.

---

## Image plan (sourcing at publish stage — plan only)

| Image | Dimensions | Spec |
|---|---|---|
| Featured | 1309×500 | Person interacting with a futuristic shopping or tech interface — or modern office with data screens and product listings. No handshakes, no lightbulbs. Search terms: "ecommerce dashboard laptop", "office data screen business" |
| Body 1 (after section 3) | 670×352 | Developer or data analyst at laptop reviewing structured data or product listings. Clean, professional, desktop scene. Search terms: "macbook desk business work", "working typing computer desk" |
| Body 2 (after section 6) | 670×352 | Ecommerce manager at desk reviewing analytics or product data on screen. Business/office context. Search terms: "office team meeting computers", "coworkers office computer work" |

All images: JPEG quality 82, under 200 KB, alt text 80–150 chars with 1–2 article keywords naturally.

---

## Things the creator must NOT do

1. **Do not reuse the GEO or AEO explanation as the main thesis.** GEO is referenced only to explain the distinction from agent-readiness. The thesis is about transaction infrastructure, not content discoverability. (Conflict with ID 41531.)
2. **Do not explain internal AI store automation agents.** Chatbots, inventory agents, pricing AI — these are covered by ID 41142. Do not re-cover them.
3. **Do not use em dashes.** Replace with commas, colons, or periods. This is a hard ban per MUST-FOLLOW-RULES section 7.
4. **Do not exceed 3 sentences per paragraph.** Every paragraph, including PAA answers and FAQ answers.
5. **Do not open any H2 section with context-setting or background.** The first sentence of every H2 section must directly answer the question that H2 poses. This is the most important rule for LLM citation.
6. **Do not link to competitor sites** (shopify.com, bigcommerce.com, etc.) under any circumstances.
7. **Do not add more than 2 external links total** across the entire article. No exceptions.
8. **Do not use unverified statistics** — specifically the 32% match accuracy and 28% price error figures flagged in research section 11.
9. **Do not use banned words:** delve, leverage, revolutionary, game-changing, cutting-edge, transform, ecosystem, landscape, realm, navigate (as verb).
10. **Do not use Title Case headings.** All H2 and H3 headings must be sentence case.
11. **Do not invent Virtina client case studies.** The case/example snippet in section 4 is a scenario (not attributed to a named Virtina client). Keep it that way.
12. **Do not write the author byline as a self-promotional paragraph.** It is Template K: one sentence, name bolded, bio follows inline.

---

## Pre-publish checklist reminder

Before any PUT call, the publisher runs every item in MUST-FOLLOW-RULES section 9. Key flags for this post:

- Em dash grep: all four forms (`—`, `&mdash;`, `&#8212;`, `&#x2014;`) must return zero.
- External link count must be exactly 2.
- Every H2 has a matching `id` attribute in the HTML.
- TOC uses Template C with inline SVG arrows — no Unicode arrows, no Thrive class-based markup.
- All bullet lists use Template F (9×9px `#43627f` circle, 16px font, `#2d3e50` text).
- Yoast title: 60 chars max. Use the 58-char fallback above.
- Yoast metadesc: 150–160 chars. Verify with character counter.
- `featured_media` set to a real uploaded media ID, not 0.
- Word count: 2000–2500.
- Phrasing uniqueness: no 8+ word verbatim sequence with any existing post.

---

## Research file reference

Full research notes, competitor analysis, and source list:
`clients/virtina/output/research/ecommerce-agent-ready-2026-05-29.md`

Uniqueness audit:
`clients/virtina/output/research/uniqueness-audit-agent-ready-2026-05-29.md`
