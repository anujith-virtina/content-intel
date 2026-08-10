---
title: Brief — WooCommerce shortcodes reference and troubleshooting guide
client: virtina
date: 2026-08-10
topic: woocommerce shortcodes
slug: woocommerce-shortcodes
stage: brief
research: clients/virtina/output/research/woocommerce-shortcodes-2026-08-10.md, clients/virtina/output/research/competitor-analysis-2026-08-10.md
---

# Brief: Are WooCommerce shortcodes deprecated? The 2026 reference and troubleshooting guide

## Thesis

WooCommerce shortcodes are not deprecated, and the reason so many store owners assume they are is that several competitor articles and the official docs blur "shortcodes" with the separate, narrower soft-deprecation of the old product-grid blocks, leaving the real long-tail problem, shortcode failures on real stores, completely uncovered.

## Why this, why now, why us

- **Why this angle:** Zero of Virtina's 50 published WooCommerce posts mention "shortcode" (confirmed via full-text grep of `published-posts-inventory.md`). Every fetched competitor, including woocommerce.com itself, either pushes blocks without nuance or gives thin, dated troubleshooting. The gap (deprecation myth, block-theme/FSE behavior, symptom-cause-fix troubleshooting, honest shortcode-vs-block guidance) is real and fully unclaimed.
- **Why now:** WooCommerce 11.0 shipped August 4, 2026, six days before this brief, with no shortcode-specific changes in the release notes. That currency is a legitimate, dateable hook that ages competitors' 2023-2025 content instantly.
- **Why this client:** Virtina positions on fixing what's broken and cutting through vendor BS (per `brand.md`). A myth-correction plus real symptom-cause-fix troubleshooting is exactly that positioning applied to a genuinely under-served long-tail query cluster.

## Audience

WooCommerce store owners, marketers, and developers, per the orchestrator's brief. Mixed technical level: some are non-technical store owners pasting a shortcode into a page and watching it fail; others are developers debugging attribute syntax or HPOS interactions. Per `style/audience.md`, this skews toward Virtina's core B2B/B2C ecommerce operator readership, self-diagnosing a problem via Google, skim-first, 5-15 minutes max. Every technical term (HPOS, FSE, Store API) needs a first-use gloss since the audience mixes developer and non-developer readers, unlike Virtina's usual industry-fluent-only assumption.

## Format and length

- **Format chosen: Format E (Contrarian thesis).**
- **One-sentence reason:** The locked thesis is literally a myth-correction ("shortcodes are not deprecated," against the conventional wisdom several competitors imply), which is the exact use case section 11 defines for Format E ("opinion pieces challenging conventional wisdom"), and it lets the reference/troubleshooting content double as the evidence that dismantles the myth.
- **Rotation check against last 10 published posts** (sorted by date, from `published-posts-inventory.md`):

| # | Post | Date | Format |
|---|---|---|---|
| 1 | 42441 leaving-shopify-ownership-risk | 2026-07-24 | B |
| 2 | 42428 shopify-vape-ban-merchant-deplatforming | 2026-07-15 | E |
| 3 | 42413 bigcommerce-to-magento-migration | 2026-07-07 | D |
| 4 | 42393 woocommerce-b2b-pricing-and-access-setup | 2026-06-18 | A |
| 5 | 42391 ecommerce-ai-search-implementation-checklist | 2026-06-18 | A |
| 6 | 42202 woocommerce-b2b-customer-portal | 2026-05-20 | A (untagged, pre-dates format tracking; default era) |
| 7 | 42177 volusion-to-woocommerce-migration | 2026-05-14 | A (untagged, pre-dates format tracking; default era) |
| 8 | 42108 woocommerce-erp-integration | 2026-05-11 | A (named reference post for Format A in section 11) |
| 9 | 42074 woocommerce-b2b-performance-fix | 2026-05-06 | A (named reference post for Format A in section 11) |
| 10 | 42068 capture-b2b-sales-24-7-ai-chat-assistant | 2026-04-30 | A (untagged, pre-dates format tracking; default era) |

  Format A appears in at least 4 of the last 10 with certainty (42393, 42391, 42108, 42074) and likely 7 once the untagged pre-tracking posts are counted, well over the 3+ threshold. **Format A is disqualified**, even though it is the most natural structural fit for a reference-plus-troubleshooting topic. Formats B, D, and E each appear exactly once in the last 10 (under the 3+ threshold, all eligible); C and F were not used at all. Format E is chosen for content fit over B and D; see next line for what was skipped and why.
- **Formats skipped:** A (overused, 4-7 of last 10). B (Conversational Q&A, used once at position 1) and D (Decision-tree, used once at position 3) were both eligible but rejected on fit: B doesn't naturally host a tabular attribute reference without forcing every shortcode into an artificial "reader question," and D fits only the shortcodes-vs-blocks section, not the deprecation correction or the troubleshooting cases that make up most of the word count.
- **Target length: 2,200-2,800 words** (word budget below sums to ~2,750, mid-range).
- **Reading time:** ~11-12 minutes.

## Structure

Base HTML structure is Virtina's standard section 2 order (Summary, Introduction, TOC, body H2s, PAA, Conclusion, FAQ, author bio) using Templates A-M from `html-templates.md`. Format E only changes the *argumentative* shape of the body H2s (myth setup -> evidence build), not the HTML templates. Do not improvise structure outside the templates.

### Opening hook (Summary + Introduction blocks)

Summary (Template A, ~80 words): open with the concrete, common scenario, a store owner reads a blog post or plugin changelog saying "shortcodes are deprecated, switch to blocks," panics, and either rips out a working `[woocommerce_my_account]` page or spends an afternoon confused about why their `[products]` grid still works fine. State the correction as the summary's closing line: none of WooCommerce's 11 core shortcodes are deprecated as of WooCommerce 11.0 (August 4, 2026).

Introduction (Template B, ~150 words, 2 paragraphs): paragraph 1 names the real confusion (shortcodes vs. the older product-grid *blocks*, which are what's actually soft-deprecated since WooCommerce 9.5). Paragraph 2 previews what the article actually covers that competitors don't: complete attribute reference, honest shortcode-vs-block guidance, block-theme/FSE behavior, and 7 documented failure modes with fixes. No internal links in the introduction (link rule: body sections only).

### Section 1: Are WooCommerce shortcodes deprecated in 2026? (~300 words, 2 H3s)

- **H2 id:** `shortcodes-deprecated`
- **First sentence must directly answer:** "No, all 11 core WooCommerce shortcodes are fully supported in WooCommerce 11.0, released August 4, 2026, with no shortcode-specific changes in that release's notes."
- Key points: state the correction plainly; distinguish shortcodes (not deprecated) from the older product-grid blocks (soft-deprecated since WC 9.5, replaced by Product Collection block); name `[woocommerce_my_account]` as the one page with zero block equivalent.
- H3 1: "What's actually being deprecated (it isn't the shortcodes)" — explain the Product Collection block replacing the older grid blocks, cite WC 9.5.
- H3 2: "Why the confusion started" — competitors conflating the two; cite the official doc's "use blocks instead" framing without naming Virtina's own competitor list from `brand.md`'s do-not-cite list (none of those are relevant here anyway; this is a doc/blog-content conflation, not an agency competitor).
- Internal link: **WooCommerce migration guide** -> `https://virtina.com/woocommerce-migration-guide/`. Context: reassure readers that staying on WooCommerce doesn't force a shortcode-to-block migration; link naturally where the piece notes shortcodes aren't going anywhere.
- Evidence to use: WC 11.0 release date and scope (research file section 1); WC 9.5 soft-deprecation of product-grid blocks (research file section 1, with both developer.woocommerce.com source URLs).
- Don't include: don't claim WooCommerce has ever stated shortcodes will be removed. Don't state a future removal date; none exists in the sources.

### Section 2: What are the complete WooCommerce shortcodes and their attributes? (~450 words, 2-3 H3s)

- **H2 id:** `complete-shortcode-reference`
- **First sentence must directly answer:** "WooCommerce ships 11 core shortcodes, each with a documented set of attributes, and every one of them still works exactly as built."
- H3 1: "Product display shortcodes" — cover `[products]` (full attribute list: limit, columns, paginate, orderby, order, skus, category, cat_operator, tag, tag_operator, attribute, terms, terms_operator, visibility, ids, class, plus the on_sale/best_selling/top_rated special flags), `[product_page]` (id, sku), `[product_category]` (category required, limit/per_page, columns, orderby, order), `[product_categories]` (ids, limit/number, columns, hide_empty, parent, orderby, order), `[add_to_cart]` (id, sku, show_price, style, class, quantity), `[add_to_cart_url]` (id, sku), `[shop_messages]` (no attributes; requires disabling "Enable AJAX add to cart buttons on archives").
- H3 2: "Cart, checkout and account shortcodes" — `[woocommerce_cart]`, `[woocommerce_checkout]`, `[woocommerce_my_account]`, `[woocommerce_order_tracking]`: none take attributes, all render from Settings > Advanced > Page setup. Flag plainly that `[woocommerce_my_account]` has no block-based alternative at all, per official docs.
- Optional H3 3 (only if section runs long): a short note mentioning `[related_products]` as a bonus shortcode outside the core 11, with its 3 attributes (limit, columns, orderby), explicitly labeled as not one of the 11 core shortcodes.
- Presentation: at least one copy-paste code example per shortcode family (e.g. `[products limit="4" columns="4" orderby="popularity"]`). Straight quotes only, this is load-bearing given troubleshooting case 2 later in the article.
- Internal links: **WooCommerce REST API guide** -> `https://virtina.com/guide-on-woocommerce-rest-api/` (natural for developers who outgrow shortcode-level customization). **WooCommerce SEO guide** -> `https://virtina.com/woocommerce-seo-made-easy/` (natural where product-display shortcodes affect what's crawlable/indexable). **B2B customer portal** -> `https://virtina.com/woocommerce-b2b-customer-portal/` (natural in the my-account subsection, since my-account has no block alternative and connects directly to portal/self-service content).
- Evidence to use: research file section 2, exact attribute names and defaults. Do not invent any attribute not listed there.
- Don't include: don't imply any of these attributes changed in WC 11.0; none did per the research.

### Section 3: Should you use a WooCommerce shortcode or a block? (~320 words, 2 H3s, comparison table required here)

- **H2 id:** `shortcodes-vs-blocks`
- **First sentence must directly answer:** "Use the block version by default for a new store, and fall back to the shortcode only when a payment gateway or extension hasn't declared block compatibility."
- H3 1: "When the block checkout is the right call" — visual editing control, no developer needed, one-click "Transform to Classic Shortcode" exists as a reversible escape hatch.
- H3 2: "When the shortcode is still the correct technical answer" — extension/gateway compatibility is the real deciding factor, not nostalgia; cite the Mike Jolley quote (paraphrase, under 15 words if quoted directly) that WooCommerce has no plans to remove classic cart/checkout from core.
- **Comparison table (Template N)** here: columns "Factor" / "Shortcode (classic)" / "Block". Rows: extension & payment gateway compatibility, editing workflow, migration cost/reversibility, My Account availability, performance (state honestly: not meaningfully documented either way in any source found, don't assert a winner).
- Internal links: **WooCommerce customization guide** -> `https://virtina.com/woocommerce-customization-guide/` (natural where the piece discusses visual editing control on the block side). **Speed up WooCommerce** -> `https://virtina.com/speed-up-woocommerce-without-switching-hosts/` (natural where the piece states performance isn't a documented differentiator; link as the resource for readers who actually want to chase page speed).
- Don't include: no performance benchmark numbers comparing shortcode vs. block; research found none. State that honestly rather than inventing a plausible-sounding stat.

### Section 4: Do WooCommerce shortcodes work on block themes and FSE? (~240 words, 1 H3)

- **H2 id:** `block-themes-fse`
- **First sentence must directly answer:** "Yes, WooCommerce shortcodes render normally on block themes and inside Full Site Editing templates, with two narrow developer-facing exceptions."
- H3 1: "The two things to actually watch for" — (1) the deprecated `wc_current_theme_is_fse_theme()` function (deprecated as of WooCommerce 9.9 in favor of WordPress core's `wp_is_block_theme()`; still works in 9.9 but faces future removal, relevant to any custom shortcode wrapper code checking theme type); (2) shortcodes wrapped in `<pre>`/`<code>` tags or dropped into a block/page-builder text field that doesn't parse shortcodes, which is the same root cause documented on classic themes, not an FSE-exclusive bug.
- Internal link: **HPOS migration guide** -> `https://virtina.com/woocommerce-hpos-migration/`. Context: brief mention that `[woocommerce_order_tracking]` reads order data through WooCommerce's own CRUD methods so it isn't directly affected by HPOS, linking to the HPOS guide for readers evaluating that migration separately.
- **Accuracy guardrail, critical for this section:** do NOT claim block themes or FSE have an exclusive shortcode bug. The research explicitly found no source for that; the honest finding is "same failure causes as classic themes." Framing this section as "FSE breaks shortcodes" would be a fabrication the publisher must catch.

### Section 5: Why is your WooCommerce shortcode not working? (~430 words, 2-3 H3s, numbered troubleshooting required)

- **H2 id:** `troubleshooting-shortcode-not-working`
- **First sentence must directly answer:** "Most WooCommerce shortcode failures trace back to one of seven documented causes, and each one has a specific fix."
- Present as a numbered sequence (1-7), each with Symptom / Cause / Fix in 2-3 sentences total per item, using Template F's bullet pattern with a bold numeral+label lead-in (e.g., `<strong>1. Shortcode renders as literal text.</strong>`) since Virtina has no separate numbered-list template; do not invent new HTML outside Template F.
- H3 groupings (pick 2-3 natural clusters to keep headers within the 150-300 word density rule): "Rendering and syntax failures" (cases 1-3: literal-text rendering, curly quotes, variation SKU mismatch), "Display and query bugs" (cases 4-5: out-of-stock counting issue, large ID list failure), "Cart, checkout, caching and widget failures" (cases 6-8: cache serving stale/blank cart, Elementor 3.33.5 regression, widget_text filter).
- Case-by-case sourcing discipline (see Accuracy risks below): case 4 (out-of-stock counting) is single-sourced, attribute it explicitly ("one report documents..."), do not state as established fact. Case 5 (GitHub #31709) must be described as reported and unresolved-as-visible-in-the-thread, never as confirmed-open-today or confirmed-fixed. Case 7 (Elementor) must always carry the exact version number 3.33.5, never a generalized "Elementor breaks WooCommerce" claim.
- Internal links: **WooCommerce bug fix guide** -> `https://virtina.com/woocommerce-bug-fix-guide/` (natural at the top of this section, positioning this as the shortcode-specific companion to Virtina's general bug guide). **Checkout troubleshooting guide** -> `https://virtina.com/woocommerce-checkout-not-working-agency/` (natural inside case 6, the cart/checkout caching failure). **HPOS migration guide** was already placed in Section 4; do not repeat the same URL with a different anchor here, choose one placement only (Section 4 per above).
- Evidence to use: research file section 3, all 8 cases (7 are the "documented failure modes" the orchestrator's brief specifies; case 8, the widget_text filter, is the 7th distinct WooCommerce-shortcode-relevant case if case 6 and case 7 are counted separately, so the creator should number 1-7 using cases 1,2,3,4,5,6,8 or fold case 7's Elementor regression in as its own numbered case alongside case 6, landing on exactly 7 numbered items; use judgment to hit "7 documented failure modes" as stated in the locked brief without dropping any case's information).

### PAA (Template H, ~160 words, 3 Q&As)

- Frame as pushback/skeptic questions, per Format E's guidance that PAA should cover pushback: e.g. "But doesn't WooCommerce's own site say to use blocks instead?", "Will shortcodes eventually be removed?", "Is `[products]` safe to keep using on a high-traffic store?"
- Each answer 2-3 sentences, direct-answer-first, matching real search-intent phrasing.

### Close (Conclusion, Template I, ~120 words)

What the reader walks away with: shortcodes are safe to keep using where they're the right technical fit; the real work is verifying extension/gateway block-compatibility and fixing the specific failure mode they're hitting, not migrating away from shortcodes out of fear. No internal links in the conclusion (rule: body sections only).

### FAQ (Template J, ~500-550 words, 6-8 Q&As)

Suggested questions (creator may adjust to match real search phrasing, keep 3-sentence-max answers):
1. Are WooCommerce shortcodes deprecated?
2. What happened to the WooCommerce product-grid blocks?
3. Does `[woocommerce_my_account]` have a block version?
4. Why is my shortcode showing as text on the page instead of running?
5. Can I use a WooCommerce shortcode inside a block theme?
6. What's the difference between the shortcode and block checkout?
7. Why does my `[products skus="..."]` shortcode return nothing?
8. Is it safe to keep the classic cart and checkout shortcodes?

## Must include

- The correction stated plainly and early: none of WooCommerce's 11 core shortcodes are deprecated as of WooCommerce 11.0 (Aug 4, 2026); the soft-deprecation applies only to older product-grid blocks since WC 9.5.
- Full, accurate attribute list for all 11 shortcodes plus `[related_products]` as a bonus, exactly matching the research file, no invented attributes.
- At least one copy-paste example per shortcode family using straight quotes.
- One Template N comparison table: shortcode vs. block.
- Numbered/checklist presentation of the 7 troubleshooting cases (Symptom / Cause / Fix).
- 10-15 semantic terms woven naturally, drawn from: block editor, Gutenberg, full site editing (FSE), block theme, classic theme, Product Collection block, Cart block, Checkout block, Store API, page builder, template part, transient cache, High-Performance Order Storage (HPOS), payment gateway compatibility, product taxonomy, do_shortcode.
- Minimum 6 H3 subheadings article-wide (outline above specifies 10-11; do not drop below 6 even if the creator condenses).
- FAQ of 6-8 Q&As, PAA of 3-4 Q&As, both direct-answer-first, max 3 sentences per answer.
- All 9 internal links placed per the section-by-section map above, with the specified 2-5 word anchor text (never a long descriptive clause, never repeated anchor text for the same or different URLs).

## Must NOT include

- No claim that shortcodes will be removed or have an announced removal date. None exists.
- No claim of an FSE-exclusive shortcode bug. Research found none; frame Section 4 as "same causes as classic themes," not "FSE breaks shortcodes."
- No stating the out-of-stock counting bug (case 4) or the HPOS/tracking-plugin risk as established fact. Attribute both explicitly as single-sourced reports, or omit them.
- No claiming GitHub issue #31709 is confirmed open or confirmed fixed today. State it as reported, unresolved as of the visible thread.
- No generalized "Elementor breaks WooCommerce" claim. The regression is specific to Elementor 3.33.5; always name that version number.
- No fabricated case studies, client names, or invented statistics (e.g., no invented performance benchmark for shortcode vs. block).
- No em dashes anywhere (banned per section 7). No banned hype/filler words (delve, leverage, revolutionary, game-changing, cutting-edge, transform your, in conclusion, etc., per `voice.md` and `brand.md`).
- No linking to any competitor domain from the do-not-cite list in `brand.md` (Absolute Web, Coalition Technologies, Blue Stout, Tako Agency, Shero Commerce, Born Group, VL OMNI, Fuel Made, Electric Eye, Underwaterpistol) or to platform competitor domains (shopify.com, bigcommerce.com). This topic shouldn't naturally trigger any of these, but the publisher should still check.
- Max 2 external, non-virtina.com links total. If citing developer.woocommerce.com or a GitHub issue directly, that counts toward the 2-external cap; keep external links to at most 2 (e.g., one developer.woocommerce.com source and one GitHub issue, or fewer), everything else stays as attributed prose without a hyperlink, or cite via internal Virtina-hosted context instead.

## Headline direction

Tone: declarative correction, no question marks required but acceptable if it reads as a direct-answer AEO headline, sentence case throughout, no clickbait.

1. Are WooCommerce shortcodes deprecated? No, and here's what's actually happening in 2026
2. WooCommerce shortcodes aren't dead: the complete 2026 reference and troubleshooting guide
3. Stop calling WooCommerce shortcodes deprecated: the 2026 reference and fix guide

All three pass Check 1 (no existing Virtina title shares 3+ consecutive meaningful words; zero titles in the inventory contain "shortcode"). Slug: `woocommerce-shortcodes`, passes Check 2 (no existing slug is a substring or shares 2+ words; "shortcodes" appears in zero existing slugs, only the common "woocommerce" prefix overlaps).

## Open questions for the creator

- Exact numbering/grouping of the 7 troubleshooting cases (research documents 8 candidate cases across cases 1-8; fold two related cases together, likely the caching case and the Elementor regression under one "cart/checkout failures" umbrella, or present all 8 and adjust the "7 failure modes" framing to "8" if that reads more honestly, creator's call, just don't drop any case's factual content).
- Whether to add a short optional H3 for `[related_products]` in Section 2 or fold it into a single closing sentence, depending on final section 2 length.
- Final FAQ question wording, to better match real search phrasing if the creator has additional SERP data.
- Featured and body image concepts (per `MUST-FOLLOW-RULES.md` section 3): featured image should show a business/office/ecommerce scene (e.g., laptop with a WordPress admin screen, developer at a desk); body images at 670x352 for the reference section (code/admin screen), the decision-framework section (team discussing a comparison), and the troubleshooting section (developer debugging), avoiding generic or nature stock per the rules.
