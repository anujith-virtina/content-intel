---
title: Research notes — Home Care Agency vs Private Caregiver: Which Is Right for Your Family
client: eldercarematters
date: 2026-09-16
topic: home care agency vs private caregiver
slug: home-care-agency-vs-private-caregiver
stage: research
---

# Research: Home Care Agency vs Private Caregiver

## Uniqueness check (required before drafting)

ECM has no `published-posts-inventory.md` (that file is a Virtina-specific reference). For ECM, uniqueness is checked against `style/examples.md`, `style/brand.md`, and the existing `output/research/` and `output/briefs/` folders, which stand in for a posts inventory since there is no single indexed file.

Findings:

- The gold-standard post 283258, "Assisted Living Vs. Home Care," compares care **settings** (in-home help vs. moving to a community). It never compares **hiring routes** within home care. No overlap.
- "How to Choose a Geriatric Care Manager" (2026-09-11) mentions home care agencies only once, inside a conflict-of-interest disclosure question ("do you have a financial relationship with any home care agency"). No overlap with hiring mechanics.
- "Who Pays for Respite Care" and "Respite Care for Family Caregivers" discuss short-term relief coverage and funding sources, not the agency-vs-private hiring decision or household-employer status. No overlap.
- "Adult Day Care vs Nursing Home" and the assisted-living-cost post are adjacent categories, not this topic.
- No existing ECM research, brief, or draft file contains the phrase "household employer," "independent contractor," or a comparison of agency vs. privately hired in-home caregivers as its main subject.

**Conclusion: this topic and angle are unique on ECM.** Recommend linking two earlier posts as internal links per section 6 of MUST-FOLLOW-RULES.md: the geriatric care manager piece (relevant to families managing complex hiring decisions) and the respite care piece (relevant to backup coverage, which is one of the biggest differences between the two hiring routes). The orchestrator should resolve exact live permalinks before drafting, per the locked rule; this researcher does not have Bash/live REST access to confirm published URLs.

## Sub-questions

1. What does an agency actually do operationally that a directly hired caregiver does not, and what does a family give up in agency fees to get it?
2. What legal and tax status does a family take on the moment they hire a caregiver directly, described in general shape only, with no rates or thresholds?
3. What happens under each model when the caregiver is sick, quits, gets hurt, or the care need escalates?
4. What screening does an agency typically perform, and what does a family hiring privately have to arrange itself?
5. How do the two routes actually compare on cost, structurally, not just per-hour?
6. What do Medicare and Medicaid pay for under each route, stated precisely and without a specific dollar figure?
7. Who is each route actually right for?

## Key findings

### Finding 1: The agency fee is buying management, not just labor

- Source: [Hiring In-Home Help](https://www.caregiver.org/resource/hiring-home-help/) — Family Caregiver Alliance
- What it says: with an agency, screening, hiring and firing, pay, and taxes are handled by the agency, and the agency provides a substitute when a worker is sick or on vacation. With a private hire, the family is responsible for all aspects of being an employer.
- Why it matters: this is the cleanest, non-commercial statement of the actual operational trade, and it comes from a nonprofit caregiving authority rather than an agency trying to sell itself.

### Finding 2: Hiring a caregiver directly generally makes the family a household employer, not a "customer"

- Source: [Hiring an In-Home Caregiver](https://www.aarp.org/caregiving/home-care/hiring-caregiver/) — AARP; and IRS, "Tax situations when taking care of a family member"
- What it says: when a family hires and directs a caregiver in their own home, supplies the tools, and the caregiver isn't independently in the business of providing care to others, the family generally takes on employer responsibilities: obtaining an employer identification number, withholding and paying payroll taxes, verifying the worker's legal eligibility to work, and in many states, carrying workers' compensation insurance. AARP is explicit that this is a package of "significant responsibilities," not a footnote.
- Why it matters: this is the single biggest thing families researching this topic get wrong. Most assume paying someone in cash or via a shared bank transfer sidesteps employment law. It generally does not. **No rate, threshold, or dollar figure from the IRS page should appear in the article** per the hard constraint; the shape of the obligation (payroll tax withholding, an EIN, work-eligibility verification, Schedule H-style annual reporting, possible state workers' comp) can be described, but every specific number is out of scope and changes yearly.

### Finding 3: Misclassifying a directly hired caregiver as an independent contractor is a named, common mistake

- Source: [Hiring an In-Home Caregiver](https://www.aarp.org/caregiving/home-care/hiring-caregiver/) — AARP; corroborated by Family Caregiver Alliance's fact sheet describing the same employer duties
- What it says: a caregiver who works in the family's home, on the family's schedule, using the family's supplies, and who does not run an independent care business, is very rarely a legitimate 1099 contractor under IRS rules. Paying by 1099 to avoid the paperwork is the mistake, not a shortcut.
- Why it matters: this needs to be stated plainly in the article, in general terms, with a pointer to a tax professional, because the consequence (back taxes, penalties) is exactly the kind of surprise this audience is trying to avoid.

### Finding 4: Federal wage and hour rules for home care workers are genuinely in flux and differ by who employs the worker

- Source: [Application of the Fair Labor Standards Act to Direct Care Workers](https://www.dol.gov/agencies/whd/direct-care) — U.S. Department of Labor
- What it says: since 2013, federal rule made minimum wage and overtime protections apply to home care workers regardless of employer, and specifically barred third-party employers (agencies) from claiming the older "companionship services" exemption. In July 2025, DOL proposed reversing that 2013 change for agencies, and in July 2025 instructed field staff to pause enforcing it. As of this writing the rule is unsettled.
- Why it matters: this is exactly the kind of thing that should be described in general terms with a "current as of publication, confirm with a professional" caveat rather than as a settled fact. It also explains why a family hiring directly and an agency can be operating under different overtime rules for what looks like the same job. [unverified: whether the 2025 proposal has been finalized by publication date; state this as in-progress, not resolved]

### Finding 5: Workers' compensation for household employees is a state-by-state requirement, not a federal one

- Source: general household-employer guidance corroborated across multiple state-specific sources; not a single primary government source with a clean national list, so this is stated only as "varies by state" per the brief's hard constraint. AARP and Family Caregiver Alliance both flag it as a required or strongly recommended coverage a private-hire family must arrange itself.
- Why it matters: an agency is already bonded and insured for this. A family that skips it and has a caregiver injured on the job can be financially exposed. No state should be named in the article.

### Finding 6: Medicare's home health benefit is narrow, skilled, and time-limited, and it is not what this article is about

- Source: [Home Health Services Coverage](https://www.ncoa.org/article/seven-things-you-should-know-about-medicares-home-health-care-benefit/) — National Council on Aging, summarizing Medicare/CMS home health rules (medicare.gov itself returns HTTP 403 to automated verification and should be named in plain text, not linked)
- What it says: Medicare pays for home health care only when a doctor certifies the person needs skilled care (nursing or therapy) on a part-time or intermittent basis, and the person is homebound under CMS criteria, meaning leaving home takes considerable effort and assistance. Medicare explicitly does not cover 24-hour care, meal delivery, or help with shopping, cleaning, or other household tasks when that is the only need.
- Why it matters: this is the single most important thing to get exactly right per the brief. Custodial, non-medical home care of the kind this article compares (agency-hired or privately hired aide help with bathing, dressing, meals, companionship) is not what Medicare's home health benefit covers, even though the two get confused constantly. Do not state a specific hours-per-week cap; NCOA's summary and CMS materials describe "part-time or intermittent" without a single clean citable number, and other hour figures found online (8 hours/day, 28-35 hours/week) trace to secondary commercial sites, not to a page this project can verify. Recommend the article state the general rule without a specific hour ceiling.

### Finding 7: Some state Medicaid programs can pay a family caregiver, but not by default and not the way most families assume

- Source: NCOA, ["Five Ways to Earn Money as a Family Caregiver"](https://www.ncoa.org/article/five-ways-family-caregivers-can-get-paid/), and general Medicaid HCBS self-direction structure (Medicaid.gov's HCBS and self-direction pages should be named in plain text; medicaid.gov could not be independently link-verified in this session, treat as medicare.gov's known 403 pattern and confirm before publish)
- What it says: most states offer some form of Medicaid self-directed or consumer-directed home and community based services, under which a qualifying person can choose, and in many states pay, a caregiver of their choosing, sometimes including a family member. This is not automatic, is not the same in every state, and does not mean a privately hired caregiver is automatically Medicaid-reimbursable.
- Why it matters: readers weighing "can Medicaid help pay if I hire privately" need the honest, general answer: sometimes, through a specific state program, never as a blanket rule, and never by simply hiring someone and billing Medicaid. Route to Medicaid.gov and a state Medicaid office in general terms. No income cap, asset limit, or look-back period stated, per the hard constraint.

### Finding 8: Cost is a structural comparison, not just a per-hour number

- Source: CareScout/Genworth Cost of Care Survey 2025 press release; CareScout/Genworth Cost of Care Survey 2024 press release
- What it says: the 2025 survey put the national median hourly rate for non-medical caregiver services at $35, up 3% year over year, translating to roughly $80,080 a year at 44 hours a week. The 2024 survey reported an annual median cost of $77,792 for home health aide services and $75,504 for homemaker services, both based on 44 hours a week, and noted that two-thirds of agencies now charge the same rate for both service types.
- Why it matters: the agency rate is a bundled number (recruiting, supervision, substitute coverage, insurance, payroll). A privately negotiated hourly wage looks lower but is unbundled: the family separately absorbs payroll tax, insurance, and the cost of its own time managing all of it. The article should say this rather than imply private hire is simply "cheaper."

### Finding 9: Screening is the other place the two routes diverge sharply

- Source: Family Caregiver Alliance, "Hiring In-Home Help"
- What it says: agencies typically run and stand behind their own background checks and credential verification as part of the service. A family hiring privately has to run its own background check, verify references directly, confirm work eligibility, and check credentials like HHA or CNA certification with the issuing body itself. FCA's plain instruction: "Always check references. Always do a background check."
- Why it matters: this is a concrete, actionable difference the article can turn into a checklist without recommending any named screening vendor, satisfying the brand rule against naming a screening company.

## Data points

| Stat | Value | Source | Date |
|------|-------|--------|------|
| National median hourly rate, non-medical in-home caregiver services | $35/hour, up 3% year over year | [CareScout/Genworth 2025 Cost of Care Survey](https://investor.genworth.com/news-events/press-releases/detail/1054/carescout-releases-2025-cost-of-care-survey-results) | 2025 |
| Annualized cost at 44 hrs/week from the 2025 median hourly rate | approx. $80,080/year | Same release, CareScout math, not separately sourced | 2025 |
| Home health aide services, national median annual cost | $77,792/year (44 hrs/week, 52 weeks), up 3% vs. 2023 | [Genworth/CareScout 2024 Cost of Care Survey](https://investor.genworth.com/news-events/press-releases/detail/982/genworth-and-carescout-release-cost-of-care-survey-results) | 2024 |
| Homemaker services, national median annual cost | $75,504/year (44 hrs/week, 52 weeks), up 10% vs. 2023 | Same 2024 release | 2024 |

Verified/unverified status:

- **Verified**: all four cost figures above. Each traces to a named, dated CareScout/Genworth primary press release, independently fetched and confirmed to say "median," not "average," matching the ECM rule.
- **Unverified, do not use**: the "8 hours/day, 28 hours/week, up to 35 hours in short medically-necessary periods" figure for Medicare skilled home health intermittent care. It appears only on commercial secondary sites (a home-care brand's guide, a Medicare-resources aggregator), not on a page this project could verify against CMS/Medicare.gov directly (which 403s). NCOA's own summary, an approved source, describes the rule as "part-time or intermittent" without giving that specific number. Recommend the article state the rule without an hours figure.
- **Unverified, do not use**: any specific IRS dollar threshold for FICA or FUTA withholding ($2,100/$1,000/$7,000-type figures). These were found directly on IRS.gov, so they are technically verified as accurate for the current tax year, but the brief's hard constraint bans stating any tax rate, dollar threshold, or wage figure regardless of verification status, because they change annually. Cut them from the draft; state only that thresholds exist and change yearly, and route the reader to a tax professional.
- **Unverified**: a claim seen on an agency-affiliated comparison site that agency clients see "95% service continuity" versus "75% for private care." This did not trace to a named primary source; it reads as an internal or marketing statistic from a home care brand. Do not use.
- **Unverified**: whether the DOL's July 2025 proposed rule reversing the 2013 companionship-exemption restriction for agencies has been finalized by publication date. Shares its only clear timeline detail with Finding 4 above; treat both facts (the proposal exists, and its status) as needing a fresh check on the day of drafting since it is a live rulemaking.

## Conflicts and disagreements

- **Position A** (agency-affiliated blogs, e.g. comfort-keepers-style franchise sites): private hire's cost advantage is straightforward, roughly 20-50% cheaper.
- **Position B** (Family Caregiver Alliance, AARP): the raw hourly comparison is misleading because it omits the family's own new costs, payroll tax, insurance, and the time cost of acting as an employer, scheduler, and backup plan.
- **What's actually true:** both are right about different things. The headline hourly number is genuinely lower for private hire. The total cost of managing that arrangement well is higher than the sticker price suggests, and most comparison content funded by either side of the market has an incentive not to say so. This is the article's honest thesis.

## Competitive scan

Top-ranking pages for this query, sampled during research (none are cited in the article; several are on ECM's competitor exclusion list and are named here only for landscape context, not for linking):

1. **Home care agencies vs. private caregivers pros and cons** — home care franchise/agency blogs (e.g. a regional home care agency site). Angle: informative on the surface, but every "con" of private hire is written to steer the reader back to booking the agency. Gap: no honest cost math, no mention of the household-employer tax exposure at all.
2. **A Place for Mom's agency-vs-private comparison** — banned competitor, not linked or named further, but its structure (checklist plus soft push toward their own referral service) is the dominant template on page one.
3. **payingforseniorcare.com's independent-caregiver comparison** — angle: neutral-sounding but ultimately promotes a private-pay caregiver matching platform. Gap: mentions taxes exist but does not explain the underlying household-employer classification or point to IRS or DOL by name.
4. **A local TV news consumer piece (1011now.com, April 2026)** — angle: genuinely neutral, "what families need to know," aimed at a general audience. Gap: light on specifics, no cost data, no mention of Medicare/Medicaid limits at all.
5. **Independent caregiver registry and comparison sites (agingtoday.com and similar)** — angle: built to promote hiring privately through their own registry. Gap: understate the employer-of-record risk, since their business model depends on families hiring directly through them.

**Shared gap across the whole field:** almost nothing on page one names the household-employer tax and wage exposure clearly and neutrally, without either scaring the reader away from private hire (agency sites) or downplaying it (registry sites). Nothing found routes the reader to both a tax professional and an elder law attorney as the two next steps. Nothing found gets the Medicare/Medicaid distinction fully right in the same piece as the hiring comparison; most either skip Medicare/Medicaid or state it too casually. This is the opening for ECM, which has no financial stake in either hiring route.

## The gap

> Every page ranking for this comparison is written by someone with a stake in one answer: an agency wants you to hire an agency, a private-caregiver registry wants you to hire privately. None of them will tell you plainly that hiring privately usually makes you a household employer with real tax and insurance obligations, point you to a tax professional and an elder law attorney in the same breath, and then let the decision genuinely go either way based on your family's situation. ECM can do that because the directory lists both.

## Recommended angle

> Frame the piece as a genuinely neutral decision guide built around what changes for the family under each route, cost structure not just cost, what happens when something goes wrong, and the household-employer obligation named clearly and routed to the two right professionals, rather than a listicle of generic pros and cons.

## Couldn't find

- A single, clean, government-sourced national number for how many hours per week Medicare's "intermittent" skilled home health benefit typically allows. NCOA describes the rule qualitatively; the specific hour figures circulating online trace to non-approved commercial sources. Recommend the article describe the rule without a specific number and direct readers to Medicare directly (named, not linked, since medicare.gov 403s automated checks).
- A single authoritative national list of exactly which states require workers' compensation for household employees. Multiple household-payroll-service sites list states, but none is a primary government source covering all fifty states in one place, and the brief bars naming a specific state's requirement anyway. State only that it varies by state.
- Confirmation of whether the DOL's July 2025 proposed FLSA rule change for home care agencies has been finalized. It was in active rulemaking as of the sources found; needs a fresh check before publication since agency/family distinctions under that rule could change.
- A primary Medicaid.gov page on self-direction and family-caregiver payment that resolves for automated verification. Medicaid.gov could not be confirmed to load cleanly in this session; treat like the known medicare.gov 403 pattern until proven otherwise, and name Medicaid in plain text rather than linking if the same block occurs at publish time.

## Sources

- [Hiring In-Home Help](https://www.caregiver.org/resource/hiring-home-help/) — Family Caregiver Alliance, fact sheet, primary, approved source
- [Hiring an In-Home Caregiver](https://www.aarp.org/caregiving/home-care/hiring-caregiver/) — AARP, primary, approved source
- [Tax situations when taking care of a family member](https://www.irs.gov/newsroom/tax-situations-when-taking-care-of-a-family-member) — IRS Newsroom, primary, approved source (used for general shape only, no figures repeated)
- [Application of the Fair Labor Standards Act to Direct Care Workers](https://www.dol.gov/agencies/whd/direct-care) — U.S. Department of Labor, primary, approved source
- [Seven Things to Know About Medicare's Home Health Care Benefit](https://www.ncoa.org/article/seven-things-you-should-know-about-medicares-home-health-care-benefit/) — National Council on Aging, primary/approved source, summarizing CMS rules
- [Five Ways Family Caregivers Can Get Paid](https://www.ncoa.org/article/five-ways-family-caregivers-can-get-paid/) — National Council on Aging, primary/approved source
- [CareScout Releases 2025 Cost of Care Survey Results](https://investor.genworth.com/news-events/press-releases/detail/1054/carescout-releases-2025-cost-of-care-survey-results) — Genworth Financial investor relations, primary, approved source, named with year
- [Genworth and CareScout Release Cost of Care Survey Results for 2024](https://investor.genworth.com/news-events/press-releases/detail/982/genworth-and-carescout-release-cost-of-care-survey-results) — Genworth Financial investor relations, primary, approved source, named with year
- Medicare.gov, "Home Health Services Coverage" — could not be fetched directly (HTTP 403 to automated requests); relied on NCOA's approved-source summary instead; name Medicare/CMS in plain text in the article, do not attempt a link
- Various agency and registry blogs (payingforseniorcare.com, agingtoday.com, comfort-keepers-style franchise sites, 1011now.com) — secondary, read for competitive landscape only, none cited or linked in the article
- A Place for Mom, Care.com — competitor sites, appeared in search results, read for landscape awareness only, never named in the article or linked
