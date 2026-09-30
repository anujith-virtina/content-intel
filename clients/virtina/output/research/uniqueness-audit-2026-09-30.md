---
title: Uniqueness audit — redesign without losing rankings
client: virtina
date: 2026-09-30
stage: research
slug: redesign-without-losing-rankings
corpus: 314 published posts + 257 published pages, fetched live 2026-09-30
---

# Uniqueness audit

Corpus pulled live from the REST API on 2026-09-30, not from the inventory file:
`GET /wp/v2/posts` (314) and `GET /wp/v2/pages` (257). Pre-check 0 satisfied: pages were swept as a
first-class part of the corpus, and matching was done on **slug and fetched heading text**, never on the
stored WP title alone.

## Candidate selected

| Field | Value |
|---|---|
| Working title | Why eCommerce Sites Lose Rankings After a Redesign (And How to Prevent It) |
| Slug | `redesign-without-losing-rankings` |
| Primary keyword | website redesign SEO |
| Supports | `https://virtina.com/ecommerce-website-redesign/` (page 42707) |

## The five checks

**CHECK 1 — title word overlap: PASS.**
Tested every 3-word consecutive content-word window of the proposed title against all 571 objects, stop
words removed. Zero matches. The nearest post, 40727, is titled "How To Redesign Your eCommerce Website
In 2026: The Ultimate Guide"; the shared words are non-consecutive.

**CHECK 2 — slug overlap: PASS.**
`redesign-without-losing-rankings` is not a substring of any existing slug, and no existing slug is a
substring of it. No existing slug shares 2 or more content words with it. Note the deliberate avoidance
of "ecommerce" and "website", which are so common across Virtina slugs that including both would have
tripped the 2-word rule against several objects, including `redesigning-your-ecommerce-website-5-steps`
and `ecommerce-website-migration-checklist`.

**CHECK 3 — primary keyword uniqueness: PASS.**
No post or page has "website redesign SEO" as its focus. Page 42707 owns the commercial term "ecommerce
website redesign"; this post deliberately takes the informational lane upstream of it rather than
competing for the same query.

**CHECK 4 — angle/thesis uniqueness: PASS, with evidence.**
The only redesign post is **40727** `/redesigning-your-ecommerce-website-5-steps/` (~3,503 words). Its
headings were fetched and read in full. It covers: what a redesign is, what AI-powered web design is, how
AI is changing design in 2026, what is new in 2026, benefits, core features, a five-step process,
best practices, cost factors, challenges, and why to partner with Virtina. **SEO appears exactly once, as
a People Also Ask H3, "Will a redesign hurt SEO?"** It does not own the mechanism.

The other near neighbour is **34921** `/ecommerce-website-migration-checklist/` (~6,221 words), which has
"SEO Considerations" and "SEO Testing" as H3s inside a migration checklist. That post is about a
**platform change**. This post is about a **redesign on the same platform**, where the failure modes are
different: template-driven metadata changes, nav simplification orphaning deep pages, structured data
dropped by a new theme, and Core Web Vitals regressions from heavier design. The distinction is kept
explicit in the brief, and 34921 is linked rather than repeated.

**CHECK 5 — cluster saturation: PASS.**
The redesign cluster contains **1** post (40727). The threshold is 5. For contrast, the migration cluster
holds 15 posts and was rejected as saturated, and speed/Core Web Vitals holds 4 posts plus 6 service
pages, so a pure speed angle was also rejected.

## Pre-check 0 — REST search sweep

`GET /wp/v2/search` for "website redesign seo", "redesign rankings", "lose rankings redesign" and
"redesign 301". Across all four queries the only closely related objects returned were page **42707**
(the money page this post supports) and post **40727** (analysed above). Page 40127
`/website-maintenance/` recurs in results but is a maintenance services page and owns no redesign or SEO
keyword.

## Candidates evaluated and rejected

| Candidate | Verdict | Reason |
|---|---|---|
| Redesign vs replatform decision guide | REJECT | Migration cluster holds 15 posts, saturated per CHECK 5 |
| Core Web Vitals for a redesign | REJECT | 4 posts plus 6 service pages already; 26024 and 23056 own the metric explanations |
| CRO and redesign | REJECT | 12 UX/CRO posts plus 6 CRO pages; 38127 owns the audit angle |
| Redesign cost and budgeting | REJECT | 40727 has a cost-factors H2; 12678 owns ecommerce website cost |
| **Ranking loss during a redesign** | **SELECT** | 1-post cluster, no post owns the mechanism, directly supports 42707 |

## Post-draft guard

Phrasing uniqueness (no 8+ word verbatim sequence against any existing Virtina post) is checked against
the fetched corpus after the draft is written, not assumed. Recorded in the publish log.
