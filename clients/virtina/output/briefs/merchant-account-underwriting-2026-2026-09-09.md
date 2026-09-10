---
title: What underwriters actually check before they approve a regulated ecommerce store
client: virtina
date: 2026-09-09
topic: Merchant account underwriting decisioning and 2026 card-network threshold management for regulated ecommerce
audience: B2B/B2C ecommerce leaders in regulated verticals running WooCommerce or Magento
stage: brief
slug: merchant-account-underwriting-2026
research: clients/virtina/output/research/high-risk-payment-gateways-2026-09-09.md
audit: clients/virtina/output/research/uniqueness-audit-2026-09-09.md
competitors: clients/virtina/output/research/competitor-analysis-2026-09-09.md
---

# Brief: What underwriters actually check before they approve a regulated ecommerce store

## Locked decisions (do not relitigate)

| Field | Value |
|---|---|
| Title / H1 | What underwriters actually check before they approve a regulated ecommerce store |
| Slug | `merchant-account-underwriting-2026` |
| Primary keyword | high risk merchant account approval |
| Format | **Format D (decision-tree / playbook)** |
| Length | 2,500–3,500 (pillar). Target 3,400. |
| Images | 1 featured (1309x500) + 3 body (670x352) |
| CTA target | Page 42417, `/high-risk-ecommerce-migration-payment-gateway-integration/` |

**REJECTED and never to be reintroduced:** the original working title "High-Risk Payment Gateways for Ecommerce: How to Get Approved and Stay Compliant in 2026", its slug `high-risk-payment-gateways-ecommerce-2026`, and its primary keyword "high risk payment gateway". It failed uniqueness checks 1, 2, 3 and 4 against page ID 36749.

---

## Format selection (MUST-FOLLOW-RULES section 11)

**Chosen: Format D, decision-tree / playbook.**

**Reason (one sentence):** getting a regulated store approved and keeping it approved is a genuinely sequenced process with gates at each stage, so the reader should walk phases in order rather than skim a survey.

**Recently overused, therefore skipped:** Format E (contrarian thesis) is used in 3 of the last 10 posts (42491, 42465, 42428) and is **blocked** by the section 11 recency rule. Format B was used recently (42441) and does not suit a threshold-heavy technical guide. Format A was the fallback but loses the phase sequence that is the article's main organising idea. Format D has been used once recently (42413, a migration post on a different cluster), which is inside the limit.

**Format D obligation for the creator:** each body section is a phase, not a chapter. Open each body section by naming the decision the reader is making at that point. End sections 1, 2 and 3 with a one-sentence gate ("If that is not true yet, do not submit the application"). This is what makes it a playbook rather than a listicle.

---

## Uniqueness position

All 5 checks PASS per `uniqueness-audit-2026-09-09.md`. Verified again at brief stage against `published-posts-inventory.md` (310 posts, refreshed 2026-09-09) plus pages 36749 and 42417.

### Cluster saturation statement (restate verbatim, required by section 4c)

> Merchant-account underwriting decisioning and post-approval card-network threshold management for regulated ecommerce merchants, as the rules stand in 2026, with the WooCommerce and Magento implementation layer that determines whether those rules can actually be satisfied.

The broad ecommerce-payments cluster is SATURATED at 9 properties. The sub-niche above is unclaimed, which is the only justification for this post.

---

## Thesis

> Approval is a documents problem you solve once, but staying approved is an engineering problem your store solves every single month, because the card networks now measure your operating posture automatically against published numeric thresholds, and the data your checkout captures decides whether disputes ever enter the count.

## Why this, why now, why us

- **Why this angle:** every page in this SERP is published by a company that sells merchant accounts. All of them are structurally optimistic about approval and vague about the rules that shut you down afterwards. Virtina sells neither accounts nor rates, so Virtina can publish the formula, the exclusions, and the sentence no processor will write: "some applications should not be submitted yet."
- **Why now:** VAMP thresholds took effect 1 June 2025 and the merchant threshold drops from 220 bps to 150 bps on 1 April 2026. PCI DSS v4.x future-dated requirements became mandatory 31 March 2025. Page 36749 was published 2024-09-12 and never modified, so it predates all of it.
- **Why this client:** the compliance outcome is downstream of the platform's data plumbing. Compelling Evidence 3.0 can force an issuer to block a dispute, but only if the store transmitted IP address, customer email, product descriptions, and address at transaction time. That is a WooCommerce and Magento build decision, which is Virtina's territory and nobody else's in this SERP.

## Audience

VP eCommerce, Director of Digital, founders and COOs at regulated-vertical stores between $1M and $50M+ doing $5M-$500M in the B2B case. Verticals: CBD and hemp, firearms and accessories, nutraceuticals, vape and ENDS, subscription and free-trial models, telehealth-adjacent retail.

**What they already know:** what a chargeback is. That "high risk" means more expensive. Their platform, deeply. Core commerce vocabulary.

**What they do not know:** that the VAMP ratio is count-based rather than dollar-based and covers card-not-present transactions only. That merchant-level VAMP thresholds only bite when their acquirer is itself in good standing. That the Mastercard ratio uses last month's sales as the denominator, so falling volume spikes it. That Visa runs its own terminated-merchant file (VMSS) separate from MATCH. That MATCH records the principal owner's name and tax ID, not just the business. That a dispute resolved before it is filed never enters the numerator at all.

**Reading context:** desktop, during work hours, either before submitting an application or immediately after being flagged or terminated. Skim-first. Give them the answer in the first sentence of every section.

## Format and length

- Format: Format D playbook, 8 body H2 phases plus 4 structural sections
- Target length: 3,400 words (hard band 2,500-3,500)
- Reading time: 13-14 minutes
- Mandatory elements by article type: this article is BOTH "how-to / setup guide" AND "comparison", so it needs **a numbered checklist** (section 2) **and** a **comparison table using Template N** (section 4). Plus the standard FAQ.

---

## Structure

Every body H2 below is already phrased as a natural-language question. Do not rewrite them into statements. Structural labels (Introduction, People also ask, Conclusion, Frequently Asked Questions) stay verbatim and are exempt from the question rule.

**Direct-answer discipline:** the first sentence of every body H2 section must answer that H2's question outright. No context-setting, no "before we get into this". Each locked first sentence below is a starting point the creator may tighten, but the answer must still come first.

### Summary block (Template A) — 80 words

States the thesis in three sentences. Must name VAMP, MATCH and VMSS so a skimmer knows within five seconds that this article covers the 2026 rules. No CTA, no links.

### Introduction (Template B, H2 "Introduction") — 160 words

Two paragraphs, max 3 sentences each. Open on the failure the reader is trying to avoid: an approved account that gets pulled six months later. Establish the split that organises the whole article: approval is a documents problem, survival is an engineering problem. State plainly that no independent dataset exists on approval rates or reserve norms and that this article publishes rules rather than rate cards. **No internal links in the introduction.**

### TOC (Template C, H3 "Table of Contents")

One `<li>` per body H2 plus `#people-also-ask`, `#conclusion`, `#faq`. Inline SVG arrow only.

### Section 1 — H2: "What makes an underwriter classify your store as high risk?" — 240 words

**Locked first sentence (direct answer):** "Underwriters classify your store as high risk when your product category, your billing model, or your history makes a future chargeback more likely than the portfolio average."

- Key point: this is Phase 0, posture. It is the shortest section on purpose.
- **Compress, do not expand.** Page 36749 owns the long version of this material. Deliver it as one compact table plus two short paragraphs and move on.
- **Table 1 (Template N markup, 3 columns):** "Risk signal" | "Why underwriters weigh it" | "What you can change before applying". Six rows: product category and MCC; chargeback and refund history; average ticket paired with delivery lag; subscription or free-trial billing; prior terminations and principal history; thin or absent processing history. Caption in 14px grey noting the framing is Virtina's, dated 9 September 2026.
- **Mandatory concession link, used exactly once in the whole article:** link to page 36749 here, in prose, and explicitly hand it the territory. Model sentence: "If you need the long-form breakdown of categories, fee structures and reserve types, our earlier guide to high-risk payment processing covers it, and this article assumes you have read it." Anchor: **high-risk payment processing**.
- H3 (~90 words): "Which risk signals come from your product, and which come from your operations?" Product-side signals are mostly fixed. Operational signals (delivery lag, refund policy visibility, free-trial mechanics) are the ones you can improve before you apply, which is why they are worth the effort.
- H3 (~80 words): "Why aggregator approval is not underwriting." Aggregators board you into a shared account against a published policy list, so there is no individual file to revisit and the only available lever is removal. Use the verified Stripe restricted-business categories (items 44-46) as the evidence: gambling, adult, credit repair, unsafe-claim nutraceuticals and negative-option marketing are prohibited outright, while tobacco, e-liquid, hemp-derived CBD within local THC limits and legal firearms are restricted and need approval. Stripe may be named factually. **Stripe must not be linked.**
- **Overlap guard, important:** post `square-cutoff-seller-action-plan` already argued "you were a sub-merchant on somebody else's merchant ID" at length, and post 42428 already argued "SaaS platforms can deplatform you". Give each idea one sentence maximum here, then pivot to the underwriting file. Do not re-run either argument.
- Gate sentence to close the section.
- Internal link: `selling-firearms-online`, anchor **online firearms sales**.

### Section 2 — H2: "What goes in the document pack, and what is the underwriter reading it for?" — 400 words

**Locked first sentence (direct answer):** "The pack is formation documents, processing history, bank statements, financials and the live site itself, and the underwriter reads all of it for one thing: whether your claims, your category and your operations agree with each other."

- Key point: Phase 1. This is the actionable heart of the front half. The insight is that underwriters are not scoring documents individually, they are checking them against each other and against the live storefront.
- **Numbered checklist required here.** Build it with Template F markup using bold ordinal labels in the `{{BOLD_LABEL}}` slot, for example `<strong>Step 1.</strong>`. Do not introduce an `<ol>` element; Template F is the only approved list pattern. 7 or 8 steps, each one line: formation and ownership documents; principal ID and tax ID; 3-6 months of processing statements and bank statements; product and compliance documentation for the vertical (lab reports, licences, age-gating evidence); the live site with visible refund, cancellation, shipping and contact terms; fulfilment timing evidence matched to average ticket; a written explanation of any prior termination; the MCC you expect to be assigned.
- H3 (~110 words): "What the documents have to agree on." The site's claims must match the requested MCC. Fulfilment timing must match the average ticket. Refund and cancellation terms must be visible without a login. A mismatch between any two of these reads as either sloppiness or misrepresentation, and both are declines.
- H3 (~100 words): "What a MATCH or VMSS screen does to your application." Acquirers screen every applicant against both files before anything else happens. A hit usually ends the application there. Keep this deliberately short here; section 6 is the full treatment. Cross-reference it in one sentence.
- H3 (~90 words): "Why nobody can tell you your approval odds." Say it plainly: there is no neutral dataset on high-risk approval rates, decline rates, reserve norms or underwriting timelines. Every number in circulation is published by a company selling merchant accounts. This honesty is a differentiator against the entire SERP, so give it a real paragraph rather than a hedge.
- **MCC caution (CONDITIONAL source):** the Visa Merchant Data Standards Manual was located but not fetched. Keep MCC content to the verified point that the assigned MCC must match what the site actually sells. The multiple-MCC assignment rule may be stated once as general practice, hedged, with **no attribution to Visa's manual**. Do not build an H3 around MCCs.
- Gate sentence to close.
- **Body image 1 goes here**, after the first paragraph.
- Internal link: `payment-gateway-service-providers`, anchor **payment gateway service providers** (used when distinguishing the gateway from the merchant account).

### Section 3 — H2: "What terms come with an approval, and what should you get in writing?" — 260 words

**Locked first sentence (direct answer):** "An approval arrives with a reserve structure, a monthly volume cap and a settlement schedule, and every one of those is negotiable enough that you should never accept it verbally."

- Key point: Phase 2. Describe the **shapes** of the terms. Publish **zero numbers**.
- Cover reserve structures by type: rolling, upfront, capped. Volume caps and what happens when you exceed one. Settlement timing and its cash-flow consequence.
- **Hard prohibition:** no percentage ranges, no dollar ranges, no day counts, no processing rates. Every published range traces to a single processor's rate card. State this in the section, in one sentence, as the reason you are not quoting one.
- H3 (~90 words): "Which terms you should insist are written into the agreement." Short Template F list: reserve type and release schedule; the exact conditions that trigger a reserve increase; the monthly volume cap and the process for raising it; settlement timing; notice period before termination; who owns the customer card tokens if the relationship ends.
- H3 (~80 words): "What changes after the first six months of clean processing." Clean processing history is the only asset that reliably improves terms, which is why the threshold management in the rest of this article is also a commercial argument, not just a compliance one.
- Gate sentence to close.
- Internal link: `b2b-ecommerce-checkout-best-practices`, anchor **B2B checkout best practices**. (Place in the token-ownership or settlement paragraph, wherever it reads naturally.)

### Section 4 — H2: "Which card network thresholds are you measured against in 2026?" — 470 words

**Locked first sentence (direct answer):** "You are measured against Visa's VAMP ratio and Mastercard's chargeback programs every month, both of them automatically, and from 1 April 2026 the Visa merchant threshold in the US, Canada, EU and AP drops from 220 basis points to 150."

- Key point: Phase 3, and the single most important section in the article. This is differentiator 1 and it is the reason the post exists.
- **This is where the mandatory Template N comparison table goes.** 4 columns, 6 rows.
  - Columns: **"Program"** | **"How the ratio is measured"** | **"Threshold (2026)"** | **"The condition most pages omit"**
  - Rows: Visa VAMP merchant level (AP, Canada, EU, US); Visa VAMP merchant level (LAC); Visa VAMP merchant level (CEMEA); Visa VAMP acquirer portfolio; Mastercard ECM; Mastercard HECM.
  - Caption (14px, `#6e6e6e`): sources are Visa's Acquirer Monitoring Program fact sheet, thresholds effective 1 June 2025 with the merchant step-down on 1 April 2026, and Mastercard ECM/HECM program documentation as published by processors. Data as of 9 September 2026.
- H3 (~130 words): "How is the VAMP ratio actually calculated?" Give the formula in words: the count of TC40 fraud plus TC15 disputes, divided by the count of settled TC05 transactions. Count-based, not dollar-based. Card-not-present VisaNet transactions only, domestic and cross-border. Effective 1 June 2025, advisory period ended 30 September 2025. State the two exclusions here and flag that section 5 is built on them: disputes resolved through pre-dispute solutions are excluded, and TC40 fraud qualified for Compelling Evidence 3.0 is excluded, both subject to data-extract timing.
- H3 (~110 words): "Why two merchants with the same ratio get treated differently." Merchant-level thresholds apply only when the acquirer is not itself Above Standard (>=50 bps) or Excessive (>=70 bps) at portfolio level. This is the conditional that every competitor page omits and it is a genuinely useful thing to know before you pick an acquirer. Say so.
- H3 (~110 words): "Why the Mastercard ratio spikes when your sales fall." The denominator is the prior month's sales transactions, not the current month's. A merchant whose volume drops sees the ratio rise on a shrinking denominator without a single extra chargeback. Exit requires being below ECM thresholds for three consecutive months. Mention the fine ladder in prose only, at the shape level: nothing in month one, USD 1,000 from month two, escalating to USD 100,000 for ECM and USD 200,000 for HECM at month 19 and beyond, with a possible USD 5 issuer recovery assessment per chargeback above 300 for HECM merchants. **Do not reproduce the full seven-tier ladder as a list.**
- **Body image 2 goes here**, after the first paragraph.
- **External link 1 of 2:** Visa Acquirer Monitoring Program fact sheet PDF, `https://corporate.visa.com/content/dam/VCOM/corporate/visa-perspectives/security-and-trust/documents/visa-acquirer-monitoring-program-fact-sheet-2025.pdf`, Template M with `target="_blank" rel="noopener noreferrer"`. Anchor: **Visa Acquirer Monitoring Program fact sheet**.
- **Do not use:** the "$8 per fraudulent or disputed transaction" VAMP fee. It is absent from Visa's own fact sheet. Do not present any VAMP fine or fee as a Visa-published figure.
- **Do not use:** the "nearly half of acquirers improved" / "VAMP ratio declined 45% quarter over quarter" claim. Snippet-only, unfetched.

### Section 5 — H2: "How do you keep the ratio down without refunding every complaint?" — 380 words

**Locked first sentence (direct answer):** "You keep the ratio down by stopping disputes before they are filed, because a dispute resolved through a pre-dispute solution never enters the VAMP numerator at all."

- Key point: Phase 4, and this is differentiator 4. Lead with the exclusion mechanic. It is the most valuable idea in the article and no competitor page contains it.
- Cover: Verifi is Visa's solution, Ethoca is Mastercard's. Verifi provides Order Insight and Rapid Dispute Resolution. Disputes resolved through RDR do not count toward dispute rates, and Ethoca Alerts help merchants exit ECM, HECM and EFM. RDR handles full-amount disputes on non-refunded transactions only, with no partial resolution. Both apply only to chargebacks initiated after enrolment, so enrolling after you are flagged does not fix the month you are already in.
- H3 (~130 words): "How does Compelling Evidence 3.0 block a dispute before it is filed?" If at least two prior transactions exist with complete product descriptions, matching IP addresses, and at least one matching email or delivery address, the issuer must block the dispute. It is never filed, so there is no fee and no ratio impact. It applies to Visa reason code 10.4, other fraud in a card-absent environment, which is the first-party misuse case. State the required fields explicitly: IP address, customer email address, product descriptions, and shipping or customer address. End by naming the dependency and pointing forward to section 7.
- H3 (~110 words): "Where representment and 3-D Secure 2 actually help." Representment recovers revenue but a dispute already filed is already counted, so representment protects the money and not the ratio. That distinction is worth stating explicitly because most merchants conflate them. **3-D Secure 2 must be covered qualitatively only.** EMVCo and Visa liability-shift documentation was not fetched, so do not state liability-shift rules as fact.
- Internal link: `woocommerce-checkout-not-working-agency`, anchor **WooCommerce checkout fixes** (place in the paragraph about checkout data capture failing silently).

### Section 6 — H2: "What puts you on MATCH or VMSS, and what happens after that?" — 380 words

**Locked first sentence (direct answer):** "Mastercard's MATCH and Visa's VMSS are terminated-merchant files that acquirers must screen every applicant against, listings last five years, and only the acquirer that created the listing can remove one."

- Key point: Phase 5, the failure state. This is differentiators 2 and 3 combined, and it is the section most likely to change reader behaviour.
- **Sourcing caution (CONDITIONAL):** Mastercard's own SPME manual returned HTTP 403 and could not be fetched. Every MATCH detail here rests on Stripe's processor documentation, which is a good source but a single one. Attribute once as "as processors document the rules" or similar. **Never write "Mastercard publishes" or "according to Mastercard".** Stripe is not to be linked.
- Cover: both networks operate parallel files. Five-year listings on both. Only the listing acquirer can remove. Removal in two circumstances only: the acquirer listed you in error, or the listing was Reason Code 12 for PCI DSS non-compliance and compliance has since been verified. An acquirer must add a qualifying merchant within one working day of termination. Closing the account does not prevent a listing. MATCH records the principal owner's name, address, phone and tax ID, so the listing follows the person to the next venture.
- **Use the Stripe breakdown: 11 qualitative reason codes plus 2 quantitative codes.** Do not write "14 MATCH reason codes"; affiliate pages get this wrong.
- H3 (~120 words): "Which triggers fire automatically, without anyone reviewing your case?" MATCH Reason Code 04, excessive chargebacks: monthly Mastercard chargebacks above 1% of monthly Mastercard sales transactions AND totalling USD 5,000 or more, both in the same month, with no minimum chargeback count. MATCH Reason Code 05, excessive fraud: monthly fraud-to-sales dollar volume at 8% or more, with 10 or more fraudulent transactions totalling USD 5,000 or more, all in one calendar month. VMSS Code 21, excessive fraud: USD 250,000 in fraud AND 180 bps fraud-to-sales. VMSS Code 22, excessive disputes: 1,000 disputes AND 180 bps dispute-to-sales. VMSS uses 13 qualitative reason codes, numbered 23 to 35.
- H3 (~100 words): "Why winning the chargebacks afterwards does not undo it." Qualification is measured in the month it happens. Reversing or winning the disputes later does not remove the qualification, and neither does closing the account. This is why the prevention mechanics in section 5 matter more than the dispute-response process most merchants invest in.
- Internal link: `shopify-vape-store-woocommerce-migration`, anchor **vape store WooCommerce migration**.

### Section 7 — H2: "What has to be true in WooCommerce or Magento for any of this to work?" — 420 words

**Locked first sentence (direct answer):** "Your store has to transmit the transaction fields the dispute rules depend on, route to a merchant account you actually control, and keep your payment page inside PCI DSS scope, and none of that is default behaviour in WooCommerce or Magento."

- Key point: Phase 6, and this is differentiator 5. This is the half of the topic that does not exist anywhere in the SERP. Virtina's authority section.
- **Body image 3 goes here**, after the first paragraph.
- H3 (~140 words): "Which transaction fields does your checkout have to send?" Tie directly back to CE 3.0: IP address, customer email, product descriptions, and shipping or customer address must reach the processor at transaction time, not just sit in the order record. If the store is not passing them, the merchant's dispute-prevention tooling underperforms silently and nobody finds out until the ratio moves. Note that product description quality matters, because a generic SKU string is not a product description. This is a build task, not a plugin setting.
- H3 (~140 words): "Gateway, merchant account, and multi-MID routing." Distinguish the gateway from the merchant account plainly, because merchants conflate them constantly. Then cover routing across more than one MID: separating product lines by MCC, isolating a subscription book from one-off sales, and keeping one account's ratio from contaminating another. Cover the integration paths honestly: Authorize.Net Payments for WooCommerce is an official extension built by the Authorize.net team with tokenised storage via Customer Information Manager, and Authorize.Net also has a first-party module on the Adobe Commerce marketplace. The WordPress.org "WP NMI Payment Gateway for WooCommerce" plugin states it is not affiliated with or endorsed by NMI, WooCommerce or Automattic, which is a maintenance risk most regulated merchants have not priced.
  - **CONDITIONAL, hedge or omit:** the NMI Gateway Emulator accepting the Authorize.Net AIM/SIM integration format is snippet-sourced only. If kept, write it as "NMI is commonly reached through an Authorize.Net compatible integration path rather than a first-party extension" and flag it for the publisher to verify. If verification fails, cut the sentence. Do not present it as a documented NMI feature.
  - **Do not claim Magento and WooCommerce have equivalent high-risk gateway coverage.** First-party NMI and USAePay Magento 2 modules were not confirmed.
- H3 (~140 words): "What PCI DSS 4.x changed for your payment page." PCI DSS v4.x introduced 64 new requirements, 51 of them future-dated and mandatory from 31 March 2025. Requirements 6.4.3 and 11.6.1 require ecommerce merchants to authorise, integrity-check and monitor payment page scripts and to prevent unauthorised changes to payment pages, targeting e-skimming. They were removed from SAQ A but remain in the standard for other SAQ types where payment functions are not fully outsourced. Frame hosted checkout as a scope decision with a named consequence rather than a generic convenience. v4.0.1 did not move the date.
- **External link 2 of 2:** PCI Security Standards Council blog post on the future-dated requirements. **The exact URL is not recorded in the research file.** The creator or publisher must re-fetch and confirm the live URL before linking. If it cannot be confirmed, cite the PCI SSC in plain text and ship with one external link. Never guess the URL.
- **Commercial CTA lives here, in body prose**, because internal links are banned from the conclusion. Link page 42417, anchor **high-risk gateway integration**. One sentence, no pitch language, no "reach out". Frame as: this is the work, and Virtina does it.
- Internal links in this section: `best-woocommerce-payment-gateways` anchor **WooCommerce payment gateways**; `platforms/magento-development-services` anchor **Magento development services**; `woocommerce-security` anchor **WooCommerce security**; plus the 42417 CTA above.

### People also ask (Template H, H2 "People also ask") — 160 words

Three questions, each answered in 2-3 sentences, direct answer first, max 3 sentences per paragraph.

1. **How long does high-risk merchant account approval take?** Answer honestly: no independent data exists, and every published range comes from a company selling accounts. Then give what actually drives it: completeness of the pack, MATCH and VMSS screening results, and whether the site's claims match the requested MCC.
2. **Can you get approved after being listed on MATCH?** Answer: usually not through normal channels, because only the acquirer that created the listing can remove it and listings run five years. Name the two removal circumstances.
3. **What chargeback ratio gets a merchant account shut down?** Answer: it depends which network is measuring you. Give the VAMP merchant threshold of 150 bps from 1 April 2026 paired with the 1,500 monthly count floor, and Mastercard ECM at 100 chargebacks and 1.50%.

### Conclusion (Template I, H2 "Conclusion") — 130 words

Two paragraphs, white text on `#00d5c0`. Restate the split: documents get you approved, engineering keeps you approved. Name the one thing to do first, which is checking whether the store is transmitting the CE 3.0 fields today. **No internal links, no external links.** Never open with "In conclusion".

### FAQ (Template J, H2 "Frequently Asked Questions") — 320 words

Eight questions, each answered in 2-4 sentences, max 3 sentences per paragraph.

1. What is the difference between a payment gateway and a merchant account?
2. How is the VAMP ratio calculated?
3. Does winning a chargeback remove it from your ratio?
4. What is VMSS, and how is it different from MATCH?
5. Do PCI DSS requirements 6.4.3 and 11.6.1 apply if you use a hosted checkout page?
6. What transaction data does Compelling Evidence 3.0 need?
7. Can one WooCommerce store run more than one merchant account?
8. What happens to your Mastercard chargeback ratio if your sales volume drops?

---

## Word budget

| Section | Words |
|---|---|
| Summary block | 80 |
| Introduction | 160 |
| S1 Risk classification | 240 |
| S2 Document pack | 400 |
| S3 Approval terms | 260 |
| S4 2026 thresholds | 470 |
| S5 Keeping the ratio down | 380 |
| S6 MATCH and VMSS | 380 |
| S7 Platform layer | 420 |
| People also ask | 160 |
| Conclusion | 130 |
| FAQ | 320 |
| **Total** | **3,400** |

Table and caption text is excluded from the counts above. Hard band remains 2,500-3,500.

**Heading density check:** 8 body H2s plus 17 H3s plus 4 structural H2s. At 3,400 words that is roughly one heading every 120-140 words, comfortably inside the 150-300 rule. Minimum 6 H3s is exceeded by a wide margin. Every H2 over 200 words has at least one H3.

---

## Stats the creator MAY use (VERIFIED only)

All items below are drawn from the VERIFIED list in the research file. Nothing outside this list may appear as a fact.

**Visa VAMP** (Visa fact sheet PDF, fetched 2026-09-09): consolidation of VAMP, VFMP and VDMP; thresholds effective 1 June 2025; advisory period ended 30 September 2025; ratio = count of (TC40 fraud + TC15 disputes) / count of settled TC05 transactions; count-based not dollar-based; card-not-present VisaNet only; excludes pre-dispute-resolved disputes and CE 3.0 qualified TC40 fraud; acquirer portfolio Above Standard >=50 bps and Excessive >=70 bps; merchant thresholds AP/Canada/EU/US >=220 bps and >=1,500 count, LAC >=150 bps and >=1,500, CEMEA >=220 bps and >=150 count and >=USD 75,000; AP/Canada/EU/US merchant threshold drops to >=150 bps on 1 April 2026; merchant thresholds apply only when the acquirer is not itself Above Standard or Excessive; enumeration ratio >=2000 bps and enumeration transaction count >=300,000.

**PCI DSS v4.x** (PCI SSC blog, both posts fetched): 64 new requirements of which 51 were future-dated, mandatory 31 March 2025; requirements 6.4.3 and 11.6.1 on payment page script authorisation, integrity and change prevention, targeting e-skimming; both removed from SAQ A but retained in the standard for other SAQ types; v4.0.1 did not change the date.

**MATCH and VMSS** (Stripe processor documentation, fetched): both files exist and are screened by acquirers; five-year listings; only the listing acquirer can remove; two removal circumstances; one working day to add; 11 qualitative plus 2 quantitative MATCH reason codes; Code 04 and Code 05 triggers as specified in section 6 above; winning the chargebacks does not undo qualification; closing the account does not prevent listing; principal owner's name, address, phone and tax ID recorded; VMSS has 13 qualitative codes numbered 23-35; VMSS Code 21 and Code 22 triggers as specified.

**Mastercard ECM/HECM** (Braintree developer documentation, fetched): ECM at 100-299 chargebacks and 1.50%-2.99%; HECM at 300+ and 3.00%+; lagged denominator using the prior month's sales; exit requires three consecutive months below ECM thresholds; fine ladder from USD 0 in month 1 to USD 100,000 / 200,000 at month 19+; possible USD 5 issuer recovery assessment per chargeback above 300 for HECM.

**Dispute prevention** (Stripe documentation, fetched): Verifi is Visa, Ethoca is Mastercard; Order Insight and RDR; RDR-resolved disputes do not count toward dispute rates; Ethoca Alerts help exit ECM, HECM and EFM; RDR is full-amount only on non-refunded transactions with no partial resolution; both apply only to chargebacks initiated after enrolment; CE 3.0 two-prior-transaction rule with matching IP and matching email or delivery address forces the issuer to block; CE 3.0 applies to Visa reason code 10.4.

**Aggregator policy** (stripe.com/legal/restricted-businesses, fetched, updated 2026-05-13): prohibited and restricted category lists as summarised in section 1 above.

**Platform** (WooCommerce marketplace, wordpress.org, Adobe Commerce marketplace): Authorize.net Payments for WooCommerce is an official extension by the Authorize.net team with CIM tokenisation; Authorize.Net has a first-party Adobe Commerce module; the WordPress.org WP NMI plugin states it is not affiliated with or endorsed by NMI, WooCommerce or Automattic.

## CONDITIONAL — state cautiously or omit

The creator must not present any of these three as hard fact.

| Item | Status | Instruction |
|---|---|---|
| All MATCH rule detail | Mastercard SPME manual returned HTTP 403; single-sourced to Stripe's processor documentation | State the rules, attribute once as "as processors document the rules". Never write "according to Mastercard" or "Mastercard publishes". |
| MCC multiple-assignment rule | Visa Merchant Data Standards Manual located but not fetched | One hedged sentence maximum, framed as general practice. No attribution to the Visa manual. Do not build a section around MCCs. |
| NMI reachable via Authorize.Net AIM/SIM emulation | Search snippet only, NMI integration portal not fetched | Hedge as "commonly reached through an Authorize.Net compatible integration path", flag for publisher verification, cut if unverified. |

## Must NOT include

- **The rejected title, slug or primary keyword.** Nothing built on "high risk payment gateway" as the head term; that belongs to service page 42417.
- **Any processing rate, reserve percentage, settlement day count, or underwriting timeline.** No "2.5%-5%", no "5%-20% held 90-180 days", no "7-10 business days", no "2.9%-9% by vertical", no "0%-15% rolling reserve", no "1-3 day settlement". All of it traces to single processor rate cards. Say plainly that no independent data exists instead.
- **The "$8 per fraudulent or disputed transaction" VAMP fee.** Not in Visa's fact sheet.
- **"14 MATCH reason codes."** Use 11 qualitative plus 2 quantitative.
- **The "45% quarter over quarter VAMP decline" claim.** Snippet-only, unfetched.
- **FTC consumer fraud figures** (3m reports, $15.9bn losses). Real numbers, wrong context, would mislead.
- **NMI volume statistics** ($502bn, 6.5bn transactions, 1.2m merchants) and **USAePay pricing**. Supplier scale claims and unsourced pricing.
- **"99% approval rate" or "approval within 24 hours"** from any source.
- **A flat "1.5% VAMP threshold" framing.** It is regional, paired with a count floor, and conditional on the acquirer's standing.
- **Any link to a processor or affiliate domain:** paymentcloud, durango, hostmerchant, soarpayments, segpay, finix, givepayments, paycompass, paymentnerds, technologyadvice, thefinrate, emerchantbroker, corepay, chargeflow. **Stripe may be named factually but must not be linked.** No shopify.com, no bigcommerce.com.
- **Named high-risk processor recommendations.** Describe the category and what to ask for.
- **Crypto or Web3 payment routing.** Brand file excludes it, and PayCompass's crypto detour is one of the weaknesses we are beating.
- **A full-length rerun of "what makes a business high-risk."** Page 36749 owns it. Table plus two paragraphs, then move on.
- **A rerun of the Square post's "you are a sub-merchant, own your MID" argument** or **post 42428's "SaaS platforms can deplatform you" argument.** One sentence each, maximum.
- **Any 3-D Secure 2 liability-shift claim.** EMVCo and Visa sources not fetched. Qualitative coverage only.
- **Any claim of Magento and WooCommerce parity on high-risk gateway support.**
- **Any invented author byline.** Brand voice ("we") or a real name supplied by the client only.
- **Em dashes in any form** (—, `&mdash;`, `&#8212;`, `&#x2014;`), semicolons, exclamation marks.
- **Banned words:** delve, leverage, navigate as a verb, realm, landscape, ecosystem, revolutionary, game-changing, cutting-edge, best-in-class, transform your, unlock value, synergize, "in today's fast-paced world", "it's important to note", "in conclusion", "reach out".

---

## Internal links (9 required, 1 optional, body sections only)

All 23 candidates in the research file were REST-verified as `status: publish` on 2026-09-09. Anchors below are clean 2-5 word noun phrases, no leading articles, no gerunds, each used exactly once.

| # | URL | Anchor | Section |
|---|---|---|---|
| 1 | https://virtina.com/high-risk-payment-processing-ecommerce-businesses/ | high-risk payment processing | S1 (mandatory concession link, once only) |
| 2 | https://virtina.com/selling-firearms-online/ | online firearms sales | S1 |
| 3 | https://virtina.com/payment-gateway-service-providers/ | payment gateway service providers | S2 |
| 4 | https://virtina.com/b2b-ecommerce-checkout-best-practices/ | B2B checkout best practices | S3 |
| 5 | https://virtina.com/woocommerce-checkout-not-working-agency/ | WooCommerce checkout fixes | S5 |
| 6 | https://virtina.com/shopify-vape-store-woocommerce-migration/ | vape store WooCommerce migration | S6 |
| 7 | https://virtina.com/best-woocommerce-payment-gateways/ | WooCommerce payment gateways | S7 |
| 8 | https://virtina.com/platforms/magento-development-services/ | Magento development services | S7 |
| 9 | https://virtina.com/woocommerce-security/ | WooCommerce security | S7 (PCI paragraph) |
| 10 | https://virtina.com/high-risk-ecommerce-migration-payment-gateway-integration/ | high-risk gateway integration | S7 (**commercial CTA**) |

Optional 11th if a natural home appears, otherwise skip: `https://virtina.com/cbd-ecommerce-how-to-make-the-most-out-of-the-young-market/`, anchor **CBD ecommerce market**. **Do not exceed 10 internal links total.**

Template L markup, `style="outline: none;"`, no `target` attribute. Never link `/contact/` (301) or any of the verified-dead paths in section 6 of MUST-FOLLOW-RULES.

## External links (maximum 2)

1. **Visa Acquirer Monitoring Program fact sheet PDF** — `https://corporate.visa.com/content/dam/VCOM/corporate/visa-perspectives/security-and-trust/documents/visa-acquirer-monitoring-program-fact-sheet-2025.pdf`, in S4, anchor **Visa Acquirer Monitoring Program fact sheet**.
2. **PCI Security Standards Council blog on future-dated requirements** — in S7. **URL not recorded in the research file. Re-fetch and confirm before linking. If it cannot be confirmed, cite PCI SSC in plain text and ship with one external link.**

Both use Template M with `target="_blank" rel="noopener noreferrer"`. Hard cap is 2. Stripe, Mastercard, WooCommerce.com and wordpress.org may be named in prose but not linked.

---

## Meta

- **Meta title (52 chars):** `High-risk merchant account approval in 2026 | Virtina`
- **Meta description (160 chars):** `Underwriters approve regulated stores on evidence, not optimism. See the 2026 VAMP and MATCH thresholds, and the checkout data that keeps your account approved.`
- **Focus keyword:** high risk merchant account approval

Alternate meta title if the client prefers the editorial framing (58 chars): `What underwriters check before approving a store | Virtina`

## Semantic terms (cover at least 15 naturally in body prose)

Required 15: MCC code, chargeback ratio, merchant account underwriting, rolling reserve, MATCH list, VMSS, VAMP ratio, representment, PCI DSS 4.0, payment aggregator, MID (merchant ID), acquirer, dispute rate, prohibited business list, 3-D Secure 2.

Optional 2 if they read naturally: KYC/KYB, sponsor bank.

**Dropped deliberately:** "interchange". The article publishes no rate content, so the term would read forced.

---

## Images

No Pexels key is available, so these are specifications for a later manual fill, not sourcing instructions. Every image must be a business, office, warehouse, data or ecommerce scene. No nature, no abstract, no stock-photo filler.

| Slot | Size | What it should depict | Draft alt text |
|---|---|---|---|
| Featured | 1309x500 | A small finance or ops team at a desk reviewing printed statements and a laptop, in a real office. Application-review scene, not a handshake. | Ecommerce finance team reviewing merchant account underwriting documents before submitting a high-risk payment application. (122 chars) |
| Body 1 (S2) | 670x352 | Desk close-up: printed bank and processing statements, folders, an open laptop showing a spreadsheet. Documents, not people. | Printed processing statements and bank records assembled for a high-risk merchant account application review. (108 chars) |
| Body 2 (S4) | 670x352 | An analyst at a monitor reading a dashboard with charts and numbers. Data-review scene. | Payments analyst tracking a monthly chargeback ratio and dispute counts against 2026 card network thresholds. (109 chars) |
| Body 3 (S7) | 670x352 | Two developers at computers reviewing code or a checkout configuration screen. | Developers configuring WooCommerce checkout fields and gateway routing for a regulated ecommerce merchant account. (113 chars) |

All body images 670x352, JPEG q82, under 200 KB, wrapped in Template G, `src` beginning `https://virtina.com/wp-content/uploads/`, `featured_media` set to a real media ID.

---

## Where the research is too thin to build on

Flagged for the creator so nothing gets padded out:

1. **MCCs.** The Visa Merchant Data Standards Manual was not fetched. Two hedged sentences maximum. Do not give MCCs an H3 or a table row beyond the risk-signal row already planned.
2. **Approval odds, timelines and reserve norms.** No neutral dataset exists. Section 3 must be built on term shapes and negotiation asks rather than numbers. Turn the absence into a paragraph, not a gap.
3. **MATCH.** Single-sourced. Do not stack additional MATCH detail beyond what the research file verifies.
4. **3-D Secure 2.** One qualitative paragraph. Nothing on liability shift.
5. **Magento-specific high-risk gateway support.** Authorize.Net's first-party Adobe Commerce module is confirmed. Nothing else is. Do not fill the gap with inference.

## Open questions for the creator

- The exact ordering of the two H3s inside section 1, and whether the aggregator contrast reads better before or after the risk-signal split.
- Whether the ECM fine ladder belongs in section 4 prose or in an FAQ answer. Either is acceptable; the full seven-tier list is not.
- The specific wording of the concession sentence handing territory to page 36749, provided it is unambiguous and appears exactly once.
- Which of the two optional semantic terms to include.
- Whether to add the optional 11th internal link, staying at or under 10 total.

## Flag for the orchestrator (not for the article)

Page 36749's WordPress `title` field reads "Ecommerce Warranty Services: A Comprehensive Guide for eCommerce Businesses" while its rendered H1 is "High-Risk Payment Processing for eCommerce Businesses". This is a live site data bug and the reason the page never surfaced in title-based inventory checks. Worth raising with the client separately.

## Post-draft checks outstanding

- 8-gram verbatim phrasing check against all live and draft Virtina content, **including page 36749**, which is the highest-collision source. Strip `<style>` blocks and inline `style=` attributes first.
- Full section 9 pre-publish checklist before any PUT.
