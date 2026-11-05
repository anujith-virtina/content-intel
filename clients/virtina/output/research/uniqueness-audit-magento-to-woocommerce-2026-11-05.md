---
title: Uniqueness audit, Magento to WooCommerce migration
client: virtina
date: 2026-11-05
topic: magento to woocommerce migration (what moves, what breaks, when not to)
audience: B2B and B2C store owners on Magento / Adobe Commerce weighing a move to WooCommerce
stage: research
slug: uniqueness-audit-magento-to-woocommerce-2026-11-05
---

# Uniqueness audit (MUST-FOLLOW section 1)

Method: live REST sweep on 2026-11-05. The inventory file is stale (last_updated 2026-09-09, 310 posts), so it was refreshed from `/wp-json/wp/v2/posts?per_page=100` (100 newest, back to 2025-01) plus keyword searches. All three pages of `/wp-json/wp/v2/pages?per_page=100` were swept (page 1: 100 items, page 2: 100, page 3: about 75, then empty). `/wp-json/wp/v2/search` was run for "magento to woocommerce migration" and "migrate magento woocommerce". Matching is on slug and fetched H1/H2/H3, never on stored title.

## Verdict: CONDITIONAL GO (see Check 2 and Check 5 for the two literal-rule failures and how they are handled)

Proposed (working) title: "Magento to WooCommerce migration: what moves, what breaks, and when to stay"
Working slug from user: `magento-to-woocommerce-migration` (FAILS Check 2, replacement below)
Primary keyword: magento to woocommerce migration

## Pre-check 0: pages and search

- No page or post has the slug `magento-to-woocommerce-migration`. `https://virtina.com/magento-to-woocommerce-migration/` returns 404 (free to use, but see Check 2).
- Nearest page objects, all read in full (H1/H2/H3):
  - 22251 `woocommerce-migration-services` (service LP). Magento appears only in a generic "migrating from other platforms (Shopify, Magento, BigCommerce)" line. No Magento-specific steps, mapping or cost.
  - 15854 `migrate-to-woocommerce` (service LP). The word "Magento" does not appear.
  - 10738 `magento-migration-services` (service LP). Entirely about migrating TO Magento (M1 to M2). Nothing on leaving Magento.
  - 20688 `ecommerce-replatform` (service LP). Platform cards only.
  - 43054 `magento-to-shopify-migration` (page). Has "What moves, and what gets rebuilt" and B2B mapping, but to Shopify. WooCommerce appears only as a footer link. This is the structural sibling, not a duplicate.
  - 42997 `woocommerce-to-shopify-migration` (page). Mapping tables WooCommerce to Shopify. No Magento.
  - 30309 `certified-platform-migration-experts`, 11175 `ecommerce-cart-migration`: generic service pages (not read in depth; titles only, no Magento-to-Woo slug).
- No Magento-to-WooCommerce page exists. Page 36749 style title-mismatch risk: none of the swept slugs hide this topic.

## Posts read in full (H2/H3)

| ID | Slug | Magento to WooCommerce coverage |
|---|---|---|
| 42582 | `magento-version-support-cliff-2026` | Read in full, not truncated. "Path 3: replatform" has H3s "Five store profiles that should stay on Magento" and "Where merchants who do leave usually land". It says leavers mostly land on WooCommerce and points to the comparison post. Nothing on how the move works. Its "stay" profiles (complex B2B, multi-store, deep ERP, large attributed catalogs, peak timing) overlap with our when-not-to section, so ours must be WooCommerce-mapped and must not restate the profile list. |
| 43110 | `magento-2-4-6-end-of-support-upgrade-or-move` | H2 "Should you upgrade Magento or move to another platform?" with H3 "When moving to another platform makes sense": one paragraph naming Shopify, BigCommerce, WooCommerce. Table row "Replatform to WooCommerce". H2 "How do you protect your SEO if you leave Magento?" exists (generic). Nothing on data mapping. |
| 43418 | `magento-2-migration-checklist-cost` | 24 H2s, all about migrating to Magento 2. WooCommerce appears once ("Shopify or WooCommerce can cost less to run"). Modified today 2026-11-05 04:13, re-read before drafting. |
| 29601 | `woocommerce-migration-guide` | Pillar, last modified 2023. H3 "Magento to WooCommerce Migration" = four LitExtension click-steps, no edge cases. Heading shares the primary keyword (see Check 3). |
| 37776 | `magento-vs-woocommerce` | Pure comparison (H2 per criterion). No migration content. |
| 10658 | `woocommerce-vs-magento-comparison` | Pure comparison. No migration content. |
| 38095 | `a-comprehensive-guide-to-adobe-commerce-b2b-features` | Feature list: company accounts, shared catalogs, quick order, negotiable quotes, PO approvals, requisition lists. No WooCommerce, no migration. Useful link target for the when-not-to section. |
| 34921 | `ecommerce-website-migration-checklist` | Generic checklist. Lists Magento and WooCommerce plugin examples only. |
| 18791 | `ecommerce-platform-migration` | Generic planning. Magento and WooCommerce named only as platform options. |
| 42177 | `volusion-to-woocommerce-migration` | Volusion source. Has phases, "What does not migrate", 301 phase, password reset. Different source platform; our post must not reuse its phrasing for passwords and redirects. |
| 43507 | `volusion-to-bigcommerce-migration` | "What changes and what breaks" format source. Different pair. |
| 42428, 42441 | Shopify leaving posts | Different source platform. |

## Check 1: title word overlap, PASS
No existing post or page title shares 3 or more consecutive content words with the proposed title. Closest: 29601 "WooCommerce Migration Guide..." (2 words: WooCommerce migration), 43507 "...What Changes and What Breaks" (2 words: what breaks). Keep "what moves" rather than "what changes" to stay clear of 43507.

## Check 2: slug overlap, FAIL for the working slug, PASS for the replacement
Working slug `magento-to-woocommerce-migration` shares two or more content words with at least: `volusion-to-woocommerce-migration` (woocommerce, migration), `woocommerce-migration-guide`, `woocommerce-migration-services`, `magento-to-shopify-migration` (magento, migration), `magento-migration-services`, `magento-vs-woocommerce` (magento, woocommerce). Literal rule says REJECT. Precedent: posts 42441 and 42491 resolved this by choosing a slug that omits one platform name and keeping the keyword in H1, meta, and first 100 words.
Recommended slug: `leaving-magento-data-map` is rejected-risk free but weak; preferred `leaving-magento-what-moves-breaks`. Shares at most one word with any slug found (leaving: `why-businesses-are-leaving-shopify`, `leaving-shopify-ownership-risk`; magento: many; no slug holds two of leaving/magento/moves/breaks). The orchestrator must re-run this check against the final slug before push because the user may prefer the keyword slug and accept the deviation explicitly.

## Check 3: primary keyword, CONDITIONAL PASS
- No post or page slug claims the keyword. Yoast focus keywords are not exposed on the public REST, so focus keywords could not be read directly. [unverified]
- Contested by: 29601 H3 "Magento to WooCommerce Migration" (a four-step tool walkthrough inside an any-platform pillar) and service page 22251 "WooCommerce migration services".
- Memory rule says a matching heading inside a big pillar is normally an outright rejection. Here the pillar heading is a thin tool tutorial, not a dedicated treatment, and the trend brief selects the keyword on demand evidence. Mitigation: the new post must own the mapping, breakpoints and stay-test (none of which 29601 contains), link to 29601 once as the generic pillar, and the creator must not copy its LitExtension step list. Orchestrator should accept this knowingly. If the user wants a zero-risk reading, reject.

## Check 4: angle and thesis, PASS
Existing angles: 42582 and 43110 = should you leave (decision, no mechanics). 29601 = tool click-through. 43054 = same mechanics to Shopify. 37776 and 10658 = feature comparison.
New thesis: leaving Magento for WooCommerce is mostly a data-mapping and rebuild exercise, and the parts that do not map (B2B account hierarchy, shared catalogs, negotiable quotes, multi-store, custom modules, password hashes, URL structure) decide whether you should go at all. No existing Virtina asset maps Magento objects to WooCommerce objects. Nothing duplicates this.
Caution: 43054 (Magento to Shopify page) already uses "what moves, and what gets rebuilt" as an H2. Use different heading wording and different mapping rows (WooCommerce specifics), and do not copy its B2B mapping sentences.

## Check 5: cluster saturation, FAIL on literal count, rescued under section 4c
Count of Virtina assets a reader seeking "move from Magento to WooCommerce" would already find: 42582, 43110, 29601, 22251, 43054 (Shopify variant), plus 37776 and 10658 (comparisons) = 5 to 7. Literal Check 5 says REJECT at 5 or more. Section 4c says saturation does not block a post when the sub-niche is clearly unique. The sub-niche here (object-by-object mapping, breakpoints, stay-test, WooCommerce-specific) is unclaimed. Precedent: 43507, 43075 and 42441 shipped on the same reasoning. This is a judgment call for the orchestrator and the user; the researcher records it as a risk, not a clean pass.

## Phrasing risks for the 8-gram gate
- Avoid the boilerplate platform sentence (WooCommerce, Magento, BigCommerce, Shopify listed together).
- Avoid 42582's line that most leavers land on WooCommerce (unsourced).
- Avoid 43054's absolute "passwords can't be exported" wording; use the sourced nuance in the research file.
- Strip style blocks before running the n-gram check (shared Thrive CSS false positives).

## Candidates evaluated
| Candidate | Result |
|---|---|
| Magento to WooCommerce migration (mapping, breakpoints, stay-test) | Conditional GO |
| "Magento to WooCommerce migration steps / guide" (tool walkthrough) | REJECT: duplicates 29601 H3 and 22251 |
| "Magento vs WooCommerce in 2026" | REJECT: 37776 and 10658 own it, no migration value |
| "Should you leave Magento after end of support?" | REJECT: 42582 and 43110 own it |
| "Magento 1 vs Magento 2" | REJECT: 37552, 43418 |
