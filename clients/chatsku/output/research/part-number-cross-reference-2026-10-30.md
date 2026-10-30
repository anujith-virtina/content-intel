---
title: Research notes, part number cross reference
client: chatsku
date: 2026-10-30
topic: part number cross reference for B2B distributors, manufacturers, wholesalers
audience: owners, sales and ecommerce managers at B2B distributors, manufacturers, wholesalers
stage: research
slug: part-number-cross-reference
---

# Research: part number cross reference

Companion file: competitor-analysis-pnxref-2026-10-30.md (5 pages, weaknesses, SERP gaps).

## Rules and uniqueness check (reported for the analyzer)

- Read in full: MUST-FOLLOW-RULES.md, voice.md, audience.md, brand.md, examples.md.
- Inventory grep: only 3 lines mention cross-ref/supersession/interchange (all passing mentions). Stale caveat: inventory is old; the analyzer must fetch https://chatsku.com/blog/ before finalizing, per rule in section 6.
- Slug `part-number-cross-reference` is not in the rules file slug list. Not verified against live site slugs.
- Format rotation: Format B is overused; recommended C, D, E or F below.
- Reminder from rules: max 2 external links, no competitor links, no em dashes, Dallas modifiers dropped.

## Sub-questions

1. What does a buyer with a competitor or OEM number actually want? (equivalent, fit, supersession, stock)
2. Why can't the distributor's website answer that today?
3. What separates a cross-reference from a supersession, and why does the difference decide the answer?
4. What must a trustworthy answer contain?
5. What should happen when no mapping exists?

## Intent analysis

Searchers fall into four jobs. The SERP serves job 1 mostly, and by manufacturer tools.

| Job | What the searcher wants | Served today by | Unanswered |
|---|---|---|---|
| 1. Find an equivalent | "I hold brand X number, what is yours?" | Manufacturer lookup tools (Samtec, Schroeder), vendor glossary pages | Independent distributors with multi-brand catalogs |
| 2. Check fit / spec match | "Is it a drop-in or just close? What differs?" | Samtec variances, Anglera equivalence levels | What "functional equivalent" means, who signed off, in plain buyer language |
| 3. Check supersession | "My number is dead. What replaced it, and does the old one still work in reverse?" | ERP help pages, OEM portals | Direction (one-way vs two-way); presenting it on a public site |
| 4. Check stock and next step | "Do you have it, price, can I order now?" | Almost nobody on the cross-reference page itself | Whole stock-plus-quote handoff after the match |

Sub-questions unanswered by the top pages:
- Where does the equivalency data live and who maintains it?
- What should the site say for a partial match?
- What happens when the buyer's number is not in the table?
- How does a buyer outside business hours get an answer?
- How should one competitor number that maps to several of your parts be presented?

## Existing ChatSKU coverage (fetched live 2026-10-30)

| Post | What it says (short) | Where |
|---|---|---|
| /how-ai-product-search-works/ | Cross-references named as the third of six failure modes; tables "keep their cross-reference tables in a spreadsheet". PAA H3 asks if AI search can handle competitor and OEM cross-reference numbers. Answer: "Only if those cross-references are in the data it can read." Ends: "The fix is a data fix, not a search fix." | H2 on why the search box fails; PAA |
| /traditional-b2b-product-search-fails/ | Bullet labeled "Cross-references nobody indexed." Says "Buyers routinely arrive holding a rival's part number." Equivalency table "lives in a spreadsheet on somebody's desktop." Zero-result cost scenario mentions checking the cross-reference sheet. | "Where does keyword search actually break?" and cost section |
| /b2b-catalog-ai-agent-readability-audit/ | Audit item: part numbers and cross-references must be on the page as text. "A buyer holding a rival's number should still land on yours." FAQ prioritizes "anything with a cross-reference." Notes only 2 of 5 readable pages had MPN or GTIN in structured data. | Checklist heading; FAQ |
| /what-is-agentic-commerce/ | One line: make sure cross-references are accurate so a buyer holding a rival's number finds your part. | Margin section |
| /who-b2b-catalog-assistant-is-built-for/ | No cross-reference language. Mentions buyers asking "whether a substitute meets a spec" and counting questions about substitutes. | Buyers and fit test |
| /chatgpt-vs-catalog-chatbot/ | No cross-reference language. A general model may suggest a "close equivalent" for a part not in the catalog; mentions a competitor's model number not in the catalog; "substitute-part questions." | "Will it make up an answer when it does not know?" |

Pattern: all six treat cross-reference as a one-sentence symptom or an audit checkbox. The recurring claim is "it lives in a spreadsheet." None explains the cross-reference data itself.

Already owned elsewhere, do not repeat:
- Spreadsheet-vs-index as a search failure (how-ai-product-search-works, traditional-b2b-product-search-fails).
- Text-and-structured-data readability checklist (agent-readability-audit).
- General "AI invents a close equivalent" risk (chatgpt-vs-catalog-chatbot).
- Retrieval mechanics: embeddings, BM25, RRF (how-ai-product-search-works). Do not re-explain.

### The open lane

The equivalency DATA itself: what a cross-reference record is, why a cross-reference, a supersession and an interchange are three different relationships, what each answer must carry (match type, differences, direction, date verified, stock, next step), who owns keeping it right, and how to answer when no mapping exists. In short, the answer design and data ownership, not the search failure and not the retrieval mechanism. Everything existing says "the table is in a spreadsheet"; nothing says what should be in the table.

Fences: do not re-argue search failure (traditional-b2b-product-search-fails); do not do a readability audit (b2b-catalog-ai-agent-readability-audit); link to how-ai-product-search-works for the retrieval mechanism instead of explaining it.

## Key findings (all sourced; fetched 2026-10-30)

### 1. Equivalence has levels, and a good record states which one
- Source: https://www.anglera.com/glossary/part-number-cross-reference (vendor glossary, secondary)
- Paraphrase: three levels: direct replacement, functional equivalent, application match. A record should also carry differences and a verification date.
- Why it matters: gives the post a vocabulary for "what the answer must say." Attribute to the concept, not as an industry standard.

### 2. Exact, partial, and variances is a workable answer shape
- Source: https://blog.samtec.com/post/find-competitor-cross-reference-matches-samtec-com/ (manufacturer blog, 2018/2019)
- Paraphrase: exact matches in one view, partial matches as suggestions, one competitor part mapping to several of the maker's parts, differences listed as variances.
- Why it matters: shows many-to-one is normal, and that the difference list is what makes a match usable.

### 3. Manufacturers themselves warn cross-references go stale
- Source: https://schroederindustries.com/cross-reference/ (manufacturer tool page)
- Paraphrase: the company says specs between makers may vary and it may not be told when an OEM changes a spec, so a listed match can be out of date.
- Why it matters: a primary admission that a cross-reference is a maintained asset, not a one-time import. Supports the data ownership lane.

### 4. Candidates, not approvals
- Source: https://www.getleo.ai/blog/supplier-part-number-cross-reference (vendor blog, Sept 2026)
- Paraphrase: results are candidates; certified assemblies still need sign-off; match on several attribute groups, not one dimension.
- Why it matters: supports an "assistant presents candidates with differences, humans approve exceptions" posture. This is a vendor stance, treat as practice not proof.

### 5. Supersession has direction
- Source: https://open-exam-prep.com/study-guides/ase-p2/inventory-merchandising/supersession-cross-reference-interchange (study guide, secondary; automotive context)
- Paraphrase: one-way supersession means the new number replaces the old but the old cannot be used where the new design is required. Two-way means fully interchangeable. Cross-reference means an equivalent from a different maker.
- Why it matters: the key distinction the SERP lacks. Concept is widely used in parts distribution but this source is not an OEM primary. Mark `[unverified against OEM source]` if the analyzer wants to attribute; safe to state as a general definition without a number.

### 6. Dealer ERP records are thin
- Source: https://help.intellidealer.com/intellidealer/Content/PSPP007.htm (product docs, one dealer ERP)
- Paraphrase: the cross-reference record is a linked part number plus an optional comment. No field for equivalence level or direction in that system.
- Why it matters: explains why the "rep's head" fills the gap. Applies to this product only; do not claim all ERPs work this way.

### 7. Distributors have offered competitor-number lookup for a long time
- Source: Alliance Truck Parts launch coverage, Feb 2012 (https://www.vehicleservicepros.com/...10631418/...)
- Paraphrase: a truck parts distributor launched a lookup accepting its own or a competitor's number, returning the suggested part plus local dealer links.
- Why it matters: buyer behavior is old; the website still often cannot do it. Press release, claims unverified.

## Data points

None used. No statistic was found with a primary source that supports a claim specific to this topic. Per client rule, prefer no stat. Candidates seen and REJECTED:
- Samtec "over 11 million products" and "up to 20 matches" (vendor tool detail, 2018, single source).
- Alliance "more than 30 product lines" (2012 press release).
- Brennan "over 200,000 competitor item numbers from over 60 competitors" and Hammond "25,000 parts crossed" appeared only in search snippets; their pages returned 403. Unverified; do not use.
- Existing ChatSKU readability audit "2 of 5 pages" is a ChatSKU internal test sample; it is a first-party number, do not recycle it as a stat.
- Baymard 48%: banned, not used.

## Conflicts and disagreements

- Vocabulary conflict: "interchange," "cross-reference," "equivalent," "substitute" are used loosely and inconsistently across sources (Anglera treats equivalence as three levels; Schroeder uses an asterisk for "functional equivalent" without defining it; Intellidealer defines cross-reference as any usable-in-place part). Resolution: the post should define its own terms once and use them consistently.
- Matching method: Anglera argues attribute-based matching beats hand-kept lists; Schroeder and Intellidealer present hand-kept lists as the working model. Unresolved; the post should stay out of method claims and focus on what the answer must contain.

## Semantic term list (14)

cross-reference table; competitor part number; OEM part number; aftermarket equivalent; interchange; supersession (one-way, two-way); equivalency table; MPN (manufacturer part number); GTIN; fitment; spec match; drop-in replacement; functional equivalent; obsolete or discontinued part; alternate part; "where used" is out of scope. Also useful: match type, variance, last verified date, no-match handoff.

## Product-fit guardrail

Supported by brand.md and the live ChatSKU posts: ChatSKU ingests PDFs, Excel, ERP exports and CSV; answers buyer questions grounded in that catalog data; refuses rather than invents (live post chatgpt-vs-catalog-chatbot and how-ai-product-search-works describe grounding and refusal); builds quotes and captures leads; one line of code, live in under a day; hands off to a human.

The post MAY say:
- If the equivalency table (spreadsheet, ERP export, CSV) is uploaded with the catalog, the assistant can answer from it in conversation, at any hour.
- The assistant answers from the rows it has; no row, no invented part; it hands the buyer to a person or captures the lead and quote request.
- A buyer holding a rival's number can get the answer without calling during business hours.
- The data fix comes first; the assistant is as good as the table.

The post MUST NOT say:
- ChatSKU generates, discovers or auto-builds cross-references or equivalency mappings.
- ChatSKU verifies fit, certifies equivalence or replaces engineering sign-off.
- Real-time stock from every ERP (brand.md lists "CRM/ecommerce/ERP sync" generally; do not promise live stock per ERP, and do not promise live supersession feeds from OEMs).
- ChatSKU maintains or updates the table when OEMs change numbers.
- Any claim that it handles supersession direction automatically; it can only repeat what the uploaded data states. If the table has a "direction" column, it can answer from it.
- Any invented customer, case study, accuracy percentage or time-saved number.
- Unverified: whether ChatSKU can ingest a multi-sheet or many-to-many table with columns like match type and notes without prep. Ask the client or test before showing a sample.

## Candidate angles (rotate off Format B)

1. **Format E, contrarian thesis: "Your cross-reference table is not a search problem, it is a record you never designed."** Thesis: the spreadsheet holds a part number pair and nothing else. Buyers need match type, differences, direction, verified date. Argue to redesign the record before buying any tool. Hand-off to how-ai-product-search-works for mechanics. Strongest differentiation from existing posts.
2. **Format D, decision tree / playbook: "A buyer sends a number that is not yours: five decisions your answer has to make."** Sequence: is it your number, a superseded number, a competitor number, a partial match, or no match? Each branch states what to show (exact, direction, variances, escalate). Highly practical; covers the no-match handoff gap on the SERP.
3. **Format C, listicle with opinions: "Seven things a cross-reference answer must say that your spreadsheet cannot."** Numbered opinionated points: match type, differences, direction, last verified, stock, price/quote path, who to call. Easy to scan, fits LLM-friendly style. Risk: overlaps the audit checklist; keep it about the answer not the page markup.

Format F (case study) is NOT recommended: no real client case exists and none may be invented.

## Red flags for the analyzer

- Keep dated/vendor sources hedged; no stats at all is acceptable.
- Interchange/supersession definitions rest on a secondary automotive source; phrase as general definitions.
- Brennan and Hammond pages returned 403; their numbers cannot be used.
- Several SERP results are scraped PDF mirrors; not sources.
- Overlap risk with traditional-b2b-product-search-fails (equivalency table "on somebody's desktop") and the audit post: avoid repeating those phrasings; 8-word uniqueness gate applies.
- Competitor names (Anglera, Leo AI, Samtec, Schroeder) must not be named or linked in the post per rules; use only as research.
- Link candidates (existing, verified live today by fetch): /how-ai-product-search-works/, /traditional-b2b-product-search-fails/, /b2b-catalog-ai-agent-readability-audit/, /chatgpt-vs-catalog-chatbot/. Their presence in the rules link list is NOT confirmed (the four slugs are not in the rules file list); the analyzer should confirm each returns 200 before linking.

## Couldn't find

- True ranked SERP data (search tool is not a rank tracker).
- Any primary-source statistic on cost of lost sales from failed cross-reference lookups. Do not invent one.
- An OEM primary source for supersession direction.
- Brennan and Hammond page content (403).

## Sources read

- https://www.anglera.com/glossary/part-number-cross-reference (secondary, vendor)
- https://www.getleo.ai/blog/supplier-part-number-cross-reference (secondary, vendor, 2026-09-21)
- https://blog.samtec.com/post/find-competitor-cross-reference-matches-samtec-com/ (primary for Samtec tool behavior, 2018/2019)
- https://www.vehicleservicepros.com/distribution/tool-distributor/press-release/10631418/alliance-truck-parts-alliance-truck-parts-launches-online-parts-cross-reference-tool (press release, 2012)
- https://schroederindustries.com/cross-reference/ (primary for its tool and disclaimer)
- https://help.intellidealer.com/intellidealer/Content/PSPP007.htm (product docs)
- https://open-exam-prep.com/study-guides/ase-p2/inventory-merchandising/supersession-cross-reference-interchange (secondary)
- The six ChatSKU posts at chatsku.com/{slug}/ listed above.
