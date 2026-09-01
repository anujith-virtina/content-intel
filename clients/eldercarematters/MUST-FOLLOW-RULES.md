# ElderCareMatters Blog — Mandatory Rules (Locked Memory)

This file is the source of truth for every ECM blog. Every agent (researcher, analyzer, creator, publisher) MUST read it in full at the start of every ECM task. Established at onboarding on 2026-09-01.

## Authoritative sub-files

- `clients/eldercarematters/style/voice.md` — tone, YMYL limits, banned words, Title Case rule
- `clients/eldercarematters/style/audience.md` — the adult child, and the provider secondary persona
- `clients/eldercarematters/style/brand.md` — positioning, competitor exclusions, approved sources
- `clients/eldercarematters/style/cms.md` — verified REST details, credentials, image specs
- `clients/eldercarematters/style/examples.md` — post 283258 is the gold standard

---

## 1. REQUIRED SECTIONS — NON-NEGOTIABLE

**Locked 2026-09-01 by user instruction.** Every ECM post must contain all four of these, as explicit H2 sections, in this order:

1. **`<h2>Introduction</h2>`** — the opening. Never leave the opening paragraphs unlabeled.
2. Body sections (as many H2s as the topic needs)
3. **`<h2>People Also Ask</h2>`** — 3 to 4 Q&As, each question an H3, each answer 2 to 4 sentences
4. **`<h2>Conclusion</h2>`** — closes the argument and points into the directory
5. **`<h2>Frequently Asked Questions</h2>`** — 5 to 8 Q&As, each question an H3

Notes:
- The site's existing posts, including the otherwise excellent 283258, do **not** carry these. Do not copy that gap. This rule overrides the observed house pattern.
- PAA questions should match real search queries and must not repeat body H2s.
- FAQ answers must not restate body copy verbatim. They handle the follow-up questions the body raises.
- The publisher blocks the push if any of the four is missing.

### FAQ must be an accordion, ChatSKU style (locked 2026-09-01)

The FAQ uses collapsible `<details>` blocks styled to match the ChatSKU accordion. ECM has no page builder
and no accordion plugin, so the markup is self-contained: native `<details>`/`<summary>`, a scoped `<style>`
block, and **no JavaScript**. Values below were read off Elementor's `widget-accordion.min.css` on
chatsku.com, not estimated.

- Item border `1px solid #d5d8dc`, items stacked flush (`border-bottom:none`, last child restores it)
- Answer panel `border-top:1px solid #d5d8dc`
- **Plus icon left of the question, swapping to minus when open**, via `details[open] .ecm-plus{display:none}`
- Icon in ECM maroon `#660000`, question text `#1f333d`
- Keep the `<h3>` **inside** the `<summary>` so questions stay headings for answer engines
- **People Also Ask stays flat.** It is meant to be scanned and extracted, not clicked.

### CRITICAL: the child theme overrides post CSS with !important

`style.css` on this install carries:

```css
.single-post .entry-content h2 { font-size: 32px !important; }
.single-post .entry-content h3 { font-size: 26px !important; }
```

Any font-size set in post content **without** `!important` is silently ignored. This wasted two rounds on
post 283684: the FAQ questions kept rendering at 26px while the inline rule said 15px, and lowering the
number again changed nothing.

**Rule:** every typography declaration in an ECM post `<style>` block must carry `!important` **and**
include `.single-post .entry-content` in the selector. Pattern:

```css
.ecm-faq .ecm-q,
.single-post .entry-content .ecm-faq h3.ecm-q{font-size:15px!important;font-weight:700!important;...}
```

Body copy on this theme is 17px. FAQ type at 15px sits deliberately below it. Do not go below 15px: the
audience is adult children in their 50s and 60s, often reading on a phone.

**When something looks wrong on screen but the markup is correct, fetch the theme CSS and check for an
`!important` override before changing your own values again.**

**ECM brand colors**, sampled from the live site 2026-09-01: `#660000` primary maroon, `#008937` green,
`#1f333d` dark slate, `#2b2b2b` body text, `#d5d8dc` accordion border, `#f5f5f5` light grey.

---

## 2. STRUCTURE

1. H2 Introduction
2. Body H2s in Title Case, with H3 subsections where a section runs long
3. One comparison table when weighing two or more options
4. A numbered question list the reader can take to a tour or a call
5. A checklist before the close
6. H2 People Also Ask
7. H2 Conclusion
8. H2 Frequently Asked Questions

Length: 1,500 to 2,400 words.

---

## 3. YMYL RULES — THE HARDEST LIMITS

Elder care content covers health, legal, and financial decisions for vulnerable people. These are blocking.

- **Never claim Medicare pays for assisted living or custodial long-term care.** It does not.
- **Never publish a Medicaid asset limit, income cap, or look-back period.** They vary by state and change annually. Stating one is eligibility advice. Route the reader to a licensed elder law attorney.
- **Never give medical advice.** Explain what a care type is and what to ask. No treatments, no diagnoses.
- **Never give tax advice.** Deductibility questions go to a tax professional.
- **Never publish a cost figure without a named, dated source in the body text.**
- **Never invent a statistic.** If it cannot be traced to a primary source, cut it.
- Call survey figures **medians** when the source reports medians, never averages.

Approved sources: Medicare.gov, Medicaid.gov, CMS, National Institute on Aging, Administration for Community Living, Alzheimer's Association, VA, AARP, Family Caregiver Alliance, NCOA, CareScout cost data (name the year).

**Known issue:** medicare.gov returns HTTP 403 to every automated request. The page is not dead, it blocks bots. Do not link a URL that cannot be verified as resolving. State the fact and name Medicare in plain text instead.

---

## 4. VOICE

- **Title Case headings.** ECM is the only client in this repo that uses Title Case. Match the live site.
- Second person: "you", "your parent", "your loved one"
- Paragraphs 2 to 3 sentences. Sentences under 25 words.
- No em dashes in any form
- Banned: "the elderly" as a noun, "suffering from dementia", "placement", "facility" where "community" fits, and anything implying the reader is failing their parent
- Banned AI tells and hype as listed in `voice.md`

---

## 5. IMAGES

- Featured: **1024 x 536, WebP**. Body images: same dimensions and format.
- 2 body images per post
- Alt text 80 to 150 characters on **every** image including the featured one. The site's own posts omit featured alt text; do not copy that.
- Alt text written against the image actually chosen, never the draft's placeholder description
- `featured_media` must be a real media ID, never 0
- **Never clinical imagery.** No wheelchairs, hospital rooms, white coats, stethoscopes, or clinical settings. Assisted living is not a nursing home, and medicalised images misrepresent it and frighten the reader. Rejected on the first run of post 283684 for exactly this.
- Never nature, flowers, or landscapes
- Visual QA is mandatory. Source 6 or more candidates per slot, resize, and look at every one.

---

## 6. LINKS

- 5 to 8 internal links, pointing mainly at **directory category pages** (`/assisted-living/`, `/memory-care/`, `/home-care-providers/`, `/nursing-homes/`, `/elder-law-attorneys/`, `/veterans-benefits/`). That is the house pattern and it matches the business model.
- Link relevant existing blog posts too, but send the reader into the directory to act.
- **Maximum 2 external links.** Both need `target="_blank" rel="noopener noreferrer"`.
- Never link competitors: A Place for Mom, Caring.com, SeniorAdvisor, AgingCare, Care.com, SeniorLiving.com, Assisted Living Locators.
- Every link verified HTTP 200 before push.

---

## 7. WORDPRESS PUBLISHING

- Status always `draft`
- Endpoint `/wp-json/wp/v2/posts`, credentials `ECM_WP_USERNAME` / `ECM_WP_APP_PASSWORD` only
- **No page builder.** Plain semantic HTML into `post_content`. No Elementor, no Thrive.
- Category: pull the real ID from `/wp/v2/categories`. The taxonomy has thousands of granular terms. Never guess.
- **Yoast is NOT REST-writable on this install.** Verified on post 283684: the write returns success but the values do not persist. Attempt it, verify with `context=edit`, then report the exact strings for manual dashboard entry. Never claim Yoast is set without verifying.

---

## 8. PRE-PUBLISH CHECKLIST

**Required sections:**
- [ ] `<h2>Introduction</h2>` present
- [ ] `<h2>People Also Ask</h2>` present with 3 to 4 H3 questions
- [ ] `<h2>Conclusion</h2>` present
- [ ] `<h2>Frequently Asked Questions</h2>` present with 5 to 8 H3 questions
- [ ] FAQ rendered as `<details>` accordion, one per question, `<h3>` kept inside `<summary>`
- [ ] `<details>` / `<summary>` / `</details>` counts all match the question count

**YMYL:**
- [ ] No claim that Medicare covers assisted living or custodial care
- [ ] No Medicaid asset limit, income cap, or look-back period
- [ ] Every dollar figure has a named, dated source in body text
- [ ] Medicaid and legal questions routed to an elder law attorney

**Structure and voice:**
- [ ] All H2s Title Case
- [ ] No paragraph with 4 or more sentences
- [ ] No sentence over 25 words
- [ ] Word count 1,500 to 2,400
- [ ] Zero em dashes, zero banned words

**Images:**
- [ ] Featured set, real media ID, 1024x536 WebP
- [ ] 2 body images, 1024x536 WebP
- [ ] All three have unique 80 to 150 char alt text
- [ ] No clinical, nature, or placeholder imagery
- [ ] Every src on `https://eldercarematters.com/wp-content/uploads/`

**Links:**
- [ ] 5 to 8 internal, all 200
- [ ] 2 or fewer external, all 200, both with target and rel
- [ ] No competitor domains

**WordPress:**
- [ ] Status draft
- [ ] Real category ID
- [ ] Yoast attempted, verified, and reported for manual entry if it did not persist

---

## 9. WHEN A NEW ISSUE APPEARS

1. Add the rule to this file
2. Add the verification to the checklist in section 8
3. Add a blocking check to the push script
4. Commit immediately
