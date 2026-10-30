---
title: "Research notes — Square's hemp and CBD cutoff, and the federal hemp law that moved"
client: virtina
date: 2026-09-11
topic: Square closing hemp/CBD selling (online and in-person), Section 781 hemp redefinition, and what a shop owner should actually do
audience: CBD and hemp shop owners selling through Square POS and Square Online. Plain-language, non-developer.
stage: research
slug: square-cbd-hemp-ban
---

# Research: Square's hemp and CBD cutoff

## 0. READ THIS FIRST — three blocking findings

### 0.1 The landing page's legal claim is now OUT OF DATE

The landing page `/square-cbd-hemp-ban-migration/` says, verbatim:

> "a new federal law takes effect November 12, 2026 that redefines legal hemp"

**That was true when the page was written. It stopped being true on September 2, 2026.**

Verified from the enrolled bill text on govinfo.gov. H.R. 6500, the *Continuing Appropriations and
Extensions Act, 2027*, Division B, Section 2019, reads in full:

> "Until December 11, 2026, the amendments made by section 781 of division B of Public Law 119-37
> (7 U.S.C. 1639o note) shall only apply with respect to products described in paragraphs (1)(C)(ii)(I)
> and (1)(C)(iv)(I) of section 297A of the Agricultural Marketing Act of 1946 (7 U.S.C. 1639o)
> (as amended by such section 781)."

Those two cross-referenced paragraphs are the synthetic-cannabinoid exclusions. So the corrected
position, as of 2026-09-11, is:

| Date | What actually happens |
|---|---|
| **Nov 12, 2026** | Section 781 takes effect, but **only** for products containing cannabinoids not capable of being naturally produced by the plant. Practically: delta-8, delta-10, HHC, THC-O and other converted/synthesised cannabinoids lose hemp status. |
| **Dec 11, 2026** | Section 781 applies in full. The total-THC-including-THCA standard and the 0.4 mg per container cap bite for everything else, including ordinary CBD and naturally derived hemp products. |

**Editorial instruction, non-negotiable:** the blog must not repeat "November 12" as the date legal
hemp gets redefined. It must carry both dates and explain the split. Do this plainly, without
implying the landing page is wrong. Frame it as "the date moved, here is where it moved to."

**Separate recommendation for the orchestrator:** flag to the client that the landing page copy and
its FAQ ("What if the federal ban gets delayed or changed?") now need a factual update. The blog
should not be the only place the correction lives.

### 0.2 A complete, unpublished draft on this exact topic already exists in this repo

- `clients/virtina/output/research/square-cbd-migration-2026-08-21.md`
- `clients/virtina/output/briefs/square-cutoff-seller-action-plan-2026-08-21.md`
- `clients/virtina/output/drafts/square-cutoff-seller-action-plan-2026-08-21.md` (3,480 words, Format D)

It was **never pushed to WordPress**. Confirmed three ways: no `output/published/` file, no CMS payload
JSON, no inventory entry, and a live REST sweep returns no post with any Square/hemp slug. The newest
published Virtina post is 42575 (2026-09-10).

**This is a decision for the orchestrator, not for me.** Either finish and publish the August draft
with the legal facts corrected, or write fresh. Writing fresh while that draft sits unpublished
risks two near-identical assets. My recommendation is in section 9.

### 0.3 Post 42575 is published as of yesterday and it owns the payments territory

`/merchant-account-underwriting-2026/` went live 2026-09-10. Its 28 H2s cover underwriting, document
packs, MATCH, VMSS, VAMP ratios, Compelling Evidence 3.0, reserves, and gateway/MID routing. It does
not mention Square, hemp, or CBD.

**Boundary:** our post must not re-explain how underwriting works or what a high-risk merchant
account is. It links to 42575 and moves on. Any attempt to teach underwriting in this post is
cannibalisation of a one-day-old article.

---

## 1. Sub-questions a hemp shop owner actually has

1. Is my whole Square account closing, or only my CBD listings, and on what date?
2. What law is behind this, and did it change? (It did.)
3. What happens to money Square still owes me, and to my Square Loan?
4. Can I take my customers and my saved card data with me?
5. Where do I go, what does it cost in time, and what is the wrong move?

---

## 2. AUDIENCE AND TONE — hard constraint from the user

**Write for a CBD or hemp shop owner. Not a developer. Not a VP of eCommerce.**

This is a deliberate departure from `audience.md`, which describes B2B eCommerce leaders who read
"API, GraphQL, headless, schema" without explanation. **That audience file does not apply here.**

Banned from this article:
- API, REST, endpoint, schema, webhook, database, plugin architecture, hosting stack, DNS, PCI scope
- Any sentence a person could not read aloud to their business partner

Required instead:
- Payments explained as money movement, not as infrastructure
- "Square is the one with the bank relationship, not you" beats "you are a sub-merchant on a PayFac master MID"
- Define every term in the same sentence it first appears in, then use it normally

Still binding regardless: **max 20 words per sentence, max 3 sentences per paragraph** (MUST-FOLLOW 4b).
Those rules help here rather than fighting the brief.

---

## 3. Key findings

### Finding 1: Section 781 changes the measuring stick, not just the limit

- Source: [Changes to the Federal Definition of Hemp](https://www.everycrsreport.com/reports/LSB11381.html) — Congressional Research Service Legal Sidebar LSB11381, via EveryCRSReport
- What it says: the standard moves from delta-9 THC alone to **total THC including THCA**, at 0.3% dry
  weight. Finished products for ingestion, inhalation or topical use face a cap of **0.4 milligrams of
  total THC per container**. Cannabinoids that cannot be naturally produced by the plant, or that were
  synthesised outside it, are excluded from hemp entirely. Fiber, stalk, grain, seed oil and edible
  greens keep an explicit carve-out.
- Why it matters: **0.4 mg is per container, not a percentage.** This is the single most misread number
  in the whole story. A 30 ml tincture and a 500 ml drink get the same absolute allowance. Most
  full-spectrum CBD products on shelves today exceed it.

### Finding 2: The effective date split in two, and it is now law

- Source: [H.R. 6500 enrolled text, Division B Sec. 2019](https://www.govinfo.gov/content/pkg/BILLS-119hr6500enr/html/BILLS-119hr6500enr.htm) — GPO govinfo, primary
- Source: [Bill Signed into Law: H.R. 6500](https://www.whitehouse.gov/briefings-statements/2026/09/congressional-bill-h-r-6500-signed-into-law/) — The White House, September 2, 2026, primary
- What it says: the bill is the *Continuing Appropriations and Extensions Act, 2027*. It was signed
  September 2, 2026 and funds agencies through December 11, 2026. Section 2019 limits Section 781's
  reach until December 11, 2026 to the synthetic-cannabinoid paragraphs only.
- Sequence, verified: Senate passed 90-6 on August 8, 2026. House passed 370-48 on September 1, 2026.
  Signed September 2, 2026. (House vote tally corroborated by [Akerman LLP](https://www.akerman.com/en/perspectives/congress-approves-one-month-delay-of-federal-hemp-thc-restrictions.html)
  and by reporting in [The Hill](https://thehill.com/policy/healthcare/6064552-hemp-ban-delayed-house-funding-bill/).)
- Why it matters: this is the correction in 0.1. It is also the single best reason the blog exists. No
  competitor page has both dates right *and* connects them to Square's separate commercial deadlines.

### Finding 3: Section 781 was enacted a year before it bites, in the shutdown-ending bill

- Source: [Congress Narrows Federal Definition of Hemp](https://www.regulatoryoversight.com/2025/12/congress-narrows-federal-definition-of-hemp-effectively-banning-most-intoxicating-hemp-products/) — Troutman Pepper Locke, Regulatory Oversight, December 2025
- What it says: the vehicle was H.R. 5371, **Public Law 119-37**, signed November 12, 2025, with a
  one-year delay written into the statute.
- Confidence: the public law number and the 7 U.S.C. 1639o note citation are **independently confirmed
  by the govinfo text of H.R. 6500**, which cites "section 781 of division B of Public Law 119-37
  (7 U.S.C. 1639o note)" verbatim. congress.gov itself returns HTTP 403 to this tool.
- Why it matters: lets the article say "this has been law since November 2025" rather than "a new law is
  coming." Shop owners who felt blindsided were, in fact, given a year. That is worth saying kindly.

### Finding 4: Square's deadlines are Square's, and a federal delay does not move them

- Source: Square's seller notice, as reported by [Marijuana Moment](https://www.marijuanamoment.net/square-tells-businesses-to-stop-selling-hemp-and-cbd-products-in-light-of-upcoming-federal-ban/) (HTTP 403 to this tool; content confirmed via search summary and corroborated by four independent secondary reports)
- Two dates, consistently reported across five unrelated outlets:
  - **October 15, 2026** — sellers with a mixed catalog remove all CBD, hemp and hemp-derived items from
    the Square catalog, **in person and online**. The rest of the account stays open.
  - **November 5, 2026, 11:59pm EST** — sellers whose business is primarily hemp or CBD lose the
    **entire Square account**.
- Notice reportedly went out around August 7, 2026.
- **The asymmetry the reader needs:** Congress moved to December 11. Square did not move. A merchant who
  reads "the ban was delayed" and relaxes will still lose Square in October or November.
- **UNVERIFIED and must be flagged as such:** Square's own public policy page. `squareup.com/help/us/en/article/5122-square-s-prohibited-goods-and-services`
  redirects to the Support Center homepage and contains no CBD or hemp language. Re-checked 2026-09-11,
  same result as the 2026-08-21 check. **Never cite a Square policy URL as the source of the ban.**
  Cite the seller notice as reported, and date the claim.

### Finding 5: The Square Loan problem is worse than "it doesn't pause"

This is the strongest under-covered fact available, and it is sourced from Square's own help centre.

- Source: [Repay your loan](https://squareup.com/help/us/en/article/8546-repay-your-loan) — Square Support, primary
  - Repayment is automatic, taken as a fixed percentage of daily card sales. A minimum payment is
    required regardless. Repayment continues until the balance is zero, against a maturity date in the
    loan agreement.
- Source: [Manage a loan for a sold or closed business](https://squareup.com/help/us/en/article/6716-business-sold-or-closed-faq) — Square Support, primary
  - If the business closes without repaying, the loan is **in default** under the loan agreement.
  - On default, Square Financial Services "may demand immediate repayment of the outstanding balance."
  - Square "may debit any past due amounts from your business' Square-linked bank account, and increase
    your repayment rate."
  - Borrowers who cannot repay are told to contact Square, because "There may be an alternative
    repayment option."
- Why it matters: the landing page says the repayment does not pause. **The real risk is a step worse.**
  Account closure can convert a sales-linked repayment into a demand for the whole balance, collected by
  direct debit from the merchant's bank account. That is a cash-flow event, not an inconvenience.
- **Practical instruction for the article:** contact Square about the loan *in writing* before the
  account closes, not after. An alternative arrangement exists but is not automatic.

### Finding 6: Saved customer cards cannot be exported without a phone call and a two-week wait

- Source: [Export card on file to third-party payment processors](https://squareup.com/help/us/en/article/7871-export-card-on-file-to-third-party-payment-processors) — Square Support, primary (verified in the 2026-08-21 research run)
- Key mechanics: only the account owner can request it. Square only sends to a PCI DSS Level 1 compliant
  processor. There is no dashboard button, it requires a support phone call for ownership verification.
  Square's own stated timeframe is **up to two weeks**.
- Why it matters: **this reverses the order most people assume.** You cannot rescue your saved cards
  until you have already chosen and been approved by the new processor. Anyone with subscriptions or
  repeat customers on file has to start with the processor, not the store.

### Finding 7: Everything else exports cleanly, and that is genuinely reassuring

- Item library exports from Dashboard → Items & services → Items → Item library → Actions → Export
  Library, as Excel or CSV. Transactions export from Reports → Transactions with a date range. Customer
  directory and 1099-K forms export from Dashboard. (Verified 2026-08-21 against Square Support.)
- Does **not** transfer: reviews, loyalty balances, gift card liabilities, booking history, and the
  Square Online site design, which has to be rebuilt.
- Why it matters: the article can tell a frightened reader "your products and your customer list come
  with you" and be honest about it. Then name the three things that do not.

### Finding 8: Moving the store does not fix the product, and no competitor will say so

- Source: [FDA Concludes Existing Regulatory Frameworks Are Not Appropriate for Cannabidiol](https://www.fda.gov/news-events/press-announcements/fda-concludes-existing-regulatory-frameworks-foods-and-supplements-are-not-appropriate-cannabidiol) — FDA, primary
- What it says: FDA has concluded CBD products are excluded from the dietary supplement definition, and
  it is not lawful to add CBD to food or market it as a supplement. FDA says a new pathway is needed and
  it will work with Congress.
- Why it matters: combine with Finding 1 and you get the honest sentence nobody in this SERP can write.
  After December 11, a product over 0.4 mg total THC per container is not hemp. No platform, no
  processor and no agency fixes that. **Sort the catalog before shopping for a processor.**

### Finding 9: The whole SERP is sellers of the thing the reader is about to buy

Every ranking page for the money queries is published by a high-risk payment processor, a cannabis POS
vendor, or a hemp law firm. Their business model prevents them from saying "you may not need a new
store, you may need a different product line." See `competitor-analysis-2026-09-11.md`.

---

## 4. Data points — VERIFIED

| Stat | Value | Source | Verified |
|---|---|---|---|
| Total THC standard incl. THCA | 0.3% dry weight | [CRS LSB11381](https://www.everycrsreport.com/reports/LSB11381.html) | Yes |
| Finished-product cap | 0.4 mg total THC **per container** | [CRS LSB11381](https://www.everycrsreport.com/reports/LSB11381.html) | Yes |
| Section 781 vehicle | H.R. 5371, Public Law 119-37, signed Nov 12, 2025 | [govinfo H.R. 6500 cross-reference](https://www.govinfo.gov/content/pkg/BILLS-119hr6500enr/html/BILLS-119hr6500enr.htm) + Troutman | Yes |
| Full effective date | December 11, 2026 | [govinfo H.R. 6500 Div. B Sec. 2019](https://www.govinfo.gov/content/pkg/BILLS-119hr6500enr/html/BILLS-119hr6500enr.htm) | Yes, primary |
| Synthetics effective date | November 12, 2026 | Same, by cross-reference to (1)(C)(ii)(I) and (1)(C)(iv)(I) | Yes, primary |
| Delay bill signed | September 2, 2026 | [White House](https://www.whitehouse.gov/briefings-statements/2026/09/congressional-bill-h-r-6500-signed-into-law/) | Yes, primary |
| House vote on delay | 370-48, September 1, 2026 | [Akerman](https://www.akerman.com/en/perspectives/congress-approves-one-month-delay-of-federal-hemp-thc-restrictions.html), [The Hill](https://thehill.com/policy/healthcare/6064552-hemp-ban-delayed-house-funding-bill/) | Yes, two independent |
| Senate vote on delay | 90-6, August 8, 2026 | Same pair | Yes, two independent |
| Card-on-file export time | up to two weeks | [Square Support 7871](https://squareup.com/help/us/en/article/7871-export-card-on-file-to-third-party-payment-processors) | Yes, primary |
| Square refund window | 120 days from payment acceptance | [Square Payment Terms](https://squareup.com/us/en/legal/general/payment) | Yes, primary (2026-08-21 run) |
| Square mixed-catalog deadline | October 15, 2026 | Seller notice, 5 independent reports | Reported, not primary |
| Square account closure | November 5, 2026, 11:59pm EST | Seller notice, 5 independent reports | Reported, not primary |

## 4b. Data points — REJECTED, do not use

| Claim | Why rejected |
|---|---|
| "Square holds funds for 90 days after deactivation" | Appears only on high-risk-processor blogs (PaymentCloud, SecureGlobalPay, Durango, Redde) who sell competing accounts. **Square's own terms contain no 90-day figure.** The verified number is the 120-day refund window, which is a different thing. |
| "180-day hold" | Same failure, same sources. |
| Any count of affected Square merchants | No neutral source exists. Nobody has published a number. |
| Market size of the CBD/hemp ecommerce sector | Every figure traces to a vendor report behind a lead form. |
| "At least seven states have banned hemp-derived THCa" (Alaska, Arkansas, Delaware, Hawaii, Idaho, Iowa, Rhode Island) | Sourced only to hemp-retailer blogs (TribeTokes, The Haze Connect). Directionally plausible, **[unverified]**. Describe the pattern, never state the count. |
| "Tennessee HB 1376 bans online hemp sale and delivery from Jan 1, 2026" | Same vendor-blog sourcing. **[unverified]**, and it shares its source pool with the rejected state-count claim, which under the shared-source rule rejects it too. |
| Square "reportedly offered alternative Square Loan arrangements" to affected sellers | Third-party "reportedly" only. **Replace with the verified version**: Square's own help centre documents that an alternative option may exist and must be asked for. That is better and it is primary. |
| Naming specific high-risk processors | All are commercial parties publishing on this keyword. Naming them lends credibility and dates the article. Describe the category instead. |

**Where no neutral data exists, say so in the article.** There is no independent count of affected
merchants, no independent estimate of revenue at risk, and no neutral survey of processor approval
rates. The post should not invent proxies.

---

## 5. Conflicts and disagreements

- **Position A** (the Virtina landing page, and most hemp-industry pages written before Sept 2):
  federal hemp redefinition takes effect November 12, 2026.
- **Position B** (govinfo enrolled text of H.R. 6500, signed Sept 2, 2026): full application moves to
  December 11, 2026; only synthetic cannabinoids are caught on November 12.
- **What's actually true:** Position B. The statute text is primary and unambiguous. Position A was
  correct until September 2 and is now stale.

- **Position A** (processor blogs): Square holds funds for 90 days after deactivation.
- **Position B** (Square Payment Terms): no 90-day figure; a 120-day refund window exists, and Square
  may hold a reserve or defer payout at its discretion.
- **What's actually true:** Position B. The 90-day number is industry folklore repeated by parties who
  sell the alternative.

- **Position A** (most coverage): this is a Square story.
- **Position B** (the honest read): Square is one of several processors moving ahead of the statute.
  Stripe, PayPal and the major aggregators have all restricted this category at various points. The
  underlying event is a legal reclassification, and the payments industry is repricing risk around it.
- **What's actually true:** both, and the article should hold both. Naming it a Square story alone
  sets the reader up to move somewhere that bans them next.

---

## 6. Competitive scan (summary; full file: `competitor-analysis-2026-09-11.md`)

1. **Evolve Payment** — "Square Is Cutting Off Hemp and CBD Merchants" (~3,500 words). Best of the set,
   genuinely covers Section 781. Gap: no Square Loans, no card-on-file export, treats December 11 as
   only "potential," sells merchant accounts.
2. **Vector Payments** — "Square Is Shutting Down CBD and Hemp Merchant Accounts by November 5, 2026"
   (~2,500-3,000 words). Gap: thin on the law, no loan or data-export content, funnels to its own
   processing product.
3. **PaymentCloud** — "How to Get a CBD Payment Processor for Your WooCommerce Store" (~2,400 words).
   Gap: never mentions the 2026 law or the Square ban at all. Stale.
4. **Hemp Law Group** — "Federal Hemp Ban 2026: Where Things Stand" (~4,500 words). Best legal
   coverage, correct on December 11. Gap: almost no payments content, no ecommerce platform content,
   heavy Tennessee bias, it is a law-firm lead magnet.

**Documented SERP bias:** 100% of the fetched top results are published by a party selling either a
merchant account, a POS system, or legal services to the affected merchant. **Never link any of these
domains.**

---

## 7. The gap

> Every page on this topic answers "who should process your payments now?" because every page is
> written by someone who wants to be the answer. None of them answers the two questions the shop owner
> actually has at 11pm: *which of my products are still legal in December*, and *what happens to the
> loan Square already gave me*.

The second one is the sharpest. Square's own help centre documents that closing the business puts the
loan in default, permits a demand for the whole balance, and permits a direct debit of the linked bank
account. Not one competitor page mentions Square Loans at all. It is the highest-value verified fact
available and it is sitting in public on squareup.com.

---

## 8. Recommended angle

> You are being told to move your store. Before you move anything, sort two things Square's email did
> not mention: which of your products are still hemp on December 11, and what your Square Loan does the
> day the account closes.

Supporting spine: three clocks running at once, two of which run *backwards*.
- Catalog clock: October 15 (mixed catalogs) or November 5 (hemp-primary).
- Law clock: November 12 for synthetics, December 11 for everything else.
- Money clock: the 120-day refund window outlives the store, and the loan can accelerate on closure.
- Running backwards: card export takes up to two weeks and needs the new processor chosen first.

---

## 9. Recommendation on the August draft (for the orchestrator)

**Do not write a second article from scratch.** The August 21 draft is 3,480 words, Format D, and its
structure survives the legal change intact. Recommended path:

1. Treat this file as a **fact-correction and re-scope pass** on the existing draft.
2. Corrections required: the November 12 / December 11 split (0.1), the Square Loan default mechanics
   (Finding 5, upgrade from "reportedly" to Square's own documentation), and a link to post 42575
   instead of any underwriting explanation.
3. Simplify the register. The August draft is good but assumes more payments literacy than the user's
   "simple language, don't go too extreme technical" instruction allows. See section 2.
4. Trim toward 2,200-2,600 words. 3,480 is above the standard band and this reader will not finish it.

If the orchestrator prefers a clean rewrite, the uniqueness audit covers that case too, because the
August draft is unpublished and therefore not part of the live corpus.

---

## 10. Semantic term list (14 — creator confirms coverage, plain-language forms preferred)

1. hemp-derived CBD
2. total THC
3. THCA
4. milligrams per container
5. certificate of analysis (COA)
6. high-risk merchant account
7. merchant of record
8. payment processor
9. chargeback
10. payout
11. card on file
12. point of sale (POS)
13. catalog export
14. self-hosted store

Supporting: Section 781, dry weight, age verification, acceptable use policy, reserve.

**Note on register:** use the plain form first and the term second. "The lab report that proves what is
in your product, the certificate of analysis" reads correctly for this audience. The reverse does not.

---

## 11. Internal links — ALL VERIFIED 2026-09-11

Verified by querying the WP REST API for each slug and reading the canonical `link` field WordPress
itself returns. This is stronger than an HTTP check here, because WebFetch silently follows same-host
redirects and virtina.com returns 429 to curl. A slug that resolves to a different `link` is a
redirect, and is excluded. No 429 was recorded as either a pass or a fail.

| # | URL (canonical, from WP) | ID | Status | Suggested anchor (clean noun phrase) |
|---|---|---|---|---|
| 1 | https://virtina.com/square-cbd-hemp-ban-migration/ | 42474 | publish | Square CBD migration support |
| 2 | https://virtina.com/merchant-account-underwriting-2026/ | 42575 | publish | merchant account underwriting |
| 3 | https://virtina.com/high-risk-payment-processing-ecommerce-businesses/ | 36749 | publish | high-risk payment processing |
| 4 | https://virtina.com/high-risk-ecommerce-migration-payment-gateway-integration/ | 42417 | publish | high-risk payment gateway integration |
| 5 | https://virtina.com/start-selling-cbd-online/ | 12517 | publish | CBD store setup |
| 6 | https://virtina.com/payment-gateway-service-providers/ | 37458 | publish | payment gateway providers |
| 7 | https://virtina.com/woocommerce-migration-services/ | 22251 | publish | WooCommerce migration services |
| 8 | https://virtina.com/woocommerce-migration-guide/ | 29601 | publish | WooCommerce migration guide |
| 9 | https://virtina.com/platforms/woocommerce-development-services/ | 10144 | publish | WooCommerce development team |
| 10 | https://virtina.com/shopify-vape-store-woocommerce-migration/ | 42428 | publish | vape retailers on Shopify |
| 11 | https://virtina.com/volusion-to-woocommerce-migration/ | 42177 | publish | Volusion store migration |
| 12 | https://virtina.com/saas-ecommerce-platforms-for-online-stores/ | 27047 | publish | hosted ecommerce platforms |
| 13 | https://virtina.com/get-in-touch/ | 30 | publish | (conclusion CTA only, not a body link) |

Target 8-10 in body sections only, per MUST-FOLLOW section 6. Link 2 is mandatory: it is how we avoid
cannibalising yesterday's post.

**Note on `woocommerce-development-services`:** the REST `link` field confirms the canonical form is
`/platforms/woocommerce-development-services/`, matching the verified-dead-list rule in section 6.

**Avoid:** `/cbd-ecommerce-how-to-make-the-most-out-of-the-young-market/` (post 13981). It exists and
returns a valid link, but it is a 2019 growth-marketing piece whose premise, that CBD is a young
growth market, reads badly next to a federal restriction. Linking it invites the reader to a dated page.

### External links — cap is 2. Recommended pair:

1. `https://www.govinfo.gov/content/pkg/BILLS-119hr6500enr/html/BILLS-119hr6500enr.htm` — the statute
   text carrying the December 11 date. This is the article's proof and the reason it beats the SERP.
2. `https://squareup.com/help/us/en/article/6716-business-sold-or-closed-faq` — Square's own page on
   what a loan does when the business closes.

Both `target="_blank" rel="noopener noreferrer"`. Neither is a Virtina competitor domain. If only one
slot survives, keep the govinfo link.

---

## 12. What I could not find, and why it matters

- **Square's own public policy page confirming the ban.** The prohibited-goods article still redirects
  to the Support Center homepage. Re-checked today. This matters because it means the single most
  important commercial fact in the article rests on a leaked seller notice and five secondary reports.
  It is well corroborated but it is not primary. **The article must date and attribute it, never state
  it as Square policy from a Square URL.**
- **congress.gov.** Returns HTTP 403 to this tool for both bill pages and CRS products. Worked around
  via govinfo.gov (GPO, equally primary) and EveryCRSReport (verbatim CRS mirror). The statutory facts
  are not weakened by this, but a human should spot-check congress.gov before publish if possible.
- **Marijuana Moment.** HTTP 403. It is the original reporter of the Square notice. Its content is
  represented here through a search summary and four corroborating outlets, which is why Finding 4 is
  labelled "reported, not primary."
- **Any neutral count of affected merchants or revenue at risk.** Does not exist. The article should
  say plainly that nobody has published a number, rather than borrow a vendor's.
- **A per-state list of hemp shipping restrictions from a government source.** Only vendor blogs carry
  it. The article should tell readers to check their own state agency and not attempt a list.
- **Square Loan minimum-payment specifics** (the commonly cited "1/18th every 60 days"). Square's
  article 6588 now redirects to the Support Center homepage. Not verified, do not state it.

---

## 13. Sources

**Primary, fetched in full:**
- [H.R. 6500 enrolled text, GPO govinfo](https://www.govinfo.gov/content/pkg/BILLS-119hr6500enr/html/BILLS-119hr6500enr.htm) — 2026, statute
- [White House, H.R. 6500 signed into law](https://www.whitehouse.gov/briefings-statements/2026/09/congressional-bill-h-r-6500-signed-into-law/) — 2026-09-02
- [CRS Legal Sidebar LSB11381 via EveryCRSReport](https://www.everycrsreport.com/reports/LSB11381.html) — Congressional Research Service
- [Square Support 6716, loan for a sold or closed business](https://squareup.com/help/us/en/article/6716-business-sold-or-closed-faq)
- [Square Support 8546, repay your loan](https://squareup.com/help/us/en/article/8546-repay-your-loan)
- [FDA, existing frameworks not appropriate for CBD](https://www.fda.gov/news-events/press-announcements/fda-concludes-existing-regulatory-frameworks-foods-and-supplements-are-not-appropriate-cannabidiol)
- Virtina WP REST API — posts, pages and search endpoints, 2026-09-11

**Primary, carried forward from the 2026-08-21 run (re-cited, not re-fetched):**
- [Square Payment Terms](https://squareup.com/us/en/legal/general/payment)
- [Square General Terms](https://squareup.com/us/en/legal/general/ua)
- [Square Support 7871, card-on-file export](https://squareup.com/help/us/en/article/7871-export-card-on-file-to-third-party-payment-processors)

**Secondary, fetched:**
- [Akerman LLP, one-month delay of hemp THC restrictions](https://www.akerman.com/en/perspectives/congress-approves-one-month-delay-of-federal-hemp-thc-restrictions.html)
- [Troutman Pepper Locke, Regulatory Oversight, Dec 2025](https://www.regulatoryoversight.com/2025/12/congress-narrows-federal-definition-of-hemp-effectively-banning-most-intoxicating-hemp-products/)
- [Hemp Law Group, where things stand](https://www.hemplawgroup.com/news/federal-hemp-ban-2026-where-things-stand) — competitor scan only
- [Evolve Payment](https://www.evolvepayment.com/blog/square-is-cutting-off-hemp-and-cbd-merchants-heres-what-actually-changed-and-what-operators-should-do-before-october-15/) — competitor scan only
- [Vector Payments](https://www.vectorpayments.com/square-is-shutting-down-cbd-and-hemp-merchant-accounts-by-november-5-2026/) — competitor scan only
- [PaymentCloud](https://paymentcloudinc.com/blog/woocommerce-cbd/) — competitor scan only
- [The Hill, hemp ban delayed](https://thehill.com/policy/healthcare/6064552-hemp-ban-delayed-house-funding-bill/)

**Blocked (HTTP 403), used only via search summaries and flagged in text:**
- congress.gov (bill page and CRS product IF13136)
- marijuanamoment.net
