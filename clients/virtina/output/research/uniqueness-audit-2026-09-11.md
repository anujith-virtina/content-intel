---
title: "Uniqueness audit — Square hemp and CBD cutoff post"
client: virtina
date: 2026-09-11
topic: Square closing hemp/CBD selling, Section 781 hemp redefinition, seller action plan
stage: research
slug: uniqueness-audit-2026-09-11
research_file: clients/virtina/output/research/square-cbd-hemp-ban-2026-09-11.md
competitor_file: clients/virtina/output/research/competitor-analysis-2026-09-11.md
supersedes: clients/virtina/output/research/uniqueness-audit-2026-08-21.md
---

# Uniqueness audit — Square hemp and CBD cutoff

## Scope of this audit

Two cases were evaluated, because a complete unpublished draft on this topic already exists in the repo
(`clients/virtina/output/drafts/square-cutoff-seller-action-plan-2026-08-21.md`, 3,480 words, Format D).

- **Case A — corrected August draft.** Fact-correct, simplify and trim the August 21 draft, then publish.
- **Case B — clean rewrite.** Discard and write fresh.

**Orchestrator decision, recorded: Case A.** Both cases are audited below because the checks differ
slightly (Case A inherits the August slug and title unless changed; Case B would not). Case A is the
binding result.

**Important corpus note:** the August 21 draft is **unpublished**. It is not part of the live Virtina
corpus and therefore cannot itself fail any of the 5 checks. It is a working asset, not a competitor.
Confirmed unpublished three ways: no `output/published/` artefact, no CMS payload JSON, no inventory
entry, and a live REST sweep on 2026-09-11 returns no post with any Square, hemp or CBD slug.

---

## PRE-CHECK 0 — pages and search sweep (MANDATORY)

Run 2026-09-11 against the live site. Matching was done on **slug and fetched H1**, never on the stored
WP `title` field, per the standing rule added after page 36749.

### Endpoints queried

- `GET /wp-json/wp/v2/search?search=hemp&per_page=40`
- `GET /wp-json/wp/v2/search?search=cbd&per_page=40`
- `GET /wp-json/wp/v2/search?search=square&per_page=40`
- `GET /wp-json/wp/v2/pages?slug[]=...` (6 slugs, canonical `link` read back)
- `GET /wp-json/wp/v2/posts?slug[]=...` (7 slugs, canonical `link` read back)

No 429 was encountered on any call. No 429 was recorded as either a pass or a fail.

### Everything the sweep surfaced on this topic

| ID | Type | Slug | Fetched H1 / real topic | Bearing on this post |
|---|---|---|---|---|
| 42474 | page | `square-cbd-hemp-ban-migration` | "Square just told you to stop selling CBD. We'll get you selling again, somewhere that works." | **CTA target.** Commercial intent. Blocks commercial queries, not informational ones. |
| 42575 | post | `merchant-account-underwriting-2026` | "What underwriters actually check before they approve a regulated ecommerce store" | **Published 2026-09-10.** Owns underwriting/MATCH/VAMP/reserves. Hard boundary. |
| 42428 | post | `shopify-vape-store-woocommerce-migration` | "Why Vape Retailers Lost Their Shopify Stores (And What to Do Now)" | Adjacent. Platform-risk thesis. |
| 42441 | post | `why-businesses-are-leaving-shopify` | "Why smart business owners are leaving Shopify (even without a ban)" | **Closest collision.** Plain-language, non-technical. |
| 12517 | page | `start-selling-cbd-online` | "Start Selling CBD Online" | Commercial CBD service page. Link target. |
| 13981 | post | `cbd-ecommerce-how-to-make-the-most-out-of-the-young-market` | "CBD eCommerce – How To Make The Most Out Of The Young Market" | 2019 growth-marketing piece. |
| 36749 | page | `high-risk-payment-processing-ecommerce-businesses` | "High-Risk Payment Processing for eCommerce Businesses" (**stored title is WRONG**: "Ecommerce Warranty Services…") | Owns high-risk payments overview. |
| 42417 | page | `high-risk-ecommerce-migration-payment-gateway-integration` | "High-Risk eCommerce Migration & Payment Gateway Integration" | Commercial LP. Link target. |
| 37458 | page | `payment-gateway-service-providers` | "Payment Gateway Service Providers – An Ultimate Guide" | Gateway overview. Link target. |
| 13533 | post | `selling-firearms-online` | "Gun Store eCommerce: Start Selling Firearms Online" | Different vertical, commercial. |
| 39362 | post | `woocommerce-niche-ecommerce-2025` | "Is WooCommerce Right for Your Niche Business in 2025?" | Niche-fit, generic. |

**Page 36749 re-confirmed as the exact trap the rule exists for.** Its stored WP title is unrelated to
its content. A title-only grep misses it. Matched here on slug and fetched H1 as required.

**No live post exists on Square, hemp, CBD account closure, or Section 781.** The topic is unclaimed in
the live corpus. **PRE-CHECK 0: PASS.**

---

## CHECK 1 — Title word overlap

**Rule:** no existing post title may share 3 or more consecutive meaningful words with the proposed title.

### Proposed title (both cases)

> Square is closing hemp and CBD accounts: what happens to your money, your data, and your catalog

### Comparison against every neighbour

| Existing title | Longest consecutive meaningful-word match | Result |
|---|---|---|
| "Why smart business owners are leaving Shopify (even without a ban)" | 0 | clear |
| "Why Vape Retailers Lost Their Shopify Stores (And What to Do Now)" | 0 | clear |
| "What underwriters actually check before they approve a regulated ecommerce store" | 0 | clear |
| "Square just told you to stop selling CBD…" (page 42474 H1) | "Square" (1) | clear |
| "CBD eCommerce – How To Make The Most Out Of The Young Market" | "CBD" (1) | clear |
| "High-Risk Payment Processing for eCommerce Businesses" | 0 | clear |
| "Gun Store eCommerce: Start Selling Firearms Online" | 0 | clear |
| "Start Selling CBD Online" | "CBD" (1) | clear |
| "Payment Gateway Service Providers – An Ultimate Guide" | 0 | clear |
| "High-Risk eCommerce Migration & Payment Gateway Integration" | 0 | clear |

Deliberate avoidances carried forward from the August audit and re-confirmed today:
- **"what to do now"** avoided. 3-word collision with post 42428's title.
- **"survival guide"** avoided. Post 41204 uses it.
- **"here's what actually changed"** avoided. Near-verbatim match to a competitor title (Evolve Payment).

Maximum consecutive match anywhere in the corpus: **1 word**. Threshold is 3.

**CHECK 1: PASS** (Case A and Case B).

---

## CHECK 2 — Slug overlap

**Rule:** proposed slug must not be a substring of any existing slug, and must not share 2 or more words
with any existing slug.

### Constraint discovered and re-confirmed

Any slug pairing `square` with any of `cbd`, `hemp`, `ban` or `migration` fails against the landing page
slug `square-cbd-hemp-ban-migration`. That rules out every obvious candidate.

### Proposed slug (both cases)

> `square-cutoff-seller-action-plan`

| Existing slug | Shared words | Result |
|---|---|---|
| `square-cbd-hemp-ban-migration` (42474) | `square` (1) | PASS |
| `shopify-vape-store-woocommerce-migration` (42428) | 0 | PASS |
| `why-businesses-are-leaving-shopify` (42441) | 0 | PASS |
| `merchant-account-underwriting-2026` (42575) | 0 | PASS |
| `cbd-ecommerce-how-to-make-the-most-out-of-the-young-market` (13981) | 0 | PASS |
| `start-selling-cbd-online` (12517) | 0 | PASS |
| `selling-firearms-online` (13533) | 0 | PASS |
| `high-risk-payment-processing-ecommerce-businesses` (36749) | 0 | PASS |
| `high-risk-ecommerce-migration-payment-gateway-integration` (42417) | 0 | PASS |
| `payment-gateway-service-providers` (37458) | 0 | PASS |
| `woocommerce-migration-guide` / `woocommerce-migration-services` | 0 | PASS |

Substring test: `square-cutoff-seller-action-plan` is not a substring of any existing slug, and no
existing slug is a substring of it. Maximum word overlap anywhere: **1**. Threshold is 2.

Rejected alternatives, for the record:
- `square-cbd-migration` — 3-word overlap with 42474. **FAIL.**
- `square-hemp-ban-deadline` — 3-word overlap with 42474. **FAIL.**
- `hemp-seller-payment-cutoff-plan` — passes, but drops the searched entity "Square". Viable fallback.
- `cbd-seller-october-deadline` — passes, but the date framing is now actively wrong given the
  December 11 move, and it ages out in weeks. **Rejected on merit, not on the check.**

**CHECK 2: PASS** (Case A and Case B).

---

## CHECK 3 — Primary keyword uniqueness

**Rule:** the primary keyword must not be the focus keyword of any existing post or page.

### Proposed primary keyword

> `Square hemp and CBD account closure` (informational intent)

Secondary: `Section 781 hemp law sellers`, `Square CBD deadline`, `payment processing after Square`.

| Property | Its focus keyword | Conflict? |
|---|---|---|
| 42474 (page) | square cbd migration to woocommerce (**commercial**) | No. Deliberately ceded. See note below. |
| 42575 (post) | merchant account underwriting | No |
| 36749 (page) | high risk payment processing | No |
| 42417 (page) | high risk ecommerce migration / payment gateway integration | No |
| 37458 (page) | payment gateway service providers | No |
| 12517 (page) | start selling CBD online | No |
| 13981 (post) | CBD ecommerce | No |
| 42428 (post) | shopify vape store woocommerce migration | No |
| 42441 (post) | leaving Shopify for WooCommerce | No |

**Cannibalisation guard, load-bearing:** the blog must not compete for commercial Square-migration
queries. Those belong to page 42474. The blog targets informational queries about *what is happening and
what it means*, then links up to 42474. The creator must keep "migration", "migrate to WooCommerce" and
"hemp-friendly processor" out of the title, slug, meta title and H1.

**Note on 42575 (published 2026-09-10):** it is not a keyword conflict, but it is a **content boundary**.
It owns underwriting, MATCH, VMSS, VAMP, Compelling Evidence 3.0, reserves, document packs and MID
routing across 28 H2s. The Square post must **not explain how underwriting works**. It states that a
dedicated merchant account requires an application and a review, links to 42575 once, and moves on.
Failing this boundary would cannibalise a one-day-old post.

**CHECK 3: PASS** (Case A and Case B), conditional on the two guards above.

---

## CHECK 4 — Angle and thesis uniqueness

**Rule:** reject if the argument or coverage is substantially the same as an existing post, even under a
different title. This is the check that matters here.

### 4.1 vs post 42441 — "Why smart business owners are leaving Shopify (even without a ban)" — THE CLOSEST COLLISION

Live H2s fetched 2026-09-11: what it means to own your store / what goes wrong when you don't / why
owners are moving to WooCommerce in 2026 / renting vs owning / isn't WooCommerce harder / what moving
looks like / cost comparison / what kinds of businesses are moving / signs it's time to leave.

Fetched-content check: 42441 contains **no mention** of Square, CBD, hemp, POS, in-person payments,
loans, or any federal law. Its thesis is ownership as a general principle.

| Dimension | 42441 | This post |
|---|---|---|
| Trigger | None. Explicitly "even without a ban" | A dated notice and an enacted federal statute |
| Subject | A platform's business model | A statute, Section 781, and its two effective dates |
| Question answered | Should I own my store? | Which of my products are still legal, and what happens to my money? |
| Decision offered | Rent vs own | Sort the catalog first, then the processor, then the store |
| Outcome promised | Control | Survival of specific SKUs, which the post concedes may fail |
| POS / in-person | Absent | Central. The cutoff hits the counter, not just the website |
| Lending | Absent | Central. Square Loan default mechanics from Square's own docs |
| Register | Plain-language, non-technical | Plain-language, non-technical (**the one shared trait**) |

**Verdict: PASS, but narrowly, and only because of the concession.** Shared plain-language register is
not an angle overlap. The differentiator that makes this defensible is that **this post argues migration
is only half the fix.** 42441 argues moving solves the problem. This post argues moving solves the
infrastructure problem and does nothing at all for the product-legality problem, because no platform
makes a 0.4 mg-over product legal on December 11.

**Binding instruction to the creator:** that concession must appear explicitly, in plain words, in the
body. If it is softened or dropped, this post loses its CHECK 4 basis and becomes a Square-flavoured
rewrite of 42441. It is also why this post must **not** use the renting-vs-owning frame, the
renting-vs-owning table, or a 3-year cost comparison. All three belong to 42441.

Linking rule: link 42441 **zero or once, at most**. It is not a supporting argument here.

### 4.2 vs post 42428 — "Why Vape Retailers Lost Their Shopify Stores"

| Dimension | 42428 | This post |
|---|---|---|
| Driver | A platform's **discretionary policy choice** | An **enacted federal statute** with a moving effective date |
| Platform | Shopify (online only) | Square (online **and** in-person POS) |
| Vertical | Vape / ENDS | Hemp and CBD |
| Format | E, contrarian thesis | D, decision-tree playbook |
| Reader | Retailer already deplatformed | Retailer with a countdown still running |
| POS dimension | None | Yes. The register stops too |
| Lending dimension | None | Yes |
| Thesis | Any SaaS platform can deplatform you; self-hosting is the structural fix | The platform is the smaller half of your problem; the statute is the larger half |

Five distinct differentiators, all confirmed by fetched content rather than assumed:
1. Different platform and different vertical.
2. **Law, not policy.** 42428's whole premise is corporate discretion. This is a statute.
3. **In-person POS is cut off too.** 42428 has no POS dimension at all.
4. **The Square Loan trap**, documented from Square's own help centre. Absent from 42428.
5. A hard near-term deadline with a countdown, and a second legal deadline that just moved.

**Verdict: PASS, comfortably.** Link 42428 once for the platform-risk argument rather than rebuilding it.

### 4.3 vs post 42575 — "What underwriters actually check" (published 2026-09-10)

Overlap risk is **coverage**, not thesis. 42575 is technical and payments-deep; this post is
plain-language and product-first. They answer different questions for different readers.

**Verdict: PASS, conditional on the CHECK 3 boundary.** No underwriting explanation in this post.

### 4.4 vs page 36749 and page 42417 — high-risk payments properties

36749 owns "what makes you high-risk / how to get approved". 42417 is a commercial migration LP. This
post covers neither. It touches payments only to say: Square was your processor as well as your
storefront, and replacing it is a separate job with its own timeline. Then it links out.

**Verdict: PASS.**

### 4.5 vs post 13981 — "CBD eCommerce – How To Make The Most Out Of The Young Market" (2019)

Opposite premise. 13981 is a growth-opportunity piece about an expanding market. This post is about a
federal contraction. No angle overlap.

**Verdict: PASS.** Recommendation: **do not link it.** It is factually stale and its optimism reads
badly beside a restriction. Noted in the research file's link table.

### 4.6 vs post 13533 — "Gun Store eCommerce: Start Selling Firearms Online" (2019)

Different vertical, commercial intent, no regulatory-change content. No overlap.

**Verdict: PASS.**

### 4.7 vs page 42474 — the Square landing page itself

This is the sharpest practical risk, because the LP already names two of our differentiators. Its H2s
include "Your in-person checkout stops working too" and "Your Square Loan repayment doesn't pause for
any of this." The blog cannot simply restate them.

Boundary map:

| LP section | Blog treatment |
|---|---|
| "If you do nothing, here's what October 15th looks like" | Go deeper and correct it: two Square dates, plus two federal dates, plus the money clock that outlives both |
| "Your in-person checkout stops working too" | LP asserts it. Blog explains what it means for the register, the card reader and the walk-in customer |
| "Your Square Loan repayment doesn't pause for any of this" | LP asserts it. Blog documents the worse version from Square's own help centre: closure can put the loan in default, permit a demand for the full balance, and permit a debit of the linked bank account |
| "Move your store off Square…" and all solution H2s | Do not restate the offer |
| "Three steps, most stores are live before the deadline" | Replace with a real timeline built backwards from verified durations |
| LP FAQ, incl. "What if the federal ban gets delayed or changed?" | Blog FAQ must use **different questions**. The delay question is now answered in the body, not the FAQ |

**Verdict: PASS**, conditional on the boundary map. The blog's job is comprehension; the LP's job is
conversion.

### 4.8 vs the unpublished August 21 draft

Not in the live corpus, so not a CHECK 4 counterparty. Under Case A it **is** this post, revised.

**CHECK 4: PASS** (Case A and Case B), conditional on the four binding instructions collected in the
"Conditions" section below.

---

## CHECK 5 — Topic cluster saturation

**Rule:** reject if 5 or more posts already exist on the same general subject within the cluster.

Three candidate clusters were counted, because the assignment matters.

### Cluster (a): broad payments — SATURATED, and this post is not in it

Nine properties per the 2026-09-09 addendum, now ten with 42575 published: 10687, 27207, 32043, 32117,
36423, 36749, 37458, 42297, 42417, 42575.

**This post is not a payments post.** Payments is one of several sections and is deliberately capped and
outsourced to 42575 and 36749 by link. Assigning it here would be a mis-assignment. Recorded for
transparency, as section 4c requires.

### Cluster (b): platform risk / deplatforming / regulated-vertical migration — the correct cluster

| ID | Slug | Subject |
|---|---|---|
| 42428 | `shopify-vape-store-woocommerce-migration` | Shopify bans vape, discretionary policy |
| 42441 | `why-businesses-are-leaving-shopify` | Ownership risk in general, no ban |
| 42177 | `volusion-to-woocommerce-migration` | A platform's business collapse |

**Three existing posts. Threshold is 5.** Not saturated.

### Cluster (c): CBD and hemp specifically

| ID | Type | Slug |
|---|---|---|
| 13981 | post | `cbd-ecommerce-how-to-make-the-most-out-of-the-young-market` (2019) |
| 12517 | page | `start-selling-cbd-online` (commercial) |
| 42474 | page | `square-cbd-hemp-ban-migration` (commercial) |

**One informational post, seven years old, with an opposite premise. Two commercial pages.** Not
saturated. Virtina lists CBD among its named industries in `brand.md`, so the cluster is on-brand.

### Sub-niche statement (required by section 4c since cluster (a) is saturated)

> The unclaimed sub-niche is **a statutory change, not a platform policy, cutting off both online and
> in-person selling for one named vertical on a deadline that has already moved once.** No Virtina
> property covers Section 781, the total-THC standard, the 0.4 mg per container cap, the November 12 /
> December 11 split, or what an outstanding Square Loan does when the account closes.

**CHECK 5: PASS** (Case A and Case B).

---

## Result

| Check | Case A (corrected August draft) | Case B (clean rewrite) |
|---|---|---|
| Pre-check 0 — pages + search sweep | **PASS** | **PASS** |
| CHECK 1 — title overlap | **PASS** (max 1 consecutive word) | **PASS** |
| CHECK 2 — slug overlap | **PASS** (max 1 shared word) | **PASS** |
| CHECK 3 — primary keyword | **PASS**, conditional | **PASS**, conditional |
| CHECK 4 — angle / thesis | **PASS**, conditional | **PASS**, conditional |
| CHECK 5 — cluster saturation | **PASS** (3 in cluster, threshold 5) | **PASS** |

**VERDICT: APPROVED. Case A is the binding path, per the orchestrator's decision.**

---

## Conditions — all four are binding, and the publisher must verify each

1. **The concession must survive.** The post states explicitly, in plain words, that moving the store
   fixes the platform problem and does nothing for the product problem. This is the sole basis on which
   CHECK 4 clears post 42441. If an edit removes it, uniqueness fails.
2. **No underwriting explanation.** Post 42575 went live 2026-09-10 and owns that territory. Link it
   once; do not teach it.
3. **No commercial Square-migration keywords** in title, H1, slug or meta title. Those belong to page
   42474.
4. **No renting-vs-owning frame, no ownership table, no 3-year cost table.** All three are post 42441's.

Additional, carried from the research file:

5. **The November 12 / December 11 split must be stated correctly.** Repeating the landing page's
   "November 12 redefines legal hemp" would publish a known factual error. Verified against the enrolled
   text of H.R. 6500, Division B, Section 2019.
6. **FAQ questions must differ from page 42474's FAQ.** The publisher pulls the LP's FAQ and dedupes.

---

## Post-draft phrasing uniqueness (publisher runs before PUT)

- No sentence longer than 8 words may appear verbatim in any existing Virtina post or page.
- Run the 8-gram check against: the live corpus, every local draft **including the August 21 draft's
  unrevised passages**, and the landing page 42474's rendered copy.
- Expected benign result, documented previously for posts 42428 and 42491: the only hit should be the
  shared TOC label sequence "people also ask conclusion frequently asked questions". Anything else is a
  real overlap and must be rewritten.

---

## Final recommendation

- **Title:** Square is closing hemp and CBD accounts: what happens to your money, your data, and your catalog
- **Slug:** `square-cutoff-seller-action-plan`
- **Primary keyword:** `Square hemp and CBD account closure`
- **Secondary:** Section 781 hemp law sellers, Square CBD deadline, payment processing after Square
- **Search intent:** informational. Commercial intent stays with page 42474.
- **Format:** D, decision-tree / playbook. Recency check on the last ten published posts (42575, 42491,
  42465, 42441, 42428, 42393, 42391, 42297, 42202, 42177) shows formats A, B and E in rotation and
  **no D**. Format D is unused and fits a sequence of decisions against a hard external date.
- **Target length:** 2,200 to 2,600 words, trimmed down from the August draft's 3,480.
