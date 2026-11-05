---
title: How to set up customer-specific pricing in a B2B store without breaking your catalog
client: virtina
date: 2026-11-02
topic: Guest post for Elogic, B2B customer-specific pricing
audience: Ecommerce owners and teams running or planning a B2B online store
stage: draft
slug: b2b-customer-specific-pricing
---

# How to set up customer-specific pricing in a B2B store without breaking your catalog

Two buyers order the same part on the same day. One pays the list price. The other pays a contract rate agreed last spring. A third gets a volume tier.

In a retail store, that sounds like a bug. In B2B, it's Tuesday.

Customer-specific pricing is one of the first things a B2B store has to get right. It's also one of the easiest to get wrong. A wrong price doesn't just annoy a buyer. It can cost margin, break trust, or send a good account back to email and phone orders.

This guide walks through how to set it up in a calm, testable way. You'll see which pricing models exist, where prices should live, how to test them, and how to roll the whole thing out without a big-bang launch.

## Why doesn't one price list work for B2B?

Retail pricing is simple. One product, one price, and the same price for everyone.

B2B pricing grows from relationships. A distributor who buys every month gets a better rate than a first-time buyer. A key account signs a contract with fixed prices for a year. A new customer gets an introductory tier.

Those rules usually live in three places. Some sit in the ERP. Some sit in spreadsheets. Many sit in the heads of your sales reps.

An online store has to bring those rules into one place. If it can't, buyers see the wrong price, or your team ends up quoting by hand anyway.

## What pricing models should you know about?

Most B2B stores mix a few models. It helps to name them clearly before you build anything.

**Customer-specific price lists.** One account or group gets its own price for each product. This is common with contract customers.

**Tiered or volume pricing.** The price drops as the quantity goes up. A buyer sees a different unit price at 10, 100, and 1,000 units.

**Group or role-based pricing.** Customers are placed in groups, such as distributor, reseller, or wholesale. Each group gets a set discount or price list.

**Quote-based pricing.** Some items have no fixed price. The buyer requests a quote, and someone on your team answers it.

You don't have to use all four. Many stores start with groups and tiers, then add contract lists for the biggest accounts.

## How do you map your pricing rules first?

Before you touch the store, write the rules down. This step feels slow, and it saves the most time later.

Start with a simple table. For each customer type, list how its price is set. Note where the data lives today and who owns it.

Then ask a few direct questions:

- Which accounts have contract prices, and when do those contracts end?
- Which products have volume tiers, and where do the tiers start and stop?
- Do any customers get a percentage discount off list price instead of a fixed price?
- Who approves a price change, and how fast does it need to reach the store?

Expect surprises. Teams often find two spreadsheets that disagree. Fix that now, not after launch.

## Where should the prices live?

This is the most important design choice. Your store needs a single source of truth for prices.

There are two common setups.

**The ERP owns prices.** The store reads prices from your ERP, either live or on a schedule. This keeps one version of the truth. The trade-off is speed. A live lookup adds load and delay, so test it with a large catalog.

**The store owns prices.** You load price lists into the store and update them there. This is fast for buyers. The trade-off is drift. If someone changes a price in the ERP and forgets the store, the two disagree.

For most mid-size catalogs, a scheduled sync works well. Prices update every few minutes or hours. Buyers get fast pages, and the ERP stays in charge.

Whichever you pick, decide who fixes a mismatch and how they find it. A small report that lists products where store and ERP prices differ is worth building early.

## Should buyers see prices before they log in?

There's no single right answer. It depends on your market and your sales process.

You can show public list prices to everyone. This helps search and gives new buyers a clear starting point. The risk is that existing customers expect their own price and may feel confused.

You can hide prices until login. This protects negotiated rates. The risk is that new visitors can't compare you with others, and search pages may have less to show.

A middle path is to show a "starting from" price publicly and the full customer price after login. Many stores land here.

Whatever you choose, be consistent. A buyer who sees one price on the product page and another in the cart loses trust fast.

## How do quotes fit in?

Not every item should have a fixed price online. Custom parts, large orders, and special terms often need a human.

A simple split works well. Standard items get an instant price. Custom or large orders go to a quote request, by form or chat. Your team answers the request, and the buyer can accept it online.

This keeps the easy orders fast and the hard orders accurate. It also gives your sales team a clear list of requests instead of scattered emails.

## How do you test customer-specific pricing?

Test with real accounts before real buyers see anything. Pick three customers who each use a different pricing rule. For each one, check these things:

- The product page shows the right price when they log in.
- The price changes correctly as the quantity crosses each tier.
- The cart and checkout show the same price as the product page.
- The order sent to your ERP carries the same price.
- A price that has expired no longer applies.

Then test the awkward cases. What happens when two rules overlap, such as a contract price and a group discount? What happens with a new customer who has no price list yet? What happens when a price is missing?

Decide ahead of time which rule wins. A written rule order, such as contract price first, then tier, then group, then list, saves many arguments.

## What mistakes should you avoid?

**Building every rule on day one.** Start with the rules that cover most of your revenue. Add the odd ones later.

**Letting two systems own the same price.** Pick one owner and keep it.

**Skipping the price-mismatch check.** Small differences between the store and ERP add up and erode trust.

**Forgetting expiry dates.** Contract prices end. Build in start and end dates so old prices don't linger.

**Ignoring the sales team.** Your reps know the exceptions. Bring them in early, and train them before launch so they see the store as help, not a threat.

## How should you roll it out?

Don't switch everyone on at once. A phased rollout keeps each step small enough to test.

1. Map your buyers, products, and pricing rules.
2. Launch a pilot with a few key accounts.
3. Add quotes, reorders, and integrations in phases.
4. Train the sales team and measure adoption.

Picture a manufacturer with 4,000 parts and 300 active accounts. This is only an illustration. It could start with twenty large accounts, move routine reorders online first, and keep custom parts with the sales team. Each phase would teach the team something before the next one begins.

If you want the wider plan around features, platforms, and ERP integration, the [B2B ecommerce development guide for manufacturers](https://virtina.com/b2b-ecommerce-development-guide-manufacturers/) covers it in more detail.

## What should you measure after launch?

Pricing works when it's accurate and when buyers trust it. Watch a few simple numbers:

- How many orders now come through the store instead of email or phone?
- How many price complaints or corrections reach support each week?
- How long does a quote take from request to answer?
- How often do repeat buyers reorder online?

If complaints fall and online orders rise, your pricing setup is working.

## What's the takeaway?

Customer-specific pricing isn't a feature you switch on. It's a set of business rules that you bring into one clear system.

Write the rules down. Pick one source of truth. Test with real accounts. Roll out in phases.

Do that, and your store can handle the buyer on list price, the contract customer, and the volume buyer, all on the same Tuesday.

---

## Production notes (not for publication)

**Target:** Elogic (elogic.co/write-for-us). Free, no stated ban on AI-assisted drafting, but the author must review and edit this in their own voice before sending. Needs 1,500+ words, conversational tone, headings, short paragraphs, images of at least 580 px sent as separate attachments. Send as a Google Doc to write@elogic.co only after Elogic approves the idea.

**Word count:** about 1,650.

**Links:** exactly 1 self-serving link in the body (guide, verified HTTP 200 on 2026-11-02). Bio may carry 1 link. No outside links yet. NEEDS: 1 or 2 verified outside resources if the author wants them (guessed Adobe and WooCommerce doc URLs returned 404, so none were used).

**Claims:** no statistics. The 4,000-parts and 300-accounts example is labelled an illustration and is taken from the live guide. Avoid adding Adobe Commerce or WooCommerce feature claims without checking their current docs.

**Author bio (needs approval):** Gigi JK is the Founder of Virtina, an eCommerce partner for B2B and B2C brands. Founded in 2012, Virtina covers strategy, platform selection, development, migration, integrations, and performance work. Link: https://virtina.com

**Images needed (3, at least 580 px wide):**
1. A simple diagram of the price rule order: contract, tier, group, list.
2. A two-column comparison, ERP owns prices versus store owns prices.
3. A rollout timeline of the four phases.

**Uniqueness:** do not publish this text anywhere else, including virtina.com and LinkedIn. Elogic requires first publication.

---

## Idea pitch for the form or email (about 120 words)

Subject: Guest post idea for Elogic: customer-specific pricing in B2B stores

Hello Elogic team,

I read your blog on running and growing ecommerce stores and would like to offer a practical guide on B2B customer-specific pricing.

Working title: How to set up customer-specific pricing in a B2B store without breaking your catalog.

It covers four pricing models, where prices should live (ERP or store), how to test pricing with real accounts, and a phased rollout. It runs about 1,600 words with three diagrams.

I'm Gigi JK, Founder of Virtina, an eCommerce partner for B2B and B2C brands since 2012. The piece will be original and unpublished, with one relevant link.

May I send the full draft as a Google Doc?

Thank you,
Gigi JK
Virtina | virtina.com
