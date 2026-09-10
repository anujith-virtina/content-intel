---
title: Brief — The August 2026 Magento support cliff
client: virtina
date: 2026-09-10
topic: Magento / Adobe Commerce end of support, and the upgrade vs replatform decision
audience: B2B eCommerce leaders (VP eCommerce, Director of Digital) running Magento Open Source or Adobe Commerce
stage: brief
slug: magento-version-support-cliff-2026
research: clients/virtina/output/research/magento-support-cliff-2026-09-10.md
competitor_analysis: clients/virtina/output/research/competitor-analysis-2026-09-10.md
uniqueness_audit: clients/virtina/output/research/uniqueness-audit-2026-09-10.md
format: D (decision-tree / playbook)
target_words: 2100
---

# Brief: The August 2026 Magento support cliff

## Format selection (MUST-FOLLOW-RULES section 11)

1. **Format chosen: D (decision-tree / playbook).**
2. **Reason:** the reader is standing at a dated fork with four real exits, and section 11 names migration and platform-selection decisions as Format D's exact use case.
3. **Formats skipped for overuse:** Format E is **blocked**, used in 3 of the last 7 published posts (42491, 42465, 42428), which trips the recency rule. Format B was used in 42441 and Format A twice (42393, 42391), so both were available but fit worse. Format D was used once recently (42413), which is inside tolerance.

**Uniqueness confirmed** against `published-posts-inventory.md` and `uniqueness-audit-2026-09-10.md`. Topic, angle and slug all clear. The rejected topic in that audit was "Magento to WooCommerce migration", which failed checks 2, 3 and 5. This post is Alternative 1 from the same audit and passes all five checks. Inventory grep for `end of support|EOL|2\.4\.[6-9]|PHP 8|Symfony|composer` returned zero matches across 310 posts.

---

## Thesis

> Adobe's own end-of-support documentation, not an agency's opinion, is what makes 11 August 2026 a real deadline, and once you read it honestly three of the four available responses do not involve leaving Magento at all.

## Why this, why now, why us

- **Why this angle:** every one of the five ranking competitors was written by a party that sells the outcome it recommends. Magento agencies conclude "upgrade". Shopify partners conclude "Shopify". SaaS vendors conclude "SaaS". Leading with the path that earns Virtina nothing is the only differentiator none of them can copy without contradicting their own business model.
- **Why now:** the cliff was one month ago, so the reader is past the panic and into the budgeting. The next cliff, 31 May 2027 for 2.4.7, is close enough to plan against. That is the window this article owns.
- **Why Virtina:** Virtina is Magento certified and also runs WooCommerce, BigCommerce and Shopify practices. It is one of the few parties that can name the five profiles who should stay on Magento without arguing against itself.

### Honesty note the creator must absorb before writing

**We do not win on breadth.** The top competitor (The Commerce Shop, ~4,500 words) cites Adobe, covers the upgrade-versus-replatform decision properly, and already has a "when the platform still fits" section. Do not try to out-cover it at 2,100 words. There are exactly three openings and the whole article is built on them:

1. **Cost structure**, where every competitor either gives nothing or gives unsourced dollar ranges that conflict by 10x.
2. **Taking a position on destinations**, where the top competitor gives five destinations equal weight and no opinion, which the audience file lists under what readers hate.
3. **Adobe's own PCI wording**, which no competitor in the set surfaces. They route PCI through PHP end-of-life instead, which suggests they could not verify it either.

## Audience

VP eCommerce, Director of Digital and Head of eCommerce at manufacturers, distributors and wholesalers between $5M and $500M revenue, running Magento Open Source or Adobe Commerce.

**They already know:** what Magento is, what a point release is, that upgrades are painful, that their agency has an interest in the answer. Do not explain Magento, do not explain what a version number means, do not explain why security patches matter.

**What they are actually trying to figure out:** whether the deadline is real or agency scare copy, whether they are non-compliant today, what it will cost, and whether this is the moment to leave. They arrive mid-budget-cycle with a board question they cannot answer.

## Format and length

- **Format:** D, decision-tree / playbook
- **Target length: 2,100 words of prose.** Per-section budgets below sum to exactly 2,100.
- **Table cell text does not count** toward the budget. Neither does the author bio.
- Reading time: 8 to 9 minutes

### Hard writing constraints (from MUST-FOLLOW-RULES 4b and 7)

- **Maximum 3 sentences per paragraph.** Every paragraph, including summary, intro, PAA answers, FAQ answers and conclusion.
- **Maximum 20 words per sentence.** Article average must stay at or under 18.
- **First sentence of every H2 section must directly answer that H2's question.** No context-setting, no background, no caveats before the answer. This is the single highest-value rule in the file.
- Sentence case headings throughout. No em dashes in any of the four forms. No banned hype or filler words.
- Second person, active voice, contractions fine.

---

## Structure and per-section word budgets

Total: **2,100 words.**

### H1

**Locked: "The August 2026 Magento support cliff: your four honest options"**

The coordinator's supplied title, "The August 2026 Magento Support Cliff: Upgrade, Move, or Replatform", names three options while the article delivers four. It is retained as an acceptable fallback only if the coordinator prefers it, but it undersells the fourth path, which is the piece no competitor has. Sentence case either way.

### Summary block (Template A) — **80 words**

States the outcome up front: your version fell out of support on 11 August 2026, your store still works, Adobe says your version is no longer PCI compliant, and for most readers the right move is an upgrade to a supported 2.4.x rather than a replatform. Name the four paths in one sentence. No links.

### Introduction block (Template B) — **120 words**, two paragraphs

Paragraph 1: the concrete scene. Two things happened on 11 August 2026 and most merchants only noticed one. 2.4.6 exited regular support and 2.4.5 exited extended support on the same day.

Paragraph 2: the promise and the disclosure. This walks four paths in order of how little each one benefits Virtina, and says so plainly. **No internal links in the introduction.**

### Table of contents (Template C) — not counted

H3 heading "Table of Contents". Inline SVG arrow, `fill:#43627f`. Links `#00a0e2` with `!important` and **no space before `!important`**. 12 entries, one per body H2 plus `#people-also-ask`, `#conclusion`, `#faq`. Place directly after the Introduction div, before the first body section div. Use `clients/virtina/reference/toc-working-template.html` verbatim. Never Thrive `tcb-styled-list` markup.

---

### Section 1 — H2: "What changed for Magento on 11 August 2026?" — id `what-changed-august-2026` — **165 words**

**Direct-answer first sentence:** on 11 August 2026 Adobe stopped issuing quality fixes and security patches for the 2.4.6 line, and 2.4.5 left its final phase of ordinary coverage on the same day.

- **H3: "Which Magento versions are still supported?"** Holds **Table 1**. Name the next cliff explicitly: 31 May 2027 for 2.4.7.
- **H3: "What Adobe stops doing after the end-of-support date"** Your store keeps running and the licence stays valid. Tickets raised after the date are not resolved. No further product changes, including security and PCI compliance changes. Community pull requests are no longer merged. Patching and PCI re-certification become yours.

**Do not include:** any claim that the store shuts down, any "% of stores still unsupported" figure, the "501 issues fixed" numbers, or the March 2026 date.

### Section 2 — H2: "Are you out of PCI compliance now?" — id `pci-compliance` — **170 words**

**This is the article's strongest section and the one no competitor has. Handle the framing exactly.**

**Direct-answer first sentence:** Adobe says yes, and that is Adobe's published position on its own software.

- **H3: "What Adobe states about unsupported versions"** Adobe's end-of-support FAQ states that a version that is no longer supported is no longer PCI compliant, and that the merchant becomes subject to fines, loss of card processing, or other penalties. Quote under 15 words. Attribute in the sentence as Adobe's own end-of-support FAQ, checked 10 September 2026. **Adobe is named in plain text, never linked.**
- **H3: "Why your acquiring bank and QSA decide this"** The practical consequence does not run through Adobe. It runs through your acquiring bank and your qualified security assessor. Tell the reader to confirm their own position with their QSA before assuming either safety or catastrophe.

**Never assert a specific PCI DSS requirement number as the mechanism.** The PCI SSC document was not fetched, so no clause can be named. Do not write "PCI DSS requirement 6.x" or any variant.

### Section 3 — H2: "Does your Magento edition change your deadline?" — id `edition-and-deadlines` — **125 words**

**Direct-answer first sentence:** possibly, and you need to confirm it yourself rather than take any agency's word for it, including ours.

- **H3: "What we could and could not verify about edition differences"** Adobe's published versions page lists the lifecycle dates without drawing a distinction between Adobe Commerce and Magento Open Source. Several agency articles assert that extended-support patches reach Adobe Commerce customers only. Virtina could not verify that split against Adobe's own documentation.

**Locked instruction to the creator: do not assert an edition split in either direction.** Say what Adobe's versions page shows, say that the split is claimed but unverified, and tell the reader to confirm their own edition's dates on Adobe's published versions page before planning around extended support. Then give the safe planning rule: if you cannot confirm you receive extended support, plan as though 11 August 2026 was your end date.

That last line is honest, useful, and does not require the split to be true.

### Section 4 — H2: "Which of the four paths fits your store?" — id `four-paths` — **130 words**

**Direct-answer first sentence:** four paths exist, and they are ordered below by how little each one earns Virtina.

Holds **Table 2**, the decision table. Then:

- **H3: "How to read this decision table"** One rule the reader can apply in thirty seconds: start at Path 1 and only move down when a row's "do not choose this if" column describes you.

### Section 5 — H2: "Path 1: upgrade to a supported 2.4.x release" — id `path-1-upgrade` — **240 words**

**Direct-answer first sentence:** for most readers this is the right answer, and it is the one that sells Virtina the least.

Who it is for: the install still fits the business, catalogue and pricing rules and ERP integration and multi-store all work, customisation is moderate, and the platform is not the reason growth stalled.

- **H3: "Should you target 2.4.8 or 2.4.9?"** Holds **Table 3**. The verdict, stated plainly: 2.4.9 buys one extra year but requires PHP 8.5, released 20 November 2025, so extension vendors have had roughly ten months to certify. 2.4.8 runs on PHP 8.4 or 8.3 where extension parity is far more likely to already exist. **A store with a heavy extension footprint should target 2.4.8 despite the earlier expiry.** No competitor makes this call.
- **H3: "What actually drives upgrade cost and effort"** No dollar table. See the cost rules below. Cover the six cost lines and the five effort drivers as prose plus one Template F bullet list.

Links here: `Magento version upgrade steps`, `Magento development services`.

### Section 6 — H2: "Path 2: move to Adobe Commerce Cloud" — id `path-2-cloud` — **90 words**

**Deliberately short. Under 200 words, so no H3 required.**

**Direct-answer first sentence:** this fits you only if you are already on Adobe Commerce licensing and infrastructure management is the actual pain.

**Hard constraint: zero figures, zero packaging detail, zero migration mechanics.** Adobe Commerce Cloud was not researched this pass. Describe the shape of the option in two or three sentences and tell the reader to price it directly with Adobe. Do not let a single sentence here come from competitor summaries. If the creator cannot write 90 honest words, write 60 and say the section is short because the pricing is not public.

### Section 7 — H2: "Path 3: replatform to a different eCommerce platform" — id `path-3-replatform` — **220 words**

**One section among four. Not the article.** Post 29601 owns Magento-to-WooCommerce migration including a verbatim H2 by that name, and 24 migration properties already exist. **This section must not become a migration how-to.** No migration steps, no data-mapping detail, no cutover checklist, no redirect strategy. Those belong to posts that already exist.

**Direct-answer first sentence:** leaving is right when the upgrade has stopped being a version bump and become a rebuild.

When leaving is genuinely right: every upgrade is a project rather than maintenance, run cost is dominated by keeping the platform alive rather than shipping features, you cannot staff it at a price you will pay, or your requirements genuinely simplified since you chose Magento.

- **H3: "Five store profiles that should stay on Magento"** Template F bullet list: complex B2B catalogues with company accounts and contract pricing and approval hierarchies; multi-store and multi-site hierarchies with no clean equivalent elsewhere; deep working ERP integration where the connector is the asset; very large or heavily attributed catalogues; and anyone mid-peak, because nobody should cut over between October and January. **Close with the blunt line: if two or more describe you, upgrade.**
- **H3: "Where merchants who do leave usually land"** Take a position rather than listing five destinations neutrally. Name WooCommerce for merchants whose requirements simplified and who want ownership of the stack. Say plainly that a destination decision made under deadline pressure is the most expensive kind.

Links here: `Adobe Commerce B2B features`, `Magento 2 multistore configuration`, `Magento ERP integration`, `eCommerce replatforming services`, `eCommerce platform selection`, and optionally `Magento vs WooCommerce comparison`.

### Section 8 — H2: "Path 4: document the risk and buy a quarter" — id `path-4-documented-risk` — **135 words**

**The path no competitor admits exists. It is what most readers will actually do.**

**Direct-answer first sentence:** if you cannot move before your next peak, the honest position is not that you are fine, it is that you write the risk down.

- **H3: "What a defensible risk acceptance contains"** Tell your acquirer and your QSA where you are. Apply the hardening you can at the WAF and infrastructure layer. Put a dated commitment in front of your board. Note that 2.4.6 stores sit better here than 2.4.5 stores, because 2.4.6 still carries published extended and security-provisioning dates while 2.4.5's last ordinary phase ended on 11 August 2026. **Close with: a documented, dated, temporary position is defensible. Silence is not.**

Link here: `Magento store security`.

### Section 9 — H2: "What should you check this week?" — id `check-this-week` — **115 words**

**Direct-answer first sentence:** five checks, all of which you can finish before Friday, decide which path you are on.

Template F bullet list, five items: confirm your exact version and edition; count installed third-party extensions; count store views and websites; list every live integration including ERP, PIM, tax and gateway; and check your current PHP version against your target version's requirement.

Then one closing line naming PHP 8.2's security-support end of 31 December 2026 as the second clock most readers have forgotten. php.net named in plain text, not linked.

Link here: `Virtina eCommerce team`. This is the only CTA link and it sits in a body section, not the conclusion, per section 6.

### People also ask (Template H) — id `people-also-ask` — **126 words**, 3 questions at ~42 words each

1. **Does Magento stop working after end of support?** No. Adobe confirms the software keeps running and the licence stays valid while your account is in good standing. What stops is patching, ticket resolution and further product changes.
2. **Is Magento 2.4.6 still safe to run in 2026?** Not indefinitely. Every vulnerability found after 11 August 2026 is patched on supported lines and left open on yours, and the public fix effectively documents the flaw.
3. **How long does a Magento version upgrade take?** Agencies typically quote 2 to 6 weeks for a straightforward version upgrade. Attribute that in the sentence as what agencies quote, never as fact. Effort scales with extension count, core overrides and store views.

### Conclusion (Template I) — id `conclusion` — **90 words**

White text on `#00d5c0`. Two short paragraphs.

Restate the decision, not the article. Most readers should upgrade to a supported 2.4.x and stay. Replatforming is right for a narrow, nameable profile. Documenting the risk is a legitimate temporary position and silence is not.

**No internal links in the conclusion.** No "in conclusion", no "to summarize". No new facts.

### FAQ (Template J) — id `faq` — **294 words**, 7 Q&As at ~42 words each

1. **When did Magento 2.4.6 lose support?** 11 August 2026, per Adobe's published release documentation. That is regular support. Do not repeat the March 2026 date that circulates in agency coverage.
2. **Do I have to replatform because there is no upgrade path?** No. Direct upgrades to supported 2.4.x lines exist. The "no upgrade path" framing comes from vendors who benefit when replatforming looks inevitable.
3. **Should I upgrade to Magento 2.4.8 or 2.4.9?** 2.4.8 if you carry a heavy extension footprint, 2.4.9 if you want the extra year and your extensions already certify on PHP 8.5.
4. **Does an unsupported version break PCI compliance?** Adobe's end-of-support FAQ states that an unsupported version is no longer PCI compliant. Confirm your own position with your QSA and your acquiring bank.
5. **Does Magento Open Source get the same extended support as Adobe Commerce?** Adobe's versions page lists the dates without drawing an edition split. Some agency coverage claims one. Confirm your edition's dates on Adobe's versions page.
6. **What PHP version does Magento 2.4.9 need?** PHP 8.5, per Adobe's system requirements. 2.4.8 accepts PHP 8.4 or 8.3.
7. **When does Magento 2.4.7 lose regular support?** 31 May 2027. If you are on 2.4.7 today, that is the deadline you should be budgeting against right now.

### Author bio (Template K) — not counted

Brand voice, no invented byline. If a real author name is not supplied, use Virtina's team voice.

---

## Tables

### Table 1 — Magento release lifecycle dates (Template N)

Sits inside Section 1, under the H3 "Which Magento versions are still supported?"

Columns: **Release line | Regular support ends | Extended support ends | Additional security fixes end**

| 2.4.9 | 31 May 2029 | Not published | Not published |
| 2.4.8 | 31 May 2028 | Not published | Not published |
| 2.4.7 | 31 May 2027 | 31 May 2028 | Not published |
| 2.4.6 | 11 August 2026 | 31 August 2027 | 31 May 2028 |
| 2.4.5 | 12 August 2025 | 11 August 2026 | 31 May 2027 |
| 2.4.4 | 12 April 2025 | 14 April 2026 | 31 May 2027 |

Use "Not published" in empty cells, never a dash and never an em dash.

**Caption (14px, `#6e6e6e`):** "Magento release lifecycle dates from Adobe's published release documentation, checked 10 September 2026. Confirm your own edition's dates on Adobe's versions page."

**Use 31 August 2027 for 2.4.6 extended support. Not 30 August.**

### Table 2 — The four paths (Template N)

Sits inside Section 4.

Columns: **Path | Choose this if | Do not choose this if**

1. **Upgrade to a supported 2.4.x** | the platform still fits and customisation is moderate | every upgrade has become a rebuild
2. **Adobe Commerce Cloud** | you are on Adobe Commerce licensing and infrastructure is the pain | you are on Open Source, or cost predictability matters more than managed infrastructure
3. **Replatform** | run cost is dominated by keeping Magento alive, or requirements genuinely simplified | you have complex B2B catalogues, multi-store, or deep ERP integration
4. **Document the risk, short term** | you cannot move before peak | you have no dated commitment to move afterwards

**Caption:** "Four responses to the August 2026 support cliff, ordered by how little each benefits Virtina."

### Table 3 — 2.4.8 vs 2.4.9 (Template N)

Sits inside Section 5, under the H3 "Should you target 2.4.8 or 2.4.9?". **No competitor in the ranking set has this table.** Keep it to six rows.

Columns: **Requirement | 2.4.8 | 2.4.9**

- Regular support ends | 31 May 2028 | 31 May 2029
- PHP | 8.4 or 8.3 | 8.5
- MariaDB | 11.4 or 11.8 | 12.3 recommended, 11.8 supported
- MySQL | 8.4 | 8.4
- OpenSearch | 3 | 3
- Valkey | 8.1 | 9

**Caption:** "Adobe's published system requirements for 2.4.8 and 2.4.9, checked 10 September 2026."

---

## Cost handling: no dollar table, no exceptions

Adobe publishes no Adobe Commerce licence pricing. The two sourced upgrade ranges conflict by roughly 10x for nominally the same work ($5K to $30K versus EUR 50K to EUR 150K), and neither is attributed in its original. **Publish cost structure and effort drivers instead of amounts.**

**Six cost lines to name as prose plus a bullet list:**
extension re-certification, which scales with extension count and not revenue; custom module remediation, which scales with how far you forked core; theme and frontend rework, which is where PHP version jumps bite; integration re-testing across ERP, PIM, tax and gateway; infrastructure changes the target version requires, which Table 3 makes concrete; and QA and UAT, which most quotes under-scope.

**Five effort drivers to give the reader:** installed extension count, core override count, store view count, live integration count, and PHP version distance to target. A reader can price that against their own agency's day rate.

**The single permitted duration figure:** "2 to 6 weeks for a straightforward version upgrade", used only in the PAA, and only with the in-sentence health warning that this is what agencies typically quote rather than a verified fact. No other figure of any kind.

---

## Claims requiring inline attribution

Every row below must carry its attribution **in the sentence that makes the claim**, not in a footnote. Adobe and php.net are named in plain text only. **Zero external links in this article.**

| # | Claim | Required inline framing | Source to name | Date to state or check |
|---|---|---|---|---|
| 1 | 2.4.6 regular support ended 11 August 2026 | State as fact, sourced | Adobe's published release documentation | 11 August 2026 |
| 2 | 2.4.5 extended support ended 11 August 2026 | State as fact, sourced | Adobe's published release documentation | 11 August 2026 |
| 3 | 2.4.7 regular support ends 31 May 2027 | State as fact, sourced | Adobe's published release documentation | 31 May 2027 |
| 4 | 2.4.6 extended support ends 31 August 2027 | State as fact, sourced. **31, not 30** | Adobe's published release documentation | 31 August 2027 |
| 5 | Store keeps running, licence stays valid after EOS | State as fact, sourced | Adobe's end-of-support FAQ | checked 10 September 2026 |
| 6 | Tickets after EOS unresolved; no further product changes including security and PCI changes; community PRs not merged | State as fact, sourced | Adobe's end-of-support FAQ | checked 10 September 2026 |
| 7 | **An unsupported version is no longer PCI compliant, exposing the merchant to fines, loss of card processing or other penalties** | **Report as Adobe's statement about Adobe's own software. Attributed in the sentence. Quote under 15 words. Never assert a PCI DSS requirement number. Note the consequence runs through the acquiring bank and QSA, not Adobe. Tell the reader to confirm with their QSA.** | Adobe's end-of-support FAQ | checked 10 September 2026 |
| 8 | Three-year standard support window from GA | State as fact, sourced | Adobe's software lifecycle policy | page updated 19 August 2026 |
| 9 | Adobe does not patch third-party dependencies such as PHP and MySQL | State as fact, sourced. Useful and counterintuitive | Adobe's software lifecycle policy | page updated 19 August 2026 |
| 10 | The one-year extension is a one-time exception | State as fact, sourced | Adobe's software lifecycle policy | page updated 19 August 2026 |
| 11 | 2.4.9 requires PHP 8.5; 2.4.8 accepts 8.4 or 8.3; MariaDB and Valkey deltas | State as fact, sourced | Adobe's system requirements documentation | checked 10 September 2026 |
| 12 | PHP 8.5 released 20 November 2025 | State as fact, sourced | php.net | 20 November 2025 |
| 13 | PHP 8.2 security support ends 31 December 2026 | State as fact, sourced | php.net | 31 December 2026 |
| 14 | Edition split on extended support | **Do not assert in either direction.** State that Adobe's versions page draws no distinction, that some agency coverage claims one, that Virtina could not verify it, and that the reader should confirm their own edition's dates on Adobe's versions page | Adobe's versions page, plus an unnamed "some agency coverage" | checked 10 September 2026 |
| 15 | "2 to 6 weeks" upgrade duration | **Attributed and health-warned in the body sentence** as what agencies typically quote. PAA only | unnamed agency estimates | no date |
| 16 | Hosting and gateway support withdrawal | **Omit, or frame strictly as a check-with-your-provider risk.** Never as a stated fact | none verified | n/a |

---

## Must NOT include

- **"Three core framework components replaced" in 2.4.9.** Adobe confirms exactly one, the `carlos-mg89/oauth` library. Omit the claim entirely.
- **"501 issues", "560 issues", "500+ enhancements".** Secondary agency sources only.
- **Any percentage or count of Magento stores on unsupported versions.** Only unattributed agency numbers exist.
- **Any Adobe Commerce Cloud or ACCS pricing, packaging or migration mechanics.** Not researched.
- **Any cost figure not marked verified in the research Part 4**, which is all of them except the health-warned "2 to 6 weeks".
- **"2.4.6 support ended March 2026."** Wrong. Adobe says 11 August 2026.
- **"30 August 2027."** Use 31 August 2027.
- **Any named PCI DSS requirement clause.** The PCI SSC document was not fetched.
- **An assertion that Magento Open Source does or does not receive extended support.**
- **Any migration how-to content.** No data mapping, no cutover sequence, no redirect strategy, no SEO preservation checklist. Post 29601 and post 34921 own that ground and 24 migration properties already exist. This is a decision article.
- **Any link to adobe.com, magento.com, experienceleague.adobe.com, php.net, or any competitor domain.** Zero external links. All sources named in plain text.
- Em dashes in any form. Semicolons. Exclamation marks. Title Case headings.
- Banned words: revolutionary, game-changing, best-in-class, cutting-edge, transform your, delve, leverage, navigate as a verb, realm, landscape, ecosystem, "in today's fast-paced world", "it's important to note", "in conclusion".

---

## Internal links: 10 maximum, body sections only

All URLs below were verified HTTP 200 today with redirects **not** followed. **The publisher must re-verify every one before push.** Anchors are clean noun phrases, no leading article, no gerund verb, no repeats.

**Nine locked, one recommended. Five of the ten are earlier blog posts, which clears the two-post minimum.**

| # | URL | Exact anchor | Placement | Type |
|---|---|---|---|---|
| 1 | `https://virtina.com/upgrade-magento-version-step-by-step-guide/` | Magento version upgrade steps | Section 5, Path 1 opening | post |
| 2 | `https://virtina.com/platforms/magento-development-services/` | Magento development services | Section 5, H3 on cost and effort | service |
| 3 | `https://virtina.com/adobe-commerce-b2b-features/` | Adobe Commerce B2B features | Section 7, H3 stay-profile 1 | post |
| 4 | `https://virtina.com/magento-2-multistore-configuration/` | Magento 2 multistore configuration | Section 7, H3 stay-profile 2 | post |
| 5 | `https://virtina.com/magento-erp-integration/` | Magento ERP integration | Section 7, H3 stay-profile 3 | post |
| 6 | `https://virtina.com/ecommerce-replatform/` | eCommerce replatforming services | Section 7 body | service |
| 7 | `https://virtina.com/ecommerce-platform-selection/` | eCommerce platform selection | Section 7, H3 on destinations | service |
| 8 | `https://virtina.com/magento-security-tips/` | Magento store security | Section 8, on WAF and hardening | post |
| 9 | `https://virtina.com/get-in-touch/` | Virtina eCommerce team | Section 9, closing line | service |
| 10 | `https://virtina.com/magento-vs-woocommerce/` | Magento vs WooCommerce comparison | Section 7, H3 on destinations | post (recommended) |

**Fallbacks if any of the above fails re-verification, to keep the count at 5 minimum:**
`https://virtina.com/platforms/woocommerce-development-services/` anchored "WooCommerce development company"; `https://virtina.com/migrate-from-magento-1-to-magento-2/` anchored "Magento 1 to 2 migration"; `https://virtina.com/ecommerce-integration/` anchored "eCommerce integration services"; `https://virtina.com/future-proof-ecommerce-magento-2025/` anchored "future-proof Magento guide".

**Deliberately excluded:** `https://virtina.com/magento-migration-services/`. It resolves 200 but sells migration **to** Magento. Linking it from the replatform section would mislead the reader.

**All internal links use Template L:** `<a href="..." style="outline: none;">anchor</a>`. No `target`, no `rel`. **None in the introduction. None in the conclusion.**

---

## Semantic terms: 15 required (section 4b)

The creator confirms coverage in the draft. All belong naturally in this topic and none should be stuffed.

1. end of support (EOS)
2. end of life (EOL)
3. release line
4. extended support
5. security patch
6. quality fix
7. PCI DSS compliance
8. qualified security assessor (QSA)
9. acquiring bank
10. Adobe Commerce Cloud
11. Magento Open Source
12. extension compatibility
13. core overrides
14. total cost of ownership
15. staging environment and rollback plan

---

## Images (section 3)

- **1 featured image at exactly 1309×500.** Suggested query: `business meeting whiteboard` or `team strategy planning office`. Alt text 80 to 150 chars including "Magento" and "end of support" naturally.
- **2 body images at exactly 670×352.** Placement: one after Section 2 (PCI), one after Section 5 (Path 1). A third after Section 7 is optional.
- Suggested queries: `office team meeting computers`, `coworkers office computer work`, `macbook desk business work`.
- **Visual QA is mandatory before selection.** Keyword search alone has produced rejected stock twice on this account. No nature, no landscapes, no building exteriors, no old computers.
- Every `src` must begin with `https://virtina.com/wp-content/uploads/`. `featured_media` must be a real media ID, never 0.

---

## Yoast

- **SEO title (54 chars):** `Magento 2.4.6 End of Support: Your 4 Options | Virtina`
- **Meta description (152 chars):** `Adobe ended regular support for Magento 2.4.6 on 11 August 2026. Compare four honest paths: upgrade to 2.4.8, Adobe Commerce Cloud, replatform, or wait.`
- **Focus keyword:** Magento end of support 2026
- **Category:** Magento. **Status: draft.**

---

## Open questions for the creator

These are the creator's calls. Everything else in this brief is locked.

- The exact opening scene in the introduction. A dated fact or a merchant-at-their-desk moment both work. Do not use a statistic.
- Whether Section 6 (Adobe Commerce Cloud) runs 60 or 90 words. Shorter and honest beats padded.
- Whether the tenth link (`magento-vs-woocommerce`) earns its place in Section 7 without pulling the section toward a comparison. Drop it if it does.
- Ordering within the five stay-on-Magento profiles.

## Escalate before drafting if

- Any of the ten internal URLs fails re-verification at 200 with redirects not followed.
- The creator wants to state the edition split. Do not. Escalate instead.
- The creator cannot hit a section's word budget without padding. Report the shortfall rather than filling it with competitor-sourced content.
