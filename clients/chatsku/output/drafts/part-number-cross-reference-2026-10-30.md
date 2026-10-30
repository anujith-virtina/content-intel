---
title: "Part number cross reference: the record nobody designed"
client: chatsku
date: 2026-10-30
slug: part-number-cross-reference
stage: draft
brief: clients/chatsku/output/briefs/part-number-cross-reference-2026-10-30.md
word_count: 1990
headlines:
  - "Part number cross reference: the record nobody designed"
  - "Your part number cross reference is a record, not a list"
  - "Why a part number cross reference table fails buyers"
---

# Part number cross reference: the record nobody designed

**Meta title:** Part number cross reference: design the record | ChatSKU

**Meta description:** A part number cross reference needs more than a pair of numbers. See the six fields every row needs, from match type to next step, and what to say on no match.

## Executive Summary

A part number cross reference is not a list of pairs. It is a record, and most distributors never designed it. Your table holds two numbers, but the buyer needs a decision.

This article separates four relationships that people mix up: cross-reference, supersession, interchange, and substitute. Every row needs six fields: match type, what differs, direction, last verified date, stock, and next step. You also get a rule for who owns the table and what to say when nothing matches.

Design the record first. Then decide who or what delivers it.

## Introduction

Say a maintenance buyer is holding a worn part. The only clue is a number stamped by another maker. Her line is down, and she needs a replacement today.

She types the number into your site. Nothing comes back, or a bare part number comes back with no context.

Is the aftermarket equivalent you stock a drop-in replacement for that OEM part number? Is it only close? The page does not say.

At your parts counter, a good rep asks which machine it is for and what has to match. Your table asks neither.

Your cross-reference table stores two numbers in a row and nothing more. The buyer needs far more than that. This piece covers the record, its owner, and what to say on no match.

A cross-reference table is a record nobody designed. It holds two numbers because that is all anyone needed when the first row was typed.

## What does a buyer holding another maker's number need?

A buyer holding another maker's number needs a decision, not a lookup. Finding a matching number is only step one. The buyer still has to trust it enough to order.

In practice, the buyer is doing four jobs at once. Each job needs a different part of the record.

- **Find an equivalent.** The buyer holds a competitor's number and wants your matching part.
- **Check fit.** Is the alternate part a drop-in or only a spec match, and what differs?
- **Check supersession.** The number may be obsolete, with a newer number in its place.
- **Check stock and next step.** Do you have it, and how does the buyer order?

Most OEM cross reference lookup tools and equivalent part finders stop at the first job. That leaves fitment, supersession, and stock for the buyer to work out alone.

How search reads your data is a separate topic, covered under [retrieval mechanics](https://chatsku.com/how-ai-product-search-works/). Where keyword search breaks is covered under [keyword search failures](https://chatsku.com/traditional-b2b-product-search-fails/). This article starts with the data.

[[IMG1]]

## Is a cross-reference the same as a supersession?

No, they are different relationships, and the difference decides what you tell the buyer. People use these words loosely. The table below shows how most parts counters use them, as general definitions and not an OEM standard.

| Term | Whose number | Direction | What the buyer is told |
|---|---|---|---|
| Cross-reference | Another maker's number | Either way, so state it | This is an equivalent from a different maker |
| Supersession | Same maker, new number replaces old | Often one way | The old number was replaced by this one |
| Interchange | Either maker | Usually two way | These parts can be used in place of each other |
| Substitute | Your suggestion | One way, from you | This part is close, and here is what differs |

Pick one meaning for each word and use it everywhere. Mixed vocabulary is how a one-way supersession gets shown as an interchange.

### Why direction changes the answer

Direction decides whether the old part still works. In a one-way supersession, the new part replaces the old one. The old one may not work where the new design is required.

A two-way relationship means the parts are fully interchangeable. Now picture two buyers, as a hypothetical.

The first holds the old number, so you can offer the new part. The second holds the new number and asks for the old one. Your answer may be no.

If the old part is discontinued, say so. A buyer should never find that out after the order ships.

### Why one competitor number can map to several of your parts

One-to-many is normal. One competitor number can point to several of your parts, each with a different finish, length, or rating.

Each candidate needs its own list of differences. Show them as separate rows, not as one merged guess. The buyer then picks the functional equivalent that fits the job.

## What should one part number cross reference record hold?

One record should hold six fields beyond the two numbers. They are match type, what differs, direction, last verified date, stock, and next step.

### The six fields

Each field exists because a buyer asks the question it answers.

- **Match type.** Say if it is a direct replacement, a functional equivalent, or an application match.
- **What differs.** List the variance, such as thread, finish, or rating.
- **Direction.** State whether the match works one way or both ways.
- **Last verified date.** Show when a person last checked the row.
- **Stock.** Say whether you have the part now.
- **Next step.** Offer a quote, a hold, or a person.

This is a way of describing matches, not an industry standard. Add the MPN and GTIN so the buyer can confirm the part. The numbers must also be readable text, which the [catalog readability audit](https://chatsku.com/b2b-catalog-ai-agent-readability-audit/) covers.

### What the buyer sees

Here is a hypothetical example record. Every name and number in it is invented.

| Field | What it says |
|---|---|
| Buyer's number | Maker A model 4410 |
| Your part | Your SKU 77-210 |
| Match type | Functional equivalent |
| What differs | Mounting holes are slightly wider, same rating |
| Direction | Two way |
| Last verified | A dated entry, with the name of who checked it |
| Stock | In stock at the main warehouse |
| Next step | Offer a quote, and a person confirms fit |

That record becomes a two-sentence answer for the buyer.

"Your SKU 77-210 is a functional equivalent of Maker A model 4410, with wider mounting holes. It is in stock, and I can start a quote now."

That answer is a candidate, not an approval. A person signs off on certified assemblies.

### Where the next step leads

The next step often hits a limit. The buyer wants a few, and the part ships only by the case. Those [minimum order rules](https://chatsku.com/minimum-order-quantity-b2b/) belong in the record or in the next answer.

## Who keeps the table right?

A named role must own the table, or it goes stale. Without an owner, every row ages at its own pace. Nobody knows which ones still hold.

### Where the table lives today

Many ERP part records hold a linked number and a free-text note. Some have no field for match type or direction.

So the rest lives in a rep's memory. That is a single point of failure. The rep retires, moves territories, or takes a week off, and the knowledge leaves too.

### What an owner actually does

Name one role as owner, such as the product data lead. Stamp a date on every row. Review a row when a trigger fires.

Triggers include a supplier change notice, a returned part, a buyer complaint, or a catalog update.

Some manufacturers publish a disclaimer that specs between makers can differ. They add that they may not hear when an OEM changes one. If they cannot promise a match, a table nobody reviews cannot either.

Export the table with its fields intact, and run an [ERP export check](https://chatsku.com/erp-export-ai-agent-ready/) before you upload it anywhere.

ChatSKU answers from the table as you upload it. If the table is wrong, the answer is wrong. The data fix comes first.

[[IMG2]]

## What should the answer say when there is no match?

It should say there is no confirmed match, say what happens next, and never guess a close part. Say a buyer types a number at 8pm, and it is not in your table. A bad answer guesses a near-match and hopes.

A good answer says there is no confirmed match and starts the next step. The bad answer sounds helpful, which is the danger. The buyer orders a guess, and your team inherits the return.

### What a good no-match answer contains

A good answer does four things. It states the gap plainly. It asks for the specs or a photo.

It captures contact details and quantity. It tells the buyer when a person will follow up.

If you upload the table with the catalog, ChatSKU, an AI catalog assistant, answers from the rows it has. No row, no invented part. It then hands the buyer to a person or captures the quote request, at any hour.

Files can be PDF, Excel, ERP exports, or CSV, as listed under [supported catalog files](https://chatsku.com/features/).

That is what [AI product search](https://chatsku.com/ai-product-search-for-b2b/) should feel like: an answer from your data, or an honest no.

### How to hand the buyer to a person

Route the buyer to a rep and pass everything along. Include the buyer's number, any specs, and the quantity so nobody asks twice. A handoff that repeats questions feels like a second dead end.

If you are weighing who this suits, read about [catalog assistant fit](https://chatsku.com/who-b2b-catalog-assistant-is-built-for/).

## People Also Ask

### What is a part number cross reference?

A part number cross reference links one part number to another that does the same job. It usually maps another maker's number to yours, and it can run one way or both. A useful record also states the match type, what differs, and when someone last verified it.

### How do you find the equivalent of a competitor part number?

Start with the cross-reference table from the maker or distributor you buy from. Search the competitor part number, then compare the listed differences against your need. If no row exists, send the number and specs to a person who can confirm a match before you order.

### Can a cross-reference be one-way?

Yes, some relationships work in one direction only, such as a supersession. The new part may replace the old one, but the old part may not fit the new design. Make direction its own field, and check it before you order the reverse.

### Is an aftermarket equivalent the same as an OEM part?

No, an aftermarket equivalent comes from a different maker and is built to do the same job. It may match the OEM part on fit and function, or differ in small ways. Check the listed variances, and get a person to sign off on certified assemblies.

## Conclusion

Design the record first, then decide who or what delivers it. Every row needs six fields: match type, what differs, direction, last verified date, stock, and next step. Add an owner and a review trigger, and the table stops going stale.

Add a clear no-match answer, and the buyer never meets a dead end. Start with the numbers buyers ask about most.

See the ChatSKU live demo to watch an assistant answer from a table you upload.

## Frequently asked questions

### Who should own the cross-reference table?

Give it to one named role, usually product data or the parts desk lead. That person schedules reviews and approves changes. Reps can suggest edits, but one owner signs them off.

### How often should a row be re-verified?

Re-verify on a trigger and on a calendar review. Triggers include a supplier change notice, a returned part, or a buyer complaint. Set the calendar cadence to match how fast your suppliers change parts.

### Can an assistant approve a substitute for a certified assembly?

No, it can only present a candidate with the differences listed. A person signs off on certified assemblies. Treat every answer as a candidate, not an approval.

### What file format should I use to upload a cross-reference table?

CSV or Excel works well, with one row per pair. That shape keeps each match type and difference on its own row. An AI catalog assistant reads PDF, Excel, ERP exports, and CSV, but tidy the table first.

### What if I have no cross-reference table yet?

Start with the competitor part numbers buyers ask about most. Record those first, with every field above. Then grow the table from the questions your reps answer by hand.
