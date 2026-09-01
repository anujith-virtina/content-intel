---
title: Uniqueness audit — "AI Search Is Changing B2B Ecommerce: Is Your WooCommerce Catalog Ready?"
client: virtina
date: 2026-08-31
stage: research
requested_by: user
verdict: REJECTED as proposed; reframed candidate PASSES all 5 checks
---

# Uniqueness audit, 2026-08-31

Run per MUST-FOLLOW-RULES.md section 1. A topic is REJECTED if it fails **any** single check.

## Inventory freshness

`published-posts-inventory.md` `last_updated` was 2026-08-21, which is 10 days stale (threshold: 7 days).
A live REST refresh was attempted against `https://virtina.com/wp-json/wp/v2/posts` and **returned HTTP 429
on every attempt including retries**, both for the listing and for `search=` queries. The refresh could not
be completed.

Mitigation: the two candidate-blocking posts were verified directly against the live site by URL instead,
which does not hit the REST API:

| URL | Live status | Live H1 |
|---|---|---|
| `/ecommerce-store-agent-ready/` | **200, published** | "The customer was a robot: how to make your store readable to AI shopping agents" |
| `/woocommerce-b2b-pricing-and-access-setup/` | 200, published | "WooCommerce B2B Configuration: A Step-by-Step Guide to Pricing Rules, Customer Groups, and Catalog Access" |
| `/ecommerce-ai-search-implementation-checklist/` | 404 (post 42391 still draft) | n/a |

Caveat carried forward: because the REST refresh failed, posts published between 2026-08-21 and 2026-08-31
are not indexed. Re-run the refresh before push.

---

## CANDIDATE A (as requested): "AI Search Is Changing B2B Ecommerce: Is Your WooCommerce Catalog Ready?"

Proposed slug: `ai-search-b2b-woocommerce-catalog`
Proposed primary keyword: AI search B2B ecommerce / WooCommerce catalog AI search

### CHECK 1 — Title word overlap (3+ consecutive content words) — PASS
No existing title shares 3 consecutive content words. The nearest, post 42391 ("...for AIO, GEO, and AEO:
A Practical Implementation Guide"), shares no consecutive run. Passes, but narrowly and misleadingly:
title distance here does not reflect topic distance.

### CHECK 2 — Slug overlap — **FAIL**
Rule: the proposed slug must not contain 2 or more words from any existing slug.
`ai-search-b2b-woocommerce-catalog` shares **`ai` + `search`** with the existing slug
`ecommerce-ai-search-implementation-checklist` (post 42391). Two-word overlap. **REJECT.**
Additionally, any slug carrying both `woocommerce` and `b2b` collides with four existing slugs
(`woocommerce-b2b-pricing-and-access-setup`, `woocommerce-b2b-customer-portal`,
`woocommerce-b2b-performance-fix`, `woocommerce-b2b-net-payment-terms`).

### CHECK 3 — Primary keyword uniqueness — **FAIL**
"ecommerce AI search" is already encoded in the slug of post 42391, which is the focus keyword of that post.
The proposed primary keyword is a direct variant of a claimed keyword. **REJECT.**

### CHECK 4 — Angle / thesis uniqueness — **FAIL (the decisive one)**
The live post `/ecommerce-store-agent-ready/` already argues this exact thesis. Its body H2s are:

- What does "agent-ready" mean for an ecommerce store?
- What is the difference between GEO and being agent-ready?
- How do AI shopping agents find and evaluate products?
- Why isn't my store showing up in AI shopping results?
- What makes a product page invisible to AI shopping agents?
- Do I need structured data for AI shopping agents?
- How do I optimize my product data for AI agents?
- What is the difference between training crawlers and retrieval bots?
- How do I make my ecommerce store agent-ready?

"AI search is changing ecommerce, here is how to get your catalog ready" **is** that post. A second post
making the same argument would compete with a live, indexed page. **REJECT.**

### CHECK 5 — Topic cluster saturation — PASS
AI / AIO / GEO / AEO cluster currently holds 3 posts (42391 draft, 42393 partial, agent-ready live).
Under the 5-post ceiling.

### VERDICT: **REJECTED.** Fails checks 2, 3, and 4.

---

## CANDIDATE B (reframed, recommended): the gated B2B catalog problem

Working title: **"Your B2B catalog is invisible to AI search, and you built it that way on purpose"**
Proposed slug: `gated-catalog-ai-visibility`
Primary keyword: gated B2B catalog AI visibility

### The gap this fills
Every existing Virtina AI post assumes a **public** catalog. `/ecommerce-store-agent-ready/` is written for a
store whose product pages are crawlable and whose prices are on the page; its whole remedy is schema, product
data quality, and retrieval-bot access. That remedy does not apply to a B2B store, because a B2B store
deliberately does the opposite:

- the catalog is behind a login, so there is nothing for a retrieval bot to fetch at all
- prices are per customer group, so there is no single price to put in `Product` schema
- "Request a quote" replaces Add to Cart, so there is no offer for an agent to evaluate
- authoritative product data sits in the ERP, not the storefront
- contract and tiered pricing cannot be expressed in schema.org `Offer` in the first place

None of that is addressed anywhere in the corpus. The thesis is also genuinely contrarian and sits *against*
the agent-ready post rather than repeating it: for B2B, AI visibility is a **commercial decision about what to
expose**, not a markup exercise. That makes it a companion piece, not a competitor.

### CHECK 1 — Title word overlap — PASS
No 3-consecutive-content-word run against any existing title. Nearest neighbours share only "catalog" and
"AI" as isolated words.

### CHECK 2 — Slug overlap — PASS
`gated-catalog-ai-visibility` = {gated, catalog, ai, visibility}.
- vs `ecommerce-ai-search-implementation-checklist`: shares `ai` only (1 word). OK.
- vs `ecommerce-store-agent-ready`: 0 shared. OK.
- vs `woocommerce-punchout-catalog-integration`: shares `catalog` only (1 word). OK.
- vs all `woocommerce-b2b-*` slugs: 0 shared (slug deliberately omits both `woocommerce` and `b2b`, which is
  the same workaround used for post 42441's slug). OK.

### CHECK 3 — Primary keyword uniqueness — PASS
"gated B2B catalog AI visibility" is not the focus keyword of any existing post and is not encoded in any slug.

### CHECK 4 — Angle / thesis uniqueness — PASS
Distinct from `/ecommerce-store-agent-ready/` (assumes a public catalog; this post's premise is that a B2B
catalog is not public and cannot simply be opened). Distinct from 42391 (implementation checklist for
citability; this is a decision framework about exposure). Distinct from 42393 (how to configure gated pricing;
this is what that gating costs you in AI visibility and what to do about it). The post should link to all
three and explicitly concede each one's territory in a sentence.

### CHECK 5 — Topic cluster saturation — PASS
Adds a 4th post to a 3-post cluster. Under the ceiling, but note the cluster is now close to saturation:
one more AI-search post after this should be rejected under check 5 unless a genuinely new sub-niche appears.

### VERDICT: **PASSES all 5 checks.** Recommended.

---

## Candidates considered and dropped

- **"How to add AI search to your WooCommerce store"** — REJECT, check 5 risk plus it is a plugin roundup,
  which is not Virtina's positioning (they are a build/migration partner, not a plugin reviewer).
- **"WooCommerce vs Shopify for AI search visibility"** — REJECT, check 2 (`shopify-vs-woocommerce` exists)
  and check 4 (36721 owns neutral platform comparison).
- **"Schema markup for WooCommerce product pages"** — REJECT, check 4, fully covered by the agent-ready post's
  structured-data sections.

## Required before push

- [ ] Re-attempt the REST inventory refresh (429 today) and index anything published 2026-08-21 to 2026-08-31
- [ ] Post-draft: no sentence over 8 words appears verbatim in any existing Virtina post
- [ ] Confirm the three internal links resolve 200 on the live site
