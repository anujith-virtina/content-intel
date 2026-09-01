---
title: Square CBD/hemp account closures — verified fact base for supporting blog post
client: virtina
date: 2026-08-21
topic: Square cutting off CBD and hemp sellers; Section 781 hemp law; migration to self-hosted WooCommerce with an owned high-risk merchant account
audience: Small business owners selling CBD/hemp on Square (retail POS and/or Square Online). Secondary: B2C founders on hosted platforms in regulated categories.
stage: research
slug: square-cbd-migration
---

# Research notes — Square CBD/hemp cutoff

## 0. Tooling limitations (read this first)

- **No Bash/shell tool was available in this session.** I could not run the python/urllib browser-UA fetch.
- `WebFetch` returns **HTTP 403 on virtina.com** (confirmed on `https://virtina.com/square-cbd-hemp-ban-migration/` and on `/wp-json/wp/v2/posts`). So:
  - **The published-posts inventory could NOT be refreshed via WP REST.** It is stale (`last_updated: 2026-07-24`, 28 days). See uniqueness audit for the workaround used and one confirmed inventory error.
  - **Internal links are index-verified, not HTTP-verified.** Every URL below was returned by a live site-restricted search of `virtina.com`, which means Google currently indexes it. That is strong but not equivalent to a 200. **The publisher must HTTP-verify all of them with the browser UA before any PUT.**
- `WebFetch` also 403s on marijuanamoment.net, congress.gov, and nothingbutcanna.net. Facts from those outlets are sourced through pages I *could* fetch, and flagged accordingly.

---

## 1. VERIFICATION STATUS OF THE OCTOBER 15 DEADLINE

**Verdict: the October 15 date is real, but the landing page tells only half the story. There are TWO Square deadlines, and the landing page states only one.**

| Date | Applies to | What happens | Confidence |
|---|---|---|---|
| **Aug 7, 2026** | affected sellers | Square sends the notice | High (Cova, Evolve, Cannabis Promotions all date it here) |
| **Oct 15, 2026** | sellers with a **mixed catalog** (CBD/hemp alongside other products) | Remove all CBD/hemp/hemp-derived items from the Square catalog, in person and online. Rest of the account stays active. | **High** |
| **Nov 5, 2026, 11:59pm EST** | sellers whose business is **primarily** CBD/hemp | **Entire Square account closes** | **High** |
| earlier dates in Oct | some individual merchants | Reported early closures | Low — anecdotal |

Verbatim from Square's notice, as quoted by Marijuana Moment (under 15 words):
> "selling CBD and hemp-derived products — online or in person — will no longer be permitted"

And the catalog instruction, as quoted:
> "remove any CBD, hemp and hemp-derived items from your Square catalog (both in-person and online)"

**What I could NOT verify — flag as UNVERIFIED:**
- **Square's own public help/policy page stating this.** I fetched `squareup.com/help/us/en/article/5122-square-s-prohibited-goods-and-services` — it redirected to the Support Center homepage and contains **no** CBD/hemp mention. Multiple sources report Square **took down** its "sell CBD online" marketing page. I could not confirm the takedown directly. **Do not cite a Square policy URL for the ban; cite the seller notice as reported.**
- Whether Nov 5 is uniform or per-account. Evolve says closure dates varied by merchant.
- The claim that Square offered alternative Square Loan repayment arrangements (Cova calls this "reportedly" — treat as UNVERIFIED).

**Editorial consequence:** the landing page's Oct 15 framing is correct for mixed-catalog sellers and **understates the risk for hemp-primary sellers, whose whole account dies Nov 5.** The blog should carry both dates. This is a real service to the reader and a legitimate reason for the blog to exist alongside the landing page.

---

## 2. THE REGULATORY CAUSE — verified in detail

### The 2018 baseline
The 2018 Farm Bill legalized hemp defined by **delta-9 THC at or below 0.3% dry weight**. Measuring only delta-9 is what created the delta-8 / THCA / HHC market: those products stayed technically compliant.

### What changed: Section 781
- **Vehicle:** **H.R. 5371**, the *Continuing Appropriations, Agriculture, Legislative Branch, Military Construction and Veterans Affairs, and Extensions Act, 2026* — the bill that ended the shutdown.
- **Signed:** **November 12, 2025**.
- **Provision:** **Section 781**.
- **Original effective date:** **November 12, 2026** (a one-year delay written into the statute).

What Section 781 does (Troutman Pepper Locke / Regulatory Oversight, Dec 2025):
1. Moves the plant standard from delta-9 only to **total THC**, explicitly **including THCA**, at not more than 0.3% dry weight.
2. Caps finished consumer products at **"0.4 milligrams per container of total THC (including THCA)."** Milligrams per container, **not a percentage** — this is the part most merchants misread.
3. Defines "container" as **"the innermost packaging that encloses the final product for retail sale"** (bottle, bag, box, can, cartridge).
4. Excludes cannabinoids **"synthesized or manufactured outside the plant"** — i.e. CBD-to-delta-8 chemical conversion.
5. Preserves **"industrial hemp"**: fiber, stalk, grain, seed oil, microgreens, qualifying research.

### The delay fight (this is live and unresolved as of 2026-08-21)
- **Aug 8, 2026:** Senate passed a CR (**H.R. 6500**) **90–6** containing a one-month hemp delay.
- **Aug 9, 2026:** Senate voted **61–32 to table** Sen. Ted Budd's (R-NC) amendment that would have kept the original Nov 12 date. Delay survives.
- **Proposed new date: December 11, 2026.**
- **Reported carve-out:** the delay reportedly applies to **naturally derived** products (e.g. THCA), while **synthetics (delta-8 and other lab-made cannabinoids) stay on the Nov 12 date.** Sourced to Marijuana Moment via search summary — **flag as [unverified in primary text]**, and do not state it as settled.
- **STATUS: NOT LAW.** The House was in recess until early September and previously passed a version **without** the hemp language. Decision expected early-to-mid September, ahead of the Sept 30 funding deadline.

**Critical editorial instruction:** never write "the ban takes effect November 12" flatly. Write: enacted Nov 12, 2025; scheduled for **Nov 12, 2026**; the Senate has voted to push most of it to **Dec 11, 2026**, but that has not passed the House. Date the claim to 2026-08-21.

**And note the asymmetry the reader needs:** even if Congress delays the law, **Square's dates do not move.** Square set its own commercial deadline. A federal delay does not reopen your Square account.

---

## 3. WHAT HAPPENS TO THE SELLER'S MONEY — primary-sourced

From **Square's own Payment Terms** (`squareup.com/us/en/legal/general/payment`):

- **Reserves (Sec. 14):** Square "may withhold funds by temporarily suspending or delaying payouts" and/or require funds be held in "a separate reserve account (a 'Reserve')". The Reserve "may be raised, reduced or removed at any time by Square, in its sole discretion."
- **Deferred payout (Sec. 12):** Square "may defer payout or restrict access to your Proceeds, temporarily or indefinitely" pending investigation or dispute.
- **Chargebacks (Sec. 19–22):** the seller is responsible for chargeback liability; "if you have pending Chargebacks, we may delay payouts."
- **The 120-day number is real and documented:** refunds can be processed **"up to one hundred and twenty (120) days from the day you accepted the payment."** This is the number to use — it is Square's own language and it explains *why* a processor holds money past a closure date.
- **After closure (Sec. 38):** funds held in custody at closure, less fees, "will be paid out according to your payout schedule, subject to the other conditions in these Payment Terms."

**From Square's General Terms (Sec. 12):** Square "may terminate... or suspend or terminate your Square Account or your access to any Service, **at any time for any reason**."

**UNVERIFIED / folklore — do not state as Square policy:** the widely repeated "**90-day hold**" after deactivation. It appears only in third-party high-risk-processor blogs (PayKings, PaymentCloud, HostMerchant, SecureGlobalPay), all of whom sell competing merchant accounts. Square's own terms contain **no 90-day figure**. If used at all, attribute it as commonly reported by merchant-services firms, not as policy. Same for "180-day hold."

**Structural point (verified):** Square is a **payment facilitator (PayFac)**. Sellers are **sub-merchants** processing under Square's **master MID**; Square is the merchant of record. There is no underwriting and no credit check at signup, which is why approval takes minutes — and why termination can also be unilateral and fast. A **dedicated merchant account** gives you **your own MID** and a direct relationship with an acquiring bank, after underwriting.

---

## 4. THE ALTERNATIVES — honest version

**The single most important honest point, which no competitor states plainly:**

> WooCommerce does not process payments. Moving your store does not get you a payment processor, and it does not make a non-compliant product legal.

Three separate problems get blurred together in every article on this topic. Separate them:

1. **Storefront/POS problem** — where your catalog and checkout live. Solved by self-hosted WooCommerce.
2. **Processing problem** — who moves the money. Solved only by getting your **own high-risk merchant account with your own MID**, through underwriting.
3. **Product-legality problem** — whether the SKU is legal after Section 781 takes effect. **Not solved by either of the above.** No platform and no processor fixes a product over 0.4 mg total THC per container.

### What WooCommerce actually enables (verified)
- WooCommerce is a plugin on self-hosted WordPress. You control the database: products, customers, order history sit on infrastructure you own.
- WooCommerce supports **arbitrary third-party gateways**, so you can attach a high-risk gateway with your own MID.
- **Honest caveat that must appear in the post:** **WooPayments (Automattic's own gateway) restricts CBD**, and WordPress.com hosted plans have their own restrictions. "WooCommerce is open" is true of the *plugin*, not of Automattic's payment product. Self-hosting is the part that matters.
- **Second honest caveat:** self-hosting moves responsibility to you — hosting, security, PCI scope, updates, and your host's own acceptable use policy. This is a real trade-off, not a free win.

### Processors that serve hemp/CBD (name sparingly, all are commercial)
Named across the sources: **NMI** (gateway), Bankful, PaymentCloud, InclusivePay, Corepay, Zen Payments, Organic Payment Gateways, Vector Payments, Evolve Payment. **Recommendation: do not name specific processors in the post.** Every one of them is publishing on this keyword to sell accounts; naming them hands them credibility and dates the article. Describe the *category* (dedicated high-risk merchant account, own MID, interchange-plus, underwriting) and what to ask for.

### What underwriting will ask for (consistent across sources)
Certificates of analysis (COAs), processing statements, business formation documents, product/lab documentation, sometimes a state license. Applications should start **at least six weeks** before the deadline (Cova). Given Aug 21 → Nov 5, that window is **already tight**.

---

## 5. MIGRATION OFF SQUARE — what actually transfers

### Transfers cleanly (self-serve export)
- **Item library:** Dashboard → Items & services → Items → Item library → Actions → **Export Library**. Excel (.xlsx recommended by Square) or CSV. Can export all or filtered.
- **Transactions:** Reports → Transactions → set date range → **Export → Transactions CSV**. Includes customer names attached to purchases.
- **Customer directory** and **1099-K forms:** exportable from Dashboard.
- Square also exposes **public APIs** for pulling your own data.

### Does NOT transfer by self-serve — and this is the buried landmine
**Saved cards on file.** Per **Square's own help article 7871** (`squareup.com/help/us/en/article/7871-export-card-on-file-to-third-party-payment-processors`):
- Only the **account owner** can request it.
- Square will only send to a **"PCI DSS Level 1-compliant payment processor."**
- You must **phone Square Support at (855) 700-6000**, Mon–Fri 6:00am–6:00pm PDT, for ownership verification. There is no dashboard button.
- **"The average card export timeframe is up to two weeks."**
- Square sends an **encrypted file directly to the new processor**, containing card ID, primary account number, expiration date, postal code, and customer ID.
- Ecommerce platforms doing bulk migration must go through a **Partner Manager**.

**This is the strongest under-covered fact in the whole topic.** If a merchant has subscriptions or repeat customers on saved cards, they cannot start this on Nov 4. And they cannot start it at all if their new processor isn't PCI DSS Level 1 — which means **you must choose the processor before you can rescue the cards**. That reverses the order most people assume.

### Also does not transfer cleanly
- Reviews, loyalty balances, gift card liabilities, appointment/booking history, Square-native marketing lists, and Square Online theme/design (a Square Online site is not portable; it must be rebuilt).
- **Square Loans balances.** If the account closes with an outstanding Square Loan, repayment terms are affected. Sources say alternative arrangements were "reportedly" offered — **UNVERIFIED, flag it, tell the reader to ask Square in writing.**

---

## 6. LANDING-PAGE OVERLAP MAP

Landing page `/square-cbd-hemp-ban-migration/` (~2,261 words, 7 H2s) owns **commercial intent**. Its H2s and the blog's boundary:

| Landing page H2 | Blog treatment |
|---|---|
| "If you do nothing, here's what October 15th looks like" | **Blog goes deeper and corrects it:** two dates (Oct 15 mixed catalog / Nov 5 hemp-primary), plus the money and data clocks that run past both. |
| "Move your store off Square, onto a setup built for hemp sellers" | **Do not restate the offer.** Blog explains the *mechanism* (own MID vs sub-merchant) and the honest trade-offs of self-hosting. |
| "Your store closes at 9pm. This doesn't." | **Skip entirely.** Pure sales copy. |
| "Three steps, most stores are live before the deadline" | **Blog replaces this with a real timeline** built backwards from the deadline using verified durations (2-week card export, ~6-week underwriting, 120-day chargeback tail). |
| "Straight answers, no sales talk" | Blog has its own FAQ, **different questions** — must not duplicate. Analyzer should pull the landing page's FAQ text and dedupe. |
| "Get your store moved before Square shuts off your CBD sales" | Blog conclusion links *up* to the landing page; does not repeat the CTA language. |

**Rule for the creator:** the blog never uses the landing page's sentences. The blog's job is to make the reader understand their situation; the landing page's job is to close.

---

## 7. THE GAP (recommended angle)

Every article on this keyword is written by someone selling a merchant account or a POS. All of them answer the same question: *who should process your payments now?* Not one of them answers the question the merchant actually has at 11pm.

**Recommended thesis:**

> Square leaving is not your problem. It is a symptom. You are actually facing two separate problems with two different fixes, and one of them cannot be fixed by moving anywhere.

Structure the whole post around splitting them:

- **Problem 1 — your infrastructure.** Square is your storefront *and* your merchant of record. You are a sub-merchant on someone else's MID, which is why this could happen without warning. Fixable: own the store, own the MID.
- **Problem 2 — your catalog.** Section 781 will make some of your SKUs not-hemp. **Migration does not save those SKUs.** Splitting your catalog into "survives Section 781" and "does not" is the first thing to do, before you shop for a processor, because the answer determines whether you need a store at all or a different product line.

Then the practical spine no one has built: **three clocks running at once, all longer than you think.**
- The **catalog clock** (Oct 15) — 8 weeks from now.
- The **account clock** (Nov 5) — money stops.
- The **hangover clock** (120 days) — chargebacks can still hit after the store is gone, and Square can hold a reserve against them.
Plus the two clocks that run *backwards* from those: card export (**up to 2 weeks**, and you need the new processor chosen first) and underwriting (**~6 weeks**).

That timeline, with honest "this may not save your product" framing, is the article. It respects the reader enough to tell them the bad news, which is exactly the "user should feel" the brief asks for.

**Emotional register for the creator:** these are people whose income was cut off by an email from a company they never spoke to, over a law they had no part in. Do not be breezy. Do not be dramatic either. Plain sentences, concrete nouns, real numbers, no reassurance that isn't earned. Say "this is not your fault" once, because it's true and nobody else will say it.

---

## 8. SEMANTIC TERM LIST (16 — creator confirms coverage)

1. high-risk merchant account
2. payment facilitator (PayFac)
3. sub-merchant
4. merchant ID (MID)
5. merchant of record
6. underwriting
7. acquiring bank
8. rolling reserve
9. chargeback
10. payout schedule
11. acceptable use policy
12. card on file
13. PCI DSS Level 1
14. total THC
15. certificate of analysis (COA)
16. hemp-derived cannabinoid

Supporting: Section 781, self-hosted WooCommerce, catalog export, interchange-plus, dry weight basis.

---

## 9. INTERNAL LINK CANDIDATES

**Index-verified via site-restricted search (Google currently indexes each). NOT HTTP-verified — no shell tool. Publisher must re-verify with browser UA.**

| # | URL | Anchor (clean noun phrase) | Note |
|---|---|---|---|
| 1 | https://virtina.com/square-cbd-hemp-ban-migration/ | Square CBD migration support | **Primary target.** Confirmed 200 by orchestrator. |
| 2 | https://virtina.com/shopify-vape-store-woocommerce-migration/ | vape retailers on Shopify | **Post 42428.** Link here for the platform-risk argument instead of rebuilding it. |
| 3 | https://virtina.com/high-risk-payment-processing-ecommerce-businesses/ | high-risk payment processing | Best fit for the MID/underwriting section. |
| 4 | https://virtina.com/start-selling-cbd-online/ | CBD ecommerce setup | Category-specific service page. |
| 5 | https://virtina.com/payment-gateway-service-providers/ | payment gateway providers | Use in the "who moves the money" section. |
| 6 | https://virtina.com/woocommerce-migration-services/ | WooCommerce migration services | |
| 7 | https://virtina.com/migrate-to-woocommerce/ | migration to WooCommerce | |
| 8 | https://virtina.com/woocommerce-migration-guide/ | WooCommerce migration guide | |
| 9 | https://virtina.com/data-services | ecommerce data migration | **No trailing slash in the index.** Verify both forms. |
| 10 | https://virtina.com/platforms/woocommerce-development-services/ | WooCommerce development team | |
| 11 | https://virtina.com/cbd-ecommerce-how-to-make-the-most-out-of-the-young-market/ | CBD ecommerce market | Post 13981, 2019. Optional; dated. |

Target 8–10 of these. Body sections only, per section 6.

### External links — cap is 2. Recommended pair:
1. `https://squareup.com/help/us/en/article/7871-export-card-on-file-to-third-party-payment-processors` — Square's own card-export page. Highest-value link in the article.
2. `https://squareup.com/us/en/legal/general/payment` — Square Payment Terms (reserves, 120-day refund window).

Both are squareup.com, which is **not** a Virtina competitor domain (Square is a payments/POS company, not an ecommerce agency). Congress.gov would be a third option but WebFetch 403s it and the 2-link cap applies.

---

## 10. SLUG CANDIDATES

Constraint discovered: under CHECK 2 strictly, **any slug containing `square` plus any of {`cbd`, `hemp`, `ban`, `migration`} fails** against the landing page slug `square-cbd-hemp-ban-migration`.

1. **`square-cutoff-seller-action-plan`** — overlap with landing slug: `square` only (1 word). No overlap with `shopify-vape-store-woocommerce-migration` or `cbd-ecommerce-how-to-make-the-most-out-of-the-young-market`. Keeps the searched entity. Doesn't date itself. **RECOMMENDED.**
2. `hemp-seller-payment-cutoff-plan` — overlap: `hemp` only. Safest of the three, but drops "Square."
3. `cbd-seller-october-deadline` — overlap: `cbd` only. Strong CTR, but ages badly and the federal date may move to Dec 11.

**Recommended title:** "Square is closing hemp and CBD accounts: what happens to your money, your data, and your catalog"
- CHECK 1 clean against all existing titles.
- Avoid "what to do now" (3-word collision risk with post 42428's title).
- Avoid "Here's what actually changed" (near-verbatim match to Evolve Payment's competing title).
- Avoid "survival guide" (post 41204 uses it).

**Primary keyword:** `Square hemp and CBD account closure` (informational).
Secondary: `Section 781 hemp law sellers`, `payment processing after Square`, `Square CBD deadline`.
**Cannibalization note:** leave commercial terms like "square cbd migration to woocommerce" to the landing page. The blog links up to it; it must not compete for the same query.

---

## 11. RECOMMENDED FORMAT

**Format D — decision-tree / playbook.** The topic is a sequence of decisions against a hard external date, and the core move is a decision (which bucket is your catalog in?) that gates everything after it.

Recency check on the last posts: 42465 = E, 42441 = B, 42428 = E, 42393 = A, 42391 = A. **Format D has not been used recently.** Analyzer confirms.

Length: **2,000–2,400 words** (standard band). Required elements: numbered/checklist steps (how-to), a case snippet (problem/solution), 6–8 Q&A FAQ.

---

## 12. SOURCES

Fetched in full:
- Square Payment Terms — https://squareup.com/us/en/legal/general/payment
- Square General Terms — https://squareup.com/us/en/legal/general/ua
- Square Help 7871, card-on-file export — https://squareup.com/help/us/en/article/7871-export-card-on-file-to-third-party-payment-processors
- Troutman Pepper Locke / Regulatory Oversight, Section 781 analysis (Dec 2025) — https://www.regulatoryoversight.com/2025/12/congress-narrows-federal-definition-of-hemp-effectively-banning-most-intoxicating-hemp-products/
- Forbes, A.J. Herrington, Aug 9 2026, Senate delay vote — https://www.forbes.com/sites/ajherrington/2026/08/09/senate-votes-to-delay-looming-hemp-thc-ban/
- Evolve Payment (Aug 2026) — https://www.evolvepayment.com/blog/square-is-cutting-off-hemp-and-cbd-merchants-heres-what-actually-changed-and-what-operators-should-do-before-october-15/
- Vector Payments (Aug 18 2026) — https://www.vectorpayments.com/square-is-shutting-down-cbd-and-hemp-merchant-accounts-by-november-5-2026/
- Cova Software (Aug 10, upd. Aug 20 2026) — https://www.covasoftware.com/blog/looking-for-a-square-alternative-why-hemp-and-cbd-retailers-should-start-preparing-now
- Cannabis Promotions (Aug 7 2026) — https://cannabispromotions.com/news/article/square-tells-businesses-to-stop-selling-hemp-and-cbd-product-zgejvlct
- Square Help 5153, bulk import items — https://squareup.com/help/us/en/article/5153-import-items-online

Blocked (403) — used only via search summaries, flagged in text:
- https://www.marijuanamoment.net/square-tells-businesses-to-stop-selling-hemp-and-cbd-products-in-light-of-upcoming-federal-ban/
- https://www.congress.gov/bill/119th-congress/house-bill/5371
- https://www.nothingbutcanna.net/blogs/news/square-opened-the-door-for-hemp-in-2019-it-closes-it-on-november-5
- https://thehill.com/policy/healthcare/6009069-senate-funding-bill-seeks-hemp-thc-ban-delay/
