---
title: Competitor analysis — Square CBD/hemp cutoff
client: virtina
date: 2026-08-21
stage: research
slug: competitor-analysis-square-cbd
---

# Competitor analysis (MUST-FOLLOW section 4c)

## Method + honesty statement

Real searches were run. Queries (5, all returned results):
1. `Square CBD hemp policy change October 15`
2. `Square seller community hemp CBD prohibited November 5 2026 support article`
3. `squareup.com help article hemp CBD products no longer supported`
4. `what to do Square banned my CBD store alternatives`
5. `"Square" CBD hemp deadline what merchants should do migrate store`

**Honesty notes required by section 4c:**
- **SERP positions below are approximate.** The search tool returns ranked result lists, not numbered SERP positions. Positions are inferred from ordering across the five queries and labelled as such.
- **Two ranking pages could not be fetched.** marijuanamoment.net and nothingbutcanna.net both return **HTTP 403** to WebFetch. They are documented from search-result summaries only and are marked as such. I did not invent content for them.
- **4 pages were fetched in full**, exceeding the 3-page minimum.
- **The competitive field is commercially conflicted.** Almost every ranking non-news page is published by a high-risk payment processor or a cannabis POS vendor selling the solution. That is itself the opportunity.

---

## 1. Cova Software — the strongest competitor

- **Approx. position:** 1–2 across queries 4 and 5
- **URL:** https://www.covasoftware.com/blog/looking-for-a-square-alternative-why-hemp-and-cbd-retailers-should-start-preparing-now
- **Title:** "Looking for a Square Alternative? Why Hemp and CBD Retailers Should Start Preparing Now"
- **Domain:** Cova — cannabis/CBD **POS vendor**
- **Word count:** ~3,500
- **Published:** Aug 10, 2026; updated Aug 20, 2026
- **Structure:** Key Takeaways / program ending / who's affected / account, data and money / what to look for in an alternative / checklist / questions / vendor CTA

**Weaknesses**
1. **It is a POS pitch and closes as one** ("Regulations Change. Cova Is Built for It"). Every recommendation funnels to a retail POS, so it is structurally unable to tell a merchant "you may not need a new POS at all — you may need a new catalog."
2. **It treats Section 781 as background, not as a decision input.** It names the law and dates, then moves straight to vendor selection. It never asks the reader which of their SKUs actually survive the 0.4 mg per-container cap. A merchant could follow this entire article, migrate perfectly, and still be selling illegal product on Dec 12.
3. **Retail-first framing.** It is built for a dispensary/shop with a counter. Online-only sellers get little: no self-hosted vs hosted storefront discussion, no gateway-vs-platform separation, no data-ownership argument.

**How Virtina beats it**
1. Virtina isn't selling a POS, so it can lead with the uncomfortable, useful question: split your catalog first, buy nothing until you have. That is credibility Cova structurally cannot buy.
2. Virtina makes the law the spine of the decision, not the intro: a "survives Section 781 / doesn't" catalog split, with the 0.4 mg **per container** definition and the "innermost packaging" definition spelled out, plus the live Dec 11 delay fight and its synthetics carve-out.
3. Virtina writes for the online seller: storefront ownership, portable product/customer/order data, and the fact that WooCommerce is a plugin, not a processor.

---

## 2. Vector Payments

- **Approx. position:** 1–3 across queries 1, 2, 5
- **URL:** https://www.vectorpayments.com/square-is-shutting-down-cbd-and-hemp-merchant-accounts-by-november-5-2026/
- **Title:** "Square CBD Merchant Account Shutdown 2026"
- **Domain:** Vector Payments — **high-risk payment processor**
- **Word count:** ~2,800
- **Published:** Aug 18, 2026
- **Structure:** quick answer / explanation / six FAQ-style H2s / FAQ / CTAs / related posts / contact form

**Weaknesses**
1. **Gets the law wrong in a way that matters.** It describes the new threshold as **"0.3% total THC"** and calls it "proposed." The operative consumer-product rule is **0.4 mg of total THC per container**, and it is **already enacted** (signed Nov 12, 2025). A percentage cap and a milligram-per-container cap produce completely different answers for a gummy or a beverage. This is the single biggest factual error in the field.
2. **Vague on the effective date.** It says the date "has reportedly shifted at least once already and may shift again" without naming H.R. 6500, the Aug 8 90–6 vote, the Aug 9 61–32 tabling of the Budd amendment, or Dec 11. Reader leaves with anxiety and no dates.
3. **Money section is a hedge.** "No evidence this is a broad payout freeze... but any account closure can affect pending settlements or reserve funds." No citation to Square's actual terms, no numbers, no timeline.

**How Virtina beats it**
1. Virtina states the rule correctly and precisely, in milligrams per container, with "container" defined, and dates the claim to 2026-08-21.
2. Virtina names the bills, the votes, the counts, and both candidate dates, and adds the point Vector misses entirely: **a federal delay does not move Square's dates.**
3. Virtina quotes Square's own Payment Terms on reserves, deferred payouts, and the documented **120-day** refund window, and explicitly labels the widely-repeated "90-day hold" as unverified merchant-services folklore.

---

## 3. Evolve Payment

- **Approx. position:** 2–4 on queries 1 and 5
- **URL:** https://www.evolvepayment.com/blog/square-is-cutting-off-hemp-and-cbd-merchants-heres-what-actually-changed-and-what-operators-should-do-before-october-15/
- **Title:** "Square Is Cutting Off Hemp and CBD Merchants. Here's What Actually Changed, and What Operators Should Do Before October 15."
- **Domain:** Evolve Payment — **payments consultancy / processor**
- **Word count:** ~2,400
- **Published:** ~Aug 7, 2026

**Weaknesses**
1. **Best legal detail in the field, worst practical follow-through.** It correctly names Section 781, H.R. 5371, the Nov 12 2025 signing, the 0.4 mg per-container cap, and the Dec 11 contingency. Then it raises the money questions as *questions* — "when does settlement stop, what reserve is held, and on what release schedule?" — and never answers any of them.
2. **October 15 only.** The title and the whole frame are built on Oct 15. The **Nov 5 full account closure** for hemp-primary sellers, which is the far worse outcome, is a passing mention. Merchants most at risk get the least guidance.
3. **Nothing on data.** No item library export path, no transactions export, and no mention of card-on-file migration at all — the one step with a hard two-week lead time and an ordering dependency.

**How Virtina beats it**
1. Virtina answers the questions Evolve only poses, using Square's own Payment Terms sections rather than speculation.
2. Virtina carries **both** deadlines side by side and states plainly which reader each one applies to, because the Nov 5 reader is the one in real trouble.
3. Virtina gives the exact export paths (Dashboard → Items & services → Item library → Actions → Export Library; Reports → Transactions → Export) and the card-on-file process from Square Help 7871, including the phone-only request, the PCI DSS Level 1 requirement, and the "up to two weeks" timeframe.

---

## 4. Marijuana Moment — the news original **[NOT FETCHED: HTTP 403]**

- **Approx. position:** 1 on queries 1, 2, 3
- **URL:** https://www.marijuanamoment.net/square-tells-businesses-to-stop-selling-hemp-and-cbd-products-in-light-of-upcoming-federal-ban/
- **Domain:** Marijuana Moment — cannabis policy news outlet
- **Published:** ~Aug 6–7, 2026
- **Word count:** not measurable (403)

**Weaknesses (from search summaries + the fact that all four other pages cite it as the origin)**
1. **News, not guidance.** It reports the notice and the dates. It does not tell a merchant what to do on Monday.
2. **No commerce or payments depth.** Nothing on exports, reserves, chargeback tails, merchant accounts, or storefront choices — it isn't trying to.
3. **Perishable.** It is a dated news item and will not be updated as the House acts in September.

**How Virtina beats it**
1. Virtina is the guidance layer the news story creates demand for.
2. Virtina supplies the payments and data mechanics Marijuana Moment doesn't cover.
3. Virtina's structure is durable: the framework (split the catalog, own the MID, three clocks) still works whichever way the House votes.

**Do not link to it** — cite the reported Square wording, keep the 2-external-link budget for squareup.com primary sources.

---

## 5. Nothing But Canna **[NOT FETCHED: HTTP 403]**

- **Approx. position:** 4–6 on queries 1, 2, 5
- **URL:** https://www.nothingbutcanna.net/blogs/news/square-opened-the-door-for-hemp-in-2019-it-closes-it-on-november-5
- **Domain:** hemp retailer blog
- **Word count:** not measurable (403)

**Weaknesses (search summary only, flagged)**
1. Retailer commentary, not operational guidance.
2. Framed entirely on **Nov 5**, the mirror of Evolve's Oct-15-only error; mixed-catalog sellers get nothing.
3. No primary sourcing on funds, data, or the underwriting timeline.

**How Virtina beats it:** both dates, both merchant types, primary sources for the money and the data, and a plan with a start date instead of a lament.

---

## Field-wide gaps Virtina should claim

1. **Nobody separates the three problems.** Storefront, processing, and product legality are blurred everywhere. Virtina separates them in the thesis.
2. **Nobody says migration won't save an illegal SKU.** Every publisher here sells migration or accounts, so none of them can. Virtina can, and it is the most useful sentence available on this topic.
3. **Card-on-file is nearly absent.** Only Cova mentions it. Nobody surfaces the ordering trap: you must choose the new processor *before* Square will release the cards, and it takes up to two weeks.
4. **Nobody notes that a federal delay doesn't reopen Square.** Merchants are reading the Dec 11 news as a reprieve. It isn't one, for their Square account.
5. **Nobody explains the sub-merchant/PayFac mechanism** that made this possible without warning, so nobody explains why owning a MID is the actual structural fix.

---

## Cluster saturation (section 4c)

- WooCommerce cluster in the inventory: **51 posts** — heavily saturated.
- Deplatforming / high-risk / platform-risk sub-cluster: **3 blog posts** (42428 vape/Shopify, 42441 leaving Shopify, 13981 CBD 2019) plus the `/square-cbd-hemp-ban-migration/` landing page.
- **Flagged as saturated at the parent-cluster level. Justifying sub-niche:** a **payment-processor** cutoff driven by an **enacted federal statute with a live effective-date fight**, where the honest conclusion is that migration fixes the infrastructure but not the catalog. No existing Virtina post makes a regulatory statute the decision spine, and none argues that migration has limits. Passes.

**Competitor domains to exclude from links:** covasoftware.com, vectorpayments.com, evolvepayment.com, corepay.net, zenpayments.com, inclusivepay.com, paymentcloudinc.com, organicpaymentgateways.com, marijuanamoment.net, nothingbutcanna.net. None are Virtina agency competitors, but all are commercially conflicted on this exact keyword — do not send them traffic.
