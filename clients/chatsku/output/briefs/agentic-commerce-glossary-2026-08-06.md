---
title: Brief — Agentic commerce glossary for B2B manufacturers
client: chatsku
date: 2026-08-06
topic: Agentic commerce terminology for B2B manufacturers, distributors, and wholesalers
slug: agentic-commerce-glossary
stage: brief
research: clients/chatsku/output/research/agentic-commerce-glossary-2026-08-06.md
---

# Brief: Agentic commerce glossary: what manufacturers actually need to know

## Locked title (do not change)

**H1 (sentence case, verbatim):** Agentic commerce glossary: what manufacturers actually need to know

## Format decision (MUST-FOLLOW-RULES section 11)

**Chosen format: Format A (Standard explanatory / technical reference), with AEO question-phrased H2s and glossary-style H3 term entries layered on top.**

**Why this overrides the steered "Format B hybrid":** I audited the last 10 published/drafted ChatSKU posts by date (2044, 1880, 1820, 1684, 1538, 1455, 1300, 1056, 685, 397). Format counts: **Format B = 5 of 10** (397, 685, 1056, 1300, 1455), **Format C = 3 of 10** (1684, 1820, 1880), Format E = 1 (1538), Format A = 1 (2044). Both B and C hit the "used in 3 or more of the last 10 posts" disqualification threshold. Format B — the exact format proposed in the task steer — is disqualified by the client's own rotation rule, not by my judgment call. That rule overrides the steer.

Of the remaining eligible formats (A, D, E, F), **A fits the topic best**: the task's required section order — Executive summary, Introduction, grouped body sections, People also ask, Conclusion, FAQ — is Format A's defined structure verbatim ("Executive Summary, Introduction, body sections, PAA, Conclusion, FAQ... technical explanations"). Format D (decision-tree) doesn't fit a reference glossary — there's no sequence of decisions to walk through. Format F (case study) doesn't fit — there's no single before/after scenario; this is lookup content. Format A was used exactly once in the last 10 posts (2044, "one line of code"), so it's compliant with the rotation rule.

The "Format B hybrid" feel the steer wanted — question-style headers with direct answers underneath — is preserved through the **cross-cutting AEO question-heading rule** (body H2s phrased as questions, H3 term entries answered directly), which several prior posts already layer on top of non-B formats (post 299 did this inside Format F; post 397 inside Format B). Applying it inside Format A gets the lookup usability without re-triggering the overuse penalty.

**Formats skipped and why:** B (disqualified, 5/10), C (disqualified, 3/10). E and F were eligible but structurally worse fits than A for a grouped reference glossary.

## Thesis

Manufacturers are being sold a version of "agentic commerce" that is mostly still on the roadmap. This glossary names the protocols, standards, and jargon precisely, states honestly which ones are shipped versus merely announced, and points out the one thing every vendor pitch skips: no protocol here has a confirmed B2B manufacturing implementation yet, so the real work right now is getting your existing catalog and pricing data in shape, not chasing a checkout feature that OpenAI itself scaled back in March 2026.

## Why this, why now, why us

- **Why this angle:** Every competing glossary found in the research (Mohammed Shehu's 110-term list, Fireblocks, joinhexagon.com, and the B2B thought-leadership pieces from Deloitte/OroCommerce/BigCommerce/Mirakl/Intershop) is either DTC/retail-flavored with B2B bolted on, or a strategy narrative with no reference format. None corrects the Instant Checkout hype against its actual March 2026 pullback. None names the unresolved gap around exposing B2B contract pricing to an outside agent. ChatSKU can own the manufacturer-first, honestly-labeled version.
- **Why now:** The two facts that make this timely — OpenAI ending in-chat Instant Checkout on March 24, 2026, and Forrester's ~30-live-merchant count from February 2026 — are five months old as of this brief and still absent from most 2026 SEO content describing ACP in launch-day terms.
- **Why this client:** ChatSKU already owns the data-layer half of this story (catalog ingestion, customer-group pricing, quote workflows) through prior posts (1538 on PIM, 685/1056/1455 on platform integrations, 1300 on the response gap). This glossary is the natural connective piece that names the new AI-agent protocol layer without abandoning that established ground.

## Audience

Sales and eCommerce leaders at manufacturers, distributors, and wholesalers ($1M–$50M revenue, 10–200 employees). They know ERP, RFQ, PIM, and CSV/EDI exports. They do not know ACP, AP2, MCP, or A2A, and they are hearing vendor pitches and LinkedIn posts using these terms as if they're already live in B2B. They're reading to figure out: is this real, does it affect me yet, and what should I actually do this quarter versus ignore for now.

## Format and length

- Format: Format A (standard explanatory / technical reference) with AEO question-phrased H2s and glossary H3 sub-entries
- Target length: 1,800–2,200 words (task-specified; overrides the house default 1,200–2,000/2,000–3,000 bands for this piece)
- Reading time: approximately 8–9 minutes

## Uniqueness verification (MUST-FOLLOW-RULES section 1)

- **Topic:** No existing ChatSKU post is a glossary/reference format. Confirmed via `published-posts-inventory.md` plus the research file's direct fetch of `/blog/` pages 1–3.
- **Slug:** `agentic-commerce-glossary` does not collide with any indexed or live slug.
- **Angle vs. post 1820** (`b2b-commerce-evolution`, the 11-stage maturity model, Format C): distinct. 1820 is a strategy/self-assessment narrative that defines "agentic commerce" and "autonomous purchasing" in one plain-language sentence each and never names a single protocol (ACP, AP2, MCP, A2A, Visa, Mastercard). This glossary is the reference piece that names them. **The creator must NOT:** re-present the 11-stage model or its stage numbers/names, re-run the "where does your company stand" self-assessment framing, or reuse the unverified 72% self-service stat.
- **Angle vs. the untracked live post `ai-ready-b2b-catalog-autonomous-buying`:** distinct. That post's spine is "your catalog must be machine-readable before autonomous agents take over" — a persuasive/urgency piece, not a definitional one. **The creator must NOT:** rebuild that persuasive spine as this article's argument, or use its unsourced "$15 trillion / 90% by 2028" or "70% of business to fastest responder" figures without independent sourcing (both are flagged unverified in research — do not use either, see Accuracy guardrails below). The one acceptable move is linking OUT to that post from the machine-readable-catalog term entry, framed as "read the deeper case," not restating its argument.
- **8-word overlap note for the publisher's dedup pass:** because this piece touches PIM (overlaps 1538), the response gap (overlaps 1300), conversational commerce (overlaps 380), and the maturity model (overlaps 1820), run the standard 8-gram dedup audit before publish. Pay particular attention to any restated definition sentences that might echo 1538's PIM framing or 1820's "software agents that negotiate, procure, and reorder" phrasing — write fresh sentences, don't paraphrase-lift.

## SEO metadata block (top of draft, required)

- **SEO title (57 chars):** Agentic Commerce Glossary for B2B Manufacturers | ChatSKU
- **Meta description (159 chars):** A plain-English glossary of agentic commerce terms for B2B manufacturers: which protocols are shipped, which are still just announced, and what to track first.
- **URL slug:** `agentic-commerce-glossary`
- **Primary keyword:** agentic commerce glossary
- **Secondary keywords:** agentic commerce protocols, what is agentic commerce, ACP AP2 MCP A2A, AI agent B2B manufacturers, agentic commerce for manufacturers
- **Search intent:** informational / definitional (reference lookup, not commercial comparison)
- **Content type:** glossary / reference guide, pillar-adjacent length

## Structure

### Opening hook (Introduction, 100–150 words)

Do NOT open with a definition. Open on a scenario: a manufacturer's sales manager gets asked in a customer call, an internal meeting, or a vendor pitch whether the company is "ready for agentic commerce," and realizes half the terms in the question are unfamiliar and the other half are being used loosely. State the problem (vendor hype has outrun what's actually shipped), why it matters (budget and roadmap decisions are getting made off imprecise terms), and what the reader will get (an honest, manufacturer-framed glossary, not a retail one, with shipped-vs-announced labels on every term).

### H2: Executive summary

First paragraph (50–80 words, standalone, liftable as a featured snippet): must directly answer "what is agentic commerce and what do manufacturers need to know" — state that agentic commerce means AI software completing part or all of a purchase without a human clicking through every step, that the protocols behind it (ACP, AP2, MCP, A2A) are real but B2C-flavored and unproven in B2B, and that no confirmed B2B manufacturing implementation exists yet as of this writing.

Then 1–2 more paragraphs: name the differentiator up front (OpenAI ended in-chat Instant Checkout March 24, 2026, after peaking around 30 live Shopify merchants per Forrester in February 2026) and state the article's organizing logic (core concepts, protocols, payment/trust layer, the data layer you likely already have, and what to actually worry about).

### H2: Table of contents

Required (article exceeds 2,000 words at render). Simple anchor `<ul>`, no custom CSS, linking to each H2 below by id.

### H2-1: What does agentic commerce actually mean for a manufacturer? (core concepts — 4 terms)

Direct-answer opening sentence, then H3 entries. Each H3 = plain-English definition, then why it matters to a manufacturer, then a status label.

- **H3: Agentic commerce** — Status: industry term, no single owning standards body. Umbrella term for everything below.
- **H3: AI agent** — Status: general AI/ML term, not commerce-specific. Distinguishes a system that answers questions from one that executes multi-step tasks (RFQ, order).
- **H3: Autonomous purchasing** — Status: descriptive term, not a formal spec name. The end state people fear most; still narrow in practice (tie to the Instant Checkout correction coming in H2-2).
  - Internal link: `/b2b-commerce-evolution/` — anchor "11 stages of B2B commerce" — framed as "see the full maturity model" for readers who want the strategic narrative; do not re-explain the stages here.
- **H3: Conversational commerce vs. agentic commerce** — Status: standard industry distinction (presence vs. absence of a human approval step at the moment of transaction). Most manufacturers today live in conversational commerce (RFQ chat, quote-building), not agentic commerce.
  - Internal link: `/b2b-conversational-commerce/` — anchor "B2B conversational commerce"

Also place one internal link here from the "AI agent" entry: `/what-is-a-b2b-catalog-chatbot/` — anchor "B2B catalog chatbot" — for readers who want the fuller category explainer.

Target: 260–300 words for this section.

### H2-2: Which agentic commerce protocols are real, and which are still just announcements? (protocols — 4 terms)

Direct-answer opening sentence naming the shipped-vs-announced split up front. This is the differentiator section — give it the most word budget and the most specific sourcing.

- **H3: Agentic Commerce Protocol (ACP)** — Status: **real, shipped, currently maintained**, but scope shifted from checkout toward product discovery/feed structure as of March 2026. Must include, inline and attributed: launched September 29, 2025 by OpenAI and Stripe with Etsy as first partner; expanded February 16, 2026 to Shopify merchants; **by February 2026 only roughly 30 Shopify merchants were actually live** (Forrester analyst Emily Pfeiffer, cited February 2026); **OpenAI ended in-chat checkout March 24, 2026** because in-chat conversion ran roughly one-third the rate of sending shoppers to the merchant's own site. No confirmed B2B implementation found. Do not state the unconfirmed April 17, 2026 "latest spec version" date — drop it, it isn't primary-sourced.
  - External link: Forrester blog on the pullback — `target="_blank" rel="noopener noreferrer"`
- **H3: AP2 (Agent Payments Protocol)** — Status: **real, announced September 16–17, 2025** by Google, with 60+ launch partners (PayPal, Mastercard, American Express, Coinbase, Salesforce, ServiceNow named), since donated to the FIDO Alliance. Explain the three chained Mandates (Intent, Cart, Payment) in one sentence each, plain-English.
  - External link: Google Cloud Blog AP2 announcement — `target="_blank" rel="noopener noreferrer"`
- **H3: MCP (Model Context Protocol)** — Status: **real, shipped, widely adopted** as general AI infrastructure (Anthropic, November 2024). Not a payment or checkout protocol — it's the connective layer that could let an agent read a manufacturer's catalog data, if that manufacturer exposes an MCP-compatible interface. Most don't yet.
- **H3: A2A (Agent2Agent Protocol)** — Status: **real, released April 2025** by Google, now governed by the Linux Foundation with 50+ contributing partners. The protocol most relevant to a future where a buyer's procurement agent talks directly to a seller's sales agent. Not yet common in B2B manufacturing.

Target: 380–420 words for this section (heaviest section by design).

### H2-3: How does an AI agent actually get authorized to pay you, and does it apply to B2B? (payment and trust layer — 4 terms)

Direct-answer opening sentence: the card networks built agent-authorization frameworks, but most B2B manufacturer transactions don't run on card rails, so treat these as adjacent infrastructure to watch, not tools to adopt now.

- **H3: Mandates and delegated authority** — Status: descriptive concept, operationalized differently per protocol (A2A: Agent Cards + OAuth 2.0; AP2: signed Mandates; ACP: Shared Payment Tokens). "Does the agent actually have permission to buy this" is the open trust question every protocol solves differently — no single universal answer yet.
- **H3: Visa Intelligent Commerce and the Trusted Agent Protocol** — Status: **real, announced April 30, 2025** (Intelligent Commerce), Trusted Agent Protocol following October 14, 2025, Intelligent Commerce Connect piloting from April 8, 2026. Card-rail infrastructure; honestly flag limited direct relevance since most B2B manufacturer sales run on invoicing, ACH, or net terms, not card rails.
- **H3: Mastercard Agent Pay and Agent Pay for Machines (AP4M)** — Status: **real, announced April 29, 2025** (Agent Pay, with Microsoft, IBM, Braintree as launch partners); **AP4M announced June 10, 2026** with 30+ organizations. Same card-rail caveat as Visa.
- **H3: Human-in-the-loop** — Status: general AI/ML term, not commerce-specific, but the practical reality for B2B today. Most real B2B agentic-flavored tools, including ChatSKU's own quote-building, keep a human in the loop by design; fully autonomous no-approval purchasing remains the less common case.
  - Internal link: `/rfq-automation-manufacturers/` — anchor "RFQ automation guide" — placed here since it's the concrete example of a human-in-the-loop quote workflow manufacturers already run.

Target: 250–290 words for this section.

### H2-4: What data standards do you already have that agentic commerce actually needs? (data layer — 5 terms)

Direct-answer opening sentence: most of the real prerequisite work isn't a new AI protocol, it's data manufacturers already partially have.

- **H3: GS1 and GTIN** — Status: real, long-established standard. If SKUs already have GTINs, that's a head start on the unique-identifier requirement agentic product-discovery feeds are built around.
- **H3: UNSPSC** — Status: real, established classification standard used heavily in procurement/spend-analysis systems. Many enterprise procurement systems that would run an autonomous purchasing agent already require it.
- **H3: ETIM** — Status: real, established sector-specific standard for electrical/technical/MRO products, widely used in Europe. Manufacturers already using it have exactly the filterable attribute data an AI shopping agent needs to compare specs.
- **H3: PIM (Product Information Management)** — Status: real software category, not a single spec. Do not re-explain PIM in depth; a PIM organizes data, it does not answer a buyer's question or complete a transaction (established ChatSKU distinction from post 1538).
  - Internal link: `/product-information-management-software/` — anchor "PIM software guide"
- **H3: Punchout, cXML, and OCI** — Status: real, long-established B2B procurement standards (punchout is the general process; cXML and SAP's OCI are the two data formats that carry the connection), predating the current AI wave by two decades. One sentence noting EDI (ANSI X12/EDIFACT) as the older, distinct document-exchange layer these are not replacing. Distinguish clearly from agentic commerce: punchout is buyer-system-initiated and rules-based; agentic commerce is AI-agent-initiated and can act with more autonomy. They coexist.

Also add a short closing note in this section (not a separate H3) on machine-readable catalogs and structured product data: descriptive term, not one formal spec, operationalized through GS1/GTIN, schema.org Product markup, ACP's feed format, and platform-specific feeds. This is the actual prerequisite behind most of the hype.
  - Internal link: `/ai-ready-b2b-catalog-autonomous-buying/` — anchor "is your catalog ready" — framed as "read the deeper case for catalog readiness," not restating its argument.

Target: 320–360 words for this section.

### H2-5: What should actually worry you about agentic commerce right now? (risk layer — 3 terms)

Direct-answer opening sentence: the real near-term risk isn't autonomous checkout, it's an agent misstating a spec or price to a buyer with no protocol responsible for catching it. Briefly caution, in the section intro (not as a full H3), that vendors will pitch jargon like "Agentic Commerce Optimization (ACO)" (not a standard, marketing terminology) and "AEO/GEO" (Answer/Generative Engine Optimization — industry jargon, no owning standards body, but a real practice describing whether AI assistants can extract and correctly cite your specs and pricing).

- **H3: Hallucinated specs and price integrity** — Status: descriptive risk term, not a formal spec. AP2's Cart Mandate addresses "what you see is what you pay for" at the payment layer, but nothing in ACP or AP2 guarantees an agent won't misstate a technical spec (tolerance, voltage rating, material grade) when summarizing a product. This is the single biggest practical risk for a manufacturer with technically complex SKUs.
- **H3: The B2B contract-pricing gap** — Status: descriptive term, not a formal spec. None of the current protocols define a standard way to expose customer-group or tiered contract pricing to an outside agent — this is a real, unsolved gap, not something already quietly solved. Say so plainly.
- **H3: No confirmed B2B implementation** — Status: honest research finding, not a term with a formal name, but worth stating as its own point: as of this writing, no protocol above (ACP, AP2, Visa Intelligent Commerce, Mastercard Agent Pay) has a publicly confirmed B2B manufacturing or industrial-distribution implementation. That means the audience is early, not behind.

Target: 220–260 words for this section.

### H2: People also ask (3–4 Q&As, H3 questions)

1. **What happened to OpenAI's Instant Checkout?** — Answer using the verified timeline: launched Sept 29 2025, expanded to Shopify Feb 16 2026, only ~30 merchants live by Feb 2026 (Forrester), discontinued March 24 2026 due to roughly one-third the conversion rate of the merchant's own site.
2. **Is MCP the same thing as an AI agent?** — No; MCP is the connective protocol that lets an agent reach outside data (like a catalog), not the agent itself.
3. **Does agentic commerce work with B2B contract pricing yet?** — No confirmed standard way exists yet to expose tiered/customer-group pricing to an outside agent; name it as an open gap.
   - Internal link: `/what-is-the-response-gap/` — anchor "the response gap" — natural tie-in if the answer touches how buyers currently wait on pricing confirmation.
4. **What should I ask my ERP or payments vendor about agent protocols?** — Whether they can produce an AP2-style signed audit trail and whether their product data is structured enough (GTIN/UNSPSC/ETIM) to be machine-readable at all.

Target: 180–220 words total.

### H2: Conclusion

Summary + one practical recommendation. No new ideas, no inline links (button widget handles the CTA at publish time). Recommendation should be concrete and near-term: get catalog and pricing data structured (GTIN/UNSPSC/ETIM, clean SKUs, real-time price/availability) now, because that work pays off regardless of which protocol wins, while treating checkout-level AI agent protocols as something to monitor, not implement, until a confirmed B2B implementation exists.

Target: 120–150 words.

### H2: Frequently asked questions (exactly 6 Q&As, H3 questions, 40–80 words each)

1. **What is agentic commerce in simple terms?**
2. **Is agentic commerce already live for B2B manufacturers?** (Answer: no confirmed implementation as of this writing — state plainly.)
3. **What's the difference between conversational commerce and agentic commerce?**
4. **Do I need to expose my catalog through ACP or AP2 right now?** (Answer: no — these are B2C-flavored and unproven in B2B; prioritize data structure instead.)
5. **What data should I clean up before agentic commerce matters to my business?** (GTIN, UNSPSC, ETIM, accurate real-time pricing/availability.)
6. **Will an AI agent replace my sales team?** (No — tie to human-in-the-loop; most real B2B agentic-flavored tools, including quote-building, keep a human in the loop by design.)

## Must include

- Inline attribution, with source and date, for: OpenAI ending in-chat Instant Checkout March 24, 2026, and the ~30 live Shopify merchants figure (Forrester analyst Emily Pfeiffer, February 2026).
- Inline attribution for AP2's 60+ launch partners (Google Cloud Blog, September 16–17, 2025).
- An explicit, plainly stated line that no protocol covered has a confirmed B2B manufacturing implementation as of this writing.
- Status labels exactly as researched for every term (see per-section notes above) — no upgrading "announced" to "shipped."
- The card-rail limitation caveat on both Visa and Mastercard entries (most B2B manufacturer transactions run on invoicing/ACH/net terms, not cards).
- The unsolved B2B contract-pricing exposure gap, stated as a genuine open problem, not something already solved.

## Must NOT include

- The 67% Gartner rep-free stat (already used in 5+ live ChatSKU posts: 380, 685, 1056, 1300, 1538, 1880).
- The "$15 trillion / 90% by 2028" figure, in any framing — it shares its unsourced origin with the rejected 70%-of-business figure from the untracked post, and per the stat-verification rule, one flagged-unverified stat makes the other equally suspect.
- "94% of B2B buyers used generative AI during their most recent purchase" — confirmed conflation of a different Forrester stat (94% of buyers in groups of six-plus report benefits). Do not use under any framing.
- "50 million shopping queries daily" (ChatGPT) — uncorroborated, secondary-only.
- "71% of buyers use AI search tools for vendor research" (G2) — uncorroborated, secondary-only.
- The 72% self-service stat from post 1820 — flagged there as unsourced; do not import it here.
- The unconfirmed April 17, 2026 "latest ACP spec version" date — drop entirely, no primary confirmation.
- Any invented spec version number, launch date, or B2B case study/customer name for any protocol. There are none confirmed. Say so instead of implying otherwise.
- The 11-stage maturity model, its stage numbers/names, or the "where does your company stand" self-assessment framing from post 1820.
- The "your catalog must be machine-readable before autonomous agents take over" persuasive spine from the untracked `ai-ready-b2b-catalog-autonomous-buying` post — link to it, don't rebuild its argument.
- "AI-powered" as filler, "just a chatbot," em dashes, hype words (revolutionary, cutting-edge, game-changing), filler words (delve, leverage, navigate, landscape, ecosystem).

## Headline direction

Locked — see top of this brief. No alternates needed; do not vary at draft stage without flagging to the user.

## Open questions for the creator

- Exact phrasing of each H2 question (spine above is directive on topic and order; word-level phrasing is the creator's call within voice guidelines).
- Whether to render the term list as a running glossary table (term | definition | status) in addition to prose H3s, given the reference nature of the content — optional, not required; if added, keep it light (no custom CSS beyond standard house table styling) and don't let it replace the prose entries.
- Exact PAA/FAQ question wording (topics above are directive).
- Whether both external links (Forrester, Google Cloud Blog) land in H2-2 as specified, or one moves to the PAA "What happened to OpenAI's Instant Checkout?" answer instead — either placement is fine as long as the 2-external-link cap holds and both stay attributed with date.

## Internal link map (8 links total, within the 3–5 minimum / 9–10 pillar ceiling)

| # | Section | Anchor text | Destination |
|---|---------|-------------|-------------|
| 1 | Introduction | "B2B manufacturers and distributors" | `/for-b2b-manufacturers-distributors-and-wholesalers/` |
| 2 | H2-1, "AI agent" entry | "B2B catalog chatbot" | `/what-is-a-b2b-catalog-chatbot/` |
| 3 | H2-1, "Conversational commerce vs. agentic commerce" entry | "B2B conversational commerce" | `/b2b-conversational-commerce/` |
| 4 | H2-1, "Autonomous purchasing" entry | "11 stages of B2B commerce" | `/b2b-commerce-evolution/` |
| 5 | H2-3, "Human-in-the-loop" entry | "RFQ automation guide" | `/rfq-automation-manufacturers/` |
| 6 | H2-4, "PIM" entry | "PIM software guide" | `/product-information-management-software/` |
| 7 | H2-4, machine-readable catalog note | "is your catalog ready" | `/ai-ready-b2b-catalog-autonomous-buying/` |
| 8 | PAA, Q3 answer | "the response gap" | `/what-is-the-response-gap/` |

No internal links in the Conclusion body (button widget carries the CTA to `/demo/`).

## External link map (2 max, both first-use for ChatSKU)

| # | Section | Destination | Notes |
|---|---------|-------------|-------|
| 1 | H2-2, ACP entry | Forrester blog, "What it means that the leader in agentic commerce just pulled back" | `target="_blank" rel="noopener noreferrer"`; source of the ~30-merchant figure |
| 2 | H2-2, AP2 entry | Google Cloud Blog, AP2 announcement | `target="_blank" rel="noopener noreferrer"`; source of the 60+ partner figure |

## Exact term list (20 H3 terms across 5 body H2 sections — do not improvise additions or removals)

1. Agentic commerce
2. AI agent
3. Autonomous purchasing
4. Conversational commerce vs. agentic commerce
5. Agentic Commerce Protocol (ACP)
6. AP2 (Agent Payments Protocol)
7. MCP (Model Context Protocol)
8. A2A (Agent2Agent Protocol)
9. Mandates and delegated authority
10. Visa Intelligent Commerce and the Trusted Agent Protocol
11. Mastercard Agent Pay and Agent Pay for Machines (AP4M)
12. Human-in-the-loop
13. GS1 and GTIN
14. UNSPSC
15. ETIM
16. PIM (Product Information Management)
17. Punchout, cXML, and OCI (with EDI mentioned in one sentence, not a standalone entry)
18. Machine-readable catalog and structured product data (short closing note in H2-4, not a full H3, to protect word budget)
19. Hallucinated specs and price integrity
20. The B2B contract-pricing gap

ACO and AEO/GEO are covered as a one-paragraph vendor-jargon caution inside the H2-5 intro, not as standalone H3 entries — this keeps the count disciplined per the research file's "18 well-explained terms, not 35 one-liners" guidance while still surfacing the caution.
