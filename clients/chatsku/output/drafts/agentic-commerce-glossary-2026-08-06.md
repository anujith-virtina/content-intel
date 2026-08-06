---
title: "Agentic commerce glossary: what manufacturers actually need to know"
client: chatsku
date: 2026-08-06
slug: agentic-commerce-glossary
stage: draft
brief: clients/chatsku/output/briefs/agentic-commerce-glossary-2026-08-06.md
word_count: 2825
headlines:
  - "Agentic commerce glossary: what manufacturers actually need to know"
---

```
SEO title: Agentic Commerce Glossary for B2B Manufacturers | ChatSKU  (57 chars)
Meta description: A plain-English glossary of agentic commerce terms for B2B manufacturers: which protocols are shipped, which are still just announced, and what to track first.  (159 chars)
URL slug: agentic-commerce-glossary
Primary keyword: agentic commerce glossary
Secondary keywords: agentic commerce protocols, what is agentic commerce, ACP AP2 MCP A2A, AI agent B2B manufacturers, agentic commerce for manufacturers
Search intent: informational / definitional (reference lookup, not commercial comparison)
Content type: glossary / reference guide, pillar-adjacent length
```

# Agentic commerce glossary: what manufacturers actually need to know

## Executive summary

Agentic commerce means AI software completes part or all of a purchase without a human clicking through every step, from finding a product to submitting payment. The protocols behind it, ACP, AP2, MCP, and A2A, are real, but they were built for consumer shopping first. None of them has a confirmed B2B manufacturing implementation as of this writing. For manufacturers, the technology is early, not something you're already behind on.

Here's the piece most 2026 content still gets wrong. OpenAI shut down in-chat Instant Checkout on March 24, 2026, after the feature topped out around 30 live Shopify merchants, according to Forrester analyst Emily Pfeiffer's February 2026 count. That's a rounding error against the "over a million merchants" figure promoted at the September 2025 launch.

This glossary is organized the way a manufacturer actually needs it: core concepts first, then the protocols and who built them, then the payment and trust layer, then the data standards you probably already have, and finally what should genuinely worry you. Every term gets a plain-English definition and an honest status label. No upgrading "announced" to "shipped."

## Table of contents

<ul>
<li><a href="#introduction">Introduction</a></li>
<li><a href="#what-does-agentic-commerce-actually-mean-for-a-manufacturer">What does agentic commerce actually mean for a manufacturer?</a></li>
<li><a href="#which-agentic-commerce-protocols-are-real-and-which-are-still-just-announcements">Which agentic commerce protocols are real, and which are still just announcements?</a></li>
<li><a href="#how-does-an-ai-agent-actually-get-authorized-to-pay-you-and-does-it-apply-to-b2b">How does an AI agent actually get authorized to pay you, and does it apply to B2B?</a></li>
<li><a href="#what-data-standards-do-you-already-have-that-agentic-commerce-actually-needs">What data standards do you already have that agentic commerce actually needs?</a></li>
<li><a href="#what-should-actually-worry-you-about-agentic-commerce-right-now">What should actually worry you about agentic commerce right now?</a></li>
<li><a href="#people-also-ask">People also ask</a></li>
<li><a href="#conclusion">Conclusion</a></li>
<li><a href="#frequently-asked-questions">Frequently asked questions</a></li>
</ul>

## Introduction

A vendor emails your sales director: "Is your catalog ready for agentic commerce?" Nobody in the room knows what half the question means. ACP, AP2, MCP, and A2A get dropped into the same sentence as budget forecasts and roadmap decisions, and most of your team can't tell which ones already ship product and which are still a press release.

That gap costs money. Vendor hype has outrun what's actually live, and budget calls are getting made off imprecise terms. This glossary is written for <a href="/for-b2b-manufacturers-distributors-and-wholesalers/">B2B manufacturers and distributors</a>, not the retail crowd every other glossary was written for. Every term below gets a plain-English definition, a status label, and an honest note on whether it touches your business yet.

## What does agentic commerce actually mean for a manufacturer?

Agentic commerce is the umbrella term for AI software buying and selling on someone's behalf, and the four terms below are where most confusion starts.

### Agentic commerce

Buying and selling where an AI agent researches, decides, and completes some or all of a purchase on a person's or company's behalf, without a human approving every step. This is the umbrella term for everything else in this glossary. If a buyer's procurement software can query your catalog and place an order without a person reading your website, you're inside this category whether you planned for it or not. Status: industry term, with no single owning standards body.

### AI agent

Software that takes multi-step action toward a goal, searching, comparing, filling a cart, submitting a payment, instead of just answering one question. This is the distinction between a system that answers a question and one that can actually execute an RFQ or place an order. For the fuller category explainer, see what a <a href="/what-is-a-b2b-catalog-chatbot/">B2B catalog chatbot</a> actually does. Status: general AI/ML term, not commerce-specific.

### Autonomous purchasing

A purchase completed by software with no human approval at the moment of payment, usually inside pre-set rules like a budget cap or an approved vendor list. This is the end state manufacturers hear about most and fear most. It's still narrow in practice, as the Instant Checkout numbers below show. For the strategic version of where this fits into your roadmap, see the <a href="/b2b-commerce-evolution/">11 stages of B2B commerce</a>. Status: descriptive term, not a formal spec name.

### Conversational commerce vs. agentic commerce

Conversational commerce is a chat interface where the buyer works through questions and pricing, but a person still confirms the sale. Agentic commerce is software completing the transaction itself, with a person setting rules in advance instead of approving each step. Most manufacturers today live in <a href="/b2b-conversational-commerce/">B2B conversational commerce</a>, RFQ chat, quote-building, not agentic commerce. Conflating the two overstates where the market actually is. Status: standard industry distinction.

## Which agentic commerce protocols are real, and which are still just announcements?

Two of these are shipped and maintained, one is AI plumbing already in wide use, and one is real but hasn't touched B2B manufacturing yet.

### Agentic Commerce Protocol (ACP)

An open interaction standard, co-built by OpenAI and Stripe, that lets a buyer's AI agent discover products, build a cart, and complete payment with a merchant, using a "Shared Payment Token" so the agent never sees raw card data. It launched September 29, 2025 with Etsy as first partner, expanded February 16, 2026 to Shopify merchants. By February 2026, only around 30 Shopify merchants were actually live on it, according to <a href="https://www.forrester.com/blogs/what-it-means-that-the-leader-in-agentic-commerce-just-pulled-back/" target="_blank" rel="noopener noreferrer">Forrester analyst Emily Pfeiffer</a>. OpenAI ended in-chat checkout entirely on March 24, 2026, after it converted at roughly a third the rate of sending shoppers to the merchant's own site. No confirmed B2B implementation exists. Status: real, shipped, currently maintained, but scope has shifted from checkout toward product discovery and feed structure since March 2026.

### AP2 (Agent Payments Protocol)

An open protocol from Google that gives an AI agent a cryptographically signed permission slip from a human before it can spend money, chained through three Mandates: an Intent Mandate for what you authorized and under what limits, a Cart Mandate for the exact items and price you approved, and a Payment Mandate for the credential sent to the payment network. It was <a href="https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol" target="_blank" rel="noopener noreferrer">announced by Google Cloud on September 16-17, 2025</a> with 60+ launch partners, including PayPal, Mastercard, American Express, Coinbase, Salesforce, and ServiceNow. Google has since donated AP2 to the FIDO Alliance. Status: real, announced, in active use by launch partners.

### MCP (Model Context Protocol)

An open standard, introduced by Anthropic in November 2024, that lets an AI model connect to outside data sources through one consistent interface instead of a custom build for every system. It isn't a payment or checkout protocol. It's the connective layer that could let an agent read your catalog data directly, if you expose an MCP-compatible interface. Most manufacturers don't yet. Status: real, shipped, widely adopted as general AI infrastructure.

### A2A (Agent2Agent Protocol)

An open protocol that lets AI agents built by different vendors find each other, authenticate, and hand off tasks using standard web technology. This is the protocol most relevant to a future where a buyer's procurement agent talks directly to a seller's sales agent. Status: real, released April 2025 by Google, now governed by the Linux Foundation with 50+ contributing partners. Not yet common in B2B manufacturing.

| Protocol | Built by | Status | What it does |
|---|---|---|---|
| ACP | OpenAI and Stripe | Shipped, scope narrowed since March 2026 | Product discovery and payment via a Shared Payment Token |
| AP2 | Google, now with FIDO Alliance | Announced, active with 60+ partners | Signed Mandates authorizing an agent to spend |
| MCP | Anthropic | Shipped, widely adopted | Connects an AI model to outside data like your catalog |
| A2A | Google, now with Linux Foundation | Shipped, early adoption | Lets agents from different vendors hand off tasks |

## How does an AI agent actually get authorized to pay you, and does it apply to B2B?

The card networks built agent-authorization frameworks, but most B2B manufacturer transactions don't run on card rails. Treat these as adjacent infrastructure to watch, not tools to adopt now.

### Mandates and delegated authority

"Does this agent actually have permission to buy this" is the trust question every protocol answers differently. A2A uses Agent Cards and OAuth 2.0, AP2 uses signed Mandates, ACP uses Shared Payment Tokens. Status: descriptive concept, operationalized differently per protocol, with no single universal answer yet.

### Visa Intelligent Commerce and the Trusted Agent Protocol

Visa's framework for authenticating, authorizing, and tokenizing payments an AI agent initiates on its network. Announced April 30, 2025, with the Trusted Agent Protocol following October 14, 2025, and Intelligent Commerce Connect piloting from April 8, 2026. Most B2B manufacturer transactions run on invoicing, ACH, or net terms, not cards, so direct relevance is currently limited. Status: real, announced, card-rail infrastructure.

### Mastercard Agent Pay and Agent Pay for Machines (AP4M)

Mastercard's framework for letting verified AI agents transact using "Agentic Tokens," a card credential tied to a specific agent, merchant, and consent policy. Agent Pay was announced April 29, 2025 with Microsoft, IBM, and Braintree as launch partners. AP4M followed June 10, 2026 with 30+ organizations. Same card-rail caveat as Visa applies. Status: real, announced, card-rail infrastructure.

### Human-in-the-loop

Any workflow where a person must approve an agent's action before it executes, instead of the agent acting on its own. Most real B2B agentic-flavored tools, including the workflow behind ChatSKU's own <a href="/rfq-automation-manufacturers/">RFQ automation guide</a>, keep a human in the loop by design. Fully autonomous, no-approval purchasing is still the less common case. Status: general AI/ML term, not commerce-specific, but the practical reality for B2B today.

## What data standards do you already have that agentic commerce actually needs?

Most of the real prerequisite work isn't a new AI protocol. It's data you likely already have in some form.

### GS1 and GTIN

GTIN is the globally unique product identifier GS1 issues. GS1 is the only authorized source for GTINs worldwide. If your SKUs already carry GTINs, you have a head start on the unique-identifier requirement agentic product-discovery feeds are built around. Status: real, long-established standard.

### UNSPSC

An open, global eight-digit classification code for products and services, managed by GS1 US on behalf of the UN Development Programme. Many enterprise procurement systems, the kind that would run an autonomous purchasing agent, already require UNSPSC codes for spend categorization. If your catalog lacks them, that's a blocker independent of any AI protocol. Status: real, established standard, used heavily in procurement systems.

### ETIM

An open technical classification standard for electrical, electronic, and technical products, pairing each product class with a defined set of features. Widely used across Europe. Manufacturers already using ETIM have exactly the filterable attribute data an AI shopping agent needs to compare specs. Status: real, established sector-specific standard.

### PIM (Product Information Management)

Software for centralizing, standardizing, enriching, and syndicating product data across channels. A PIM organizes your data. It doesn't answer a buyer's question or complete a transaction on its own, a distinction worth checking against <a href="/features/">what ChatSKU connects to</a>. Status: real software category, not a single spec.

### Punchout, cXML, and OCI

Punchout is the process where a buyer's procurement system connects to your catalog to shop and return a cart for a purchase order. cXML and SAP's OCI are the two data formats that carry that connection. EDI (ANSI X12 in the US, EDIFACT internationally) is the older, separate layer for exchanging documents like POs and invoices. None of the AI-agent protocols above replace it. Punchout is buyer-system-initiated and rules-based. Agentic commerce is AI-agent-initiated and can act with more autonomy. The two coexist. Status: real, long-established B2B procurement standards, predating the current AI wave by two decades.

One more term worth defining here: a machine-readable catalog, or structured product data, is a catalog an AI agent can parse reliably. It isn't one formal spec, but it's operationalized through GS1/GTIN, schema.org Product markup, ACP's feed format, and platform-specific feeds. This is the actual prerequisite behind most of the hype. For the deeper case on why it matters, read <a href="/ai-ready-b2b-catalog-autonomous-buying/">is your catalog ready</a>.

## What should actually worry you about agentic commerce right now?

The real near-term risk isn't autonomous checkout. It's an agent misstating a spec or price to your buyer, with no protocol responsible for catching it.

Expect vendors to pitch jargon along the way. "Agentic Commerce Optimization (ACO)" isn't a standard or a spec, it's marketing terminology. "AEO" and "GEO" (Answer Engine Optimization and Generative Engine Optimization) are industry jargon with no owning standards body, but they describe a real practice: whether AI assistants can extract and correctly cite your specs and pricing at all.

### Hallucinated specs and price integrity

AP2's Cart Mandate addresses "what you see is what you pay for" at the payment layer, but nothing in ACP or AP2 guarantees an agent won't misstate a technical spec, a tolerance, a voltage rating, a material grade, when summarizing your product to a buyer. This is the single biggest practical risk for a manufacturer with technically complex SKUs. Status: descriptive risk term, not a formal spec.

### The B2B contract-pricing gap

None of the current protocols define a standard way to expose your customer-group or tiered contract pricing to an outside agent. This is a real, unsolved gap, not something already quietly solved. Status: descriptive term, not a formal spec.

### No confirmed B2B implementation

As of this writing, no protocol above, ACP, AP2, Visa Intelligent Commerce, or Mastercard Agent Pay, has a publicly confirmed B2B manufacturing or industrial-distribution implementation. That means you're early, not behind. Status: honest research finding, not a named term.

## People also ask

### What happened to OpenAI's Instant Checkout?

It launched September 29, 2025 with Stripe and Etsy, expanded to Shopify merchants on February 16, 2026, but only about 30 merchants were actually live by that point, per Forrester analyst Emily Pfeiffer. OpenAI shut it down March 24, 2026, because in-chat purchases converted at roughly a third the rate of sending shoppers to the merchant's own site.

### Is MCP the same thing as an AI agent?

No. MCP is the connective protocol that lets an agent reach outside data, like your catalog. It isn't the agent itself, and it isn't a payment or checkout protocol.

### Does agentic commerce work with B2B contract pricing yet?

No confirmed standard exists for exposing tiered or customer-group pricing to an outside agent. That's an open gap, not something quietly solved. Buyers today still wait on manual pricing confirmation, the same <a href="/what-is-the-response-gap/">response gap</a> that slows down quotes.

### What should I ask my ERP or payments vendor about agent protocols?

Ask whether they can produce an AP2-style signed audit trail, and whether your product data is structured enough (GTIN, UNSPSC, ETIM) to be machine-readable at all. Most vendors can't answer both of those yet.

## Conclusion

Agentic commerce is real infrastructure, but very little of it has reached B2B manufacturing yet. ACP, AP2, MCP, and A2A are shipped or announced protocols built mostly for consumer shopping. Visa and Mastercard's frameworks mostly touch card-rail transactions your buyers probably aren't running. No protocol covered here has a confirmed manufacturing implementation as of this writing.

The practical move this quarter isn't picking a protocol. It's getting your catalog and pricing data structured: GTINs assigned, UNSPSC or ETIM codes in place, SKUs clean, pricing accurate in real time. That work pays off no matter which protocol eventually wins, and it's the same groundwork that makes any AI-assisted buying experience possible. Treat checkout-level agent protocols as something to monitor this year, not something to implement.

## Frequently asked questions

### What is agentic commerce in simple terms?

Agentic commerce is AI software buying or selling on someone's behalf, from research through payment, without a person clicking through every step. It's built on protocols like ACP, AP2, MCP, and A2A. For manufacturers, it's still early. No protocol covered here has a confirmed B2B manufacturing implementation as of this writing.

### Is agentic commerce already live for B2B manufacturers?

No. As of this writing, no protocol, ACP, AP2, Visa Intelligent Commerce, or Mastercard Agent Pay, has a publicly confirmed implementation at a B2B manufacturer or industrial distributor. The live implementations found in research are consumer and DTC brands on Shopify and Etsy. You're early to this, not behind competitors.

### What's the difference between conversational commerce and agentic commerce?

Conversational commerce is a chat interface where the buyer works through questions and pricing, but a person still confirms the sale. Agentic commerce is software completing the transaction itself, with a person setting rules in advance instead of approving each step. Most manufacturers today run on conversational commerce, not agentic commerce.

### Do I need to expose my catalog through ACP or AP2 right now?

No. Both protocols are B2C-flavored and unproven in B2B manufacturing right now. Prioritize structuring your catalog and pricing data instead: GTINs, UNSPSC or ETIM codes, accurate real-time availability. That groundwork matters regardless of which protocol eventually gains traction in B2B.

### What data should I clean up before agentic commerce matters to my business?

Start with GTINs on every SKU, UNSPSC or ETIM classification codes depending on your industry, and accurate, real-time pricing and availability. These aren't AI-specific fixes. They're the same data quality that improves your existing search, quoting, and procurement integrations today.

### Will an AI agent replace my sales team?

No. Most real B2B agentic-flavored tools, including quote-building assistants, keep a human in the loop by design rather than executing purchases with no approval step. Fully autonomous, no-human purchasing remains the less common case in practice. Agents are built to filter and prepare deals, not replace the people closing them.
