---
title: Research notes — WooCommerce dropship plugin refresh (post 38972)
client: virtina
date: 2026-09-08
topic: WooCommerce dropshipping plugins — status verification and refresh of live post 38972
audience: B2B/B2C ecommerce operators evaluating WooCommerce dropshipping tooling
stage: research
slug: woocommerce-dropshipping-plugins
---

# Research: refresh of https://virtina.com/woocommerce-dropshipping-plugins/ (post 38972)

**Type:** optimisation of an existing live, ranking page. Not a new post.
**Target keyword:** `woocommerce dropship plugin` (currently position 7).
**All plugin/pricing/link checks below were performed 2026-09-08.**

---

## 0. Uniqueness check (MUST-FOLLOW-RULES section 1)

This is an in-place refresh of an existing post, so the 5 uniqueness checks apply differently: the
job is to keep 38972 distinct from its two neighbours, not to clear a new slug.

Related posts found in `published-posts-inventory.md`:

| ID | Slug | Date | Overlap risk |
|---|---|---|---|
| 38972 | `woocommerce-dropshipping-plugins` | 2025-07-02 | **this post** |
| 31786 | `woocommerce-dropshipping-guide` | 2023-05-15 | Guide + setup + "top plugins" + suppliers. Names AliDropship, DropshipMe, Dropified, WooDropship, Spocket (verified live 2026-09-08) |
| 31534 | `how-to-set-up-woocommerce-for-dropshipping` | 2023-05-03 | Six-step setup how-to |

No other Virtina post claims the dropshipping cluster. Cluster size = 3, under the 5-post
saturation limit. **Uniqueness posture for the refresh:** 38972 must stay the *plugin selection and
status* page. It must not absorb setup steps (31534's territory) or supplier directories (31786's
territory). Both are usable as internal links, and both are verified 200 below.

**Warning for the analyzer:** post 31786 already recommends WooDropship and DropshipMe. If the
refresh cuts or flags WooDropship, 31786 becomes internally contradictory with 38972. Flag it for a
follow-up pass; do not silently create a conflict between two live Virtina pages.

---

## 1. Testing the diagnosis

All four of the orchestrator's hypotheses were tested against the live backup
(`clients/virtina/output/backups/post-38972-tve_updated_post-2026-09-08.html`) and the live URL.

| Claim | Verdict | Evidence |
|---|---|---|
| Exact phrase "dropship plugin" = 0 occurrences | **CONFIRMED** | Grep of the live backup returns zero. The page ranks on topical strength with no exact-match anchor for its own target keyword |
| Title says 20, page lists 25 | **CONFIRMED** | H1 "Top 20 WooCommerce Dropshipping Plugins (Updated 2026)"; H3s numbered 1–25; the comparison-table H2 reads "The Comparison Table For The 25 Popular Woocommerce Dropshipping Plugins". Live page still shows H1 "Top 20", last modified 10 Aug 2026 |
| Several listed plugins are defunct | **CONFIRMED, but the specific guesses were partly wrong** | See section 2. Beeketing and Ezusy are dead. **ChinaDS, AutoDS and AliNext are alive and actively maintained** — those three guesses were wrong. The real problems are different and worse: two entries are the same plugin, one is not a dropshipping plugin at all, and two vendors have quietly dropped WooCommerce |
| No Introduction H2, no PAA, market block above the list | **CONFIRMED** | Heading order: Summary → TOC → Global Dropshipping Market Trends → Role of Dropshipping Plugins → Best WooCommerce Dropshipping Plugins. No Introduction H2, no People Also Ask H2 |

### Four further defects found that were not in the brief

1. **Zero prices on the page.** The only dollar figures anywhere in 7,679 words are the five
   market-trends statistics. The comparison table columns are: Plugin | AliExpress Support |
   Multi-Supplier Support | Print-on-Demand | Automation Level | Unique Feature. **No price column,
   no status column, no last-updated column.** All five ranking competitors price every plugin.
2. **A broken TOC link.** The third TOC item points at `href="http://best-woocommerce-dropshipping-plugins"`
   — the `#` is missing, so it resolves to an external hostname, not an on-page anchor.
3. **The TOC uses the banned Thrive markup.** `<ul class="tcb-styled-list">` /
   `<li class="thrv-styled-list-item">` / `<div class="tcb-styled-list-icon">` throughout. Section 4
   of MUST-FOLLOW-RULES prohibits exactly this pattern (it is what broke post 42202). The 25 plugin
   TOC entries are also plain text, not anchor links.
4. **A name inconsistency inside the page.** The TOC says "20. AutoDS"; the body H3 says "20. AutoD";
   the H4 beneath it says "AutoDS". The correct product name is AutoDS.

---

## 2. Plugin status verification (task 1) — all 25, checked 2026-09-08

Method: WordPress.org plugin API (`api.wordpress.org/plugins/info/`) for anything in the repository,
plus the vendor's own live site for SaaS products. A vendor's integrations page is treated as
authoritative for "does this still support WooCommerce".

### Verdict summary

- **Cut outright: 6** — Beeketing, Ezusy, Modalyst, Zendrop, CartFlows, AliNext Lite (duplicate)
- **Cut or heavily caveat: 2** — WooDropship, NextsChain
- **Rename required: 3** — WooShark, Ali2Woo, AutoD
- **Correct a false claim: 1** — DSers
- **Keep with a staleness flag: 3** — AppScenic, Spreadr, Wholesale2b
- **Keep as-is: 10**

### Full table

| # | Plugin as listed | 2026 verdict | Evidence (checked 2026-09-08) |
|---|---|---|---|
| 1 | AliDropship | **Active. Keep.** | `alidropship.com/woocommerce-dropshipping-plugin/` live and selling. **$89 one-time**, lifetime updates, 30-day money-back |
| 2 | Dropified | **Active, narrowed. Keep with a note.** | `dropified.com/pricing/`: $50/mo, or $500/yr ($41.66/mo). `dropified.com/manage-stores-2/` states supported platforms are **Shopify and WooCommerce only** — down from the Shopify/CommerceHQ/WooCommerce/GrooveKart/BigCommerce set it advertised in 2024. The pricing page copy is now entirely Shopify-framed ("AI builds your Shopify store") |
| 3 | WooDropship | **Probable zombie. Cut, or flag hard.** | Site loads, but its newest blog post is from **July 2023**, its "done-for-you store" offer refunds "any Shopify fees", and `/pricing/` shows no price. No plugin on wordpress.org. Cannot verify the plugin is still maintained — **[unverified]** |
| 4 | Spocket | **Active. Keep.** | `spocket.co/pricing`: Starter $39.99, Professional $59.99, Empire $99.99, Unicorn $299.99 per month. Annual: Professional $24/mo, Empire $57/mo, Unicorn $79/mo. WooCommerce named in integrations |
| 5 | Spreadr | **Active but flagged by WP.org. Keep with a caveat.** | WP.org `spreadr-for-woocomerce` v1.1.0, **updated 2026-07-29**, 500+ installs, but tested only to WP 6.8.8, so the page carries the "hasn't been tested with the latest 3 major releases" warning. `spreadr.co` fails DNS resolution |
| 6 | Printful | **Active. Keep, but reframe as print-on-demand.** | WP.org `printful-shipping-for-woocommerce` v2.2.12, updated **2026-01-14**, **50,000+ installs**, tested 6.9.7. `printful.com/pricing`: Free $0, Growth $24.99/mo (free above $12K/yr sales), Enterprise custom |
| 7 | Modalyst | **CUT. No longer a WooCommerce tool.** | `modalyst.co` lists Shopify, Wix, BigCommerce, Alibaba. **WooCommerce is absent.** `modalyst.co/woocommerce/` returns **404**. Site banner: "Modalyst has joined Wix.com" |
| 8 | WooShark | **RENAMED to SharkDropship.** | WP.org slug `wooshark-aliexpress-importer` now displays as "Sharkdropship & affiliate for AliExpress", v3.0.1, updated 2026-01-28, 300+ installs, tested 6.9.7, author Marc dooder. A sibling listing `woo-aliexpress-dropshipping` v3.2.0 (400+ installs) covers eBay/Amazon/Etsy/Temu. Note the pivot toward *affiliate*, not pure dropshipping |
| 9 | CartFlows | **CUT. Not a dropshipping plugin.** | WP.org name is literally "CartFlows – **Funnel Builder & Checkout Plugin** for WooCommerce", v3.2.0, updated 2026-08-24, tested WP 7.1, by Brainstorm Force. Extremely healthy product, but it has no supplier network, no product import and no fulfilment. Its presence is a category error that damages the page's credibility |
| 10 | Wholesale2b | **Alive; WooCommerce support unconfirmed.** | `wholesale2b.com/pricing`: Basic $20, Professional $59, Premium $99 per user/month, 10% yearly discount. **WooCommerce is not named on the pricing page**, and `/dropship-woocommerce.html` returned an empty body. Current Woo integration **[unverified]** |
| 11 | Doba | **Active. Keep.** | `doba.com/pricing`: Limited $28.66/mo, Basic $56.99/mo, Standard $142.66/mo, Enterprise custom (quarterly billing). WooCommerce listed among integrations |
| 12 | Syncee | **Active. Keep — strongest in the set.** | WP.org `syncee-global-dropshipping` v1.0.31, **updated 2026-09-02**, tested WP 7.1, 1,000+ installs. `syncee.com/pricing`: Free $0, Basic $39.99, Pro $59.99, Business $99.99 per month. WooCommerce named explicitly in the supported-platform sentence |
| 13 | CJdropshipping | **Active. Keep.** | `cjdropshipping.com` lists WooCommerce in integrations; `/integrations/woocommerce` is live and directs users to install from the WooCommerce marketplace. **No published price** — CJ does not disclose fees publicly **[unverified]** |
| 14 | Ali2Woo | **RENAMED to AliNext. Also a DUPLICATE of entry 23.** | WP.org `ali2woo-lite` now displays as "AliNext – WooCommerce Dropshipping Plugin for AliExpress", v3.7.3, **updated 2026-09-07** (the day before this check), tested WP 7.1, 4,000+ installs. The plugin page states AliNext is the evolved version of Ali2Woo |
| 15 | Ezusy | **DEAD. Cut.** | `ezusy.com` does not resolve. DNS lookup fails (ENOTFOUND). No product, no site |
| 16 | Importify | **Active. Keep — but fix the domain.** | WP.org `importify` v1.0.19, updated **2026-08-30**, 2,000+ installs. Pricing at `importify.com/pricing/`: Basic $14.95, Premium $27.95, Gold $37.95 per month, 20% off annual. WooCommerce is 1 of 5 supported platforms. **`importify.net` 404s** — the `.net` domain is not the live product |
| 17 | Zendrop | **CUT. Dropped WooCommerce.** | Both `zendrop.com/pricing/` and `zendrop.com/integrations/` list **Shopify, Wix, TikTok Shop, ClickFunnels only**. Pricing page states users connect "through our available integrations for Shopify, Wix, TikTok Shop, and ClickFunnels". Plans: Free $0, Pro $49/mo, Plus $79/mo. Verified on two separate pages |
| 18 | Printify | **Active. Keep, reframe as print-on-demand.** | WP.org `printify-for-woocommerce` v3.2, updated 2026-05-27, 10,000+ installs, tested 7.0.4. `printify.com/pricing/`: Free $0, Premium from $39/mo ($24.99/mo annual), Enterprise custom |
| 19 | Beeketing | **DEAD. Cut immediately.** | WP.org plugin last updated **2019-12-19**, tested WP 5.3.23, flagged untested, and the API returns no `active_installs` field. **`beeketing.com` returns a 301 to `shopbase.com`** — the company pivoted away. This is a six-and-a-half-year-dead product on a page badged "Updated 2026" |
| 20 | AutoD | **Active. Keep, but the name is wrong.** | Correct name is **AutoDS**. `autods.com` lists WooCommerce among its selling channels. Plan prices are JavaScript-rendered and **could not be read — [unverified]**. Visible add-on prices: auto-ordering $9.90/mo, VA access $14.97/mo, product finding hub $14.97/mo, mentor $39.97/mo. Trial advertised at $1 |
| 21 | DSers | **Alive as a SaaS, but the page's implicit claim is wrong.** | `dsers.com/integration` does list WooCommerce (alongside 17 other channels). **However the WordPress.org plugin, slug `dsers`, was permanently closed on 2021-04-28 for "Guideline Violation"**, last version 1.4.6, tested WP 5.6.19. There is no repository-hosted DSers plugin; it is distributed off-repo only. Every competitor listing DSers misses this |
| 22 | AppScenic | **SaaS alive, plugin stale. Keep with a caveat.** | `appscenic.com/pricing`: Free $0, Standard $39, Pro $79, Elite $99 per month; WooCommerce explicitly supported. But WP.org `appscenic` v1.2.2 was **last updated 2025-01-13**, tested only to WP 6.7.7, 3,000+ installs, and carries the "hasn't been tested with the latest 3 major releases" warning |
| 23 | AliNext Lite | **DUPLICATE of entry 14.** | Same WP.org slug (`ali2woo-lite`). The page lists one plugin twice, once under its dead name and once under its live name, five entries apart, without noticing |
| 24 | ChinaDS | **ALIVE and current. The brief's guess was wrong.** | WP.org `chinads-dropshipping-taobao-woocommerce` v2.2.2 by **VillaTheme**, updated **2026-08-20**, tested WP 7.1, 100+ installs. Tmall/Taobao sourcing. Small install base, but actively maintained by a serious vendor |
| 25 | NextsChain (ScaleOrder) | **Ambiguous. Cut or flag.** | `nextschain.com` resolves and serves **ScaleOrder-branded** content — active site, claims 1,000,000+ orders since 2020. But the integration logos are images with no readable platform names, **no pricing is published**, and there is **no wordpress.org plugin**. WooCommerce support and the NextsChain/ScaleOrder naming relationship are both **[unverified]** |

### Plugins to cut (8)

Beeketing, Ezusy, Modalyst, Zendrop, CartFlows, AliNext Lite (merge into Ali2Woo/AliNext),
WooDropship, NextsChain.

That takes 25 down to 17 real, distinct, verified WooCommerce dropshipping plugins.

---

## 3. Missing plugins (task 2) — all verified maintained on 2026-09-08

Ranked by how badly the omission hurts.

| Plugin | Why it belongs | Verified status |
|---|---|---|
| **Dropshipping for WooCommerce (OPMC)** | The **official WooCommerce.com marketplace extension**. Appears on 3 of the 5 ranking competitor pages. Virtina omits it entirely — the single most damaging gap on the page | Live on `woocommerce.com/products/woocommerce-dropshipping/`. v5.2.7, 3K+ active installs, rated **2.7/5 from 38 reviews**. Requires WP 6.5+, WooCommerce 5.0+, PHP 7.4+. Price shown in INR (₹7,575/yr; ₹12,120 for 2 years); WPBeginner quotes $79/yr. **The low rating is itself the story** — the official extension is the weakest-reviewed option |
| **ALD – Dropshipping and Fulfillment for AliExpress and WooCommerce** (VillaTheme) | **9,000+ active installs — the largest install base of any pure AliExpress dropshipping plugin on wordpress.org.** Omitting it while listing three dead products is indefensible | WP.org `woo-alidropship` v2.2.4, updated 2026-08-20, tested WP 7.1. Note the confusing name collision with AliDropship.com — worth calling out explicitly for readers |
| **DropshipMe** | On 4 of the 5 competitor lists (WPBeginner, Omnisend, LiquidWeb, WPFactory). Virtina's own post 31786 already recommends it | `dropship.me` live, copyright 2026, 14-day free trial. Curated AliExpress catalogue (50,000+ pre-edited listings). **Not on wordpress.org**; price is not published on the site — **[unverified]** |
| **TMDS – Dropshipping for TEMU and Woo** (VillaTheme) | Temu sourcing did not meaningfully exist when this article was written. This is the genuinely new category since 2025 | WP.org `tmds-dropshipping-for-temu-and-woo` v1.0.15, updated 2026-08-20, tested WP 7.1, 400+ installs |
| **EPROLO-Dropshipping** | Free supplier network with branding/POD | WP.org `eprolo-dropshipping` v2.4.2, updated 2025-12-11, 1,000+ installs, tested 6.9.7. Ageing but current enough |
| **BigBuy Dropshipping Connector** | The main EU-supplier answer, and the article has no EU option | WP.org `bigbuy-wc-dropshipping-connector` v2.1.0, updated 2025-11-24, 200+ installs, tested 6.8.8. Vendor-published |
| **TopDawg Wholesale Dropshipping** | US-based suppliers, 500,000+ products; ranks organically for the target phrase | WP.org `topdawg-wholesale-dropshipping` v1.1.8, updated 2026-08-20, tested WP 7.1, 40+ installs |
| **Hertwill – EU and US Dropshipping** | Second EU/US option | WP.org `hertwill` v1.2.0, updated 2026-08-03, 100+ installs |
| **BuckyDrop** | Branded China-sourcing alternative to CJ | WP.org `buckydrop-dropshipping-for-woocommerce` v1.0.6, updated 2026-03-12, 300+ installs |
| **Qikink Print On Demand and DropShipping** | India-based POD, no equivalent on the current list | WP.org `qikink-pod-and-drop-shipping` v1.1.2, updated 2026-01-03, 1,000+ installs, tested 6.7.7 |

**Recommendation:** add the first four without hesitation. The remaining six are legitimate but
niche — use them to fill regional gaps (EU, US, India) rather than to pad the count back to 25.

---

## 4. SERP analysis (task 3)

Searches run 2026-09-08: `woocommerce dropship plugin`, `best woocommerce dropshipping plugins 2026`.
Five ranking pages fetched in full.

| Page | Plugins | Words | Exact singular phrase? | Table | Prices | Date shown | Verifies plugin status? |
|---|---|---|---|---|---|---|---|
| **WPBeginner** — "I tested the 5 best WooCommerce dropshipping plugins" | 5 (+2 bonus) | ~4,200 | **No** | **Yes, above the fold** | **Yes, all 7** | 2026-03-20 | **No** |
| **Omnisend** — "WooCommerce Dropshipping: Complete Guide + 11 Best Plugins" | 11 | ~10,000–12,000 | **No** | Yes, comprehensive | Yes | 2025-11-11 | **No** |
| **LiquidWeb** — "The 10 Top WordPress Dropshipping Plugins [2026]" | 10 (title says 11) | ~2,300 | **No** | Yes, pricing table | Yes | **None shown** | **No** |
| **WPFactory** — "6 Best WooCommerce Dropshipping Plugins in 2026" | 6 | ~1,500 | **No** | Yes | Yes | **Published 2023-05-06** despite the 2026 title | **No** |
| **Wbcom Designs** — "10 Best WooCommerce Dropshipping Plugins 2026" | 10 | **798** (per its own schema `wordCount`) | **No** | No | Barely | Pub 2023-01-28, mod 2026-05-29 | **No** |
| **Virtina (position 7)** | 25 | 7,679 | **No** | Yes, 6 columns | **No, zero** | Modified 2026-08-10 | **No** |

Also ranking: `woocommerce.com/products/woocommerce-dropshipping/` (the official OPMC extension
product page) and `alidropship.com/woocommerce-dropshipping-plugin/` — both vendor pages, both
beating Virtina on commercial intent because they answer "what does it cost" immediately.

### What the pages above Virtina have that this page does not

1. **Price on every plugin.** All five competitors do it. Virtina has zero dollar figures for any
   plugin. This is the clearest single deficit and it maps directly onto searcher intent.
2. **A comparison table before the list, not after it.** WPBeginner's table is the first thing on
   the page. Virtina's arrives after 25 H3 sections and roughly 6,000 words.
3. **A stated methodology.** WPBeginner claims hands-on testing in the H1 itself ("I tested…").
   Virtina asserts nothing about how the 25 were chosen.
4. **Speed to the answer.** WPBeginner 4,200 words, LiquidWeb 2,300, WPFactory 1,500. Virtina 7,679
   with a generic market-trends block sitting between the reader and the list.
5. **Coverage of DropshipMe and the official Woo extension.** Between them these two appear on all
   five competitor pages. Virtina names neither.

### What Virtina has that they do not

Depth per plugin (two Q&A sub-headings each) and the only 25-item list. That is volume, not
authority, and Google is currently rewarding the shorter, priced, tested pages above it.

### People Also Ask

**I could not retrieve Google's live PAA box.** The search tool available here returns organic
results only, with no PAA payload, and I will not invent questions. What I can report factually:

- Not one of the five ranking pages carries an FAQ section. LiquidWeb, WPFactory and Wbcom have
  none at all; WPBeginner and Omnisend end in prose.
- The question-shaped headings that recur across the competitor set and Virtina's own FAQ are:
  what dropshipping is on WooCommerce, whether free dropshipping plugins exist, how to choose one,
  whether more than one can run at once, and which suppliers a plugin connects to.

**Recommendation for the analyzer:** treat the PAA section as a genuine content opportunity —
nobody in the top 10 has one — but have someone open an incognito Google search and paste in the
real PAA questions before drafting. Do not let the creator guess them.

---

## 5. Pricing (task 4) — verified 2026-09-08

Only these figures are safe to publish. Everything else must be omitted, not estimated.

| Plugin | Price (verified today) | Source |
|---|---|---|
| AliDropship Woo | **$89 one-time** | alidropship.com/woocommerce-dropshipping-plugin/ |
| Dropified | **$50/mo**, or $500/yr ($41.66/mo) | dropified.com/pricing/ |
| Spocket | Starter **$39.99**, Professional **$59.99**, Empire **$99.99**, Unicorn **$299.99**/mo. Annual: $24 / $57 / $79 per month | spocket.co/pricing |
| Syncee | Free, Basic **$39.99**, Pro **$59.99**, Business **$99.99**/mo | syncee.com/pricing/ |
| Importify | Basic **$14.95**, Premium **$27.95**, Gold **$37.95**/mo (20% off annual) | importify.com/pricing/ |
| Doba | Limited **$28.66**, Basic **$56.99**, Standard **$142.66**/mo (quarterly billing), Enterprise custom | doba.com/pricing |
| Wholesale2b | Basic **$20**, Professional **$59**, Premium **$99** per user/mo, 10% off yearly | wholesale2b.com/pricing |
| AppScenic | Free, Standard **$39**, Pro **$79**, Elite **$99**/mo | appscenic.com/pricing |
| Printful | Free $0, Growth **$24.99/mo** (waived above $12K/yr sales), Enterprise custom | printful.com/pricing |
| Printify | Free $0, Premium from **$39/mo** ($24.99/mo billed annually), Enterprise custom | printify.com/pricing/ |
| Zendrop | Free, Pro $49/mo, Plus $79/mo — **but no WooCommerce integration, so do not publish** | zendrop.com/pricing/ |
| Official Dropshipping for WooCommerce (OPMC) | ₹7,575/yr, ₹12,120/2yr as displayed. **USD price not confirmed** | woocommerce.com/products/woocommerce-dropshipping/ |

### Prices that could NOT be verified — do not publish

- **AutoDS** — pricing tiers are JavaScript-rendered; the served HTML contains `$__` placeholders.
- **CJdropshipping** — no published pricing anywhere on the site.
- **DropshipMe** — free trial advertised; paid package prices not shown.
- **WooDropship** — `/pricing/` shows no figure. The frequently repeated "$89 lifetime" comes from
  WPBeginner, not from WooDropship, and I could not corroborate it at source.
- **NextsChain / ScaleOrder** — registration required to see pricing.
- **Spreadr** — `spreadr.co` does not resolve; no pricing page reachable.
- **Printful / Printify / CJdropshipping per-item costs** — these are product-level, not plan-level,
  and vary by SKU. Do not summarise them.

**Rule for the creator:** state the check date beside the price table and say plainly that prices
were verified on 2026-09-08. A dated price ages honestly; an undated one rots silently.

---

## 6. Market statistics (task 5) — the hard audit

The page's opening "Global Dropshipping Market Trends" block contains five numeric claims. **None of
them survives.**

### Claim 1 — "valued at approximately $365.67 billion in 2024… projected to reach $470.92 billion by 2025"

**CUT.** Two separate problems.

- The $365.67bn figure is Grand View Research's, and Grand View attributes it to **2025, not 2024**.
  The page has shifted it back a year.
- $470.92bn with a 28.8% CAGR is **The Business Research Company's** number, from a different report
  with a different methodology. The sentence silently splices two firms' figures into one trend line.
- Grand View's own newer report gives **$464.4bn for 2025**, contradicting the $365.67bn it is
  credited with.

Neither primary report was reachable to confirm at source: `grandviewresearch.com` returned **HTTP
403** to this session. Publishing a figure I could not open is not acceptable under section 4c.

### Claim 2 — "the market will reach $1.2 trillion by 2030"

**CUT.** Directionally common but not traceable. Circulating 2030 forecasts include $1.25tn, $1.254tn
and $1.432tn from three different firms, off three different base years ($336.29bn/2024,
$248.18bn/2024, $464bn/2025). No named, dated primary source says "$1.2 trillion". **[unverified]**

### Claim 3 — fashion and apparel "CAGR of 7.56% from 2024 to 2028… roughly $802.33 billion by 2025"

**CUT. This is the worst one.** Two failures:

- **Wrong scope.** It sits inside a dropshipping section, implying a dropshipping figure. It is a
  *total global apparel market* figure. Dropshipping is a fraction of that.
- **Wrong number.** Statista's global apparel market forecast for 2025 is **US$662.70bn**, not
  $802.33bn. The $802.33bn figure could not be located in any Statista source.

### Claim 4 — beauty and personal care "projected to reach $672.20 billion by 2025"

**CUT.** Same scope error as claim 3 — a whole-category market figure presented inside a dropshipping
trends block. Not independently verifiable to a named, dated primary source today. **[unverified]**

### Claim 5 — "Asia-Pacific, particularly China, plays a crucial role as a primary source"

**Keep as qualitative context only.** It carries no number and is uncontroversial. But it does not
earn a section of its own.

### The spread, which is the actual story

Three research firms, all reporting the **same year (2025)**:

| Firm | 2025 global dropshipping market | Report date |
|---|---|---|
| Global Market Insights | **$290.7 billion** | December 2025 |
| IMARC Group | **$405.7 billion** | 2025 |
| Grand View Research | **$464.4 billion** | 2025 |

A 60% spread between the low and high estimate for a single year. **Recommendation: delete the
market-trends block entirely.** It sits above the list, delays the answer, and every number in it is
either mis-scoped, mis-dated or untraceable. If the analyzer wants to keep a market note, the only
honest version is one sentence acknowledging that published estimates for 2025 range from roughly
$291bn to $464bn depending on the firm — which is itself a more interesting and more defensible
claim than any single figure. Never restate the $365.67bn / $470.92bn pair.

---

## 7. Internal links (task 6) — verification results

**Method limitation, stated plainly:** Bash is disabled in this session, so I could not run a
curl-style check with a browser User-Agent and `--max-redirs 0`. The fetch tool available here
follows same-host redirects silently. To compensate I requested the `rel=canonical` and the rendered
H1/title for every URL and compared them to the requested path. A same-host 301 would surface as a
canonical or H1 that does not match the slug. **This is weaker than the section 6 standard. The
publisher must re-run all of these with a proper no-redirect check before any PUT.**

| URL | Result | H1 / title returned | Canonical | Recommend |
|---|---|---|---|---|
| `/woocommerce-dropshipping-guide/` | **200** | "WooCommerce Dropshipping: Major Features, Set Up Guide, Top Plugins, and Popular Suppliers" | Self-referential, exact match | **Yes** |
| `/how-to-set-up-woocommerce-for-dropshipping/` | **200** | "How to Set Up WooCommerce for Dropshipping?" | Not surfaced; H1 matches slug | **Yes** |
| `/platforms/woocommerce-development-services/` | **200** | "The Leading WooCommerce Development Company in the U.S." | **No canonical tag present** on the page | **Yes** (also verified 200 for post 42491) |
| `/woocommerce-plugin-development/` | **200** | "WooCommerce Plugin Development" | Not surfaced; H1 matches slug | **Yes** |
| `/hire-woocommerce-developer/` | **200** | "Hire WooCommerce Experts and Developers" | Self-referential, exact match | **Yes** |
| `/woocommerce-guide/` | **200** | "WooCommerce Complete Guide: Top Features, Review, and How to Setup WooCommerce" | Self-referential | **Yes** |
| `/woocommerce-migration-guide/` | **200** | "WooCommerce Migration Guide: Migrate to WooCommerce From Any eCommerce Platform" | Self-referential, exact match | **Yes** |
| `/wordpress/` | **200** | "Harness the Power of WordPress for Your Business" | Not surfaced; content matches | **Yes** |
| `/get-in-touch/` | **200** | "Just ask. Get answers." (contact page) | Not surfaced | Yes, but section 6 bans internal links in the conclusion — body only |

Nine verified destinations, comfortably inside the 5–10 requirement. The page currently uses six of
them (`/wordpress/`, `/platforms/woocommerce-development-services/`, `/woocommerce-dropshipping-guide/`,
`/woocommerce-plugin-development/`, `/woocommerce-guide/`, `/hire-woocommerce-developer/`) and all six
still resolve.

**Not checked and not recommended** (never guessed from slug patterns): every other Virtina path.

**Confirmed dead, do not link** (from MUST-FOLLOW-RULES section 6, re-stated for the creator):
`/ecommerce-migration-services/` 404, `/ecommerce-development-services/` 404,
`/ecommerce-seo-services/` 404, `/contact/` 301 to `/get-in-touch/`.

### Anchor text suggestions (2–5 words, clean noun phrases, each naming its destination)

- `/woocommerce-dropshipping-guide/` → "WooCommerce dropshipping guide"
- `/how-to-set-up-woocommerce-for-dropshipping/` → "WooCommerce dropshipping setup"
- `/woocommerce-plugin-development/` → "custom WooCommerce plugin development"
- `/platforms/woocommerce-development-services/` → "WooCommerce development services"
- `/hire-woocommerce-developer/` → "WooCommerce developers"
- `/woocommerce-guide/` → "WooCommerce platform guide"
- `/woocommerce-migration-guide/` → "WooCommerce migration guide"

---

## 8. Competitor safety (task 7)

Checked against `style/brand.md`. Virtina's named competitors are agencies — Absolute Web, Coalition
Technologies, Blue Stout, Tako Agency, Shero Commerce, Born Group, VL OMNI, Fuel Made, Electric Eye,
Underwaterpistol. **None of the 25 plugins, and none of the 10 additions, is on that list.** Naming
all of them in prose is safe.

Two constraints the creator must observe:

1. **Maximum 2 external links.** The page currently has **zero** external links, which is fine. If
   the refresh adds any, the two highest-value candidates are the official WooCommerce.com extension
   page and a wordpress.org plugin page used as the evidence for a status claim. Everything else
   stays plain text.
2. **`shopify.com` and `bigcommerce.com` are banned.** Several plugin vendors (Zendrop, Modalyst,
   Dropified) are Shopify-first. Describe them factually, but do not link out to any Shopify-owned
   property.

---

## 9. Everything else on the live page that is now stale (task 8)

1. **H1 says "Top 20", body lists 25.** Whatever the final count, the H1, the TOC, the comparison
   table heading and the numbered H3s must all agree.
2. **"Updated 2026" badge on a page containing a plugin dead since 2019.** Beeketing alone makes the
   badge a trust liability.
3. **Inventory excerpt drift.** `published-posts-inventory.md` line 141 still records the old title,
   "Top 20 WooCommerce Dropshipping Plugins (Updated June 2025, tested on Woo 8.x)". **"Tested on Woo
   8.x" is badly stale** — WordPress.org now reports plugins tested up to WP 7.1. Any surviving
   "tested on" claim in copy or metadata needs to be re-anchored or removed.
4. **Yoast focus keyword is empty.** Set it to `woocommerce dropship plugin`, the actual target.
5. **The Yoast title omits the singular target phrase.** Currently "Top 20 WooCommerce Dropshipping
   Plugins 2026 | Virtina". It also says 20.
6. **No Introduction H2 and no People Also Ask H2** — both required by the standard structure.
7. **Broken TOC anchor** (`http://best-woocommerce-dropshipping-plugins`, missing `#`).
8. **TOC uses the banned Thrive `tcb-styled-list` markup** — the exact pattern that broke post 42202.
   Must be rebuilt from `reference/toc-working-template.html`.
9. **H3 headings are wrapped in up to eight nested `<strong>` tags** (e.g. Market Size and Growth,
   Product Category Growth). Serializer corruption from repeated Thrive edits.
10. **`⇨` glyphs are hard-coded into H3 and H4 text.** They are decorative characters inside heading
    content, not icons, and they pollute the extracted heading text that LLMs read.
11. **"AutoD" vs "AutoDS"** inconsistency between H3, H4 and TOC.
12. **The FAQ H2 reads "Best WooCommerce Dropshipping Plugins - Frequently Asked Questions (FAQs)"**
    but the TOC anchors to `#frequently-asked-questions` and labels it "Frequently Asked Questions
    -FAQs". Verify the id actually exists on the H2.

---

## Semantic keyword list for the creator (section 4b requires 10–15)

woocommerce dropship plugin (exact target, currently zero occurrences — must appear in the H1 or an
early H2 and 3–5 times in body prose), dropshipping plugin, supplier network, AliExpress import,
print-on-demand, order fulfilment automation, product import, inventory sync, profit margin rules,
ePacket shipping, active installs, tested up to, plugin maintenance, abandoned plugin, WooCommerce
marketplace extension, Temu sourcing, EU suppliers, US suppliers, Chrome extension importer,
supplier diversification.

---

## The gap

> Every page in the top 10 recommends WooCommerce dropshipping plugins. Not one of them checks
> whether the plugins still exist. LiquidWeb still recommends WooShark, which was renamed. Omnisend
> and LiquidWeb both still recommend Zendrop, which quietly dropped WooCommerce support. Four of the
> five still recommend WooDropship, whose blog stopped in July 2023. And Virtina's own page — the one
> badged "Updated 2026" — lists Beeketing, whose domain has redirected to a different company since
> the pivot, and Ezusy, whose domain no longer resolves at all. It also lists the same plugin twice
> under two names, and one plugin that is a checkout funnel builder with no dropshipping function.

## Recommended angle

> Rebuild 38972 as the only WooCommerce dropship plugin page that shows its work: every plugin gets a
> verified status, an active-install count, a last-updated date and a price checked on a stated date,
> the eight dead or misclassified entries are removed and named as removed, and the ten that were
> missing (starting with the official WooCommerce.com extension and VillaTheme's 9,000-install ALD)
> are added.

The "we cut eight" framing is the differentiator. A page that publicly removes plugins is making a
claim no competitor can copy without redoing the work. It also fixes the Top 20 vs 25 contradiction
by design rather than by patching a number.

**Format note for the analyzer:** this is Format C (listicle with opinions) by nature. Section 11
requires an opinionated position on each item — which the status verdicts supply directly. The
current page is the neutral survey that `audience.md` explicitly lists under what readers hate.

---

## Couldn't verify — flagged explicitly

- **Google's live People Also Ask questions.** The search tool returns organic results only. Do not
  let the creator invent them; get them from a manual incognito search.
- **Grand View Research's dropshipping report at source.** `grandviewresearch.com` returned HTTP 403.
  Its figures are therefore secondhand and must not be published.
- **AutoDS plan prices.** JavaScript-rendered; the HTML contains `$__` placeholders.
- **CJdropshipping fees.** Not published anywhere on their site.
- **DropshipMe paid pricing.** Only the 14-day free trial is shown.
- **WooDropship plugin price and maintenance status.** No price on `/pricing/`; newest blog post July
  2023; not on wordpress.org.
- **Wholesale2b's current WooCommerce integration.** Absent from the pricing page;
  `/dropship-woocommerce.html` returned an empty body.
- **NextsChain vs ScaleOrder.** `nextschain.com` serves ScaleOrder content. Whether this is a rename,
  a sibling brand or a parked redirect could not be established. No pricing, no WooCommerce
  confirmation, no plugin.
- **The official Woo extension's USD price.** The product page served INR (₹7,575/yr). WPBeginner
  quotes $79/yr but that is secondhand.
- **CartFlows active-install count.** The API returned 10,929,414, which is the cumulative *download*
  count, not active installs. Do not publish that figure. CartFlows' status as actively maintained is
  confirmed regardless (v3.2.0, 2026-08-24, tested WP 7.1).
- **Whether a no-redirect internal link check would change any result in section 7.** Bash was
  unavailable. Publisher must re-verify.

## Sources

WordPress.org plugin API and plugin pages (primary):
- api.wordpress.org/plugins/info/1.2/ — query_plugins for "woocommerce dropshipping", "dropshipping", "aliexpress import woocommerce", "printify", "dropified", "wooshark", "dropshipme"
- api.wordpress.org/plugins/info/1.0/cartflows.json, beeketing-for-woocommerce.json, dsers.json (404)
- wordpress.org/plugins/dsers/ — permanent closure notice, 2021-04-28
- wordpress.org/plugins/beeketing-for-woocommerce/ — last updated 2019
- wordpress.org/plugins/ali2woo-lite/ — AliNext rename
- wordpress.org/plugins/appscenic/, wordpress.org/plugins/spreadr-for-woocomerce/ — staleness warnings

Vendor sites (primary):
- alidropship.com/woocommerce-dropshipping-plugin/, dropified.com/pricing/, dropified.com/manage-stores-2/,
  spocket.co/pricing, syncee.com/pricing/, importify.com/pricing/, doba.com/pricing,
  wholesale2b.com/pricing, appscenic.com/pricing, printful.com/pricing, printify.com/pricing/,
  zendrop.com/pricing/, zendrop.com/integrations/, dsers.com/integration, modalyst.co,
  modalyst.co/woocommerce/ (404), cjdropshipping.com, cjdropshipping.com/integrations/woocommerce,
  autods.com/pricing, woodropship.com, dropship.me, nextschain.com, beeketing.com (301 to shopbase.com),
  ezusy.com (DNS failure), woocommerce.com/products/woocommerce-dropshipping/

Competitive scan (secondary):
- wpbeginner.com/showcase/best-woocommerce-dropshipping-plugins-compared/ — 2026-03-20
- omnisend.com/blog/woocommerce-dropshipping/ — 2025-11-11
- liquidweb.com/wordpress/ecommerce/compatible-dropship-companies/ — no date
- wpfactory.com/blog/top-plugins-for-successful-woocommerce-dropshipping/ — 2023-05-06
- wbcomdesigns.com/woocommerce-dropshipping-plugins/ — 2023-01-28, mod 2026-05-29

Market data (secondary, all rejected for publication):
- gminsights.com/industry-analysis/dropshipping-market — Dec 2025, $290.7bn 2025
- grandviewresearch.com/industry-analysis/dropshipping-market — HTTP 403, not read
- imarcgroup.com/dropshipping-market — $405.7bn 2025
- statista.com apparel forecast — US$662.70bn 2025 worldwide

Internal (primary):
- virtina.com live page and the 2026-09-08 `_tve_updated_post` backup
- Nine virtina.com URLs listed in section 7
