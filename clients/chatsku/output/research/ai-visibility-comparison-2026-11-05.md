---
title: "Research: Build in-house or buy an AI catalog assistant (AI-visibility comparison post)"
client: chatsku
date: 2026-11-05
topic: Build vs buy for a B2B AI catalog assistant (decision/comparison post for AI citation)
audience: Owners, sales and ecommerce managers at B2B manufacturers, distributors, wholesalers
stage: research
slug: build-or-buy-ai-catalog-assistant
---

# Research notes: build vs buy an AI catalog assistant

Rules read: chatsku MUST-FOLLOW-RULES.md (sections 1, 6, 11, 11b), brand.md, voice.md, audience.md, memory notes on AI-visibility posts and Blog 2 (post 4078). Check date for all live-site facts: 2026-11-05.

## 1. Uniqueness verdict

Live corpus: 44 posts via REST /posts (newest 4078) plus clients/chatsku/output/research/chatsku-headings-2026-11-02.md (52 posts incl. drafts). Matched on H2/H3 text, not titles. /pages not swept (no Bash; REST list fetched through WebFetch for /posts only). Residual risk: pages (money pages) may hold build-vs-buy text. Analyzer should run a final H2 grep.

| Candidate | Overlap found | Verdict |
|---|---|---|
| (a) AI assistant vs site search vs live chat vs RFQ form | Post 3956 (AI sales agent vs chatbot vs sales rep: table, cost, choose). Post 3767 has H2 "Quote form vs live chat vs AI catalog assistant: side by side" plus "How do you choose between the three paths?". Post 2665 owns why site search fails. | HIGH overlap. Reject. |
| (b) PDF vs online catalog vs AI assistant | Posts 1, 215 ("Static PDF Catalogs Are a Dead End for Buyers"), 2665, 397, 216. | MEDIUM-HIGH overlap. Reject. |
| (c) Build in-house vs buy | Only partial: post 1880 PAA H3 "Should I build my own AI chatbot or buy one?" (3-sentence answer: upkeep, pricing logic, accuracy hard to sustain). Post 3461 (ChatGPT vs catalog chatbot) covers custom GPTs and file uploads as the DIY path, with H2 "Is a catalog chatbot worth it when ChatGPT costs so little?". Post 3798 PAA "Does a catalog assistant replace a developer?" (script tag; ERP and pricing may need technical help). Post 4078 and 4066 do not discuss build vs buy. | LOW overlap. CHOSEN, with fences below. |

Ownership fences for (c):
- Do NOT re-run the custom GPT / file upload comparison (3461 owns it). Treat it as one sentence and link.
- Do NOT re-explain retrieval mechanics (2468 owns embeddings, hybrid retrieval, RAG grounding). Link.
- Do NOT repeat the 7 catalog-readiness checks (4066) or the platform comparison (4078). Link.
- Do NOT repeat vendor questions list (1880). This post is about the decision to build, not vendor evaluation.
- Own: the decision itself, framed by the components a B2B catalog assistant needs, three paths (build on a model API, buy a purpose-built assistant, hybrid), who should build, total-ownership checklist, and a 90-day pilot test.
- Format per rule 11: D (decision tree / playbook). Recent formats: 4078 B, 4015 D, 3956 (A/B-ish). Format D was used by 4015 and 3010 already; Format B (question H2s) also suits AI extraction. Analyzer to choose and record; D with question-style H2s is recommended.

Suggested slug: `build-or-buy-ai-catalog-assistant` (no collision with any existing slug in the 44-post list).

## 2. Why this topic

- Real buyer question with a decision attached. Fits audience (budget authority, evaluating to buy).
- Fits product: brand.md themes "catalog-to-chat without site rebuilds" and ROI math; one-line deployment is a verified differentiator.
- Not a competitor-name post: compare approaches (build on a model API, buy a purpose-built assistant, hybrid) with no competitor product names.
- AI answers for the head question are dominated by vendor posts for B2C ecommerce, generic customer service bots, or analytics/ERP software. No neutral, B2B-catalog-specific answer (customer-group pricing, quote handoff, catalog sources like PDF/Excel/ERP). That is the gap.
- Honest limitation: I could not measure search volume (no keyword tool). "Most question-style searches" is not proven; the head phrasing "build vs buy AI chatbot" is clearly active (many ranking vendor posts), but the B2B-catalog variant is thin. Treat as [unverified] demand.
- Honest limitation 2: this topic is a "decision" post, not a product-vs-product post. It still earns a comparison table (three paths x named criteria).

## 3. What AI/search answers currently say (head question: "build vs buy AI chatbot for B2B product catalog")

Two WebSearch runs (2026-11-05). Observed sources cited by the search engine:
- alhena.ai, zipchat.ai, instantdm.com (ecommerce chatbot build vs buy; B2C framing; cost ranges vary by the same vendor between posts)
- auralis.ai, redwerk.com, searchunify.com, shelf.io, weav.com (generic enterprise/customer-service build vs buy)
- nobi.ai ("build your own site search with Claude or buy": the closest to our topic, vendor)
- phocassoftware.com "Build vs. buy in the age of AI: the question every distributor is asking" (distributor audience, but about analytics/ERP data platforms, not catalog assistants; undated)
- wizcommerce.com "build vs buy AI order entry software" (B2B, order entry not catalog Q&A)
- dev.to write-ups (hybrid agent for guided selling)

Consensus answer in these sources: buy by default; build only when AI is core IP, rules are unusual, or data-control is strict; hybrid is common; maintenance never ends. Almost all are vendors with a stake.

Gaps ChatSKU can fill:
1. No source ties build vs buy to B2B catalog specifics: per-customer pricing, customer groups, MOQ/pack rules, cross-references, quote handoff, after-hours capture.
2. No source gives a short "who should actually build" test with plain criteria for a $1M-$50M manufacturer/distributor with no AI team.
3. No source separates what the model vendor provides (hosted retrieval) from what you still build (auth, pricing, quote, review, analytics).
4. Cost figures conflict widely and are unsourced. Opportunity: refuse to quote numbers, give a cost-of-ownership checklist instead.

## 4. Neutral, primary-source facts (usable)

Check date 2026-11-05.

1. OpenAI Assistants API: announced deprecated 2025-08-26, shutdown 2026-08-26, replaced by Responses API and Conversations API. Source: https://developers.openai.com/api/docs/deprecations. Use: a custom build depends on a model vendor's API lifecycle; plan migrations. Same page lists other shutdown dates (e.g. gpt-3.5-turbo-instruct and others on 2026-09-28), showing recurring retirements. Note: the Assistants shutdown date (2026-08-26) has already passed as of today, so write in past tense and verify wording on the page at build time.
2. OpenAI file search (hosted retrieval) lets a model search uploaded files via vector stores, and OpenAI hosts the tool. The developer still creates the vector store, uploads and waits for processing, sets result count and metadata filters. Source: https://developers.openai.com/api/docs/guides/tools-file-search. Use: the model vendor supplies retrieval; it does not supply buyer login, customer-specific pricing, quote capture or review workflow. (Inference, flag as ChatSKU's reading, not the doc's claim.) The page does not state a max file size; do not claim one.
3. OWASP Top 10 for LLM Applications, 2025 edition: ten risks including Prompt Injection (LLM01), Sensitive Information Disclosure (LLM02), Excessive Agency (LLM06), Misinformation (LLM09), Unbounded Consumption (LLM10). Source: https://genai.owasp.org/llm-top-10/. Use: a buyer-facing assistant that sees prices needs a security review; each risk is a build task.
4. Google on AI features: a page can be a supporting link in AI Overviews / AI Mode if it is indexed and eligible for Search with a snippet; Google states no additional technical requirements and no special markup or AI text files needed. Source: https://developers.google.com/search/docs/appearance/ai-features. IMPORTANT for rule 11b item 8: do not claim schema boosts AI citation. Use FAQ/Article schema only as normal structured data consistent with visible text, and say nothing about guaranteed lift.

Facts to avoid (unverifiable or vendor-only):
- Any build cost range ($13K-$25K, $150K-$400K, $77K-$168K) and any "67% vs one-third success" claim (Rework page citing Hyperion, not verifiable).
- "70% complete attribute data" threshold (single vendor guide).
- Phocas/DSG distributor AI adoption percentages (93%, 16%, 4.5x etc.): secondhand via a vendor blog; verify at DSG primary or skip.
- Anything from DCatalog/Publitas about PDF conversion rates.

Conflicts between sources: the same ecommerce vendor gives two different build-cost ranges in two posts; vendors disagree on timelines. Handled by not quoting numbers.

## 5. Comparison criteria buyers use (for the table)

Derived from the ranking sources plus ChatSKU's own buyer's guide (1880) and B2B specifics. Table: 3 paths (Build on a model API / Buy a purpose-built assistant / Hybrid) x criteria:
1. Time to first live answer (build: depends on your team [unverified, avoid numbers]; ChatSKU: setup in under one day on average per home page, same-day for most per FAQ)
2. Catalog sources it must read (PDF, Excel, CSV, ERP sync; ChatSKU FAQ lists CSV, PDF extraction, manual entry, HTML listings, platform/ERP sync)
3. Buyer-specific pricing (customer groups, tiers). ChatSKU supports; NOTE free trial excludes customer groups and tiered pricing (pricing page).
4. Quote / RFQ handoff
5. Preventing invented answers (grounding, refusal, handoff)
6. Security and data ownership (OWASP risks; ChatSKU FAQ: encrypted in transit and at rest, customer owns data, not sold)
7. Who maintains it (model changes, catalog refresh, price updates)
8. Analytics on unanswered questions / buyer intent
9. Control and exit (export, portability)
10. Cost shape (build: staff time + usage; buy: subscription or performance fee; ChatSKU public structure below)

Cells for the build column must be neutral ("you build and own this"), not disparaging. Include "When build is the right call" honestly (AI is core product, unusual product-rule logic, strict data control, in-house engineers with a roadmap).

## 6. ChatSKU facts available (verified on live site 2026-11-05)

Entity sentences on site: home page: "converts an existing product list into an always-on buying assistant that handles buyer questions, quotes, and orders without a website rebuild." FAQ: "B2B chat-commerce plugin that adds AI product search, chat, and quote requests to your website." Footer on 4078: "AI-powered chat commerce for B2B businesses" (avoid "AI-powered" per voice). Use a consistent line per brand.md: ChatSKU is an AI catalog assistant that turns existing PDF, Excel and ERP catalogs into a 24/7 assistant that answers buyer questions and builds quotes, for manufacturers, distributors and wholesalers.

Features listed (home/FAQ/features):
- Product chat: stock, lead time, spec questions; offers to start a quote
- Natural-language product search and filtering
- In-conversation quote building; order capture; RFQ workflows and quote management
- Kate O'Log, AI phone agent (answers calls, spec/fitment/pricing answers, orders, leads, quotes). Not in brand.md; confirm before featuring.
- Catalog ingestion: PDF, Excel/CSV, existing store catalogs; up to 10 images per product; configured by the Virtina team
- Single-line embed script; setup under one day on average
- Customer import via CSV; sync with CRM, eCommerce platform or ERP
- Customer groups, group-specific pricing/discounts, tiered pricing
- Buyer intent and behavior analytics
- Image search, cross-reference support, custom branding (pricing page)
- Security (FAQ): encryption in transit and at rest; customer owns data, not sold; GDPR DPAs, deletion requests; hCaptcha on quote forms

Pricing page (/chatsku-pricing/): Subscription = setup from $2,500 + from $299/month; Performance-based = no setup/monthly, 0.75% of revenue ChatSKU generates; Free trial no card/contract, ends at first of 3 orders, 6 quotes, 6 leads or 60 days; caps 10,000 SKUs, 500 PDF pages. Both paid plans: same features, unlimited SKUs. Trial excludes image search, customer groups and tiered pricing, ERP/eCommerce/PIM/IMS/WHMS integration, cross-reference, custom branding, analytics. FAQ page says "plans custom, no public price list" - CONFLICT with pricing page. Use pricing page (more specific, newer-looking); flag to user. Decision for the analyzer: quoting price numbers is a verifiable fact but dated; state check date or omit. Rule: do not promise customer groups/tiered pricing in trials.

## 7. Verified live URLs (loaded via WebFetch 2026-11-05; WebFetch does not return raw HTTP codes, so "loaded" = content rendered)

Pages:
- https://chatsku.com/ (home)
- https://chatsku.com/demo/ (H1 "See ChatSKU in action"; widget showed "Loading demo...")
- https://chatsku.com/features/ (thin: H1 "Everything you need to sell smarter", no feature headings visible to fetch)
- https://chatsku.com/chatsku-pricing/
- https://chatsku.com/faq/
- https://chatsku.com/signup/ (linked as CTA site-wide; not fetched directly)
- https://chatsku.com/roi-calculator/ (linked sitewide; not fetched directly)
- https://chatsku.com/rfq-automation-for-product-catalogs/ LOADED as a real RFQ page (title "RFQ Automation for B2B Product Catalogs | ChatSKU", H1 "Your website has products. Why aren't buyers finding them?"). The rules file says DO NOT USE (it served homepage content on 2026-08-18). That is now STALE. Recommend updating section 6 and using it. Note the user's task names it as a page AI should see.
- https://chatsku.com/shopify-b2b-chatbot/ (loaded)
- https://chatsku.com/bigcommerce-b2b-chatbot/ (loaded; rules say copy errors exist, do not rely on its text)
- https://chatsku.com/magento-b2b-chatbot/ (loaded)
- No WooCommerce solutions page in nav (confirmed absent from site menu).
- https://chatsku.com/ai-sales-assistant-b2b-ecommerce/, /for-b2b-manufacturers-distributors-and-wholesalers/, /pdf-catalog-chatbot/ appear in the live nav (not individually fetched).

Posts (all loaded):
- https://chatsku.com/chatgpt-vs-catalog-chatbot/ (3461; the DIY/custom GPT fence)
- https://chatsku.com/ai-chatbot-buyers-guide/ (1880; build-or-buy PAA)
- https://chatsku.com/who-b2b-catalog-assistant-is-built-for/ (3798)
- https://chatsku.com/is-your-b2b-catalog-ready-for-ai-chatbot/ (4066)
- https://chatsku.com/best-b2b-platforms-for-catalog-chatbot/ (4078, live, dated 2026-11-04)
- https://chatsku.com/ai-sales-agent-vs-chatbot-vs-sales-rep/ (3956; in REST list, not individually fetched)
- https://chatsku.com/how-ai-product-search-works/ (2468; in REST list)
- https://chatsku.com/erp-export-ai-agent-ready/ (2684; in REST list)
- https://chatsku.com/tiered-b2b-pricing-online/ (3039; 301s to the long slug, use /one-catalog-a-thousand-prices-making-tiered-b2b-pricing-work-online/)
- https://chatsku.com/one-line-of-code/ (2044; in REST list)
- https://chatsku.com/inquiry-tracking-seven-day-count/ (4015; in REST list)

Not verified per-URL: any link not marked "loaded". Orchestrator should confirm 200 via REST/status before publishing (rule: no 404s).

## 8. External links (max 2 allowed; no competitors)

Candidates, all non-competitor primary sources:
1. https://genai.owasp.org/llm-top-10/ (security checklist)
2. https://developers.openai.com/api/docs/deprecations (API lifecycle). Fits: it is a model vendor's doc, not a competitor chatbot tool. Judgment call for orchestrator; alternative is the Google AI features page for an AI-visibility aside (not recommended in body).

## 9. Risks

1. Partial overlap with 1880 PAA, 3461 DIY section, 3798 PAA. Mitigation: fences above, link to them, 8-gram check against all three.
2. Build-vs-buy is commercially biased coming from a vendor. Mitigation: include an honest "when to build" section; no invented cost numbers; no disparaging build.
3. Pricing page vs FAQ conflict (public prices vs "custom"). Confirm which is current before quoting any price.
4. Trial excludes customer groups/tiered pricing: do not imply the trial shows them.
5. Rules-file staleness: /rfq-automation-for-product-catalogs/ now a valid RFQ page; rules still ban it.
6. Schema: Google states no special markup for AI features. Do not claim AI visibility from schema; keep FAQ schema factual. Do not promise AI citation.
7. OpenAI Assistants API shutdown date (2026-08-26) has passed; phrase in past tense and re-read the page when drafting.
8. No search-volume data; "most question-style searches" is unproven.
9. Kate O'Log phone agent appears on the home page but not in brand.md; confirm before mentioning.
10. Fetch tool cannot confirm HTTP status codes; /pages not swept via REST.
11. Competitor names: search results name several vendors (e.g. in build-vs-buy pages); none to be named or linked.

## 10. Proposed H2 questions (for the analyzer to refine)

1. Should you build or buy an AI catalog assistant? (direct answer first)
2. What does a B2B catalog assistant have to do beyond answering questions?
3. What do you build yourself on a model API, and what does the model vendor give you?
4. How do the three paths compare? (table)
5. What does the build path cost you after launch? (maintenance list, no dollar figures)
6. When is building the right call?
7. What does a hybrid look like?
8. How do you test the decision in 30 days?
9. People Also Ask, Conclusion, FAQ

Primary question for the AI head query: "Should a distributor build its own AI catalog assistant or buy one?"
