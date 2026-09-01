---
title: How AI product search actually works for B2B catalogs
client: chatsku
date: 2026-08-18
topic: AI product search for B2B — informational companion to the /ai-product-search-for-b2b/ landing page
audience: Owners, sales managers, ecommerce and ops managers at B2B manufacturers, distributors, and wholesalers ($1M–$50M revenue). Industry-fluent, not engineers.
stage: brief
slug: how-ai-product-search-works
research: clients/chatsku/output/research/ai-product-search-b2b-2026-08-18.md
---

# Brief: How AI product search actually works for B2B catalogs

## Final title, slug, and metadata

- **H1 / title (sentence case):** How AI product search actually works for B2B catalogs
- **Slug:** `how-ai-product-search-works` — **confirmed.** It matches the informational query the landing page's own FAQ asks and answers in one sentence, and it leaves `ai-product-search-for-b2b` cleanly to the money page. Same companion pattern as posts 1300 (`what-is-the-response-gap` vs `/response-gap/`) and 1056 (`magento-b2b-chatbot-integration` vs `/magento-b2b-chatbot/`).
- **Primary keyword:** AI product search (B2B qualifier carried in the title, H1, and first sentence)
- **Secondary keywords:** how does AI product search work, semantic search B2B catalog, hybrid search B2B ecommerce, B2B site search failure
- **Meta title (44 chars):** `How AI Product Search Works for B2B | ChatSKU`
- **Meta description (158 chars):** `AI product search turns your catalog into vectors, runs keyword and meaning-based retrieval together, and answers only from real records. Here is how it works.`
- **Category:** Chatbot (29). Not DFW Local.

## Format

**Format B — conversational Q&A (LLM-style), with a Format E contrarian spine running through sections B5 and B6.**

**Reason:** the post's entire job is to answer, in 300–400 words each, the questions the landing page's FAQ answers in one line each. That is Format B by definition, and it is the exact structure of the two proven companion posts on this site (1300 and 1056). It also satisfies the house AEO rule with no extra work: every body H2 is a buyer question answered direct-answer-first.

**Correction to the record (the analyzer flags this rather than repeating it):** the task brief stated Format B "has never been used for ChatSKU." That is not accurate. Format B is the **most-used** format in the inventory (posts 251, 266, 277, 353, 380, 397, 685, 1056, 1300, 1455) and it appears **3 times in the last 10 posts** (1455, 1300, 1056). Format C also appears 3 times (1880, 1820, 1684). Under the strict "no format used in 3+ of the last 10" test, both B and C would be disqualified and the honest alternatives would be E (used once, 1538) or F (used once, 299).

**The call, and why Format B still wins on merit:** MUST-FOLLOW section 11's actual ChatSKU rule is "do not use Format A for more than 1 of the next 3 posts; pick the format that best fits." A is out (used on 2129 and 2044). D was the immediately preceding post (2422), so repeating it is a second consecutive use. Format B is the right structural fit and is now three posts back. To offset the repetition, sections **B5 and B6 carry an explicit Format E contrarian argument** (pure semantic search is worse than a keyword box on part numbers), which no prior Format B post on this site has done. The post reads as a mechanism explainer with a contrarian centre, not as another Q&A rerun.

- **Length:** body prose **2,400–2,600 words**. Rendered with PAA, FAQ, and conclusion, approximately **3,100–3,300**. Consistent with post 353 (2,780 draft / ~3,500 rendered) and 1684.
- **Reading time:** 11–13 minutes.

## Thesis

> AI product search is not "the search box got smarter"; it is three separate mechanisms working together, and the one every competitor article celebrates, meaning-based semantic search, is the one that fails hardest on exactly the part numbers and grade codes a B2B catalog is made of.

## Why this, why now, why us

- **Why this angle:** every article on this SERP runs the same three beats, keyword search is dumb, semantic search understands intent, buy our product. None explain embeddings in plain language. None admit that on out-of-domain, exact-match retrieval, BM25 beats dense retrieval, which is the single most operationally important fact for a distributor. And none map measured search-failure rates by query type onto the query types B2B buyers actually live in. Those three moves are the post.
- **Why now:** `/ai-product-search-for-b2b/` is live at ~3,200 words and ranks for commercial intent. It has zero statistics, zero citations, and answers "how does AI product search work?" in one mechanism-free sentence. The informational half of the keyword is unclaimed, by us and by everyone else writing for this audience.
- **Why this client:** ChatSKU's whole positioning is "your existing messy catalog is enough." That claim is only credible if we can explain what happens to the catalog. Education-first is also the correction the user has now issued twice (posts 1455 and 2422, plus the "too promotional, didn't feel like a blog" rejection on 2044).

## Strategic frame: this post must not cannibalise the landing page

| | `/ai-product-search-for-b2b/` (landing page) | This post |
|---|---|---|
| Intent | Commercial / evaluation | Informational / mechanism |
| Question owned | "Can ChatSKU do this for my catalog?" | "How does this actually work?" |
| Evidence | None. Zero stats, zero citations. | 5 verified stats, 2 external citations, 4 papers named |
| Tone | Assertive product claims | Explanatory, and honest about failure modes |
| Relationship | Receives 2 links with varied anchors | Hands commercial intent back to the landing page |

**The opening premise:** the landing page's FAQ answers "How does AI product search work?" with roughly "it connects to your catalog, understands your product data, and matches buyer requests to real stocked products." That sentence is true and it is not an explanation. Say so, in our own voice, without quoting our own marketing copy back at the reader. That admission is the post's reason to exist and its credibility opener.

## Audience

The ops manager or owner at a $5M–$30M distributor who already has a search box and knows it is failing. They can read "vector" and "index" without panic but will close the tab on "high-dimensional latent space." They are evaluating, not researching. They want to leave with: a definition they can repeat to their boss, one specific question to ask any vendor, and one test they can run in a demo. They must get all three without buying anything.

## Structure

Every body H2 is a buyer question. Every one leads with a direct answer in the first sentence, before any setup. Structural labels stay verbatim: **Executive summary**, **People also ask**, **Conclusion**, **Frequently asked questions**.

### Executive summary (H2, verbatim label) — 130 words

Answer-first, no scenario, no ChatSKU mention (precedent: post 2044). Three short paragraphs: what AI product search is in one sentence; the three mechanisms (meaning-based retrieval, exact keyword retrieval, structured spec filters, plus grounding on top); and the counterintuitive part, that the "AI" half of it is the half that fails on part numbers, which is why good systems keep the old keyword search running.

### Introduction (H2, structural label) — 170 words

**Hook (locked, do not substitute):** the substitution query. A buyer types something like *"same as the 2-inch one we bought last year, but in stainless."* No filter UI ever built can express that query. It requires knowing what they bought, which attribute is being varied, and which attributes must hold constant.

Then the pivot: ask any vendor how their AI search handles that and you get a sentence like "it understands your product data." We publish a version of that sentence ourselves. This post is the version with the mechanism in it.

- **Internal link 1:** `/ai-product-search-for-b2b/`, anchor **"AI product search for B2B"**.
- Do not use the hinge example anywhere in the post. That belongs to the landing page.

### B1. What is AI product search, in one sentence you could repeat to your boss? — 150 words

**Leads with:** "AI product search is a search system that matches a buyer's plain-language description to real products in your catalog, using meaning, exact strings, and structured specifications at the same time, and answers only from records that actually exist in your data."

Then the boundary the reader needs: this is not autocomplete, not synonym lists, and not a filter UI with a nicer skin. It is also not the same as having a catalog with no search at all, which is a different problem.

- **Internal link 2:** `/passive-catalog-costing-you-sales/`, anchor **"what a passive catalog is"**.
- Do not restate the landing page's one-sentence definition. Ours is the mechanism-bearing version.

### B2. Why does your search box fail when a buyer types "SS316 3/4 NPT"? — 300 words

**Leads with:** "Because a keyword box matches strings, not meaning. Your catalog says 'stainless steel 316.' The buyer typed 'SS316.' To the search index those are two unrelated pieces of text."

Name BM25 once, define it in half a sentence (the ranking algorithm behind most classic search boxes), and credit what it is genuinely good at: it is fast, precise, and explainable on exact terms. Do not strawman it. That fairness is what makes B5 land.

Then the B2B failure taxonomy **in prose with mechanism, not as a stuffed bullet list**. Use these six, which the landing page never covers:

1. Abbreviation and trade shorthand ("SS316" vs "stainless steel 316")
2. Part-number formatting drift ("ABC-1234", "abc1234", "ABC 1234" are one product to a human, three strings to a database)
3. Competitor and OEM cross-references, which usually live outside the search index entirely
4. Compatibility queries ("the seal that fits pump XY-2000"), which need a relationship the catalog stores implicitly or not at all
5. Unit-of-measure mismatch (buyer thinks in feet and cases, catalog is in metres and eaches)
6. Substitution intent, the hook query, which no filter UI can express

- **Stat:** Baymard, 56% of sites fail to adequately support users' search needs, from a benchmark of 170+ sites and 10,000+ performance ratings, updated April 2026. **External link 1 goes here.**
- **Internal link 3:** `/convert-pdf-catalog-to-website/`, anchor **"make a PDF catalog searchable"** (for readers whose catalog has no search index at all).
- Maximum 6 items. Do not run all 10 from the research file. Prose with mechanism beats a list of examples.

### B3. Are the searches B2B buyers rely on most the ones that fail most often? — 290 words

**Leads with:** "On the best evidence available, yes. The three query types with the worst measured failure rates are the three a B2B buyer uses all day."

The mapping, which is this post's original contribution:

| Baymard's worst-performing query types | The B2B query it maps to |
|---|---|
| Abbreviation and symbol searches, **54%** of sites have issues | "SS316", "1/2-13 UNC", "3/4 NPT" |
| Compatibility searches, **44%** | "fits pump XY-2000" |
| Use-case searches, **43%** | "for an outdoor gate", "for a caustic line" |

**Mandatory honesty paragraph, non-negotiable, in the creator's own words:** Baymard's benchmark measures general ecommerce, not B2B. There is no B2B-specific, independently audited study of onsite search failure that survives verification. The mapping above is **our argument from the data, not measured B2B data**, and the post must say that plainly in a full sentence. Label it as reasoning. Do not present it as a B2B finding.

Close with the stakes, hedged the same way: Constructor's "Beyond Relevance" study of 609 million searches across 113 retail sites (Oct–Dec 2024) found searchers were 24% of visitors but drove 44% of revenue, converting at 2.5x non-searchers. **State in the sentence that this is retail data.** The transferable point is that search is a revenue surface, not a utility.

- **Internal link 4:** `/roi-calculator/`, anchor **"model the revenue impact"**. We cannot put a number on lost B2B search revenue, because none survives verification. Let the reader model it instead.
- Constructor is cited **by name with methodology, not linked** (external link budget, see below).

### B4. What actually happens when a system "learns" your catalog? — 300 words

**Leads with:** "Nothing gets memorised, and no model gets retrained on your products. Every product's text is converted into a long list of numbers called a vector, and those numbers encode what the product means."

Plain-language explanation, no maths:
- Each product description becomes a set of coordinates. Products that mean similar things land near each other.
- The buyer's sentence gets converted the same way. The system looks for whatever is closest.
- "Closest" is a real, measurable distance, not a vibe. That is the whole trick.
- The store that holds these and finds neighbours fast is a vector database. Cite AWS's documentation **by name only, no link**, for the "high-dimensional points, ranked by distance" framing.

**The myth-buster that earns this section:** "learns your catalog" does not mean the AI now knows your products by heart. It means your catalog was converted into a form the system can measure similarity against. If your catalog changes, that conversion has to be redone. This directly explains the phrase the landing page uses and never defines.

- **Image slot 1 goes here.**
- Do not reuse post 353's "reads your catalog, not the internet" phrasing or any variant of it.

### B5. If meaning-based search is smarter, why do serious systems still run keyword search? — 380 words

**This is the credibility anchor. Do not soften it. Do not hedge it into mush.**

**Leads with:** "Because on a catalog full of part numbers, grade codes, and thread specs, meaning-based search on its own is often worse than the plain keyword box you already have."

The evidence: BEIR (Thakur et al., NeurIPS 2021 Datasets and Benchmarks Track) evaluated 10 retrieval systems across 18 datasets and found BM25 to be a robust baseline that dense retrieval models often underperform in zero-shot, out-of-domain settings. Translate "out-of-domain" in one sentence: **your specialist catalog is nothing like the general text the embedding model was trained on.** That is the exact condition BEIR measures.

**Required caveat, one sentence:** BEIR is from 2021 and embedding models have improved since. The takeaway is not "vectors don't work." It is "this is why keyword retrieval never left."

Then hybrid retrieval as the actual answer, framed as the design choice rather than a compromise: run both searches in parallel and fuse the two ranked lists by **position** rather than score, so two incompatible scoring scales never have to be reconciled. Name Reciprocal Rank Fusion once and describe it in plain terms. Mention that the weighting between the two is a dial, not a fixed setting.

**Include the post's one table here.** Three rows, a completely different axis from the landing page's 8-row table (which compares a buyer's need against traditional search and ChatSKU). Ours compares retrieval methods:

| Retrieval method | What it is good at | Where it fails | The B2B query it handles |
|---|---|---|---|
| Keyword / lexical (BM25) | Exact strings, speed, explainability | Different wording for the same thing | "ABC-1234", "SS316" |
| Meaning-based / dense vectors | Paraphrase, description, application | Exact identifiers, out-of-domain jargon | "for an outdoor gate" |
| Hybrid, both fused | Both of the above in one ranked list | Still needs spec filters on top (see B6) | "SS316 hinge for an outdoor gate" |

**The takeaway the reader leaves with, state it explicitly:** when you evaluate any AI search tool, ask whether it still does exact matching on part numbers alongside the AI. If the answer is a version of "we use AI now," that is a red flag.

- **External link 2 goes here** (BEIR, arXiv).

### B6. How does it handle "316 grade, 1/2 inch NPT" without guessing? — 250 words

**Leads with:** "It doesn't rely on similarity for those at all. It pulls the specifications out of the sentence, turns them into filters, and applies them as hard rules."

The reasoning, framed as engineering rationale rather than a cited claim: an embedding encodes approximate meaning. A specification is an exact fact. "Roughly similar" is a correct answer for "outdoor gate" and a wrong answer for 316 versus 304, where the difference is a corrosion failure six months later.

So the sentence gets split into two things:
- **Hard constraints**, applied as filters: size = 1/2 inch, thread = NPT, material grade = 316, pressure rating ≥ 150.
- **Soft meaning**, handled by retrieval: "for a caustic line" implies chemical compatibility, which no filter box on your site has ever had.

Note that this is an active research area, not a solved one. Reference the Query Attribute Modeling work (Menon et al., 2025) **by name only, no link**, as evidence that extracting structured filters from free-form queries is treated as its own problem in the field.

- **Worked example must be a valve, gasket, bearing, or motor. Not a hinge.** Recommended: the 1/2 inch NPT 316 stainless ball valve for a caustic line.
- Do not build this as a four-card structure. The landing page owns the four-buyer-phrasing card layout.

### B7. What stops it from inventing a part number that doesn't exist? — 310 words

**Leads with:** "Retrieval first, then generation. The system finds real records in your catalog before it writes a word, and it is constrained to answer from those records rather than from anything it absorbed in training."

Name retrieval-augmented generation once and define it in plain language, citing Lewis et al. (NeurIPS 2020) **by name only, no link**: combining what a model learned in training with records retrieved at question time produces more specific and more factual answers, and makes provenance possible. Provenance is the point. Every answer can be traced to a record.

**Then the honest half, which is what makes this section worth reading:** grounding reduces hallucination. It does not eliminate it. The hard case is the out-of-knowledge-base question, the one your catalog simply cannot answer. Reference the Know Or Not / PolicyBench work (Foo et al., 2025) **by name only, no link** as evidence that "does the system correctly refuse?" is a real, measurable engineering property that people build test suites for.

The four guardrails that matter, in prose:
1. Retrieve before answering, never answer from memory.
2. Answer only from what was retrieved.
3. Label a near match as a near match, out loud.
4. Refuse and hand off to a human when nothing supports an answer.

**The test the reader leaves with, state it as a direct instruction:** in any demo, ask the assistant for something you deliberately do not stock. Watch what it does. A system that invents a plausible part number just told you everything you need to know.

- **Image slot 2 goes here.**
- Do not reuse the landing page's three trust-card labels ("Grounded in your catalog" / "Honest about near matches" / "No invented products"). Our four guardrails are mechanism-framed and phrased differently.

### B8. Is AI product search the same thing as an AI catalog assistant? — 320 words

**Leads with:** "No. Search is a layer inside the assistant. Retrieval finds the candidates. The conversation is everything that happens around it."

Draw the boundary cleanly: retrieval answers "which products match?" The assistant layer handles the follow-up question, the quantity, the price tier, and the move toward a quote. A buyer rarely stops at the first result, which is why a search box that returns a perfect list and then goes silent is only half a system.

- **Internal link 5:** `/what-is-a-b2b-catalog-chatbot/`, anchor **"B2B catalog chatbot"**.
- **The post 266 handoff, exactly one sentence, then move on:** better discovery is not the same thing as better conversion, and we have argued elsewhere that AI search alone does not move a catalog conversion rate because buyers still stall on pricing, minimum order quantity, and compatibility at the point of decision. **Internal link 6:** `/b2b-catalog-conversion-rate/`, anchor **"B2B catalog conversion rate"**. Do not re-argue it. Do not quote its numbers.

**Then the single dedicated ChatSKU block, roughly 150 words, and this is the only place ChatSKU gets a real explanation in the body.**

What we can say, all verifiable from live client materials:
- ChatSKU is the assistant layer over the catalog files you already have: PDF, Excel, ERP export, or an existing store. Ingestion is file-based and human-configured. **Do not claim a live automatic pull from any named ERP** (post 2422 precedent).
- Answers come from your catalog records, near matches are flagged as near matches, and it goes live with one line of code.

**What we must not say, and the post should say why:** we are not going to tell you which retrieval architecture sits under any vendor's product, including ours, because vendors change architectures and the claim is unverifiable from the outside. What matters is what you can test, and B5 and B7 gave you the two tests. **Do not invent or assert a retrieval architecture for ChatSKU.** This paragraph turns the constraint into a credibility move.

- **Internal link 7:** `/features/`, anchor **"what ChatSKU connects to"**.
- **Internal link 8:** `/ai-product-search-for-b2b/` second use, anchor **"see it on your catalog"**.

### People also ask (H2, verbatim label) — 4 H3s, 60 words each

1. **Is AI product search the same thing as semantic search?** No. Semantic search is one component. AI product search in practice is semantic retrieval, keyword retrieval, structured spec filters, and grounding, working together.
2. **Does AI product search need clean, structured product data to work?** It works with messy data and works better with clean data. Duplicated SKUs and inconsistent units degrade results before retrieval is even involved.
3. **Can AI product search handle competitor and OEM cross-reference part numbers?** Only if those cross-references are in the data it can read. Most distributors keep them in a separate file that never reaches the search index.
4. **How do you test whether an AI search tool actually works on your catalog?** Three queries: an abbreviation, a compatibility question, and something you do not stock.

### Conclusion (H2, verbatim label) — 100 words

Three short centred paragraphs. Restate the thesis in one line: the interesting part of AI product search is not that it is smart, it is that it knows when to be literal. Then the one thing to take away: ask any vendor whether exact matching still runs alongside the AI, and ask the assistant for something you do not stock.

**No inline CTA links in the conclusion body.** CTA is the `#e94560` button widget: **"See the live demo"** → `https://chatsku.com/demo/` (**internal link 9**).

### Frequently asked questions (H2, verbatim label) — 6 Qs, Elementor native accordion, placed after the Conclusion

1. What is the difference between AI product search and filters or faceted navigation?
2. What is an embedding, in one sentence?
3. Why would an old-fashioned keyword search ever beat AI search?
4. What if buyers search in a different unit of measure than your catalog uses?
5. What happens when a buyer searches for something you do not stock?
6. Does AI product search replace your sales team?

**None of these duplicate the landing page's seven FAQ questions.** Q6 must answer "no, it augments" per brand.md.

## Stats: exactly five, placed exactly here

| # | Stat | Section | Link? |
|---|---|---|---|
| 1 | 56% of sites fail to adequately support search needs (Baymard, 170+ sites, updated Apr 2026) | B2 | **Yes, external link 1** |
| 2 | Abbreviation and symbol searches: 54% of sites have issues (Baymard) | B3 | Same source, linked once only |
| 3 | Compatibility searches: 44% (Baymard) | B3 | Same source |
| 4 | Use-case searches: 43% (Baymard) | B3 | Same source |
| 5 | Searchers = 24% of visitors, 44% of revenue, 2.5x conversion (Constructor "Beyond Relevance", 609M searches, 113 retail sites, Oct–Dec 2024) | B3, closing paragraph | **No link.** Cite by name with methodology, and flag it as retail data. |

**No other numbers appear anywhere in this post.** No invented ROI scenario, no worked revenue math, no percentage that is not on this table.

## External links: 2, and here is the reasoning

The cap is 2. Three candidates competed: Baymard, Constructor, BEIR.

1. **Baymard** — https://baymard.com/blog/ecommerce-search-query-types — `target="_blank" rel="noopener noreferrer"`. Non-negotiable: it carries 4 of the 5 stats and it is the only primary research in the set.
2. **BEIR** — https://arxiv.org/abs/2104.08663 — `target="_blank" rel="noopener noreferrer"`. **Chosen over Constructor deliberately.** Link the claim most likely to be disbelieved. "Meaning-based search underperforms a keyword box on part numbers" is the post's most contestable and most differentiating assertion; an unlinked contrarian claim is a weak contrarian claim. Constructor's figure is a directionally uncontroversial supporting stat with a disclosed methodology stated in-sentence, which is sufficient without a link.

**Named but not linked:** Constructor, AWS, Elastic, Weaviate, Lewis et al. (RAG), Menon et al. (QAM), Foo et al. (Know Or Not). Naming a source without linking it is normal academic practice and costs us nothing.

**Zero competitor mentions.** No Algolia, Coveo, Zoovu, Constructor-as-a-product, Lucidworks, Klevu, Fast Simon, Drift, Intercom, Tidio. Constructor appears only as the author of a cited study, never as a product.

## Internal links: 9 hrefs, with exact anchors

| # | Section | URL | Anchor (2–5 words) |
|---|---|---|---|
| 1 | Introduction | `/ai-product-search-for-b2b/` | AI product search for B2B |
| 2 | B1 | `/passive-catalog-costing-you-sales/` | what a passive catalog is |
| 3 | B2 | `/convert-pdf-catalog-to-website/` | make a PDF catalog searchable |
| 4 | B3 | `/roi-calculator/` | model the revenue impact |
| 5 | B8 | `/what-is-a-b2b-catalog-chatbot/` | B2B catalog chatbot |
| 6 | B8 | `/b2b-catalog-conversion-rate/` | B2B catalog conversion rate |
| 7 | B8 | `/features/` | what ChatSKU connects to |
| 8 | B8 | `/ai-product-search-for-b2b/` (2nd use) | see it on your catalog |
| 9 | Conclusion | `/demo/` | button widget: See the live demo |

Clears MUST-FOLLOW section 6: 3 page links (`/roi-calculator/`, `/features/`, `/demo/`) plus the money page twice, and 4 blog links.

**Blocked, do not link under any circumstances:**
- `/rfq-automation-for-product-catalogs/` — research found it serving homepage content. If an RFQ link is ever wanted, use `/rfq-automation-manufacturers/`. Flag the stale entry in MUST-FOLLOW section 6 to the publisher.
- `/product-information-management-software/` (post 1538, WP draft, 404s)
- `/erp-export-ai-agent-ready/` (post 2422, WP draft, 404s)

Every href must be re-verified 200 by the build script's User-Agent-aware checker before push. WebFetch produces false negatives on chatsku.com.

## Images: 1 featured + 2 body, all 860×452

| Slot | Placement | What it must depict |
|---|---|---|
| Featured | Top | A procurement or purchasing person at a desk, laptop open, product paperwork or a printed spec sheet beside them, mid-search. Office or industrial-office setting. |
| Body 1 | End of **B4** (embeddings) | Two colleagues at a screen reviewing structured product data, a spreadsheet or catalog listing visible. Depicts a catalog being organised into something a machine can measure. |
| Body 2 | End of **B7** (grounding and abstention) | A parts counter or warehouse scene where a person is checking a physical stock record or shelf against a screen. Depicts "the answer comes from what is actually on the shelf." |

**Hard bans:** no glowing brains, no neural-network renders, no circuit-board abstractions, no robot hands, no nature, no flowers. Source 6+ candidates per slot, resize to 860×452, and look at every one. Use the `QA_DIR` override. Rewrite alt text at publish time to describe the image actually chosen, 80–150 chars each.

## Must include

- The opening admission that "it connects to your catalog and understands your product data" is not an explanation, in our own words, without quoting our own marketing copy.
- The substitution-intent hook: *"same as the 2-inch one we bought last year, but in stainless."*
- The explicit label on the Baymard-to-B2B mapping as **our reasoning, not measured B2B data**, in a full sentence.
- The "retail data" flag on the Constructor stat, inside the sentence.
- The BEIR concession, blunt, unhedged, with its one-sentence 2021 caveat.
- The plain-language definition of "out-of-domain."
- The 3-row retrieval-method table in B5.
- Both reader takeaways: the vendor question (does exact matching still run?) and the demo test (ask for something you do not stock).
- The statement that we will not assert any vendor's internal retrieval architecture, including our own.
- Sentence case on every heading.

## Must NOT include

**Landing-page cannibalisation:**
- The 8-row traditional-vs-ChatSKU comparison table, or any table on that axis.
- The hinge worked example. No 316 vs 304 hinge, no 4" vs 3.5" size comparison, no butt hinge, no continuous hinge.
- The four buyer-phrasing cards as a structure.
- The manufacturers / distributors / industrial suppliers / B2B eCommerce audience segmentation.
- The five-step connect → learns → describes → finds → RFQ sequence as a numbered how-to.
- Landing-page FAQ questions 1, 4, 5, 6, 7 in any recognisable form.
- The three trust-card labels.
- The commercial framings "Want ChatSKU to do this with your catalog?" and "See it on your own catalog" as headings.

**Post 266 collision:**
- Its comparison table, its H2 "Why does AI search improve discovery but not conversion?", the 10–15% relative lift figure, the 2.4% baseline, the 12.3% / 3.1% chat-engagement figures, and any re-argument of the discovery-versus-conversion thesis. One acknowledging sentence and a link. That is the entire allowance.

**Other post collisions:**
- Post 353's "reads your catalog, not the internet" framing or any near variant.
- Post 380's 3-column comparison table.
- Post 397's passive-vs-active table and after-hours ROI math.

**Banned stats:** McKinsey 76%, all zero-result-rate figures (10–15%, 10–20%, 30%), the 17%/20% zero-result abandonment figures, Baymard 41%, all Sana Commerce figures, Gartner 67% rep-free, the $15T / 90%-by-2028 figure, VML's 56% B2B keyword-matching figure, and any invented ROI number.

**Claims we cannot make:**
- Any assertion about ChatSKU's retrieval architecture (hybrid, vector, reranking, RRF, or otherwise).
- Any claim of a live automatic pull from SAP, NetSuite, Epicor, or any named ERP.
- Any revenue figure for lost B2B search. None survives verification.
- "Embeddings poorly represent numerical values" as a **cited** claim. State it as engineering rationale in our own voice, never attributed to a paper.

**Voice bans (MUST-FOLLOW section 7 and voice.md):** em dashes and `&mdash;`, "just a chatbot", "AI-powered" as a modifier, "solutions" as a noun, "chatbot" alone, delve, leverage, navigate as a verb, realm, landscape, ecosystem, revolutionary, game-changing, cutting-edge, "transform your", "in today's fast-paced world", "in conclusion", Title Case headings.

**Structural bans:** no bullet stuffing. Sections B2, B4, B5, B7 are prose-first. Bullets only for the genuinely list-shaped content flagged above (the four guardrails, the hard-constraint split in B6). LLMs read bullet stuffing as thin content.

## Uniqueness: how this differs from every adjacent post

Verified against all 31 entries in `published-posts-inventory.md`. **No existing ChatSKU post covers AI product search, semantic search, embeddings, vector retrieval, or search technology as its primary subject.** The slug `how-ai-product-search-works` matches no existing slug.

| Adjacent post | What it owns | How this post stays out of its lane |
|---|---|---|
| **`/b2b-catalog-conversion-rate/` (266) — closest risk** | The argument that AI search improves discovery but **not** conversion, plus the AI-search-vs-conversational-commerce table and the 10–15% / 2.4% / 12.3% stats | This post lives **entirely upstream, inside discovery**: how retrieval works and why B2B queries break it. It never touches conversion mechanics, never re-argues 266's thesis, reuses none of its stats or its table, and acknowledges it in exactly one sentence in B8 before handing the conversion question over with a link. |
| `/what-is-a-b2b-catalog-chatbot/` (353) | Defines the **tool category** | This defines the **retrieval mechanism** several layers below. 353 answers "what is this thing"; this answers "how does it find the right SKU." No category definition, no vendor criteria. |
| `/b2b-conversational-commerce/` (380) | The **category and commercial strategy**: use cases, ROI, RFQ workflows | No use-case list, no ROI model, no before/after scenario, no 3-column table. Retrieval mechanics only. |
| `/passive-catalog-costing-you-sales/` (397) | A static catalog **cannot respond at all** | Different failure mode entirely: this explains why a catalog **with** a working search box still fails. No passive-vs-active table, no after-hours math. |
| `/agentic-commerce-glossary/` (2129) | Protocol and standard **definitions** (ACP, AP2, MCP, A2A) | No protocols, no agentic commerce framing. |
| `/erp-export-ai-agent-ready/` (2422) | Data-quality audit of the **export file** | Upstream of retrieval, not retrieval. Touched only in PAA Q2, in two sentences, unlinked (it 404s). |
| `/ai-ready-b2b-catalog-autonomous-buying/` (untracked, live) | The persuasive "machine-readable catalog" business case | Confirmed by research to contain zero mention of product search, semantic search, or embeddings. No overlap. |

**Dedup requirement:** run the 8-gram audit against all live and draft posts before push. Highest collision risk sits in B4 and B8 against post 353 (RAG and catalog-ingestion phrasing), and in B2 against 397 and 1538 (catalog-failure openings). Expect to reword, not find-replace.

## Open questions for the creator

- Which product carries the B6 worked example. Valve is recommended; gasket, bearing, or motor are all fine. It must not be a hinge.
- Whether the B5 table sits before or after the RRF explanation. Either works; put it wherever the argument reads cleanest.
- The exact wording of the opening admission. It has to be self-aware without being self-flagellating, and it must not quote the landing page.
- Bullet-versus-prose call inside B2's six failure modes. Prose is preferred; a short labelled list is acceptable if the mechanism stays in the sentences.

## Locked, not open to interpretation

- Format B with the contrarian spine in B5 and B6.
- The five stats, their placement, and the two external links.
- The nine internal links and their exact anchors.
- The BEIR concession, stated bluntly.
- The "our reasoning, not B2B data" label on the Baymard mapping.
- The refusal to assert ChatSKU's retrieval architecture.
- ChatSKU confined to one block in B8 plus light mentions in PAA, FAQ, and Conclusion.
