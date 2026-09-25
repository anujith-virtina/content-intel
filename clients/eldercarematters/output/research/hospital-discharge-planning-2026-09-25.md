---
title: Research notes — Hospital Discharge Planning: What to Do When a Parent Is Being Sent Home
client: eldercarematters
date: 2026-09-25
topic: Hospital discharge planning process and decisions for adult children
audience: Adult child, 45-65, working, parent has a discharge date 24-72 hours out
stage: research
slug: hospital-discharge-planning
---

# Research: Hospital Discharge Planning — What to Do When a Parent Is Being Sent Home

## MUST-FOLLOW-RULES and style files read

Read in full before research: `clients/eldercarematters/MUST-FOLLOW-RULES.md`, `style/voice.md`, `style/audience.md`, `style/brand.md`. Applying: Title Case headings, no Medicaid figures, no "Medicare covers assisted living/custodial care" claims, every dollar figure needs a named dated source, no invented statistics, approved-source list only, competitor exclusion list, `/nursing-homes/` and `/veterans-benefits/` link-anchor traps noted for the analyzer/creator.

## Uniqueness check (per orchestrator brief — reporting, not re-deriving)

Confirmed against the brief: ECM has 890 published posts. The only adjacent coverage is post 212662, `/medicare-observation-trap/`. I fetched this post directly. It is ~450-500 words, one plain heading ("WHAT IS THE MEDICARE OBSERVATION TRAP?"), no H2/H3 structure, published August 9, 2023, last modified January 23, 2025, byline Stephen J. Silverberg, Esq. It covers only: the definition of observation status, that observation time does not count toward Part A SNF eligibility, that hospitals choose observation for billing reasons, and a bare instruction to "request formal admission documentation." It does **not** cover: the discharge planning process, discharge rights or the Important Message from Medicare, the BFCC-QIO appeal, the 3-midnight rule mechanics or the 2026 waiver demonstration, the MOON notice, the Alexander v. Azar/Barrows appeal-rights rule, SNF Part A cost-sharing, home health eligibility, or the choice between post-acute settings. Plus two legacy Q&As from 2011 and 2013 (not fetched; described by the orchestrator as thin).

Conclusion: the new post should treat observation status as **one section only**, point to `/medicare-observation-trap/` for the deep dive on that narrow topic, and not re-explain what that post already covers. The new post's job is the process and the fork-in-the-road decision, not the billing-status trap.

## Sub-questions a reader in this situation would ask

1. What is the hospital actually required to do for my parent before sending them home, and what am I entitled to ask for?
2. If I think this is too soon, can I stop it, and how, before they're literally out the door?
3. Does it matter whether my parent was "admitted" or just "under observation," and does that change what happens next?
4. If my parent needs a rehab stay, will Medicare pay for it, and for how long?
5. If my parent goes home instead, what will Medicare home health actually do, and what will I have to arrange myself?
6. What are the actual questions I should be asking the discharge planner in the next hour?

## Key findings

### Finding 1: Federal discharge planning rules require hospitals to give patients real choices, not just a checklist

- Source: [CMS Final Rule on Discharge Planning Requirements](https://www.kutakrock.com/newspublications/publications/2019/10/cms-final-rule-on-discharge-planning-requirements) — Kutak Rock LLP legal summary of the CMS final rule, October 2019; corroborated by [Hall Render, "Discharge Planning: Key Takeaways from the Long-Awaited Final Rule"](https://hallrender.com/2019/10/02/discharge-planning-key-takeaways-from-the-long-awaited-final-rule/), October 2019, and [AAPC Knowledge Center](https://www.aapc.com/blog/48915-final-rule-revises-discharge-planning-requirements/).
- What it says: CMS finalized revised discharge planning Conditions of Participation for hospitals, critical access hospitals, and home health agencies on September 26, 2019, effective November 29, 2019. Hospitals must focus discharge planning on the patient's own goals and treatment preferences, involve the patient and caregiver as active partners, give the patient a list of Medicare-participating home health agencies, SNFs, inpatient rehab facilities, or long-term care hospitals serving the patient's area, and share relevant quality and resource-use data for those providers. Hospitals must tell the patient they are free to choose among participating providers and must not steer them, and must disclose any financial interest the hospital has in a referred provider.
- Why it matters: this is the direct, actionable fact for the reader — they can ask for this list and this choice by name, in the room, before discharge. This is the primary spine of the "what to do" section. **Note:** I could not verify the exact CFR citation (42 CFR 482.43) from a source I fetched directly; the legal-firm summaries state it is a CoP revision but I did not confirm the section number against the regulation text itself, since cms.gov and the Federal Register full text both blocked automated fetch. Treat the CFR pincite as `[unverified]` if used; the substance of the requirement is corroborated by three independent legal summaries of the same rule.

### Finding 2: The Important Message from Medicare is the reader's actual appeal trigger, and timing is exact

- Source: Synthesis of [Medicare.gov "Fast appeals"](https://www.medicare.gov/providers-services/claims-appeals-complaints/appeals/fast-appeals) (direct fetch returned HTTP 403 — known issue, could not be machine-verified directly) and [Medicare Interactive, "Original Medicare appeals if your care is ending"](https://www.medicareinteractive.org/understanding-medicare/denials-appeals/original-medicare-appeals/original-medicare-appeals-if-your-care-is-ending) (direct fetch also 403'd; content reflected in search synthesis), corroborated by [NRHP Reporting, "Important Message from Medicare (IM)"](https://data.nrhp.org/mandated_postings/important-message-from-medicare-im/).
- What it says: Medicare inpatients must receive the Important Message from Medicare (IMM) within 2 calendar days of admission, and a second copy no more than 2 days before, and no later than 4 hours before, discharge. If the family disagrees with the discharge, they can request a fast/expedited appeal to the area's BFCC-QIO by the day of discharge. Filing the appeal keeps the patient in the hospital while the BFCC-QIO decides, and Medicare states the patient will not be billed for that extra stay beyond normal coinsurance and deductibles. The BFCC-QIO is expected to call with a decision within 24 hours of getting the needed information.
- Why it matters: this is the single most concrete, time-boxed lever a family has. It should be a named, numbered step in the post: "ask for the Important Message from Medicare, then call the number on it." **Flag:** because both medicare.gov and medicareinteractive.org returned 403 to direct fetch, this is stated on Medicare's own site per the known 403 issue and corroborated by two independent secondary sources describing the same mechanics consistently (timing, no-bill-during-appeal, 24-hour QIO turnaround). Confidence is reasonably high because the two secondary descriptions agree in specific numeric detail, but flag as **[unverified by direct primary fetch]**.

### Finding 3: The 3-midnight inpatient rule for SNF coverage still applies to Original Medicare in 2026, with one narrow new carve-out

- Source: Search synthesis referencing [CMS two-midnight rule fact sheet](https://www.cms.gov/files/document/two-midnight-rule-fact-sheet.pdf) (direct fetch 403'd) and multiple secondary summaries including [Medical News Today](https://www.medicalnewstoday.com/articles/3-midnight-rule-medicare) and [Center for Medicare Advocacy, "Repeal the 3-Day Hospital Stay Requirement"](https://medicareadvocacy.org/repeal-the-3-day-hospital-stay-requirement-for-care-in-a-skilled-nursing-facility/).
- What it says: to qualify for Original Medicare Part A coverage of a skilled nursing facility stay, a patient generally still needs 3 consecutive midnights as a **formally admitted inpatient** — time spent under observation status does not count, no matter how many nights it lasts. Beginning January 1, 2026 and running through December 31, 2030, CMS is running a demonstration that waives the 3-day rule for beneficiaries having one of five specific surgical procedures. This is a narrow, procedure-specific carve-out, not a general repeal.
- Why it matters: this is exactly the fork the reader is standing at. I could not directly verify the CMS fact sheet PDF (403) or name the five surgical procedures in the 2026 demonstration from a source I fetched directly. **The 3-day rule's continued general applicability should be described in the body as the current rule, but the demonstration/waiver detail should either be omitted or described only in general terms ("a narrow surgical-procedure exception") since I could not verify which five procedures qualify from a primary source.**
- Note on Medicare Advantage: I found repeated secondary claims that Medicare Advantage plans "commonly waive" the 3-day rule, but no primary CMS or plan-level source confirming a general practice as opposed to plan-by-plan variation. **This claim is `[unverified]` and should not be stated as a fact.** Safer framing: Medicare Advantage plans set their own rules for SNF coverage, and the plan's own documents, not the 3-midnight rule, control.

### Finding 4: The MOON notice was updated in 2026 and is required for all outpatient observation stays over 24 hours

- Source: [Center for Medicare Advocacy, "CMS Updates 'Moon' Notice"](https://medicareadvocacy.org/cms-updates-moon-notice/); corroborated by [Community Health Choice provider bulletin, March 13, 2026](https://provider.communityhealthchoice.org/wp-content/uploads/sites/2/2026/03/Release-of-the-Updated-Medicare-Outpatient-Observation-Notice-MOON.pdf) and [Wellcare provider bulletin](https://www.wellcare.com/en/providers/medicare-bulletins/cms-outpatient-observation-policy).
- What it says: CMS released an updated Medicare Outpatient Observation Notice (MOON), effective April 21, 2026, valid through February 28, 2029 (OMB control number CMS-10611 reauthorized). The updated version adds space for the hospital to explain why the patient is classified as outpatient rather than inpatient. Hospitals could use old stock through April 20, 2026.
- Why it matters: the MOON is the document that tells the family, in writing, "your parent is not admitted." That is the trigger to ask about the 3-midnight rule and to consider the existing observation-trap post. Confidence: reasonably high, corroborated by two independent provider-facing regulatory bulletins reporting the same effective date and control number, though neither is on the approved-source list; the underlying fact (CMS requires the MOON) is a CMS program (Beneficiary Notices Initiative) and is treated as sourced to CMS in the body.

### Finding 5: A 2024 final rule gives a narrow group of reclassified patients the right to appeal an observation determination — this is not a general observation-status appeal right

- Source: Search synthesis quoting Federal Register document 2024-23195, "Medicare Program: Appeal Rights for Certain Changes in Patient Status," 89 FR (October 15, 2024); corroborated by [Medicare Rights Center, "Final Rule Codifies Observation Stay Appeal Rights"](https://www.medicarerights.org/medicare-watch/2024/10/17/final-rule-codifies-observation-stay-appeal-rights) (direct fetch 403'd, content reflected via search) and by the case history in [Justice in Aging, Alexander v. Azar / Barrows v. Becerra summary](https://justiceinaging.org/alexander-v-azar-litigation/) (fetched directly).
- What it says: the rule implements a federal court order from Barrows v. Becerra (2d Cir. 2022), building on Alexander v. Azar (D. Conn. 2020). It applies only to beneficiaries who, on or after January 1, 2009, were **first formally admitted as a hospital inpatient**, then **reclassified by the hospital to outpatient observation** during the same stay, received a determination or MOON stating the observation time is not covered under Part A, and either were not enrolled in Part B at the time or stayed 3+ consecutive days but were designated inpatient for fewer than 3 of them. The rule took effect October 11, 2024; retrospective appeal procedures were targeted for January 1, 2025.
- Why it matters: this is a narrow, specific fact that a family should not over-read as "you can always appeal observation status." It only helps a defined group: those switched from inpatient to observation mid-stay. I could not confirm this eligibility language against the primary Federal Register/govinfo.gov PDF text directly (the PDF fetch failed to parse, and the live Federal Register page blocked automated access), so this is **corroborated by two independent secondary legal/advocacy summaries quoting matching eligibility language, but not independently verified against the raw regulation text I could read myself.** Flag as **[unverified against primary text; corroborated by two secondary legal sources]**. Recommend describing this narrowly and conservatively in the post, or omitting the case citations and simply saying "a federal rule now lets some patients whose status was changed from inpatient to observation mid-stay appeal that change," without asserting the exact 2009 date range or Part B enrollment detail.

### Finding 6: Medicare Part A SNF cost-sharing for 2026 is set and dated

- Source: [CMS 2026 Medicare Parts A & B Premiums and Deductibles fact sheet](https://www.cms.gov/newsroom/fact-sheets/2026-medicare-parts-b-premiums-deductibles), released November 14, 2025 (direct fetch 403'd, known issue), corroborated by [AHA News summary](https://www.aha.org/news/headline/2025-11-17-cms-releases-details-medicare-premiums-deductibles-2026) and [medicare.tools policy summary](https://www.medicare.tools/blog/medicare-part-A/policy-changes-medicare-part-a-2026).
- What it says: for 2026, the Part A inpatient hospital deductible is $1,736 (up from $1,676 in 2025). For a Medicare-covered SNF stay following a qualifying hospital stay, days 1-20 have no coinsurance, days 21-100 cost $217/day coinsurance in 2026 (up from $209.50 in 2025), and the beneficiary pays all costs after day 100.
- Why it matters: this is the day-range and cost-sharing structure the reader needs at the fork between SNF/rehab and home. Because I could not directly fetch and confirm the CMS fact sheet itself, treat the exact dollar figures as **corroborated by two independent secondary sources citing the same CMS release date (November 14, 2025) and matching numbers, but not independently confirmed against the CMS page I could read myself.** Recommend the creator name CMS and 2026 explicitly in body text per the "no dollar figure without a named dated source" rule, and flag internally that a manual spot-check against the live CMS fact sheet (via browser, not automated fetch) is advisable before publish.

### Finding 7: Medicare home health has two gating requirements and clear, named exclusions

- Source: [National Council on Aging, "7 Things to Know About Medicare and Home Health"](https://www.ncoa.org/article/seven-things-you-should-know-about-medicares-home-health-care-benefit/), fetched directly, dated July 8, 2026.
- What it says: to qualify, the patient must be homebound (leaving home requires considerable effort or is medically inadvisable, occasional outings for medical care, religious services, or adult day care do not disqualify) and must need skilled nursing on an intermittent basis, or physical/speech/occupational therapy, under a physician-established plan of care. Covered services include skilled nursing, therapy, home health aide personal care, medical social services, durable medical equipment, and supplies. The benefit explicitly does **not** cover 24-hour care at home, delivered meals, help with shopping or cleaning, or personal-care assistance "if that's the only care you need," and does not cover long-term custodial or extended full-time nursing care.
- Why it matters: this is the exact fact that prevents the most common and costly misunderstanding this audience has (per `style/audience.md`): that "going home with home health" means the family doesn't need to arrange anything else. NCOA is an approved source and was fetched directly with a clean date — this is the strongest-sourced finding in the file.

### Finding 8: A family can raise an unsafe-discharge concern with the discharge planner and, for Medicare patients, escalate through the same BFCC-QIO appeal — there is no separate "block the discharge" legal mechanism described in approved sources

- Source: general pattern confirmed across [CANHR, "Challenging Hospital Discharge Decisions"](https://canhr.org/challenging-hospital-discharge-decisions/) and [Disability Rights California, "Hospital Discharge Rights for Medi-Cal and Medicare Recipients"](https://www.disabilityrightsca.org/publications/hospital-discharge-rights-for-medi-cal-and-medicare-recipients) (both fetched via search synthesis only, neither on the approved-source list, neither fetched directly).
- What it says: the discharge planning CoP requires hospitals to have a grievance process and to tell each patient who to contact to file one. The actionable step described consistently across sources is: tell the discharge planner and put the disagreement in writing before the patient leaves, and for a Medicare inpatient, use the IMM/BFCC-QIO fast-appeal process (Finding 2) as the formal mechanism, since that appeal keeps the patient in the hospital while it's reviewed.
- Why it matters: the reader wants to know "can I stop this." The honest, sourceable answer is: there is no separate veto power, but there is a real, time-boxed appeal mechanism (the BFCC-QIO fast appeal) plus the hospital's own grievance process. **Because the specific sources describing "hospital has a duty not to discharge to an unsafe situation" are not on the approved list (CANHR, Disability Rights CA, law-firm blogs), do not cite them by name in the post. Ground the actionable advice in the CMS discharge planning CoP and the BFCC-QIO appeal instead, both of which are traceable to CMS/Medicare.** This is a structural recommendation for the analyzer/creator, not a citation to include.

## Data points

| Stat | Value | Source | Date | Verified? |
|---|---|---|---|---|
| Part A inpatient hospital deductible | $1,736 | CMS 2026 Parts A & B fact sheet (via AHA News secondary confirmation) | Nov 14, 2025 release, for calendar year 2026 | Corroborated by 2 secondary sources; primary CMS page 403'd — flag for manual spot-check |
| SNF coinsurance, days 21-100 | $217/day | Same as above | 2026 | Same as above |
| SNF days 1-20 | $0 coinsurance | Same as above | 2026 | Same as above |
| IMM must arrive within X days of admission | within 2 calendar days | Medicare.gov (via secondary corroboration) | current | Corroborated by 2 secondary sources; primary 403'd |
| IMM second copy before discharge | no more than 2 days, no later than 4 hours before discharge | Medicare.gov (via secondary corroboration) | current | Same |
| BFCC-QIO decision turnaround | 24 hours after receiving needed info | Medicare.gov (via secondary corroboration) | current | Same |
| MOON updated notice effective date | April 21, 2026 | CMS Beneficiary Notices Initiative (via 2 provider-bulletin secondary sources) | 2026 | Corroborated, not on approved list, treat as CMS-sourced fact only |
| 3-day rule surgical waiver demonstration window | Jan 1, 2026 - Dec 31, 2030 | CMS (via secondary search synthesis) | 2026 | Unverified against primary CMS text — recommend omitting the demonstration detail or describing only in general terms |
| 30-day Medicare readmission rate | ~17.8%-19% | CMS MMRR briefs / Congressional testimony | **2012-2013 data, stale** | **UNVERIFIED for a 2026 post — do not use. No current-year primary figure found.** |

## Conflicts and disagreements

- **Medicare Advantage and the 3-day rule:** secondary consumer sites repeatedly assert MA plans "commonly waive" the 3-day rule. No primary CMS or plan-level source was found confirming this as a general practice rather than plan-by-plan variation. **What's actually true:** unresolved from sources available; safest framing is that MA plans set their own SNF coverage rules and the enrollee must check the specific plan, not assume a waiver.
- **Scope of the new observation-status appeal right:** all corroborating secondary sources agree it is limited to patients first admitted as inpatient, then reclassified to observation — not a general right to appeal an initial observation determination. No conflict found here, but flagging because it is easy to over-generalize in a blog post, and I could not verify the primary regulation text myself.

## Competitive scan

Searched broadly for "hospital discharge planning what to do parent," "hospital discharge checklist elderly parent," "discharge planning rights Medicare." The pages that surface are dominated by:
1. Law firm and elder-law blogs (Garrett Law Firm, EZ Elder Law, Burzynski Elder Law) — angle: legal rights and appeals, heavy on the IMM/BFCC-QIO mechanics, thin on the actual setting-choice decision (home vs. SNF vs. assisted living) and thin on medication reconciliation/readmission risk.
2. Consumer-finance/insurance content mills (Brevy Care, BenefitsUSA, medicare.tools) — angle: "2026 guide" SEO pages, generally accurate on dollar figures but written for a Medicare-shopping audience, not a family in a discharge crisis; no emotional or decision-fork framing.
3. Competitor-adjacent senior-living sites (Autumn Lake Healthcare, thekey.com, 24hourcaregivers.com) — angle: promotional, steering the reader toward the site's own service, exactly what ECM must not do.

Gap across all three clusters: none of them combine (a) the CMS discharge-planning entitlements, (b) the IMM/BFCC-QIO appeal mechanics, (c) the observation-vs-inpatient fork, and (d) a neutral walk through the actual post-acute setting choices, in one piece aimed at a reader with a 24-72 hour clock running. Most pick one lane (legal rights, or cost figures, or setting comparison) and stop.

## The gap

Everyone either explains the appeal rights (legal blogs) or explains the money (Medicare-shopping content) or sells a setting (senior-living marketers). Nobody walks the reader through the sequence they're actually living: get the IMM, ask about admission status, get the provider list, evaluate the setting options against the parent's actual needs, and know the one number-boxed thing they can do if the timeline feels wrong.

## Recommended angle

Structure the post as the sequence of decisions and actions in the order the reader will hit them in the next 24-72 hours, not as a topic-by-topic explainer, with observation status treated as one checkpoint in that sequence that links out to the existing post rather than re-explaining it.

## Couldn't find

- The five specific surgical procedures covered by the 2026 CMS 3-day-rule waiver demonstration. Recommend omitting or describing only in general terms.
- Direct primary-source confirmation (via a fetch I could complete myself) of the CFR citation for the discharge planning CoP, the exact IMM timing rule, the BFCC-QIO 24-hour turnaround, the 2026 SNF dollar figures, and the Barrows/Alexander eligibility language. All of medicare.gov, cms.gov, and federalregister.gov blocked automated fetch (403, consistent with the known ECM issue plus new blocks on cms.gov and federalregister.gov specifically). Each of these is corroborated by 2+ independent secondary sources with consistent numeric/factual detail, but none was independently confirmed against a primary page I could read myself. Recommend a manual (human, browser-based) spot check of the CMS 2026 fact sheet and the medicare.gov fast-appeals page before publish, given the YMYL stakes.
- A current, citable federal statistic on 30-day readmission rates among Medicare beneficiaries. The only figures found (17.8%-19%) are 2012-2013 vintage. Per the hard constraint against approximating a stale stat as current, this should be **omitted entirely** from the post rather than cited with a caveat.
- Confirmation of whether Medicare Advantage plans "commonly" waive the 3-day SNF rule, versus this varying plan-by-plan. Recommend the neutral framing above.

## Sources

Fetched directly:
- [eldercarematters.com/medicare-observation-trap/](https://eldercarematters.com/medicare-observation-trap/) — ECM, 2023/2025, existing coverage to avoid duplicating
- [NCOA, "7 Things to Know About Medicare and Home Health"](https://www.ncoa.org/article/seven-things-you-should-know-about-medicares-home-health-care-benefit/) — NCOA, July 8, 2026, primary/approved
- [Justice in Aging, Alexander v. Azar litigation summary](https://justiceinaging.org/alexander-v-azar-litigation/) — Justice in Aging, dated content circa Jan 2022, secondary
- Attempted but blocked (HTTP 403): medicare.gov/fast-appeals, medicareinteractive.org, cms.gov (two-midnight fact sheet, QSO-25-24, newsroom fact sheet), medicarerights.org, medicareadvocacy.org (two pages), federalregister.gov (direct page and PDF-via-govinfo.gov did not parse cleanly)

Read via search synthesis only (not independently fetched):
- [Kutak Rock, CMS Final Rule on Discharge Planning Requirements](https://www.kutakrock.com/newspublications/publications/2019/10/cms-final-rule-on-discharge-planning-requirements) — law firm summary, Oct 2019
- [Hall Render, Discharge Planning: Key Takeaways](https://hallrender.com/2019/10/02/discharge-planning-key-takeaways-from-the-long-awaited-final-rule/) — law firm summary, Oct 2019
- [AAPC Knowledge Center, Final Rule Revises Discharge Planning Requirements](https://www.aapc.com/blog/48915-final-rule-revises-discharge-planning-requirements/) — Oct 2019
- [Medicare Interactive, Original Medicare appeals if your care is ending](https://www.medicareinteractive.org/understanding-medicare/denials-appeals/original-medicare-appeals/original-medicare-appeals-if-your-care-is-ending)
- [NRHP Reporting, Important Message from Medicare](https://data.nrhp.org/mandated_postings/important-message-from-medicare-im/)
- [Medical News Today, Understanding Medicare's 3-midnight rule](https://www.medicalnewstoday.com/articles/3-midnight-rule-medicare)
- [Center for Medicare Advocacy, Repeal the 3-Day Hospital Stay Requirement](https://medicareadvocacy.org/repeal-the-3-day-hospital-stay-requirement-for-care-in-a-skilled-nursing-facility/)
- [Center for Medicare Advocacy, CMS Updates 'Moon' Notice](https://medicareadvocacy.org/cms-updates-moon-notice/)
- [Community Health Choice, Release of the Updated MOON](https://provider.communityhealthchoice.org/wp-content/uploads/sites/2/2026/03/Release-of-the-Updated-Medicare-Outpatient-Observation-Notice-MOON.pdf) — March 13, 2026
- [Medicare Rights Center, Final Rule Codifies Observation Stay Appeal Rights](https://www.medicarerights.org/medicare-watch/2024/10/17/final-rule-codifies-observation-stay-appeal-rights) — Oct 17, 2024
- [AHA News, CMS releases details on Medicare premiums, deductibles for 2026](https://www.aha.org/news/headline/2025-11-17-cms-releases-details-medicare-premiums-deductibles-2026) — Nov 17, 2025
- [medicare.tools, Medicare Part A 2026 Changes](https://www.medicare.tools/blog/medicare-part-A/policy-changes-medicare-part-a-2026)
- [CMS MMRR 2013 readmissions brief](https://www.cms.gov/mmrr/Briefs/B2013/mmrr-2013-003-02-b01.html) — stale data, not for use
- [CANHR, Challenging Hospital Discharge Decisions](https://canhr.org/challenging-hospital-discharge-decisions/) — not approved source, do not cite in post
- [Disability Rights California, Hospital Discharge Rights](https://www.disabilityrightsca.org/publications/hospital-discharge-rights-for-medi-cal-and-medicare-recipients) — not approved source, do not cite in post

## UNVERIFIED — explicit list for the analyzer/creator/publisher

1. **CFR citation for the discharge planning Conditions of Participation** (commonly cited elsewhere as 42 CFR 482.43) — not confirmed against regulation text I could read myself. Describe the requirement in plain language; avoid citing a section number unless separately confirmed.
2. **Exact IMM timing (2 calendar days after admission; 2 days/4 hours before discharge) and BFCC-QIO 24-hour decision turnaround** — corroborated by 2 secondary sources, medicare.gov itself returned 403. Recommend a manual browser spot-check before publish.
3. **2026 SNF cost-sharing figures ($1,736 deductible, $217/day days 21-100)** — corroborated by 2 secondary sources citing the same CMS release date; CMS page itself 403'd. Recommend a manual spot-check; per house rule, name CMS and 2026 in body text regardless.
4. **Barrows/Alexander v. Azar eligibility criteria detail** (2009 date range, Part B enrollment condition) — corroborated by 2 secondary legal sources, not confirmed against the Federal Register text itself (PDF fetch failed to parse, live page blocked automated access). Recommend a narrow, conservative description in the post rather than the precise eligibility bullet list.
5. **2026 3-day-rule surgical waiver demonstration** — cannot name the five qualifying procedures. Recommend omitting this detail entirely or describing only in the most general terms ("a narrow, procedure-specific exception").
6. **"Medicare Advantage plans commonly waive the 3-day rule"** — this is a widely repeated secondary claim with no primary confirmation found. Do not state as fact; frame as "check your specific plan's rules."
7. **30-day Medicare readmission rate** — only stale (2012-2013) data found. Per the hard constraint, omit this stat entirely rather than publish it as current.
8. **"Hospital has a duty not to discharge to an unsafe situation" / unsafe-discharge legal framing** — sourced only to non-approved advocacy/legal sites (CANHR, Disability Rights CA). Ground any "what can I do if I think this is unsafe" section in the CMS discharge-planning CoP and the BFCC-QIO appeal mechanism instead, both traceable to CMS/Medicare, and describe the hospital's grievance-process obligation rather than asserting a broader legal duty.
