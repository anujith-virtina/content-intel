---
title: Uniqueness audit — Ecommerce Redesign vs. Website Rebuild
client: virtina
date: 2026-10-05
topic: Ecommerce Redesign vs. Website Rebuild, What's the Difference
stage: research
---

# Uniqueness audit — "Ecommerce Redesign vs. Website Rebuild: What's the Difference?"

## Pre-check: inventory staleness

`published-posts-inventory.md` `last_updated` = 2026-09-09. Today is 2026-10-05 (26 days stale, over the
7-day threshold). Live REST pulls were run in place of a full file refresh:

- `GET /wp-json/wp/v2/posts?per_page=20&orderby=date&order=desc&status=publish` — returned the 20 most
  recent published posts through 2026-10-01 (IDs 43036 down to 42108). This confirms three posts the
  static inventory file does NOT separately list at the top level by date but which ARE already
  documented in the body of the file: 43029, 43036 (both 2026-09-30/10-01), plus 42985 (UCP guide,
  2026-09-29), 42692 (food & beverage platforms, 2026-09-24), 42585 (Square CBD, 2026-09-15), 42582
  (Magento support cliff, 2026-09-11), 42575 (merchant underwriting, 2026-09-10). None of these are
  in the redesign/rebuild cluster except 43029 and 43036, already analyzed below.
- `GET /wp-json/wp/v2/search?search=redesign` and `search=rebuild` — both run, each returning 30 results
  spanning posts and pages. No additional redesign/rebuild post or page surfaced beyond what's already
  known (43029, 43036, 40727, page 42707).

**Inventory file itself was not edited** (out of scope for this task) — the live pulls above substitute
for the refresh requirement for audit purposes. Recommend a full file refresh on the next task that
touches the inventory.

## Pre-check 0: pages sweep (not posts-only)

Per the posts-only blind spot documented 2026-09-09 (page 36749 incident), pages were swept directly:

- `GET /wp-json/wp/v2/pages?per_page=100&status=publish&_fields=id,slug,title,link` — reviewed in full.
  Only one page matches the redesign/rebuild/replatform keyword set: **page 42707**,
  `ecommerce-website-redesign`, "eCommerce Website Redesign Services" — this is the intended money page
  target for this new post, not a competing uniqueness risk. No page titled or slugged around "rebuild"
  or "replatform" exists.
- `search=redesign` confirmed page 42707 as the only redesign-relevant page result (plus unrelated posts
  already known).
- `search=rebuild` confirmed no page result at all for "rebuild" — zero pages use that term.

No false-pass risk from an untracked page. Pre-check 0 clear.

## Candidate evaluated

**Topic**: Ecommerce Redesign vs. Website Rebuild: What's the Difference?
**Proposed primary keyword**: redesign vs rebuild (ecommerce)
**Proposed slug candidates**: `redesign-or-rebuild` (preferred) or `redesign-vs-rebuild-decision` — both
avoid pairing "ecommerce" with "redesign" or "website" with "redesign", which are the two-word
combinations already claimed by existing slugs (see Check 2).

### CHECK 1 — Title word overlap: PASS

Compared against every title containing "redesign" or "rebuild" in the corpus:

| Existing title | Shared consecutive words with proposed title |
|---|---|
| "Why eCommerce Sites Lose Rankings After a Redesign (And How to Prevent It)" (43029) | "a Redesign" — 2 words, not 3 |
| "How an Outdated Ecommerce Website Hurts Conversions" (43036) | "Ecommerce Website" — 2 words, not 3 |
| "How To Redesign Your eCommerce Website In 2026: The Ultimate Guide" (40727) | "eCommerce Website" — 2 words, not 3. Word order differs ("Redesign Your eCommerce Website" vs proposed "Ecommerce Redesign vs. Website Rebuild") |
| "eCommerce Website Redesign Services" (page 42707, not a post but checked for safety) | "eCommerce Website Redesign" is a 3-word consecutive phrase in the page title. The proposed title does NOT reproduce that exact consecutive sequence ("Redesign vs. Website Rebuild" breaks the sequence with "vs."), so no 3-consecutive-word match. **Flagged as a close call** — the analyzer should keep the final H1 phrased with "vs." or "or" directly after "Redesign" (not "Website Redesign") to stay clearly clear of this page's exact phrase. |

No existing POST title shares 3+ consecutive meaningful words. PASS, with the H1-phrasing caution noted
above for the analyzer.

### CHECK 2 — Slug overlap: PASS (with a slug constraint)

- `redesign-without-losing-rankings` (43029): shares only "redesign" — 1 word. Safe.
- `outdated-store-hurts-conversions` (43036): 0 words shared. Safe.
- `redesigning-your-ecommerce-website-5-steps` (40727): shares "ecommerce" if the proposed slug used it, plus the stem "redesign". To stay under the 2-word threshold, the proposed slug must NOT contain both "ecommerce" and "redesign" together, and must not contain both "website" and "redesign" together.
- `ecommerce-website-redesign` (page 42707): shares "ecommerce" + "redesign" = 2 words if the proposed slug naively used `ecommerce-redesign-vs-rebuild`. **This combination is blocked.**

**Resulting constraint**: the final slug must drop either "ecommerce" or "website" from the string, since
"redesign" is the unavoidable anchor term. Recommended: `redesign-or-rebuild` or
`redesign-vs-rebuild-decision` — neither contains "ecommerce" or "website", so neither trips the 2-word
rule against any existing slug or the money-page slug. PASS once slug follows this constraint.

### CHECK 3 — Primary keyword uniqueness: PASS

No existing post or page claims "redesign vs rebuild," "redesign or rebuild," or "when to rebuild instead
of redesign" as a focus keyword. 43029's focus is ranking loss mechanics after a redesign (SEO-specific).
43036's focus is conversion loss from an outdated store (with one short diagnostic subsection touching
this decision, addressed under Check 4). 40727's focus is redesign process/benefits/AI trends, not a
redesign-vs-rebuild decision at all. Page 42707 is a service page, not a keyword-targeting informational
asset. PASS.

### CHECK 4 — Angle/thesis uniqueness: PASS, with mandatory differentiation requirements

This is the decisive check. Full content audit of the two closest neighbors:

**Post 43029** (`redesign-without-losing-rankings`): owns the SEO-mechanics lane only — redirect
maps/chains, content loss, template-rewritten titles/H1s, nav orphaning, structured data loss, Core Web
Vitals regressions, staging noindex left live. It does not address whether to redesign or rebuild at all;
it assumes a redesign is happening and protects rankings during it. **No overlap risk.**

**Post 43036** (`outdated-store-hurts-conversions`): fetched and read the live draft HTML directly. It
contains exactly one H2 ("When should you redesign instead of optimising what you have?") with two H3
subsections ("Fix in place when the problem is local and additive," "Rebuild when the constraint is the
build itself") and one short H3 ("A short test for whether you need a rebuild"). The entire treatment is
roughly 4 short paragraphs plus one example. It:
- States one single test: "redesign when the build itself blocks the fix, optimise when the problem is
  local and fixable in place"
- Gives one example each for "fix in place" and "rebuild"
- Does NOT include a comparison table
- Does NOT break out cost, timeline, or risk as separate dimensions
- Does NOT address budget, risk tolerance, or codebase/platform constraints as named decision criteria
- Does NOT describe what a redesign project or a rebuild/replatform project actually involves
  process-wise (phases, deliverables, team composition, typical duration)
- Frames the whole discussion as one diagnostic step inside a broader article about technical debt and
  conversion cost, not as a standalone decision guide

**Required differentiation for the new post** (binding on the analyzer and creator):
1. Do not reuse 43036's test language verbatim or near-verbatim ("fix in place when the problem is local
   and additive," "rebuild when the constraint is the build itself," "short test for whether you need a
   rebuild"). Build an independent criteria framework: scope of change, codebase/platform constraints,
   technical debt, budget, timeline, risk tolerance.
2. Include a comparison table (redesign vs. rebuild: cost, timeline, risk, what you keep, what you lose)
   — this content element does not exist anywhere in the cluster today.
3. Include process-level detail: what a redesign project actually involves (phases, typical scope) versus
   what a rebuild/replatform project actually involves. This is the structural gap in 43036 and the
   differentiator that makes this post the standalone resource 43036 only gestures at.
4. Treat this as the definitive decision guide the money page (42707) and 43036 both link out to, not a
   second pass at 43036's symptom test.

Angle is distinct and the required differentiation is documented. **PASS**, conditioned on the creator
following the four points above. The post-draft phrasing check (no 8+ word verbatim match) will verify
this at the publisher stage.

### CHECK 5 — Topic cluster saturation: PASS

Posts directly in the redesign/rebuild decision cluster: 43029, 43036, 40727 — **3 posts**. Below the
5-post saturation threshold. Loosely adjacent posts (replatform-flavored but on a different specific
topic) — 42582 (Magento version support cliff: upgrade/move/replatform, which is a forced-deadline
scenario, not a redesign-vs-rebuild choice) and 42413 (BigCommerce to Magento migration, a specific
migration path, not a redesign/rebuild framework) — were reviewed and are thematically adjacent but not
the same general subject a reader asking "redesign or rebuild my ecommerce site" would land on. Cluster
is not saturated. PASS.

## Final verdict

| Check | Result |
|---|---|
| 1. Title word overlap | PASS (H1-phrasing caution vs. page 42707 noted) |
| 2. Slug overlap | PASS (slug must exclude "ecommerce"+"redesign" and "website"+"redesign" pairs — use `redesign-or-rebuild` or `redesign-vs-rebuild-decision`) |
| 3. Primary keyword uniqueness | PASS |
| 4. Angle/thesis uniqueness | PASS, with 4 binding differentiation requirements vs. post 43036 |
| 5. Topic cluster saturation | PASS (3 posts in cluster, under the 5-post threshold) |

**Topic approved.** Proceed to brief stage with the differentiation requirements above carried forward
verbatim into the brief.
