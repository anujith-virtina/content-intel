---
title: Published posts inventory — addendum 2026-09-09
client: virtina
purpose: REST refresh result + newly discovered unindexed PAGE objects that block uniqueness checks
applies_to: published-posts-inventory.md
last_updated: 2026-09-09
total_posts: 310 (post count unchanged)
---

# Inventory addendum — 2026-09-09

> **Why this is a separate file:** the `Edit` tool was disabled in the session that produced this,
> and `published-posts-inventory.md` is 1,338 lines. Rewriting it wholesale was not safe.
> **Merge this into the main inventory and set its `last_updated` to 2026-09-09 when Edit is available.**
> Until then, read this file alongside the main inventory.

## 1. REST refresh — SUCCEEDED

The 2026-08-31 refresh had failed with HTTP 429 on every attempt and was left outstanding. Re-run
successfully on 2026-09-09 against:

`GET https://virtina.com/wp-json/wp/v2/posts?per_page=100&status=publish&orderby=date&order=desc`

- Newest published post is **ID 42491** (`gated-catalog-ai-visibility`), date **2026-09-01**. Already indexed.
- **No posts published between 2026-08-31 and 2026-09-09.** No additions to the post list.
- `total_posts` stays **310**.
- Set `last_updated: 2026-09-09` in the main file.
- Cosmetic date drift, not corrected: REST reports 42491 as 2026-09-01 (inventory says 2026-08-31) and
  42428 as 2026-07-16 (inventory says 2026-07-15).

## 2. ⚠ The inventory indexes POSTS only — pages are a uniqueness blind spot

Discovered 2026-09-09 during the high-risk payments audit.

Several **live, long-form, keyword-owning Virtina `page` objects are absent from the inventory entirely.**
A title-and-slug check against the inventory alone can therefore return a **false PASS**.

**New standing rule for every Virtina uniqueness audit:**

> Before declaring uniqueness, run BOTH of these in addition to the inventory grep:
> - `GET /wp-json/wp/v2/pages?_fields=id,slug,link,status,title&per_page=50&slug[]=...`
> - `GET /wp-json/wp/v2/search?search={head term}&per_page=40&_fields=id,title,url,subtype,type`
>
> The `search` endpoint returns pages and posts together and is the only reliable sweep.
> Do not trust the WP `title` field alone — see 36749 below, whose stored title is wrong.

## 3. Unindexed pages that own blog-style topics

### High-Risk Payment Processing for eCommerce Businesses
- **ID**: 36749  **Slug**: `high-risk-payment-processing-ecommerce-businesses`  **Type**: page  **Date**: 2024-09-12  **Modified**: 2024-09-12
- **Link**: https://virtina.com/high-risk-payment-processing-ecommerce-businesses/ (**published**, fetched HTTP 200 on 2026-09-09)
- **⚠ WP `title` field is WRONG.** Stored title reads "Ecommerce Warranty Services: A Comprehensive Guide for
  eCommerce Businesses". Rendered H1 is "High-Risk Payment Processing for eCommerce Businesses".
  This mismatch is exactly why the page never surfaced in any title-based check. **Report to client as a site data bug.**
- **Excerpt**: ~4,500 words. What makes a business high-risk; high-risk vs regular merchant accounts; lengthier
  application process; elevated processing fees; higher chargeback fees; processing volume caps; cash reserve
  requirements (rolling / capped / upfront); additional compliance requirements; a passing MATCH-list mention;
  an eight-point "how to choose a high-risk processor" framework.
- **BLOCKS**: any post targeting "high risk payment processing" or "high risk payment gateway" as primary keyword,
  and any "what makes you high-risk / how to get approved" overview angle.
- **Leaves open**: it predates Visa VAMP (thresholds effective 1 June 2025), VMSS, PCI DSS v4.x future-dated
  requirements (31 March 2025), Compelling Evidence 3.0, and has zero WooCommerce/Magento implementation content.

### High-Risk eCommerce Migration & Payment Gateway Integration
- **ID**: 42417  **Slug**: `high-risk-ecommerce-migration-payment-gateway-integration`  **Type**: page
- **Link**: https://virtina.com/high-risk-ecommerce-migration-payment-gateway-integration/ (**published**, fetched HTTP 200 on 2026-09-09)
- **Excerpt**: Commercial service landing page. Emergency migration off SaaS, platform comparison,
  NMI / Authorize.Net / USAePay integration, 6-step migration process, industries served, FAQ.
- **Confirmed by fetch NOT to cover**: merchant account approval, underwriting, VAMP/ECM thresholds, MATCH,
  reserves, or ongoing compliance. It is the **commercial CTA target** for any payments blog.

### Payment Gateway Service Providers — An Ultimate Guide
- **ID**: 37458  **Slug**: `payment-gateway-service-providers`  **Type**: page
- **Link**: https://virtina.com/payment-gateway-service-providers/ (**published**, fetched HTTP 200 on 2026-09-09)
- **Excerpt**: General gateway functionality, gateway types, provider comparisons. Mentions high-risk verticals in
  passing only. No underwriting, approval, or chargeback-compliance content.

### Other pages seen in the REST sweep (not yet assessed)
`shopify-development-services` (41866), `b2b-quote-chatbot` (41430), `b2b-ecommerce-referral-program` (41285),
`salesforce-commerce-data-customer-experience` (40972), `ai-powered-woocommerce-bug-fix` (39979).

## 4. Payments cluster count (for CHECK 5)

Nine properties, posts and pages combined:

| ID | Type | Slug | Date |
|---|---|---|---|
| 10687 | post | `payment-gateways-for-ecommerce-websites` | 2016 |
| 27207 | post | `woocommerce-payment-gateways` | 2022 |
| 32043 | post | `b2b-ecommerce-checkout-best-practices` | 2023 |
| 32117 | post | `payment-solutions-for-b2b-ecommerce-stores` | 2023 |
| 36423 | post | `best-woocommerce-payment-gateways` | 2024 |
| 36749 | **page** | `high-risk-payment-processing-ecommerce-businesses` | 2024 |
| 37458 | **page** | `payment-gateway-service-providers` | — |
| 42297 | post | `woocommerce-b2b-net-payment-terms` | 2026 |
| 42417 | **page** | `high-risk-ecommerce-migration-payment-gateway-integration` | 2026 |

**Broad payments cluster is SATURATED.** New payments posts require a documented unique sub-niche per section 4c.
