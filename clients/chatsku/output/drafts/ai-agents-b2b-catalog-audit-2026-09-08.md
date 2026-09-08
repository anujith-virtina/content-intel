---
title: We tested 20 real B2B catalogs to see what AI agents can actually read
client: chatsku
date: 2026-09-08
topic: A first-party audit of 20 real B2B distributor and manufacturer catalogs, testing what an AI agent can reach and read at product level
audience: Sales and ops leaders at B2B manufacturers, distributors, and wholesalers ($1M-$50M revenue)
stage: draft
slug: ai-agents-b2b-catalog-audit
format: Format F (case study / audit write-up)
research: clients/chatsku/output/research/ai-agents-visit-b2b-catalog-2026-09-08.md
primary_keyword: AI agents B2B catalog
secondary_keywords: agent-readable product data, AI crawler B2B, machine-readable catalog
word_count: 2043
meta_title: "We Tested 20 B2B Catalogs for AI Agents | ChatSKU"
meta_description: "We ran an automated reader at 20 real B2B catalogs. None blocked AI agents in robots.txt. Only 5 of 20 served a product page a machine could read."
headlines:
  - "We tested 20 real B2B catalogs to see what AI agents can actually read"
  - "20 B2B catalogs, one automated reader: only 5 had a product page it could read"
  - "Nobody is blocking AI agents. 15 of 20 catalogs still gave one nothing"
---

[FEATURED IMAGE - 860x452 | slot: top | concept: a distributor's product data or catalog page open on a desktop monitor in a working office, spec sheets or part listings visible on screen, no branding. Pose exclusions: no hand-to-chin-at-laptop, no tired-man-leaning-over-laptop, no stock "AI brain" graphics.]

<h2>Executive summary</h2>

<p>On 8 September 2026 we pointed an automated reader at 20 real B2B catalogs. Only 5 of them served a product page it could read.</p>

<p>We expected to find gatekeeping. We found the opposite. Of the 13 robots.txt files we could read, zero blocked any of the 12 AI agents we checked. Nobody was shutting the door on purpose.</p>

<p>The refusals happened somewhere else entirely. Seven of the 20 would not answer an automated request at all. Of the 13 that did answer, 7 exposed no product URL a machine could find, and 1 returned an error on the product page itself.</p>

<p>So the published policy says come in. The plumbing says no. That is a very different problem, and a much more fixable one.</p>

<h2>Introduction</h2>

<p>Fifteen of twenty B2B catalogs gave an automated reader nothing usable at product level. That is the finding. We ran it ourselves, today, and you can re-run it.</p>

<p>No survey. No vendor report. Two scripts, 20 named distributors and manufacturers, one product page each.</p>

<p>Here is why we bothered. Buyers are increasingly sending software ahead of themselves, which is <a href="/what-is-agentic-commerce/">what agentic commerce means</a> in practice. That software reads whatever your site hands it and scores you on that alone.</p>

<p>It does not call to clarify. It does not fill in your form. If it cannot find your part number, your price, or your stock position, you are simply not on the short list.</p>

<p>We assumed the industry was quietly locking AI crawlers out while legal figured out a position. The doors were unlocked. There was just nothing behind most of them a machine could read.</p>

<h2>What did we test, and how?</h2>

<p>Twenty public B2B catalogs, one product page each, on 8 September 2026. Every number in this post comes from that run.</p>

<p>Here is the full list, so you can check our work: Grainger, McMaster-Carr, Fastenal, MSC Industrial, Motion Industries, Applied Industrial, Zoro, Global Industrial, DigiKey, Mouser, Newark, Allied Electronics, Ferguson, Wesco, Border States, Rexel USA, Hisco, Kaman, Genuine Parts, and Sonepar. All are real distributors or manufacturers. None is a competitor of ours.</p>

<p>The method was deliberately boring:</p>

<ul>
<li><strong>One request per host.</strong> We asked for robots.txt, then for a single product page. No crawling, no load.</li>
<li><strong>The site chose the product page.</strong> We took it from the company's own declared sitemap, or failing that from a product link on its own homepage.</li>
<li><strong>We used a normal desktop browser User-Agent.</strong> This is the friendly version of the test. A crawler identifying honestly as GPTBot or ClaudeBot would very likely do worse, not better.</li>
<li><strong>JavaScript was not executed.</strong> Some AI crawlers render pages. Others do not. What we measured is what a non-rendering retrieval client receives.</li>
<li><strong>n = 20, one page each.</strong> This is an audit, not a statistical sample. We report counts, never percentages of the industry.</li>
</ul>

<p>The scripts are re-runnable and the results are a snapshot dated 8 September 2026. Sites change. Ours might have changed by the time you read this, and so might theirs.</p>

<h2>Is anyone blocking AI agents on purpose?</h2>

<p>No. Not one of them.</p>

<p>Robots.txt is the plain text file at the root of a website that tells automated readers which parts they may fetch. It is the closest thing the web has to a published door policy.</p>

<p>Of the 13 catalogs whose robots.txt we could read, <strong>zero blocked any of the 12 AI agents we tested</strong>. That list included GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, PerplexityBot, Google-Extended, CCBot, Amazonbot, and Bytespider.</p>

<p>Not a single Disallow rule aimed at any of them. Whatever your board thinks the industry position is on AI crawlers, the published position is open.</p>

<p>The other 7 robots.txt files could not be read at all. Which is a finding of its own.</p>

[BODY IMAGE 1 - 860x452 | slot: end of "Is anyone blocking AI agents on purpose?" | concept: a server rack or network operations screen in a business setting, suggesting edge infrastructure and traffic filtering rather than a person. Alternative: two colleagues at a monitor reviewing website traffic logs.]

<h2>Then why did 7 of 20 refuse the connection?</h2>

<p>Bot protection at the edge, almost certainly. Not policy.</p>

<p>Seven hosts would not answer a plain automated request at all. This happened before any question of content, markup, or product data. The connection itself was the problem.</p>

<div style="overflow-x:auto;width:100%;margin:20px 0;">
<table style="border-collapse:collapse;width:100%;min-width:420px;font-size:15px;margin:0;">
<thead>
<tr>
<th style="background:#1a1a2e;color:#fff;padding:10px 12px;text-align:left;">What happened</th>
<th style="background:#1a1a2e;color:#fff;padding:10px 12px;text-align:left;">Count</th>
<th style="background:#1a1a2e;color:#fff;padding:10px 12px;text-align:left;">What it means</th>
</tr>
</thead>
<tbody>
<tr style="background:#f0f4ff;">
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">HTTP 403, refused</td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;"><strong>5 of 20</strong></td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">Something in front of the site decided the request was not a person</td>
</tr>
<tr style="background:#ffffff;">
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">Connection timed out</td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;"><strong>2 of 20</strong></td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">No answer at all within the wait window</td>
</tr>
<tr style="background:#f0f4ff;">
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">Answered the connection</td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;"><strong>13 of 20</strong></td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">Got as far as the content question</td>
</tr>
</tbody>
</table>
</div>

<p>Remember the User-Agent detail. We were presenting as an ordinary desktop browser and still got shut out. An agent that identified itself honestly would have a harder time, not an easier one.</p>

<p>This is the gap that should worry you most, because it is invisible from the inside. The policy layer says yes. The edge layer says no. The person who wrote your robots.txt is rarely the person who configured your bot protection, and neither one is checking the other's work.</p>

<h2>How many catalogs gave an agent a product page it could read?</h2>

<p>Five of twenty.</p>

<p>Work through the 13 that answered. <strong>Seven exposed no product URL at all</strong> that could be found in their sitemap or in their homepage HTML. A sitemap is the machine-readable index of a site's pages, and if products are missing from it, an agent has no path in.</p>

<p>In most of those cases the category menus and product links are built by JavaScript after the page loads. A person sees a full catalog. A non-rendering client sees a shell with no way through to a product.</p>

<p><strong>One more returned an error on the product page itself</strong>, after serving robots.txt without complaint. So the door opened, then the room was locked.</p>

<p>That leaves 5 of 20 catalogs that put a readable product page in front of an automated reader. If you want the mechanics of what happens next, we have written up <a href="/how-ai-product-search-works/">how AI product search works</a> once the data is actually reachable.</p>

<h2>What was on the five pages that did answer?</h2>

<p>Less than you would guess. And the gaps were not deliberate.</p>

<p>Structured data is a labelled copy of the facts on a page, written for machines, so software does not have to guess which number on screen is the price. Schema.org is the shared vocabulary most search engines and AI systems use for those labels.</p>

<div style="overflow-x:auto;width:100%;margin:20px 0;">
<table style="border-collapse:collapse;width:100%;min-width:640px;font-size:14px;margin:0;">
<thead>
<tr>
<th style="background:#1a1a2e;color:#fff;padding:10px 12px;text-align:left;">Catalog</th>
<th style="background:#1a1a2e;color:#fff;padding:10px 12px;text-align:left;">Visible words</th>
<th style="background:#1a1a2e;color:#fff;padding:10px 12px;text-align:left;">Structured data</th>
<th style="background:#1a1a2e;color:#fff;padding:10px 12px;text-align:left;">Price in structured data</th>
<th style="background:#1a1a2e;color:#fff;padding:10px 12px;text-align:left;">Availability</th>
</tr>
</thead>
<tbody>
<tr style="background:#f0f4ff;">
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">Kaman</td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">1,721</td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">Yes, not Product schema</td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">No</td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">No</td>
</tr>
<tr style="background:#ffffff;">
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">Global Industrial</td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">784</td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">Yes, not Product schema</td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;"><strong>Yes</strong></td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;"><strong>Yes</strong></td>
</tr>
<tr style="background:#f0f4ff;">
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">Zoro</td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">689</td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;"><strong>Yes, full Product schema</strong></td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;"><strong>Yes</strong></td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;"><strong>Yes</strong></td>
</tr>
<tr style="background:#ffffff;">
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">Unnamed catalog 1</td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">115</td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">None</td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">No</td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">No</td>
</tr>
<tr style="background:#f0f4ff;">
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">Unnamed catalog 2</td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">75</td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">None</td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">No</td>
<td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;">No</td>
</tr>
</tbody>
</table>
</div>

<p>Two of the five are unnamed on purpose. Their pages are built by JavaScript, so an agent that renders may well see a full product page where our non-rendering client saw a stub. Naming them would be a claim our method cannot support.</p>

<p>Across all five: schema.org Product markup on <strong>1 of 5</strong>. Price in structured data on <strong>2 of 5</strong>. Availability on <strong>2 of 5</strong>. A manufacturer part number or GTIN in structured data on <strong>2 of 5</strong>.</p>

<p>The bright spots deserve names. Zoro was the only site of the twenty with full Product structured data. Global Industrial published price and availability in structured data and backed it with an 18-row spec table. Kaman served the deepest readable page in the set at 1,721 words, with a 25-row spec table.</p>

<p>Now the detail that reframes everything. <strong>Zero of the five put a login or a quote wall in the way.</strong> Nothing was being withheld as strategy. The data simply was not in the HTML.</p>

<p>And two of the five returned under 200 visible words. A buyer sees a full page. A retrieval client sees a headline and a menu.</p>

<h2>What this audit does not prove</h2>

<p>Plenty. We would rather say it than have you find it.</p>

<p>Twenty hosts and one product page each is an audit, not a survey of the industry. Treat every number here as "5 of 20", never as a percentage of B2B distribution.</p>

<p>We also cannot tell you what any of this costs anyone. No revenue figure, no conversion figure, and no lost-deal estimate can be honestly derived from a set of 20 page fetches. Anyone selling you one from data like this is guessing.</p>

<p>And JavaScript rendering is a real variable, not a technicality. Some agents render. Some do not. A catalog that fails our test may pass for a different reader tomorrow.</p>

<h2>What should you check on your own catalog this week?</h2>

<p>Six things. None of them needs a project, and most take under an hour.</p>

<ul>
<li><strong>Read your own product page with JavaScript disabled.</strong> Or just view the page source. If the price, specs, and stock line are not in the text, an agent may never see them.</li>
<li><strong>Ask whoever runs your bot protection what it does to non-browser traffic.</strong> Your robots.txt can say yes while your edge quietly says no. Nobody finds this out by accident.</li>
<li><strong>Open your sitemap and search it for a product URL.</strong> If products are not listed, an agent has no route to them.</li>
<li><strong>Confirm price and availability exist as labelled data</strong>, not only as styled text inside a widget that loads late.</li>
<li><strong>Check that part numbers and cross-references are on the page as text.</strong> A buyer holding a rival's number should still land on yours.</li>
<li><strong>Count how much sits behind a login.</strong> Not one of our five readable pages used a wall, so the assumption that everybody gates this data is worth re-testing.</li>
</ul>

<p>If the failure is in your source data rather than your site, start upstream. Our <a href="/erp-export-ai-agent-ready/">ERP export self-check</a> covers the file itself: field integrity, duplicate SKUs, units of measure, price tiers. This post covers the website. They are two different surfaces and both can fail independently.</p>

<p>For the wider business case, we have argued elsewhere why <a href="/ai-ready-b2b-catalog-autonomous-buying/">machine-readable catalogs</a> are becoming a commercial requirement rather than an IT preference.</p>

<p>ChatSKU approaches the same gap from the opposite direction. Rather than waiting for a front-end rebuild, it answers product questions on your site from the source files your team already maintains. Setup is a single embed, not a replatform. If you are weighing that against repairing your markup, start with our <a href="/what-is-a-b2b-catalog-chatbot/">B2B catalog chatbot guide</a> and the <a href="/roi-calculator/">ROI calculator</a>. Because it was designed <a href="/for-b2b-manufacturers-distributors-and-wholesalers/">for distributors and wholesalers</a>, buyer-specific pricing tiers are native rather than bolted on. The full list of <a href="/features/">ChatSKU's catalog integrations</a> is here.</p>

[BODY IMAGE 2 - 860x452 | slot: end of "What should you check on your own catalog this week?" | concept: an operations or ecommerce manager at a desk reviewing a product spec sheet against a screen, checking data rather than posing. Warehouse or office background acceptable.]

<h2>People also ask</h2>

<h3>Does blocking AI crawlers protect my catalog data?</h3>

<p>It might protect it from being copied. It will not protect your position on a short list. In our run, blocking was not the reason 15 of 20 catalogs came back empty. Broken access and missing labels were.</p>

<h3>Is a 403 error to an AI agent a security setting or a mistake?</h3>

<p>Usually neither, exactly. It is bot protection doing the job it was configured to do, before anyone considered that some bots are now buyers. It is a settings conversation, not a rebuild.</p>

<h3>If my site works fine for Google, will it work for AI agents?</h3>

<p>Not necessarily. Google has rendered JavaScript for years and has a crawl budget you cannot buy. A retrieval client fetching one page in real time has neither.</p>

<h3>How many products need to be readable before this matters?</h3>

<p>Start with the ones you actually want to sell. Your top movers, your stocked lines, and anything with a cross-reference. Fixing 200 pages that earn revenue beats fixing 40,000 that do not.</p>

<h2>Conclusion</h2>

<p>Twenty catalogs. Not one blocking AI agents by published policy. Five with a product page a machine could read.</p>

<p>The gap is not permission. It is plumbing and labels, and both of those are yours to fix.</p>

<p>So run the test yourself this week. Open your best-selling product page with JavaScript disabled, and read what is left on the screen. That is your catalog as software sees it.</p>

<p>If what is left is a headline and a menu, you already know what to do first.</p>

[CTA BUTTON - background #e94560, white text, centered, border-radius 6px: "See the live demo" -> https://chatsku.com/demo/]

<h2>Frequently asked questions</h2>

<h3>What exactly did you test on each of the 20 catalogs?</h3>

<p>Two things. Whether robots.txt allowed 12 named AI agents, and what a single product page returned to a non-rendering client. One request per host, on 8 September 2026.</p>

<h3>Why report counts instead of percentages?</h3>

<p>Because 20 hosts is not a sample of an industry. "5 of 20" is a fact about 20 catalogs. "25% of B2B distributors" would be a claim we cannot support, and you should distrust anyone who makes it from a set this size.</p>

<h3>Would the results change if the test executed JavaScript?</h3>

<p>For some sites, yes. Two of the five readable pages would very likely look much fuller. The 7 refused connections and the 7 with no findable product URL would not improve, because those failed before rendering was ever a question.</p>

<h3>What is structured data, in one sentence?</h3>

<p>It is a labelled copy of the facts already on your page, written in a format software can read without guessing which number is the price and which is the part number.</p>

<h3>Do I need structured data if I already have a catalog assistant on my site?</h3>

<p>They cover different moments. An assistant answers a buyer who has arrived. Structured data helps software decide whether to arrive at all. Most catalogs benefit from both, and the second one is cheaper than it sounds.</p>

<h3>Can I re-run this audit on my own catalog?</h3>

<p>Yes, and you should. Fetch your robots.txt in a browser, then view the page source on a product page and search it for your price and stock text. That is the entire test in five minutes.</p>

---

## Publishing notes

**Format:** F (case study / audit write-up). Format F was last used on post 299 (2026-06-17), so the rotation is clean. Format C (listicle with opinions) was disqualified: this is a genuine first-party audit with a dataset, not an opinion list.

**Body word count:** approximately 2,043 (Executive summary through FAQ, excluding frontmatter, image markers, and these notes). Hard range 1,800-2,200. Publisher should confirm with an exact count before push.

**Yoast meta title (48 chars):**
`We Tested 20 B2B Catalogs for AI Agents | ChatSKU`

**Yoast meta description (152 chars):**
`We ran an automated reader at 20 real B2B catalogs. None blocked AI agents in robots.txt. Only 5 of 20 served a product page a machine could read.`

### Image slots (all 860 x 452, JPEG q82, under 200 KB)

| Slot | Placement | Draft alt text (rewrite at publish against the image actually chosen) |
|---|---|---|
| Featured | Top | "B2B distributor product catalog data open on a desktop monitor, the page an AI agent reads when it visits a supplier site." (121 chars) |
| Body 1 | End of "Is anyone blocking AI agents on purpose?" | "Network operations screen in a distributor's office, the edge layer that returned HTTP 403 to automated requests in our catalog audit." (133 chars) |
| Body 2 | End of "What should you check on your own catalog this week?" | "Operations manager checking product spec data against a screen, the manual audit that reveals what AI agents can read on a B2B catalog." (134 chars) |

Pose exclusions: no hand-to-chin-at-laptop (post 2468 featured), no tired-man-leaning-over-laptop (post 2665 featured), no abstract "AI brain" or circuit-board graphics.

### Links used

Internal (8 inline, 1 button). Zero external.

- `/what-is-agentic-commerce/` — anchor "what agentic commerce means" — Introduction, exactly once
- `/how-ai-product-search-works/` — anchor "how AI product search works" — body 4
- `/erp-export-ai-agent-ready/` — anchor "ERP export self-check" — checklist section, exactly once, explicitly fenced as the export-file audit vs this post's website audit
- `/ai-ready-b2b-catalog-autonomous-buying/` — anchor "machine-readable catalogs" — checklist section. Its $15T / 90%-by-2028 figures are NOT quoted anywhere in this post
- `/what-is-a-b2b-catalog-chatbot/` — anchor "B2B catalog chatbot guide" — checklist section
- `/roi-calculator/` — anchor "ROI calculator" — checklist section
- `/for-b2b-manufacturers-distributors-and-wholesalers/` — anchor "for distributors and wholesalers" — checklist section
- `/features/` — anchor "ChatSKU's catalog integrations" — checklist section
- `/demo/` — Conclusion CTA button only, never an inline link

Page links: 4 (`/roi-calculator/`, `/for-b2b-.../`, `/features/`, `/demo/`). Blog links: 5. Both above the section 6 minimums.

**Never used, per corrected section 6:** `/pricing/`, `/revenue-calculator`, `/lost-b2b-revenue-calculator/`, `/product-information-management-software/`.

**Publisher must verify before push:** `/what-is-agentic-commerce/` (post 2831) was listed as WP draft in MUST-FOLLOW-RULES section 6 but supplied to the creator as verified live 200 on 2026-09-07. Confirm HTTP 200 on the live site or remove the link.

### Stat discipline observed

- Every figure is a count out of 20 or out of 13 or out of 5. No percentage of the industry appears anywhere.
- No revenue, conversion, GMV, or lost-deal figure is claimed or implied from this dataset. A dedicated "What this audit does not prove" section states this explicitly.
- Banned figures confirmed absent: $15T, 90% by 2028, 70% to first accurate quote, Gartner 67% rep-free, 72% self-service.
- Zero external links and zero third-party statistics. The dataset is first-party.

### Naming rule observed

- All 20 catalogs named once, up front, in the method section, so the audit is verifiable.
- Positive findings named: Zoro (only full Product structured data), Global Industrial (price and availability in structured data, 18-row spec table), Kaman (deepest readable page, 1,721 words, 25-row spec table).
- All negative findings reported in aggregate. The two thin/JS-shell pages appear in the results table as "Unnamed catalog 1" and "Unnamed catalog 2", with an inline sentence explaining why we are not naming them.
- The 7 refused connections are reported as counts by failure type (5 HTTP 403, 2 timeout), not as a named list. See the note to the orchestrator.

### Fences observed

- Post 2129 (glossary) owns protocol definitions. No ACP, AP2, MCP, or A2A anywhere in this post.
- Post 2684 (ERP export) owns the export-file audit. Linked once, field-level checks not rebuilt.
- Post 2831 (what is agentic commerce) owns the plain-English definition. Linked once, definition assumed rather than restated, and none of its Deloitte/Forrester/Gartner stats reused.
- Post 2468 owns retrieval mechanics. Linked once, embeddings and ranking not explained.
- No after-hours framing, no 8pm buyer, no "night-shift sales rep". This post is a daylight infrastructure story.
- No em dashes. No banned hype or filler. No code samples. Second person throughout. Sentence case headings.
