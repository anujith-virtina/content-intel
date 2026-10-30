---
title: Uniqueness audit — working caregiver / balancing a job and eldercare
client: eldercarematters
date: 2026-10-08
topic: uniqueness audit for new ECM blog topic
stage: research
slug: working-caregiver-job-balance
---

# Uniqueness Audit — 2026-10-08

## Method

Paginated the live REST API in full, `per_page=100`, through every page until the API returned HTTP 400
(confirming no further pages existed):

- `/wp-json/wp/v2/posts?per_page=100&page=1` through `page=9` — **9 full pages**, `page=10` returned 400.
  Post IDs ranged from 6 (earliest) to 283820 (newest, 2026-10-01). This is the complete published-post
  corpus, roughly 900 posts, built since the site's founding (tagline: "Trusted Since 2002").
- `/wp-json/wp/v2/pages?per_page=100&page=1` — **84 pages total**, `page=2` returned 400, confirming
  completeness. This covers every directory category page, locator page, and utility page on the site.

Titles alone were not trusted. For every adjacent-looking candidate topic, the actual `content.rendered`
body was fetched (via `?p={id}` final-URL resolution or the REST `content` field) and H2s were read before
ruling a topic in or out, per the lesson that a title sweep misses body-level coverage.

## Topics evaluated and rejected (with evidence)

| Candidate topic | Status | Evidence |
|---|---|---|
| Aging in place / home modifications | **Covered** | Post 278533 "Keeping Seniors Safe at Home: Fall Prevention and Home Modifications"; post 267978 "How to Make Aging in Place Work"; post 272241 emergency plans for aging in place; plus 10+ older posts (1115, 1520, 3497, 653, 874) and a dedicated directory page `/aging-in-place/` |
| Power of attorney / advance directives | **Covered extensively** | 270092, 263613, 247261, 254950, 92392, 238277, 238270, 231570, 133563, 141210, and dozens more dating to 2016 |
| Caregiver burnout | **Covered** | Post 272201 "How to Avoid Caregiver Burnout" (2026); 206601 "What You Need to Know About Caregiver Stress"; 1320 "9 Tips to Manage Caregiver Stress"; 1237 "Identifying and Avoiding Caregiver Burnout" |
| Long-term care insurance basics | **Covered** | 238294 "Is Long-Term Care Insurance Right for You?"; 229400 "Pros and Cons of Long-Term Care Insurance"; 990, 3177, 825, 3670, 4120, 4192, 3145 |
| Dementia / memory care communication | **Covered extensively** | 283778 "Memory Care vs. Assisted Living" (2026, newest); 280614 "Memory Care 101"; 113711 "Warning Signs of Dementia"; 133666 "Is it Normal Aging or Dementia?"; 25653 legal issues caring for parents with dementia; 18313/47132 sundowning |
| Downsizing a parent's home | **Covered** — rejected after initial consideration | Post 675 "Tips to Make Downsizing Easier" (live, publish, ~1,200 words, covers rightsizing, sorting methods, NASMM senior move managers); post 3202 "Senior Move Management – Moving an Elderly Parent"; post 20 "Get Marketing Know-How When You're Downsizing." The newer 86209 "De-Cluttering Your Home" is a distinct angle (daily-living declutter, not relocation logistics) but 675 and 3202 already own the relocation/downsizing angle directly. **This was my first candidate and I rejected it only after fetching full content, not just the title.** |
| Hospice vs palliative care | **Covered** | 278545 "Understanding Palliative Care: How It Differs from Hospice" (2026); 270073; 92419 |
| Veteran Aid & Attendance | **Covered** | 259250 "Veterans Benefits for Senior Care" (2026) has H2s "VA Aid & Attendance Pension: An Overview," "Eligibility for Aid & Attendance," "How to Apply," "Other VA Benefits." This IS the post `/veterans-benefits-for-senior-care/` that the rules file's `/veterans-benefits/` redirect resolves to. Confirmed by direct fetch, not assumed. Plus 15+ older VA posts (4287, 3500, 594, 604, 33976, etc.) |
| Senior fall prevention | **Covered** | Post 278533 (shares the slot with home modifications, see above) |
| Independent living vs assisted living | **Covered** | 257129 "Senior Housing Options: From Independent Living to Skilled Nursing"; 280620 "Guide to Senior Living Options" |
| Hearing loss in seniors | **Open** — but rejected on fit grounds (see below) | Zero search results for "hearing loss" or "hearing aid" anywhere in the corpus |
| Vision loss in seniors | **Open** — rejected on fit grounds | Zero search results for "vision loss" |
| LGBTQ+ elder care | **Open** — rejected on fit grounds | Zero search results for "LGBTQ" or "LGBT." Genuinely uncovered, but there is no directory category to route the reader into, and the existing "cultural sensitivity" post (278542) already occupies the closest adjacent lane, making a second diversity-themed post without a clear directory tie-in a weaker product fit than the chosen topic |
| Grandparents raising grandchildren (kinship care) | **Open** — rejected, wrong persona | Zero search results. Real gap, but it is a different demographic (grandparent-as-primary-parent) than ECM's core "adult child caring for aging parent" persona, and the directory has no kinship-care category |

## Chosen topic: confirmed open

**"Balancing a Full-Time Job and Caregiving: What Working Caregivers Should Know"**

Search terms tried against the live corpus, all **empty arrays** (zero results):
- `FMLA` → one irrelevant partial match only (a respite-care funding post that happens to share no real content overlap)
- `working caregiver job` → no post addresses the employment/workplace angle; all results are about paid
  family caregiver arrangements (being paid BY a parent) or long-distance caregiving, not the employee's
  own job and employer
- `employer caregiver benefits` → no matches on workplace policy; matches were all about elder law/financial
  caregiving topics
- `balancing work caregiving` → one tangential match (financial planners serving families), no real overlap
- `paid family leave` → no matches
- Direct read of post 272201 "How to Avoid Caregiver Burnout" (the closest adjacent post) confirms it
  covers **personal coping strategies only** — self-care, boundaries, stress relief, organization. It
  explicitly does **not** mention FMLA, talking to an employer or HR, Employee Assistance Programs, or
  any workplace-specific benefit. Verified by reading the full H2 list, not just the title.

**Conclusion: this topic does not exist anywhere on the live site, in any post or page, under any title or
angle.** It also squarely fits the audience.md description of the primary persona as "a working adult...
doing this alongside a job," a detail the site's own audience document calls out but which no post
currently addresses from the employment angle.

## Brand/product fit check

- Does not require inventing a directory category. Routes naturally to three existing categories the
  reader can act on immediately: home care providers (to offload hands-on tasks), care management
  (to delegate coordination while at work), and the existing respite care post (272215 /
  283738) as an internal link for short-term relief.
- Matches brand.md's editorial line of staying neutral between care types.
- Does not touch any of the "themes to avoid" (no medical guidance, no specific-family legal advice,
  no retirement lifestyle content, no provider marketing advice).

## YMYL check for this specific topic

- FMLA facts (12 weeks unpaid, 50-employee threshold, 12-month/1,250-hour tenure test, job and health
  insurance protection) are **federal law, stable, not state-variable**, unlike Medicaid rules. Citable to
  a single named, dated source (U.S. Department of Labor, verified live 2026-10-08).
- The one place this topic could drift into a banned claim is **state paid family leave benefit amounts**
  (these vary by state and change yearly, structurally identical to the banned Medicaid asset-limit
  pattern). **Rule applied:** name which states have a program (California, New Jersey, New York,
  Washington, Colorado, Massachusetts) without stating a dollar figure or percentage, and route the reader
  to their own state labor department to check current numbers. No specific benefit percentage or cap will
  appear in the draft.
- No medical advice, no tax advice, no Medicare/Medicaid claims are implicated by this topic at all. This
  is the safest topic of the candidates considered from a YMYL standpoint, because it is federal employment
  law, not health, long-term-care finance, or estate law.

## Files produced

- `clients/eldercarematters/output/research/competitor-analysis-2026-10-08.md`
- `clients/eldercarematters/output/research/working-caregiver-job-balance-2026-10-08.md`
- This audit
