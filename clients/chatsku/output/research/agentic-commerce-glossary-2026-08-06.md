---
title: Agentic commerce glossary - what manufacturers actually need to know
client: chatsku
date: 2026-08-06
topic: Agentic commerce terminology for B2B manufacturers and distributors
audience: Sales/eCommerce leaders at manufacturers, distributors, wholesalers ($1M-$50M revenue, 10-200 employees)
stage: research
slug: agentic-commerce-glossary
---

# Research notes: agentic commerce glossary for B2B manufacturers

## 0. Uniqueness check (per MUST-FOLLOW-RULES.md section 1)

Read `clients/chatsku/reference/published-posts-inventory.md` in full plus fetched the live `/blog/` (3 pages) to catch posts added after the inventory's last update (2026-07-27).

**Untracked live posts found (not yet in inventory file) that are directly relevant:**

1. **"AI Agents Are Buying for Your Customers Right Now: Is Your Catalog Ready for Them?"** - https://chatsku.com/ai-ready-b2b-catalog-autonomous-buying/. Narrative/persuasive piece (not a glossary), thesis: B2B distributors must make catalogs machine-readable before autonomous procurement agents mediate most buying. Four H2 sections build a general urgency case. It uses "AI agents," "agentic commerce," and "machine-readable catalog" as working phrases but does not formally define them and does not mention ACP, AP2, MCP, A2A, Visa, or Mastercard by name. It cites two figures with **no source attribution**: "AI agents will intermediate 90% of B2B purchasing, routing over $15 trillion in annual spend by 2028" and "first vendor returning accurate quote captures 70% of business." Both are unsourced in the live post.
2. **"5 Minutes to 24/7 Sales: How to Turn Your B2B Catalog Into an AI Buying Assistant"** - https://chatsku.com/24-7-b2b-ai-buying-assistant/ (title only, not fetched in depth; relevant as an internal-link candidate, not a glossary competitor).
3. **"The Response Gap Is Costing You Deals: 3 Steps to Quote in Under 1 Hour"** - https://chatsku.com/reduce-b2b-quote-response-time/ (title only; not glossary-relevant).
4. **"Funnel Inversion: Why Answer First Beats Capture First in B2B"** - https://chatsku.com/funnel-inversion-answer-first/ (title only).
5. **"Your Buyers Want Answers, Not a Callback: Why B2B Customers Leave for Faster Competitors"** - https://chatsku.com/b2b-customers-leave-for-faster-competitors/ (title only; noted in post 1300's dedup log as excluded angle already).

None of these are glossary/reference format. None formally defines ACP, AP2, MCP, A2A, Visa Intelligent Commerce, or Mastercard Agent Pay. This clears the way for a definitional glossary, provided it does not re-run the "why machine-readable catalogs matter" persuasive argument as its spine, and does not reuse the unsourced "$15 trillion / 90% by 2028" or "70% of business" figures from `ai-ready-b2b-catalog-autonomous-buying` without independent sourcing (see Statistics section - I found a possible primary trail for the $15T/90% figure, but it traces to a conference remark, not a published report, and must be labeled as a forecast, not current adoption).

**Existing post that already touches agentic commerce: "The 11 stages of B2B commerce evolution"** (ID 1820, `b2b-commerce-evolution`, live at https://chatsku.com/b2b-commerce-evolution/). Confirmed by direct fetch:
- Stage 10 ("Agentic commerce") is defined only as: "software agents that negotiate, procure, and reorder on a buyer's behalf" without human involvement in every loop.
- Stage 11 ("Fully autonomous B2B purchasing") is defined only as: "machine-to-machine buying, with humans setting the rules instead of clicking the buttons," projected around 2028.
- The article does **not** name or define ACP, AP2, MCP, A2A, Visa Intelligent Commerce, or Mastercard Agent Pay anywhere.
- It's a maturity-model listicle (Format C), not a definitional reference.
- It uses a "72% self-service" stat that the inventory itself flags as user-supplied and never independently sourced - **do not reuse this stat in the glossary without independent verification** (I could not independently verify it either; treat as still unverified).

**What the glossary must NOT re-explain to avoid cannibalizing post 1820:**
- Do not re-present the 11-stage maturity model or reuse its stage numbering/names.
- Do not re-argue "where does your company stand" self-assessment framing.
- Do not reuse the 72% stat.
- Keep the one-sentence definitions of "agentic commerce" and "autonomous purchasing" **more technical and sourced** than 1820's plain-language versions - the glossary's job is to name the actual protocols and standards bodies behind the concept, which 1820 deliberately left out (it's a strategy piece, not a reference piece).
- Good practice: link to 1820 as "read the full maturity model" for readers who want the strategic narrative, while the glossary itself stays reference-format.

**What the glossary must NOT re-explain to avoid cannibalizing `ai-ready-b2b-catalog-autonomous-buying`:**
- Do not build the glossary's persuasive spine around "your catalog must be machine-readable before autonomous agents take over." That is that post's core argument.
- Do not reuse its unsourced 90%/$15T or 70%-of-business figures without attribution; if used, must be re-sourced independently (see below) and clearly labeled as a forecast.

**Slug check:** proposed slug `agentic-commerce-glossary` does not match any existing slug in the inventory or the three fetched blog-listing pages.

---

## 1. Terminology sweep

Every term below was checked against a primary or near-primary source. Status label explains what kind of thing it actually is.

### A. Core concepts

**Agentic commerce**
- Plain-English definition: buying and selling where an AI agent researches, decides, and completes some or all of a purchase on a person's or company's behalf, without a human clicking "buy" at every step.
- Status: **industry term**, not owned by one standards body. Used consistently across OpenAI, Stripe, Google, Visa, and Mastercard material, but no single authoritative definition body.
- Why a manufacturer should care: this is the umbrella term for everything below. If a buyer's procurement software can query your catalog and place an order without a human reading your website, you're inside this category whether you planned for it or not.

**AI agent**
- Plain-English definition: a piece of software that can take multi-step actions (search, compare, fill a cart, submit a payment) toward a goal, instead of just answering a single question.
- Status: general AI/ML industry term, not commerce-specific.
- Why care: distinguishes a chat assistant that answers questions from a system that can actually execute the RFQ or order for the buyer.

**Autonomous purchasing**
- Plain-English definition: a purchase completed by software with no human approval step at the moment of payment, usually inside pre-set rules (budget cap, approved vendor list, quantity limits).
- Status: descriptive term used across the industry and inside Gartner's public commentary; not a formal spec name.
- Why care: this is the end state manufacturers hear about most and fear most. It's still narrow in practice today (see Statistics section on Instant Checkout's real merchant count).

**Conversational commerce vs. agentic commerce (the distinction)**
- Conversational commerce: a chat interface where the buyer talks through questions, pricing, and a quote, but a human still confirms and completes the transaction. ChatSKU's own post 380 (`b2b-conversational-commerce`) frames this as a B2B operations layer, not a checkout replacement.
- Agentic commerce: the software itself completes the transaction end-to-end, with the human setting rules in advance rather than approving each step.
- Status: this distinction is standard across industry usage (Fireblocks glossary, Mohammed Shehu's 110-term glossary, and ChatSKU's own prior post all draw the same line: presence vs. absence of a human approval step at the moment of transaction).
- Why care: most manufacturers today are living in conversational commerce (RFQ chat, quote-building chat), not agentic commerce. Conflating the two overstates where the market actually is.

**Instant Checkout / in-chat purchase flows**
- Plain-English definition: a feature that let a ChatGPT user complete a purchase inside the chat window itself, without leaving the conversation.
- Status: **real feature, launched, then substantially scaled back** - this is the most important accuracy correction to make.
- Timeline (verified):
  - Launched September 29, 2025 by OpenAI and Stripe, first partner Etsy, powered by the newly released Agentic Commerce Protocol. [Stripe newsroom](https://stripe.com/newsroom/news/stripe-openai-instant-checkout)
  - Expanded February 16, 2026 as "Buy it in ChatGPT" with Shopify merchants (Glossier, SKIMS, Spanx, Vuori named) and PayPal added as an ACP-compliant payment server.
  - **By February 2026, only roughly 30 Shopify merchants were actually live on it**, per Forrester principal analyst Emily Pfeiffer - a rounding error against the "over a million" merchant figure that was promoted at launch. [Forrester blog](https://www.forrester.com/blogs/what-it-means-that-the-leader-in-agentic-commerce-just-pulled-back/)
  - **March 24, 2026: OpenAI ended in-chat checkout.** Checkout completed inside ChatGPT converted at roughly one-third the rate of sending the same shopper to the merchant's own site to finish the purchase. OpenAI is redirecting purchases to merchant-built "Apps" inside ChatGPT or back to the merchant's own site. [CNBC coverage via search corroboration; Forrester blog above]
  - ACP itself did not die - it was repurposed from a checkout protocol toward product discovery and feed standardization, with continued Stripe/OpenAI maintenance.
- Why a manufacturer should care: this is the single most-hyped agentic commerce feature, and it is materially less live than most 2026 SEO content still implies. A glossary that reports it as a thriving, in-chat, million-merchant checkout channel would be publishing something already outdated by five months. This correction is a genuine differentiator - the competitive scan (section 3) shows most existing glossaries still describe ACP/Instant Checkout in launch-day terms.

### B. Protocols and standards (verify status honestly)

**Agentic Commerce Protocol (ACP)**
- What it is: an open interaction standard, co-developed by OpenAI and Stripe, for how a buyer's AI agent discovers products, negotiates a cart, and completes a payment with a merchant, using a "Shared Payment Token" so the agent never sees raw card data.
- Status: **real, shipped, currently maintained**, but its scope shifted (see Instant Checkout above) from checkout toward product discovery and feed structure as of March 2026. Latest spec activity dated April 17, 2026 per third-party protocol trackers (treat that specific date as [unverified] - I could not confirm it on a primary GitHub/Stripe page directly).
- Source: [GitHub - agentic-commerce-protocol](https://github.com/agentic-commerce-protocol/agentic-commerce-protocol), [Stripe: Developing an open standard for agentic commerce](https://stripe.com/blog/developing-an-open-standard-for-agentic-commerce), [Stripe docs](https://docs.stripe.com/agentic-commerce/acp)
- Why care: B2B manufacturers selling on Shopify or through a merchant catalog connected to ChatGPT are the ones this protocol touches directly. It is B2C-shopping-flavored in its current implementations (Etsy, Shopify DTC brands) - no confirmed B2B distributor or manufacturer implementation was found in this research.

**AP2 (Agent Payments Protocol)**
- What it is: an open protocol from Google that gives an AI agent a cryptographically signed, verifiable "permission slip" from a human before the agent can spend money. It chains three signed Mandates: an **Intent Mandate** (what the user authorized and under what constraints), a **Cart Mandate** (the exact items/price the user approved), and a **Payment Mandate** (a minimal, network-facing credential derived from the cart, flagging whether a human was present at the moment of purchase).
- Status: **real, announced September 16-17, 2025**, with 60+ launch partners including PayPal, Mastercard, American Express, Coinbase, Salesforce, and ServiceNow. Google has since donated AP2 to the FIDO Alliance to make it an industry standard rather than a Google-owned spec. Can extend the A2A protocol and be used alongside MCP.
- Source: [Google Cloud Blog announcement](https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol)
- Why care: this is the piece manufacturers should ask their ERP/payments vendors about if a customer's procurement agent wants a cryptographic paper trail before it will authorize a purchase.

**MCP (Model Context Protocol)**
- What it is: an open standard, introduced by Anthropic in November 2024, that lets an AI model connect to external data sources and tools through one consistent interface, instead of a custom integration for every system. Commonly described as "a USB-C port for AI applications."
- Status: **real, shipped, widely adopted** as general AI infrastructure - not commerce-specific on its own, but AP2 explicitly can run as an extension of MCP, and it's the plumbing that lets an agent read a manufacturer's product data in the first place.
- Source: [Anthropic: Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
- Why care: MCP is not a payment or checkout protocol. It's the connective layer that could let a buyer's AI agent query your ERP or catalog data directly, IF you expose an MCP-compatible interface. Most manufacturers don't have one yet.

**A2A (Agent2Agent Protocol)**
- What it is: an open protocol that lets AI agents built by different vendors discover each other, authenticate, and hand off tasks, using standard web technology (HTTP/HTTPS, JSON-RPC, OAuth 2.0).
- Status: **real, released April 2025** by Google, now governed by the Linux Foundation with 50+ contributing partners (Atlassian, Box, PayPal, Salesforce, SAP, ServiceNow, and others).
- Source: [Google Developers Blog announcement](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/), [A2A GitHub](https://github.com/a2aproject/A2A)
- Why care: this is the protocol most relevant to a future where a buyer's procurement agent talks directly to a seller's sales agent (agent-to-agent negotiation). Not yet common in B2B manufacturing; still early infrastructure.

**Visa Intelligent Commerce / Visa Trusted Agent Protocol**
- What it is: Visa's framework for authenticating, authorizing, and tokenizing payments initiated by AI agents on its network. "Intelligent Commerce Connect," announced for pilot in April 2026, gives merchants and agent builders one integration point into the system.
- Status: **real, announced April 30, 2025** (Intelligent Commerce), with the Trusted Agent Protocol following October 14, 2025, and Intelligent Commerce Connect piloting from April 8, 2026.
- Source: [Visa newsroom](https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.21361.html), [Visa Payments Forum 2026 coverage](https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.22491.html)
- Why care: this is card-network infrastructure, not a B2B-specific tool. Relevant mainly if your buyers pay by card through an agent; most B2B manufacturer transactions run through invoicing, ACH, or net terms, not card rails, so the direct relevance is currently limited - flag this honestly rather than overstating it.

**Mastercard Agent Pay / Agent Pay for Machines (AP4M)**
- What it is: Mastercard's framework for letting verified AI agents transact using "Agentic Tokens" (a card credential bound to a specific agent, merchant scope, and consent policy). Agent Pay for Machines, launched June 2026, extends this to high-frequency, low-value, machine-to-machine payments.
- Status: **real, announced April 29, 2025** (Agent Pay) with Microsoft, IBM, and Braintree as launch partners; AP4M announced June 10, 2026 with 30+ organizations including Adyen, Coinbase, Stripe, and Checkout.com.
- Source: [Mastercard press release, April 2025](https://www.mastercard.com/global/en/news-and-trends/press/2025/april/mastercard-unveils-agent-pay-pioneering-agentic-payments-technology-to-power-commerce-in-the-age-of-ai.html), [Mastercard AP4M press release, June 2026](https://www.mastercard.com/us/en/news-and-trends/press/2026/june/mastercard-launches-agent-pay-for-machines.html)
- Why care: same caveat as Visa above - card-rail infrastructure, most relevant to consumer/card-based transactions, not yet a dominant channel for B2B manufacturer sales.

### C. Vendor jargon vs. real terms (label honestly)

**Agentic Commerce Optimization (ACO)**
- Status: **not a standard, not a spec.** It's marketing/agency terminology (seen in aggregator glossaries like Mohammed Shehu's and various "AI visibility" agencies) analogous to how "SEO" describes a practice, not a body. Treat as a practice-description term, not something with a governing authority.
- Why care: if a vendor pitches "ACO services," know that this is a coined term, not a certification or protocol.

**AEO / GEO (Answer Engine Optimization / Generative Engine Optimization)**
- Status: **industry jargon**, no single standard body, but widely used descriptively across SEO/content marketing to mean structuring content so AI assistants can extract and cite it directly, rather than ranking it in a list of blue links.
- Why care: this determines whether ChatGPT, Perplexity, or a shopping agent can find and correctly quote your specs, pricing, and availability at all - a prerequisite to being usable in any agentic flow.

**Machine-readable catalog / structured product data / product feed**
- Status: **descriptive term**, not one formal spec, though it's operationalized through real standards (GS1/GTIN, schema.org Product markup, ACP's product feed format, platform-specific feed specs from Shopify/Google Merchant Center).
- Why care: this is the actual prerequisite work behind most of the hype. A catalog an AI agent can parse reliably (consistent SKUs, structured attributes, real-time price/availability) is different from a catalog that's just "on the internet."

**Agent-readable pricing / contract pricing / customer-specific pricing**
- Status: descriptive term, not a formal spec. In B2B specifically this maps onto existing customer-group/tiered-pricing logic (ChatSKU's own domain) that now also has to be exposed in a way an external agent could query, not just a logged-in human buyer.
- Why care: none of the protocols above (ACP, AP2) currently define a standard way to expose B2B contract-specific pricing to an outside agent. This is a real, unsolved gap - worth naming plainly rather than implying it's already solved.

**"Hallucinated specs" / price integrity / guardrails**
- Status: descriptive risk terms, not formal specs. AP2's Cart Mandate is explicitly designed to address "what you see is what you pay for" price integrity at the payment layer, but nothing in ACP or AP2 guarantees an agent won't misstate a technical spec (tolerance, voltage rating, material grade) when summarizing a product to a buyer.
- Why care: this is the single biggest practical risk for a manufacturer with technically complex SKUs - an agent confidently repeating a wrong spec to a buyer, with no protocol currently responsible for catching that.

### D. Data standards manufacturers likely already have

**GS1 / GTIN (Global Trade Item Number)**
- What it is: the globally unique product identifier GS1 issues and manages; GS1 is "the only authorised source for GTINs worldwide."
- Status: real, long-established standard.
- Source: [GS1.org - GTIN](https://www.gs1.org/standards/id-keys/gtin)
- Why care: if your SKUs already have GTINs, you have a head start on the "unique, verifiable identifier" requirement that agentic product-discovery feeds are built around.

**UNSPSC (United Nations Standard Products and Services Code)**
- What it is: an open, global classification code (eight-digit, four-level hierarchy) for products and services, owned by the UN Development Programme, with GS1 US as code manager since May 2003.
- Status: real, established standard, used heavily in procurement/spend-analysis systems.
- Source: [UNDP - UNSPSC](https://www.undp.org/unspsc)
- Why care: many enterprise procurement systems (the kind that would run an autonomous purchasing agent) already require UNSPSC codes for spend categorization - if your catalog lacks them, that's a blocker independent of any AI protocol.

**ETIM**
- What it is: an open technical classification standard for electrical, electronic, and technical products, pairing each product class with a defined set of features and controlled value lists, widely used across Europe.
- Status: real, established standard, sector-specific (electrical/technical/MRO).
- Source: [ETIM International](https://www.etim-international.com/)
- Why care: manufacturers of technical/electrical products already using ETIM have machine-readable, filterable attribute data - exactly the format an AI shopping agent needs to compare specs.

**PIM (Product Information Management)**
- What it is: a category of software for centralizing, standardizing, enriching, and syndicating product data across channels.
- Status: real software category, not a single spec. (ChatSKU already published a full post on this: `product-information-management-software`, ID 1538 - the glossary should link to it rather than re-explain PIM in depth.)
- Why care: a PIM organizes data; it does not itself answer a buyer's question or complete a transaction, which is ChatSKU's own established distinction from post 1538.

**Punchout / cXML / OCI**
- What it is: punchout is the general process where a buyer's procurement system connects to a supplier's catalog to shop and return a cart for PO creation. cXML (Commerce eXtensible Markup Language) and OCI (Open Catalog Interface, developed by SAP) are the two data formats that carry that connection.
- Status: real, long-established B2B procurement standards, predate the current AI wave by two decades.
- Why care: many enterprise buyers ChatSKU's own customers sell to already have punchout infrastructure. This is worth distinguishing clearly from agentic commerce: punchout is buyer-system-initiated and rules-based; agentic commerce is AI-agent-initiated and can act with more autonomy. They can coexist - punchout is not being replaced by agentic protocols in this research window.

**EDI (Electronic Data Interchange)**
- What it is: the long-established standard (ANSI X12 in the US, EDIFACT internationally) for structured document exchange (POs, invoices, ASNs) between trading partners' systems.
- Status: real, decades-old standard, not new. Included here only because manufacturers should know it is a distinct, older layer from the AI-agent protocols above, not something ACP/AP2 replace.

### E. Trust / identity / guardrails

**Agent authentication / delegated authority**
- Status: descriptive concept, operationalized differently by each protocol - A2A uses Agent Cards and OAuth 2.0; AP2 uses signed Mandates; ACP uses Shared Payment Tokens.
- Why care: "does the agent actually have permission to buy this" is the trust question every one of these protocols is trying to solve differently. There is no single universal answer yet.

**Human-in-the-loop**
- Status: general AI/ML industry term, not commerce-specific, but directly relevant - it describes any workflow where a human must approve an agent's action before it executes (as opposed to full autonomous execution).
- Why care: today, most real B2B agentic-flavored tools (including ChatSKU's own quote-building) are human-in-the-loop by design. Fully autonomous, no-human-approval purchasing (AP2's "human-not-present" flag) remains the less common case in practice.

---

## 2. Statistics

### Usable, verified

1. **"67% of B2B buyers prefer a rep-free buying experience."** Source: Gartner Sales Survey press release, March 9, 2026. [gartner.com](https://www.gartner.com/en/newsroom/press-releases/2026-03-09-gartner-sales-survey-finds-67-percent-of-b2b-buyers-prefer-a-rep-free-experience) - **Caution: this exact stat is already used in at least five other live/draft ChatSKU posts** (380, 685, 1056, 1300, 1538, 1880). If reused here, it should be attributed and not treated as a fresh finding; consider whether the glossary needs it at all given the overuse, or use a different Gartner figure instead.

2. **OpenAI's Instant Checkout had roughly 30 live Shopify merchants by February 2026**, against an initial "over a million" merchant promotion at the September 2025 launch, before OpenAI discontinued in-chat checkout on March 24, 2026. Source: Forrester analyst Emily Pfeiffer, cited in [Forrester's blog on the pullback](https://www.forrester.com/blogs/what-it-means-that-the-leader-in-agentic-commerce-just-pulled-back/); corroborated independently by multiple trade outlets (Digital Commerce 360, MarketScale). This is the strongest, most differentiated stat available - it directly corrects the vendor-hype narrative most competing glossaries still repeat.

3. **AP2 launched September 16-17, 2025 with 60+ payments and technology partners** (PayPal, Mastercard, American Express, Coinbase, Salesforce, ServiceNow, and others named). Source: [Google Cloud Blog, primary announcement](https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol). This is a factual adoption/partner-count figure, not a projection, and directly primary-sourced.

### Rejected or flagged UNVERIFIED

- **"AI agents will intermediate 90% of B2B purchasing, routing over $15 trillion in annual spend by 2028."** Traces to Gartner analyst Daryl Plummer's remarks at Gartner IT Symposium/Xpo, reported via Digital Commerce 360 (Nov 28, 2025) and echoed by several secondary outlets (MarketScale, GSPann). I could not load the Gartner press release directly (403 error on gartner.com) to confirm this appears in a formal published document rather than only conference remarks. **Label as a forecast/prediction attributed to a named Gartner analyst, not as measured current adoption, and do not present it as a settled fact.** This is also the same unsourced figure the untracked ChatSKU post `ai-ready-b2b-catalog-autonomous-buying` already uses without citation - if the glossary uses it, it must add the sourcing that post is missing, or should avoid it to sidestep repeating an already-shaky number.

- **"94% of B2B buyers used generative AI during their most recent purchase" (attributed to Forrester's State of Business Buying, 2026).** I fetched Forrester's own press release for this report directly. It does **not** contain that statistic. It does state "94% of buyers with groups of six or more report clear benefits" - a completely different metric (about buying-group size benefits, not AI usage). Multiple aggregator sites (Semrush, Creatuity, machinerelations.ai) appear to have conflated these two different 94% figures from the same report. **Do not use this stat under any framing** - it fails primary-source verification and shows a clear conflation pattern.

- **"50 million shopping queries daily" (ChatGPT shopping volume).** Found only via secondary aggregator (Opascope), never independently corroborated by a primary OpenAI or Stripe source in this research pass. Reject as unverified.

- **"71% of buyers use AI search tools for vendor research" (attributed to G2, March 2026).** Found only via a secondary aggregator summary, not fetched from a primary G2 report. Flag as [unverified] - do not use without independently locating the G2 source.

- **"72% self-service" stat used in ChatSKU's own post 1820.** Already flagged in that post's inventory entry as user-supplied and never independently sourced. I could not independently verify it either. Do not reuse.

**Note on shared-source risk:** the $15T/90%-by-2028 figure and the "70% of business to fastest quote responder" figure both originate from the same untracked, unsourced ChatSKU post (`ai-ready-b2b-catalog-autonomous-buying`). Per the stat-verification rule, since one of these is already flagged unverified, treat the other as equally suspect even though it wasn't separately checked in depth here.

---

## 3. Competitive scan

**Search patterns used:** "agentic commerce glossary," "agentic commerce terms," "AI commerce glossary," "agentic commerce glossary B2B manufacturers."

**Who ranks:**
- Mohammed Shehu's "The Complete Agentic Commerce Glossary" (110+ terms) - the most comprehensive individual glossary found. Confirmed (via direct fetch) to be **general/DTC-retail flavored with a B2B-and-procurement category bolted on** (approved supplier list, purchase order, contracted pricing, punchout catalog, approval workflow, three-way match, invoice matching). It explicitly does **not** cover EDI, RFQ, or PIM, and treats B2B as one segment within a broader retail framework, not the primary audience.
- Fireblocks glossary, 5W PR glossary, Paz.ai glossary, joinhexagon.com glossary (30+ terms), paulaccornero.com glossary - all general commerce/marketing-agency glossaries, consumer/retail framing (checkout, shopping assistants like Amazon Rufus, Perplexity, ChatGPT Shopping).
- Deloitte, OroCommerce, BigCommerce, Mirakl, Intershop all publish B2B-flavored "agentic commerce" thought-leadership articles, but these are strategy narratives (readiness frameworks, guides), not glossary/reference-format content, and none is manufacturer/complex-catalog specific in the way ChatSKU's audience needs (contract pricing exposure, punchout coexistence, technical-spec hallucination risk).

**Confirmed gap:** my hypothesis holds. Every dedicated glossary found is DTC/retail-flavored by default, with B2B treated as an afterthought category rather than the organizing frame. None of them corrects the Instant Checkout hype against the actual March 2026 pullback, and none names the unresolved gap around exposing B2B contract-specific pricing to an external agent. ChatSKU can own a glossary that (1) is organized around a manufacturer's actual stack (GS1/ETIM/PIM/punchout/EDI alongside the new protocols, not instead of them), and (2) is honest about what's still vaporware versus shipped.

---

## 4. Internal-link candidates (all confirmed live via direct fetch of chatsku.com/blog, page 2, and page 3)

Strong contextual fits for a glossary post:

- `/b2b-conversational-commerce/` - defines conversational commerce; the glossary's "conversational vs. agentic" entry should link here for the deeper dive.
- `/what-is-a-b2b-catalog-chatbot/` - category-definition companion; natural link from the "AI agent" or "conversational commerce" entries.
- `/what-is-the-response-gap/` - relevant if the glossary touches response-time stakes.
- `/b2b-commerce-evolution/` - the 11-stages post; link from the "agentic commerce" / "autonomous purchasing" entries as "see the full maturity model," since the glossary should NOT re-explain the stages itself (see uniqueness section above).
- `/ai-ready-b2b-catalog-autonomous-buying/` - link from "machine-readable catalog" entry as the deeper persuasive case for catalog readiness, since the glossary itself should stay reference-format and not re-argue that case.
- `/rfq-automation-for-product-catalogs/` (or `/rfq-automation-manufacturers/` per inventory - confirmed live as `rfq-automation-manufacturers` slug on page 3) - natural link from an "RFQ automation" glossary entry.
- `/product-information-management-software/` - direct link from the PIM entry, since ChatSKU already has a full post distinguishing PIM from ChatSKU; the glossary should point there rather than re-litigate it.
- `/24-7-b2b-ai-buying-assistant/` - candidate link from "autonomous purchasing" or "AI agent" entries if the angle fits at draft time.

Pages (per MUST-FOLLOW-RULES.md list): `/features/`, `/demo/`, `/signup/`, `/for-b2b-manufacturers-distributors-and-wholesalers/` are all reasonable candidates; pick contextually at brief/draft stage.

---

## 5. Format note for analyzer

Per MUST-FOLLOW-RULES.md section 11, format should rotate. Most recent post (2044, `one-line-of-code`) used Format A. Prior to that, the last ~10 posts skewed heavily B/C. A glossary/reference piece does not fit neatly into any single format label as defined (A explanatory, B conversational Q&A, C listicle-with-opinions, D decision-tree, E contrarian, F case study). Recommend the analyzer treat this as a **Format B variant** (each term or term-cluster as an H2/H3, answered directly) since that's the closest existing pattern to a definitional reference, while flagging to the analyzer that Format B has been used often and a genuinely distinct structure (e.g., grouped tables plus short prose entries, avoiding a repetitive "Q: What is X? A:..." rhythm) would keep it structurally fresh.

---

## Summary of what I could not verify (and why it matters)

- Could not directly access the Gartner press release behind the "$15T / 90% by 2028" figure (403 on gartner.com) - only secondary reporting confirms it, tied to a named analyst's conference remarks rather than a citable published report. Matters because this is the single most attention-grabbing number in the space and it needs to be handled as a forecast, explicitly attributed, not stated as fact.
- Could not confirm the exact April 17, 2026 "latest ACP spec version" date on a primary source - only found via a third-party protocol tracker. Matters because spec version dates should not be stated with false precision if unconfirmed.
- Could not find any confirmed case of a B2B manufacturer or industrial distributor (as opposed to DTC/consumer brands) live on ACP, AP2, Visa Intelligent Commerce, or Mastercard Agent Pay. This is itself a useful, honest point for the glossary to make: as of August 2026, none of these protocols has a publicly confirmed B2B-manufacturing implementation yet. The audience should know they are early, not behind.
