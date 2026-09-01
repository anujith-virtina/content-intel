---
title: "BigCommerce to Magento migration: 2026 guide"
client: virtina
date: 2026-07-07
slug: bigcommerce-to-magento-migration
stage: draft
format: "Format D: Decision-tree / Playbook"
brief: clients/virtina/output/briefs/bigcommerce-to-magento-migration-2026-07-07.md
research: clients/virtina/output/research/bigcommerce-to-magento-migration-2026-07-07.md
word_count: ~2380
yoast_title: "BigCommerce to Magento migration guide 2026 | Virtina"
yoast_metadesc: "BigCommerce's 2026 fee changes now tax B2B purchase orders. Honest decision framework, 7 migration phases, and SEO protection plan for moving to Magento."
headlines:
  - "BigCommerce to Magento migration: 2026 guide"
  - "Migrating from BigCommerce to Magento in 2026: an honest B2B decision guide"
  - "Should you migrate from BigCommerce to Magento in 2026?"
byline: "[BYLINE: insert real author name]"
---

[FEATURED IMAGE: B2B ecommerce professional reviewing migration dashboard on laptop in modern office | concept: A business professional at a clean desk reviewing a platform analytics dashboard on a laptop, office environment, representing strategic eCommerce platform migration planning]

# BigCommerce to Magento migration: 2026 guide

[BYLINE: insert real author name] | eCommerce Migration | Updated July 2026

---

## Executive summary

- BigCommerce's June 2026 Open Payment Provider Fee now charges B2B merchants between 0.6% and 2% on every order processed outside BigCommerce's embedded payment list, including purchase orders. A store doing $500K GMV on the Scale plan now pays $3,000 per year in transaction fees on top of a $3,588 annual subscription.
- Migration to Magento Open Source makes financial and operational sense above roughly $500K GMV, when customization requirements exceed BigCommerce's configuration ceiling, or when ERP integration needs direct database access. Below $500K GMV, Magento's Year 1 total cost of ownership ($30,000-$60,000) makes the payback math negative.
- A BigCommerce to Magento migration runs through 7 phases: pre-migration audit, theme build, catalog migration, integration rebuild, B2B data configuration, staging QA, and post-launch monitoring.
- Four data types cannot be migrated automatically: customer passwords, URL structure, product variants, and B2B account data. Each requires manual reconstruction.
- The single biggest post-migration risk is SEO. Incomplete redirect mapping causes 15-30% organic traffic loss in 90 days post-launch.

---

## Introduction

BigCommerce rewrote its pricing on June 1, 2026. Every merchant processing orders outside the embedded payment list now pays a fee per transaction: 2% on Core, 1% on Growth, 0.6% on Scale. For B2B stores running purchase order-based workflows, that fee applies to every PO. It did not exist before June 2026.

That change is driving a real migration evaluation across B2B manufacturers, distributors, and wholesalers. But migration to Magento is not the right answer for every store. This guide draws that line honestly.

If your GMV is under $500K and your B2B workflows are standard, this guide will tell you to stay put. If you're above that threshold and hitting customization or API limits, it walks you through the 7 migration phases and the specific failure points that trip up most projects.

---

## Table of contents

[TOC: Template C, H3 heading]
- Why are B2B merchants leaving BigCommerce in 2026?
- Should you migrate to Magento: the honest decision framework
- What does a BigCommerce to Magento migration actually involve?
- What data won't migrate automatically, and why it matters
- How do you protect your SEO through the migration?
- What does migration cost and how long does it take?
- How does Virtina run a BigCommerce to Magento migration?
- People Also Ask
- Conclusion
- FAQ

---

[H2: Why are B2B merchants leaving BigCommerce in 2026?]

The main reason is BigCommerce's June 2026 Open Payment Provider Fee, which charges B2B merchants between 0.6% and 2% on every order processed outside BigCommerce's embedded payment list, including purchase orders.

[H3: The Open Payment Provider Fee and what it costs B2B stores]

The fee applies by plan tier: Core at 2%, Growth at 1%, and Scale at 0.6%. This is new as of June 1, 2026. Before that date, BigCommerce did not charge transaction fees on PO-based orders or offline payment methods.

The cost compounds quickly. A B2B merchant doing $500K GMV on the Scale plan now pays $3,000 per year in transaction fees, plus a $3,588 annual plan subscription: $6,588 in pure platform fees before extensions or development.

The plan restructuring also tightened GMV thresholds. A merchant at $150K annual GMV who was on the Plus plan at $79 per month moves to Scale at $299 per month. That is a 278% platform cost increase before transaction fees apply.

[H3: The platform scale decline: what the numbers say]

BigCommerce had approximately 47,000 live stores at its peak in 2022-2023. As of Q2 2026, that number stands at 36,855, an 11% year-over-year decline, per Storeleads Q2 2026 data.

In the most recent tracked 90-day period, 474 stores left BigCommerce while only 260 arrived, for a net loss of 214 merchants. The platform has reported three consecutive quarters of net customer losses at the enterprise tier.

This matters for one specific reason. A shrinking merchant base affects the breadth of available apps and extensions over time. Fewer merchants means fewer developers maintaining BigCommerce-specific integrations.

[H3: When the API and customization ceiling becomes the issue]

Beyond fees, some B2B stores hit a technical ceiling. Limits reported by third-party sources document Core and Growth plans at 20,000 API calls per hour, and Scale at 60,000. Stores running real-time ERP synchronization across large catalogs can saturate these limits during peak hours.

BigCommerce also caps product variants at 600. Merchants with configurable products (industrial equipment with spec variations, medical devices with model variants) hit this wall regardless of plan tier.

Magento Open Source has no platform-imposed API rate limits or variant ceilings. Its only constraints are server capacity, which you control.

---

[H2: Should you migrate to Magento: the honest decision framework]

Migration to Magento Open Source makes financial and operational sense above roughly $500K GMV, when customization requirements exceed BigCommerce's configuration ceiling, or when your ERP integration needs direct database access.

[H3: When the migration math works in your favor]

The clearest signal is GMV above $1M. At that scale, BigCommerce transaction fees compound year over year while Magento's self-hosted infrastructure eliminates them permanently. For a fuller analysis of why Magento pays off at this scale, see Virtina's coverage of [Magento for long-term growth](https://virtina.com/future-proof-ecommerce-magento-2025/).

Customization is the second trigger. If your store needs multi-level approval chains, buyer-specific catalogs with 5,000+ SKUs, company account hierarchies, or ERP integrations requiring direct database access, and BigCommerce's configuration options have reached a ceiling, migration is the right call.

Multi-store infrastructure is the third factor. Magento's multi-store setup with a shared backend handles different catalogs and buyer segments more cleanly than BigCommerce's multi-storefront offering at this scale.

Score yourself against these criteria:

- GMV over $500K with PO-based ordering and growing transaction fee exposure
- Customization requirements beyond what BigCommerce's app stack can configure
- ERP integration needing direct database access or a custom API architecture
- Multi-store or multi-buyer-segment catalog requirements

If you check two or more of these, migration warrants a serious evaluation. For context on where Magento sits relative to other platforms, Virtina's [eCommerce platform comparison](https://virtina.com/ecommerce-platforms-comparison/) covers the full four-way breakdown.

[H3: When to stay on BigCommerce]

If your GMV is under $500K and your B2B workflows are standard, migrating to Magento this year will cost more than it saves. That's the direct answer, not a caveat.

Magento Open Source Year 1 total cost of ownership typically runs $30,000-$60,000 for a small-to-mid store. At $500K GMV, the payback calculation comes out negative in Year 1. Stay on BigCommerce, tighten your app stack, and revisit when transaction fee exposure justifies the switch.

BigCommerce B2B Edition handles company accounts, custom pricing, quote management, net terms, and PO ordering natively. If those features cover your workflows, you don't need Magento's flexibility. Review Virtina's guide to [BigCommerce B2B Edition setup](https://virtina.com/bigcommerce-b2b-edition-setup-quick-wins/) before making any replatforming decision.

Stores that need fast time-to-market should also stay put. A mid-market migration runs 12-24 agency weeks minimum. That timeline matters.

[H3: Magento Open Source vs Adobe Commerce: which tier?]

Magento Open Source is free to download. Adobe Commerce carries a license cost of $22,000-$125,000+ per year depending on GMV tier. The question is whether the Commerce B2B module (15+ natively built workflows) is worth that license over building a comparable stack on Open Source.

For stores migrating primarily for customization and TCO, Open Source is the right starting point at under $5M GMV. Adobe Commerce is worth evaluating at $5M+ GMV when the native B2B module replaces a paid app stack you're already running on BigCommerce. See Virtina's breakdown of [Adobe Commerce B2B features](https://virtina.com/adobe-commerce-b2b-features/) for a full list of what ships natively.

For B2B operations specifically: customer group pricing, RFQ workflows, and multi-level approvals. The Adobe Commerce B2B module at scale can replace several paid BigCommerce apps at once. The economics depend on your current app spend. Virtina's [Magento for B2B](https://virtina.com/magento-for-b2b-ecommerce/) guide covers those native capabilities in detail.

---

[BODY IMAGE: eCommerce team planning B2B platform migration at office workstations with monitors displaying product data | concept: Two or three business professionals collaborating at desks with monitors showing catalog and customer data, representing B2B eCommerce replatforming strategy work]

---

[H2: What does a BigCommerce to Magento migration actually involve?]

A BigCommerce to Magento migration runs through 7 phases: pre-migration audit, theme build, catalog migration, integration rebuild, B2B data configuration, staging QA, DNS cutover, and post-launch monitoring.

One important clarification before the phases: Adobe's Magento Data Migration Tool is designed exclusively for Magento 1 to Magento 2 migrations. It requires a source Magento 1 database. It cannot connect to BigCommerce. If you've seen it suggested as an option for this route, that information is incorrect.

For BigCommerce to Magento, you have three approaches: third-party migration tools (LitExtension, Cart2Cart), manual CSV export and data transformation, or a custom API-based migration scripted by a development agency. Your catalog size and B2B complexity determine which approach fits.

A structured [eCommerce migration checklist](https://virtina.com/ecommerce-website-migration-checklist/) should be your starting document for any replatforming project: it covers pre-launch QA, redirect verification, and post-launch monitoring requirements. Virtina's [platform migration planning](https://virtina.com/ecommerce-platform-migration/) guide covers the broader strategic framework for eCommerce replatforming decisions.

[H3: Phases 1 and 2: audit, catalog, and theme]

Phase 1 is a 2-week audit. Document every page URL and map it to a Magento equivalent. Build your redirect map before writing a single line of code. Map your BigCommerce app stack to Magento extension equivalents. Missing an app replacement on launch day is one of the most common sources of post-launch chaos.

Phase 2 runs in parallel and takes 4-8 weeks. Build the Magento theme and migrate the catalog. Hyva is the recommended theme framework for performance: it generates leaner frontend output than Luma, which translates directly to better Core Web Vitals scores. Alongside the theme build, migrate catalog data via tool or API scripts, and transform variant data from BigCommerce's single-row format to Magento's configurable product and child simple SKU pairs.

Set up your hosting environment to spec: Magento 2.4.9 (the current release as of May 2026) supports PHP 8.3, 8.4, and 8.5, and requires OpenSearch 2.x, Valkey 8, and Varnish 7.6 for a production-grade environment.

For stores under 5,000 SKUs with standard product data, tools like LitExtension (starting at $79, supporting 140+ source platforms, with 60-day post-migration support) are a viable option. Cart2Cart supports 85+ platforms and suits smaller stores. For stores above 5,000 SKUs, complex B2B structures, or custom extension requirements, an agency API-based migration is the right approach. Tools move data. They don't rebuild integrations or configure B2B architecture.

[H3: Phases 3-7: integrations, QA, and go-live]

Phase 3 takes 2-4 weeks. Reconnect your ERP, CRM, payment gateways, and email platform. Each integration needs to be rebuilt to Magento's API architecture, not merely reconnected. An ERP integration that ran on a BigCommerce app must be rebuilt as a Magento extension or via a middleware connector.

Rebuild your B2B configuration in parallel: customer groups, tier pricing, company accounts, and approval workflows. This step does not exist in a tool migration. It requires manual setup in the Magento B2B module.

Phase 4 is the launch sequence. Switch DNS, deploy 301 redirects at the server or CDN layer, and submit your new XML sitemap to Google Search Console immediately. Set up daily crawl error monitoring for the first two weeks. Virtina's [eCommerce replatforming](https://virtina.com/ecommerce-replatform/) service covers the specific QA stages this phase requires.

---

[H2: What data won't migrate automatically, and why it matters]

Four data types cannot be migrated automatically: customer passwords, URL structure, product variants, and B2B-specific data. Each requires a different manual reconstruction strategy.

[H3: The 4 non-automatable failure points]

**Customer passwords**: BigCommerce and Magento use incompatible hashing algorithms. Passwords cannot be transferred. Every customer must reset their password on first login. Plan a proactive reset email campaign for launch day to minimize support volume and buyer friction.

**URL structure**: BigCommerce defaults to `/products/product-name/` paths. Magento defaults to `/product-name.html`. Every URL must be individually mapped and 301-redirected. Any URL you miss loses its search ranking and link equity.

**Product variants**: BigCommerce stores variants as a single row. Magento requires a configurable product paired with child simple SKUs. Each row must be expanded and re-mapped. This is what makes large catalogs labor-intensive and why tools struggle above 5,000 SKUs.

**Historical orders**: Import as read-only records only. No functional transaction replay is possible.

[H3: Rebuilding B2B data: the most underestimated work]

Customer groups and tier pricing must be manually rebuilt in Magento's Customer Groups and tier pricing configuration. There is no automated transfer path from BigCommerce.

Company accounts, shared catalogs, and negotiable quote histories from BigCommerce B2B Edition are not transferred by automated tools. They require full manual setup in the Magento B2B module. Budget 20-30% of total migration time for this work if your store has active B2B account structures.

This is where agency expertise pays for itself. A tool can move your product records. It cannot reconstruct your buyer hierarchy, approval rules, or customer-specific catalog visibility.

---

[BODY IMAGE: business professional working on eCommerce data migration with laptop showing product and customer records | concept: Close-up of a professional at a laptop displaying data tables with product SKUs and customer records, representing B2B catalog and account data reconstruction work]

---

[H2: How do you protect your SEO through the migration?]

You protect your SEO by building a complete URL redirect map before migration starts, deploying server-side 301 redirects on launch day, and monitoring Google Search Console daily for two weeks after cutover.

[H3: Building the URL redirect map: before day one]

A poorly managed migration causes 15-30% organic traffic loss in the 90 days post-launch. That range is documented across migrations where redirect mapping was incomplete or delayed. The fix is not complicated: it is work that cannot be skipped or deferred.

The map must cover every BigCommerce URL: products, categories, static pages, and blog posts. Use 301 redirects only. A 302 does not pass link equity. Never chain redirects: map A directly to C, not A to B to C. Chains slow crawling and dilute equity with each hop.

Watch for structured data loss. Magento requires separate schema configuration for rich snippets. Product schema, breadcrumb schema, and review markup from BigCommerce do not carry over automatically. Missing this step costs you rich snippet visibility. Virtina's [eCommerce SEO](https://virtina.com/ecommerce-seo/) team handles schema as part of migration scope.

[H3: AI citation preservation: the 2026 migration KPI]

A new performance indicator has emerged alongside organic traffic for 2026 migrations: AI citation preservation. If your BigCommerce pages are currently cited by AI Overviews, Perplexity, or similar tools, those citations are tied to specific URLs.

Migration without complete redirect coverage breaks those citations. Unlike Google rankings, AI citations do not auto-recover on a predictable timeline. Target 95% or more of pre-migration AI citations retained within 60 days of launch.

Track this by monitoring AI search outputs for your brand and product terms before migration, then again at 30 and 60 days post-launch. Add it to your monitoring checklist alongside Search Console crawl errors.

---

[BODY IMAGE: ecommerce SEO analytics dashboard showing organic traffic trends and crawl error monitoring on desktop screen | concept: A monitor displaying an analytics dashboard with traffic trend lines and a crawl error report panel, representing post-migration SEO monitoring for an eCommerce store]

---

[H2: What does migration cost and how long does it take?]

Agency-led migration costs $5,000-$15,000 for small stores, $20,000-$50,000 for mid-market stores, and $75,000-$250,000+ for enterprise stores with complex B2B and ERP requirements.

[H3: Timeline and investment by store size]

| Store size | DIY with tools | Agency timeline | Agency Year 1 cost |
|---|---|---|---|
| Small (under 500 SKUs, no custom B2B) | 2-4 weeks | 8-12 weeks | $5,000-$15,000 |
| Mid-market (500-5,000 SKUs) | 4-8 weeks | 12-24 weeks | $20,000-$50,000 |
| Enterprise (5,000+ SKUs, complex B2B/ERP) | Not recommended | 24-52+ weeks | $75,000-$250,000+ |

The honest comparison: a BigCommerce merchant at $500K GMV on Scale pays $6,588 per year in pure platform fees before extensions or development. Magento Year 1 total cost of ownership for a small-to-mid store typically runs $30,000-$60,000. Break-even generally occurs in Year 2 for stores above $500K GMV that execute the migration correctly.

From Year 2 onward, Magento ongoing costs drop to 20-40% of Year 1. Hosting, extension renewals, and security patches replace the compounding SaaS fees. The self-hosted model eliminates transaction fees permanently.

[H3: Budget the post-launch phase]

Allocate 20-30% of your migration project cost for the first 6 months post-launch. A migrated store is not a finished store on launch day.

That budget covers performance tuning, extension configuration, B2B workflow refinement, and the edge-case bugs that surface only under real traffic. Planning for this phase is accurate project scoping, not pessimism.

---

[H2: How does Virtina run a BigCommerce to Magento migration?]

Virtina is a Magento Certified partner with 1,000+ client engagements across B2B and B2C eCommerce. When you work with Virtina on a BigCommerce migration, the project starts with a full pre-migration audit: every URL catalogued, every app replacement mapped, every B2B data structure documented before any build work begins.

The build phase addresses the 4 failure points proactively. Password reset campaigns are prepared for launch day. The URL redirect map is built from the audit, not reconstructed after cutover. Variant data is transformed through scripted re-mapping, not manual entry. B2B account structures, customer groups, and tier pricing are rebuilt in the Magento B2B module during staging, not patched in after launch.

[CASE STUDY: insert real BigCommerce-to-Magento client data here if available]

Post-launch support covers the critical 6-month window: Search Console monitoring, performance tuning, and B2B workflow refinement as your team adapts to the new platform. To get an honest scoping conversation for your store, contact Virtina's [Magento migration services](https://virtina.com/magento-migration-services/) team.

---

## People Also Ask

**How long does a BigCommerce to Magento migration take?**

Agency-led migration takes 8-12 weeks for a small store (under 500 SKUs), 12-24 weeks for a mid-market store (500-5,000 SKUs), and 24-52+ weeks for an enterprise store with complex B2B and ERP requirements. DIY with tools is faster but not recommended for stores above 5,000 SKUs or with custom B2B configurations.

**Will I lose my SEO rankings when I migrate from BigCommerce to Magento?**

You can protect your rankings if you build a complete URL redirect map before launch and deploy server-side 301 redirects on cutover day. Poorly managed migrations cause 15-30% organic traffic loss in 90 days, but that outcome is avoidable with proper redirect planning and immediate post-launch Search Console monitoring.

**Can I use the Magento Data Migration Tool for BigCommerce?**

No. Adobe's Magento Data Migration Tool is designed exclusively for Magento 1 to Magento 2 migrations. It requires a source Magento 1 database and cannot connect to BigCommerce. For BigCommerce migrations, you need LitExtension, Cart2Cart, manual CSV transformation, or an agency API-based migration.

**How much does a BigCommerce to Magento migration cost?**

Agency costs range from $5,000-$15,000 for small stores to $20,000-$50,000 for mid-market stores and $75,000-$250,000+ for enterprise stores. Magento Open Source Year 1 TCO (hosting, development, and extensions) typically runs $30,000-$60,000 for a small-to-mid store.

**What B2B data can't be migrated automatically from BigCommerce?**

Customer passwords cannot be migrated due to incompatible hashing algorithms. B2B-specific data (customer groups, tier pricing, company account hierarchies, and shared catalogs) requires full manual rebuild in the Magento B2B module. Automated migration tools do not handle this work.

---

## Conclusion

If your GMV is above $500K, you're processing PO-based orders, and BigCommerce's June 2026 transaction fees are adding $3,000 or more to your annual platform cost, migration to Magento Open Source is worth a serious evaluation. Add deep B2B customization needs or an API ceiling to that picture and the case strengthens further.

Migration is not simple. The 4 failure points (passwords, URLs, variants, and B2B data) trip up most projects that move too fast. A phased approach with proper pre-audit work, staging QA, and a planned post-launch support window makes the difference between a clean cutover and a 90-day recovery.

---

## FAQ

**Does migrating to Magento affect my existing customer accounts?**

Yes, in one specific way: customer passwords cannot be migrated. BigCommerce and Magento use incompatible hashing algorithms, so every customer must reset their password on first login. Send a proactive reset email on launch day to reduce support friction. All other account data (order history, billing addresses, and company assignments) transfers through the standard migration process.

**What happens to my BigCommerce integrations (ERP, payment, shipping)?**

Your integrations need to be rebuilt for Magento's API architecture, not just reconnected. Magento uses its own extension framework, REST API, and GraphQL layer. An ERP integration that ran on a BigCommerce app must be rebuilt as a Magento extension or via a middleware connector. Plan for 2-4 weeks of integration rebuild work in Phase 3.

**Should I choose Magento Open Source or Adobe Commerce?**

Open Source is the right starting point for stores migrating primarily for customization and TCO control at under $5M GMV. Adobe Commerce is worth evaluating at $5M+ GMV when the native B2B module (RFQ, negotiable quotes, multi-level approvals, requisition lists, company account hierarchies) replaces a paid app stack you're already running on BigCommerce. Compare your current app spend against the Adobe Commerce license cost ($22,000-$125,000+ per year) before deciding.

**Is Magento harder to manage than BigCommerce day-to-day?**

Yes, operationally. BigCommerce is a managed SaaS platform: security patches, infrastructure updates, and uptime are handled by BigCommerce. Magento Open Source requires your team or a managed hosting partner to handle those tasks. You own the server, which gives you full control, but also full responsibility. Factor in a managed Magento hosting partner at $1,200-$12,000+ per year as part of your ongoing operational plan.

**What is the Hyva theme and why is it recommended?**

Hyva is a Magento frontend theme framework that replaces the default Luma stack with a leaner build using Alpine.js and Tailwind CSS. It generates significantly less JavaScript than Luma, which improves Core Web Vitals scores and reduces Time to First Byte directly. For a B2B store where catalog page load affects buyer workflows, Hyva is the performance-first choice over the standard Magento theme.

**Can I migrate product reviews and customer wishlists?**

Product reviews can typically be migrated as read-only records using migration tools or custom scripts. Customer wishlists are more variable: migration depends on whether your BigCommerce setup stored wishlist data in a recoverable format. In most agency-led migrations, wishlists are migrated where data is clean and skipped where it isn't. Historical orders are imported as read-only records with no functional transaction replay.

**How do I handle the B2B pricing structures I've built in BigCommerce?**

BigCommerce customer group pricing and tier pricing must be manually rebuilt in Magento's Customer Groups and tier pricing configuration. There is no automated transfer. Shared catalogs from BigCommerce B2B Edition require full manual reconstruction in the Magento B2B module. Budget 20-30% of total migration time for this work on any store with active B2B pricing structures.

**When should I NOT migrate from BigCommerce to Magento?**

Don't migrate if your GMV is under $500K and your B2B workflows are standard: company accounts, custom pricing, quote management, net terms, and PO ordering. The Year 1 Magento TCO makes the payback math negative at that scale. Also don't migrate if you need fast time-to-market: a mid-market migration takes 12-24 agency weeks minimum. And don't migrate if the June 2026 fee change is your only reason at lower GMV levels: the fee increase may cost less than the migration itself.
