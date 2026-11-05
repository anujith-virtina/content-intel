---
title: "WooCommerce standing orders for B2B: subscription plugin or custom build?"
client: virtina
date: 2026-11-05
slug: standing-orders-plugin-or-custom-build
stage: draft
brief: clients/virtina/output/briefs/standing-orders-plugin-or-custom-build-2026-11-05.md
format: C (opinionated options, adapted to a decision post)
seo_title: Standing Orders in WooCommerce: Plugin or Custom? | Virtina
meta_description: B2B standing orders in WooCommerce: when the Subscriptions plugin works as is, when to extend it and when to build custom, plus seven staging tests to run.
focus_keyword: WooCommerce standing orders
word_count: 3100
headlines:
  - WooCommerce standing orders for B2B: subscription plugin or custom build?
  - B2B standing orders on WooCommerce: use the plugin, extend it or build custom
  - Do WooCommerce standing orders need a custom build, or does Subscriptions do the job?
---

[FEATURED IMAGE: Split view of a consumer subscription screen beside a B2B standing order sheet, showing why WooCommerce standing orders differ from subscriptions. | concept: Cinematic ultra-wide image split by a thin bright vertical line. Left panel is a laptop with a single product and a payment card icon titled SUBSCRIPTION. Right panel is the same desk with a long multi-line order sheet and a clipboard titled STANDING ORDER. Teal and amber grade, no people, Virtina logo pill bottom-right.]

[SUMMARY]

A B2B standing order is a repeat order on a fixed schedule, with agreed lines, price and terms. This guide was checked on 5 November 2026.

WooCommerce standing orders can run on the official Subscriptions plugin as is. That works when renewals follow a saved payment method or a manual pay step.

Extend the plugin when one rule is missing. Build custom when its billing model does not match your order model.

[INTRODUCTION]

A distributor sends the same eight lines to the same customer on the first of every month. Someone on the team re-keys the order each time. The owner asks whether a plugin can do it.

Virtina is an eCommerce solutions partner for B2B and B2C brands. Its WooCommerce work includes custom plugin development and ERP integration. This guide lays out three routes, a comparison table and a staging test list.

**How this was checked:** the facts below come from WooCommerce's own Subscriptions documentation, read on 5 November 2026. That covers the renewal process, payment gateways, the FAQ and the product page. Behavior that no source documents is written as a test to run, and no prices are quoted.

[TOC: sections 1 to 7 H2s, then People Also Ask, Conclusion, Frequently asked questions, Sources and verification]

[H2: What is a B2B standing order, and how is it different from a consumer subscription?]

A B2B standing order is a repeat order on a fixed schedule, with agreed lines, price and terms. That is Virtina's working definition, not a quoted standard.

A consumer subscription is a billing arrangement for a product or plan. A standing order is an agreement between two companies about what ships, at what price and on what terms.

[H3: What does a standing order carry that a subscription does not?]

A standing order carries whatever the buyer's account brings with it. That means a customer-specific price, several lines per order and payment by purchase order or invoice. It may also mean an approval step and a handoff to your ERP.

These come from the account, not from any plugin. A distributor on net 30 expects the renewal to land in accounts receivable like any other order. Setting up account prices is its own job, covered in [INTERNAL LINK: role-based pricing setup | purpose: /woocommerce-b2b-pricing-and-access-setup/].

[H3: Who controls the schedule, the buyer or the seller?]

In a seller-managed program, you control the schedule and the order ships on its own. In a buyer-confirmed program, someone approves each cycle before it ships.

In Virtina's view, this choice decides the route more than any feature does. A seller-managed program fits a charge or invoice that runs by itself. A buyer-confirmed program is closer to a scheduled draft order that a person approves.

Many B2B programs are the second kind. That is a different thing from a subscription charge. When the buyer reorders by hand instead, a [INTERNAL LINK: quick order form | purpose: /quick-order-form-line-checks/] is the lighter tool.

[H2: Can the official WooCommerce Subscriptions plugin run B2B standing orders as is?]

Yes, if your standing orders behave like subscriptions: a set interval and a payment method that can renew. Use it as is when the interval is standard and the price does not change by account at renewal.

The buyer should also have a saved payment method or agree to pay each renewal. It is the wrong route when the renewal price must come from somewhere else, such as your ERP.

[H3: Automatic or manual renewal: which fits a distributor?]

Automatic renewal charges the saved payment method with no action from the customer. Manual renewal creates a pending renewal order, and the customer pays it after logging in. Both modes are described in WooCommerce's [EXTERNAL LINK: renewal process documentation | url: https://woocommerce.com/document/subscriptions/renewal-process/ | target=_blank rel="noopener noreferrer"].

Any payment gateway can process manual renewals, and the setting is off by default. The same document advises against manual renewals for subscriptions that renew more than once a year. It also says coupons and taxes are generally fixed at sign-up.

In Virtina's view, a buyer who pays by purchase order or invoice fits the manual path in principle. A person still has to pay each interval.

Can your purchase order or [INTERNAL LINK: net payment terms | purpose: /woocommerce-b2b-net-payment-terms/] method pay a renewal order? That is a staging test, covered in the last section.

[H3: What happens when a renewal payment fails?]

A failed automatic payment leaves the subscription on hold by default. The customer is told to pay the failed order from My Account.

An optional payment recovery feature retries the charge and emails the customer. That is dunning in plain terms. Renewals run as scheduled jobs through Action Scheduler.

If the gateway is deactivated, the renewal order is created as pending with a manual-payment note. Gateway behavior varies, so scope [INTERNAL LINK: payment gateway integration | purpose: /woocommerce-payment-gateway-integration/] early if you plan to add a new gateway.

[H3: What do the plugin's own pages not say?]

The product page lists trials, sign-up fees, billing synchronization, proration and failed-payment retries. It also lists gifting, combined orders and a health check. It says nothing about customer-specific pricing, net terms or approval.

That is a statement about the documentation, not a verdict on the plugin. The staging tests in the last section settle it. Other [INTERNAL LINK: WooCommerce subscription plugins | purpose: /woocommerce-subscription-plugins/] exist, but this guide does not compare them.

**Verdict:** use it as is when it behaves like a subscription. Skip it when a person must approve or reprice each cycle.

[BODY IMAGE: Split panel comparing an automatic WooCommerce subscription renewal paid by a saved card with a manual renewal waiting on a purchase order. | concept: Cinematic 2:1 image split by a thin bright vertical line, no people. Left monitor shows a payment going through on its own with a card reader, titled AUTOMATIC. Right monitor shows an unpaid renewal order beside a printed purchase order and stamp, titled MANUAL. Teal and amber grade.]

[H2: When is extending the plugin the better route?]

Extend the plugin when it handles billing correctly but one rule, interval or field is missing. For most distributors with a mostly standard schedule and one or two account-specific rules, this is the right middle route.

It is the wrong route when the rule you need replaces how renewals are created or charged. Then you are rebuilding, not extending.

[H3: What counts as an extension, and what counts as a rewrite?]

WooCommerce's own [EXTERNAL LINK: Subscriptions FAQ | url: https://woocommerce.com/document/subscriptions/faq/ | target=_blank rel="noopener noreferrer"] points to this route. It describes custom billing intervals, such as every 10 weeks, and custom lengths, such as 36 months. Both are set through a small plugin that uses a filter.

The FAQ says some gateways limit lengths. It also says this is developer-level work outside WooCommerce's support policy. That is a documented fact worth weighing before you commit.

In Virtina's view, the line is simple. If you hook filters and keep the plugin's billing engine, that is an extension. If you replace how renewals are created or charged, that is a rebuild.

[H3: What does extending commit you to?]

Extending commits you to every plugin update. Each release is a retest of your code on staging. Renewals still run through Action Scheduler, so a stuck job affects your rule too.

Custom code that touches orders should use WooCommerce's CRUD methods instead of direct database queries. That keeps it working with high-performance order storage (HPOS). A checklist for [INTERNAL LINK: HPOS plugin compatibility | purpose: /woocommerce-hpos-plugin-compatibility/] helps before each update.

In Virtina's view, this work is usually a smaller scope than a full build. It is done as [INTERNAL LINK: custom WooCommerce plugin development | purpose: /woocommerce-plugin-development/], with the extension kept small on purpose.

**Verdict:** extend when one rule is missing and the rest of the plugin fits.

[H2: When does a custom build earn its cost?]

Build custom when the plugin's billing model fights your order model at every renewal. That is right when the schedule, the price or the approval step is the product itself.

An example is a buyer-approved draft order each cycle instead of an automatic charge. In Virtina's view, many B2B standing orders are exactly that. They are scheduled draft orders that a buyer confirms, which is not a subscription charge.

[H3: What do you take on when you build?]

You take on everything the plugin did for you. That includes gateway tokens and retries, failed-payment holds and Action Scheduler jobs. It also includes HPOS-safe data access and a staging site that cannot bill real customers.

You also own the ERP write path. WooCommerce's Subscriptions FAQ says scale depends on hosting, data and other plugins, not on a fixed cap. In Virtina's view, a custom build moves that risk onto your team.

The ERP link needs the most care. A renewal order that reaches your ERP in a different format from a manual order creates rework. A [INTERNAL LINK: WooCommerce ERP integration | purpose: /woocommerce-erp-integration/] plan should cover renewals from day one.

[H3: Which signs say a build is justified?]

These are test results you would see on staging. Any one of them is a reason to price a build:

- **Renewal price from the ERP:** the renewal order line shows the wrong price, and the right one lives in your ERP at renewal time.
- **Invoice terms:** payment by invoice uses terms that the renewal order cannot represent.
- **Buyer approval:** the buyer must approve each shipment before it goes out.
- **Contract schedule:** dates follow a contract, not a fixed interval.
- **ERP order format:** renewals must create ERP orders in a non-standard format.

Teams that reach this point usually need [INTERNAL LINK: WooCommerce development services | purpose: /platforms/woocommerce-development-services/] for the build itself. Price it against the maintenance list above, not just the first release.

**Verdict:** build when the order model, not a single rule, is what differs.

[H2: How do the three routes compare side by side?]

Compare the three routes by who pays at renewal, what you maintain and what you must test first. The table draws on the documentation above and on Virtina's view.

[TABLE: Three routes for B2B standing orders compared]

| Route | Best when | Who pays at renewal | What you maintain | Test first |
|---|---|---|---|---|
| Use as is | Standard interval, one price list, a saved payment method or a customer who pays each renewal | Automatic: the saved payment method. Manual: the customer pays a pending renewal order after login | Plugin and gateway updates | The failed-payment path, and whether the renewal price matches what the account signed up for |
| Extend | Mostly standard schedule with one missing interval, length or rule | The same two paths as use as is | Your small plugin on every update, with HPOS-safe data access | The filter on staging with a real gateway in test mode |
| Build custom | The order model differs from a subscription, such as buyer-approved cycles | Whatever payment path you design | Everything, including retries, scheduling and the ERP write path | Renewal, failure, ERP write and staging safety from day one |

Checked against WooCommerce documentation on 5 November 2026. The Best when and Test first columns are Virtina's view, not documentation.

[H3: Which route should you test first?]

Test route one first, on a staging site. It costs the least to disprove, because you change no code. If it passes the pricing and payment tests, you may need nothing more.

If it fails one rule, you have found your extension. If it fails the order model, you have found your build. Either way, the test result writes the brief.

[BODY IMAGE: Three equal panels labeled as is, extend and build, comparing the three routes for WooCommerce B2B standing orders on identical laptops. | concept: Cinematic 2:1 image split by two thin bright vertical lines into three equal panels, no people. The same laptop and neutral icon in each. Panel titles AS IS, EXTEND, BUILD. A small toolkit under the middle laptop and a blueprint under the right one. Teal and amber grade, no check marks.]

[H2: Which route fits your store?]

Pick the route by your payment method, your pricing rules and how many accounts renew on the same day. These profiles are Virtina's opinion, not documentation.

[H3: Which store profiles fit each route?]

Profile one: buyers pay by card on file, on a standard monthly schedule, from one price list. Use the plugin as is.

Profile two: buyers pay by purchase order or invoice, and you have a few account-specific rules. Extend the plugin and turn on manual renewals. Expect a person on the buyer's side to pay each interval.

Profile three: the price comes from the ERP at renewal, and the buyer approves each cycle. Build custom. A subscription charge is the wrong shape for that program.

If your accounts split across profiles, run the routes side by side. Start with the largest group and test the others on staging.

[H3: When should you ask for help instead of testing alone?]

Ask for help when the staging tests in the next section fail on the pricing or payment rows. Ask as well when more than one ERP is involved. Those are the cases where a wrong guess costs a renewal cycle.

As a suggestion, you could talk to Virtina with your test results in hand. A failed test is a better brief than a feature wish list.

[H2: What should you test on a staging site before you pick a route?]

Run these tests on a staging site before you pick a route, and keep it out of live payment mode. WooCommerce's FAQ warns that a staging site in live mode can cause customers to be charged twice on renewal.

Use gateway test mode, or deactivate the gateway. Never point a copy of the store at real saved payment methods.

[H3: Which seven tests settle the choice?]

Run them in order. Each one is a test to perform, not a claim about what the plugin does:

- **Test 1. Renewal price.** Sign up an account that has a customer-specific price. Run the renewal early and compare the renewal order line to the price you expect.
- **Test 2. Payment path.** Sign up a purchase order or invoice buyer with manual renewals on. Watch who gets which email and what status the renewal order holds.
- **Test 3. Terms.** Check whether a renewal order can use your net-terms or purchase-order method at all.
- **Test 4. Failed payment.** Force a decline in gateway test mode. Confirm the on-hold state, the recovery behavior and the customer message.
- **Test 5. Stock.** Renew a line that is out of stock or on backorder, and see what the renewal order does.
- **Test 6. ERP.** Confirm that a renewal order reaches your ERP the same way a manually placed order does.
- **Test 7. Gateway off.** Deactivate the gateway on staging. Confirm the renewal order is created as pending with a manual-payment note.

Tests 1 and 2 settle most decisions. If both pass, route one may be enough. If either fails, you now know which rule to extend or which model to rebuild.

[BODY IMAGE: Staging and live WooCommerce stores sharing one payment card with two receipts printing, illustrating the double-billing risk on a staging site. | concept: Cinematic 2:1 image split by a thin bright vertical line, no people. Left laptop with a test-mode banner titled STAGING. Right laptop titled LIVE. One payment card on the desk between them with two receipts printing and a red tag reading DOUBLE CHARGE. Teal and amber grade.]

[H2: People Also Ask]

[H3: Is a standing order the same as a subscription?]

No. A subscription is a billing arrangement. A standing order also carries account price, terms and often an approval step. That is Virtina's view, not a quoted standard.

[H3: Do B2B standing orders need a payment gateway?]

Automatic renewals need a gateway that supports them. Manual renewals work with any gateway, according to WooCommerce's renewal documentation. The buyer then pays each renewal order after logging in.

[H3: What is Action Scheduler and why does it matter here?]

Action Scheduler is the job queue that WooCommerce uses for background tasks. WooCommerce's renewal documentation says subscription renewals run through it. A stuck queue means a late renewal.

[H3: Should a buyer approve each standing order before it ships?]

It depends on order value and stock risk. In Virtina's view, this is a design decision, not a plugin setting. High-value or low-stock lines are the usual candidates for approval.

[H2: Conclusion]

Use the Subscriptions plugin as is when your standing orders behave like subscriptions. Extend it when one rule is missing. Build custom when your order model differs.

That is the rule, and staging is how you apply it. This week, run test 1 and test 2. They show whether the renewal price and the payment path survive a real cycle.

[H2: Frequently asked questions]

**What is a standing order in WooCommerce?**
It is a repeat order on a fixed schedule, with agreed lines, price and terms. That is Virtina's working definition. WooCommerce itself calls recurring billing a subscription.

**Does WooCommerce have standing orders built in?**
WooCommerce's documentation covers recurring billing through the Subscriptions extension. It lists no separate standing-order feature, as checked on 5 November 2026.

**Can distributors pay renewals by purchase order or invoice?**
Manual renewals work with any gateway, and the buyer pays each interval. Whether your purchase order or net-terms method can pay a renewal order is a staging test. Run test 3 to find out.

**What happens when a renewal payment fails?**
A failed automatic payment leaves the subscription on hold by default. The customer is told to pay the failed order from My Account. An optional payment recovery feature retries and emails the customer.

**Can you set a billing interval the plugin does not offer?**
WooCommerce's FAQ says yes, through a small plugin that uses a filter. That includes custom intervals and lengths. It is developer-level work outside WooCommerce's support policy, and some gateways limit lengths.

**How do you avoid double billing on a staging site?**
Keep staging out of live payment mode. WooCommerce's FAQ warns that a staging site in live mode can charge customers twice on renewal. Use gateway test mode or deactivate the gateway.

**Does a custom build avoid the plugin's limits?**
It removes some and adds others. You no longer fit the plugin's billing model. You now maintain retries, scheduling, HPOS-safe data access and the ERP write path yourself.

[H2: Sources and verification]

Each source below is named with what it supports. WooCommerce documentation pages carry no date, so they are read as published on 5 November 2026.

- **WooCommerce Subscriptions renewal process documentation.** Automatic and manual renewals, failed payments, payment recovery, Action Scheduler and gateway deactivation.
- **WooCommerce Subscriptions payment gateways documentation.** Gateway feature tables and how automatic renewals depend on the gateway.
- **WooCommerce Subscriptions FAQ.** Custom intervals and lengths, the support policy, scale and the staging double-billing warning.
- **WooCommerce Subscriptions product page.** The feature list, and what it does not mention.

Behavior with no source is written as a staging test. Role-based pricing, net terms and approval on renewals were not verified for any plugin.

[AUTHOR BIO: Template K, unchanged boilerplate]

---

QA BLOCK (not for publication)

**Word count.** About 3,100 words of visible prose by hand estimate (no script available). Summary about 75, Introduction about 160, H2 1 about 270, H2 2 about 430, H2 3 about 330, H2 4 about 340, H2 5 about 260 including table, H2 6 about 240, H2 7 about 300, PAA about 150, Conclusion about 55, FAQ about 330, Sources about 150. Publisher should recount after pour. Conclusion and PAA are short of the brief target.

**Internal links (9), all in body H2 sections.**
1. role-based pricing setup: /woocommerce-b2b-pricing-and-access-setup/ (H2 1)
2. quick order form: /quick-order-form-line-checks/ (H2 1)
3. net payment terms: /woocommerce-b2b-net-payment-terms/ (H2 2)
4. payment gateway integration: /woocommerce-payment-gateway-integration/ (H2 2)
5. WooCommerce subscription plugins: /woocommerce-subscription-plugins/ (H2 2, roundup 31274, once)
6. HPOS plugin compatibility: /woocommerce-hpos-plugin-compatibility/ (H2 3)
7. custom WooCommerce plugin development: /woocommerce-plugin-development/ (H2 3)
8. WooCommerce ERP integration: /woocommerce-erp-integration/ (H2 4)
9. WooCommerce development services: /platforms/woocommerce-development-services/ (H2 4)

**External links (2), body only, target=_blank rel="noopener noreferrer".**
1. renewal process documentation: https://woocommerce.com/document/subscriptions/renewal-process/ (H2 2)
2. Subscriptions FAQ: https://woocommerce.com/document/subscriptions/faq/ (H2 3)

No links in Summary, Introduction, PAA, Conclusion, FAQ or Sources. Post 43845 not linked. ChatSKU omitted. Optional 37714 not linked because it is not in the research's verified list.

**Least confident.**
- HPOS sentence (H2 3): based on a search snippet of the developer blog, worded without a version number. Re-check the full page or cut the sentence.
- "Action Scheduler is the job queue that WooCommerce uses for background tasks" (PAA 3) is general knowledge, not from the fetched research.
- "That is dunning in plain terms" labels the optional payment recovery feature with a generic term. The docs describe retries and emails, not the word dunning.
- "scale depends on hosting, data and other plugins, not on a fixed cap" paraphrases fact 6. Check wording against the FAQ.
- "gifting, combined orders" on the product page are from fact 8 as fetched. The product page can change.
- Quick order form URL /quick-order-form-line-checks/ came from the research's live search result. Confirm 200 with redirects off now that 43753 is published.
- Meta description is 155 characters by hand count. Meta title is 59. Verify both by script.
- Format C verdict lines are present for routes one to three, but the closing verdict for route one sits after the plugin-pages paragraph, not at the very end of the section.
