---
title: Uniqueness audit - B2B marketplaces ranked list
client: virtina
date: 2026-11-02
topic: ranked list of existing B2B and wholesale marketplaces
audience: B2B sellers and buyers (manufacturers, distributors, wholesalers)
stage: research
slug: uniqueness-audit-b2b-marketplaces-2026-11-02
---

## Method and limits

- Corpus: `scratchpad/corpus.json` (all live posts and pages) grepped for "marketplace" and "wholesale" in slugs and titles.
- Live sweep: `/wp-json/wp/v2/search?search=b2b marketplace` and `?search=wholesale marketplace` (50 results each, fetched via WebFetch, no 429).
- Pages sweep: pages list in corpus.json contains NO page with marketplace or wholesale in slug or title. The search endpoint returned no page-type result about marketplaces. Pre-check 0: PASS.
- Inventory file `published-posts-inventory.md` last_updated 2026-09-09 (over 7 days stale). I did not rebuild it. corpus.json is the fresher source and was used instead. Only the first ~500 of its 1,386 lines were read. The rest was substituted by the corpus grep.
- Neighbour posts were fetched and their headings read (below). I read them through the fetch summariser, not raw HTML. The creator must still run the 8-gram diff against local files.

## Neighbour posts (headings fetched 2026-11-02)

| ID | Slug | What it actually covers | Names real marketplaces? |
|---|---|---|---|
| 36161 | top-multi-vendor-marketplaces-for-ecommerce-platforms | 20 SOFTWARE products to BUILD a marketplace (Shipturtle, Dokan, Sharetribe, Mirakl, etc.). Reader: entrepreneur launching a marketplace. | No (no Alibaba, Faire, Amazon Business) |
| 20975 | the-role-of-b2b-marketplaces-in-shaping-todays-successful-businesses | 2020 explainer. Why sell through marketplaces (6 benefits), 8 questions before BUILDING one, 5 features, 10 challenges, how to create one. | Amazon Business only, in passing |
| 26936 | b2b-ecommerce-marketplace-on-woocommerce | How to customise WooCommerce as a B2B marketplace. WCFM plugin named. | No |
| 41015 | marketplace-trap-amazon-ebay-only-sales-risk | Contrarian thesis: selling only on Amazon/eBay is a risk for manufacturers. Mentions Amazon fees, eBay metrics, Walmart once. | Amazon, eBay, Walmart (risk framing, no directory) |
| 36865 | marketplace-multi-vendor-module-for-magento | Magento 2 multi-vendor module. | No |
| 37791 | best-ecommerce-websites | B2C ranked list. Entries: Amazon, Temu, AliExpress, Walmart, eBay, Etsy, Rakuten, Shein, Coupang, Ozon; plus Target, Wayfair, Chewy, Sephora, StockX, ThredUp, Zappos, Newegg, Best Buy. | Overlap risk: Amazon, AliExpress (not in the B2B entry set) |
| 43753 | quick-order-form (draft) | B2B quick order forms. Different topic. | n/a |
| 10690 | multi-vendor-plugins-woocommerce | Plugins to build a multi-vendor store. | No |
| 19808 | mobile-marketplace-and-millennials-... | 2020 trend piece. | No |

Finding: no existing Virtina page is a directory of existing, named B2B marketplaces that a business can buy from or sell on. All marketplace content is either build-your-own (software) or a single risk argument.

## Candidates evaluated

### Candidate A (SELECTED): B2B marketplaces ranked by US search traffic, with an own-store decision section

Proposed title: **B2B marketplaces ranked: 9 platforms by US search traffic**
Proposed slug: **wholesale-marketplaces-ranked-by-traffic**
Primary keyword: b2b marketplaces. Variants: best b2b wholesale marketplaces, best b2b marketplaces, b2b wholesale marketplaces list.

| Check | Result | Evidence |
|---|---|---|
| Pre-check 0 (pages) | PASS | No page slug/title with marketplace or wholesale. Search endpoint: no page-type hit. |
| CHECK 1 title overlap | PASS | Closest: 20975 "Role of B2B Marketplaces in Shaping..." shares "B2B marketplaces" (2 consecutive content words, then "in Shaping" vs "ranked"). 36161 shares "marketplaces" only. 26936 shares "B2B" then "eCommerce Marketplace" (the new title has no "B2B ecommerce"). 37791 "Top 10 online shopping sites" shares nothing. Max run = 2. |
| CHECK 2 slug overlap | PASS | `wholesale-marketplaces-ranked-by-traffic` is not a substring of any slug. Max overlap with any single slug is 1 word: `marketplaces` (36161, 20975), `traffic` (34096 scaling-woocommerce-...-high-traffic-volume). `wholesale` does not match `wholesalers` (9978). Does not start with `best-ecommerce`. |
| CHECK 3 primary keyword | PASS WITH FLAG | No slug is exactly the keyword. BUT 20975's slug encodes "b2b-marketplaces" and its Yoast focus keyword is probably "b2b marketplace". I did not read 20975's Yoast fields. Different intent (explainer on building, 2020) vs this list. **Orchestrator: check 20975's focus keyword via `context=edit` before push.** Slug deliberately avoids "b2b" + "marketplace(s)" because the pair collides on 20975 (`b2b`+`marketplaces`) and 26936 (`b2b`+`marketplace`). |
| CHECK 4 angle | PASS | Thesis: a ranked directory of EXISTING marketplaces, ordered by a disclosed metric, plus an own-store decision. 36161 = software to build one. 20975 = why and how to build/sell in one (2020). 26936 = Woo customisation. 41015 = risk of marketplace-only selling, no directory, no entries. 37791 = B2C. No overlap in coverage. Closest conceptual neighbour is 41015 (own store vs marketplace). Keep the own-store section to one decision section that links 41015 rather than re-arguing fees/algorithm risk. |
| CHECK 5 cluster saturation | FLAG, ruling needed | Posts a reader on "marketplaces" would already find: 36161, 20975, 26936, 36865, 41015, 10690 = 6 (plus 19808 = 7). Strict letter of Check 5 (5 or more) = FAIL. Section 4c says saturation does not block when the sub-niche is clearly unique. The sub-niche (directory of existing, named B2B marketplaces) has zero existing coverage, so I recommend proceeding under 4c. **This needs the orchestrator/user to accept the 4c exception explicitly.** |

Cluster is flagged SATURATED (6+). Unique sub-niche: directory-and-ranking of existing B2B marketplaces for buyers and sellers, versus the existing build-your-own and risk posts.

### Candidate B (REJECTED): How to build a B2B marketplace
- Fails Check 4 and Check 5. Covered by 20975 (how to create), 26936 (WooCommerce), 36161 (software list), 36865 (Magento module).

### Candidate C (REJECTED): Best B2B ecommerce platforms
- Fails Check 5 and likely Check 4. Platform-comparison cluster is far over 5 posts (29137, 36721, 37776, 27047, 43728, and more).

### Candidate D (REJECTED): Pros and cons of selling on Amazon Business
- Fails Check 4. 41015 already argues marketplace dependency for the same reader. Single-marketplace piece would also be thin.

## Duplicate-phrasing guard against 37791

Because the new post mirrors 37791's structure, the likeliest 8-gram collisions are boilerplate: "how this ranking is measured", the "what this means for your store" block, the self-check wording, the PAA/FAQ labels. Rules for the creator:
- Do not reuse 37791 section headings verbatim. Use different wording for the method, exclusions, second-metric and decision sections.
- Strip `<style>` blocks and inline styles before the 8-gram diff (see inventory note on post 42465) or every structural clone looks like a false positive.
- Do not copy 37791's entry paragraph openings.

## Final status

Candidate A: Pre-check 0 PASS, Check 1 PASS, Check 2 PASS, Check 3 PASS WITH FLAG (verify 20975 focus keyword), Check 4 PASS, Check 5 FLAG (6 posts; 4c exception, needs ruling).
