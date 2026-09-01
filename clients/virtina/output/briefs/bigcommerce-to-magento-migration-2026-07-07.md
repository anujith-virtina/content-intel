---
title: Brief — BigCommerce to Magento migration: 2026 guide
client: virtina
date: 2026-07-07
topic: BigCommerce to Magento Migration 2026
slug: bigcommerce-to-magento-migration
stage: brief
audience: B2B store owners and eCommerce directors currently on BigCommerce, evaluating Magento as a migration destination
research: clients/virtina/output/research/bigcommerce-to-magento-migration-2026-07-07.md
---

# Brief: BigCommerce to Magento migration — 2026 guide

---

## Format selection

**Chosen format: Format D — Decision-tree / Playbook**

**Reason:** This topic is inherently a sequential decision, not a list of options. The reader wants to answer "should I migrate?" and then "how do I do it?" in order. Format D's phased structure maps directly to those two questions.

**Recency check (last 10 published posts):**
Format A appears at least 4 times in the last 10 posts (IDs 42393, 42391, 42108, 42074) — exceeds the 3-post threshold, therefore Format A is overused and skipped.
Format D does not appear in any of the last 10 posts and is not overused.

---

## Uniqueness audit (5-check summary)

Source: research file uniqueness audit section. Inventory last updated 2026-06-18 (306 posts).

| Check | Status | Notes |
|---|---|---|
| CHECK 1 — Title word overlap | PASS | No existing title shares 3+ consecutive meaningful words with "BigCommerce to Magento migration" |
| CHECK 2 — Slug overlap | PASS | `bigcommerce-to-magento-migration` is not a substring of any existing slug. Shares at most one word (migration) with others. "bigcommerce" + "migration" never appear together in any existing slug. |
| CHECK 3 — Primary keyword | PASS | "bigcommerce to magento migration" is not the focus keyword of any existing post |
| CHECK 4 — Angle/thesis | PASS | Migration cluster has 3 posts (Volusion→WooCommerce ID 42177, generic checklist ID 34921, generic platform migration ID 18791). None covers BigCommerce→Magento execution. Platform comparison post ID 29137 is a 4-way comparison, not a migration guide. |
| CHECK 5 — Cluster saturation | PASS | Migration cluster: 3 posts. Well below the 5-post threshold. |

**Verdict: all 5 checks pass. Topic is approved.**

**Related posts — avoid duplicating their angles:**
- ID 29137 (`ecommerce-platforms-comparison`): generic platform comparison table. Do not rehash platform pros/cons — this article is about migration execution and the decision to leave BigCommerce.
- ID 39502 (`future-proof-ecommerce-magento-2025`): "why Magento" advocacy post. Do not restate the general case for Magento — assume the reader already knows BigCommerce and is evaluating the switch.
- ID 38078 (`adobe-commerce-b2b-features`): Adobe Commerce B2B feature list. Reference B2B capabilities as migration motivation; do not exhaustively list them.
- ID 37552 (`migrate-from-magento-1-to-magento-2`): M1 to M2 migration. Different direction entirely — clarify the Magento Data Migration Tool is for M1→M2 only, not BigCommerce.

---

## Thesis

> BigCommerce's June 2026 Open Payment Provider Fee now charges B2B merchants on every purchase order, but migration to Magento is only worth it above a clear revenue and complexity threshold — this guide gives you the honest decision framework and a 7-phase execution playbook to move without losing your SEO rankings or B2B data.

---

## Why this, why now, why us

- **Why this angle:** No existing Virtina post addresses migration away from BigCommerce. The research gap is real: every competitor article on this topic was written before June 1, 2026, and none addresses the Open Payment Provider Fee that now taxes B2B purchase orders — the single most concrete migration trigger in the market right now.
- **Why now:** The June 2026 pricing overhaul is live. B2B merchants on BigCommerce are doing the math in real time. A guide that starts from that trigger (not from abstract platform-comparison theory) will capture high-intent search traffic.
- **Why this client:** Virtina is a Magento Certified partner with a migration services page at `/magento-migration-services/`. This post funnels decision-ready B2B merchants directly to Virtina's strongest service offering. The honest "when NOT to migrate" framework also positions Virtina as a trusted advisor, not a pitch machine.

---

## Audience

**Primary reader:** VP eCommerce, Director of Digital, or Head of eCommerce at a B2B manufacturer, distributor, or wholesaler currently running BigCommerce. Revenue range: $500K to $25M GMV. Likely on BigCommerce's Growth or Scale plan. Doing PO-based orders. Frustrated by the June 2026 fee announcement or hitting API/customization limits.

**What they already know:** BigCommerce's strengths, their own ERP integration pain, what a platform migration is. Do not explain basic eCommerce vocabulary.

**What they need from this article:** An honest answer to "should I actually migrate?" with real numbers, not a vendor pitch. Then, if yes, a credible execution plan with the 4 failure points called out honestly.

**Do not:** Write for someone choosing a first platform. Do not explain what Magento is at a basic level. Assume the reader can evaluate a cost table.

---

## Primary keyword and slug

- **Primary keyword:** BigCommerce to Magento migration
- **Slug:** `bigcommerce-to-magento-migration`
- **Secondary keywords to cover naturally in body prose (from semantic list in research file):**
  - eCommerce replatforming
  - Adobe Commerce Open Source
  - Magento 2 migration
  - BigCommerce transaction fees
  - 301 redirect mapping
  - purchase order (PO) payment
  - data migration tool
  - customer group pricing
  - URL structure mapping
  - Hyva theme
  - ERP integration
  - configurable product / simple SKU
  - Magento B2B module
  - hosted vs self-hosted
  - total cost of ownership (TCO)

---

## Meta title and meta description

**Meta title (Yoast `wpseo_title`):**
`BigCommerce to Magento migration guide 2026 | Virtina`
Character count: 52 — under the 60-char maximum.

**Meta description (Yoast `metadesc`, 150-160 chars):**
`BigCommerce's 2026 fee changes now tax B2B purchase orders. Honest decision framework, 7 migration phases, and SEO protection plan for moving to Magento.`
Character count: 153 — within the 150-160 target range.

---

## H1 title

`BigCommerce to Magento migration: 2026 guide`

(Sentence case, per Virtina voice rules. Drop the colon if A/B testing cleaner titles.)

---

## Full section outline (H2/H3 hierarchy)

### [Executive Summary] — structural label, verbatim
Template A block. 3-4 bullet points, no prose paragraphs. Cover: June 2026 pricing trigger, honest GMV threshold (~$500K), 7-phase structure, 4 failure points, SEO risk.

### [Introduction] — structural label, verbatim
Template B block. 2-3 short paragraphs. Open with the June 2026 fee announcement as the hook. Establish the honest thesis: migration is right for some B2B stores, wrong for others, and this guide draws that line. No preamble about "in today's eCommerce world."

### [Table of Contents] — H3, structural label per section 2
SVG-arrow TOC, Template C. Link to all 6 body H2 sections, PAA, Conclusion, and FAQ. Anchors must match body H2 ids exactly.

---

### H2 1: Why are B2B merchants leaving BigCommerce in 2026?

**First sentence must directly answer the question.** Answer: "The main reason is the June 2026 Open Payment Provider Fee, which now charges B2B merchants between 0.6% and 2% on every order processed outside BigCommerce's embedded payment list — including purchase orders."

**H3 1.1: The Open Payment Provider Fee and what it costs B2B stores**
- Detail the fee structure: Core = 2%, Growth = 1%, Scale = 0.6%
- Explain that the fee applies to PO-based orders and offline payment methods — this did not exist before June 2026
- Concrete example: a merchant doing $500K GMV on Scale pays $3,000/year in transaction fees on top of the $3,588/year plan fee
- Use the 278% plan cost increase example at $150K GMV (Plus→Scale threshold tightening)
- Source: Netalico (May 2026), Shopifreaks (April 2026)
- Keep to 2-3 short paragraphs. No em dashes. No "leverage."

**H3 1.2: The platform scale decline — what the numbers say**
- BigCommerce live stores: 36,855 as of Q2 2026, down 11% year-over-year from ~47,000 at peak
- Net loss of 214 merchants in the last tracked 90-day period (474 exits, 260 arrivals)
- Source: Storeleads Q2 2026 (high confidence)
- State this as context, not as a verdict on BigCommerce. The platform has not been abandoned — the decline matters because a shrinking merchant base affects extension ecosystem investment over time.
- Do NOT say BigCommerce is "failing" — that's hype. State the numbers and let the reader draw conclusions.

**H3 1.3: When the API and customization ceiling becomes the issue**
- BigCommerce reported limits: 20,000 API calls/hour on Core/Growth, 60,000 on Scale
- 600 variant ceiling per product
- Checkout JavaScript injection and analytics incompatibility with headless configurations
- Phrase the API limits as "reported limits" — the official docs page returned errors during research. Say "limits reported by multiple third-party sources" or "plans are documented to allow."
- Magento: constrained only by server capacity, no platform-imposed caps
- Source: BigCommerce docs (secondary confirmed), MGT Commerce 2026

---

### H2 2: Should you migrate to Magento? — the honest decision framework

**First sentence must directly answer the question.** Answer: "Migration to Magento Open Source makes financial and operational sense above roughly $500K GMV, when customization requirements exceed BigCommerce's configuration ceiling, or when your ERP integration needs direct database access."

**H3 2.1: When the migration math works in your favor**
- At $1M+ GMV: BigCommerce transaction fees compound; Magento self-hosted eliminates them permanently
- When B2B customization exceeds configuration options (multi-level approval chains, buyer-specific catalogs with 5,000+ SKUs, company account hierarchies)
- When ERP integration requires custom API work or direct database access
- When multi-store infrastructure is needed (Magento multi-store with shared backend is architecturally stronger at this scale)
- Present as a checklist: 3-4 bullet criteria the reader can score themselves

**H3 2.2: When to stay on BigCommerce**
- Below $500K GMV: Magento Year 1 TCO ($30K-$60K) makes the payback math negative
- Standard B2B workflows (company accounts, custom pricing, quote management, net terms) that BigCommerce B2B Edition already handles
- Stores that need fast time-to-market — Magento is operationally heavier
- Be direct and opinionated here. State: "If your GMV is under $500K and your B2B workflows are standard, migrating to Magento this year will cost more than it saves."
- This section is what builds trust. Do not soften or omit it.

**H3 2.3: Magento Open Source vs Adobe Commerce — which tier?**
- Magento Open Source: free to download; $30K-$60K Year 1 TCO; community extensions; no native B2B module
- Adobe Commerce: $22K-$125K+/year license; 15+ native B2B workflows (RFQ, negotiable quotes, multi-level approvals, requisition lists, company account hierarchies); built-in Page Builder and advanced analytics
- Guidance: Open Source is the right starting point for stores under $5M GMV that are migrating primarily for customization/TCO. Adobe Commerce is worth evaluating at $5M+ GMV when the B2B module capabilities replace a paid app stack.
- Source: IWD Agency 2026, Adobe Experience League (Magento 2.4.9 release notes)

---

### H2 3: What does a BigCommerce to Magento migration actually involve?

**First sentence must directly answer the question.** Answer: "A BigCommerce to Magento migration runs through 7 phases: pre-migration audit, theme build and catalog migration, integration rebuild, B2B data configuration, staging QA, DNS cutover, and post-launch monitoring."

**Important note for creator:** Clarify upfront that Adobe's Magento Data Migration Tool is designed for Magento 1 to Magento 2 only. It requires a source Magento 1 database and cannot connect to BigCommerce. This is a common misconception — name it early and clearly.

**H3 3.1: Phases 1 and 2 — audit, catalog, and theme**
- Phase 1 (2 weeks): Document every page URL, map BigCommerce app stack to Magento extension equivalents, build redirect map, audit B2B data structures
- Phase 2 (4-8 weeks, parallel): Build Magento theme (Hyva or Luma — Hyva recommended for performance); migrate catalog via tool or API scripts; transform variant data; set up hosting (PHP 8.3+, OpenSearch, Valkey/Redis, Varnish)
- Magento 2.4.9 is the current release (PHP 8.3, 8.4, 8.5 support)
- LitExtension: supports 140+ platforms, starts at $79, handles stores under 5,000 SKUs with standard product data, 60-day post-migration support
- Cart2Cart: 85+ platforms, similar pricing, better for very small stores
- For 5,000+ SKUs, complex B2B, or custom extensions: agency API-based migration is the appropriate approach — tools move data, they don't rebuild integrations or configure B2B architecture

**H3 3.2: Phases 3-7 — integrations, QA, and go-live**
- Phase 3 (2-4 weeks): Reconnect ERP, CRM, payment gateways, email platform; rebuild B2B configuration (customer groups, tier pricing, company accounts, approval workflows)
- Phase 4 (1 week): DNS switch, deploy 301 redirects at server/CDN layer, submit sitemap, set up Google Search Console monitoring, daily crawl error checks for 2 weeks post-launch
- Timeline table (from research file): small store <500 SKUs: 2-4 weeks DIY / 8-12 weeks agency; mid-market 500-5K SKUs: 4-8 weeks DIY / 12-24 weeks agency; enterprise 5K+ SKUs: not recommended DIY / 24-52+ weeks agency

---

### H2 4: What data won't migrate automatically — and why it matters

**First sentence must directly answer the question.** Answer: "Four data types cannot be migrated automatically: customer passwords, URL structure, product variants, and B2B-specific data — and each requires a different manual reconstruction strategy."

**H3 4.1: The 4 non-automatable failure points**
Prose-first, then a list. Each item is 1-2 sentences:
1. Customer passwords: incompatible hashing algorithms between BigCommerce and Magento. All customers must trigger a password reset on first login. Prepare a proactive reset email campaign for day-of-launch.
2. URL structure: BigCommerce defaults to `/products/product-name/`; Magento defaults to `/product-name.html`. Every URL must be individually mapped and 301-redirected.
3. Product variants: BigCommerce stores variants as a single row; Magento requires configurable product + child simple SKU pairs. Each row must be expanded and re-mapped. This is what makes large catalogs labor-intensive.
4. Historical orders: import as read-only records only — no functional transaction replay.

**H3 4.2: Rebuilding B2B data — the most underestimated work**
- Customer groups and tier pricing must be manually rebuilt in Magento's Customer Groups and tier pricing configuration
- Company accounts, shared catalogs, and negotiable quote histories from BigCommerce B2B Edition are not transferred by automated tools
- They require manual Magento B2B module setup
- Estimate this at 20-30% of total migration time for stores with active B2B account structures
- This is where agency expertise pays for itself — tools cannot do this work

---

### H2 5: How do you protect your SEO through the migration?

**First sentence must directly answer the question.** Answer: "You protect your SEO by building a complete URL redirect map before migration starts, deploying server-side 301 redirects on launch day, and monitoring Google Search Console daily for two weeks after cutover."

**H3 5.1: Building the URL redirect map — before day one**
- A poorly managed migration causes 15-30% organic traffic loss in the 90 days post-launch
- The map must be complete: every BigCommerce URL to its Magento equivalent — products, categories, static pages, blog posts
- Use 301s only — never 302 or 307 (302s do not pass link equity)
- No redirect chains: map A directly to C, not A→B→C (chains slow crawling and leak equity)
- Post-launch: generate and submit new XML sitemap immediately; check Search Console for crawl errors daily for 2 weeks
- Watch for structured data/schema loss — Magento requires separate schema configuration; rich snippets from BigCommerce do not transfer

**H3 5.2: AI citation preservation — the 2026 migration KPI**
- A new KPI has emerged alongside traditional organic traffic: AI citation preservation
- If your BigCommerce pages are cited by AI Overviews, Perplexity, or other AI tools, those citations are tied to specific URLs
- Migration without complete redirects breaks those AI citations, which do not auto-recover as fast as Google rankings
- Target: 95%+ of pre-migration AI citations retained within 60 days of launch
- Track this by monitoring AI search tools for brand/product mentions before and after migration
- Source: Digital Applied 2026 (AI citation KPI data)

---

### H2 6: What does migration cost and how long does it take?

**First sentence must directly answer the question.** Answer: "Agency-led migration costs $5,000-$15,000 for small stores, $20,000-$50,000 for mid-market stores, and $75,000-$250,000+ for enterprise stores with complex B2B and ERP requirements."

**H3 6.1: Timeline and investment by store size**
Use the comparison table from the research file (store size / DIY with tools / agency-led timeline + Year 1 investment). Creator should build this as a Template N comparison table.

Recap the honest math:
- Year 1 Magento Open Source TCO: $30K-$60K for small-to-mid stores
- From Year 2: ongoing costs drop to 20-40% of Year 1 (hosting, extension renewals, security patches)
- BigCommerce comparison: a merchant at $500K GMV on Scale pays $6,588/year in pure SaaS fees ($3,588 plan + $3,000 Open Payment Provider) — before extensions and development
- Break-even generally occurs in Year 2 for stores above $500K GMV, assuming the migration is executed correctly

**H3 6.2: Budget the post-launch phase**
- Allocate 20-30% of the migration project cost for the first 6 months post-launch
- Covers: performance tuning, extension configuration, B2B workflow refinement, and the inevitable edge-case bugs
- A migrated store is not a finished store on launch day — plan for it

---

### H2 7: How does Virtina run a BigCommerce to Magento migration?

**Note for creator:** This is the CTA section. Keep it 2-3 paragraphs. No H3 needed (short section). Write in second person: "When you work with Virtina..."

Key points to cover:
- Virtina is a Magento Certified partner with 1,000+ client engagements
- Migration process: pre-migration audit → phased build → staging QA → go-live → post-launch support
- Specifically handle the 4 failure points: password reset campaigns, URL mapping, variant re-mapping, B2B data rebuild
- Close with a link to Virtina's Magento migration services page

**Internal link placement:** Place the `/magento-migration-services/` link here — anchor text "Magento migration services" (noun phrase, 3 words, accurately names the destination). This is the primary conversion CTA link.

---

### [People Also Ask] — structural label, verbatim
Template H block. 4-5 questions. Each answer is 2-3 sentences max, direct-answer-first.

Suggested questions (creator picks 4-5):
1. How long does a BigCommerce to Magento migration take?
2. Will I lose my SEO rankings when I migrate from BigCommerce to Magento?
3. Can I use the Magento Data Migration Tool for BigCommerce?
4. How much does a BigCommerce to Magento migration cost?
5. What B2B data can't be migrated automatically from BigCommerce?

---

### [Conclusion] — structural label, verbatim
Template I block (background: `#00d5c0`, white text). 2 short paragraphs. No "in conclusion." No em dashes. Summarize the decision framework: if GMV is above $500K and customization needs exceed BigCommerce's ceiling, migration is the right move. Acknowledge the complexity. Close with a CTA to Virtina's migration services — do NOT repeat the same anchor text used in section 7; use a different phrase (e.g., "Virtina migration team" — 3 words, noun phrase).

**Note:** Internal links are allowed in body sections only, not in the Conclusion per MUST-FOLLOW-RULES.md section 6. Do not add links inside the Conclusion block.

---

### [FAQ] — structural label, verbatim
Template J accordion. 6-8 Q&As. Direct-answer-first for each. Cover practical questions the decision-maker has after reading the article. Suggested Q&A topics:

1. Does migrating to Magento affect my existing customer accounts?
2. What happens to my BigCommerce integrations (ERP, payment, shipping)?
3. Should I choose Magento Open Source or Adobe Commerce?
4. Is Magento harder to manage than BigCommerce day-to-day?
5. What is the Hyva theme and why is it recommended?
6. Can I migrate product reviews and customer wishlists?
7. How do I handle the B2B pricing structures I've built in BigCommerce?
8. When should I NOT migrate from BigCommerce to Magento?

---

## Internal link targets (5-10 links required, body sections only)

| Destination | Suggested anchor text | Section to place in |
|---|---|---|
| `/magento-migration-services/` (Virtina service page) | `Magento migration services` | Section 7 (Virtina CTA) |
| `ecommerce-platforms-comparison` (ID 29137) | `eCommerce platform comparison` | Section 2 (decision framework) |
| `magento-for-b2b-ecommerce` (ID 20229) | `Magento for B2B` | Section 2.3 (Adobe Commerce vs Open Source) |
| `adobe-commerce-b2b-features` (ID 38078) | `Adobe Commerce B2B features` | Section 3.2 (Magento B2B module) |
| `ecommerce-website-migration-checklist` (ID 34921) | `eCommerce migration checklist` | Section 3 (what migration involves) |
| `ecommerce-platform-migration` (ID 18791) | `platform migration planning` | Section 3 (phases intro) |
| `future-proof-ecommerce-magento-2025` (ID 39502) | `Magento for long-term growth` | Section 2.1 (when migration works) |

**Anchor text rules confirmed:** All anchors are 2-5 words, clean noun phrases, no leading articles, no gerunds, no setup words. All accurately name the destination's actual topic.

**External link maximum: 2.** If the creator needs to reference a source in-text, use at most 2 external links. Strip all others to plain text. Never link to competitor domains (bigcommerce.com, shopify.com, etc.).

---

## Stats to use — with confidence levels

| Stat | Value | Confidence | How to phrase it |
|---|---|---|---|
| BigCommerce live stores, Q2 2026 | 36,855 | High | State directly |
| BigCommerce YoY decline | -11% | High | State directly |
| Open Payment Provider Fee, Core plan | 2% | High | State directly |
| Open Payment Provider Fee, Growth plan | 1% | High | State directly |
| Open Payment Provider Fee, Scale plan | 0.6% | High | State directly |
| $500K GMV = $3,000/year in PO fees on Scale | $3,000 | High | State with calculation context |
| Plan cost increase example ($150K GMV, Plus→Scale) | 278% | High | Use as illustration, not as a general claim |
| Magento Open Source current version | 2.4.9 | High | State directly |
| Magento 2.4.9 PHP support | 8.3, 8.4, 8.5 | High | State directly |
| Year 1 Magento Open Source TCO | $30K-$60K | Medium | Phrase as "typically runs $30,000-$60,000" |
| Post-migration traffic drop (poor redirects) | 15-30% in 90 days | Medium | Phrase as "studies document" or "documented across migrations" |
| LitExtension starting price | $79 | High | State directly |
| Agency migration cost: small | $5K-$15K | Medium | Present as ranges, not fixed prices |
| Agency migration cost: mid-market | $20K-$50K | Medium | Same |
| Agency migration cost: enterprise | $75K-$250K+ | Medium | Same |
| BigCommerce API rate limits (Core/Growth) | 20,000 calls/hr | Medium | Phrase as "reported limits" — official docs page returned 404; confirmed via secondary sources |

---

## Stats to OMIT — do not use in the draft

| Stat | Why |
|---|---|
| "98% backlink equity preserved with correct 301s" | Single-source unverified (digitalapplied.com only). No independent corroboration. Remove. |
| "523 days to recover traffic after a poorly managed migration" | Single-source unverified, suspiciously specific, no methodology shown. Remove. |

---

## Stats to phrase softly

| Stat | Required phrasing |
|---|---|
| BigCommerce API rate limits (20,000/60,000 calls/hr) | "Reported API rate limits" or "limits documented by third-party sources" — do NOT say "official BigCommerce documentation states" |

---

## Image plan note

Per Virtina image rules (MUST-FOLLOW-RULES.md section 3, feedback_virtina_image_rules.md):
- 1 featured image: 1309×500 px, JPEG quality 82, under 200 KB, real WordPress media ID
- 2-3 body images: 670×352 px each, JPEG quality 82, under 200 KB, all same dimensions
- All images must show business/office/eCommerce scenes — no nature, landscapes, or generic stock
- Suggested search terms for this topic: "ecommerce dashboard laptop," "office team meeting computers," "business professional desk," "warehouse worker inventory"
- Final image selection and upload is the user's call at publish time — the creator should mark image placement in the draft with `[IMAGE: description]` placeholders at appropriate section breaks
- Images go INSIDE body section divs, not between sections

---

## Mandatory content element checklist (section 4b)

This is a "how-to / phased guide" article type:
- [ ] Comparison table (migration cost and timeline by store size) — Template N
- [ ] Decision checklist (when to migrate vs stay) — bullet format Template F
- [ ] FAQ section 6-8 Q&As — Template J
- [ ] LLM extractability check: the article must be self-contained. An AI should be able to answer "should I migrate from BigCommerce to Magento?" from this article alone.

---

## What NOT to do

- Do not write a generic platform comparison. ID 29137 already covers 4-way platform comparison. This post is about one specific migration path.
- Do not write a vendor pitch. The "when to stay on BigCommerce" section is mandatory and must be honest. Omitting it or softening it damages Virtina's credibility.
- Do not cite the "98% backlink equity" or "523 days recovery" stats under any circumstances.
- Do not say the Magento Data Migration Tool can be used for BigCommerce. It cannot. Clarify this early.
- Do not phrase API limits as "officially stated" — the docs page 404'd. Use "reported" or "documented by third-party sources."
- Do not invent a case study. If referencing Virtina client work, use "stores we've moved from BigCommerce" without fabricated specifics, or leave a `[CASE STUDY: insert real client data]` placeholder.
- Do not use em dashes anywhere — this is a hard Virtina rule. Use commas, colons, or periods instead.
- Do not use banned words: revolutionary, game-changing, cutting-edge, best-in-class, leverage, delve, navigate (as verb), realm, landscape, ecosystem, "in today's fast-paced world."
- Do not use Title Case on headings — sentence case only.
- Do not link to bigcommerce.com or any competitor domain.
- Do not add a byline with a fictional author name. Use brand voice ("we") or leave a `[BYLINE: insert real author name]` placeholder.
- Do not place internal links in the Introduction or Conclusion blocks — body sections only.
- Prose for reasoning and analysis; bullets only for genuinely list-shaped content (criteria, phases, checklists). Do not bullet-stuff explanatory paragraphs.

---

## Headline direction

Sentence case throughout, per Virtina rules.

Working title (for reference):
`BigCommerce to Magento migration: 2026 guide`

Three iteration options for the creator:
1. `BigCommerce to Magento migration: 2026 guide` (direct, keyword-first)
2. `Migrating from BigCommerce to Magento in 2026: an honest B2B decision guide`
3. `Should you migrate from BigCommerce to Magento in 2026?` (Format D question-style)

The creator should pick one and confirm with user before drafting if in doubt. Option 1 is the default.

---

## Word count target

- Minimum: 2,000 words
- Target: 2,200-2,500 words (standard Virtina range; this is not a pillar guide)
- The comparison table and decision checklist count toward word count but the creator must not pad prose to hit the target — cut thin sections before adding filler

---

## Open questions for the creator

- Does Virtina have a live `virtina.com/magento-migration-services/` URL? Confirm before linking. If the URL is different or does not exist, ask the user for the correct CTA destination.
- Is there a real BigCommerce→Magento client case study the user can provide? If yes, insert it in section 7 (Virtina CTA section) with specific numbers. If not, use placeholder.
- Should the article cover Magento 1 to Magento 2 migration at all (as a contrast to BigCommerce→Magento)? The recommendation is: one sentence clarifying the Magento Data Migration Tool is M1→M2 only, then move on. Do not expand.
