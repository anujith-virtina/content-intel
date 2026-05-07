---
title: Brief — How B2B manufacturers can fix slow WooCommerce stores without replatforming
client: virtina
date: 2026-04-30
topic: WooCommerce B2B performance optimization
audience: B2B eCommerce leaders at manufacturers/distributors/wholesalers
stage: brief
slug: woocommerce-b2b-performance-fix-2026-04-30
research: clients/virtina/output/research/woocommerce-b2b-performance-fix-2026-04-30.md
---

# Brief: Your WooCommerce store isn't slow — it's misconfigured for B2B

## Thesis

> Most slow WooCommerce B2B stores have one or two specific, fixable failures masquerading as a platform problem — a 60-second diagnostic tells you which bottleneck is costing you the most revenue, and replatforming is almost never the right first answer.

## Angle scoring

| Criterion | Score (1–5) | Notes |
|---|---|---|
| Originality | 5 | No competitor addresses B2B-specific failure modes or provides a fix-vs-replatform decision framework |
| Audience fit | 5 | Exactly the question a VP eCommerce or Ecommerce Manager Googles when their store is slow |
| Brand fit | 5 | Core Virtina territory: B2B performance as a revenue lever, not a tech metric; contrarian framing matches the "Marketplace Trap" style |
| Evidence strength | 4 | Strong platform-level benchmarks; gap is named client case studies with before/after numbers — handled in brief |

## Why this, why now, why us

- **Why this angle:** Every existing article on "slow WooCommerce" is written for B2C operators or developers. None address the architectural differences that make B2B WooCommerce slow in completely different ways — authenticated users bypassing page cache, ERP sync firing on every request, B2B plugin query overhead. The competitive gap is real and documentable.
- **Why now:** WooCommerce 9.8 and 10.x delivered major performance improvements (51.9% faster slowest admin requests, up to 95% critical page-load reduction). HPOS is now the default in 10.x. Stores on 6.x or 7.x avoiding upgrades are compounding their performance debt. The fix-in-place case has never been stronger.
- **Why Virtina:** Virtina is a certified WooCommerce Expert with 1,000+ clients, including B2B manufacturers and distributors — this is not generic advice. The brief instructs the creator to weave credentials in naturally, not as a pitch.

## Audience

VP eCommerce, Director of Digital, and Ecommerce Manager at B2B manufacturers, distributors, and wholesalers running WooCommerce. Companies in the $5M–$500M revenue range. They know their platform and integrations deeply. They do not need WooCommerce basics explained. They are already suspicious the problem might require replatforming and are looking for an honest, expert answer — not reassurance.

Do not explain: what WooCommerce is, what TTFB means, what an ERP is, what a plugin is, what Core Web Vitals are. Assume all of these are known.

## Format and length

- Format: How-to diagnostic guide with embedded decision framework
- Target length: 2,000–2,500 words (lean toward 2,300)
- Reading time: 8–10 minutes
- Structure: Summary block → Introduction → TOC → 60-second self-audit → Bottlenecks by impact order → Fix-vs-replatform decision criteria → People Also Ask (3–4 Q&As) → Conclusion → FAQ (6–8 Q&As)

---

## Structure

### Hero image concept

A VP or Director at a desktop workstation, multiple monitors showing WooCommerce admin and analytics dashboards, manufacturing or warehouse context visible in background (shelving, industrial space). Photorealistic, not stock-photo generic. Do not use abstract blue-glow tech imagery. Standard size: 1309×500. Alt text: "WooCommerce B2B performance optimization — eCommerce manager reviewing store diagnostics."

---

### Summary block (not a section heading — this is the opening block above the intro)

Opens with a scenario, not a definition. Pattern from the Agentic AI example.

Suggested scenario frame: A B2B eCommerce manager whose store loads in 6 seconds for authenticated buyers, whose team has been told by two agencies it's a "WooCommerce limitation," and who is about to approve a $150K replatforming project. The twist: it's a Redis configuration that takes an afternoon to fix.

The summary should land the thesis in 2–3 sentences without bullet points.

---

### Introduction (1–2 paragraphs)

Sets up the problem: B2B WooCommerce has architectural differences from B2C that make generic speed guides useless. Authenticated buyers bypass full-page cache entirely. ERP sync fires per-request. B2B pricing plugins run database lookups on every page load. The result is that a technically competent team can follow every standard WooCommerce optimization guide and see no improvement.

End the introduction by pointing to the self-audit below as the entry point.

---

### Section 1: The 60-second self-audit (decision tree)

**What this section does:** Lets the reader identify which of the five bottleneck categories is their primary problem before reading further. Each branch of the tree leads to the numbered section below.

**Format:** A short framing paragraph, then the decision tree as a structured list. Not a visual diagram (the creator cannot generate diagrams) — use indented bullet logic that reads clearly as a tree.

**The five branches and their diagnostic signal:**

| Symptom | Likely bottleneck | Go to |
|---|---|---|
| High TTFB (>600ms) on all pages, even uncached | Hosting/server config or database | Section 2 (hosting) or Section 5 (database) |
| Slow for logged-in buyers only; anonymous visitors are fine | B2B caching architecture | Section 3 (plugin/caching) |
| Checkout is slower than everything else; cart pages fine | Checkout-specific failures | Section 4 (checkout) |
| Admin is slow; order management takes 10–30 seconds | HPOS not enabled; Action Scheduler bloat | Section 5 (database) |
| Speed degrades after ERP sync events or inventory updates | ERP sync architecture | Section 6 (ERP) |

**Diagnostic tools to name:** Query Monitor (WP plugin — flag queries >100 per page as the threshold), WooCommerce Health Check (WooCommerce > Status > Tools), New Relic or Datadog for server-side tracing. TTFB measurement: WebPageTest.org with a logged-in user session.

**Key instruction to creator:** The audit should feel like a quick triage, not a comprehensive tutorial. Keep it tight — 150–200 words maximum for this section. The bottleneck sections do the real work.

---

### Section 2: Hosting and server configuration

**Why it's first in the body:** Most B2B WooCommerce operators on shared or entry-level managed hosting are sitting on 10x performance gains from pure config changes. This is the highest-revenue-impact fix for the largest cohort of readers.

**Key point:** Default server configuration is not tuned for WooCommerce — and almost no managed hosting provider sets InnoDB buffer pool, OPcache, or PHP-FPM correctly out of the box.

**What to cover:**
- InnoDB buffer pool: default 128MB means MySQL reads from disk on every query (200ms per query vs. 2ms in memory); set to 70–80% of available RAM on a dedicated DB server. For WooCommerce databases over 500MB, this single change is typically the biggest TTFB win.
- OPcache: `memory_consumption` at 128MB minimum (256MB for large stores); `max_accelerated_files` at 20,000+; `interned_strings_buffer` at 32–64MB (default 8MB is undersized for WooCommerce with many plugins).
- PHP memory limit: 256MB minimum per WooCommerce official; 512MB for stores with 1,000+ products and active B2B extensions. Below this, large order processing silently fails with "Allowed memory size exhausted" errors.
- PHP-FPM: use `pm = static` for sustained B2B traffic; `pm = dynamic` fails under both sustained load and sudden spikes.
- MySQL query cache: must be disabled (`query_cache_type = 0`). It serializes all writes through a global mutex lock — still left enabled by default on many managed hosts running older MySQL 5.7 branches.
- Hosting tier red lines: Bluehost, GoDaddy, HostGator are explicitly inadequate for B2B WooCommerce. Minimum acceptable tier is premium shared (SiteGround, A2). VPS (UpCloud, Vultr HF) is the best price-to-performance option — one benchmark shows uncached demo stores loading under 100ms on UpCloud.

**Data to use:**
- InnoDB disk read: 200ms vs. 2ms in-memory — source: [Marcin Dudek, 2026](https://marcindudek.dev/blog/30-wordpress-woocommerce-performance-tips-2026/)
- TTFB target: <200ms; Google flags >600ms — source: [Online Media Masters, 2025](https://onlinemediamasters.com/speed-up-slow-woocommerce-store/)

**Section image concept:** Server rack or cloud infrastructure dashboard on a monitor — clean, professional, business context.

**End of section:** Forward-pointing line that hints at the caching problem specific to B2B.

---

### Section 3: B2B caching — why page caching alone fails authenticated buyers

**Key point:** B2B WooCommerce is architecturally incompatible with full-page caching, which means every generic "enable caching" recommendation misses the actual fix. The correct solution is Redis object caching — not page caching.

**What to cover:**
- The core problem: every authenticated B2B buyer sees individualized pricing, customer-specific catalogs, and role-based product visibility. Full-page caching either serves the wrong content (a poisoned cache bug — B2C visitor sees a B2B price tier) or bypasses on every authenticated request and delivers no benefit.
- The right fix: Redis object caching stores the results of expensive database queries (role lookups, pricing calculations, visibility checks) at the object level and serves them on subsequent requests within the same session. This is where B2B stores get their caching wins.
- Correct Redis configuration: set `maxmemory-policy volatile-lru` to prevent eviction of persistent keys; ensure user-specific pricing data is scoped per-user at the object level — default Redis config does not do this.
- If using Nginx FastCGI: bypass rules must key on `woocommerce_items_in_cart` and user session cookies; without these, checkout serves cached state and payment gateway tokens expire.
- WP Rocket: per-user cache feature is available but requires explicit configuration — it's off by default.
- B2BKing-specific: enable the Product Visibility Cache toggle (Settings > Other); add `b2bking_use_simple_query_system` and `b2bking_flush_permalinks` filters to reduce per-request query load. These are documented in B2BKing's own performance guide.

**Data to use:**
- WholesaleX Pro admin page load >30 seconds before fix — source: B2BKing community reports (flag as unverified exact timing — the point is the failure mode is real and documented)
- Source: [B2BKing Hosting & Performance Guide](https://woocommerce-b2b-plugin.com/woocommerce-b2b-hosting-performance-what-really-matters/), 2025

**Creator note:** Name the specific plugins (B2BKing, WholesaleX, Wholesale Suite) with their specific config flags — this is what separates this from generic WooCommerce advice and earns credibility with the target reader.

---

### Section 4: Checkout failures — a separate diagnostic pass from page speed

**Key point:** Checkout is where GMV is won or lost, and its failure modes are distinct from general slowness — fixing TTFB won't fix checkout if the real problem is PHP memory exhaustion or a misconfigured payment gateway.

**What to cover:**
- Custom pricing not reflecting at checkout: price filters running after the cart is built — common when B2B plugins hook into `woocommerce_cart_item_price` too late in the filter chain. Fix: audit filter priority order with Query Monitor.
- Caching the checkout page: misconfigured Nginx FastCGI cache without the `woocommerce_items_in_cart` cookie bypass causes checkout to serve stale state. Roughly 15% of checkout-blocking issues trace to this. Fix: verify cache bypass rules in Nginx config.
- Payment gateway timeout at high AOV: multiple gateways loaded simultaneously add round-trip API calls. At B2B order values in the thousands, timeout thresholds get hit. Fix: disable unused payment gateways; increase timeout threshold in gateway settings.
- PHP memory exhaustion on large carts: B2B orders with hundreds of line items exhaust PHP memory during order processing when custom pricing runs per line item. Fix: raise PHP memory limit to 512MB minimum; profile with Query Monitor during a large test order.
- Session table bloat: `wp_woocommerce_sessions` grows from bot traffic and expired sessions never cleaned up. Fix: schedule regular WP-CLI cleanup (`wp db query "DELETE FROM wp_woocommerce_sessions WHERE session_expiry < UNIX_TIMESTAMP()"`).

**Data to use:**
- 70% of carts abandoned due to sluggish checkout — source: [Pantheon, 2025](https://pantheon.io/learning-center/wordpress/woocommerce-checkout-slow)
- 1-second delay = ~7% conversion drop — source: [WP Rocket speed stats, 2025](https://wp-rocket.me/blog/website-load-time-speed-statistics/)

**Creator note:** These are specific and actionable — keep each sub-point to 2–3 sentences. The reader knows what PHP memory is; don't explain it.

---

### Section 5: Database bottlenecks — HPOS, Action Scheduler, and autoload bloat

**Key point:** HPOS is the single highest-impact free fix available to any B2B WooCommerce store with 50,000+ orders — it is not enabled by default on existing stores and most teams haven't turned it on.

**What to cover:**
- HPOS: moves order data from `wp_postmeta` (hundreds of SQL joins per query at 50k+ orders) to dedicated custom tables (`wp_wc_orders`, `wp_wc_orders_meta`). Must be explicitly migrated on existing stores — it's the default only on new WooCommerce 10.x installs. Requires staging validation because older payment gateways and warehouse integrations can break.
- Action Scheduler bloat: completed jobs in `wp_actionscheduler_actions` are not deleted by default. A high-volume B2B store with ERP sync hooks, email automation, and recurring tasks can accumulate millions of rows — causing slow admin, backup timeouts, degraded cron. Fix: add retention filter to purge completed actions older than 30 days; use WP-CLI to run a one-time cleanup.
- `wp_options` autoload bloat: data loaded on every single page request. Alert threshold is >1MB; many B2B stores with 40+ plugins are at 5–10MB. Fix: query autoloaded rows by size (`SELECT option_name, LENGTH(option_value) FROM wp_options WHERE autoload = 'yes' ORDER BY LENGTH(option_value) DESC LIMIT 20`), identify large entries, and either deactivate the responsible plugin or set autoload to 'no' for non-critical entries.
- Product meta at scale: HPOS does not fix product meta bloat. At 100k SKUs with variations, `wp_postmeta` still runs into the millions of rows. Adding `ALTER TABLE wp_postmeta ADD INDEX idx_meta_value(meta_value(191))` reduces unindexed product search from 2 seconds to 20ms. For large-catalog search, Elasticsearch (ElasticPress) or Algolia offloads search from MySQL entirely.

**Data to use:**
- HPOS: 5x faster order creation, 40x faster backend filtering, 80–90% faster admin for 50k+ order stores — source: [WooCommerce Dev Blog, 2023](https://developer.woocommerce.com/2023/03/17/performance-benchmarking-for-woocommerce-hpos/)
- HPOS checkout speed: up to 35% improvement — source: [ThriveWP, 2025](https://thrivewp.com/woocommerce-hpos-2025-guide/)
- Product search with meta_value index: 2s → 20ms — source: [Marcin Dudek, 2026](https://marcindudek.dev/blog/30-wordpress-woocommerce-performance-tips-2026/)
- Autoload alert threshold: >1MB — source: [Marcin Dudek, 2026](https://marcindudek.dev/blog/30-wordpress-woocommerce-performance-tips-2026/)
- ElasticPress Instant Results: 6x faster than native WordPress search — source: [ElasticPress, 2025](https://www.elasticpress.io/features/)
- WooCommerce 9.8 admin improvements: slowest admin requests 51.9% faster, JS bundle 221KB → 60.2KB — source: [WooCommerce Dev Blog, Oct 2025](https://developer.woocommerce.com/2025/10/01/improving-woocommerce-performance-at-scale/)
- WooCommerce 10.x: critical page-load times reduced up to 95% — source: [WooCommerce Dev Blog, Oct 2025](https://developer.woocommerce.com/2025/10/01/improving-woocommerce-performance-at-scale/)

**Creator note:** Mention that stores on WooCommerce 6.x or 7.x that have avoided upgrades for compatibility reasons are missing compounding free performance gains. Staging-validate, then upgrade — the risk of not upgrading is not free.

**Section image concept:** Split-screen or side-by-side dashboard showing slow admin order list vs. fast order list — or a WooCommerce database schema visualization. Keep it photorealistic/business-context, not abstract.

---

### Section 6: ERP sync — stop blaming WooCommerce for an integration architecture problem

**Key point:** Real-time ERP sync executed via WordPress hooks fires during page load or checkout, adding direct per-request latency — the fix is not a faster server, it's moving to batch/cron sync.

**What to cover:**
- The misdiagnosis: teams see slowness after ERP sync events (inventory update, price sync, order push) and blame WooCommerce. The real culprit is the integration architecture — plugin-based ERP connectors (for SAP Business One, NetSuite, Microsoft Dynamics, Epicor P21) that execute synchronously on WordPress hooks during the customer request.
- The failure modes: one-way sync breaks after a WooCommerce update; SKU mismatches create failed orders; real-time pricing logic collapses and B2B customers see wrong prices; large batch sync operations during business hours cause 503 errors.
- The fix: switch from real-time/hook-based sync to scheduled batch sync (every 5–15 minutes via system cron, not WP-Cron). This removes per-request latency from customer-facing pages entirely. For teams not ready to rebuild the integration, this single architectural change is typically achievable in days.
- The right architecture: webhook-driven or batch sync with custom middleware handling throttling, queuing, and error recovery. Not plugins executing on-request.
- WP-Cron caveat: WP-Cron is unreliable under high traffic (it runs on page load; if no pages load, it doesn't run). For B2B stores, replace with system cron calling `wp cron event run --due-now` on a 5-minute schedule.

**Data to use:**
- Source: [Seota ERP Integration Guide, 2025](https://seota.com/erp-integration-with-wordpress-and-woocommerce/)

**Creator note:** This section should validate the reader's frustration — they've been told it's a WooCommerce problem. It isn't. That reframe earns trust. Keep it diagnostic and specific; don't sell Virtina's integration services here.

---

### Section 7: When to fix in place vs. when to replatform

**Key point:** The genuine signal to replatform is a capability gap — not speed. If HPOS isn't enabled, Redis isn't configured, and the server is on shared hosting, the store hasn't been given a fair shot.

**What to cover (decision criteria):**

Fix in place when:
- HPOS has not been enabled (highest-impact free fix available)
- Server is on shared hosting with default PHP-FPM and InnoDB config
- Redis object caching is not implemented
- B2B plugins have known configuration fixes (B2BKing visibility cache, WholesaleX filter chain) that have not been applied
- ERP sync is running real-time on hooks
- WooCommerce version is below 9.x (free performance gains from upgrade)

Consider replatforming when:
- Business requires multi-company account hierarchies with sub-account permissions and approval workflows that WooCommerce cannot deliver without heavy custom development
- Native RFQ/quote management, purchase order as payment method, or customer-specific price lists are core to the buyer workflow and the plugin stack to replicate them is unstable
- ERP-grade audit trails and procurement workflow compliance are competitive requirements — not nice-to-haves
- The store has been fully optimized (HPOS enabled, Redis configured, correct hosting, up-to-date WooCommerce) and still cannot meet TTFB and checkout targets

**What the competitors offer that WooCommerce does not natively:** Shopify Plus B2B and BigCommerce B2B Edition have company profiles, purchase approval workflows, native RFQ, and purchase order as payment in the platform kernel — no plugin conflicts, no per-update breakage risk. If the business is differentiating on procurement workflow complexity rather than catalog and pricing, those platforms close the gap faster. Be honest about this — the credibility of the contrarian thesis depends on acknowledging where WooCommerce genuinely falls short.

**Format:** Two clear lists (fix in place / replatform signals). Keep each list to 4–6 bullets. No hedging.

**Creator note:** This is not a comparison of platforms — do not turn it into a BigCommerce vs. Shopify vs. WooCommerce article. The frame is: "here is the honest signal that the performance problem is actually a capability problem." Land the thesis: if the store hasn't been properly configured, replatforming moves the problem, it doesn't solve it.

---

### People Also Ask (3–4 Q&As)

Short answers — 2–4 sentences each. Optimized for SERP featured snippets.

Suggested questions:
1. How do I know if my WooCommerce store is slow because of plugins or because of hosting?
2. Does WooCommerce HPOS really improve performance, and is it safe to enable on a live store?
3. What is the biggest performance mistake B2B WooCommerce stores make?
4. When should a B2B manufacturer replatform from WooCommerce to Shopify Plus or BigCommerce?

---

### Conclusion (short, action-oriented)

One paragraph. Restate the thesis in different words. End with a forward-pointing action: run the 60-second audit, identify the bottleneck, apply the highest-revenue fix first. Do not use "in conclusion" — banned phrase. Do not summarize — the reader just read the article. CTA: natural, one line, pointing to Virtina's WooCommerce performance services. Something like: "If you want a second set of eyes on the diagnosis, our team works with B2B operators on exactly this — [contact us] to talk through what you're seeing."

---

### FAQ (6–8 Q&As)

Longer, conversational Q&As for bottom-of-page SEO and reader trust. 4–8 sentences per answer.

Suggested questions:
1. What is HPOS in WooCommerce and why does it matter for B2B stores?
2. Why does my WooCommerce store load fast for guests but slow for logged-in buyers?
3. Can WooCommerce handle 100,000+ SKUs?
4. What's the difference between page caching and object caching for WooCommerce?
5. How do I know if my ERP integration is causing WooCommerce slowness?
6. What are the minimum hosting requirements for a B2B WooCommerce store?
7. Is it risky to upgrade WooCommerce when I have custom plugins and B2B extensions?
8. What does Virtina look at first when diagnosing a slow WooCommerce B2B store?

**Creator note on question 8:** This is the natural place to bring in Virtina's credentials — 1,000+ clients, B2B manufacturing experience, WooCommerce Expert certification. Keep it diagnostic ("we look at TTFB, Query Monitor output, HPOS status, and hosting config before touching anything else") rather than promotional. The answer should feel like a senior practitioner describing their intake process.

---

## Must include

- HPOS benchmarks: 5x order creation, 40x backend filtering, 80–90% admin improvement for 50k+ order stores — source: WooCommerce Dev Blog
- InnoDB buffer pool default problem (128MB vs. 500MB+ typical WooCommerce DB) with the disk read penalty (200ms vs. 2ms)
- The B2B caching architecture problem — authenticated users bypass full-page cache — as a named, explained concept (not assumed knowledge)
- WooCommerce version update performance data: 9.8 admin improvements (51.9% faster slowest requests, 73% JS bundle reduction), 10.x up to 95% critical page-load reduction
- The ERP sync reframe: not a WooCommerce problem, an integration architecture problem
- Fix-vs-replatform decision criteria as two clean lists
- Virtina credential mention: natural, once, in FAQ Q8 (1,000+ clients, B2B manufacturing expertise, WooCommerce Expert certified, result: 22.5% revenue growth in 9 months for MM-Source)

## Must NOT include

- Generic WooCommerce speed advice written for B2C (image compression tips, CDN setup guides, lazy loading — unless framed specifically in B2B context)
- Explanations of what WooCommerce is, what an ERP is, what TTFB is, what Core Web Vitals are
- Named competitor agencies (see brand.md: Absolute Web, Coalition Technologies, Blue Stout, etc.)
- Promises not backed by numbers or case studies
- "In conclusion," "to summarize," "it's important to note," "leverage," "navigate," "ecosystem," "landscape," "realm," "delve," "revolutionary," "game-changing," "cutting-edge," "transform your..."
- Exclamation marks, semicolons
- Shopify and BigCommerce framed as clearly superior to WooCommerce — they are honest alternatives for specific capability gaps, not a general recommendation
- The WholesaleX 30-second admin load stat stated as a verified exact number — the research flags it as unverified; use it as a qualitative reference ("reports of 30+ second admin load times before the fix was applied")
- The 70% checkout abandonment stat framed as B2B-specific — it is a general ecommerce stat; qualify it as such

## Headline direction

Declarative. No clickbait. No question marks in the headline. Should signal the self-audit framework and the contrarian thesis together.

Three working options:

1. **Your WooCommerce B2B store isn't slow — it's misconfigured: a 60-second diagnostic and fix guide**
2. **How to diagnose and fix a slow WooCommerce B2B store (without replatforming)**
3. **The B2B WooCommerce performance diagnostic: find your bottleneck in 60 seconds and apply the highest-impact fix first**

Option 1 is the strongest — it leads with the contrarian reframe and names the format. Creator should iterate from it.

## Open questions for the creator

- Virtina may have internal client data on B2B WooCommerce performance improvements (before/after TTFB, checkout conversion lift, order processing time). If so, one specific client result (anonymous is fine) would replace the platform-level benchmarks as the most compelling evidence in the article. Ask the account team before drafting.
- The self-audit decision tree in Section 1 can be formatted as a structured list or as a simple table — creator's call based on what reads most cleanly in the Virtina CMS. Both are valid; table may scan better.
- The creator should decide where to place the section image for Section 5 (database bottlenecks) — it's the densest technical section and may benefit from breaking the text earlier with an image rather than waiting for the standard 3–4 section interval.

## Gaps and risks

- **No named B2B client case study with before/after numbers.** All benchmarks are from plugin vendors and WooCommerce core. The creator must frame these as platform benchmarks ("WooCommerce's own benchmarks show...") not as client results. If Virtina can supply even one internal result, use it — it would significantly strengthen the piece.
- **HPOS migration safety caveat must be included.** The brief instructs the creator to note that HPOS requires staging validation — older payment gateways and warehouse integrations can break. Do not omit this. Omitting it would be irresponsible advice.
- **Redis configuration risk must be acknowledged.** B2BKing's own docs flag that Redis "requires thorough testing and can cause pricing errors if misconfigured." The article must not recommend Redis unconditionally — it must name the `maxmemory-policy volatile-lru` requirement and the per-user data scoping requirement. A single sentence is enough; don't make it a disclaimer block.
- **WooCommerce 100k-product ceiling conflict.** Two reputable sources disagree (Pressable: "no ceiling"; White Label Coders: "degrades past 10k–20k on standard hosting"). The brief resolves this correctly: both are true in different infrastructure contexts. The creator must not flatten this to a simple "WooCommerce can handle 100k SKUs" claim without the infrastructure qualifier.
- **Tone risk: don't let the contrarian thesis slide into dismissing replatforming.** The "fix in place" argument is strong and defensible — but the honest treatment is that capability gaps (approval workflows, native RFQ, ERP-grade audit trails) are genuine reasons to replatform. The article's credibility depends on that honesty. A reader who replatforms after reading this because their use case genuinely warrants it should feel the article served them well.
