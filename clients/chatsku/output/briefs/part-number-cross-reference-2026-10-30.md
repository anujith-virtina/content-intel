---
title: Part number cross reference, content brief
client: chatsku
date: 2026-10-30
topic: part number cross reference as a designed record, not a lookup list
audience: owners, sales and ecommerce managers at B2B distributors, manufacturers, wholesalers
stage: brief
slug: part-number-cross-reference
---

# Brief: part number cross reference

Research inputs: `output/research/part-number-cross-reference-2026-10-30.md`, `output/research/competitor-analysis-pnxref-2026-10-30.md`.

## 1. Thesis, format, keywords

**Thesis (one sentence):** A cross-reference table is a record nobody designed. It stores two part numbers, but the buyer needs a decision, so every row must state match type, what differs, direction, last-verified date, stock, and the next step.

**Why this angle, why now, why ChatSKU:**
- Gap: every existing ChatSKU post treats cross-reference as a one-line symptom. None says what belongs in the record. The SERP (manufacturer lookup tools, ERP help pages, scraped PDFs) has no buyer-facing, distributor-side piece on answer design or data ownership.
- Why defensible for ChatSKU: an assistant only answers from rows it has. The data fix comes first, and that is ChatSKU's honest position.
- Primary keyword: `part number cross reference`. Secondaries: competitor part number cross reference, OEM cross reference lookup, equivalent part finder.

**Format chosen: E (contrarian thesis).**
- Reason: the post argues against the common belief that cross-reference is a search or lookup problem, and for treating it as record design.
- Recency check (inventory file plus live briefs; the inventory file itself stops at post 3066, so later posts come from briefs and project notes):
  - Known recent order, newest first: bigcommerce-chatbot-quoting brief 2026-10-22 = D; 3305 buyers guide = E; 3294 sales KPIs = A; 3281 MOQ = not confirmed; 3066 = C; 3039 tiered pricing = not confirmed; 3023 = B; 3010 = D; 2974 = E; 2869 = F.
  - Counts in that window: E = 2, D = 2, A = 1, C = 1, B = 1, F = 1. No format has 3 or more, so E is allowed (E reaches 3 only if 3281 or 3039 is E; the inventory has no record of either, so confirm before drafting).
- Overused and skipped: B (flagged as overused in the inventory's earlier posts; also skipped per the instruction). D is not chosen because it was used on the immediately preceding brief.
- OPEN ITEM: formats of 3281 and 3039 could not be confirmed from the files. If either is E, the E count becomes 3 and this choice breaks the rotation rule. Orchestrator to check.

**Fences (do not do):**
- Do not re-argue search failure (`/traditional-b2b-product-search-fails/`).
- Do not rebuild the readability checklist (`/b2b-catalog-ai-agent-readability-audit/`).
- Do not explain embeddings, BM25 or retrieval. One link only (`/how-ai-product-search-works/`).
- Do not write a case study or use any number.

## 2. Uniqueness audit

| Check | Result |
|---|---|
| Slug `part-number-cross-reference` vs known slugs (rules list, inventory, web search of chatsku.com on 2026-10-30) | PASS (no collision found; a full live slug crawl was not possible, so the REST slug check at push time is the final gate) |
| Title shares no 3+ consecutive meaningful words with any known title | PASS (known titles checked: MOQ, tiered pricing, quote response time, BigCommerce, WooCommerce guides, readability audit, how AI product search works, traditional search fails, agentic commerce posts; none contain "part number cross reference" or "record nobody designed") |
| Angle vs how-ai-product-search-works (cross-reference as failure mode 3, PAA answer "only if in the data") | PASS (this post owns what the data holds, not the retrieval fact) |
| Angle vs traditional-b2b-product-search-fails ("Cross-references nobody indexed", spreadsheet scenario) | PASS if the creator avoids the symptom framing; this post starts after the symptom |
| Angle vs b2b-catalog-ai-agent-readability-audit (cross-reference as audit item, text on page) | PASS (no markup or checklist content) |
| Angle vs what-is-agentic-commerce (one margin line) | PASS |
| Angle vs who-b2b-catalog-assistant-is-built-for (substitute questions mention) | PASS |
| Angle vs chatgpt-vs-catalog-chatbot (general model invents a close equivalent) | PASS if the creator does not argue the invention risk; only the refusal behavior appears, briefly |
| Format rotation | PASS provisionally (see open item on 3281 and 3039) |
| Stale-inventory rule (fetch /blog/) | PARTIAL: a site-restricted web search was run; the blog index itself was not fetched. Orchestrator to confirm no cross-reference post went live since 2026-10-22. |

## 3. Title and meta

**Final H1:** Part number cross reference: the record nobody designed (55 chars)
**Alternate 1:** Your part number cross reference is a record, not a list (58 chars)
**Alternate 2:** Why a part number cross reference table fails buyers (53 chars)

**Meta title (57 chars):** Part number cross reference: design the record | ChatSKU
**Meta description (159 chars):** A part number cross reference needs more than a pair of numbers. See the six fields every row needs, from match type to next step, and what to say on no match.

## 4. Outline (target 1,800 to 2,300 words; plan about 2,100)

All headings sentence case. Body H2s are question-style with the direct answer in the first sentence. Short sentences (20 words or fewer), paragraphs of 3 sentences or fewer, second person.

| Section | H2 | Plan words |
|---|---|---|
| Executive Summary | Executive Summary | 110 |
| Introduction | Introduction | 180 |
| Body 1 | What does a buyer holding another maker's number need? | 190 (no H3, stay under 200) |
| Body 2 | Is a cross-reference the same as a supersession? | 330 (H3s required) |
| Body 3 | What should one cross-reference record hold? | 380 (H3s required) |
| Body 4 | Who keeps the table right? | 230 (H3s required if over 200) |
| Body 5 | What should the answer say when there is no match? | 260 (H3s required) |
| PAA | People Also Ask | 170 |
| Conclusion | Conclusion | 110 |
| FAQ | Frequently Asked Questions (after Conclusion) | 300 |

### Executive Summary
- Point: a cross-reference row that holds two numbers cannot answer a buyer. Name the six fields, the four relationship types, and the no-match rule.
- Evidence: none needed. State the thesis and the sequence of the article.
- Terms: cross-reference table, competitor part number, match type, direction, last verified date.

### Introduction (buyer scenario, not a definition)
- Point: a buyer holds a competitor or OEM number, finds your site, and gets nothing useful, or a bare number with no context.
- Evidence: a clearly labelled hypothetical. Example: a maintenance buyer has a worn part with a stamped number from another maker and a line that is down. Your counter rep would ask three questions. Your table asks none. Label it "picture this" or "say a buyer" so it reads as hypothetical. No stats.
- Close the intro with the thesis in two sentences. No links in the intro.
- Terms: OEM part number, aftermarket equivalent, drop-in replacement, competitor part number cross reference.

### Body 1: What does a buyer holding another maker's number need?
- Point: a decision (will it fit, what differs, can I have it now), not a lookup.
- Evidence: reasoning only. List the four jobs from the research (find an equivalent, check fit, check supersession, check stock and next step) in prose, one sentence each. A short list is acceptable here only because it is list-shaped (four jobs).
- Link here: retrieval mechanics pointer, one sentence: "How the search layer reads your data is a separate topic" with link to `/how-ai-product-search-works/` (anchor: retrieval mechanics). Optional second link to `/traditional-b2b-product-search-fails/` (anchor: keyword search failures), one clause only, no re-argument.
- Terms: OEM cross reference lookup, equivalent part finder, spec match, fitment, alternate part.

### Body 2: Is a cross-reference the same as a supersession?
- Point: no. They are different relationships, and the difference decides the answer.
- Required element: a compact table with columns Term, Whose number, Direction, What the buyer is told. Rows: cross-reference, supersession, interchange, substitute. Define each once and use it consistently afterwards (research flagged inconsistent vocabulary across sources). Hedge: "as most parts counters use the words" and state these are general definitions, not an OEM standard. Mark nothing as a statistic.
  - Cross-reference: an equivalent from a different maker.
  - Supersession: same maker, new number replaces old. One-way means the old part may not work where the new design is required. Two-way means fully interchangeable.
  - Interchange: parts that can be used in place of each other; usually two-way. Say this is how it is commonly used.
  - Substitute: a close part you suggest that is not an established match, offered with differences stated.
- H3 1: "Why direction changes the answer" (one-way vs two-way, in prose; hypothetical: a buyer holds the old number versus the new number).
- H3 2: "Why one competitor number can map to several of your parts" (many-to-one is normal; each candidate needs its own differences).
- Terms: supersession, interchange, one-way, two-way, obsolete or discontinued part, functional equivalent, equivalency table.
- Link: `/minimum-order-quantity-b2b/` is NOT here (placed in Body 3).

### Body 3: What should one cross-reference record hold?
- Point: six fields beyond the two numbers: match type, what differs, direction, last-verified date, stock, next step.
- Evidence: one example record, clearly labelled "Hypothetical example" and using invented neutral part numbers (for example "Maker A model 4410" and "your SKU 77-210"). Lay out as a two-column field list or small table: Field / What it says. Show the buyer-facing sentence the record produces. Keep any numbers inside the example obviously fictional and not statistics.
- H3 1: "The six fields" (one sentence of why each exists; match type uses three levels: direct replacement, functional equivalent, application match; treat as a way of describing, not an industry standard).
- H3 2: "What the buyer sees" (the example record turned into a two-sentence answer; shows candidates not approvals: "a person signs off on certified assemblies").
- H3 3 (optional if word count permits): "Where the next step leads" (quote, hold, or a person; link to `/minimum-order-quantity-b2b/`, anchor: minimum order rules, because the next step often hits a minimum or pack size).
- Link: `/b2b-catalog-ai-agent-readability-audit/` (anchor: catalog readability audit), one clause saying the numbers must be readable text, handled there.
- Terms: match type, variance, last verified date, candidate match, drop-in replacement, MPN, GTIN.
- Stat discipline: no number.

### Body 4: Who keeps the table right?
- Point: someone must own it, with a review trigger, or it goes stale.
- Evidence: reasoning plus the general observation, paraphrased with no name, that some manufacturers publish a disclaimer saying specs between makers can differ and they may not be told when an OEM changes one. Do not name the manufacturer or link it. Also: many ERP part records hold a linked number and a free-text note, with no field for match type or direction. Hedge: "many" and "some", never "all ERPs".
- Practical content: one named owner (role, not a person); a date stamp per row; review triggers (supplier change notice, a returned part, a buyer complaint, a catalog update); where the table lives (ERP note, spreadsheet, rep memory) and why rep memory is the single point of failure. Avoid the phrase "on somebody's desktop".
- Link: `/erp-export-ai-agent-ready/` (anchor: ERP export check), one sentence about exporting the table with its fields intact.
- ChatSKU mention 1 (soft, factual): the assistant answers from the table as uploaded. If the table is wrong, the answer is wrong. The data fix comes first.
- Terms: aftermarket equivalent, OEM part number, equivalency table, discontinued part.

### Body 5: What should the answer say when there is no match?
- Point: say there is no confirmed match, say what you can do next, and never guess a close part.
- Evidence: reasoning with a labelled hypothetical: a buyer's number is not in the table at 8pm. Compare a bad answer (a guessed near-match) with a good one (no confirmed match, here is how to get one, capture the details). Candidates, not approvals.
- H3 1: "What a good no-match answer contains" (state the gap, ask for the specs or a photo, capture contact and quantity, tell the buyer when a person will follow up).
- H3 2: "How to hand the buyer to a person" (route to a rep, include the buyer's number and any specs in the handoff so nobody re-asks).
- Links: `/who-b2b-catalog-assistant-is-built-for/` (anchor: catalog assistant fit) and `/ai-product-search-for-b2b/` (anchor: AI product search) and `/features/` (anchor: supported catalog files), each in a different paragraph, none as a pitch.
- ChatSKU mention 2: if the table is uploaded with the catalog (PDF, Excel, ERP export, CSV), the AI catalog assistant answers from the rows it has, refuses when there is no row, then hands off to a person or captures the quote request, at any hour.
- Terms: no-match handoff, alternate part, functional equivalent, equivalent part finder, spec match.

### People Also Ask (H3 questions, 40 to 60 word answers each, answer in first sentence)
1. What is a part number cross reference?
2. How do you find the equivalent of a competitor part number?
3. Can a cross-reference be one-way?
4. Is an aftermarket equivalent the same as an OEM part?
(Keep definitions short; do not repeat the Body 2 table.)

### Conclusion
- Point: design the record first, then decide who or what delivers it. Restate the six fields in one sentence.
- Soft CTA only here, once: the button widget links to `/demo/`. Body text carries no inline CTA link. Offer: see the live demo or start a free trial (`/signup/`) with a table uploaded. ChatSKU mention 3 is this CTA.
- Do not add links in the conclusion text.

### FAQ (after Conclusion; 5 questions; 40 to 70 words each; no repeat of PAA)
1. Who should own the cross-reference table?
2. How often should a row be re-verified? (answer: on a trigger and a calendar review; give no number)
3. Can an assistant approve a substitute for a certified assembly? (no: candidates, with sign-off by a person)
4. What file format should I use to upload a cross-reference table? (CSV or Excel, one row per pair is the cleaner shape; say ChatSKU ingests PDF, Excel, ERP, CSV, but do NOT claim it handles many-to-many tables without prep; flag in draft review)
5. What if I have no cross-reference table yet? (no number. Start with the competitor part numbers buyers ask about most, record those first, and grow the table from the questions reps answer by hand.)

## 5. Product guardrail (copied from research)

**ChatSKU may say:**
- If the equivalency table (spreadsheet, ERP export, CSV) is uploaded with the catalog, the assistant answers from it in conversation, at any hour.
- It answers from the rows it has. No row, no invented part. It then hands the buyer to a person or captures the lead and quote request.
- A buyer holding a competitor's number gets an answer without calling during business hours.
- It ingests PDF, Excel, ERP exports and CSV (brand.md).
- The data fix comes first. The assistant is as good as the table.

**ChatSKU must NOT be said to:**
- Generate, discover or auto-build cross-references or equivalency mappings.
- Verify fit, certify equivalence or replace engineering sign-off.
- Give real-time stock from every ERP, or live supersession feeds from OEMs.
- Maintain or update the table when OEMs change numbers.
- Handle supersession direction automatically (it only repeats what the data states; a direction column would be answerable).
- Ingest many-to-many or multi-sheet tables without prep (unverified; ask the client or test before asserting either way).
- Any invented customer, accuracy percentage, or time-saved number.

**Placement:** at most three natural mentions: Body 4 (data fix first), Body 5 (answers from rows, refuses, hands off), Conclusion (soft CTA). Not in every section. Use "AI catalog assistant", never "chatbot" alone.

## 6. Link plan (internal only; body sections only)

| # | Anchor (2 to 5 words) | URL | Section |
|---|---|---|---|
| 1 | retrieval mechanics | /how-ai-product-search-works/ | Body 1 |
| 2 | keyword search failures | /traditional-b2b-product-search-fails/ | Body 1 (one clause; drop if it feels like re-arguing) |
| 3 | catalog readability audit | /b2b-catalog-ai-agent-readability-audit/ | Body 3 |
| 4 | minimum order rules | /minimum-order-quantity-b2b/ | Body 3 |
| 5 | ERP export check | /erp-export-ai-agent-ready/ | Body 4 |
| 6 | catalog assistant fit | /who-b2b-catalog-assistant-is-built-for/ | Body 5 |
| 7 | AI product search | /ai-product-search-for-b2b/ | Body 5 |
| 8 | supported catalog files | /features/ | Body 5 |

- `/demo/` and `/signup/` appear only via the conclusion button and, if the orchestrator wants, one FAQ answer. No other uses.
- No links in the intro, executive summary, PAA or conclusion text.
- External links: zero. The research read vendor and manufacturer pages, none authoritative enough to cite, so none are used.
- Never name or link competitors. The research vendor names (Anglera, Leo AI, Samtec, Schroeder, Intellidealer) must not appear.
- No "our" in link sentences (no "our guide", "check out our").
- Note for verification: rules file marks `/minimum-order-quantity-b2b/` as draft at its last update, but a web search on 2026-10-30 shows it live. Confirm 200 before the push.

## 7. Phrasing fence (avoid so the 8-word duplicate check passes)

Do not reuse from other ChatSKU posts:
- "spreadsheet on somebody's desktop", "lives in a spreadsheet", "keep their cross-reference tables in a spreadsheet"
- "rival's part number", "rival's number", "a buyer holding a rival's number should still land on yours"
- "Cross-references nobody indexed"
- "The fix is a data fix, not a search fix", "Only if those cross-references are in the data it can read"
- "anything with a cross-reference"
- "make sure cross-references are accurate"
- "close equivalent" (from chatgpt-vs-catalog-chatbot), "whether a substitute meets a spec"
- "selling to software since 1979", "one line of code, live in under a day" in the exact form used elsewhere (vary the wording; avoid a verbatim 8-word match)
- "night-shift sales rep" in a repeated boilerplate sentence
Say instead: "another maker's number", "a competitor's number", "stamped number", "the table", "the record".
Also vary the boilerplate sentence describing what ChatSKU ingests; do not copy it from brand.md or other posts.
The creator should run a local 8-gram check against all live posts before handoff.

## 8. Images (860x452, realistic, no text in image)

- **Featured:** a parts counter at a distributor, a counter worker holding a worn metal component beside a monitor showing a product list. Reason: it shows the "buyer holds a number, needs a decision" moment.
- **Body image 1 (Body 2 or 3):** hands comparing two similar mechanical parts side by side on a workbench. Reason: it visualizes "same job, what differs" without text.
- **Body image 2 (Body 5):** a warehouse aisle at low light with a laptop on a desk in the foreground. Reason: it signals the after-hours, no-one-at-the-counter case.
- Rules: visual QA of 6+ candidates per slot, avoid two images from the same photoshoot, alt text 80 to 150 chars with 1 to 2 keywords, written after choosing the image. Image widget after the text-editor in each section.

## 9. Style reminders

- No em dashes anywhere (including the headings and the meta).
- Sentences 20 words or fewer. Paragraphs 3 sentences or fewer.
- Second person ("you", "your"). Sentence case headings.
- Banned: "AI-powered" as filler, "chatbot" alone, "solutions" as filler, delve, leverage, navigate (verb), landscape, ecosystem, revolutionary, game-changing, cutting-edge, "in conclusion".
- Never: "replaces your sales team", "just a chatbot", "Schedule a demo to learn more".
- Direct answer in the first sentence of each body H2 and each PAA and FAQ answer.
- Every example is hypothetical and labelled. No invented statistics, customers, case studies or quoted numbers. Where a number would help, argue without one.
- Bullets only for list-shaped content (the four buyer jobs, the six fields). Otherwise prose.
- Required H2s: Executive Summary, Introduction, People Also Ask, Conclusion, Frequently Asked Questions.
- Word count 1,800 to 2,300; include a TOC only if the final count passes 2,000 (optional).

## 10. Creator judgment vs locked

- **Locked:** thesis, format E, H1, section order, the table, the example record, the guardrail, the link list, the phrasing fence, zero external links.
- **Creator judgment:** the exact hypothetical scenario wording, which alternate heading wording reads best, whether to keep link 2, FAQ phrasing.

## 11. Unresolved

1. Formats of posts 3281 and 3039 could not be confirmed. If either is E, the E rotation count hits 3.
2. The blog index was not fetched directly; only a site-restricted search ran.
3. Whether ChatSKU ingests many-to-many cross-reference tables without prep is unverified. Do not assert either way.
4. Interchange and supersession definitions rest on a secondary automotive source; present them as general usage.
