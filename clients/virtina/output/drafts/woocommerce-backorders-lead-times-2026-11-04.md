---
title: "WooCommerce backorders for B2B: how to set lead times, cap orders and avoid overselling"
client: virtina
date: 2026-11-04
slug: woocommerce-backorders-lead-times
stage: draft
brief: clients/virtina/output/briefs/woocommerce-backorders-lead-times-2026-11-04.md
format: B (conversational Q&A body)
seo_title: WooCommerce Backorders for B2B: Set Lead Times | Virtina
meta_description: Learn what the three WooCommerce backorders settings do for B2B, how to set lead times, limit open orders and avoid overselling. Checked on WooCommerce 11.2.1.
focus_keyword: WooCommerce backorders
word_count: 2900
headlines:
  - WooCommerce backorders for B2B: lead times, caps and overselling
  - How to set up WooCommerce backorders without overselling to B2B buyers
  - WooCommerce backorders: what core does, what it skips and what to add
---

[FEATURED IMAGE: Purchasing manager in a distribution warehouse aisle checking a stock list while planning WooCommerce backorders for B2B buyers | concept: A purchasing manager standing in a distribution warehouse aisle, checking a printed stock list against a pallet rack with a visible gap. Wide composition with room to crop.]

[SUMMARY]

WooCommerce backorders let you sell a stocked product past zero, but core only records the promise. This guide shows what each Allow backorders value does, how to message a lead time and how to limit exposure.

It also covers the ERP and webhook points where backorder state can drift. Every claim traces to a named source, checked on WooCommerce 11.2.1.

[INTRODUCTION]

A distributor's buyer adds a large quantity of one part to the cart late on a Tuesday. Only a few units sit on your shelf. WooCommerce accepts the order anyway.

Your team learns about it from a single staff email, if anyone reads that inbox. By then the buyer expects every unit this week.

Should you allow backorders on a B2B store, and how do you keep them from becoming overselling? This guide covers the three Allow backorders values, the lead-time message, the cap problem and the ERP touchpoints.

**How this was checked:** every point was checked against WooCommerce 11.2.1 on 4 November 2026. That release is current on WordPress.org's plugin page, updated 9 October 2026. Settings and fields come from WooCommerce's documentation and the REST API v3 schema.

Cart, stock and email behavior comes from source code, and the text says so each time. Product fields were read at release 11.2.1. Other code behavior was read from the development branch on the same date.

Confirm code-based points with a test order on your version. Nothing here was measured on a live store.

[TOC: sections 1 to 8 H2s, then People Also Ask, Conclusion, Frequently asked questions, Sources and verification]

[H2: What is a backorder in WooCommerce, and when does it suit a B2B store?]

A backorder is an order WooCommerce accepts for a product that has run out of stock. The product sits at zero or below, yet the buyer can still place the order. WooCommerce calls the stock status On backorder.

In Virtina's view, a backorder is a promise to a buyer. Core records that promise only as a product setting. Back it with a lead time, a limit you enforce, a mailbox someone reads and a clean ERP path.

[H3: How is a backorder different from a pre-order?]

Pre-orders come from a separate WooCommerce extension, while backorders are a setting on a product you already stock. The WooCommerce Pre-Orders page describes an optional availability date and a choice to charge upfront or on release. It also describes its own pre-order order status.

In Virtina's view, use a backorder for a SKU that has been in stock. Use a pre-order for a SKU you have not released yet.

[H3: Should you allow backorders, show out of stock, or hide the product?]

You have three choices for a product at zero stock. You can allow backorders, show the product as out of stock, or hide it. WooCommerce's Products settings page lists an Out of stock visibility setting for the hiding option.

A waitlist is a middle path. The Back In Stock Notifications extension emails sign-ups when stock returns, according to the vendor's own page. Seasonal timing changes the answer, so read the [INTERNAL LINK: holiday readiness checklist | purpose: /woocommerce-holiday-season-checklist/] before peak weeks.

[H2: What do the three Allow backorders settings do?]

The Allow backorders field has three values: "Do not allow", "Allow, but notify customer" and "Allow". The [EXTERNAL LINK: WooCommerce product editor settings | url: https://woocommerce.com/document/managing-products/product-editor-settings/ | target=_blank rel="noopener noreferrer"] page documents each one on the product Inventory tab. In the REST API and in code, the keys are `no`, `notify` and `yes`.

The table below sums up each value. It draws on that documentation and on current WooCommerce code.

[TABLE: What each Allow backorders value does for the buyer and the cart]

| Setting (API value) | What the buyer sees | Cart quantity check | B2B fit (Virtina view) |
|---|---|---|---|
| Do not allow (`no`) | The product turns Out of stock at zero and cannot be bought. | The cart blocks a quantity above stock minus stock held by other pending orders (current code). | Fits made-to-order or unconfirmed-supply SKUs. |
| Allow, but notify customer (`notify`) | A backorder notice on the product page, block cart and checkout, the order and customer emails. | Skipped, so stock does not limit the quantity (current code). | Safer default for stocked SKUs with a supplier date. |
| Allow (`yes`) | Backorders are accepted and the product looks like an in-stock item. | Skipped, so stock does not limit the quantity (current code). | Use only when the delay is invisible to the buyer. |

Last column is Virtina's opinion, not WooCommerce documentation.

[H3: Which Allow backorders value fits a B2B store?]

For most B2B stores, "Allow, but notify customer" is the safer default, in Virtina's view. Plain Allow makes the product look like it is in stock. The buyer sees no delay, so the buyer calls sales when the shipment runs late.

The notify value puts the delay in front of the buyer before the order is placed. Choose "Do not allow" for SKUs where you cannot confirm any supply.

[H3: What happens if Manage stock is switched off?]

With Manage stock off, you can set On backorder by hand, but only the product page shows a notice. Cart, checkout, order and email notices are not shown. The Allow backorders field is hidden too, because it appears only when Manage stock is checked.

Turn on Manage stock for any SKU you plan to backorder. Otherwise your buyer sees the delay on one page only.

[BODY IMAGE: 1 | What do the three Allow backorders settings do? | An ecommerce manager at an office desk comparing a handwritten notepad of SKU numbers with a laptop. Laptop angled so the screen is not legible.]

[H2: How do you set up backorders on a product?]

Turn on Manage stock for the product, then pick a value in the Allow backorders field. WooCommerce's Products settings page lists the store-wide inventory settings. The product Inventory tab can override them.

[H3: Which steps set up a backordered product?]

General stock setup is covered in [INTERNAL LINK: WooCommerce inventory management | purpose: /woocommerce-inventory-management/]. The steps below focus on what a backorder needs.

- **Step 1.** Open the store-wide Inventory settings. Confirm Manage stock is on, the backorder notification is on (the default) and the recipients are set.
- **Step 2.** Open the product, go to the Inventory tab and tick Manage stock.
- **Step 3.** Enter the quantity you hold.
- **Step 4.** Choose a value in the Allow backorders field.
- **Step 5.** Keep the store default low stock threshold and out-of-stock threshold, or set one for this product. Current code defaults the low stock level to 2 and the no-stock level to 0.
- **Step 6.** View the product page and add the item to the cart.
- **Step 7.** Place a test order past zero, then read the staff email and the order notes.

Run this test on a staging copy if you can. You will see the notice, the stock quantity and the email in one pass.

[H3: How do variable products and bulk edits behave?]

On variable products, the parent quantity covers every variation unless the parent leaves Manage stock off. If the parent leaves it off, the setting on each variation applies. A catalog with sizes or pack sizes may need that choice made per variation.

The product CSV importer documentation lists the columns for bulk edits. They are `Stock`, `In stock?`, `Low stock amount` and `Backorders allowed?`, which takes 1, 0 or notify. A number in `Stock` turns stock management on, and a blank value turns it off.

[H2: What do buyers and your team see when a backorder is placed?]

Buyers see a notice under the notify setting, and your team gets an email, not a status. Under plain Allow, the product looks like any in-stock item.

[H3: What does the buyer see, page by page?]

Under Allow, but notify customer, WooCommerce's product editor documentation lists a notice in five places. They are the product page, the block cart, block checkout, the order and customer emails.

This post says only that buyers see a backorder notice. It does not quote the text. The shortcode-based cart and checkout are not covered here, so check your own store.

[H3: Who receives the backorder email, and what does it say?]

The backorder email goes to your stock notification recipients, not to the buyer. In current WooCommerce code, it names the units backordered and the order number. WooCommerce's Products settings page says the alert is on by default.

It fires only when stock is managed and backorders are allowed. If nobody reads that mailbox, the signal is lost, which is an inference from where the email goes. If staff or buyer emails never arrive, read [INTERNAL LINK: WooCommerce emails not sending | purpose: /order-emails-not-sending/].

[H3: Why is there no backorder order status?]

WooCommerce's default order statuses include none for backorders, and the order gets no backorder note. WooCommerce's order statuses documentation lists the default statuses and never mentions backorders. Stock reduces when an order reaches Processing or On hold, and it returns on Cancelled or Failed.

In Virtina's view, track open backorders in a report or in the ERP, not in the order status. Keep one list of every open order that contains a backordered line.

[H2: How do you show a lead time on backordered items?]

WooCommerce's documented product fields include no restock date, so a lead time needs your own wording or an extension. A notice that only says an item is backordered gives the buyer nothing to plan around.

[H3: What should a lead-time message say?]

A good lead-time message names a ship-by week or date you can keep. It also says what happens if the date slips and who the buyer should ask.

In Virtina's view, take the date from the supplier's confirmed purchase order, not from a guess. A notice with no date makes a buyer call sales. Do not promise a date you have not confirmed.

[H3: Which extensions add lead times or waitlists?]

The Product Lead Time extension lists separate lead times for in-stock, out-of-stock and backorder products, according to the vendor's page. Plugify makes it. Its page says it shows them on shop, product, cart and checkout pages.

Back In Stock Notifications is a waitlist that emails sign-ups when stock returns. Pre-Orders, covered earlier, handles items not yet released. Every claim here comes from the vendor's own page.

Check each vendor page for version support. Then run the checks in [INTERNAL LINK: HPOS plugin compatibility | purpose: /woocommerce-hpos-plugin-compatibility/] before you install anything on a live store.

[BODY IMAGE: 2 | How do you show a lead time on backordered items? | A warehouse receiving clerk in a hi-vis vest scanning a carton barcode with a handheld scanner at a loading dock as an inbound pallet arrives.]

[H2: How do you cap backorders and avoid overselling?]

WooCommerce's documented fields include no backorder cap, so you enforce the limit with policy and monitoring. So in this post, "cap orders" is a practice Virtina recommends, not a core setting.

[H3: How can one large account order oversell a SKU?]

One large account order can commit more units than you have, because the cart skips its stock check. In current WooCommerce code, this applies to stock-managed products that allow backorders.

Here is an illustrative example, not a client case. A distributor's account orders a pallet-sized quantity of a SKU with a handful of units left.

Allow is on, so the cart accepts the order. Stock goes below zero. The only signal is one staff email.

Sales learns the size of the gap only when it asks the supplier for a date. The example shows a mechanism, not a result.

[H3: What caps exposure when core has no cap field?]

Three practices cap your exposure, and all three are Virtina recommendations, not documented settings. First, publish only supplier-confirmed inbound units as the sellable quantity, and hold back safety stock. Second, watch the negative quantity and the staff email.

Switch the SKU to "Do not allow" once committed units reach the supplier-confirmed number. Third, have a developer add a rule in code and test it on staging. [INTERNAL LINK: WooCommerce development services | purpose: /platforms/woocommerce-development-services/] cover custom stock rules of this kind.

That third option is not a documented setting. Two settings look like caps but are not. Hold stock reserves stock only for Pending payment orders.

Sold individually limits each order to one unit but does not stop separate orders. Any rule that differs by account must come from a plugin or custom code you verify. Setup for [INTERNAL LINK: B2B customer groups | purpose: /woocommerce-b2b-pricing-and-access-setup/] sits in a separate guide.

[H3: Why does negative stock matter?]

Stock can go below zero, and current WooCommerce code fires a backorder action whenever it does. The action is `woocommerce_product_on_backorder`, confirmed at release 11.2.1. Negative stock is an expected state, not an error.

Confirm how your ERP reads a negative quantity before you rely on it. This post does not assert how any specific ERP behaves. Overselling bugs have other causes too, listed in [INTERNAL LINK: common WooCommerce bugs | purpose: /woocommerce-bug-fix-guide/].

[BODY IMAGE: 3 | How do you cap backorders and avoid overselling? | An operations manager and a finance colleague at a meeting table, one pointing at a line on a printed open-orders report beside a supplier purchase-order folder, notes in hand.]

[H2: How do you keep ERP and WooCommerce stock in step?]

Your ERP writes stock into WooCommerce through REST or CSV, and WooCommerce reports orders to the ERP through webhooks. Stock sync design, batch versus real-time updates and the system of record belong to [INTERNAL LINK: WooCommerce ERP integration | purpose: /woocommerce-erp-integration/]. This section names only the points that touch backorder state.

[H3: Which REST fields control backorder state?]

Five fields in the WooCommerce REST API v3 schema, read at release 11.2.1, control backorder state. They are `manage_stock`, `stock_quantity`, `stock_status`, `backorders` and `low_stock_amount`. The `backorders` field takes `no`, `notify` or `yes`.

The fields `backorders_allowed` and `backordered` are read-only, so `backorders` is the writable control. When stock is managed, the quantity drives the status.

In Virtina's view, write the quantity from your ERP and let it drive the status. The [INTERNAL LINK: WooCommerce REST API guide | purpose: /guide-on-woocommerce-rest-api/] is a general API reference, not backorder documentation.

[H3: What happens when your ERP endpoint stops responding?]

WooCommerce disables a webhook after more than five consecutive failed deliveries and stops sending until someone re-enables it. The [EXTERNAL LINK: WooCommerce webhooks documentation | url: https://woocommerce.com/document/webhooks/ | target=_blank rel="noopener noreferrer"] counts any response other than 2xx, 301 or 302 as a failure. Deliveries are logged under WooCommerce, Status, Logs.

The documentation does not describe retries. Do not assume them. In Virtina's view, monitor webhook status and alert when it shows Disabled.

[H2: What does WooCommerce core not do for backorders?]

WooCommerce's documented settings include no backorder cap, no restock date and no backorder order status. The list below pulls together the gaps this post found.

- No maximum backorder quantity and no expected restock date appear in the documented product fields.
- No backorder status appears in the default order statuses, and current code adds no backorder order note.
- The dedicated backorder email goes to your staff, not the buyer. The buyer's notice reaches the order and customer emails only under the notify setting.
- Pre-orders come from a separate extension.

[H3: Which backorder questions should you test on your own store?]

Test the following on your own store, because no source was read for them. Check how the shortcode-based cart and checkout treat backorders. Check any rule that differs by customer group or role.

Check how order quantity minimums interact with backorders. Check when your gateway takes payment on a backordered order, and how your accountant books it. Check how partial or split shipments work.

Check whether each extension works with your theme, ERP and B2B plugin. A failing result is a developer job, and a [INTERNAL LINK: WooCommerce bug fix | purpose: /woocommerce-bug-fix/] engagement can cover broken stock behavior.

[H2: People Also Ask]

[H3: What does on backorder mean in WooCommerce?]

On backorder is one of three stock statuses, next to In stock and Out of stock. With Manage stock on, the status follows the quantity. With it off, you set the status by hand.

[H3: How do you turn backorders off for one product?]

Set Allow backorders to "Do not allow" on the product's Inventory tab. The field appears only when Manage stock is checked. A product setting overrides the store-wide one.

[H3: Is a backorder the same as a pre-order?]

No, in Virtina's view. A backorder covers a SKU you normally stock, and a pre-order covers a SKU not yet released. Pre-orders come from a separate WooCommerce extension.

[H3: Can you allow backorders on one variation only?]

Yes, when the parent does not manage stock, because each variation's own setting then applies. If the parent manages stock, its quantity covers every variation.

[H2: Conclusion]

A backorder is a promise. WooCommerce core records it as a setting, and nothing more.

So the store needs four things around it. Set a lead time the buyer can plan around, and enforce your own limit. Make sure someone reads the stock mailbox, and monitor the ERP path.

Place one test order past zero on your version before you change a live product. As a suggestion, you could ask Virtina for a free initial review of your store's stock settings.

[H2: Frequently asked questions]

**What does "Allow, but notify customer" do in WooCommerce?**
It accepts backorders and shows a backorder notice. The notice appears on the product page, the block cart and checkout, the order and customer emails.
**Why is the Allow backorders option missing on my product?**
The field appears only when Manage stock is checked on that product. Tick the box and the field shows.
**Can WooCommerce stock go negative on backorders?**
Yes. In current code, a stock reduction that leaves a negative quantity fires a backorder action. Negative stock is an expected state.
**Does WooCommerce email me when someone places a backorder?**
Yes, when the backorder notification is on and the product manages stock and allows backorders. The email goes to your stock notification recipients and names the units and the order number. The buyer does not receive it.
**Does a backordered order get its own order status?**
No. The default statuses include none for backorders. Stock reduces once an order reaches Processing or On hold.
**How do I change backorder settings through the REST API?**
Write `manage_stock`, `stock_quantity` and `backorders`, using `no`, `notify` or `yes`. The fields `backorders_allowed` and `backordered` are read-only.
**What happens if my ERP webhook keeps failing?**
WooCommerce disables the webhook after more than five consecutive failures. It stops sending until someone re-enables it. The documentation does not describe retries.

[H2: Sources and verification]

Each source below is named with what it supports. Documentation pages carry no date, so they are read as published on 4 November 2026.

- **WooCommerce product editor settings documentation.** Inventory tab, Manage stock rule, Allow backorders values, notices, variable products and Sold individually.
- **WooCommerce Products settings documentation.** Hold stock, notifications, recipients, thresholds and stock visibility.
- **WooCommerce order statuses documentation.** Default statuses and when stock reduces or returns.
- **WooCommerce webhooks documentation.** Failure definition, disabling after more than five consecutive failures and delivery logs.
- **WooCommerce REST API v3 products schema at release 11.2.1.** Field names and read-only fields.
- **WooCommerce product CSV importer documentation.** Column names.
- **WooCommerce source code, development branch, read 4 November 2026.** Negative stock, cart quantity check, backorder email recipient and the missing backorder order note. The backorder action was also read at release 11.2.1.
- **WooCommerce developer blog, December 2017.** Automatic stock status when stock is managed, used for that one principle only.
- **WooCommerce Marketplace pages for Pre-Orders, Product Lead Time and Back In Stock Notifications.** Vendor-stated feature lists only.
- **WordPress.org plugin page for WooCommerce.** Current version 11.2.1, updated 9 October 2026.

Not covered because no source was read: shortcode-based checkout behavior, group-specific rules, order quantity minimums, payment timing and partial shipments. Test these on your own store.

[AUTHOR BIO]

QA BLOCK (not for publication)

**Word count.** Hand estimate about 2,880 words of prose (Summary 60, Introduction 183, body H2s about 1,960, PAA about 150, Conclusion about 90, FAQ about 230, Sources about 205). Including headings the total is about 3,100. Both counts fall inside 2,700 to 3,200. No script was available, so the build script's count is authoritative.

**Links.**
- Internal (10), all in body H2 sections: holiday readiness checklist (H2 1), WooCommerce inventory management (H2 3), WooCommerce emails not sending (H2 4), HPOS plugin compatibility (H2 5), WooCommerce development services, B2B customer groups, common WooCommerce bugs (H2 6), WooCommerce ERP integration, WooCommerce REST API guide (H2 7), WooCommerce bug fix (H2 8). All paths exactly as in the brief plan. Link 10 is the optional one and can be dropped first.
- External (2): WooCommerce product editor settings (H2 2) and WooCommerce webhooks documentation (H2 7), URLs exactly as in brief 4(c).
- No links in Summary, Introduction, PAA, Conclusion, FAQ, Sources.

**Body image alt text (brief section 8, re-count at publish).**
1. Ecommerce manager at a desk comparing a notepad of SKU numbers with a laptop while choosing WooCommerce backorders settings
2. Warehouse receiving clerk scanning an inbound pallet barcode to confirm restock dates for WooCommerce backorders
3. Operations and finance colleagues comparing a printed open-orders report with supplier purchase orders to avoid overselling

**Claims I was unsure about, for the publisher to check.**
- The "How this was checked" lead-in uses a colon instead of "How this was checked." so a sentence splitter does not count it as its own sentence.
- Table cells say "(current code)" for the cart check, matching F14 and F15 (development branch). The Sources list says so.
- "Plugify makes it" rests on S16 listing the extension as by Plugify. Wording is kept to the vendor page.
- "Cap" is stated as a Virtina practice, not a core setting, in the first paragraph of H2 6.
- The H2 6 example uses no numbers. "A handful" and "pallet-sized" are plain descriptions, not data.
- Step 5 states the low stock default of 2 and the no-stock default of 0 (F22, current code).
- The H2 8 check-your-own-store text avoids the words "classic", "minimum order" and "captured" so the blocking regex stays clean. If the whitelist is wanted for those terms, nothing needs changing.
- The regex `(By|Written by)\s[A-Z][a-z]+\s[A-Z][a-z]+` is case-insensitive in the brief. I avoided "by its own description" and used "according to the vendor's page" for that reason.
- No percentages, money, day counts, Baymard, or the 97 percent figure appear.

**Semantic terms used.** backorder, on backorder status, lead time, restock date, pre-order, out-of-stock threshold, low stock threshold, negative stock, safety stock, made-to-order, supplier purchase order, system of record, stock sync, waitlist, committed units, order status, open order.

**Format and structure.** Format B. Eight question H2s in brief order. Body H3 count 17, PAA H3 count 4. First sentence of each body H2 is the locked sentence. No semicolons, em dashes, exclamation marks, emoji or banned words by reading. No ChatSKU, ImpelHub or ElderCareMatters mention.
