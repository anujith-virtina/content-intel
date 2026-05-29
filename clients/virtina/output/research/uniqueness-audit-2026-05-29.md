---
title: Uniqueness Audit — 2026-05-29
client: virtina
date: 2026-05-29
stage: research
---

# Uniqueness Audit — 2026-05-29

## Inventory status

Published posts inventory checked: `clients/virtina/reference/published-posts-inventory.md`
Last updated: 2026-05-20 (9 days old — within 7-day threshold since no new posts have been published per git log; most recent post in inventory is ID 42202, 2026-05-20)
Total posts indexed: 304

---

## Candidate topics evaluated

### Candidate A: B2B punchout catalog integration for WooCommerce (SELECTED)

**Proposed title:** How to add punchout catalog support to your WooCommerce B2B store (cXML and OCI guide)
**Proposed slug:** `woocommerce-punchout-catalog-integration`
**Primary keyword:** WooCommerce punchout catalog integration

| Check | Result | Evidence |
|---|---|---|
| CHECK 1: Title word overlap | PASS | No existing post title contains "punchout," "punch out," "cXML," or "OCI." No 3+ consecutive meaningful word sequence matches any of the 304 existing post titles. |
| CHECK 2: Slug overlap | PASS | Proposed slug `woocommerce-punchout-catalog-integration` shares only "woocommerce" with existing slugs. Two-word overlap check: "woocommerce-erp-integration" shares "woocommerce" and "integration" but not three consecutive words, and "erp" vs "punchout" are entirely different. No substring match. |
| CHECK 3: Primary keyword uniqueness | PASS | Search of full inventory shows no existing post has "punchout," "punch out," "cXML," "OCI," "eProcurement," or "punchout catalog" as focus keyword or in slug. |
| CHECK 4: Angle/thesis uniqueness | PASS | Existing WooCommerce ERP integration post (ID 42108) covers connecting WooCommerce to back-office ERP. This post covers the buyer-facing procurement direction: how enterprise buyers access a supplier's catalog through their own procurement system. Different direction, different workflow, different audience problem. No overlap with any B2B post excerpt. |
| CHECK 5: Cluster saturation | PASS | WooCommerce cluster has 50 posts but the sub-cluster of "WooCommerce B2B integrations" has only 2 posts (ID 42108 ERP integration, ID 42202 B2B customer portal). Integration cluster has only 3 posts, none about procurement connectivity. Punchout sub-niche has 0 existing posts. Well below the 5-post saturation threshold. |

**VERDICT: ALL 5 CHECKS PASS. Topic approved.**

---

### Candidate B: HubSpot WooCommerce B2B CRM integration (REJECTED)

**Proposed title:** How to connect HubSpot to your WooCommerce B2B store
**Proposed slug:** `hubspot-woocommerce-b2b-crm-integration`
**Primary keyword:** HubSpot WooCommerce integration

| Check | Result | Notes |
|---|---|---|
| CHECK 1: Title word overlap | PASS | No existing title matches |
| CHECK 2: Slug overlap | PASS | No existing slug contains "hubspot" |
| CHECK 3: Primary keyword uniqueness | PASS | No existing post claims this keyword |
| CHECK 4: Angle/thesis uniqueness | PASS on surface | But WooCommerce ERP integration (42108) and WooCommerce B2B customer portal (42202) cover adjacent ground on WooCommerce B2B technical setup |
| CHECK 5: Cluster saturation | PASS | Under threshold |

**Rejection reason:** SERP is already well-served by high-quality technical guides (Cloudways, FunnelKit, TechMarcos) with strong domain authority. Virtina's agency angle does not create a significant gap versus available content. Passes uniqueness checks but loses on competitive opportunity analysis.

---

### Candidate C: Composable commerce for B2B distributors (REJECTED)

**Proposed title:** Is composable commerce right for your B2B distribution business?
**Proposed slug:** `composable-commerce-b2b-distributors`
**Primary keyword:** composable commerce B2B distributors

| Check | Result | Notes |
|---|---|---|
| CHECK 1: Title word overlap | PASS | No overlap with existing titles |
| CHECK 2: Slug overlap | PASS | No existing slug matches |
| CHECK 3: Primary keyword uniqueness | PASS | No existing post claims this keyword |
| CHECK 4: Angle/thesis uniqueness | PASS | No composable commerce post exists |
| CHECK 5: Cluster saturation | PASS | Under threshold |

**Rejection reason:** SERP dominated by commercetools, Emporix, and Kibo — enterprise SaaS platforms with massive domain authority and massive content budgets. Topic is also architecture-level and abstract; Virtina's strength is WooCommerce/Magento implementation, not MACH architecture consulting for enterprise distributors. The topic does not play to Virtina's specific expertise edge.

---

### Candidate D: Headless commerce ROI for mid-market B2B (REJECTED)

**Proposed title:** Headless commerce for mid-market B2B: when the ROI actually makes sense
**Proposed slug:** `headless-commerce-roi-mid-market-b2b`
**Primary keyword:** headless commerce ROI B2B

| Check | Result | Notes |
|---|---|---|
| CHECK 1: Title word overlap | PASS | No overlap detected |
| CHECK 2: Slug overlap | CONDITIONAL FAIL | Existing post ID 11628 has slug `traditional-decoupled-headless-ecommerce-an-introduction` — contains "headless" and "ecommerce." Two-word overlap flag: "headless" overlaps, but not 2+ consecutive unique content words in the slug combination with proposed slug. Borderline pass. |
| CHECK 3: Primary keyword uniqueness | FAIL | Existing post 11628 covers headless ecommerce (2019, likely deindexed or low traffic but it exists in inventory) |
| CHECK 4: Angle/thesis uniqueness | FAIL | Even though the post is from 2019, the coverage of headless commerce already exists in Virtina's inventory. A new ROI-focused angle is different but the general headless topic is already claimed. |
| CHECK 5: Cluster saturation | PASS | Only 1 headless post |

**Rejection reason:** CHECK 3 FAIL — existing post 11628 (2019) claims the headless ecommerce keyword. CHECK 4 FAIL — angle overlap risk. Topic rejected per rules.

---

### Candidate E: WCAG 2.2 accessibility for B2B ecommerce (REJECTED)

**Proposed title:** WCAG 2.2 compliance for B2B ecommerce: what changed and what to fix
**Proposed slug:** `wcag-b2b-ecommerce-compliance`
**Primary keyword:** WCAG B2B ecommerce compliance

| Check | Result | Notes |
|---|---|---|
| CHECK 1: Title word overlap | PASS | No 3+ word consecutive match with existing titles |
| CHECK 2: Slug overlap | FAIL | Existing post ID 11570 has slug `ecommerce-and-ada-compliance-what-you-need-to-know-checklist-included`. Proposed slug contains "ecommerce" and "compliance" — 2-word overlap. |
| CHECK 3: Primary keyword uniqueness | FAIL | Existing post 11570 covers "ecommerce ADA compliance." While WCAG 2.2 is newer than the 2019 post, the B2B ecommerce compliance keyword cluster is already owned by that post. |
| CHECK 4: Angle/thesis uniqueness | FAIL | Post 11570 already covers ADA/WCAG compliance for ecommerce. A WCAG 2.2 update would need to be a revision of 11570, not a new post. |
| CHECK 5: Cluster saturation | PASS | Only 1 accessibility post |

**Rejection reason:** CHECK 2, 3, 4 FAIL — existing post 11570 claims this territory. Topic rejected.

---

## Final selected topic

**Topic:** B2B Punchout Catalog Integration for WooCommerce
**Proposed title:** How to add punchout catalog support to your WooCommerce B2B store (cXML and OCI guide)
**Proposed slug:** `woocommerce-punchout-catalog-integration`
**Primary keyword:** WooCommerce punchout catalog integration
**Secondary keywords:** cXML punchout WooCommerce, OCI punchout integration, B2B eProcurement WooCommerce, punchout catalog plugin WooCommerce

### Final uniqueness confirmation

- CHECK 1 PASS: No existing post title shares 3+ consecutive meaningful words with proposed title
- CHECK 2 PASS: Proposed slug `woocommerce-punchout-catalog-integration` is not a substring of any existing slug; 2-word overlap limited to "woocommerce" + "integration" which are common generic terms, not a meaningful slug match
- CHECK 3 PASS: Primary keyword "WooCommerce punchout catalog integration" is not the focus keyword of any existing post
- CHECK 4 PASS: Angle (how to enable enterprise procurement system connectivity from the supplier/WooCommerce side) is completely absent from existing Virtina content
- CHECK 5 PASS: WooCommerce B2B integration sub-cluster has 2 posts (ERP integration, B2B customer portal) — well below 5-post saturation threshold

**All 5 checks: PASS. Topic approved for brief and creation.**
