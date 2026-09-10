---
title: Research notes — The August 2026 Magento version support cliff
client: virtina
date: 2026-09-10
topic: Magento / Adobe Commerce end of support, and the upgrade vs replatform decision
audience: B2B eCommerce leaders on Magento Open Source or Adobe Commerce
stage: research
slug: magento-version-support-cliff-2026
format: D (decision-tree / playbook)
uniqueness_audit: uniqueness-audit-2026-09-10.md
competitor_analysis: competitor-analysis-2026-09-10.md
---

# Research: the August 2026 Magento version support cliff

## Sub-questions a reader actually wants answered

1. My Magento version fell out of support on 11 August 2026. What literally changed that day?
2. Am I actually non-compliant now, or is that agency scare copy?
3. Is upgrading to a supported 2.4.x enough, or am I just buying two more years?
4. What does the upgrade cost and how long does it take for a store my size?
5. Under what conditions is leaving Magento the right answer, and under what conditions is it a mistake?

---

## Part 1 — The lifecycle facts, precisely dated

**Every date below is fetched from Adobe Experience League on 2026-09-10 and is Adobe-sourced.** These are the load-bearing facts of the article. Nothing here is secondary.

### The supported-version table as it stands today

| Release line | GA date | Regular support ends | Extended support ends | Additional security provisioning ends |
|---|---|---|---|---|
| 2.4.9 | 12 May 2026 | 31 May 2029 | — | — |
| 2.4.8 | 8 April 2025 | 31 May 2028 | — | — |
| 2.4.7 | 9 April 2024 | **31 May 2027** | 31 May 2028 | — |
| 2.4.6 | 14 March 2023 | **11 August 2026** | 31 August 2027 | 31 May 2028 |
| 2.4.5 | 9 August 2022 | 12 August 2025 | **11 August 2026** | 31 May 2027 |
| 2.4.4 | 12 April 2022 | 12 April 2025 | 14 April 2026 | 31 May 2027 |

Source: [Released versions](https://experienceleague.adobe.com/en/docs/commerce-operations/release/versions) — Adobe Experience League, fetched 2026-09-10.

**The 11 August 2026 double event is the news hook.** Two things happened on the same day, one month ago:
- 2.4.6 exited **regular** support.
- 2.4.5 exited **extended** support, which was its last phase of ordinary coverage.

**The next cliff is 31 May 2027, when 2.4.7 exits regular support.** That is the deadline a reader on 2.4.7 should be planning against right now.

### What "end of support" does and does not mean

This is where most competitor coverage is vague and where Virtina can be precise. Adobe states it directly.

**Does not mean:** your store stops working. Adobe's own end-of-support FAQ confirms the software does not shut down and the licence remains valid while the account is in good standing. Orders keep processing.

**Does mean, per Adobe:**
- Adobe stops issuing quality fixes and security patches for that version.
- Support tickets submitted after the end-of-support date will not be resolved. Tickets opened before it continue.
- No further product changes are made, including security and PCI compliance changes.
- Community pull requests are no longer accepted or merged.
- Responsibility for security patching and PCI re-certification transfers to the merchant.

Source: [Adobe Commerce Software End of Support FAQ](https://experienceleague.adobe.com/en/docs/support-resources/adobe-support-tools-guide/adobe-commerce-support/adobe-commerce-eos-policy-faq) — Adobe Experience League, fetched 2026-09-10.

### The support-window policy itself

Adobe's lifecycle policy (page last updated 19 August 2026) sets a **three-year standard support window from each version's GA date**. Standard support covers quality fixes, security patches, and on-call support.

Two further points from the same page matter and are frequently missed:

- **Adobe does not patch your third-party dependencies.** The policy states explicitly that Adobe does not provide security and quality fixes for third-party services and software dependencies such as PHP and MySQL, even while your Magento version is in support. That burden was always yours.
- **The extension is one-time.** Adobe describes one year of additional support at no extra cost for 2.4.6 and 2.4.7, and states the security-only transitional period is a one-time exception that will not be extended beyond published dates.

Source: [Software lifecycle policy](https://experienceleague.adobe.com/en/docs/commerce-operations/release/planning/lifecycle-policy) — Adobe Experience League, last updated 19 August 2026, fetched 2026-09-10.

---

## Part 2 — What running an unsupported Magento actually exposes you to

Four distinct exposures. Keep them separate in the draft, because they have different severities and different remedies.

### 2a. Security patching stops, permanently, for your version

Every vulnerability found after your end-of-support date is fixed on supported lines and left open on yours. This is not a risk that decays. It compounds, because the fix for supported versions is public and effectively documents the vulnerability.

Adobe-sourced. No embellishment needed and none should be added.

### 2b. PCI — the one hard, citable consequence

**This is the strongest fact in the entire research set and no competitor surfaces it.**

Adobe's own end-of-support FAQ states that once a version is no longer supported, that version is no longer PCI compliant, and that the merchant becomes subject to fines, removal of card processing ability, or other penalties.

That is Adobe stating it about Adobe's own software. It can be reported as Adobe's position, quoted under 15 words, and attributed. Source: the EOS FAQ linked above.

**What must NOT be claimed:** do not assert a specific PCI DSS requirement number as the mechanism. I did not fetch the PCI Security Standards Council document, so I cannot verify which named requirement of PCI DSS v4.x is breached, or on what timetable an acquirer would act. The competitor set routes this through PHP end-of-life rather than the standard itself, which suggests they could not verify it either.

**Recommended framing for the creator:** report Adobe's statement as Adobe's statement, note that the practical consequence runs through the merchant's acquiring bank and QSA rather than through Adobe, and tell the reader to confirm their own position with their QSA. Under section 4c's honesty rule that is more defensible than implying a specific standards clause we have not read.

### 2c. PHP and dependency drift

This is where the timeline gets genuinely uncomfortable, and it is verifiable.

| PHP branch | Active support until | Security support until |
|---|---|---|
| 8.2 | 31 Dec 2024 | **31 Dec 2026** |
| 8.3 | 31 Dec 2025 | 31 Dec 2027 |
| 8.4 | 31 Dec 2026 | 31 Dec 2028 |
| 8.5 | 31 Dec 2027 | 31 Dec 2029 |

Source: [Supported Versions](https://www.php.net/supported-versions.php) — php.net, fetched 2026-09-10.

**PHP 8.2 loses even security support on 31 December 2026, sixteen weeks from now.** A store sitting on an out-of-support Magento version running PHP 8.2 has two independent clocks expiring within five months of each other, and Adobe has already said it does not patch PHP for you.

### 2d. Hosting and gateway support can be withdrawn

Both are plausible and both are commonly asserted by competitors. **I could not verify either against a named provider's published policy in this research pass.** Treat as [unverified]. If the creator wants this point, it must be framed as a risk to check with your own host and gateway, not as a stated fact, or a specific provider's published deprecation notice must be sourced first.

---

## Part 3 — The real choice this forces

Frame as four paths, not three. The fourth exists in practice and pretending otherwise is dishonest.

### Path 1 — Upgrade to a supported 2.4.x. **This is the right answer for most readers.**

Lead with this. It is the path that sells Virtina the least, which is exactly why leading with it earns the read.

**Who this is for:** your Magento install still fits the business. Your catalogue, pricing rules, ERP integration and multi-store setup work. Your customisation is moderate. You have a functioning dev relationship. The platform is not the reason growth stalled.

**The 2.4.8 vs 2.4.9 choice**, which no competitor lays out properly:

| | 2.4.8 | 2.4.9 |
|---|---|---|
| GA | 8 April 2025 | 12 May 2026 |
| Regular support ends | 31 May 2028 | 31 May 2029 |
| PHP | 8.4, 8.3 | 8.5 |
| MariaDB | 11.4, 11.8 | 12.3 recommended, 11.8 |
| MySQL | 8.4 | 8.4 |
| OpenSearch | 3 | 3 |
| Valkey | 8.1 | 9 |
| RabbitMQ | 4.3 | 4.3 |
| Varnish | 8 | 8 |
| Composer | 2.10 | 2.10 |
| nginx | 1.30 | 1.30 |

Source: [System requirements](https://experienceleague.adobe.com/en/docs/commerce-operations/installation-guide/system-requirements) — Adobe Experience League, fetched 2026-09-10. Adobe-sourced.

**The decision this table drives:** 2.4.9 gives you one extra year of support but requires PHP 8.5, which was released 20 November 2025. Your extension vendors have had roughly ten months to certify against it. 2.4.8 runs on PHP 8.4 or 8.3, where extension parity is far more likely to already exist. For a store with a heavy extension footprint, 2.4.8 is usually the lower-risk target even though it expires a year sooner. Say that plainly.

### Path 2 — Move to Adobe Commerce Cloud

**Who this is for:** you are already on Adobe Commerce licensing, infrastructure management is the actual pain, and you want Adobe to own the stack.

**Research gap, stated honestly:** I did not verify Adobe Commerce Cloud or Adobe Commerce as a Cloud Service pricing, packaging, or migration mechanics against Adobe's own documentation in this pass. Two competitors reference ACCS; my earlier search for an "Adobe Commerce Optimizer" announcement returned nothing confirmable. **The analyzer should either commission a second research pass on ACCS specifically, or keep this path deliberately short and descriptive with no figures.** Do not let the creator fill this section from competitor summaries.

### Path 3 — Replatform. Proportionate, honest, and NOT the whole article.

This is the bridge to Virtina's commercial intent and it must stay one section among four.

**When leaving is genuinely right:**
- The upgrade is not a version bump but a rebuild. Your customisation is deep enough that every upgrade has become a project rather than a maintenance task.
- Your Magento total run cost is dominated by keeping the platform alive rather than by shipping features.
- You cannot staff it. Your agency relationship has failed and replacing it is hard at a price you will pay.
- Your requirements have genuinely simplified since you chose Magento. Many merchants bought enterprise complexity they never used.

**When leaving is a mistake, and say this plainly (section 4c honesty rule):**
- **Complex B2B catalogues.** Company accounts, contract pricing, requisition lists and approval hierarchies are native in Adobe Commerce B2B. Rebuilding them elsewhere is a real project, not a migration.
- **Multi-store and multi-site.** Magento's website / store / store-view hierarchy has no clean one-to-one equivalent on most alternatives. Multi-store is the single most common reason a replatform overruns.
- **Deep ERP integration.** If a working, tested ERP connector is carrying your order and inventory flow, that integration is the asset, not the storefront. Moving platforms means rebuilding and re-testing it.
- **Very large or highly attributed catalogues.** Configurable products with many attribute combinations, and catalogues where attribute-set structure carries business meaning, do not map cleanly.
- **You are mid-peak.** Nobody should cut over a store between October and January.

**Blunt version for the draft:** if two or more of those five describe you, upgrade. The migration will cost more than the upgrade and deliver less than the pitch.

### Path 4 — Documented risk acceptance, short term

The path every merchant actually takes for at least a quarter and no competitor admits exists.

If you cannot move before your next peak, the honest position is not "you are fine". It is: write the risk down, tell your acquirer and your QSA where you are, apply what hardening you can at the WAF and infrastructure layer, and put a dated commitment in front of your board. That is a defensible temporary position. Silence is not.

Note that 2.4.6 stores are better placed here than 2.4.5 stores, because 2.4.6 still has extended support to 31 August 2027 and security provisioning to 31 May 2028, whereas 2.4.5's last phase ended on 11 August 2026.

---

## Part 4 — Cost and effort by store size

**This section carries the highest factual risk in the article. Read the flags before using any number.**

### What I could verify

Nothing. **No cost figure in this research is traceable to a primary source.** Adobe does not publish Adobe Commerce licence pricing; it is quote-based and scales with GMV. No vendor publishes upgrade pricing. Every figure below comes from agency marketing content.

### What competitors published, with attribution and health warnings

| Figure | Value | Source | Status |
|---|---|---|---|
| Typical upgrade duration | 2 to 6 weeks | Codilar; Webgarh (independently) | [unverified] Two independent agency sources agree. Weakest usable claim. |
| Migration duration | 6 to 12 weeks | Webgarh | [unverified] Single source. |
| Upgrade cost | $5K to $30K | Webgarh | [unverified] Single source, Shopify partner, unattributed in original. |
| Shopify migration cost | $10K to $75K | Webgarh | [unverified] Single source with a direct commercial interest in the number. |
| Magento 2.4.8 upgrade cost | EUR 50K to 150K | Search summary of djust.io | [unverified] Order of magnitude conflicts with Webgarh above. |
| Replatform to composable B2B, year 1 | EUR 100K to 350K | Search summary of djust.io | [unverified] Vendor with a direct interest. |
| Magento store count decline | 162K to 112K, 2021 to 2026 | Webgarh | **[unverified] Unattributed in the original. Do not reuse.** |
| Shopify TCO advantage | 30% to 55% lower | Webgarh | **[unverified] Unattributed in the original. Do not reuse.** |

**There is a direct factual conflict on cost.** Webgarh puts a Magento upgrade at $5K to $30K. The djust.io figure is EUR 50K to 150K. Those differ by roughly an order of magnitude and both are unsourced. **Unresolved.** They are probably measuring different things (a patch-level version bump versus a full re-implementation on a supported version) but neither says so.

### Recommendation to the analyzer

**Do not publish a cost table of dollar ranges.** It cannot be sourced, the sources conflict by 10x, and Virtina's rules forbid inventing statistics.

Publish **cost structure** instead, which is defensible without a single invented number:
- Extension re-certification, which scales with extension count, not revenue.
- Custom module remediation, which scales with how far you forked core.
- Theme and frontend rework, which is where PHP version jumps bite.
- Integration re-testing, ERP and PIM and tax and gateway.
- Infrastructure changes required by the target version, which the Adobe system requirements table above makes concrete and verifiable.
- QA and UAT, which most quotes under-scope.

Then give **effort drivers** rather than prices: number of installed extensions, number of core overrides, number of store views, number of live integrations, PHP version distance to target. A reader can price that against their own agency's day rate. That is more useful than a fabricated range and it is honest.

The only duration claim I would let through is "2 to 6 weeks for a straightforward version upgrade", attributed in-copy as what agencies typically quote, never as fact.

---

## Part 5 — Facts discipline ledger

Per the coordinator's instruction, here is exactly what is Adobe-sourced and what is not.

### Adobe-sourced, safe to state as fact (all fetched 2026-09-10)

- All six release lines' GA, regular, extended and security dates (Released versions page).
- Three-year standard support window from GA; standard support includes quality fixes, security patches, on-call support (Lifecycle policy, updated 19 Aug 2026).
- Adobe does not patch third-party dependencies such as PHP and MySQL (Lifecycle policy).
- The one-year extension for 2.4.6 and 2.4.7 at no additional cost, and that the security-only transitional period is a one-time exception (Lifecycle policy).
- Store keeps running after EOS; licence stays valid; tickets after EOS unresolved; no further security or PCI compliance changes; community PRs no longer merged; merchant assumes patching and PCI re-certification (EOS FAQ).
- Adobe's statement that an unsupported version is no longer PCI compliant (EOS FAQ).
- Full system requirements per version for 2.4.7, 2.4.8, 2.4.9 (System requirements page).
- 2.4.9 release note items: Symfony dependencies in `magento/composer` moved to Symfony LTS 7.4; official support added for Symfony 7.4 LTS and PHP 8.5; Composer support extended from 2.2.x to 2.4.x; the `carlos-mg89/oauth` library replaced with native PHP OAuth functions; `clearCart` GraphQL mutation opened to all Open Source users (2.4.9 release notes).

### Verified from another primary source

- PHP branch support dates, including PHP 8.2 security support ending 31 December 2026 (php.net, fetched 2026-09-10). Primary, not Adobe.

### RESOLVED since the audit

The claim I previously flagged as secondary-source-only, that 2.4.9 raises requirements across PHP, database, search and caching, **is now verified** against Adobe's own system requirements page. 2.4.9 requires PHP 8.5 where 2.4.8 takes 8.4 or 8.3; MariaDB moves to 12.3 recommended; Valkey moves from 8.1 to 9. Use the table in Part 3, not the competitor phrasing.

### DO NOT PUBLISH — still unverified

- **"Three core framework components were replaced" in 2.4.9.** Adobe's release notes confirm exactly one such replacement, the `carlos-mg89/oauth` library. **Omit the claim.**
- **"501 issues fixed in Open Source, 560 in Adobe Commerce" and "500+ enhancements."** Secondary agency sources only, not confirmed against Adobe. Omit.
- **"Magento Open Source does not receive the extended support that Adobe Commerce receives on 2.4.6."** This appears in agency coverage and would materially change the advice for Open Source readers. I fetched the Magento Open Source release-notes overview and it states no support dates and draws no distinction. **Unresolved and important.** Either verify against Adobe before drafting, or write the article without asserting an edition split and tell readers to confirm their own edition's dates on Adobe's versions page.
- **"2.4.6 support ended March 2026."** One search result asserted this. It contradicts Adobe's own versions page, which says 11 August 2026. **Adobe wins. Ignore the March date.**
- **Adobe's extended support end for 2.4.6: 30 vs 31 August 2027.** A competitor said 30 August; Adobe's page says 31 August. Use 31 August 2027.
- **Hosting providers and payment gateways dropping support for old stacks.** Plausible, uncited. Frame as a check-with-your-provider risk or omit.
- **Every cost figure in Part 4.** See the table there.
- **Any Adobe Commerce Cloud / ACCS pricing, packaging or mechanics.** Not researched. See Path 2.
- **Any "% of Magento stores still on unsupported versions" figure.** I looked and found only unattributed agency numbers. Do not use one.

---

## Conflicts between sources

- **2.4.6 end-of-support date.** Position A (one search result): March 2026. Position B (Adobe Released versions): 11 August 2026. **Adobe is authoritative. B.**
- **Upgrade cost.** Position A (Webgarh): $5K to $30K. Position B (djust.io): EUR 50K to 150K. **Unresolved, roughly 10x apart, both unsourced. Publish neither.**
- **Does an upgrade path exist at all?** Position A (SyncSpider): "no upgrade path without replatforming." Position B (Adobe, Codilar, The Commerce Shop, Webgarh): direct upgrades to supported 2.4.x lines are supported. **B is correct. A is a vendor framing device.**
- **Whether extended support covers Magento Open Source.** Position A (several agencies): Open Source gets nothing after 11 Aug 2026, Commerce gets extended support. Position B: Adobe's versions page lists extended dates without an edition split. **Unresolved. Flagged above as the single most important open question.**

---

## The gap

> Every article ranking for this deadline was written by someone who sells the outcome they recommend. Magento agencies conclude "upgrade." Shopify partners conclude "Shopify." SaaS vendors conclude "SaaS." Not one of the five leads with the answer that earns them nothing, which for most readers is: upgrade to 2.4.8 and stay. And not one surfaces Adobe's own flat statement that an unsupported version is no longer PCI compliant, which is the single most consequential and most citable fact about the whole event.

## Recommended angle

> One month after the 11 August cliff, walk the reader through four honest paths in order of how little they benefit Virtina, lead with "most of you should upgrade to 2.4.8 and stay," name the five store profiles for whom replatforming is a mistake, and ground every date in Adobe's own documentation rather than agency estimates.

---

## Semantic term list (section 4b, 10 to 15 terms)

The creator must confirm coverage in the draft. All belong naturally in this topic:

1. end of support (EOS)
2. end of life (EOL)
3. release line
4. extended support
5. security patch
6. quality fix
7. PCI DSS compliance
8. qualified security assessor (QSA)
9. acquiring bank
10. Adobe Commerce Cloud / ACCS
11. Magento Open Source
12. extension compatibility
13. core overrides / customisation debt
14. composable commerce
15. total cost of ownership
16. staging environment / rollback plan

## Mandatory content elements (section 4b)

Format D is a decision guide, and it is also a comparison. Required:
- **Comparison table** (Template N): 2.4.8 vs 2.4.9, built from the Adobe system requirements table in Part 3.
- **Checklist**: the "what to do this week" audit list (confirm your version and edition, count extensions, count store views, list live integrations, check your PHP version against the target).
- **FAQ**: 6 to 8 Q&As (Template J).
- **Supported-version table** from Part 1, which doubles as the article's most linkable asset.

---

## Proposed internal links

5 to 10 required, body prose only, anchors 2 to 5 words, clean noun phrases, no repeats. **None of these are on the section 6 verified-dead list.** The `/platforms/` form is used for WooCommerce. **The publisher must verify all of these live with redirects NOT followed; I have not verified them.**

**Earlier blog posts (new standing rule: minimum 2 — five proposed here):**

| Target | Suggested anchor | Why it fits |
|---|---|---|
| `/upgrade-magento-version-step-by-step-guide/` (37127) | Magento version upgrade steps | The mechanical how-to that Path 1 should hand off to. Most natural link in the article. |
| `/magento-security-tips/` (38040) | Magento store security | Belongs in Path 4, hardening while you wait. |
| `/magento-erp-integration/` (37600) | Magento ERP integration | Belongs in the "when leaving is a mistake" list, on the ERP point. |
| `/magento-2-multistore-configuration/` (38255) | Magento 2 multistore setup | Same section, on the multi-store point. |
| `/adobe-commerce-b2b-features/` (38078) | Adobe Commerce B2B features | Same section, on the complex B2B catalogue point. |
| `/future-proof-ecommerce-magento-2025/` (39502) | future-proofing with Magento | Optional sixth. Supports Path 1 and shows Virtina is not anti-Magento. |

**Service and platform pages:**

| Target | Suggested anchor |
|---|---|
| `/platforms/magento-development-services/` | Magento development services |
| `/platforms/woocommerce-development-services/` | WooCommerce development company |
| `/ecommerce-replatform/` | eCommerce replatforming |
| `/ecommerce-platform-selection/` | eCommerce platform selection |
| `/get-in-touch/` | (conclusion CTA only, not a body link) |

**Deliberately NOT proposed:**
- `/ecommerce-migration-services/`, `/ecommerce-development-services/`, `/ecommerce-seo-services/`, `/contact/`, and the bare `/woocommerce-development-services/` — all on the section 6 verified-dead or redirect list.
- `/magento-migration-services/` (page 10738) — it sells migration **to** Magento and would confuse a reader in the replatform section.
- Anything from the migration cluster that would drag this post back toward the territory rejected in the audit.

**External links: 2 maximum.** Recommended pair, both Adobe primary sources, both `target="_blank" rel="noopener noreferrer"`:
1. Adobe Released versions page (the date table).
2. Adobe end-of-support FAQ (the PCI statement).

php.net is a strong third source but the cap is 2. Cite it in prose without a link.

---

## Format note for the analyzer

- **Format D (decision-tree / playbook) confirmed.** It is the correct fit: the reader walks a sequence of decisions, and section 11 names migration and platform-selection decisions as Format D's use case.
- **Format E is BLOCKED.** Used in 3 of the last 7 published posts (42491, 42465, 42428), which trips the section 11 recency rule.
- Format D was used once recently (42413), which is within tolerance.
- Formats C and F remain entirely unused recently if the analyzer prefers a different fit.

## Couldn't find

- **Adobe Commerce Cloud / ACCS pricing, packaging or migration mechanics.** Not researched this pass. Path 2 is thin as a result and must not be padded from competitor content.
- **Whether Magento Open Source receives the same extended support as Adobe Commerce on 2.4.6.** Adobe's pages I fetched do not draw the distinction; agencies assert one. This changes the advice for a large share of Virtina's readers and should be resolved before drafting.
- **Any verifiable cost figure for a Magento upgrade or replatform.** None exists in public primary sources. Adobe does not publish licence pricing.
- **Any verifiable count of stores still running unsupported Magento versions.** Only unattributed agency numbers found.
- **A named PCI DSS requirement clause** establishing the compliance mechanism. Adobe's own assertion is available and citable; the underlying standards clause is not, because I did not fetch the PCI SSC document.
- **A named hosting provider or payment gateway with a published deprecation policy** for old Magento stacks.

## Sources read

Primary:
- [Released versions](https://experienceleague.adobe.com/en/docs/commerce-operations/release/versions) — Adobe Experience League, fetched 2026-09-10. Primary.
- [Software lifecycle policy](https://experienceleague.adobe.com/en/docs/commerce-operations/release/planning/lifecycle-policy) — Adobe Experience League, updated 2026-08-19, fetched 2026-09-10. Primary.
- [Adobe Commerce Software End of Support FAQ](https://experienceleague.adobe.com/en/docs/support-resources/adobe-support-tools-guide/adobe-commerce-support/adobe-commerce-eos-policy-faq) — Adobe Experience League, fetched 2026-09-10. Primary.
- [System requirements](https://experienceleague.adobe.com/en/docs/commerce-operations/installation-guide/system-requirements) — Adobe Experience League, fetched 2026-09-10. Primary.
- [Magento Open Source 2.4.9 release notes](https://experienceleague.adobe.com/en/docs/commerce-operations/release/notes/magento-open-source/2-4-9) — Adobe Experience League, fetched 2026-09-10. Primary.
- [Magento Open Source release notes overview](https://experienceleague.adobe.com/en/docs/commerce-operations/release/notes/magento-open-source/overview) — Adobe Experience League, fetched 2026-09-10. Primary. Fetched specifically to test the edition-split question; it does not answer it.
- [PHP Supported Versions](https://www.php.net/supported-versions.php) — php.net, fetched 2026-09-10. Primary.

Secondary, competitor set, documented in `competitor-analysis-2026-09-10.md`, none linkable from the post:
- The Commerce Shop, ~4,500 words, fetched.
- Codilar, ~4,200 words, fetched.
- Webgarh, ~3,800 to 4,200 words, fetched.
- SyncSpider, ~3,500 words, fetched.
- Uncap — HTTP 403, not assessed.

Failed fetch:
- `https://experienceleague.adobe.com/en/docs/commerce-operations/release/lifecycle-policy` — HTTP 404. Correct path is under `/release/planning/lifecycle-policy`, which was fetched successfully.
