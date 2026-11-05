---
title: "Brief: WooCommerce standing orders for B2B: subscription plugin or custom build?"
client: virtina
date: 2026-11-05
topic: B2B standing orders on WooCommerce, three routes (use the official Subscriptions plugin as is, extend it, build custom)
audience: B2B ecommerce leaders (VP eCommerce, Director of Digital, ecommerce managers) at manufacturers, distributors and wholesalers on WooCommerce
stage: brief
slug: standing-orders-plugin-or-custom-build
format: C (opinionated options, adapted to a decision post)
research: clients/virtina/output/research/google-trends-virtina-2026-11-05.md
competitor_analysis_and_uniqueness_audit: clients/virtina/output/research/competitor-analysis-standing-orders-2026-11-05.md
---

# Brief: WooCommerce standing orders for B2B: subscription plugin or custom build?

## 1. Thesis

> A B2B standing order is not a consumer subscription, so "plugin or custom?" is the wrong binary: there are three routes (use WooCommerce Subscriptions as is, extend it, build custom), and the right one depends on how each account pays and prices every renewal, which you prove on a staging site before you commit.

**Why this angle**
- It is a decision post with named options and a real comparison table, which is the shape the user wants for AI visibility. Each H2 opens with its own answer so a model can lift it.
- It is the only angle that passes uniqueness (see audit file). A generic "plugin vs custom" post collides with roundup 31274 on the head term. A pricing post collides with 42393.
- The official docs themselves point to three routes, not two: custom intervals and lengths are possible only through developer-level code on top of the plugin (research fact 5).

**Why now.** WooCommerce 11 era docs were fetched on 5 November 2026, so every fact can carry a date. Year-end is when distributors review reorder programs. The topic is evergreen, so there is no seasonal risk.

**Why Virtina.** Theme 1 (B2B eCommerce done right: complex pricing, customer-specific catalogs, ERP integration). The service answer is custom WooCommerce plugin development plus ERP integration. Honest framing: for some stores "use the official plugin as is" is the right answer, and the post says so. That is the anti-pitch credibility the audience asks for.

**Product-fit line (feedback_topic_must_fit_product).** Owned theme served: theme 1. Product capability that answers the reader's problem: custom plugin development (page `woocommerce-plugin-development`, which lists a subscription plugin service) and ERP integration.

**Honesty about demand.** Do not call this topic "Trends-proven" anywhere (post, Yoast, social, reports). The Trends signal was weak (related searches "woocommerce subscription plugin" and "woocommerce wholesale prices", low volume, relative index only). The topic rests on the corpus gap plus product fit.

## 2. Audience

VP eCommerce, Director of Digital, ecommerce manager at a distributor or manufacturer, $5M to $500M revenue, on WooCommerce. They already know their ERP, net terms, PO flow and what a subscription is. They do not need WooCommerce explained. They are trying to decide whether to buy the official extension, pay a developer to bend it, or fund a custom build, and they want to know what to test before spending. Skim-first desktop readers, 5 to 15 minutes.

## 3. Format decision (MUST-FOLLOW-RULES section 11)

1. **Chosen: Format C (listicle with opinions), adapted.** Standard frame stays (H1, Summary, Introduction, TOC, body H2s, PAA, Conclusion, FAQ, author bio). The three routes are three opinionated body H2s ("use it as is", "extend it", "build custom"), each takes a position and names who should pick it. No "N things" title.
2. **Reason (one sentence).** The reader is choosing between named options, which is what Format C defends with opinions, and Format D has just been used twice in a row (43764, 43805) so a third playbook adds no structural variety.
3. **Recency check.** The inventory file is stale (last_updated 2026-09-09), so rotation is inferred from sibling briefs, the research and the corpus: 43845 (B), the RFQ form-vs-chat draft (B), 43805 (D), 43764 (D), 43758 (C), 43753 (E), 43728 (A or D, unconfirmed), 43583 (A), 43420 / 43418 / 43414 (A), 43361 (likely A, unconfirmed), 43254 (D, from `high-risk-payment-gateways-2026-09-09.md`). Counts over the last 10: A about 3 to 4, D 2 to 3, B 2, C 1, E 1, F 0.
4. **Overused, therefore skipped.** Format A (3 to 4 of 10, at or over the limit). Format D (2 to 3 of 10 and the two newest published; the natural fit, but at risk of being the third). Format E skipped (used in 43753, and "standing orders are not subscriptions" is a setup, not a contrarian thesis). Format B skipped (two uses in the last two days). Format F skipped (no client result may be named).
5. **Caveat for the orchestrator.** Format of 43728 and 43361 is unconfirmed. If the publisher confirms D is at 2 or fewer, switching to D would also be allowed, but C is the safer pick and the outline works either way. Refresh the inventory before push.
6. **Format C obligation for the creator.** Every route section must pick a side in its own first sentence ("Use it as is when..."), name who it is wrong for, and end with a one-line verdict. No neutral surveys.

## 4. Title, slug, SEO fields

- **H1 (user-decided, sentence case, 73 chars):** WooCommerce standing orders for B2B: subscription plugin or custom build?
- **Slug:** `standing-orders-plugin-or-custom-build` (token check in audit: PASS).
- **Primary keyword / Yoast focus keyword:** WooCommerce standing orders. Secondary: B2B recurring orders WooCommerce, WooCommerce Subscriptions for B2B.
- **Do NOT target** "woocommerce subscription plugin" as primary or focus keyword and do not use it as an H2. It belongs to roundup 31274. The phrase "subscription plugin" appears only in the H1 as decided by the orchestrator, and in natural prose.
- **Yoast SEO title (59 chars):** Standing Orders in WooCommerce: Plugin or Custom? | Virtina
- **Meta description (draft, creator must count 150 to 160):** B2B standing orders in WooCommerce: when the Subscriptions plugin works as is, when to extend it, and when to build custom. Includes a staging test list. (153 chars by hand count; verify.)
- **Categories:** WooCommerce (79), B2B eCommerce (84), as used on 43845. Tags from existing taxonomy.
- **Byline / category / Updated line:** follow recent posts (43764, 43845): none above the Summary, the theme prints its own byline. Never invent an author. Author bio = the standard brand-voice block from the latest push script, unchanged (intentional repeat, publisher whitelists it in the 8-gram check).

## 5. Length

Target 3,100 words, floor 2,700, hard cap 3,300 (counted over all visible prose including table, FAQ and Sources). Reading time about 13 minutes. Sentences max 20 words, paragraphs max 3 sentences, H2s sentence case, at least 6 H3s (plan has 14).

## 6. Structure

Order: Summary, Introduction, TOC, body H2 1 to 7, People also ask, Conclusion, FAQ, Sources and verification, author bio. Every body H2 carries an `id` matching the TOC. First sentences below are locked in meaning; the creator may tighten wording but must keep each at 20 words or fewer and must answer the H2 directly.

### Summary (Template A, about 80 words, no links)
Quotable block with the date. Seed: "As of 5 November 2026, a B2B standing order is a repeat order on a fixed schedule, with agreed lines, price and terms. The official WooCommerce Subscriptions plugin can run it as is when renewals follow a saved payment method or a manual pay step. Extend it when one rule is missing. Build custom when the plugin's billing model does not match your order model." Keyword in the first sentence area.

### Introduction (Template B, about 160 words, three short paragraphs, no links)
- P1: concrete scene, no statistic. A distributor sends the same eight lines to the same customer on the first of every month. Someone on the team re-keys it. The owner asks whether a plugin can do it.
- P2: entity definition, one fresh sentence (not the boilerplate platform sentence): "Virtina is an eCommerce solutions partner for B2B and B2C brands; its WooCommerce work includes custom plugin development and ERP integration." Then promise: three routes, a comparison table, a staging test list.
- P3 "How this was checked" (bold lead-in): checked on 5 November 2026 against WooCommerce's own documentation pages for Subscriptions (renewal process, payment gateways, FAQ) and its product page; behavior that no source documents is written as a test to run, not as a fact; no prices are quoted because they change.

### TOC (Template C)
One entry per body H2, then `#people-also-ask`, `#conclusion`, `#faq`, `#sources`.

### H2 1 (about 260 words), id `what-is-a-standing-order`
**What is a B2B standing order, and how is it different from a consumer subscription?**
Locked first sentence: "A B2B standing order is a repeat order on a fixed schedule, with agreed lines, price and terms."
- Label it as Virtina's working definition, not a quoted standard.
- H3 **What does a standing order carry that a subscription does not?** Account-specific price, multi-line orders, PO or invoice payment, approval, ERP handoff. Say these are what the buyer's account brings, not what any plugin ships. Terms to include naturally: purchase order, net 30, accounts receivable, customer-specific price.
- H3 **Who controls the schedule, the buyer or the seller?** Short, opinion-labeled. Some programs are seller-managed replenishment, some are buyer-confirmed each cycle. This choice changes which route fits. Link once to 37714 only if it reads naturally ("subscription business model"); do not borrow its replenishment definitions.

### H2 2 (about 400 words), id `use-it-as-is`
**Can the official WooCommerce Subscriptions plugin run B2B standing orders as is?**
Locked first sentence: "Yes, if your standing orders behave like subscriptions: a set interval and a payment method that can renew."
Route 1 verdict: use as is when the interval is standard, the price does not vary by account at renewal, and the buyer either has a saved payment method or will pay each renewal.
- H3 **Automatic or manual renewal: which fits a distributor?** Facts 1, 2, 4: automatic renewals charge the saved method with no action; manual renewals create a pending renewal order the customer pays after logging in; any gateway can process manual renewals; manual is off by default and the docs advise against it for subscriptions renewing more than once a year. Inference, labeled: a PO or invoice buyer fits the manual path but needs a human to pay each interval. Link once to `woocommerce-b2b-net-payment-terms` (anchor "net payment terms"). External link 1: the renewal-process doc.
- H3 **What happens when a renewal payment fails?** Fact 3: default is on hold, the customer is told to pay the failed order from My Account; optional payment recovery retries and emails; renewals run through Action Scheduler; if the gateway is deactivated the renewal order is created pending with a manual-payment note. Link: "payment gateway integration" (service page) only if it reads as help, not as a pitch.
- H3 **What do the plugin's own pages not say?** Fact 8 and the Do-not-assert list: the product page lists trials, sign-up fees, billing synchronization, proration, failed-payment retries and a health check, and says nothing about customer-specific pricing, net terms or approval. Say "its documentation does not say" and point to the staging tests in H2 7. Not "it does not support".
- One more roundup mention, once: "other WooCommerce subscription plugins" with a single link to 31274 (anchor "WooCommerce subscription plugins"). No plugin named. No comparison with other plugins.
- **Image body 1 after this section (inside the section box).**

### H2 3 (about 320 words), id `extend-the-plugin`
**When is extending the plugin the better route?**
Locked first sentence: "Extend the plugin when it handles billing correctly but one rule, interval or field is missing."
Route 2 verdict: the middle route is right for most distributors with a mostly standard schedule and one or two account-specific rules.
- H3 **What counts as an extension, and what counts as a rewrite?** Fact 5: the official FAQ describes custom billing intervals (example: every 10 weeks) and custom lengths (example: 36 months) via a small plugin using a filter, needing Subscriptions 1.4.4 or later, some gateways limit lengths; the FAQ says this is developer-level and outside Woo's support policy. Opinion: if you hook filters and keep the plugin's billing engine, that is an extension. If you replace how renewals are created or charged, that is a rebuild.
- H3 **What does extending commit you to?** Fact 9 (see HPOS rule below): custom code that touches subscription data must use WooCommerce CRUD methods, not direct database queries. Action Scheduler runs the renewals. Every plugin update is a retest. Link once to `woocommerce-hpos-plugin-compatibility` (anchor "HPOS plugin compatibility").
- Service CTA, natural prose, no "our": one link to `woocommerce-plugin-development` (anchor "custom WooCommerce plugin development") as the place this work is done.

### H2 4 (about 330 words), id `build-custom`
**When does a custom build earn its cost?**
Locked first sentence: "Build custom when the plugin's billing model fights your order model at every renewal."
Route 3 verdict: custom is right when the schedule, price or approval step is the product itself, for example a buyer-approved draft order each cycle instead of an automatic charge. Opinion-labeled: many B2B "standing orders" are scheduled draft orders that a buyer confirms, which is a different thing from a subscription charge.
- H3 **What do you take on when you build?** Prose, not a bullet dump: gateway tokens and retries, failed-payment holds, Action Scheduler jobs, HPOS-safe data access (fact 9), staging safety, the ERP write path, and the fact that Woo's own FAQ says subscription scale depends on hosting, data and other plugins (fact 6, paraphrase, no numbers).
- H3 **Which signs say a build is justified?** This one IS list-shaped: use Template F bullets (4 to 5 items): a renewal price that must come from an ERP at renewal time; payment by invoice with terms the plugin cannot represent; a buyer approval step before each shipment; a schedule that follows a contract, not a fixed interval; renewals that must create ERP orders in a non-standard format. Each item framed as a test result you would see, not as a plugin limit.
- Link: "WooCommerce ERP integration" (`woocommerce-erp-integration`). Link: "WooCommerce development services" (`/platforms/woocommerce-development-services/`). Keep total CTA link count to these two plus the plugin development link from H2 3, all as factual references.

### H2 5 (about 250 words), id `compare-the-three-routes`
**How do the three routes compare side by side?**
Locked first sentence: "Compare the three routes by who pays at renewal, what you maintain and what you must test first."
**Comparison table (Template N), 4 columns, 3 data rows, identical depth per row, no check marks, no prices:**

| Route | Best when | Who pays at renewal | What you maintain | Test first |
|---|---|---|---|---|

(5 columns allowed on desktop; if width is an issue, drop "Best when" into the row label.) Cell content comes ONLY from facts 1 to 9 or from clearly labeled Virtina opinion ("Virtina view"). Rows:
1. Use as is. Standard interval. Saved method pays automatically, or the customer pays a manual renewal. Maintenance: plugin and gateway updates. Test first: the failed-payment path and whether the renewal price matches what the account signed up for.
2. Extend. One missing rule or interval. Same payment paths as route 1. Maintenance: your small plugin on every update, HPOS-safe data access. Test first: the filter on staging with a real gateway in test mode.
3. Build custom. Order model differs from a subscription. Payment path is whatever you design. Maintenance: everything, including retries and scheduling. Test first: renewal, failure, ERP write and staging safety from day one.
Caption (Template N, 14px grey): "Checked against WooCommerce documentation on 5 November 2026. The Best when and Test first columns are Virtina's view, not documentation."
- H3 **Does the table change if you are on HPOS?** Short. Only if there is a sourced sentence (see HPOS rule). Otherwise drop this H3 and use a different one, for example **What is the cheapest route to test first?** (answer: route 1 on staging, since it costs the least to disprove). Do not name prices.
- **Image body 2 after this section.**

### H2 6 (about 240 words), id `which-route-fits`
**Which route fits your store?**
Locked first sentence: "Pick the route by your payment method, your pricing rules and how many accounts renew on the same day."
- H3 **Which store profiles fit each route?** Short prose, three profiles, each ending in a verdict line: (a) buyers pay by card on file, standard monthly schedule, one price list: route 1; (b) buyers pay by PO or invoice, a few account-specific rules: route 2, with manual renewals; (c) price comes from the ERP at renewal, buyer approves each cycle: route 3. These are Virtina opinions and are labeled.
- H3 **When should you ask for help instead of testing alone?** Honest: when the staging tests in H2 7 fail on the pricing or payment rows, or when more than one ERP is involved. This is the soft CTA. No "reach out"; use "contact" or "talk to us" only if a link is not needed (no link in this sentence).

### H2 7 (about 300 words), id `staging-tests`
**What should you test on a staging site before you pick a route?**
Locked first sentence: "Run these tests on a staging site before you pick a route, and keep it out of live payment mode."
Fact 7: Woo's FAQ warns that a staging site in live mode can cause customers to be charged twice on renewal. This is a real, sourced risk and is the lead warning.
- H3 **Which seven tests settle the choice?** Template F bullets with bold "Test N." labels (genuinely sequential): (1) Renewal price: sign up an account that has a customer-specific price, run the renewal early and compare the renewal order line to the price you expect. (2) Payment path: sign up a PO or invoice buyer with manual renewals on and watch who gets which email and what status the renewal order holds. (3) Terms: check whether a renewal order can use your net-terms or purchase-order method at all. (4) Failed payment: force a decline in gateway test mode and confirm the on-hold state, the recovery behavior and the customer message. (5) Stock: renew a line that is out of stock or backordered. (6) ERP: confirm a renewal order reaches your ERP like a manually placed order. (7) Gateway off: deactivate the gateway on staging and confirm the renewal order is created pending with a manual-payment note (fact 3). Every item is a test, never a claim about what the plugin does. Link in test 6: already used `woocommerce-erp-integration` in H2 4, so do not link twice; or move the ERP link here and drop it from H2 4. One link per target.
- **Image body 3 after this section.**

### People also ask (Template H, about 200 words, 4 questions, answers 2 to 3 sentences, no links)
1. Is a standing order the same as a subscription? (No: a subscription is a billing arrangement; a standing order carries account price, terms and often approval. Virtina's view.)
2. Do B2B standing orders need a payment gateway? (Automatic renewals need a gateway that supports them; manual renewals work with any gateway, per Woo's renewal docs.)
3. What is Action Scheduler and why does it matter here? (Renewals run through it; fact 3.)
4. Should a buyer approve each standing order before it ships? (Virtina view: depends on order value and stock risk; a design decision, not a plugin setting.)

### Conclusion (Template I, about 110 words, white text, no links)
Restate the three routes in two short paragraphs with the verdict rule: use as is when it behaves like a subscription, extend when one rule is missing, build when the order model differs. End with the one thing to do this week: run test 1 and test 2 on staging. No "in conclusion". No CTA link in the conclusion (rule: internal links in body sections only).

### FAQ (Template J, 7 items, about 380 words, no links)
1. What is a standing order in WooCommerce?
2. Does WooCommerce have standing orders built in? (Say: WooCommerce's documentation covers recurring billing through the Subscriptions extension and lists no separate standing-order feature, as checked 5 November 2026.)
3. Can distributors pay renewals by purchase order or invoice? (Manual renewals work with any gateway; buyer pays each interval; PO and net-terms behavior is a staging test.)
4. What happens when a renewal payment fails? (Fact 3.)
5. Can you set a billing interval the plugin does not offer? (Fact 5, with the support-policy caveat.)
6. How do you avoid double billing on a staging site? (Fact 7.)
7. Does a custom build avoid the plugin's limits? (It removes some and adds the maintenance listed in H2 4.)

### Sources and verification (about 80 words, styled like the box on 43845)
Names the pages checked and the date, no extra links: WooCommerce Subscriptions renewal-process document, payment-gateways document, FAQ, product page, and the developer blog on HPOS. States that behavior with no source is framed as a test. Only 2 external links exist in the whole post (see section 8), and they sit in the body.

## 7. Facts bank (dated, from the research, fetched 5 November 2026)

| # | Fact (paraphrase) | Source | Status |
|---|---|---|---|
| 1 | Automatic renewals charge the saved method; Marketplace gateway extensions are sorted by supported subscription features | woocommerce.com payment-gateways doc, renewal-process doc | Verified |
| 2 | Manual renewals create a pending renewal order the customer pays after logging in; any gateway works; off by default; docs advise against it for subscriptions renewing more than once a year; coupons and taxes generally locked at signup | renewal-process doc | Verified |
| 3 | Failed automatic payment leaves the subscription on hold; optional payment recovery retries and emails; renewals run via Action Scheduler; gateway deactivated means the renewal order is created pending with a manual-payment note | renewal-process doc | Verified |
| 4 | A gateway outside the hand-picked list may still support automatic renewals and can be tested; manual renewals work regardless | Subscriptions FAQ | Verified |
| 5 | Custom billing intervals and lengths possible through a small plugin using a filter (needs Subscriptions 1.4.4+, some gateways limit lengths); developer-level, outside Woo's support policy | Subscriptions FAQ | Verified |
| 6 | No fixed subscription cap; problems depend on hosting, data and other plugins | Subscriptions FAQ | Verified. Paraphrase only, no numbers |
| 7 | A staging site in live mode can cause customers to be charged twice on renewal | Subscriptions FAQ | Verified |
| 8 | Product page lists trials, sign-up fees, billing synchronization, proration, failed-payment retries, gifting, combined orders, health check; says 25+ gateways for automatic renewals; names nothing on customer-specific pricing or net terms | woocommerce.com product page | Verified as of fetch date. Avoid version, rating and install numbers |
| 9 | Subscriptions 4.9.0 added HPOS compatibility; subscriptions stored as `shop_subscription` in `wc_orders`; custom integrations must use WooCommerce CRUD methods | developer.woocommerce.com HPOS post | **Snippet-confirmed only, re-check.** Until the orchestrator fetches the full page, write it without the version number ("WooCommerce's developer blog says Subscriptions has supported HPOS since an earlier release and that custom code must use CRUD methods"), or drop the sentence |

**Possibly upgradeable (not in the research, found by this run's search):** the official WooCommerce Purchase Order Gateway document appears to say the PO field shows at checkout when a subscription product is in the cart and manual renewals are on, with the order held On hold until staff mark it complete. This came from a search summary only. If the orchestrator fetches `woocommerce.com/document/woocommerce-purchase-order-gateway/` and it checks out, it turns test 2 from a guess into a sourced fact and is the strongest B2B-specific content in the post. Until then it is a staging test.

## 8. Links

Internal (8 planned, 5 to 10 required; every target is a published page or post per the 2026-11-04 corpus with canonical permalink equal to the URL below; HTTP status NOT confirmed in this run, see section 10):

| Target | Anchor | Where |
|---|---|---|
| `/woocommerce-subscription-plugins/` (31274, roundup) | WooCommerce subscription plugins | H2 2, once only |
| `/woocommerce-plugin-development/` (page 10745) | custom WooCommerce plugin development | H2 3 |
| `/platforms/woocommerce-development-services/` | WooCommerce development services | H2 4 |
| `/woocommerce-b2b-net-payment-terms/` (42297) | net payment terms | H2 2 |
| `/woocommerce-b2b-pricing-and-access-setup/` (42393) | role-based pricing setup | H2 1 or H2 3, once |
| `/woocommerce-erp-integration/` (42108) | WooCommerce ERP integration | H2 4 or H2 7, once |
| `/woocommerce-hpos-plugin-compatibility/` (43361) | HPOS plugin compatibility | H2 3 |
| `/woocommerce-payment-gateway-integration/` | payment gateway integration | H2 2 |

Optional: `/what-is-subscription-business-model-ecommerce/` (37714, anchor "subscription business model") in H2 1. Do NOT link 43753 (quick order form) or 43845 (backorders) unless the publisher confirms status `publish`; the corpus dated 2026-11-04 does not contain them and the 43845 memory note says it is a draft. Never link `/contact/`, `/ecommerce-development-services/`, `/woocommerce-development-services/` (301) or `/ecommerce-seo-services/`. Anchors: 2 to 5 word clean noun phrases, none contains "our", none repeats, no links in intro, conclusion or FAQ.

External (max 2, `target="_blank" rel="noopener noreferrer"`, no competitor domains; woocommerce.com is the platform vendor and allowed): (1) the Subscriptions renewal-process document in H2 2; (2) the Subscriptions FAQ document in H2 3 or H2 7. The gateway list, product page and developer blog are named in prose without links.

**ChatSKU: omit.** ChatSKU is an AI catalog chat and RFQ platform. Scheduled repeat orders are not a conversation or quote problem, so a mention would not be honest and would dilute the entity. No ChatSKU link, no ChatSKU name.

## 9. Uniqueness and phrasing guard

Formal audit: see `competitor-analysis-standing-orders-2026-11-05.md`, section A (Checks 1 to 5 all PASS, with margins noted). Slug passes. The 8-gram check (post-draft, publisher) must compare the stripped prose (remove `<style>` and inline style attributes) against: 31274, 17289, 37714, 42393, 42297, 43753. Also run it against 43845, 42108 and 43361 as a courtesy. Specific traps:
- **31274:** roundup phrasing ("Types of WooCommerce Subscription Plugins", "How do you install a WooCommerce subscription plugin", "Tips to choose"), and any "what is WooCommerce Subscription" definition sentences.
- **17289:** migration vocabulary and its "highlights" bullets. This post never covers migration.
- **37714:** its "Replenishment Subscription" definition ("automatic workplace shipments at regular intervals"). Define a standing order from scratch.
- **42393:** its role-based pricing headings and its quote field list (SKU, quantity, account ID, spec notes, target delivery date). Do not reuse the field list; link instead.
- **42297:** net 30 and net terms explanations. Define terms in one fresh sentence at most and link.
- **43753:** its reorder-line vocabulary. The corpus also holds a sentence on saved lists streamlining "the process of recurring orders, reducing the time spent searching for and adding products" in older posts; do not echo it.
- **Boilerplate platform sentence** (feedback_virtina_boilerplate_platform_sentence): do not write any "builds on WooCommerce, Magento, BigCommerce and Shopify" sentence. The only Virtina description is the fresh entity sentence in the Introduction. Author bio is the one whitelisted repeat.
- Use each approved locked sentence once; no sentence longer than 8 words may match any existing post.

## 10. Verification status of this brief (be honest in the report)

- **Done:** reads of MUST-FOLLOW-RULES (all 12 sections), brand-teal, body-font-size, visual-specs, html-templates, voice, audience, brand, the five named memory notes; inventory lines 1 to 497 (the rest is the older back catalog, covered by the 598-item corpus grep); corpus grep of `virtina-corpus-2026-11-04.json` for slugs, titles, headings and body phrases.
- **Not done (this run had WebSearch only, no page fetch, no curl):** HTTP status of any Virtina URL (redirects off); full-page fetch of any competitor beyond the two the researcher fetched; the live `/pages` second page and live `/search` REST sweep. The publisher or orchestrator must (a) confirm each internal URL returns 200 with redirects off (virtina.com 429s curl, use WebFetch or REST and read the status honestly), (b) re-run `/wp-json/wp/v2/pages?per_page=100&page=2` and `/search?search=standing orders`, (c) refresh the inventory.
- The corpus `link` field equals the URL in the table for every planned internal link, which means WordPress itself does not redirect them, but a redirect plugin could still exist.

## 11. Image plan (user's HIGH-IMPACT style, overrides the generic person-at-desk rule)

Rules for all four: cinematic photorealistic, moody teal and amber grade, deep contrast, ONE image split by a thin bright vertical line into two panels showing the same moment from two sides (body 2 uses three panels), no people as the subject, no logos, no numbers, no price figures, at most 6 short bold on-image words in total, large and legible, nothing small. Identical neutral icons only; no check marks or question marks that could read as capability claims. Leave the top 20 percent calm. Export at 2x the displayed size, JPEG q90 or higher, 4:4:4, no upscaling, view at 100% before upload. Place body images inside the section box (before the closing `</div>`), never between boxes. The featured image is NOT repeated in the body (theme prints it); the body starts at the Summary. Add the Virtina logo pill to the featured image only (white rounded pill, about 13.75% of image width, logo from `social/brand/virtina-logo.webp` at about 85% of pill width, bottom-right, about 1.6% right and 3.6% bottom margin, white at about 93% opacity with a faint shadow).

**Featured (display 1309x500, request 2.6:1 ultra-wide, upload at 1895x724 or larger).** Subject: the article's subject, standing order versus subscription.
Prompt: "Cinematic photorealistic ultra-wide 2.6:1 image split by a thin bright vertical line into two panels, no people. LEFT panel: one laptop showing a single product with a payment card icon and a big bold title SUBSCRIPTION. RIGHT panel: the same desk, a laptop showing a long multi-line order sheet with a clipboard of paperwork beside it and a big bold title STANDING ORDER. Teal and amber grade, deep contrast, shallow depth of field, calm top 20 percent of the frame, no logos, no numbers, no small text, only those two words." Alt (80 to 150 chars): "Split view of a consumer subscription screen beside a B2B standing order sheet, showing why WooCommerce standing orders differ from subscriptions."

**Body 1, after H2 2 (renewal modes), display 670x352, request 2:1, upload at 1340x704 or larger.**
Prompt: "Cinematic photorealistic 2:1 image split by a thin bright vertical line, no people. LEFT: a monitor showing a payment going through on its own, big bold word AUTOMATIC, a card reader beside it. RIGHT: the same office, a monitor showing an unpaid renewal order waiting, a printed purchase order paper and a stamp beside it, big bold word MANUAL. Teal and amber grade, calm top 20 percent, no logos, no numbers, no small text, only those two words." Alt: "Split panel comparing an automatic WooCommerce subscription renewal paid by a saved card with a manual renewal waiting on a purchase order."

**Body 2, after H2 5 (three routes), display 670x352, request 2:1.**
Prompt: "Cinematic photorealistic 2:1 image split by two thin bright vertical lines into three equal panels, no people. Each panel shows the same laptop on the same desk with the same neutral grey icon on screen. Panel titles in big bold type: AS IS, EXTEND, BUILD. Under the middle laptop a small toolkit, under the right laptop an architect's blueprint, under the left laptop nothing. Teal and amber grade, deep contrast, calm top 20 percent, no logos, no numbers, no check marks, no question marks, no small text." Alt: "Three equal panels labeled as is, extend and build, comparing the three routes for WooCommerce B2B standing orders on identical laptops."

**Body 3, after H2 7 (staging tests), display 670x352, request 2:1.**
Prompt: "Cinematic photorealistic 2:1 image split by a thin bright vertical line, no people. LEFT: a laptop with a test-mode banner and a big bold word STAGING. RIGHT: the same store on a second laptop with a big bold word LIVE, and one payment card on the desk between them with two receipts printing, big bold words DOUBLE CHARGE in a red tag. Teal and amber grade, calm top 20 percent, no logos, no numbers, no small text, only those words." Alt: "Staging and live WooCommerce stores sharing one payment card with two receipts printing, illustrating the double-billing risk on a staging site."

Offer 3 to 4 variants per image to the user. Check each image against its H2 and the facts table before upload. Do not use the 4 prompts above to imply a plugin defect; image 3 shows a documented warning (fact 7), not a bug.

## 12. Must include

- The date "5 November 2026" in the Summary, the Introduction and the table caption.
- The three routes named exactly: use as is, extend, build custom.
- Facts 1 to 8 as paraphrase with attribution; fact 9 only as allowed in the facts table.
- At least 10 of: standing order, recurring order, repeat order, automatic renewal, manual renewal, renewal order, payment token, on hold, payment retry, dunning, purchase order, net 30, accounts receivable, customer-specific price, ERP sync, Action Scheduler, HPOS, billing synchronization, proration.
- Comparison table (Template N) with caption and date. A staging test list. FAQ of 7 with plain answers. Case snippet: the Introduction scene counts as the problem/solution example.
- Questions that an AI can lift: every H2 first sentence answers its H2.

## 13. Must NOT include

- Any price, any rating, install count or version number except where the facts table allows it.
- Any claim about role-based pricing plugins (B2BKing, Wholesale Suite or others) applying a tier price on renewals, or about the official plugin supporting net terms, PO payment, approval or per-account catalogs. Tests only.
- Other subscription plugins by name (YITH, SUMO and others are vendor-sourced and unverified), Shopify apps, or any competitor agency.
- The words "Trends-proven", "data shows demand", or any Trends claim.
- "woocommerce subscription plugin" as an H2, focus keyword or repeated exact-match anchor.
- Statistics of any kind, Baymard, or invented client results. No ChatSKU. No em dashes in any form. No banned hype or filler words. No "our" in anchors. No links in intro, conclusion or FAQ.
- The boilerplate platform sentence. Any sentence over 20 words. Any paragraph over 3 sentences.
- 31274's structure (a ranked list of plugins). This is a decision post.

## 14. Headline direction

Declarative, sentence case, no hype, no exclamation. The H1 is locked by the orchestrator. Working alternates only if the user rejects it:
1. WooCommerce standing orders for B2B: subscription plugin or custom build? (locked)
2. B2B standing orders on WooCommerce: use the plugin, extend it or build custom
3. Do WooCommerce standing orders need a custom build, or does Subscriptions do the job?

## 15. Open questions for the creator

- Whether to move the ERP link to H2 7 (test 6) or leave it in H2 4. One link per target in either case.
- Whether the "Best when" column fits the table width. If not, fold it into the Route cell.
- Exact wording of the three profile verdicts in H2 6. They must stay labeled as Virtina opinion.
- Pace: keep the table before the long profile section so an AI reading top to bottom meets the decision early.

**Locked:** thesis, H1, slug, Format C, the seven body H2 headings and order, the three route names, the 9-row facts table and its status flags, the link table and anchors, the no-ChatSKU rule, the no-prices rule, the staging-test framing, the image plan (4 images, 4 prompts), the banned items list.
