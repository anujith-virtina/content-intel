---
title: Research notes — Is your ERP export AI-agent-friendly? A 10-minute self-check
client: chatsku
date: 2026-08-17
topic: How IT/operations managers at B2B manufacturers/distributors can audit their ERP product-data export for AI-agent readiness
slug: erp-export-ai-agent-ready
stage: research
---

# Research: Is your ERP export AI-agent-friendly? A 10-minute self-check

## Mandatory-rules check (done first)

Read in full: `clients/chatsku/MUST-FOLLOW-RULES.md`, `style/voice.md`, `style/audience.md`, `style/brand.md`, `style/cms.md`, `style/examples.md`, `reference/published-posts-inventory.md` (all 29 entries + topic-gaps list). Also fetched `https://chatsku.com/blog/` live (10 most recent posts, current through Aug 10 2026) to catch anything published after the inventory file's last update (2026-07-27) — nothing on ERP export mechanics found there; the newest posts are `agentic-commerce-glossary` (Aug 6/10) and `one-line-of-code` (Aug 3/5).

## Sub-questions

1. What does a real product-data export actually look like out of the ERPs this audience runs (SAP, NetSuite, Business Central, Epicor, Infor, Acumatica, Sage, spreadsheet-era setups) — format, structure, characteristic gaps?
2. What specific, checkable properties does an AI assistant/agent need from that data to answer a buyer correctly, and which of those map to real named standards (GS1/GTIN, UNSPSC, ETIM, cXML/punchout, EDI 832/846/850, schema.org Product) versus vendor jargon?
3. What are the concrete, mechanically explainable failure modes when the export is bad?
4. What stats survive primary-source scrutiny, and which fail?
5. What already ranks for this topic, and what's the structural gap ChatSKU can own?
6. Does this duplicate any existing ChatSKU post (especially the glossary post, the untracked persuasive catalog post, and the PIM post)?
7. What can ChatSKU truthfully claim about its own ingestion mechanics, verified against its live pages?

## Key findings

### Finding 1: ERP exports are still overwhelmingly flat-file, not live API, for the mid-market B2B audience this reader represents

- Source: [NetSuite CSV Export documentation](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_1201045458.html) — Oracle NetSuite official docs
- What it says: Saved-search results and full item catalogs export as CSV; long numeric IDs (like GTINs) can get silently mangled into scientific notation when opened in Excel because CSV has no type information.
- Why it matters: This is a real, checkable failure mode a reader can verify in 30 seconds by opening their own export and looking at any 13-14 digit ID column.

### Finding 2: SAP's native master-data exchange format is IDoc (MATMAS message type), not CSV — a fundamentally different structure than what most integrators expect

- Source: [SAP Help Portal — IDoc Types for Distributing Material Master Data by ALE](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/f7fddfe4caca43dd967ac4c9ce6a70e4/afb1c053f89eb64ce10000000a174cb4.html); [SAP Help — Export Master Data app](https://help.sap.com/docs/SAP_S4HANA_CLOUD/f86dc2eb1f8b48c880a7607213104b27/ef48d2d293294b2a98afc3637bbbbf6f.html)
- What it says: Material master data is natively distributed via MATMAS06 IDocs (segment-based, e.g. E1MARAM), a hierarchical EDI-like format; S/4HANA also offers an "Export Master Data" app for flat-file extracts of selected fields, and OData/BAPI for programmatic access.
- Why it matters: A SAP shop that says "we already export our data" may mean an IDoc feed a middleware consultant built years ago, not a clean flat file — worth calling out explicitly since this audience runs SAP Business One or S/4HANA disproportionately.

### Finding 3: Dynamics 365 Business Central exposes items through a documented REST/OData API with selectable fields, but the older OData v4 page-based endpoints are being retired in favor of `/api/v2.0/` API pages

- Source: [Microsoft/Celigo — Business Central API reference](https://docs.celigo.com/hc/en-us/articles/5993778738203-Available-Microsoft-Dynamics-365-Business-Central-APIs); [rapidionline.com — OData to API Pages migration guide](https://www.rapidionline.com/product-updates/dynamics-365-business-central-odata-api-pages-migration-guide)
- What it says: `GET /api/v2.0/companies({id})/items` with `$select`/`$filter` returns item number, description, unit price, category code, inventory quantity; legacy `/ODataV4/Page/...` endpoints are being phased out.
- Why it matters: Two Business Central shops can hand over structurally different exports depending on when their integration was built — a good concrete example for the self-check's "which endpoint version" checkpoint.

### Finding 4: Acumatica and Epicor both expose contract-based REST APIs, but field-level documentation is fragmented across partner/integrator sites rather than one canonical reference

- Source: [Acumatica Cloud ERP APIs overview](https://www.acumatica.com/blog/yes-we-have-an-api-for-that-an-introduction-to-the-acumatica-cloud-erp-apis/); [DCKAP — Epicor API integration guide](https://www.dckap.com/blog/epicor-api/)
- What it says: Acumatica directs new integrations to its contract-based REST API (with OData/Generic Inquiry for custom views); Epicor's API surfaces product info, inventory quantity, and availability status but detailed field-by-field docs aren't consolidated publicly.
- Why it matters: [unverified] I could not find a single authoritative field list for Epicor or Infor product exports — flag this honestly in the piece rather than inventing field names for those systems. Keep Epicor/Infor treatment general (what categories of fields exist) rather than claiming exact field names, unlike SAP/NetSuite/Business Central where I found primary docs.

### Finding 5: The named data standards this audience should recognize are real and distinct — not interchangeable, not vendor jargon

- Source: [GS1.org — GTIN Management Standard](https://ref.gs1.org/standards/gtin-management/); [GS1 US Data Hub guide](https://www.gs1us.org/content/dam/gs1us/documents/tools-resources/resources/data-hub-help-center/gs1-us-data-hub-product-create-manage-user-guide.pdf); [Claro — ETIM vs UNSPSC vs eCl@ss](https://getclaro.ai/resources/comparisons/etim-vs-unspsc-vs-eclass/); [1EDISource — EDI 832](https://www.1edisource.com/resources/edi-transactions-sets/edi-832/); [Comparatio — EDI 846](https://www.commport.com/edi-inventory-accuracy-edi-832-vs-edi-846-vs-edi-947/); [Wikipedia — cXML](https://en.wikipedia.org/wiki/CXML)
- What it says: GTIN = globally unique product identifier (GS1). UNSPSC = 5-level procurement/spend classification with no attribute payload — good for categorization, useless for specs. ETIM/eCl@ss = technical classification standards that DO carry defined attributes and permitted values per class, used heavily in electrical/HVAC/industrial distribution. EDI 832 = price/sales catalog transaction; EDI 846 = inventory inquiry/advice; EDI 850 = purchase order (pulls item numbers/prices from the 832). cXML = Ariba-originated XML standard for B2B punchout procurement; SAP shops instead often use OCI (Open Catalog Interface).
- Why it matters: This is exactly the kind of "which of these are real standards vs. vendor jargon" grounding the audience will fact-check. UNSPSC-without-attributes vs ETIM-with-attributes is a genuinely useful, underused distinction for the checklist.

### Finding 6: AI shopping/product agents are documented to skip products when structured attributes or stable identifiers are missing — this is the direct mechanical link between "bad export" and "wrong or missing answer"

- Source: [Rewarx — AI Shopping Agents Need Structured Data](https://www.rewarx.com/blogs/ai-shopping-agents-need-structured-data)
- What it says: In a cited production audit of one Shopify store, AI shopping assistants reportedly ignored over 40% of inventory where the feed lacked structured attributes and stable identifiers; agents generally don't infer missing attributes, so incomplete records drop out of the candidate set entirely.
- Why it matters: [unverified — single-site claim, no named auditor, no methodology, not independently reproducible]. Useful for the *mechanism* (agents don't guess, they drop) but do NOT cite the "40%" figure as a stat; describe the mechanism in our own words instead.

### Finding 7: Poor data quality's "$X million per year" figure is a real, widely-cited Gartner estimate — but only reachable through secondary citations, not Gartner's original paywalled report

- Source: [Gartner — Data Quality overview page](https://www.gartner.com/en/data-analytics/topics/data-quality) (confirms Gartner as originator); secondary citations at [Dataversity](https://www.dataversity.net/articles/putting-a-number-on-bad-data/) and [Actian](https://www.actian.com/blog/data-management/the-costly-consequences-of-poor-data-quality/)
- What it says: Gartner's often-cited figure is that poor data quality costs organizations an average of $12.9–15 million per year (the $15M figure traces to Gartner's 2017 research; a related $12.9M figure comes from Gartner's 2020 Magic Quadrant for Data Quality Solutions, based on a survey of 154 reference customers).
- Why it matters: [use with caution] This is a real Gartner-attributed figure, distinct from the banned "67% rep-free" Gartner stat, but I could not verify it against Gartner's original document (paywalled) — only against secondary aggregator citations that don't agree on the exact year/number ($12.9M vs $15M). Recommend either dropping it or citing it narrowly as "Gartner has estimated poor data quality costs organizations $12–15 million a year" with a hedge, not a precise single figure.

## Data points

| Stat | Value | Source | Date | Verification status |
|------|-------|--------|------|------|
| Gartner data-quality cost estimate | "$12.9M–$15M/year average" | Gartner (via secondary citations: Dataversity, Actian) | 2017/2020 | Real Gartner-attributed figure but only found via secondary sources; two different numbers/years circulating. Use hedged or drop. |
| MCP enterprise adoption prediction | "30% of enterprise application vendors will launch MCP servers in 2026" | CData Software estimate (via Medium article) | 2026 | Vendor prediction, not measured outcome. Flag as [unverified] forward-looking claim if used at all — better to omit. |
| AI agents skipping incomplete inventory | "ignored over 40% of inventory" in one Shopify audit | Rewarx blog, uncredited "production audit" | 2026 | [unverified] — single site, no methodology, not a study. Do not cite the number; may describe the mechanism qualitatively. |
| UNSPSC / ETIM structural distinction | UNSPSC = no attribute payload; ETIM/eCl@ss = defined attributes per class | GS1/Claro/AtroPIM comparison pieces citing the standards' own governing bodies | Evergreen | Verified — matches how the standards bodies themselves describe scope. Safe to state as fact, not a "stat." |
| EDI 832/846/850 roles | 832=catalog, 846=inventory, 850=purchase order | 1EDISource, Commport, SPS Commerce (EDI VAN/vendor documentation, consistent across sources) | Evergreen | Verified — standard, non-controversial transaction-set definitions. |

**Rejected per explicit instruction (do not reuse):**
- Gartner "67% rep-free" — banned, used in 5+ ChatSKU posts already.
- "$15T/90% by 2028" AI-agent-intermediated spend — this is the exact unsourced figure the untracked `/ai-ready-b2b-catalog-autonomous-buying/` post uses with "no external sources or studies referenced." Confirmed unsourced on refetch. Do not use.
- "94% of B2B buyers used AI" — prior research already flagged this as an aggregator conflation of a different Forrester buying-group stat. Not reused here.

## Conflicts and disagreements

- **Position A** (Gartner via Dataversity): poor data quality costs ~$15M/year (2017 estimate).
- **Position B** (Gartner via Actian, citing the 2020 Magic Quadrant survey): ~$12.9M/year.
- **What's actually true:** Both trace to Gartner but are different survey years/methodologies circulating interchangeably online. Treat as a directional, hedged range — not a precise citation-worthy figure. Recommend the article state it qualitatively ("Gartner has repeatedly put the cost of bad data in the eight figures annually") rather than quoting either number as exact, or omit entirely given the ambiguity.
- **Position A** (ChatSKU's own live marketing pages — `/features/`, `/for-b2b-manufacturers-distributors-and-wholesalers/`, `/pdf-catalog-chatbot/`): ingestion is manual and human-configured — "send us your catalog," ChatSKU's team configures it, no named ERP systems, no described sync mechanism beyond CRM/ERP CSV import for customer lists.
- **Position B** (prior ChatSKU technical posts, e.g. `/woocommerce-b2b-chatbot-integration/`, post 1455): describes a more automated, API-level integration model with plugin-specific data reads, "automatic background sync over the API."
- **What's actually true:** Post 1455 itself had to be corrected after publish for overclaiming a "live/cached/hybrid sync + named webhooks" architecture ChatSKU could not verify (see inventory note on post 1455, and memory `feedback-verify-product-mechanics`). The verifiable baseline, confirmed on ChatSKU's own live pages today, is: ChatSKU ingests PDF/Excel/ERP-export/CSV files that a customer sends, its team configures the assistant against that file, and updates happen through that same human-mediated process — not a described live ERP-to-ChatSKU sync. This new post must not claim ChatSKU auto-pulls from SAP/NetSuite/etc. It should describe the self-check as something the reader runs on their own export FILE before sending it, and stay silent on (or only lightly/vaguely reference) how ChatSKU refreshes data afterward, rather than asserting a sync mechanism.

## Competitive scan

1. **Rewarx — "AI Shopping Agents Need Structured Data"** (rewarx.com). Angle: schema.org/JSON-LD-only, retail/Shopify-BigCommerce framing, includes a genuine 9-point structured-data checklist and 8-step workflow. Gap: zero mention of ERP systems, zero backend/export-file mechanics, targets marketing ops not IT/operations managers, no B2B-specific fields (MOQ, tiered pricing, UOM/case-pack).
2. **Stellagent.ai — "Agent-Ready Product Data"** and **writetext.ai — "How AI Shopping Agents Pick Products"**. Angle: structured-data strategy explainers, consumer/DTC-leaning. Gap: same as above — abstract "structure your data" advice, no literal file-level audit steps.
3. **Optimizely — "The AI Checklist" / "The B2B AI Checklist"**. Angle: enterprise readiness checklist including single-source-of-truth and real-time ERP sync questions; closer to B2B but framed as a strategic/organizational checklist (people, process, governance), not a technical pass/fail test against an actual export file's fields and formatting.
4. **iovista — "AI-Ready Catalogs for B2B"**. Angle: PIM/enrichment vendor content; states general principles (structured attributes, consistent naming, real-time pricing) without file-level mechanics or named ERP export formats.
5. **CNABKE "GEO Self-Audit Checklist for B2B Export Websites"**. Angle: closest structural match found — a 10-point self-audit format — but it's a website/GEO (generative engine optimization) audit, not an ERP-export/product-data audit; different subject entirely, same *format* worth noting.

**The gap, confirmed:** Every piece found either (a) stays at the abstract "your data must be clean/structured" level with no way to test it, or (b) is schema.org/website-markup focused with zero ERP vocabulary, or (c) is a strategic/organizational B2B AI-readiness checklist (governance, single source of truth) rather than a field-by-field technical audit an IT manager can run against the literal CSV/XML/IDoc file sitting on their desktop in ten minutes. Nobody names SAP IDoc segments, NetSuite CSV scientific-notation corruption, Business Central OData field selection, or UNSPSC-vs-ETIM in the same piece as a checklist. That is the opening.

## Uniqueness verdict

**Verdict: unique. Clear to proceed with the technical-audit angle, subject to the guardrails below.**

- `clients/chatsku/reference/published-posts-inventory.md` topic-gaps list explicitly lists "ERP-to-chat: turning SAP/NetSuite exports into live product answers" and "Catalog data quality: why bad SKU data breaks AI assistants" as **open gaps, not yet covered**. This post fills both.
- **`/agentic-commerce-glossary/` (post 2129)** owns protocol-definition intent (ACP/AP2/MCP/A2A, shipped-vs-announced labels) and already covers GS1/UNSPSC/ETIM/PIM/punchout/EDI at a glossary-definition level in its "data standards you already own" section. **Overlap risk: real but manageable.** Our post must not re-define these standards from scratch — reference them once each, briefly, in service of the checklist item, and link to the glossary post for readers who want the full definition. Do not reproduce the glossary's exact phrasing or its status-label framing (shipped/announced/vendor-jargon).
- **Untracked live post `/ai-ready-b2b-catalog-autonomous-buying/`** (fetched directly): confirmed thesis is the urgent, high-level persuasion piece — "transform your catalog into a machine-readable system before AI agents dominate by 2028," structured as Problem/Business-Impact/How-to-spot-it under 5 H2s, uses the unsourced $15T/90%-by-2028 and "70% of business to fastest quote" figures, "no external sources or studies referenced" per the fetch. It does NOT contain SAP/NetSuite/Business Central mechanics, does NOT contain a field-level or file-level checklist, and does NOT name any real data standard by its correct technical scope. **Our post is the hands-on technical companion this piece gestures at but never delivers** — safe to link to it once (e.g., "for the bigger why, see our piece on agentic buying") without cannibalizing it.
- **Post 1538 (`product-information-management-software`)**: contrarian "PIM organizes data, still can't answer the buyer" thesis. Explicitly different problem (PIM-adjacency/category positioning vs. our raw export-mechanics audit). Its own inventory note calls out that the "bad SKU data breaks AI assistants" gap was deliberately left open for a future post — this is that post. Do not link to it: **it 404s (post 1538 still in WP draft, no public permalink) — confirmed still true per the rule already documented in MUST-FOLLOW-RULES and the inventory. Do not propose it as an internal link.**
- **`/woocommerce-b2b-chatbot-integration/` (1455) and `/magento-b2b-chatbot-integration/` (1056)**: both cover "what data ChatSKU reads" but for ecommerce-platform-plus-plugin stacks (WooCommerce/B2BKing/Wholesale Suite; Magento/Adobe Commerce B2B), not ERP systems. Different systems, different mechanics, low overlap risk — good internal-link candidates for readers whose "ERP" is actually a WooCommerce/Magento store with a B2B plugin bolted on.
- Checked `/blog/` live (fetched directly, current through Aug 10 2026) and two untracked posts not yet in the inventory file: `/24-7-b2b-ai-buying-assistant/` (July 22, deployment-speed/5-minutes-to-live angle) and `/reduce-b2b-quote-response-time/` (July 26, quote response time). Neither touches ERP export mechanics or data-format standards. No overlap.
- Slug `erp-export-ai-agent-ready` does not match any existing slug in the inventory or the live `/blog/` list.
- Format: MUST-FOLLOW-RULES section 11 rotation note (from post 2129) says Format A was just used for the glossary post and reset a B/C-heavy run. **Recommend Format D (decision-tree/playbook) or a checklist-native structural variant** — the brief's "10-minute self-check" structure is inherently a sequenced pass/fail playbook, which fits Format D better than repeating Format A twice in a row, and better than Format B (this isn't a Q&A) or C (this isn't an opinionated listicle of reasons). Flagging for the analyzer to make the final call and document it.

## ChatSKU product truth (verified against live pages)

Fetched `/features/`, `/for-b2b-manufacturers-distributors-and-wholesalers/`, `/pdf-catalog-chatbot/` directly.

- **Verified, can state plainly:** ChatSKU reads PDF, Excel, ERP export, and product-feed files — quoted directly from the live `/pdf-catalog-chatbot/` page: ChatSKU "reads your existing PDF, Excel, or ERP export," including "old, messy, scanned, or spread across multiple files." Customer lists can be imported "by CSV, sync from CRM or ERP" per `/pdf-catalog-chatbot/`.
- **Verified, can state plainly:** No specific ERP system (SAP, NetSuite, Dynamics, etc.) is named on any of the three live pages. Do not imply ChatSKU has a named, certified SAP/NetSuite connector — it does not claim one.
- **NOT verifiable, must not claim:** Any real-time or automated pull FROM an ERP. The live pages describe a human-mediated flow: customer sends their catalog/export file, ChatSKU's team configures the assistant against it, then a one-line script deploys it. No API-level ERP sync, no named webhook architecture, no refresh-cadence claim appears on any live page. Post 1455's prior overclaim-and-correction (see memory `feedback-verify-product-mechanics`) is the direct cautionary precedent — do not repeat that mistake here by implying the self-check feeds directly into an automated ChatSKU pull.
- **Framing implication for the brief:** the article's premise should be "run this check on the export file BEFORE you send it to whatever tool (ChatSKU or otherwise) is going to answer buyer questions from it" — a genuinely vendor-neutral technical audit with ChatSKU positioned as the downstream beneficiary of clean data, not as the thing performing the audit or the ERP sync.

## Internal link candidates (6-8, contextually chosen)

1. `/agentic-commerce-glossary/` — for readers who want the full ACP/AP2/MCP/A2A and standards definitions this post only references in passing. Anchor idea: "agentic commerce glossary."
2. `/ai-ready-b2b-catalog-autonomous-buying/` — the persuasive "why this matters" companion piece; link once for the broader stakes argument this post doesn't re-make. Anchor idea: "why AI agents are already buying from your competitors" (verify live 200 before use — untracked in inventory, confirm via direct fetch at publish time).
3. `/woocommerce-b2b-chatbot-integration/` — for readers whose "ERP" is really WooCommerce plus a B2B pricing plugin. Anchor idea: "WooCommerce B2B data architecture."
4. `/magento-b2b-chatbot-integration/` — same logic for Adobe Commerce/Magento readers. Anchor idea: "Magento B2B integration guide."
5. `/what-is-a-b2b-catalog-chatbot/` — definitional companion for readers new to the category. Anchor idea: "what a B2B catalog chatbot actually does."
6. `/for-b2b-manufacturers-distributors-and-wholesalers/` — solution page, contextual mid-article or pre-CTA. Anchor idea: "built for manufacturers and distributors."
7. `/features/` — what ChatSKU connects to, factually accurate per verification above. Anchor idea: "what ChatSKU connects to."
8. `/demo/` and `/signup/` — standard CTA closers per brand.md conventions.

**Explicitly excluded:** `/product-information-management-software/` (404s, post 1538 still WP draft — confirmed still the case). Do not link to it.

**Note for publisher:** every one of the above (except the untracked autonomous-buying post) should still get the standard live-200 pre-publish check per `feedback-verify-internal-links-live` — this research only confirms they existed in the inventory/live blog list, not that they resolve at publish time.

## The gap

> Every "AI-ready product data" article either stays abstract ("your data must be clean and structured") or is schema.org/website-markup focused with zero ERP vocabulary. Nobody hands an IT or operations manager who owns the actual ERP export a literal, field-by-field pass/fail test they can run against the CSV/XML/IDoc file sitting on their desktop in ten minutes — naming real formats (SAP IDoc, NetSuite CSV, Business Central OData), real standards (GTIN, UNSPSC vs. ETIM, EDI 832/846/850), and real failure mechanics (wrong UOM quoted, duplicate SKUs, price shown to wrong tier).

## Recommended angle

> A hands-on, vendor-neutral 10-point self-check the reader runs against their own real export file today — grounded in how SAP, NetSuite, Business Central, Epicor, Infor, and Acumatica actually structure exports, and in real data standards (GTIN, UNSPSC/ETIM, EDI 832/846/850) — positioned as the technical companion to ChatSKU's existing persuasive "why this matters" post, not a rehash of it.

## Couldn't find

- **Epicor and Infor field-level export documentation.** Public docs are fragmented across partner/integrator blogs; I could not find an authoritative field list for either system the way I could for SAP (IDoc/MATMAS), NetSuite (CSV/saved search), and Business Central (OData `$select`). The brief/draft should treat Epicor/Infor at the category level (what kinds of fields typically exist) rather than naming exact field names, and flag this limitation if precision is needed.
- **A single authoritative primary source for the Gartner data-quality cost figure.** Only secondary citations found, with two different numbers ($12.9M vs $15M) attributed to two different Gartner years. Recommend hedging or omitting rather than quoting a precise figure.
- **Any credible, reproducible study quantifying how much of "AI agent gave a wrong B2B answer" traces specifically to export-file problems** (as opposed to general "bad data quality" ecommerce-returns statistics, which are consumer-retail-focused and not clearly transferable to B2B agent-answer-accuracy). The article's failure-mode examples should therefore be framed as illustrative, mechanically-explained scenarios — which the brief explicitly asked for — not as stat-backed incidence rates.

## Sources

- [NetSuite — Create a Saved Search and Export to a CSV file](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_1201045458.html) — Oracle official docs, primary
- [NetSuite — Exporting Search Results](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N663983.html) — Oracle official docs, primary
- [SAP Help Portal — IDoc Types for Distributing Material Master Data by ALE](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/f7fddfe4caca43dd967ac4c9ce6a70e4/afb1c053f89eb64ce10000000a174cb4.html) — SAP official docs, primary
- [SAP Help Portal — Export Master Data](https://help.sap.com/docs/SAP_S4HANA_CLOUD/f86dc2eb1f8b48c880a7607213104b27/ef48d2d293294b2a98afc3637bbbbf6f.html) — SAP official docs, primary
- [Celigo — Available Microsoft Dynamics 365 Business Central APIs](https://docs.celigo.com/hc/en-us/articles/5993778738203-Available-Microsoft-Dynamics-365-Business-Central-APIs) — integrator documentation citing Microsoft API structure, secondary
- [RapidiOnline — OData to API Pages migration guide](https://www.rapidionline.com/product-updates/dynamics-365-business-central-odata-api-pages-migration-guide) — integrator, secondary
- [Acumatica — Yes, We Have an API for That](https://www.acumatica.com/blog/yes-we-have-an-api-for-that-an-introduction-to-the-acumatica-cloud-erp-apis/) — Acumatica official blog, primary
- [DCKAP — Exploring Epicor API Integration](https://www.dckap.com/blog/epicor-api/) — integrator, secondary
- [GS1 — GTIN Management Standard](https://ref.gs1.org/standards/gtin-management/) — GS1 official standard, primary
- [GS1 US — Data Hub Product GTIN Creation Guide (PDF)](https://www.gs1us.org/content/dam/gs1us/documents/tools-resources/resources/data-hub-help-center/gs1-us-data-hub-product-create-manage-user-guide.pdf) — GS1 US official, primary
- [Claro — ETIM vs UNSPSC vs eCl@ss](https://getclaro.ai/resources/comparisons/etim-vs-unspsc-vs-eclass/) — vendor content, secondary but accurately describes standards' own scope
- [1EDISource — EDI 832: Price/Sales Catalog](https://www.1edisource.com/resources/edi-transactions-sets/edi-832/) — EDI VAN documentation, secondary/industry-standard reference
- [Commport — EDI 832 vs EDI 846 vs EDI 947](https://www.commport.com/edi-inventory-accuracy-edi-832-vs-edi-846-vs-edi-947/) — EDI VAN documentation, secondary
- [Wikipedia — cXML](https://en.wikipedia.org/wiki/CXML) — general reference, secondary
- [Rewarx — AI Shopping Agents Need Structured Data](https://www.rewarx.com/blogs/ai-shopping-agents-need-structured-data) — vendor blog, secondary, competitive scan + one unverified stat flagged
- [Rewarx — AI Shopping Agents Read Schema, Not Homepages](https://www.rewarx.com/blogs/ai-shopping-agents-read-schema-2026) — vendor blog, competitive scan
- [Stellagent — Agent-Ready Product Data](https://stellagent.ai/insights/agent-ready-product-data-structured-data) — vendor blog, competitive scan
- [Optimizely — The AI Checklist](https://www.optimizely.com/insights/blog/the-ai-checklist/) — vendor blog, competitive scan
- [Optimizely — The B2B AI Checklist](https://www.optimizely.com/insights/blog/the-b2b-ai-checklist/) — vendor blog, competitive scan
- [iovista — AI-Ready Catalogs for B2B](https://www.iovista.com/ai-ready-catalog-b2b-product-data-optimization/) — vendor blog, competitive scan
- [CNABKE — GEO Self-Audit Checklist for B2B Export Websites](https://www.cnabke.com/en/blogs/geo-self-audit-checklist-b2b-site.html) — vendor blog, competitive scan (format reference only)
- [Gartner — Data Quality topic page](https://www.gartner.com/en/data-analytics/topics/data-quality) — Gartner official, confirms Gartner as originator of the cost estimate but not the specific figure
- [Dataversity — Putting a Number on Bad Data](https://www.dataversity.net/articles/putting-a-number-on-bad-data/) — secondary citation of Gartner figure
- [Actian — The Costly Consequences of Poor Data Quality](https://www.actian.com/blog/data-management/the-costly-consequences-of-poor-data-quality/) — secondary citation of Gartner figure
- [chatsku.com/pdf-catalog-chatbot/](https://chatsku.com/pdf-catalog-chatbot/) — ChatSKU live page, primary/brand-truth source
- [chatsku.com/features/](https://chatsku.com/features/) — ChatSKU live page, primary/brand-truth source
- [chatsku.com/for-b2b-manufacturers-distributors-and-wholesalers/](https://chatsku.com/for-b2b-manufacturers-distributors-and-wholesalers/) — ChatSKU live page, primary/brand-truth source
- [chatsku.com/ai-ready-b2b-catalog-autonomous-buying/](https://chatsku.com/ai-ready-b2b-catalog-autonomous-buying/) — ChatSKU live post, primary source for uniqueness check
- [chatsku.com/blog/](https://chatsku.com/blog/) — ChatSKU live blog index, primary source for uniqueness check
- `clients/chatsku/reference/published-posts-inventory.md` — internal inventory, primary source for uniqueness check
