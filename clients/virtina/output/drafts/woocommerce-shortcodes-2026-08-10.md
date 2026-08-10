---
title: WooCommerce shortcodes aren't dead: the complete 2026 reference and troubleshooting guide
client: virtina
date: 2026-08-10
slug: woocommerce-shortcodes
stage: draft
brief: clients/virtina/output/briefs/woocommerce-shortcodes-2026-08-10.md
word_count: 2710
headlines:
  - "WooCommerce shortcodes aren't dead: the complete 2026 reference and troubleshooting guide"
  - "Are WooCommerce shortcodes deprecated? No, and here's what's actually happening in 2026"
  - "Stop calling WooCommerce shortcodes deprecated: the 2026 reference and fix guide"
---

```
SEO title (59 chars): Are WooCommerce Shortcodes Deprecated? 2026 Reference Guide
Meta description (155 chars): WooCommerce shortcodes aren't deprecated in 2026. Get the full attribute reference, honest shortcode vs block guidance, and fixes for all 8 failure modes.
URL slug: woocommerce-shortcodes
Primary keyword: woocommerce shortcodes deprecated
Secondary keywords: woocommerce shortcode not working, woocommerce shortcode vs block, woocommerce shortcodes reference, woocommerce shortcodes list, woocommerce shortcode troubleshooting
Search intent: informational / troubleshooting, mix of "is this deprecated" reassurance searches and "not working" diagnostic searches
```

# Are WooCommerce shortcodes deprecated? No, and here's what's actually happening in 2026

Format: E (contrarian thesis), per MUST-FOLLOW-RULES.md section 11 and the brief's format rotation check. Base structure follows section 2 (Summary, Introduction, TOC, body H2s, PAA, Conclusion, FAQ, author bio) using Templates A-M.

[FEATURED IMAGE: WordPress admin screen showing a WooCommerce shortcode entered into a page editor, illustrating shortcode reference and troubleshooting for store owners | concept: a business owner or developer at a desk viewing the WordPress block editor with a WooCommerce shortcode typed into a text field on a laptop screen]

## [H2: Summary]

You read a blog post claiming WooCommerce shortcodes are dead. So you rip `[woocommerce_my_account]` off your account page and brace for a block that never arrives.

Meanwhile your working `[products]` grid runs fine, though you worry it will vanish in the next update. Neither reaction holds up. As of WooCommerce 11.0, released August 4, 2026, all 11 core shortcodes still work exactly as documented.

## [H2: Introduction]

The confusion has a real source. WooCommerce soft-deprecated a set of older product-grid blocks back in WooCommerce 9.5, replacing them with the newer Product Collection block. Somewhere between that change and today, blog posts and plugin changelogs started treating shortcodes and blocks as the same thing.

This guide separates the two clearly, then covers what the official docs and most competitor articles skip. You'll get the complete attribute list for every core shortcode and an honest shortcode-versus-block call. You'll also see how shortcodes behave in block themes and full site editing, plus fixes for eight documented failure modes.

(Table of contents generated automatically from H2 anchors below: Are WooCommerce shortcodes deprecated in 2026 / What are the complete WooCommerce shortcodes and their attributes / Should you use a WooCommerce shortcode or a block / Do WooCommerce shortcodes work on block themes and full site editing / Why is your WooCommerce shortcode not working / People also ask / Conclusion / Frequently asked questions)

## [H2: Are WooCommerce shortcodes deprecated in 2026?]
(anchor id: shortcodes-deprecated)

No, all 11 core WooCommerce shortcodes are fully supported in WooCommerce 11.0, released August 4, 2026. That release's notes list zero shortcode-specific changes.

What actually changed is a set of older product-grid blocks, not the shortcodes themselves. WooCommerce soft-deprecated those blocks back in version 9.5, in favor of the newer Product Collection block.

One shortcode deserves a special note. `[woocommerce_my_account]` has no block-based alternative at all, per WooCommerce's own documentation, so there's no decision to make there yet.

### [H3: What's actually being deprecated (it isn't the shortcodes)]

The Product Collection block now replaces older grid blocks like Products by Category, Best Selling Products, and Products by Tag. WooCommerce announced the change in a [EXTERNAL LINK: Product Collection block announcement | target: developer.woocommerce.com post on the soft-deprecation of product-grid blocks since WC 9.5 | attributes: target="_blank" rel="noopener noreferrer"], framing it as a soft deprecation rather than a removal. Store owners who never touched those specific blocks have nothing to change.

### [H3: Why the confusion started]

Competitor articles and even WooCommerce's own troubleshooting page use loose language that blurs shortcodes and blocks together. Some guides still write as if the classic editor, Gutenberg, and block themes are three separate worlds. The official shortcodes page sits under "Classic themes" and nudges readers toward blocks, without saying shortcodes still work fine elsewhere.

That framing is technically accurate but easy to misread. If you're not planning a [INTERNAL LINK: WooCommerce migration guide | purpose: link to virtina.com/woocommerce-migration-guide/, reassures readers that staying on WooCommerce doesn't force a shortcode-to-block migration] anytime soon, nothing here forces your hand.

## [H2: What are the complete WooCommerce shortcodes and their attributes?]
(anchor id: complete-shortcode-reference)

WooCommerce ships 11 core shortcodes, each with a documented attribute set, and every one still works exactly as built. Nothing on this list changed in WooCommerce 11.0.

### [H3: Product display shortcodes]

The workhorse is `[products]`, which accepts limit, columns, orderby, order, category, tag, attribute, terms, visibility, ids, skus, and class. Category and tag values pull straight from your store's product taxonomy, so slugs have to match exactly. Three special flags, `on_sale="true"`, `best_selling="true"`, and `top_rated="true"`, can't combine with the content attributes above.

```
[products limit="4" columns="4" orderby="popularity" category="apparel"]
```

`[product_page]` pulls a single product by id or sku. `[product_category]` and `[product_categories]` handle category grids. Both use category (required on the singular version), limit or per_page, columns, orderby, order, hide_empty, and parent.

```
[product_category category="hoodies" columns="3" orderby="date" order="DESC"]
```

`[add_to_cart]` and `[add_to_cart_url]` output a standalone buy button using id or sku, plus show_price, style, class, and quantity. `[shop_messages]` takes no attributes. It needs "Enable AJAX add to cart buttons on archives" turned off under WooCommerce > Settings > Products > General to display correctly.

How you configure these attributes also affects what's crawlable on your shop pages. Virtina's [INTERNAL LINK: WooCommerce SEO guide | purpose: link to virtina.com/woocommerce-seo-made-easy/, natural where product-display shortcodes affect what's indexable] covers that side of things if product visibility is a priority.

### [H3: Cart, checkout and account shortcodes]

`[woocommerce_cart]`, `[woocommerce_checkout]`, `[woocommerce_my_account]`, and `[woocommerce_order_tracking]` take no attributes at all. Each renders a full page based on your settings under WooCommerce > Settings > Advanced > Page setup.

`[woocommerce_my_account]` is the one to flag plainly. It has no block-based alternative, so there's nothing to switch to even if you wanted to. Readers building self-service features should see Virtina's [INTERNAL LINK: B2B customer portal | purpose: link to virtina.com/woocommerce-b2b-customer-portal/, natural in the my-account subsection since my-account has no block alternative and connects to portal/self-service content] guide for what's possible beyond the default layout.

One bonus shortcode sits outside the official 11: `[related_products]` takes limit, columns, and orderby, and it doesn't paginate. It's documented on the same official page but isn't part of the core list.

If you eventually need programmatic control beyond what these attributes offer, Virtina's [INTERNAL LINK: WooCommerce REST API guide | purpose: link to virtina.com/guide-on-woocommerce-rest-api/, natural for developers who outgrow shortcode-level customization] guide picks up from here.

Every example above uses straight double quotes, not curly ones. Pasting from Word or Google Docs converts them automatically, and a curly quote breaks the shortcode with no visible error. More on that fix in the troubleshooting section below.

[BODY IMAGE: Developer typing a WooCommerce products shortcode with attributes into the WordPress code editor on a laptop in an office setting | concept: close shot of hands typing shortcode syntax into WordPress's code editor view, laptop on an office desk, straight-quote attribute values visible on screen]

## [H2: Should you use a WooCommerce shortcode or a block?]
(anchor id: shortcodes-vs-blocks)

Use the block version by default for a new store. Fall back to the shortcode only when a payment gateway or extension hasn't declared block compatibility.

### [H3: When the block checkout is the right call]

Blocks give you direct visual control inside the site editor: add trust badges, reorder fields, adjust copy, without a developer. Since WooCommerce 8.3, the Cart block and Checkout block became the default for new installs. Existing stores can switch anytime.

The switch is reversible. Select the block, click Transform in the toolbar, and choose "Classic Shortcode" to fall back instantly if something breaks.

That level of no-code control is exactly what Virtina's [INTERNAL LINK: WooCommerce customization guide | purpose: link to virtina.com/woocommerce-customization-guide/, natural where the piece discusses visual editing control on the block side] guide covers in more depth.

### [H3: When the shortcode is still the correct technical answer]

Extension and payment gateway compatibility is the real deciding factor here, not nostalgia for the old checkout. The block checkout runs on React instead of the classic PHP hook system.

A gateway that hasn't declared block support can silently drop off the block checkout. It may still work fine on the shortcode version.

WooCommerce developer Mike Jolley has said there are "no plans to phase out the classic cart and checkout in core." That's meant to protect stores that depend on older extensions or custom checkout code.

Official documentation also states plainly that in some cases the shortcode version has better extension compatibility. That's WooCommerce acknowledging the shortcode path is sometimes the more reliable choice, not just a legacy fallback.

| Factor | Shortcode (classic) | Block |
|---|---|---|
| Extension and payment gateway compatibility | Generally more reliable for gateways that haven't declared block support | Requires the extension to explicitly declare Cart/Checkout block compatibility |
| Editing workflow | Fixed PHP template, needs code or a compatible page builder to customize | Visual, drag-and-drop editing inside the site editor, no developer required |
| Migration cost and reversibility | No migration needed on existing stores already using it | One-click "Transform to Classic Shortcode" makes switching back instantly reversible |
| My Account availability | Only supported option, no block equivalent exists | Not available |
| Performance | Not documented as faster or slower in any source found | Not documented as faster or slower in any source found |

[TABLE: build using Template N, caption below the table: "Comparison current as of WooCommerce 11.0, August 2026."]

If page speed is the real concern behind this question, neither option is a documented performance advantage on its own. Virtina's [INTERNAL LINK: WooCommerce performance guide | purpose: link to virtina.com/speed-up-woocommerce-without-switching-hosts/, natural where the piece states performance isn't a documented differentiator between shortcode and block] covers the levers that actually move the needle.

[BODY IMAGE: Two coworkers reviewing a WooCommerce shortcode versus block comparison on a laptop screen during an office planning meeting | concept: two people at a shared desk pointing at a laptop screen showing WooCommerce checkout block settings, office background]

## [H2: Do WooCommerce shortcodes work on block themes and full site editing?]
(anchor id: block-themes-fse)

Yes, WooCommerce shortcodes render normally on block themes and inside full site editing templates, with two narrow developer-facing exceptions. Neither exception is a shortcode bug specific to FSE.

### [H3: The two things to actually watch for]

First, the function `wc_current_theme_is_fse_theme()` was deprecated as of WooCommerce 9.9, in favor of WordPress core's `wp_is_block_theme()`. It still works for now, but custom shortcode wrapper code checking theme type this way should switch before removal.

Second, a shortcode pasted into a block that doesn't parse shortcodes will render as literal bracketed text. That includes some custom blocks and page-builder text fields. It's the same root cause documented on classic themes, not something unique to block themes or full site editing.

Shortcodes render fine inside a Shortcode block or a Paragraph block in the block editor. They also work inside a template part in most current setups.

`[woocommerce_order_tracking]` is worth a specific mention here. It reads order data through WooCommerce's own CRUD methods, the correct pattern for High-Performance Order Storage (HPOS). That means it isn't directly affected by an HPOS migration.

Some third-party order-tracking plugins report issues even after declaring HPOS compatibility, according to one technical write-up on the topic. If you're evaluating that migration separately, Virtina's [INTERNAL LINK: HPOS migration guide | purpose: link to virtina.com/woocommerce-hpos-migration/, brief mention that the order-tracking shortcode reads via CRUD methods and isn't directly affected by HPOS] walks through readiness and rollout.

## [H2: Why is your WooCommerce shortcode not working?]
(anchor id: troubleshooting-shortcode-not-working)

Most WooCommerce shortcode failures trace back to one of eight documented causes, and each one has a specific fix. Virtina's [INTERNAL LINK: WooCommerce bug fix guide | purpose: link to virtina.com/woocommerce-bug-fix-guide/, positions this as the shortcode-specific companion to Virtina's general bug guide] covers store-wide issues if the problem turns out to be bigger than one shortcode.

### [H3: Rendering and syntax failures]

1. **Shortcode renders as literal text on the page.** Symptom: the bracketed text shows up exactly as typed instead of running. Cause: it's wrapped in `<pre>` or `<code>` tags, or sits in a text field that doesn't parse shortcodes. Fix: strip the wrapper tags in the Text/HTML view, or use a dedicated Shortcode widget instead.

2. **Curly quotes break the shortcode silently.** Symptom: a shortcode with attributes fails silently, while the same shortcode with no attributes still works. Cause: pasting from Word or Google Docs converts straight quotes into curly ones, which the shortcode parser rejects. Fix: retype the quotes directly in the WordPress editor, or use code view to force straight quotes.

3. **`[products skus="..."]` returns nothing for a variable product.** Symptom: the SKU clearly exists on the product edit screen, but the shortcode returns nothing. Cause: that SKU belongs to a product variation, and the shortcode only matches parent-level SKUs. Fix: pull the SKU from the parent product's Inventory tab, not the individual variation.

### [H3: Display and query bugs]

4. **`[products]` or `[product_category]` shows fewer products than expected.** Symptom: a category with dozens of products displays only a handful, or none. Cause: one report documents a counting bug where the out-of-stock filter excludes items before the limit is applied. Fix: raise the limit to cover the full category, or disable "Hide out of stock items from the catalog" in WooCommerce > Settings > Products > Inventory.

5. **`[products ids="..."]` fails with a very large ID list.** Symptom: passing thousands of IDs returns "No products were found matching your selection" instead of a subset. Cause: reported and unresolved on [EXTERNAL LINK: GitHub issue #31709 | target: github.com/woocommerce/woocommerce/issues/31709 | attributes: target="_blank" rel="noopener noreferrer" | note: describe only as reported and unresolved in the visible thread, never as confirmed open or fixed today], likely a query-length ceiling. Fix: break large ID lists into batches, or query by category instead.

### [H3: Cart, checkout, caching and widget failures]

6. **Cart or checkout renders blank or shows a stale cart.** Symptom: the cart or checkout page loads blank, or shows another visitor's contents. Cause: these pages are per-visitor and dynamic, so aggressive caching, including WooCommerce's own transient cache, can serve stale results if exclusions aren't set. Fix: exclude cart, checkout, and my-account URLs from every caching layer, then purge and retest. See Virtina's [INTERNAL LINK: Checkout troubleshooting guide | purpose: link to virtina.com/woocommerce-checkout-not-working-agency/, natural inside the cart/checkout caching failure case] for a deeper walkthrough.

7. **Elementor 3.33.5 breaks cart or checkout JavaScript.** Symptom: raw JavaScript appears as visible text, and quantity fields stop responding. Cause: a confirmed regression in Elementor version 3.33.5, reproduced on WooCommerce 10.4.2 and WordPress 6.9. Fix: downgrade Elementor to 3.33.4 or earlier until a patched release ships.

8. **Shortcodes in a widget or template part don't execute.** Symptom: a shortcode in a Text widget outputs as plain text instead of running. Cause: WordPress's `widget_text` filter doesn't run `do_shortcode()` on widget content by default. Fix: add a filter to run `do_shortcode` on `widget_text`, or use a block-based Shortcode widget instead.

[BODY IMAGE: Developer debugging a WooCommerce shortcode error in a browser console on a desktop monitor at an office workstation | concept: developer at a desktop computer reviewing browser console error output while troubleshooting a WooCommerce page, office setting]

## [H2: People also ask]
(anchor id: people-also-ask)

### [H3: But doesn't WooCommerce's own site say to use blocks instead?]

The official docs do steer new users toward blocks, but that's a recommendation, not a deprecation notice. All 11 core shortcodes remain fully supported in WooCommerce 11.0, and nothing in the roadmap points to their removal.

### [H3: Will shortcodes eventually be removed?]

No announced removal date exists for any of the 11 core shortcodes. WooCommerce has stated it has no plans to phase out the classic cart and checkout from core. The other shortcodes carry no removal notice at all.

### [H3: Is [products] safe to keep using on a high-traffic store?]

Yes, `[products]` is a supported, documented shortcode with no performance warning attached in current WooCommerce documentation. Set a sensible limit and avoid unbounded queries, the same caching and query discipline you'd apply to any dynamic page.

## [H2: Conclusion]
(anchor id: conclusion)

Shortcodes are safe to keep using wherever they're the right technical fit for your store. The real work isn't migrating away from them out of fear. It's verifying that your extensions and payment gateways have actually declared block compatibility before you switch anything.

If a shortcode is misbehaving, the fix is almost always one of the eight causes covered above. It's rarely a sign the feature is dying.

Check the syntax, check the cache exclusions, check the plugin versions. You'll usually find the answer in minutes, not a migration project.

## [H2: Frequently asked questions]
(anchor id: faq)

**Are WooCommerce shortcodes deprecated?**
No. All 11 core WooCommerce shortcodes are fully supported as of WooCommerce 11.0, released August 4, 2026. That release made no shortcode-specific changes.

**What happened to the WooCommerce product-grid blocks?**
WooCommerce soft-deprecated a set of older product-grid blocks in version 9.5, replacing them with the newer Product Collection block. This affected specific blocks only, not the shortcodes themselves.

**Does `[woocommerce_my_account]` have a block version?**
No. Per WooCommerce's own documentation, `[woocommerce_my_account]` has no block-based alternative at all. The classic shortcode remains the only supported option for that page.

**Why is my shortcode showing as text on the page instead of running?**
It's usually wrapped in `<pre>` or `<code>` tags, or dropped into a text field that doesn't parse shortcodes. Switch to the Text/HTML editor view and remove the wrapper tags, or use a dedicated Shortcode widget.

**Can I use a WooCommerce shortcode inside a block theme?**
Yes. Shortcodes render normally in block themes and full site editing templates, with no exclusive bug documented for that setup. The two developer-facing exceptions are a deprecated theme-detection function and shortcode-parsing conflicts, the same ones that affect classic themes.

**What's the difference between the shortcode and block checkout?**
The block checkout gives visual, no-code editing, while the shortcode checkout renders from a fixed PHP template. Extension and payment gateway compatibility is the deciding factor, not which one looks nicer.

**Why does my `[products skus="..."]` shortcode return nothing?**
The SKU you entered likely belongs to a product variation rather than the parent variable product. Pull the SKU from the parent product's Inventory tab instead, and the shortcode should return results.

**Is it safe to keep the classic cart and checkout shortcodes?**
Yes. WooCommerce has stated it has no plans to phase out the classic cart and checkout from core. That's specifically to protect stores relying on older extensions or custom checkout code.

## [H2: Author bio]

Written by the Virtina eCommerce team. Virtina strategizes, optimizes, and solves for B2B and B2C stores across WooCommerce, Magento, BigCommerce, Shopify, and more.

---

**Internal links used (9):**
1. WooCommerce migration guide → virtina.com/woocommerce-migration-guide/ (Section 1)
2. WooCommerce SEO guide → virtina.com/woocommerce-seo-made-easy/ (Section 2)
3. B2B customer portal → virtina.com/woocommerce-b2b-customer-portal/ (Section 2)
4. WooCommerce REST API guide → virtina.com/guide-on-woocommerce-rest-api/ (Section 2)
5. WooCommerce customization guide → virtina.com/woocommerce-customization-guide/ (Section 3)
6. WooCommerce performance guide → virtina.com/speed-up-woocommerce-without-switching-hosts/ (Section 3)
7. HPOS migration guide → virtina.com/woocommerce-hpos-migration/ (Section 4)
8. WooCommerce bug fix guide → virtina.com/woocommerce-bug-fix-guide/ (Section 5)
9. Checkout troubleshooting guide → virtina.com/woocommerce-checkout-not-working-agency/ (Section 5)

**External links used (2, both within the 2-max cap):**
1. Product Collection block announcement → developer.woocommerce.com (Section 1)
2. GitHub issue #31709 → github.com/woocommerce/woocommerce/issues/31709 (Section 5)

**Semantic terms included:** block editor, Gutenberg, full site editing (FSE), block theme, classic theme, Product Collection block, Cart block, Checkout block, page builder, template part, High-Performance Order Storage (HPOS), payment gateway compatibility, do_shortcode, transient cache, product taxonomy.
