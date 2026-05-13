---
title: Research — Volusion to WooCommerce migration
client: virtina
date: 2026-05-11
topic: Volusion to WooCommerce migration
audience: Volusion merchants frustrated with platform limits, considering migration
stage: research
slug: volusion-to-woocommerce-migration
---

# Research: Volusion to WooCommerce migration

## Sub-questions

A reader (Volusion merchant) would want to know:

1. What are the real, specific frustrations that make Volusion merchants want to leave?
2. What pushed others to finally pull the trigger and migrate?
3. What does the migration actually involve — what moves cleanly, what breaks?
4. What do you actually gain on WooCommerce that you couldn't have on Volusion?
5. What are the honest risks and downsides of switching to WooCommerce?
6. How big is the problem — is Volusion actually dying?
7. What do other merchants ask when they're at this decision point?

---

## Key findings

### Finding 1: Volusion's active store count has collapsed 75% since 2020

Volusion peaked at approximately 13,889 active stores in Q1 2020. By Q1 2026 it had fallen to 3,526 stores — a 75% contraction over six years. The year-over-year rate in Q1 2026 was -20%. In a 90-day window, the platform gained 2 stores from competitors while losing 40 — a 20-to-1 defection ratio. This is not a platform in slow decline; it is one in accelerating collapse.

- Source: [The State of Volusion in 2026](https://storeleads.app/reports/volusion) — StoreLeads, May 2026 (primary, tracked data)
- Why it matters: The "is Volusion dying?" question has a data answer. The before-and-after narrative can open with this momentum and use it as the tipping-point evidence.

### Finding 2: Annual sales caps create a pricing trap that triggers forced upgrades

Volusion's pricing structure caps annual sales per plan tier: $50K on Personal ($35/mo), $100K on Professional ($79/mo), $500K on Business ($299/mo). When a merchant exceeds the cap, Volusion automatically upgrades the account — no notification required. Merchants report bills jumping from $35 to $79 overnight, and others describe charges increasing by "600% in 3 weeks" without consent. One merchant reported revenue was withheld, causing layoffs; another lost $80,000 held in their Volusion account during an account dispute.

- Source: [Volusion PissedConsumer Reviews](https://volusion.pissedconsumer.com/review.html) — PissedConsumer (primary, merchant-reported)
- Source: [Volusion Review: 17% Store Drop](https://steva.co/volusion-review/) — Steva, 2025 (secondary)
- Why it matters: The pricing trap is the most emotionally charged tipping point for small-to-mid merchants. It gives the narrative a concrete financial antagonist.

### Finding 3: The platform has ~80 integrations vs. WooCommerce's access to 60,000+ WordPress plugins

Volusion's app marketplace holds approximately 80 apps. One Capterra reviewer described the API as "an absolute disaster" and noted that no agency will build on it because the API is proprietary. Native Amazon and eBay integrations are actively warned against by experienced users. WooCommerce, as a WordPress plugin, gives access to 60,000+ WordPress plugins plus 1,100+ official WooCommerce extensions, including dedicated B2B tools (B2BKing, WholesaleX, Wholesale Suite) that support tiered pricing, role-based catalogs, quote workflows, and wholesale registration — none of which exist natively in Volusion.

- Source: [Volusion Reviews - Capterra](https://www.capterra.com/p/32398/Volusion-eCommerce/reviews/) — Capterra (primary, merchant-reported)
- Source: [WooCommerce B2B Plugins](https://woocommerce.com/products/b2b-for-woocommerce/) — WooCommerce official marketplace
- Why it matters: Integration gaps are the core growth ceiling for merchants scaling into B2B. This contrast is the strongest functional argument for migration.

### Finding 4: Volusion's SEO architecture has structural problems that hurt rankings

Multiple sources confirm: Volusion uses URL structures that break canonical best practices, has inconsistent H1 usage, paginated content that confuses crawlers, and limited support for schema markup beyond basic product and store types. One case study cited a firearms merchant losing all Google Shopping visibility because Volusion's structure didn't support required schema. The platform has no built-in blogging, which eliminates content-driven SEO entirely. WooCommerce, running on WordPress — the platform that powers 43% of all websites — has full schema markup control via plugins like Yoast, RankMath, and Schema Pro.

- Source: [Volusion Migration in 2026](https://www.optimum7.com/blog/volusion-complaints-issues-negative-reviews-and-new-pricing.html) — Optimum7, 2026 (secondary with primary case study data)
- Source: [Schema.org Markup in Volusion](https://helpcenter.volusion.com/en/articles/424637-schema-org-markup-in-volusion) — Volusion official docs (primary)
- Why it matters: SEO is a critical revenue lever for ecommerce. A platform that limits your SEO ceiling is directly limiting revenue.

### Finding 5: The migration process has seven phases — and two steps where most merchants get hurt

The migration sequence is: (1) back up Volusion data via admin Data Management export; (2) install WordPress and WooCommerce; (3) export Volusion products/customers/orders as CSV; (4) map fields between platforms; (5) run test migration on a subset; (6) execute full migration; (7) post-migration cleanup and 301 redirect setup.

What migrates cleanly: product titles, descriptions, prices, customer accounts, order history, product categories, basic meta data.

What requires manual work or breaks: custom product fields without WooCommerce equivalents, payment gateway reconfiguration, tax and shipping rule rebuilds, store design (zero theme migration — must be rebuilt), complex URL redirects (Volusion and WooCommerce use different URL structures by default; without a proper 301 map, Google treats new URLs as new pages and rankings drop). WooCommerce requires an SEO plugin (Yoast, RankMath) to handle meta data at all — meta fields don't exist natively.

Timeline: small-to-mid stores typically 1-3 weeks; larger stores with custom features 4-8 weeks. Automated tools (LitExtension, Cart2Cart) handle data transfer starting around $69 for basic migrations, but do not handle theme rebuild, redirect mapping, or SEO configuration.

- Source: [Volusion to WooCommerce Migration - LitExtension](https://litextension.com/woocommerce-migration-tool/volusion-to-woocommerce.html) — LitExtension (secondary)
- Source: [How to Migrate Volusion to WooCommerce - Convesio](https://convesio.com/knowledgebase/article/how-to-migrate-volusion-to-woocommerce-a-step-by-step-guide/) — Convesio (secondary)
- Source: [Volusion to WooCommerce Migration Guide - Power Commerce](https://powercommerce.com/blogs/guides/volusion-to-woocommerce-migration-guide-power-commerce) — Power Commerce (secondary)
- Why it matters: The article's "what the switch actually looks like" section needs this specificity to earn trust from readers who've already read vague "just migrate" content.

### Finding 6: WooCommerce gives full data and code ownership — Volusion does not

On Volusion, all data lives on Volusion's servers. The company can lock accounts, freeze funds, and shut down stores without merchant consent — as documented in multiple PissedConsumer reports. Merchants are "partial owners" of their store. On WooCommerce, the merchant owns the WordPress installation, the database, and all customer and order data. They choose the host, they control backups, and no third party can lock them out. This is not a hypothetical advantage: the 2019 Volusion security breach compromised 239,000 credit card records across 6,589 stores, with estimated damages of $133.89 million, and the 2020 bankruptcy raised real questions about platform continuity that some merchants are still processing.

- Source: [Is Volusion Still a Reliable E-Commerce Platform?](https://www.cardpaymentoptions.com/credit-card-processors/volusion/) — Card Payment Options (secondary)
- Source: [WooCommerce vs Volusion - Cloudways](https://www.cloudways.com/blog/woocommerce-vs-volusion/) — Cloudways (secondary)
- Why it matters: Ownership and business continuity risk are underweighted in most migration articles. This is a real differentiator, especially for merchants who lived through the 2020 bankruptcy scare.

### Finding 7: WooCommerce's honest downsides are real and need to be stated plainly

WooCommerce is self-hosted. That means the merchant (or their agency) is responsible for: hosting selection and management, plugin updates and compatibility, performance tuning (WooCommerce can become slow under high traffic if not properly cached and configured), security hardening, and database optimization. Approximately 4.5 million WooCommerce stores rely heavily on third-party plugins for essential features, creating ongoing maintenance burdens. Each additional plugin introduces potential compatibility conflicts. Scaling WooCommerce involves both hardware upgrades and software/database optimization — it is not "set and forget" the way a SaaS platform is.

- Source: [5 reasons why you should not use WooCommerce - SapientPro](https://sapient.pro/blog/disadvantages-woocommerce) — SapientPro (secondary)
- Source: [16 WooCommerce Migration Statistics for 2025 - Swell](https://www.swell.is/content/woocommerce-migration-statistics) — Swell (secondary, note: Swell is a competing platform, treat with appropriate skepticism)
- Why it matters: The article must give honest warnings or it will read as a Virtina sales pitch. Honest warnings build credibility and address the reader's real fears.

### Finding 8: Product variants in Volusion are a friction point merchants specifically call out

Volusion's variant system requires merchants to create "global options" and then assign them individually to each product. Pricing variations display as "(+/-)$0.00" rather than final prices, causing customer checkout confusion. A Reddit user cited a specific blocker: QuickBooks integration only works with simple products, not variants — a common mid-market dealbreaker. Variants with multiple option types (size + color simultaneously) are "difficult to create." This is not a cosmetic limitation: for apparel, accessories, or any SKU-intensive business, this is a direct revenue constraint.

- Source: [Volusion Reviews - Capterra](https://www.capterra.com/p/32398/Volusion-eCommerce/reviews/) — Capterra (primary, merchant-reported)
- Why it matters: Variants and SKU management are a specific, named pain point in the brief. This gives the article a concrete example with emotional detail.

---

## Data points table

| Stat | Value | Source | Date |
|------|-------|--------|------|
| Volusion active stores | 3,526 | [StoreLeads](https://storeleads.app/reports/volusion) | May 2026 |
| Volusion active stores at peak | 13,889 | [StoreLeads](https://storeleads.app/reports/volusion) | Q1 2020 |
| Volusion YoY store decline rate | -20% | [StoreLeads](https://storeleads.app/reports/volusion) | Q1 2026 |
| Volusion 90-day defection ratio | 40 lost : 2 gained | [StoreLeads](https://storeleads.app/reports/volusion) | Q1 2026 |
| Volusion platform satisfaction rating | 1.7 / 5 | [Steva Review](https://steva.co/volusion-review/) | 2025 |
| Volusion G2 rating | 3.4 / 5 | [G2 via search](https://www.g2.com/products/volusion/reviews) | 2026 |
| Volusion app marketplace | ~80 apps | [Steva Review](https://steva.co/volusion-review/) | 2025 |
| WooCommerce active stores globally | ~4.65 million | [Shoptrial](https://www.shoptrial.co/woocommerce-statistics/) | Q2 2025 |
| WooCommerce market share (all ecommerce sites) | 33.4% | [StoreLeads WooCommerce](https://storeleads.app/reports/woocommerce) | Aug 2025 |
| WooCommerce YoY change | -3.2% | [Shoptrial](https://www.shoptrial.co/woocommerce-statistics/) | 2025 |
| WordPress plugins total | 60,000+ | [THE.Hosting](https://the.hosting/en/help/why-people-choose-wordpress-open-source-60000-plugins-and-scalability) | 2024 |
| WooCommerce official extensions | 1,100+ | [Cloudways](https://www.cloudways.com/blog/woocommerce-vs-volusion/) | 2024 |
| Volusion 2019 breach: cards stolen | 239,000 | [Steva Review](https://steva.co/volusion-review/) | 2019 |
| Volusion 2019 breach: stores affected | 6,589 | [Steva Review](https://steva.co/volusion-review/) | 2019 |
| Volusion 2019 breach: estimated damages | $133.89 million | [Steva Review](https://steva.co/volusion-review/) | 2019 |
| Volusion Personal plan sales cap | $50,000/year | [LitExtension](https://litextension.com/blog/volusion-review/) | 2024 |
| Volusion Professional plan sales cap | $100,000/year | [LitExtension](https://litextension.com/blog/volusion-review/) | 2024 |
| Volusion Business plan sales cap | $500,000/year | [LitExtension](https://litextension.com/blog/volusion-review/) | 2024 |
| Volusion gateway maintenance fee (Personal) | 1.25% | [Volusion official](https://helpcenter.volusion.com/en/articles/446796-behind-the-scenes-credit-card-payment-processing) | current |
| Volusion gateway maintenance fee (Business) | 0.35% | [Volusion official](https://helpcenter.volusion.com/en/articles/446796-behind-the-scenes-credit-card-payment-processing) | current |
| Volusion bandwidth overage charge | $7.00/GB | [Volusion help center](https://helpcenter.volusion.com/run-your-business/store-management-101/bandwidth-overages-things-to-know) | current |
| Migration timeline (small-mid store) | 1–3 weeks | [LitExtension](https://litextension.com/woocommerce-migration-tool/volusion-to-woocommerce.html) | 2024 |
| Migration timeline (large/complex store) | 4–8 weeks | [LitExtension](https://litextension.com/woocommerce-migration-tool/volusion-to-woocommerce.html) | 2024 |
| Basic automated migration tool cost | ~$69 | Cart2Cart (via search) | 2024 |
| Volusion free theme library | ~24 themes | [LitExtension Volusion Review](https://litextension.com/blog/volusion-review/) | 2024 |

---

## Migration process steps (in order)

These are the actual steps a Volusion-to-WooCommerce migration involves. The article should walk the reader through these, not as a checklist, but as a narrative they can picture themselves doing:

**Phase 1 — Pre-migration prep (1-3 days)**
- Export all Volusion data: products, customers, orders via Admin > Data Management > Export (CSV format)
- Document all existing Volusion URLs (products, categories, CMS pages) — this list becomes your redirect map
- Screenshot or export all active SEO meta titles and descriptions (Volusion stores these in product/category fields)
- Note all installed Volusion integrations — each will need a WooCommerce equivalent identified

**Phase 2 — WooCommerce environment setup (1-2 days)**
- Procure managed WordPress hosting (WP Engine, Kinsta, Cloudways, SiteGround — hosting choice matters for performance)
- Install WordPress, install and configure WooCommerce plugin
- Install SEO plugin (Yoast or RankMath) — required because WooCommerce has no native meta field management
- Install redirect manager plugin (Redirection or Yoast Premium) before any content goes live

**Phase 3 — Data migration (1-5 days depending on catalog size)**
- Run test migration on a data subset using a migration tool (LitExtension or Cart2Cart)
- Review test results: product titles, prices, variants, customer records, order history
- Fix field mapping mismatches before full run
- Execute full migration; confirm product count, order count, customer count match Volusion export totals

**Phase 4 — What does NOT migrate automatically (requires manual work)**
- Store theme/design: must be rebuilt from scratch in WordPress/WooCommerce — no design carries over
- Payment gateway setup: must be reconfigured (Stripe, PayPal, etc. require new API key entry)
- Tax rules: must be rebuilt (Volusion and WooCommerce handle tax configuration differently)
- Shipping zones and rules: must be rebuilt
- Complex custom fields: any Volusion-specific product fields without WooCommerce equivalents are dropped
- Product images: may require regeneration if CDN or file path issues occur during transfer
- SEO meta data: migrates as raw data but requires SEO plugin to render correctly

**Phase 5 — SEO preservation (critical, often underweighted)**
- Map every old Volusion URL to its new WooCommerce equivalent
- Volusion default URL structure: `/product-name` or `/category/product-name`
- WooCommerce default URL structure: `/product/product-name` or `/shop/product-name`
- Every changed URL needs a 301 redirect; missing redirects = Google treats pages as new = traffic drop
- Submit new XML sitemap to Google Search Console
- Monitor Google Search Console for crawl errors in 4-6 weeks post-launch

**Phase 6 — Integration rebuild**
- Identify WooCommerce equivalents for each Volusion integration
- Payment gateways: most major gateways (Stripe, PayPal, Square, Authorize.net) have official WooCommerce extensions
- Email marketing: Klaviyo, Mailchimp, and most major ESPs have official WooCommerce plugins
- ERP/accounting: QuickBooks, Xero, NetSuite all have WooCommerce connectors
- B2B-specific: evaluate B2BKing, WholesaleX, or B2B for WooCommerce for wholesale/tiered pricing needs

**Phase 7 — Testing and launch**
- Full checkout flow test on staging environment
- Mobile-friendly test (Google Mobile-Friendly Test)
- Page speed benchmark (Pingdom or GTmetrix)
- Verify all 301 redirects resolve correctly
- Check all product images load
- Confirm order confirmation emails send correctly
- DNS cutover from Volusion hosting to new WooCommerce hosting

---

## Merchant pain point quotes (paraphrased from primary review sources)

These paraphrases preserve merchant voice without exceeding the 15-word quote rule. Use these for the "before" half of the narrative:

- On the API: described by one Capterra reviewer as "an absolute disaster" with no agencies willing to build on it
- On technology pace: "It's like working on a platform that hasn't been updated since the early 2000's" (Capterra)
- On pricing shock: charges that "just kept skyrocketing" due to usage overages
- On support access: no way to reach a live person after phone support was eliminated
- On variant pricing: customer confusion from "(+/-)" pricing display instead of final prices
- On billing practices: plan upgrades executed without notification or consent
- On growth ceiling: hitting the $50K annual sales cap and facing an automatic jump to the next tier

---

## Common PAA / search questions this article should address

Based on search patterns and what migration service pages use as FAQs:

1. Is it worth migrating from Volusion to WooCommerce?
2. How long does it take to migrate from Volusion to WooCommerce?
3. Will I lose my SEO rankings if I migrate from Volusion?
4. What data can I take with me when I leave Volusion?
5. Do I need a developer to migrate from Volusion to WooCommerce?
6. Is WooCommerce free compared to Volusion?
7. What are the risks of migrating from Volusion to WooCommerce?
8. Can I keep my Volusion store running while I migrate?
9. What happens to my order history and customer accounts?
10. How do I handle Volusion's payment processing after migration?

---

## Conflicts and disagreements between sources

**On WooCommerce market share:**
- StoreLeads (Aug 2025) reports 33.4% share of tracked ecommerce sites
- BuiltWith reports 18.2% share among top 1 million ecommerce sites
- Some aggregators cite 38.76%
- **Resolution:** Different methodologies (all sites vs. top-traffic sites). For this article, use the StoreLeads 33.4% figure as most current and methodology-transparent.

**On WooCommerce year-over-year trend:**
- Swell (competitor platform) reports -3.2% YoY decline in 2025
- StoreLeads reports continued large absolute store count (4.65M+)
- **Resolution:** WooCommerce is declining slightly from peak while still being the dominant open-source ecommerce platform by a wide margin. Flag Swell as a competitor source with potential bias — use with appropriate hedging. The -3.2% figure is [unverified as neutral-source data].

**On Volusion 2024 store count:**
- StoreLeads (2026 data) shows 3,526 stores currently
- LitExtension (2024 review) cites "approximately 5,000 active stores"
- **Resolution:** StoreLeads is live tracked data, more current. Use 3,526 for 2026 articles. The discrepancy reflects continued decline between 2024 and 2026 reporting.

---

## Competitive scan — what existing articles cover and what they miss

1. **Optimum7 "Volusion Migration in 2026"** — Covers complaints broadly, has good technical depth on SEO problems. Angle: "here are the problems." Gap: no merchant narrative, no honest downsides of WooCommerce, no before/after story structure.

2. **Power Commerce Volusion-to-WooCommerce Migration Guide** — Step-by-step technical checklist. Angle: "here is the process." Gap: zero cost or timeline estimates, no SEO redirect specifics, reads like a service page not an editorial.

3. **LitExtension Volusion vs WooCommerce** — Thorough comparison table format. Angle: feature-by-feature comparison. Gap: written for a reader who hasn't decided yet, not one who is already on Volusion and frustrated.

4. **Convesio Volusion to WooCommerce guide** — Basic migration steps. Gap: no SEO guidance, no honest warnings, missing the "what breaks" discussion entirely.

5. **ebizondigital Ultimate Guide** — Could not fetch full content (truncated).

**The gap that exists across all competing articles:**
None of them are written from the perspective of the Volusion merchant who is already frustrated. They are all written from the outside looking in — clinical, checklist-driven, neutral. None give the merchant permission to feel what they're feeling (trapped by pricing, frustrated by the API, spooked by the bankruptcy) before walking them through what happens next. The "you are not crazy for wanting to leave" framing is completely absent. The honest WooCommerce downsides section is also completely absent from articles written by WooCommerce migration services (obvious commercial bias).

---

## The gap

> Every existing Volusion-to-WooCommerce article talks at merchants from the outside. None of them start where the merchant actually is: frustrated, behind on features, possibly spooked by a billing surprise or the 2020 bankruptcy, and uncertain whether the complexity of WooCommerce is worth it. The gap is a narrative that validates the merchant's experience first, then walks them honestly through both the gains and the real costs of switching.

---

## Recommended angle

> A story-driven before-and-after (Format F) that starts inside the Volusion merchant's specific frustrations — pricing traps, integration dead ends, and the SEO ceiling — then walks through what the migration actually involves step-by-step, and lands on an honest account of what WooCommerce gives you and what it will demand of you.

---

## What I could not find / gaps in available data

1. **Volusion-to-WooCommerce migration case studies with specific numbers (revenue change, organic traffic change, conversion rate change post-migration):** No primary case study data with measurable outcomes is publicly available from Virtina or competitors. Virtina's own client work would be the source — the creator agent should note that if Virtina has internal case study data, it should be pulled in at draft stage. Without it, the article uses the format of a "composite merchant journey" rather than a named client story.

2. **Exact Volusion product variant/SKU limits by plan:** The specific maximum number of product variants Volusion supports is not clearly published in their documentation. The constraint is more architectural (the global options workflow) than a hard numeric cap. [unverified whether numeric SKU limit exists at plan level].

3. **Post-migration SEO recovery timeline (traffic impact duration):** No neutral-source data found on how long it typically takes for organic traffic to recover after a properly executed Volusion-to-WooCommerce migration with 301 redirects in place. General ecommerce migration SEO recovery literature suggests 3-6 months for stabilization, but this is not Volusion-specific.

4. **Volusion pricing history — when exactly plan structure changed post-bankruptcy:** The PissedConsumer reviews reference significant pricing changes but the exact dates of post-bankruptcy plan restructuring are not clearly documented in publicly available sources.

5. **Current Volusion support tier details (what you actually get on each plan):** Support access appears to have degraded significantly post-2020 but the current official support model by plan is not clearly documented in reviewed sources.

---

## Sources

Full list:

- [The State of Volusion in 2026](https://storeleads.app/reports/volusion) — StoreLeads, May 2026 (primary tracked data)
- [Volusion Migration in 2026](https://www.optimum7.com/blog/volusion-complaints-issues-negative-reviews-and-new-pricing.html) — Optimum7, 2026 (secondary)
- [Volusion Reviews — PissedConsumer](https://volusion.pissedconsumer.com/review.html) — PissedConsumer (primary, merchant-reported)
- [Volusion Reviews — Capterra](https://www.capterra.com/p/32398/Volusion-eCommerce/reviews/) — Capterra (primary, merchant-reported)
- [Volusion Review: 17% Store Drop](https://steva.co/volusion-review/) — Steva, 2025 (secondary)
- [Volusion Review — LitExtension](https://litextension.com/blog/volusion-review/) — LitExtension, 2026 (secondary)
- [Volusion to WooCommerce Migration — LitExtension](https://litextension.com/woocommerce-migration-tool/volusion-to-woocommerce.html) — LitExtension (secondary)
- [How to Migrate Volusion to WooCommerce — Convesio](https://convesio.com/knowledgebase/article/how-to-migrate-volusion-to-woocommerce-a-step-by-step-guide/) — Convesio (secondary)
- [Volusion to WooCommerce Migration Guide — Power Commerce](https://powercommerce.com/blogs/guides/volusion-to-woocommerce-migration-guide-power-commerce) — Power Commerce (secondary)
- [Volusion to WooCommerce Migration — Shopping Cart Migration](https://www.shopping-cart-migration.com/shopping-cart-migration-options/4925-volusion-to-woocommerce-migration) — Shopping Cart Migration (secondary)
- [WooCommerce vs Volusion — Cloudways](https://www.cloudways.com/blog/woocommerce-vs-volusion/) — Cloudways (secondary)
- [Volusion vs WooCommerce — LitExtension comparison](https://litextension.com/blog/volusion-vs-woocommerce/) — LitExtension (secondary)
- [Is Volusion Still Reliable?](https://www.cardpaymentoptions.com/credit-card-processors/volusion/) — Card Payment Options (secondary)
- [WooCommerce B2B Plugin](https://woocommerce.com/products/b2b-for-woocommerce/) — WooCommerce official (primary)
- [WooCommerce Wholesale for WooCommerce](https://woocommerce.com/products/wholesale-for-woocommerce/) — WooCommerce official (primary)
- [Schema.org Markup in Volusion](https://helpcenter.volusion.com/en/articles/424637-schema-org-markup-in-volusion) — Volusion official help center (primary)
- [Volusion Bandwidth Overages](https://helpcenter.volusion.com/run-your-business/store-management-101/bandwidth-overages-things-to-know) — Volusion official help center (primary)
- [Volusion Payment Processing Fees](https://helpcenter.volusion.com/en/articles/446796-behind-the-scenes-credit-card-payment-processing) — Volusion official (primary)
- [WooCommerce Statistics 2025](https://www.shoptrial.co/woocommerce-statistics/) — Shoptrial (secondary)
- [The State of WooCommerce in 2026](https://storeleads.app/reports/woocommerce) — StoreLeads (primary tracked data)
- [5 Reasons Not to Use WooCommerce — SapientPro](https://sapient.pro/blog/disadvantages-woocommerce) — SapientPro (secondary)
- [16 WooCommerce Migration Statistics — Swell](https://www.swell.is/content/woocommerce-migration-statistics) — Swell (secondary; Swell is a competing ecommerce platform — treat data with skepticism)
- [WooCommerce Migration — Pressable](https://pressable.com/blog/woocommerce-migration-avoid-downtime-and-data-loss/) — Pressable (secondary)
- [Open Source, 60000 Plugins — THE.Hosting](https://the.hosting/en/help/why-people-choose-wordpress-open-source-60000-plugins-and-scalability) — THE.Hosting (secondary)
