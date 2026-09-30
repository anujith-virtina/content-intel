---
title: Research notes — What your site search logs are already telling you
client: chatsku
date: 2026-09-30
topic: How a B2B distributor reads internal site-search data to find where buyers fail to find products
audience: owner / ecommerce manager / marketing lead at a B2B manufacturer, distributor or wholesaler (not a data analyst)
stage: research
slug: site-search-logs
---

# Research: What your site search logs are already telling you

## Uniqueness check (per orchestrator, already run against corpus)

Corpus-wide regex sweep of ChatSKU's 40 published posts shows "site search logs / zero-result reports" appearing only twice, both in `/traditional-b2b-product-search-fails/`. That post owns WHY keyword search breaks and the cost of zero-result pages. `/how-ai-product-search-works/` owns the retrieval mechanism (embeddings, BM25/hybrid, RRF, RAG). `/b2b-catalog-conversion-rate/` owns the found-it-to-bought-it gap. This post is scoped narrowly to the DIAGNOSTIC WORKFLOW: where the data physically lives (GA4/Magento/WooCommerce report paths), how to read a query log, and how to verify a fix worked. Confirmed open lane. No re-derivation needed here — task brief already established this.

## Sub-questions

1. Where does a non-technical B2B operator actually find site-search data in GA4, Magento/Adobe Commerce, and WooCommerce? What are the exact report paths and their limits?
2. Is there a credible, citable zero-result-rate benchmark, or is this one of the industry's untraceable round numbers?
3. Is there a credible, citable figure for the share of visitors who use site search and how they convert?
4. What specific B2B query patterns (part numbers, cross-references, application language, compound specs, UOM, superseded parts) produce zero results, and why does keyword/substring matching fail on each?
5. What does a refinement chain (search, refine, refine, exit) mean, and is there a standard way to read it?
6. Why do synonym dictionaries and manual redirects fail to scale as a permanent fix?
7. How should an operator verify a fix actually worked?

## Key findings

### Finding 1: GA4's site-search event only fires when the search term shows up in the URL's query string

- Source: [Enhanced measurement events - Analytics Help](https://support.google.com/analytics/answer/9216061?hl=en) — Google Analytics Help, accessed 2026-09-30. VERIFIED (fetched directly, HTTP 200).
- What it says: the `view_search_results` event fires "each time a user is presented with a search results page, as indicated by the presence of a URL query parameter." By default GA4 looks for one of five parameters: `q`, `s`, `search`, `query`, `keyword`, and you can add up to 10 custom parameters in the enhanced measurement settings.
- Why it matters: this is the single most common reason an operator opens GA4, finds nothing, and concludes "we don't have this data." If the site's search implementation is AJAX/JS-driven and never writes the term into the visible URL (common on Magento layered-search widgets and many WooCommerce search bars), GA4 captures zero rows even though enhanced measurement is switched on. The fix is either exposing the parameter in the URL or pushing the term to the dataLayer via Google Tag Manager and mapping it to the `search_term` event parameter — no code change to the search engine itself required.

### Finding 2: The report path is Explore/Events, not a dedicated "Site Search" report like Universal Analytics had

- Source: cross-referenced secondary implementation guides (Analytics Mania, Measureschool) against the primary GA4 automatically-collected-events documentation — accessed 2026-09-30. [unverified against a single Google page for the exact click path, but consistent across three independent implementation guides and matches GA4's known Events model]
- What it says: GA4 has no standalone "Site Search" report. The practical path is Reports > Engagement > Events, find the `view_search_results` event row, then add `search_term` as a secondary dimension (or build a free-form Explore report with `search_term` as a dimension and event count as the metric) to see individual terms and volumes.
- Why it matters: this is a genuinely confusing UX change from Universal Analytics, which had a labeled Site Search report. Readers searching "site search report GA4" need to be told plainly that the report doesn't exist by that name anymore and where the same information now lives.

### Finding 3: Magento/Adobe Commerce has two separate things with similar names: a management grid and an analytics report

- Source: [Search Terms report and Search Terms management — Adobe Commerce Admin docs](https://experienceleague.adobe.com/en/docs/commerce-admin/catalog/catalog/search/search-terms) — Adobe, last updated 2026-08-20. VERIFIED (fetched directly, HTTP 200).
- What it says: Marketing > SEO & Search > Search Terms is the management grid (columns: Search Query, Store, Results, Uses, Redirect URL, Suggested Terms, Actions) where you can set a redirect URL per term or add suggested terms. A separate view, Reports > Marketing > Search Terms, is the read-only analytics report — same underlying data (results count, hits/uses) but filterable and exportable to CSV/Excel.
- Why it matters: operators who only find the management grid think Magento's search reporting is a static list. The exportable analytics report is what lets them sort by highest-hit zero-result terms, which is the actual diagnostic step.

### Finding 4: WooCommerce core has no native site-search report at all

- Source: [Analytics and Sales Reports - WooCommerce](https://woocommerce.com/document/woocommerce-analytics/) and [Searches report - WooCommerce Product Search](https://woocommerce.com/document/woocommerce-product-search/reports/searches/) — WooCommerce official docs, accessed 2026-09-30.
- What it says: WooCommerce's built-in Analytics (WooCommerce > Analytics) ships six reports: Revenue, Orders, Products, Variations, Categories, Customers. Search terms are not among them. A "Searches" report showing searches-with-results vs. searches-without-results curves exists only inside the paid WooCommerce Product Search extension.
- Why it matters: WooCommerce operators cannot assume this data exists in their dashboard the way Magento operators can. Their two real options are the paid extension or GA4 event tracking (same `view_search_results` mechanism as Finding 1) — there is no free native fallback.

### Finding 5: The zero-result-rate "benchmark" numbers circulating online do not trace to a named study

- Source: attempted trace of "12-18% zero-result rate" and "under 2-3% is top-performer" figures through Baymard Institute's own published pages — [27 On-Site Search UX Articles](https://baymard.com/blog/collections/on-site-search), [5 Proven UX Strategies For "No Results" Pages](https://baymard.com/blog/no-results-page) (published 2019-02-04, updated 2025-02-18), [E-Commerce Search Usability Research](https://baymard.com/research/ecommerce-search) — accessed 2026-09-30, both fetched directly, HTTP 200.
- What it says: Baymard's own no-results-page article does not cite a zero-result-rate percentage anywhere. It states that "nearly 50%" of benchmarked sites fail to give users a way to recover from a zero-result search — a UX-quality metric, not a frequency-of-occurrence metric. The 12-18%, 8%, and "under 2-3%" figures only appear on SEO/vendor blogs (zipchat, doofinder, helloretail, hyberx) that cite "Baymard" generically without a link to a specific report or page.
- Why it matters: this is a fabricated-by-repetition statistic, structurally identical to the already-flagged 48% Baymard search-box-abandonment figure. **Do not use a zero-result-rate benchmark number in this article.** Describe the metric (what it measures, why it matters) without attaching an industry-average figure.

### Finding 6: The "site-search users convert 2-3x better" and "2.77% vs 4.63%" figures also fail to trace

- Source: attempted trace through Forrester's own site — [SEO And Site Search: Not Quite The Match Made In Heaven](https://www.forrester.com/blogs/seo-and-site-search-not-quite-the-match-made-in-heaven/), Forrester, published 2019-11-11 — fetched directly, HTTP 200. Also checked for an original Econsultancy report; none surfaced independent of secondary citations.
- What it says: Forrester's own blog post, which is the closest thing to an original source for the "site-search users convert better" claim, attributes a conversion uplift of "somewhere between 40% and 250%" to a single unnamed interviewed expert — not a study, not a defined methodology. The Econsultancy "2.77% vs. 4.63%" figure could not be traced to any Econsultancy report; it appears only in blogs citing "Econsultancy" with no link.
- Why it matters: both of the most commonly repeated site-search conversion statistics are unusable. Per the client's standing rule (the banned Baymard 48% figure), any ubiquitous round number without a traceable primary source should be cut, not softened with "reportedly."

### Finding 7: B2B query patterns that defeat keyword/substring search are a known, well-documented category (mechanism-level, not statistical)

- Source: general pattern description corroborated across a vendor engineering explainer on B2B search failure modes (name withheld per client competitor rule; ChatSKU's own established themes) and Adobe Commerce's own Search Terms documentation (Finding 3), which exists specifically because exact-match catalog search fails on these patterns. Accessed 2026-09-30.
- What it says: B2B keyword search is exact-match or near-exact-match against a product's indexed text fields (title, SKU, description). It has no concept of "close enough" unless a synonym or redirect entry already exists for that literal string. See the query-pattern table below for the six recurring failure types and why each defeats substring matching specifically.
- Why it matters: this is the structural reason the "just add synonyms" fix doesn't hold up (Finding 8) — every one of these six patterns generates a near-infinite number of literal-string variants, and a synonym dictionary can only ever cover strings someone has already typed and someone has already noticed.

### Finding 8: Synonym dictionaries are inherently reactive, not predictive

- Source: [Search with Synonyms: Problems and Solutions](https://aclanthology.org/C10-2151.pdf) — ACL Anthology (peer-reviewed NLP/IR proceedings), and Adobe Commerce's own synonym vs. redirect distinction (Finding 3: "Search synonyms do not trigger redirects... must be configured as a separate search term"). Accessed 2026-09-30.
- What it says: a synonym dictionary only matches term pairs a human has already entered by hand; it has no mechanism for anticipating a variant nobody has typed yet. In Magento specifically, synonyms and redirects are two separate manual entries per term (Finding 3) — there is no bulk or rule-based way to say "treat any punctuation variant of this SKU the same."
- Why it matters: this grounds the "why this doesn't scale" section in a mechanism (one-entry-per-variant, no generalization) rather than an assertion. It also gives a concrete, checkable claim: in Magento, adding a redirect and adding a synonym are two different admin actions, each covering exactly one literal string.

### Finding 9: Query reformulation within a session is an established, practical signal in IR research

- Source: [Analyzing and Evaluating Query Reformulation Strategies in Web Search Logs](https://jeffhuang.com/papers/Reformulation_CIKM09.pdf) — Huang & Efthimiadis, CIKM 2009 (peer-reviewed, hosted on author's own site). Accessed 2026-09-30.
- What it says: session boundaries in query-log analysis are commonly drawn at a 30-minute gap between actions from the same user. Consecutive queries from one user within a session are classified by comparing the first query to the reformulated one; over half of e-commerce queries occur as part of a reformulation sequence (general IR finding, not B2B-specific).
- Why it matters: this gives a practical, citable basis for telling a non-technical operator: "when you see the same visitor search 3 times in a row and then leave, that's not 3 separate weak signals, it's one strong signal — read those rows as a single failed session, not three data points." [unverified: the specific "3 refinements then exit" threshold is not itself in the paper; the paper supports the general session/reformulation-as-signal concept, not a specific refinement count. Present this in the article as a practical heuristic, not as a cited statistic.]

## Report paths (exact, for the article's most load-bearing section)

| Platform | Exact path | What it shows | Native or paid | Source |
|---|---|---|---|---|
| GA4 | Reports > Engagement > Events > `view_search_results` row, add `search_term` as secondary dimension (or build a free-form Explore with `search_term` dimension) | Individual search terms and counts, only for terms that appear in the URL query string (`q`, `s`, `search`, `query`, `keyword` by default, up to 10 configurable) | Native, on by default via enhanced measurement, but silently fails on AJAX search UIs that don't write to the URL | support.google.com/analytics/answer/9216061 |
| Magento / Adobe Commerce | Reports > Marketing > Search Terms (analytics, exportable) or Marketing > SEO & Search > Search Terms (management grid, lets you set a Redirect URL) | Search Query, Store, Results (products matched), Uses/Hits (times searched), Redirect URL | Native | experienceleague.adobe.com/en/docs/commerce-admin/catalog/catalog/search/search-terms |
| WooCommerce (core, free) | None | Nothing — search terms are not tracked anywhere in core WooCommerce Analytics (Revenue, Orders, Products, Variations, Categories, Customers only) | N/A | woocommerce.com/document/woocommerce-analytics/ |
| WooCommerce (with paid Product Search extension, or via GA4) | Product Search > Reports > Searches (if extension installed) or same GA4 path as above | Searches-with-results vs. searches-without-results over time | Paid extension, or fall back to GA4 | woocommerce.com/document/woocommerce-product-search/reports/searches/ |

## Query-pattern table (task 4)

| Pattern | What it looks like in a log | Why keyword/substring matching fails |
|---|---|---|
| Part number punctuation/spacing mismatch | Buyer types `SS-304-1/2NPT`, catalog stores `SS304-1/2-NPT` (no dash after SS, different spacing) | Exact-match and even simple substring indexing treat punctuation and whitespace as literal characters; one dash out of place is a different string, so results = 0 |
| Competitor/OEM cross-reference numbers | Buyer types a competitor's or OEM's part number that isn't in the catalog as an attribute at all, only the distributor's internal SKU is indexed | The catalog has no field containing that string anywhere, so there is nothing for even a fuzzy matcher to partially match against — it's a missing-attribute problem, not a matching-algorithm problem |
| Application/problem language | Buyer types `pump for pool` or `fitting for 1/2 copper` instead of the product noun (`1/2 in. sweat x sweat ball valve`) | Keyword search matches literal text in the product title/description; it has no mapping from a use-case phrase to a product category unless someone manually wrote that phrase into the product copy |
| Compound spec strings | Buyer types `316 stainless 3/4 npt` as one query | Basic search either requires all terms to match one field (AND logic, usually too strict, zero results) or matches any term (OR logic, usually too loose, wrong results) — most implementations tuned for B2C default to AND, which breaks multi-attribute queries |
| Unit-of-measure / pack-size terms | Buyer types `case of 144` or searches for `each` vs `box`, expecting UOM-filtered results | UOM is typically a transactional/pricing attribute (tied to a specific SKU record), not a searchable text field, so the term has nothing to index against |
| Obsolete or superseded part numbers | Buyer types a legacy part number the manufacturer has since replaced with a new SKU | If the old number was never added as a synonym or cross-reference on the new product record, the catalog has zero knowledge that the two numbers ever referred to the same item |

## Data points

| Stat | Value | Source | Date | Status |
|---|---|---|---|---|
| GA4 default site-search query parameters | q, s, search, query, keyword (up to 10 configurable) | support.google.com/analytics/answer/9216061 | accessed 2026-09-30 | VERIFIED, primary |
| Magento Search Terms report columns | Search Query, Store, Results, Uses, Redirect URL, Suggested Terms, Actions | experienceleague.adobe.com/.../search-terms | last updated 2026-08-20 | VERIFIED, primary |
| WooCommerce core Analytics reports | 6 reports: Revenue, Orders, Products, Variations, Categories, Customers (no search) | woocommerce.com/document/woocommerce-analytics/ | accessed 2026-09-30 | VERIFIED, primary |
| Session boundary convention in query-log research | 30-minute gap between actions, same user | jeffhuang.com/papers/Reformulation_CIKM09.pdf | CIKM 2009 | VERIFIED, primary (peer-reviewed) |
| Zero-result rate industry benchmark | no traceable figure | attempted trace via Baymard's own pages | accessed 2026-09-30 | UNVERIFIED — do not use |
| Site-search-user conversion uplift | no traceable figure ("2-3x", "2.77% vs 4.63%" both untraceable) | attempted trace via Forrester's own blog | accessed 2026-09-30 | UNVERIFIED — do not use |

## Conflicts and disagreements

- **Position A** (multiple SEO/vendor blogs — zipchat, doofinder, helloretail, hyberx): zero-result rate industry average is 12-18%, top performers under 2-3%, all attributed to "Baymard."
- **Position B** (Baymard's own published pages, fetched directly): no such percentage appears anywhere in Baymard's no-results-page article or ecommerce-search research page. Baymard's actual published finding is a UX-quality metric (~50% of sites lack good no-results recovery), not a frequency metric.
- **What's actually true:** Position B. The percentage is a fabricated-by-repetition figure with no traceable origin. Treat as unusable, consistent with the client's prior ruling on the Baymard 48% figure.

## Competitive scan

1. **`/traditional-b2b-product-search-fails/`** (ChatSKU, existing) — owns why keyword search breaks structurally and the cost of zero-result pages. Does not cover where to find the data or how to read a log. Gap this new post fills: the practical, tool-by-tool "open this report" workflow.
2. Generic "how to fix zero search results" vendor posts (Bloomreach, Wizzy, Searchanise) — all lean on the untraceable benchmark numbers flagged above, and all pitch a vendor tool as the fix. None walk a non-technical reader through GA4's actual current click path or Magento's actual report path with platform-verified column names.
3. GA4/Magento implementation guides (Analytics Mania, mgt-commerce, magefan) — accurate on mechanics but written for developers/agencies, not for a distributor owner; none frame the data as a buyer-intent diagnostic.

## The gap

Every competing article either (a) quotes an unsourced zero-result benchmark to create urgency, or (b) explains the report mechanics for a technical audience. Nobody hands a non-technical B2B operator the exact three-platform lookup path, the specific query patterns their own catalog will produce, and a way to read consecutive searches in a session as one signal instead of noise.

## Recommended angle

> Skip the benchmark number. Show the reader exactly where their own data already lives across GA4, Magento, and WooCommerce, what a B2B-specific zero-result row actually looks like in their own log, and how to tell a real pattern from noise before doing anything about it.

## Couldn't find

- A citable zero-result-rate benchmark for B2B or general ecommerce site search. Every version traces back to blog-to-blog repetition, not a named study. The article should describe the metric without a benchmark number.
- A citable figure for the share of visitors who use site search, or their conversion rate vs. non-searchers. The "2-3x" and "2.77%/4.63%" figures both fail to trace to a primary source, including at Forrester's and Econsultancy's own sites.
- A specific, named threshold for "how many refinements before a session should be read as a failure" — IR research supports reading consecutive reformulations as one signal, but does not supply a specific count like "3 refinements." Present as a practical heuristic, not a statistic.
- Confirmation, directly from a single Google support page, that enhanced measurement (and specifically the Site search toggle) is on by default for every newly created GA4 data stream. This is corroborated by three independent secondary implementation guides but not pinned to one exact primary sentence in the time available. Recommend the article phrase this as "enhanced measurement is on by default in current GA4 setups" rather than an absolute claim with a specific version/date.

## Sources

- [Enhanced measurement events - Analytics Help](https://support.google.com/analytics/answer/9216061?hl=en) — Google, accessed 2026-09-30, primary, VERIFIED 200. **Recommended external link #1.**
- [Search Terms - Adobe Commerce Admin docs](https://experienceleague.adobe.com/en/docs/commerce-admin/catalog/catalog/search/search-terms) — Adobe, last updated 2026-08-20, primary, VERIFIED 200. **Recommended external link #2.**
- [Marketing reports - Adobe Commerce Admin docs](https://experienceleague.adobe.com/en/docs/commerce-admin/start/reporting/marketing-reports) — Adobe, last updated 2026-06-15, primary, VERIFIED 200 (background only, not needed as a separate link since search-terms page above covers both grid and report).
- [Analytics and Sales Reports - WooCommerce](https://woocommerce.com/document/woocommerce-analytics/) — WooCommerce, accessed 2026-09-30, primary.
- [Searches report - WooCommerce Product Search](https://woocommerce.com/document/woocommerce-product-search/reports/searches/) — WooCommerce, accessed 2026-09-30, primary.
- [5 Proven UX Strategies For "No Results" Pages](https://baymard.com/blog/no-results-page) — Baymard Institute, published 2019-02-04 / updated 2025-02-18, primary, VERIFIED 200 (used to disprove a benchmark claim, not to cite a number).
- [E-Commerce Search Usability Research Studies](https://baymard.com/research/ecommerce-search) — Baymard Institute, accessed 2026-09-30, primary, VERIFIED 200 (same use as above).
- [SEO And Site Search: Not Quite The Match Made In Heaven](https://www.forrester.com/blogs/seo-and-site-search-not-quite-the-match-made-in-heaven/) — Forrester, published 2019-11-11, primary, VERIFIED 200 (used to disprove a benchmark claim).
- [Analyzing and Evaluating Query Reformulation Strategies in Web Search Logs](https://jeffhuang.com/papers/Reformulation_CIKM09.pdf) — Huang & Efthimiadis, CIKM 2009, peer-reviewed, accessed 2026-09-30.
- [Search with Synonyms: Problems and Solutions](https://aclanthology.org/C10-2151.pdf) — ACL Anthology, peer-reviewed proceedings, accessed 2026-09-30.
- Secondary/corroborating (not for citation, used only to confirm GA4 click-path consistency): Analytics Mania, Measureschool — accessed 2026-09-30.
