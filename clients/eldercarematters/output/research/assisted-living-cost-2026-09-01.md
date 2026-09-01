---
title: Research — How much does assisted living cost?
client: eldercarematters
date: 2026-09-01
topic: Assisted living cost, what drives it, what is excluded, and who pays
audience: Adult children pricing assisted living for a parent, often after a fall or a hospital discharge
stage: research
slug: how-much-does-assisted-living-cost
---

# Research notes

## Uniqueness check

Searched the live ECM REST API for "cost", "assisted living cost", "how much does", "price", "pay for".
**No dedicated assisted living cost post exists.** Nearest neighbours:

| Post | Date | Overlap risk | How this post stays clear |
|---|---|---|---|
| 283258 `assisted-living-vs-home-care` | 2026-08-13 | Medium. Contains a cost section. | That post decides **between two care types**. This post prices **one** of them in detail. Link to it for the comparison and do not re-argue it. **User explicitly requested this link.** |
| 261436 `hidden-costs-long-term-care-financial-preparation` | 2025-06-16 | Medium. 949 words, covers "hidden costs" and Medicare/Medicaid. | That post is general long-term care financial preparation with round illustrative figures ($3,000, $6,000, $10,000). This post is assisted living specifically, with sourced 2025 medians and pricing mechanics (base rate, care tiers, community fee). Link once, concede the planning territory. |
| 267897 `understanding-medicare-and-medicaid` | 2025-09-10 | Low | Keep the Medicare/Medicaid section short and hand off. |
| 259250 `veterans-benefits-for-senior-care` | 2025-05-14 | Low | Mention VA Aid and Attendance in one line, link the directory category. |
| 261414 `choosing-home-care-vs-assisted-living-elders` | 2025-06-06 | Low | Superseded by 283258. Do not link. |

**Verdict: PASS.** The dedicated cost query is unclaimed.

## Verified figures (only these may be used)

**Source: CareScout 2025 Cost of Care Survey** — https://www.carescout.com/cost-of-care (fetched and verified 200 on 2026-09-01)

Methodology as stated by the source: fielded July through November 2025, approximately 16,000 completed
surveys from 211,985 providers contacted, all 50 states. Assisted living communities: 4,944 surveys.
Nursing homes: 4,425. Home health: 6,014. Adult day: 608.

| Care type | 2025 national median |
|---|---|
| Assisted living | **$6,200 / month**, $74,400 / year |
| Non-medical caregiver at home | $35 / hour, $80,080 / year at 44 hrs/week |
| Skilled nursing at home | $90 / hour |
| Adult day health care | $95 / day |
| Nursing home, semi-private room | $315 / day, $114,975 / year |
| Nursing home, private room | $355 / day, $129,575 / year |

**Rules for using these:** always attach the year and the source name in body text. Always call them
**medians, not averages**, because that is what the survey reports. Never present a median as what the
reader will pay.

## Coverage facts

**Medicare does not pay for assisted living.** Medicare covers medically necessary care, including a
limited skilled nursing facility stay after a qualifying hospital admission. It does not cover custodial
long-term care, and it does not cover room and board in an assisted living community.

**Link discipline:** medicare.gov returns **HTTP 403 to every automated request**, tested with full
browser headers on 2026-09-01. The page is not dead, it blocks bots. Since the link cannot be verified as
resolving, **do not link it.** State the fact and name Medicare in plain text instead. Same discipline as
the Gartner stat on ChatSKU post 294.

**Medicaid may pay for the care services in assisted living, never the room and board.** Coverage runs
through state HCBS waivers, so it varies by state. Some states do not fund assisted living through
Medicaid at all. Income limits differ by state and change annually.

Source: NCOA, "Does Medicaid Pay for Assisted Living?" — https://www.ncoa.org/article/does-medicaid-pay-for-assisted-living/ (verified 200).

**Do not** publish a specific state income limit or asset figure. They change annually and vary by state,
and quoting one would be giving eligibility advice. Point the reader to an elder law attorney.

## Rejected

- Any "average cost" phrasing. The survey reports medians.
- State-by-state cost tables from commercial senior-living directories. Those are competitors under
  `brand.md` and their methodology is not published.
- Any Medicaid asset limit, look-back period, or income cap. Varies by state, changes yearly, and stating
  one is legal advice.
- Any claim that a specific community type is a better financial choice. The directory lists all of them.

## Pricing mechanics to explain (the actual value of this post)

Competitors publish a national median and stop. The mechanics are what families get wrong:

1. **Base rate plus care level.** Most communities quote rent and then add a care tier priced separately,
   often several hundred to over a thousand dollars a month.
2. **Care level is reassessed.** A tier can be raised after a fall or a change in medication, mid-stay.
3. **Community fee.** A one-time move-in fee, commonly one to two months of rent, usually non-refundable.
4. **Annual increases.** Rates typically rise every year, independent of any care-level change.
5. **Second person fee** when a couple shares an apartment.
6. **Excluded extras.** Incontinence supplies, medication management, two-person transfers, escorts to
   meals, salon, transport.

## Semantic terms to cover

assisted living, memory care, custodial care, activities of daily living (ADLs), level of care, community
fee, base rate, tiered pricing, all-inclusive pricing, HCBS waiver, room and board, long-term care
insurance, VA Aid and Attendance, skilled nursing facility, respite care

## Internal links (all verified 200 on 2026-09-01)

- `/assisted-living-vs-home-care/` — **required by the user**
- `/hidden-costs-long-term-care-financial-preparation/` — the planning companion
- `/assisted-living/` — directory category
- `/nursing-homes/` — directory category
- `/home-care-providers/` — directory category
- `/elder-law-attorneys/` — directory category, for Medicaid planning
- `/veterans-benefits/` — directory category, for Aid and Attendance

## Format

Match post 283258: 1,500 to 1,800 words, Title Case H2s, one comparison table, numbered questions to take
to a tour, a checklist before the close, and a final section that answers the title question directly.
