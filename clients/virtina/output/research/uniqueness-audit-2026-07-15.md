---
title: Uniqueness audit - Shopify vape ban / WooCommerce migration post
client: virtina
date: 2026-07-15
topic: Shopify ENDS ban and platform-risk thesis for WooCommerce migration
stage: research
slug: shopify-vape-ban-uniqueness-audit
---

# Uniqueness audit: Shopify ENDS ban post

## Pre-check: inventory refresh

`published-posts-inventory.md` `last_updated` was 2026-07-07 (8 days stale). Refreshed via WP REST API:

`GET https://virtina.com/wp-json/wp/v2/posts?per_page=50&status=publish&orderby=date&order=desc&after=2026-07-06T23:59:59`

Result: exactly **one** published post since 2026-07-07 — ID 42413 "BigCommerce to Magento migration: 2026 guide," slug `bigcommerce-to-magento-migration`, live post_date 2026-07-10T03:12:15. This post was already present in the inventory (previously logged as a draft pushed 2026-07-07). No net-new post to add; its status has since moved to published and its date should be corrected from 2026-07-07 to 2026-07-10.

**Inventory file updated:** `last_updated` set to 2026-07-15; `total_posts` remains 307 (no new titles added, only a status/date correction on an existing entry). No other posts published in the gap window.

## Candidates evaluated

### Candidate 1 (rejected as proposed): slug `shopify-vape-ban-woocommerce-migration`

- CHECK 1 (title overlap): PASS — no existing title shares 3+ consecutive words.
- CHECK 2 (slug overlap): **FAIL.** The word set {shopify, vape, ban, woocommerce, migration} shares 2 words ("woocommerce" + "migration") with existing slug `woocommerce-migration-guide` (ID 29601) and separately with `volusion-to-woocommerce-migration` (ID 42177). Per MUST-FOLLOW-RULES section 1 CHECK 2, 2+ word overlap is an automatic reject regardless of title distinctiveness.
- Verdict: **Slug rejected. Do not use.**

### Candidate 2 (rejected): slug `shopify-vape-ban-ecommerce-platform-risk`

- CHECK 2: **FAIL.** The word set includes "ecommerce" + "platform," which together match existing slug `ecommerce-platform-migration` (ID 18791) on 2 words.
- Verdict: **Slug rejected.**

### Candidate 3 (SELECTED): slug `shopify-vape-ban-merchant-deplatforming`

- **CHECK 1 — Title overlap: PASS.** Proposed working title: *"Shopify's vape ban proves no SaaS platform is safe for your store."* No existing post title (checked against all 307) shares 3+ consecutive meaningful words with this phrasing. Closest existing titles — "Shopify Vs. WooCommerce: Which Is The Better Platform?" (36721) and "Why Choose Shopify As Your eCommerce Platform?" (20763) — share at most "Shopify" + "platform" non-consecutively, well under the 3-consecutive-word threshold.
- **CHECK 2 — Slug overlap: PASS.** Word set {shopify, vape, ban, merchant, deplatforming}. Cross-checked against all 307 existing slugs. "Vape," "ban," "merchant," and "deplatforming" appear in zero existing slugs. "Shopify" alone appears in 10 existing slugs (e.g., `shopify-vs-woocommerce`, `shopify-plus-features`, `shopify-guide`) but each shares only that single word — never 2+. No substring match. **PASS.**
- **CHECK 3 — Primary keyword uniqueness: PASS.** Primary keyword recommendation: **"Shopify vape ban"** (secondary: "WooCommerce migration for high-risk merchants"). No existing post's focus keyword or slug claims this phrase or a close variant. Nearest posts (`shopify-vs-woocommerce`, general platform comparison; `bigcommerce-to-magento-migration`, fee-driven migration) target different keywords entirely.
- **CHECK 4 — Angle/thesis uniqueness: PASS, with one required differentiation.** Thesis: *the Shopify ENDS ban is not a vape-industry story, it's proof any SaaS platform can deplatform any merchant for any reason, and self-hosted WooCommerce plus a specialized high-risk payment gateway is the only structural fix.* This is checked against:
  - `shopify-vs-woocommerce` (36721): feature/pricing comparison, no deplatforming or regulatory angle. Distinct.
  - `volusion-to-woocommerce-migration` (42177): closest analog — also "platform failure forces a WooCommerce move." **Must be explicitly differentiated in the brief and draft**: Volusion's post is about a platform's business collapse (bankruptcy/decline) forcing an unplanned migration; the new post is about a healthy, dominant platform actively and deliberately dropping a legal, regulated product category under external political pressure. The causal mechanism (insolvency vs. policy enforcement) and the generalizable lesson (platform survival risk vs. platform product-policy risk) are different. The creator must not reuse Volusion-post phrasing or structure.
  - `top-ecommerce-solutions-for-firearm-and-ammunition-retailers` (36827) and `gun-store-ecommerce-platforms-comparison` (29279): high-risk vertical custom-development pitches, not tied to a specific deplatforming event or ban. Distinct.
  - `cbd-ecommerce-how-to-make-the-most-out-of-the-young-market` (13981, 2019): CBD market-opportunity overview, unrelated angle, six years old. Distinct.
  - No existing post makes the "platform risk is universal, not vape-specific" argument. **PASS.**
- **CHECK 5 — Cluster saturation:**
  - **Shopify cluster: 11 existing posts** — over the 6+ saturation threshold. Flagged as saturated. Per MUST-FOLLOW-RULES, saturation does not block a post if the sub-niche angle is clearly unique. None of the 11 existing Shopify posts (B2B channel setup, Shopify Plus features, dev-store transfer, hiring developers, mobile optimization, dev checklist, general guide, Shopify vs Shopify Plus, why choose Shopify, useful apps, developer tips) address deplatforming, product bans, regulatory pressure, or high-risk payment gateways. Sub-niche angle justified.
  - **Migration cluster: 4 existing posts** (BigCommerce→Magento, Volusion→WooCommerce, eCommerce migration checklist, platform-to-platform migration guide) — under the 5-post threshold. Adding this post brings the cluster to 5, which is within the current rule (REJECT triggers only at 5+ *existing* before the new post; 4 existing < 5). **PASS.**

## Final selected topic

- **Slug**: `shopify-vape-ban-merchant-deplatforming`
- **Working title**: "Shopify's vape ban proves no SaaS platform is safe for your store" (analyzer to finalize exact phrasing at brief stage; must stay under the sentence-case, non-hype rules in voice.md)
- **Primary keyword**: Shopify vape ban
- **Secondary keyword**: WooCommerce migration for high-risk merchants / self-hosted ecommerce platform risk
- CHECK 1: PASS
- CHECK 2: PASS
- CHECK 3: PASS
- CHECK 4: PASS (with required differentiation from post 42177 noted above)
- CHECK 5: PASS (Shopify cluster saturated but sub-niche angle justifies inclusion; migration cluster under threshold)

## Post-draft reminder for the publisher

- Phrasing uniqueness check still required: no 8+ word verbatim sequence may match any existing Virtina post, including post 42177 (Volusion→WooCommerce) given its topical proximity.
- Format selection: per MUST-FOLLOW-RULES section 11, review the last 10 published posts before picking a format. Recent formats used: 42391/42393/42413 = Format A/A/D. Format A and D have been used recently; consider **Format E (contrarian thesis)** given the "not just a vape problem" reframing, or **Format D (decision-tree/playbook)** given the migration-decision content — analyzer to confirm final choice and document reasoning in the brief.
