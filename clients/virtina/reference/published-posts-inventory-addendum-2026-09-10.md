---
title: Published posts inventory — addendum 2026-09-10
client: virtina
purpose: Pre-check 0 sweep results — 11 unindexed PAGE objects, 1 unindexed published page, 1 new title/H1 mismatch, migration cluster saturation flag
applies_to: published-posts-inventory.md, published-posts-inventory-addendum-2026-09-09.md
last_updated: 2026-09-10
total_posts: 310 (unchanged)
---

# Inventory addendum — 2026-09-10

> **Read this alongside the main inventory AND the 2026-09-09 addendum.** Merge all three when `Edit` is available.
> Produced during the Magento-to-WooCommerce uniqueness audit (`output/research/uniqueness-audit-2026-09-10.md`).

## 1. Inventory staleness

`last_updated: 2026-09-09`, one day old at time of sweep. **Not stale, no post refresh required.** Newest published post remains 42491 (`gated-catalog-ai-visibility`). `total_posts` stays 310.

## 2. ⚠ Post 42474 — PUBLISHED and absent from both the inventory and the 09-09 addendum

### Square CBD/Hemp Ban Migration
- **ID**: 42474  **Slug**: `square-cbd-hemp-ban-migration`  **Type**: page
- **Link**: https://virtina.com/square-cbd-hemp-ban-migration/ (**published**, returned in the pages sweep 2026-09-10)
- **Topic**: deplatforming-driven emergency migration, Square's CBD/hemp ban.
- **Why it matters**: it sits directly beside posts **42428** (`shopify-vape-store-woocommerce-migration`) and **42441** (`why-businesses-are-leaving-shopify`), and beside page **42417**. Any future deplatforming, high-risk, or platform-risk topic must be checked against this page. A posts-only audit misses it entirely.
- **ACTION**: add to the "Indexed PAGE objects" table in the main inventory.

This is the **second** confirmed instance of a published, keyword-owning page being invisible to the audit process, after 36749 on 2026-09-09. The blind spot is systemic, not a one-off.

## 3. Eleven unindexed migration-cluster PAGE objects

All returned by `GET /wp-json/wp/v2/pages?per_page=100&status=publish` (pages 1 and 2) and `/wp-json/wp/v2/search` on 2026-09-10. None appear in the main inventory or the 09-09 addendum.

| ID | Slug | Direction / real topic | Audit relevance |
|---|---|---|---|
| 15854 | `migrate-to-woocommerce` | **H1 fetched: "Migrate to WooCommerce Now".** Service LP, ~1,200 words. Sections: "Any Platform to WooCommerce", "All Entities", "Our Migration Workflow", FAQ. Does **not** name Magento as a source. | Owns the head term "migrate to WooCommerce". CTA target, not a content blocker. |
| 10738 | `magento-migration-services` | **H1: "Magento Migration Services". Fetched and confirmed: migration TO Magento 2, and M1 to M2.** Explicitly lists WooCommerce, BigCommerce, Shopify, Volusion, PrestaShop as **sources**, never destinations. | Confirms virtina.com has **no** commercial page for leaving Magento. |
| 15570 | `migrate-to-magento` | Service LP, migration TO Magento. | Cluster count. |
| 22251 | `woocommerce-migration-services` | Service LP. | Cluster count. |
| 22185 | `bigcommerce-migration-services` | Service LP. | Cluster count. |
| 22206 | `shopify-migration-services` | Service LP. | Cluster count. Already used as a link target by post 42441. |
| 11175 | `ecommerce-cart-migration` | Service LP, "Shopping Cart Migration Service". | Already the approved section 6 replacement for the dead `/ecommerce-migration-services/`. |
| 30309 | `certified-platform-migration-experts` | Service LP. | Cluster count. |
| 34828 | `volusion-to-shopify-migration` | Service LP. | Cluster count. Sits beside post 42177. |
| 34736 | `volusion-migration-services` | Service LP. **Title/H1 mismatch, see section 4.** | Cluster count. |
| 42417 | `high-risk-ecommerce-migration-payment-gateway-integration` | Already indexed in the 09-09 addendum. Listed here for cluster completeness. | Cluster count. |

**ACTION**: add all of the above to the "Indexed PAGE objects" table.

## 4. ⚠ Second title-vs-H1 mismatch found: page 34736

- **ID**: 34736  **Slug**: `volusion-migration-services`
- **Stored WP title**: "Volusion Migration Services"
- **Rendered H1 / real content**: "Don't Get Stuck! Escape Volusion's Limitations and Elevate Your eCommerce Empire"

Same class of client-side data bug as **36749**, whose stored title ("Ecommerce Warranty Services...") has nothing to do with its content.

**Two confirmed instances now.** The standing rule from the 09-09 addendum is reinforced and should be treated as non-negotiable:

> **Match on slug and fetched H1. Never trust the stored WP `title` field.** A title grep will keep returning false passes.

**ACTION**: report both 36749 and 34736 to the client as a site data bug.

## 5. Migration cluster count for CHECK 5

**Twenty-four properties, posts and pages combined.**

| # | ID | Type | Slug |
|---|---|---|---|
| 1 | 29601 | post | `woocommerce-migration-guide` |
| 2 | 34921 | post | `ecommerce-website-migration-checklist` |
| 3 | 18791 | post | `ecommerce-platform-migration` |
| 4 | 42177 | post | `volusion-to-woocommerce-migration` |
| 5 | 42413 | post | `bigcommerce-to-magento-migration` |
| 6 | 42428 | post | `shopify-vape-store-woocommerce-migration` |
| 7 | 36792 | post | `secure-your-woocommerce-site-post-migration` |
| 8 | 17289 | post | `migrating-woocommerce-subscriptions` |
| 9 | 37552 | post | `migrate-from-magento-1-to-magento-2` |
| 10 | 26989 | post | `reasons-to-migrate-from-magento-1-to-magento-2` |
| 11 | 11936 | post | `migrate-from-magento-1-0-to-magento-2-0` |
| 12 | 42037 | post | `woocommerce-hpos-migration` (different sense, counted for completeness) |
| 13 | 15854 | page | `migrate-to-woocommerce` |
| 14 | 15570 | page | `migrate-to-magento` |
| 15 | 22251 | page | `woocommerce-migration-services` |
| 16 | 10738 | page | `magento-migration-services` |
| 17 | 11175 | page | `ecommerce-cart-migration` |
| 18 | 30309 | page | `certified-platform-migration-experts` |
| 19 | 22185 | page | `bigcommerce-migration-services` |
| 20 | 22206 | page | `shopify-migration-services` |
| 21 | 34828 | page | `volusion-to-shopify-migration` |
| 22 | 34736 | page | `volusion-migration-services` |
| 23 | 42417 | page | `high-risk-ecommerce-migration-payment-gateway-integration` |
| 24 | 42474 | page | `square-cbd-hemp-ban-migration` |

> **⚠ The MIGRATION cluster is SATURATED at 24 properties.** Threshold for CHECK 5 rejection is 5.
> New migration content requires a documented, genuinely unclaimed sub-niche per section 4c, and the
> bar should be the 42465 test: does a grep of the corpus for the sub-niche term return **zero**?

This joins the payments cluster (9 properties, flagged 2026-09-09) as a standing SATURATED flag.

## 6. ⚠ Post 29601 owns a verbatim "Magento to WooCommerce Migration" H2

Recorded so no future audit re-litigates this.

- **ID**: 29601  **Slug**: `woocommerce-migration-guide`  **Published.** ~7,500 to 8,000 words (fetched and counted 2026-09-10; the inventory has no word count for it).
- It carries **18 H2s and 21 H3s**, including a dedicated H2 titled verbatim **"Magento to WooCommerce Migration"**, plus per-platform H2s for BigCommerce, Shopify, OpenCart, SquareSpace and PrestaShop.
- **BLOCKS**: any post targeting "Magento to WooCommerce migration", or any other single-platform-to-WooCommerce migration keyword, as its primary keyword. Each destination already has its own H2 here.
- **Lesson for the process**: the inventory excerpt for 29601 is two sentences of intro prose and shows none of this. **Excerpt fields are not sufficient for CHECK 3 or CHECK 4 on long-form pillar posts. Fetch the post and read its headings.**

## 7. Rejected topics log

| Date | Proposed topic | Verdict | Audit file |
|---|---|---|---|
| 2026-09-10 | "Complete eCommerce Platform Migration Guide: Magento, Volusion, BigCommerce, Shopify" | REJECT, all 5 checks | uniqueness-audit-2026-09-10.md |
| 2026-09-10 | Migrating from Magento / Adobe Commerce to WooCommerce | REJECT: C2, C3, C5 FAIL; C4 split | uniqueness-audit-2026-09-10.md |
| 2026-09-10 | **The August 2026 Magento version support cliff** (`magento-version-support-cliff-2026`) | **ACCEPTED, all 5 PASS.** Format D. | uniqueness-audit-2026-09-10.md |

## 8. Confirmed content gap on virtina.com

All 40 Magento posts are pro-Magento, neutral, or upgrade-oriented. Both Magento migration pages (10738, 15570) sell migration **to** Magento. **Nothing on the site argues a case for leaving Magento, or costs the case for staying.**

Inventory grep for `end of support | EOL | 2\.4\.[6-9] | PHP 8 | Symfony | composer | total cost | TCO | licen` returns **zero** matches across all 310 posts. The Magento version-lifecycle and Magento-cost sub-niches are both genuinely unclaimed.
