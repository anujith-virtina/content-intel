---
title: "Brief: WooCommerce backorders for B2B: how to set lead times, cap orders and avoid overselling"
client: virtina
date: 2026-11-04
topic: WooCommerce backorders, lead-time messaging, self-enforced caps and ERP stock touchpoints for B2B stores
audience: B2B ecommerce leaders and ops managers (manufacturers, distributors, wholesalers) running WooCommerce
stage: brief
slug: woocommerce-backorders-lead-times
format: B (conversational Q&A body)
research: clients/virtina/output/research/woocommerce-backorders-lead-times-2026-11-04.md
uniqueness_audit: clients/virtina/output/research/uniqueness-audit-2026-11-04.md
---

# Brief: WooCommerce backorders for B2B

## 1. Thesis, unique angle and fences

**Thesis (one sentence):** In WooCommerce a backorder is a promise to a buyer that core records only as a product setting, so a B2B store must back that promise with a lead-time message, a cap it enforces itself, a staff mailbox someone reads and a clean ERP write path.

**Why this angle, why now, why Virtina**
- Defensible: all seven competitor pages (research section 4) are plugin-vendor content in B2C framing. None traces behavior to WooCommerce's own docs and code, none names negative stock, the staff-only backorder email, the missing order status, the cart quantity skip or the webhook failure threshold. None cites a source at all for field behavior.
- Now: verified against WooCommerce 11.2.1 (released 9 October 2026) on 4 November 2026, and holiday order volume makes stock promises matter most.
- Virtina fit: brand themes 1 (B2B done right, ERP integration) and 6 (fix revenue-leaking issues). The post is vendor-neutral and honest about limits, which is the trust-building route to the service links.

**Uniqueness (re-verified from the audit file, 598 posts and pages):** all 5 checks PASS. "backorder" has zero hits in any slug, title or heading. Slug `woocommerce-backorders-lead-times` shares only the word `woocommerce` with any slug (`lead` appears only in `interactive-cro-lead`, a one-word overlap). Cluster sub-niche justification is documented in the audit. Post-draft 8-gram gate still applies.

### What this post owns
Backorder stock policy and its B2B consequences:
- the three Allow backorders values and what each does on the product page, in cart and checkout, in emails and in the cart quantity check
- the Manage stock dependency and the manual On backorder trap
- the order-status and order-note gap, stock going negative, the staff-only backorder email
- lead-time messaging (core gap plus the extension route), self-enforced caps, the illustrative oversell example
- the ERP and webhook touchpoints for backorder state (REST fields, CSV columns, webhook failure threshold)
- the honest "what core does not do" list

### Hand-offs (link, do not re-explain)

| Neighbour | It owns | This post does only this |
|---|---|---|
| p42108 `woocommerce-erp-integration` | Sync architecture, batch vs real-time, field mapping, system of record, status translation table, connector choice | Names the write touchpoints for backorder state and links for design. No sync-design advice. Never requote its "97 percent accuracy" benchmark. |
| p43264 `woocommerce-holiday-season-checklist` | Seasonal readiness, one-sentence sold-out rule | Year-round policy. One link for seasonal timing. Never reuse its sentence "hide, allow backorders with a delivery date, or show notify-me". |
| p36598 `woocommerce-inventory-management`, p10692 `stock-management-plugin-for-woocommerce` | Generic stock setup, plugin tour | One link for basic inventory settings. No hold-stock, threshold or plugin tutorial beyond what a backorder decision needs. |
| p42393 `woocommerce-b2b-pricing-and-access-setup` | Customer groups, MOQ, role pricing | One link. Says only that a rule that differs by account must come from a plugin or code you verify. No MOQ talk. |
| p40347 `woocommerce-bug-fix-guide` | Overselling fix: dedicated sync, no stock caching | One link for overselling bugs. This post explains the policy-side cause (backorders allowed, no cap). |
| p43764 `order-emails-not-sending` | Email diagnosis | One link for staff or buyer emails that never arrive. |

## 2. Format decision (MUST-FOLLOW-RULES section 11)

1. **Chosen: Format B, conversational Q&A body.** Standard frame stays: H1, Summary (Template A), Introduction (Template B), TOC (Template C), body H2s, People Also Ask, Conclusion, FAQ, author bio. Format B governs the body: every body H2 is a verbatim reader question, answered directly first, then 2 to 4 short paragraphs, TOC built from the questions, one image every 2 to 3 questions.
2. **Reason:** backorders generate a chain of specific reader questions (what does each value do, why is the field missing, can stock go negative, who gets the email, what breaks my ERP), and each answer raises the next. That is Format B's stated use case, and it makes every H2 an extraction target.
3. **Researcher suggested Format D. Not used.** Recency (last 10 by date; the inventory file is stale at 2026-09-09, so this is inferred from sibling briefs and corpus): b2b-store-rebuild-or-ai-chatbot (D), order-emails-not-sending 43764 (D), 43758 (C), 43753 (E), 43336 (C), 43728 (A or D), 43583 (A), 43418 (A), 43414 (A), 43420 (A). D sits at 2, possibly 3, and the two newest posts are both D. A third consecutive D playbook adds no structural variety.
4. **Overused, therefore skipped:** Format A (about 4 of 10, over the limit). Format D (2 to 3, and the last two posts). Format C (2) and E (1, and the thesis is not contrarian). Format F needs a client result, and none may be named. Format B appears in none of the last 10 (last use 43089, 6 October).
5. **Format-B-compatible mandatory elements:** the decision table, the numbered setup steps, the illustrative example and the "check your own store" list are all placed inside question sections. Do not add a separate playbook-phase scaffold.
6. **Byline, category, updated line:** recent posts (43764, b2b-store-rebuild) carry no manual category or Updated line above the Summary, and the theme prints its own byline. Follow that. Never invent an author. Author bio (Template K) = the standard brand-voice block from the latest push script (`build_b2b_rebuild_chatbot.py`, the "Virtina is an eCommerce web design and development company..." paragraph), unchanged. It is an intentional repeat; the publisher whitelists it in the 8-gram check.

**Locked H1 (user-supplied, sentence case, 85 characters):** WooCommerce backorders for B2B: how to set lead times, cap orders and avoid overselling
Because core has no cap field, the post must say plainly that "cap" means a limit you enforce yourself.

## 3. Section outline (target 3,000 words; floor 2,700, hard cap 3,200, counted over all visible prose including table, FAQ and Sources)

Order: Summary, Introduction, TOC, body H2 1 to 8, People Also Ask, Conclusion, FAQ, Sources and verification, author bio. All H2s sentence case. Locked first sentences are 20 words or fewer. Every H2 over 200 words carries at least one H3. Plan has 15 body H3s (rule minimum 6) plus 4 PAA H3s.

### Summary (about 70 words, Template A, no links)
Seed: "WooCommerce backorders let you sell a stocked product past zero, but core only records the promise. This guide shows what each Allow backorders value does, how to message a lead time and how to limit your exposure. It also covers the ERP and webhook points where backorder state can drift." Keyword in the first sentence.

### Introduction (about 130 words, Template B, no links, three paragraphs)
- P1 hook, no statistic: a large account order lands on a product with a few units left, WooCommerce accepts it, and your team learns of it from a staff email, if anyone reads that inbox. Two or three short sentences.
- P2: what the reader gets: the three values, the lead-time message, the cap problem, the ERP touchpoints. Two sentences.
- P3 "How this was checked" (bold lead-in). Required content, all in plain sentences: checked against WooCommerce 11.2.1 on 4 November 2026; settings and fields come from WooCommerce's documentation and the REST API v3 schema; cart, stock and email behavior comes from reading WooCommerce source code (mostly the development branch), so confirm it with a test order on your version; the post says so wherever a point rests on code; it was not measured on a live store. Four sentences is too many for one paragraph: split to two short paragraphs or trim to three.

### TOC (Template C): one entry per body H2, then `#people-also-ask`, `#conclusion`, `#faq`, `#sources`.

### H2 1 (about 210 words) id `what-is-a-backorder`
**What is a backorder in WooCommerce, and when does it suit a B2B store?**
Locked first sentence: "A backorder is an order WooCommerce accepts for a product that has run out of stock."
Then the thesis in 2 sentences (a backorder is a promise; the rest of the post is about backing it). Facts: F2, F7.
- H3 **How is a backorder different from a pre-order?** First sentence: "Pre-orders come from a separate WooCommerce extension, while backorders are a setting on a product you already stock." Extension facts only (F29, S15): availability date, charge upfront or on release, its own pre-order order status. Virtina opinion, labeled: backorder for a SKU that has been in stock, pre-order for a SKU that has not been released. Do not say core has no pre-order feature (U1).
- H3 **Should you allow backorders, show out of stock, or hide the product?** Short decision paragraph in prose (three options; name the "Out of stock visibility" setting, F12, and the Back In Stock Notifications waitlist extension, F31). One link: seasonal timing (anchor "holiday readiness checklist"). No numbers.

### H2 2 (about 330 words) id `allow-backorders-values`
**What do the three Allow backorders settings do?**
Locked first sentence: "The Allow backorders field has three values: \"Do not allow\", \"Allow, but notify customer\" and \"Allow\"."
Source mention in prose: "WooCommerce's product editor documentation" (external link 1 here). API keys `no`, `notify`, `yes` once (F3).
**Decision table (Template N), VERIFIED facts only, 4 columns:**

| Setting (API value) | What the buyer sees | Cart quantity check | B2B fit (Virtina view) |
|---|---|---|---|
| Do not allow (`no`) | The product turns Out of stock at zero and cannot be bought (F2). | Cart blocks a quantity above stock minus stock held by other pending orders (F15, current code). | Fits made-to-order or unconfirmed-supply SKUs. |
| Allow, but notify customer (`notify`) | A notice on the product page, in block cart and checkout, on the order and in customer emails (F5). | Skipped, so quantity is not limited by stock (F14, current code). | Safer default for stocked SKUs with a supplier date. |
| Allow (`yes`) | Backorders accepted and the product looks like an in-stock item (F6). | Skipped (F14, current code). | Use only when the delay is invisible to the buyer. |

Caption line, 14px grey per Template N: "Last column is Virtina's opinion, not WooCommerce documentation."
- H3 **Which Allow backorders value fits a B2B store?** First sentence: "For most B2B stores, \"Allow, but notify customer\" is the safer default, in Virtina's view." Reason: plain Allow hides the delay, so the buyer calls sales. Opinion label required.
- H3 **What happens if Manage stock is switched off?** First sentence: "With Manage stock off, you can set On backorder by hand, but only the product page shows a notice." (F8). Add: the Allow backorders field appears only when Manage stock is checked (F4). Cart, checkout, order and email notices are not shown (F8).
- Image body 1 after this section.

### H2 3 (about 280 words) id `set-up-backorders`
**How do you set up backorders on a product?**
Locked first sentence: "Turn on Manage stock for the product, then pick a value in the Allow backorders field."
Source mentions: "WooCommerce's Products settings page" (named, not linked), the CSV importer documentation (named).
- H3 **Which steps set up a backordered product?** Template F bullets with bold "Step N." labels (genuinely sequential). Seven steps: (1) in Inventory settings confirm Manage stock is on, the backorder notification is on (default) and the stock email recipients are set (F12, F21); (2) open the product, Inventory tab, tick Manage stock (F1, F2); (3) enter Quantity; (4) choose the Allow backorders value; (5) leave the low stock threshold at the store default or set it per product (F10, F22 defaults); (6) view the product page and add it to cart; (7) place a test order past zero and read the staff email and order notes. One link: basic inventory settings (anchor "WooCommerce inventory management"). Second external link is NOT here.
- H3 **How do variable products and bulk edits behave?** First sentence: "On variable products, the parent quantity covers every variation unless the parent leaves Manage stock off." (F10). Then CSV columns `Stock`, `Backorders allowed?` (1, 0 or notify), `In stock?`, `Low stock amount` (F26). Note the CSV `Stock` field turns stock management on, blank turns it off (S13 as read).

### H2 4 (about 290 words) id `buyer-and-team-view`
**What do buyers and your team see when a backorder is placed?**
Locked first sentence: "Buyers see a notice under the notify setting, and your team gets an email, not a status."
- H3 **What does the buyer see, page by page?** Product page, cart, checkout, order and customer emails under notify (F5); nothing special under plain Allow (F6). Do not describe classic checkout (U2) or quote notice text (U13). Say "a backorder notice".
- H3 **Who receives the backorder email, and what does it say?** First sentence: "The backorder email goes to your stock notification recipients, not to the buyer." (F20, in current code). It names the units backordered and the order number. It is on by default and fires only when stock is managed and backorders are allowed (F21). Consequence, labeled as inference: if nobody reads that mailbox, the signal is lost. One link: emails that never arrive (anchor "WooCommerce emails not sending").
- H3 **Why is there no backorder order status?** First sentence: "WooCommerce's default order statuses include none for backorders, and the order gets no backorder note." (F17, F18). Add: stock reduces when an order reaches Processing or On hold and returns on Cancelled or Failed (F16, order statuses documentation, named). Virtina opinion: track open backorders in a report or the ERP, not in order status.

### H2 5 (about 270 words) id `lead-time-message`
**How do you show a lead time on backordered items?**
Locked first sentence: "WooCommerce's documented product fields include no restock date, so a lead time needs your own wording or an extension."
- H3 **What should a lead-time message say?** Prose, Virtina opinion, no numbers of days: a ship-by week or date you can keep (taken from the supplier's confirmed purchase order), what happens if it slips, who to contact. The reason: a "backordered" notice with no date makes a buyer call sales.
- H3 **Which extensions add lead times or waitlists?** First sentence: "The Product Lead Time extension lists separate lead times for in-stock, out-of-stock and backorder products, by its own description." (F30, S16, vendor-stated). Back In Stock Notifications is a waitlist with an email when stock returns (F31, S17). Pre-Orders as above. Every claim is "the vendor page says". Do not state block checkout or HPOS support for any of them (U8; S16 states neither). Tell the reader to check each page and run a compatibility check. One link: anchor "HPOS plugin compatibility". Name no other plugins.
- Image body 2 after this section.

### H2 6 (about 310 words) id `cap-backorders`
**How do you cap backorders and avoid overselling?**
Locked first sentence: "WooCommerce's documented fields include no backorder cap, so you enforce the limit with policy and monitoring." (F23)
- H3 **How can one large account order oversell a SKU?** First sentence: "One large account order can commit more units than you have, because the cart skips its stock check." (F14, current code). Then the worked scenario, labeled "Illustrative example, not a client case." No numbers, no names: a distributor's account orders a pallet-sized quantity of a SKU with a handful of units left; Allow is on; the cart accepts it; stock goes negative; the only signal is one staff email; sales finds out when the supplier date is asked for. State the outcome as a mechanism, never as a result.
- H3 **What caps exposure when core has no cap field?** Virtina opinion, labeled. Three prose options: (a) publish only supplier-confirmed inbound units as sellable quantity; (b) watch the negative quantity and the staff email, and switch the SKU to "Do not allow" when committed units reach the supplier-confirmed number; (c) have a developer add a rule in code and test it on staging. State plainly that (c) is not a documented setting. Two things that look like caps but are not: Hold stock reserves stock only for Pending payment orders (F13) and Sold individually limits one unit per order but not separate orders (F11). Links: anchor "B2B customer groups" for account-specific rules, with the sentence "any rule that differs by account must come from a plugin or custom code you verify" (U4); anchor "WooCommerce development services" next to option (c), stated as fact.
- H3 **Why does negative stock matter?** First sentence: "Stock can go below zero, and current WooCommerce code fires a backorder action whenever it does." (F19; the action `woocommerce_product_on_backorder` is confirmed at tag 11.2.1; name it once in code font). Link: anchor "common WooCommerce bugs" (overselling bugs). Tell the reader to confirm how their ERP reads a negative quantity. Do not assert how any specific ERP behaves.
- Image body 3 at the end of this section.

### H2 7 (about 270 words) id `erp-and-webhooks`
**How do you keep ERP and WooCommerce stock in step?**
Locked first sentence: "Your ERP writes stock into WooCommerce through REST or CSV, and WooCommerce reports orders to the ERP through webhooks."
Hand-off sentence: sync design, batch vs real-time and system of record belong to the ERP post (link, anchor "WooCommerce ERP integration"). Optional second sentence only if natural: inventory and catalog synchronization service page (anchor "inventory and catalog synchronization"). Skip if it crowds.
- H3 **Which REST fields control backorder state?** Source in prose: "the WooCommerce REST API v3 schema, read at release 11.2.1". Fields: `manage_stock`, `stock_quantity`, `stock_status`, `backorders` (`no`, `notify`, `yes`), `low_stock_amount`; `backorders_allowed` and `backordered` are read-only, so the writable control is `backorders` (F24, F25). When stock is managed, the quantity drives status (F9). Do NOT say what happens if you write `stock_status` on a managed product (U9). Link: anchor "WooCommerce REST API guide".
- H3 **What happens when your ERP endpoint stops responding?** First sentence: "WooCommerce disables a webhook after more than five consecutive failed deliveries and stops sending until someone re-enables it." (F27, F28). Source: "WooCommerce's webhooks documentation" (external link 2 here). A response other than 2xx, 301 or 302 counts as a failure; deliveries are logged under WooCommerce, Status, Logs. Add: the documentation does not describe retries, so do not assume them (U12). Virtina opinion: monitor webhook status and alert on Disabled.

### H2 8 (about 200 words) id `core-limits`
**What does WooCommerce core not do for backorders?**
Locked first sentence: "WooCommerce's documented settings include no backorder cap, no restock date and no backorder order status."
Template F bullets (genuinely list-shaped): (1) no maximum backorder quantity and no expected restock date in the documented product fields (F23); (2) no backorder order status in the default list, no backorder order note (F17, F18); (3) the dedicated backorder email goes to your staff, not to the buyer, and the buyer's notice appears in order and customer emails only under the notify setting (F20, F5); (4) pre-orders come from a separate extension (F29).
- H3 **Which backorder questions should you test on your own store?** Plain "check your own store" list (no facts asserted): how classic (non-block) cart and checkout behave; any rule that differs by customer group or role; how minimum order quantities interact; when your gateway takes payment on a backordered order, and how your accountant books it; partial or split shipments; whether each extension works with your theme, ERP and B2B plugin. Close: a failing result is a developer job. Link: anchor "WooCommerce bug fix" (service page) stated as fact. Skip if links exceed 10.

### People Also Ask (about 120 words, Template H, 4 questions, answers 2 to 3 sentences, no links)
1. **What does on backorder mean in WooCommerce?** It is one of three stock statuses: In stock, Out of stock, On backorder. With Manage stock on, the status follows the quantity; with it off, you set it by hand (F7, F8, F9; S1, S4).
2. **How do you turn backorders off for one product?** Set Allow backorders to "Do not allow" in the product's Inventory tab. The field appears only when Manage stock is checked, and a product setting overrides the store-wide one (F1, F3, F4; S1).
3. **Is a backorder the same as a pre-order?** No, in Virtina's view: a backorder covers a SKU you normally stock, a pre-order a SKU not yet released. Pre-orders come from a separate WooCommerce extension (F29; S15).
4. **Can you allow backorders on one variation only?** Yes when the parent does not manage stock, because the variation setting then applies. If the parent manages stock, its quantity covers all variations (F10; S1).

### Conclusion (about 80 words, Template I, white on teal, no links, no CTA language)
Restate the thesis: a backorder is a promise, core records it as a setting, so the store needs a lead time, a self-enforced limit, a mailbox that is read and an ERP path that is monitored. End on the practical step: place one test order past zero on your version before you change a live product. No "in conclusion".

### FAQ (about 340 words, Template J, 7 questions, answers 2 to 3 sentences, no links)
Answers must not repeat PAA wording.
1. **What does "Allow, but notify customer" do in WooCommerce?** Accepts backorders and shows a backorder notice on the product page, block cart and checkout, the order and customer emails. (F5; S1)
2. **Why is the Allow backorders option missing on my product?** The field appears only when Manage stock is checked on that product. Tick it and the field shows. (F4; S1)
3. **Can WooCommerce stock go negative on backorders?** Yes. In current code a reduction that leaves a negative quantity fires a backorder action, so negative stock is an expected state. (F19; S9)
4. **Does WooCommerce email me when someone places a backorder?** Yes, if the backorder notification is on (the default) and the product manages stock and allows backorders. It goes to your stock notification recipients, names the units and the order number, and does not go to the buyer. (F20, F21; S2, S10)
5. **Does a backordered order get its own order status?** No. The default statuses include none for backorders, and stock is reduced once an order reaches Processing or On hold. (F16, F17; S3)
6. **How do I change backorder settings through the REST API?** Write `manage_stock`, `stock_quantity` and `backorders` with `no`, `notify` or `yes`. `backorders_allowed` and `backordered` are read-only. (F24, F25; S8)
7. **What happens if my ERP webhook keeps failing?** WooCommerce disables the webhook after more than five consecutive failures and stops sending until someone re-enables it. The documentation does not describe retries. (F27, F28; S14)

### Sources and verification (about 120 words, plain text, `id="sources"`)
Structural heading, not a question (allowed, like Conclusion and FAQ). Placed after the FAQ and before the author bio, in a Template D box. Format and content in section 4(d). No links in this block.

### Author bio (Template K): see section 2 item 6.

## 4. Documentation plan (how the post proves its claims)

**(a) "How this was checked" note.** Third paragraph of the Introduction, bold lead-in "How this was checked." It must name: WooCommerce 11.2.1, the date 4 November 2026, the split between documentation-based and code-based claims, the instruction to confirm code-based behavior with a test order, and the plain admission that nothing was measured on a live store. Version scope sentence for code facts: "Product fields were read at release 11.2.1. Other code behavior was read from the development branch on the same date." (Only S8 and the backorder action in S9 were re-read at the 11.2.1 tag.) Keep every sentence at 20 words or fewer.

**(b) In-prose source mentions (named, not linked unless listed in (c)).** Use these exact source names once each where the claim sits:
- "WooCommerce's product editor documentation": Inventory tab override, Manage stock rules, the three Allow backorders values, what each shows, variable products, Sold individually (F1 to F11)
- "WooCommerce's Products settings page": Hold stock, notifications, recipients, thresholds, visibility (F12, F13, F21)
- "WooCommerce's order statuses documentation": default statuses, when stock reduces and returns (F16, F17)
- "current WooCommerce code": cart quantity skip, stock reduction notifications, negative stock action, no backorder order note, backorder email recipient, low-stock default of 2 and no-stock default of 0 (F14, F15, F18 to F20, F22)
- "the WooCommerce REST API v3 schema, read at release 11.2.1": field names (F24, F25)
- "WooCommerce's product CSV importer documentation": column names (F26)
- "WooCommerce's webhooks documentation": failure definition, five-failure disable, logging (F27, F28)
- "the vendor's own page" or "by its own description": Pre-Orders, Product Lead Time and Back In Stock Notifications feature lists (F29 to F31)
- "WordPress.org's plugin page": 11.2.1 and the update date, in the Intro note only (F32)
- Label every Virtina opinion with "in Virtina's view", "in practice" or "an illustrative example". Never present opinion as documentation.

**(c) External links (maximum 2, `target="_blank" rel="noopener noreferrer"`, Template M). Both pages fetched in research on 2026-11-04.**
1. `https://woocommerce.com/document/managing-products/product-editor-settings/` anchor **WooCommerce product editor settings** (4 words), in H2 2, first paragraph. It is the primary source for the post's central table (S1).
2. `https://woocommerce.com/document/webhooks/` anchor **WooCommerce webhooks documentation** (3 words), in H2 7, webhook failure H3 (S14).
Why these two: S1 carries the main claim set and S14 carries the most surprising, most consequential claim (the five-failure disable), which readers will want to check. S2 (Products settings) and S3 (order statuses) are named in prose and the Sources list but not linked, to respect the cap. Never link vendor extension pages, code files, GitHub, the REST docs site or any competitor.

**(d) Closing "Sources and verification" list (plain text, no hyperlinks).** Intro sentence: "Each source below is named, with what it supports. Documentation pages carry no date, so they are read as published on 4 November 2026." One bullet (Template F, list-shaped) per source, name then dash-free support clause:
- WooCommerce product editor settings documentation: Inventory tab, Manage stock rule, three Allow backorders values, notices, variable products, Sold individually.
- WooCommerce Products settings documentation: Hold stock, notifications, recipients, thresholds, stock visibility.
- WooCommerce order statuses documentation: default statuses and when stock reduces or returns.
- WooCommerce webhooks documentation: failure definition, disable after more than five consecutive failures, delivery logs.
- WooCommerce REST API v3 documentation and the wc/v3 products schema at release 11.2.1: field names and read-only fields.
- WooCommerce product CSV importer documentation: column names.
- WooCommerce source code, stock, cart and email files, development branch read on 4 November 2026 (backorder action also at 11.2.1): negative stock, cart quantity skip, backorder email recipient, no backorder order note.
- WooCommerce developer blog, December 2017: automatic stock status when stock is managed (dated; supports one principle only).
- WooCommerce Marketplace pages for Pre-Orders, Product Lead Time and Back In Stock Notifications: vendor-stated feature lists only.
- WordPress.org plugin directory page for WooCommerce: current version 11.2.1, updated 9 October 2026.
Closing line: "Not covered because no source was read: classic checkout behavior, customer-group rules, minimum order quantities, payment timing and partial shipments. Test these on your own store."

**(e) UNVERIFIED items: leave out, or word as "check your own store".** Leave out entirely: U1 (core has no pre-order feature), U3 (`is_in_stock()` handling), U9 (API `stock_status` writes on managed stock), U10 (Store API backorder flag), U11 (Pre-Orders marks orders Processing), U13 (exact notice text such as "Available on backorder"). Check-your-own-store only: U2 classic checkout, U4 per-role or per-group rules, U5 MOQ interplay, U6 payment timing and revenue booking, U7 partial shipments, U8 extension compatibility with a given theme, ERP or B2B plugin, U12 webhook retries (say the documentation does not describe them).

## 5. Internal link plan (9 required, 1 optional; body prose only; Template L)

No links in Summary, Introduction, PAA, Conclusion, FAQ or Sources. Every anchor is a clean 2 to 5 word noun phrase, unique, no leading article, no gerund, no "our". All slugs are present in `virtina-corpus-2026-11-04.json` and were fetched by the researcher on 2026-11-04. WebFetch cannot show status codes, so the publisher must confirm HTTP 200 with redirects off before the PUT (use the browser or REST, not curl, which gets 429).

| # | URL | Anchor | Section |
|---|---|---|---|
| 1 | https://virtina.com/woocommerce-holiday-season-checklist/ | holiday readiness checklist | H2 1, H3 allow, show or hide |
| 2 | https://virtina.com/woocommerce-inventory-management/ | WooCommerce inventory management | H2 3, steps H3 |
| 3 | https://virtina.com/order-emails-not-sending/ | WooCommerce emails not sending | H2 4, backorder email H3 |
| 4 | https://virtina.com/woocommerce-b2b-pricing-and-access-setup/ | B2B customer groups | H2 6, caps H3 |
| 5 | https://virtina.com/platforms/woocommerce-development-services/ | WooCommerce development services | H2 6, caps H3, option (c) |
| 6 | https://virtina.com/woocommerce-bug-fix-guide/ | common WooCommerce bugs | H2 6, negative stock H3 |
| 7 | https://virtina.com/woocommerce-erp-integration/ | WooCommerce ERP integration | H2 7, opening hand-off |
| 8 | https://virtina.com/guide-on-woocommerce-rest-api/ | WooCommerce REST API guide | H2 7, REST fields H3 |
| 9 | https://virtina.com/woocommerce-hpos-plugin-compatibility/ | HPOS plugin compatibility | H2 5, extensions H3 |
| 10 (optional) | https://virtina.com/woocommerce-bug-fix/ | WooCommerce bug fix | H2 8, test-on-your-store H3 |

Notes
- Service-page links (5 and 10) are stated as facts ("a developer can add a rule in code, and WooCommerce development services cover custom stock rules"), never as a pitch. Drop link 10 first if the section feels crowded.
- Link 2: p36598 is thin and part Magento. The anchor names the destination's topic ("inventory management"), and the sentence must not promise settings detail it does not hold.
- Link 8: the REST guide mentions stock status but not backorders. Frame it as the general API reference, not as backorder documentation.
- Rejected from the candidate list: B2B customer portal (cannot confirm it covers order visibility), B2B net payment terms (payment timing is U6), stock-management-plugin post (would send readers to a plugin tour), B2B inventory tips (Magento-leaning), order fulfillment and 3PL page, inventory and catalog sync page (optional only, in H2 7 if natural; counts toward the 10 maximum).
- Never use the verified-dead paths: `/woocommerce-development-services/` (301), `/contact/` (301, use `/get-in-touch/`), `/ecommerce-migration-services/`, `/ecommerce-development-services/`, `/ecommerce-seo-services/` (404). Any CTA button, if the user wants one, goes only to `/get-in-touch/` after a fresh 200 check; none planned.
- No competitor domains. No Barn2, FunnelKit, WebToffee, WebAppick, Agile Store Locator, Racklify or HotWax links or name mentions.

## 6. Stats and claims discipline

**Zero statistics policy.** The only numbers allowed: WooCommerce 11.2.1, 4 November 2026, 9 October 2026, the word "three" (values), the threshold "more than five consecutive failures", the 2xx, 301 and 302 codes, the Hold stock "Pending payment" fact, the low-stock default of 2 and the no-stock default of 0 (only if used), and step numbers.

**Must NOT appear**
- Baymard 41 percent, or any Baymard figure
- any dollar-per-backorder or fulfillment cost figure, any dollar amount
- "7 to 14 days", or any target number of days or weeks for lead times
- the 97 percent inventory accuracy or sub-5-minute figure from p42108, or any benchmark from it
- any percentage of shoppers who accept, abandon or cancel on backorders, any lost-sales figure from overselling
- any "WooCommerce powers X percent of stores" or install-count figure
- classic (shortcode) cart or checkout backorder behavior
- per-role or per-customer-group backorder rules in core, in either direction
- minimum order quantity interplay
- payment-capture, authorization, revenue recognition or accounting timing (say "when your gateway takes payment", "talk to your accountant")
- partial or split shipments as a core feature
- the claim that core has no pre-order feature
- exact backorder notice text, `is_in_stock()` behavior, API `stock_status` write behavior, Store API backorder flag, webhook retries
- any named plugin other than WooCommerce Pre-Orders, Product Lead Time (by Plugify) and Back In Stock Notifications; any compatibility claim for a theme, ERP, B2B plugin, block checkout or HPOS beyond "check the vendor page"
- any Virtina client result, client name, invented author, invented quote
- the stock "builds on WooCommerce/Magento/BigCommerce/Shopify" sentence or any variant
- sentences copied from p43264, p42108, p40347, p10692 or p36598 (8-gram gate)

**Blocking phrase list for the build script** (case-insensitive regex; any hit fails the build; run on visible text with `<style>` and inline styles stripped)
```
\d+(\.\d+)?\s?(%|percent|per cent)            # no percentages at all
\$\s?\d|\b(usd|dollars?)\b                    # no money figures
Baymard|\b41\s?%|97\s?%|inventory accuracy|sub-?5-?minute
7\s?(to|-)\s?14\s?days|\b\d+\s?(-|to)\s?\d+\s?(business\s)?(days|weeks)|within\s\d+\s(business\s)?(days|weeks)
\bmillion\b|powers?\s\d|\d\s?(of|in)\s\d+\s(stores|merchants|buyers)
classic (cart|checkout)[^.]{0,80}(shows?|displays?|skips?|blocks?|behaves?|works?)
(core|WooCommerce) (supports?|lacks?|offers?|provides?)[^.]{0,60}(role|customer group|per-group)
minimum order|\bMOQ\b
\bcaptur(e|ed|es|ing)\b|authori[sz](e|ed|ation)|revenue recogni|deferred revenue|chargeback
(partial|split) (shipment|fulfil)[^.]{0,40}(core|WooCommerce)\s(supports|handles|does)
core (has|includes|offers) no pre-?order|no pre-?order feature
Available on backorder|is_in_stock|Store API
will (automatically )?retry|automatic(ally)? retr|retries (automatically|failed)
(never|can't|cannot|impossible to) oversell|eliminat\w+ overselling|guarantee
WholesaleX|Barn2|B2BKing|Wholesale Suite|WebToffee|FunnelKit|WebAppick|Agile ?Store ?Locator|Racklify|HotWax|Plugify's? (competitor)
Shopify Enterprise
\b(trunk|GitHub)\b
\bour\b|we offer|contact us|reach out|check out|read our|see our|click here|talk to us
—|&mdash;|&#8212;|&#x2014;|;                  # em dash in 4 forms and semicolons
!
\b(revolutionary|game-?changing|best-in-class|cutting-edge|world-class|industry-leading|synerg\w+|unlock value|transform your|delve|leverage|navigate|realm|landscape|ecosystem)\b
in today's fast-paced|it's important to note|in conclusion|in the world of
(By|Written by)\s[A-Z][a-z]+\s[A-Z][a-z]+     # no invented byline
```
Allowed-with-exact-wording exceptions (publisher whitelists these sentences only): the sentence "The documentation does not describe retries." and the single "check your own store" list item that names classic cart and checkout, customer groups, minimum order quantities, payment timing and partial shipments as things to test. The word `capture` stays banned everywhere, so use "when your gateway takes payment".

Also block in the build: 4+ sentence paragraphs, sentences over 20 words, Title Case headings, H2 count mismatch with TOC ids, fewer than 6 H3s, external hrefs above 2, any external href outside the two in section 4(c), any internal href not in section 5, any anchor repeated, and a body H2 whose first sentence does not match the locked sentence (allow minor wording change only on H3 openers).

## 7. Semantic term coverage (13 minimum, natural prose only)

backorder, on backorder status, lead time, restock date, pre-order, out-of-stock threshold, low stock threshold, negative stock, safety stock, made-to-order, supplier purchase order, system of record, stock sync, back-in-stock waitlist, committed quantity, order status, open order. (Use "available-to-promise" at most once; use "partial fulfilment" as a concept only, never as a core feature.) Creator lists the terms used in the QA block.

## 8. Images (Section 3 and the all-client quality floor)

Specs: realistic documentary-style photos of one person in the section's exact situation. No abstract art, no neon, no glow, no concept scenes. Featured displayed 1309x500, uploaded at about 1895x724 (2.618:1). Body displayed 670x352 (`width="670" height="352"`, `loading="lazy"`, Template G), uploaded at 1340x704. JPEG quality 90 or higher, 4:4:4, no upscaling, no quality-for-size trade (resize instead; keep under 600 KB). View each at 100% before upload. Every `src` begins `https://virtina.com/wp-content/uploads/`. `featured_media` is a real media ID. The theme prints the featured image, so keep it out of the body. All four images from four different shoots. Screens in frame must show no readable brand, no platform claim, no readable text: the image depicts the section's own content, not claims about WooCommerce or any platform. Do not reuse any image from 43764, 43758, 43753, b2b-store-rebuild, 43089, 43075 or earlier posts (check the media library by source photo ID, not file name). Avoid: empty shelves with no person, handshake, shipping-box flat lay, nature, building exteriors, glow.

| Slot | Under H2 | Scene | Alt text (80 to 150 chars, keyword included) |
|---|---|---|---|
| Featured | top of post | A purchasing manager standing in a distribution warehouse aisle, checking a printed stock list against a pallet rack with a visible gap. Wide composition with room to crop. | Purchasing manager in a distribution warehouse aisle checking a stock list while planning WooCommerce backorders for B2B buyers (127 chars) |
| Body 1 | H2 2, after the table | An ecommerce manager at an office desk comparing a handwritten notepad of SKU numbers with a laptop. Laptop angled so the screen is not legible. | Ecommerce manager at a desk comparing a notepad of SKU numbers with a laptop while choosing WooCommerce backorders settings (123 chars) |
| Body 2 | H2 5, after the extensions H3 | A warehouse receiving clerk in a hi-vis vest scanning a carton barcode with a handheld scanner at a loading dock as an inbound pallet arrives. | Warehouse receiving clerk scanning an inbound pallet barcode to confirm restock dates for WooCommerce backorders (112 chars) |
| Body 3 | H2 6, end of section | An operations manager and a finance colleague at a meeting table, one pointing at a line on a printed open-orders report beside a supplier purchase-order folder, notes in hand. | Operations and finance colleagues comparing a printed open-orders report with supplier purchase orders to avoid overselling (123 chars) |

Optional fourth body image (pillar band allows up to 5, but only if it adds value): customer service rep on a headset, laptop open on an order list, mid-call explaining a delivery date to a trade buyer, under H2 5 "What should a lead-time message say?". Skip by default to keep the page light. Re-count every alt length after final wording.

## 9. SEO

| Field | Value |
|---|---|
| H1 | WooCommerce backorders for B2B: how to set lead times, cap orders and avoid overselling |
| Yoast SEO title | WooCommerce Backorders for B2B: Set Lead Times \| Virtina (56 chars) |
| Meta description | Learn what the three WooCommerce backorders settings do for B2B, how to set lead times, limit open orders and avoid overselling. Checked on WooCommerce 11.2.1. (about 159 chars; the build script must count and trim to 150 to 160) |
| Focus keyword | WooCommerce backorders |
| Secondary keywords | allow backorders WooCommerce; WooCommerce on backorder status; WooCommerce backorder vs pre-order; WooCommerce lead time message; B2B backorders; WooCommerce overselling; backorder notification email WooCommerce |
| Slug | `woocommerce-backorders-lead-times` |
| Categories | WooCommerce (79), eCommerce (405), the same pair used by sibling WooCommerce posts; publisher confirms IDs in the live taxonomy |
| Status | draft only, Yoast fields sent in `meta` and verified with a `context=edit` GET |

Keyword placement: Summary first sentence, H1, first 100 words, one H2 (allow backorders values), meta description, Yoast title, image alt (featured). Do not stuff.

## 10. Checklist and voice for the creator

- Sentences 20 words or fewer; article average 18 or less. Paragraphs 2 to 3 sentences, one idea each. No semicolons, no exclamation marks, no emoji.
- No em dashes in any form (four forms), anywhere, including headings, table cells, bullets and alt text.
- Sentence-case headings. Active voice, second person ("you"). Contractions fine. US spelling ("behavior", "fulfillment"). Date as "4 November 2026" per the user's wording.
- First sentence of every body H2 answers the H2 (locked sentences in section 3). Lead with the answer, then the caveat.
- Bullets only where list-shaped: the setup steps, the core-limits list, the Sources list. Everything else is prose. Template F for all bullets (slate #43627f circles, 16px text, #2d3e50).
- Quotes under 15 words, paraphrase otherwise. Do not quote competitors. The only quoted text is exact setting labels.
- Banned: hype words and AI-tell filler (list in section 6), "vendor" for Virtina, "reach out", "solutions" as filler. Virtina is a "partner" only if a sentence needs it; this post is vendor-neutral and needs it rarely.
- No promotional possessive link phrasing ("our guide", "check out our"). State the fact; the link carries the reference. Virtina service page links only where natural (links 5 and 10), correct canonical paths only.
- Label every Virtina opinion and the illustrative example. No number in the example. The example is not a client story.
- Do not use the boilerplate platform-list sentence. Do not echo p43264, p42108, p40347, p10692 or p36598 wording.
- Template use: A, B, C (SVG arrows, `list-style:none!important`, no space before `!important`), D (every body H2 has an `id` matching the TOC), F, G, H, I, J, K, L, M, N. TOC heading is H3. All H3 use `<h3 style="color:#43627f;font-size:22px;">`. No Thrive class-based markup. No stray `<<` or `>>`.
- Run before handing to the publisher: word count 2,700 to 3,200; at least 6 H3; 9 or 10 internal links; 2 external links exactly as in section 4(c); 0 links in Summary, Introduction, PAA, Conclusion, FAQ, Sources.
- Publisher gates (MUST-FOLLOW section 9): 8-gram check against all posts and drafts with styles stripped (whitelist the author bio), internal link 200 with redirects off, Flesch calibrated to the Virtina corpus, Yoast verified, Thrive note (`_tve_updated_post` is not REST-writable, so the post needs one open-and-save in Thrive Architect), then the standing `/social virtina {post-id}` step.

## 11. Locked versus creator judgment

**Locked:** thesis, H1, slug, Format B, the 8 body H2 headings and order, the locked first sentences, the table content, the two external links and anchors, the internal link table, the "How this was checked" content, the Sources list, the banned list, the image plan, the Yoast title and focus keyword.

**Creator judgment:** H3 opener wording beyond the ones given, the hook scene in the Introduction, the wording of the illustrative example (no numbers), the Conclusion's closing line, the exact meta description wording (must land at 150 to 160), which 13 or more semantic terms are used.

## 12. Risks and open points

- **Format counts are inferred.** The inventory is stale (2026-09-09) and has no format field for recent posts. B is the right call even if the counts shift, because it is unused recently and fits the topic.
- **The "cap orders" promise.** Core has no cap field. The post stays honest by saying so in the first sentence of H2 6 and labeling the three cap approaches as Virtina opinion.
- **Code facts come mostly from the development branch.** Only the REST v3 schema and the backorder action were re-read at the 11.2.1 tag. The post says so, and tells readers to confirm with a test order.
- **Length.** Eight body H2s, 15 body H3s and a table push toward the cap. Hold each H3 to about 80 to 110 words and keep the Sources list to one line per source.
- **Link 2 and link 8 are thin matches.** Their anchors are accurate but the posts do not deeply cover the point. Keep the surrounding sentences general.
- **Author bio contains a "free initial review" claim.** It repeats from the latest bio block unchanged. Confirm it is still current before push.
