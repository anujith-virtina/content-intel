---
title: Uniqueness audit — outdated store hurts conversions
client: virtina
date: 2026-10-01
stage: research
slug: outdated-store-hurts-conversions
corpus: 314 published posts + 257 published pages, fetched live
---

# Uniqueness audit

## Headline finding: the requested article, written as specified, would cannibalise the money page

The brief asked for a symptom catalogue: slow speed, poor mobile, hard navigation, complicated checkout,
weak product presentation, poor discovery, weak CTAs, missing trust signals, dated payment options,
browser issues, weak site search, buying-journey friction. **The target page already owns that exact
section, in the same frame.**

Page **42707** `/ecommerce-website-redesign/`, H2 **"Is Your Store Design Costing You Sales?"**, verbatim:

> "A dated store rarely fails all at once. It leaks revenue slowly: mobile shoppers bounce, product pages
> feel slow, buyers cannot find what they need, and checkout loses orders at the last step."

Its six H3s are: Mobile visitors bounce / Pages load slowly / Customers can't find products / Checkout
drops shoppers / Your brand looks older than your business / Every change needs a developer. Each carries
a one-line causal explanation. That covers roughly nine of the sixteen requested symptoms, including the
"still works but leaks revenue" framing the brief asked for as the article's core idea.

A blog post repeating that list would compete with the page it exists to support. That is the worst case
for a supporting article.

## Cluster saturation: FAIL as originally scoped

MUST-FOLLOW-RULES CHECK 5 rejects a topic when 5 or more posts already cover the same general subject.
The conversion / UX cluster holds far more than that:

| Object | Owns |
|---|---|
| page 42707 `/ecommerce-website-redesign/` | the dated-store symptom list and the "leaks revenue" frame |
| page 35530 `/tips-for-ecommerce-conversion-rate-optimization/` (3,451w) | design/UX, mobile, social proof, CTAs, plus ~30 checkout, trust and filter tips |
| page 13307 `/ecommerce-conversion-rate-optimization/` (2,435w) | the CRO service framing |
| post 38127 `/cro-audit-guide-for-ecommerce-websites/` (3,481w) | friction points, UX, mobile, page load, Core Web Vitals |
| post 19040 `/cro-hd-to-boost-ecommerce-revenue/` (2,681w) | value proposition, trust, friction, urgency, relevance, clarity |
| post 33988 `/bigcommerce-custom-themes-conversions/` | navigation, product pages, speed, trust elements, checkout, CTA placement |
| post 34086 `/woocommerce-mobile-optimization-guide/` | mobile UX, mobile checkout, cart abandonment |
| post 23056 `/page-speed-optimization-for-improved-ranking-and-conversion-rate/` | speed and conversion |
| post 41808 `/ecommerce-site-search-optimization/` | site search as a revenue lever |
| post 10902 `/reduce-shopping-cart-abandonment/` | checkout abandonment |
| posts 11200, 11012 | older UX and CRO primers |

## What IS open

Three targeted probes across all 571 objects returned **zero** title or slug matches:

- "outdated / legacy / dated site" as a subject: **0**
- "optimise or rebuild" decision: **0**
- "technical debt / plugin bloat / theme hack" as a subject: **0**

So the **keyword is free, the symptom content is not**. The open lane is the decision the brief itself
asks for in its fourth section: when does an outdated store stop being an optimisation problem and become
a rebuild? Nothing in the corpus answers that.

## De-duplication decision

Keep the requested title, primary keyword and audience. Move the centre of gravity:

- **Spine becomes the threshold**: symptoms you can fix in place versus symptoms that mean the underlying
  build is the constraint. This is new search value and it feeds the redesign page's commercial intent.
- **Symptoms become diagnostic inputs, not a catalogue.** Each one is named briefly and **links to the
  post that already owns it**, which strengthens the cluster instead of competing with it.
- **Do not restate** the money page's six H3s, its wording, or its "leaks revenue slowly" sentence.
- **Technical debt gets real treatment** (plugin bloat, theme hacks, every change needing a developer as a
  compounding cost), since the corpus has nothing on it.

## The five checks, as rescoped

| Check | Verdict | Evidence |
|---|---|---|
| 1 title overlap | **PASS** | no 3 consecutive content words shared with any of 571 objects |
| 2 slug overlap | **PASS** | `outdated-store-hurts-conversions`. Note `outdated-ecommerce-website` FAILED: "ecommerce" + "website" collide with 9 slugs including the money page |
| 3 primary keyword | **PASS** | "outdated ecommerce website" is the focus of no post or page |
| 4 angle/thesis | **PASS only as rescoped** | FAILS as originally briefed, see the headline finding. Passes once the spine is the optimise-versus-rebuild threshold |
| 5 cluster saturation | **PASS only as rescoped** | FAILS as a symptom catalogue. Passes as a decision article, a sub-niche with zero existing coverage |

## Fence against the sibling post

Post **43029** `redesign-without-losing-rankings` (2026-09-30) owns redirects, URL changes, title tags and
H1s, internal linking, indexation and Core Web Vitals **after** a redesign. This article must not touch
redirect mechanics, indexation or ranking recovery. Different intent: revenue and conversions **before**
the decision, not search rankings after it. The two link to each other once.
