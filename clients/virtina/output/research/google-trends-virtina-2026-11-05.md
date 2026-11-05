---
title: "Research: WooCommerce standing orders for B2B, subscription plugin or custom build (Google Trends driven)"
client: virtina
date: 2026-11-05
topic: WooCommerce recurring/standing orders for B2B, Woo Subscriptions plugin vs custom build
audience: B2B ecommerce leaders (manufacturers, distributors, wholesalers) on WooCommerce
stage: research
slug: standing-orders-plugin-or-custom-build
---

# Research notes, 2026-11-05

Rules read first: MUST-FOLLOW-RULES.md (all 12 sections), reference/published-posts-inventory.md (first 497 of 1386 lines, plus Grep of the whole reference folder for wholesale/subscription/role-based/tiered), voice.md, audience.md, brand.md, and the memory notes named in the task. No Bash was available: uniqueness sweep ran through WebFetch against public REST (`/search`, `/pages`) and fetched page bodies.

## 1. Google Trends evidence (read by the orchestrator in Chrome, US, 12 months, 2026-11-05)

- "woocommerce wholesale": top related = "woocommerce wholesale prices" (index 100).
- "woocommerce subscription": top related = "woocommerce subscription plugin" (index 100).
- "woocommerce b2b", "woocommerce checkout/slow": too little data to display.
- Rising lists: unrelated noise, ignored.

**Honest strength rating: weak to moderate.** Index 100 on a related-query list is relative to the other related queries, not an absolute volume. Both seed terms are low volume. This tells us the two phrasings people use (wholesale prices, subscription plugin), not how many people search. It does not measure B2B standing orders at all. The chosen angle is therefore an inference from the Trends demand for "subscription plugin", paired with a corpus gap. Do not describe it to the user as "Trends-proven".

## 2. Uniqueness verdict

### Candidate (a) WooCommerce wholesale pricing approaches: REJECTED

- Post 42393 `woocommerce-b2b-pricing-and-access-setup` (live REST search hit; body fetched 2026-11-05, ~2,700 words) already owns it. Its H2/H3: "How do you set up customer groups and role-based pricing in WooCommerce?" with H3 "Which plugin should you pick for customer groups" and "Setting the actual role-based price"; "How do tiered and quantity-based pricing rules work in WooCommerce?"; "Which B2B pricing plugin should you choose: B2BKing, Wholesale Suite, or native B2B Pricing?".
- Only gap: custom code is not covered. That is a thin gap and a "custom pricing code" post would still sit on 42393's keyword. Fails CHECK 4 (angle overlap) and CHECK 5 (cluster: 42393, 42202, 42297, 42074, 42491, 43753, 43845 all touch B2B Woo pricing/ordering).
- Also related: 42108 (ERP as pricing engine), 43753 (quick order form), 42491 (gated pricing and AI).
- Page sweep: no page has a wholesale-pricing slug. `/search?search=wholesale` returned only posts above plus service pages (certified-b2b..., b2b-ecommerce-development).

### Candidate (b) WooCommerce subscriptions, plugin vs custom build, generic: PARTIAL CONFLICT, so reframed

- Post 31274 `woocommerce-subscription-plugins` ("20 Best WooCommerce Subscription Plugins (Updated 2024)", ~3,500 words, page header says updated Sept 28, 2026, title says 2024, intro says 2023). It owns the head query "woocommerce subscription plugin(s)". Its H2s: "What is WooCommerce Subscription?", "Why Subscription Plugin?", "Types of WooCommerce Subscription Plugins for WooCommerce Website", "How Do You Install A Woocommerce Subscription Plugin?", "20 Best WooCommerce Subscription Plugins", "Tips to Choose a WooCommerce Subscription Plugin for Your Website". Custom build appears only as a Virtina CTA. It does NOT cover gateway-token/automatic-renewal limits, HPOS, dunning by name, or B2B.
- Post 17289 `migrating-woocommerce-subscriptions` (migration only). Post 37714 `what-is-subscription-business-model-ecommerce` (generic model, no WooCommerce H2s). Post 43254 has a "recurring billing" column in a high-risk gateway table only. Post 43361 (HPOS plugin compatibility) mentions Subscriptions renewal testing in a checklist and FAQ.
- Cluster count for "subscription": 3 posts (31274, 17289, 37714). Below the 5-post saturation line, but a plain "plugin vs custom" post would collide with 31274 on the head term (CHECK 3) and arguably CHECK 4.

### Chosen angle (proposed): B2B standing orders on WooCommerce, subscription plugin or custom build. PASS (pending the analyzer's formal 5-check audit file)

- Thesis: for a distributor or manufacturer, a "standing order" (same SKUs, fixed interval, account-specific price, net terms, ERP sync) is not a consumer subscription. Woo's official Subscriptions extension handles the billing engine well, but the B2B parts (per-account pricing at renewal, invoice/net-terms payment, approval, ERP) decide whether you use the plugin, extend it, or build custom. Decision-tree answer by store profile.
- No Virtina post or page mentions standing orders. Searches `recurring` and `replenishment reorder` on `/wp-json/wp/v2/search` returned no standing-order/recurring-order post. `42297` (net terms) fetched: zero mention of recurring, standing, or subscription. 43753 (quick order form) covers one-off reorder entry, not scheduled orders. 43845 (backorders) is stock mechanics.
- Checks (preliminary, analyzer to formalize):
  - CHECK 1 title: proposed title below shares no 3 consecutive content words with any title seen.
  - CHECK 2 slug `standing-orders-plugin-or-custom-build`: not a substring of any slug; word overlap with `woocommerce-subscription-plugins` is "plugin" vs "plugins" (different token). Deliberately avoids `woocommerce` and `b2b` (those collide with many slugs, same workaround as 42491). Analyzer should confirm with token-level comparison.
  - CHECK 3 keyword "WooCommerce standing orders B2B": not claimed. Do NOT target "woocommerce subscription plugin" as the primary keyword.
  - CHECK 4 angle: distinct from 31274 (roundup), 17289 (migration), 37714 (model), 42393 (pricing config), 42297 (net terms), 43753 (single reorder form).
  - CHECK 5 cluster: 3 subscription posts, fewer than 5. B2B Woo cluster is large (6+): saturation flag per section 4c; the sub-niche (scheduled repeat orders) is the justification.
- Pages sweep (`/pages?per_page=100`, first page, ~95 slugs; matched on slug): no page owns subscriptions, standing orders, or recurring orders. Service page 10745 `woocommerce-plugin-development` lists a "WooCommerce Subscription Plugin" service (billing intervals, trials, cancellations tracking). That is a commercial page, so it is the natural CTA target, not a conflict. Page 36749 and 42417 (payments) are not relevant to this topic. Only the first `/pages` page was inspected (100 per page; slug list was cut at 100), so a second page request was not made: [unverified] that no later page owns the keyword. The search endpoint for "woocommerce subscription" returned no page about subscriptions beyond 10745's absence from results, so risk is low.
- Inventory staleness: `last_updated` 2026-09-09 (57 days). Live `/search` surfaced newer posts (43254, 43361, 43753, 43764, 43805, 43845, 43728, 43414, 43421, 43507). Inventory file not refreshed by this agent (no Bash/write to that file requested); the orchestrator or analyzer should append them.
- Known data bug: 38095 and 38078 share an identical H1 (already flagged in memory).

**Verdict: reject (a); reject generic (b); proceed with the standing-order reframe of (b).**

Proposed title (sentence case): "WooCommerce standing orders for B2B: subscription plugin or custom build?"
Proposed format: Format D (decision-tree/playbook), with a comparison table. Analyzer to confirm against the last-10-posts format rotation (43845, 43764, 43753 etc. were E/A style; D has not been checked by me).

## 3. Product fit and AI-visibility fit

- Owned theme served (brand.md): theme 1, "B2B eCommerce done right: complex pricing, quote workflows, multi-tier customer catalogs, ERP integration". Also services: custom plugin development, integrations.
- Virtina capability that answers the reader's problem: custom WooCommerce plugin development (page 10745 explicitly lists a subscription plugin service) and ERP integration (42108, `woocommerce-integration-service`).
- Audience fit: VP eCommerce/Director of Digital at distributors ("scaling B2B workflows", "fix vs build" decisions).
- AI-visibility fit: it is a decision/comparison post (plugin vs extend vs custom), with named options compared on dated, official criteria. Note the user's own correction (memory) that "comparison" for ChatSKU means brand-vs-brand; for Virtina the brief here says comparison or decision style is preferred, which this meets. Virtina's brand.md forbids naming/linking agency competitors; naming plugin vendors is fine ("Tools" and platform vendors OK to mention factually).

## 4. Sourced facts (all fetched 2026-11-05; paraphrased)

Primary sources: woocommerce.com docs and product page. Note: WebFetch was served from a non-US locale so the product page showed INR prices; **do not publish any price**. Third-party blogs quote $249 to $279 per year for the official plugin; these are vendor/affiliate sources and [unverified].

1. **Official gateway list** (https://woocommerce.com/document/subscriptions/payment-gateways/): the doc sorts Marketplace gateway extensions into tables of supported subscription features. Basic features: suspend, cancel, reactivate. Advanced: multiple subscriptions, changing recurring totals, changing payment dates, payment method changes. Gateways outside the Marketplace are not covered but may work. Named automatic-payment gateways include WooPayments, Stripe, Square, Authorize.net, PayPal Braintree, PayPal Payments, Chase Paymentech, CyberSource, Elavon Converge, Moneris, Worldpay and others. No last-updated date on the page.
2. **Automatic vs manual renewals** (same doc and https://woocommerce.com/document/subscriptions/renewal-process/): automatic renewals charge the saved method with no customer action. Manual renewals create a pending renewal order that the customer pays by logging in; any gateway can process them and all subscription features work. Manual renewals are off by default and the doc advises against them for subscriptions renewing more than once a year. Coupons and taxes are generally locked at signup. This is the key B2B fact: a distributor paying by PO or invoice fits the manual-renewal path, but needs a human to pay each interval.
3. **Failed payments**: a failed automatic payment leaves the subscription on hold by default; the customer is told to pay the failed order from My Account. An optional payment recovery feature retries and emails the customer. A renewal due runs through Action Scheduler (`woocommerce_scheduled_subscription_payment`). If the gateway is deactivated, the renewal order is created as pending with a manual-payment note.
4. **Gateway not on list**: the FAQ (https://woocommerce.com/document/subscriptions/faq/) says a gateway not on the hand-picked list may still support automatic renewals and can be tested; manual renewals work regardless.
5. **Custom intervals/lengths**: FAQ says custom billing intervals (example given: every 10 weeks) and custom lengths (example 36 months) are possible via a small plugin using a filter (needs Subscriptions 1.4.4+, some gateways limit lengths). The FAQ states these are developer-level and outside Woo's support policy. Directly relevant to "custom code": the official route to non-standard intervals IS custom code on top of the plugin, which weakens a pure "plugin vs custom" binary and supports a three-way decision (use as is, extend, build).
6. **Scale**: FAQ says no fixed subscription cap; problems can appear from a few thousand to over 80,000 subscriptions depending on hosting, data and other plugins; Woo reports 100,000+ subscriptions renewing on one day on some sites. Paraphrase only.
7. **Staging double-billing risk**: FAQ warns a staging site in live mode can cause customers to be charged twice on renewal. Useful custom-build/test checklist item.
8. **Product page** (https://woocommerce.com/products/woocommerce-subscriptions/): trials, sign-up fees, billing synchronization, upgrades/downgrades with proration, failed-payment retries, gifting, combined multi-subscription orders, Subscriptions Health Check. Says 25+ gateways for automatic renewals. Version 9.3.0, 100K+ active installs, rating 3.9 of 5 (144 reviews), requires WooCommerce 11.0+, tested with WooCommerce 11.1 (as shown on the fetch date). HPOS and block checkout are NOT stated on this page. The page shows no price in USD. Does not mention per-account/customer-specific pricing or net terms.
9. **HPOS**: Woo developer blog "WooCommerce Subscriptions + HPOS: Understanding Next Steps" (https://developer.woocommerce.com/2023/03/07/woocommerce-subscriptions-hpos-understanding-next-steps/) says Subscriptions 4.9.0 added HPOS compatibility, subscriptions are stored as a `shop_subscription` type in `wc_orders`, and custom integrations must swap direct database queries for WooCommerce CRUD methods. Relevant to any custom build and to extensions. Link-checked via search result only, not fetched in full; the fetched 1-line summary came from the search tool. Treat as [verified via search snippet, fetch full page before quoting].
10. **Third-party plugin facts**: roundups list YITH, SUMO, Subscriptions for WooCommerce (WebToffee/WP Swings), Sublium and others. All claims come from vendor or affiliate blogs and are [unverified] until checked on each plugin's own page. The brief should either verify 2 or 3 named alternatives on their own pages or restrict the plugin side to the official extension plus "other plugins" generically.
11. **B2B-specific gap**: a search for WooCommerce B2B standing orders returned Shopify B2B apps (Orumio), other platforms, and one WooCommerce.com feature-request page for "Order Subscriptions" (not a documented product). No WooCommerce source documents per-account catalogs, net terms, or approval for recurring distributor orders. The gap is real, but it also means the post must not claim a plugin does or does not do these things without testing. State "check on a staging site" items as test steps, not as facts.

**Do not assert** (cannot be verified from primary sources): whether role-based pricing plugins (B2BKing, Wholesale Suite) apply the customer's tier price on subscription renewals; whether the official plugin supports net terms or PO payment natively. Frame these as "questions to test before you buy".

## 5. What the top results and AI answers currently say (head query "woocommerce subscription plugin")

I cannot query ChatGPT/Perplexity/Google AI Overviews from this toolset. The WebSearch tool's own synthesis of 2026 results is the only AI-style answer I could read: it says the official WooCommerce Subscriptions is the default for gateway coverage, YITH the budget alternative, and the sources are mostly vendor/affiliate. That mirrors the SERP.

SERP gap analysis (fetched 2026-11-05):

| Pos (approx, from result order, not rank-verified) | URL | Domain type | Words | Weaknesses |
|---|---|---|---|---|
| 1 | https://www.bluehost.com/blog/woocommerce-subscription-plugins/ | hosting vendor | ~4,270 | Published Feb 20, 2026; 15-plugin list; zero B2B; no custom-build discussion; mixed-period prices with "indicative" disclaimer; hosting CTAs |
| 2 | https://www.flycart.org/blog/woocommerce-subscription-plugin | plugin vendor | ~2,200 | July 2, 2026; 6 plugins; zero B2B; recommends a plugin it did not review (internal inconsistency); price conflicts between table and body; no test data |
| 3 | https://virtina.com/woocommerce-subscription-plugins/ | Virtina | ~3,500 | Our own roundup; dates inconsistent (2024/2023/Sept 2026 header); no gateway limits, HPOS, or B2B |
| 4 | swarmify, funnelkit, omnisend, wbcomdesigns, instawp (result titles only) | vendors/affiliates | not fetched | Not assessed |

Position numbers are search-result order, not verified rankings. Only the first two rows were fetched in full beyond Virtina's own page; the requirement of 3 to 5 fetched competitors for the section 4c competitor-analysis file is NOT yet met (2 external fetched). The analyzer or orchestrator should fetch at least one more (for example funnelkit or omnisend) and save `competitor-analysis-2026-11-05.md`. I did not create that file.

Common gap across all fetched results: none treat subscriptions as B2B standing orders, none explain the automatic-vs-manual renewal choice in terms of invoice/PO buyers, none give a build-vs-extend-vs-buy decision with test steps.

Wholesale pricing SERP (for reference; candidate (a), rejected): Barn2 (Wholesale Pro, Discount Manager), iconicwp, ELEX, wordpress.org free plugins, woocommerce.com User Roles Based Price. Consensus: core WooCommerce has no role-based pricing, a plugin is required.

## 6. Sub-questions the post should answer (H2 candidates, question style, direct answer first)

1. What is a B2B standing order, and how does it differ from a consumer subscription?
2. Can the official WooCommerce Subscriptions plugin run B2B standing orders as is? (answer from facts 1, 2, 3, 8)
3. When do manual renewals fit a distributor better than automatic ones? (fact 2)
4. What breaks first: pricing at renewal, payment method, stock, or ERP sync? (test list, not claims)
5. When should you extend the plugin instead of building custom? (fact 5)
6. When is a fully custom build justified, and what does it cost you in maintenance (HPOS, gateways, Action Scheduler, retries)? (facts 3, 9)
7. Decision table: store profile vs recommended route. Plus a pre-launch test checklist (including staging double-billing, fact 7).
Plus mandatory Summary, Introduction, TOC, PAA, Conclusion, FAQ (6 to 8 Q&As). Minimum 6 H3s. No bulleted padding (bullets only for genuinely list-shaped content).

## 7. Semantic term list (10 to 15)

standing order, recurring order, replenishment, repeat order, automatic renewal, manual renewal, renewal order, payment token, on hold, payment retry, dunning, purchase order, net 30, accounts receivable, customer-specific price, ERP sync, Action Scheduler, HPOS, billing synchronization, proration.

## 8. Verified live Virtina URLs for interlinking

WebFetch returned page content for each (so they exist), but WebFetch does NOT expose HTTP status or the redirect chain, and MUST-FOLLOW-RULES section 6 requires a 200 check with redirects not followed. **The orchestrator must run a curl-style check (or equivalent) before the push.** Treat the list below as "content-loaded 2026-11-05", not "200 confirmed with redirects off".

| Use | URL | H1 as fetched |
|---|---|---|
| Money/service page (custom build CTA) | https://virtina.com/woocommerce-plugin-development/ | WooCommerce Plugin Development |
| Matching service page (platform) | https://virtina.com/platforms/woocommerce-development-services/ | The Leading WooCommerce Website Development Company in the U.S. (search showed a slightly different title; page content loaded) |
| Integration service | https://virtina.com/woocommerce-integration-service/ | WooCommerce Integration |
| B2B service | https://virtina.com/b2b-ecommerce-development/ | B2B eCommerce Development |
| Payments service | https://virtina.com/woocommerce-payment-gateway-integration/ | Your gateway is approved. Now make the checkout actually take money. |
| Existing roundup (link once, do not cannibalize) | https://virtina.com/woocommerce-subscription-plugins/ | 20 Best WooCommerce Subscription Plugins (Updated 2024) |
| Net terms | https://virtina.com/woocommerce-b2b-net-payment-terms/ | Why your WooCommerce B2B buyers leave without buying (and how net payment terms fix it) |
| Pricing config | https://virtina.com/woocommerce-b2b-pricing-and-access-setup/ | WooCommerce B2B Configuration: ... |
| ERP | https://virtina.com/woocommerce-erp-integration/ | How to connect WooCommerce to your ERP... |
| Portal | https://virtina.com/woocommerce-b2b-customer-portal/ | Does your WooCommerce store have a B2B customer portal, or just an account page? |
| HPOS plugin check | https://virtina.com/woocommerce-hpos-plugin-compatibility/ | WooCommerce HPOS Plugin Compatibility... |
| High-risk gateway recurring column | https://virtina.com/best-high-risk-payment-gateways-woocommerce/ | Best High Risk Payment Gateways for WooCommerce... |
| Backorders | https://virtina.com/woocommerce-backorders-lead-times/ | WooCommerce backorders for B2B... |
| Quick order form | https://virtina.com/quick-order-form-line-checks/ | B2B quick order form... (appeared in live search) |
| Contact | https://virtina.com/get-in-touch/ | "Just ask. Get answers." |
| Migrating subs (optional) | https://virtina.com/migrating-woocommerce-subscriptions/ | How to Migrate Your Subscriptions to WooCommerce? |

Do not link: `/ecommerce-development-services/`, `/contact/`, `/ecommerce-seo-services/` (dead or redirecting per rules). Anchors must be 2 to 5 word clean noun phrases, no "our". Interlink at least one previous blog post (several above are posts). External: max 2, suggest woocommerce.com subscriptions payment-gateways doc and the Woo FAQ (not competitor domains; woocommerce.com is the platform vendor and is allowed, and 43753 already links it).

## 9. Image direction (user preference override of generic person-at-desk)

Per memory (images show the pain, split-panel; ChatGPT scenes; no duplicate featured in body; featured carries the logo pill; 2x export, q90+): do not use person-at-desk. Ideas:
- Featured (2.6:1): split panel, "Automatic renewal: card on file" vs "Manual renewal: PO and invoice", same account, same order lines.
- Body 1: renewal order on hold next to a paid card order (the failed-payment mechanic).
- Body 2: renewal price row showing "Contract price" vs "List price" mismatch (the pricing-at-renewal test).
- Body 3: plugin / extended / custom three-column decision panel with identical neutral icons (no per-vendor check marks that read as capability claims).

## 10. Risks

1. **Trends signal is weak** and does not measure the chosen angle. Honest framing: demand for "woocommerce subscription plugin" exists but is low; the post is chosen on corpus gap plus product fit.
2. **Cannibalization of 31274** on "woocommerce subscription plugin". Mitigation: different primary keyword, link to 31274 once, do not title it as a plugin list.
3. **Unverifiable B2B behavior claims**: pricing at renewal, net terms, PO payment. Written as test steps only. No stats, no prices.
4. **Plugin alternatives** only vendor-sourced; verify on each plugin's own page or omit.
5. **Link status**: WebFetch cannot confirm 200 with redirects off; re-check with curl before push (virtina.com 429s curl per memory, so use WebFetch or REST for the 200/redirect proof, noting this limitation).
6. **Inventory stale** (2026-09-09); inventory needs the newer posts appended.
7. **Competitor-analysis file is incomplete** (2 external fetched, needs 3 to 5).
8. **Winter cadence**: subscriptions topic is evergreen, so no seasonal risk. No hype claims, no em dashes, no banned words in later stages.
9. Brand tone: this is a decision guide ending in "extend or build custom" which serves Virtina's plugin-development service. Keep it neutral and honest that "use the official plugin as is" is the right answer for some stores (anti-pitch credibility).
