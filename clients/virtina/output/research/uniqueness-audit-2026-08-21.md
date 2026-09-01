---
title: Uniqueness audit — Square CBD/hemp cutoff post
client: virtina
date: 2026-08-21
stage: research
slug: uniqueness-audit-square-cbd
---

# Uniqueness audit (MUST-FOLLOW section 1 — all 5 checks)

## Pre-check: inventory refresh — FAILED, workaround used

- `published-posts-inventory.md` `last_updated: 2026-07-24`. Today is 2026-08-21 → **28 days stale**, refresh required.
- **Refresh could not be performed.** No Bash/shell tool in this session, and `WebFetch` returns **HTTP 403** on `https://virtina.com/wp-json/wp/v2/posts?...` (Cloudflare). The mandated browser-UA python fetch was not executable.
- **Workaround:** site-restricted searches against `virtina.com` (Google index) to surface live URLs, plus the orchestrator's live post list.

### ⚠ CONFIRMED INVENTORY ERRORS — fix these

The inventory records **wrong slugs** for the two most adjacent posts. This is dangerous, because CHECK 2 is run against slugs.

| Post | Slug in inventory | **Actual live slug** | Evidence |
|---|---|---|---|
| 42428 | `shopify-vape-ban-merchant-deplatforming` | **`shopify-vape-store-woocommerce-migration`** | Confirmed twice by site-restricted search: `https://virtina.com/shopify-vape-store-woocommerce-migration/` is indexed with title "Why Vape Retailers Lost Their Shopify Stores \| Virtina". Matches the orchestrator's live pull. |
| 42441 | `leaving-shopify-ownership-risk` | **`why-businesses-are-leaving-shopify`** | Per orchestrator's live post list. Not independently index-confirmed by me. |

Also: 42428 is recorded as **draft** in the inventory but is **`publish`** per the orchestrator's live pull. **All checks below use the live slugs, not the inventory slugs.** The inventory needs a real REST refresh before the next post.

### Adjacent items used in this audit

| Ref | Title | Slug | Status |
|---|---|---|---|
| Landing page | Square CBD Migration to WooCommerce Before Oct 15 | `square-cbd-hemp-ban-migration` | live, ~2,261 words |
| 42428 | Why Vape Retailers Lost Their Shopify Stores (And What to Do Now) | `shopify-vape-store-woocommerce-migration` | publish, 2,014 words |
| 42441 | Why smart business owners are leaving Shopify (even without a ban) | `why-businesses-are-leaving-shopify` | draft |
| 13981 | CBD eCommerce – How To Make The Most Out Of The Young Market | `cbd-ecommerce-how-to-make-the-most-out-of-the-young-market` | 2019 |
| 36423 | 11 Best WooCommerce Payment Gateways | `best-woocommerce-payment-gateways` | 2024 |
| 27207 | Top WooCommerce Payment Gateways for WordPress | `woocommerce-payment-gateways` | 2022 |
| 29601 | WooCommerce Migration Guide | `woocommerce-migration-guide` | 2022 |

---

## Candidate topics evaluated

### Candidate A — REJECTED
**"Square banned CBD: how to migrate your store to WooCommerce"**
- **CHECK 2: FAIL.** Slug `square-cbd-woocommerce-migration` shares `square`+`cbd`+`migration` (3 words) with `square-cbd-hemp-ban-migration`, and `woocommerce`+`migration` (2 words) with `shopify-vape-store-woocommerce-migration`.
- **CHECK 4: FAIL.** This is the naive version. Its thesis ("you got cut off, WooCommerce is the fix") is 42428's thesis with the nouns swapped. Rejected.

### Candidate B — REJECTED
**"Why any platform can cut off your CBD store overnight"**
- **CHECK 4: FAIL, hard.** This is 42428's thesis verbatim in spirit ("Why this is not just a vape industry problem" / "Why any SaaS platform can deplatform you"). Duplicates the exact argument the orchestrator flagged. Rejected.

### Candidate C — REJECTED
**"Best payment gateways for CBD sellers in 2026"**
- **CHECK 3: FAIL.** Payment-gateway keyword already claimed by 36423 and 27207.
- **CHECK 5: FAIL.** Gateway/payment cluster already carries 36423, 27207, 32117, plus the `payment-gateway-service-providers` and `high-risk-payment-processing-ecommerce-businesses` service pages. Rejected.

### Candidate D — **SELECTED**
**Title:** "Square is closing hemp and CBD accounts: what happens to your money, your data, and your catalog"
**Slug:** `square-cutoff-seller-action-plan`
**Primary keyword:** Square hemp and CBD account closure
**Thesis:** Square leaving is a symptom, not the disease. You have two separate problems — an infrastructure problem (you are a sub-merchant on Square's MID) and a catalog problem (Section 781 removes some SKUs from the definition of hemp). Migration fixes the first. **Nothing fixes the second.** Sort your catalog before you buy anything, then work backwards from three overlapping clocks.

---

## The five checks on Candidate D

### CHECK 1 — Title word overlap: **PASS**
Proposed title content words: `Square, closing, hemp, CBD, accounts, happens, money, data, catalog`.

Longest consecutive meaningful-word run against any existing title: **1**.
- vs 42428 ("Why Vape Retailers Lost Their Shopify Stores (And What to Do Now)") — 0 shared content words.
- vs 42441 ("Why smart business owners are leaving Shopify (even without a ban)") — 0.
- vs 13981 ("CBD eCommerce – How To Make The Most Out Of The Young Market") — shares `CBD` only, non-consecutive.
- vs landing page ("Square CBD Migration to WooCommerce Before Oct 15") — shares `Square` and `CBD`, but **not consecutively** (proposed reads "Square is closing hemp and CBD"; landing reads "Square CBD Migration"). No 3-word run.

**Deliberate avoidances baked into the title:**
- No "what to do now" → would collide with 42428's title tail.
- No "Here's what actually changed" → near-verbatim match to Evolve Payment's competing title.
- No "survival guide" → post 41204 uses it.

### CHECK 2 — Slug overlap: **PASS**
Proposed slug: `square-cutoff-seller-action-plan`.
- Not a substring of any existing slug, and no existing slug is a substring of it.
- vs `square-cbd-hemp-ban-migration` → **1** shared word (`square`). Under the threshold.
- vs `shopify-vape-store-woocommerce-migration` → **0**.
- vs `cbd-ecommerce-how-to-make-the-most-out-of-the-young-market` → **0**.
- vs `why-businesses-are-leaving-shopify` → **0**.
- vs `high-risk-payment-processing-ecommerce-businesses` → **0**.
- vs `woocommerce-migration-guide` / `migrate-to-woocommerce` / `best-woocommerce-payment-gateways` → **0**.

**Constraint documented for future posts:** any slug containing `square` plus any of {`cbd`, `hemp`, `ban`, `migration`} automatically fails CHECK 2 against the landing page slug. This eliminated every obvious slug and is why the recommended one is entity-plus-action rather than entity-plus-topic.

**Backups, both also passing:** `hemp-seller-payment-cutoff-plan` (1 overlap: `hemp`), `cbd-seller-october-deadline` (1 overlap: `cbd`).

### CHECK 3 — Primary keyword uniqueness: **PASS, with a self-cannibalization guard**
- `Square hemp and CBD account closure` is not the focus keyword of any existing post. Grepping the inventory for `square` returns **zero** posts; Square appears only as a platform mention.
- **Guard:** the `/square-cbd-hemp-ban-migration/` landing page owns the **commercial** terms ("square cbd migration to woocommerce", "move my square cbd store"). The blog must target **informational** intent only: what changed, which deadline is mine, what happens to my money/data, what survives the law. The blog links **up** to the landing page and must not compete for its queries. Analyzer to enforce.

### CHECK 4 — Angle/thesis uniqueness: **PASS** (see extended reasoning below)

### CHECK 5 — Topic cluster saturation: **PASS, flagged**
- Parent WooCommerce cluster: **51 posts** — saturated at the parent level.
- Relevant sub-cluster (deplatforming / high-risk / regulated-category migration): **3 blog posts** — 42428, 42441, 13981 — plus one landing page. **Below the 5-post threshold.**
- **Sub-niche justification (required because the parent cluster is saturated):** no existing Virtina post makes an **enacted federal statute** the spine of the decision, none deals with a **payment processor** rather than a storefront platform, and none argues that **migration has limits**. Sub-niche is unclaimed.
- **Warning to the orchestrator:** this makes 4 items in the deplatforming sub-cluster. One more and CHECK 5 is at risk. Recommend no further platform-risk posts without a genuinely new axis.

---

## CHECK 4, extended: the 42428 separation

The orchestrator asked me to verify or correct the proposed separation and not to force a PASS.

**Verdict: PASS — but the orchestrator's proposed separation is not sufficient on its own. I am correcting it upward.**

### Where the orchestrator's separation is weak
The proposed split was "42428 = a platform removed the store; ours = a processor cut off a category." That distinction is real but **thin**, for two reasons:

1. **Square is not purely a processor.** For most affected sellers Square is the POS *and* Square Online *and* the merchant of record. So "the storefront survives, only payments stop" is **not true** for hemp-primary sellers, whose entire Square account closes Nov 5. The clean processor-vs-platform line does not hold.
2. **Any post built on that split still lands on 42428's two owned theses** — "SaaS platforms can deplatform you" and "WooCommerce removes platform risk" — just with Square in the subject slot. 42428 even has a payment-gateway H2 already. On its own, this separation would be a CHECK 4 near-miss.

### The separation that does hold
Move the subject of the sentence from the **company** to the **statute**, and add a limit that 42428 never concedes.

| | 42428 (vape/Shopify) | This post |
|---|---|---|
| Cause | A platform's **discretionary policy** decision | An **enacted federal statute** (Section 781, H.R. 5371, signed Nov 12 2025) with a **live, unresolved** effective date |
| Thesis | Platform risk is structural; own your store | **Two problems, not one.** Infrastructure is fixable. Catalog legality is not. |
| Does migrating solve it? | **Yes** — that is the post's promise | **Partly, and the post says so out loud.** Moving does not make a 5 mg gummy legal. |
| Core mechanism explained | SaaS platform control | **PayFac / sub-merchant vs owned MID** — never covered in 42428 |
| Decision the reader makes | Which platform to be on | **Which of my SKUs survive Section 781** — a product decision, made before any platform decision |
| Time structure | Open-ended | Three dated, overlapping clocks: Oct 15, Nov 5, 120-day chargeback tail; plus 2-week card export and ~6-week underwriting running backwards |

The load-bearing difference is the **concession**. 42428 argues migration is the fix. This post argues migration is *half* the fix and refuses to sell the other half. Two posts cannot have the same thesis when one of them limits the other's promise. They are complementary, not duplicative.

### Enforcement rules for the analyzer and creator
1. **Do not re-argue "any SaaS platform can deplatform you."** State it in one sentence, **link to 42428**, move on.
2. **Do not re-argue "WooCommerce removes platform risk."** Link to 42428. This post's WooCommerce section is about **owning your own MID and your own database**, framed as ownership of the *payment relationship*, not as platform-risk elimination.
3. **Do not open with a deplatforming story.** 42428 and 42441 both open that way. Open on the catalog decision or on the email that landed on Aug 7.
4. **Avoid 42441's "renting vs owning" metaphor entirely.**
5. **No comparison table of Shopify vs WooCommerce.** Owned by 36721 and 42441.
6. Phrasing guard: publisher runs the 8-gram check against 42428, 42441, 13981 **and the landing page HTML**, with `<style>` blocks and inline `style="..."` attributes stripped first (per the post-42465 methodology note).

---

## FINAL RESULT

**Candidate D — APPROVED. All five checks PASS.**

- CHECK 1 (title overlap): **PASS**
- CHECK 2 (slug overlap): **PASS**
- CHECK 3 (primary keyword): **PASS**, with self-cannibalization guard against the landing page
- CHECK 4 (angle/thesis): **PASS**, on the corrected statute-plus-concession separation, not the processor-vs-platform separation
- CHECK 5 (cluster saturation): **PASS**, flagged — sub-cluster goes to 4 of 5

**Blocking items to clear before publish:**
1. **Refresh `published-posts-inventory.md` via WP REST with the browser UA**, and correct the two wrong slugs and 42428's status. Re-run CHECK 2 against the refreshed list.
2. **HTTP-verify every internal link** with the browser UA. My verification was index-based only.
