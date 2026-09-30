---
title: "Your site search box is keeping a list of everything buyers couldn't find"
client: chatsku
date: 2026-09-30
topic: "How a B2B distributor reads internal site-search data to find where buyers fail to find products"
audience: "owner / ecommerce manager / marketing lead at a B2B manufacturer, distributor or wholesaler, not a data analyst"
stage: draft
slug: site-search-logs
format: "Format B (conversational Q&A)"
research: clients/chatsku/output/research/site-search-logs-2026-09-30.md
primary_keyword: "site search logs"
secondary_keywords: "zero result searches, internal site search report, B2B product search"
word_count: 2210
meta_title: "What Your Site Search Logs Reveal | ChatSKU"
meta_description: "Site search logs already show exactly which buyer queries return zero results in your B2B catalog search, and how to read them before buying new tools."
headlines:
  - "Your site search box is keeping a list of everything buyers couldn't find"
  - "What your site search logs are already telling you"
  - "The zero-result searches your team will never hear about"
---

[FEATURED IMAGE - 860x452 | Laptop on a desk displaying a colourful web analytics dashboard with bar charts, a pie chart and session metrics]

<h2>Executive summary</h2>
<p>You don't need a new tool to find out where your catalog loses buyers. You already have one. It's your site search log, and it's been recording every query, every zero-result page, and every abandoned session since the day your site went live.</p>
<p>Most B2B distributors never open it. They guess instead. Better photos, a bigger banner, a new pop-up on the homepage. Meanwhile the actual list of what buyers typed and couldn't find sits untouched in an analytics dashboard nobody checks.</p>
<p>This post shows you exactly where that data lives on GA4, Magento, and WooCommerce. It covers how to read it without a data background, and what to fix first once you can see it.</p>

<h2>Introduction</h2>
<p>Picture a buyer on your site right now. They type a part number into your search box. Nothing. They try it again with a hyphen instead of a slash. Still nothing. They try the plain-English version, "ball valve half inch." One result, and it's the wrong one. They close the tab and email a competitor.</p>
<p>Nobody on your team will ever hear about that. No support ticket gets filed. No sales rep gets a callback request. As far as anyone in your building knows, that buyer never existed.</p>
<p>But it did happen, and it got recorded. Three queries, three failures, one exit, timestamped, sitting in a report you've probably never opened.</p>

<h2>Where is this data, and do I already have it?</h2>
<p>Yes, you already have it. Where you find it depends on what you're running.</p>
<ul>
<li><strong>GA4.</strong> Reports, then Engagement, then Events. Look for a row called <code>view_search_results</code>, and add <code>search_term</code> as a secondary dimension to see the actual queries people typed.</li>
<li><strong>Magento or Adobe Commerce.</strong> Reports, then Marketing, then Search Terms. It's a real report, exportable, sortable by how many times a term was searched and how many products it matched. Adobe's own <a href="https://experienceleague.adobe.com/en/docs/commerce-admin/catalog/catalog/search/search-terms" target="_blank" rel="noopener noreferrer">Search Terms documentation</a> covers both this report and the separate management grid where you can set redirects.</li>
<li><strong>WooCommerce.</strong> Brace yourself. Core WooCommerce Analytics tracks revenue, orders, products, variations, categories, and customers. Search terms aren't one of the six. You either add the paid Product Search extension or fall back on GA4's event tracking, same as everyone else.</li>
</ul>
<p>Wherever it lives, the log only tells you half the story. It records what buyers asked for. Comparing that against <a href="/features/">what your catalog actually exposes</a> is the other half, and that comparison is where the fixes come from.</p>

<h2>Why does my report look empty when I know people search?</h2>
<p>Because GA4 only counts a search when the term shows up in the page URL, and a lot of search boxes never put it there.</p>
<p>Here's the mechanism. GA4's <code>view_search_results</code> event fires when a visitor lands on a results page. The URL has to contain one of five parameters by default: <code>q</code>, <code>s</code>, <code>search</code>, <code>query</code>, or <code>keyword</code>. You can add up to ten custom ones in enhanced measurement settings, per <a href="https://support.google.com/analytics/answer/9216061?hl=en" target="_blank" rel="noopener noreferrer">Google's own documentation</a>.</p>
<p>That works fine for plenty of WooCommerce search boxes. It breaks completely on AJAX-driven search, which a lot of Magento layered-search widgets and custom search bars use. The results update on the page. The URL never changes. No query parameter, no event, no row in your report, even though enhanced measurement is on by default in current GA4 setups.</p>
<p>So you open GA4, see a handful of rows or none at all, and conclude buyers barely use search. That's usually wrong. What's actually true is your search box never told the URL what happened.</p>
<p>The fix doesn't touch your search engine. Either expose the term in the URL, or push it to the dataLayer with Google Tag Manager and map it to the <code>search_term</code> parameter. Either way, the event starts firing and the rows start showing up.</p>

[BODY IMAGE 1 - 860x452 | Man working alone at a laptop at a wooden desk in a bright modern office, reviewing a report on screen]

<h2>Which rows should I read first?</h2>
<p>Start with the queries that returned nothing, ranked by how often they happened.</p>
<p>A single zero-result search from one visitor might be a typo. The same zero-result query showing up forty times a month is a catalog gap, and it's probably costing you a deal every week. Sort by volume first. That's where the real money is.</p>
<p>Next, look for searches followed by an exit. A visitor searches, sees the results, and leaves the site in the same session. Whatever they found, or didn't find, wasn't good enough to keep them around.</p>
<p>Last, watch for a visitor who searches, refines, searches again, refines again, and then leaves. Read that whole chain as one failed session, not three separate weak signals. As a rough rule of thumb, three attempts in a row before someone leaves is a pattern worth flagging. Adjust that number to whatever your own logs actually show you. It's a guideline, not a finding.</p>
<p>What happens after a search succeeds is a separate question. Your <a href="/b2b-catalog-conversion-rate/">B2B catalog conversion rate</a> covers that side, once your results stop returning zero.</p>

<h2>What do the failures actually look like in a B2B catalog?</h2>
<p>They fall into six recurring patterns, and once you've seen them once, you'll spot them in your own log immediately.</p>
<div style="overflow-x:auto">
<table style="width:100%; border-collapse:collapse; margin:20px 0; font-size:15px;">
<thead>
<tr style="background-color:#1a1a2e; color:#ffffff;">
<th style="padding:12px 15px; text-align:left;">Pattern</th>
<th style="padding:12px 15px; text-align:left;">Example query</th>
<th style="padding:12px 15px; text-align:left;">Why it fails</th>
</tr>
</thead>
<tbody>
<tr style="background-color:#f0f4ff;">
<td style="padding:12px 15px;">Part number punctuation or spacing</td>
<td style="padding:12px 15px;"><code>SS-304-1/2NPT</code>, catalog stores <code>SS304-1/2-NPT</code></td>
<td style="padding:12px 15px;">One dash or space out of place is a different string. Exact-match indexing has no tolerance for it.</td>
</tr>
<tr style="background-color:#ffffff;">
<td style="padding:12px 15px;">Competitor or OEM cross-reference number</td>
<td style="padding:12px 15px;">A rival's or OEM's part number, not your internal SKU</td>
<td style="padding:12px 15px;">That string doesn't exist anywhere in your catalog data. There's nothing for even a fuzzy matcher to partially match.</td>
</tr>
<tr style="background-color:#f9f9fb;">
<td style="padding:12px 15px;">Application or problem language</td>
<td style="padding:12px 15px;">"pump for pool" instead of the product name</td>
<td style="padding:12px 15px;">Keyword search matches literal text in the title and description, not a use case nobody wrote into the copy.</td>
</tr>
<tr style="background-color:#ffffff;">
<td style="padding:12px 15px;">Compound spec string</td>
<td style="padding:12px 15px;">"316 stainless 3/4 npt" as one query</td>
<td style="padding:12px 15px;">Most B2B search defaults to matching every term, too strict and zero results, or any term, too loose and wrong results.</td>
</tr>
<tr style="background-color:#f9f9fb;">
<td style="padding:12px 15px;">Unit-of-measure or pack size</td>
<td style="padding:12px 15px;">"case of 144" expecting UOM-filtered results</td>
<td style="padding:12px 15px;">UOM usually lives as a pricing attribute tied to a SKU record, not as searchable text.</td>
</tr>
<tr style="background-color:#ffffff;">
<td style="padding:12px 15px;">Obsolete or superseded part number</td>
<td style="padding:12px 15px;">A legacy number the manufacturer already replaced</td>
<td style="padding:12px 15px;">If nobody added the old number as a cross-reference on the new product, the catalog has no idea they're the same item.</td>
</tr>
</tbody>
</table>
</div>
<p>The mechanics behind why keyword search breaks on strings like these are worth understanding on their own. <a href="/traditional-b2b-product-search-fails/">Why traditional search fails</a> covers that in full. What matters here is learning to recognize these six shapes the moment you see them in your own report.</p>

<h2>Why won't a synonym list just fix this?</h2>
<p>Because a synonym list only knows what a human already typed in once.</p>
<p>Every one of the six patterns above throws off near-infinite string variants. A part number gets punctuated a dozen different ways. A buyer describes an application in a hundred different phrasings. A synonym dictionary matches literal strings, one at a time. Somebody on your team has to notice each variant and enter it by hand before it ever gets matched.</p>
<p>In Magento specifically, a synonym and a redirect are two separate manual entries per term. There's no bulk rule that says "treat any punctuation variant of this SKU the same." You catch the string a buyer already typed. You never catch the one they'll type tomorrow.</p>
<p>That's a ceiling on the approach, not a flaw in how you've set it up. <a href="/ai-product-search-for-b2b/">AI product search for B2B</a> exists to match on meaning instead of literal strings. A new variant doesn't need a human to notice it first. <a href="/how-ai-product-search-works/">How AI product search works</a> gets into the mechanics behind that, if you want the technical version.</p>

<h2>What do I fix this week, and what needs a real fix?</h2>
<p>Split your zero-result list into two piles. What you can fix by Friday, and what needs a structural change.</p>
<p><strong>Quick wins, this week:</strong></p>
<ul>
<li><strong>Add redirects for your top 10 to 20 zero-result terms.</strong> Point each one at the right product or category page by hand.</li>
<li><strong>Add the obvious synonyms.</strong> Buyer-facing terms your catalog copy doesn't use yet, limited to your highest-volume queries.</li>
<li><strong>Fix the search-then-exit rows with an obvious cause.</strong> A typo in a product title, a missing attribute, a broken filter.</li>
</ul>
<p><strong>Structural fixes, budget for these separately:</strong></p>
<ul>
<li><strong>Application-language and compound-spec queries.</strong> No manual entry list keeps up with how many ways a buyer can describe a spec.</li>
<li><strong>Cross-reference and superseded part numbers.</strong> These need a mapping layer, not a redirect list that grows forever.</li>
<li><strong>Search that understands meaning, not just literal strings.</strong> This is what closes the gap a synonym list can't. <a href="/ai-product-search-for-b2b/">meaning-based catalog search</a>, and run your own numbers with the <a href="/roi-calculator/">ROI calculator</a> before deciding whether it's worth the change.</li>
</ul>

[BODY IMAGE 2 - 860x452 | Two colleagues at a white office table reviewing figures together with a laptop, tablet and notepad]

<h2>How do I know it worked?</h2>
<p>Pull the same zero-result query list again, over the same length of time, and see which ones dropped off.</p>
<p>Don't compare against an industry number. There isn't a credible one to compare against, no matter what a vendor blog tells you. The benchmarks that get quoted for this metric don't trace back to any named study once you check the source. Your own baseline, measured before and after, is the only comparison that means anything for your catalog.</p>
<p>Give it a full reporting cycle, at minimum a month, so seasonal query patterns don't skew the read. Watch three things. Are your top zero-result terms from before still zero-result now? Did the search-then-exit rate on those terms drop? And did the multi-refinement sessions get shorter?</p>
<p>If you want to see what a working search layer looks like first, <a href="/demo/">the live demo</a> walks through it on a real B2B catalog.</p>

<h2>People also ask</h2>
<h3>Is GA4 automatically tracking my site search?</h3>
<p>Enhanced measurement turns it on by default in current GA4 setups, but only for searches where the term shows up in the URL. If your search box doesn't write the term to the URL, GA4 records nothing even though tracking is switched on.</p>
<h3>Does WooCommerce track search terms by default?</h3>
<p>No. Core WooCommerce Analytics covers revenue, orders, products, variations, categories, and customers. Search terms require the paid Product Search extension or the same GA4 event tracking every other platform relies on.</p>
<h3>How many searches should I look at before I trust a pattern?</h3>
<p>Look at volume, not a single instance. One zero-result search could be a typo. The same query returning nothing dozens of times a month is a real gap worth fixing first.</p>

<h2>Conclusion</h2>
<p>You don't need a survey to find out where your catalog loses buyers. You need twenty minutes in a report you already have.</p>
<p>Pull your zero-result list this week. Read it the way we just walked through. Fix what you can fix by Friday, and flag what needs a real search layer instead of another redirect.</p>
<p>Your buyers have already told you exactly where they're stuck. All that's missing is someone reading the log.</p>

<h2>Frequently asked questions</h2>
<h3>Where exactly do I find site search data in GA4?</h3>
<p>Reports, then Engagement, then Events. Find the <code>view_search_results</code> row and add <code>search_term</code> as a secondary dimension. Or build a free-form Explore report, with <code>search_term</code> as the dimension and event count as the metric.</p>
<h3>What's the difference between Magento's Search Terms grid and its Search Terms report?</h3>
<p>Marketing, then SEO and Search, then Search Terms is a management grid, where you set a redirect URL or suggested terms per query. Reports, then Marketing, then Search Terms is a separate, exportable analytics view of the same underlying data, better for sorting by volume.</p>
<h3>Why would a synonym list not be enough for my catalog?</h3>
<p>Because it only covers literal strings someone has already typed and someone has already noticed. Part numbers, application phrases, and spec strings generate more variants than any team can enter by hand, one at a time.</p>
<h3>Should I trust the zero-result-rate benchmarks I see online?</h3>
<p>No. The percentages that circulate for this metric don't trace back to a named study when you check the cited source directly. Measure your own zero-result rate and use it as your own baseline instead of comparing to an unverifiable industry number.</p>
<h3>How long should I wait before re-checking my search log after a fix?</h3>
<p>Give it a full reporting cycle, at minimum a month, so normal seasonal variation in queries doesn't get mistaken for a real change either way.</p>
<h3>Does this diagnostic work if I don't have a developer on staff?</h3>
<p>Yes. Reading the GA4, Magento, or WooCommerce report requires no code. One step may need a developer: exposing a search term in the URL, or wiring it into Google Tag Manager. That only applies if your current search box doesn't already do it.</p>

[CTA BUTTON - See the live demo -> https://chatsku.com/demo/]
