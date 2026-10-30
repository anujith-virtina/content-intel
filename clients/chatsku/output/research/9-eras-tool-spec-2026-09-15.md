---
title: "9 Eras of B2B Catalogs - interactive tool spec (source of truth)"
client: chatsku
date: 2026-09-15
topic: 9 Eras interactive self-assessment, Era 07 deep dive
audience: Ops and sales leaders
stage: research
slug: 9-eras-tool-spec
---

# Source tool

- **URL**: https://chatsku.com/9-eras-of-b2b-catalogs/ (WP page ID 1940, live, verified 200 on 2026-09-15)
- **Type**: interactive self-assessment. Dropdown "Select an era" -> "This is us" button -> email-gated era report (WPForms ID 1959).
- **Page hook**: "Every catalog sits in an era. Find yours."
- **Sub-hook**: "Nine eras separate a mailed paper catalog from a system that sells to software. Each one is scored here on the same five measures, so you can read down the column and see exactly where your business stops being able to answer."
- **9pm framing on page**: "A buyer opens your site needing a price and a compatibility answer on one specific part. Can they get it without emailing your team and waiting until morning?"
- **Closing block**: "The work that makes you answerable is the work that makes you *buyable*." Era 08 called out as "the one worth watching."
- **Page CTAs**: `/demo/` (Book a live demo) and `/maturity-calculator/` (Score your catalog maturity).
- **Page already links to**: `/b2b-commerce-evolution/` ("the B2B commerce evolution breakdown").

## The five measures (verbatim row labels from the tool)

1. Time to an answer
2. Who does the answering
3. Price visibility
4. At 9pm on a Tuesday
5. Machine-readability flag: `Not machine-readable` / `Partly machine-readable` / `Machine-readable`

## All nine eras (verbatim from the tool's ERAS array)

| Era | Name | Years | One-liner | Machine-readable |
|---|---|---|---|---|
| 01 | Paper Catalog | 1950 - 1990 | Your product data lives on paper, in someone else's filing cabinet. | Not |
| 02 | PDF / Digital Catalog | 1995 - 2005 | The file downloads in a second. The answer still takes a day. | Not |
| 03 | HTML Catalog + Basic RFQ | 2002 - 2012 | Products are browsable. Anything specific becomes a ticket. | Not |
| 04 | Early B2B Portal | 2008 - 2018 | Fast for the accounts you already won. Closed to everyone else. | Not |
| 05 | B2B eCommerce Platform | 2013 - 2022 | They can buy from you. They still cannot ask you anything. | Not |
| 06 | AI Customer Service Chat | 2018 - 2024 | A chat window that has never seen your product data. | Not |
| 07 | AI-Enabled ChatCommerce | 2025 - 2028 | Your catalog answers in its own words, down to the spec. | Partly |
| 08 | Agentic Commerce | 2026 - 2028 | The thing on the other side is software, and software does not browse. | Yes |
| 09 | Autonomous Agentic Commerce | 2028 - 2030 | Reordering happens without anyone opening a browser. | Yes |

## ERA 07 - full verbatim row data (the subject of this article)

**Name**: AI-Enabled ChatCommerce
**Years**: 2025 - 2028
**Headline**: "Your catalog answers in its own words, down to the spec."
**Machine-readability**: Partly machine-readable

| Measure | Era 07 answer (verbatim) |
|---|---|
| Time to an answer | Seconds. |
| Who does the answering | The catalog itself. |
| Price visibility | Tier-aware, mid-conversation. |
| At 9pm on a Tuesday | No difference between 9pm and 9am. |

**Closing line (verbatim)**: "The buyer describes the application instead of guessing a part number. Back comes the matching SKUs, the spec that decides it, the price at their volume, and a quote they can forward."

## Adjacent eras, for contrast in the article

- **Era 06 (AI Customer Service Chat)** — the era most sellers mistake for Era 07. Verbatim: "It is trained on policies, hours, and shipping. Ask about torque ratings and it collects an email address instead." Rows: "Instant, then a handoff." / "A script, then a person tomorrow." / "Out of scope for the bot." / "It replies. It does not answer."
- **Era 05 (B2B eCommerce Platform)** — where most well-funded sellers actually sit. Verbatim: "Search returns matches for the words a buyer typed. It cannot confirm whether the part suits the application they are actually working on." Rows: "Immediate, if the SKU is already known." / "Filters and a search box." / "Tiered and visible." / "Checkout works fine."
- **Era 08 (Agentic Commerce)** — what Era 07 work unlocks. Verbatim: "An agent shortlists the suppliers it can query. A catalog it cannot parse is not rejected on merit, it is simply never considered."

## Why Era 07 is only *partly* machine-readable (the article's most useful tension)

Era 07 scores `part`, not `yes`, on the tool's fifth measure. That is the single most interesting fact on the page and no existing ChatSKU post explains it. A conversational layer answers a human in seconds but does not, by itself, make the underlying catalog queryable by another machine. That gap is exactly what Era 08 requires. This is the article's spine.
