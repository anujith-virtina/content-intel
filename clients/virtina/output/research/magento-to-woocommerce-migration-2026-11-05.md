---
title: Research notes, Magento to WooCommerce migration (what moves, what breaks, when to stay)
client: virtina
date: 2026-11-05
topic: Magento to WooCommerce migration
audience: B2B and B2C ecommerce leaders on Magento or Adobe Commerce evaluating WooCommerce
stage: research
slug: magento-to-woocommerce-migration
---

# Research: Magento to WooCommerce migration

All facts checked 2026-11-05 against primary pages unless flagged. No prices, no vendor percentages, no market-share stats.

## 0. Uniqueness check report (for the analyzer)
- Full audit: `uniqueness-audit-magento-to-woocommerce-2026-11-05.md`.
- Inventory was stale (2026-09-09), refreshed live. Full /pages sweep (3 pages) and /search done. No Magento-to-WooCommerce page or post exists. 404 at `/magento-to-woocommerce-migration/`.
- Checks: 1 PASS, 2 FAIL for user slug (use `leaving-magento-what-moves-breaks`), 3 conditional (29601 H3 "Magento to WooCommerce Migration" is a thin LitExtension walkthrough), 4 PASS, 5 literal FAIL rescued by section 4c sub-niche.
- Related posts whose angle to avoid: 42582 and 43110 (should you leave), 29601 (tool click-steps), 43054 (same mapping idea, Shopify destination), 42177 (Volusion source), 43507 (format source), 37776 and 10658 (feature comparisons).

## 1. Trend evidence (honest)
Moderate signal, low absolute volume. "magento to woocommerce migration" is the top related query for both "woocommerce migration" (100) and "magento migration" (52) and is rising (160) under "magento migration". Seed momentum +12.7% is the only migration seed trending up. Source: `trends-scan-2026-11-05.md`.

## 2. Sub-questions a reader asks
1. What data moves from Magento to WooCommerce, and what does not?
2. Which migration route fits my catalog?
3. What happens to customer logins, URLs and rankings?
4. How do Magento B2B features (groups, shared catalogs, quotes) map to WooCommerce?
5. When should I not move?

## 3. Fact list with sources (primary)

### Magento / Adobe Commerce side
- Export types in the admin (System > Data Transfer > Export): Advanced Pricing, Products, Customer Finances, Customers Main File, Customer Addresses, Stock Sources. CSV default. Runs through a message queue, so cron must run. Special characters can break transfer, so enable Fields Enclosure. Page last updated Oct 8, 2026. Source: https://experienceleague.adobe.com/en/docs/commerce-admin/systems/data-transfer/data-export
- Customer passwords: stored as hash:salt:version. Adobe's example uses SHA256 and Argon 2ID13, default is Argon 2ID13 with Sodium, otherwise SHA256. Raw passwords are not stored. Source: https://experienceleague.adobe.com/en/docs/commerce-operations/configuration-guide/security/password-hashing (surfaced via search; page not fetched directly, so treat the example-format detail as verified from the search extract only).
- Product types documented: simple, configurable, virtual, downloadable, bundle, grouped. Updated Oct 8, 2026. Source: https://experienceleague.adobe.com/en/docs/commerce-admin/inventory/basics/product-types . Gift cards are Adobe Commerce only [unverified at primary level; from third-party extract].
- Product URL suffix is configurable as html or htm, applied automatically. Category path is NOT included in product URLs by default. Updated Oct 8, 2026. Source: https://experienceleague.adobe.com/en/docs/commerce-admin/catalog/catalog/catalog-urls . Do not state that .html is the default; the page does not say so.
- B2B features named: company accounts, company credit ("Pay on Account"), company management hierarchy, shared catalogs, quick order, negotiable quotes, purchase order approvals, requisition lists. Shared catalogs and negotiable quotes are "available only for Commerce stores configured to support Company accounts". The page does not state an edition boundary for the rest. Updated Oct 1, 2026. Source: https://experienceleague.adobe.com/en/docs/commerce-admin/b2b/introduction . [Edition (Open Source vs Adobe Commerce) NOT verified at primary level; do not assert.]
- Hierarchy: global, website, store, store view; stores share one catalog and admin; store views carry language and currency symbol; websites can have their own domain. Updated Oct 8, 2026. Source: https://experienceleague.adobe.com/en/docs/commerce-admin/start/setup/websites-stores-views
- Adobe Commerce support dates: 2.4.6 regular support ended Aug 11, 2026, extended support ends Aug 31, 2027; 2.4.7 regular support May 31, 2027; 2.4.8 May 31, 2028; 2.4.9 (released May 12, 2026) May 31, 2029. Adobe Commerce only, no Open Source dates on page. Updated Oct 14, 2026. Source: https://experienceleague.adobe.com/en/docs/commerce-operations/release/versions
- Not retrieved (404 or not reached): Adobe URL rewrites page, Adobe customer-import page, developer.adobe.com import-export. Whether the Customers Main File export carries the password hash column was NOT verified.

### WooCommerce side
- Core Product CSV Importer/Exporter supports simple, variable, grouped, external, variation, virtual, downloadable. Variation rows need a Parent SKU or id. Images must be reachable or pre-uploaded; first image becomes featured. Match on ID or SKU. Image alt text cannot be set by the core importer. Unrecognized columns are not imported. No fixed size limit; limited by server memory and time, so split large files and test on staging. No last-updated date shown. Source: https://woocommerce.com/document/product-csv-importer-exporter/
- Customer and order import is NOT in core; WooCommerce's own docs route it through the Import Export Suite extension (users, products, reviews, coupons, orders, subscriptions; recommended order: users, products, reviews, coupons, orders, subscriptions). Passwords: the extension accepts plain text and WordPress-hashed passwords; "Retain user passwords" keeps WordPress hashes. Sources: https://woocommerce.com/document/import-and-export-of-woocommerce-users/ and https://woocommerce.com/document/preparing-woocommerce-content-for-migration/
- Official extension "Magento Migration for WooCommerce" (developer FmeAddons): migrates products, customers, orders over an API; Magento 2 only; filters for products, customers (incl. group) and orders; needs ample CPU and memory; configurable batch size; no redirect feature listed; reviews, categories, coupons and passwords not listed either way. Requirements: PHP 7.4, WP 5.0+, WC 5.0+. Source: https://woocommerce.com/products/magento-migration-for-woocommerce/
- FG Magento to WooCommerce: free version migrates categories, products, tags, images, stock and CMS pages; premium adds attributes, variations, grouped products, customers, orders, reviews, coupons, SEO meta, tax classes, Magento-URL redirects and authenticating users with their Magento passwords. Tested Magento 1.3 to 2.4. Customer groups, bundle products, wish lists and tiered prices are only via separate paid add-ons. Page modified Sep 24, 2026. Source: https://wordpress.org/plugins/fg-magento-to-woocommerce/
- LitExtension: lists products, categories, customers, orders, reviews, coupons, taxes, CMS pages. Says passwords can be retained only for supported Magento formats via its own plugin, otherwise a reset flow. Customer groups are NOT recreated automatically; custom modules, themes and extension data need separate assessment; B2B described as potentially unsuited to WooCommerce. Vendor page, treat as vendor claim. Source: https://litextension.com/woocommerce-migration-tool/magento-to-woocommerce.html
- Core tax: tax classes plus rate tables, CSV import/export of rates, a sample file marked not for production. The page does not cover tax-exempt customers. Source: https://woocommerce.com/document/setting-up-taxes-in-woocommerce/
- Permalinks: default product base `product`, category base `product-category`; options Default, Shop base, Shop base with category, Custom base. Source: https://woocommerce.com/document/configuring-woocommerce-settings/permalinks/
- Core product types are simple, grouped, external, variable (importer page adds variation, virtual, downloadable). Product Bundles is a separate paid extension, so Magento bundle products need an extension. Source: https://woocommerce.com/products/product-bundles/
- HPOS: enabled by default on new installs since WooCommerce 8.2 (Oct 2023). If an active plugin is incompatible the HPOS option is disabled; extension developers must add support. Source: https://developer.woocommerce.com/docs/features/high-performance-order-storage/
- REST API: keys tied to a WP user; read/write scopes; permalinks must not be Plain. Source: https://woocommerce.com/document/woocommerce-rest-api/
- WordPress password hashing: 6.8 moved to bcrypt; existing phpass hashes keep working via wp_check_password and are rehashed at next login. The post does not cover importing hashes from other systems. Comment-level claim that MD5 is still accepted [unverified]. Source: https://make.wordpress.org/core/2025/02/17/wordpress-6-8-will-use-bcrypt-for-password-hashing/
- WordPress Multisite: each site has its own content tables, only the user table is shared. Source: https://developer.wordpress.org/advanced-administration/multisite/ . WooCommerce multi-store from one admin with shared catalog is therefore a different model from Magento's store-view hierarchy (inference from the two sources, label as such).
- WooCommerce core B2B: no official WooCommerce page found stating what core lacks. Claim "company accounts, shared catalogs and negotiable quotes need extensions in WooCommerce" is supported only by third-party plugin pages, so phrase it as "core WooCommerce does not list these features in its docs; they come from extensions such as the B2B plugins Virtina already covers" and link 42393. [unverified at primary level]

### Google Search Central
- Site move with URL changes: prepare and test the new site, build old-to-new URL mapping, set server redirects, monitor. Use server-side 301 or 308. Map each old URL to its equivalent; consolidation is fine; do not send many URLs to an irrelevant page such as the homepage; avoid chains, ideally no more than 3 hops. Change of Address tool is only for domain moves, not path changes. Keep redirects at least 1 year. Expect temporary fluctuation; medium sites may take weeks or more. Source: https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes
- Redirects: permanent redirects signal the new URL as canonical; server-side preferred; JavaScript redirects are last resort. Source: https://developers.google.com/search/docs/crawling-indexing/301-redirects
- Site move without URL changes page returned 404; not used.

## 4. Data-mapping view (for the post)

| Magento object | WooCommerce result | Status | Basis |
|---|---|---|---|
| Simple, virtual, downloadable products | Core importer types | Moves cleanly | Woo importer doc |
| Configurable products | Variable products with attribute columns | Moves with cleanup (attributes and variation rows) | Both docs; cleanup need is inference |
| Grouped products | Grouped products | Moves | Both docs |
| Bundle products | No core type; Product Bundles extension | Rebuild | Woo extension page |
| Categories, tags, images | Importer categories use ">" hierarchy; images by URL | Moves; alt text must be added separately | Woo importer doc |
| Customers (main file + addresses) | Needs extension (not core) | Moves via extension or tool | Woo docs |
| Password hashes | Magento SHA256 or Argon 2ID13 is not a WordPress format | Breaks natively; plugin verification or reset | Adobe + WP docs; tools conflict |
| Customer groups | WP user roles plus pricing plugin | Rebuild | LitExtension, FG add-ons |
| Tier and advanced pricing | No core equivalent in docs | Rebuild (plugin) | FG add-on note; Adobe export type |
| Orders and history | Extension or tool; HPOS affects plugin compat | Moves with tool, test HPOS | Woo docs |
| Tax rules | Tax classes and rate CSV | Rebuild and re-enter | Woo tax doc |
| Company accounts, shared catalogs, negotiable quotes, PO approvals, requisition lists | No core equivalent in docs | Rebuild via plugins or custom; main stay-or-go test | Adobe B2B page; Woo docs silent |
| Multi-store / store views | Separate WP sites (Multisite) or plugin model | Rebuild | Adobe hierarchy + WP Multisite |
| Product URLs (suffix, no category path default) | `/product/` base, `/product-category/` | Breaks unless 301 mapped | Adobe URL page, Woo permalinks, Google |
| Extensions and custom modules | No migration path | Rebuild or replace | LitExtension, 3 vendor pages |
| Theme | Not transferable | Rebuild | LitExtension [vendor claim] |
| Saved payment tokens | Held by the gateway | Check portability with processor | Commerce Shop claim [unverified, third-party] |

## 5. Competitor and SERP scan
Queries run: "magento to woocommerce migration" (extended), "Magento to WooCommerce migration what breaks customer groups tier pricing B2B passwords redirects". Positions are as returned by the search tool (US), not a rank tracker.

| # | URL | Domain / who | Date | Est. words | Weaknesses |
|---|---|---|---|---|---|
| 1 | https://wisdmlabs.com/blog/magento-to-woocommerce-migration/ | WisdmLabs (agency) | 2026-06-26 | ~2,000 | No when-not-to; no B2B, redirect, password or SEO coverage; tool sections generic; unsourced market stats; heavy CTA |
| 2 | https://woocommerce.com/products/magento-migration-for-woocommerce/ | WooCommerce marketplace (FmeAddons ext.) | n/a | product page | Magento 2 only; no redirects, passwords or reviews listed; load warning; sells the tool |
| 3 | https://woocommerce.com/posts/how-migrate-from-magento-to-woocommerce/ | WooCommerce blog | 2020-02-06 | ~1,900 | Dated (2020), no B2B, no timeline or cutover, thin SEO (redirect note only), promotes Cart2Cart with prices, no stay case |
| 4 | https://www.thecommerceshop.com/blog/magento-to-woocommerce-migration/ | CommerceShop (agency) | 2026-03-06 | ~2,500 | Best of the set: covers audit, 301 map, passwords, B2B gap. But no when-not-to, unsourced stats and inconsistent cost figures, agency CTAs |
| 5 | https://litextension.com/woocommerce-migration-tool/magento-to-woocommerce.html | LitExtension (tool vendor) | n/a | ~5,000 incl. nav | Vendor claims (zero downtime, guarantees), customer groups and custom modules left to you, no decision guidance |

Also seen: FG Magento to WooCommerce plugin page (wordpress.org), Cart2Cart, eseospace, folio3, shopappy checklist. A shopappy extract advised that stores with complex B2B pricing may be better kept on Magento (not fetched in full).

Gap (what none do): (a) object-by-object mapping table with status; (b) a sourced when-not-to-move test; (c) the password truth (hashes unsupported natively, plugin verify or reset) with the vendor conflict stated; (d) Magento URL structure to Woo permalink change tied to Google's own redirect rules; (e) neutral coverage of the routes including the official extension's Magento-2-only limit; (f) no pricing, no invented stats.

AI answers check: no direct ChatGPT, Perplexity or Gemini query is possible from this toolset. The search tool's own synthesised answer for the keyword listed: official extension (Magento 2 only), LitExtension, FG, Cart2Cart and others, manual CSV, and flagged passwords, themes, extensions and B2B as the limits. So an answerable page needs a route table, a password statement and a B2B/extension caution. Treat this as a proxy, not a measurement.

## 6. Factual conflicts between sources
- Passwords: tool vendors (FG premium, LitExtension) say Magento passwords can be retained via a plugin that verifies legacy hashes; others say they cannot move. Reconciliation consistent with Adobe and WordPress docs: WordPress core cannot verify Magento's hash formats, so either a plugin verifies the old hash at first login and rehashes, or customers reset. Virtina's own page 43054 says Magento passwords "can't be exported"; the new post should say "WordPress cannot verify Magento hashes natively" and avoid contradicting 43054 flatly. Whether the Magento export includes the hash was NOT verified.
- 42582 says most leavers land on WooCommerce (no source). Do not repeat.
- Edition of B2B features (Open Source vs Adobe Commerce) not stated on Adobe's B2B intro page. Do not assert.
- WooCommerce core product-type count varies by source (4 vs 6 vs 7 in the importer). Use the importer page's list.

## 7. Semantic term list (10-15, for coverage)
URL mapping, 301 redirect map, product URL suffix, customer group, tier pricing, shared catalog, company account, negotiable quote, configurable product, variable product, attribute mapping, CSV importer, HPOS, tax class, password hash, staging, cutover, DNS TTL, store view, custom module.

## 8. Recommended unique angle
"Leaving Magento for WooCommerce is a data-mapping job, and the pieces that do not map decide whether you should go." Reader leaves with an object-by-object map (moves / rebuild / breaks), a route chooser, and a stay-or-go scorecard.

Format suggestion (analyzer to confirm after checking the last 10 posts): Format D (decision-tree / playbook), with Template N comparison tables (mapping table, route table). Format B is a fallback for AI-visibility lift.

## 9. H2 skeleton (question headings, direct answer first; min 6 H3 overall)
1. Summary, Introduction, Table of Contents (standard)
2. What moves cleanly from Magento to WooCommerce? (H3: Products and categories; H3: Customers and addresses; H3: Orders and history)
3. What has to be rebuilt instead of moved? (H3: Configurable and bundle products; H3: Customer groups, tier pricing and tax rules; H3: Extensions, custom modules and theme)
4. What breaks on launch day if you do nothing? (H3: Customer passwords; H3: URLs and rankings; H3: Saved payment methods)
5. Which migration route fits your catalog? (route comparison table: manual CSV, official Magento 2 extension, third-party tools, agency build; H3 per route kept short)
6. When should you not move from Magento to WooCommerce? (H3: Heavy company-account and quote workflows; H3: Multi-store hierarchies; H3: Custom modules and deep ERP; H3: Timing around peak season; include a scorecard)
7. What does a safe cutover look like? (numbered checklist from Google's move steps; staging, URL map, DNS TTL, monitoring)
8. People also ask; Conclusion; FAQ (6 to 8)
Keep Path-3 profile wording from 42582 out; link to 42582 and 43110 for the upgrade-or-move decision instead.

## 10. Verified Virtina URLs (checked 2026-11-05)
Method: REST returned status publish and canonical link for each; selected pages also loaded live. WebFetch follows same-host redirects, so 301s are inferred from canonical-link mismatch and from the MUST-FOLLOW verified-dead list.

Link (200, canonical):
- https://virtina.com/platforms/woocommerce-development-services/ (page 43604)
- https://virtina.com/woocommerce-migration-services/ (page 22251, loaded live)
- https://virtina.com/ecommerce-replatform/ (page 20688)
- https://virtina.com/ecommerce-cart-migration/ (page 11175)
- https://virtina.com/migrate-to-woocommerce/ (page 15854; thin, optional)
- https://virtina.com/magento-version-support-cliff-2026/ (42582)
- https://virtina.com/magento-2-4-6-end-of-support-upgrade-or-move/ (43110)
- https://virtina.com/woocommerce-migration-guide/ (29601, once only)
- https://virtina.com/magento-vs-woocommerce/ (37776)
- https://virtina.com/a-comprehensive-guide-to-adobe-commerce-b2b-features/ (38095, loaded live)
- https://virtina.com/woocommerce-b2b-pricing-and-access-setup/ (42393)
- https://virtina.com/woocommerce-b2b-customer-portal/ (42202)
- https://virtina.com/woocommerce-b2b-net-payment-terms/ (42297)
- https://virtina.com/woocommerce-erp-integration/ (42108)
- https://virtina.com/woocommerce-hpos-plugin-compatibility/ (43361)
- https://virtina.com/woocommerce-hpos-migration/ (42037)
- https://virtina.com/redesign-without-losing-rankings/ (43029)
- https://virtina.com/ecommerce-website-migration-checklist/ (34921)
- https://virtina.com/volusion-to-woocommerce-migration/ (42177)
- https://virtina.com/woocommerce-payment-gateway-integration/ (page 42682)
- https://virtina.com/woocommerce-punchout-catalog-integration/ (42329)
- https://virtina.com/b2b-ecommerce-development/ (page 30546)
- https://virtina.com/magento-upgrade-services/ (page 43207)
- https://virtina.com/woocommerce-website-cost/ (43414)
- https://virtina.com/get-in-touch/ (canonical contact)

Sibling pages (do not use as mapping source, link only if natural): https://virtina.com/magento-to-shopify-migration/ (43054), https://virtina.com/woocommerce-to-shopify-migration/ (42997; page REST fetch succeeded, link not separately loaded).

Avoid:
- /woocommerce-development-services/ is 301 to /platforms/woocommerce-development-services/
- /contact/ is 301 to /get-in-touch/
- /adobe-commerce-b2b-features/ loads but is an alias of the long-slug post; use the long form
- /ecommerce-migration-services/, /ecommerce-development-services/, /ecommerce-seo-services/ are 404
- /magento-to-woocommerce-migration/ is 404 (free, not a link target)
- /magento-migration-services/ (200) is about migrating TO Magento; wrong intent, skip
- External links: max 2. Suggested: Google site-move-with-url-changes doc and Adobe export or B2B doc. Never link LitExtension, Cart2Cart, or WooCommerce marketplace competitor domains per brand rule (WooCommerce.com/Adobe are platform vendors and OK; the tool vendors are not).

## 11. Risks
1. Check 2 slug fail and Check 5 literal saturation: need an explicit orchestrator decision (see audit).
2. Overlap with 43054 (same structure, Shopify) and 42582 (stay profiles). Different wording and WooCommerce rows required.
3. Source gaps: Adobe URL-rewrite, customer import and developer pages 404 via fetch; Magento export password hash column unverified; B2B edition boundary unverified; no WooCommerce primary page on what core lacks for B2B. Phrase carefully or cut.
4. Gov-style stat risk: no unsourced stats used; competitor pages carry many (market share, cost ranges, traffic dips). Do not requote any.
5. 43418 was modified today; re-read before drafting for phrase overlap.
6. Product-fit: serves owned themes 2 and 5 plus B2B (theme 1). Not a topic outside brand. Tone must be neutral on WooCommerce, with honest stay cases (brand rule: no blanket dismissals).
7. Image plan: ChatGPT section scenes, no duplicate featured image in body, per memory rules.
