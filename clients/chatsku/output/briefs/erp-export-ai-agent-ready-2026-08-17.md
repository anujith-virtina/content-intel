---
title: Brief — Is your ERP export AI-agent-friendly? A 10-minute self-check
client: chatsku
date: 2026-08-17
topic: How IT/operations managers at B2B manufacturers/distributors can audit their ERP product-data export for AI-agent readiness
audience: IT managers and operations managers at B2B manufacturers, distributors, wholesalers who own the ERP/PIM export
slug: erp-export-ai-agent-ready
stage: brief
research: clients/chatsku/output/research/erp-export-ai-agent-ready-2026-08-17.md
---

# Brief: Is your ERP export AI-agent-friendly? A 10-minute self-check

## Thesis

Your ERP already "exports" your product data, but that export was built for a different purpose than feeding an AI agent, and ten specific, checkable file properties determine whether an AI assistant reading it will answer buyers correctly or confidently wrong.

## Why this, why now, why us

- **Why this angle:** Every existing "AI-ready data" piece (ours included, on the untracked persuasive post) stays abstract — "your data must be clean and structured" — or is schema.org/website-markup content with zero ERP vocabulary. Nobody hands the person who actually owns the export file a literal, field-by-field pass/fail test they can run against the CSV/IDoc/OData pull sitting on their desktop today. That's the open gap the research confirmed and it's explicitly listed as a topic gap in the inventory ("ERP-to-chat," "catalog data quality").
- **Why now:** Post 2129 (agentic commerce glossary, Aug 6) just built reader familiarity with GTIN/UNSPSC/ETIM/EDI as terms. This post is the natural next step: stop defining the standards, start using them as a checklist against a real file.
- **Why this client:** ChatSKU's entire pitch depends on catalog data actually being readable. This piece proves technical credibility with the audience that controls whether ChatSKU gets a clean file or a mangled one, without pretending ChatSKU performs the audit or syncs to the ERP itself.

## Format and length

- **Format: D — Decision-tree / playbook.** Chosen because the article's spine is a sequenced, run-this-yourself self-check, not a Q&A (Format B), not an opinionated numbered-reasons list (Format C), and not a contrarian thesis (Format E). It is inherently staged: know your file, clean it, enrich it, validate it — a playbook structure.
- **Rotation justification:** Format A was just used on post 2129 (agentic commerce glossary, Aug 6, the most recent post). Of the last 10 posts (2129, 2044, 1880, 1820, 1684, 1538, 1455, 1300, 1056, 685), the breakdown is Format A ×2, Format C ×3 (1684, 1820, 1880), Format B ×4 (1538... actually 1538 is E; 1455, 1300, 1056, 685 are B), Format E ×1 (1538). Format B is heavily overused across the broader archive and Format D has never been used. D is the right pick both for topic fit and for genuine structural novelty.
- Target length: 2,000–2,500 words
- Reading time: ~9–10 minutes

## Audience

IT managers and operations managers at B2B manufacturers, distributors, and wholesalers who personally own the ERP or PIM export and would run this check themselves. More technical than ChatSKU's usual sales-leader reader: they know what a CSV delimiter is, they know what their ERP is called (SAP, NetSuite, Business Central, Epicor, Infor, Acumatica), and they do not need agentic commerce evangelized to them — post 2129 already did that education, this reader may have already read it or doesn't need to. They are here because someone (a vendor, a sales leader, their own curiosity) raised the question "is our data ready for an AI assistant to read," and they want a way to test that themselves in the next ten minutes, not a strategy deck.

## Structure

### Opening hook

Concrete scenario, not a definition. Suggested direction: an IT manager gets asked by sales/leadership "can we hook an AI assistant up to our catalog," pulls up the export they already have (an CSV a consultant set up in 2019, or a MATMAS IDoc feed nobody's looked at since), and realizes they don't actually know if it's usable. Do not open with "AI agents are changing B2B commerce" or any definition of agentic commerce — that ground is already covered by post 2129 and the untracked autonomous-buying post.

### Executive Summary (structural label — keep verbatim)

2–3 paragraphs. State the thesis directly: most ERP exports were built for something other than feeding an AI agent, and there are 10 specific, checkable properties that determine whether it will work. No stat-padding — say plainly that this is a technical audit, not a vendor pitch, and that the reader can run it today against their own file.

### Introduction (structural label — keep verbatim)

Set up why "we already have an export" is not the same as "our export is AI-agent-ready." Reference, without redefining, that agentic commerce depends on real data standards (GTIN, UNSPSC/ETIM, EDI) — one sentence, link to the glossary post, move on.

### H2: What kind of export file do you actually have? (checkpoints 1–3)

Grouping logic: before you can check data quality, you have to know what format and mechanism produced the file in front of you. This stage establishes format literacy.

- **H3: Do you know your export's native format?**
  Test: name the exact format your product data leaves the ERP in — a flat CSV/Excel pull, or a structured feed (SAP IDoc/MATMAS06, Business Central OData). If SAP, know whether it's an IDoc feed or the newer flat-file "Export Master Data" app extract; if Business Central, know whether it's the current `/api/v2.0/` endpoint or a legacy OData v4 page (Microsoft is retiring the latter).
  PASS: you can name it specifically.
  FAIL: "someone set this up a while back" is the honest answer.
  Mechanical consequence: nobody currently knows which fields survived translation from the source system. An assistant built against an outdated field mapping answers with a value (price, spec) that was correct in the old format but silently dropped or renamed after a later system upgrade.

- **H3: Does a GTIN or long numeric ID survive the export intact?**
  Test: open the file, find the GTIN/UPC/EAN column, check 5 random rows for the full digit string.
  PASS: full 12–14 digit ID intact as text, leading zeros preserved.
  FAIL: displays as scientific notation (e.g. 1.23457E+12) or has lost leading zeros — the default behavior when a CSV with no type information is opened in Excel (verified NetSuite CSV export behavior).
  Mechanical consequence: an assistant matching a buyer's barcode scan or GTIN lookup against the mangled ID gets a value that matches nothing, or matches the wrong product because two different GTINs rounded to the same corrupted number.

- **H3: If your export comes from an API call, does the field selection include what buyers actually ask about?**
  Test: pull up the field/query definition behind the export (the `$select` list, or whatever fields an integrator chose) and compare it against what your sales team fields most: price, stock quantity, category, lead time.
  PASS: all of those fields are explicitly selected.
  FAIL: the integration was built for a narrower original purpose (e.g., syncing item numbers into another system) and buyer-relevant fields were never added.
  Mechanical consequence: the assistant has no price field to read, so it either refuses to answer or, if a similarly-named stray field exists, quotes the wrong number.

### H2: Does your export have duplicate or conflicting records? (checkpoints 4–5)

Grouping logic: once you know the file's format, the next thing to test is whether the records in it are even internally trustworthy — before worrying about richness or freshness.

- **H3: Are there duplicate SKUs in the file?**
  Test: sort or pivot on the SKU/item-number column, look for repeats.
  PASS: every SKU appears exactly once.
  FAIL: the same SKU appears more than once, often because a legacy feed and a newer manually maintained list both got merged into one export without deduplication.
  Mechanical consequence: an assistant asked about that SKU has two conflicting records to pick from. It either arbitrarily picks one (possibly wrong) or hedges with a "conflicting information" response, both of which look broken to a buyer.

- **H3: If your data comes from more than one source, do the sources agree?**
  Test: pick 5–10 SKUs that exist in both your primary ERP export and any secondary source (a manually maintained price sheet, an older catalog feed), compare price and spec fields side by side.
  PASS: values match across sources.
  FAIL: the ERP says one price, the manual sheet says another, and nobody has reconciled them recently.
  Mechanical consequence: the same buyer question, asked minutes apart, could get two different prices depending on which file happened to feed the assistant — the exact inconsistency a human rep would never produce.

### H2: Can an AI agent actually filter and compare your products? (checkpoints 6–8)

Grouping logic: once records are deduplicated and internally consistent, the next question is whether they're rich enough to support the kind of comparative, spec-level questions buyers actually ask, not just lookup by name.

- **H3: Does every product carry a classification code?**
  Test: check whether the category/classification column (UNSPSC code, ETIM class, or internal category field) is populated on every row, not just a subset.
  PASS: populated on all or nearly all rows.
  FAIL: blank on a meaningful share of rows, typically older SKUs that predate the current classification scheme.
  Mechanical consequence: a buyer asking "show me all the enclosures rated for outdoor use" gets no answer for the unclassified products — not because they're irrelevant, but because there's no category signal for the assistant to filter on.

- **H3: Does your classification carry actual attributes, or just a bucket?**
  Test: check whether the classification standard in use is UNSPSC (a category code with no attribute payload by design) or ETIM/eCl@ss (a category plus a defined set of technical attributes such as voltage, IP rating, dimensions).
  PASS: for technical/spec-heavy lines (electrical, HVAC, industrial components), the export includes attribute fields, not just a category code.
  FAIL: a UNSPSC code and nothing else — the product is categorized but has no queryable specs.
  Mechanical consequence: the assistant can say "this is an enclosure" but not answer "what's the IP rating" or "is this compatible with a 24V system," because that data was never structured as its own field.

- **H3: Is unit of measure explicit and consistent?**
  Test: check whether every priced line has a UOM field (each, case, pallet, linear foot) and whether the price consistently corresponds to that UOM.
  PASS: UOM is a distinct field and price always matches it.
  FAIL: UOM is implied, inconsistent, or missing — the same price column sometimes means "per each," sometimes "per case," with no flag distinguishing them.
  Mechanical consequence: the assistant quotes a number without (or with the wrong) unit, and a buyer assumes $12 is per unit when it's actually per case of 50.

### H2: Will your pricing and inventory data still be true tomorrow? (checkpoints 9–10)

Grouping logic: the final stage is trust over time — does the reader know what kind of signal they're actually holding, and does it reflect who's asking.

- **H3: Do you know whether this file is a catalog snapshot or a live inventory signal?**
  Test: if your export is fed by or resembles an EDI transaction, check which transaction set it is — an 832 (price/sales catalog), an 846 (inventory inquiry/advice), or an 850 (purchase order, which pulls item numbers/prices from the 832). Also check the file's own generation timestamp.
  PASS: you know which transaction type and timestamp you're handing over, and know a catalog snapshot (832) does not carry live stock levels.
  FAIL: an 832 catalog extract gets treated as a real-time inventory source, because "it came from the ERP" felt authoritative enough not to question further.
  Mechanical consequence: the assistant states or implies stock availability from a file that structurally has no inventory field — that's not what an 832 is for. The buyer gets a stock claim backed by no data.

- **H3: Does pricing reflect customer groups, or only one list price?**
  Test: check whether the export includes a customer-group, contract-price, or tier field, or only a single flat price column regardless of buyer type.
  PASS: tier/group-specific pricing is present and mapped to the corresponding segment.
  FAIL: one price per SKU, no way to distinguish a list-price buyer from a contracted account.
  Mechanical consequence: the assistant quotes the same list price to every buyer, including ones with negotiated contract pricing — a pricing-integrity problem that erodes trust the moment a contracted buyer notices the mismatch.

### H2: What happens after your export passes this check? (ChatSKU's ONE dedicated section)

This is the only section that talks about ChatSKU directly. Keep it short (150–200 words), factual, and grounded only in verified mechanics: ChatSKU reads the PDF, Excel, ERP export, or CSV file a customer sends, and its team configures the assistant against that file. Do not claim ChatSKU pulls live from SAP/NetSuite/Business Central/etc., does not name any ERP connector, and does not describe an automated sync mechanism. Frame this section as: run this check on the file BEFORE you send it anywhere — to ChatSKU or any other tool that's going to answer buyer questions from it. A clean file makes the setup faster and the answers more trustworthy regardless of which tool receives it. One light, natural additional ChatSKU mention is fine in the Conclusion CTA; do not add ChatSKU mentions inside the checkpoint sections themselves.

### H2: People Also Ask (structural label — keep verbatim)

Use these 4 as H3 questions, answer each in 2–4 sentences:
1. What file format does my ERP actually export?
2. Why does my GTIN show up as scientific notation in Excel?
3. What's the difference between UNSPSC and ETIM classification?
4. How often should I re-export my product data for an AI assistant?

### H2: Conclusion (structural label — keep verbatim) + CTA

Reader walks away with: a completed (or partially completed) 10-point self-check and a clear sense of which checkpoints they failed and why it matters mechanically. CTA per brand.md convention — self-serve, specific, not "learn more." Suggested: "Start a free trial" → chatsku.com/signup/, or a line like "If your export just failed three of these checks, fix them first, then see how ChatSKU turns a clean one into a live catalog assistant" → chatsku.com/demo/. Conclusion body copy in the styled dark section per MUST-FOLLOW-RULES section 8 (no inline CTA link in the paragraph text itself; CTA is a separate button widget).

### H2: Frequently Asked Questions (structural label — keep verbatim)

Use these 5 as accordion Qs:
1. What is the minimum file format an AI catalog assistant needs to work with?
2. Can I use a plain CSV export, or do I need an API connection to my ERP?
3. What is GTIN scientific-notation corruption and how do I fix it?
4. Is UNSPSC enough for AI-agent product matching, or do I need ETIM/eCl@ss?
5. Does ChatSKU connect directly to my ERP, or do I need to send a file?
(Q5 should get a direct, honest answer per the ChatSKU positioning guardrail below — no connector claim.)

## AEO/GEO heading discipline

- Body H2s (the 4 thematic stages and the ChatSKU section) phrased as questions with direct-answer-first text underneath — lead each section with the plain-language answer, then unpack the checkpoints.
- Structural labels stay verbatim: Executive Summary, Introduction, People Also Ask, Conclusion, Frequently Asked Questions.
- H3 checkpoint headings should also read as questions where natural (see spine above) — this doubles as scannable pass/fail framing.

## Stats guidance — read carefully

The verified stat pool for this topic is thin, and that's expected. This article earns authority through technical specificity (naming real formats, real standards, real failure mechanics), not stat density. Do not pad with numbers to compensate.

**Explicitly dropped, do not reintroduce in any form, hedged or otherwise:**
- Gartner data-quality-cost figure ($12.9M–$15M/year) — dropped per instruction, even hedged.
- Gartner "67% rep-free" stat — banned, already used in 5+ ChatSKU posts.
- "$15T/90% by 2028" AI-agent-intermediated spend figure — unsourced, used by the untracked autonomous-buying post; do not reuse here.
- "94% of B2B buyers used AI" — aggregator conflation of a different Forrester stat, previously flagged unusable.
- "40% of inventory ignored" (Rewarx single-site claim) — no methodology, not reproducible. The creator may describe the underlying *mechanism* (AI agents don't infer missing attributes, they drop incomplete records from the candidate set) in the creator's own words, but must not cite "40%" or attribute it to a study.
- Do not invent any stat tying "wrong AI answer" incidence to export defects — research found no such study. Every failure-mode consequence in the spine above must stay illustrative and mechanical ("here's exactly what breaks"), never framed as "X% of the time this happens."

The two genuinely usable, evergreen, non-controversial facts (safe to state plainly, not as "stats" needing hedges):
- UNSPSC = classification with no attribute payload by design; ETIM/eCl@ss = classification with defined attributes per class. Verified against the standards bodies' own described scope.
- EDI 832 = price/sales catalog, EDI 846 = inventory inquiry/advice, EDI 850 = purchase order. Standard, non-controversial transaction-set definitions.

## Real technical grounding to include (mandatory)

- SAP: material master data is natively distributed via MATMAS06 IDocs (segment-based, e.g. E1MARAM), not a simple flat CSV; S/4HANA also offers an "Export Master Data" app for flat-file extracts and OData/BAPI for programmatic access. A SAP shop that says "we already export our data" may mean a years-old IDoc feed, not a clean flat file — worth calling out explicitly.
- NetSuite: saved-search results and item catalogs export as CSV; long numeric IDs like GTINs can get silently corrupted into scientific notation when opened in Excel, because CSV carries no type information. This is the single most concrete, self-verifiable test in the whole piece — use it prominently.
- Business Central: items are exposed via a documented REST/OData API with `$select`/`$filter` field selection; the legacy OData v4 page-based endpoints are being retired in favor of `/api/v2.0/`. Two BC shops can hand over structurally different exports depending on when their integration was built.
- Epicor and Infor: speak generally about categories of fields that typically exist (item info, inventory quantity, availability status). Do NOT invent specific field names, endpoint paths, or API structures for these two systems — research could not verify field-level detail. If precision is needed and unavailable, say so plainly rather than guessing.
- UNSPSC vs. ETIM/eCl@ss, GTIN, and EDI 832/846/850 are used throughout as checkable properties inside the self-check (per the spine above) — NOT as definitions. Post 2129 (agentic commerce glossary) owns the definitional treatment of these terms; this post assumes basic familiarity and links to 2129 once for readers who want the full definitions.

## ChatSKU positioning — critical guardrail

Research confirmed ChatSKU's ingestion is human-mediated: the customer sends a PDF/Excel/ERP export/CSV, and ChatSKU's team configures it against that file. There are no named ERP connectors and no verified automated-sync mechanics on any live ChatSKU page. Post 1455 was previously corrected post-publish for overclaiming a "live/cached/hybrid sync + named webhooks" architecture that couldn't be verified — do not repeat that mistake here.

- Zero claims anywhere in the article about live ERP sync, named connectors, or automatic ingestion.
- ChatSKU appears in exactly ONE dedicated section (see spine above) plus light, natural mentions elsewhere (e.g., the FAQ answer to "does ChatSKU connect directly to my ERP").
- The reader must get full, standalone value from running the 10-point self-check even if they never buy anything. This is an education-first technical piece, not a pitch — the user has previously rejected a ChatSKU draft for feeling "too promotional, didn't feel like a blog." Do not let that happen again.
- Frame the self-check as something the reader runs on their own file BEFORE sending it anywhere — vendor-neutral framing, ChatSKU as downstream beneficiary of clean data, not as the thing performing the audit.

## Uniqueness verification (performed)

- **Topic/angle/slug/keyword:** Checked against `published-posts-inventory.md` (all 29+ entries) and the live `/blog/` index. Slug `erp-export-ai-agent-ready` matches no existing slug. The inventory's own "topic gaps" list names this exact gap ("ERP-to-chat: turning SAP/NetSuite exports into live product answers," "catalog data quality: why bad SKU data breaks AI assistants") as open — this post fills both, deliberately.
- **Boundary vs. post 2129 (`/agentic-commerce-glossary/`):** 2129 owns protocol/standard definitions (ACP/AP2/MCP/A2A, and a definitional pass on GS1/UNSPSC/ETIM/PIM/punchout/EDI). This post does not redefine any of those terms from scratch — it references GTIN, UNSPSC/ETIM, and EDI 832/846/850 once each as checkable properties inside a pass/fail test, and links to 2129 once for readers who want full definitions. Do not reproduce 2129's phrasing or its shipped/announced status-label framing.
- **Boundary vs. the untracked live post `/ai-ready-b2b-catalog-autonomous-buying/`:** that post owns the persuasive, high-level "why machine-readable data matters before AI agents dominate by 2028" spine (and uses unsourced figures this post must never reuse). This post is the hands-on technical companion — link to it once for the broader stakes argument, do not rebuild its argument or reuse its framing/claims.
- **Boundary vs. WooCommerce/Magento integration guides (685/1056/1455) and PIM post 1538:** those posts cover ecommerce-platform-plus-plugin data architecture (WooCommerce/B2BKing/Wholesale Suite; Magento/Adobe Commerce) or the PIM-adjacency contrarian thesis — different systems and different argument from this post's raw ERP-export mechanics audit. Low overlap risk; 685/1056/1455 are good internal-link candidates for readers whose "ERP" is really an ecommerce platform with a B2B plugin. Do not link to `/product-information-management-software/` — post 1538 is still WP draft status and 404s on its public permalink.
- **Format rotation:** documented above under Format and length. Format D, first use for ChatSKU, chosen for structural fit (a sequenced playbook) and to avoid a third consecutive B/C-family post.

## Internal links (6–8, approved-list only)

Per MUST-FOLLOW-RULES section 6, only links from the approved list may be used. The untracked `/ai-ready-b2b-catalog-autonomous-buying/` post is NOT on that static list (it was found only by live-fetching `/blog/`), so it is excluded here even though the uniqueness section above discusses it as a boundary case — flag to the publisher as a candidate to add to the approved list once it's formally indexed, but do not link to it from this brief's approved set.

1. `/agentic-commerce-glossary/` — place in the Introduction, right after the one-sentence standards reference. Anchor: **"agentic commerce glossary"**
2. `/woocommerce-b2b-chatbot-integration/` — place in "What kind of export file do you actually have?" as an aside for readers whose "ERP" is really WooCommerce plus a B2B plugin. Anchor: **"WooCommerce B2B data guide"**
3. `/magento-b2b-chatbot-integration/` — same section, same logic, for Adobe Commerce/Magento readers. Anchor: **"Magento B2B integration guide"**
4. `/what-is-a-b2b-catalog-chatbot/` — place in the Introduction or the ChatSKU section, for readers new to the category. Anchor: **"what a catalog assistant does"**
5. `/rfq-automation-for-product-catalogs/` — place in "Will your pricing and inventory data still be true tomorrow?" (ties pricing-tier mapping to RFQ/quote workflows). Anchor: **"RFQ automation for catalogs"**
6. `/for-b2b-manufacturers-distributors-and-wholesalers/` — place just before the Conclusion CTA. Anchor: **"built for manufacturers and distributors"**
7. `/features/` — place in the ChatSKU dedicated section, factually accurate per verification (reads PDF/Excel/ERP export/CSV). Anchor: **"what ChatSKU connects to"**
8. `/demo/` (Conclusion CTA button) and `/signup/` (optional second CTA mention) — standard closers, not counted against the contextual-link count above.

**External links (max 2, load-bearing only):**
1. GS1 GTIN Management Standard (`ref.gs1.org/standards/gtin-management/`) — place at the GTIN checkpoint. Anchor: **"GS1 GTIN standard"**
2. SAP Help Portal — IDoc Types for Material Master Data (`help.sap.com`) — place at the "know your export's native format" checkpoint. Anchor: **"SAP IDoc documentation"**

Publisher must verify both external and all internal links return HTTP 200 immediately before push, per `feedback-verify-internal-links-live` — this brief only confirms they were valid at research time.

## Images

- **Featured (860×452):** IT/operations manager at a monitor reviewing a spreadsheet or data export, office setting. Search direction: "IT manager reviewing data spreadsheet office" or "person analyzing data screen office desk."
- **Body image 1 (860×452):** placed in "What kind of export file do you actually have?" — close-up of hands/keyboard with spreadsheet or code/data on screen, suggesting the literal act of opening and inspecting an export file. Search direction: "close up computer screen spreadsheet data" or "person typing data analysis screen."
- **Body image 2 (860×452):** placed in "Will your pricing and inventory data still be true tomorrow?" or the ChatSKU section — warehouse operations desk with inventory/order software visible on screen, connecting the pricing/inventory checkpoint to a real operations setting. Search direction: "warehouse operations desk computer inventory" or "distribution warehouse office inventory screen."
- No abstract AI/robot imagery, no nature. All business/office/IT/warehouse scenes per section 3. Visual QA required before selection (generic keyword search alone produces mismatched stock).

## Meta

- **Yoast meta title (≤60 chars, ends `| ChatSKU`):** `ERP Export AI-Agent Ready? 10-Minute Self-Check | ChatSKU` (57 chars)
- **Yoast meta description (150–160 chars):** `A 10-minute technical self-check for your ERP product export before an AI agent reads it: GTIN integrity, duplicate SKUs, UNSPSC vs ETIM, and price tiers.` (154 chars)
- Publisher should recount both precisely at build time and adjust by a few characters if needed; these are close estimates.

## Voice reminder for the creator

- No em dashes anywhere (periods, commas, or hyphens instead).
- No "AI-powered" as filler — be specific about what the AI does at each failure point.
- No hype words (revolutionary, game-changing, cutting-edge, transform your...).
- No AI-tell words (delve, leverage, navigate as a verb, realm, landscape, ecosystem).
- Second person throughout ("you," "your").
- Open with a concrete scenario, not a definition of agentic commerce or AI agents — that ground is already covered elsewhere.
- Vary sentence length aggressively per voice.md; lead each section with its strongest sentence.
- Never call ChatSKU "just a chatbot"; never say "solutions" as filler.

## Must include

- All 10 checkpoints from the spine above, each with its literal pass/fail test and mechanical consequence.
- SAP MATMAS06/IDoc, NetSuite CSV scientific-notation corruption, and Business Central OData `$select` as the three concretely-sourced ERP mechanics.
- UNSPSC-vs-ETIM/eCl@ss attribute distinction, stated plainly as fact.
- EDI 832/846/850 roles, used as checkable file properties.
- The one dedicated ChatSKU section, framed vendor-neutral ("run this before you send the file to anyone").
- 5 FAQ answers and 4 PAA answers as specified above.

## Must NOT include

- Any claim of ChatSKU live ERP sync, named connectors, or automated ingestion.
- Gartner data-quality-cost figure (even hedged), Gartner 67% rep-free stat, "$15T/90% by 2028," "94% of B2B buyers used AI," "40% of inventory ignored."
- Any invented stat tying wrong-AI-answer incidence to export defects.
- Invented field names, endpoint paths, or API structures for Epicor or Infor — speak generally only.
- Redefinition of ACP/AP2/MCP/A2A or any protocol-level content — that's post 2129's job.
- A link to `/product-information-management-software/` (404s, post 1538 still draft).
- More than 2 external links, or any link to a competitor.

## Headline direction

Declarative-with-question-mark hybrid, matching the given direction. Keep the self-check promise and the ERP export subject; sentence case.

1. Is your ERP export AI-agent-friendly? A 10-minute self-check
2. Your ERP export isn't ready for an AI agent yet. Here's the 10-minute check that tells you.
3. Ten minutes, one file: the AI-agent readiness check for your ERP export

## Open questions for the creator

- Whether to open with a SAP-specific scenario or a more generic "pulled up our export" scenario — either works; pick whichever lands more vividly in under 60 words.
- Whether checkpoint 3 (field-selection completeness) reads better folded into checkpoint 1 as a sub-point rather than its own H3, if word count runs tight — creator's call, as long as all 10 checkpoints' pass/fail/consequence content survives somewhere.
- Whether to add a one-line summary checklist (10 items, no elaboration) near the top of the Executive Summary as a scannable preview — optional, use judgment on whether it helps or just repeats content.
