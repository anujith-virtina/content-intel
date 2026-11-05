---
title: How many B2B inquiries never reach your pipeline? Run a 7-day count
client: chatsku
date: 2026-11-02
topic: b2b inquiry tracking, measuring unlogged inquiries (supports /black-hole-pipeline/)
audience: owners, sales managers, ecommerce managers at B2B manufacturers, distributors, wholesalers ($1M-$50M)
stage: brief
slug: inquiry-tracking-seven-day-count
---

# Brief: inquiry tracking, the 7-Day Inquiry Count

Research inputs: `output/research/inbound-pipeline-visibility-2026-11-02.md`, `uniqueness-audit-2026-11-02.md`, `competitor-analysis-2026-11-02.md`, `black-hole-pipeline-page-2026-11-02.md`, `chatsku-headings-2026-11-02.md`.

## 1. Thesis, angle, format

**Thesis:** You cannot fix a pipeline you have never counted. A one-week tally by door, set against what exists as a shared record, gives you an unlogged inquiry rate, and that rate is a floor because the buyer who left silently never appears in any ledger.

**Why this angle, why now, why ChatSKU:**
- Gap: every competitor page starts after the record exists. None gives a reconciliation count, a named metric, or a formula. None has a worked example labelled illustrative, and none has an honest "what the count cannot see" section.
- Why now: the money page `/black-hole-pipeline/` states the problem and the fix but gives no way to size the gap. This post is the measurement step before it.
- Why ChatSKU can say it: the AI catalog assistant turns website conversations into dashboard records. Phone and email remain a process gap, and the post says so. That honesty is the differentiator against vendors who claim to unify everything.
- Primary keyword: `b2b inquiry tracking`. Secondaries: unlogged inquiry rate, sales inquiry audit, quote request tracking, RFQ tracking.

**Format chosen: D (decision playbook).**
- Reason: the post is a sequenced method (count, reconcile, score) that ends in a decision (which door to fix first).
- Recency check, last 6 to 7 ChatSKU posts: 3929 = E, 3767 = D, 3305 = E, 3956 / 3846 / 3798 / 3461 = A or B (comparison, explanatory; the corpus file does not record formats). D appears once (3767), E twice. No format reaches 3, so D is allowed and is the least recent of the playbook-fit formats.
- Overused and skipped: E (two of the last seven, and 3929 is the immediately preceding brief). B is not suited to a method post.
- Fence: 3767 (D) compares intake paths for quotes. This post must not compare form vs chat vs assistant. 3010 (D) owns the persona narrative. Do not borrow it.

## 2. Uniqueness result

| Check | Result |
|---|---|
| Topic | PASS. Zero body-level hits in 52 posts for "unlogged", "inquiry log", "7-day" counts, or a reconciliation method. |
| Slug `inquiry-tracking-seven-day-count` | PASS. Shares no word with any existing slug. Final gate is the REST slug check at push. |
| Angle | PASS. 299 owns post-quote silence, 3846 owns booth open-question queue, 3010 owns manager narrative, 3929 owns a part-mapping record, 3294 (draft) owns post-rollout KPIs. This post owns the pre-rollout baseline count. |
| Money page | PASS if the creator never restates the page's symptom list. |
| Stale inventory | The inventory file stops at 2026-07. Orchestrator should fetch `/blog/` once more before push. |

**Fences (do not do):**
- Do not retell 299's silence table, 3846's shared-inbox or reply-owner advice, 3010's personas, 3294's metric names (deflection rate, qualified-handoff rate, time-to-quota), or 3929's six-field record.
- Do not use the money page's copy: "single source of truth", "heads and inboxes", "no audit trail", "if it isn't tracked, it isn't revenue", "Your competitor answered. You didn't know it happened."
- Avoid "record nobody designed" and "stamp a date on every row".
- Vary the "one line of code, live in under a day" sentence and any platform-ingestion boilerplate so the 8-gram check passes.

## 3. Title, meta, categories

- **H1:** How many B2B inquiries never reach your pipeline? Run a 7-day count (65 chars, sentence case, keyword "B2B inquiries" plus the method). Keep as locked. The exact phrase "b2b inquiry tracking" sits in the Executive Summary sentence 1, the Introduction, and the meta.
- **Freshness line** (plain text paragraph directly under the H1, before the Executive Summary): `Updated November 2026`
- **Meta title (57 chars):** B2B inquiry tracking: run a 7-day inquiry count | ChatSKU
- **Meta description (about 155 chars, creator to verify 150 to 160 programmatically):** B2B inquiry tracking starts with a count. Tally inquiries by door for 7 days, compare to your shared records, and get your unlogged inquiry rate in a week.
- **Focus keyword (Yoast):** b2b inquiry tracking
- **Categories:** 22 and 24.
- **Byline:** brand voice only. No invented author (house rule).

## 4. Structure, word budget (target 2,100, hard range 1,800 to 2,200)

All headings sentence case. Body H2s are questions. First sentence of each body H2 is locked below (25 words or fewer) and must be self-contained, with the subject noun named rather than "it". Paragraphs are 3 sentences or fewer. Sentences about 20 words or fewer. Second person.

| Section | H2 | Words |
|---|---|---|
| Exec | Executive Summary | 110 |
| Intro | Introduction | 140 |
| Body 1 | What is an unlogged inquiry in B2B sales? | 130 |
| Body 2 | How do you count B2B inquiries that never reach your CRM? | 350 |
| Body 3 | What is the unlogged inquiry rate and how do you calculate it? | 250 |
| Body 4 | What should a B2B inquiry record include? | 190 |
| Body 5 | Which door should you fix first? | 280 (includes the table) |
| Body 6 | What can the 7-day count not see? | 180 |
| PAA | People Also Ask | 200 |
| Concl | Conclusion | 90 |
| FAQ | Frequently asked questions (after Conclusion) | 225 |

Background colour cycle, widgets and conclusion button follow MUST-FOLLOW-RULES section 2 and 8. H3 only in PAA and FAQ for questions. No H3s inside body sections unless a section runs over 200 words (Body 2, Body 3 may take one each if the creator prefers).

### Executive Summary (standalone answer, the passage an AI engine will quote)
Locked first sentence: **B2B inquiry tracking starts with a seven-day count: tally every inquiry by door, then count how many exist as a shared record.**
Then 3 to 4 short sentences: the gap between the two counts is your unlogged inquiry rate. Give the formula in plain words. State that the rate is a floor. Say the count takes one working week and no new software. Name the follow-up decision (fix the door with the largest unlogged count first). One sentence, factual, that a website AI catalog assistant records the conversations it handles while phone and email are a process fix. No links here.

### Introduction (buyer scenario)
Monday. The owner asks how many quote requests came in last week. The counter rep says "a handful". The inside sales manager says 19 from email. The shared CRM shows 11. Three answers, no number anyone trusts. Label the scenario clearly as a picture (say "Picture a Monday"), and use the word "illustrative" nowhere that implies data. Close with the thesis in two sentences and the keyword "b2b inquiry tracking" once. Link 1 (`/black-hole-pipeline/`, anchor "black hole pipeline") may sit in the last sentence of the intro. Keep the money page's symptom list out.

### Body 1: What is an unlogged inquiry in B2B sales?
Locked first sentence: **An unlogged inquiry is a buyer request that reached someone on your team but exists in no record that others can open.**
Then: define "door" in one sentence (a channel where buyers reach you: email, phone, web form, website chat). Define "shared record" in one sentence (an entry in a CRM, quote tool, or dashboard that anyone on the team can open). State that a note in a personal inbox, a notebook, or a rep's memory is not a shared record. Link 1 goes here if not placed in the intro (anchor: "black hole pipeline"). Terms: inquiry, inbound inquiry, RFQ, quote request, source of inquiry, handoff.

### Body 2: How do you count B2B inquiries that never reach your CRM?
Locked first sentence: **Tally every inbound inquiry by door for seven working days, then count how many exist as a shared record and score the gap.**
Define "The 7-Day Inquiry Count" in the second sentence: a one-week tally-and-reconcile method that measures how much inbound demand has no shared record.
Required element, a numbered list (genuinely sequential, 5 steps, one or two sentences each):
1. Hand every person who receives buyer contact a tally sheet. Include the counter rep, inside sales, the owner's own inbox, and whoever picks up the main line.
2. Log one line per inquiry as it arrives: day, door, product or question in a few words, quote asked yes or no.
3. On day eight, search your shared system for each line.
4. Mark each line "record" or "no record".
5. Calculate the rate (next section) and rank the doors by unlogged count.
Then one short paragraph: the whole job takes about five minutes a day per person plus about an hour to reconcile on day eight (state as an estimate, "plan on", not as a statistic). Link: `/b2b-quote-to-order-automation/` is NOT here. Keep this section method-only. Terms: 7-day tally, reconciliation, shared inbox, spreadsheet, voicemail, counter sales, inside sales.

### Body 3: What is the unlogged inquiry rate and how do you calculate it?
Locked first sentence: **The unlogged inquiry rate is the share of counted inquiries with no shared record, calculated as counted minus recorded, divided by counted.**
Required elements:
- Formula in plain text on its own line: `Unlogged inquiry rate = (inquiries counted - inquiries with a shared record) / inquiries counted`
- Two companion numbers, one defining sentence each: the **ownerless rate** is the share of recorded inquiries with no named owner. The **stale-stage count** is the number of open quotes whose stage has not changed in seven days.
- Worked example, labelled **"Illustrative example, not a benchmark"**. Verified arithmetic and a per-door split that adds up:

| Door | Counted | With a record | Unlogged | Door rate |
|---|---|---|---|---|
| Email | 41 | 16 | 25 | 61.0% |
| Phone (asking about a product) | 17 | 2 | 15 | 88.2% |
| Web form | 12 | 11 | 1 | 8.3% |
| Total | 70 | 29 | 41 | 58.6% |

(41 / 70 = 0.5857, so 58.6%, say "about 59%". Do not present this as a second table in the page if the creator prefers prose: the brief allows the example as a short sentence run instead. The page is allowed ONE comparison table, which is the door table in Body 5. Put this example in prose or a 4-line list, not a table.) Prose version: of 70 counted, 29 had a record, so 41 did not, a rate of about 59%. Email holds the largest unlogged count (25), phone has the highest door rate (15 of 17), forms are nearly clean.
**Correction to research:** the research notes say phone is the largest unlogged door. With the split above, email has the largest count and phone the highest rate. The creator must use this split, not the research wording.
No stale-stage or ownerless worked numbers needed. Terms: pipeline, quote stage, owner, ownerless rate, stale quote.

### Body 4: What should a B2B inquiry record include?
Locked first sentence: **A usable inquiry record holds five fields: source door, product or question, intent, owner, and quote stage.**
One sentence on each field (a short list is acceptable because it is list-shaped, five items). Intent has three levels: browsing, comparing, ready to quote (described as a working scale, not a standard). Owner is a process field your team assigns, not a ChatSKU feature claim. Quote stage names: new, quote open, quote sent, won or lost. Link 3: `/b2b-quote-to-order-automation/`, anchor "silence after the quote", one clause: what happens after the quote is sent is covered there. Do not retell its table. Do not reuse 3929's six fields or 3294's names.

### Body 5: Which door should you fix first?
Locked first sentence: **Fix the door with the largest unlogged count first, because that is where the most unrecorded demand enters.**
Required element: **one comparison table** with real header cells. Columns: Door | What gets lost | What the count shows | First fix.
- Email: RFQs with a PDF attached, replies to a rep who has left | unlogged count per mailbox | forward inquiry emails to one shared address and log them by the end of the day
- Phone: repeat-customer orders, spec questions a counter rep answers | highest door rate in most shops (do not state as fact, say "often") | a one-line call log at the desk, owner named
- Web form: submissions that land in one person's inbox | forms with no record | route every form into the shared system
- Website chat: questions asked after hours | conversations without a record | an AI catalog assistant records each conversation it handles as a dashboard entry with source, product interest, intent signals, and quote status
Text around the table: 2 short paragraphs. State plainly that ChatSKU records website conversations and sends a complete RFQ to your team or CRM with the conversation attached. State that phone and email stay a process fix the count exposes. NEVER claim phone or email capture.
Links (each in a different paragraph, none a pitch): `/ai-sales-assistant-b2b-ecommerce/` anchor "AI sales assistant for B2B", `/features/` anchor "ChatSKU integrations" (CRM sync wording as in brand.md), `/ai-sales-agent-vs-chatbot-vs-sales-rep/` anchor "AI sales agent vs chatbot", `/trade-show-booth-catalog-assistant/` anchor "trade show open questions" (one clause: events add a temporary fifth door for a few weeks a year, covered there, not retold).

### Body 6: What can the 7-day count not see?
Locked first sentence: **The count cannot see buyers who left without contacting anyone, so your unlogged inquiry rate is a floor, not the full loss.**
Content: voicemail never returned, mail sent to a rep who left, the silent after-hours visitor. Add that a visitor who asks the website assistant a question becomes a record, so one blind spot narrows. Link 2 to `/black-hole-pipeline/`, anchor "pipeline visibility problem", in a different paragraph from link 1. Link `/roi-calculator/` anchor "ROI calculator": once you have a rate, price the gap with your own deal size. No statistics.

### People Also Ask (H3 questions, 2 to 3 sentences each, answer in sentence one)
1. **How do you track B2B inquiries that come in by phone and email?** Log each one at the door as it arrives, then check it against the shared record on day eight. Do not repeat the Body 5 table.
2. **What is a good inquiry capture rate for a distributor or manufacturer?** Locked first sentence: **No verified benchmark for inquiry capture rate exists for distributors or manufacturers, so set your own baseline in week one.** Then: repeat the count monthly and aim to move your own number.
3. **How long does a 7-day inquiry audit take?** Seven working days of tallying, about five minutes a day per person, plus about an hour to reconcile. Estimate, not a statistic.
4. **Can an AI catalog assistant log inquiries automatically?** It records website conversations and quote requests it handles, with source, product interest, intent signals, and quote status. It does not capture phone calls or inbox mail.

### Conclusion (dark navy, three widgets, no inline link)
Point: run the count Monday, rank the doors by unlogged count, close the biggest one first. One sentence naming what the AI catalog assistant covers (the website door). CTA button text: "See the live demo", link `https://chatsku.com/demo/`. Short, concrete, no "learn more".

### FAQ (5 Q&As, 40 to 60 words each, no repeat of PAA)
1. **Who should own incoming sales inquiries?** One named role per door, assigned before the count. Keep to two sentences, link nothing (3846 and 3798 own the owner advice).
2. **What should a sales manager be able to see about the pipeline?** Four answers in 60 seconds: inquiries this week, how many have a quote open, how many open quotes are older than seven days, which door each came through. (This replaces the list that was in Body 4.)
3. **Does ChatSKU log phone calls and emails?** No. It records the conversations it handles on your website. Phone and email need a process fix, which the count helps you rank.
4. **Do I need a CRM to run the 7-day count?** No. A shared spreadsheet that everyone can open counts as a shared record. A personal inbox does not.
5. **How often should I repeat the count?** Repeat it after each fix and then monthly. Compare your rate against your own week-one baseline, not against anyone else's number.

## 5. AIO and GEO design checklist (locked)

- Every body H2 is a question; first sentence self-contained and 25 words or fewer (locked above).
- Each named term is defined once, in one sentence, the first time it appears: unlogged inquiry, door, shared record, The 7-Day Inquiry Count, unlogged inquiry rate, ownerless rate, stale-stage count.
- Executive Summary reads alone as the answer to "How do you track B2B inquiries and measure the ones that go missing?"
- One comparison table (Body 5), one numbered step list (Body 2), one plain-text formula (Body 3), the "no verified benchmark" line (PAA 2).
- Entities used by name: ChatSKU, AI catalog assistant, inquiry, shared record, owner, quote stage, RFQ, CRM, dashboard, shared inbox.
- Freshness: `Updated November 2026` as plain text under the H1.
- Schema: Article + BreadcrumbList as JSON-LD through an HTML widget, if the build script supports one. FAQPage JSON-LD only as harmless markup, matching the visible FAQ exactly (5 Q&As). Do not describe it as a rich-result tactic (Google dropped FAQ rich results). Article author should be the Organization "ChatSKU", no personal byline, `dateModified` 2026-11-02. If the script cannot add an HTML widget, skip all schema and flag it. Keep schema text identical to visible text.
- No keyword stuffing. The keyword appears in the H1 area, first 100 words (Executive Summary sentence 1), the Introduction, and the meta.

## 6. Evidence and links

**Statistics:** zero external statistics. The only numbers are the labelled illustrative example and plan-on time estimates. Banned: Gartner 61/67%, HBR 42-hr, MIT 5-minute/21x, Baymard figures, Sana Commerce, Workato study, "$15T/90% by 2028", and the competitor-page figures (79% leakage, 30% of phone inquiries, 3 to 4 of 10 leads).
**External links:** zero.
**Internal links (total 9 distinct URLs, 10 link instances):**

| # | Anchor | URL | Section | Status |
|---|---|---|---|---|
| 1 | black hole pipeline | /black-hole-pipeline/ | Intro or Body 1 | read live 2026-11-02 |
| 2 | pipeline visibility problem | /black-hole-pipeline/ | Body 6 | same |
| 3 | silence after the quote | /b2b-quote-to-order-automation/ | Body 4 | fetched live per research |
| 4 | AI sales assistant for B2B | /ai-sales-assistant-b2b-ecommerce/ | Body 5 | fetched per research |
| 5 | ChatSKU integrations | /features/ | Body 5 | fetched per research |
| 6 | AI sales agent vs chatbot | /ai-sales-agent-vs-chatbot-vs-sales-rep/ | Body 5 | fetched live per research |
| 7 | trade show open questions | /trade-show-booth-catalog-assistant/ | Body 5 | fetched live per research |
| 8 | ROI calculator | /roi-calculator/ | Body 6 | canonical |
| 9 | See the live demo (button) | /demo/ | Conclusion widget | fetched per research |

Status note: this agent has no HTTP tool, so the "200 with redirects off" check was not run by me. The research file records that each page was fetched. The orchestrator must re-check all nine with redirects disabled before push. Do not link drafts 3294 and 3848, `/pricing/`, `/rfq-automation-for-product-catalogs/`, or `/lost-b2b-revenue-calculator/`. No competitor names. No "our guide" phrasing. Anchors are 2 to 5 words and name the real destination topic.

## 7. Product guardrail

**May say:** ChatSKU is an AI catalog assistant. Every conversation it handles on your website is captured as a dashboard record showing inquiry source, product interest, buyer intent signals, and quote status. A complete RFQ goes to your team or CRM with the conversation attached. It ingests PDF, Excel, ERP exports and CSV, and goes live with one line of code in under a day (vary the wording). Full conversation logs and shopper-intent analytics exist on the assistant solution page.
**Must not say:** phone-call capture, email-inbox capture, automatic CRM write-back beyond "sends the RFQ to your CRM or inbox", a field list beyond the four above, unified-everything claims, an "inquiry dashboard" product name, any customer or percentage result, "replaces your sales team", "just a chatbot", "AI-powered" as filler, "chatbot" alone.
**Placement:** about three mentions: Body 5 (website door row and paragraph), Body 6 (one clause), Conclusion. Not in the Introduction.

## 8. Style reminders

No em dashes, no semicolons, no exclamation marks. Sentence-case headings. Oxford comma. Use "catalog", "buyer", "quote", "after-hours". Bullets only for genuinely list-shaped content (the five record fields, the numbered steps). Banned words: delve, leverage, navigate (verb), landscape, ecosystem, realm, revolutionary, game-changing, cutting-edge, "solutions" as filler. Required H2s: Executive Summary, Introduction, People Also Ask, Conclusion, Frequently asked questions. Run the 8-gram shingle audit against all 52 posts and the money page text, and a Flesch check against ChatSKU's corpus, before push.

## 9. Image plan (3 images, 860x452, generated in ChatGPT, realistic, no text or legible writing in any image)

Existing scenes to avoid: hydraulic fitting, valve counter, trade fair, warehouse aisle at dusk, parts counter with worn component, hands comparing two parts, a warehouse aisle with a laptop.

1. **Featured.** A distributor sales manager at a desk on a Monday morning, reading a paper tally sheet covered in pencil strokes, with a laptop and a coffee beside it and a sales office behind. Mood: puzzled, focused, daylight. No readable text.
   Alt (about 121 chars): Sales manager reviewing a paper tally of inbound B2B inquiries at a distributor office desk during a Monday pipeline check
2. **Body 1, in Body 2 (the count method).** Close-up of a hand marking a grid of tally strokes on a clipboard sheet next to a desk phone and a keyboard at an inside-sales desk. Warm office light.
   Alt (about 112 chars): Inside sales rep marking a handwritten inquiry tally sheet beside a desk phone for a seven-day B2B inquiry count
3. **Body 2, in Body 5 (the doors).** A shipping office at a loading dock: a desk phone ringing, order sheets pinned to a corkboard, a laptop open, a forklift visible through the window behind. Different room and light from image 2.
   Alt (about 126 chars): Distributor shipping office with a ringing desk phone, order sheets on a corkboard, and a laptop open at the loading dock window

Rules: image widget AFTER the text-editor widget in its section. Do not use two images from the same photo shoot. Alt text is rewritten after the final images are chosen and checked at 80 to 150 characters with 1 to 2 keywords.

## 10. Semantic terms

inquiry, inbound inquiry, door, shared record, 7-day tally, reconciliation, unlogged inquiry rate, ownerless rate, stale-stage count, quote stage, owner, intent, source of inquiry, RFQ, quote request, CRM, spreadsheet, shared inbox, voicemail, counter sales, inside sales, handoff, stale quote, product interest, intent signal, dashboard, conversation log, AI catalog assistant, ChatSKU, distributor, manufacturer, wholesaler, sales manager. Avoid: "single source of truth", "heads and inboxes", "chatbot" alone, "AI-powered", "solutions".

## 11. Social angle note (for the later carousel; not section headings)

Three facts from the post that surprise: (1) a note in your own inbox does not count as a record, so a rep who answered every email can still score badly; (2) in the illustrative example email had the biggest pile of unlogged inquiries (25) while phone had the worst rate (15 of 17), so the loudest channel and the leakiest channel are different; (3) the headline number is a floor, because the buyer who left without a word never enters any ledger. Hook: "Three people, three answers to one Monday question." The formula and the 70 to 59% example land best as one slide each. Keep the visuals as ChatGPT scenes with the logo, per house social rules, and do not reuse the last carousel layout.

## 12. Locked vs creator judgment

**Locked:** thesis, Format D, slug, H1, H2 list and order, the locked first sentences, formula, example numbers and per-door split, five record fields, the one table, zero external statistics and links, link plan, product guardrail, meta, image plan.
**Creator judgment:** the Monday scenario wording, where link 1 sits (intro or Body 1), FAQ phrasing beyond the locked questions, whether the worked example is prose or a four-line list, H3 use in Body 2 and Body 3.

## 13. Open items for the orchestrator

1. Re-check all nine internal URLs with redirects off (not possible from this agent).
2. Fetch `/blog/` for posts newer than the stale inventory before push.
3. Confirm the build script can add an HTML widget for JSON-LD. If not, drop schema and note it.
4. Formats of 3956, 3846, 3798, 3461 are not recorded in the corpus file. D was chosen on the basis that none of the recorded recent posts shows three of any one format.
5. Research stated phone as the largest unlogged door in the worked example. This brief fixes that with a per-door split that sums to 70 / 29 / 41.
