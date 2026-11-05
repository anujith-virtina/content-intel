---
title: Uniqueness audit - WooCommerce emails not sending
client: virtina
date: 2026-11-02
topic: woocommerce emails not sending (lead-gen, US store owners)
audience: US WooCommerce store owners losing orders to missing store emails
stage: research
slug: order-emails-not-sending
---

# Uniqueness audit: "WooCommerce emails not sending"

## Method and limits
- Corpus: `scratchpad/corpus.json` (596 live posts and pages, id/date/slug/title only, no body text). Because it holds titles and slugs only, body-level checks were done by fetching the nearest posts and pages through the REST API and reading H2/H3 and email sentences.
- Pre-check 0 sweeps run: `/wp-json/wp/v2/search?search=` for `email`, `SMTP`, `deliverability`, `transactional`, `woocommerce emails not sending`. Pages 15893, 39979, 30341, 10747, 38710, 43504, 43604, 11103, 20484, 20519, 10742, 40127, 33663 were fetched by id and by live URL.
- Inventory refresh: `published-posts-inventory.md` last_updated is 2026-09-09 (stale, more than 7 days). The live corpus.json dated 2026-11-02 replaces it for this audit.
- Tooling note: no Bash for sub-agents. Page "200" checks were done with WebFetch (successful render). WebFetch follows same-host redirects, so canonical URLs were confirmed from the REST `link` field. Zero 429s were hit on page loads. One REST list call returned 429 (treated as rate limit, not dead).

## Corpus grep results
- Posts with "email", "smtp", "deliverability", "transactional" in slug or title: **0**.
- Slugs containing `email`: none.
- Titles containing `email`: only partner-resources internal posts (outreach email, Gmail signature guide, URLs for email/CRM). Not public editorial, not topical.
- Search "SMTP": 1 hit, post 40347. Search "deliverability": hit on page 15893 (the WooCommerce Bug Fix service page). Search "transactional": only post 10619 (WooCommerce 3.5, 2018 update post, mentions "improved transactional emails" as a feature).

## Nearest content, fetched and read

| Item | Email content found | Verdict |
|---|---|---|
| Post 40347 `woocommerce-bug-fix-guide` | H2 "How to Fix Email Errors" (2 short steps: use a dedicated SMTP plugin and name WP Mail SMTP; confirm From address exists) plus one table row "Missing order emails". ~3,000-word post. | **Closest overlap.** One section, no diagnostic order, no logs, no DNS, no order-status causes, no handoff criteria. New post must not reuse its wording ("stop using the default WordPress email function") or name its plugin. Link to it. |
| Post 43264 `woocommerce-holiday-season-checklist` | One bullet: confirmation email within a minute, not in spam; "If your host limits outgoing mail, use a dedicated email service." | Passing mention. Vary phrasing. |
| Post 40784 `woocommerce-checkout-not-working-agency` | None. H2s are agency hiring criteria. | No overlap. |
| Post 38785 `woocommerce-issues-killing-conversions` | Only marketing email list mentions. | No overlap. |
| Post 43361 `woocommerce-hpos-plugin-compatibility` | Custom order fields that go blank in customer emails (one test). | Minor; useful interlink. |
| Post 10902 `reduce-shopping-cart-abandonment` | One abandoned-cart reminder sentence. H4s only. | No overlap. |
| Post 43266 mobile checkout/BNPL | "Check that the order email arrives" (x2). | Passing mention. |
| Post 40439 black friday | Marketing emails only. | No overlap. |
| Post 43336 `ecommerce-website-problems` | "Check the order, the email and the payment record." | Passing mention. |
| Post 43583 holiday returns policy | Returns/refund email templates (post-sale comms). | Different topic. |
| Draft 43089 `customer-payment-declined-guide` | No email/SMTP content in local draft. REST `?p=43089` returns 404 publicly, state file says `status: draft`. | **Not live: do not link.** |
| Drafts 43753 (quick order form), 43758 (B2B marketplaces) | Not email topics. | No overlap. |

## Pages: who owns the "fix" intent (lead targets)
- **`/woocommerce-bug-fix/` (page 15893, ~1,500 words).** Service landing page. Has a card titled "Email & Order Notifications" ("Fix deliverability and trigger logic so everyone receives the right emails"). Pitch only, no explanatory content. This is the **best lead target** and does not own the informational keyword.
- `/ai-powered-woocommerce-bug-fix/` (39979): symptom-led service page, CTA "Fix my WooCommerce store". No email content.
- `/ecommerce-store-takeover/` (43504): contact form has an "Email & Order Issues" option. For stores inherited from another developer.
- `/woocommerce-support/` (10747): ongoing support packages and one-time fix request.
- `/ecommerce-bug-fix/` (30341, ~400 words, thin). `/wordpress-support-maintenance/` (38710), `/ecommerce-support/` (20484): generic.
- `/platforms/woocommerce-development-services/` (43604): the broad money page. WooCommerce rules say always use the `/platforms/` form.
- No page owns an editorial answer to "woocommerce emails not sending". No cannibalisation risk with the service pages: they are transactional pages, this post is informational and feeds them.

## Candidate topics evaluated

| Candidate | Result | Reason |
|---|---|---|
| A. WooCommerce emails not sending: diagnose by stage, then hand-off criteria | **SELECTED** | Passes all 5 checks (below) |
| B. WooCommerce SMTP setup guide | REJECT (Check 4, brand) | Becomes a plugin tutorial that duplicates 40347 section and every vendor SERP; pushes toward naming plugins; weak lead intent |
| C. Email deliverability SPF/DKIM/DMARC for stores | REJECT (brand.md) | "Generic email marketing/deliverability" is a theme to avoid; low volume; no fix intent |
| D. Abandoned cart email recovery | REJECT (Check 4) | Overlaps 10902 and marketing-themed; off-brand |

## Proposed title and slug
- **H1 / title (recommended):** "WooCommerce emails not sending? Diagnose it in four steps, then decide who fixes it"
- **Yoast title (54 chars):** "WooCommerce Emails Not Sending? How to Fix It | Virtina"
- **Slug (recommended):** `order-emails-not-sending`. Fallback: `store-emails-not-sending`.
- Slug note: the natural `woocommerce-emails-not-sending` FAILS Check 2 (shares `woocommerce` + `not` with `woocommerce-checkout-not-working-agency`, and `woocommerce` with ~30 slugs). Same workaround as posts 42441/42491: keyword stays in title, H1, meta, first 100 words; slug omits `woocommerce`.

## The 5 checks

**CHECK 1, title overlap: PASS.** Compared against all 596 titles. Content-word runs in the proposed title: "WooCommerce emails not sending", "diagnose it", "decide who fixes". No existing title has any 3-word run in common. Nearest: "Which Agency Can Fix a WooCommerce Checkout Not Working" (shares "WooCommerce" only), "Top 10 WooCommerce Issues That Kill Conversions (and How to Fix Them)" ("How to Fix" appears only if the title were rewritten that way; the recommended H1 avoids it). Note: if the Yoast title "How to Fix It" is used, "how to fix" is 3 words but the stop words "to" and "it" are ignored, leaving "fix" only, and no title has "emails ... fix".

**CHECK 2, slug overlap: PASS** for `order-emails-not-sending`. Not a substring of any slug. Words: order, emails, not, sending. Slugs containing `order`: `order-fulfillment-services-ecommerce` (1 word). Slugs containing `not`: `woocommerce-checkout-not-working-agency` (1 word, and "not" is a function word). No slug contains 2 of the 4 words. `emails` and `sending` appear in no existing slug.

**CHECK 3, primary keyword: PASS.** "woocommerce emails not sending" is the focus keyword of no post or page. No slug encodes it. Closest: page 15893 `woocommerce-bug-fix` (service page, keyword "woocommerce bug fix").

**CHECK 4, angle/thesis: PASS (with conditions).** Existing angle in 40347: "use an SMTP plugin and verify From". New thesis: a missing store email fails at one of four distinct stages (not triggered, not sent, sent but not delivered, delivered to spam), and WooCommerce's own transactional-emails log tells you which stage within minutes, before you install anything. The post then draws a hard line between what an owner can fix and what needs a developer (order status never reaching Processing, fatal errors, conflicts that need staging, DNS access, host-level failures). Conditions: no plugin name; do not reuse 40347 or 43264 phrasing; link to 40347 as the broader bug list.

**CHECK 5, cluster saturation: PASS.** Posts a reader seeking "woocommerce emails not sending" would already find on virtina.com: 2 (40347 one section, 43264 one bullet). Under 5. The wider WooCommerce troubleshooting cluster is large (40347, 40784, 38785, 43361, 43264, 43266, 43336, drafts 43089 = 8), so it is flagged saturated at cluster level, but the email-failure sub-niche is unclaimed. Documented sub-niche: diagnosis by stage plus developer handoff criteria.

**Phrasing uniqueness (post-draft, to be run by the publisher):** 8-gram check against all live posts and local drafts. Specific watch phrases: "default WordPress email function", "host limits outgoing mail", "From address is valid and actually exists", the boilerplate "builds on WooCommerce" platform sentence.

## Verdict
**GO.** Selected topic passes all 5 checks and pre-check 0. Main risk is the 40347 email section; mitigated by angle, no plugin naming, and linking to it.
