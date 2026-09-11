---
title: Uniqueness audit — raise price or repackage
client: impelhub
date: 2026-09-10
topic: B2B SaaS price increase vs repackaging decision
audience: founders, CEOs, growth leaders
stage: research
slug: raise-price-or-repackage-saas-offer
---

# Uniqueness audit — 2026-09-10

## Pre-check: inventory freshness

`published-posts-inventory.md` `last_updated: 2026-06-11`. That is 91 days old, so stale.
Refreshed live: `GET /wp-json/wp/v2/posts?per_page=100&status=publish` returned **HTTP 200, 50 published posts**.
Newest published post is **12444, 2026-04-28**. No posts have been published since the inventory was written, so the inventory's post list is still accurate in substance. The `last_updated` stamp was refreshed to 2026-09-10.

The inventory listed 51 rows because it includes one unpublished row (`reduce-churn-b2b-saas-early-stage`, ID "TBD"). Live published count is 50.

## Scope of the sweep (posts AND pages, matched on real content)

- 50 published posts, **full `content.rendered` downloaded** (not just titles)
- 82 published pages, **full `content.rendered` downloaded** (not just titles)
- `GET /wp-json/wp/v2/search?search=pricing|packaging|price+increase` run separately, which also surfaced `elementor_library` and `awsm_job_openings` post types

Matching was done on **slug tokens and fetched body text**, never on the stored WP `title` field alone. This was deliberate: a page can store a title unrelated to its content and stay invisible to a title grep.

## Candidates evaluated

| # | Candidate | Verdict |
|---|---|---|
| 1 | Revenue-based financing vs VC for SMB founders | REJECTED. Off-positioning. ImpelHub is a growth decision filter, not a capital-structure advisor. No product module maps to it. |
| 2 | OKRs for SMBs | REJECTED on CHECK 4. Angle collides with 11955 ("Why teams need a system, not more strategy") and 12238 ("Growth metrics that matter by stage"). Same thesis: goals without a system fail. |
| 3 | Product-led vs sales-led growth | REJECTED on CHECK 5 borderline. Sits inside the GTM cluster, which is at 11 posts and flagged SATURATED. Sub-niche not distinct enough from 12444 GTM vs growth strategy. |
| 4 | Hiring your first marketing hire | REJECTED on CHECK 4. Structurally the same decision-readiness argument as 12330 ("When to hire your first sales rep"). Would read as a find-and-replace of an existing post. |
| 5 | **Raise your price or repackage the offer** | **SELECTED.** See below. |

## Selected topic

**Title:** Should you raise your price or repackage the offer? A B2B SaaS decision filter
**Slug:** `raise-price-or-repackage-saas-offer`
**Primary keyword:** raise price or repackage SaaS
**Cluster:** B2B SaaS Founder Decisions (3 posts, open)
**Thesis:** Founders reach for a price increase because it is the fastest lever to pull. The revenue leak is usually in packaging, specifically in a value metric that does not scale with the value the customer receives. Diagnose which of the two is broken before you touch either.

### CHECK 1 — Title word overlap: **PASS**
Programmatic 3-consecutive-content-word comparison against **132 titles** (50 posts + 82 pages), stop words removed. Zero collisions.

### CHECK 2 — Slug overlap: **PASS**
Programmatic comparison against **132 slugs**. Result: only single-word overlaps, both on `saas`:
- `product-market-fit-signals-b2b-saas` → 1 word
- `when-to-hire-first-sales-rep-b2b-saas` → 1 word

No substring match. No 2+ word overlap.

Note: an earlier candidate slug, `pricing-or-packaging-saas-founder-decision`, was **discarded** because the existing page slug `pricing` (ID 10637, ImpelHub's own product pricing page) sat inside it. Rather than argue the direction of the substring rule, the slug was rewritten to remove the collision entirely.

### CHECK 3 — Primary keyword uniqueness: **PASS**
No existing post or page has pricing-vs-packaging as its focus keyword. `/pricing/` (page 10637) is ImpelHub's own transactional plan page, a different URL path and a different search intent. No cannibalisation.

### CHECK 4 — Angle/thesis uniqueness: **PASS**
Full-text scan of all 50 posts for `packaging|repackag|value metric|pricing tier|price increase|good-better-best` returned 8 posts with any hit, max 6 hits in a 6,527-word post. Every hit was inspected in context. All are incidental, listing "pricing and packaging" as one item in a list of GTM levers:
- 12444 — one table row, one clause
- 11700 — manufacturing offer structure, plus literal packaging OEMs
- 11287 — lifestyle segmentation activating into pricing/packaging
- others: single passing mentions

**No existing ImpelHub post treats the price-vs-packaging choice as its subject.** Zero angle overlap.

### CHECK 5 — Cluster saturation: **PASS**
B2B SaaS Founder Decisions = 3 published posts (12433, 12330, plus draft 	churn). Threshold is 5. Not saturated, and no exception clause needed.

### Sister-brand check
Virtina content was not consulted, referenced, or reused. Virtina is an eCommerce implementation partner. This topic has no Virtina analogue and no Virtina framing was carried over.

## Format selection

Last 10 published posts, format inferred from live structure:

| Post | Inferred format |
|---|---|
| 12444 | E (contrarian) |
| 12433 | C (listicle with opinions) |
| 12356 | A (standard explanatory) |
| 12330 | D (decision playbook) |
| 12290 | E (contrarian) |
| 12242 | E (contrarian) |
| 12238 | A |
| 12189 | A |
| 12173 | A |
| 12133 | A |

Format A appears 5 times and Format E 3 times in the last 10. Both are barred by the "no format used in 3+ of the last 10" rule.
**Format B (conversational Q&A) has been used zero times in the last 10.** It is also the best fit: this is a topic where founders arrive with a specific stack of sub-questions. **Format B selected.**

## Semantic term list (10-15, to appear naturally)

value metric, packaging, price increase, willingness to pay, ACV, expansion revenue, net revenue retention, gross retention, tier, grandfathering, discount rate, ICP, churn, upgrade path, seat-based pricing, usage-based pricing
