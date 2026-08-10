---
title: WooCommerce shortcodes reference and troubleshooting guide
client: virtina
date: 2026-08-10
topic: woocommerce shortcodes
audience: B2B ecommerce leaders and B2C store operators on WooCommerce, mostly mid-technical, self-diagnosing store problems via Google
stage: research
slug: woocommerce-shortcodes
---

# Research notes: WooCommerce shortcodes

## Strategic framing (confirmed, do not relitigate)

Virtina will not attempt to outrank woocommerce.com for the head term "woocommerce shortcodes." That page is filed under Store design > Classic themes, opens with a note pointing readers to blocks instead, and covers roughly 1,200 words spread across 5 sub-pages. It is the canonical, authoritative source and Google will keep ranking it first for the head term. The opportunity is the long tail: troubleshooting ("[shortcode] not working"), block-theme behavior, and the shortcode-vs-block decision, none of which the official page or any competitor fetched actually covers in depth. See `competitor-analysis-2026-08-10.md` for full detail.

## Uniqueness check (per MUST-FOLLOW-RULES.md section 1 and 4c)

- Grepped `published-posts-inventory.md` (all 1,303 lines, full WooCommerce section of 50 posts) for "shortcode" (case-insensitive): **zero matches.**
- WooCommerce cluster has 50 existing posts — well past the 5-post saturation threshold. Per section 4c, saturation does not block a new post if the sub-niche angle is clearly unique. Shortcode troubleshooting/reference has no existing coverage anywhere in the inventory (WooCommerce, B2B, or otherwise).
- Closest adjacent posts for angle differentiation: `woocommerce-customization-guide` (34029, general customization via themes/plugins/no-code, doesn't touch shortcodes), `guide-on-woocommerce-rest-api` (37434, API not shortcodes), `woocommerce-bug-fix-guide` (40347, general bug list, not shortcode-specific), `woocommerce-checkout-not-working-agency` (40784, hiring-guide angle on checkout failures broadly, not shortcode syntax/rendering issues specifically). None overlap on angle or primary keyword.
- A full formal uniqueness audit (5-check format) should still be run by the analyzer at brief stage per section 1, once title/slug candidates exist. This research confirms no blocking overlap exists for the topic itself.

## 1. Current technical state (verified against official sources, dated)

**Current WooCommerce version as of research date:** WooCommerce 11.0, released August 4, 2026 (developer.woocommerce.com). Release notes for 11.0 focus on guest checkout improvements, an experimental block-based email editor, a new Settings UI, and full deprecation of the Product Editor Beta. **No shortcode-specific changes appear in the 11.0 release notes** — worth stating plainly in the article as reassurance that shortcodes are stable, not a moving target.

### Shortcode support status table

| Shortcode | Status as of WC 11.0 (Aug 2026) | Notes |
|---|---|---|
| `[products]` | Supported | Full attribute set intact (see section 4) |
| `[product_page]` | Supported | Only `id` and `sku` attributes |
| `[product_category]` | Supported | |
| `[product_categories]` | Supported | |
| `[add_to_cart]` | Supported | |
| `[add_to_cart_url]` | Supported | |
| `[shop_messages]` | Supported | Requires disabling "Enable AJAX add to cart buttons on archives" to display correctly |
| `[woocommerce_cart]` | Supported, no longer the default for new installs since WC 8.3 (2023) | See cart/checkout section below |
| `[woocommerce_checkout]` | Supported, no longer the default for new installs since WC 8.3 (2023) | See cart/checkout section below |
| `[woocommerce_my_account]` | Supported | **No block-based alternative exists for My Account** per official docs — this is the one page shortcode with no block replacement |
| `[woocommerce_order_tracking]` | Supported | No block alternative documented |

**Important correction to a common competitor conflation:** none of these 11 shortcodes are formally deprecated. What IS being "soft-deprecated" (as of WooCommerce 9.5, per developer.woocommerce.com) are several older **blocks** — Products by Category, All Products, Best Selling Products, Top Rated Products, Newest Products, On Sale Products, Hand-picked Products, Products by Tag, Products by Attribute — in favor of the newer Product Collection block. Several competitor articles blur this distinction and imply shortcodes themselves are being phased out. That is not accurate as of this research. Source: [Product Collection block—The new default](https://developer.woocommerce.com/2024/11/19/product-collection-block-the-new-default/), [Product Collection block: New JS events and soft deprecation of Product Grid blocks](https://developer.woocommerce.com/2024/11/11/product-collection-block-new-js-events-and-soft-deprecation-of-product-grid-blocks/).

### Cart and checkout: shortcode vs block, in detail

- Starting with **WooCommerce 8.3**, the Cart and Checkout **blocks** became the default for new installations. Existing stores keep whatever version (shortcode or block) they already had unless manually switched.
- WooCommerce has stated no plans to remove the classic shortcode-based cart/checkout from core. Direct quote from WooCommerce developer Mike Jolley (developer.woocommerce.com FAQ, Nov 2023, still consistent with current docs as of this research): "We don't have any plans to phase out the classic cart and checkout in core at this time. These will continue to be supported to ensure backward compatibility for stores that may not be able to migrate due to extensions or customisations." [unverified as current 2026 policy beyond this 2023 statement — no contradicting 2026 source found]
- Official current documentation states plainly: "in some cases the shortcode versions will have better compatibility with extensions" — i.e. WooCommerce itself acknowledges the shortcode path is sometimes the more reliable choice, not just a legacy fallback.
- **Extension/payment gateway compatibility is the real caveat, not the shortcode itself.** Because block checkout relies on React rather than the traditional PHP template/hook system, jQuery-based extensions or payment gateways that hook into the classic checkout process may not render correctly on the block version. A payment gateway must separately declare Cart/Checkout block compatibility — if it hasn't, it may not appear as a payment option on the block checkout even if it works fine on the shortcode checkout. Merchants can check a plugin's product page for a "Compatibility" section to confirm.
- A block can be converted to the classic shortcode placeholder directly in the editor: select the Cart or Checkout block, click "Transform" in the block toolbar, choose "Classic Shortcode." This is a real, current escape hatch worth documenting since it's not obvious to non-developers.
- Practical implication for the decision-guidance section: if a store depends on an older payment gateway, shipping extension, or heavily customized checkout hook that hasn't declared block compatibility, the shortcode checkout is still the correct, supported technical answer in 2026, not a legacy compromise.

### HPOS (High-Performance Order Storage) interaction

- HPOS moves order data out of shared `wp_posts`/`wp_postmeta` tables into dedicated `wc_orders` tables.
- I found **no documented direct incompatibility between HPOS and the 11 core shortcodes** in this list. `[woocommerce_order_tracking]` reads order data through WooCommerce's own object/CRUD methods (the correct HPOS-safe pattern), so it should not be directly affected.
- The real HPOS risk is with **third-party order-tracking plugins** (not the native shortcode) that still read order data via legacy WordPress post APIs instead of `wc_get_order()` and CRUD methods. Some plugins declare HPOS compatibility without having actually updated their data-access code, which can silently return empty or stale order data. Source: [WooCommerce HPOS Is Silently Breaking Your Tracking Plugins](https://seresa.io/blog/data-quality-validation/woocommerce-hpos-is-silently-breaking-your-tracking-plugins) (single source — flag as [unverified] beyond this one article; worth a caution line in the post rather than a confident claim).
- This is a genuinely useful, non-obvious flag for the article: readers using a third-party order tracking plugin alongside `[woocommerce_order_tracking]` should verify actual HPOS compatibility, not just the checkbox declaration.

### Block themes / Full Site Editing (FSE) behavior

- WooCommerce blocks are designed to work with most modern themes but perform best with themes built specifically for FSE.
- Using WooCommerce with an up-to-date block theme requires no special setup for the built-in shop functionality — it works out of the box.
- Relevant developer-facing detail: the function `wc_current_theme_is_fse_theme()` was deprecated as of **WooCommerce 9.9**, in favor of WordPress core's `wp_is_block_theme()`. This matters for any developer-written code (custom shortcode wrappers, theme conditionals) still checking theme type with the old function — it still works in 9.9 but faces future removal. Source: [Developer advisory: Deprecation of wc_current_theme_is_fse_theme()](https://developer.woocommerce.com/2025/05/12/developer-advisory-deprecation-of-wc_current_theme_is_fse_theme/).
- Practical shortcode-in-block-theme behavior: shortcodes render fine inside a Shortcode block or a Paragraph block in the block editor, and inside a template part, in most current setups. The real-world failures reported are not "shortcodes fundamentally don't work in FSE" but narrower: a shortcode pasted into a block that doesn't parse shortcodes correctly (some custom/ACF blocks, some page-builder text widgets), or wrapped in `<pre>`/`<code>` tags by the editor. [unverified as an FSE-specific finding — the failure mode is the same one documented for classic themes; I did not find evidence of an FSE-exclusive shortcode bug, and should not claim one exists without a source]

## 2. Complete attribute reference (verified from official woocommerce.com docs, accuracy over completeness)

### `[products]`
- `limit` — number to display, default `-1` (all)
- `columns` — default `4`
- `paginate` — `true`/`false`, default `false`
- `orderby` — `title` (default), `date`, `id`, `menu_order`, `popularity`, `rand`, `rating`
- `order` — `ASC` (default) or `DESC`
- `skus` — comma-separated SKU list
- `category` — comma-separated category slugs
- `cat_operator` — `IN` (default), `NOT IN`, `AND`
- `tag` — comma-separated tag slugs
- `tag_operator` — `IN` (default), `NOT IN`, `AND`
- `attribute` — attribute slug
- `terms` — comma-separated attribute terms
- `terms_operator` — `IN` (default), `NOT IN`, `AND`
- `visibility` — `visible` (default), `catalog`, `search`, `hidden`, `featured`
- `ids` — comma-separated post IDs
- `class` — custom CSS wrapper class
- Special (cannot combine with content attributes above): `on_sale="true"`, `best_selling="true"`, `top_rated="true"`

### `[product_page]`
- `id` — product ID
- `sku` — product SKU (alternative to id)

### `[product_category]`
- `category` — category ID, name, or slug (required)
- `limit` / `per_page` — number of products, default all
- `columns` — default `4`
- `orderby` — `title` (default), `date`, `id`, `menu_order`, `popularity`, `rand`, `rating`
- `order` — `ASC` (default) or `DESC`

### `[product_categories]`
- `ids` — specific category IDs
- `limit` / `number` — default `0` (all)
- `columns` — default `4`
- `hide_empty` — `0` or `1`, default `1`
- `parent` — category ID, `0` shows top-level only
- `orderby` — `name` (default), `id`, `slug`, `menu_order`, `include`
- `order` — `ASC` (default) or `DESC`

### `[add_to_cart]`
- `id` — product ID
- `sku` — product SKU (alternative)
- `show_price` — `TRUE`/`FALSE`, default `TRUE`
- `style` — inline CSS (developer-level)
- `class` — additional CSS class
- `quantity` — only functions via theme template implementation, not universally

### `[add_to_cart_url]`
- `id` — product ID
- `sku` — product SKU

### `[shop_messages]`
- No attributes. Requires "Enable AJAX add to cart buttons on archives" to be disabled (WooCommerce > Settings > Products > General) for messages to display on non-WooCommerce pages.

### `[woocommerce_cart]`, `[woocommerce_checkout]`, `[woocommerce_my_account]`, `[woocommerce_order_tracking]`
- No documented attributes for any of the four page shortcodes. They render the full page based on WooCommerce settings (Settings > Advanced > Page setup), not shortcode parameters.

### `[related_products]` (not in the official 11-shortcode list, but documented on the same official page and worth a passing mention)
- `limit` — no documented default limit; does not paginate
- `columns` — default `4`
- `orderby` — default random; accepts `price` or `title`

## 3. Troubleshooting cases (sourced from real reports, symptom → cause → fix)

1. **Shortcode renders as literal text on the page instead of executing.**
   Symptom: the bracketed text `[products limit="4"]` shows up verbatim on the front end. Cause: the shortcode is wrapped in `<pre>` or `<code>` tags, usually from pasting into the Text/Code editor view, or placed inside a block that doesn't parse shortcodes (a Paragraph block behaves fine; some third-party or ACF blocks and page-builder "Text" widgets sanitize/escape the brackets). Fix: edit the page, switch to the Text/HTML view, and strip any `<pre>`/`<code>` wrapper; in page builders, use a dedicated Shortcode widget instead of a generic text field. Source: [official WooCommerce troubleshooting doc](https://woocommerce.com/document/woocommerce-shortcodes/troubleshooting-shortcodes/), corroborated by an open [WordPress.org support thread](https://wordpress.org/support/topic/woocommerce-shortcodes-not-working-4/) (WordPress 6.8.3, WooCommerce 10.3.4, Genesis theme) where this remained unresolved after theme-switch troubleshooting — a real, current, unresolved-in-the-wild case worth citing as evidence the problem persists.

2. **Curly ("smart") quotes break the shortcode silently.**
   Symptom: shortcode with attributes fails with no visible error; a plain `[products]` with no attributes still works. Cause: word processors or some editors auto-convert straight quotes (`"`) to curly quotes (`"` `"`), and WordPress's shortcode parser requires straight quotes around attribute values. Fix: retype the quotes directly in the WordPress editor rather than pasting from Word/Google Docs, or use the code view to force straight quotes. Source: [official WooCommerce troubleshooting doc](https://woocommerce.com/document/woocommerce-shortcodes/troubleshooting-shortcodes/).

3. **`[products skus="..."]` returns nothing for a variable product.**
   Symptom: SKU-based shortcode returns empty even though the SKU visibly exists on the product edit screen. Cause: the SKU entered belongs to a product *variation*, not the parent variable product — the shortcode only matches parent-level SKUs. Fix: use the SKU from the parent variable product's Inventory tab, not the individual variation's SKU field. Source: [official WooCommerce troubleshooting doc](https://woocommerce.com/document/woocommerce-shortcodes/troubleshooting-shortcodes/).

4. **`[products]` or `[product_category]` shows fewer products than expected, or none, in a category with out-of-stock items.**
   Symptom: a category with 35 products only shows a handful, or none, via shortcode. Cause: a documented counting bug — the shortcode applies "hide out of stock items" at render time but counts against the raw, unfiltered product set first. If the first N products checked are out of stock, they get excluded from the count entirely rather than backfilled with the next in-stock product. Fix: as a workaround, set `limit`/`per_page` high enough to cover the full category so filtering happens after the full set is retrieved, or disable "Hide out of stock items from the catalog" under WooCommerce > Settings > Products > Inventory if out-of-stock display is acceptable. Source: [Websavers: WooCommerce shortcodes not showing all products](https://websavers.ca/woocommerce-shortcodes-not-showing-products) [unverified beyond this single source — flag as a real but not independently corroborated bug report].

5. **`[products ids="..."]` with a very large ID list returns "No products were found matching your selection."**
   Symptom: passing thousands of product IDs (reported case: over 4,000) to the `ids` attribute causes the shortcode to fail entirely instead of showing a subset. Cause: not resolved by WooCommerce core maintainers in the thread; likely a query-length or performance ceiling. Fix: no confirmed fix; practical workaround is to break large ID lists into smaller batches or use a category/tag-based query instead of listing every ID. Source: [GitHub issue #31709, woocommerce/woocommerce](https://github.com/woocommerce/woocommerce/issues/31709) — confirmed bug, marked "needs: developer feedback," left open/unresolved in the visible thread. Flag as [unverified current status] since I could not confirm if it has since been closed.

6. **Cart or checkout page renders blank, or shows a stale cart, especially right after a caching plugin or hosting change.**
   Symptom: the cart/checkout page loads empty for a returning visitor, or worse, shows another visitor's cart contents. Cause: cart, checkout, and my-account pages must never be served from cache because their content is per-visitor and dynamic; aggressive full-page caching (WP Super Cache, W3 Total Cache, LiteSpeed Cache, Cloudflare APO, or server-level/host caching) can cache these pages if exclusions aren't configured, especially after a plugin update resets settings. Fix: explicitly exclude the cart, checkout, and my-account URLs from every caching layer (plugin, CDN, and server/host-level), then purge all caches and retest. Source: pattern independently confirmed across multiple caching-focused troubleshooting guides found in the same search (Kind-of-Lost, SeedProd, Business Bloomer) — treated as a well-established consensus fact rather than a single-source claim.

7. **Elementor breaks WooCommerce cart/checkout JavaScript after a specific update.**
   Symptom: raw JavaScript renders as visible text on the page, cart quantity fields stop responding, browser console shows errors like `Cannot read properties of undefined (reading 'tools')`. Cause: confirmed regression in Elementor 3.33.5 (working fine in 3.33.4 and earlier), reproduced on WooCommerce 10.4.2, WordPress 6.9, PHP 8.4.5. Fix: downgrade Elementor to 3.33.4 or earlier until a patched version ships; the issue was marked "solved"/closed in the tracker but the fetched content did not show the exact patched version number. Source: [GitHub issue #33898, elementor/elementor](https://github.com/elementor/elementor/issues/33898). This is the strongest, most specific, most current page-builder-conflict case found and worth featuring prominently since it names exact version numbers.

8. **Shortcodes placed inside a widget or template part don't execute.**
   Symptom: a shortcode pasted into a Text widget (classic widgets) or certain template parts outputs as plain text rather than running. Cause: by default, WordPress's `widget_text` filter does not run `do_shortcode()` on widget content in some setups/themes. Fix: add `add_filter('widget_text', 'do_shortcode');` to the theme's functions.php, or use a block-based widget/Shortcode block instead of the legacy Text widget. Source: pattern confirmed across multiple search results including fixrunner.com and general WordPress shortcode documentation; this is a long-standing, well-documented WordPress-level behavior, not WooCommerce-specific, but frequently the actual cause when a reader reports "shortcode works on the page but not in my sidebar."

## 4. Shortcodes vs blocks: honest decision guidance

What genuinely informs the choice, based on findings above:

- **Extension and payment gateway compatibility is the single biggest deciding factor for cart/checkout.** If a store runs a payment gateway or extension that has not declared Cart/Checkout block compatibility, the block checkout can silently drop that payment option or break the flow. The shortcode/classic checkout remains the reliable, supported choice in that case — this is not nostalgia, it's a documented current limitation.
- **My Account has no block equivalent at all.** For `[woocommerce_my_account]`, there is no "which should I use" decision to make — the shortcode/classic page is still the only supported path as of this research.
- **Editing workflow favors blocks for cart/checkout when extensions are compatible.** Blocks give merchants direct visual control (add trust badges, reorder fields, adjust copy) inside the site editor without a developer; the shortcode path renders from a fixed PHP template that generally requires code or a compatible page builder to customize visually.
- **Migration cost is asymmetric.** Moving from shortcode to block cart/checkout is a low-risk, reversible one-click "Transform" action per block once compatibility is confirmed. There is no forced migration; WooCommerce has stated no plans to remove the classic versions.
- **Performance is not a meaningfully documented differentiator either way** in the sources found — no competitor or official source presented benchmarked load-time data comparing shortcode vs block cart/checkout. This should be stated honestly as unproven rather than asserted either direction.
- **Bottom line for the article's decision framework:** default to blocks for new stores and for any store whose payment/shipping extensions have declared compatibility. Stay on or move to the shortcode/classic version if a critical extension or gateway hasn't declared block compatibility, if the store has heavy custom checkout-hook code, or if the store is on a page builder with better shortcode support than block support.

## 5. Semantic term list (10-15 terms for natural inclusion)

block editor, Gutenberg, full site editing (FSE), block theme, classic theme, Product Collection block, Cart block, Checkout block, Store API, page builder, template part, transient cache, High-Performance Order Storage (HPOS), payment gateway compatibility, product taxonomy, do_shortcode

## 6. Internal link candidates (all verified HTTP 200 live on virtina.com as of 2026-08-10)

| Anchor topic | URL | Relevance |
|---|---|---|
| HPOS migration | https://virtina.com/woocommerce-hpos-migration/ | Direct source for the HPOS caveat section |
| Checkout not working | https://virtina.com/woocommerce-checkout-not-working-agency/ | Adjacent troubleshooting angle, checkout failures |
| WooCommerce bug fixes | https://virtina.com/woocommerce-bug-fix-guide/ | General bug list, natural link from troubleshooting section |
| Store speed without switching hosts | https://virtina.com/speed-up-woocommerce-without-switching-hosts/ | Performance angle for the shortcode-vs-block performance discussion |
| WooCommerce REST API guide | https://virtina.com/guide-on-woocommerce-rest-api/ | Adjacent developer-facing content, natural for the attributes/technical sections |
| WooCommerce customization guide | https://virtina.com/woocommerce-customization-guide/ | Broader customization context, natural link from decision-guidance section |
| WooCommerce SEO guide | https://virtina.com/woocommerce-seo-made-easy/ | For any note on shop page/product display SEO |
| B2B customer portal | https://virtina.com/woocommerce-b2b-customer-portal/ | For the my-account shortcode section, since my-account has no block alternative and connects to portal/self-service content |
| WooCommerce migration guide | https://virtina.com/woocommerce-migration-guide/ | For readers evaluating platform-level decisions adjacent to shortcode/block choices |

All 9 URLs confirmed to load with matching titles/content via direct fetch on 2026-08-10. None returned a 404 or redirect-to-home pattern. Recommend the creator select 5-9 of these based on natural fit per section (MUST-FOLLOW-RULES.md requires 5-10 total internal links).

## 7. What I could not confirm (flagged honestly)

- No confirmed, sourced evidence of an FSE/block-theme-exclusive shortcode rendering bug distinct from the same causes that break shortcodes on classic themes (pre-tags, block-parsing conflicts). Do not claim block themes uniquely break shortcodes without a source — I did not find one.
- The out-of-stock counting bug in `[products]`/`[product_category]` (case 4) rests on a single source (Websavers) and I could not independently corroborate it against a second source or an official WooCommerce bug tracker entry. Flag as real-but-single-sourced in the draft.
- GitHub issue #31709 (large ID list failure) status could not be confirmed as still open vs. since resolved — the fetched content showed no maintainer resolution in the visible thread, but issue trackers can be updated after a fetch. Present as "reported, unresolved as of the visible thread" rather than "confirmed open bug in WC 11.0."
- The HPOS/order-tracking-plugin risk (seresa.io) is single-sourced. It's a reasonable, technically plausible caution (CRUD API vs legacy post API) but should be framed as a caution to verify, not a confirmed widespread failure.
- Could not fetch diviflash.com/woocommerce-shortcodes/ (HTTP 403) despite it ranking in the initial search results — excluded from competitor analysis rather than guessed at.
- No rank-checker tool was used to confirm actual live Google SERP positions; search-tool result order was used as an approximation and flagged as such in the competitor file.
