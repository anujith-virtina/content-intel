---
title: How many B2B inquiries never reach your pipeline? Run a 7-day count
client: chatsku
date: 2026-11-02
topic: B2B inquiry tracking, measuring unlogged inquiries (supports /black-hole-pipeline/)
audience: owners, sales managers, ecommerce managers at B2B manufacturers, distributors, wholesalers ($1M-$50M)
stage: research
slug: inquiry-tracking-seven-day-count
---

# Research notes

Companion files: uniqueness-audit-2026-11-02.md, competitor-analysis-2026-11-02.md.

## 0. Required checks (reported for the analyzer)
- Rules read: MUST-FOLLOW-RULES.md (all sections), brand.md, voice.md, audience.md, cms.md. The published-posts-inventory.md is stale (stops at 2026-07); the 2026-11-02 headings file, full-text JSON, and money-page text were used instead.
- Topic and slug uniqueness: PASS. See audit. Slug shares no word with any existing slug.
- Money-page rule: the post must not restate the page's symptoms or copy. Link to it twice.

## 1. Chosen topic
Title: How many B2B inquiries never reach your pipeline? Run a 7-day count
Slug: inquiry-tracking-seven-day-count
Primary keyword: b2b inquiry tracking
Secondary: unlogged inquiry rate, sales inquiry audit, quote request tracking, RFQ tracking, lead leakage (B2B)
Recommended format: D (decision-tree / playbook). Word target 1,800 to 2,200.
Reader state: pre-decision. Suspects leads go missing but has no number. Leaves with a count to run Monday and a rule for what to fix first.

## 2. Thesis
You cannot fix a pipeline you have never counted, and the count is a one-week job with a pencil. Count what arrived at each door (inbox, phone, web forms and chat), count what exists in one shared record, and the gap is your unlogged inquiry rate. The number is a floor, not a ceiling, because the buyer who left without a word never shows up in any ledger.

Relationship to the money page: /black-hole-pipeline/ states the problem and the fix. This post is the measurement step before it: size the gap, then decide which doors to close first. The post must stay honest that ChatSKU records the conversations it handles on the website. Phone and email stay a process question the count exposes.

## 3. Named framework (the post's own, coined here)
Name: **The 7-Day Inquiry Count**
Three steps and one metric.

1. **Count the doors.** For seven working days, every person who receives inbound buyer contact keeps a tally by door: email, phone, web form, website chat. One line per inquiry: day, door, product or question in a few words, quote asked yes/no. Include the counter rep and the owner's own inbox.
2. **Count the records.** On day eight, count how many of those same inquiries exist as a record in a shared system anyone on the team can open (CRM, quote tool, or dashboard). An inquiry living only in a personal inbox, notebook, or memory is not a record.
3. **Score the gap.** Three numbers (below). Then rank the doors by unlogged count.

**Unlogged inquiry rate (UIR)** = (inquiries counted at the doors minus inquiries with a shared record) divided by inquiries counted at the doors.

Two companion numbers, so the post can offer "three visibility numbers":
- **Ownerless rate** = share of recorded inquiries with no named owner.
- **Stale-stage count** = open quotes whose stage has not changed in 7 days.

Illustrative worked example (label "illustrative, not a benchmark"): 41 emails + 17 phone calls asking about a product + 12 form submissions = 70 inquiries counted. 29 have a shared record. UIR = (70 - 29) / 70 = 58.6%, round to 59%. Verified arithmetic. Phone is the largest unlogged door in the example; fix rank follows.

Why a coined term works for AI citation: a short, named, defined metric with a formula is a self-contained passage an answer engine can quote and attribute. Keep the definition in one sentence directly under its H2.

Honesty section ("What the count cannot see"): buyers who left without contacting anyone, calls that went to voicemail and were never returned, and mail sent to a rep who has left. The UIR is a floor. This also sets up where a website assistant adds visibility: the silent after-hours visitor who asks something becomes a record.

Minimum inquiry record (short section, five fields, own framing to avoid 3929 and the money page list): Source (which door), Product or question, Intent (browsing, comparing, ready to quote), Owner, Stage. Money-page fields are source, product interest, buyer intent signals, quote status; the extra field "Owner" is a process field the team assigns, not a claimed ChatSKU feature.

What a manager should be able to answer in 60 seconds (short list, 3 to 4 items, not a KPI redesign; 3294 owns that): how many inquiries this week, how many have a quote open, how many open quotes are older than 7 days, which door they came through.

## 4. Target questions (PAA style). Use verbatim as H2/H3, answer in the first sentence.
1. What is an unlogged inquiry in B2B sales?
2. How do you find out how many sales inquiries never reach your CRM?
3. How do you track B2B inquiries that come in by phone and email?
4. What is the unlogged inquiry rate and how do you calculate it?
5. What should a B2B inquiry record include?
6. What is a good inquiry capture rate for a distributor or manufacturer? (Answer: there is no verified published benchmark; set your own baseline in week one and aim to move it. Do not invent one.)
7. How long does a 7-day inquiry audit take?
8. Who should own incoming sales inquiries?
9. What should a sales manager be able to see about the pipeline?
10. Can an AI catalog assistant log inquiries automatically? (Answer scoped to website conversations and quote requests; phone and email not claimed.)

Structure suggestion for the analyzer: Executive summary; Introduction (buyer scenario: Monday, owner asks "how many quote requests came in last week?" and three people give three answers); H2 per question 1, 2/4 (the count, as steps), 5, 9, then "which door do you fix first" decision table, "what the count cannot see", PAA (3 to 4 of the above not already H2s), Conclusion, FAQ. Sentence-case headings; no em dashes.

## 5. AIO/GEO findings (sources fetched)
Verified at primary source:
- Google Search Central, "AI features and your website" (https://developers.google.com/search/docs/appearance/ai-features): to be a supporting link in AI Overviews or AI Mode a page must be indexed and eligible to show in Search with a snippet; Google states no additional requirements or special optimizations; structured data must match the visible text; no special schema is needed; recommends helpful, reliable, people-first content. Fetched 2026-11-02; page shows no date.
- Google Search Central blog, "Top ways to ensure your content performs well in Google's AI experiences" (https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search), John Mueller, 21 May 2025: focus on unique, non-commodity content; markup content must be visible on the page; make sure Googlebot is not blocked and pages return 200; nosnippet and max-snippet limit AI use of content.
- Google "Creating helpful, reliable, people-first content" (https://developers.google.com/search/docs/fundamentals/creating-helpful-content): original information, analysis; trust is the most important E-E-A-T aspect; bylines must be accurate; explain how content was produced when readers would wonder. (Consistent with the house rule against fake bylines.)
- Google Search Central FAQPage structured data page (https://developers.google.com/search/docs/appearance/structured-data/faqpage): the page's change log says the FAQ rich result is no longer shown in Search (entries dated May 8 and June 15, 2026). Secondary coverage agrees (Search Engine Land: https://searchengineland.com/google-to-no-longer-support-faq-rich-results-476957 ; reports say Google still uses FAQ markup to understand pages, not verified at primary source). Practical effect: keep the visible FAQ for readers and for answer engines that read the page text; FAQPage JSON-LD is optional, harmless if it matches visible text, and must not be sold as a rich-result tactic. This corrects older house notes that treat FAQ schema as a rich-result lever.
- Aggarwal et al., "GEO: Generative Engine Optimization", KDD 2024, arXiv 2311.09735 (https://arxiv.org/abs/2311.09735): GEO methods can raise visibility in generative-engine answers by up to 40%; efficacy varies by domain. The paper's own tests found that adding statistics, quotations, and citations helped most and that keyword stuffing did not help. Source for method design only; do not quote the percentage in the post (reader is not an SEO audience; stat is not about inquiry tracking).

Not verifiable from primary sources: any claim of the form "pages with schema get X% more AI citations" (vendor blogs only). Excluded.

Practical rules derived (for the creator):
1. Question headings, answer in the first sentence (one or two sentences), then the how.
2. One definition per named term, in a single self-contained sentence.
3. Short paragraphs, each able to be lifted alone; put the subject noun in the sentence rather than "it".
4. One comparison table (doors vs what gets lost vs fix) with real header cells.
5. Specific entities: names of channels, record fields, quote stages; labelled illustrative numbers rather than invented statistics.
6. Original, citable framework with a formula (see section 3). This is the "unique, non-commodity" element Google's guidance describes.
7. Freshness: put a visible date and a "last reviewed" line; refresh when the money page changes.
8. Visible FAQ matching any FAQPage markup exactly.

## 6. Verified facts usable in the post (all internal to the brand, no external statistics)
- Money page: ChatSKU captures every conversation it handles into a dashboard showing inquiry source, product interest, buyer intent signals, quote status (https://chatsku.com/black-hole-pipeline/, fetched 2026-11-02).
- Demo page admin dashboard sections: products, quotes, orders, customers, analytics, chatbot settings, team management; setup about four hours on average, one line of code (https://chatsku.com/demo/, fetched 2026-11-02). Use brand.md wording "one line of code, live in under a day".
- /ai-sales-assistant-b2b-ecommerce/ lists full conversation logs and shopper-intent analytics.
- Post 3956: a complete RFQ is sent to your team or CRM with the conversation attached.
No external statistic is proposed. Banned or already used: Gartner 61%/67%, HBR 42-hr, MIT 5-minute/21x, Baymard 12% or 48%, Sana Commerce 75/78/91%, Workato 114-company study, "$15T/90% by 2028". The competitor pages' figures (79% leakage, 30% of phone inquiries, 3 to 4 of 10 leads) are unsourced or self-reported and are NOT to be used.

## 7. Semantic terms and entities
inquiry, inbound inquiry, RFQ, quote request, quote stage, pipeline, shared record, CRM, spreadsheet, shared inbox, voicemail, counter sales, inside sales, repeat-customer phone order, web form, website chat, source of inquiry, owner, handoff, stale quote, 7-day tally, reconciliation, unlogged inquiry rate, ownerless rate, intent signal, product interest, sales manager, distributor, manufacturer, wholesaler, AI catalog assistant, conversation log, dashboard.
Avoid: "single source of truth" and "heads and inboxes" (money page copy); "chatbot" alone; "AI-powered"; "solutions".

## 8. Internal links (status verified or read 2026-11-02)
Pages (3 or more required):
1. https://chatsku.com/black-hole-pipeline/ (money page, read live; use TWICE with different anchors, e.g. "black hole pipeline" and "pipeline you can't see")
2. https://chatsku.com/ai-sales-assistant-b2b-ecommerce/ (fetched, loads, H1 "Your store has the cart...")
3. https://chatsku.com/features/ (fetched, loads)
4. https://chatsku.com/roi-calculator/ (fetched, loads, H1 "Revenue Left on the Table"; canonical per rules)
5. https://chatsku.com/demo/ (fetched, loads; use for the CTA button)
Optional: https://chatsku.com/response-gap/ (not re-fetched; listed in rules).
Blog posts (2 or more required, all status publish in the corpus and fetched where noted):
- https://chatsku.com/b2b-quote-to-order-automation/ (299, fetched live). Anchor idea: "silence after the quote". Role: next step downstream.
- https://chatsku.com/trade-show-booth-catalog-assistant/ (3846, fetched live). Anchor idea: "trade show open questions". Role: another place unlogged questions pile up; do not retell.
- https://chatsku.com/ai-sales-agent-vs-chatbot-vs-sales-rep/ (3956, fetched live). Anchor idea: "AI sales agent vs chatbot".
- https://chatsku.com/b2b-customers-leave-for-faster-competitors/ (369, fetched live). Optional.
Do NOT link: /pricing/ (redirects), /rfq-automation-for-product-catalogs/ (homepage), drafts 3294 and 3848 (also 3066/3281/3023/3305 now show as publish in the corpus but were not re-verified; skip them). Do not use 2992 or 1855 without confirming the canonical slug (rules: 1855 canonical is /reduce-b2b-quote-response-time/).
Anchors must be 2 to 5 words and name the destination's real topic. No promotional "our guide" phrasing.

## 9. External link picks (max 2)
Recommended: zero external links. The post is an operational how-to built on the reader's own data and on the post's own framework; no verified external statistic is needed. If the analyzer wants one for E-E-A-T, the only fully verified candidate is Google's AI features page above, but it is off-topic for this reader and not recommended. No competitor links.

## 10. Conflicts and uncertainty
- Competitor and vendor pages disagree on what counts as "leakage" and none defines a formula; the post defines its own and says so.
- Google guidance says no special optimization is needed for AI features, while GEO research reports gains from stats, quotes, and citations. These are reconcilable: the paper tests a research benchmark; Google speaks about eligibility. The post should follow the content-quality practices without promising citations.
- FAQ rich result is gone per Google's page; some house notes and many SEO pages still treat it as live.

## 11. Could not verify or find
- Real People Also Ask boxes and exact SERP rank order (tool returns no SERP feature data). Question list is derived from search results and reader need, not from scraped PAA.
- Any credible B2B manufacturer or distributor benchmark for inquiry capture rate. None found; the post says so (question 6).
- Whether ChatSKU can push website-chat inquiries into a CRM automatically beyond the RFQ-to-CRM/inbox statement in post 3956. Do not claim more.
- Whether HowTo structured data still earns any display in Google (not checked; do not rely on it).
- Whether the demo page's "about four hours" setup figure matches brand.md's "under a day"; use the brand.md wording.

## 12. Carousel hooks (for the later social step, not part of the blog)
Slide ideas that follow the framework: (1) "Monday question: how many quote requests last week? Three people, three answers." (2) The four doors. (3) The formula. (4) The 70-inquiry example landing on 59%. (5) Five fields every inquiry record needs. (6) What the count cannot see. CTA to the post. The scene-based visual style is a creator decision.
