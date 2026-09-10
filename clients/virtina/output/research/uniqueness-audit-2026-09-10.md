---
title: Uniqueness audit — Magento / Adobe Commerce to WooCommerce
client: virtina
date: 2026-09-10
topic: Migrating away FROM Magento / Adobe Commerce TO WooCommerce
audience: B2B eCommerce leaders (VP eCommerce, Director of Digital) on Magento Open Source / Adobe Commerce
stage: research
slug: uniqueness-audit-2026-09-10
verdict: REJECT
---

# Uniqueness audit — 2026-09-10

## Verdict at a glance

**Proposed topic: "Migrating from Magento / Adobe Commerce to WooCommerce" — REJECTED.**

| Check | Result | Decisive evidence |
|---|---|---|
| CHECK 1 — Title word overlap | PASS (narrow) | No existing title carries 3+ consecutive content words. Passes only on a technicality. |
| CHECK 2 — Slug overlap | **FAIL** | Every viable slug hits 2+ word overlap against 6 or more existing slugs. |
| CHECK 3 — Primary keyword uniqueness | **FAIL** | Post 29601 carries a dedicated H2 titled verbatim "Magento to WooCommerce Migration". |
| CHECK 4 — Angle / thesis uniqueness | **SPLIT: execution angle FAIL, reasons-to-leave angle PASS** | 29601 already runs the four-phase how-to. Nothing runs the why-leave case. |
| CHECK 5 — Topic cluster saturation | **FAIL, severely** | 24 live migration properties (posts + pages). Rule rejects at 5. |

A topic is rejected if it fails any single check. This fails four.

---

## Pre-check 0 — PAGES sweep (mandatory, per section 1)

Run 2026-09-10. All fetches returned HTTP 200. Matched on **slug and fetched H1**, never the stored title.

**Endpoints swept:**
- `GET /wp-json/wp/v2/pages?per_page=100&status=publish&_fields=id,slug,link` — pages 1 and 2, 200 slugs returned
- `GET /wp-json/wp/v2/search?search=magento&per_page=50`
- `GET /wp-json/wp/v2/search?search=migration&per_page=50`
- `GET /wp-json/wp/v2/search?search=woocommerce+magento&per_page=40`

### New unindexed PAGE objects found (not in the inventory or the 2026-09-09 addendum)

| ID | Slug | Direction / real topic | Blocks what |
|---|---|---|---|
| 15854 | `migrate-to-woocommerce` | H1 fetched: "Migrate to WooCommerce Now". Service LP, ~1,200 words. Sections include "Any Platform to WooCommerce", "Our Migration Workflow". Does **not** name Magento specifically. | Owns the head term "migrate to WooCommerce". Confirmed CTA target, not a content blocker. |
| 10738 | `magento-migration-services` | H1: "Magento Migration Services". Fetched and confirmed: this is migration **TO** Magento 2, and M1→M2. Explicitly lists WooCommerce as a *source*, never a destination. | Confirms the "leaving Magento" direction is commercially unrepresented on the site. |
| 15570 | `migrate-to-magento` | Service LP, migration TO Magento. | Same. |
| 22251 | `woocommerce-migration-services` | Service LP. | Migration cluster count. |
| 30309 | `certified-platform-migration-experts` | Service LP. | Migration cluster count. |
| 11175 | `ecommerce-cart-migration` | Service LP ("Shopping Cart Migration Service"). Already the approved replacement for the dead `/ecommerce-migration-services/`. | Migration cluster count. |
| 22185 | `bigcommerce-migration-services` | Service LP. | Migration cluster count. |
| 22206 | `shopify-migration-services` | Service LP. | Migration cluster count. |
| 34828 | `volusion-to-shopify-migration` | Service LP. | Migration cluster count. |
| 34736 | `volusion-migration-services` | H1 differs from title: "Don't Get Stuck! Escape Volusion's Limitations..." | Migration cluster count. Another title/H1 mismatch, same class of bug as 36749. |
| **42474** | `square-cbd-hemp-ban-migration` | **Newly discovered. Published page, absent from both the inventory and the 2026-09-09 addendum.** Deplatforming-driven emergency migration. | Sits directly beside 42428 and 42441. **Add to inventory.** |

### Pre-check: inventory staleness

`last_updated: 2026-09-09`, one day old. Not stale, no refresh required. The 2026-09-09 addendum confirms newest post is 42491 (2026-09-01) and `total_posts: 310`.

**However, the addendum's own warning is now proven twice over:** the pages sweep above surfaced 11 uniqueness-relevant page objects, one of them (42474) published and completely unindexed. The inventory's page coverage is still incomplete.

---

## CHECK 1 — Title word overlap: PASS (narrow, technical)

Proposed working title: "Migrating from Magento to WooCommerce" or similar.

Meaningful-word sequences after stop-word removal, against the nearest titles:

| Existing post | Title content words | Longest consecutive match |
|---|---|---|
| 42413 | bigcommerce, magento, migration, 2026, guide | 1 |
| 29601 | woocommerce, migration, guide, migrate, woocommerce, any, ecommerce, platform | 1 |
| 37776 | magento, woocommerce, comparison, better | 2 ("magento woocommerce") |
| 10658 | woocommerce, magento, best, ecommerce, platform | 2 |
| 37552 | migrate, magento, 1, magento, 2 | 1 |

No 3+ consecutive match. **PASS.**

This is the only clean pass, and it is a technicality. The rule counts *consecutive* words, and "Magento to WooCommerce" survives only because "to" is a stop word and "vs" separates the pair in 37776. It should not be read as evidence of real distinctiveness.

## CHECK 2 — Slug overlap: FAIL

Rule: reject on substring match **OR** 2+ word overlap with any existing slug.

Natural slug `magento-to-woocommerce-migration` tested:

| Existing slug | Type | Overlapping words | Result |
|---|---|---|---|
| `woocommerce-migration-guide` (29601) | post | woocommerce, migration | FAIL |
| `bigcommerce-to-magento-migration` (42413) | post | magento, migration, to | FAIL |
| `volusion-to-woocommerce-migration` (42177) | post | woocommerce, migration, to | FAIL |
| `magento-vs-woocommerce` (37776) | post | magento, woocommerce | FAIL |
| `woocommerce-vs-magento-comparison` (10658) | post | woocommerce, magento | FAIL |
| `shopify-vape-store-woocommerce-migration` (42428) | post | woocommerce, migration | FAIL |
| `secure-your-woocommerce-site-post-migration` (36792) | post | woocommerce, migration | FAIL |
| `woocommerce-migration-services` (22251) | page | woocommerce, migration | FAIL |
| `magento-migration-services` (10738) | page | magento, migration | FAIL |

Nine collisions. Precedent exists for a workaround slug that drops the colliding words (42441 used `leaving-shopify-ownership-risk`; 42491 used `gated-catalog-ai-visibility`). But in both those cases the keyword survived in the H1 and meta while the *body topic* was still unclaimed. Here the body topic is claimed too, so a slug workaround only hides the collision. **FAIL.**

## CHECK 3 — Primary keyword uniqueness: FAIL

Primary keyword: "Magento to WooCommerce migration".

**Post 29601 (`woocommerce-migration-guide`, ~7,500-8,000 words, published) contains a dedicated H2 heading titled verbatim "Magento to WooCommerce Migration."** Fetched and confirmed 2026-09-10. The section runs roughly four paragraphs across a four-phase walkthrough (select source and target, choose entities to transfer, run via a migration tool, optional demo migration), with step images.

A strict literal reading of the check ("must not be the focus keyword of any existing post; cross-check against slug fields") would return a PASS, because no *slug* encodes the phrase. I am not taking that reading. The check's stated purpose is to stop two Virtina URLs competing for the same query. A published 8,000-word page with an H2 matching the target keyword exactly is already the site's answer for that query. Publishing a second post on it is textbook self-cannibalisation.

**FAIL.**

## CHECK 4 — Angle / thesis uniqueness: SPLIT

Two sub-theses were assessed separately.

**Sub-thesis A: "here is how to execute a Magento to WooCommerce move" — FAIL.**
29601 already covers method selection (manual / tool / hire an expert), a named tool path, a pre-migration checklist, a post-migration checklist, DNS cutover, link testing, and SEO. 34921 (`ecommerce-website-migration-checklist`, 6,221 words) covers the checklist generically. 18791 (`ecommerce-platform-migration`, 3,911 words) covers the planning. 36792 covers post-migration hardening. 42413 already covers the four non-automatable failure points (passwords, URLs, variants, B2B account data), the SEO/redirect preservation, the AI-citation-preservation KPI, and cost-and-timeline-by-store-size. There is nothing left in the execution brief that isn't already published.

**Sub-thesis B: "here is why a merchant should leave Magento" — PASS, and the orchestrator's finding is confirmed.**
Every one of the 40 Magento posts is pro-Magento, neutral, or upgrade-oriented. Verified sample: 39502 (future-proof *with* Magento), 33839 (why choose Magento), 21145 (why use Magento), 20229 (Magento is best for B2B), 11079 (Open Source vs Commerce, 2019), 36776 (what is Adobe Commerce), 38078 (Adobe Commerce B2B features). The migration posts move merchants *to* Magento (10738, 15570, 42413) or between Magento versions (37552, 26989, 11936, 37127).

**Nothing on virtina.com argues a case for leaving Magento. That gap is real.** It is the one genuinely valuable finding in this audit, and the three alternatives below are built on it.

## CHECK 5 — Topic cluster saturation: FAIL

Rule: reject at 5 or more existing properties on the same general subject, where "same general subject means posts a reader seeking info on topic X would already find."

### Migration cluster, full count (posts + pages)

| # | ID | Type | Slug |
|---|---|---|---|
| 1 | 29601 | post | `woocommerce-migration-guide` (contains the exact target H2) |
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

**24 properties. Threshold is 5.**

The rule survives every narrower cut too:

- "Migrating **to** WooCommerce from another platform": 29601, 42177, 42428, 36792, 17289, 15854, 22251 = **7**. FAIL.
- "**Magento** + migration": 37552, 26989, 11936, 42413, 10738, 15570 = **6**. FAIL.
- "**Magento to WooCommerce** specifically": 29601's H2, 37776, 10658 = **3**, plus the two service LPs = 5. FAIL at the boundary.

There is no definition of the cluster under which this passes.

### On the section 1 / section 4c tension

Section 4c says saturation "does NOT block a post if the sub-niche angle is clearly unique." Section 1 CHECK 5 says reject at 5+. Read literally, CHECK 5 alone would make every new Magento post impossible, since the Magento cluster holds 40 posts.

The site's own working precedent resolves this. Post 42465 shipped into a 50-post WooCommerce cluster because a grep of the full inventory for "shortcode" returned **zero**. Post 42491 shipped into a saturated AI cluster on the same basis. The operative test is therefore: **does the sub-niche term return zero matches against the corpus?**

Magento-to-WooCommerce returns the opposite of zero. It returns a verbatim H2 on a published 8,000-word post. The 4c escape hatch does not apply. **FAIL stands.**

---

## Rejected candidate summary

| Candidate | C1 | C2 | C3 | C4 | C5 | Verdict |
|---|---|---|---|---|---|---|
| Magento / Adobe Commerce to WooCommerce migration | PASS | FAIL | FAIL | SPLIT | FAIL | **REJECT** |
| (prior session) Complete eCommerce Platform Migration Guide | FAIL | FAIL | FAIL | FAIL | FAIL | REJECT |

---

## Three alternatives that pass all five checks

All three are built on the confirmed CHECK 4 gap: **virtina.com has no content that argues a case for leaving, or costs the case for staying on, Magento.** All three deliberately sit outside the migration cluster, so CHECK 5 is clean rather than argued.

Ranked.

---

### ALTERNATIVE 1 (recommended) — The August 2026 Magento support cliff

**Working title:** "Your Magento version lost support last month. What are your four options?"
**Proposed slug:** `magento-version-support-cliff-2026`
**Primary keyword:** Magento end of support 2026
**Format:** D (decision-tree / playbook). Format D last used once in the recent 10 (42413), so it is available.

**One-line thesis:** Adobe ended regular support for the 2.4.6 line on 11 August 2026 and extended support for 2.4.5 on the same day, so a large slice of the Magento install base is now unpatched, and the honest answer is that three of the four available responses do not involve leaving Magento at all.

**Verified anchor facts** (Adobe Experience League, fetched 2026-09-10):
- Adobe Commerce / Magento Open Source **2.4.9 GA: 12 May 2026**; regular support to 2029.
- **2.4.6 regular support ended 11 August 2026.** Extended support runs to 31 August 2027, security provisioning to 31 May 2028.
- **2.4.5 regular support ended 12 August 2025**; extended support ended **11 August 2026**.
- **2.4.7 regular support ends 31 May 2027.** 2.4.8 runs to 2028.

**Checks cleared:**
- C1: no existing title carries "support", "end of life", or any 2.4.x version string. Inventory grep for `end of support|EOL|2\.4\.[6-9]|PHP 8|Symfony|composer` returned **zero** post matches.
- C2: slug shares at most 1 word ("magento") with any existing slug.
- C3: "Magento end of support 2026" is claimed by nothing on the site. The nearest, 18636 `magento-2-4-update`, is a 2020 post about 2.4.2 features.
- C4: unclaimed. 37127 (`upgrade-magento-version-step-by-step-guide`, 2024) is a mechanical how-to with no decision content and predates every fact above.
- C5: the "Magento version lifecycle" cluster contains **0** properties. The adjacent "Magento upgrade" cluster (37127, 18636, 10666, 10702) is 4, and a reader searching "magento 2.4.6 end of support" would not surface any of them.

**Why it is ranked first:** it is the only option that legitimately carries everything the original brief wanted. The maintenance burden, the cost of staying current, the developer scarcity, the upgrade fatigue, and an honest "option four is replatform, and here is exactly when that is right" all belong in a support-cliff decision article. It is also news-anchored and dated, which is the pattern that worked for 42428 and 42465.

---

### ALTERNATIVE 2 — What Magento actually costs to run in 2026

**Working title:** "What does it really cost to run a Magento store in 2026?"
**Proposed slug:** `magento-running-costs-2026`
**Primary keyword:** Magento total cost of ownership
**Format:** A (standard explanatory) with a mandatory comparison table, or C if each cost line gets a defensible opinion. Format A used twice in the recent 10, so still available.

**One-line thesis:** The licence is the smallest line on a Magento budget, and the four costs that actually decide whether a mid-market store can stay (hosting, the upgrade cycle, extension re-certification, and developer day rate) are the ones nobody quotes up front.

**Checks cleared:**
- C1/C2/C3: inventory grep for `total cost|TCO|licen` returned zero post matches. Nearest is 12678 `ecommerce-website-cost` (2019, generic build cost, not Magento, not run-rate).
- C4: unclaimed. 11079 `magento-open-source-vs-magento-commerce` (2019) compares editions on features, not cost.
- C5: "Magento cost / TCO" cluster = **0**. Broader "eCommerce cost" cluster = 12678 plus two calculator pages (35921, 12042) = 3. Under threshold.

**Ranked second because of a factual risk you should weigh before committing:** Adobe does not publish Adobe Commerce list pricing. It is quote-based and scales with GMV. Every dollar figure in circulation is a third-party estimate. Under the never-invent-a-statistic rule this post would have to be built almost entirely on ranged, attributed, clearly-labelled third-party estimates, or on cost *structure* rather than cost *amounts*. That is doable but it is a harder brief than Alternative 1.

---

### ALTERNATIVE 3 — What the 2.4.9 upgrade actually breaks

**Working title:** "Magento 2.4.9: what actually breaks when you upgrade"
**Proposed slug:** `magento-249-upgrade-breaking-changes`
**Primary keyword:** Magento 2.4.9 upgrade
**Format:** A, structured as symptom / cause / fix cases. This mirrors the structure that made 42465 work.

**One-line thesis:** 2.4.9 is not a routine point release, and the extension and integration parity work it forces is the real reason merchants stall on an unsupported version.

**Verified anchor facts** (Adobe Magento Open Source 2.4.9 release notes, fetched 2026-09-10):
- GA 12 May 2026.
- All Symfony dependencies in the `magento/composer` package moved to **Symfony LTS 7.4**.
- Official support added for **Symfony 7.4 LTS and PHP 8.5**.
- Composer support extended from 2.2.x to **2.4.x**.
- The third-party `carlos-mg89/oauth` library was **replaced with native PHP OAuth functions**.
- `clearCart` GraphQL mutation now available to all Open Source users, not just Adobe Commerce.

**Checks cleared:** identical grep evidence to Alternative 1. C5 cluster = 0.

**Ranked third for two reasons.** First, it is narrower and more developer-facing than Virtina's primary audience of VP eCommerce and Director of Digital. Second, and more important, there is a live factual conflict flagged below that would need resolving before drafting.

---

## Factual risks to carry forward

- **[unverified] "2.4.9 raises system requirements across PHP, database, search and caching" and "three core framework components were replaced."** These claims appear in secondary agency coverage. Adobe's own 2.4.9 release notes confirm only the Symfony 7.4 LTS move, added PHP 8.5 support, the Composer 2.4.x extension, and the single `carlos-mg89/oauth` replacement. They explicitly do not state minimum PHP, MySQL/MariaDB, OpenSearch, or Redis/Valkey versions. **Do not repeat the stronger claim without pulling Adobe's separate system requirements page.**
- **[unverified] The "501 fixed issues in Open Source / 560 in Adobe Commerce" and "500+ enhancements" counts.** Secondary sources only, not confirmed against Adobe's notes.
- **Adobe Commerce pricing is not published by Adobe.** Any licence figure is a third-party estimate and must be labelled as one.
- Two more title-vs-H1 mismatches were found on live pages (34736, and previously 36749). This is a recurring site data bug worth reporting to the client. It also means **future audits must keep matching on slug and fetched H1**, never the stored title.

## Inventory maintenance actions

1. Add page **42474** (`square-cbd-hemp-ban-migration`) to the indexed PAGE objects table. It is published and completely unindexed.
2. Add the 10 other migration-cluster pages listed in Pre-check 0 to the indexed PAGE objects table.
3. Record that post **29601 owns a verbatim "Magento to WooCommerce Migration" H2**, so no future audit re-litigates this.
4. Note the migration cluster is **SATURATED at 24 properties**, matching the existing SATURATED flag on payments.

## Format rotation note for the analyzer

Formats in the recent published set: E (42491), E (42465), B (42441), E (42428), D (42413), A (42393), A (42391).

**Format E is used in 3 of the last 7 and is therefore blocked** by the section 11 recency rule. Formats C and F have not been used recently at all. D and A remain available.
