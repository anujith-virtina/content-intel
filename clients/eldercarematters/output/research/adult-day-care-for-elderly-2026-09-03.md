---
title: Research — Adult Day Care 101: A Guide for Busy Family Caregivers
client: eldercarematters
date: 2026-09-03
topic: Adult day care for older adults, explained for family caregivers researching supervised daytime care
audience: Adult children (45-65) caring for a parent while working; informational search intent
stage: research
slug: adult-day-care-for-elderly
primary_keyword: adult day care for elderly
---

# Research notes

## 1. Uniqueness check (live corpus, fetched 2026-09-03)

Pulled all 190+ posts from `/wp/v2/posts?status=publish,draft&context=edit`. **No post on this site covers
adult day care.** The slug `adult-day-care-for-elderly` matches nothing.

Adjacent posts and how this one stays clear:

| Post | Owns | Separation |
|---|---|---|
| 272215 `/the-benefits-of-respite-care-for-family-caregivers/` (439 words) | Respite care generally. Mentions adult day 3 times, only as one bullet under "Types of Respite Care Options". | This post is the deep dive on the one option that post lists in passing. Link to it, do not restate it. |
| 272201 `/how-to-avoid-caregiver-burnout.../` | The caregiver's own health | This post is the practical service, not the emotional argument. Link from the "who it helps" section. |
| 283258 `/assisted-living-vs-home-care/` | Two residential/in-home options | Adult day care is neither. It is the daytime option that lets a parent stay at home. |
| 283684 `/how-much-does-assisted-living-cost/` | Assisted living pricing | Shares the CareScout survey but a different line item. Cross-link on cost. |
| 280614 `/memory-care-101-supporting-loved-ones-with-dementia/` (542 words, thin) | Memory care | Dementia-specialized day centers get one subsection, not a section. |

**Verdict: PASS.** Genuine gap, and it fills the site's own `Adult Day Care Services for Seniors`
category (ID 12639), which currently holds only 2 posts.

## 2. Publishing facts verified this session

- **Category ID 12639** "Adult Day Care Services for Seniors" — pulled from `/wp/v2/categories`, exact match.
- **Wordfence rate-limits hard.** A 17-URL burst returned HTTP 429 on 15 of them. Link verification had to
  be re-run with a 6-second gap between requests. Do not batch-check links against this host.

### Link targets verified 200 with no redirect (2026-09-03)

Directory category pages: `/assisted-living/`, `/home-care-providers/`, `/memory-care/`,
`/nursing-homes/`, `/elder-law-attorneys/`

Blog posts: `/the-benefits-of-respite-care-for-family-caregivers/`,
`/how-to-avoid-caregiver-burnout-.../`, `/assisted-living-vs-home-care/`,
`/how-much-does-assisted-living-cost/`, `/how-to-make-aging-in-place-work-for-your-loved-one/`,
`/veterans-benefits-for-senior-care/`, `/when-shared-caregiving-isnt-enough-...care-manager/`

### Link targets that DO NOT exist — do not link

These all return 200 but **silently redirect to the homepage**, so a naive status check passes them:

- `/adult-day-care/`
- `/adult-day-care-services-for-seniors/`
- `/adult-day-care-centers/`
- `/adult-day-services/`
- `/home-health-care/`
- `/senior-centers/`

Also redirecting (to a single post, not a directory page):
- `/veterans-benefits/` -> `/what-medical-and-pension-benefits-are-available-to-veterans/`
- `/geriatric-care-managers/` -> `/geriatric-care-managers-helping-hands-.../`

**Consequence: ECM has no adult day care directory page.** The post's main CTA cannot be "browse our adult
day care listings", because that page does not exist. The CTA routes to the Eldercare Locator (a government
service, explicitly approved in `brand.md`) for finding a local center, and into the home care and assisted
living directory pages for the adjacent decisions. This is worth raising with the client as a directory gap.

## 3. Cost data — the only figures in the post

**Source: CareScout 2025 Cost of Care Survey.** Fielded July through November 2025. Roughly 16,000 completed
surveys from 211,985 providers contacted, across all 50 states and DC, 434 regions. Of those, **608 were
adult day health care surveys**. All figures are **medians**, not averages.

| Care type | 2025 national median | Annual equivalent |
|---|---|---|
| Adult day health care | **$95 per day** | **~$24,700** at 5 days a week |
| Non-medical caregiver at home | $35 per hour | $80,080 at 44 hrs/week |
| Assisted living | $6,200 per month | $74,400 |
| Nursing home, semi-private | $9,581 per month | ~$114,972 |
| Nursing home, private | $10,798 per month | ~$129,576 |

Notable: adult day health care was the **only line item that fell**, down 5% year over year, while other
settings rose 1% to 5%. CareScout attributes this partly to Medicaid reimbursement rates acting as a price
benchmark in many markets.

The cheapest-option framing is the strongest hook available: ~$24,700 a year against $74,400 for assisted
living and $80,080 for full-time care at home. Consistent with the figures already published in post 283684.

## 4. Verified subject facts

### What it is
- Centers serve older adults with physical or cognitive needs who require supervision during the day.
  Distinct from a senior center, which serves relatively healthy older adults. (National Institute on Aging)
- **Alzheimer's Association:** "Adult day centers offer people with Alzheimer's and other dementias the
  opportunity to be social and to participate in activities in a safe environment." Some centers are
  **"open from seven to 10 hours per day"**, some with weekend or evening availability.
- Services commonly offered (Alzheimer's Association): music, art, recreation, discussion and support
  groups; personal care including toileting, eating and showering assistance; medication management and
  blood pressure checks; meals and snacks with special diets; counseling; behavior management for
  wandering and incontinence; arranged physical, occupational or speech therapy.
- Transportation to and from the center is offered by some centers, not all. (NIA)

### The three models
1. **Social** — activities, meals, supervision, some personal care
2. **Adult day health care** — the above plus skilled nursing and therapy services
3. **Dementia-specialized** — secured setting, dementia-trained staff. A minority of centers.

### Who pays
- **Medicare does not pay for adult day care.** Consistent across NIA and AARP. `medicare.gov` returns 403
  to automated requests per the client rules, so Medicare is named in plain text and not linked.
- **Medicaid** may cover it through state home and community based services (HCBS) 1915(c) waivers.
  Coverage and eligibility vary by state. No eligibility figures published; routed to an elder law attorney.
- **PACE** (Program of All-Inclusive Care for the Elderly). Medicaid.gov lists adult day care as a covered
  PACE benefit, and states that PACE "programs provide services primarily in an adult day health center."
  PACE is available to Medicaid recipients in 33 states and DC. Enrollees in PACE may not simultaneously
  use Medicaid HCBS 1915(c) waivers.
- **VA Adult Day Health Care.** "All enrolled Veterans are eligible for Adult Day Health Care IF they are
  eligible for community care and meet the clinical criteria for the service and it is available."
  A copay may apply based on service-connected disability status and financial information; VA Form 10-10EC
  determines it. Access is arranged through a VA social worker or case manager.
- **Sliding scale.** Alzheimer's Association: "Many centers offer services on sliding scales, where
  caregivers pay according to ability or income."

## 5. Stats considered and REJECTED

- **"More than half of adult day care attendees have cognitive impairment"** (AARP). Conflicts directly
  with the CDC NPALS figures below. Not used.
- **34.1% (2022) / 24.7% (2020) of adult day services participants had Alzheimer's or another dementia**
  (CDC NCHS, National Post-acute and Long-term Care Study). Traceable and dated, but (a) CDC/NCHS is not on
  this client's approved-source list in `MUST-FOLLOW-RULES.md` section 3, and (b) it contradicts the AARP
  claim above, which means the real figure depends on definitions the post cannot explain in one line.
  **Cut.** The post says qualitatively that many participants live with dementia and that a minority of
  centers are dementia-specialized, which every source agrees on.
- **"10% of centers are dementia-specialized, serving 15% of participants with dementia"** (same NPALS
  family of studies). Rejected for the same source reason. Used qualitatively as "a minority of centers".

## 6. External links (cap is 2, both used)

1. `https://www.carescout.com/cost-of-care` — CareScout 2025 Cost of Care Survey, for every dollar figure.
   Matches the house pattern in posts 283258 and 283684. Not on the competitor exclusion list.
2. `https://eldercare.acl.gov/` — Eldercare Locator, "a public service of the Administration for Community
   Living", toll-free **1-800-677-1116**. This carries the find-a-center CTA that the missing directory
   page cannot.

Named in body text but deliberately not linked, to stay under the cap: Alzheimer's Association, the VA,
Medicaid.gov, the National Institute on Aging, Medicare.

## 7. Keyword handling note

Target keyword is **"adult day care for elderly"**. `voice.md` bans "the elderly" as a noun, and the push
script blocks the literal string. The keyword is carried by the **slug**, the **Yoast title and
description**, and an H2 phrased "What Is Adult Day Care for Older Adults?". Body copy uses "older adults"
and "your parent" throughout. Exact-match keyword stuffing would break the client's voice rules, which
outrank the keyword.
